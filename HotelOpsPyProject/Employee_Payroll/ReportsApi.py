import pdfkit
import calendar
from .views import *
from datetime import datetime
from django.db import connection
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime, timedelta
from app.models import OrganizationMaster
from django.template.loader import get_template
from Employee_Payroll.models import SalaryAttendance, Organization_Details
from app.views import EmployeeDataSelectForSalary
from .views import days_in_selected_month



def MonthlyAttendenceReport_Pdf_View(request):
    OrganizationID = request.GET.get('OID')
    year = request.GET.get('year')
    month_no = request.GET.get('month_no')
    GetDepartments = request.GET.get('dpt', 'All')
    EmployeeCode = request.GET.get('EmpCode', 'All')

    if year:
        year = int(year)
    else:
        year = datetime.now().year

    if month_no:
        month_no = int(month_no)
    else:
        month_no = datetime.now().month  

    emp_list = EmployeeDataSelectForSalary(OrganizationID, month_no, year)
    Org_Name = OrganizationMaster.objects.filter(
        OrganizationID=OrganizationID, IsDelete=False, IsNileHotel=True
    ).only('OrganizationName').first()

    od = Organization_Details.objects.filter(OID=OrganizationID, IsDelete=False)
    cyS = od.first().EndDate if od.exists() else None

    month_name = calendar.month_name[int(month_no)]
    StartDate = datetime(year, month_no, 1)

    if cyS == 1 or cyS == 31:
        _, last_day = calendar.monthrange(year, month_no)
        EndDate = datetime(year, month_no, last_day)
    else:
        if month_no == 1:
            year -= 1
            month_no = 12
        else:
            month_no -= 1
        StartDate = datetime(year, month_no, 26)
        next_month = StartDate.replace(day=28) + timedelta(days=4)
        EndDate = next_month.replace(day=25)
        month_no = 1 if month_no == 12 else month_no + 1

    days = [(StartDate + timedelta(days=i)).strftime('%#d') for i in range((EndDate - StartDate).days + 1)]
    days_FrontEnd = [
        {
            'date': (StartDate + timedelta(days=i)).strftime('%#d'),
            'weekday': (StartDate + timedelta(days=i)).strftime('%a')
        }
        for i in range((EndDate - StartDate).days + 1)
    ]

    with connection.cursor() as cursor:
        # cursor.execute("EXEC GetAttendancePivot_New %s, %s, %s, %s", [OrganizationID, StartDate, EndDate, EmployeeCode])
        cursor.execute("EXEC GetAttendancePivot_New_For_Payroll %s, %s, %s, %s", [OrganizationID, StartDate, EndDate, EmployeeCode])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    rowslist = [dict(zip(columns, row)) for row in rows]
    leavetype = Leave_Type_Master.objects.filter(IsDelete=False, Is_Active=True)
    leavelist = [leave.Type for leave in leavetype]

    for row in rowslist:
        TotalDays = len(days)
        WeekOffCount = PresentCount = AbsentCount = Presentco = Total_AR = l_Count = 0
        leave_counts = {leave: 0 for leave in leavelist}

        for day in days:
            status = row[day]
            actual_status = status.split("^")[-1].strip() if status else None
            if actual_status:
                if actual_status.lower() in ['week off', 'w']:
                    WeekOffCount += 1
                elif actual_status.lower() in ['p', 'present']:
                    PresentCount += 1
                elif actual_status.lower() in ['co', 'comp-off']:
                    Presentco += 1
                    leave_counts['Comp-off'] = Presentco
                elif actual_status.lower() == 'ar':
                    Total_AR += 1
                elif actual_status.lower() in ['a', None]:
                    AbsentCount += 1
                if actual_status in leavelist:
                    if actual_status.lower() not in ['ar']:
                        l_Count += 1
                        leave_counts[actual_status] += 1

        TotalWorkingDays = WeekOffCount + PresentCount + l_Count + Total_AR + Presentco
        row['TotalWorkingDays'] = TotalWorkingDays
        row['Present'] = PresentCount
        row['Absent'] = AbsentCount
        row['WeekOff'] = WeekOffCount
        row["Comp-off"] = Presentco
        total_no_Days_in_month = days_in_selected_month(int(month_no), int(year))
        minus = TotalDays - total_no_Days_in_month
        row['TotalPaidDays'] = TotalWorkingDays - minus if row.get("iscalm") == "1" else TotalWorkingDays
        row['leave_counts'] = leave_counts
        row['l_Count'] = l_Count

    today = datetime.today()
    context = {
        'CYear': range(today.year, 2020, -1),
        'CMonth': today.month,
        'month_no': month_no,
        'year': year,
        'month_name': month_name,
        'rowslist': rowslist,
        'days': days,
        'leavelist': leavelist,
        'emp_list': emp_list,
        'EmployeeCode': EmployeeCode,
        'StartDate': StartDate,
        'EndDate': EndDate,
        'OrganizationID': OrganizationID,
        'Org_Name': Org_Name,
        'days_FrontEnd': days_FrontEnd,
        'today': today,
    }

    # Render HTML
    template = get_template("EMP_PAY/Reports_Page/MonthlyAttendenceReport_Pdf.html")
    html = template.render(context)

    # Create PDF
    wkhtmltopdf_path = getattr(settings, 'WKHTMLTOPDF_CMD', None)

    if not wkhtmltopdf_path:
        raise Exception("WKHTMLTOPDF_CMD is not configured in settings.py")

    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)


    options = {
        'page-size': 'A4',
        'orientation': 'Landscape',
        'encoding': 'UTF-8',
        'margin-top': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'margin-right': '0mm',
        'enable-local-file-access': None,
    }

    pdf = pdfkit.from_string(
        html,
        False,
        options=options,
        configuration=config
    )

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="Monthly_Attendance_Report_{month_name}_{year}.pdf"'
    )
    return response






def Audit_Attendance_Report_PDF_View(request):

    # OrganizationID = request.session["OrganizationID"]
    OrganizationID = request.GET.get('OID')
    # OrganizationID = 1401
      
    current_date = datetime.now()
    year = int(request.GET.get('year', current_date.year))
    month_no = int(request.GET.get('month_no', current_date.month))
    # year = 2025
    # month_no = 11


    start_date = date(year, month_no, 1)
    last_day = calendar.monthrange(year, month_no)[1]  
    end_date = date(year, month_no, last_day)
    month_name = calendar.month_name[month_no]  

    Org_Name = OrganizationMaster.objects.filter(
        OrganizationID=OrganizationID, IsDelete=False, IsNileHotel=True
    ).only('OrganizationName').first()

    today = datetime.today()

    # Get employee list
    emp_list = EmployeeDataSelectForSalary(OrganizationID, month_no, year)

    # Get all salary attendance records for the month
    salary_attendance_qs = SalaryAttendance.objects.filter(
        month=month_no,
        year=year,
        OrganizationID=OrganizationID,
        IsDelete=False,
        IsAttendanceMoved=True,
        IsAttendanceModified=True
    ).values('EmployeeCode', 'Status', 'ActualStatus', 'ModifyDateTime', 'Date', 'Remarks')

    # Group all attendance records per EmployeeCode
    salary_attendance_map = {}
    for item in salary_attendance_qs:
        emp_code = item['EmployeeCode']
        if emp_code not in salary_attendance_map:
            salary_attendance_map[emp_code] = []
        salary_attendance_map[emp_code].append({
            'Status': item['Status'],
            'Date': item['Date'],
            'ModifyDateTime': item['ModifyDateTime'],
            'Remarks': item['Remarks'],
            'ActualStatus': item['ActualStatus']
        })

    # Build final employee list with all their attendance records
    final_emp_list = []
    for emp in emp_list:
        emp_code = emp['EmployeeCode']
        if emp_code in salary_attendance_map:
            final_emp_list.append({
                'EmployeeCode': emp['EmployeeCode'],
                'EmpName': emp['EmpName'],
                'attendance_records': salary_attendance_map[emp_code]  # all records for this employee
            })

    # Month navigation
    previous_month = (datetime(year, month_no, 1) - timedelta(days=1)).strftime('%Y-%m-%d')
    next_month_date = min(
        datetime(year, month_no, 28) + timedelta(days=4),
        datetime.now().replace(day=1)
    )
    if next_month_date.month == month_no:
        next_month_date = next_month_date.replace(day=1)
    next_month = next_month_date.strftime('%Y-%m-%d')


    context = {
        'Session_OrganizationID':OrganizationID,
        'emps': final_emp_list,
        'current_month': datetime(year, month_no, 1).strftime('%Y-%m-%d'),
        'previous_month': previous_month,
        'next_month': next_month,
        'month_no': month_no,
        'year': year,
        'Org_Name': Org_Name,
        'today': today,
        'StartDate': start_date,
        'EndDate': end_date,
    }

    template = get_template(
        "EMP_PAY/Reports_Page/Audit_Attendance_Report_Pdf_View.html"
    )
    html = template.render(context)
    
    # Create PDF
    wkhtmltopdf_path = getattr(settings, 'WKHTMLTOPDF_CMD', None)

    if not wkhtmltopdf_path:
        raise Exception("WKHTMLTOPDF_CMD is not configured in settings.py")

    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    options = {
        'page-size': 'A4',
        'orientation': 'Portrait',
        'encoding': 'UTF-8',
        'margin-top': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'margin-right': '0mm',
        'enable-local-file-access': None,
        'footer-right': 'Page [page] of [topage]',
        'footer-font-size': '8',
    }

    pdf = pdfkit.from_string(
        html,
        False,
        options=options,
        configuration=config
    )

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="Audit_Trail_Attendance_Report_{month_name}_{year}.pdf"'
    )
    return response









from decimal import Decimal, ROUND_DOWN
import math
from num2words import num2words
from django.db.models import Sum
from .models import *

def Salary_Slip_Pdf_Download(request):
    EmpID = int(request.GET.get('EmpID'))
    OID = int(request.GET.get('OID'))
    Year = int(request.GET.get('Year'))
    Month = int(request.GET.get('Month'))
    
    # === Fetch Basic Slip Information ===
    slip = Salary_Slip_V1.objects.filter(
        EmpID=EmpID,
        OrganizationID=OID,
        year=Year,
        month=Month,
        IsDelete=False
    ).first()

    if not slip:
        return render(request, 'payslip_not_found.html')

    # === Fixed Salary ===
    fixed_details = list(
        Salary_Fixed_Details.objects
        .filter(
            SalaryAttendance__EmpID=EmpID,
            SalaryAttendance__OrganizationID=OID,
            SalaryAttendance__year=Year,
            SalaryAttendance__month=Month,
            IsDelete=False
        )
        .values('SalaryTitle')
        .annotate(total=Sum('Amount'))
        .order_by('TitleOrder')
    )

    fixed_details = fixed_details[:-1]
    Fixed = {item['SalaryTitle']: math.ceil(float(item['total'])) for item in fixed_details}

    # === Earnings ===
    earning_details = list(
        Salary_Earning_Details.objects
        .filter(
            month=Month,
            year=Year,
            OrganizationID=OID,
            EmpID=EmpID,
            IsDelete=False
        )
        .values('SalaryTitle')
        .annotate(total=Sum('Amount'))
        .order_by('TitleOrder')
    )

    earning_details = earning_details[:-1]

    Earning = {
        item['SalaryTitle']: Decimal(item['total']).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        for item in earning_details
    }


    Earning_Show = {
        item['SalaryTitle']: float(f"{item['total']:.2f}")
        for item in earning_details
    }

    # === Deductions ===
    deduction_details = list(
        Salary_Deduction_Details.objects
        .filter(
        SalaryAttendance__EmpID=EmpID,
        SalaryAttendance__OrganizationID=OID,
        SalaryAttendance__year=Year,
        SalaryAttendance__month=Month,
        IsDelete=False
        )
        .values('SalaryTitle')
        .annotate(total=Sum('Amount'))
        .order_by('TitleOrder')
    )
    deduction_details = deduction_details[:-1]
    Deductions = {item['SalaryTitle']: math.ceil(float(item['total'])) for item in deduction_details}


    # === Totals ===
    total_fixed = sum(Fixed.values())

    total_earning = sum(Earning.values(), Decimal("0.00"))
    total_deduction = sum(Deductions.values())
    net_pay = Decimal(total_earning - total_deduction).quantize(Decimal('0.01'))
    net_pay_int = int(net_pay)
    net_pay_in_words = num2words(net_pay_int, lang='en_IN').replace(',', '').title()
    net_pay_in_words = f"{net_pay_in_words} Rupees Only"


    month_name = calendar.month_name[Month]
    org_Details  =  OrganizationMaster.objects.get(OrganizationID=OID)
    


    context = {
        'slip': slip,
        'Fixed': Fixed,
        'Earning': Earning_Show,
        'Deductions': Deductions,
        'total_fixed': total_fixed,
        'total_earning': total_earning,
        'total_deduction': total_deduction,
        'net_pay_in_words': net_pay_in_words,
        'org_Details': org_Details,
        'month_name': month_name,
        'net_pay': net_pay,
        'Month': Month,
        'year': Year,
    }

    template = get_template(
        "EMP_PAY/MoveToPayroll_Template/Generate_Salary_Slip_PDF.html"
    )
    html = template.render(context)
    
    # Create PDF
    wkhtmltopdf_path = getattr(settings, 'WKHTMLTOPDF_CMD', None)

    if not wkhtmltopdf_path:
        raise Exception("WKHTMLTOPDF_CMD is not configured in settings.py")

    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    options = {
        'page-size': 'A4',
        'orientation': 'Portrait',
        'encoding': 'UTF-8',
        'margin-top': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'margin-right': '0mm',
        'enable-local-file-access': None,
        'footer-right': 'Page [page] of [topage]',
        'footer-font-size': '8',
    }

    pdf = pdfkit.from_string(
        html,
        False,
        options=options,
        configuration=config
    )

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="Salary_Slip_{month_name}_{Year}.pdf"'
    )
    return response
