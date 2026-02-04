
from itertools import groupby
from operator import attrgetter
from django.shortcuts import render,redirect
from Employee_Payroll.forms import AlifFileUploadForm
from hotelopsmgmtpy.GlobalConfig import MasterAttribute,OrganizationDetail
from app.models import OrganizationMaster,EmployeeMaster

from Leave_Management_System.models import  Leave_Type_Master,Emp_Leave_Balance_Master
import calendar
import requests
from django.contrib import messages
from django.db import   transaction
from datetime import timedelta
# from datetime import datetime
# from Employee_Payroll.models import Raw_Attendance_Data, Attendance_Data, SalaryAttendance
from Leave_Management_System.models import Leave_Application
from django.db.models import Q

from django.db.models import Min, Max
# from datetime import datetime
import csv
import pandas as pd
from django.shortcuts import get_object_or_404


from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta
import datetime

from django.http import HttpResponse
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from app.views import EmployeeDataSelect,EmployeeDataSelectForSalary

from Employee_Payroll.models import *

def days_in_selected_month(month_no, year):
    if month_no == 12:
        next_month = 1
        next_month_year = year + 1
    else:
        next_month = month_no + 1
        next_month_year = year
    # start_date = datetime(year, month_no, 1)
    # end_date = datetime(next_month_year, next_month, 1)
    start_date = timezone.datetime(year, month_no, 1).date()
    end_date = timezone.datetime(next_month_year, next_month, 1).date()

    return (end_date - start_date).days
import calendar


def Week_Off_view(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')
    else:
        OrganizationID = request.session["OrganizationID"]
    
    UserID = str(request.session["UserID"])
    EmployeeCode = request.session["EmployeeCode"]
    Department_Name  =  request.session["Department_Name"]
    
    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {
        'hotel-api-token': hotelapitoken
    }
    
    # print("The Request is Reached here ----------::")
    Approval_url = "https://hotelops.in/API/PyAPI/HREmployeeListForApproval?UserID="+str(UserID)
    
    try:
        response = requests.get(Approval_url, headers=headers)
        response.raise_for_status()
        emp_list = response.json()
        emp_list.sort(key=lambda emp: emp.get('FirstName', '').lower()) 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching approval list: {e}")
                
                
    # today = datetime.today()
    today = datetime.datetime.today()
    # print(today)
    CYear = today.year
    CMonth = today.month            
    context = {'emp_list': emp_list,'CYear':range(CYear,2020,-1),'CMonth':CMonth}
    return render(request, 'LMS/Attendance_Pages/Weekoff.html', context)




def View_Attendance_Leave_View(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
     
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    EmployeeCode = request.session["EmployeeCode"] 
    
    # current_date = datetime.now()
    current_date = timezone.now()
    
    year = int(request.GET.get('year', current_date.year))
    month_no = int(request.GET.get('month_no', current_date.month))
    
    previous_month = current_date.replace(year=year, month=month_no, day=1) - timedelta(days=1)
    
   
    next_month = min(
        current_date.replace(year=year, month=month_no, day=28) + timedelta(days=4),
        timezone.now().replace(day=1)
    )
    
    if next_month.month == month_no:
        next_month = next_month.replace(day=1)
    
   
    attendance_data = Attendance_Data.objects.filter(
        OrganizationID=OrganizationID, 
        EmployeeCode=EmployeeCode,
        Date__year=year,
        Date__month=month_no,
         Date__lte=current_date,
        IsDelete=False
    ).order_by('Date')
    
    for record in attendance_data:

        update_request_exists = Update_Attendance_Request.objects.filter(
            Attendance_Data=record,
            OrganizationID=OrganizationID, 
            IsDelete=False 
        ).exists()
        record.update_request_exists = update_request_exists
          
    context = {
        'attendance_data': attendance_data,
        # 'current_month': datetime(year, month_no, 1),
        'current_month': timezone.datetime(year, month_no, 1).date(),
        'previous_month': previous_month,
        'next_month': next_month
    }
    
    return render(request, "LMS/Attendance_Pages/View_Attendance.html", context)



from app.models import DepartmentMaster
from django.db import connection
def AttendaceMonthlyReport_Leave(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
     
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
    Departments =  DepartmentMaster.objects.filter(IsDelete =False)

    I = request.GET.get('I',OrganizationID)
    GetDepartments = request.GET.get('Departments', 'All')
    # print('GetDepartments', GetDepartments)

    year = request.GET.get('year')
    if year:
        year = int(year)
    else:
        year = timezone.now().year
        
    month_no =  request.GET.get('month_no')
    if month_no:
        month_no = int(month_no)
    else:
        month_no = timezone.now().month  

    emp_list =  EmployeeDataSelectForSalary(OrganizationID,month_no,year)
    EmployeeCode = request.GET.get('EmployeeCode','All')  # Get the EmployeeCode from the form

    # print("EmployeeCode = ",EmployeeCode)
    od =Organization_Details.objects.filter(OID=OrganizationID,IsDelete=False)

    cyS=None
    try:
        if od.exists():
            cyS=od.first().EndDate
    except:
        cyS=None
   
    month_name = calendar.month_name[int(month_no)]    
    StartDate = timezone.datetime(year, month_no, 1).date()

    start_date = timezone.datetime(year, month_no, 1).date()
    # end_date = timezone.datetime(next_month_year, next_month, 1).date()
    
    if cyS is not None and cyS == 1:
        # Cycle = 1st → last day of month
        StartDate = timezone.datetime(year, month_no, 1).date()
        _, last_day = calendar.monthrange(year, month_no)
        EndDate = timezone.datetime(year, month_no, last_day).date()

    elif cyS is not None and cyS == 31:
        # Cycle = full calendar month (1 → 31 / or last day if <31)
        StartDate = timezone.datetime(year, month_no, 1).date()
        _, last_day = calendar.monthrange(year, month_no)
        EndDate = timezone.datetime(year, month_no, last_day).date()

    else:
        # Default cycle: 26th prev month → 25th current month
        if month_no == 1:
            year -= 1
            month_no = 12
        else:
            month_no -= 1
        StartDate = timezone.datetime(year, month_no, 26).date()
        EndDate = timezone.datetime(year, month_no + 1, 25) if month_no < 12 else timezone.datetime(year + 1, 1, 25).date()

        next_month = StartDate.replace(day=28) + timedelta(days=4)
        EndDate = next_month.replace(day=25)
        if month_no==12:
            month_no=1
        else:
            month_no +=  1

    # print("----------------------------------------------------------------------::")        
    # print("The End Date is here::", EndDate)        
    # print("The Start Date is here::", StartDate)        
    days = [(StartDate + timedelta(days=i)).strftime('%#d') for i in range((EndDate - StartDate).days + 1)]

    # print("the start date is here::", StartDate)
    # print("the Start Date is here::", EndDate)
    # print("the EmployeeCode is here::", EmployeeCode)
    # print("the OrganizationID is here::", OrganizationID)
    
    with connection.cursor() as cursor:
        cursor.execute("EXEC GetAttendancePivot_New %s, %s, %s, %s", [OrganizationID, StartDate, EndDate, EmployeeCode])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    rowslist = [dict(zip(columns, row)) for row in rows]
    
   
    leavetype = Leave_Type_Master.objects.filter(IsDelete=False,Is_Active=True)
    leavelist = [leave.Type for leave in leavetype]
   
    for row in rowslist:
            TotalDays = len(days)
            Presentco=0
            WeekOffCount = 0
            PresentCount = 0
            AbsentCount = 0
            Total_AR=0
            l_Count = 0
            leave_counts = {leave: 0 for leave in leavelist}
            
            for day in days:
                status = row[day]
                actual_status=None
                if status:
                    # Extract the actual status from the last part of the string
                    actual_status = status.split("^")[-1].strip()
                if actual_status is not None:
                    if actual_status.lower() == 'week off' or actual_status.lower()=='w': 
                        WeekOffCount += 1
                    elif actual_status.lower() == 'p' or actual_status.lower() == 'present':
                        PresentCount += 1
                    elif actual_status.lower() == 'co' or actual_status.lower() == 'comp-off':
                        Presentco += 1
                        Aactual_status="Comp-off"
                        leave_counts[Aactual_status] =Presentco
                    elif actual_status.lower() == 'ar':
                        Total_AR += 1 
                    elif actual_status.lower() == 'a' or actual_status == None :
                        AbsentCount += 1
                       
                    if actual_status in leavelist:
                        if actual_status.lower() != 'ar':
                            if actual_status.lower() == 'co' or actual_status.lower() == 'comp-off':
                                actual_status="Comp-off"
                                # leave_counts[actual_status] =Presentco
                            else:
                                l_Count=l_Count+1
                                leave_counts[actual_status] += 1
                        if actual_status.lower() == 'ar':
                            leave_counts[actual_status] += 1

            # for leave in leavelist:
              
            #     l_Count =  l_Count + leave_counts[leave] 
            TotalWorkingDays = WeekOffCount + PresentCount + l_Count+Total_AR+Presentco
            row['TotalWorkingDays'] =  TotalWorkingDays
            row['Present'] = PresentCount
            row['Absent'] = AbsentCount
            row['WeekOff'] = WeekOffCount
            row["Comp-off"]=Presentco
            total_no_Days_in_month = days_in_selected_month(int(month_no), int(year))
            minus = TotalDays - total_no_Days_in_month 
            if row["iscalm"]=="1":
                row['TotalPaidDays'] = TotalWorkingDays - ( minus )
            else:
                row['TotalPaidDays'] = TotalWorkingDays
            

            row['leave_counts'] = leave_counts 
            row['l_Count'] = l_Count 
        
        
    # today = datetime.today()
    today = datetime.datetime.today()
    CYear = today.year
    CMonth = today.month      

    context = {
        'CYear':range(CYear,2020,-1),'CMonth':CMonth,
        'month_no':month_no,
        'year':year,
        'month_name':month_name,
        'rowslist':rowslist,
        'days':days,
        'leavelist':leavelist,
        'emp_list':emp_list,
        'EmployeeCode':EmployeeCode,
        'Departments':Departments,
        'StartDate':StartDate,
        'EndDate':EndDate,
        'EmployeeCode':EmployeeCode,
        'OrganizationID':OrganizationID,
        'GetDepartments':GetDepartments,
    }
     
    return render(request, "LMS/Attendance_Pages/AttendaceMonthlyReport.html", context)


# Attendance  
@transaction.atomic     
def AttendanceProcess(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    # emp_list =  EmployeeMaster.objects.filter(OrganizationID=OrganizationID,IsDelete=False).order_by('EmployeeCode')
    emp_list = EmployeeDataSelect(OrganizationID)
   
    try:
        org_obj = Organization_Details.objects.get(OID=OrganizationID, IsDelete=False)
        S_EndDate = org_obj.EndDate
    except Organization_Details.DoesNotExist:
        S_EndDate = 26

    # current_date = datetime.now().date()
    current_date = timezone.now().date()
    #current_date =  datetime.strptime("2024-04-26", "%Y-%m-%d").date()
    current_date= timezone.datetime(current_date.year, current_date.month, 25).date()

    _, last_day_of_month = calendar.monthrange(current_date.year, current_date.month)

    if S_EndDate is not None:
        safe_day = min(S_EndDate, last_day_of_month)
        start_date = current_date.replace(day=safe_day)
    else:
        safe_day = min(26, last_day_of_month)
        start_date = current_date.replace(day=safe_day)

    # _, last_day_of_month = calendar.monthrange(current_date.year, current_date.month)
    end_date = current_date.replace(day=last_day_of_month)
    with transaction.atomic():
            if request.method == "POST":
                all_emp_codes = request.POST.getlist('all_emp_codes[]')
                all_emp_ids  = request.POST.getlist('all_emp_id[]')
                # print("all emp code:", all_emp_codes)
                # print("all emp id:", all_emp_ids)
                start_date = timezone.datetime.strptime(request.POST.get('Start_Date'), "%Y-%m-%d").date()
                To_Date = timezone.datetime.strptime(request.POST.get('To_Date'), "%Y-%m-%d").date()
                # print(f"Date is Start_Date:{start_date} -- End_Date:{To_Date}")
                end_date=To_Date
                current_date = start_date
                # print("current_date is here:",current_date)
                while current_date <= end_date:
                    # print("Me with current_date:: in whiile Loop")
                    for emp_code, emp_id in zip(all_emp_codes, all_emp_ids):
                        # print(f"EmpCode: {emp_code} and EmpID:{emp_id}")
                        if emp_code:
                            Att_obj = Attendance_Data.objects.update_or_create(
                                EmployeeCode=emp_code,
                                EmpID=emp_id,
                                Date=current_date,
                                In_Time='00:00',
                                Out_Time='00:00',
                                Duty_Hour='00:00',
                                OrganizationID=OrganizationID,
                                CreatedBy=UserID,
                                Status='Present',
                                IsUpload=False,
                                IsDelete=False
                            )

                    current_date += timedelta(days=1)

                messages.success(request,"Attendace Record Created Successfully !")
                return redirect('Daily_Attendace_Leave')
    context = {
        'Emp_list': emp_list, 
        'Start_Date': start_date,
        'To_Date': end_date,
    }
    return render(request, "LMS/Attendance_Pages/AttendanceProcess.html", context)




def Daily_Attendace_Leave_View(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
     
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
    emp_list = EmployeeDataSelect(OrganizationID)
    
    
    Q_Date  =  request.GET.get('Q_Date')

    attendance_data = Attendance_Data.objects.filter(
        OrganizationID=OrganizationID, 
        Date= Q_Date,
        IsDelete=False
    ).order_by('Date','EmployeeCode')
    
    # for record in attendance_data:
    #     update_request_exists = Update_Attendance_Request.objects.filter(Attendance_Data=record,OrganizationID=OrganizationID, 
    #                                         IsDelete=False ).exists()
    #     record.update_request_exists = update_request_exists

    for record in attendance_data:
        for emp in emp_list:
            if emp['EmployeeCode'] == record.EmployeeCode:
                
                record.EmployeeName = emp['EmpName']
                break
        
        update_request_exists = Update_Attendance_Request.objects.filter(
            Attendance_Data=record,
            OrganizationID=OrganizationID,
            IsDelete=False
        ).exists()
        
        # update_request_exists = Update_Attendance_Request.objects.filter(
        #     Attendance_Data=record,
        #     OrganizationID=OrganizationID,
        #     IsDelete=False
        # ).exists()
        record.update_request_exists = update_request_exists

          
    context = {
        'attendance_data': attendance_data,
        'Q_Date':Q_Date
    }
    
    return render(request, "LMS/Attendance_Pages/Daily_Attendace.html", context)






def Excel_Attendance_Upload_View(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    context = {}
    # return render(request, "LMS/Attendance/Alifupload_csv.html", {'form':form})
    return render(request, "LMS/Attendance_Pages/Excel_Attendance_Upload.html", context)


def Excel_Attendance_Upload_CSV_Api(request):
    if request.method != "POST":
        # print("request method is not post")
        return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
    
    OID = request.session.get("OrganizationID") or 0
    

    excel_file = request.FILES.get("excel_file")

    if not excel_file:
        return JsonResponse({
            "status": "error",
            "message": str(e),
            "errors": []
        }, status=500)


    try:
        # df = pd.read_excel(excel_file)
        df = pd.read_excel(excel_file, header=6)
        df.columns = df.columns.str.strip().str.upper()

        required_columns = {"ID", "INDATE", "INTIME", "OUTTIME", "DAYTOTAL", "DAYSTATUS"}
        if not required_columns.issubset(df.columns):
            return JsonResponse({
                "status": "error",
                "message": f"Missing columns: {required_columns - set(df.columns)}"
            }, status=400)

        created_count = 0
        updated_count = 0
        errors = []

        with transaction.atomic():
            for index, row in df.iterrows():
                try:
                    # employee_code = str(row["ALPHANUMERIC"]).strip()
                    if OID == '2120':
                        # print("rd delhi is here")
                        employee_code = str(row["ALPHANUMERIC"]).strip()
                    else:
                        employee_code = str(row["ID"]).strip()
                    # attendance_date = pd.to_datetime(row["INDATE"]).date()
                    
                    attendance_date = pd.to_datetime(
                        row["INDATE"],
                        dayfirst=True,
                        errors="coerce"
                    ).date()

                    attendance, created = Excel_Attendance_Upload_Punch_Record.objects.get_or_create(
                        EmployeeCode=employee_code,
                        Date=attendance_date,
                        OrganizationID=OID,
                        defaults={
                            "IsDelete": False,
                        }
                    )
                    
                    STATUS_MAP = {
                        "A": "Absent",
                        "P": "Present",
                        "P*": "Present",
                    }
                    
                    attendance.In_Time = str(row["INTIME"]) if pd.notna(row["INTIME"]) else None
                    attendance.Out_Time = str(row["OUTTIME"]) if pd.notna(row["OUTTIME"]) else None
                    attendance.Duty_Hour = str(row["DAYTOTAL"]) if pd.notna(row["DAYTOTAL"]) else None
                    # attendance.Status = str(row["DAYSTATUS"]) if pd.notna(row["DAYSTATUS"]) else None
                    
                    raw_status = str(row["DAYSTATUS"]).strip().upper() if pd.notna(row["DAYSTATUS"]) else None
                    attendance.Status = STATUS_MAP.get(raw_status, raw_status)


                    attendance.IsUpload = True
                    attendance.IsAttendanceModified = True
                    attendance.OrganizationID = OID
                    attendance.save()
                    

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                        
                    # 🔥 Sync to Attendance_Data
                    sync_attendance_async(attendance)
                        
                except Exception as row_err:
                    print("the data is not saved")
                    errors.append(f"Row {index+2}: {str(row_err)}")

        return JsonResponse({
            "status": "success",
            "created_records": created_count,
            "updated_records": updated_count,
            "errors": errors
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)


from django.utils import timezone
# from .models import Attendance_Data


import threading

def sync_attendance_async(attendance):
    thread = threading.Thread(
        target=sync_attendance_data_from_punch,
        args=(attendance,)
    )
    thread.daemon = True
    thread.start()


# def sync_attendance_data_from_punch(attendance):
#     """
#     Sync Excel_Attendance_Upload_Punch_Record
#     to Attendance_Data table
#     """

#     attendance_data, created = Attendance_Data.objects.get_or_create(
#         EmployeeCode=attendance.EmployeeCode,
#         Date=attendance.Date,
#         defaults={
#             "IsDelete": False,
#             "OrganizationID": attendance.OrganizationID,
#             "CreatedDateTime": timezone.now(),
#         }
#     )
#     # HARD STOP: do not touch Leave data
#     if not created and attendance_data.Is_Leave:
#         return attendance_data, False
    
    
#     attendance_data.In_Time = attendance.In_Time
#     attendance_data.Out_Time = attendance.Out_Time
#     attendance_data.Duty_Hour = attendance.Duty_Hour
#     attendance_data.Status = attendance.Status
#     # attendance_data.IsUpload = True
#     attendance_data.ModifyDateTime = timezone.now()

#     attendance_data.save()

#     return attendance_data, created

from django.db import transaction

def sync_attendance_data_from_punch(attendance):
    with transaction.atomic():
        attendance_data = Attendance_Data.objects.select_for_update().filter(
            EmployeeCode=attendance.EmployeeCode,
            Date=attendance.Date
        ).first()

        if not attendance_data:
            attendance_data = Attendance_Data.objects.create(
                EmployeeCode=attendance.EmployeeCode,
                Date=attendance.Date,
                OrganizationID=attendance.OrganizationID,
                IsDelete=False,
                CreatedDateTime=timezone.now(),
            )

        if attendance_data.Is_Leave:
            return

        attendance_data.In_Time = attendance.In_Time
        attendance_data.Out_Time = attendance.Out_Time
        attendance_data.Duty_Hour = attendance.Duty_Hour
        attendance_data.Status = attendance.Status
        attendance_data.ModifyDateTime = timezone.now()
        attendance_data.save()



from django.urls import reverse

@transaction.atomic
def Update_Attendance_HR(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
     
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    id = request.GET.get('ID')
    
    obj = Attendance_Data.objects.get(id=id)
    pre_status = obj.Status
    leave_type = Leave_Type_Master.objects.filter(Is_Active=True,IsDelete=False)
    
    with transaction.atomic():
        if request.method == "POST":
                Page = request.POST.get('Page')
                emp = request.POST.get('emp')
                year = request.POST.get('year')
                month_no = request.POST.get('month_no')


           
                obj.In_Time = request.POST.get('in') 
                obj.Out_Time =  request.POST.get('Out')
                Q_Date = obj.Date
                
                Status =  request.POST.get('Status')
                if Status == "":
                    obj.Status = pre_status
                else:
                    obj.Status = Status    
                obj.ModifyBy = UserID
                obj.save()
            
                messages.success(request,"Updated Successfully")
                if Page == "VESD":
                    return redirect(reverse('View_Emmployee_Salary_Details') + f'?emp={emp}&year={year}&month_no={month_no}')
                    
                if Page  == "DA":
                    return redirect(reverse('Daily_Attendace_Leave') + f'?Q_Date={Q_Date}') 
                    

    context ={'obj':obj,'leave_type':leave_type}
    return render(request,"LMS/Attendance_Pages//Update_Attendance_HR.html", context)
