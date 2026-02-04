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
from .models import Leave_Type_Master,Leave_Config_Details,Leave_Process_Master,Leave_Process_Details, Emp_Leave_Balance_Master


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
# from django.http import JsonResponse
# from datetime import date
# from dateutil.relativedelta import relativedelta
# from django.db.models import Count, Q
# from django.http import JsonResponse
# from datetime import date
# from dateutil.relativedelta import relativedelta
from django.db.models import Count, Q, OuterRef, Subquery, IntegerField, Value
from django.db.models.functions import Coalesce
# from django.db.models import Count, Q
from datetime import datetime

def get_previous_month(year, month):
    if month == 1:
        return year - 1, 12
    return year, month - 1


# def get_previous_month_weekoff_compoff(org_id, year=None, month=None):
#     """
#     Returns employee-wise WeekOff & CompOff count for previous month
#     """
#     org_id=20180612060935

#     # 🔹 Default to current month if not provided
#     today = datetime.today()
#     year = year or today.year
#     month = month or today.month

#     prev_year, prev_month = get_previous_month(year, month)

#     # 🔹 Fetch all active employees
#     employees = EmployeePersonalDetails.objects.filter(
#         IsEmployeeCreated=True,
#         OrganizationID=org_id,
#         IsDelete=False
#     ).values("EmpID", "EmployeeCode")

#     employee_map = {
#         emp["EmployeeCode"]: emp["EmployeeCode"]
#         for emp in employees
#     }

#     # 🔹 Attendance aggregation (Optimized)
#     attendance_data = SalaryAttendance.objects.filter(
#         EmpID__in=employee_map.keys(),
#         month=prev_month,
#         year=prev_year,
#         OrganizationID=org_id,
#         IsDelete=False,
#         Status__in=["Week off", "Comp-off"]
#         # Status__iexact__in=["Week off", "Comp-off"]
#     ).values("EmpID").annotate(
#         WeekOffCount=Count("EmpID", filter=Q(Status__iexact="Week off")),
#         CompOffCount=Count("EmpID", filter=Q(Status__iexact="Comp-off"))
#     )

#     # 🔹 Build response
#     result = []

#     for record in attendance_data:
#         result.append({
#             "EmpID": record["EmpID"],
#             "EmployeeCode": employee_map.get(record["EmployeeCode"]),
#             "WeekOffCount": record["WeekOffCount"],
#             "CompOffCount": record["CompOffCount"],
#             "TotalOff": record["WeekOffCount"] + record["CompOffCount"]
#         })

#     for record in attendance_data:
#         result.append({
#             "EmpID": record["EmpID"],
#             "EmployeeCode": employee_map.get(record["EmpID"]),
#             "WeekOffCount": record["WeekOffCount"],
#             "CompOffCount": record["CompOffCount"],
#             "TotalOff": record["WeekOffCount"] + record["CompOffCount"]
#         })

#     return {
#         "month": prev_month,
#         "year": prev_year,
#         "employees": result
#     }




# from datetime import datetime
# from django.db.models import Count, Q


# def get_previous_month(year, month):
#     if month == 1:
#         return year - 1, 12
#     return year, month - 1


# def get_previous_month_weekoff_compoff(org_id, year=None, month=None):
def get_previous_month_weekoff_compoff(request):
    """
    Returns employee-wise WeekOff & CompOff count for previous month
    """
    
    org_id=request.GET.get('OID')
    year=request.GET.get('year')
    month=request.GET.get('month')
    # org_id=1001

    today = datetime.today()
    # year = year or today.year
    # month = month or today.month
    
    # year = 2025
    # month = 11

    # prev_year, prev_month = get_previous_month(year, month)
    prev_year = year
    prev_month = month

    # Fetch all active employees
    employees = EmployeePersonalDetails.objects.filter(
        IsEmployeeCreated=True,
        OrganizationID=org_id,
        IsDelete=False
    ).values("EmpID", "EmployeeCode")

    # 🔹 Build employee map
    employee_map = {
        emp["EmpID"]: emp["EmployeeCode"]
        for emp in employees
    }

    # Attendance aggregation
    attendance_data = SalaryAttendance.objects.filter(
        EmpID__in=employee_map.keys(),
        month=prev_month,
        year=prev_year,
        OrganizationID=org_id,
        IsDelete=False,
        Status__in=["Week off", "Comp-off"]
    ).values("EmpID").annotate(
        WeekOffCount=Count("id", filter=Q(Status__iexact="Week off")),
        CompOffCount=Count("id", filter=Q(Status__iexact="Comp-off"))
    )
    
    # Convert attendance data to dict for fast lookup
    attendance_map = {
        record["EmpID"]: record
        for record in attendance_data
    }
   
    LTID = Leave_Type_Master.objects.get(
        IsDelete=False,
        Is_Active=True,
        Type="Comp-off"
    ).id
    # print("LTID:",LTID)
    result = []

    for emp_id, emp_code in employee_map.items():
        record = attendance_map.get(emp_id, {})

        week_off = record.get("WeekOffCount", 0)
        comp_off = record.get("CompOffCount", 0)
        
        Total_Off = week_off + comp_off

        Leave_Balance = Emp_Leave_Balance_Master.objects.filter(
            Leave_Type_Master_id=LTID,
            Emp_code=emp_code,
            OrganizationID=org_id,
            IsDelete=False
        )
        logs = Comp_Off_Assign_Logs.objects.create(
            Leave_Type_Master_id=LTID,
            Emp_code=emp_code,
            OrganizationID=org_id,
            IsDelete=False
        )
        
        if Total_Off > 2:
            Assign_Balance = 2
        else:
            Assign_Balance = Total_Off
        
        if Leave_Balance.exists():
            Leave_Balance=Leave_Balance.first()
            previous_balance = Leave_Balance.Balance
            total = previous_balance + Assign_Balance
            Leave_Balance.Balance = total
            Leave_Balance.save()

        # result.append({
        #     "EmpID": emp_id,
        #     "EmployeeCode": emp_code,
        #     "WeekOffCount": week_off,
        #     "CompOffCount": comp_off,
        #     "Total_Off_week_Compoff": Total_Off,
        #     "TotalOff": week_off + comp_off,
        #     "Assign_Balance": Assign_Balance,
        #     "previous_balance": previous_balance,
        #     "total_balance": total,
        # })

    result.append({
        "Success": True,
        "msg": "The Balance is assigned",
    })

    return JsonResponse(result, safe=False)
