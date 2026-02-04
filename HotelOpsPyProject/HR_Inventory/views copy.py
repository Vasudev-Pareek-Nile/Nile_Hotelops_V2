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
from weasyprint import HTML
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
    
    print("EmployeeCode is here::", EmployeeCode)
    print("OID is here::", OID)
    print("Employee Data is here::", EmployeeData)
    print("id is here::", id)

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


# @transaction.atomic
# def HR_Inventory_Return_Request(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")

#     OrganizationID = request.session["OrganizationID"]
#     OID  = request.GET.get('OID')
#     if OID:
#         OrganizationID= OID    
        
#     RequestedBy = request.session["FullName"]
#     UserID = str(request.session["UserID"])
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     uitem = HR_Inventory_Item_Master.objects.filter(IsDelete=False)
#     EmployeeCode = request.GET.get("EC")
#     Hide = request.GET.get("Hide")
#     id = request.GET.get("ID")
#     UN = None
    
    
#     Hide_Value=False
#     if Hide:
#         Hide_Value = Hide
    
#     EmployeeData=None  
#     if EmployeeCode:
#         EmployeeData = Get_Employee_Master_Data_By_Code(EmployeeCode,OID)
    
#     print("EmployeeCode is here::", EmployeeCode)
#     print("OID is here::", OID)
#     print("Employee Data is here::", EmployeeData)
#     print("id is here::", id)

#     uitem = HR_Inventory_Item_Master.objects.filter(IsDelete=False)
#     UN = None

#     if id:
#         UN = HR_Inventory_Information.objects.filter(
#             id=id, OrganizationID=OrganizationID, IsDelete=False
#         ).first()

#         existing_details = {
#             d.HR_Inventory_Item_Master.id: d
#             for d in HR_Inventory_Details.objects.filter(
#                 HR_Inventory_Information=UN, IsDelete=False
#             )
#         }

#         for item in uitem:
#             detail = existing_details.get(item.id)
#             item.Item_Issued = detail.Item_Issued if detail else ""

#     if request.method == "POST":

#         EmpID = request.POST.get("EmpID")
#         EmployeeCode = request.POST.get("EmployeeCode")
#         EmployeeName = request.POST.get("EmployeeName")
#         Department = request.POST.get("Department")
#         DesignationGrade = request.POST.get("DesignationGrade")
#         ReportingtoDesigantion = request.POST.get("ReportingtoDesigantion")
#         IssuedDate = request.POST.get("IssuedDate")

#         if UN:
#             UN.EmpID = EmpID
#             UN.EmployeeName = EmployeeName
#             UN.EmployeeCode = EmployeeCode
#             UN.Department = Department
#             UN.DesignationGrade = DesignationGrade
#             UN.ReportingtoDesigantion = ReportingtoDesigantion
#             UN.IssuedDate = IssuedDate
#             UN.ModifyBy = UserID
#             UN.save()

#         else:
#             UN = HR_Inventory_Information.objects.create(
#                 EmpID=EmpID,
#                 EmployeeName=EmployeeName,
#                 EmployeeCode=EmployeeCode,
#                 Department=Department,
#                 DesignationGrade=DesignationGrade,
#                 ReportingtoDesigantion=ReportingtoDesigantion,
#                 IssuedDate=IssuedDate,
#                 OrganizationID=OrganizationID,
#                 CreatedBy=UserID,
#             )

#         Total_item = int(request.POST["Total_item"])

#         for i in range(Total_item):
#             item_id = request.POST.get(f"ItemID_{i}")
#             issued = request.POST.get(f"Item_Issued_{i}") or ""

#             if not item_id:
#                 continue

#             item_obj = HR_Inventory_Item_Master.objects.get(id=item_id)

#             # Update OR create (NO DELETE)
#             HR_Inventory_Details.objects.update_or_create(
#                 HR_Inventory_Information=UN,
#                 HR_Inventory_Item_Master=item_obj,
#                 defaults={
#                     "Item_Issued": issued,
#                     "OrganizationID": OrganizationID,
#                     "ModifyBy": UserID,
#                 }
#             )

#         LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
#             OrganizationID=OID, IsDelete=False, emp_code=EmployeeCode
#         ).update(
#             HR=True,
#             HRCreatedBy=UserID,
#             HRCreatedDateTime=timezone.now()
#         )

#         messages.success(request, "Saved Successfully")
#         return redirect("Clearance_view")
    
#     context = {
#         'OrganizationID': OrganizationID, 
#         'hotelapitoken': hotelapitoken, 
#         'UN': UN, 
#         'EmployeeData': EmployeeData, 
#         'Hide_Value': Hide_Value, 
#         'uitem': uitem,
#         "date": date.today().isoformat(),
#     }
#     return render(request, "HR_Inventory/HR_Inventory_Return_Request.html", context)


# @transaction.atomic
# def HR_Inventory_Request(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)

#     OrganizationID = request.session["OrganizationID"]
#     OID = request.GET.get("OID") or OrganizationID
#     OrganizationID = OID

#     UserID = str(request.session["UserID"])
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     id = request.GET.get("ID")
    
    
#     print("Id is here::", id)
#     print("OID is here::", OID)

#     uitem = HR_Inventory_Item_Master.objects.filter(IsDelete=False)
#     UN = None

#     if id:
#         UN = HR_Inventory_Information.objects.filter(
#             id=id, OrganizationID=OrganizationID, IsDelete=False
#         ).first()

#         existing_details = {
#             d.HR_Inventory_Item_Master.id: d
#             for d in HR_Inventory_Details.objects.filter(
#                 HR_Inventory_Information=UN, IsDelete=False
#             )
#         }

#         for item in uitem:
#             detail = existing_details.get(item.id)
#             item.Item_Issued = detail.Item_Issued if detail else ""

#     if request.method == "POST":

#         EmpID = request.POST.get("EmpID")
#         EmployeeCode = request.POST.get("EmployeeCode")
#         EmployeeName = request.POST.get("EmployeeName")
#         Department = request.POST.get("Department")
#         DesignationGrade = request.POST.get("DesignationGrade")
#         ReportingtoDesigantion = request.POST.get("ReportingtoDesigantion")
#         IssuedDate = request.POST.get("IssuedDate")

#         if UN:
#             UN.EmpID = EmpID
#             UN.EmployeeName = EmployeeName
#             UN.EmployeeCode = EmployeeCode
#             UN.Department = Department
#             UN.DesignationGrade = DesignationGrade
#             UN.ReportingtoDesigantion = ReportingtoDesigantion
#             UN.IssuedDate = IssuedDate
#             UN.ModifyBy = UserID
#             UN.save()

#         else:
#             UN = HR_Inventory_Information.objects.create(
#                 EmpID=EmpID,
#                 EmployeeName=EmployeeName,
#                 EmployeeCode=EmployeeCode,
#                 Department=Department,
#                 DesignationGrade=DesignationGrade,
#                 ReportingtoDesigantion=ReportingtoDesigantion,
#                 IssuedDate=IssuedDate,
#                 OrganizationID=OrganizationID,
#                 CreatedBy=UserID,
#             )

#         Total_item = int(request.POST["Total_item"])

#         for i in range(Total_item):
#             item_id = request.POST.get(f"ItemID_{i}")
#             issued = request.POST.get(f"Item_Issued_{i}") or ""

#             if not item_id:
#                 continue

#             item_obj = HR_Inventory_Item_Master.objects.get(id=item_id)

#             # Update OR create (NO DELETE)
#             HR_Inventory_Details.objects.update_or_create(
#                 HR_Inventory_Information=UN,
#                 HR_Inventory_Item_Master=item_obj,
#                 defaults={
#                     "Item_Issued": issued,
#                     "OrganizationID": OrganizationID,
#                     "ModifyBy": UserID,
#                 }
#             )

#         LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
#             OrganizationID=OID, IsDelete=False, emp_code=EmployeeCode
#         ).update(
#             HR=True,
#             HRCreatedBy=UserID,
#             HRCreatedDateTime=timezone.now()
#         )

#         messages.success(request, "Saved Successfully")
#         return redirect("Issue_view")
    
#     context = {
#         "UN": UN,
#         "uitem": uitem,
#         "OrganizationID": OrganizationID,
#         "hotelapitoken": hotelapitoken,
#         "date": date.today().isoformat(),
#     }
    
#     return render(request, "HR_Inventory/HR_Inventory_Request.html", context)




# @transaction.atomic
# def HR_Inventory_Return_Request(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")

#     OrganizationID = request.session["OrganizationID"]
#     OID  = request.GET.get('OID')
#     Hide = request.GET.get("Hide")
    
#     Hide_Value=False
#     if Hide:
#         Hide_Value = Hide
    
#     EmpCode  = request.GET.get('EC')
#     EmployeeCode = None
#     if EmpCode:
#         EmployeeCode = EmpCode
        
#     if OID:
#             OrganizationID= OID    
#     # OrganizationID = 1001

#     RequestedBy = request.session["FullName"]
#     UserID = str(request.session["UserID"])
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     uitem = HR_Inventory_Item_Master.objects.filter(IsDelete=False)
#     id = request.GET.get("ID")
#     UN = None

#     if id is not None:
#         UN = HR_Inventory_Information.objects.filter(OrganizationID=OrganizationID, IsDelete=False, id=id).first()
#         UnDetails = HR_Inventory_Details.objects.filter(HR_Inventory_Information=UN, OrganizationID=OrganizationID, IsDelete=False)

#         for item in uitem:

#             if UnDetails.exists():
#                 un_detail = UnDetails.filter(HR_Inventory_Item_Master=item).first()
#                 if un_detail:
#                     item.NewQuantity = un_detail.NewQuantity
#                     item.AlteredQuantity = un_detail.AlteredQuantity
#                     item.IssuedQuantity = un_detail.IssuedQuantity

#                     item.ReturnNewQuantity = un_detail.ReturnNewQuantity
#                     item.ReturnAlteredQuantity = un_detail.ReturnAlteredQuantity
#                     item.ReturnIssuedQuantity = un_detail.ReturnIssuedQuantity

#                     item.NewVariance = un_detail.NewVariance
#                     item.AlterVariance = un_detail.AlterVariance
#                     item.IssueVariance = un_detail.IssueVariance


#     if request.method == "POST":
       
#         Total_item = int(request.POST["Total_item"])
        
#         for i in range(Total_item):  
#             ItemID_ = request.POST.get(f"ItemID_{i}")
#             ReturnNew_ = request.POST.get(f"ReturnNew_{i}") 
#             ReturnAltered_ = request.POST.get(f"ReturnAltered_{i}") 
#             ReturnIssued_ = request.POST.get(f"ReturnIssued_{i}") 
#             NewVariance_= request.POST.get(f"NewVariance_{i}") 
#             AlterVariance_ = request.POST.get(f"AlterVariance_{i}") 
#             IssueVariance_ = request.POST.get(f"IssueVariance_{i}") 
#             TotalCharged_ = request.POST.get(f"TotalCharged_{i}") or 0

#             if ItemID_:
#                 uniform_item = HR_Inventory_Item_Master.objects.get(id=ItemID_)
#                 un_detail = HR_Inventory_Details.objects.get(HR_Inventory_Information=UN, HR_Inventory_Item_Master=uniform_item, IsDelete=False)
#                 if un_detail:
#                     un_detail.ReturnNewQuantity = ReturnNew_
#                     un_detail.ReturnAlteredQuantity = ReturnAltered_
#                     un_detail.ReturnIssuedQuantity = ReturnIssued_
#                     un_detail.NewVariance = NewVariance_
#                     un_detail.AlterVariance = AlterVariance_
#                     un_detail.IssueVariance = IssueVariance_
#                     un_detail.TotalCharged = TotalCharged_
                    
#                     un_detail.ModifyBy = UserID
#                     un_detail.save()
                    
#         UN.Return = True
#         UN.ReturnAmount = request.POST['ReturnAmount']
#         UN.save()    
        
#         ResignationData = EmpResigantionModel.objects.filter(
#             OrganizationID=OID, IsDelete=False, Emp_Code=EmployeeCode
#         )

#         ResignationData.update(
#             HK=True,
#             HKCreatedBy=UserID,
#             HKCreatedDateTime=timezone.now()
#         )
           
#         messages.success(request, "Updated Successfully")
#         return redirect("Clearance_view")

#     context = {
#         'OrganizationID': OrganizationID, 
#         'hotelapitoken': hotelapitoken, 
#         'UN': UN, 
#         'Hide_Value': Hide_Value, 
#         'uitem': uitem
#     }
#     return render(request, "HR_Inventory/HR_Inventory_Return_Request.html", context)












# @transaction.atomic
# def housekeeping_returns_pdf_api(request):

#     OrganizationID = request.GET.get("OID")
#     ID = request.GET.get("ID")

#     if not OrganizationID or not ID:
#         return HttpResponse("OID and ID are required.", status=400)

#     # Same logic you already use
#     UN = HR_Inventory_Information.objects.filter(
#         OrganizationID=OrganizationID, 
#         IsDelete=False, 
#         id=ID
#     ).first()

#     if not UN:
#         return HttpResponse("Record not found.", status=404)

#     uitem = HR_Inventory_Item_Master.objects.filter(IsDelete=False)

#     # Your existing template context
#     context = {
#         "OrganizationID": OrganizationID,
#         "UN": UN,
#         "uitem": uitem,
#         "Hide_Value": False
#     }

#     # Render your HTML template
#     html_string = render_to_string("UniformInventroy/HouseKeepingReturnRequest_PDF.html", context)

#     # Convert HTML to PDF
#     pdf_file = HTML(string=html_string).write_pdf()

#     # Return as PDF download
#     response = HttpResponse(pdf_file, content_type="application/pdf")
#     response["Content-Disposition"] = f"attachment; filename=HK_Return_{ID}.pdf"
#     return response






# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.db import transaction
# from .models import *
# from .serializers import HRInventorySerializer, InventoryDetailSerializer

# @api_view(["GET", "POST", "PUT"])
# @transaction.atomic
# def HR_Inventory_API(request, id=None):

#     OrganizationID = request.GET.get("OID") or request.data.get("OID")
#     EmployeeCode = request.GET.get("EC") or request.data.get("EmployeeCode")

#     # ---------- GET MODE ----------
#     if request.method == "GET":
#         UN = None
#         if id:
#             UN = HR_Inventory_Information.objects.filter(
#                 id=id, IsDelete=False
#             ).first()
#             if not UN:
#                 return Response({"message": "Not Found"}, status=404)

#         # Load all items
#         items = HR_Inventory_Item_Master.objects.filter(IsDelete=False)

#         details_dict = {}
#         if UN:
#             details = HR_Inventory_Details.objects.filter(
#                 HR_Inventory_Information=UN, IsDelete=False
#             )
#             details_dict = {d.HR_Inventory_Item_Master.id: d.Item_Issued for d in details}

#         item_list = []
#         for item in items:
#             item_list.append({
#                 "item_id": item.id,
#                 "item_name": item.ItemName,
#                 "Item_Issued": details_dict.get(item.id, "")
#             })

#         return Response({
#             "employee": EmployeeCode,
#             "details": item_list,
#             "UN_id": UN.id if UN else None
#         })

#     # ---------- POST MODE (Create) ----------
#     if request.method == "POST":
#         serializer = HRInventorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Created", "data": serializer.data}, status=201)
#         return Response(serializer.errors, status=400)

#     # ---------- PUT MODE (Edit) ----------
#     if request.method == "PUT":
#         UN = HR_Inventory_Information.objects.filter(id=id).first()
#         if not UN:
#             return Response({"message": "Not Found"}, status=404)

#         serializer = HRInventorySerializer(UN, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Updated", "data": serializer.data})
#         return Response(serializer.errors, status=400)
