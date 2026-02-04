
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
from .views import EmployeeDataSelect

from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


def format_time(time_str):
    """Convert '13:21:03.0000000' to '01:21 PM'."""
    if time_str:
        try:
            return datetime.strptime(time_str[:8], "%H:%M:%S").strftime("%I:%M %p")
        except ValueError:
            return time_str  # Return original if parsing fails
    return ""



@api_view(['GET'])
def Employee_Dashboard_Leave_API(request):
    
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    # Token checks
    if not AccessToken:
        return JsonResponse({'error': 'Token not found'}, status=400)
    if AccessToken != Fixed_Token:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    

    # print("Employee_Dashboard_Leave_API IS CALLED")
    OrganizationID = request.GET.get("OID")
    UserID = request.GET.get("UserID")
    UserDepartment = request.GET.get("Department_Name")
    UserDesi_Value = request.GET.get("Desi_Name")
    UserType = request.GET.get("UserType")
    
    
    if UserDesi_Value == 'Founder & CEO':
        UserDesignation = 'CEO'
    else:
        UserDesignation = UserDesi_Value
        
    # Defaults
    Selected_Year = request.GET.get('year', timezone.now().year)
    Selected_Month = request.GET.get('month', timezone.now().month)

    # Validate year & month
    # try:
    #     Selected_Year = int(Selected_Year)
    # except (ValueError, TypeError):
    #     Selected_Year = timezone.now().year

    # try:
    #     Selected_Month = int(Selected_Month)
    # except (ValueError, TypeError):
    #     Selected_Month = timezone.now().month

    # Basic validation
    if not OrganizationID or not UserDesignation:
        return Response(
            {"status": False, "message": "OrganizationID and Designation are required"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    Empobjs_filter = {
        "ReportingtoDesigantion": UserDesignation,
        "IsSecondary": False,     
        "IsDelete": False,     
    }
    
    if OrganizationID != '3':
        Empobjs_filter["OrganizationID"] = OrganizationID
        # print("I am filtring it here::", OrganizationID)

    # Fetch Employees
    Empobjs = EmployeeMaster.objects.filter(
        **Empobjs_filter
    ).values(
        'EmployeeCode',
        'EmpName',
        'ReportingtoDesigantion',
        'Department',
        'Designation'
    )

    employee_data = {}

    for emp in Empobjs:
        emp_code = emp["EmployeeCode"]
        # print("EmplpyeeCode is here::", emp_code)
        employee_data[emp_code] = {
            "EmployeeCode": emp_code,
            "EmployeeName": emp["EmpName"],
            "LeaveData": []
        }

    today = timezone.now().date()

    leave_filter = {
        # "OrganizationID": OrganizationID,
        "IsDelete": False,
        "Emp_code__in": employee_data.keys(),
        # "Start_Date__year": Selected_Year,
        "End_Date__gte": today,      
        "Status__in": [0, 1],       
    }
    
    
    if OrganizationID != '3':
        leave_filter["OrganizationID"] = OrganizationID
        # print("I am filtring it here::", OrganizationID)
        

    leave_data = Leave_Application.objects.filter(**leave_filter)

    for leave in leave_data:
        emp_code = leave.Emp_code
        leave_days = (
            (leave.End_Date - leave.Start_Date).days + 1
            if leave.Start_Date and leave.End_Date else 0
        )

        if emp_code not in employee_data:
            employee_data[emp_code] = {
                "EmployeeCode": emp_code,
                "EmployeeName": "Unknown",
                "LeaveData": []
            }

        employee_data[emp_code]["LeaveData"].append({
            "title": leave.Leave_Type_Master.Type,
            "Leavestatus": leave.Status,
            "start": leave.Start_Date.strftime('%d-%m-%Y'),
            "end": leave.End_Date.strftime('%d-%m-%Y'),
            "leave_days": leave_days,
            "type": "leave",
            "Reason": leave.Reason,
            "Total_credit": leave.Total_credit,
            "ReportingtoDesigantion": leave.ReportingtoDesigantion,
            "Remark": leave.Remark,
        })

    filtered_employees = [
        emp for emp in employee_data.values()
        if emp["LeaveData"]  
    ]

    return Response({
        "status": True,
        # "year": Selected_Year,
        # "month": Selected_Month,
        "data": filtered_employees
    }, status=status.HTTP_200_OK)





# # modified
# def Employee_Dashboard_Leave_Api(request):

#     OrganizationID = request.GET.get("OrganizationID")
#     UserID = request.GET.get("UserID")
#     UserDepartment = request.GET.get("Department_Name")
#     UserDesignation = request.GET.get("Desi_Name")
#     UserType = request.GET.get("UserType")
    
#     Selected_Year = request.GET.get('year', timezone.now().year)  # Default to current year
#     Selected_Month = request.GET.get('month', timezone.now().month)  # Default to current month
#     # EmployeeCode = request.GET.get('EmployeeCode', 'All')  # Default to 'All'


#     # Convert Selected_Year and Selected_Month to integers (if they exist)
#     try:
#         Selected_Year = int(Selected_Year)
#     except (ValueError, TypeError):
#         Selected_Year = timezone.now().year  # Default to current year if invalid

#     try:
#         Selected_Month = int(Selected_Month)
#     except (ValueError, TypeError):
#         Selected_Month = timezone.now().month  # Default to current month if invalid

#     # Fetch Employee Personal Details
#     # Empobjs = EmployeePersonalDetails.objects.filter(
#     #     IsDelete=False, OrganizationID=OrganizationID, IsEmployeeCreated=True
#     # ).values('EmployeeCode', 'Prefix', 'FirstName', 'MiddleName', 'LastName')
    
#     Empobjs = EmployeeMaster.objects.filter(
#         ReportingtoDesigantion=UserDesignation,
#         OrganizationID=OrganizationID, 
#         IsSecondary=False, 
#         IsDelete=False, 
#     ).values('EmployeeCode', 'EmpName', "ReportingtoDesigantion","Department","Designation" )

#     employee_data = {}
#     for emp in Empobjs:
#         emp_code = emp["EmployeeCode"]
#         full_name = f"{emp['FirstName']} {emp['MiddleName']} {emp['LastName']}".strip()
        
#         employee_data[emp_code] = {
#             "EmployeeCode": emp_code,
#             "EmployeeName": full_name,
#             "LeaveData": [],  # Initialize an empty list for attendance
#         }
        
#     leave_data = Leave_Application.objects.filter(
#         OrganizationID=OrganizationID,
#         ReportingtoDesigantion=UserDesignation,
#         IsDelete=False,
#         Start_Date__year=Selected_Year,
#         Start_Date__month=Selected_Month,
#     ).distinct()


#     for leave in leave_data:
#         emp_code = leave.Emp_code
#         leave_days = (leave.End_Date - leave.Start_Date).days + 1 if leave.Start_Date and leave.End_Date else 0

#         if emp_code not in employee_data:
#             employee_data[emp_code] = {
#                 "EmployeeCode": emp_code,
#                 "EmployeeName": "Unknown",
#                 "Attendance": [],
#             }

#         leave_dict = {
#             'title': leave.Leave_Type_Master.Type,
#             'Leavestatus': leave.Status,
#             'start': leave.Start_Date.strftime('%d-%m-%Y'),
#             'end': leave.End_Date.strftime('%d-%m-%Y'),
#             'leave_Days': leave_days,
#             'type': 'leave',
#             'Reason': leave.Reason,
#             'Total_credit': leave.Total_credit,
#             'ReportingtoDesigantion': leave.ReportingtoDesigantion,
#             'Remark': leave.Remark,
#         }

#         employee_data[emp_code]["LeaveData"].append(leave_dict)

#     return employee_data





# # oldest
# def Employee_Dashboard(request):

#     OrganizationID = request.GET.get("OrganizationID")
#     UserID = request.GET.get("UserID")
#     UserDepartment = request.GET.get("Department_Name")
#     UserDesignation = request.GET.get("Desi_Name")
#     UserType = request.GET.get("UserType")
    
#     Selected_Year = request.GET.get('year', timezone.now().year)  # Default to current year
#     Selected_Month = request.GET.get('month', timezone.now().month)  # Default to current month
#     # EmployeeCode = request.GET.get('EmployeeCode', 'All')  # Default to 'All'


#     # Convert Selected_Year and Selected_Month to integers (if they exist)
#     try:
#         Selected_Year = int(Selected_Year)
#     except (ValueError, TypeError):
#         Selected_Year = timezone.now().year  # Default to current year if invalid

#     try:
#         Selected_Month = int(Selected_Month)
#     except (ValueError, TypeError):
#         Selected_Month = timezone.now().month  # Default to current month if invalid

#     # Fetch Employee Personal Details
#     # Empobjs = EmployeePersonalDetails.objects.filter(
#     #     IsDelete=False, OrganizationID=OrganizationID, IsEmployeeCreated=True
#     # ).values('EmployeeCode', 'Prefix', 'FirstName', 'MiddleName', 'LastName')
    
#     Empobjs = EmployeeMaster.objects.filter(
#         ReportingtoDesigantion=UserDesignation,
#         OrganizationID=OrganizationID, 
#         IsSecondary=False, 
#         IsDelete=False, 
#     ).values('EmployeeCode', 'Prefix', 'FirstName', 'MiddleName', 'LastName')

#     # Create a dictionary mapping EmployeeCode to full name
#     employee_data = {}
#     for emp in Empobjs:
#         emp_code = emp["EmployeeCode"]
#         full_name = f"{emp['FirstName']} {emp['MiddleName']} {emp['LastName']}".strip()
        
#         employee_data[emp_code] = {
#             "EmployeeCode": emp_code,
#             "EmployeeName": full_name,
#             "Attendance": [],  # Initialize an empty list for attendance
#         }

#     attendance_data = Attendance_Data.objects.filter(
#         OrganizationID=OrganizationID,
#         IsDelete=False,
#         Date__year=Selected_Year, 
#         Date__month=Selected_Month,
#         # EmployeeCode=Emp_code  # Restrict normal users to their own data
#     ).distinct()


#     if attendance_data.exists():  # Check if data exists
#         for attendance in attendance_data:
#             emp_code = attendance.EmployeeCode

#             if emp_code not in employee_data:
#                 employee_data[emp_code] = {
#                     "EmployeeCode": emp_code,
#                     "EmployeeName": "Unknown",  # Default name if not found
#                     "Attendance": [],
#                 }

#             # Add attendance data
#             employee_data[emp_code]["Attendance"].append({
#                 'title': attendance.Status,
#                 'in_time': format_time(attendance.In_Time),
#                 'out_time': format_time(attendance.Out_Time),
#                 's_in_time': format_time(attendance.S_In_Time),
#                 's_out_time': format_time(attendance.S_Out_Time),
#                 'duty_hours': attendance.Duty_Hour,
#                 'status': attendance.Status if attendance.Status else "",
#                 'type': 'attendance',
#                 'Date': attendance.Date,  # Store as datetime for sorting
#                 'DateFormatted': attendance.Date.strftime('%d-%m-%Y'),
#             })

#             for emp_code in employee_data:
#                 employee_data[emp_code]["Attendance"].sort(key=lambda x: x["Date"])  # Oldest date first
#     else:
#         attendance = None



    
#     leave_data = Leave_Application.objects.filter(
#         OrganizationID=OrganizationID,
#         IsDelete=False,
#         Start_Date__year=Selected_Year,
#         Start_Date__month=Selected_Month,
#         # Emp_code=Emp_code  # Restrict normal users to their own data
#     ).distinct()


#     for leave in leave_data:
#         emp_code = leave.Emp_code
#         leave_days = (leave.End_Date - leave.Start_Date).days + 1 if leave.Start_Date and leave.End_Date else 0
#         # print('leave days are here ------ ',leave_days)

#         # Ensure the employee exists in employee_data
#         if emp_code not in employee_data:
#             employee_data[emp_code] = {
#                 "EmployeeCode": emp_code,
#                 "EmployeeName": "Unknown",
#                 "Attendance": [],
#             }

#         leave_dict = {
#             'title': leave.Leave_Type_Master.Type,
#             'Leavestatus': leave.Status,
#             'start': leave.Start_Date.strftime('%d-%m-%Y'),
#             'end': leave.End_Date.strftime('%d-%m-%Y'),
#             'leave_Days': leave_days,
#             'type': 'leave',
#             'Reason': leave.Reason,
#             'Total_credit': leave.Total_credit,
#             'ReportingtoDesigantion': leave.ReportingtoDesigantion,
#             'Remark': leave.Remark,
#         }

#         employee_data[emp_code]["Attendance"].append(leave_dict)


#     # Prepare Context
#     context = {
#         'employee_data': employee_data,  # Single dictionary with EmployeeCode & Name
#     }

#     return render(request, "LMS/DASHBOARD/Employee_Dashboard.html", context)
