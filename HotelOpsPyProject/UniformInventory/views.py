from django.shortcuts import render
from .models import UniformInformation,UniformItemMaster,UniformDetails
from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail

from django.shortcuts import redirect,render
from django.db import transaction
# Hr Request


from django.urls import reverse
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from HumanResources.views import EmployeeDetailsData, HrManagerNameandDesignation,ManagerNameandDesignation,EmployeeNameandDesignation

@transaction.atomic()
def  UniformHrRequest(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
     
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID    
    RequestedBy =   request.session["FullName"] 
    UserID = str(request.session["UserID"])
    hotelapitoken = MasterAttribute.HotelAPIkeyToken 
    EmpCode = request.GET.get('EC')
    EmpID = request.GET.get('EmpID')
  
    
    id = request.GET.get("UID")
    UN  = None
    UnDetails=None
    if EmpCode is not None:
        if id is not None:
            UN = UniformInformation.objects.get(OrganizationID=OrganizationID,IsDelete = False,id = id)
            UnDetails = UniformDetails.objects.filter(UniformInformation=UN,OrganizationID=OrganizationID,IsDelete=False)
        if UN is not None:
            DataFromUniformobj = 'DataFromUniformobj'
        else:
            DataFromUniformobj = 'DataFromUniformobjHR'
            EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
            
            UN = {
                'EmployeeCode': EmpDetails.EmployeeCode,
                'EmployeeName': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
                'Department': EmpDetails.Department,
                'DesignationGrade': EmpDetails.Designation,
                'ReportingtoDesigantion' : EmpDetails.ReportingtoDesignation 
              
            }
    
    
    if request.method == "POST":
        if DataFromUniformobj == "DataFromUniformobj" and id:    
            UN.ModifyBy = UserID
            UN.save()
            
        else:
            EmployeeName =   request.POST['EmployeeName'] or ''
            EmployeeCode =   request.POST['EmpCode'] or ''
            DesignationGrade =  request.POST['DesignationGrade']  or ''
            Department =   request.POST['Department'] or ''
            ReportingtoDesigantion = request.POST['ReportingtoDesigantion']  
            try:
                UN = UniformInformation.objects.get(OrganizationID=OrganizationID, IsDelete=False, EmployeeCode=EmployeeCode,HodStatus='0',HousekeppingStatus='0')
              
            except UniformInformation.DoesNotExist:
                UN = UniformInformation.objects.create(EmployeeName=EmployeeName,
                                                    EmployeeCode=EmployeeCode,
                                                    DesignationGrade=DesignationGrade,
                                                    Department=Department,
                                                    OrganizationID=OrganizationID,
                                                    ReportingtoDesigantion= ReportingtoDesigantion,
                                                    CreatedBy=UserID,HrStatus=1,HodStatus=0,HousekeppingStatus=0)
            


            # SendUniformNotificationHOD(EmployeeCode, OrganizationID, UserID)
           
        Success = True        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('Uniform')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
        return redirect(redirect_url)    
     

    
    context = {'OrganizationID':OrganizationID,'hotelapitoken':hotelapitoken,'UN':UN,'UnDetails':UnDetails}
    return render(request,"UniformInventroy/UniformHrRequest.html",context)







from django.contrib import messages

from LETTEROFAPPOINTMENT.models import LOALETTEROFAPPOINTMENTEmployeeDetail
from app.models import EmployeeMaster
from app.Global_Api import Get_Employee_Master_Data_By_Code
from django.utils import timezone

# @transaction.atomic
# def HouseKeepingRequest(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")

#     OrganizationID = request.session["OrganizationID"]
#     OID  = request.GET.get('OID')
#     if OID:
#             OrganizationID= OID    
#     RequestedBy = request.session["FullName"]
#     UserID = str(request.session["UserID"])
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     uitem = UniformItemMaster.objects.filter(IsDelete=False)
#     EmployeeCode = request.GET.get("EC")
#     id = request.GET.get("ID")
#     UN = None
    
#     EmployeeData=None  
#     if EmployeeCode:
#         EmployeeData = Get_Employee_Master_Data_By_Code(EmployeeCode,OID)
    
#     print("EmployeeCode is here::", EmployeeCode)
#     print("OID is here::", OID)
#     print("Employee Data is here::", EmployeeData)

#     if id is not None:
#         UN = UniformInformation.objects.filter(OrganizationID=OrganizationID, IsDelete=False, id=id).first()
    
#         UnDetails = UniformDetails.objects.filter(UniformInformation=UN, OrganizationID=OrganizationID, IsDelete=False)

#         for item in uitem:
#             item.NewQuantity = 0
#             item.AlteredQuantity = 0
#             item.IssuedQuantity = 0

#             if UnDetails.exists():
#                 un_detail = UnDetails.filter(UniformItemMaster=item).first()
#                 if un_detail:
#                     item.NewQuantity = un_detail.NewQuantity
#                     item.AlteredQuantity = un_detail.AlteredQuantity
#                     item.IssuedQuantity = un_detail.IssuedQuantity

#     if request.method == "POST":
#         if id is not None and UN:
#             UN.ModifyBy = UserID
#             UN.HousekeppingStatus = '1'
#             UN.HousekeppingComment = 'Approved'

#             UN.save()
#             UnDetails.update(IsDelete=True, ModifyBy=UserID)

#         Total_item = int(request.POST["Total_item"])
       
        
#         for i in range(Total_item + 1):  
#             ItemID_ = request.POST.get(f"ItemID_{i}")
#             New_ = request.POST.get(f"New_{i}") or 0
#             Altered_ = request.POST.get(f"Altered_{i}") or 0
#             Issued_ = request.POST.get(f"Issued_{i}") or 0
         
#             if ItemID_ is not None:
#                 UTM = UniformItemMaster.objects.get(id=ItemID_)
#                 UniformDetails.objects.create(
#                     UniformInformation=UN,
#                     OrganizationID=OrganizationID,
#                     UniformItemMaster=UTM,
#                     NewQuantity=New_,
#                     AlteredQuantity=Altered_,
#                     IssuedQuantity=Issued_,
#                 )
                
#             if not UN:
#                 UN = UniformInformation.objects.create(
#                     OrganizationID=OrganizationID,
#                     CreatedBy=UserID,
#                     HousekeppingStatus='1',
#                 )
                        
#         # Update Appointment Letters HK fields
#         AppointemetLetters = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
#             OrganizationID=OrganizationID, IsDelete=False
#         )

#         AppointemetLetters.update(
#             HK=True,
#             HKCreatedBy=UserID,
#             HKCreatedDateTime=timezone.now()
#         )

#         messages.success(request, "Updated Successfully")
#         return redirect("Issue_And_Clearance")
#         # return redirect("ManagerList")

#     context = {
#         'OrganizationID': OrganizationID, 
#         'hotelapitoken': hotelapitoken, 
#         'UN': UN, 
#         'EmployeeData': EmployeeData, 
#         'uitem': uitem
#     }
#     return render(request, "UniformInventroy/HouseKeepingRequest.html", context)

from datetime import date
from Checklist_Issued.views import run_background_checklist_tasks
from django.db import transaction

@transaction.atomic
def HouseKeepingRequest(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
        OrganizationID= OID    
        
    RequestedBy = request.session["FullName"]
    UserID = str(request.session["UserID"])
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    uitem = UniformItemMaster.objects.filter(IsDelete=False)
    EmployeeCode = request.GET.get("EC")
    Hide = request.GET.get("Hide")
    id = request.GET.get("ID")
    UN = None
    
    
    Hide_Value=False
    if Hide:
        Hide_Value = Hide
    
    EmployeeData=None  
    if EmployeeCode:
        EmployeeData = Get_Employee_Master_Data_By_Code(EmployeeCode,OID)
    
    print("EmployeeCode is here::", EmployeeCode)
    print("OID is here::", OID)
    print("Employee Data is here::", EmployeeData)

    if id is not None:
        UN = UniformInformation.objects.filter(OrganizationID=OrganizationID, IsDelete=False, id=id).first()
    
        UnDetails = UniformDetails.objects.filter(UniformInformation=UN, OrganizationID=OrganizationID, IsDelete=False)

        for item in uitem:
            item.NewQuantity = 0
            item.AlteredQuantity = 0
            item.IssuedQuantity = 0

            if UnDetails.exists():
                un_detail = UnDetails.filter(UniformItemMaster=item).first()
                if un_detail:
                    item.NewQuantity = un_detail.NewQuantity
                    item.AlteredQuantity = un_detail.AlteredQuantity
                    item.IssuedQuantity = un_detail.IssuedQuantity
                    
    if request.method == "POST":
        
        EmployeeCode = request.POST.get("EmployeeCode")
        EmployeeName = request.POST.get("EmployeeName")
        Department = request.POST.get("Department")
        DesignationGrade = request.POST.get("DesignationGrade")
        ReportingtoDesigantion = request.POST.get("ReportingtoDesigantion")
        EmpID = request.POST.get("EmpID")
        IssuedDate = request.POST.get("IssuedDate")
    

        # 1. If editing an existing request
        if id is not None and UN:
            UN.ModifyBy = UserID
            UN.HousekeppingStatus = '1'
            UN.HousekeppingComment = 'Approved'
            UN.save()
            UnDetails.update(IsDelete=True, ModifyBy=UserID)

        # 2. If creating NEW request → create UN BEFORE looping
        if not UN:
            UN = UniformInformation.objects.create(
                EmpID = EmpID,
                EmployeeName = EmployeeName,
                IssuedDate = IssuedDate,
                EmployeeCode = EmployeeCode,
                DesignationGrade = DesignationGrade,
                Department = Department,
                ReportingtoDesigantion = ReportingtoDesigantion,
                OrganizationID=OrganizationID,
                CreatedBy=UserID,
                HousekeppingStatus='1',
            )

        # 3. Save item details
        Total_item = int(request.POST["Total_item"])

        for i in range(Total_item):
            ItemID_ = request.POST.get(f"ItemID_{i}")
            New_ = request.POST.get(f"New_{i}") or 0
            Altered_ = request.POST.get(f"Altered_{i}") or 0
            Issued_ = request.POST.get(f"Issued_{i}") or 0

            if ItemID_:
                UTM = UniformItemMaster.objects.get(id=ItemID_)
                UniformDetails.objects.create(
                    UniformInformation=UN,
                    OrganizationID=OrganizationID,
                    UniformItemMaster=UTM,
                    NewQuantity=New_,
                    AlteredQuantity=Altered_,
                    IssuedQuantity=Issued_,
                )

        # 4. Update LOA table
        AppointemetLetters = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
            OrganizationID=OID, IsDelete=False, emp_code=EmployeeCode
        )

        AppointemetLetters.update(
            HK=True,
            HKCreatedBy=UserID,
            HKCreatedDateTime=timezone.now()
        )
        Object_ID = 36      # Uniform Issued
        
        transaction.on_commit(
            lambda: run_background_checklist_tasks(EmployeeCode, OrganizationID, Object_ID, UserID)
        )

        messages.success(request, "Updated Successfully")
        return redirect("Issue_view")

    context = {
        'OrganizationID': OrganizationID, 
        'hotelapitoken': hotelapitoken, 
        'UN': UN, 
        'EmployeeData': EmployeeData, 
        'Hide_Value': Hide_Value, 
        'uitem': uitem,
        "date": date.today().isoformat(),
    }
    return render(request, "UniformInventroy/HouseKeepingRequest.html", context)




from django.contrib import messages

from HumanResources.views import DepartmentofEmployee
from django.shortcuts import render, redirect
from .models import UniformInformation, UniformDetails  

from EmpResignation.models import EmpResigantionModel


@transaction.atomic
def HouseKeepingReturnRequest(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    Hide = request.GET.get("Hide")
    
    Hide_Value=False
    if Hide:
        Hide_Value = Hide
    
    EmpCode  = request.GET.get('EC')
    EmployeeCode = None
    if EmpCode:
        EmployeeCode = EmpCode
        
    if OID:
            OrganizationID= OID    
    # OrganizationID = 1001

    RequestedBy = request.session["FullName"]
    UserID = str(request.session["UserID"])
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    uitem = UniformItemMaster.objects.filter(IsDelete=False)
    id = request.GET.get("ID")
    UN = None

    if id is not None:
        UN = UniformInformation.objects.filter(OrganizationID=OrganizationID, IsDelete=False, id=id).first()
        UnDetails = UniformDetails.objects.filter(UniformInformation=UN, OrganizationID=OrganizationID, IsDelete=False)

        for item in uitem:

            if UnDetails.exists():
                un_detail = UnDetails.filter(UniformItemMaster=item).first()
                if un_detail:
                    item.NewQuantity = un_detail.NewQuantity
                    item.AlteredQuantity = un_detail.AlteredQuantity
                    item.IssuedQuantity = un_detail.IssuedQuantity

                    item.ReturnNewQuantity = un_detail.ReturnNewQuantity
                    item.ReturnAlteredQuantity = un_detail.ReturnAlteredQuantity
                    item.ReturnIssuedQuantity = un_detail.ReturnIssuedQuantity

                    item.NewVariance = un_detail.NewVariance
                    item.AlterVariance = un_detail.AlterVariance
                    item.IssueVariance = un_detail.IssueVariance


    if request.method == "POST":
       
        Total_item = int(request.POST["Total_item"])
        
        for i in range(Total_item):  
            ItemID_ = request.POST.get(f"ItemID_{i}")
            ReturnNew_ = request.POST.get(f"ReturnNew_{i}") 
            ReturnAltered_ = request.POST.get(f"ReturnAltered_{i}") 
            ReturnIssued_ = request.POST.get(f"ReturnIssued_{i}") 
            NewVariance_= request.POST.get(f"NewVariance_{i}") 
            AlterVariance_ = request.POST.get(f"AlterVariance_{i}") 
            IssueVariance_ = request.POST.get(f"IssueVariance_{i}") 
            TotalCharged_ = request.POST.get(f"TotalCharged_{i}") or 0

            if ItemID_:
                uniform_item = UniformItemMaster.objects.get(id=ItemID_)
                un_detail = UniformDetails.objects.get(UniformInformation=UN, UniformItemMaster=uniform_item, IsDelete=False)
                if un_detail:
                    un_detail.ReturnNewQuantity = ReturnNew_
                    un_detail.ReturnAlteredQuantity = ReturnAltered_
                    un_detail.ReturnIssuedQuantity = ReturnIssued_
                    un_detail.NewVariance = NewVariance_
                    un_detail.AlterVariance = AlterVariance_
                    un_detail.IssueVariance = IssueVariance_
                    un_detail.TotalCharged = TotalCharged_
                    
                    un_detail.ModifyBy = UserID
                    un_detail.save()
                    
        UN.Return = True
        UN.ReturnAmount = request.POST['ReturnAmount']
        UN.save()    
        
        ResignationData = EmpResigantionModel.objects.filter(
            OrganizationID=OID, IsDelete=False, Emp_Code=EmployeeCode
        )

        ResignationData.update(
            HK=True,
            HKCreatedBy=UserID,
            HKCreatedDateTime=timezone.now()
        )
           
        messages.success(request, "Updated Successfully")
        return redirect("Clearance_view")

    context = {
        'OrganizationID': OrganizationID, 
        'hotelapitoken': hotelapitoken, 
        'UN': UN, 
        'Hide_Value': Hide_Value, 
        'uitem': uitem
    }
    return render(request, "UniformInventroy/HouseKeepingReturnRequest.html", context)


from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

# @csrf_exempt
# @transaction.atomic
# def housekeeping_returns_pdf_api(request):
#     """API that returns PDF instead of rendering an HTML page."""

#     # Read parameters from URL or POST
#     OrganizationID = request.GET.get("OID") or request.POST.get("OID")
#     ID = request.GET.get("ID") or request.POST.get("ID")

#     if ID is None:
#         return HttpResponse({"error": "ID is required"}, status=400)

#     # Fetch data exactly like your current view
#     UN = UniformInformation.objects.filter(
#         OrganizationID=OrganizationID,
#         IsDelete=False,
#         id=ID
#     ).first()

#     if not UN:
#         return HttpResponse({"error": "Record not found"}, status=404)

#     # Create an in-memory PDF buffer
#     buffer = io.BytesIO()
#     p = canvas.Canvas(buffer, pagesize=A4)

#     # -------- PDF CONTENT ----------
#     p.setFont("Helvetica", 12)
#     p.drawString(50, 800, f"House Keeping Return Request")
#     p.drawString(50, 780, f"Organization: {OrganizationID}")
#     p.drawString(50, 760, f"Employee: {UN.EmployeeName}")
#     p.drawString(50, 740, f"Return Amount: {UN.ReturnAmount or '0'}")

#     # Add each uniform item line
#     y = 700
#     details = UniformDetails.objects.filter(
#         UniformInformation=UN,
#         IsDelete=False
#     )

#     for d in details:
#         p.drawString(50, y, f"{d.UniformItemMaster.ItemName} - Returned: "
#                             f"N:{d.ReturnNewQuantity}, A:{d.ReturnAlteredQuantity}, I:{d.ReturnIssuedQuantity}")
#         y -= 20

#     p.showPage()
#     p.save()
#     buffer.seek(0)
#     # -------- END PDF CONTENT ----------

#     # Return actual PDF response
#     response = HttpResponse(buffer, content_type="application/pdf")
#     response["Content-Disposition"] = f'attachment; filename="HK_Return_{ID}.pdf"'
#     return response



from django.http import HttpResponse

from django.db import transaction
import pdfkit
from django.template.loader import get_template
from django.conf import settings


@transaction.atomic
def housekeeping_returns_pdf_api(request):

    OrganizationID = request.GET.get("OID")
    ID = request.GET.get("ID")

    if not OrganizationID or not ID:
        return HttpResponse("OID and ID are required.", status=400)

    # Same logic you already use
    UN = UniformInformation.objects.filter(
        OrganizationID=OrganizationID, 
        IsDelete=False, 
        id=ID
    ).first()

    if not UN:
        return HttpResponse("Record not found.", status=404)

    uitem = UniformItemMaster.objects.filter(IsDelete=False)

    # Your existing template context
    context = {
        "OrganizationID": OrganizationID,
        "UN": UN,
        "uitem": uitem,
        "Hide_Value": False
    }


    # Render HTML
    template = get_template("UniformInventroy/HouseKeepingReturnRequest_PDF.html")
    html = template.render(context)

    # Create PDF
    wkhtmltopdf_path = getattr(settings, 'WKHTMLTOPDF_CMD', None)

    if not wkhtmltopdf_path:
        raise Exception("WKHTMLTOPDF_CMD is not configured in settings.py")

    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)


    # options = {
    #     'page-size': 'A4',
    #     'orientation': 'Landscape',
    #     'encoding': 'UTF-8',
    #     'margin-top': '0mm',
    #     'margin-bottom': '0mm',
    #     'margin-left': '0mm',
    #     'margin-right': '0mm',
    #     'enable-local-file-access': None,
    # }

    pdf = pdfkit.from_string(
        html,
        False,
        # options=options,
        configuration=config
    )

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="attachment; filename=HK_Return_{ID}.pdf"'
    )
    return response



# def ManagerList(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")

#     OrganizationID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])
#     EmployeeCode = request.session["EmployeeCode"]
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     ReportingtoDesignation = ''
#     HKM = False
#     Created = "0"  # Initialize Created here

#     if EmployeeCode:
#         Repobj = ReptoDesignation(request, OrganizationID, EmployeeCode)
        
#         if Repobj:
#             ReportingtoDesignation = Repobj.get('work_designation')
#             if 'Housekeeping Manager' in ReportingtoDesignation or 'HK Manager' in ReportingtoDesignation:
#                 HKM = True
#                 Created = "0"  # Assignment instead of comparison
    
#     UNI = None

#     if HKM:
#         if OrganizationID and UserID:
#             UNI = UniformInformation.objects.filter(
#                 HodStatus=1,
#                 HrStatus=1,
#                 OrganizationID=OrganizationID,
#                 IsDelete=False
#             )
#             for u in UNI:
#                 u.Rights = "HKM"
#                 if u.id:
#                     uobj = UniformDetails.objects.filter(
#                         OrganizationID=OrganizationID,
#                         IsDelete=False,
#                         UniformInformation_id=u.id
#                     ).first()
#                     if uobj:
#                         Created = "1"  # Assignment instead of comparison
#                 u.Created = Created
#                 u.save()
#     else:
#         if OrganizationID and ReportingtoDesignation and UserID:
#             UNI = UniformInformation.objects.filter(
#                 ReportingtoDesigantion=ReportingtoDesignation,
#                 OrganizationID=OrganizationID,
#                 IsDelete=False,
#                 HrStatus=1,
#                 HodStatus = 0
#             )
#             for u in UNI:
#                 u.Rights = "REP"
#                 u.save()

#     context = {
#         'UNI': UNI,
#         'hotelapitoken': hotelapitoken,
#         'ReportingtoDesigantion': ReportingtoDesignation,
#         'UserID': UserID,
#         'OrganizationID': OrganizationID
#     }
#     return render(request, "UniformInventroy/ManagerList.html", context)


from django.db.models import Q
from HumanResources.views import get_employee_designation_by_EmployeeCode

def ManagerList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID    
    UserID = str(request.session["UserID"])
    EmployeeCode = request.session["EmployeeCode"]
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    ReportingtoDesignation = get_employee_designation_by_EmployeeCode(OrganizationID,EmployeeCode)
    
    HKM = False
    Created = "0"

    if EmployeeCode:
        Repobj = DepartmentofEmployee(request, OrganizationID,EmployeeCode)
        
        if Repobj:
            work_Department = Repobj.get('work_Department')
            print("work_Department = ",work_Department)
            if 'Housekeeping' in work_Department:
                HKM = True

    if OrganizationID and UserID:
        filter_conditions = Q(OrganizationID=OrganizationID, IsDelete=False, HrStatus=1)
        
        if HKM:
            # filter_conditions &= Q(HodStatus=1)
            filter_conditions &= (
                    Q(HodStatus=1) |
                    (Q(ReportingtoDesigantion=ReportingtoDesignation) & Q(HodStatus=0))
                )
            Rights = "HKM"
           
        else:
            filter_conditions &= Q(ReportingtoDesigantion=ReportingtoDesignation, HodStatus=0)
            Rights = "REP"
        
        UNI = UniformInformation.objects.filter(filter_conditions).order_by('-id')

        for u in UNI:
            if u.HodStatus == '0' and HKM:
                u.Rights="REP"
            else:
                u.Rights = Rights
            u.Created  = Created
            if HKM and u.id:
                uobj = UniformDetails.objects.filter(
                    OrganizationID=OrganizationID,
                    IsDelete=False,
                    UniformInformation_id=u.id
                ).first()
                if uobj:
                    Created = "1"
            u.Created = Created if HKM else u.Created  
            u.save()

    context = {
        'UNI': UNI,
        'hotelapitoken': hotelapitoken,
        'ReportingtoDesigantion': ReportingtoDesignation,
        'UserID': UserID,
        'OrganizationID': OrganizationID
    }
    return render(request, "UniformInventroy/ManagerList.html", context)




def UniformDelete(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")

     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID    
     UserID = str(request.session["UserID"])
     
     with transaction.atomic():
        id = request.GET.get("ID")
        if id is not None:
            un = UniformInformation.objects.get(OrganizationID=OrganizationID,IsDelete = False,id = id)
            un.IsDelete = 1
            un.ModifyBy = UserID
            un.save()
        e = request.GET.get('E', "")       
        if e!='':
                    EC = request.GET.get('EC', "")
                    O = request.GET.get('O', "")
                    od = OrganizationDetail(OrganizationID)
                    DomainCode=od.get_OrganizationDomainCode()
                    newd = MasterAttribute.CurrentHost.replace("http://hotelops.in","http://"+DomainCode+".hotelops.in")
                    return redirect(newd+"/HR/Home/EmpProfile?E="+e+"&Q=empuniforminventory&EC="+EC+"&O="+O+"") 
  
        







from rest_framework import status


from rest_framework.decorators import api_view
from django.http import JsonResponse


@api_view(['GET'])
def UniformHodApprovalListApi(request):
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    token = request.headers.get('hotel-api-token')
    
    if token != hotelapitoken:
        return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)
    
    OrganizationID = request.query_params.get('OrganizationID')
    ReportingtoDesignation = request.query_params.get('Designation')
    UserID = request.query_params.get('UserID')
   
    if OrganizationID and ReportingtoDesignation and UserID:
        employee_uniform_details = UniformInformation.objects.filter(
            ReportingtoDesigantion=ReportingtoDesignation, 
            OrganizationID=OrganizationID,
            IsDelete=False
        )
        print(employee_uniform_details)
        if not employee_uniform_details.exists():
            return JsonResponse({"error": "Employee Uniform details not found"}, status=status.HTTP_404_NOT_FOUND)
        
      
        employee_data = [
            {
                "ID":emp.id,
                "EmployeeName": emp.EmployeeName,
                "EmployeeCode": emp.EmployeeCode,
                "DesignationGrade": emp.DesignationGrade,
                "Department": emp.Department,
                
                "HodStatus": emp.HodStatus,
                "HodComment": emp.HodComment,
                "ReportingtoDesigantion": emp.ReportingtoDesigantion,
                "OrganizationID": emp.OrganizationID
            }
            for emp in employee_uniform_details
        ]
        
        return JsonResponse(employee_data, safe=False, status=status.HTTP_200_OK)
    
    return JsonResponse({"error": "Invalid parameters: OrganizationID, ReportingtoDesignation, or UserID"}, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

@api_view(['POST'])
def UniformHodApprovalApi(request):
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    token = request.headers.get('hotel-api-token')
    
    if token != hotelapitoken:
        return Response({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)
    
    ID = request.data.get('ID')
    OrganizationID = request.data.get('OrganizationID') 
    UserID = request.data.get('UserID')
    HodStatus = request.data.get('HodStatus')
    HodComment = request.data.get('HodComment')
    
    if ID and UserID and HodStatus is not None and HodComment:
        try:
            employee_it_detail = UniformInformation.objects.get(id=ID, IsDelete=False, OrganizationID=OrganizationID)
            
            if int(HodStatus) not in [1, -1]:
                return Response({"error": "Invalid status value. Use 1 for approve, -1 for reject."}, status=status.HTTP_400_BAD_REQUEST)
            
            employee_it_detail.HodStatus = HodStatus
            employee_it_detail.HodComment = HodComment
            employee_it_detail.save()
            
            if str(HodStatus) == '1':
                return JsonResponse({"success": "Approved successfully"}, status=200)
            elif str(HodStatus) == '-1':
                return JsonResponse({"success": "Rejected successfully"}, status=200)

        except UniformInformation.DoesNotExist:
            return JsonResponse({"error": "Employee Uniform detail not found"}, status=404)
    else:
        return JsonResponse({"error": "Invalid parameters: ID, UserID, OrganizationID, or HodComment"}, status=400)




import requests
def SendUniformNotification(EmployeeCode, OrganizationID, UserID):
    url = "http://127.0.0.1:8000/EmailNotification/EmployeeUniformRequest/"
    hotel_api_token = MasterAttribute.HotelAPIkeyToken  
    headers = {
        "hotel-api-token": hotel_api_token,
        "Content-Type": "application/json"
    }
    payload = {
        "EmployeeCode": EmployeeCode,
        "OrganizationID": OrganizationID,
        "UserID": UserID
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  
        return response.json()  
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")






import requests
def SendUniformNotificationHOD(EmployeeCode, OrganizationID, UserID):
    url = "http://127.0.0.1:8000/EmailNotification/EmployeeUniformRequestHOD/"
    hotel_api_token = MasterAttribute.HotelAPIkeyToken  
    headers = {
        "hotel-api-token": hotel_api_token,
        "Content-Type": "application/json"
    }
    payload = {
        "EmployeeCode": EmployeeCode,
        "OrganizationID": OrganizationID,
        "UserID": UserID
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  
        return response.json()  
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
