from HumanResources.views import EmployeeDetailsData, HrManagerNameandDesignation,ManagerNameandDesignation,EmployeeNameandDesignation
from .models import HR_Inventory_Information,HR_Inventory_Item_Master,HR_Inventory_Details
from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail
from LETTEROFAPPOINTMENT.models import LOALETTEROFAPPOINTMENTEmployeeDetail
from Checklist_Issued.views import run_background_checklist_tasks
from app.Global_Api import Get_Employee_Master_Data_By_Code
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from HumanResources.views import DepartmentofEmployee
from EmpResignation.models import EmpResigantionModel
from django.template.loader import render_to_string
from django.shortcuts import redirect,render
from app.models import EmployeeMaster
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.urls import reverse
from datetime import date




@transaction.atomic
def HR_Inventory_Request(request):
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
    uitem = HR_Inventory_Item_Master.objects.filter(IsDelete=False)
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
    
    # print("EmployeeCode is here::", EmployeeCode)
    # print("OID is here::", OID)
    # print("Employee Data is here::", EmployeeData)
    # print("id is here::", id)

    uitem = HR_Inventory_Item_Master.objects.filter(IsDelete=False)
    UN = None

    if id:
        UN = HR_Inventory_Information.objects.filter(
            id=id, OrganizationID=OrganizationID, IsDelete=False
        ).first()

        existing_details = {
            d.HR_Inventory_Item_Master.id: d
            for d in HR_Inventory_Details.objects.filter(
                HR_Inventory_Information=UN, IsDelete=False
            )
        }

        for item in uitem:
            detail = existing_details.get(item.id)
            item.Item_Issued = detail.Item_Issued if detail else ""

    if request.method == "POST":

        EmpID = request.POST.get("EmpID")
        EmployeeCode = request.POST.get("EmployeeCode")
        EmployeeName = request.POST.get("EmployeeName")
        Department = request.POST.get("Department")
        DesignationGrade = request.POST.get("DesignationGrade")
        ReportingtoDesigantion = request.POST.get("ReportingtoDesigantion")
        IssuedDate = request.POST.get("IssuedDate")

        if UN:
            UN.EmpID = EmpID
            UN.EmployeeName = EmployeeName
            UN.EmployeeCode = EmployeeCode
            UN.Department = Department
            UN.DesignationGrade = DesignationGrade
            UN.ReportingtoDesigantion = ReportingtoDesigantion
            UN.IssuedDate = IssuedDate
            UN.ModifyBy = UserID
            UN.save()

        else:
            UN = HR_Inventory_Information.objects.create(
                EmpID=EmpID,
                EmployeeName=EmployeeName,
                EmployeeCode=EmployeeCode,
                Department=Department,
                DesignationGrade=DesignationGrade,
                ReportingtoDesigantion=ReportingtoDesigantion,
                IssuedDate=IssuedDate,
                OrganizationID=OrganizationID,
                CreatedBy=UserID,
            )

        Total_item = int(request.POST["Total_item"])

        for i in range(Total_item):
            item_id = request.POST.get(f"ItemID_{i}")
            issued = request.POST.get(f"Item_Issued_{i}") or ""

            if not item_id:
                continue

            item_obj = HR_Inventory_Item_Master.objects.get(id=item_id)

            # Update OR create (NO DELETE)
            HR_Inventory_Details.objects.update_or_create(
                HR_Inventory_Information=UN,
                HR_Inventory_Item_Master=item_obj,
                defaults={
                    "Item_Issued": issued,
                    "OrganizationID": OrganizationID,
                    "ModifyBy": UserID,
                }
            )

        LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
            OrganizationID=OID, IsDelete=False, emp_code=EmployeeCode
        ).update(
            HR=True,
            HRCreatedBy=UserID,
            HRCreatedDateTime=timezone.now()
        )

        messages.success(request, "Saved Successfully")
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
    return render(request, "HR_Inventory/HR_Inventory_Request.html", context)




@transaction.atomic
def HR_Inventory_Return_Request(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    OID = request.GET.get("OID")
    if OID:
        OrganizationID = OID

    UserID = str(request.session["UserID"])
    hotelapitoken = MasterAttribute.HotelAPIkeyToken

    EmployeeCode = request.GET.get("EC")
    Hide = request.GET.get("Hide")
    id = request.GET.get("ID")

    Hide_Value = Hide if Hide else False

    # LOAD ALL ITEMS
    uitem = HR_Inventory_Item_Master.objects.filter(IsDelete=False)

    UN = None

    if id:
        UN = HR_Inventory_Information.objects.filter(
            id=id, OrganizationID=OrganizationID, IsDelete=False
        ).first()

        details = HR_Inventory_Details.objects.filter(
            HR_Inventory_Information=UN, OrganizationID=OrganizationID, IsDelete=False
        )

        # Load existing values into the uitem list
        for item in uitem:
            d = details.filter(HR_Inventory_Item_Master=item).first()
            if d:
                item.Item_Issued = d.Item_Issued
                item.Item_Returned = getattr(d, "Item_Returned", "")
                # item.Return_Remark = getattr(d, "Return_Remark", "")
                
    if request.method == "POST":

        Total_item = int(request.POST["Total_item"])

        for i in range(Total_item):

            item_id = request.POST.get(f"ItemID_{i}")
            issued = request.POST.get(f"Issued_{i}") or ""
            returned = request.POST.get(f"Item_Returned_{i}") or ""
            total_charged = request.POST.get(f"TotalCharged_{i}") or 0

            if not item_id:
                continue

            item_obj = HR_Inventory_Item_Master.objects.get(id=item_id)

            detail = HR_Inventory_Details.objects.get(
                HR_Inventory_Information=UN,
                HR_Inventory_Item_Master=item_obj,
                IsDelete=False
            )

            detail.Item_Issued = issued
            detail.Item_Returned = returned
            detail.TotalCharged = total_charged
            detail.ModifyBy = UserID
            detail.save()

        UN.Return = True
        UN.ReturnAmount = request.POST.get("TotalCharged", 0)
        UN.ReturnAmount = request.POST.get("TotalCharged", 0)
        UN.HRCreatedBy = UserID
        UN.HR = True
        UN.save()
        
        ResignationData = EmpResigantionModel.objects.filter(
            OrganizationID=OID, IsDelete=False, Emp_Code=EmployeeCode
        )

        ResignationData.update(
            HR=True,
            HRCreatedBy=UserID,
            HRCreatedDateTime=timezone.now()
        )
           
        messages.success(request, "Return Updated Successfully")
        return redirect("Clearance_view")


    context = {
        "OrganizationID": OrganizationID,
        "hotelapitoken": hotelapitoken,
        "UN": UN,
        "Hide_Value": Hide_Value,
        "uitem": uitem,
        "date": date.today().isoformat(),
    }

    return render(request, "HR_Inventory/HR_Inventory_Return_Request.html", context)
