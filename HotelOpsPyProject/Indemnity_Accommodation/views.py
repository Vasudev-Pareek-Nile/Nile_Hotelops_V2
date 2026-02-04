from django.shortcuts import render,redirect
from .models import *
# Create your views here.
from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail
import io ,os
from django.utils import timezone
# Azure.
from hashlib import new
from pathlib import Path
import mimetypes
from django.contrib import messages
from .azure import upload_file_to_blob,ALLOWED_EXTENTIONS,download_blob
# Azure.

from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse,Http404
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from .models import Indemnity_Accommodation_Employee_Detail,Indemnity_Accommodation_Deleted_File_Of_Employee
from django.shortcuts import render,redirect
from xhtml2pdf import pisa
from django.template.loader import get_template


from HumanResources.views import ManagerNameandDesignation,HrManagerNameandDesignation,EmployeeDetailsData,HrNameOnTheBasisofDesignation,EmployeeNameOnTheBasisofDesignation
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from django.urls import reverse
from HumanResources.models import EmployeePersonalDetails
from Policy_Data_Privacy.models import Letter_Data_Item_Master, Letter_Editor 

def Indemnity_Accommodation_Entry_Emp(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID   
    UserID = str(request.session["UserID"])
    EmpCode = request.GET.get('EC')
    EmpID = request.GET.get('EmpID')
    LOE_ID = request.GET.get('LOE_ID')
    Page  = request.GET.get('Page')

    DepartmentName = request.GET.get('DepartmentName')
    DepartmentName = request.GET.get('DepartmentName')


    ManagerNames =  EmployeeNameOnTheBasisofDesignation( DepartmentName,OrganizationID)
    HRManagerNames  = HrNameOnTheBasisofDesignation(OrganizationID)
 

    Experienceobj = None

    if EmpCode is not None:
        if LOE_ID is not None:
            Experienceobj = Indemnity_Accommodation_Employee_Detail.objects.filter(id=LOE_ID, emp_code=EmpCode, OrganizationID=OrganizationID, IsDelete=False).first()
        else:
            Experienceobj = Indemnity_Accommodation_Employee_Detail.objects.filter(emp_code=EmpCode, OrganizationID=OrganizationID, IsDelete=False).first()

        if Experienceobj is not None:
            DataFromExperienceobj = 'Experienceobj'
        else:
            DataFromExperienceobj = 'ExperienceobjHR'
            EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
            Experienceobj = {
                'emp_code': EmpDetails.EmployeeCode,
                'prefix': EmpDetails.Prefix,
               'first_name': (EmpDetails.FirstName + " " + EmpDetails.MiddleName) if EmpDetails.MiddleName else EmpDetails.FirstName,
 
                'last_name': EmpDetails.LastName,
                'date_of_joining': EmpDetails.DateofJoining,
                'department': EmpDetails.Department,
                'designation': EmpDetails.Designation,
            }

    if request.method == "POST":
        # Retrieve form data
        emp_code = request.POST['emp_code']
        prefix = request.POST['prefix']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        generate_date = request.POST['generate_date']
        date_of_joining = request.POST['date_of_joining']
        date_of_last_working = request.POST.get('date_of_last_working')  # Optional
        department = request.POST['department']
        designation = request.POST['designation']
        Hr_Name = request.POST['Hr_Name']
        Hr_Designation = request.POST['Hr_Designation']

        # Update existing record or create a new one
        if DataFromExperienceobj == "Experienceobj" and LOE_ID:
            Experienceobj.emp_code = emp_code
            Experienceobj.prefix = prefix
            Experienceobj.first_name = first_name
            Experienceobj.last_name = last_name
            Experienceobj.generate_date = generate_date
            Experienceobj.date_of_joining = date_of_joining
            Experienceobj.date_of_last_working = date_of_last_working
            Experienceobj.department = department
            Experienceobj.designation = designation
            Experienceobj.Hr_Name = Hr_Name
            Experienceobj.Hr_Designation = Hr_Designation
            Experienceobj.ModifyBy = UserID
            Experienceobj.save()

        else:
            Experienceobj = Indemnity_Accommodation_Employee_Detail.objects.create(
                emp_code=emp_code,
                prefix=prefix,
                first_name=first_name,
                last_name=last_name,
                generate_date=generate_date,
                date_of_joining=date_of_joining,
                date_of_last_working=date_of_last_working,
                department=department,
                designation=designation,
                Hr_Name=Hr_Name,
                Hr_Designation=Hr_Designation,
                CreatedBy=UserID,
                OrganizationID=OrganizationID
            )
            
        if Page == 'Indemnity_Accommodation_Emp_List':
            return redirect('Indemnity_Accommodation_Emp_List')

        # Redirect with success message
        Success = True
        encrypted_id = encrypt_id(EmpID)
        url = reverse('EmployeeLetters')
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}"
        return redirect(redirect_url)
    context = {'Experienceobj': Experienceobj, 'ManagerNames': ManagerNames, 'HRManagerNames': HRManagerNames}
    return render(request, "Indemnity_Accommodation/Entry_Emp.html", context)



from django.db.models import Subquery, OuterRef
from app.views import OrganizationList
def Indemnity_Accommodation_Emp_List(request):
 
    if 'OrganizationID' not in request.session:

        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    UserType = request.session.get("UserType")

    OrganizationID =request.session["OrganizationID"]
    memOrg = OrganizationList(OrganizationID)  


    
    I = request.GET.get('I',OrganizationID)
    
    if UserType == 'CEO' and request.GET.get('I') is None:
        I = 401
    
    emp_id_subquery = Subquery(
        EmployeePersonalDetails.objects.filter(
            EmployeeCode=OuterRef('emp_code'),
            IsDelete=False
        ).values('EmpID')[:1]
        )

    ExperienceLetters = Indemnity_Accommodation_Employee_Detail.objects.filter(IsDelete=False,OrganizationID= I).annotate(
        EmpID=emp_id_subquery
    ).order_by('-CreatedDateTime','-ModifyDateTime').values()
    context  = { 
        'ExperienceLetters':ExperienceLetters,
        'I':I,
        'memOrg':memOrg
    }
    return render(request,"Indemnity_Accommodation/Emp_ListPage.html",context)

# For generate_appointment_letter
def Generate_Letter_of_Indemnity_Accommodation(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    id = request.GET.get("LOE_ID")
    OID = request.GET.get("OID")
    emp = Indemnity_Accommodation_Employee_Detail.objects.get(id=id)
    policy = Letter_Editor.objects.filter(OrganizationID=OID, IsDelete=False, Letter_Data_Item_Master_id=3).first()
    

    # Organization Details
    od = OrganizationDetail(emp.OrganizationID)
    hotel_name = od.get_Organization_name()
    OLogo = od.get_OrganizationLogo()
    NileLogo = MasterAttribute.NileLogoURL if od.get_MComLogo() == 1 else ""

    header = ""
    head = request.GET.get("head", "true")
    if str(head).lower() == "true":
        header = f"""
            <table class='header-table'>
                <tr>
                    <td align='left'><img width="100px" height="100px" src='{OLogo}'></td>
                    <td></td>
                    <td align='right'><img width="100px" height="100px" src='{NileLogo}'></td>
                </tr>
            </table>
        """

    context = {
        "Ed": emp,
        "header": header,
        "HotelName": hotel_name,
        "policy_html": policy.content if policy else "",
    }

    template = get_template("Indemnity_Accommodation/Letter_Of_Indemnity_Accommodation.html")
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Trainee_Experience_Letter.pdf"'

    result = BytesIO()
    pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    return HttpResponse(result.getvalue(), content_type="application/pdf")




def Indemnity_Accommodation_Emp_Delete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID =request.session["OrganizationID"]
        OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID   
    UserID =str(request.session["UserID"])
    EmpID = request.GET.get('EmpID')
    id = request.GET.get('LOE_ID') 
    empdetail = Indemnity_Accommodation_Employee_Detail.objects.get(id=id)
    empdetail.IsDelete=True
    empdetail.ModifyBy = UserID
    empdetail.save()
    Success = 'Deleted'        
    encrypted_id = encrypt_id(EmpID)
    url = reverse('EmployeeLetters')  
    redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
    return redirect(redirect_url)




def Indemnity_Accommodation_Upload_File(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID =request.session["OrganizationID"]
        OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID   
    EmpID = request.GET.get('EmpID')
    Page  = request.GET.get('Page')
    id = request.GET.get('LOE_ID')    
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix

        new_file = upload_file_to_blob(file,id)
        if not new_file:
            messages.warning(request, f"{ext} not allowed only accept {', '.join(ext.lower()for ext in ALLOWED_EXTENTIONS)} ")
            return render(request, "letterofexp/upload_file.html", {}) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()
        if Page == 'Indemnity_Accommodation_Emp_List':
            return redirect('Indemnity_Accommodation_Emp_List')
      
        Success = 'Uploaded'        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('EmployeeLetters')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
        return redirect(redirect_url)
    
    
    return render(request, "Indemnity_Accommodation/Upload_File.html")


def Indemnity_Accommodation_Download_File(request):
    id = request.GET.get('LOE_ID')
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID   
    file = Indemnity_Accommodation_Employee_Detail.objects.get(pk=id)
    file_id = file.file_id
    file_name = file.file_name
    
    file_type, _ = mimetypes.guess_type(file_id)
    
    
    blob_name = file_id
    blob_content = download_blob(blob_name)
    
    if blob_content:
        response = HttpResponse(blob_content.readall(), content_type=file_type)
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        messages.success(request, f"{file_name} was successfully downloaded")
        return response
    return Http404


def Indemnity_Accommodation_Repalce_File(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
        OrganizationID =request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    Page  = request.GET.get('Page')
    if OID:
            OrganizationID= OID   
    UserID =str(request.session["UserID"])
    EmpID = request.GET.get('EmpID')
    id = request.GET.get('LOE_ID')     
    file = Indemnity_Accommodation_Employee_Detail.objects.get(pk=id)
    file_id = file.file_id
    file_name = file.file_name
    EmployeeDetail = Indemnity_Accommodation_Employee_Detail.objects.get(pk=id)
    
    
    deletefile = Indemnity_Accommodation_Deleted_File_Of_Employee.objects.create(Indemnity_Accommodation_Employee_Detail= EmployeeDetail,file_id = file_id,file_name = file_name)

    file = Indemnity_Accommodation_Employee_Detail.objects.get(pk=id)
    file.file_name = None
    file.file_id = None
    file.ModifyBy = UserID
    file.save()
    if Page == 'Indemnity_Accommodation_Emp_List':
        return redirect('Indemnity_Accommodation_Emp_List')
    Success = 'Deleted'        
    encrypted_id = encrypt_id(EmpID)
    url = reverse('EmployeeLetters')  
    redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
    return redirect(redirect_url)
    
