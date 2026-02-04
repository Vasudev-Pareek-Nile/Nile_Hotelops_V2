from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .services import EmployeeDataSelect   # adjust import path
# from django.shortcuts import render,redirect
# import requests
# from .models import CompOffApplication, Leave_Type_Master,Leave_Config_Details,Leave_Application,Leave_Process_Master,Leave_Process_Details,Emp_Leave_Balance_Master,EmpMonthLevelCreditMaster,EmpMonthLevelDebitMaster,National_Holidays,Optional_Holidays
# from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail
# from datetime import date,timedelta, timezone
# from datetime import datetime
# from django.contrib import messages
# from django.shortcuts import get_object_or_404
from django.db  import connection, transaction
# import datetime
# from django.http import HttpResponse, JsonResponse
# from django.db.models import Q
# from app.models import EmployeeMaster
# from .models import *
# from Employee_Payroll.models import Attendance_Data, WeekOffDetails
# from django.utils.timezone import now

def EmployeeDataSelect(OrganizationID=None, EmployeeCode=None,Designation =None,ReportingtoDesignation =None):
    with connection.cursor() as cursor:
        cursor.execute("EXEC SP_EmployeeMaster_For_Leave_Api @OrganizationID=%s, @EmployeeCode=%s, @Designation=%s, @ReportingtoDesignation=%s", [OrganizationID, EmployeeCode,Designation,ReportingtoDesignation])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    rowslist = [dict(zip(columns, row)) for row in rows]
    return rowslist



class Employee_Data_API(APIView):
    def get(self, request):
        try:
            OrganizationID = request.query_params.get('OID')
            EmployeeCode = request.query_params.get('EmployeeCode')
            Designation = request.query_params.get('Designation')
            ReportingtoDesignation = request.query_params.get('ReportingtoDesignation')
            
            print('OrganizationID:',OrganizationID)

            data = EmployeeDataSelect(
                OrganizationID=OrganizationID,
                EmployeeCode=EmployeeCode,
                Designation=Designation,
                ReportingtoDesignation=ReportingtoDesignation
            )

            return Response({
                "success": True,
                "count": len(data),
                "data": data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)



from django.http import JsonResponse
from .models import Leave_Config_Details
from django.db.models import F


def Leave_Config_Details_Api(request):
    OrganizationID = request.session["OrganizationID"]
    
    data = Leave_Config_Details.objects.filter(
        IsDelete=False,
        IsMonthly=True,
        IsAutoCredit=True,
        Carry_FWD=True,
        OrganizationID=OrganizationID,
        Leave_Type_Master__IsDelete=False
    ).values(
        ML=F('MonthlyLeave'),
        type=F('Leave_Type_Master__Type'),
        type_id=F('Leave_Type_Master__id')
    )

    return JsonResponse({
        "status": True,
        "data": list(data)
    })



from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Leave_Type_Master,Leave_Config_Details,Leave_Process_Master,Leave_Process_Details, Emp_Leave_Balance_Master, Comp_Off_Assign_Logs


@require_POST
@transaction.atomic
def Leave_Monthly_Carry_Forward_View_Api(request):
    OrganizationID = request.POST.get('OID')
    leave_UserID = request.POST.get('UserID')
    leave_id = request.POST.get('type')
    credit_Val = request.POST.get('credit')
    all_emp_codes = request.POST.getlist('all_emp_codes[]')
    
    if not leave_id:
        return JsonResponse({
            "success": False,
            "message": "Leave type is required"
        }, status=400)

    if not all_emp_codes:
        return JsonResponse({
            "success": False,
            "message": "Please select at least one employee"
        }, status=400)

    try:
        leave_type = Leave_Type_Master.objects.get(
            id=leave_id,
            IsDelete=False,
            Is_Active=True
        )

        process = Leave_Process_Master.objects.create(
            OrganizationID=OrganizationID,
            Leave_Type_Master=leave_type,
            Credit=credit_Val,
            Status=False
        )

        details = [
            Leave_Process_Details(
                OrganizationID=OrganizationID,
                Leave_Process_Master=process,
                Emp_code=empcode
            )
            for empcode in all_emp_codes if empcode
        ]

        Leave_Process_Details.objects.bulk_create(details)

        return JsonResponse({
            "success": True,
            "message": "Leave assigned successfully"
        })

    except Leave_Type_Master.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Invalid leave type"
        }, status=404)

    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)




from django.http import JsonResponse
from django.db import transaction
from django.views.decorators.http import require_GET

@require_GET
@transaction.atomic
def employee_leave_balance_api(request):

    OrganizationID = request.GET.get('OID')
    UserID = request.GET.get('UserID')
    UserType = request.GET.get('UserType')
    Emp_code = request.GET.get('ID')

    if not Emp_code or not UserType:
        return JsonResponse({
            "success": False,
            "message": "Required parameters are missing"
        }, status=400)

    if UserType == "CEO":
        leave_balance_qs = Emp_Leave_Balance_Master.objects.filter(
            IsDelete=False,
            Emp_code=Emp_code
        ).order_by('Leave_Type_Master_id')
    else:
        leave_balance_qs = Emp_Leave_Balance_Master.objects.filter(
            OrganizationID=OrganizationID,
            IsDelete=False,
            Emp_code=Emp_code
        ).order_by('Leave_Type_Master_id')


    data = [
        {
            "Leave_Type": lb.Leave_Type_Master.Type,
            "Balance": float(lb.Balance),
        }
        for lb in leave_balance_qs.order_by('Leave_Type_Master_id')
    ]

    return JsonResponse({
        "success": True,
        "count": len(data),
        "data": data
    })
    
    
from django.http import JsonResponse
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models import Count, Q
from Employee_Payroll.models import SalaryAttendance
from HumanResources.models import EmployeePersonalDetails
from django.db.models import Count, Q, OuterRef, Subquery, IntegerField, Value
from django.db.models.functions import Coalesce
from datetime import datetime

# def get_previous_month(year, month):
#     if month == 1:
#         return year - 1, 12
#     return year, month - 1


# from django.db import transaction
# from django.db.models import Count, Q
# from django.http import JsonResponse


# def get_previous_month_weekoff_compoff(request):
#     org_id = request.GET.get('OID')
#     user_year = int(request.GET.get('year'))
#     user_month = int(request.GET.get('month'))
    
#     today = datetime.today()
#     user_year = user_year or today.year
#     user_month = user_month or today.month

#     year, month = get_previous_month(user_year, user_month)

#     # Employees
#     employees = EmployeePersonalDetails.objects.filter(
#         IsEmployeeCreated=True,
#         OrganizationID=org_id,
#         IsDelete=False
#     ).values("EmpID", "EmployeeCode")

#     employee_map = {e["EmpID"]: e["EmployeeCode"] for e in employees}
#     emp_ids = employee_map.keys()

#     # Attendance aggregation
#     attendance_map = {
#         row["EmpID"]: row
#         for row in SalaryAttendance.objects.filter(
#             EmpID__in=emp_ids,
#             month=month,
#             year=year,
#             OrganizationID=org_id,
#             IsDelete=False,
#             Status__in=["Week off", "Comp-off"]
#         ).values("EmpID").annotate(
#             WeekOffCount=Count("id", filter=Q(Status__iexact="Week off")),
#             CompOffCount=Count("id", filter=Q(Status__iexact="Comp-off")),
#         )
#     }

#     # Leave Type ID
#     LTID = Leave_Type_Master.objects.only("id").get(
#         IsDelete=False,
#         Is_Active=True,
#         Type="Comp-off"
#     ).id

#     # Leave balances (ONE QUERY)
#     leave_balance_map = {
#         lb.Emp_code: lb
#         for lb in Emp_Leave_Balance_Master.objects.filter(
#             Leave_Type_Master_id=LTID,
#             Emp_code__in=employee_map.values(),
#             OrganizationID=org_id,
#             IsDelete=False
#         )
#     }

#     existing_logs = set(
#         Comp_Off_Assign_Logs.objects.filter(
#             EmpID__in=emp_ids,
#             OrganizationID=org_id,
#             Year=year,
#             Month=month,
#             Leave_Type_Master_id=LTID,  # 🔥 REQUIRED
#             Is_Assigned=True,
#             IsDelete=False
#         ).values_list("EmpID", flat=True)
#     )


#     balances_to_update = []
#     logs_to_create = []
#     with transaction.atomic():
#         for emp_id, emp_code in employee_map.items():

#             already_assigned = Comp_Off_Assign_Logs.objects.filter(
#                 EmpID=emp_id,
#                 OrganizationID=org_id,
#                 Year=year,
#                 Month=month,
#                 Leave_Type_Master_id=LTID,
#                 Is_Assigned=True,
#                 IsDelete=False
#             ).exists()

#             if already_assigned:
#                 continue  

#             record = attendance_map.get(emp_id, {})
#             total_off = record.get("WeekOffCount", 0) + record.get("CompOffCount", 0)

#             assign_balance = min(total_off, 2)
#             if assign_balance <= 0:
#                 continue

#             lb = leave_balance_map.get(emp_code)
#             if not lb:
#                 continue

#             lb.Balance += assign_balance
#             balances_to_update.append(lb)

#             logs_to_create.append(
#                 Comp_Off_Assign_Logs(
#                     EmpID=emp_id,
#                     EmployeeCode=emp_code,
#                     Leave_Type_Master_id=LTID,
#                     OrganizationID=org_id,
#                     Year=year,
#                     Month=month,
#                     Is_Assigned=True,
#                     Message="The Balance is assigned"
#                 )
#             )

#         if balances_to_update:
#             Emp_Leave_Balance_Master.objects.bulk_update(
#                 balances_to_update, ["Balance"]
#             )

#         if logs_to_create:
#             Comp_Off_Assign_Logs.objects.bulk_create(logs_to_create)

#     return JsonResponse({
#         "Success": True,
#         "msg": "Comp-off balance assigned successfully"
#     })



