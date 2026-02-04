from HumanResources.models import EmployeePersonalDetails, EmployeeWorkDetails
from HumanResources.templatetags.encryption_filters import encrypt_id_filter
from LETTEROFAPPOINTMENT.models import LOALETTEROFAPPOINTMENTEmployeeDetail
from django.db.models.functions import ExtractMonth,ExtractYear
from Leave_Management_System.models import Leave_Application
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from EmpResignation.models import  EmpResigantionModel
from Open_position.models import OpenPosition
from PADP.models import APADP, Entry_Master
from django.utils.timezone import now
from django.http import JsonResponse
from datetime import date, timedelta
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone

# Create your views here.


# HR Dashboard Home
def HR_Dashboard_Home(request):
    return render(request, 'HR_Dashboard/HR_Dashboard.html')


# First Card -- Employee Basic Information
def Employee_Card_Details_Api(request):
    if 'OrganizationID' not in request.session:
        return JsonResponse({'error': 'No organization in session'}, status=400)

    OrganizationID = request.session.get("OrganizationID")
    SessionUserID = str(request.session.get("UserID"))
    UserID = encrypt_id(SessionUserID)

    EmployeeCode = request.session.get("EmployeeCode")
    Emobj_data = {}

    if EmployeeCode:
        # Fetch both models
        Personal_Obj = EmployeePersonalDetails.objects.only(
            'EmpID', 'EmployeeCode', 'Prefix', 'FirstName', 'MiddleName', 'LastName',
            'Gender', 'MaritalStatus', 'DateofBirth', 'MobileNumber',
            'EmailAddress', 'ProfileImageFileName', 'ProfileImageFileTitle',
            'ProfileCompletion', 'IsDelete', 'IsEmployeeCreated'
        ).filter(
            EmployeeCode=EmployeeCode,
            IsDelete=False,
            OrganizationID=OrganizationID,
            IsEmployeeCreated=True
        ).first()

        if Personal_Obj:
            Workobj = EmployeeWorkDetails.objects.only(
                'EmpID', 'Department', 'EmpStatus', 'Designation', 'Level',
                'DateofJoining', 'ReportingtoDesignation',
                'ReportingtoDepartment', 'ReportingtoLevel'
            ).filter(
                OrganizationID=OrganizationID,
                IsDelete=False,
                IsSecondary=False,
                EmpID=Personal_Obj.EmpID
            ).first()

            # Prepare response
            if Workobj:
                tenure = Workobj.tenure_till_today()
                try:
                    Emobj_data = {
                        'EmpID': getattr(Personal_Obj, 'EmpID', None),
                        'EmployeeCode': getattr(Personal_Obj, 'EmployeeCode', None),
                        'FullName': f"{getattr(Personal_Obj, 'FirstName', '') or ''} {getattr(Personal_Obj, 'MiddleName', '') or ''} {getattr(Personal_Obj, 'LastName', '') or ''}".strip(),
                        'Department': getattr(Workobj, 'Department', None),
                        'EmpStatus': getattr(Workobj, 'EmpStatus', None),
                        'Designation': getattr(Workobj, 'Designation', None),
                        'Level': getattr(Workobj, 'Level', None),
                        'DateofJoining': Workobj.DateofJoining.strftime('%Y-%m-%d') if getattr(Workobj, 'DateofJoining', None) else None,
                        'ReportingtoDesignation': getattr(Workobj, 'ReportingtoDesignation', None),
                        'ReportingtoDepartment': getattr(Workobj, 'ReportingtoDepartment', None),
                        'ReportingtoLevel': getattr(Workobj, 'ReportingtoLevel', None),
                        'TenureTillToday': tenure if 'tenure' in locals() else None,

                        # Masked contact details
                        'MobileNumber': mask_mobile_number(Personal_Obj.MobileNumber) if Personal_Obj else None,
                        'EmailAddress': mask_email_address(Personal_Obj.EmailAddress) if Personal_Obj else None,

                        'ProfileImageFileName': getattr(Personal_Obj, 'ProfileImageFileName', None),
                        'DateofBirth': getattr(Personal_Obj, 'DateofBirth', None),
                        'Gender': getattr(Personal_Obj, 'Gender', None),
                    }

                except Exception as e:
                    Emobj_data = {}
                    print(f"[Error] Failed to create Emobj_data: {str(e)}")


    return JsonResponse({
        'UserID': UserID,
        'Emobj': Emobj_data,
    }, safe=False)


# HR_Dashboard_Summary_Api
def HR_Dashboard_Summary_Api(request):
    if 'OrganizationID' not in request.session:
        return JsonResponse({'error': 'No organization in session'}, status=400)

    OrganizationID = request.session.get("OrganizationID")
    SessionUserID = str(request.session.get("UserID"))
    UserID = encrypt_id(SessionUserID)
    
    selectedOrganizationID = request.GET.get('OrganizationID', OrganizationID)
    request.session['OrganizationID'] = selectedOrganizationID

    emp_status_counts = list(
        EmployeeWorkDetails.objects.filter(
            OrganizationID=selectedOrganizationID,
            IsDelete=False,
            IsSecondary=False,
            EmpStatus__in=["Confirmed", "Not Confirmed", "On Probation"]
        ).values('EmpStatus').annotate(count=Count('EmpStatus'))
    )

    current_month = now().month
    # thirty_days_after = timezone.now().date() + timedelta(days=30)
    current_year = now().year

    not_confirmed_employees = EmployeeWorkDetails.objects.filter(
        OrganizationID=selectedOrganizationID,
        EmpStatus="Not Confirmed",
        IsDelete=False,
        IsSecondary=False
    )
    
    not_confirmed_count = not_confirmed_employees.count()
    not_confirmed_data = fetch_employee_data(not_confirmed_employees)


    # Encrypt EmpID in not_confirmed_data
    for emp in not_confirmed_data:
        emp["EmpID"] = encrypt_id_filter(emp["EmpID"])

    resigned_employees = EmpResigantionModel.objects.annotate(
        joinning_month=ExtractMonth('Date_Of_res'),
        joinning_year=ExtractYear('Date_Of_res')
    ).filter(
        OrganizationID=selectedOrganizationID,
        IsDelete=False,
        joinning_month=current_month,
        joinning_year=current_year
    )
    resigned_count = resigned_employees.count()
    resigned_data = []  # fetch_employee_data(resigned_employees)


    TotalEmployee = sum(item['count'] for item in emp_status_counts)

    APADP_Status_Count = list(
        APADP.objects.filter(
            # OrganizationID=601,
            OrganizationID=selectedOrganizationID,
            IsDelete=False,
            LastApporvalStatus__in=["Pending", "Approved", "Returned", "Submitted"]
        ).values('LastApporvalStatus').annotate(count=Count('LastApporvalStatus'))
    )

    Leave_Status_Count = list(
        Leave_Application.objects.filter(
            OrganizationID=selectedOrganizationID,
            IsDelete=False,
            Status__in=[1, 0, -1]
        ).values('Status').annotate(count=Count('Status')).order_by()
    )


    # Today's date minus 30 days
    thirty_days_ago = timezone.now().date() - timedelta(days=30)

    # Total openings (not deleted and for specific org)
    total_openings = OpenPosition.objects.filter(
        IsDelete=False,Status=1,
        Locations=selectedOrganizationID
        # OrganizationID=selectedOrganizationID
    ).count()

    # Openings older than 30 days
    older_openings = OpenPosition.objects.filter(
        IsDelete=False,Status=1,
        # OrganizationID=selectedOrganizationID,
        Locations=selectedOrganizationID,
        Opened_On__lte=thirty_days_ago
    ).count()


    # Convert list to dict
    emp_status_counts_dict = {
        item["EmpStatus"]: item["count"] for item in emp_status_counts
    }

    apadp_status_count_dict = {
        item["LastApporvalStatus"]: item["count"] for item in APADP_Status_Count
    }

    leave_status_count_dict = {
        item["Status"]: item["count"] for item in Leave_Status_Count
    }

    # Unpack Employee status counts
    Confirmed_Employee_Status = emp_status_counts_dict.get("Confirmed", 0)
    Not_Confirmed_Employee_Status = emp_status_counts_dict.get("Not Confirmed", 0)
    On_Probation_Employee_Status = emp_status_counts_dict.get("On Probation", 0)

    # Unpack APADP status counts
    pending_apadp = apadp_status_count_dict.get("Pending", 0)
    approved_apadp = apadp_status_count_dict.get("Approved", 0)
    returned_apadp = apadp_status_count_dict.get("Returned", 0)
    submitted_apadp = apadp_status_count_dict.get("Submitted", 0)

    # Unpack Leave status counts
    approved_leave = leave_status_count_dict.get(1, 0)
    pending_leave = leave_status_count_dict.get(0, 0)
    rejected_leave = leave_status_count_dict.get(-1, 0)



    print("--------------- HR Dashboard Summery API ---------------------------")

    return JsonResponse({
        'emp_status_counts': emp_status_counts_dict,
        'not_confirmed_count': not_confirmed_count,
        'not_confirmed_data': not_confirmed_data,
        'resigned_count': resigned_count,
        'resigned_data': resigned_data,
        'selectedOrganizationID': selectedOrganizationID,
        # 'Emobj': Emobj_data,
        'TotalEmployee': TotalEmployee,

        # Open Positions
        "total_openings": total_openings,
        "older_than_30_days": older_openings,

        # Example Unpack
        "pending_apadp":pending_apadp,
        "approved_apadp":approved_apadp,
        "returned_apadp":returned_apadp,
        "submitted_apadp":submitted_apadp,

        "approved_leave":approved_leave,
        "pending_leave":pending_leave,
        "rejected_leave":rejected_leave,

        "Confirmed_Employee_Status":Confirmed_Employee_Status,
        "Not_Confirmed_Employee_Status":Not_Confirmed_Employee_Status,
        "On_Probation_Employee_Status":On_Probation_Employee_Status,
    }, safe=False)


from datetime import timedelta

def Upcoming_Birthday_Api(request):
    if 'OrganizationID' not in request.session:
        return JsonResponse({'error': 'No organization in session'}, status=400)

    OrganizationID = request.session.get("OrganizationID")
    SessionUserID = str(request.session.get("UserID"))
    UserID = encrypt_id(SessionUserID)

    today = timezone.now().date()
    end_date = today + timedelta(days=30)

    # Build MM-DD strings for today + next 30 days
    mmdd_list = [(today + timedelta(days=i)).strftime("%m-%d") for i in range(31)]

    AllActiveEmployee = EmployeeWorkDetails.objects.filter(
        OrganizationID = OrganizationID,
        IsDelete=False,
        IsSecondary=False,
        EmpStatus__in=['Confirmed', 'On Probation', 'Not Confirmed']
    ).values_list("EmpID", flat=True)

    # Fetch all DOBs and filter in Python (not ideal for huge data, but safe)
    # if AllActiveEmployee:
    all_employees = EmployeePersonalDetails.objects.filter(
        EmpID__in=AllActiveEmployee,
        IsDelete=False,
        IsEmployeeCreated=True
    ).only('EmpID', 'FirstName', 'MiddleName', 'LastName', 'DateofBirth')

    # Filter in Python using mm-dd
    birthday_employees = [
        emp for emp in all_employees
        if emp.DateofBirth and emp.DateofBirth.strftime('%m-%d') in mmdd_list
    ]


    birthday_employees.sort(
        key=lambda x: (date(today.year, x.DateofBirth.month, x.DateofBirth.day) - today).days
    )
    
    # birthday_employees.sort(
    #     key=lambda x: (date(today.year, x.DateofBirth.month, x.DateofBirth.day) - today).days,
    #     reverse=True
    # )

    birthday_count = len(birthday_employees)
    birthday_data = fetch_employee_data_with_birthday(birthday_employees)

    return JsonResponse({
        'birthday_count': birthday_count,
        'birthday_data': birthday_data,
        'UserID': UserID,
    }, safe=False)


# Upcoming PADP ------>
def Upcoming_PADP_API(request):
    if 'OrganizationID' not in request.session:
        return JsonResponse({'error': 'No organization in session'}, status=400)

    OrganizationID = request.session.get("OrganizationID")
    SessionUserID = str(request.session.get("UserID"))
    UserID = encrypt_id(SessionUserID)
   
    # Upcoming PADP Employees
    one_year_ago = date.today() - timedelta(days=365)

    # Step 1: Work details of employees who completed 1 year
    eligible_employees = EmployeeWorkDetails.objects.filter(
        OrganizationID=OrganizationID,
        IsDelete=False,
        DateofJoining__lte=one_year_ago,
        IsSecondary=False,
        # EmpStatus__in=["Confirmed", "Not Confirmed", "On Probation"]
        EmpStatus="Confirmed"
    )

    emp_ids = [emp.EmpID for emp in eligible_employees]

    # Step 2: Map EmpID → EmployeeCode from personal table
    personal_map = {
        pd.EmpID: pd for pd in EmployeePersonalDetails.objects.filter(
            EmpID__in=emp_ids,
            OrganizationID=OrganizationID,
            IsDelete=False
        )
    }

    # Step 3: Get PADP-created EmployeeCodes from both tables
    padp_apadp_codes = set(APADP.objects.filter(
        OrganizationID=OrganizationID,
        IsDelete=False
    ).values_list('EmployeeCode', flat=True))

    padp_entry_codes = set(Entry_Master.objects.filter(
        OrganizationID=OrganizationID,
        IsDelete=False
    ).values_list('EmployeeCode', flat=True))

    padp_done_codes = padp_apadp_codes.union(padp_entry_codes)

    # Step 4: Filter upcoming PADP employees
    upcoming_padp_data = []

    for emp in eligible_employees:
        personal = personal_map.get(emp.EmpID)
        if not personal:
            continue

        emp_code = personal.EmployeeCode
        if not emp_code or emp_code in padp_done_codes:
            continue

        upcoming_padp_data.append({
            "EmpID": encrypt_id(emp.EmpID),
            "Name": f"{personal.FirstName or ''} {personal.LastName or ''}".strip(),
            "Designation": emp.Designation,
            "DateOfJoining": emp.DateofJoining,
            "Tenure": emp.tenure_till_today(),
        })
    
    upcoming_padp_count = len(upcoming_padp_data)


    # print("--------------- Example ---------------------------")

    return JsonResponse({
        'UserID': UserID,
    
        # Upcoming PADP 
        'upcoming_padp_count':upcoming_padp_count,
        'upcoming_padp_data':upcoming_padp_data,
    }, safe=False)


# Pending Appointment Letter
def Pending_Appointment_Letter_Api(request):
    if 'OrganizationID' not in request.session:
        return JsonResponse({'error': 'No organization in session'}, status=400)

    OrganizationID = request.session.get("OrganizationID")
    SessionUserID = str(request.session.get("UserID"))
    UserID = encrypt_id(SessionUserID)

    # Pending Appointment Letter
    unmatched_count, unmatched_employees = fetch_unmatched_employee_details(OrganizationID)

    return JsonResponse({
        'unmatched_count': unmatched_count,
        'unmatched_employees': unmatched_employees,
        'UserID': UserID,
    }, safe=False)


# F&F In Process __And__ Pending Appointment Letter
def FNF_In_Process_API(request):
    if 'OrganizationID' not in request.session:
        return JsonResponse({'error': 'No organization in session'}, status=400)

    OrganizationID = request.session.get("OrganizationID")
    SessionUserID = str(request.session.get("UserID"))
    UserID = encrypt_id(SessionUserID)

    # Full and Final Settlement card
    ff_employees = EmployeeWorkDetails.objects.filter(
        OrganizationID=OrganizationID,
        EmpStatus="F&F In process",
        IsDelete=False,
        IsSecondary=False
    ).only('EmpID', 'EmpStatus', 'Designation', 'Department')

    ffpro_count = ff_employees.count()
    ff_datapro = fetch_employee_data(ff_employees)

    return JsonResponse({
        'ffpro_count': ffpro_count,
        'ff_datapro': ff_datapro,
        'UserID': UserID,
    }, safe=False)



#  <----------------------- Helper Functions -------------------->
# Helper Function for -- Pending Appointment Letter
def fetch_unmatched_employee_details(organization_id):
    """
        Efficiently fetch employees from LOALETTEROFAPPOINTMENTEmployeeDetail
        that do not have a matching EmployeeCode in EmployeePersonalDetails.
    """
    # Fetch all existing employee codes in the org
    existing_codes = set(
        EmployeePersonalDetails.objects.filter(OrganizationID=organization_id, IsDelete=False)
        .values_list('EmployeeCode', flat=True)
    )

    # Fetch all appointment employees
    employees = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(OrganizationID=organization_id, IsDelete=0)

    # print("Emloyee codes", existing_codes)
    # Filter out unmatched
    unmatched_employees = [
        {
            'emp_code': emp.emp_code,
            'FirstName': emp.first_name,
            'LastName': emp.last_name,
            'Department': emp.department,
            'Designation': emp.designation
        }
        # print("employee codes that in not apl::", emp)
        for emp in employees if emp.emp_code not in existing_codes
    ]
    print("employee codes that in not apl::", unmatched_employees)

    return len(unmatched_employees), unmatched_employees


# Helper Function for -- Upcoming_Birthday_Api
def fetch_employee_data_with_birthday(employee_queryset):
    """
    Optimized: Fetch all required EmployeeWorkDetails in one query,
    then map by EmpID for fast lookup.
    """
    emp_ids = [emp.EmpID for emp in employee_queryset]

    # Fetch work details in bulk
    work_details_map = {
        w.EmpID: w
        for w in EmployeeWorkDetails.objects.filter(
            EmpID__in=emp_ids,
            IsDelete=False,
            IsSecondary=False
        ).only('EmpID', 'Department', 'Designation')
    }

    employee_data = []
    for emp in employee_queryset:
        work = work_details_map.get(emp.EmpID)
        employee_data.append({
            'EmpID': encrypt_id_filter(emp.EmpID),
            'FirstName': emp.FirstName,
            'MiddleName': emp.MiddleName,
            'LastName': emp.LastName,
            'DateofBirth': emp.DateofBirth,
            'Department': work.Department if work else None,
            'Designation': work.Designation if work else None,
        })

    return employee_data


# Helper Function for -- Pending Confirmation Letter - in HR_Dashboard_Summary_Api
def fetch_employee_data(employee_queryset):
    """
    Optimized version to prevent N+1 queries by using pre-fetched personal data.
    """
    emp_ids = [work.EmpID for work in employee_queryset]

    # Bulk fetch personal details in one query
    personal_details_map = {
        p.EmpID: p
        for p in EmployeePersonalDetails.objects.filter(EmpID__in=emp_ids, IsDelete=False)
        .only('EmpID', 'FirstName', 'MiddleName', 'LastName')
    }

    employee_data = []
    for work in employee_queryset:
        personal = personal_details_map.get(work.EmpID)
        employee_data.append({
            'EmpID': encrypt_id_filter(work.EmpID),
            # 'EmpStatus': work.EmpStatus,
            'Designation': work.Designation,
            # 'Department': work.Department,
            'FirstName': personal.FirstName if personal else None,
            'MiddleName': personal.MiddleName if personal else None,
            'LastName': personal.LastName if personal else None,
        })

    return employee_data



# Hide Mobile number Digits
def mask_mobile_number(number):
    """
    Return masked mobile number in format: xxxxx-78
    """
    if number and len(number) >= 2:
        return f"xxxxx-{number[-2:]}"
    return "xxxxx-xx"


# Hide Email 
def mask_email_address(email):
    """
    Return masked email address like: a***@domain.com
    """
    if not email or "@" not in email:
        return "****@****"
    
    name_part, domain_part = email.split("@", 1)
    if len(name_part) > 1:
        return f"{name_part[0]}***@{domain_part}"
    return f"***@{domain_part}"



from app.models import EmployeeMaster

def Upcoming_Work_Anniversary_Api(request):
    if 'OrganizationID' not in request.session:
        return JsonResponse({'error': 'No organization in session'}, status=400)

    OrganizationID = request.session.get("OrganizationID")
    today = timezone.now().date()

    # Look ahead 30 days
    mmdd_list = [(today + timedelta(days=i)).strftime("%m-%d") for i in range(31)]

    # Fetch active employees
    employees = EmployeeMaster.objects.filter(
        OrganizationID=OrganizationID,
        IsDelete=False,
        IsSecondary=False,
        EmpStatus__in=['Confirmed', 'On Probation', 'Not Confirmed']
    ).only('EmployeeCode', 'EmpName', 'DateofJoining', 'EmpID','Designation')

    # Filter employees whose joining date (month-day) falls in next 30 days
    anniversary_employees = [
        emp for emp in employees
        if emp.DateofJoining and emp.DateofJoining.strftime('%m-%d') in mmdd_list
    ]

    anniversary_employees.sort(
        key=lambda x: (date(today.year, x.DateofJoining.month, x.DateofJoining.day) - today).days
    )

    # Calculate work years completed
    anniversary_data = []
    for emp in anniversary_employees:
        years_completed = today.year - emp.DateofJoining.year
        # adjust if anniversary not yet reached this year
        if (today.month, today.day) < (emp.DateofJoining.month, emp.DateofJoining.day):
            years_completed -= 1

        anniversary_data.append({
            'EmployeeCode': emp.EmployeeCode,
            'EmpName': emp.EmpName,
            'EmpID': encrypt_id_filter(emp.EmpID),
            'Designation': emp.Designation,
            'DateofJoining': emp.DateofJoining.strftime('%Y-%m-%d'),
            'YearsCompleted': years_completed,
        })

    return JsonResponse({
        'anniversary_count': len(anniversary_data),
        'anniversary_data': anniversary_data,
    }, safe=False)
