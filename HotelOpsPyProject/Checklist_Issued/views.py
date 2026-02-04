from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
# Create your views here.
from .models import HREmployeeChecklistMaster,HREmployeeChecklist_Entry,HREmployeeChecklist_Details
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from HumanResources.views import EmployeeDetailsData
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from django.urls import reverse

from django.template.loader import render_to_string, get_template
from django.http import JsonResponse, HttpResponse
from xhtml2pdf import pisa  
from datetime import datetime
from django.utils import timezone  
from app.models import OrganizationMaster

from django.db import transaction
from app.models import EmployeeMaster
from HumanResources.models import EmployeeWorkDetails, EmployeePersonalDetails, EmployeeDocumentsInformationDetails, EmployeeQualificationDetails  
from InterviewAssessment.models import Assessment_Master
import threading
from app.Global_Api import Get_Employee_Master_Data_By_Code


def Checklistadd(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID = str(request.session.get("UserID"))
    checkemps = HREmployeeChecklistMaster.objects.filter(IsDelete=False)
    
    checkemp = None  
    checklist_entry_id = request.GET.get('ID')  
    EmpID = request.GET.get('EmpID')
    
    
    EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
    check_instance = {
        'EmployeeCode': EmpDetails.EmployeeCode,
        'EmpName': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
        'Department': EmpDetails.Department,
        'Designation': EmpDetails.Designation,
        'DateofJoining' : EmpDetails.DateofJoining,
        'OrganizationID':EmpDetails.OrganizationID,
    }
    
    if checklist_entry_id:
        try:
            checkemp = HREmployeeChecklist_Entry.objects.get(id=checklist_entry_id,OrganizationID=OrganizationID,IsDelete=False)

            for cl in checkemps:
                    cl.ReceivedStatus = 0
                    clearance_items = HREmployeeChecklist_Details.objects.filter(HREmployeeChecklist_Entry=checkemp,HREmployeeChecklistMaster=cl)
                    if clearance_items.exists():
                        cl.ReceivedStatus =  clearance_items[0].ReceivedStatus
        except HREmployeeChecklist_Entry.DoesNotExist:
            checkemp = None  

    if request.method == "POST":
        EmpCode = request.POST.get('EmpCode')
        Name = request.POST.get('Name')
        Department = request.POST.get('Department')
        Designtions = request.POST.get('Designtions')

       
        if checkemp:
            checkemp.EmpCode = EmpCode
            checkemp.Name = Name
            checkemp.Department = Department
            checkemp.Designtions = Designtions
            checkemp.ModifyBy = UserID
            checkemp.save()
        else:
            checkemp = HREmployeeChecklist_Entry.objects.create(
                EmpCode=EmpCode, Name=Name, Department=Department, Designtions=Designtions,
                OrganizationID=OrganizationID, CreatedBy=UserID
            )

        
        TotalChecklist = int(request.POST.get("TotalChecklist", 0))
        for i in range(TotalChecklist + 1):
            checkemps_key = f"checkemps_ID_{i}"
            checkemps_value = request.POST.get(checkemps_key)

            if not checkemps_value:
                print(f"No checklist ID found for {checkemps_key}, skipping.")
                continue

            try:
                returndat = HREmployeeChecklistMaster.objects.get(id=checkemps_value)
            except HREmployeeChecklistMaster.DoesNotExist:
                print(f"ChecklistMaster with id {checkemps_value} does not exist, skipping.")
                continue

            ReceivedStatus_key = f"ReceivedStatus_{i}"
            ReceivedStatus_value = request.POST.get(ReceivedStatus_key, 0)

            
            HREmployeeChecklist_Details.objects.update_or_create(
                HREmployeeChecklistMaster=returndat,
                HREmployeeChecklist_Entry=checkemp,
                defaults={'ReceivedStatus': ReceivedStatus_value}
            )

        
        Success = True
        encrypted_id = encrypt_id(EmpID)  
        url = reverse('Checklist')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}"
        return redirect(redirect_url)  

    
    
    context = {
        'checkemps': checkemps,
        'checkemp': checkemp,
        'check_instance':check_instance  
    }
    return render(request, 'Checklist/Checklistadd.html', context)


def Checklistshow(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = str(request.session.get("UserID"))

    checkempdata = HREmployeeChecklist_Entry.objects.filter(OrganizationID=OrganizationID,IsDelete=False)

    context = {'checkempdata': checkempdata}
    return render(request, 'Checklist/Checklistshow.html', context)


def EmpChecklist(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    EmpID  = request.GET.get('EmpID')
    cle=HREmployeeChecklist_Entry.objects.get(id=id)
    cle.IsDelete=True
    cle.ModifyBy=UserID
    cle.save()

    
    Success = 'Deleted'        
    encrypted_id = encrypt_id(EmpID)
    url = reverse('Checklist')  
    redirect_url = f"{url}?EmpID={encrypted_id}&Success={Success}" 
    return redirect(redirect_url) 


def ChecklistView(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID = str(request.session.get("UserID"))

    id = request.GET.get('ID')
    
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    check = get_object_or_404(HREmployeeChecklist_Entry, id=id)
    checkemps = HREmployeeChecklistMaster.objects.filter(IsDelete=False)

    checkempsdetalis = HREmployeeChecklist_Details.objects.filter(IsDelete=False,HREmployeeChecklist_Entry=check)
    template_path = 'Checklist/ChecklistView.html'
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    
    context = {
       'check':check,"checkemps":checkemps,"checkempsdetalis":checkempsdetalis,"current_datetime":current_datetime,"organization_logos":organization_logos,'organization_logo':organization_logo,
        
    }
   
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Report.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
   
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


from LETTEROFAPPOINTMENT.models import LOALETTEROFAPPOINTMENTEmployeeDetail

# New Function:

# def create_initial_checklist_entry(EmpCode, OrganizationID, UserID):
    
#     print(f"We are here at create_initial_checklist_entry and the parameters are there, EmpCode: {EmpCode}, OrganizationID={OrganizationID}, UserID = {UserID}")
#     EmpDetails = Get_Employee_Master_Data_By_Code(EmpCode, OrganizationID)
    
#     entry = HREmployeeChecklist_Entry.objects.create(
#         EmpCode =  EmpDetails.EmployeeCode,
#         Name =  EmpDetails.EmpName,
#         Department =  EmpDetails.Department,
#         Designtions =  EmpDetails.Designation,
#         OrganizationID = EmpDetails.OrganizationID,
#     )
#     if entry:
#         LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
#             emp_code=EmpCode,
#             OrganizationID=OrganizationID,
#             IsDelete=False
#         ).update(IsChecklist_Created=True)
        

#         # Create default detail rows
#         masters = HREmployeeChecklistMaster.objects.filter(IsDelete=False)
#         for m in masters:
#             HREmployeeChecklist_Details.objects.create(
#                 HREmployeeChecklistMaster=m,
#                 HREmployeeChecklist_Entry=entry,
#                 ReceivedStatus=0
#             )
            
#         Object_Id = 1
#         # Update or create the detail row
#         HREmployeeChecklist_Details.objects.update_or_create(
#             HREmployeeChecklistMaster_id=Object_Id,
#             HREmployeeChecklist_Entry=entry,
#             defaults={"ReceivedStatus": 1}
#         )

#         return entry



@transaction.atomic
def create_initial_checklist_entry(EmpCode, OrganizationID, UserID):

    print(
        f"We are here at create_initial_checklist_entry | "
        f"EmpCode={EmpCode}, OrganizationID={OrganizationID}, UserID={UserID}"
    )

    EmpDetails = Get_Employee_Master_Data_By_Code(EmpCode, OrganizationID)
    if not EmpDetails:
        return None

    entry = HREmployeeChecklist_Entry.objects.create(
        EmpCode=EmpDetails.EmployeeCode,
        Name=EmpDetails.EmpName,
        Department=EmpDetails.Department,
        Designtions=EmpDetails.Designation,
        OrganizationID=EmpDetails.OrganizationID,
    )

    LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
        emp_code=EmpCode,
        OrganizationID=OrganizationID,
        IsDelete=False
    ).update(IsChecklist_Created=True)

    masters = HREmployeeChecklistMaster.objects.filter(IsDelete=False)

    for m in masters:
        HREmployeeChecklist_Details.objects.create(
            HREmployeeChecklistMaster=m,
            HREmployeeChecklist_Entry=entry,
            ReceivedStatus=1 if m.id == 1 else 0
        )

    return entry



def update_checklist_entry(EmpCode, OID, Data_Id, UserID):

    print(f"We are here at create_initial_checklist_entry and the parameters are EmpCode={EmpCode}, OrganizationID={OID}, UserID={UserID}")

    # Get the entry object
    entry = HREmployeeChecklist_Entry.objects.filter(
        EmpCode=EmpCode, 
        OrganizationID=OID, 
        IsDelete=False
    ).first()

    if not entry:
        print("No entry found. Cannot update.")
        return False

    # Update or create the detail row
    HREmployeeChecklist_Details.objects.update_or_create(
        HREmployeeChecklistMaster_id=Data_Id,
        HREmployeeChecklist_Entry=entry,
        defaults={"ReceivedStatus": 1}
    )
    # Object_Id = 1
    # # Update or create the detail row
    # HREmployeeChecklist_Details.objects.update_or_create(
    #     HREmployeeChecklistMaster_id=Object_Id,
    #     HREmployeeChecklist_Entry=entry,
    #     defaults={"ReceivedStatus": 1}
    # )

    return True



# This Function is move to HR View's.py 


def run_background_checklist_tasks_with_creatiion(EmpCode, OrganizationID, UserID):
    def task():
        create_initial_checklist_entry(EmpCode, OrganizationID, UserID)
        update_checklist_entry(EmpCode, OrganizationID, 30, UserID)       # Appointment Letter
        update_checklist_entry_particular_field(EmpCode, OrganizationID, UserID)

    thread = threading.Thread(target=task)
    thread.daemon = True
    thread.start()

def run_background_checklist_tasks(EmpCode,OID, Object_ID, UserID):
    def task():
        update_checklist_entry(EmpCode, OID, Object_ID, UserID)

    thread = threading.Thread(target=task)
    thread.daemon = True
    thread.start()

def run_background_checklist_tasks_Employee_ID(EmpID,OID, UserID):
    def task():
        update_checklist_entry_particular_field_By_EmpID(EmpID, OID, UserID)

    thread = threading.Thread(target=task)
    thread.daemon = True
    thread.start()





def update_checklist_entry_particular_field(EmpCode, OID, UserID):

    Emp_Personal = EmployeePersonalDetails.objects.filter(
        EmployeeCode=EmpCode,
        OrganizationID=OID,
        IsDelete=False
    ).only('EmpID','ProfileImageFileTitle','ProfileImageFileName', 'InterviewAssessmentID').first()

    if not Emp_Personal:
        return False

    Emp_Work = EmployeeWorkDetails.objects.filter(
        EmpID=Emp_Personal.EmpID,
        OrganizationID=OID,
        IsDelete=False
    ).values('Locker').first()

    Emp_Docs = EmployeeDocumentsInformationDetails.objects.filter(
        EmpID=Emp_Personal.EmpID,
        OrganizationID=OID,
        IsDelete=False
    ).values('Title')

    entry = HREmployeeChecklist_Entry.objects.filter(
        EmpCode=EmpCode, 
        OrganizationID=OID, 
        IsDelete=False
    ).first()

    if not entry:
        return False


    if Emp_Work and Emp_Work.get("Locker") == "Yes":
        object_id = 32      # Lockers
        HREmployeeChecklist_Details.objects.update_or_create(
            HREmployeeChecklistMaster_id=object_id,
            HREmployeeChecklist_Entry=entry,
            defaults={"ReceivedStatus": 1, "ModifyBy": UserID}
        )

    if Emp_Personal.ProfileImageFileName and Emp_Personal.ProfileImageFileTitle:
        object_id = 26      # Photos
        HREmployeeChecklist_Details.objects.update_or_create(
            HREmployeeChecklistMaster_id=object_id,
            HREmployeeChecklist_Entry=entry,
            defaults={"ReceivedStatus": 1, "ModifyBy": UserID}
        )
        
    if Emp_Personal.InterviewAssessmentID and Emp_Personal.InterviewAssessmentID != 0:
        # AssessmentMaster = Assessment_Master.objects.filter
        
        AssessmentMaster = Assessment_Master.objects.filter(
            id=Emp_Personal.InterviewAssessmentID,
            IsDelete=False
        ).only('LOIStatus','reference').first()
        
        
        if AssessmentMaster:
            if AssessmentMaster.LOIStatus == 'Accepted':
                object_id = 21      # Letter of Intent
                HREmployeeChecklist_Details.objects.update_or_create(
                    HREmployeeChecklistMaster_id=object_id,
                    HREmployeeChecklist_Entry=entry,
                    defaults={"ReceivedStatus": 1, "ModifyBy": UserID}
                )
                
            if AssessmentMaster.reference:   
                object_id = 3       # Reference Checks
                HREmployeeChecklist_Details.objects.update_or_create(
                    HREmployeeChecklistMaster_id=object_id,
                    HREmployeeChecklist_Entry=entry,
                    defaults={"ReceivedStatus": 1, "ModifyBy": UserID}
                )

    doc_titles = {doc["Title"].strip().lower() for doc in Emp_Docs if doc.get("Title")}
    # object_id_one = 54
    # object_id_two = 55
    # object_id_three = 2
    # object_id_Medical = 18
    # object_id_PF_Form = 57
    # object_id_Professional = 52
    # object_id_Esic = 58
    
    object_id_one = 24          # Aadhar Card
    object_id_two = 25          # PAN Card
    object_id_three = 2
    object_id_Medical = 18
    object_id_PF_Form = 27      # PF Form 11
    object_id_Professional = 22 # Professional Certificates
    object_id_Esic = 28         # ESI Form

    doc_map = {
        "aadhaar card": object_id_one,
        "pan card": object_id_two,
        "resume": object_id_three,
        "medical fitness certificate": object_id_Medical,
        "pf form 11": object_id_PF_Form,
        "Professional Certificates": object_id_Professional,
        "esic form": object_id_Esic,
    }

    for title, master_id in doc_map.items():
        if title in doc_titles:
            HREmployeeChecklist_Details.objects.update_or_create(
                HREmployeeChecklistMaster_id=master_id,
                HREmployeeChecklist_Entry=entry,
                defaults={"ReceivedStatus": 1, "ModifyBy": UserID}
            )

    return True

def update_checklist_entry_particular_field_By_EmpID(EmpID, OID, UserID):

    Emp_Personal = EmployeePersonalDetails.objects.filter(
        EmpID=EmpID,
        OrganizationID=OID,
        IsDelete=False
    ).only('EmpID','EmployeeCode','ProfileImageFileTitle','ProfileImageFileName').first()

    if not Emp_Personal:
        return False
    
    EmpCode = Emp_Personal.EmployeeCode

    Emp_Work = EmployeeWorkDetails.objects.filter(
        EmpID=Emp_Personal.EmpID,
        OrganizationID=OID,
        IsDelete=False
    ).values('Locker').first()

    Emp_Docs = EmployeeDocumentsInformationDetails.objects.filter(
        EmpID=Emp_Personal.EmpID,
        OrganizationID=OID,
        IsDelete=False
    ).values('Title')

    Emp_Qualification = EmployeeQualificationDetails.objects.filter(
        EmpID=Emp_Personal.EmpID,
        OrganizationID=OID,
        IsDelete=False
    ).values('EducationType')

    entry = HREmployeeChecklist_Entry.objects.filter(
        EmpCode=EmpCode, 
        OrganizationID=OID, 
        IsDelete=False
    ).first()

    if not entry:
        return False

    if Emp_Work and Emp_Work.get("Locker") == "Yes":
        # print("Locker:", Emp_Work.get("Locker"))
        object_id = 32                # Lockers
        HREmployeeChecklist_Details.objects.update_or_create(
            HREmployeeChecklistMaster_id=object_id,
            HREmployeeChecklist_Entry=entry,
            defaults={"ReceivedStatus": 1, "ModifyBy": UserID}
        )

    if Emp_Personal.ProfileImageFileName and Emp_Personal.ProfileImageFileTitle:
        object_id = 26              # Photos
        HREmployeeChecklist_Details.objects.update_or_create(
            HREmployeeChecklistMaster_id=object_id,
            HREmployeeChecklist_Entry=entry,
            defaults={"ReceivedStatus": 1, "ModifyBy": UserID}
        )

    doc_titles = {doc["Title"].strip().lower() for doc in Emp_Docs if doc.get("Title")}
    object_id_one = 24          # Aadhar Card
    object_id_two = 25          # PAN Card
    object_id_three = 2
    object_id_Medical = 18
    object_id_PF_Form = 27      # PF Form 11
    object_id_Professional = 22 # Professional Certificates
    object_id_Esic = 28         # ESI Form

    doc_map = {
        "aadhaar card": object_id_one,
        "pan card": object_id_two,
        "resume": object_id_three,
        "medical fitness certificate": object_id_Medical,
        "pf form 11": object_id_PF_Form,
        "Professional Certificates": object_id_Professional,
        "esic form": object_id_Esic,
    }

    for title, master_id in doc_map.items():
        if title in doc_titles:
            HREmployeeChecklist_Details.objects.update_or_create(
                HREmployeeChecklistMaster_id=master_id,
                HREmployeeChecklist_Entry=entry,
                defaults={"ReceivedStatus": 1, "ModifyBy": UserID}
            )

    Qual_titles = {Qual["EducationType"].strip().lower() for Qual in Emp_Qualification if Qual.get("EducationType")}
    object_id = 23    # Educational Certificates

    Qual_Data = {
        "secondary": object_id,
        "higher secondary": object_id,
        "graduation": object_id,
        "post graduation": object_id,
    }

    for title in Qual_titles:
        if title in Qual_Data:
            HREmployeeChecklist_Details.objects.update_or_create(
                HREmployeeChecklistMaster_id=Qual_Data[title],
                HREmployeeChecklist_Entry=entry,
                defaults={
                    "ReceivedStatus": 1,
                    "ModifyBy": UserID
                }
            )

    return True
