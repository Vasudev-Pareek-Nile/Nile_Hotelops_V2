from django.shortcuts import render,redirect
import requests
from .models import CompOffApplication, Leave_Type_Master,Leave_Config_Details,Leave_Application,Leave_Process_Master,Leave_Process_Details,Emp_Leave_Balance_Master,EmpMonthLevelCreditMaster,EmpMonthLevelDebitMaster,National_Holidays,Optional_Holidays
from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail
from datetime import date,timedelta, timezone
from datetime import datetime
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db  import connection, transaction
import datetime
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from app.models import EmployeeMaster
from .models import *
from Employee_Payroll.models import Attendance_Data, WeekOffDetails
from django.utils.timezone import now

def EmployeeDataSelect(OrganizationID=None, EmployeeCode=None,Designation =None,ReportingtoDesignation =None):
    with connection.cursor() as cursor:
        cursor.execute("EXEC SP_EmployeeMaster_For_Leave @OrganizationID=%s, @EmployeeCode=%s, @Designation=%s, @ReportingtoDesignation=%s", [OrganizationID, EmployeeCode,Designation,ReportingtoDesignation])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    rowslist = [dict(zip(columns, row)) for row in rows]
    return rowslist


def Delete_Monthly_Leave_Process(request, id):
    if request.method == "POST":
        obj = get_object_or_404(Leave_Process_Master, id=id)
        obj.IsDelete = 1
        obj.save()
        messages.success(request, "Leave process marked as deleted.")
    return redirect('/Leave_Management_System/LeaveProcessDetails/')  # Replace with your actual view name
# Leave Proccess Master 

# @transaction.atomic     
# def Leave_Monthly_Carry_Forward_View(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
        
#     print("Enter in Leave_Monthly_Carry_Forward_View")

#     OrganizationID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])
#     # emp_list = EmployeeDataSelect(OrganizationID)
    
#     with transaction.atomic():
#         if request.method == "POST":
#             print("method is post")
            
#             leave_ids = request.POST.getlist('leave_ids[]')
#             for leave_id in leave_ids:
#                 credit = request.POST.get(f'credits_{leave_id}')
#                 leave_type_id = leave_id # request.POST['type']
#                 # credit = request.POST['credit']
                
#                 print("Credit:", credit)
#                 print("leave_type_id:", leave_type_id)

#                 leave_type = Leave_Type_Master.objects.get(
#                     id=leave_type_id,
#                     IsDelete=False,
#                     Is_Active = True
#                 )
#                 process = Leave_Process_Master.objects.create(
#                     OrganizationID=OrganizationID,
#                     Leave_Type_Master=leave_type, 
#                     Credit=credit, Status=False
#                 )
#                 all_emp_codes = request.POST.getlist('all_emp_codes[]')
            
#                 for empcode in all_emp_codes:
#                     if empcode is not None and empcode != '':
#                         Emp_code =   empcode 
#                         data = Leave_Process_Details.objects.create(
#                             OrganizationID=OrganizationID,
#                             Leave_Process_Master=process, 
#                             Emp_code=Emp_code
#                         )
                        
#             messages.success(request,"Leave Assigned Succesfully")
#             return redirect('LeaveProcessDetails')
#         else:
#             print("method is not post")
#             messages.error(request,"Leave Assigned Faild")
#             return redirect('Monthly_Leave_Process')
        
#     # leave_type_list = Leave_Type_Master.objects.filter(IsDelete=False, Is_Active=True)
#     # leave_type_list = Leave_Type_Master.objects.filter(IsDelete=False, Is_Active=True)

#     context = {
#         # 'Leave_Type': leave_type_list, 
#         'OrganizationID':OrganizationID,
#         # 'Emp_list': emp_list
#     }
#     return render(request, "LMS/Leave_Monthly_Carry_Forward/Leave_Monthly_Process_Master.HTML", context)
   
   
# @transaction.atomic
# def Leave_Monthly_Carry_Forward_View(request):

#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)

#     print("Enter in Leave_Monthly_Carry_Forward_View")

#     OrganizationID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])

#     if request.method == "POST":
#         print("method is post")

#         # leave_ids = request.POST.getlist('leave_ids[]')
#         leave_ids = request.POST.get('type')
#         all_emp_codes = request.POST.getlist('all_emp_codes[]')
        
#         print("leave ids:",leave_ids)
#         print("all_emp_codes:",all_emp_codes)

#         with transaction.atomic():
#             for leave_id in leave_ids:
#                 credit = request.POST.get(f'credits_{leave_id}')

#                 leave_type = Leave_Type_Master.objects.get(
#                     id=leave_id,
#                     IsDelete=False,
#                     Is_Active=True
#                 )

#                 process = Leave_Process_Master.objects.create(
#                     OrganizationID=OrganizationID,
#                     Leave_Type_Master=leave_type,
#                     Credit=credit,
#                     Status=False
#                 )

#                 for empcode in all_emp_codes:
#                     if empcode:
#                         Leave_Process_Details.objects.create(
#                             OrganizationID=OrganizationID,
#                             Leave_Process_Master=process,
#                             Emp_code=empcode
#                         )

#         messages.success(request, "Leave Assigned Successfully")
#         return redirect('LeaveProcessDetails')

#     # 👇 GET request comes here (NO redirect)
#     print("method is GET")

#     context = {
#         'OrganizationID': OrganizationID,
#     }
#     return render(
#         request,
#         "LMS/Leave_Monthly_Carry_Forward/Leave_Monthly_Process_Master.HTML",
#         context
#     )
 
 
 
@transaction.atomic
def Leave_Monthly_Carry_Forward_View(request):

    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    # print("Enter in Leave_Monthly_Carry_Forward_View")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])

    context = {
        'OrganizationID': OrganizationID,
        'UserID': UserID,
    }
    return render(
        request,
        "LMS/Leave_Monthly_Carry_Forward/Leave_Monthly_Process_Master.HTML",
        context
    )

    
from django.db.models import Prefetch
# Leave Process Details
@transaction.atomic     
def Leave_Monthly_Process_Details_View(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    ID = request.GET.get('ID')
    
    with transaction.atomic():
        if ID is not None:
            Leave_Process = Leave_Process_Master.objects.get(id=ID, OrganizationID=OrganizationID, IsDelete=False)
            Leave_Details = Leave_Process_Details.objects.filter(
                OrganizationID=OrganizationID, 
                IsDelete=False,
                Leave_Process_Master=Leave_Process.id
            )
            
            for detail in Leave_Details:
                L_id = detail.Leave_Process_Master
                balance = detail.Leave_Process_Master.Credit
                Emp_code = detail.Emp_code
                try:
                    previous_balance=0
                    
                    Leave_Balance = Emp_Leave_Balance_Master.objects.filter(
                        Leave_Type_Master=L_id.Leave_Type_Master,
                        Emp_code=Emp_code,
                        OrganizationID=OrganizationID,
                        IsDelete=False
                    )
                    
                    if Leave_Balance.exists():
                        Leave_Balance=Leave_Balance.first()
                        previous_balance = Leave_Balance.Balance
                        total = previous_balance + balance
                        Leave_Balance.Balance = total
                        Leave_Balance.save()
                        
                    else:
                        if Emp_code is not None and Emp_code != '':  
                            Leave_Balance = Emp_Leave_Balance_Master.objects.create(
                                OrganizationID=OrganizationID,
                                Leave_Type_Master=L_id.Leave_Type_Master, 
                                Emp_code=Emp_code, 
                                Balance=balance
                            )
                            
                            Leave_Credit = EmpMonthLevelCreditMaster.objects.create(
                                Leave_Type_Master=L_id.Leave_Type_Master,
                                OrganizationID=OrganizationID,
                                Emp_code=Emp_code, 
                                credit=balance
                            )

                except: #Emp_Leave_Balance_Master.DoesNotExist:
                        if Emp_code is not None and Emp_code != '':  
                            Leave_Balance = Emp_Leave_Balance_Master.objects.create(
                                OrganizationID=OrganizationID,
                                Leave_Type_Master=L_id.Leave_Type_Master, 
                                Emp_code=Emp_code, 
                                Balance=balance
                            )
                            
                EmpMonthLevelCreditMaster.objects.create(
                    Leave_Type_Master=L_id.Leave_Type_Master,
                    OrganizationID=OrganizationID,
                    Emp_code=Emp_code, credit=balance
                )
                # Leave_Credit = EmpMonthLevelCreditMaster.objects.create(
                #     Leave_Type_Master=L_id.Leave_Type_Master,
                #     OrganizationID=OrganizationID,
                #     Emp_code=Emp_code, credit=balance
                # )

            Leave_Process.Status = True
            Leave_Process.save()

    details = Leave_Process_Master.objects.filter(
        OrganizationID=OrganizationID, 
        IsDelete=False, 
        Status=False
    )
    for m in details:
        m.leave_process_details= Leave_Process_Details.objects.filter(Leave_Process_Master=m)

    context = {
        'details': details
    }
    return render(request, "LMS/Leave_Monthly_Carry_Forward/Leave_Monthly_Process_Details.html", context)


    