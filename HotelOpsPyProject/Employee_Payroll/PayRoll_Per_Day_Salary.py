from datetime import date
import calendar
from decimal import Decimal

def process_daily_earning(employee_id, year, month):
    # 1️⃣ Get salary slip for the month
    slip = Salary_Slip_V1.objects.filter(
        EmployeeCode=employee_id, 
        year=year, 
        month=month,
        IsDelete=False
    ).first()

    if not slip:
        return f"No salary slip found for employee {employee_id}"

    # 2️⃣ Get attendance records for that month
    attendances = SalaryAttendance.objects.filter(
        EmpID=employee_id,
        year=year,
        month=month,
        IsPresent=True,
        IsDelete=False
    )

    # 3️⃣ Calculate per-day salary parts
    total_days = calendar.monthrange(year, month)[1]
    daily_basic = Decimal(slip.Basic_Salary_Fixed or 0) / total_days
    daily_hra = Decimal(slip.HRA_Fixed or 0) / total_days
    daily_conveyance = Decimal(slip.Conveyance_Fixed or 0) / total_days

    # 4️⃣ For each attendance record, insert daily earning details
    for att in attendances:
        present_value = Decimal(att.PresentValue or 0)

        Salary_Earning_Details.objects.create(
            Date=att.Date,
            SalaryAttendance=att,
            SalaryTitleID='BASIC',
            Type='Earning',
            Amount=daily_basic * present_value,
            OrganizationID=att.OrganizationID,
            CreatedBy=att.CreatedBy
        )
        
        Salary_Earning_Details.objects.create(
            Date=att.Date,
            SalaryAttendance=att,
            SalaryTitleID='HRA',
            Type='Earning',
            Amount=daily_hra * present_value,
            OrganizationID=att.OrganizationID,
            CreatedBy=att.CreatedBy
        )

        Salary_Earning_Details.objects.create(
            Date=att.Date,
            SalaryAttendance=att,
            SalaryTitleID='CONVEYANCE',
            Type='Earning',
            Amount=daily_conveyance * present_value,
            OrganizationID=att.OrganizationID,
            CreatedBy=att.CreatedBy
        )
