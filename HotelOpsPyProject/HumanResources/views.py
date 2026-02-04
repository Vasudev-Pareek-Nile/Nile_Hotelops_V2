from django.shortcuts import render,HttpResponse,redirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from InterviewAssessment.models import EmployeeDataRequest_Master,EmployeeChildData,EmployeeFamilyData,EmployeePersonalData,EmployeeEmergencyInfoData,EmployeeBankInfoData,EmployeePreviousWorkData,EmployeeDocumentsInfoData,EmployeeAddressInfoData,EmployeeEducationData,EmployeeIdentityInfoData,Assessment_Master
from Manning_Guide.models import OnRollDesignationMaster,CorporateDesignationMaster,OnRollDepartmentMaster,OnRollDivisionMaster, LavelAdd
# from .models import SalaryTitle_Master,Salary_Detail_Master,EmployeePersonalDetails,EmployeeWorkDetails,EmployeeFamilyDetails,EmployeeChildDetails,EmployeeEmergencyInformationDetails,EmployeeAddressInformationDetails,EmployeeBankInformationDetails,EmployeeQualificationDetails,EmployeePreviousWorkInformationDetails,EmployeeDocumentsInformationDetails,EmployeeIdentityInformationDetails,DesignationHistory
from .models import *
from InterviewAssessment.views import view_file,CopyFile
from .azure import upload_file_to_blob,download_blob
from io import BytesIO
from django.http import HttpResponse, Http404
import mimetypes
from Leave_Management_System.models import Leave_Type_Master,Emp_Leave_Balance_Master
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from django.urls import reverse
from app.models  import EmployeeMaster
from .Profile import calculate_profile_completion,update_employee_profile
from django.db import connection

from django.contrib import messages
from itertools import chain
from django.db.models import Count

from django.db.models.functions import ExtractMonth,ExtractYear
from django.utils.timezone import now
from .models import EmployeePersonalDetails, EmployeeWorkDetails


from LetteofPromotion.models import PromotionSalaryDetails
from django.db import transaction
from LetteofPromotion.models import PromotionSalaryDetails
from django.utils.timezone import now

from django.db import transaction
from datetime import timedelta
from decimal import Decimal
from LetterSalaryIncrement.models import IncreamentSalaryDetails


# def HumanResourcesDashboard(request):
#         if 'OrganizationID' not in request.session:
#             return redirect(MasterAttribute.Host)
#         else:
#             print("Show Page Session")
#         return render(request,'HR/HumanResourcesDashboard.html')


def fetch_employee_data(employee_queryset):
    """
    Helper function to fetch employee details and prepare the data.
    """
    employee_data = []
    for work in employee_queryset:
        personal_details = EmployeePersonalDetails.objects.filter(EmpID=work.EmpID).first()
        employee_data.append({
            'EmpID': work.EmpID,
            'EmpStatus': work.EmpStatus,
            'Designation': work.Designation,
            'Department': work.Department,
            'FirstName': personal_details.FirstName if personal_details else None,
            'MiddleName': personal_details.MiddleName if personal_details else None,
            'LastName': personal_details.LastName if personal_details else None,
        })
    return employee_data


def fetch_employee_dataByEmpCode(employee_queryset):
    """
    Helper function to fetch employee details and prepare the data.
    """
    employee_data = []
    for work in employee_queryset:
        personal_details = EmployeePersonalDetails.objects.filter(EmpCode=work.EmpCode,).first()
        employee_data.append({
            'EmpID': work.EmpID,
            'EmpStatus': work.EmpStatus,
            'Designation': work.Designation,
            'Department': work.Department,
            'FirstName': personal_details.FirstName if personal_details else None,
            'MiddleName': personal_details.MiddleName if personal_details else None,
            'LastName': personal_details.LastName if personal_details else None,
        })
    return employee_data

def fetch_employee_data_with_birthday(employee_queryset):
    """
    Helper function to fetch employee details with birthday information.
    """
    employee_data = []
    for work in employee_queryset:
       
        work_details = EmployeeWorkDetails.objects.filter(EmpID=work.EmpID, IsDelete=False,IsSecondary=False).first()
        employee_data.append({
            'EmpID': work.EmpID,
            'FirstName': work.FirstName,
            'MiddleName': work.MiddleName,
            'LastName': work.LastName,
            'DateofBirth': work.DateofBirth,
            'Department': work_details.Department if work_details else None,
            'Designation': work_details.Designation if work_details else None,
        })
    return employee_data


def GetMailofHR(OrganizationID):
    work_details = EmployeeWorkDetails.objects.filter(
        Department='Human Resources',
        IsDelete=False,IsSecondary=False,
        EmpStatus__in=["Confirmed"],
        OrganizationID=OrganizationID
    ).exclude(OfficialEmailAddress__isnull=True).exclude(OfficialEmailAddress='').values_list('OfficialEmailAddress', flat=True)
 
    return list(work_details) if work_details else []

def fetch_employee_joing_(employee_queryset):
    """
    Helper function to fetch employee details with birthday information.
    """
    employee_data = []
    for work in employee_queryset:
        personal_details = EmployeePersonalDetails.objects.filter(EmpID=work.EmpID).first()
        employee_data.append({
            'EmpID': work.EmpID,
            'EmpStatus': work.EmpStatus,
            'Designation': work.Designation,
            'Department': work.Department,
            'DateofJoining': work.DateofJoining,
            'FirstName': personal_details.FirstName if personal_details else None,
            'MiddleName': personal_details.MiddleName if personal_details else None,
            'LastName': personal_details.LastName if personal_details else None,
        })
    return employee_data

def fetch_unmatched_employee_details(organization_id):
    """
    Helper function to fetch employees from LOALETTEROFAPPOINTMENTEmployeeDetail
    that do not have a matching EmployeeCode in EmployeePersonalDetails, 
    filtered by OrganizationID.
    """
    
    employees = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(OrganizationID=organization_id)
    unmatched_employees = []

    
    for emp in employees:
        if not EmployeePersonalDetails.objects.filter(EmployeeCode=emp.emp_code).exists():
            unmatched_employees.append({
                'FirstName': emp.first_name,
                'LastName': emp.last_name,
                'Department': emp.department,
                'Designation': emp.designation
            })
    
    
    unmatched_count = len(unmatched_employees)
    return unmatched_count, unmatched_employees

# # Original
# def HumanResourcesDashboard(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
#     OrganizationID = request.session.get("OrganizationID")
#     SessionUserID = str(request.session["UserID"])
#     UserID=encrypt_id(SessionUserID)
#     memOrg  =  OrganizationList(OrganizationID)
    
#     selectedOrganizationID = request.GET.get('OrganizationID', OrganizationID)

    
#     if selectedOrganizationID:
#         request.session['OrganizationID'] = selectedOrganizationID

    
#     emp_status_counts = (
#         EmployeeWorkDetails.objects.filter(OrganizationID=selectedOrganizationID, IsDelete=False,IsSecondary=False,EmpStatus__in=["Confirmed","Not Confirmed","On Probation"])
#         .values('EmpStatus')
#         .annotate(count=Count('EmpStatus'))
#     )
#     current_month = now().month
#     current_year = now().year
    
#     not_confirmed_employees = EmployeeWorkDetails.objects.filter(
#         OrganizationID=selectedOrganizationID, EmpStatus="Not Confirmed", IsDelete=False,IsSecondary=False
#     )
#     not_confirmed_count = not_confirmed_employees.count()
#     not_confirmed_data = fetch_employee_data(not_confirmed_employees)

   
#     resigned_employees = EmpResigantionModel.objects.annotate(
#         joinning_month=ExtractMonth('Date_Of_res'),
#         joinning_year=ExtractYear('Date_Of_res')
#     ).filter(
#         OrganizationID=selectedOrganizationID, IsDelete=False,
#           joinning_month=current_month,   joinning_year=current_month, 
#     )
#     resigned_count = resigned_employees.count()
#     resigned_data =[] #fetch_employee_data(resigned_employees)

   
#     ff_employees = EmployeeWorkDetails.objects.filter(
#         OrganizationID=selectedOrganizationID, EmpStatus="F&F In process", IsDelete=False,IsSecondary=False
#     )
#     ffpro_count = ff_employees.count()
#     ff_datapro = fetch_employee_data(ff_employees)

   
   
#     birthday_employees = EmployeePersonalDetails.objects.annotate(
#         birth_month=ExtractMonth('DateofBirth')
#     ).filter(
#         birth_month=current_month, OrganizationID=selectedOrganizationID, IsDelete=False
#     )
#     birthday_count = birthday_employees.count()
#     birthday_data = fetch_employee_data_with_birthday(birthday_employees)

    
#     unmatched_count, unmatched_employees = fetch_unmatched_employee_details(selectedOrganizationID)

   
#     joinning_employees = EmployeeWorkDetails.objects.annotate(
#         joinning_month=ExtractMonth('DateofJoining'),
#         joinning_year=ExtractYear('DateofJoining')
#     ).filter(
#         joinning_month=current_month,joinning_year=current_year, OrganizationID=selectedOrganizationID, IsDelete=False,IsSecondary=False
#     )
#     joinning_count = joinning_employees.count()
#     joinning_data = fetch_employee_joing_(joinning_employees)
#     print("joinning_count:", joinning_count)

#     return render(
#         request,
#         'HR/HumanResourcesDashboard.html',
#         {
#             'emp_status_counts': emp_status_counts,
#             'memOrg': memOrg,
#             'not_confirmed_count': not_confirmed_count,
#             'not_confirmed_data': not_confirmed_data,
#             'resigned_count': resigned_count,
#             'resigned_data': resigned_data,
#             'birthday_count': birthday_count,
#             'birthday_data': birthday_data,
#             'unmatched_count': unmatched_count,
#             'unmatched_employees': unmatched_employees,
#             'ffpro_count': ffpro_count,
#             'ff_datapro': ff_datapro,
#             'joinning_count': joinning_count,
#             'joinning_data': joinning_data,
#             'selectedOrganizationID': selectedOrganizationID,
#             'UserID':UserID
#         },
#     )


# Copid
# def HumanResourcesDashboard(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
#     OrganizationID = request.session.get("OrganizationID")
#     SessionUserID = str(request.session["UserID"])
#     UserID=encrypt_id(SessionUserID)
#     memOrg  =  OrganizationList(OrganizationID)
    
#     selectedOrganizationID = request.GET.get('OrganizationID', OrganizationID)

    
#     if selectedOrganizationID:
#         request.session['OrganizationID'] = selectedOrganizationID

    
#     emp_status_counts = (
#         EmployeeWorkDetails.objects.filter(OrganizationID=selectedOrganizationID, IsDelete=False,IsSecondary=False,EmpStatus__in=["Confirmed","Not Confirmed","On Probation"])
#         .values('EmpStatus')
#         .annotate(count=Count('EmpStatus'))
#     )
#     current_month = now().month
#     current_year = now().year
    
#     not_confirmed_employees = EmployeeWorkDetails.objects.filter(
#         OrganizationID=selectedOrganizationID, EmpStatus="Not Confirmed", IsDelete=False,IsSecondary=False
#     )
#     not_confirmed_count = not_confirmed_employees.count()
#     not_confirmed_data = fetch_employee_data(not_confirmed_employees)

   
#     resigned_employees = EmpResigantionModel.objects.annotate(
#         joinning_month=ExtractMonth('Date_Of_res'),
#         joinning_year=ExtractYear('Date_Of_res')
#     ).filter(
#         OrganizationID=selectedOrganizationID, IsDelete=False,
#           joinning_month=current_month,   joinning_year=current_month, 
#     )
#     resigned_count = resigned_employees.count()
#     resigned_data =[] #fetch_employee_data(resigned_employees)

   
#     ff_employees = EmployeeWorkDetails.objects.filter(
#         OrganizationID=selectedOrganizationID, EmpStatus="F&F In process", IsDelete=False,IsSecondary=False
#     )
#     ffpro_count = ff_employees.count()
#     ff_datapro = fetch_employee_data(ff_employees)

   
   
#     birthday_employees = EmployeePersonalDetails.objects.annotate(
#         birth_month=ExtractMonth('DateofBirth')
#     ).filter(
#         birth_month=current_month, OrganizationID=selectedOrganizationID, IsDelete=False
#     )
#     birthday_count = birthday_employees.count()
#     birthday_data = fetch_employee_data_with_birthday(birthday_employees)

    
#     unmatched_count, unmatched_employees = fetch_unmatched_employee_details(selectedOrganizationID)

   
#     joinning_employees = EmployeeWorkDetails.objects.annotate(
#         joinning_month=ExtractMonth('DateofJoining'),
#         joinning_year=ExtractYear('DateofJoining')
#     ).filter(
#         joinning_month=current_month,joinning_year=current_year, OrganizationID=selectedOrganizationID, IsDelete=False,IsSecondary=False
#     )
#     joinning_count = joinning_employees.count()
#     joinning_data = fetch_employee_joing_(joinning_employees)
#     print("joinning_count:", joinning_count)

#     return render(
#         request,
#         'HR/HumanResourcesDashboard.html',
#         {
#             'emp_status_counts': emp_status_counts,
#             'memOrg': memOrg,
#             'not_confirmed_count': not_confirmed_count,
#             'not_confirmed_data': not_confirmed_data,
#             'resigned_count': resigned_count,
#             'resigned_data': resigned_data,
#             'birthday_count': birthday_count,
#             'birthday_data': birthday_data,
#             'unmatched_count': unmatched_count,
#             'unmatched_employees': unmatched_employees,
#             'ffpro_count': ffpro_count,
#             'ff_datapro': ff_datapro,
#             'joinning_count': joinning_count,
#             'joinning_data': joinning_data,
#             'selectedOrganizationID': selectedOrganizationID,
#             'UserID':UserID
#         },
#     )

# Copid - 2
def HumanResourcesDashboard(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    print("Show Page Session")

    OrganizationID = request.session.get("OrganizationID")
    SessionUserID = str(request.session["UserID"])
    UserID = encrypt_id(SessionUserID)
    
    show_OrgFilter = False
    if OrganizationID == '3':
        show_OrgFilter = True
        
    Is_Show_Module = OrganizationMaster.objects.filter(
        IsDelete=False,
        IsNileHotel=1,
        Activation_status=1,
        OrganizationID=OrganizationID
    ).exists()

    memOrg = OrganizationList(OrganizationID)  # If used in template
    selectedOrganizationID = request.GET.get('OrganizationID', OrganizationID)

    if selectedOrganizationID:
        request.session['OrganizationID'] = selectedOrganizationID

    context = {
        'UserID': UserID,
        'OrganizationID': OrganizationID,
        'selectedOrganizationID': selectedOrganizationID,
        'Is_Show_Module': Is_Show_Module,
        'show_OrgFilter': show_OrgFilter,
        'memOrg': memOrg  
    }

    return render(request, 'HR/HumanResourcesDashboard.html', context)


from django.views.decorators.http import require_GET
# from .templatetags import encryption_filters
from .templatetags.encryption_filters import encrypt_id_filter

@require_GET
def api_human_resources_dashboard(request):
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
    current_year = now().year

    not_confirmed_employees = EmployeeWorkDetails.objects.filter(
        OrganizationID=selectedOrganizationID,
        EmpStatus="Not Confirmed",
        IsDelete=False,
        IsSecondary=False
    )
    not_confirmed_count = not_confirmed_employees.count()
    not_confirmed_data = fetch_employee_data(not_confirmed_employees)

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

    ff_employees = EmployeeWorkDetails.objects.filter(
        OrganizationID=selectedOrganizationID,
        EmpStatus="F&F In process",
        IsDelete=False,
        IsSecondary=False
    )
    ffpro_count = ff_employees.count()
    ff_datapro = fetch_employee_data(ff_employees)

    birthday_employees = EmployeePersonalDetails.objects.annotate(
        birth_month=ExtractMonth('DateofBirth')
    ).filter(
        birth_month=current_month,
        OrganizationID=selectedOrganizationID,
        IsDelete=False
    )
    birthday_count = birthday_employees.count()
    birthday_data = fetch_employee_data_with_birthday(birthday_employees)

    unmatched_count, unmatched_employees = fetch_unmatched_employee_details(selectedOrganizationID)

    joinning_employees = EmployeeWorkDetails.objects.annotate(
        joinning_month=ExtractMonth('DateofJoining'),
        joinning_year=ExtractYear('DateofJoining')
    ).filter(
        joinning_month=current_month,
        joinning_year=current_year,
        OrganizationID=selectedOrganizationID,
        IsDelete=False,
        IsSecondary=False
    )
    joinning_count = joinning_employees.count()
    joinning_data = fetch_employee_joing_(joinning_employees)

    # Encrypt EmpID in not_confirmed_data
    for emp in not_confirmed_data:
        emp["EmpID"] = encrypt_id_filter(emp["EmpID"])

    # Encrypt EmpID in ff_datapro
    for emp in ff_datapro:
        emp["EmpID"] = encrypt_id_filter(emp["EmpID"])

    # Encrypt EmpID in birthday_data
    for emp in birthday_data:
        if emp.get("EmpID"):  # make sure EmpID exists
            emp["EmpID"] = encrypt_id_filter(emp["EmpID"])

    # Encrypt EmpID in joinning_data
    for emp in joinning_data:
        if emp.get("EmpID"):
            emp["EmpID"] = encrypt_id_filter(emp["EmpID"])

    return JsonResponse({
        'emp_status_counts': emp_status_counts,
        'not_confirmed_count': not_confirmed_count,
        'not_confirmed_data': not_confirmed_data,
        'resigned_count': resigned_count,
        'resigned_data': resigned_data,
        'birthday_count': birthday_count,
        'birthday_data': birthday_data,
        'unmatched_count': unmatched_count,
        'unmatched_employees': unmatched_employees,
        'ffpro_count': ffpro_count,
        'ff_datapro': ff_datapro,
        'joinning_count': joinning_count,
        'joinning_data': joinning_data,
        'selectedOrganizationID': selectedOrganizationID,
        'UserID': UserID,
    }, safe=False)


from django.db.models import Subquery, OuterRef, Value, F
from django.db.models.functions import Concat

def ManagerNameandDesignation(request, OrganizationID):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    work_details = EmployeeWorkDetails.objects.filter(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,IsSecondary=False,
        OrganizationID=OrganizationID,EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"]
    ).values('Designation')

    employees = EmployeePersonalDetails.objects.annotate(
        work_designation=Subquery(work_details[:1]),
        full_name=Concat(
            F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
        )
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID
    ).values('full_name', 'work_designation')

   

    return employees if employees else None


# def EmployeeNameOnTheBasisofDesignation(DepartmentName, OrganizationID):
#     level_exclusions = ['A', 'E', 'T']

    
#     on_roll_designations = list(
#         OnRollDesignationMaster.objects.filter(
#             IsDelete=False,
#             OnRollDepartmentMaster__DepartmentName=DepartmentName
#         )
#         .exclude(Lavel__in=level_exclusions)
#         .values('designations', 'Order')
#     )
    
#     corporate_designations = list(
#         CorporateDesignationMaster.objects.filter(
#             IsDelete=False,
#             # CorporateDepartmentMaster__DepartmentName=DepartmentName
#         )
#         .exclude(Lavel__in=level_exclusions)
#         .values('designations', 'Order')
#     )
    
#     for designation in corporate_designations:
#         designation['designations'] += ' - Nile'
    
#     merged_designations = on_roll_designations + corporate_designations
    
#     for designation in merged_designations:
#         if ' - Nile' in designation['designations']:
#             clean_designation = designation['designations'].replace(' - Nile', '').strip()
#             OrganizationIDNile  = 3 
#             employee_names = get_employee_names_by_designation(OrganizationIDNile, clean_designation)
#         else:
#             employee_names = get_employee_names_by_designation(OrganizationID, designation['designations'])
        
#         designation['EmployeeName'] = employee_names if employee_names else ''
    
#     merged_designations.sort(key=lambda x: (x['designations'], x.get('Order', 0)))
    
#     return merged_designations

# ---------------------------------------------------------

def EmployeeNameOnTheBasisofDesignation(DepartmentName, OrganizationID):
    level_exclusions = ['A', 'E', 'T']
    department_conditions = [DepartmentName, 'Executive Office','Human Resources']
    
    on_roll_designations = list(
        OnRollDesignationMaster.objects.filter(
            IsDelete=False,
            OnRollDepartmentMaster__DepartmentName__in=department_conditions
        )
        .exclude(Lavel__in=level_exclusions)
        .values('designations', 'Order')
    )
    
    corporate_designations = list(
        CorporateDesignationMaster.objects.filter(
            IsDelete=False,
        )
        .exclude(Lavel__in=level_exclusions)
        .values('designations', 'Order')
    )
    
    for designation in corporate_designations:
        designation['designations'] += ' - Nile'
    
    merged_designations = on_roll_designations + corporate_designations
    
    for designation in merged_designations:
        if ' - Nile' in designation['designations']:
            clean_designation = designation['designations'].replace(' - Nile', '').strip()
            OrganizationIDNile = 3
            employee_names = get_employee_names_by_designation(OrganizationIDNile, clean_designation)
        else:
            employee_names = get_employee_names_by_designation(OrganizationID, designation['designations'])
        
        designation['EmployeeName'] = employee_names if employee_names else ''
    
    merged_designations.sort(key=lambda x: (x['designations'], x.get('Order', 0)))
    
    return merged_designations





def HrNameOnTheBasisofDesignation(OrganizationID):
    level_exclusions = ['A', 'E', 'T']
    DepartmentName = 'Human Resources'
    
    
    on_roll_designations = list(
        OnRollDesignationMaster.objects.filter(
            IsDelete=False,
            OnRollDepartmentMaster__DepartmentName = DepartmentName  
        )
        .exclude(Lavel__in=level_exclusions)
        .values('designations', 'Order')
    )
    
    corporate_designations = list(
        CorporateDesignationMaster.objects.filter(
            IsDelete=False,
        )
        .exclude(Lavel__in=level_exclusions)
        .values('designations', 'Order')
    )
    
    for designation in corporate_designations:
        designation['designations'] += ' - Nile'
    
    merged_designations = on_roll_designations + corporate_designations
    
    for designation in merged_designations:
        if ' - Nile' in designation['designations']:
            clean_designation = designation['designations'].replace(' - Nile', '').strip()
            OrganizationIDNile = 3
            employee_names = get_employee_names_by_designation(OrganizationIDNile, clean_designation)
        else:
            employee_names = get_employee_names_by_designation(OrganizationID, designation['designations'])
        
        designation['EmployeeName'] = employee_names if employee_names else ''
    
    merged_designations.sort(key=lambda x: (x['designations'], x.get('Order', 0)))
    
    return merged_designations





def HrManagerNameandDesignation(request,OrganizationID):
        if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
        else:
            print("Show Page Session")
        work_details = EmployeeWorkDetails.objects.filter(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,IsSecondary=False,
        OrganizationID=OrganizationID,EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"]
        ).values('Designation')

        employees = EmployeePersonalDetails.objects.annotate(
            work_designation=Subquery(work_details[:1]),
            full_name=Concat(
                F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
            )
        ).filter(
            IsDelete=False,
            OrganizationID=OrganizationID
        ).values('full_name', 'work_designation')

       
        return employees if employees else None



def EmployeeDetailsDataFromDesignation(Designation,OrganizationID):
        
    Workobj = EmployeeWorkDetails.objects.filter(OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False, Designation=Designation).first()
    if Workobj is None:
         Workobj = EmployeeWorkDetails.objects.filter(OrganizationID=3, IsDelete=False,IsSecondary=False, Designation=Designation).first()
    if Workobj is not None :
         EmpP = EmployeePersonalDetails.objects.filter(EmpID=Workobj.EmpID,IsDelete=False).first()
         if EmpP is not None:
              return EmpP


def TargetAssignNames(request, OrganizationID, ReportingtoDesignation):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    # else:
    #     print("Show Page Session")
    
    if OrganizationID == '3':
        work_details = EmployeeWorkDetails.objects.filter(
            EmpID=OuterRef('EmpID'),
            ReportingtoDesignation =  ReportingtoDesignation,
            IsDelete=False,IsSecondary=False,
            OrganizationID=OrganizationID
        ).values('Designation')[:1] 
    else:
         work_details = EmployeeWorkDetails.objects.filter(
            EmpID=OuterRef('EmpID'),
            IsDelete=False,IsSecondary=False,
            ReportingtoDesignation =  ReportingtoDesignation,
             EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"],
            OrganizationID=OrganizationID
        ).values('Designation')[:1] 
         
    employees = EmployeePersonalDetails.objects.annotate(
        work_designation=Subquery(work_details),
        DateofJoining=Subquery(work_details.values('DateofJoining')[:1]),
        full_name=Concat(
            F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
        )
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID
    )

    employees = employees.filter(work_designation__isnull=False)

    return employees if employees else None



from django.db.models import OuterRef, Subquery, F, Value
from django.db.models.functions import Concat


from django.db.models import Q, OuterRef, Subquery, F, Value
from django.db.models.functions import Concat
from django.shortcuts import redirect

def TargetAssignNamesWithReportingtoDesignationEmployeeNameCode(request, OrganizationID, ReportingtoDesignation):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    print("Show Page Session")

    work_details_filter = Q(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,IsSecondary=False,
        OrganizationID=OrganizationID,
        EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"],
    )

    if OrganizationID == '3':
        work_details_filter &= (Q(ReportingtoDesignation=ReportingtoDesignation) | Q(Designation=ReportingtoDesignation))
    else:
        work_details_filter &= (Q(ReportingtoDesignation=ReportingtoDesignation) | Q(Designation=ReportingtoDesignation))

    work_details = EmployeeWorkDetails.objects.filter(work_details_filter).values('Designation')[:1]

    # Subquery for Date of Joining
    doj_subquery = EmployeeWorkDetails.objects.filter(work_details_filter).values('DateofJoining')[:1]

    employees = EmployeePersonalDetails.objects.annotate(
        work_designation=Subquery(work_details),
        date_of_joining=Subquery(doj_subquery),

        full_name=Concat(
            F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
        )
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID,
        work_designation__isnull=False
    )

    return employees if employees.exists() else None

def TargetAssignNamesWithReportingtoDesignationEmployeeNameCode_New(request, OrganizationID, ReportingtoDesignation):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    work_details_filter = Q(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,
        IsSecondary=False,
        OrganizationID=OrganizationID,
        EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"],
    )

    if OrganizationID == '3':
        work_details_filter &= (Q(ReportingtoDesignation=ReportingtoDesignation) | Q(Designation=ReportingtoDesignation))

    designation_subquery = EmployeeWorkDetails.objects.filter(work_details_filter).values('Designation')[:1]
    doj_subquery = EmployeeWorkDetails.objects.filter(work_details_filter).values('DateOfJoining')[:1]

    employees = EmployeePersonalDetails.objects.annotate(
        Designation=Subquery(designation_subquery),
        DateofJoining=Subquery(doj_subquery),  # <-- make sure key matches the template
        full_name=Concat(F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName'))
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID,
        Designation__isnull=False
    )

    return employees if employees.exists() else None


from django.db.models import OuterRef, Subquery, Value, F
from django.db.models.functions import Concat

def EmployeeNameandDesignation(request, OrganizationID):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    # Define work_details subquery to include all required fields
    work_details = EmployeeWorkDetails.objects.filter(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,IsSecondary=False,
       OrganizationID=OrganizationID,EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"]
    ).values(
        'Designation', 'Department', 'Level', 'ReportingtoDesignation', 
        'ReportingtoDepartment', 'ReportingtoLevel', 'DottedLine'
    )

    # Annotate the main queryset with each individual field from work_details and concatenated name
    employees = EmployeePersonalDetails.objects.annotate(
        designation=Subquery(work_details.values('Designation')[:1]),
        department=Subquery(work_details.values('Department')[:1]),
        level=Subquery(work_details.values('Level')[:1]),
        reporting_to_designation=Subquery(work_details.values('ReportingtoDesignation')[:1]),
        reporting_to_department=Subquery(work_details.values('ReportingtoDepartment')[:1]),
        reporting_to_level=Subquery(work_details.values('ReportingtoLevel')[:1]),
        dotted_line=Subquery(work_details.values('DottedLine')[:1]),
        full_name=Concat(
            F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
        )
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID
    ).values(
        'full_name', 'EmployeeCode', 'designation', 'department', 'level', 
        'reporting_to_designation', 'reporting_to_department', 
        'reporting_to_level', 'dotted_line','EmpID'
    )
    employees = [employee for employee in employees if employee['designation'] is not None]

    return employees if employees else None



def EmployeeNameonTheBasisofDepartment(Department, OrganizationID):
    level_exclusions = ['A', 'E', 'T']
    department_conditions = [Department, 'Executive Office', 'Human Resources','Nile Regional Office']
    
    on_roll_designations = list(
        OnRollDesignationMaster.objects.filter(
            IsDelete=False,
            #OnRollDepartmentMaster__DepartmentName__in=department_conditions
        )
        .exclude(Lavel__in=level_exclusions)
        .values('designations', 'Order')
    )
    
    corporate_designations = list(
        CorporateDesignationMaster.objects.filter(
            IsDelete=False,
        )
        .exclude(Lavel__in=level_exclusions)
        .values('designations', 'Order')
    )
    
    for designation in corporate_designations:
        designation['designations'] += ' - Nile'
    
    merged_designations = []
    
    for designation in on_roll_designations + corporate_designations:
        if ' - Nile' in designation['designations']:
            clean_designation = designation['designations'].replace(' - Nile', '').strip()
            OrganizationIDNile = 3
            employee_names = get_employee_names_by_designation(OrganizationIDNile, clean_designation)
        else:
            employee_names = get_employee_names_by_designation(OrganizationID, designation['designations'])
        
        if employee_names: 
            designation['EmployeeName'] = employee_names
            merged_designations.append(designation)
    
    merged_designations.sort(key=lambda x: (x['designations'], x.get('Order', 0)))
    
    return merged_designations







from django.db.models import OuterRef, Subquery, F, Value
from django.db.models.functions import Concat

# def EmployeeNameandDesignationFilter(request, OrganizationID, department=None, emp_id=None):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
    
#     work_details = EmployeeWorkDetails.objects.filter(
#         EmpID=OuterRef('EmpID'),
#         IsDelete=False,IsSecondary=False,
#         OrganizationID=OrganizationID,EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"]
#     ).values(
#         'Designation', 'Department', 'Level', 'ReportingtoDesignation', 
#         'ReportingtoDepartment', 'ReportingtoLevel', 'DottedLine'
#     )

#     employees = EmployeePersonalDetails.objects.annotate(
#         designation=Subquery(work_details.values('Designation')[:1]),
#         department=Subquery(work_details.values('Department')[:1]),
#         level=Subquery(work_details.values('Level')[:1]),
#         reporting_to_designation=Subquery(work_details.values('ReportingtoDesignation')[:1]),
#         reporting_to_department=Subquery(work_details.values('ReportingtoDepartment')[:1]),
#         reporting_to_level=Subquery(work_details.values('ReportingtoLevel')[:1]),
#         dotted_line=Subquery(work_details.values('DottedLine')[:1]),
#         full_name=Concat(
#             F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
#         )
#     ).filter(
#         IsDelete=False,
#         OrganizationID=OrganizationID
#     )

#     if department:
#         employees = employees.filter(department=department)
#     if emp_id:
#         employees = employees.filter(EmpID=emp_id)
    
#     return employees.values(
#         'full_name', 'EmployeeCode', 'designation', 'department', 'level', 
#         'reporting_to_designation', 'reporting_to_department', 
#         'reporting_to_level', 'dotted_line', 'EmpID'
#     ) if employees else None


# def EmployeeNameandDesignationFilter(request, OrganizationID, department=None, emp_id=None):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
    
#     employees = EmployeePersonalDetails.objects.filter(
#         IsDelete=False,
#         OrganizationID=OrganizationID
#     )

#     if department:
#         employees = employees.filter(department=department)
#     if emp_id:
#         employees = employees.filter(EmpID=emp_id)
    
#     employee_data = []
    
#     for employee in employees:
#         work_details = EmployeeWorkDetails.objects.filter(
#             EmpID=employee.EmpID,
#             IsDelete=False,
#             IsSecondary=False,
#             OrganizationID=OrganizationID,
#             EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"]
#         ).values(
#             'Designation', 'Department', 'Level', 'ReportingtoDesignation', 
#             'ReportingtoDepartment', 'ReportingtoLevel', 'DottedLine'
#         ).first()  
        
#         if work_details:
#             employee_data.append({
#                 'full_name': f"{employee.FirstName} {employee.MiddleName} {employee.LastName}",
#                 'EmployeeCode': employee.EmployeeCode,
#                 'designation': work_details.get('Designation'),
#                 'department': work_details.get('Department'),
#                 'level': work_details.get('Level'),
#                 'reporting_to_designation': work_details.get('ReportingtoDesignation'),
#                 'reporting_to_department': work_details.get('ReportingtoDepartment'),
#                 'reporting_to_level': work_details.get('ReportingtoLevel'),
#                 'dotted_line': work_details.get('DottedLine'),
#                 'EmpID': employee.EmpID
#             })
    
#     return employee_data if employee_data else None

def EmployeeNameandDesignationFilter(request, OrganizationID, department=None, emp_id=None):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    # Step 1: Fetch all employees first
    employees = EmployeePersonalDetails.objects.filter(
        IsDelete=False,
        OrganizationID=OrganizationID
    )

    if emp_id:
        employees = employees.filter(EmpID=emp_id)

    employee_data = []

    for employee in employees:
        # Step 2: Get work details
        work_details = EmployeeWorkDetails.objects.filter(
            EmpID=employee.EmpID,
            IsDelete=False,
            IsSecondary=False,
            OrganizationID=OrganizationID,
            EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"]
        ).first()

        if not work_details:
            continue

        # Step 3: Apply department filter (NOW CORRECT)
        if department and work_details.Department != department:
            continue

        # Step 4: Add to list
        employee_data.append({
            'full_name': f"{employee.FirstName} {employee.MiddleName} {employee.LastName}",
            'EmployeeCode': employee.EmployeeCode,
            'designation': work_details.Designation,
            'department': work_details.Department,
            'level': work_details.Level,
            'reporting_to_designation': work_details.ReportingtoDesignation,
            'reporting_to_department': work_details.ReportingtoDepartment,
            'reporting_to_level': work_details.ReportingtoLevel,
            'dotted_line': work_details.DottedLine,
            'EmpID': employee.EmpID
        })

    return employee_data if employee_data else None



def get_employee_names_by_designation(OrganizationID, designation):
    work_details = EmployeeWorkDetails.objects.filter(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,IsSecondary=False,
        OrganizationID=OrganizationID,EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"]
    ).values('Designation')
    
    employees = EmployeePersonalDetails.objects.annotate(
        designation=Subquery(work_details.values('Designation')[:1]),
        full_name=Concat(
            F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
        )
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID,
        designation=designation 
    ).values_list('full_name').first()
    
    return employees[0] if employees else None


from django.db.models import F, Value
from django.db.models.functions import Concat

def get_employee_name_by_code(OrganizationID, employee_code):
    try:
        employee = EmployeePersonalDetails.objects.filter(
            EmployeeCode=employee_code,
            OrganizationID=OrganizationID,
            IsDelete=False
        ).annotate(
            full_name=Concat(
                F('FirstName'), Value(' '),
                F('MiddleName'), Value(' '),
                F('LastName')
            )
        ).values_list('full_name', flat=True).first()

        return employee.strip() if employee else None

    except Exception as e:
        print(f"Error in get_employee_name_by_code: {e}")
        return None




def get_employee_designation_by_EmployeeCode(OrganizationID, EmployeeCode):
    work_details = EmployeeWorkDetails.objects.filter(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,IsSecondary=False,
        OrganizationID=OrganizationID
    ).values('Designation')
    
    employees = EmployeePersonalDetails.objects.annotate(
        designation=Subquery(work_details.values('Designation')[:1]),
        full_name=Concat(
            F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
        )
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID,
        EmployeeCode=EmployeeCode 
    ).values_list('designation').first()
    
    return employees[0] if employees else None





def get_employee_designation_by_EmployeeCode_For_Waring(OrganizationID, EmployeeCode):
    work_details = EmployeeWorkDetails.objects.filter(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,IsSecondary=False,
        OrganizationID=OrganizationID
    ).values('Designation')
    
    employees = EmployeePersonalDetails.objects.annotate(
        designation=Subquery(work_details.values('Designation')[:1]),
        full_name=Concat(
            F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
        )
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID,
        EmployeeCode=EmployeeCode 
    ).values_list('designation').first()
    
    return employees[0] if employees else None





def get_employee_department_by_EmployeeCode(OrganizationID, EmployeeCode):
    work_details = EmployeeWorkDetails.objects.filter(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,IsSecondary=False,
        OrganizationID=OrganizationID
    ).values('Department')
    
    employees = EmployeePersonalDetails.objects.annotate(
        department=Subquery(work_details.values('Department')[:1]),
        full_name=Concat(
            F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
        )
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID,
        EmployeeCode=EmployeeCode 
    ).values_list('department').first()
    
    return employees[0] if employees else None





def get_employee_name_designation_by_EmployeeCode(OrganizationID, EmployeeCode):
    work_details = EmployeeWorkDetails.objects.filter(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,IsSecondary=False,
        OrganizationID=OrganizationID,EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"]
    ).values('Designation')
    
    employees = EmployeePersonalDetails.objects.annotate(
        designation=Subquery(work_details.values('Designation')[:1]),
        full_name=Concat(
            F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
        )
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID,
        EmployeeCode=EmployeeCode 
    ).values_list('full_name').first()
    
    return employees[0] if employees else None





def get_employee_name_designation_by_EmployeeCode_For_Waring(OrganizationID, EmployeeCode):
    work_details = EmployeeWorkDetails.objects.filter(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,IsSecondary=False,
        OrganizationID=OrganizationID,
        # EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"]
    ).values('Designation')
    
    employees = EmployeePersonalDetails.objects.annotate(
        designation=Subquery(work_details.values('Designation')[:1]),
        full_name=Concat(
            F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
        )
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID,
        EmployeeCode=EmployeeCode 
    ).values_list('full_name').first()
    
    return employees[0] if employees else None




def ReptoDesignation(request, OrganizationID, EmployeeCode):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    work_details = EmployeeWorkDetails.objects.filter(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,IsSecondary=False,
        OrganizationID=OrganizationID
    ).values('Designation')

    employee = EmployeePersonalDetails.objects.annotate(
        work_designation=Subquery(work_details[:1])
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID,
        EmployeeCode=EmployeeCode
    ).values('work_designation').first()

    return employee if employee else None


def get_employee_details_with_mobile():
    personal_details = EmployeePersonalDetails.objects.filter(IsDelete=False).values(
        'EmpID', 'FirstName', 'LastName', 'MobileNumber'
    )
 
    work_details = EmployeeWorkDetails.objects.filter(IsDelete=False).values(
        'EmpID', 'Department', 'Designation', 'Level'
    )
 
    work_details_dict = {wd['EmpID']: wd for wd in work_details}
 
    for pd in personal_details:
        wd = work_details_dict.get(pd['EmpID'], {})
        print(
            f"EmpID: {pd['EmpID']}, Name: {pd['FirstName']} {pd['LastName']}, "
            f"Mobile Number: {pd['MobileNumber']}, Department: {wd.get('Department', 'N/A')}, "
            f"Designation: {wd.get('Designation', 'N/A')}, Level: {wd.get('Level', 'N/A')}"
        )

def DepartmentofEmployee(request, OrganizationID, EmployeeCode):
    print(OrganizationID,EmployeeCode)
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    work_details = EmployeeWorkDetails.objects.filter(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,IsSecondary=False,
        OrganizationID=OrganizationID
    ).values('Department')

    employee = EmployeePersonalDetails.objects.annotate(
        work_Department=Subquery(work_details[:1])
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID,
        EmployeeCode=EmployeeCode
    ).values('work_Department').first()

    return employee if employee else None





def EmployeeIsRD(request, OrganizationID, EmployeeCode):
    print(OrganizationID,EmployeeCode)
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    work_details = EmployeeWorkDetails.objects.filter(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,IsSecondary=False,
        OrganizationID=OrganizationID
    ).values('Level')

    employee = EmployeePersonalDetails.objects.annotate(
        Level=Subquery(work_details[:1])
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID,
        EmployeeCode=EmployeeCode
    ).values('Level').first()
    # RdList = ['R5']
    RdList = ['R6', 'R5']
    if employee:
         if employee['Level'] in RdList:
              return True

    return False



def MultipleDepartmentofEmployee(OrganizationID, EmployeeCode):
    personal_details = EmployeePersonalDetails.objects.filter(
        IsDelete=False,
        OrganizationID=OrganizationID,
        EmployeeCode=EmployeeCode
    )

    if personal_details.exists():
        personal_details=personal_details.first()
        work_details_qs = EmployeeWorkDetails.objects.filter(
            EmpID=personal_details.EmpID,  
            IsDelete=False,
            OrganizationID=OrganizationID
        )
        if work_details_qs.exists():
            department_list = list(work_details_qs.values_list('Department', flat=True))
            return department_list
    return None



from django.db.models import F, Value
from django.db.models.functions import Concat

def get_Appraisers_ReportingtoDesignation(OrganizationID, ReportingtoDesignation):
    default_OrganizationID = 3
    
    try:
        employee_work_details_Rep = EmployeeWorkDetails.objects.filter(
            OrganizationID=OrganizationID,
            Designation=ReportingtoDesignation,
            IsDelete=False, IsSecondary=False
        ).first()
        
        # Check if the first query returns None and if so, fallback to the default organization
        if employee_work_details_Rep is None:
            employee_work_details = EmployeeWorkDetails.objects.filter(
                OrganizationID=default_OrganizationID,
                Designation=ReportingtoDesignation,
                IsDelete=False, IsSecondary=False
            ).first()
        else:
            employee_work_details = employee_work_details_Rep
        
        # Ensure that employee_work_details is not None before continuing
        if employee_work_details:
            # If there's a valid employee, try to get the full name
            employee_work_details_Rep = EmployeeWorkDetails.objects.filter(
                OrganizationID=default_OrganizationID,
                Designation=employee_work_details.ReportingtoDesignation,
                IsDelete=False, IsSecondary=False
            ).first()

            full_name = EmployeePersonalDetails.objects.annotate(
                full_name=Concat(
                    F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
                )
            ).filter(
                OrganizationID=OrganizationID,
                EmpID=employee_work_details.EmpID,
                IsDelete=False
            ).values_list('full_name').first()

            if full_name is None:
                # Fallback if no name is found in the current organization
                full_name = EmployeePersonalDetails.objects.annotate(
                    full_name=Concat(
                        F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
                    )
                ).filter(
                    OrganizationID=default_OrganizationID,
                    EmpID=employee_work_details.EmpID,
                    IsDelete=False
                ).values_list('full_name').first()

            return full_name[0] if full_name else None
        
    except AttributeError as e:
        # Handle case where employee_work_details is None and EmpID cannot be accessed
        print(f"Error: {e}")
        return None
    except Exception as e:
        # Handle any other unforeseen exceptions
        print(f"Unexpected error: {e}")
        return None


          

     

def upload_file(file,id,folder_name,ModelName):
        if ModelName == "EmployeeEmergencyInformationDetails_Pan":
            new_file = upload_file_to_blob(file,id,folder_name,ModelName)
            new_file.PanFileTitle = file.name
            new_file.save()
        elif ModelName == "EmployeeEmergencyInformationDetails_Aadhaar":
            new_file = upload_file_to_blob(file,id,folder_name,ModelName)
            new_file.AadhaarFileTitle = file.name
            new_file.save()    
        elif ModelName == "EmployeeEmergencyInformationDetails_License":
            new_file = upload_file_to_blob(file,id,folder_name,ModelName)
            new_file.DrivingFileTitle = file.name
            new_file.save()   
                 
        elif ModelName == "EmployeePersonalDetails":
            new_file = upload_file_to_blob(file,id,folder_name,ModelName)
            new_file.ProfileImageFileTitle = file.name
            new_file.save()   
        
        else:
            new_file = upload_file_to_blob(file,id,folder_name,ModelName)
            new_file.FileTitle = file.name
            new_file.save()



def Humanview_file(request):
    ID = request.GET.get('ID')
    model_name = request.GET.get('model') 

    if model_name == 'EmployeePersonalDetails':
        try:
            file = EmployeePersonalDetails.objects.get(EmpID=ID)
        except EmployeePersonalDetails.DoesNotExist:
            raise Http404("EmployeePersonalDetails record not found.")
    elif model_name == 'EmployeeQualificationDetails':
        try:
            file = EmployeeQualificationDetails.objects.get(id=ID)
        except EmployeeQualificationDetails.DoesNotExist:
            raise Http404("EmployeeQualificationDetails record not found.")
    elif model_name == 'EmployeePreviousWorkInformationDetails':
        try:
            file = EmployeePreviousWorkInformationDetails.objects.get(id=ID)
        except EmployeePreviousWorkInformationDetails.DoesNotExist:
            raise Http404("EmployeePreviousWorkInformationDetails record not found.")    
    
    elif model_name == 'EmployeeDocumentsInformationDetails':
        try:
            file = EmployeeDocumentsInformationDetails.objects.get(id=ID)
        except EmployeeDocumentsInformationDetails.DoesNotExist:
            raise Http404("EmployeeDocumentsInformationDetails record not found.")
    elif model_name == 'EmployeeIdentityInformationDetails_Pan':
        try:
            file = EmployeeIdentityInformationDetails.objects.get(id=ID)
        except EmployeeIdentityInformationDetails.DoesNotExist:
            raise Http404("EmployeeIdentityInformationDetails record not found.")  
    elif model_name == 'EmployeeIdentityInformationDetails_Aadhaar':
        try:
            file = EmployeeIdentityInformationDetails.objects.get(id=ID)
        except EmployeeIdentityInformationDetails.DoesNotExist:
            raise Http404("EmployeeIdentityInformationDetails record not found.")
    elif model_name == 'EmployeeIdentityInformationDetails_License':
        try:
            file = EmployeeIdentityInformationDetails.objects.get(id=ID)
        except EmployeeIdentityInformationDetails.DoesNotExist:
            raise Http404("EmployeeIdentityInformationDetails record not found.")            



    else:
        raise Http404("Invalid model name.")

    if model_name == "EmployeeIdentityInformationDetails_Pan":
        file_id = file.PanFileName
        file_name = file.PanFileTitle
        file_type, _ = mimetypes.guess_type(file_id)
    elif model_name == "EmployeeIdentityInformationDetails_Aadhaar":
        file_id = file.AadhaarFileName
        file_name = file.AadhaarFileTitle
        file_type, _ = mimetypes.guess_type(file_id)
    elif model_name == "EmployeeIdentityInformationDetails_License":
        file_id = file.DrivingFileName
        file_name = file.DrivingFileTitle
        file_type, _ = mimetypes.guess_type(file_id)
    
    elif model_name == "EmployeePersonalDetails":
        file_id = file.ProfileImageFileName
        file_name = file.ProfileImageFileTitle
        file_type, _ = mimetypes.guess_type(file_id)


    else:

        file_id = file.FileName
        file_name = file.FileTitle
        file_type, _ = mimetypes.guess_type(file_id)

    
    
    
    
    if file_type is None:
        file_type = 'application/octet-stream'
    
    blob_content = download_blob(file_id)
    
    if blob_content:
        response = HttpResponse(blob_content.readall(), content_type=file_type)
        response['Content-Disposition'] = f'inline; filename="{file_name}"'
        return response
    else:
        raise Http404("File content not found.")

from django.http import JsonResponse

from .models import EmployeeUrlMaster
from django.urls import reverse



def ActiveLink(EmpID,return_dict=False):
    Links = {
        'EMPIDActive': False,
        'WorkIDActive':False,
        'FamilyIDActive': False,
        'EmergencyIDActive': False,
        'EducationsIDActive': False,
        'PreviousworkIDActive': False,
        'DocumentIDActive': False,
        'AddressIDActive': False,
        'IdentityIDActive': False,
        'BankIDActive': False,

        'LeaveIDActive': False,
        'SalaryIDActive': False,


    }
  

    
    if EmpID is not None:
            Links['EMPIDActive'] = True    
            Emobj  = EmployeePersonalDetails.objects.filter(IsDelete=False,EmpID = EmpID).values('EmployeeCode').first()
            if Emobj:
                EmployeeCode = Emobj['EmployeeCode']
            
            workobj = EmployeeWorkDetails.objects.filter(EmpID=EmpID, IsDelete=False,IsSecondary=False).first()
            if workobj is not None:
                Links['WorkIDActive'] = True

            Finfoobj = EmployeeFamilyDetails.objects.filter(EmpID=EmpID, IsDelete=False).first()
            if Finfoobj is not None:
                Links['FamilyIDActive'] = True


            Emergencyobj = EmployeeEmergencyInformationDetails.objects.filter(EmpID=EmpID, IsDelete=False).first()
            if Emergencyobj is not None:
                Links['EmergencyIDActive'] = True

            
            Educations = EmployeeQualificationDetails.objects.filter(EmpID=EmpID, IsDelete=False)
            if Educations.exists():
                Links['EducationsIDActive'] = True

            previousworks = EmployeePreviousWorkInformationDetails.objects.filter(EmpID=EmpID, IsDelete=False)
            if previousworks.exists():
                Links['PreviousworkIDActive'] = True

            Documents = EmployeeDocumentsInformationDetails.objects.filter(EmpID=EmpID, IsDelete=False)
            if Documents.exists():
                Links['DocumentIDActive'] = True

            Addressinfo = EmployeeAddressInformationDetails.objects.filter(EmpID=EmpID, IsDelete=False).first()
            if Addressinfo is not None:
                Links['AddressIDActive'] = True

            IdentityInfo = EmployeeIdentityInformationDetails.objects.filter(EmpID=EmpID, IsDelete=False).first()
            if IdentityInfo is not None:
                Links['IdentityIDActive'] = True

            Bankinfo = EmployeeBankInformationDetails.objects.filter(EmpID=EmpID, IsDelete=False).first()
            if Bankinfo is not None:
                Links['BankIDActive'] = True

            Leaveinfo = Emp_Leave_Balance_Master.objects.filter(Emp_code=EmployeeCode, IsDelete=False)
            if Leaveinfo.exists():
                Links['LeaveIDActive'] = True    

            salaryinfo = Salary_Detail_Master.objects.filter(EmpID=EmpID, IsDelete=False)
            if salaryinfo.exists():
                Links['SalaryIDActive'] = True


            
                

    if return_dict:
        return Links


from django.http import JsonResponse
from rest_framework import status
from django.http import JsonResponse
from rest_framework import status
from django.http import JsonResponse
from rest_framework import status

def CheckEmployeeCode(request):
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    token = request.headers.get('hotel-api-token')

    # Validate API token
    if token != hotelapitoken:
        return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)

    EmployeeCode = request.GET.get('EmployeeCode')
    OrganizationID = request.GET.get('OrganizationID')

    # Validate parameters
    if not EmployeeCode or not OrganizationID:
        return JsonResponse({"error": "Employee Code or Organization ID not provided."}, status=status.HTTP_400_BAD_REQUEST)
    EmployeeCodeobj = None 
    workobj = None
    
    # Query for existing employee code
    EmployeeCodeobj = EmployeePersonalDetails.objects.filter(
        OrganizationID=OrganizationID, 
        EmployeeCode=EmployeeCode,
        IsDelete=False
    ).first()
    if  EmployeeCodeobj:
            workobj = EmployeeWorkDetails.objects.filter(
            OrganizationID=OrganizationID, 
            EmpID=EmployeeCodeobj.EmpID,
            IsDelete=False,IsSecondary=False
        ).exclude(EmpStatus__in=['Archive']).first()
         

    # Check if the employee exists
    if workobj is not None and EmployeeCodeobj is not None:
        return JsonResponse({
            "status": "exists",
            "message": f"Already exists."
        }, status=status.HTTP_200_OK)
    else:
        return JsonResponse({
            "status": "not_found",
            "message": f"No employee found with code '{EmployeeCode}'."
        }, status=status.HTTP_200_OK)


def generate_next_employee_code(OrganizationID):
    last_emp = EmployeePersonalDetails.objects.filter(
        OrganizationID=OrganizationID,
        IsDelete=False,
        IsEmployeeCreated=True
    ).order_by('-EmpID').first()

    if last_emp and last_emp.EmployeeCode:
        # Extract number part
        last_number = int(last_emp.EmployeeCode.replace('EMP', ''))
        next_number = last_number + 1
    else:
        next_number = 1

    return f"EMP{next_number:04d}"


from django.http import HttpResponseBadRequest

def NewEmployeeDataForm(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    ActiveLinkDict  = None
    HrEmobj  = None
    EmpID = None
    Emobj = None  
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    CurrentUrl = 'NewEmployeePersonalData'
    urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    if urlobj:
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName

    last_emp = None
    if OrganizationID:
        last_emp = EmployeePersonalDetails.objects.filter(
            OrganizationID=OrganizationID,
            IsDelete=False,
            IsEmployeeCreated=True
        ).order_by('-EmpID').first()
    else:
        last_emp = ''
        
    print("last_emp::",last_emp.EmployeeCode)
    print("OrganizationID::",OrganizationID)


    IND = request.GET.get('IND', None)  # IND Means Employee_InterviewAssessmentID 
    D = request.GET.get('D', None)      # D means Employee_IASource

    InterviewID = None
    Emobj = None

    # Only process interview data if both IND and D are present
    if IND and IND.isdigit() and D == 'IA':
        Mobj = EmployeeDataRequest_Master.objects.filter(InterviewID=IND, IsDelete=False).first()
        if Mobj:
            InterviewID = Mobj.InterviewID
            Emobj = EmployeePersonalData.objects.filter(DataMasterID=InterviewID, IsDelete=False).first()
     
  
    if UserID  is not None  and D != "IA":
            HrEmobj = EmployeePersonalDetails.objects.filter(
                OrganizationID=OrganizationID, IsDelete=False, CreatedBy=UserID,IsEmployeeCreated=False
            ).order_by('-CreatedDateTime').first()
            if HrEmobj is not None:
                EmpID  = HrEmobj.EmpID     
        
    ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

    if request.method == "POST":
        EmployeeCode  = request.POST['EmployeeCode']
        Prefix  = request.POST['Prefix']
        FirstName = request.POST['FirstName']
        MiddleName = request.POST['MiddleName']
        LastName = request.POST['LastName']
        Gender = request.POST['Gender']
        MaritalStatus = request.POST['MaritalStatus']
        DateofBirth = request.POST['DateofBirth']
        age = request.POST['age']
        MobileNumber = request.POST['MobileNumber']
        EmailAddress = request.POST['EmailAddress']
        ProfileImage  = request.FILES.get('ProfileImage')
        IllnessDetails = request.POST['IllnessDetails']
        Pre_EmpID   = request.POST['Pre_EmpID']

        
        if HrEmobj  is not None:
            Em = EmployeePersonalDetails.objects.filter(EmpID=EmpID ).first()
            Em.EmployeeCode = EmployeeCode
            Em.Prefix  = Prefix
            Em.FirstName  = FirstName
            Em.MiddleName  = MiddleName
            Em.LastName = LastName
            Em.Gender  = Gender
            Em.MaritalStatus  = MaritalStatus
            Em.DateofBirth  = DateofBirth 
            Em.age = age
            Em.MobileNumber = MobileNumber
            Em.EmailAddress  = EmailAddress
            Em.DetailsofIllness  = IllnessDetails
            Em.ModifyBy  =  UserID
            
            if IND and D:
                Em.InterviewAssessmentID  = IND
                Em.Source  = D
            Em.save()
            if ProfileImage:
                    upload_file(ProfileImage, Em.EmpID, "ProfileImage","EmployeePersonalDetails")   
                    
            
        else:
            HrEmobj  = EmployeePersonalDetails.objects.create(
                EmployeeCode = EmployeeCode,
                Prefix  = Prefix,
                FirstName = FirstName,
                MiddleName = MiddleName,
                LastName  = LastName,
                Gender = Gender,
                MaritalStatus = MaritalStatus ,
                DateofBirth  = DateofBirth ,
                age  = age,
                MobileNumber  = MobileNumber,
                EmailAddress  = EmailAddress,
                DetailsofIllness = IllnessDetails,
                OrganizationID = OrganizationID,
                CreatedBy = UserID,
                InterviewAssessmentID=IND, 
                Source=D
            )
            if Pre_EmpID:
                File  = EmployeePersonalData.objects.filter(id=Pre_EmpID).first()
                if File:
                    file_content, file_type = CopyFile(File.FileName)
                    file_io = BytesIO(file_content)
                    file_io.name = File.FileName 
                    upload_file(file_io, HrEmobj.EmpID, "ProfileImage","EmployeePersonalDetails")    
            else:
                if ProfileImage:
                    upload_file(ProfileImage, HrEmobj.EmpID, "ProfileImage","EmployeePersonalDetails") 
            
        EmpID  = HrEmobj.EmpID
        EmployeeCode   = HrEmobj.EmployeeCode
        url = reverse(Nexturl)  
        redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}"  
        return redirect(redirect_url)
        
     
    # Perseonal Details Dict
    EmobjhrDict = {
        'id': HrEmobj.EmpID if HrEmobj and HrEmobj.EmpID else Emobj.id if Emobj and Emobj.id else '',
        'EmployeeCode': HrEmobj.EmployeeCode if HrEmobj and HrEmobj.EmployeeCode else '',
        'Prefix': HrEmobj.Prefix if HrEmobj and HrEmobj.Prefix else Emobj.Prefix if Emobj and Emobj.Prefix else '',
        'FirstName': HrEmobj.FirstName if HrEmobj and HrEmobj.FirstName else Emobj.FirstName if Emobj and Emobj.FirstName else '',
        'MiddleName': HrEmobj.MiddleName if HrEmobj and HrEmobj.MiddleName else Emobj.MiddleName if Emobj and Emobj.MiddleName else '',
        'LastName': HrEmobj.LastName if HrEmobj and HrEmobj.LastName else Emobj.LastName if Emobj and Emobj.LastName else '',
        'Gender': HrEmobj.Gender if HrEmobj and HrEmobj.Gender else Emobj.Gender if Emobj and Emobj.Gender else '',
        'MaritalStatus': HrEmobj.MaritalStatus if HrEmobj and HrEmobj.MaritalStatus else Emobj.MaritalStatus if Emobj and Emobj.MaritalStatus else '',
        'DateofBirth': HrEmobj.DateofBirth if HrEmobj and HrEmobj.DateofBirth else Emobj.DateofBirth if Emobj and Emobj.DateofBirth else '',
        'age': HrEmobj.age if HrEmobj and HrEmobj.age else Emobj.age if Emobj and Emobj.age else '',
        'MobileNumber': HrEmobj.MobileNumber if HrEmobj and HrEmobj.MobileNumber else Emobj.MobileNumber if Emobj and Emobj.MobileNumber else '',
        'EmailAddress': HrEmobj.EmailAddress if HrEmobj and HrEmobj.EmailAddress else Emobj.EmailAddress if Emobj and Emobj.EmailAddress else '',
        'DetailsofIllness': HrEmobj.DetailsofIllness if HrEmobj and HrEmobj.DetailsofIllness else '',
        'id': HrEmobj.EmpID if HrEmobj and HrEmobj.EmpID and HrEmobj.ProfileImageFileName else Emobj.id if Emobj and Emobj.id else '',
    
    }
    
    ProfileImagePreview =  'HrEmobj' if HrEmobj else ('Emobj' if Emobj else '')    
    
    context = {
        'Emobj':EmobjhrDict,
        'ProfileImagePreview':ProfileImagePreview,
        'ActiveLinkDict':ActiveLinkDict,
        'CurrentUrl':CurrentUrl,
        'D':D,
        'Nexturl':Nexturl,
        'EmpID':EmpID,
        'IND':IND,
        'hotelapitoken':hotelapitoken,
        'OrganizationID':OrganizationID
    }
    return render(request, 'HR/NewEmployeeAdd/NewEmployeePersonalData.html', context)

def NewEmployeePersonalData(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    ActiveLinkDict  = None
    CurrentUrl = 'NewEmployeePersonalData'
    urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    if urlobj:
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName


    HrEmobj  = None
    EmpID = None
  
    IND = request.GET.get('IND')
    D = request.GET.get('D')
    EmpID   =  request.GET.get('EmpID')
    

    if EmpID is not None:
         HrEmobj  = EmployeePersonalDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID).first()
         HrEmobj.id  = HrEmobj.EmpID
         HrEmobj.save()

    ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

    if request.method == "POST":
                
                EmployeeCode  = request.POST['EmployeeCode']
                Prefix  = request.POST['Prefix']
                FirstName = request.POST['FirstName']
                MiddleName = request.POST['MiddleName']
                LastName = request.POST['LastName']
                Gender = request.POST['Gender']
                MaritalStatus = request.POST['MaritalStatus']
                DateofBirth = request.POST['DateofBirth']
                age = request.POST['age']
                MobileNumber = request.POST['MobileNumber']
                EmailAddress = request.POST['EmailAddress']
                ProfileImage  = request.FILES.get('ProfileImage')
                # CovidVaccination = request.POST['CovidVaccination']
                IllnessDetails = request.POST['IllnessDetails']
                Pre_EmpID   =request.POST['Pre_EmpID']

                
               
                if HrEmobj  is not None:
                    Em = EmployeePersonalDetails.objects.filter(EmpID=EmpID ).first()
                    Em.EmployeeCode = EmployeeCode
                    Em.Prefix  = Prefix
                    Em.FirstName  = FirstName
                    Em.MiddleName  = MiddleName
                    Em.LastName = LastName
                    Em.Gender  = Gender
                    Em.MaritalStatus  = MaritalStatus
                    Em.DateofBirth  = DateofBirth 
                    Em.age = age
                    Em.MobileNumber = MobileNumber
                    Em.EmailAddress  = EmailAddress
                    # Em.CovidVaccination  = CovidVaccination
                    Em.DetailsofIllness  = IllnessDetails
                    Em.ModifyBy  =  UserID
                    Em.save()
                    if ProfileImage:
                         upload_file(ProfileImage, Em.EmpID, "ProfileImage","EmployeePersonalDetails")   
                         
                 
                else:
                    
                    HrEmobj  = EmployeePersonalDetails.objects.create(
                        EmployeeCode = EmployeeCode,
                        Prefix  = Prefix,
                        FirstName = FirstName,
                        MiddleName = MiddleName,
                        LastName  = LastName,
                        Gender = Gender,
                        MaritalStatus = MaritalStatus ,
                        DateofBirth  = DateofBirth ,
                        age  = age,
                        MobileNumber  = MobileNumber,
                        EmailAddress  = EmailAddress,
                        # CovidVaccination = CovidVaccination,
                        DetailsofIllness = IllnessDetails,
                        OrganizationID = OrganizationID,
                        CreatedBy = UserID
                    )
                    if Pre_EmpID:
                         File  = EmployeePersonalData.objects.filter(id=Pre_EmpID).first()
                         if File:
                            file_content, file_type = CopyFile(File.FileName)
                            file_io = BytesIO(file_content)
                            file_io.name = File.FileName 
                            upload_file(file_io, HrEmobj.EmpID, "ProfileImage","EmployeePersonalDetails")    
                    else:
                        if ProfileImage:
                            upload_file(ProfileImage, HrEmobj.EmpID, "ProfileImage","EmployeePersonalDetails")           
                    
                EmpID  = HrEmobj.EmpID
                EmployeeCode   = HrEmobj.EmployeeCode
                url = reverse(Nexturl)  
                redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}"  
                return redirect(redirect_url)

    ProfileImagePreview =  'HrEmobj'
    
    context = {
        'Emobj':HrEmobj,
        'ProfileImagePreview':ProfileImagePreview,
        'ActiveLinkDict':ActiveLinkDict,
        'CurrentUrl':CurrentUrl,
        'D':D,
        'Nexturl':Nexturl,
        'EmpID':EmpID,
        'IND':IND,
        'hotelapitoken':hotelapitoken,
        'OrganizationID':OrganizationID
    }
    return render(request, 'HR/NewEmployeeAdd/NewEmployeePersonalData.html', context)

from .models import SalaryHistory


# def NewEmployeeWorkData(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
    
#     OrganizationID =request.session["OrganizationID"]
#     UserID =str(request.session["UserID"])

#     Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
#     DottedLineDesignations = CorporateDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
#     MergedDesignations = chain(Designations, DottedLineDesignations)
   
#     MergedDottedLineDesignations =  chain(Designations, DottedLineDesignations)
#     MergedReportingtoDesignation =  chain(Designations, DottedLineDesignations)
   
#     if OrganizationID == "3":
#             Designations = CorporateDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
  
#     IND = request.GET.get('IND')
#     D = request.GET.get('D')
#     EmpID = request.GET.get('EmpID')

    
    
   
#     if EmpID is not None:
#         Workobj  = EmployeeWorkDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID).first()
#         Datafrom = 'DatafromHR'
#         if Workobj is None and D == "IA":
#                     Workobj = {}
               
                 
#                     Designationobj = Assessment_Master.objects.filter(IsDelete=False, OrganizationID=OrganizationID, id=IND).first()
                    
                    
#                     if Designationobj:
#                         Designation = Designationobj.position
#                         Workobj['Designation'] = Designation
#                         Workobj['DateofJoining'] = Designationobj.ProposedDOJ
#                         Datafrom = 'DatafromIN'


                

#     ActiveLinkDict  = None
#     ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

   

#     CurrentUrl = 'NewEmployeeWorkData'

#     urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
#     Nexturl = CurrentUrl
#     PreviousUrl = CurrentUrl
#     if urlobj:
#         # Next Url
#         Increament = urlobj.sortorder
#         Increament   = Increament + 1
#         nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
#         if nextobj:
#             Nexturl = nextobj.UrlName
#         # Previous Url
#         Decreament = urlobj.sortorder
#         Decreament   = Decreament - 1
#         Prevtobj  = EmployeeUrlMaster.objects.filter(sortorder=Decreament).first()
#         if Prevtobj:
#             PreviousUrl = Prevtobj.UrlName

#     if request.method == "POST":
#                 Designation = request.POST['Designation']
#                 Department  = request.POST['Department']
#                 Level  = request.POST['Level']
#                 ReportingtoDesignation = request.POST['ReportingToDesignation']
#                 ReportingtoDepartment = request.POST['ReportingToDesignationDepartment']
#                 ReportingtoLevel = request.POST['ReportingToDesignationLevel']
#                 DottedLine = request.POST['DottedLine'] or ''
#                 Vip = request.POST.get('VipCheckbox')
#                 VipCheckbox = False
                
#                 if Vip  == 'Vip':
#                      VipCheckbox = True
#                 OfficialEmailAddress = None
#                 if 'OfficialEmailAddress' in request.POST:
#                     OfficialEmailAddress = request.POST['OfficialEmailAddress']
#                 OfficialMobileNo = None
#                 if 'OfficialMobileNo' in request.POST:
#                     OfficialMobileNo  = request.POST['OfficialMobileNo']
#                 DateofJoining = request.POST['DateOfJoining']
#                 CompanyAccommodation  =  request.POST['CompanyAccommodation']
                
#                 Locker  =  request.POST['Locker']
#                 LockerType  =  request.POST['LockerType']
#                 LockerNumber  = request.POST['LockerNumber']
#                 EmploymentType   = request.POST['EmploymentType']
#                 ContractStartDate  = None
#                 if 'ContractStartDate' in request.POST:
#                     ContractStartDate  =  request.POST['ContractStartDate'] 
#                     if ContractStartDate == '':
#                         ContractStartDate  = None
                         
#                 ContractEndDate  = None
#                 if 'ContractEndDate' in request.POST:    
#                     ContractEndDate  = request.POST['ContractEndDate']
#                     if ContractEndDate == '':
#                         ContractEndDate  = None

#                 if Workobj  is not None and Datafrom  == 'DatafromHR':
#                     Workobj.Designation  = Designation
#                     Workobj.Department  = Department
#                     Workobj.Level  = Level
#                     Workobj.ReportingtoDesignation  = ReportingtoDesignation
#                     Workobj.ReportingtoDepartment  = ReportingtoDepartment
#                     Workobj.ReportingtoLevel  = ReportingtoLevel
#                     Workobj.DottedLine  = DottedLine
#                     Workobj.VipCheckbox  = VipCheckbox


#                     Workobj.OfficialEmailAddress = OfficialEmailAddress
#                     Workobj.OfficialMobileNo  = OfficialMobileNo
#                     Workobj.DateofJoining = DateofJoining
#                     Workobj.CompanyAccommodation  = CompanyAccommodation
#                     Workobj.Locker = Locker
#                     Workobj.LockerType = LockerType
#                     Workobj.LockerNumber  = LockerNumber
#                     Workobj.EmploymentType  = EmploymentType
#                     Workobj.ContractEndDate = ContractEndDate
#                     Workobj.ContractStartDate = ContractStartDate
#                     Workobj.ModifyBy = UserID
#                     Workobj.save()


#                 else:

#                     Workobj = EmployeeWorkDetails.objects.create(EmpID = EmpID,
#                          Designation = Designation,Department =Department,Level=Level,ReportingtoDesignation = ReportingtoDesignation,ReportingtoDepartment =ReportingtoDepartment,ReportingtoLevel  = ReportingtoLevel,OfficialEmailAddress = OfficialEmailAddress,OfficialMobileNo = OfficialMobileNo,DateofJoining = DateofJoining,CompanyAccommodation = CompanyAccommodation,Locker = Locker,LockerType = LockerType,LockerNumber = LockerNumber,EmploymentType  =EmploymentType,ContractEndDate = ContractEndDate,ContractStartDate =  ContractStartDate, OrganizationID = OrganizationID,CreatedBy = UserID,DottedLine=DottedLine,VipCheckbox=VipCheckbox
#                     )
#                 if OrganizationID == "3":
#                      hrobj  =  EmployeePersonalDetails.objects.filter(EmpID=EmpID,OrganizationID=OrganizationID,IsDelete=False).first()
#                      if   hrobj:
#                         hrobj.IsEmployeeCreated =  True
#                         hrobj.save()
#                         result = update_employee_profile(EmpID, OrganizationID)
#                         return redirect('EmployeeList')
                     
               

#                 url = reverse(Nexturl)  
#                 redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}"  
#                 return redirect(redirect_url)

    
#     context = {'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl,'Nexturl':Nexturl,'MergedDesignations':MergedDesignations,'Workobj':Workobj,'EmpID':EmpID,'PreviousUrl':PreviousUrl,'IND':IND,'D':D,'MergedDottedLineDesignations':MergedDottedLineDesignations,
#     'MergedReportingtoDesignation':MergedReportingtoDesignation,
#     'OrganizationID':str(OrganizationID)}
#     return render(request, 'HR/NewEmployeeAdd/NewEmployeeWorkData.html', context)



def NewEmployeeWorkData(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    DottedLineDesignations = CorporateDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    MergedDesignations = chain(Designations, DottedLineDesignations)
   
    MergedDottedLineDesignations =  chain(Designations, DottedLineDesignations)
    MergedReportingtoDesignation =  chain(Designations, DottedLineDesignations)
   
    if OrganizationID == "3":
        Designations = CorporateDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
  
    IND = request.GET.get('IND')
    D = request.GET.get('D')
    EmpID = request.GET.get('EmpID')

   
    if EmpID is not None:
        Workobj  = EmployeeWorkDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,IsSecondary=False,EmpID = EmpID).first()
        Datafrom = 'DatafromHR'
        if Workobj is None and D == "IA":
            Workobj = {}
        
            Designationobj = Assessment_Master.objects.filter(IsDelete=False, OrganizationID=OrganizationID, id=IND).first()
            
            if Designationobj:
                Designation = Designationobj.position
                Workobj['Designation'] = Designation
                Workobj['DateofJoining'] = Designationobj.ProposedDOJ
                Datafrom = 'DatafromIN'
                
    ActiveLinkDict  = None
    ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

    CurrentUrl = 'NewEmployeeWorkData'

    urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = EmployeeUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName

    if request.method == "POST":
                Designation = request.POST['Designation']
                Department  = request.POST['Department']
                Division  = request.POST['Division']      # New
                # print("Division ::", Division)
                Level  = request.POST['Level']
                ReportingtoDivision  = request.POST['ReportingtoDivision']      # New
                # print("ReportingtoDivision ::", ReportingtoDivision)
                ReportingtoDesignation = request.POST['ReportingToDesignation']
                ReportingtoDepartment = request.POST['ReportingToDesignationDepartment']
                ReportingtoLevel = request.POST['ReportingToDesignationLevel']
                DottedLine = request.POST['DottedLine'] or ''
                # Vip = request.POST.get('VipCheckbox')
                # WeekOffDay = request.POST.get('WeekOffDay') or ''

                VipCheckbox = False
                
                # if Vip  == 'Vip':
                #      VipCheckbox = True
                
                OfficialEmailAddress = None
                if 'OfficialEmailAddress' in request.POST:
                    OfficialEmailAddress = request.POST['OfficialEmailAddress']
                    
                OfficialMobileNo = None
                if 'OfficialMobileNo' in request.POST:
                    OfficialMobileNo  = request.POST['OfficialMobileNo']
                    
                DateofJoining = request.POST['DateOfJoining']
                CompanyAccommodation  =  request.POST['CompanyAccommodation']
                AccommodationFlatNumber  =  request.POST['AccommodationFlatNumber'] or ''
                
                Locker  =  request.POST['Locker']
                LockerType  =  request.POST['LockerType']
                LockerNumber  = request.POST['LockerNumber']
                EmploymentType   = request.POST['EmploymentType']
                
                ContractStartDate  = None
                if 'ContractStartDate' in request.POST:
                    ContractStartDate  =  request.POST['ContractStartDate'] 
                    if ContractStartDate == '':
                        ContractStartDate  = None
                         
                ContractEndDate  = None
                if 'ContractEndDate' in request.POST:    
                    ContractEndDate  = request.POST['ContractEndDate']
                    if ContractEndDate == '':
                        ContractEndDate  = None

                if Workobj  is not None and Datafrom  == 'DatafromHR':
                    Workobj.Designation  = Designation
                    Workobj.Department  = Department
                    Workobj.Division  = Division    # New
                    Workobj.Level  = Level
                    Workobj.ReportingtoDivision  = ReportingtoDivision     # New
                    Workobj.ReportingtoDesignation  = ReportingtoDesignation
                    Workobj.ReportingtoDepartment  = ReportingtoDepartment
                    Workobj.ReportingtoLevel  = ReportingtoLevel
                    Workobj.DottedLine  = DottedLine
                    Workobj.VipCheckbox  = VipCheckbox
                    # Workobj.WeekOffDay  = WeekOffDay

                    Workobj.OfficialEmailAddress = OfficialEmailAddress
                    Workobj.OfficialMobileNo  = OfficialMobileNo
                    Workobj.DateofJoining = DateofJoining
                    Workobj.CompanyAccommodation  = CompanyAccommodation
                    Workobj.Locker = Locker
                    Workobj.LockerType = LockerType
                    Workobj.LockerNumber  = LockerNumber
                    Workobj.EmploymentType  = EmploymentType
                    Workobj.ContractEndDate = ContractEndDate
                    Workobj.ContractStartDate = ContractStartDate
                    Workobj.AccommodationFlatNumber = AccommodationFlatNumber
                    Workobj.save()


                else:

                    Workobj = EmployeeWorkDetails.objects.create(
                        EmpID = EmpID,
                        Designation = Designation,
                        Department =Department,
                        Division = Division,
                        Level=Level,
                        ReportingtoDivision = ReportingtoDivision,
                        ReportingtoDesignation = ReportingtoDesignation,
                        ReportingtoDepartment =ReportingtoDepartment,
                        ReportingtoLevel  = ReportingtoLevel,
                        OfficialEmailAddress = OfficialEmailAddress,
                        OfficialMobileNo = OfficialMobileNo,
                        DateofJoining = DateofJoining,
                        CompanyAccommodation = CompanyAccommodation,
                        AccommodationFlatNumber = AccommodationFlatNumber,
                        Locker = Locker,
                        LockerType = LockerType,
                        LockerNumber = LockerNumber,
                        EmploymentType  =EmploymentType,
                        ContractEndDate = ContractEndDate,
                        ContractStartDate =  ContractStartDate, 
                        OrganizationID = OrganizationID,
                        CreatedBy = UserID,
                        DottedLine=DottedLine,
                        VipCheckbox=VipCheckbox,
                        # WeekOffDay=WeekOffDay
                    )
                    
                if OrganizationID == "3" and VipCheckbox ==  True:
                     hrobj  =  EmployeePersonalDetails.objects.filter(EmpID=EmpID,OrganizationID=OrganizationID,IsDelete=False).first()
                     if hrobj:
                        hrobj.IsEmployeeCreated =  True
                        hrobj.save()
                        result = update_employee_profile(EmpID, OrganizationID)
                        return redirect('EmployeeList')

                url = reverse(Nexturl)  
                redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}"  
                return redirect(redirect_url)

    
    context = {
        'ActiveLinkDict':ActiveLinkDict,
        'CurrentUrl':CurrentUrl,
        'Nexturl':Nexturl,
        'MergedDesignations':MergedDesignations,
        'Workobj':Workobj,
        'EmpID':EmpID,
        'PreviousUrl':PreviousUrl,
        'IND':IND,
        'D':D,
        'MergedDottedLineDesignations':MergedDottedLineDesignations,
        'MergedReportingtoDesignation':MergedReportingtoDesignation,
        'OrganizationID':str(OrganizationID)
    }
    return render(request, 'HR/NewEmployeeAdd/NewEmployeeWorkData.html', context)




def NewEmployeeFamilyinfo(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    IND = request.GET.get('IND')
    EmpID   =  request.GET.get('EmpID')
    D = request.GET.get('D')
    ActiveLinkDict  = None
    ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

    Finfoobj  = None
    childs  = None
    Childbbj  = None
    FamilyObj  = None
    Childbbj   = None

    CurrentUrl = 'NewEmployeeFamilyinfo'

    urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = EmployeeUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName
    if IND is not None and D == "IA":
        Emobj = EmployeePersonalData.objects.filter(DataMasterID=IND,IsDelete=False).first()
      
        if Emobj:
            INEmpID  = Emobj.id
            if INEmpID is not None:
               
                Finfoobj =  EmployeeFamilyData.objects.filter(MasterID = INEmpID,IsDelete=False).first()
                if Finfoobj is not None:
                    childs  =  EmployeeChildData.objects.filter(IsDelete=False,FamilyID = Finfoobj.id)
    
    if EmpID is not None:
         FamilyObj =  EmployeeFamilyDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID).first()
         
         if FamilyObj is not  None:
            Childbbj = EmployeeChildDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,FamilyID = FamilyObj.id)
    
    
    if request.method == "POST":
                SpouseName = request.POST.get('SpouseName', None)
                SpouseAge = request.POST.get('SpouseAge', 0)
                if SpouseAge == '' :
                     SpouseAge = '' 
                SpouseDOB = request.POST.get('SpouseDOB', None)
                if SpouseDOB == '':
                        SpouseDOB = None 
                SpouseContactNo = request.POST.get('SpouseContact', None)


                MotherName = request.POST.get('MotherName', None)
                MotherAge = request.POST.get('MotherAge', 0)
                if MotherAge == '' :
                     SpouseAge = ''
                MotherDOB = request.POST.get('MotherDOB', None)
                if MotherDOB == '':
                        MotherDOB = None 
                MotherContactNo = request.POST.get('MotherContact', None)

                FatherName = request.POST.get('FatherName', None)
                FatherAge = request.POST.get('FatherAge', 0)
                if FatherAge == '' :
                     SpouseAge = ''
                FatherDOB = request.POST.get('FatherDOB', None)
                if FatherDOB == '':
                        FatherDOB = None 
                FatherContactNo = request.POST.get('FatherContact', None)
                
                            
                # LandlineNo = request.POST.get('LandlineNo', None)
                child_update_ids  = request.POST.getlist('child_ids[]')
             
                child_names = request.POST.getlist('childName[]')
                child_ages = request.POST.getlist('childAge[]')
                child_relations = request.POST.getlist('childrelations[]')
                
                removed_child_ids_str = request.POST.get('removed_child_ids[]')


                removed_child_ids = []
                if removed_child_ids_str:
                    try:
                        # Only include numeric strings in the list, skip any non-numeric values
                        removed_child_ids = [int(id_str) for id_str in removed_child_ids_str.split(',') if id_str.isdigit()]
                    except ValueError as e:
                        print(f"Error parsing removed_child_ids: {e}")

                # LandlineNo = request.POST['LandlineNo']
                if FamilyObj is not None:
                    FamilyObj.SpouseName  = SpouseName
                    FamilyObj.SpouseAge  = SpouseAge
                    FamilyObj.SpouseContactNo = SpouseContactNo
                    FamilyObj.SpouseDateofBirth  = SpouseDOB

                    FamilyObj.MotherName = MotherName
                    FamilyObj.MotherDateofBirth  = MotherDOB
                    FamilyObj.MotherAge  = MotherAge
                    FamilyObj.MotherContactNo = MotherContactNo

                    FamilyObj.FatherName  = FatherName  
                    FamilyObj.FatherDateofBirth = FatherDOB
                    FamilyObj.FatherAge  = FatherAge
                    FamilyObj.FatherContactNo = FatherContactNo
                    FamilyObj.ModifyBy = UserID
                    # FamilyObj.LandlineNo = LandlineNo
                    FamilyObj.save()
                    

                 
                    # if len(removed_child_ids) > 0:
                    #     for rid in removed_child_ids:
                    #         rdelete = EmployeeChildDetails.objects.filter(id=rid).first()
                    #         if rdelete:
                    #             rdelete.IsDelete = True
                    #             rdelete.save()
                      # Proceed if there are valid IDs
                    if removed_child_ids:
                            for rid in removed_child_ids:
                                rdelete = EmployeeChildDetails.objects.filter(id=rid).first()
                                if rdelete:
                                    rdelete.IsDelete = True
                                    rdelete.save()

                    for id, name, age, relation in zip(child_update_ids, child_names, child_ages, child_relations):
                        if id.startswith('new_'):
                         
                            EmployeeChildDetails.objects.create(
                                FamilyID=FamilyObj.id,
                                Name=name,
                                Age=age,
                                Relation=relation,
                                OrganizationID=OrganizationID,
                                CreatedBy=UserID
                            )
                        else:
                            updated_rows = EmployeeChildDetails.objects.filter(FamilyID=FamilyObj.id, id=id).update(
                                Name=name,
                                Age=age,
                                Relation=relation
                            )
                           
                            if not updated_rows:
                                EmployeeChildDetails.objects.create(
                                    FamilyID=FamilyObj.id,
                                    Name=name,
                                    Age=age,
                                    Relation=relation,
                                    OrganizationID=OrganizationID,
                                    CreatedBy=UserID
                                )
                else:
                     FamilyObj = EmployeeFamilyDetails.objects.create(
                        EmpID = EmpID,
                        SpouseName = SpouseName,
                        SpouseAge = SpouseAge,
                        SpouseContactNo = SpouseContactNo,
                        SpouseDateofBirth = SpouseDOB,
                        MotherName = MotherName,
                        MotherDateofBirth = MotherDOB,
                        MotherAge = MotherAge,
                        MotherContactNo = MotherContactNo,
                        FatherName = FatherName,  
                        FatherDateofBirth = FatherDOB,
                        FatherAge = FatherAge,
                        FatherContactNo = FatherContactNo,
                        # LandlineNo=LandlineNo
                        OrganizationID = OrganizationID,
                        CreatedBy = UserID                       
                     )
                     if len(child_names) > 0:
                        for name, age, relation in zip(child_names, child_ages, child_relations):
                                cobj  = EmployeeChildDetails.objects.create(
                                    FamilyID = FamilyObj.id,
                                    Name = name,
                                    Age = age,
                                    Relation = relation,OrganizationID = OrganizationID,CreatedBy = UserID
                                )  
                
                url = reverse(Nexturl)  
                redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}" 
                return redirect(redirect_url)
    SpouseChild = True 
    if EmpID:
         Employeeobj  = EmployeePersonalDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID=EmpID).first()     
         if Employeeobj.MaritalStatus ==  'Unmarried':
                SpouseChild = False 
    context = {
        'SpouseChild':SpouseChild,
        'ActiveLinkDict':ActiveLinkDict,
        'CurrentUrl':CurrentUrl,
        'Nexturl':Nexturl,
        'EmpID':EmpID,
        'PreviousUrl':PreviousUrl,
        'IND':IND,
        'D':D,
        'Finfoobj':FamilyObj if FamilyObj else( Finfoobj if Finfoobj else None ) ,
        'childs': Childbbj if Childbbj else (childs if childs else None),          
    }
    return render(request, 'HR/NewEmployeeAdd/NewEmployeeFamilyinfo.html', context)

def NewEmployeeEmergencyinfo(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    IND = request.GET.get('IND')
    EmpID   =  request.GET.get('EmpID')
    D = request.GET.get('D')
   
    ActiveLinkDict  = None
    ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

   
    Emergencyobj = None                 
    Emerobj = None
   

    CurrentUrl = 'NewEmployeeEmergencyinfo'

    urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = EmployeeUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName
    if IND is not None and D == "IA":
        Emobj = EmployeePersonalData.objects.filter(DataMasterID=IND,IsDelete=False).first()
      
        if Emobj:
            INEmpID  = Emobj.id
            if INEmpID is not None:
                Emergencyobj = EmployeeEmergencyInfoData.objects.filter(MasterID = INEmpID,IsDelete=False).first()
               
                
    
    if EmpID is not None:
          Emerobj = EmployeeEmergencyInformationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID).first()
         
    
    if request.method == "POST":
                EmergencyFirstName =  request.POST['EmergencyFirstName']
                EmergencyMiddleName =  request.POST['EmergencyMiddleName']
                EmergencyLastName =  request.POST['EmergencyLastName']
                Relation =  request.POST['Relation']
                EmergencyContactNumber_1 = request.POST['EmergencyContactNumber_1']
                EmergencyContactNumber_2 =  request.POST['EmergencyContactNumber_2']
                ProvidentFundNumber  = request.POST['ProvidentFundNumber']
                ESINumber =  request.POST['ESINumber'] or ''
                BloodGroup =  request.POST['BloodGroup']     
              
                if Emerobj  is not None:
                    Emerobj.FirstName  = EmergencyFirstName
                    Emerobj.MiddleName  = EmergencyMiddleName
                    Emerobj.LastName  = EmergencyLastName
                    Emerobj.Relation  = Relation
                    Emerobj.EmergencyContactNumber_1  = EmergencyContactNumber_1
                    Emerobj.EmergencyContactNumber_2 = EmergencyContactNumber_2
                    Emerobj.ProvidentFundNumber = ProvidentFundNumber 
                    Emerobj.ESINumber  = ESINumber
                    Emerobj.BloodGroup  = BloodGroup
                    Emerobj.ModifyBy = UserID
                    Emerobj.save()
                else:
                
                        Emerobj = EmployeeEmergencyInformationDetails.objects.create(
                                                        EmpID =  EmpID,
                                                        FirstName = EmergencyFirstName,
                                                        MiddleName = EmergencyMiddleName,
                                                        LastName = EmergencyLastName,
                                                        Relation  = Relation,
                                                        EmergencyContactNumber_1  = EmergencyContactNumber_1,
                                                        EmergencyContactNumber_2 = EmergencyContactNumber_2,
                                                        ProvidentFundNumber  = ProvidentFundNumber,
                                                        ESINumber  = ESINumber,
                                                        BloodGroup  = BloodGroup, OrganizationID = OrganizationID,CreatedBy = UserID
                                                    )    

                
                
                url = reverse(Nexturl)  
                redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}" 
                return redirect(redirect_url)
         

    context = {'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl,'Nexturl':Nexturl,'EmpID':EmpID,'PreviousUrl':PreviousUrl,'IND':IND,'D':D,'Emergencyobj':Emerobj if Emerobj else( Emergencyobj if Emergencyobj else None )}
    return render(request, 'HR/NewEmployeeAdd/NewEmployeeEmergencyinfo.html', context)


def NewEmployeeQualificationinfo(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    IND = request.GET.get('IND')
    EmpID   =  request.GET.get('EmpID')
    D = request.GET.get('D')
    ActiveLinkDict  = None
    ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

   
    Educations = None                 
    Eduboj = None
   

    CurrentUrl = 'NewEmployeeQualificationinfo'

    urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = EmployeeUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName
    if IND is not None and D == "IA":
        Emobj = EmployeePersonalData.objects.filter(DataMasterID=IND,IsDelete=False).first()
      
        if Emobj:
            INEmpID  = Emobj.id
            if INEmpID is not None:
                Educations  = EmployeeEducationData.objects.filter(MasterID = INEmpID,IsDelete=False)

               
                
    
    if EmpID is not None:
          Eduboj  =  EmployeeQualificationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID)
         

    
    if request.method == "POST":
                EducationType  = request.POST.getlist('EducationType[]')
                DegreeCourse =  request.POST.getlist('DegreeCourse[]')
                InstitutionName = request.POST.getlist('InstitutionName[]')
                Year= request.POST.getlist('Year[]')
                # Percentage  = request.POST.getlist('Percentage[]')
                AttachmentsFile = request.FILES.getlist('AttachmentEducation[]')
                

                Edu_ids = request.POST.getlist('Edu_ids[]')

                removed_Edu_ids_str = request.POST.get('removed_Edu_ids[]', '')
               
                removed_Edu_ids = []
                if removed_Edu_ids_str:
                    try:
                        removed_Edu_ids = [int(id_str) for id_str in removed_Edu_ids_str.split(',') if id_str.isdigit()]
                    except ValueError as e:
                        print(f"Error parsing removed_Edu_ids: {e}")  
               
               
                if len(removed_Edu_ids)>0:
                    for id in removed_Edu_ids:
                        education_delete = EmployeeQualificationDetails.objects.filter(id=id).first()
                        if education_delete:
                            education_delete.IsDelete = True
                            education_delete.save()

                if Edu_ids:
                  
                    i = 0 
                    for id, Education, Degree, Institution, year in zip(Edu_ids, EducationType, DegreeCourse, InstitutionName, Year):
                        if id.startswith('new_'):
                            newEdud = EmployeeQualificationDetails.objects.create(
                                EmpID=EmpID,
                                EducationType=Education,
                                Degree_Course=Degree,
                                NameoftheInstitution=Institution,
                                Year=year,
                              
                                OrganizationID=OrganizationID,
                                CreatedBy=UserID
                            )
                            if len(AttachmentsFile) > 0: 
                                File = AttachmentsFile[i]
                                if  File:
                                    upload_file(File, newEdud.id, "Education", "EmployeeQualificationDetails")
                                i = i + 1

                            

                        else:
                            updated = EmployeeQualificationDetails.objects.filter(
                                EmpID=EmpID, IsDelete=False, id=id
                            ).update(
                                EducationType=Education,
                                Degree_Course=Degree,
                                NameoftheInstitution=Institution,
                                Year=year,
                              
                                ModifyBy=UserID
                            )
                         
                              
                            if not updated:
                                Obj = EmployeeQualificationDetails.objects.create(
                                    EmpID=EmpID,
                                    EducationType=Education,
                                    Degree_Course=Degree,
                                    NameoftheInstitution=Institution,
                                    Year=year,
                                   
                                    OrganizationID=OrganizationID,
                                    CreatedBy=UserID
                                )
                                File = EmployeeEducationData.objects.filter(id=id).first()

                                if File:
                                    file_content, file_type = CopyFile(File.FileName)
                                    
                                   
                                    file_io = BytesIO(file_content)
                                    file_io.name = File.FileName 
                                    
                                    upload_file(file_io, Obj.id, "Education", "EmployeeQualificationDetails")
 


                else:
                    for Education, Degree, Institution, year, Attachment in zip(EducationType, DegreeCourse, InstitutionName, Year, AttachmentsFile):
                        Eobj=EmployeeQualificationDetails.objects.create(
                            EmpID=EmpID,
                            EducationType=Education,
                            Degree_Course=Degree,
                            NameoftheInstitution=Institution,
                            Year=year,
                         
                            OrganizationID=OrganizationID,
                            CreatedBy=UserID
                        )
                        if Attachment:
                                
                                  upload_file(Attachment, Eobj.id, "Education", "EmployeeQualificationDetails")
               

                url = reverse(Nexturl)  
                redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}" 
                return redirect(redirect_url)
    EducationPreview  =  'Eduboj' if Eduboj else ('Educations' if Educations else '')    

    context = {'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl,'Nexturl':Nexturl,'EmpID':EmpID,'PreviousUrl':PreviousUrl,'IND':IND,'D':D, 'Educations':  Eduboj if Eduboj else (Educations if Educations else None),'EducationPreview':EducationPreview}
    return render(request, 'HR/NewEmployeeAdd/NewEmployeeQualificationinfo.html', context)



# def NewEmployeeQualificationinfo(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
    
#     OrganizationID =request.session["OrganizationID"]
#     UserID =str(request.session["UserID"])

#     IND = request.GET.get('IND')
#     EmpID   =  request.GET.get('EmpID')
#     D = request.GET.get('D')
#     ActiveLinkDict  = None
#     ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

   
#     Educations = None                 
#     Eduboj = None
   

#     CurrentUrl = 'NewEmployeeQualificationinfo'

#     urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
#     Nexturl = CurrentUrl
#     PreviousUrl = CurrentUrl
#     if urlobj:
#         # Next Url
#         Increament = urlobj.sortorder
#         Increament   = Increament + 1
#         nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
#         if nextobj:
#             Nexturl = nextobj.UrlName
#         # Previous Url
#         Decreament = urlobj.sortorder
#         Decreament   = Decreament - 1
#         Prevtobj  = EmployeeUrlMaster.objects.filter(sortorder=Decreament).first()
#         if Prevtobj:
#             PreviousUrl = Prevtobj.UrlName
#     if IND is not None and D == "IA":
#         Emobj = EmployeePersonalData.objects.filter(DataMasterID=IND,IsDelete=False).first()
      
#         if Emobj:
#             INEmpID  = Emobj.id
#             if INEmpID is not None:
#                 Educations  = EmployeeEducationData.objects.filter(MasterID = INEmpID,IsDelete=False)

               
                
    
#     if EmpID is not None:
#           Eduboj  =  EmployeeQualificationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID)
         

    
#     if request.method == "POST":
#                 EducationType = request.POST.getlist('EducationType[]')
#                 DegreeCourse = request.POST.getlist('DegreeCourse[]')
#                 InstitutionName = request.POST.getlist('InstitutionName[]')
#                 Year = request.POST.getlist('Year[]')
#                 AttachmentsFile = request.FILES.getlist('AttachmentEducation[]')
#                 FID = request.POST.getlist('FID[]')
#                 Edu_ids = request.POST.getlist('Edu_ids[]')
#                 removed_Edu_ids_str = request.POST.get('removed_Edu_ids[]', '')

#                 # Convert removed education IDs to a list of integers
#                 removed_Edu_ids = [
#                     int(value) for value in removed_Edu_ids_str.split(',') if value.isdigit()
#                 ] if removed_Edu_ids_str else []

#                 # Handle removals (mark records as deleted)
#                 if removed_Edu_ids:
#                     EmployeeQualificationDetails.objects.filter(id__in=removed_Edu_ids).update(IsDelete=True)
               
               
#                 if Edu_ids:
                  
#                     i = 0 
#                     for id, Education, Degree, Institution, year in zip(Edu_ids, EducationType, DegreeCourse, InstitutionName, Year):
#                         if id.startswith('new_'):
#                             newEdud = EmployeeQualificationDetails.objects.create(
#                                 EmpID=EmpID,
#                                 EducationType=Education,
#                                 Degree_Course=Degree,
#                                 NameoftheInstitution=Institution,
#                                 Year=year,
                              
#                                 OrganizationID=OrganizationID,
#                                 CreatedBy=UserID
#                             )
                           
#                             # Handle new file upload
#                             key = f'FID_new_{i}'
#                             if key in FID:
#                                 file_index = FID.index(key)
#                                 if file_index is not None:
#                                     file = AttachmentsFile[file_index]
#                                     if file:
#                                         upload_file(file, newEdud.id, "Education", "EmployeeQualificationDetails")
#                             i += 1    

                            

#                         else:
#                             updated = EmployeeEducationData.objects.filter(
#                                 EmpID=EmpID, IsDelete=False, id=id
#                             ).first()
#                             if updated:
#                                 updated.EducationType = Education
#                                 updated.Degree_Course = Degree
#                                 updated.NameoftheInstitution = Institution
#                                 updated.Year = year
#                                 updated.save()

#                                 # Handle file replacement
#                                 key = f'FID_{id}'
#                                 if key in FID:
#                                     file_index = FID.index(key)
#                                     if file_index is not None:
#                                         file = AttachmentsFile[file_index]
#                                         if file:
                                           
#                                             upload_file(file, updated.id, "Education", "EmployeeQualificationDetails")

                         
                              
#                             if not updated:
#                                 Obj = EmployeeQualificationDetails.objects.create(
#                                     EmpID=EmpID,
#                                     EducationType=Education,
#                                     Degree_Course=Degree,
#                                     NameoftheInstitution=Institution,
#                                     Year=year,
                                   
#                                     OrganizationID=OrganizationID,
#                                     CreatedBy=UserID
#                                 )
#                                 File = EmployeeEducationData.objects.filter(id=id).first()

#                                 if File:
#                                     file_content, file_type = CopyFile(File.FileName)
                                    
                                   
#                                     file_io = BytesIO(file_content)
#                                     file_io.name = File.FileName 
                                    
#                                     upload_file(file_io, Obj.id, "Education", "EmployeeQualificationDetails")
 


#                 else:
#                     i = 1  # Index for dynamic files
#                     for id, education, degree, institution, year in zip(Edu_ids, EducationType, DegreeCourse, InstitutionName, Year):
#                         if id.startswith('new_'):
#                             # Add new record
#                             Educationobj = EmployeeQualificationDetails.objects.create(
#                                 EmpID=EmpID,
#                                 EducationType=education,
#                                 Degree_Course=degree,
#                                 NameoftheInstitution=institution,
#                                 Year=year,
#                             )
#                             # Handle new file upload
#                             key = f'FID_new_{i}'
#                             if key in FID:
#                                 file_index = FID.index(key)
#                                 if file_index is not None:
#                                     file = AttachmentsFile[file_index]
#                                     if file:
#                                         upload_file(file, Educationobj.id, "Education", "EmployeeEducationData")
#                             i += 1
               

#                 url = reverse(Nexturl)  
#                 redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}" 
#                 return redirect(redirect_url)
#     EducationPreview  =  'Eduboj' if Eduboj else ('Educations' if Educations else '')    

#     context = {'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl,'Nexturl':Nexturl,'EmpID':EmpID,'PreviousUrl':PreviousUrl,'IND':IND,'D':D, 'Educations':  Eduboj if Eduboj else (Educations if Educations else None),'EducationPreview':EducationPreview}
#     return render(request, 'HR/NewEmployeeAdd/NewEmployeeQualificationinfo.html', context)

def NewEmployeePreviousWorkinfo(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    IND = request.GET.get('IND')
    EmpID   =  request.GET.get('EmpID')
    D = request.GET.get('D')
   
    ActiveLinkDict  = None
    ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

   
    previousworks = None                 
    prevobj = None
   

    CurrentUrl = 'NewEmployeePreviousWorkinfo'

    urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = EmployeeUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName
    if IND is not None and D == "IA":
        Emobj = EmployeePersonalData.objects.filter(DataMasterID=IND,IsDelete=False).first()
      
        if Emobj:
            INEmpID  = Emobj.id
            if INEmpID is not None:
                previousworks  = EmployeePreviousWorkData.objects.filter(MasterID = INEmpID,IsDelete=False)

               
                
    
    if EmpID is not None:
          prevobj = EmployeePreviousWorkInformationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID)

    
    if request.method == "POST":
                Company =  request.POST.getlist('Company[]')
                Position =  request.POST.getlist('Position[]')
                FromDate =  request.POST.getlist('FromDate[]')
                ToDate =  request.POST.getlist('ToDate[]')
                Salary =  request.POST.getlist('Salary[]')
                AttachmentPreviousWork  = request.FILES.getlist('AttachmentPreviousWork[]')
                
                Pre_ids = request.POST.getlist('Pre_ids[]')
                removed_Pre_ids_str = request.POST.get('removed_Pre_ids[]', '')
               
                # if removed_Pre_ids_str:
                #     removed_Pre_ids = list(map(int, removed_Pre_ids_str.split(',')))  
                # else:
                #     removed_Pre_ids = []

                removed_Pre_ids = []
                if removed_Pre_ids_str:
                    try:
                        removed_Pre_ids = [int(id_str) for id_str in removed_Pre_ids_str.split(',') if id_str.isdigit()]
                    except ValueError as e:
                        print(f"Error parsing removed_Pre_ids: {e}")    
                if len(removed_Pre_ids) > 0:
                      
                        for id in removed_Pre_ids:
                          
                            previousdelete = EmployeePreviousWorkInformationDetails.objects.filter(id=id).first()
                          
                            previousdelete.IsDelete  = True
                            previousdelete.ModifyBy = UserID

                            previousdelete.save()
                if  Pre_ids:
                     p = 0
                     for  id,company,position,fromDate,toDate,salary in zip(Pre_ids,Company,Position,FromDate,ToDate,Salary):
                        if id.startswith('new_'):
                            newPreviousObject  = EmployeePreviousWorkInformationDetails.objects.create(
                                 EmpID =  EmpID,
                                 Company  = company,Position = position,FromDate =fromDate,ToDate = toDate,Salary = salary, OrganizationID=OrganizationID
                            ,CreatedBy=UserID

                            )
                            if len(AttachmentPreviousWork)>0:
                                File = AttachmentPreviousWork[p]
                                if File:
                                    upload_file(File, newPreviousObject.id, "PreviousWork", "EmployeePreviousWorkInformationDetails")

                                p =  p + 1
                        else:
                            PreviousObjectUpdated  = EmployeePreviousWorkInformationDetails.objects.filter( EmpID=EmpID,IsDelete=False, id=id).update(
                            Company  = company
                            ,Position  = position
                            ,FromDate  =fromDate
                            ,ToDate   = toDate
                            ,Salary  = salary
                            ,ModifyBy=UserID
                            )
                            if not  PreviousObjectUpdated:
                                 Pobj  = EmployeePreviousWorkInformationDetails.objects.create(
                                 EmpID =  EmpID,
                                 Company  = company,Position = position,FromDate =fromDate,ToDate = toDate,Salary = salary, OrganizationID=OrganizationID
                                 ,CreatedBy=UserID

                                )
                                 File = EmployeePreviousWorkData.objects.filter(id=id).first()

                                 if File:
                                        file_content, file_type = CopyFile(File.FileName)
                                        
                                    
                                        file_io = BytesIO(file_content)
                                        file_io.name = File.FileName 
                                        
                                        upload_file(file_io, Pobj.id, "PreviousWork", "EmployeePreviousWorkInformationDetails")
                                
                                                 
                           
                else:
                    for  company,position,fromDate,toDate,salary,Attachment in zip(Company,Position,FromDate,ToDate,Salary,AttachmentPreviousWork):
                       
                            PreviousObject  = EmployeePreviousWorkInformationDetails.objects.create(
                                 EmpID =  EmpID,
                                 Company  = company,Position = position,FromDate =fromDate,ToDate = toDate,Salary = salary ,OrganizationID=OrganizationID,   CreatedBy=UserID

                            )

                            if Attachment:
                                
                                  upload_file(File, PreviousObject.id, "PreviousWork", "EmployeePreviousWorkInformationDetails")       
                url = reverse(Nexturl)  
                redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}" 
                return redirect(redirect_url)
    PreviousPreview = 'prevobj' if prevobj else ('previousworks' if previousworks else '')
    context = {'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl,'Nexturl':Nexturl,'EmpID':EmpID,'PreviousUrl':PreviousUrl,'IND':IND,'D':D,  'previousworks': prevobj if prevobj else (previousworks if previousworks else None),'PreviousPreview':PreviousPreview}
    return render(request, 'HR/NewEmployeeAdd/NewEmployeePreviousWorkinfo.html', context)


def NewEmployeeAddressinfo(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    IND = request.GET.get('IND')
    EmpID   =  request.GET.get('EmpID')
    D = request.GET.get('D')
   
    ActiveLinkDict  = None
    ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

   
    Addressinfo = None                 
    Emerobj = None
   

    CurrentUrl = 'NewEmployeeAddressinfo'

    urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = EmployeeUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName
    if IND is not None and D =="IA":
        Emobj = EmployeePersonalData.objects.filter(DataMasterID=IND,IsDelete=False).first()
      
        if Emobj:
            INEmpID  = Emobj.id
            if INEmpID is not None:
                Addressinfo = EmployeeAddressInfoData.objects.filter(MasterID = INEmpID,IsDelete=False).first()

               
                
    
    if EmpID is not None:
          Addressobj = EmployeeAddressInformationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID).first()

    
    if request.method == "POST":
                
                Permanent_Address  =  request.POST['Permanent_Address'] or ''
                Permanent_City   =  request.POST['Permanent_City'] or ''
                Permanent_State  =  request.POST['Permanent_State'] or ''
                Permanent_Pincode  =  request.POST['Permanent_Pincode'] or ''
                Permanent_HousePhoneNumber  =  request.POST['Permanent_HousePhoneNumber'] or ''
                
                # Permanent_LandlineNumber  =  request.POST['Permanent_LandlineNumber'] or ''


                Temporary_Address  =  request.POST['Temporary_Address'] or ''
                Temporary_City   =  request.POST['Temporary_City'] or ''
                Temporary_State  =  request.POST['Temporary_State'] or ''
                Temporary_Pincode  =  request.POST['Temporary_Pincode'] or ''
                Temporary_HousePhoneNumber  =  request.POST['Temporary_HousePhoneNumber'] or ''
                # Temporary_LandlineNumber  =  request.POST['Temporary_LandlineNumber'] or ''

                if Addressobj is not None  :
                   
                        Addressobj.Permanent_Address = Permanent_Address
                        Addressobj.Permanent_City = Permanent_City
                        Addressobj.Permanent_State  = Permanent_State
                        Addressobj.Permanent_Pincode = Permanent_Pincode
                        Addressobj.Permanent_HousePhoneNumber  = Permanent_HousePhoneNumber        
                        # Addressobj.Permanent_Landline  = Permanent_LandlineNumber        
                        
                        Addressobj.Temporary_Address = Temporary_Address        
                        Addressobj.Temporary_City  = Temporary_City        
                        Addressobj.Temporary_Pincode = Temporary_Pincode        
                        Addressobj.Temporary_HousePhoneNumber   = Temporary_HousePhoneNumber
                        # Addressobj.Temporary_Landline   = Temporary_LandlineNumber


                        Addressobj.ModifyBy  = UserID
                        Addressobj.save()        
                        
                else:
                    Addressobj  = EmployeeAddressInformationDetails.objects.create(   EmpID =  EmpID,Permanent_Address  = Permanent_Address,Permanent_City = Permanent_City,Permanent_State = Permanent_State,Permanent_Pincode = Permanent_Pincode,Permanent_HousePhoneNumber = Permanent_HousePhoneNumber,Temporary_Address = Temporary_Address,Temporary_City =Temporary_City,Temporary_State = Temporary_State,Temporary_Pincode=Temporary_Pincode,Temporary_HousePhoneNumber=Temporary_HousePhoneNumber,OrganizationID = OrganizationID,CreatedBy = UserID
                                                                                   )

                
                
                url = reverse(Nexturl)  
                redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}" 
                return redirect(redirect_url)
         

    context = {'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl,'Nexturl':Nexturl,'EmpID':EmpID,'PreviousUrl':PreviousUrl,'IND':IND,'D':D,  'Addressinfo':Addressobj if Addressobj else( Addressinfo if Addressinfo else None ),}
    return render(request, 'HR/NewEmployeeAdd/NewEmployeeAddressinfo.html', context)

def NewEmployeeIdentityinfo(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    IND = request.GET.get('IND')
    EmpID   =  request.GET.get('EmpID')
    D = request.GET.get('D')
   
    ActiveLinkDict  = None
    ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

   
    IdentityInfo = None                 
    identityobj = None
   

    CurrentUrl = 'NewEmployeeIdentityinfo'

    urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = EmployeeUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName
    if IND is not None and D == "IA":
        Emobj = EmployeePersonalData.objects.filter(DataMasterID=IND,IsDelete=False).first()
      
        if Emobj:
            INEmpID  = Emobj.id
            if INEmpID is not None:
                IdentityInfo = EmployeeIdentityInfoData.objects.filter(MasterID = INEmpID,IsDelete=False).first()
                
    
    if EmpID is not None:
             identityobj = EmployeeIdentityInformationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID).first()

    
    if request.method == "POST":
                 # Identity Information 
                Pre_Identity_ID = request.POST['Pre_Identity_ID']
                PANNo = request.POST['PANNo'] or ''
                AadhaarNumber = request.POST['AadhaarNumber'] or ''
                DrivingLicenceNo = request.POST['DrivingLicenceNo'] or ''
                PANattachment = request.FILES.get('PANattachment')
                Aadhaarattachment = request.FILES.get('Aadhaarattachment')
                DrivingLicenceattachment = request.FILES.get('DrivingLicenceattachment')

                if identityobj is not None:
                    identityobj.PANNo  = PANNo
                    identityobj.AadhaarNumber = AadhaarNumber
                    identityobj.DrivingLicenceNo  = DrivingLicenceNo
                    identityobj.ModifyBy  = UserID
                    identityobj.save()
                    if PANattachment:
                                upload_file(PANattachment,identityobj.id,"Docuemnts","EmployeeIdentityInformationDetails_Pan")
                    if Aadhaarattachment:
                                upload_file(Aadhaarattachment,identityobj.id,"Docuemnts","EmployeeIdentityInformationDetails_Aadhaar")
                    if DrivingLicenceattachment:
                                upload_file(DrivingLicenceattachment,identityobj.id,"Docuemnts","EmployeeIdentityInformationDetails_License")            
                                
                                            
                                            


                else:
                    newidentityobj =  EmployeeIdentityInformationDetails.objects.create(   EmpID =  EmpID,
                            PANNo = PANNo,AadhaarNumber = AadhaarNumber,DrivingLicenceNo = DrivingLicenceNo,OrganizationID=OrganizationID,
                                    CreatedBy=UserID
                        )
                    
                    if PANattachment:
                                upload_file(PANattachment,newidentityobj.id,"Docuemnts","EmployeeIdentityInformationDetails_Pan")
                    else:
                         if 'Pre_Identity_ID' in request.POST and Pre_Identity_ID != '' :
                            File  = EmployeeIdentityInfoData.objects.filter(id=Pre_Identity_ID).first()
                            if File and File.PanFileName:
                                        file_content, file_type = CopyFile(File.PanFileName)
                                        
                                    
                                        file_io = BytesIO(file_content)
                                        file_io.name = File.PanFileName 
                                        upload_file(file_io, newidentityobj.id, "Docuemnts","EmployeeIdentityInformationDetails_Pan")
                              

                    if Aadhaarattachment:
                                upload_file(Aadhaarattachment,newidentityobj.id,"Docuemnts","EmployeeIdentityInformationDetails_Aadhaar")
                    else:
                         if 'Pre_Identity_ID' in request.POST and Pre_Identity_ID != '':
                            File  = EmployeeIdentityInfoData.objects.filter(id=Pre_Identity_ID).first()
                            if File  and File.AadhaarFileName:
                                        file_content, file_type = CopyFile(File.AadhaarFileName)
                                        
                                    
                                        file_io = BytesIO(file_content)
                                        file_io.name = File.AadhaarFileName 
                                        upload_file(file_io, newidentityobj.id, "Docuemnts","EmployeeIdentityInformationDetails_Aadhaar")            
                    if DrivingLicenceattachment:
                                upload_file(DrivingLicenceattachment,newidentityobj.id,"Docuemnts","EmployeeIdentityInformationDetails_License")
                    else:
                         if 'Pre_Identity_ID' in request.POST and Pre_Identity_ID != '':
                            File  = EmployeeIdentityInfoData.objects.filter(id=Pre_Identity_ID).first()
                            if File  and File.DrivingFileName:
                                        file_content, file_type = CopyFile(File.DrivingFileName)
                                        
                                    
                                        file_io = BytesIO(file_content)
                                        file_io.name = File.DrivingFileName 
                                        upload_file(file_io, newidentityobj.id, "Docuemnts","EmployeeIdentityInformationDetails_License")    
             

                
                
                url = reverse(Nexturl)  
                redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}" 
                return redirect(redirect_url)
              
    IdentityPreview = 'identityobj' if identityobj else ('IdentityInfo' if IdentityInfo else '')
    context = {'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl,'Nexturl':Nexturl,'EmpID':EmpID,'PreviousUrl':PreviousUrl,'IND':IND,'D':D, 'IdentityInfo':identityobj if identityobj else( IdentityInfo if IdentityInfo else None),'IdentityPreview':IdentityPreview}
    return render(request, 'HR/NewEmployeeAdd/NewEmployeeIdentityinfo.html', context)


def NewEmployeeBankinfo(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    IND = request.GET.get('IND')
    EmpID   =  request.GET.get('EmpID')
    D = request.GET.get('D')
   
    ActiveLinkDict  = None
    ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

   
    Bankinfo = None                 
    Bankobj = None
   

    CurrentUrl = 'NewEmployeeBankinfo'

    urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = EmployeeUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName
    if IND is not None and D == "IA":
        Emobj = EmployeePersonalData.objects.filter(DataMasterID=IND,IsDelete=False).first()
      
        if Emobj:
            INEmpID  = Emobj.id
            if INEmpID is not None:
                Bankinfo = EmployeeBankInfoData.objects.filter(MasterID = INEmpID,IsDelete=False).first()
               
               
                
    
    if EmpID is not None:
          Bankobj   = EmployeeBankInformationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID).first()

    
    if request.method == "POST":
          # Bank Details Information 
                BankAccountNumber = request.POST['BankAccountNumber'] or ''
                NameofBank   = request.POST['NameofBank'] or ''
                BankBranch   = request.POST['BankBranch'] or ''
                IFSCCode   = request.POST['IFSCCode'] or ''
                if Bankobj is not None:
                   Bankobj.BankAccountNumber  = BankAccountNumber
                   Bankobj.NameofBank   = NameofBank
                   Bankobj.BankBranch  =BankBranch
                   Bankobj.IFSCCode  = IFSCCode
                   Bankobj.save()
                else:
                    Bankobj = EmployeeBankInformationDetails.objects.create(EmpID =  EmpID,
                        BankAccountNumber  =BankAccountNumber,NameofBank  = NameofBank,BankBranch  = BankBranch,IFSCCode = IFSCCode,OrganizationID = OrganizationID,CreatedBy = UserID
                    )
               
                
                url = reverse(Nexturl)  
                redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}" 
                return redirect(redirect_url)
         

    context = {'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl,'Nexturl':Nexturl,'EmpID':EmpID,'PreviousUrl':PreviousUrl,'IND':IND,'D':D, 'Bankinfo':Bankobj if Bankobj else( Bankinfo if Bankinfo else None ),            
    }
    return render(request, 'HR/NewEmployeeAdd/NewEmployeeBankinfo.html', context)




from Letterofintent.models import SalaryDetails


def NewEmployeeSalaryDetailsData(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    IND = request.GET.get('IND')
    EmpID   =  request.GET.get('EmpID')
    D = request.GET.get('D')
   
    ActiveLinkDict  = None
    ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

    Emobj = EmployeePersonalDetails.objects.filter(EmpID=EmpID,IsDelete=False).first()

    OID = None
    if Emobj:
        OID = Emobj.OrganizationID
    
    if not OID:
        OID = OrganizationID

    CurrentUrl = 'NewEmployeeSalaryDetailsData'

    urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = EmployeeUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName
    SalaryTitles  = SalaryTitle_Master.objects.filter(IsDelete=False, OrganizationID=OID).order_by('TypeOrder','TitleOrder')
    for salary in SalaryTitles:
        salary.Permonth = 0
        salary.Perannum = 0
        
        SC = Salary_Detail_Master.objects.filter(IsDelete=False,EmpID=EmpID, Salary_title_id = salary.id,OrganizationID=OID)
        if SC.exists():
                salary.Permonth = SC[0].Permonth
                salary.Perannum = SC[0].Perannum 
        else:
                SC = SalaryDetails.objects.filter(IsDelete=False,LETTEROFINTENTEmployeeDetail__InterviewID=IND, Salary_title_id = salary.id,OrganizationID=OID)
                if SC.exists():
                    salary.Permonth = SC[0].Permonth
                    salary.Perannum = SC[0].Perannum 

    
    if request.method == "POST":
                SC = Salary_Detail_Master.objects.filter(IsDelete=False,EmpID=EmpID,OrganizationID=OID)
                for s in SC:
                    s.IsDelete = True
                    s.ModifyBy  = UserID
                    s.save()
                
                
                Total_Title  =  request.POST['Total_Title']
                
                for i in range(int(Total_Title)+1):
                    TitleID = request.POST[f'TitleID_{i}']
                    Permonth  =  request.POST[f'Permonth_{i}']
                    Perannum  = request.POST[f'Perannum_{i}']
                
                    salaryObj = Salary_Detail_Master.objects.create(
                        EmpID = EmpID,
                        Salary_title_id = TitleID,
                        Permonth=Permonth,
                        Perannum=Perannum,
                        OrganizationID=OID,
                        CreatedBy  = UserID
                    )
                
                UpdateCTC(EmpID, OID, UserID)
                url = reverse(Nexturl)  
                redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}" 
                return redirect(redirect_url)
         

    context = {
        'ActiveLinkDict':ActiveLinkDict,
        'CurrentUrl':CurrentUrl,
        'Nexturl':Nexturl,
        'EmpID':EmpID,
        'PreviousUrl':PreviousUrl,
        'IND':IND,
        'D':D,
        'SalaryTitles' :SalaryTitles            
    }
    return render(request, 'HR/NewEmployeeAdd/NewEmployeeSalaryDetailsData.html', context)



def NewEmployeeLeaveDetailsData(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    IND = request.GET.get('IND')
    EmpID   =  request.GET.get('EmpID')
    D = request.GET.get('D')
   
    ActiveLinkDict  = None
    ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

    EmployeeCode  = None

    CurrentUrl = 'NewEmployeeLeaveDetailsData'

    urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = EmployeeUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName
    if EmpID  is not None:
         HrEmobj  = EmployeePersonalDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID).first()
         if HrEmobj:
              EmployeeCode = HrEmobj.EmployeeCode
    Leaveobj  = None
    
    LeaveTypes   =  Leave_Type_Master.objects.filter(IsDelete=False, Is_Active=True)
    for Leave in LeaveTypes:
         Leave.Balance = 0
         if HrEmobj:
            LT  =Emp_Leave_Balance_Master.objects.filter(OrganizationID = OrganizationID,CreatedBy=UserID,Leave_Type_Master_id = Leave.id,Emp_code=EmployeeCode)
            if LT.exists():
                Leave.Balance = LT[0].Balance
    if request.method == "POST":
               LT  =Emp_Leave_Balance_Master.objects.filter(OrganizationID = OrganizationID,CreatedBy=UserID,Emp_code=EmployeeCode)
               for l in LT:
                     l.IsDelete = True
                     l.ModifyBy   = UserID
                     l.save()

               Total_Leave  = int(request.POST['Total_Leave'])
                
               for i in range(int(Total_Leave)+1):
                    LeaveID = request.POST[f'LeaveID_{i}']
                    LeaveBalace  =  request.POST[f'LeaveBalance_{i}']
                    Leaveobj  = Emp_Leave_Balance_Master.objects.create(OrganizationID = OrganizationID,CreatedBy=UserID,Leave_Type_Master_id = LeaveID,Balance=LeaveBalace,Emp_code=EmployeeCode)
                
                
               url = reverse(Nexturl)  
               redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}" 
               return redirect(redirect_url)
         

    context = {'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl,'Nexturl':Nexturl,'EmpID':EmpID,'PreviousUrl':PreviousUrl,'IND':IND,'D':D, 'LeaveTypes':LeaveTypes,
            'Leaveobj':Leaveobj
           
    }
    return render(request, 'HR/NewEmployeeAdd/NewEmployeeLeaveDetailsData.html', context)


def NewEmployeeDocumentinfo(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    IND = request.GET.get('IND')
    EmpID   =  request.GET.get('EmpID')
    D = request.GET.get('D')
   
    ActiveLinkDict  = None
    ActiveLinkDict  = ActiveLink(EmpID=EmpID,return_dict=True)

   
    Documents = None                 
    docobj = None
   

    CurrentUrl = 'NewEmployeeDocumentinfo'

    urlobj  = EmployeeUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = EmployeeUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = EmployeeUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName
    if IND is not None and D == "IA":
        Emobj = EmployeePersonalData.objects.filter(DataMasterID=IND,IsDelete=False).first()
      
        if Emobj:
            INEmpID  = Emobj.id
            if INEmpID is not None:
                 Documents  = EmployeeDocumentsInfoData.objects.filter(MasterID = INEmpID,IsDelete=False)

               
                
    
    if EmpID is not None:
         docobj = EmployeeDocumentsInformationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID)


    
    if request.method == "POST":
                 # Document Information
                Title = request.POST.getlist('Title[]')
              
                Doc_ids = request.POST.getlist('Doc_ids[]')
                AttachmentDocumenstsFile  = request.FILES.getlist('AttachmentDocumenstsFile[]')
                
                removed_Doc_ids_str = request.POST.getlist('removed_Doc_ids[]')
                removed_Doc_ids = [int(id) for id in removed_Doc_ids_str if id.isdigit()]
                
                
                
                if len(removed_Doc_ids) > 0:
                      
                        for id in removed_Doc_ids:
                          
                            docdelete = EmployeeDocumentsInformationDetails.objects.filter(id=id).first()
                          
                            docdelete.IsDelete  = True
                            docdelete.save()
                if Doc_ids:
                    d = 0
                    for  id,title in zip(Doc_ids,Title):
                        if id.startswith('new_'):
                            newDocObject  = EmployeeDocumentsInformationDetails.objects.create(
                                 EmpID =  EmpID,
                                Title = title, OrganizationID=OrganizationID,
                                    CreatedBy=UserID
                            )
                            File = AttachmentDocumenstsFile[d]
                            if  File:
                                upload_file(File, newDocObject.id, "Documents", "EmployeeDocumentsInformationDetails")
                            d = d + 1
                        else:
                            DocObjectUpdated  = EmployeeDocumentsInformationDetails.objects.filter(IsDelete=False,EmpID = EmpID,id=id).update(Title  = title,ModifyBy = UserID)
                            if not DocObjectUpdated:
                                 DocObject  = EmployeeDocumentsInformationDetails.objects.create(
                                 EmpID =  EmpID,
                                 Title = title, OrganizationID=OrganizationID,
                                    CreatedBy=UserID
                                 )
                                 File  = EmployeeDocumentsInfoData.objects.filter(id=id).first()
                                 if File:
                                    file_content, file_type = CopyFile(File.FileName)
                                    
                                   
                                    file_io = BytesIO(file_content)
                                    file_io.name = File.FileName 
                                    
                                    upload_file(file_io, DocObject.id, "Documents", "EmployeeDocumentsInformationDetails")

                else:
                    for  title,Attachment in zip(Title,AttachmentDocumenstsFile):
                            DObject  = EmployeeDocumentsInfoData.objects.create(
                                 MasterID =  EmpID,
                                Title = title,OrganizationID=OrganizationID,
                                    CreatedBy=UserID

                            )
                            if Attachment:
                                
                                  upload_file(Attachment, DObject.id, "Documents", "EmployeeDocumentsInformationDetails")
                
                if IND and D == "IA":
                    assobj = Assessment_Master.objects.filter(id=IND,IsDelete=False).first()
                    if assobj:
                         assobj.IsEmployeeCreated = True
                         assobj.save()
                hrobj  =  EmployeePersonalDetails.objects.filter(EmpID=EmpID,OrganizationID=OrganizationID,IsDelete=False).first()
                if   hrobj:
                        hrobj.IsEmployeeCreated =  True
                        hrobj.save()

                result = update_employee_profile(EmpID, OrganizationID)
                url = reverse(Nexturl)  
                redirect_url = f"{url}?EmpID={EmpID}&IND={IND}&D={D}" 
                return redirect(redirect_url)
    DocumentPreview = 'docobj' if docobj else ('Documents' if Documents else '')
    context = {'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl,'Nexturl':Nexturl,'EmpID':EmpID,'PreviousUrl':PreviousUrl,'IND':IND,'D':D,  'Documents':docobj if docobj else (Documents if Documents else None),'DocumentPreview':DocumentPreview
    }
    return render(request, 'HR/NewEmployeeAdd/NewEmployeeDocumentinfo.html', context)



def get_departments_by_division(request):
    division_name = request.GET.get('division_name')
    if division_name == "AllDivision":
        departments = OnRollDepartmentMaster.objects.filter(IsDelete=False).values('DepartmentName')
    else:
        departments = OnRollDepartmentMaster.objects.filter(
            OnRollDivisionMaster__DivisionName=division_name,
            IsDelete=False
        ).values('DepartmentName')
    print(get_departments_by_division)    
    return JsonResponse(list(departments), safe=False)
   


# ------- Employee List is here
def EmployeeList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
 
    OrganizationID = request.session["OrganizationID"]
    # memOrg = OrganizationList(OrganizationID)
 
    UserType=request.session["UserType"]
    Departments = OnRollDepartmentMaster.objects.filter(IsDelete=False).order_by('DepartmentName')
    Divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).order_by('DivisionName')
 
   
    selected_org_id = request.GET.get("Organizations", OrganizationID)
    if not selected_org_id or selected_org_id == "all":
        selected_org_id = OrganizationID
    else:
        selected_org_id = int(selected_org_id)  

    selected_division = request.GET.get("Divisions")
    employee_code = request.GET.get("employee_code")
    
    # print("selected divisions:", selected_division)
    # print("selected_org_id:", selected_org_id)

    Status = request.GET.get("Status", '')
    Status_list = Status.split(",") if Status else []

    Departments = request.GET.get("Departments") 
    Departments_list = Departments.split(",") if Departments else []

    Levels = request.GET.get("Levels") 
    Levels_List = Levels.split(",") if Levels else []


    # if UserType == 'CEO' and request.GET.get('Organizations') is None:
    #         selected_org_id = 401

    Empobjs = EmployeePersonalDetails.objects.filter(
        IsDelete=False, OrganizationID=selected_org_id, IsEmployeeCreated=True
    ).values(
        'EmpID', 'EmployeeCode', 'Prefix', 'FirstName', 'MiddleName', 'LastName',
        'Gender', 'MobileNumber', 'ProfileImageFileName', 'CovidVaccination', 'DetailsofIllness', 'ProfileCompletion'
    )
 
    work_details = EmployeeWorkDetails.objects.filter(
        IsDelete=False, OrganizationID=selected_org_id,IsSecondary=False
    ).values(
        'EmpID','Division', 'Designation', 'Level', 'Department', 'DateofJoining', 'EmpStatus'
    )

   
    if selected_org_id and selected_org_id != "all":
        Empobjs = Empobjs.filter(OrganizationID=selected_org_id)
        work_details = work_details.filter(OrganizationID=selected_org_id)
 

    if employee_code:
        Empobjs = Empobjs.filter(EmployeeCode__icontains=employee_code)
 

    departments_in_division = []
    if selected_division and selected_division != "":
        departments_in_division = OnRollDepartmentMaster.objects.filter(
            OnRollDivisionMaster__DivisionName=selected_division, IsDelete=False
        ).values_list('DepartmentName', flat=True)  


    if Departments_list:
        work_details = work_details.filter(Department__in=Departments_list)
    else:
        if departments_in_division:  # only filter if there are departments
            work_details = work_details.filter(Department__in=departments_in_division)
            Departments_list = list(departments_in_division)

    #  ----------- Status
    if not Status_list or Status_list == [""]:  
        Status_list = ["On Probation", "Not Confirmed", "Confirmed"]
        # work_details = work_details.filter(EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"])
        work_details = work_details.filter(EmpStatus__in=Status_list)
    elif "all" in Status_list:
        pass  
    else:
        work_details = work_details.filter(EmpStatus__in=Status_list)

    # ------------ Levels
    if not Levels_List or Levels_List == [""]:  
        Levels_List = list(LavelAdd.objects.filter(IsDelete=False).values_list("lavelname", flat=True))
        work_details = work_details.filter(Level__in=Levels_List)
    elif "all" in Levels_List:
        pass  
    else:
        work_details = work_details.filter(Level__in=Levels_List)


    work_details_dict = {wd['EmpID']: wd for wd in work_details}
    combined_Empobj_data = []
    for emp in Empobjs:
        emp_id = emp['EmpID']
        work_detail = work_details_dict.get(emp_id, {})
        combined_Empobj_data.append({
            **emp,
            'Department': work_detail.get('Department', 'N/A'),
            'Designation': work_detail.get('Designation', 'N/A'),
            'DateofJoining': work_detail.get('DateofJoining', 'N/A'),
            'Level': work_detail.get('Level', 'N/A'),
            'EmpStatus': work_detail.get('EmpStatus', 'N/A')
        })
 
   
    filtered_data = []
    for emp in combined_Empobj_data:
        if not Status_list or Status_list == [""]:
            if emp['EmpStatus'] in ["On Probation", "Not Confirmed", "Confirmed"]:
                filtered_data.append(emp)

        elif "all" in Status_list:
            filtered_data.append(emp)

        elif emp['EmpStatus'] in Status_list:
            filtered_data.append(emp)
                
    filtered_data = sorted(filtered_data, key=lambda x: x['EmployeeCode'], reverse=True)


    context = {
        'Empobjs': filtered_data,
        'Divisions': Divisions,
        'selected_org_id': selected_org_id,
        "Status_list": json.dumps(Status_list), 
        'selected_Department_list': json.dumps(Departments_list),  
        'Levels_List': json.dumps(Levels_List),  
        'selected_division': selected_division,
        'employee_code': employee_code,
        'Session_OrganizationID':OrganizationID
       
    }
    return render(request, 'HR/EmployeeList.html', context)


# def EmployeeList(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
 
#     OrganizationID = request.session["OrganizationID"]
#     memOrg  =  OrganizationList(OrganizationID)
   
#     Departments = OnRollDepartmentMaster.objects.filter(IsDelete=False).order_by('DepartmentName')
 
   
#     selected_org_id = request.GET.get("OrganizationID",OrganizationID)
#     selected_emp_status = request.GET.get("EmpStatus")
#     selected_department = request.GET.get("Department")
#     employee_code = request.GET.get("employee_code")
 
   
#     if not selected_emp_status:
#         selected_emp_status = "all"
 
   
#     Empobjs = EmployeePersonalDetails.objects.filter(
#         IsDelete=False, OrganizationID=selected_org_id, IsEmployeeCreated=True
#     ).values(
#         'EmpID', 'EmployeeCode', 'Prefix', 'FirstName', 'MiddleName', 'LastName',
#         'Gender', 'MobileNumber', 'ProfileImageFileName', 'CovidVaccination', 'DetailsofIllness', 'ProfileCompletion'
#     ).order_by('-EmpID')
 
   
#     work_details = EmployeeWorkDetails.objects.filter(
#         IsDelete=False, OrganizationID=selected_org_id
#     ).values(
#         'EmpID', 'Designation', 'Department', 'DateofJoining', 'EmpStatus'
#     )
 
   
#     if selected_org_id and selected_org_id != "all":
#         Empobjs = Empobjs.filter(OrganizationID=selected_org_id)
#         work_details = work_details.filter(OrganizationID=selected_org_id)
 
#     if employee_code:
#         Empobjs = Empobjs.filter(EmployeeCode__icontains=employee_code)
 
   
#     if selected_emp_status == "all":
#         work_details = work_details.filter(EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"])
 
   
#     if selected_department and selected_department != "AllDepartment":
#         work_details = work_details.filter(Department=selected_department)
 
   
#     work_details_dict = {wd['EmpID']: wd for wd in work_details}
#     combined_Empobj_data = []
#     for emp in Empobjs:
#         emp_id = emp['EmpID']
#         work_detail = work_details_dict.get(emp_id, {})
#         combined_Empobj_data.append({
#             **emp,
#             'Department': work_detail.get('Department', 'N/A'),
#             'Designation': work_detail.get('Designation', 'N/A'),
#             'DateofJoining': work_detail.get('DateofJoining', 'N/A'),
#             'EmpStatus': work_detail.get('EmpStatus', 'N/A')
#         })
 
   
#     filtered_data = []
#     for emp in combined_Empobj_data:
       
#         if selected_emp_status == "all":
#             if emp['EmpStatus'] in ["On Probation", "Not Confirmed", "Confirmed"]:
#                 filtered_data.append(emp)
#         else:
           
#             if (
#                 (not selected_emp_status or selected_emp_status == 'all' or emp['EmpStatus'] == selected_emp_status) and
#                 (not selected_department or selected_department == 'AllDepartment' or emp['Department'] == selected_department) and
#                 (not employee_code or employee_code.lower() in emp['EmployeeCode'].lower())
#             ):
#                 filtered_data.append(emp)
 
#     context = {
#         'Empobjs': filtered_data,
#         'memOrg': memOrg,
#         'Departments': Departments,
#         'selected_org_id': selected_org_id,
#         'selected_emp_status': selected_emp_status,
#         'selected_department': selected_department,
#         'employee_code': employee_code,
#     }
 
#     return render(request, 'HR/EmployeeList.html', context)

# from django.db.models import Subquery, OuterRef
# def EmployeeList(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")

#     OrganizationID = request.session["OrganizationID"]

#     Empobjs = EmployeePersonalDetails.objects.filter(
#         IsDelete=False, OrganizationID=OrganizationID, IsEmployeeCreated=True
#     ).values(
#         'EmpID', 'EmployeeCode', 'Prefix', 'FirstName', 'MiddleName', 'LastName',
#         'Gender', 'MobileNumber', 'ProfileImageFileName', 'CovidVaccination', 'DetailsofIllness'
#     )

#     work_details = EmployeeWorkDetails.objects.filter(
#         IsDelete=False, OrganizationID=OrganizationID
#     ).values(
#         'EmpID', 'Designation', 'Department', 'DateofJoining', 'EmpStatus'
#     )

#     work_details_dict = {wd['EmpID']: wd for wd in work_details}

#     combined_Empobj_data = []
#     for emp in Empobjs:
#         emp_id = emp['EmpID']

#         # Fetch full EmployeePersonalDetails object to use the method
#         personal_obj = EmployeePersonalDetails.objects.get(EmpID=emp_id)
#         personal_filled_percentage = personal_obj.data_filled_percentage()
#         personal_missing_fields = personal_obj.get_missing_fields()

#         # Fetch related work details if available
#         work_detail = work_details_dict.get(emp_id, {})
        
#         if work_detail:
#             work_obj = EmployeeWorkDetails.objects.get(EmpID=emp_id)
#             work_filled_percentage = work_obj.data_filled_percentage()
#             work_missing_fields = work_obj.get_missing_fields()
#         else:
#             work_filled_percentage = 0
#             work_missing_fields = []

#         total_filled_percentage = (personal_filled_percentage + work_filled_percentage) / 2

#         # Combine personal and work missing fields
#         all_missing_fields = personal_missing_fields + work_missing_fields

#         combined_Empobj_data.append({
#             **emp,
#             'Department': work_detail.get('Department', 'N/A'),
#             'Designation': work_detail.get('Designation', 'N/A'),
#             'DateofJoining': work_detail.get('DateofJoining', 'N/A'),
#             'EmpStatus': work_detail.get('EmpStatus', 'N/A'),
#             'PersonalFilledPercentage': personal_filled_percentage,
#             'WorkFilledPercentage': work_filled_percentage,
#             'TotalFilledPercentage': total_filled_percentage,
#             'MissingFields': ", ".join(all_missing_fields)  # Create a comma-separated string
#         })

#     context = {
#         'Empobjs': combined_Empobj_data,
#     }


   

#     return render(request, 'HR/EmployeeList.html', context)


def EmployeeCardDetails(EmpID,OrganizationID):
    Emobj = EmployeePersonalDetails.objects.filter(
        IsDelete=False, EmpID=EmpID, OrganizationID=OrganizationID
    ).first()

    if Emobj:
        Workobj = EmployeeWorkDetails.objects.filter(OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False, EmpID=EmpID).first()
        

    if Emobj and Workobj:
      
        tenure = Workobj.tenure_till_today()

        Emobj.Department = Workobj.Department if Workobj else 'N/A'
        Emobj.EmpStatus = Workobj.EmpStatus if Workobj else 'N/A'

        Emobj.Designation = Workobj.Designation if Workobj else 'N/A'
        Emobj.Level = Workobj.Level if Workobj else 'N/A'
        Emobj.DateofJoining = Workobj.DateofJoining if Workobj else 'N/A'
        Emobj.ReportingtoDesignation = Workobj.ReportingtoDesignation if Workobj else 'N/A'
        Emobj.ReportingtoDepartment = Workobj.ReportingtoDepartment if Workobj else 'N/A'
        Emobj.ReportingtoLevel = Workobj.ReportingtoLevel if Workobj else 'N/A'
        Emobj.TenureTillToday = tenure

        Emobj.save()
    return Emobj








from app.views import Error

from datetime import timedelta
def EmployeeDetailsData(EmpID,OrganizationID):
    print("employee id  is here::", EmpID, "OID is here::", OrganizationID)
        
    # annotate
    Emobj = EmployeePersonalDetails.objects.filter(
        IsDelete=False, EmpID=EmpID, OrganizationID=OrganizationID, 
      
    ).annotate(full_name=Concat(
            F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName'))).first()

    if Emobj:
        Workobj = EmployeeWorkDetails.objects.filter(OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False, EmpID=EmpID).first()
        Addressobj  = EmployeeAddressInformationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID).first()
        

    if Emobj and Workobj:
      
        if Emobj:
            CTC = 0
            BasicSalary = 0

            basic_salary_details = Salary_Detail_Master.objects.filter(
                Salary_title__Title='Basic',
                IsDelete=False,
                OrganizationID=OrganizationID,
                EmpID=EmpID
            ).order_by('-id').first()  
            if basic_salary_details:
                 BasicSalary = basic_salary_details.Permonth
                 

            ctc_salary_details = Salary_Detail_Master.objects.filter(
                Salary_title__Title='CTC (A+C)',
                IsDelete=False,
                OrganizationID=OrganizationID,
                EmpID=EmpID
            ).order_by('-id').first()


            if ctc_salary_details:
                CTC = ctc_salary_details.Permonth
            
            # print("HUMAN rESOURCE CTC IS HERE::",CTC)

        Emobj.Department = Workobj.Department if Workobj else 'N/A'
        Emobj.OrganizationID = Workobj.OrganizationID if Workobj else 'N/A'
        Emobj.EmpStatus = Workobj.EmpStatus if Workobj else 'N/A'
        Emobj.Designation = Workobj.Designation if Workobj else 'N/A'
        Emobj.Level = Workobj.Level if Workobj else 'N/A'
        Emobj.DateofJoining = Workobj.DateofJoining if Workobj else 'N/A'
        DateofJoining = Workobj.DateofJoining
        review_from_date = None
        review_to_date = None

        if DateofJoining:
                review_from_date = DateofJoining

                review_to_date = DateofJoining + timedelta(days=365)
       

        # Emobj.review_from_date =  review_from_date
        # Emobj.review_to_date =  review_to_date

        Emobj.ReportingtoDesignation = Workobj.ReportingtoDesignation if Workobj else 'N/A'
        Emobj.DottedLine = Workobj.DottedLine if Workobj else 'N/A'

        

        
        ReportingtoDesignationName = get_employee_names_by_designation(OrganizationID,Emobj.ReportingtoDesignation)
        if ReportingtoDesignationName is None:
            OrganizationIDCo = 3
            ReportingtoDesignationName = get_employee_names_by_designation(OrganizationIDCo , Emobj.ReportingtoDesignation)

        Emobj.ReportingtoDesignationName = ReportingtoDesignationName
        Emobj.ReportingtoLevel = Workobj.ReportingtoLevel if Workobj else 'N/A'
        Emobj.tenure_till_today = Workobj.tenure_till_today if Workobj else 'N/A'
        Emobj.Address=''
        if Addressobj:
            try:
                Emobj.Address = (Addressobj.Permanent_Address  +" "+ Addressobj.Permanent_City +" "+ Addressobj.Permanent_State +" "+ str(Addressobj.Permanent_Pincode)) if Workobj else 'N/A'
            except:
                 print()
        else:
            Emobj.Address = ''
                  
        Emobj.review_from_date =  review_from_date  # Reinittialize
        Emobj.review_to_date =  review_to_date      # Reinittialize

        Emobj.BasicSalary  = BasicSalary
       
        Emobj.CTC  = CTC
        # print("Existing CTC is here:: ---,", CTC)


        Emobj.DateofJoining  = Workobj.DateofJoining  if Workobj else 'N/A'
        Emobj.save()
    return Emobj



def EditEmployee(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
          OrganizationID= OID   

     UserID = str(request.session["UserID"])   
     Designations = OnRollDesignationMaster.objects.filter(IsDelete=False)
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Success  =  False
     Emobj    = None
     hotelapitoken = MasterAttribute.HotelAPIkeyToken
              
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
       

     if request.method == "POST":   
         #  Persoan Details 
                EmployeeCode  = request.POST['EmployeeCode']
                Prefix  = request.POST['Prefix']
                FirstName = request.POST['FirstName']
                MiddleName = request.POST['MiddleName']
                LastName = request.POST['LastName']
                Gender = request.POST['Gender']
                MaritalStatus = request.POST['MaritalStatus']
                DateofBirth = request.POST['DateofBirth']
                age = request.POST['age']
                MobileNumber = request.POST['MobileNumber']
                EmailAddress = request.POST['EmailAddress']
                ProfileImage  = request.FILES.get('ProfileImage')
                CovidVaccination = request.POST['CovidVaccination']
                IllnessDetails = request.POST['IllnessDetails']
              
                
               
                if Emobj  is not None:
                    Em = EmployeePersonalDetails.objects.filter(EmpID=EmpID ).first()
                    Em.EmployeeCode = EmployeeCode
                    Em.Prefix  = Prefix
                    Em.FirstName  = FirstName
                    Em.MiddleName  = MiddleName
                    Em.LastName = LastName
                    Em.Gender  = Gender
                    Em.MaritalStatus  = MaritalStatus
                    Em.DateofBirth  = DateofBirth 
                    Em.age = age
                    Em.MobileNumber = MobileNumber
                    Em.EmailAddress  = EmailAddress
                    Em.CovidVaccination  = CovidVaccination
                    Em.DetailsofIllness  = IllnessDetails
                    Em.ModifyBy  =  UserID
                    
                   
                    # profile_completion_percentage, missing_fields = calculate_profile_completion(Em, modelname="Personal Details")

                   
                    # Em.ProfileCompletion = profile_completion_percentage
                    # Em.MissingFields = missing_fields

                  
                    Em.save()
                    if EmpID:
                         result = update_employee_profile(EmpID, OrganizationID)
                    if ProfileImage:
                         upload_file(ProfileImage, Em.EmpID, "ProfileImage","EmployeePersonalDetails")   
                         result = update_employee_profile(EmpID, OrganizationID)
 
                    Success  = True     
                 
                  
                              
                    
                encrypted_id = encrypt_id(Emobj.EmpID)
                url = reverse('PersonalDetails')  
                redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
                return redirect(redirect_url)

     context = {'Emobj':Emobj,'EmpID':EmpID,'Success':Success,'OID':OID,'hotelapitoken':hotelapitoken,'OrganizationID':OrganizationID}        
     return render(request, 'HR/EmployeeDashboard/PersonalDetails.html', context)



def EmployeeList_StatusFormHandle(request):
    if request.method == 'POST':
        emp_id = request.POST.get('EmpID')       # 7656
        new_status = request.POST.get('EmpStatus')
        OrganizationID = request.POST.get('OrganizationID')   # Optional: get from POST if needed

        try:
            work = EmployeeWorkDetails.objects.get(EmpID=emp_id, IsDelete=False, IsSecondary=False, OrganizationID=OrganizationID)
            work.EmpStatus = new_status
            work.save()
            
            messages.success(request, 'Employee status updated successfully.')
            Success  = True         
            encrypted_id = encrypt_id(emp_id)
            url = reverse('EditEmployee')  
            redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
            return redirect(redirect_url)

        except EmployeeWorkDetails.DoesNotExist:
            messages.error(request, 'Employee not found or invalid.')

    return redirect("EditEmployee")  # fallback



def  PersonalDetails(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
          OrganizationID= OID
     UserID = str(request.session["UserID"])   
     Designations = OnRollDesignationMaster.objects.filter(IsDelete=False)
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Success  =  False
     Emobj    = None
     hotelapitoken = MasterAttribute.HotelAPIkeyToken
              
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
    
    
   

     if request.method == "POST":   
         #  Persoan Details 
                EmployeeCode  = request.POST['EmployeeCode']
                Prefix  = request.POST['Prefix']
                FirstName = request.POST['FirstName']
                MiddleName = request.POST['MiddleName']
                LastName = request.POST['LastName']
                Gender = request.POST['Gender']
                MaritalStatus = request.POST['MaritalStatus']
                DateofBirth = request.POST['DateofBirth']
                age = request.POST['age']
                MobileNumber = request.POST['MobileNumber']
                EmailAddress = request.POST['EmailAddress']
                ProfileImage  = request.FILES.get('ProfileImage')
                CovidVaccination = request.POST['CovidVaccination']
                IllnessDetails = request.POST['IllnessDetails']
              
                
               
                if Emobj  is not None:
                    Em = EmployeePersonalDetails.objects.filter(EmpID=EmpID ).first()
                    Em.EmployeeCode = EmployeeCode
                    Em.Prefix  = Prefix
                    Em.FirstName  = FirstName
                    Em.MiddleName  = MiddleName
                    Em.LastName = LastName
                    Em.Gender  = Gender
                    Em.MaritalStatus  = MaritalStatus
                    Em.DateofBirth  = DateofBirth 
                    Em.age = age
                    Em.MobileNumber = MobileNumber
                    Em.EmailAddress  = EmailAddress
                    Em.CovidVaccination  = CovidVaccination
                    Em.DetailsofIllness  = IllnessDetails
                    Em.ModifyBy  =  UserID                  
                    Em.save()
                    if EmpID:
                        result = update_employee_profile(EmpID, OrganizationID)

                    if ProfileImage:
                        upload_file(ProfileImage, Em.EmpID, "ProfileImage","EmployeePersonalDetails")
                        result = update_employee_profile(EmpID, OrganizationID)
                    
                    
                
                
                Success  = True         
                encrypted_id = encrypt_id(Emobj.EmpID)
                url = reverse('PersonalDetails')  
                redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
                return redirect(redirect_url)

     context = {'Emobj':Emobj,'EmpID':EmpID,'Success':Success,'OrganizationID':OrganizationID,'hotelapitoken':hotelapitoken}        
     return render(request, 'HR/EmployeeDashboard/PersonalDetails.html', context)



def DepartmentJson():
     
     Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
     
     DottedLineDesignations = CorporateDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
     MergedDesignations = chain(Designations, DottedLineDesignations)

    #  print("Designations :::", Designations)
    #  print("DottedLineDesignations :::", DottedLineDesignations)
    #  print("MergedDesignations :::", MergedDesignations)
    #  for item in MergedDesignations:
    #     print(item)
     
     merged_designations_data = []
     for merged in MergedDesignations:
        if ( hasattr(merged, 'OnRollDepartmentMaster') and merged.OnRollDepartmentMaster and hasattr(merged, 'OnRollDivisionMaster') and merged.OnRollDivisionMaster
            ):
            merged_designations_data.append({
                'designations': merged.designations,
                'DepartmentName': merged.OnRollDepartmentMaster.DepartmentName,
                'DivisionName': merged.OnRollDivisionMaster.DivisionName
            })
        elif ( hasattr(merged, 'CorporateDepartmentMaster') and merged.CorporateDepartmentMaster and hasattr(merged, 'CorporateDivisionMaster') and merged.CorporateDivisionMaster):
            merged_designations_data.append({
                'designations': merged.designations,
                'DepartmentName': merged.CorporateDepartmentMaster.DepartmentName,
                'DivisionName': merged.CorporateDivisionMaster.DivisionName
            })

     merged_designations_json = json.dumps(merged_designations_data)
    #  print("merged_designations_json :::", merged_designations_json)
     return merged_designations_json



def subrecordsjson(EmpID,OrganizationID):
     subrecordslist =[]
     subrecords = EmployeeWorkDetails.objects.filter(OrganizationID=OrganizationID, IsDelete=False,IsSecondary=True ,EmpID=EmpID)
     for sb in subrecords:
            subrecordslist.append({
                 'id':sb.id,
                'designations': sb.Designation,
                'DepartmentName': sb.Department,
                'DivisionName':sb.Division
            })

     subrecordslist_json = json.dumps(subrecordslist)
     return subrecordslist_json


from django.core.serializers import serialize
import json

# from django.core.cache import cache
from Checklist_Issued.views import run_background_checklist_tasks_Employee_ID


# def EmployeeWorkDetailsPage(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
#     OrganizationID = request.session["OrganizationID"]
#     OID  = request.GET.get('OID')
#     if OID:
#         OrganizationID= OID
#     UserID = str(request.session["UserID"])   
    
#     Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).values("id","designations").order_by('designations')
     
#     DottedLineDesignations = CorporateDesignationMaster.objects.filter(IsDelete=False).values("id","designations").order_by('designations')


#     MergedDesignations = chain(Designations, DottedLineDesignations)
#     # MergedDesignations = Designations.union(DottedLineDesignations)

  
#     MergedDottedLineDesignations =  chain(Designations, DottedLineDesignations)
#     MergedReportingtoDesignation =  chain(Designations, DottedLineDesignations)

   

#     merged_designations_json = DepartmentJson()
   

#     encrypted_id = request.GET.get('EmpID')
#     EmpID = decrypt_id(encrypted_id)
    
#     Success  =  False
#     Emobj    = None     
#     if EmpID:
#         Emobj = EmployeeCardDetails(EmpID,OrganizationID)

#         Workobj = EmployeeWorkDetails.objects.filter(OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False, EmpID=EmpID).first()

#         subrecordslist_json =  subrecordsjson(EmpID,OrganizationID)
#         # print(subrecordslist_json)
                    

#     if request.method  ==  "POST":
#         Designation = request.POST['Designation']
#         Department  = request.POST['Department']
#         Division  = request.POST['Division']      # New
#         Level  = request.POST['Level']
#         ReportingtoDivision  = request.POST['ReportingtoDivision']      # New
#         ReportingtoDesignation = request.POST['ReportingToDesignation']
#         ReportingtoDepartment = request.POST['ReportingToDesignationDepartment']
#         ReportingtoLevel = request.POST['ReportingToDesignationLevel']
#         Vip = request.POST.get('VipCheckbox')

#         AccommodationFlatNumber = request.POST['AccommodationFlatNumber'] or ''
        
#         WeekOffDay = request.POST.get('WeekOffDay')

#         VipCheckbox = False
        
#         if Vip  == 'Vip':
#                 VipCheckbox = True
                


#         DottedLine = request.POST['DottedLine'] or ''

#         OfficialEmailAddress = None
        
#         if 'OfficialEmailAddress' in request.POST:
#             OfficialEmailAddress = request.POST['OfficialEmailAddress']
#         OfficialMobileNo = None
#         if 'OfficialMobileNo' in request.POST:
#             OfficialMobileNo  = request.POST['OfficialMobileNo']
#         DateofJoining = request.POST['DateOfJoining']
#         CompanyAccommodation  =  request.POST['CompanyAccommodation']
        
#         Locker  =  request.POST['Locker']
#         LockerType  =  request.POST['LockerType']
#         LockerNumber  = request.POST['LockerNumber']
#         EmploymentType   = request.POST['EmploymentType']
#         ContractStartDate  = None
#         if 'ContractStartDate' in request.POST:
#             ContractStartDate  =  request.POST['ContractStartDate']
#             if ContractStartDate == '':
#                     ContractStartDate = None
                    
                    
#         ContractEndDate  = None
#         if 'ContractEndDate' in request.POST:    
#             ContractEndDate  = request.POST['ContractEndDate']
#             if ContractEndDate == '':
#                     ContractEndDate = None



#         if Workobj  is not None:
#             Workobj.Designation  = Designation
#             Workobj.Department  = Department
#             Workobj.Division  = Division    # New
#             Workobj.Level  = Level
#             Workobj.ReportingtoDivision  = ReportingtoDivision     # New
#             Workobj.ReportingtoDesignation  = ReportingtoDesignation
#             Workobj.ReportingtoDepartment  = ReportingtoDepartment
#             Workobj.ReportingtoLevel  = ReportingtoLevel
            
#             Workobj.OfficialEmailAddress = OfficialEmailAddress
#             Workobj.OfficialMobileNo  = OfficialMobileNo
#             Workobj.DateofJoining = DateofJoining
#             Workobj.CompanyAccommodation  = CompanyAccommodation
#             Workobj.AccommodationFlatNumber = AccommodationFlatNumber
#             Workobj.Locker = Locker
#             Workobj.LockerType = LockerType
#             Workobj.LockerNumber  = LockerNumber
#             Workobj.EmploymentType  = EmploymentType
#             Workobj.ContractEndDate = ContractEndDate 
#             Workobj.ContractStartDate = ContractStartDate
#             Workobj.ModifyBy = UserID
#             Workobj.DottedLine = DottedLine
#             Workobj.VipCheckbox = VipCheckbox
#             Workobj.WeekOffDay = WeekOffDay

#             Workobj.save()
            
#             run_background_checklist_tasks_Employee_ID(EmpID,OID,UserID)
            
#             if EmpID:
#                 result = update_employee_profile(EmpID, OrganizationID)
            
#             Success  = True
                            
#             # Get lists from the request
#             DivisionList = request.POST.getlist('Division[]')
#             DesignationList = request.POST.getlist('Designation[]')
#             DepartmentList = request.POST.getlist('Department[]')
#             IsDeleteList = request.POST.getlist('IsDelete[]')
#             IdList = request.POST.getlist('ID[]')
#             # print("IdList = ",IdList)
#             # print("IsDeleteList = ",IsDeleteList)
#             # print("DivisionList = ",DivisionList)


#             # Ensure all lists are of the same length
#             if DivisionList and DesignationList and DepartmentList and IsDeleteList and IdList:
#                 for id, designation, department, is_delete, division in zip(IdList, DesignationList, DepartmentList, IsDeleteList, DivisionList):
#                     is_delete = int(is_delete)  # Convert to integer for comparison
                    
#                     if designation and department and division:
#                         if int(id) == 0 and is_delete == 0:  # Create new record
#                             EmployeeWorkDetails.objects.create(
#                                 EmpID=EmpID,
#                                 IsSecondary=True,
#                                 Division = division,
#                                 Designation=designation,
#                                 Department=department,
#                                 OrganizationID=OrganizationID
#                             )
#                         elif int(id) > 0 and is_delete == 0:  # Update existing record
#                             existing_record = EmployeeWorkDetails.objects.filter(id=id, IsSecondary=True, EmpID=EmpID).first()
#                             if existing_record:
#                                 existing_record.Designation = designation
#                                 existing_record.Department = department
#                                 existing_record.Division = division
#                                 existing_record.save()
#                         elif int(id) > 0 and is_delete == 1:  # Mark record as deleted
#                             EmployeeWorkDetails.objects.filter(id=id, IsSecondary=True, EmpID=EmpID).update(IsDelete=True)

#         encrypted_id = encrypt_id(EmpID)
#         url = reverse('EmployeeWorkDetailsPage')  
#         redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
#         return redirect(redirect_url)       

#     context = {
#         'MergedReportingtoDesignation':MergedReportingtoDesignation,
#         'MergedDottedLineDesignations':MergedDottedLineDesignations , 
#         # 'MergedReportingtoDesignation':MergedDesignations,
#         # 'MergedDottedLineDesignations':MergedDesignations , 
#         'OrganizationID':OrganizationID,
#         'Workobj':Workobj,
#         'Emobj':Emobj,
#         'EmpID':EmpID,
#         'Success':Success,
#         'MergedDesignations':MergedDesignations, 
#         'merged_designations_json':merged_designations_json,
#         'subrecordslist_json':subrecordslist_json,
#     }
#     return render(request, 'HR/EmployeeDashboard/EmployeeWorkDetailsPage.html', context)



# def  EmployeeWorkDetailsPage(request):
#      if 'OrganizationID' not in request.session:
#          return redirect(MasterAttribute.Host)
#      else:
#         print("Show Page Session")
#      OrganizationID = request.session["OrganizationID"]
#      OID  = request.GET.get('OID')
#      if OID:
#           OrganizationID= OID
#      UserID = str(request.session["UserID"])   
    
#      Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
     
#      DottedLineDesignations = CorporateDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    
     
#      MergedDesignations = chain(Designations, DottedLineDesignations)
  
#      MergedDottedLineDesignations =  chain(Designations, DottedLineDesignations)
#      MergedReportingtoDesignation =  chain(Designations, DottedLineDesignations)

   

#      merged_designations_json = DepartmentJson()
   

#      encrypted_id = request.GET.get('EmpID')
#      EmpID = decrypt_id(encrypted_id)
#      Success  =  False
#      Emobj    = None     
#      if EmpID:
#         Emobj = EmployeeCardDetails(EmpID,OrganizationID)
#         Workobj = EmployeeWorkDetails.objects.filter(OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False, EmpID=EmpID).first()
#         subrecordslist_json =  subrecordsjson(EmpID,OrganizationID)
#         print(subrecordslist_json)
                    
    
   
#      if request.method  ==  "POST":
#                 Designation = request.POST['Designation']
#                 Department  = request.POST['Department']
#                 Division  = request.POST['Division']      # New
#                 Level  = request.POST['Level']
#                 ReportingtoDivision  = request.POST['ReportingtoDivision']      # New
#                 ReportingtoDesignation = request.POST['ReportingToDesignation']
#                 ReportingtoDepartment = request.POST['ReportingToDesignationDepartment']
#                 ReportingtoLevel = request.POST['ReportingToDesignationLevel']
#                 Vip = request.POST.get('VipCheckbox')

#                 AccommodationFlatNumber = request.POST['AccommodationFlatNumber'] or ''
                
#                 WeekOffDay = request.POST.get('WeekOffDay')

#                 VipCheckbox = False
                
#                 if Vip  == 'Vip':
#                      VipCheckbox = True
                     


#                 DottedLine = request.POST['DottedLine'] or ''

#                 OfficialEmailAddress = None
                
#                 if 'OfficialEmailAddress' in request.POST:
#                     OfficialEmailAddress = request.POST['OfficialEmailAddress']
#                 OfficialMobileNo = None
#                 if 'OfficialMobileNo' in request.POST:
#                     OfficialMobileNo  = request.POST['OfficialMobileNo']
#                 DateofJoining = request.POST['DateOfJoining']
#                 CompanyAccommodation  =  request.POST['CompanyAccommodation']
                
#                 Locker  =  request.POST['Locker']
#                 LockerType  =  request.POST['LockerType']
#                 LockerNumber  = request.POST['LockerNumber']
#                 EmploymentType   = request.POST['EmploymentType']
#                 ContractStartDate  = None
#                 if 'ContractStartDate' in request.POST:
#                     ContractStartDate  =  request.POST['ContractStartDate']
#                     if ContractStartDate == '':
#                          ContractStartDate = None
                         
                         
#                 ContractEndDate  = None
#                 if 'ContractEndDate' in request.POST:    
#                     ContractEndDate  = request.POST['ContractEndDate']
#                     if ContractEndDate == '':
#                          ContractEndDate = None



#                 if Workobj  is not None:
#                     Workobj.Designation  = Designation
#                     Workobj.Department  = Department
#                     Workobj.Division  = Division    # New
#                     Workobj.Level  = Level
#                     Workobj.ReportingtoDivision  = ReportingtoDivision     # New
#                     Workobj.ReportingtoDesignation  = ReportingtoDesignation
#                     Workobj.ReportingtoDepartment  = ReportingtoDepartment
#                     Workobj.ReportingtoLevel  = ReportingtoLevel
                  
#                     Workobj.OfficialEmailAddress = OfficialEmailAddress
#                     Workobj.OfficialMobileNo  = OfficialMobileNo
#                     Workobj.DateofJoining = DateofJoining
#                     Workobj.CompanyAccommodation  = CompanyAccommodation
#                     Workobj.AccommodationFlatNumber = AccommodationFlatNumber
#                     Workobj.Locker = Locker
#                     Workobj.LockerType = LockerType
#                     Workobj.LockerNumber  = LockerNumber
#                     Workobj.EmploymentType  = EmploymentType
#                     Workobj.ContractEndDate = ContractEndDate 
#                     Workobj.ContractStartDate = ContractStartDate
#                     Workobj.ModifyBy = UserID
#                     Workobj.DottedLine = DottedLine
#                     Workobj.VipCheckbox = VipCheckbox
#                     Workobj.WeekOffDay = WeekOffDay


#                     Workobj.save()
                  
                  
#                     if EmpID:
#                         result = update_employee_profile(EmpID, OrganizationID)
                    
#                     Success  = True
                                    
#                     # Get lists from the request
#                     DivisionList = request.POST.getlist('Division[]')
#                     DesignationList = request.POST.getlist('Designation[]')
#                     DepartmentList = request.POST.getlist('Department[]')
#                     IsDeleteList = request.POST.getlist('IsDelete[]')
#                     IdList = request.POST.getlist('ID[]')
#                     # print("IdList = ",IdList)
#                     # print("IsDeleteList = ",IsDeleteList)
#                     print("DivisionList = ",DivisionList)


#                     # Ensure all lists are of the same length
#                     if DivisionList and DesignationList and DepartmentList and IsDeleteList and IdList:
#                         for id, designation, department, is_delete, division in zip(IdList, DesignationList, DepartmentList, IsDeleteList, DivisionList):
#                             is_delete = int(is_delete)  # Convert to integer for comparison
                            
#                             if designation and department and division:
#                                 if int(id) == 0 and is_delete == 0:  # Create new record
#                                     EmployeeWorkDetails.objects.create(
#                                         EmpID=EmpID,
#                                         IsSecondary=True,
#                                         Division = division,
#                                         Designation=designation,
#                                         Department=department,
#                                         OrganizationID=OrganizationID
#                                     )
#                                 elif int(id) > 0 and is_delete == 0:  # Update existing record
#                                     existing_record = EmployeeWorkDetails.objects.filter(id=id, IsSecondary=True, EmpID=EmpID).first()
#                                     if existing_record:
#                                         existing_record.Designation = designation
#                                         existing_record.Department = department
#                                         existing_record.Division = division
#                                         existing_record.save()
#                                 elif int(id) > 0 and is_delete == 1:  # Mark record as deleted
#                                     EmployeeWorkDetails.objects.filter(id=id, IsSecondary=True, EmpID=EmpID).update(IsDelete=True)


#                 encrypted_id = encrypt_id(EmpID)
#                 url = reverse('EmployeeWorkDetailsPage')  
#                 redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
#                 return redirect(redirect_url)       
   

#      context = {
#           'OrganizationID':OrganizationID,
#           'MergedReportingtoDesignation':MergedReportingtoDesignation,
#           'Workobj':Workobj,
#           'Emobj':Emobj,
#           'EmpID':EmpID,
#           'Success':Success,
#           'MergedDottedLineDesignations':MergedDottedLineDesignations , 
#           'MergedDesignations':MergedDesignations, 
#           'merged_designations_json':merged_designations_json,
#           'subrecordslist_json':subrecordslist_json,
#         }
#      return render(request, 'HR/EmployeeDashboard/EmployeeWorkDetailsPage.html', context)


def  EmployeeWorkDetailsPage(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
          OrganizationID= OID
     UserID = str(request.session["UserID"])   
    
     Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
     
     DottedLineDesignations = CorporateDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    
     
     MergedDesignations = chain(Designations, DottedLineDesignations)
  
     MergedDottedLineDesignations =  chain(Designations, DottedLineDesignations)
     MergedReportingtoDesignation =  chain(Designations, DottedLineDesignations)

   

     merged_designations_json = DepartmentJson()
   


   
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Success  =  False
     Emobj    = None     
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        Workobj = EmployeeWorkDetails.objects.filter(OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False, EmpID=EmpID).first()
        subrecordslist_json =  subrecordsjson(EmpID,OrganizationID)
        print(subrecordslist_json)
                    
    
   
     if request.method  ==  "POST":
                Designation = request.POST['Designation']
                Department  = request.POST['Department']
                Division  = request.POST['Division']      # New
                Level  = request.POST['Level']
                ReportingtoDivision  = request.POST['ReportingtoDivision']      # New
                ReportingtoDesignation = request.POST['ReportingToDesignation']
                ReportingtoDepartment = request.POST['ReportingToDesignationDepartment']
                ReportingtoLevel = request.POST['ReportingToDesignationLevel']
                Vip = request.POST.get('VipCheckbox')

                AccommodationFlatNumber = request.POST['AccommodationFlatNumber'] or ''
                
                WeekOffDay = request.POST.get('WeekOffDay')

                VipCheckbox = False
                
                if Vip  == 'Vip':
                     VipCheckbox = True
                     


                DottedLine = request.POST['DottedLine'] or ''

                OfficialEmailAddress = None
                
                if 'OfficialEmailAddress' in request.POST:
                    OfficialEmailAddress = request.POST['OfficialEmailAddress']
                OfficialMobileNo = None
                if 'OfficialMobileNo' in request.POST:
                    OfficialMobileNo  = request.POST['OfficialMobileNo']
                DateofJoining = request.POST['DateOfJoining']
                CompanyAccommodation  =  request.POST['CompanyAccommodation']
                
                Locker  =  request.POST['Locker']
                LockerType  =  request.POST['LockerType']
                LockerNumber  = request.POST['LockerNumber']
                EmploymentType   = request.POST['EmploymentType']
                ContractStartDate  = None
                if 'ContractStartDate' in request.POST:
                    ContractStartDate  =  request.POST['ContractStartDate']
                    if ContractStartDate == '':
                         ContractStartDate = None
                         
                         
                ContractEndDate  = None
                if 'ContractEndDate' in request.POST:    
                    ContractEndDate  = request.POST['ContractEndDate']
                    if ContractEndDate == '':
                         ContractEndDate = None



                if Workobj  is not None:
                    Workobj.Designation  = Designation
                    Workobj.Department  = Department
                    Workobj.Division  = Division    # New
                    Workobj.Level  = Level
                    Workobj.ReportingtoDivision  = ReportingtoDivision     # New
                    Workobj.ReportingtoDesignation  = ReportingtoDesignation
                    Workobj.ReportingtoDepartment  = ReportingtoDepartment
                    Workobj.ReportingtoLevel  = ReportingtoLevel
                  
                    Workobj.OfficialEmailAddress = OfficialEmailAddress
                    Workobj.OfficialMobileNo  = OfficialMobileNo
                    Workobj.DateofJoining = DateofJoining
                    Workobj.CompanyAccommodation  = CompanyAccommodation
                    Workobj.AccommodationFlatNumber = AccommodationFlatNumber
                    Workobj.Locker = Locker
                    Workobj.LockerType = LockerType
                    Workobj.LockerNumber  = LockerNumber
                    Workobj.EmploymentType  = EmploymentType
                    Workobj.ContractEndDate = ContractEndDate 
                    Workobj.ContractStartDate = ContractStartDate
                    Workobj.ModifyBy = UserID
                    Workobj.DottedLine = DottedLine
                    Workobj.VipCheckbox = VipCheckbox
                    Workobj.WeekOffDay = WeekOffDay


                    Workobj.save()
                    run_background_checklist_tasks_Employee_ID(EmpID,OID,UserID)
                  
                    if EmpID:
                        result = update_employee_profile(EmpID, OrganizationID)
                    
                    Success  = True
                                    
                    # Get lists from the request
                    DivisionList = request.POST.getlist('Division[]')
                    DesignationList = request.POST.getlist('Designation[]')
                    DepartmentList = request.POST.getlist('Department[]')
                    IsDeleteList = request.POST.getlist('IsDelete[]')
                    IdList = request.POST.getlist('ID[]')
                    # print("IdList = ",IdList)
                    # print("IsDeleteList = ",IsDeleteList)
                    # print("DivisionList = ",DivisionList)


                    # Ensure all lists are of the same length
                    if DivisionList and DesignationList and DepartmentList and IsDeleteList and IdList:
                        for id, designation, department, is_delete, division in zip(IdList, DesignationList, DepartmentList, IsDeleteList, DivisionList):
                            is_delete = int(is_delete)  # Convert to integer for comparison
                            
                            if designation and department and division:
                                if int(id) == 0 and is_delete == 0:  # Create new record
                                    EmployeeWorkDetails.objects.create(
                                        EmpID=EmpID,
                                        IsSecondary=True,
                                        Division = division,
                                        Designation=designation,
                                        Department=department,
                                        OrganizationID=OrganizationID
                                    )
                                elif int(id) > 0 and is_delete == 0:  # Update existing record
                                    existing_record = EmployeeWorkDetails.objects.filter(id=id, IsSecondary=True, EmpID=EmpID).first()
                                    if existing_record:
                                        existing_record.Designation = designation
                                        existing_record.Department = department
                                        existing_record.Division = division
                                        existing_record.save()
                                elif int(id) > 0 and is_delete == 1:  # Mark record as deleted
                                    EmployeeWorkDetails.objects.filter(id=id, IsSecondary=True, EmpID=EmpID).update(IsDelete=True)


                encrypted_id = encrypt_id(EmpID)
                url = reverse('EmployeeWorkDetailsPage')  
                redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
                return redirect(redirect_url)       
   

     context = {
          'OrganizationID':OrganizationID,
          'MergedReportingtoDesignation':MergedReportingtoDesignation,
          'Workobj':Workobj,
          'Emobj':Emobj,
          'EmpID':EmpID,
          'Success':Success,
          'MergedDottedLineDesignations':MergedDottedLineDesignations , 
          'MergedDesignations':MergedDesignations, 
          'merged_designations_json':merged_designations_json,
          'subrecordslist_json':subrecordslist_json,
        }
     return render(request, 'HR/EmployeeDashboard/EmployeeWorkDetailsPage.html', context)



def UpdateEmployeeDesignation(EmpID, Promotiondesignation, OrganizationID, UserID):
    if not Promotiondesignation:
        return  
    
    PreviousWorkData = EmployeeWorkDetails.objects.filter(
        EmpID=EmpID, IsDelete=False,IsSecondary=False, OrganizationID=OrganizationID
    ).first()

    if not PreviousWorkData:
        return  

    DesignationDetails = (
        OnRollDesignationMaster.objects.filter(designations=Promotiondesignation, IsDelete=False).first()
        or CorporateDesignationMaster.objects.filter(designations=Promotiondesignation, IsDelete=False).first()
    )

    if not DesignationDetails:
        return 

  
    Department = (
        getattr(DesignationDetails.OnRollDepartmentMaster, "DepartmentName", None)
        or getattr(DesignationDetails.CorporateDepartmentMaster, "DepartmentName", None)
    )
    Level = getattr(DesignationDetails, "Lavel", None)

   
    PreviousWorkData.Designation = Promotiondesignation
    PreviousWorkData.Department = Department
    PreviousWorkData.Level = Level
    PreviousWorkData.ModifyBy = UserID
    PreviousWorkData.save()

   

def LeaveDetails(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
          OrganizationID= OID
    UserID = str(request.session["UserID"])

    encrypted_id = request.GET.get('EmpID')
    EmpID = decrypt_id(encrypted_id)
    Success  =  False
    Emobj    = None     
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID, OrganizationID)
        LeaveTypes = Leave_Type_Master.objects.filter(IsDelete=False)
        for Leave in LeaveTypes:
            Leave.Balance = 0
            if Emobj:
                LT = Emp_Leave_Balance_Master.objects.filter(
                    OrganizationID=OrganizationID, 
                    Leave_Type_Master_id=Leave.id, Emp_code=Emobj.EmployeeCode)
                if LT.exists():
                    Leave.Balance = LT[0].Balance
    
    if request.method == "POST":
      
        LT = Emp_Leave_Balance_Master.objects.filter(
            OrganizationID=OrganizationID, 
            Emp_code=Emobj.EmployeeCode)
        for l in LT:
            l.IsDelete = True
            l.ModifyBy = UserID
            l.save()

        Total_Leave = int(request.POST['Total_Leave'])
        
        for i in range(int(Total_Leave) + 1):
            LeaveID = request.POST[f'LeaveID_{i}']
            LeaveBalance = request.POST[f'LeaveBalance_{i}'] 
            Leaveobj = Emp_Leave_Balance_Master.objects.create(
                OrganizationID=OrganizationID, CreatedBy=UserID, 
                Leave_Type_Master_id=LeaveID, Balance=LeaveBalance, 
                Emp_code=Emobj.EmployeeCode)
        Success  = True    
        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('LeaveDetails')
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
        return redirect(redirect_url)
    
    context = {'Emobj': Emobj, 'LeaveTypes': LeaveTypes, 'EmpID': EmpID,'Success':Success,'OrganizationID':OrganizationID}
    return render(request, 'HR/EmployeeDashboard/LeaveDetails.html', context)


def  EmergencyInfoPage(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
          OrganizationID= OID
     UserID = str(request.session["UserID"])   
     Designations = OnRollDesignationMaster.objects.filter(IsDelete=False)
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Success  =  False
     Emobj    = None    
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        Emerobj = EmployeeEmergencyInformationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID).first()
    
     if request.method  ==  "POST":
                EmergencyFirstName =  request.POST['EmergencyFirstName']
                EmergencyMiddleName =  request.POST['EmergencyMiddleName']
                EmergencyLastName =  request.POST['EmergencyLastName']
                Relation =  request.POST['Relation']
                EmergencyContactNumber_1 = request.POST['EmergencyContactNumber_1']
                EmergencyContactNumber_2 =  request.POST['EmergencyContactNumber_2']
                ProvidentFundNumber  = request.POST['ProvidentFundNumber']
                ESINumber =  request.POST['ESINumber']
                BloodGroup =  request.POST['BloodGroup']     
                if Emerobj  is not None:
                    Emerobj.FirstName  = EmergencyFirstName
                    Emerobj.MiddleName  = EmergencyMiddleName
                    Emerobj.LastName  = EmergencyLastName
                    Emerobj.Relation  = Relation
                    Emerobj.EmergencyContactNumber_1  = EmergencyContactNumber_1
                    Emerobj.EmergencyContactNumber_2 = EmergencyContactNumber_2
                    Emerobj.ProvidentFundNumber = ProvidentFundNumber 
                    Emerobj.ESINumber  = ESINumber
                    Emerobj.BloodGroup  = BloodGroup
                    Emerobj.ModifyBy = UserID
                    Emerobj.save()
                 
                else:
                      Emerobj = EmployeeEmergencyInformationDetails.objects.create(
                                                        EmpID =  EmpID,
                                                        FirstName = EmergencyFirstName,
                                                        MiddleName = EmergencyMiddleName,
                                                        LastName = EmergencyLastName,
                                                        Relation  = Relation,
                                                        EmergencyContactNumber_1  = EmergencyContactNumber_1,
                                                        EmergencyContactNumber_2 = EmergencyContactNumber_2,
                                                        ProvidentFundNumber  = ProvidentFundNumber,
                                                        ESINumber  = ESINumber,
                                                        BloodGroup  = BloodGroup, OrganizationID = OrganizationID,CreatedBy = UserID
                                                    )    



                # if Emobj:
                #         profile_completion_percentage, missing_fields = calculate_profile_completion(Emerobj, modelname="Emergency Information")

                    
                #         Emobj.ProfileCompletion = profile_completion_percentage
                #         Emobj.MissingFields = missing_fields

                    
                #         Emobj.save()    
                if EmpID:
                        result = update_employee_profile(EmpID, OrganizationID)

                Success  =  True
                encrypted_id = encrypt_id(EmpID)
                url = reverse('EmergencyInfoPage')  
                redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
                return redirect(redirect_url)       
     context = {'Emobj':Emobj,'EmpID':EmpID,'Emergencyobj':Emerobj,'Success':Success,'OrganizationID':OrganizationID}
     return render(request, 'HR/EmployeeDashboard/EmergencyInfoPage.html', context)
              




def  AddressPage(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
          OrganizationID= OID
     UserID = str(request.session["UserID"])   
   
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Success  =  False
     Emobj    = None    
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        Addressobj = EmployeeAddressInformationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID).first()

       

     if request.method  ==  "POST":
                              
                Permanent_Address  =  request.POST['Permanent_Address'] or ''
                Permanent_City   =  request.POST['Permanent_City'] or ''
                Permanent_State  =  request.POST['Permanent_State'] or ''
                Permanent_Pincode  =  request.POST['Permanent_Pincode'] or ''
                Permanent_HousePhoneNumber  =  request.POST['Permanent_HousePhoneNumber'] or ''
                
                Permanent_LandlineNumber  =  request.POST['Permanent_LandlineNumber'] or ''


                Temporary_Address  =  request.POST['Temporary_Address'] or ''
                Temporary_City   =  request.POST['Temporary_City'] or ''
                Temporary_State  =  request.POST['Temporary_State'] or ''
                Temporary_Pincode  =  request.POST['Temporary_Pincode'] or ''
                Temporary_HousePhoneNumber  =  request.POST['Temporary_HousePhoneNumber'] or ''
                Temporary_LandlineNumber  =  request.POST['Temporary_LandlineNumber'] or ''




                if Addressobj is not None  :
                   
                        Addressobj.Permanent_Address = Permanent_Address
                        Addressobj.Permanent_City = Permanent_City
                        Addressobj.Permanent_State  = Permanent_State
                        Addressobj.Permanent_Pincode = Permanent_Pincode
                        Addressobj.Permanent_HousePhoneNumber  = Permanent_HousePhoneNumber        
                        
                        Addressobj.Temporary_Address = Temporary_Address        
                        Addressobj.Temporary_City  = Temporary_City        
                        Addressobj.Temporary_State  = Temporary_State        
                        Addressobj.Temporary_Pincode = Temporary_Pincode        
                        Addressobj.Temporary_HousePhoneNumber   = Temporary_HousePhoneNumber


                        Addressobj.ModifyBy  = UserID
                        Addressobj.save()
                         
                
                
                else:
                    Addressobj  = EmployeeAddressInformationDetails.objects.create(   EmpID =  EmpID,Permanent_Address  = Permanent_Address,Permanent_City = Permanent_City,Permanent_State = Permanent_State,Permanent_Pincode = Permanent_Pincode,Permanent_HousePhoneNumber = Permanent_HousePhoneNumber,Temporary_Address = Temporary_Address,Temporary_City =Temporary_City,Temporary_State = Temporary_State,Temporary_Pincode=Temporary_Pincode,Temporary_HousePhoneNumber=Temporary_HousePhoneNumber,OrganizationID = OrganizationID,CreatedBy = UserID,Temporary_Landline = Temporary_LandlineNumber,Permanent_Landline = Permanent_LandlineNumber
                                                                                   )
                
                # if Emobj:
                #         profile_completion_percentage, missing_fields = calculate_profile_completion(Addressobj, modelname="Address Information")

                    
                #         Emobj.ProfileCompletion = profile_completion_percentage
                #         Emobj.MissingFields = missing_fields

                    
                #         Emobj.save()            
                if EmpID:
                        result = update_employee_profile(EmpID, OrganizationID)

                Success  =  True    
                encrypted_id = encrypt_id(EmpID)
                url = reverse('AddressPage')  
                redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
                return redirect(redirect_url)       
     context = {'Emobj':Emobj,'EmpID':EmpID,'Success':Success,'Addressinfo':Addressobj,'OrganizationID':OrganizationID}
     return render(request, 'HR/EmployeeDashboard/AddressPage.html', context)






def  IdentityPage(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
          OrganizationID= OID
     UserID = str(request.session["UserID"])   
  
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Success  =  False
     Emobj    = None    
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        identityobj = EmployeeIdentityInformationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID).first()

       

     if request.method  ==  "POST":
                                        
                        PANNo = request.POST['PANNo'] or ''
                        AadhaarNumber = request.POST['AadhaarNumber'] or ''
                        DrivingLicenceNo = request.POST['DrivingLicenceNo'] or ''
                        PANattachment = request.FILES.get('PANattachment')
                        Aadhaarattachment = request.FILES.get('Aadhaarattachment')
                        DrivingLicenceattachment = request.FILES.get('DrivingLicenceattachment')

                        if identityobj is not None:
                            identityobj.PANNo  = PANNo
                            identityobj.AadhaarNumber = AadhaarNumber
                            identityobj.DrivingLicenceNo  = DrivingLicenceNo
                            identityobj.ModifyBy  = UserID
                            identityobj.save()
                            if PANattachment:
                                        upload_file(PANattachment,identityobj.id,"Documents","EmployeeIdentityInformationDetails_Pan")
                                        result = update_employee_profile(EmpID, OrganizationID) 

                            if Aadhaarattachment:
                                        upload_file(Aadhaarattachment,identityobj.id,"Documents","EmployeeIdentityInformationDetails_Aadhaar")
                                        result = update_employee_profile(EmpID, OrganizationID) 
                                        
                            if DrivingLicenceattachment:
                                        upload_file(DrivingLicenceattachment,identityobj.id,"Documents","EmployeeIdentityInformationDetails_License")          
                                        result = update_employee_profile(EmpID, OrganizationID) 

                          
                        
                        else:
                            newidentityobj =  EmployeeIdentityInformationDetails.objects.create(   EmpID =  EmpID,
                                    PANNo = PANNo,AadhaarNumber = AadhaarNumber,DrivingLicenceNo = DrivingLicenceNo,OrganizationID=OrganizationID,
                                            CreatedBy=UserID
                                )
                            
                            if PANattachment:
                                        upload_file(PANattachment,newidentityobj.id,"Docuemnts","EmployeeIdentityInformationDetails_Pan")
                           

                            if Aadhaarattachment:
                                        upload_file(Aadhaarattachment,newidentityobj.id,"Docuemnts","EmployeeIdentityInformationDetails_Aadhaar")
                         
                            if DrivingLicenceattachment:
                                        upload_file(DrivingLicenceattachment,newidentityobj.id,"Docuemnts","EmployeeIdentityInformationDetails_License")
                           
                        
                        
                        # if Emobj:
                        #     profile_completion_percentage, missing_fields = calculate_profile_completion(identityobj, modelname="Identity Information")

                        
                        #     Emobj.ProfileCompletion = profile_completion_percentage
                        #     Emobj.MissingFields = missing_fields

                        
                        #     Emobj.save()   
                        if EmpID:
                            result = update_employee_profile(EmpID, OrganizationID) 
                        Success  =  True        
                        

                        encrypted_id = encrypt_id(EmpID)
                        url = reverse('IdentityPage')  
                        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
                        return redirect(redirect_url)       
     context = {'Emobj':Emobj,'EmpID':EmpID,'Success':Success,'IdentityInfo':identityobj,'OrganizationID':OrganizationID}
     return render(request, 'HR/EmployeeDashboard/IdentityPage.html', context)





def  BankDetailsPage(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
          OrganizationID= OID
     UserID = str(request.session["UserID"])   
  
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Success  =  False
     Emobj    = None    
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        Bankobj   = EmployeeBankInformationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID).first()
        
       
       

     if request.method  ==  "POST":
                        # Bank Details Information 
                        BankAccountNumber = request.POST['BankAccountNumber'] or ''
                        NameofBank   = request.POST['NameofBank'] or ''
                        BankBranch   = request.POST['BankBranch'] or ''
                        IFSCCode   = request.POST['IFSCCode'] or ''
                        if Bankobj is not None:
                            Bankobj.BankAccountNumber  = BankAccountNumber
                            Bankobj.NameofBank   = NameofBank
                            Bankobj.BankBranch  =BankBranch
                            Bankobj.IFSCCode  = IFSCCode
                            Bankobj.save()
                        

                        else:
                            Bankobj = EmployeeBankInformationDetails.objects.create(EmpID =  EmpID,
                                BankAccountNumber  =BankAccountNumber,NameofBank  = NameofBank,BankBranch  = BankBranch,IFSCCode = IFSCCode,OrganizationID = OrganizationID,CreatedBy = UserID
                            )
                    
                        
                        # if Emobj:
                        #     profile_completion_percentage, missing_fields = calculate_profile_completion(Bankobj, modelname="Bank Information")

                        
                        #     Emobj.ProfileCompletion = profile_completion_percentage
                        #     Emobj.MissingFields = missing_fields

                        
                        #     Emobj.save()    
                        if EmpID:
                            result = update_employee_profile(EmpID, OrganizationID)
                
                        Success  =  True   
                        encrypted_id = encrypt_id(EmpID)
                        url = reverse('BankDetailsPage')  
                        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
                        return redirect(redirect_url)       
     context = {'Emobj':Emobj,'EmpID':EmpID,'Success':Success,'Bankinfo':Bankobj,'OrganizationID':OrganizationID}
     return render(request, 'HR/EmployeeDashboard/BankDetailsPage.html', context)



def  SalaryDetailsPage(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")

     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
          OrganizationID= OID
     UserID = str(request.session["UserID"])   
   
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Success  =  False
     Emobj    = None  
       
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        Effective_Data = Salary_Details_Effective.objects.filter(IsDelete=0, OrganizationID=OrganizationID, EmpID=EmpID)
        # Effective_Data = Salary_Details_Effective.objects.filter(IsDelete=0, OrganizationID=OrganizationID, EmpID=EmpID).values("EffectiveFrom","CTC")
        
     context = {
          'Emobj':Emobj,
          'EmpID':EmpID,
          'UserID':UserID,
          'Success':Success, 
          'OrganizationID':OrganizationID,
          'Effective_Data':Effective_Data
        }
     return render(request, 'HR/EmployeeDashboard/SalaryDetailsPage.html', context)



def update_employee_ctc(EmpID, OrganizationID, UserID, ctc):
    if EmpID:
        Workobj = EmployeeWorkDetails.objects.filter(
            OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False, EmpID=EmpID
        ).first()
        
        if Workobj:
            if ctc is not None:
                Workobj.Salary = ctc
                Workobj.ModifyBy = UserID
                Workobj.save()
            update_employee_profile(EmpID, OrganizationID) 

            print("Salary updated successfully.")
        else:
            print("Employee Work Details not found for the given Employee ID.")
    else:
        print("Employee ID is required.")


def UpdateCTC(EmpID, OrganizationID, UserID):
    if EmpID:
        Workobj = EmployeeWorkDetails.objects.filter(
            OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False, EmpID=EmpID
        ).first()
        
        if Workobj:
            salarytitle = SalaryTitle_Master.objects.filter(
                IsDelete=False, Title__icontains='CTC (A+C)'
            ).first()
            
            if salarytitle:
                salaryobj = Salary_Detail_Master.objects.filter(
                    IsDelete=False, EmpID=EmpID, OrganizationID=OrganizationID,
                    Salary_title_id=salarytitle.id
                ).first()
                
                if salaryobj:
                    Salary = salaryobj.Permonth
                    if Salary:
                        Workobj.Salary = Salary
                        Workobj.ModifyBy = UserID
                        Workobj.save()
                        result = update_employee_profile(EmpID, OrganizationID) 

                        print("Salary updated successfully.")
                    else:
                        print("Salary value is missing in Salary_Detail_Master.")
                else:
                    print("Salary details not found for the given Employee.")
            else:
                print("Salary title 'CTC (A+C)' not found.")
        else:
            print("Employee Work Details not found for the given Employee ID.")
    else:
        print("Employee ID is required.")



@transaction.atomic
def UpdateEmployeeSalaryGridByPromotion(EmpID, Promotionobj, OrganizationID, UserID):

    prev_effective = Salary_Details_Effective.objects.filter(
        EmpID=EmpID,
        OrganizationID=OrganizationID,
        IsDelete=False
    ).order_by('-EffectiveFrom').first()

    promotion_date = Promotionobj.date_of_promtion

    if isinstance(promotion_date, str):
        promotion_date = datetime.strptime(promotion_date, "%Y-%m-%d").date()

    if prev_effective:
        prev_effective.EffectiveTo = promotion_date - timedelta(days=1)
        prev_effective.ModifyBy = UserID
        prev_effective.save()

    promotion_salaries = PromotionSalaryDetails.objects.filter(
        PromotionLetterEmployeeDetail=Promotionobj,
        OrganizationID=OrganizationID,
        IsDelete=False
    )

    if not promotion_salaries.exists():
        raise ValueError("No promotion salary details found")

    effective_obj = Salary_Details_Effective.objects.create(
        EmpID=EmpID,
        EffectiveFrom=Promotionobj.date_of_promtion,
        EffectiveTo=None,
        OrganizationID=OrganizationID,
        CreatedBy=UserID,
    )

    total_ctc = Decimal(0)

    for ps in promotion_salaries:
        per_month = Decimal(ps.RevisedSal or 0)
        per_annum = per_month * Decimal(12)
        total_ctc += per_annum

        Salary_Detail_Master.objects.create(
            EmpID=EmpID,
            Salary_title_id=ps.Salary_title_id,
            Permonth=per_month,
            Perannum=per_annum,
            Effective=effective_obj,
            OrganizationID=OrganizationID,
            CreatedBy=UserID,
        )

    effective_obj.CTC = total_ctc
    effective_obj.save()

    update_employee_ctc(EmpID, OrganizationID, UserID, total_ctc / Decimal(12))


# @transaction.atomic
# def UpdateEmployeeSalaryGridByIncreamnet(EmpID, Increamentobj, OrganizationID, UserID):

#     prev_effective = Salary_Details_Effective.objects.filter(
#         EmpID=EmpID,
#         OrganizationID=OrganizationID,
#         IsDelete=False
#     ).order_by('-EffectiveFrom').first()

#     Increament_date = Increamentobj.date_of_salary_increament

#     if isinstance(Increament_date, str):
#         Increament_date = datetime.strptime(Increament_date, "%Y-%m-%d").date()

#     if prev_effective:
#         prev_effective.EffectiveTo = Increament_date - timedelta(days=1)
#         prev_effective.ModifyBy = UserID
#         prev_effective.save()

#     Increament_salaries = IncreamentSalaryDetails.objects.filter(
#         LETTEROFSALARYINCREAMENTEmployeeDetail=Increamentobj,
#         OrganizationID=OrganizationID,
#         IsDelete=False
#     )

#     if not Increament_salaries.exists():
#         raise ValueError("No promotion salary details found")

#     effective_obj = Salary_Details_Effective.objects.create(
#         EmpID=EmpID,
#         EffectiveFrom=Increamentobj.date_of_salary_increament,
#         EffectiveTo=None,
#         OrganizationID=OrganizationID,
#         CreatedBy=UserID,
#     )

#     total_ctc = Decimal(0)

#     for ps in Increament_salaries:
#         per_month = Decimal(ps.RevisedSal or 0)
#         per_annum = per_month * Decimal(12)
#         total_ctc += per_annum
                 
#         Salary_Detail_Master.objects.create(
#             EmpID=EmpID,
#             Salary_title_id = ps.Salary_title.id,
#             Permonth=ps.RevisedSal,
#             Perannum=per_annum,
#             Effective=effective_obj,
#             OrganizationID=OrganizationID,  
#             CreatedBy=UserID,
#         )

#     effective_obj.CTC = total_ctc
#     effective_obj.save()

#     update_employee_ctc(EmpID, OrganizationID, UserID, total_ctc / Decimal(12))


# def UpdateEmployeeSalaryGridByIncreamnet(EmpID, Increamentobj, OrganizationID, UserID):
#     try:
       
#         SC = Salary_Detail_Master.objects.filter(IsDelete=False,EmpID=EmpID,OrganizationID=OrganizationID)
#         for s in SC:
              
#                 s.IsDelete = True
#                 s.ModifyBy  = UserID
#                 s.save()

#         increamnet_salaries = IncreamentSalaryDetails.objects.filter(LETTEROFSALARYINCREAMENTEmployeeDetail=Increamentobj,OrganizationID=OrganizationID,IsDelete=False)

#         for increa_salary in increamnet_salaries:
          
#             per_annum_salary = increa_salary.RevisedSal * 12  

            
#             newsal = Salary_Detail_Master.objects.create(
#                 EmpID=EmpID,
#                 Salary_title_id = increa_salary.Salary_title.id,
#                 Permonth=increa_salary.RevisedSal,
#                 Perannum=per_annum_salary,
#                 OrganizationID=OrganizationID,  
#                 CreatedBy=UserID,
            
#             )
          

#         UpdateCTC(EmpID, OrganizationID, UserID)
#         print("Employee salary grid updated with new entries successfully.")
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         raise



# from datetime import datetime, timedelta
# from decimal import Decimal
# from django.db import transaction


@transaction.atomic
def UpdateEmployeeSalaryGridByIncreamnet(EmpID, Increamentobj, OrganizationID, UserID):

    # 1. Fetch previous effective record
    prev_effective = Salary_Details_Effective.objects.filter(
        EmpID=EmpID,
        OrganizationID=OrganizationID,
        IsDelete=False
    ).order_by('-EffectiveFrom').first()

    # 2. Normalize increment date (important to avoid TypeError)
    increament_date = Increamentobj.date_of_salary_increament
    if isinstance(increament_date, str):
        increament_date = datetime.strptime(increament_date, "%Y-%m-%d").date()

    # 3. Close previous effective period
    if prev_effective:
        prev_effective.EffectiveTo = increament_date - timedelta(days=1)
        prev_effective.ModifyBy = UserID
        prev_effective.save()

    # 4. Fetch increment salary details
    increament_salaries = IncreamentSalaryDetails.objects.filter(
        LETTEROFSALARYINCREAMENTEmployeeDetail=Increamentobj,
        OrganizationID=OrganizationID,
        IsDelete=False
    )

    if not increament_salaries.exists():
        raise ValueError("No increment salary details found")

    # 5. Create new effective record
    effective_obj = Salary_Details_Effective.objects.create(
        EmpID=EmpID,
        EffectiveFrom=increament_date,
        EffectiveTo=None,
        OrganizationID=OrganizationID,
        CreatedBy=UserID,
    )

    # 6. Insert salary grid for this effective period
    total_ctc = Decimal("0.00")

    for sal in increament_salaries:
        per_month = Decimal(sal.RevisedSal or 0)
        per_annum = per_month * Decimal(12)
        # total_ctc += per_annum
        total_ctc += per_month

        Salary_Detail_Master.objects.create(
            EmpID=EmpID,
            Salary_title_id=sal.Salary_title.id,
            Permonth=per_month,
            Perannum=per_annum,
            Effective=effective_obj,
            OrganizationID=OrganizationID,
            CreatedBy=UserID,
        )

    # 7. Update CTC
    effective_obj.CTC = total_ctc
    print("montlhy ctc is here:", total_ctc)
    effective_obj.save()

    update_employee_ctc(
        EmpID,
        OrganizationID,
        UserID,
        total_ctc / Decimal(12)
    )




def EmployeeDetailHistroy(EmpID,OrganizationID,EmpCode):
    Salaryhis  = SalaryHistory.objects.filter(OrganizationID=OrganizationID,EmpID=EmpID,IsDelete=False)
    Designationhis  = DesignationHistory.objects.filter(OrganizationID=OrganizationID,EmpID=EmpID,IsDelete=False)
    Appointment =  LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(OrganizationID=OrganizationID,IsDelete=False,emp_code=EmpCode).first()
    SalaryIncreament  = LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(OrganizationID=OrganizationID,IsDelete=False,emp_code=EmpCode)
    Confirmation = Emp_Confirmation_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpCode=EmpCode).first()
    Promotion  =  PromotionLetterEmployeeDetail.objects.filter(OrganizationID=OrganizationID,IsDelete=False,emp_code=EmpCode)
    TenureData  = EmployeeWorkDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,IsSecondary=False,EmpID=EmpID).first().tenure_till_today
    if TenureData:
         tenure_till_today = TenureData
         
    History = {'Salaryhis':Salaryhis,'Designationhis':Designationhis,'Appointment':Appointment,'SalaryIncreament':SalaryIncreament,'Confirmation':Confirmation,'Promotion':Promotion,'tenure_till_today':tenure_till_today}
    
    
    return History
    

from Checklist_Issued.views import run_background_checklist_tasks_Employee_ID


def DocumentinfoPage(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
          OrganizationID= OID
    UserID = str(request.session["UserID"])   
  
    encrypted_id = request.GET.get('EmpID')
    EmpID = decrypt_id(encrypted_id)
    Success = False
    Emobj = None
    
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID, OrganizationID)
        docobj = EmployeeDocumentsInformationDetails.objects.filter(OrganizationID=OrganizationID, IsDelete=False, EmpID=EmpID)
    
    if request.method == "POST":
        Title = request.POST.getlist('Title[]')
        Doc_ids = request.POST.getlist('Doc_ids[]')
        AttachmentDocumenstsFile = request.FILES.getlist('AttachmentDocumenstsFile[]')
        removed_Doc_ids_str = request.POST.getlist('removed_Doc_ids[]', [])
        removed_Doc_ids = [int(id) for id in removed_Doc_ids_str if id.isdigit()]
        
        if len(removed_Doc_ids) > 0:
            for id in removed_Doc_ids:

                docdelete = EmployeeDocumentsInformationDetails.objects.filter(id=id).first()
                if docdelete:  
                    docdelete.IsDelete = True
                    docdelete.save()
        
        if Doc_ids:
            d = 0
            for id, title in zip(Doc_ids, Title):
                if id.startswith('new_'):
                    newDocObject = EmployeeDocumentsInformationDetails.objects.create(
                        EmpID=EmpID,
                        Title=title,
                        OrganizationID=OrganizationID,
                        CreatedBy=UserID
                    )
                    File = AttachmentDocumenstsFile[d]
                    if File:
                        upload_file(File, newDocObject.id, "Documents", "EmployeeDocumentsInformationDetails")
                    d = d + 1
                else:
                    DocObjectUpdated = EmployeeDocumentsInformationDetails.objects.filter(IsDelete=False, EmpID=EmpID, id=id).update(Title=title, ModifyBy=UserID)
                    if not DocObjectUpdated:
                        DocObject = EmployeeDocumentsInformationDetails.objects.create(
                            EmpID=EmpID,
                            Title=title,
                            OrganizationID=OrganizationID,
                            CreatedBy=UserID
                        )
                        File = EmployeeDocumentsInfoData.objects.filter(id=id).first()
                        if File:
                            file_content, file_type = CopyFile(File.FileName)
                            file_io = BytesIO(file_content)
                            file_io.name = File.FileName
                            upload_file(file_io, DocObject.id, "Documents", "EmployeeDocumentsInformationDetails")
        else:
                    for  title,Attachment in zip(Title,AttachmentDocumenstsFile):
                            DObject  = EmployeeDocumentsInfoData.objects.create(
                                MasterID =  EmpID,
                                Title = title,OrganizationID=OrganizationID,
                                CreatedBy=UserID
                            )
                            if Attachment:
                                upload_file(Attachment, DObject.id, "Documents", "EmployeeDocumentsInformationDetails")

        run_background_checklist_tasks_Employee_ID(EmpID,OID,UserID)
                                  
        Success = True        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('DocumentinfoPage')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
        return redirect(redirect_url)
    
    context = {'Emobj': Emobj, 'EmpID': EmpID, 'Success': Success, 'Documents': docobj,'OrganizationID':OrganizationID}
    return render(request, 'HR/EmployeeDashboard/DocumentinfoPage.html', context)






def PreviousworkinfoPage(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
          OrganizationID= OID
    UserID = str(request.session["UserID"])   
 
    encrypted_id = request.GET.get('EmpID')
    EmpID = decrypt_id(encrypted_id)
    Success = False
    Emobj = None
    
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID, OrganizationID)
        prevobj = EmployeePreviousWorkInformationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID)
    
    if request.method == "POST":
                       
                Company =  request.POST.getlist('Company[]')
                Position =  request.POST.getlist('Position[]')
                FromDate =  request.POST.getlist('FromDate[]')
                ToDate =  request.POST.getlist('ToDate[]')
                Salary =  request.POST.getlist('Salary[]')
                AttachmentPreviousWork  = request.FILES.getlist('AttachmentPreviousWork[]')
                
                
                Pre_ids = request.POST.getlist('Pre_ids[]')
                removed_Pre_ids_str = request.POST.get('removed_Pre_ids[]', '')
              
             
              
                
                removed_Pre_ids = []
                if removed_Pre_ids_str:
                    try:
                        removed_Pre_ids = [int(id_str) for id_str in removed_Pre_ids_str.split(',') if id_str.isdigit()]
                    except ValueError as e:
                        print(f"Error parsing removed_Pre_ids: {e}")    
                if len(removed_Pre_ids) > 0:
                      
                        for id in removed_Pre_ids:
                          
                            previousdelete = EmployeePreviousWorkInformationDetails.objects.filter(id=id).first()
                          
                            previousdelete.IsDelete  = True
                            previousdelete.ModifyBy = UserID

                            previousdelete.save()
                if  Pre_ids:
                     p = 0
                     for  id,company,position,fromDate,toDate,salary in zip(Pre_ids,Company,Position,FromDate,ToDate,Salary):
                        if id.startswith('new_'):
                            newPreviousObject  = EmployeePreviousWorkInformationDetails.objects.create(
                                 EmpID =  EmpID,
                                 Company  = company,Position = position,FromDate =fromDate,ToDate = toDate,Salary = salary, OrganizationID=OrganizationID
                            ,CreatedBy=UserID

                            )
                            File = AttachmentPreviousWork[p]
                            if File:
                                upload_file(File, newPreviousObject.id, "PreviousWork", "EmployeePreviousWorkInformationDetails")

                            p =  p + 1
                        else:
                            PreviousObjectUpdated  = EmployeePreviousWorkInformationDetails.objects.filter( EmpID=EmpID,IsDelete=False, id=id).update(
                            Company  = company
                            ,Position  = position
                            ,FromDate  =fromDate
                            ,ToDate   = toDate
                            ,Salary  = salary
                            ,ModifyBy=UserID
                            )
                            if not  PreviousObjectUpdated:
                                 Pobj  = EmployeePreviousWorkInformationDetails.objects.create(
                                 EmpID =  EmpID,
                                 Company  = company,Position = position,FromDate =fromDate,ToDate = toDate,Salary = salary, OrganizationID=OrganizationID
                                 ,CreatedBy=UserID

                                )
                                 File = EmployeePreviousWorkData.objects.filter(id=id).first()

                                 if File:
                                        file_content, file_type = CopyFile(File.FileName)
                                        
                                    
                                        file_io = BytesIO(file_content)
                                        file_io.name = File.FileName 
                                        
                                        upload_file(file_io, Pobj.id, "PreviousWork", "EmployeePreviousWorkInformationDetails")    
        
                
                else:
                    for  company,position,fromDate,toDate,salary,Attachment in zip(Company,Position,FromDate,ToDate,Salary,AttachmentPreviousWork):
                       
                            PreviousObject  = EmployeePreviousWorkInformationDetails.objects.create(
                                 EmpID =  EmpID,
                                 Company  = company,Position = position,FromDate =fromDate,ToDate = toDate,Salary = salary ,OrganizationID=OrganizationID,   CreatedBy=UserID

                            )

                            if Attachment:
                                
                                  upload_file(File, PreviousObject.id, "PreviousWork", "EmployeePreviousWorkInformationDetails") 
                
                Success = True        
                encrypted_id = encrypt_id(EmpID)
                url = reverse('PreviousworkinfoPage')  
                redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
                return redirect(redirect_url)
    
    context = {'Emobj': Emobj, 'EmpID': EmpID, 'Success': Success, 'previousworks': prevobj,'OrganizationID':OrganizationID}
    return render(request, 'HR/EmployeeDashboard/PreviousworkinfoPage.html', context)








def QualificationinfoPage(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
          OrganizationID= OID
    UserID = str(request.session["UserID"])   
 
    encrypted_id = request.GET.get('EmpID')
    EmpID = decrypt_id(encrypted_id)
    Success = False
    Emobj = None
    
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID, OrganizationID)
        Eduboj  =  EmployeeQualificationDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID)
        
    
    if request.method == "POST":
                             
                EducationType  = request.POST.getlist('EducationType[]')
                DegreeCourse =  request.POST.getlist('DegreeCourse[]')
                InstitutionName = request.POST.getlist('InstitutionName[]')
                Year= request.POST.getlist('Year[]')
                # Percentage  = request.POST.getlist('Percentage[]')
                AttachmentsFile = request.FILES.getlist('AttachmentEducation[]')

                Edu_ids = request.POST.getlist('Edu_ids[]')

                removed_Edu_ids_str = request.POST.get('removed_Edu_ids[]', '')
               
                removed_Edu_ids = []
                if removed_Edu_ids_str:
                    try:
                        removed_Edu_ids = [int(id_str) for id_str in removed_Edu_ids_str.split(',') if id_str.isdigit()]
                    except ValueError as e:
                        print(f"Error parsing removed_Edu_ids: {e}")  
               
               
                if len(removed_Edu_ids)>0:
                    for id in removed_Edu_ids:
                        education_delete = EmployeeQualificationDetails.objects.filter(id=id).first()
                        if education_delete:
                            education_delete.IsDelete = True
                            education_delete.save()


                if Edu_ids:
                  
                    i = 0 
                    for id, Education, Degree, Institution, year in zip(Edu_ids, EducationType, DegreeCourse, InstitutionName, Year):
                        if id.startswith('new_'):
                            newEdud = EmployeeQualificationDetails.objects.create(
                                EmpID=EmpID,
                                EducationType=Education,
                                Degree_Course=Degree,
                                NameoftheInstitution=Institution,
                                Year=year,
                              
                                OrganizationID=OrganizationID,
                                CreatedBy=UserID
                            )
                            File = AttachmentsFile[i]
                            if  File:
                                upload_file(File, newEdud.id, "Education", "EmployeeQualificationDetails")
                            i = i + 1

                            

                        else:
                            updated = EmployeeQualificationDetails.objects.filter(
                                EmpID=EmpID, IsDelete=False, id=id
                            ).update(
                                EducationType=Education,
                                Degree_Course=Degree,
                                NameoftheInstitution=Institution,
                                Year=year,
                             
                                ModifyBy=UserID
                            )
                         
                              
                            if not updated:
                                Obj = EmployeeQualificationDetails.objects.create(
                                    EmpID=EmpID,
                                    EducationType=Education,
                                    Degree_Course=Degree,
                                    NameoftheInstitution=Institution,
                                    Year=year,
                                 
                                    OrganizationID=OrganizationID,
                                    CreatedBy=UserID
                                )
                                File = EmployeeEducationData.objects.filter(id=id).first()

                                if File:
                                    file_content, file_type = CopyFile(File.FileName)
                                    
                                   
                                    file_io = BytesIO(file_content)
                                    file_io.name = File.FileName 
                                    
                                    upload_file(file_io, Obj.id, "Education", "EmployeeQualificationDetails")
 
                else:
                     for Education, Degree, Institution, year, Attachment in zip(EducationType, DegreeCourse, InstitutionName, Year, AttachmentsFile):
                        Eobj=EmployeeQualificationDetails.objects.create(
                            EmpID=EmpID,
                            EducationType=Education,
                            Degree_Course=Degree,
                            NameoftheInstitution=Institution,
                            Year=year,
                         
                            OrganizationID=OrganizationID,
                            CreatedBy=UserID
                        )
                        if Attachment:
                                
                                  upload_file(Attachment, Eobj.id, "Education", "EmployeeQualificationDetails")
                       
              
                run_background_checklist_tasks_Employee_ID(EmpID,OID,UserID)
            
                Success = True        
                encrypted_id = encrypt_id(EmpID)
                url = reverse('QualificationinfoPage')  
                redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
                return redirect(redirect_url)
    
    context = {'Emobj': Emobj, 'EmpID': EmpID, 'Success': Success, 'Educations': Eduboj,'OrganizationID':OrganizationID}
    return render(request, 'HR/EmployeeDashboard/QualificationinfoPage.html', context)








def FamilyinfoPage(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
          OrganizationID= OID
    UserID = str(request.session["UserID"])   
 
    encrypted_id = request.GET.get('EmpID')
    EmpID = decrypt_id(encrypted_id)
    Success = False
    Emobj = None
    Childbbj  = None
    
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID, OrganizationID)
        FamilyObj =  EmployeeFamilyDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID = EmpID).first()
         
        if FamilyObj is not  None:
            Childbbj = EmployeeChildDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,FamilyID = FamilyObj.id)
      
    
    if request.method == "POST":
                             
                SpouseName = request.POST.get('SpouseName', None)
                SpouseAge = request.POST.get('SpouseAge', 0)
                if SpouseAge == '' :
                     SpouseAge = '' 
                SpouseDOB = request.POST.get('SpouseDOB', None)
                if SpouseDOB == '':
                        SpouseDOB = None 
                SpouseContactNo = request.POST.get('SpouseContact', None)


                MotherName = request.POST.get('MotherName', None)
                MotherAge = request.POST.get('MotherAge', 0)
                if MotherAge == '' :
                     SpouseAge = ''
                MotherDOB = request.POST.get('MotherDOB', None)
                if MotherDOB == '':
                        MotherDOB = None 
                MotherContactNo = request.POST.get('MotherContact', None)

                FatherName = request.POST.get('FatherName', None)
                FatherAge = request.POST.get('FatherAge', 0)
                if FatherAge == '' :
                     SpouseAge = ''
                FatherDOB = request.POST.get('FatherDOB', None)
                if FatherDOB == '':
                        FatherDOB = None 
                FatherContactNo = request.POST.get('FatherContact', None)
                
                            
                # LandlineNo = request.POST.get('LandlineNo', None)
                child_update_ids  = request.POST.getlist('child_ids[]')
             
                child_names = request.POST.getlist('childName[]')
                child_ages = request.POST.getlist('childAge[]')
                child_relations = request.POST.getlist('childrelations[]')
                
                removed_child_ids_str = request.POST.get('removed_child_ids[]')


                removed_child_ids = []
                if removed_child_ids_str:
                    try:
                        removed_child_ids = [int(id_str) for id_str in removed_child_ids_str.split(',') if id_str.isdigit()]
                    except ValueError as e:
                        print(f"Error parsing removed_child_ids: {e}")
                if FamilyObj is not None:
                    FamilyObj.SpouseName  = SpouseName
                    FamilyObj.SpouseAge  = SpouseAge
                    FamilyObj.SpouseContactNo = SpouseContactNo
                    FamilyObj.SpouseDateofBirth  = SpouseDOB

                    FamilyObj.MotherName = MotherName
                    FamilyObj.MotherDateofBirth  = MotherDOB
                    FamilyObj.MotherAge  = MotherAge
                    FamilyObj.MotherContactNo = MotherContactNo

                    FamilyObj.FatherName  = FatherName  
                    FamilyObj.FatherDateofBirth = FatherDOB
                    FamilyObj.FatherAge  = FatherAge
                    FamilyObj.FatherContactNo = FatherContactNo
                    # FamilyObj.LandlineNo = LandlineNo
                    FamilyObj.ModifyBy = UserID
                    FamilyObj.save()
                    child_update_ids  = request.POST.getlist('child_ids[]')
                
                   

                 
                    if len(removed_child_ids) > 0:
                        for rid in removed_child_ids:
                            rdelete = EmployeeChildDetails.objects.filter(id=rid).first()
                            if rdelete:
                                rdelete.IsDelete = True
                                rdelete.save()

                    for id, name, age, relation in zip(child_update_ids, child_names, child_ages, child_relations):
                        if id.startswith('new_'):
                         
                            EmployeeChildDetails.objects.create(
                                FamilyID=FamilyObj.id,
                                Name=name,
                                Age=age,
                                Relation=relation,
                                OrganizationID=OrganizationID,
                                CreatedBy=UserID
                            )
                        else:
                          
                            updated_rows = EmployeeChildDetails.objects.filter(FamilyID=FamilyObj.id, id=id).update(
                                Name=name,
                                Age=age,
                                Relation=relation
                            )
                           
                            if not updated_rows:
                                EmployeeChildDetails.objects.create(
                                    FamilyID=FamilyObj.id,
                                    Name=name,
                                    Age=age,
                                    Relation=relation,
                                    OrganizationID=OrganizationID,
                                    CreatedBy=UserID
                                )
                else:
                     FamilyObj = EmployeeFamilyDetails.objects.create(
                                 EmpID = EmpID
                                ,SpouseName  = SpouseName
                                ,SpouseAge  = SpouseAge
                                ,SpouseContactNo = SpouseContactNo
                                ,SpouseDateofBirth  = SpouseDOB

                                ,MotherName = MotherName
                                ,MotherDateofBirth  = MotherDOB
                                ,MotherAge  = MotherAge
                                ,MotherContactNo = MotherContactNo

                                ,FatherName  = FatherName  
                                ,FatherDateofBirth = FatherDOB
                                ,FatherAge  = FatherAge
                                ,FatherContactNo = FatherContactNo,
                                # LandlineNo=LandlineNo,
                                OrganizationID = OrganizationID,
                                CreatedBy = UserID                       
                     )
                     if len(child_names) > 0:
                        for name, age, relation in zip(child_names, child_ages, child_relations):
                                cobj  = EmployeeChildDetails.objects.create(
                                    FamilyID = FamilyObj.id,
                                    Name = name,
                                    Age = age,
                                    Relation = relation,OrganizationID = OrganizationID,CreatedBy = UserID
                                )  
                
                # if Emobj:
                #         profile_completion_percentage, missing_fields = calculate_profile_completion(FamilyObj, modelname="Family Details")

                    
                #         Emobj.ProfileCompletion = profile_completion_percentage
                #         Emobj.MissingFields = missing_fields

                    
                #         Emobj.save()    
                if EmpID:
                        result = update_employee_profile(EmpID, OrganizationID)
                Success = True        
                encrypted_id = encrypt_id(EmpID)
                url = reverse('FamilyinfoPage')  
                redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
                return redirect(redirect_url)
    SpouseChild = True 
    if EmpID:
         Employeeobj  = EmployeePersonalDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID=EmpID).first()     
         if Employeeobj.MaritalStatus ==  'Unmarried':
                SpouseChild = False 
    context = {'Emobj': Emobj, 'EmpID': EmpID, 'Success': Success,   'Finfoobj': FamilyObj,
            'childs':Childbbj,'SpouseChild':SpouseChild,'OrganizationID':OrganizationID }
    return render(request, 'HR/EmployeeDashboard/FamilyinfoPage.html', context)





from Letter_Of_Trainees_Experience.models import Trainees_Experience_Employee_Detail
from Policy_Data_Privacy.models import Data_Privacy_Employee_Detail
from LETTEROFAPPOINTMENT.models import LOALETTEROFAPPOINTMENTEmployeeDetail
from LETTER_OF_WORK_EXPERIENCE.models import LETTEROFEXPERIENCEEmployeeDetail
from LetteofPromotion.models import PromotionLetterEmployeeDetail
from LetterSalaryIncrement.models import LETTEROFSALARYINCREAMENTEmployeeDetail
from RevealingLetter.models import RevealingLetterEmployeeDetail
from AdvanceSalaryForm.models import AdvanceSalaryForm 
from Debit_Note.models import Debit_Note_Employee_Detail
from Policy_Posh.models import Policy_Posh_Employee_Detail
from Indemnity_Accommodation.models import Indemnity_Accommodation_Employee_Detail
from django.db.models import Max

def EmployeeLetters(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
        OrganizationID= OID
    UserID = str(request.session["UserID"])   
   
    encrypted_id = request.GET.get('EmpID')
    EmpID = decrypt_id(encrypted_id)
    Succcess = False
    Emobj    = None    
    if EmpID:
       Emobj = EmployeeCardDetails(EmpID,OrganizationID)
       EC  = Emobj.EmployeeCode
       
    AppointemetLetters  = None
    ExperienceLetters  = None
    PromotionLetters  = None
    IncreamentLetters  = None
    RevealingLetters = None 

    # Appointemet = 'Show'
    # AppointemetLetters  = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(OrganizationID=OrganizationID,IsDelete=False,emp_code= EC)
    # if  AppointemetLetters.count() >0:
    #     Appointemet = 'Hide'

    AppointemetLetters = list(
        LOALETTEROFAPPOINTMENTEmployeeDetail.objects
        .filter(OrganizationID=OrganizationID,IsDelete=False,emp_code=EC)
        .only(
            'id',
            'emp_code',
            'first_name',
            'last_name',
            'designation',
            'department',
            'file_name',
            'date_of_appointment'
        )
    )
    Appointemet = 'Show' if not AppointemetLetters else 'Hide'
        
    # Experienceshow = 'Show'   
    # ExperienceLetters  = LETTEROFEXPERIENCEEmployeeDetail.objects.filter(OrganizationID=OrganizationID,IsDelete=False,emp_code= EC)
    # if  ExperienceLetters.count() >0:
    #     Experienceshow = 'Hide'

    ExperienceLetters = list(
        LETTEROFEXPERIENCEEmployeeDetail.objects
        .filter(OrganizationID=OrganizationID,IsDelete=False,emp_code=EC)
        .only(
            'id',
            'emp_code',
            'first_name',
            'last_name',
            'designation',
            'department',
            'file_name',
            'date_of_last_working'
        )
    )
    Experienceshow = 'Show' if not ExperienceLetters else 'Hide'
        
    # PromotionLetters  = PromotionLetterEmployeeDetail.objects.filter(OrganizationID=OrganizationID,IsDelete=False,emp_code=EC)
    # last_Promotion_id = None
    # if PromotionLetters.count() >0 :
    #    last_Promotion_id = PromotionLetters.aggregate(Max('id'))['id__max']
       
    PromotionLetters = list(
        PromotionLetterEmployeeDetail.objects
        .filter(OrganizationID=OrganizationID,IsDelete=False,emp_code=EC)
        .only(
            'id',
            'emp_code',
            'first_name',
            'last_name',
            'department',
            'designation',
            'date_of_promtion',
        )
    )

    last_Promotion_id = max(
        (obj.id for obj in PromotionLetters),
        default=None
    )
    # IncreamentLetters  = LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(OrganizationID=OrganizationID,IsDelete=False,emp_code= EC)
    # last_Increamen_id = None
    # if IncreamentLetters.count() >0 :
    #    last_Increamen_id = IncreamentLetters.aggregate(Max('id'))['id__max']
       
    IncreamentLetters = list(
        LETTEROFSALARYINCREAMENTEmployeeDetail.objects
        .filter(OrganizationID=OrganizationID,IsDelete=False,emp_code=EC)
        .only(
            'id',
            'emp_code',
            'first_name',
            'last_name',
            'department',
            'designation',
            'date_of_salary_increament',
        )
    )

    last_Increamen_id = max(
        (obj.id for obj in IncreamentLetters),
        default=None
    )

    # Revealingshow = 'Show'
    # RevealingLetters  = RevealingLetterEmployeeDetail.objects.filter(OrganizationID=OrganizationID,IsDelete=False,emp_code= EC)
    # if  RevealingLetters.count() >0:
    #     Revealingshow = 'Hide'
     

    RevealingLetters = list(
        RevealingLetterEmployeeDetail.objects
        .filter(OrganizationID=OrganizationID,IsDelete=False,emp_code= EC)
        .only(
            'id',
            'emp_code',
            'first_name',
            'last_name',
            'department',
            'designation',
        )
    )
    Revealingshow = 'Show' if not RevealingLetters else 'Hide'
        

    AdvanceSalary = list(
        AdvanceSalaryForm.objects
        .filter(OrganizationID=OrganizationID,is_delete=False,emp_code= EC)
        .only(
            'Application_Form_No',
            'EmpID',
            'emp_code',
            'EmployeeName',
            'Designation',
            'Department',
        )
    )
    AdvanceSalaryShow = 'Show' if not AdvanceSalary else 'Hide'
        
        
    #  New One
    Trainees_ExperienceLetters = list(
        Trainees_Experience_Employee_Detail.objects
        .filter(OrganizationID=OrganizationID, IsDelete=False, emp_code=EC)
        .only(
            'id',
            'emp_code',
            'first_name',
            'last_name',
            'designation',
            'department',
            'file_name',
            'date_of_last_working'
        )
    )
    Trainees_Experienceshow = 'Show' if not Trainees_ExperienceLetters else 'Hide'
        
        

    Data_Privacy = list(
        Data_Privacy_Employee_Detail.objects
        .filter(OrganizationID=OrganizationID, IsDelete=False, emp_code=EC)
        .only(
            'id',
            'emp_code',
            'first_name',
            'last_name',
            'designation',
            'department',
            'file_name',
            'date_of_last_working'
        )
    )
    Data_Privacy_Show = 'Show' if not Data_Privacy else 'Hide'
        

    Debit_Note = list(
        Debit_Note_Employee_Detail.objects
        .filter(OrganizationID=OrganizationID, IsDelete=False, emp_code=EC)
        .only(
            'id',
            'emp_code',
            'first_name',
            'last_name',
            'designation',
            'department',
            'file_name',
            'date_of_last_working'
        )
    )
    Debit_Note_Show = 'Show' if not Debit_Note else 'Hide'
        

    Policy_Posh = list(
        Policy_Posh_Employee_Detail.objects
        .filter(OrganizationID=OrganizationID, IsDelete=False, emp_code=EC)
        .only(
            'id',
            'emp_code',
            'first_name',
            'last_name',
            'designation',
            'department',
            'file_name',
            'date_of_last_working'
        )
    )
    Policy_Posh_Show = 'Show' if not Policy_Posh else 'Hide'
        
    Indemnity_Accommodation = list(
        Indemnity_Accommodation_Employee_Detail.objects
        .filter(OrganizationID=OrganizationID, IsDelete=False, emp_code=EC)
        .only(
            'id',
            'emp_code',
            'first_name',
            'last_name',
            'designation',
            'department',
            'file_name',
            'date_of_last_working'
        )
    )
    Indemnity_Accommodation_Show = 'Show' if not Indemnity_Accommodation else 'Hide'

    context = {
        'Emobj':Emobj,
        'EmpID':EmpID,
        'EC':EC,
        'AppointemetLetters':AppointemetLetters,
        'Succcess':Succcess,
        'ExperienceLetters':ExperienceLetters,
        'Trainees_ExperienceLetters':Trainees_ExperienceLetters,
        'last_Increamen_id':last_Increamen_id,
        'PromotionLetters':PromotionLetters,
        'last_Promotion_id':last_Promotion_id,
        'IncreamentLetters':IncreamentLetters,
        'RevealingLetters':RevealingLetters,
        'Appointemet':Appointemet,
        'OrganizationID':OrganizationID,
        'Experienceshow':Experienceshow,
        'Trainees_Experienceshow':Trainees_Experienceshow,
        'Data_Privacy_Show':Data_Privacy_Show,
        'Data_Privacy':Data_Privacy,
        'Debit_Note_Show':Debit_Note_Show,
        'Debit_Note':Debit_Note,
        'Policy_Posh_Show':Policy_Posh_Show,
        'Policy_Posh':Policy_Posh,
        'Indemnity_Accommodation_Show':Indemnity_Accommodation_Show,
        'Indemnity_Accommodation':Indemnity_Accommodation,
        'Revealingshow':Revealingshow, 
        'AdvanceSalary':AdvanceSalary,
        'AdvanceSalaryShow':AdvanceSalaryShow
    }
    return render(request, 'HR/EmployeeDashboard/EmployeeLetters.html', context)

from Warning_Letters.models import WarningMasterDetail,VerbalWarningmoduls,WrittenWarningModul,FinalWarningModule
def Warning_Letters(request):
    if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
          OrganizationID= OID
    UserID = str(request.session["UserID"])  
   
    encrypted_id = request.GET.get('EmpID')
    EmpID = decrypt_id(encrypted_id)
    Succcess = False
    Emobj    = None    
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
       
    verbal_warnings = VerbalWarningmoduls.objects.filter(OrganizationID=OrganizationID,IsDelete=False,emp_code= EC)
    written_warnings = WrittenWarningModul.objects.filter(OrganizationID=OrganizationID,IsDelete=False,employee_no= EC)
   
 
    FinalWarning = 'Show'      
    final_warnings = FinalWarningModule.objects.filter(OrganizationID=OrganizationID,IsDelete=False,employee_no= EC)
    if  final_warnings.count() >0:
          FinalWarning = 'Hide'  
         
    warnings = []
    for warning in verbal_warnings:
        warnings.append({
            'type': 'Verbal',
            'data': warning
        })
    for warning in written_warnings:
        warnings.append({
            'type': 'Written',
            'data': warning
        })
    for warning in final_warnings:
        warnings.append({
            'type': 'Final',
            'data': warning
        })
       
   
    context = {'Emobj':Emobj,'EmpID':EmpID,'EC':EC,'warnings':warnings,'Succcess':Succcess,'OrganizationID':OrganizationID,'FinalWarning':FinalWarning}
    return render(request, 'HR/EmployeeDashboard/Warning_Letters.html', context)
 





from Clearance_From.models import ClearenceEmp,ClearanceItemDetail
def Clearance_From(request):
    if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
          OrganizationID= OID
    UserID = str(request.session["UserID"])   
   
    encrypted_id = request.GET.get('EmpID')
    EmpID = decrypt_id(encrypted_id)
    Succcess = False
    Emobj    = None    
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode

    item_statuses = {}
    ClearanceFromdatashow = 'Show'       
   
    ClearanceFromdatas = ClearenceEmp.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpCode = EC)
    if  ClearanceFromdatas.count() >0:
          ClearanceFromdatashow = 'Hide'         
    for CF  in ClearanceFromdatas:
        item_statuses = {}
        for item in ClearanceItemDetail.objects.filter(IsDelete=False,OrganizationID = OrganizationID,ClearenceEmp=CF):
            emp_id = item.ClearenceEmp.id
            if emp_id not in item_statuses:
                item_statuses[emp_id] = {}
            item_statuses[emp_id][item.MasterClearanceItem.id] = item.ItemStatus
    context = {'Emobj':Emobj,'EmpID':EmpID,'EC':EC,'ClearanceFromdatas': ClearanceFromdatas,'Succcess':Succcess,'item_statuses':item_statuses,'ClearanceFromdatashow':ClearanceFromdatashow,'OrganizationID':OrganizationID}
    return render(request, 'HR/EmployeeDashboard/Clearance_From.html', context)

 
from ExitInterview.models import Exitinterviewdata
def ExitInterview(request):
    if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
          OrganizationID= OID
    UserID = str(request.session["UserID"])   
   
    encrypted_id = request.GET.get('EmpID')
    EmpID = decrypt_id(encrypted_id)
    Succcess = False
    Emobj    = None    
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
   
    exitinterviewshow = 'Show'       
    exitinterviews = Exitinterviewdata.objects.filter(IsDelete=False, OrganizationID=OrganizationID,Employee_Code=EC)
    if  exitinterviews.count() >0:
          exitinterviewshow = 'Hide'  
    context = {'Emobj':Emobj,'EmpID':EmpID,'EC':EC,'exitinterviews':exitinterviews,'Succcess':Succcess,'OrganizationID':OrganizationID,'exitinterviewshow':exitinterviewshow}
    return render(request, 'HR/EmployeeDashboard/ExitInterview.html', context)



from Job_Description.models import JobDescription
def JobDescriptions(request):
    if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
          OrganizationID= OID
   
    UserID = str(request.session["UserID"])  
   
    encrypted_id = request.GET.get('EmpID')
    EmpID = decrypt_id(encrypted_id)
    Succcess = False
    Emobj    = None    
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
        Ed  = Emobj.Designation
       
       
       
    joblists = JobDescription.objects.filter(IsDelete=False,Position=Ed)
    context = {'Emobj':Emobj,'EmpID':EmpID,'EC':EC,'joblists':joblists,'OrganizationID':OrganizationID}
    return render(request, 'HR/EmployeeDashboard/JobDescriptions.html', context)

from ProbationConfirmation.models import Emp_Confirmation_Master
from LetterOfConfirmation.models import LETTEROFCONFIRMATIONEmployeeDetail
def ProbationConfirmation(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
          OrganizationID= OID
    
     UserID = str(request.session["UserID"])   
   
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Succcess = False
     Emobj    = None    
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
        
     # Do not chagne this part   
     Emp_objs  = None   
     Emp_objshow = 'Show'   
     Emp_objs = Emp_Confirmation_Master.objects.filter(OrganizationID = OrganizationID,IsDelete=False,EmpCode=EC)
     for emp in Emp_objs:
          Cnf_Filename = None
          if emp.LOC_ID:
               Cnf_Filenameobj =  LETTEROFCONFIRMATIONEmployeeDetail.objects.filter(OrganizationID=OrganizationID, IsDelete=False,id=emp.LOC_ID).first()
               if Cnf_Filenameobj:
                    Cnf_Filename = Cnf_Filenameobj.file_name
          emp.Cnf_Filename = Cnf_Filename
          emp.save()          
                
     if  Emp_objs.count() >0:
          Emp_objshow = 'Hide'
     
     context = {'Emobj':Emobj,'EmpID':EmpID,'EC':EC,'Emp_objs':Emp_objs,'OrganizationID':OrganizationID,'Emp_objshow':Emp_objshow}
     return render(request, 'HR/EmployeeDashboard/ProbationConfirmation.html', context)





from EmpResignation.models import  EmpResigantionModel
def Resigantion(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID
    
     UserID = str(request.session["UserID"])   
   
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Succcess = False
     Emobj    = None    
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
        
     # Do not chagne this part   
     Resigantions  = None
     Resigantionshow = 'Show'   
     Resigantions = EmpResigantionModel.objects.filter(OrganizationID = OrganizationID,IsDelete=False,Emp_Code=EC)
     if  Resigantions.count() >0:
          Resigantionshow = 'Hide'
     context = {'Emobj':Emobj,'EmpID':EmpID,'EC':EC,'Resigantions':Resigantions,'OrganizationID':OrganizationID,'Resigantionshow':Resigantionshow}
     return render(request, 'HR/EmployeeDashboard/Resigantion.html', context)






from EmpTermination.models import EmpTerminationModel
def Termination(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID
     UserID = str(request.session["UserID"])   
   
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Succcess = False
     Emobj    = None    
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
        
     # Do not chagne this part   
     Terminations  = None   
     Terminationshow = 'Show'   
     Terminations = EmpTerminationModel.objects.filter(OrganizationID = OrganizationID,IsDelete=False,Emp_Code=EC)
     if  Terminations.count() >0:
          Terminationshow = 'Hide'
     context = {'Emobj':Emobj,'EmpID':EmpID,'EC':EC,'Terminations':Terminations,'OrganizationID':OrganizationID,'Terminationshow':Terminationshow}
     return render(request, 'HR/EmployeeDashboard/Termination.html', context)









# from EmpAbsconding.models import EmpAbscondingModel
# def Absconding(request):
#      if 'OrganizationID' not in request.session:
#          return redirect(MasterAttribute.Host)
#      else:
#         print("Show Page Session")
#      OrganizationID = request.session["OrganizationID"]
#      UserID = str(request.session["UserID"])   
   
#      encrypted_id = request.GET.get('EmpID')
#      EmpID = decrypt_id(encrypted_id)
#      Succcess = False
#      Emobj    = None    
#      if EmpID:
#         Emobj = EmployeeCardDetails(EmpID,OrganizationID)
#         EC  = Emobj.EmployeeCode
        
#      Abscondings  = None   
#      Abscondings = EmpAbscondingModel.objects.filter(OrganizationID = OrganizationID,IsDelete=False,Emp_Code=EC)
#      context = {'Emobj':Emobj,'EmpID':EmpID,'EC':EC,'Abscondings':Abscondings}
#      return render(request, 'HR/EmployeeDashboard/Absconding.html', context)

from EmpAbsconding.models import EmpAbscondingModel,Empshowcausenotice
def Absconding(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID
     UserID = str(request.session["UserID"])  
   
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     EC = None
     Succcess = False
     Emobj    = None  
     AbscondingRevoke = 'Hide'

     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode

        if Emobj:
            if Emobj.EmpStatus == "Absconding":
                AbscondingRevoke = 'Show'
            else:
                AbscondingRevoke = 'Hide'
        else:
            print("Emobj is not found ")
     else:
        print("EmpID is not found ")
          
     Notices  = None  
     Abscondingshow = 'Show'   
     Abscondings = EmpAbscondingModel.objects.filter(OrganizationID = OrganizationID,IsDelete=False,Emp_Code=EC)
     if  Abscondings.count() >0:
          Abscondingshow = 'Hide'
     Noticeshow = 'Show'   
     Notices = Empshowcausenotice.objects.filter(OrganizationID = OrganizationID,IsDelete=False,Emp_Code=EC)
     if  Notices.count() >0:
          Noticeshow = 'Hide'
 
     context = {
        'Emobj':Emobj,
        'EmpID':EmpID,
        'EC':EC,
        'Abscondings':Abscondings,
        'Notices':Notices,
        'OrganizationID':OrganizationID,
        'Noticeshow':Noticeshow,
        'Abscondingshow':Abscondingshow,
        'AbscondingRevoke':AbscondingRevoke
        }
     return render(request, 'HR/EmployeeDashboard/Absconding.html', context)



# Absconding_Revoke_View
def Absconding_Revoke_View(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    User_OrganizationID = request.GET.get('OID')
    EmployeeCode = request.GET.get('EC')  # corrected

    # print("EmployeeCode::", EmployeeCode)
    

    if User_OrganizationID:
        OrganizationID = User_OrganizationID

    EmpID = request.GET.get('EmpID')
    # print("encrypted_id", EmpID)
    # EmpID = decrypt_id(encrypted_id)
    # print("decrypt_id", EmpID)
    Success = False  # corrected spelling
    PersonalObj = None
    Workobj = None

    if EmpID:
        PersonalObj = EmployeePersonalDetails.objects.filter(
            OrganizationID=OrganizationID, IsDelete=False, IsEmployeeCreated=True,
            EmpID=EmpID, EmployeeCode=EmployeeCode
        ).only("EmpID").first()

        print("PersonalObj id", PersonalObj)

    if PersonalObj and PersonalObj.EmpID:
        Workobj = EmployeeWorkDetails.objects.filter(
            OrganizationID=OrganizationID, IsDelete=False, IsSecondary=False,
            EmpID=PersonalObj.EmpID
        ).only("EmpStatus").first()

        CurrentStatus = Workobj.EmpStatus

        # print("Workobj status::", Workobj)

        if EmployeeCode:
            Absconding_Obj = EmpAbscondingModel.objects.filter(
                OrganizationID=OrganizationID, IsDelete=False,
                Emp_Code=EmployeeCode
            ).only("LastEmpStatus").first()

            # print("Absconding_Obj LastEmpStatus", Absconding_Obj)

            if Absconding_Obj and Workobj:
                try:
                    Workobj.EmpStatus = Absconding_Obj.LastEmpStatus
                    Workobj.save()

                    params = {
                        'EmpID':encrypt_id(EmpID),
                        'OID':User_OrganizationID,
                        'Success': "True",
                        'message': f"Employee status changed successfuly from '{CurrentStatus}' to '{Workobj.EmpStatus}' !"
                    }
                    url = f"{reverse('Absconding')}?{urlencode(params)}"
                    return redirect(url)
                except Exception as e:
                    print("Failed to Change Status:", str(e))

    params = {
        'EmpID':encrypt_id(EmpID),
        'OID':User_OrganizationID,
        'Success': "True",
        'message': "Faild To change Employee status!"
    }
    url = f"{reverse('Absconding')}?{urlencode(params)}"
    return redirect(url)
    # encrypted_id = encrypt_id(EmpID)
    # url = reverse('Absconding')
    # redirect_url = f"{url}?EmpID={encrypted_id}?&OID={OrganizationID}&Success={Success}"
    # redirect_url = f"{url}?EmpID={encrypted_id}&OID={User_OrganizationID}&OID={User_OrganizationID}&Success={Success}"
    # redirect_url = f"{url}?EmpID={encrypted_id}&OID={User_OrganizationID}&OID={User_OrganizationID}&Success={Success}" 
    # return redirect(redirect_url)


from IT.models import ItInformation,SimDetail,EmailDetail,SystemDetail,MobileDetail
def IT(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID
     UserID = str(request.session["UserID"])   
   
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Succcess = False
     Emobj    = None    
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
        
        
    
     its = ItInformation.objects.filter(OrganizationID=OrganizationID, IsDelete=False,EmployeeCode=EC).order_by('-id')

  
     its_with_issued_status = []
     for it in its:
        sim_issued = SimDetail.objects.filter(ItInformation=it, IsIssued=True,OrganizationID=OrganizationID, IsDelete=False).exists()
        mobile_issued = MobileDetail.objects.filter(ItInformation=it, IsIssued=True,OrganizationID=OrganizationID, IsDelete=False).exists()
        email_issued = EmailDetail.objects.filter(ItInformation=it, IsIssued=True,OrganizationID=OrganizationID, IsDelete=False).exists()
        system_issued = SystemDetail.objects.filter(ItInformation=it, IsIssued=True,OrganizationID=OrganizationID, IsDelete=False).exists()
        
        its_with_issued_status.append({
            'it': it,
            'sim_issued': 'Issued' if sim_issued else 'Not Issued',
            'mobile_issued': 'Issued' if mobile_issued else 'Not Issued',
            'email_issued': 'Issued' if email_issued else 'Not Issued',
            'system_issued': 'Issued' if system_issued else 'Not Issued',
        })
    
 
     context = {'Emobj':Emobj,'EmpID':EmpID,'EC':EC,'ITS': its_with_issued_status,'OrganizationID':OrganizationID}
     return render(request, 'HR/EmployeeDashboard/IT.html', context)







from UniformInventory.models import UniformInformation
def Uniform(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID
     UserID = str(request.session["UserID"])   
   
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Succcess = False
     Emobj    = None    
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
        
   
    
     UNI = None
     UNIshow = 'Show'   
     UNI = UniformInformation.objects.filter(EmployeeCode=EC,OrganizationID =OrganizationID ,IsDelete=False)
     if  UNI.count() >0:
          UNIshow = 'Hide'  

    
          
     context = {'Emobj':Emobj,'EmpID':EmpID,'EC':EC,'UNI':UNI,'OrganizationID':OrganizationID,'UNIshow':UNIshow}
     return render(request, 'HR/EmployeeDashboard/Uniform.html', context)



from FullandFinalSettlement.models import Full_and_Final_Settltment
def FullandFinal(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID
     UserID = str(request.session["UserID"])   
   
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Succcess = False
     Emobj    = None    
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
        
   
    
     
     FIN = Full_and_Final_Settltment.objects.filter(Emp_Code=EC,OrganizationID =OrganizationID ,IsDelete=False)  
     context = {'Emobj':Emobj,'EmpID':EmpID,'EC':EC,'FIN':FIN,'OrganizationID':OrganizationID}
     return render(request, 'HR/EmployeeDashboard/FullandFinal.html', context)






def PADP(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID
     UserID = str(request.session["UserID"])   
   
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Succcess = False
     Emobj    = None    
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
        
   
    
     
     
     context = {'Emobj':Emobj,'EmpID':EmpID,'EC':EC,'OrganizationID':OrganizationID}
     return render(request, 'HR/EmployeeDashboard/PADP.html', context)






def Checklist(request):
    if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID = str(request.session["UserID"])  
   
    encrypted_id = request.GET.get('EmpID')
    EmpID = decrypt_id(encrypted_id)
    Succcess = False
    Emobj    = None    
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
       
       
    checkempdata = HREmployeeChecklist_Entry.objects.filter(OrganizationID=OrganizationID, IsDelete=False, EmpCode=EC)
    IsShow = 'Yes' if checkempdata.exists() else 'No'
 
     
    context = {'Emobj':Emobj,'EmpID':EmpID,'EC':EC,'checkempdata':checkempdata,'Succcess':Succcess,'IsShow':IsShow,'OrganizationID':OrganizationID}
    return render(request, 'HR/EmployeeDashboard/Checklist.html', context)
 
 
 
from CodeOfConduct.models import EmpCodeofConductDocMaster,Docmaster
def CodeConduct(request):
    if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID = str(request.session["UserID"])  
   
    encrypted_id = request.GET.get('EmpID')
    EmpID = decrypt_id(encrypted_id)
    Succcess = False
    Emobj    = None    
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
       
       
    codeconductsadd = 'Show'  
    codeconducts = EmpCodeofConductDocMaster.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Empcode=EC)
    if  codeconducts.count() >0:
          codeconductsadd = 'Hide'
   
    docs = Docmaster.objects.all()
    context = {'Emobj':Emobj,'EmpID':EmpID,'EC':EC,'codeconducts':codeconducts,'Succcess':Succcess,'docs':docs,'OrganizationID':OrganizationID,'codeconductsadd':codeconductsadd}
    return render(request, 'HR/EmployeeDashboard/CodeConduct.html', context)
 





from django.shortcuts import get_object_or_404
from django.http import HttpResponse
 
from django.template.loader import get_template
from xhtml2pdf import pisa  
 
def generate_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
from datetime import datetime
from django.utils import timezone  
from app.models import OrganizationMaster
from UniformInventory.models import UniformDetails
from Checklist_Issued.models import HREmployeeChecklistMaster,HREmployeeChecklist_Entry,HREmployeeChecklist_Details
def EmpView(request):
    if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID = str(request.session["UserID"])  
   
    organization_logos = None
    current_datetime = None
    Emppersonal = None
    empaddress = None
    empIdentity = None
    empqualifications = None
    emppreviouswork = None
    empworkdata = None
    organization_logo = None
    empbankdata = None
    SalaryTitles = None
    empfamily = None
    empchilddata = None
    empemergencydata = None
    warnings = None
    UnDetails = None
    checkemps = None
    Emp_objs = None
    PRIMG = None
    Emp_objspromotions = None
    LeaveTypes = None
 
    encrypted_id = request.GET.get('EmpID')
    EmpID = decrypt_id(encrypted_id)
 
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
   
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
    organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
 
    Emppersonal = EmployeePersonalDetails.objects.filter(
        OrganizationID=OrganizationID, IsDelete=False, EmpID=EmpID
    ).first()
    if Emppersonal:
         PRIMG  = f'{MasterAttribute.Host}/HumanResources/Humanview_file/?ID={Emppersonal.EmpID}&model=EmployeePersonalDetails'
 
   
    empaddress=EmployeeAddressInformationDetails.objects.filter(
        OrganizationID=OrganizationID, IsDelete=False, EmpID=EmpID
    ).first()
   
    empIdentity=EmployeeIdentityInformationDetails.objects.filter(
        OrganizationID=OrganizationID, IsDelete=False, EmpID=EmpID
    ).first()
   
    empqualifications = EmployeeQualificationDetails.objects.filter(
        OrganizationID=OrganizationID, IsDelete=False, EmpID=EmpID
    )
 
    emppreviouswork=EmployeePreviousWorkInformationDetails.objects.filter(
        OrganizationID=OrganizationID, IsDelete=False, EmpID=EmpID
    )
 
    empworkdata = EmployeeWorkDetails.objects.filter(
        OrganizationID=OrganizationID, IsDelete=False, EmpID=EmpID,IsSecondary=False
    ).first()
 
    empbankdata=EmployeeBankInformationDetails.objects.filter(
        OrganizationID=OrganizationID, IsDelete=False, EmpID=EmpID
    ).first()
 
 
    empfamily=EmployeeFamilyDetails.objects.filter(
        OrganizationID=OrganizationID, IsDelete=False, EmpID=EmpID
    ).first()
    if empfamily:
        empchilddata=EmployeeChildDetails.objects.filter(
            OrganizationID=OrganizationID, IsDelete=False, FamilyID=empfamily.id
        )
 
    if EmpID:
        SalaryTitles  = SalaryTitle_Master.objects.filter(IsDelete=False, OrganizationID=OrganizationID).order_by('TypeOrder','TitleOrder')
        for salary in SalaryTitles:
            salary.Permonth = 0
            salary.Perannum = 0
            SC = Salary_Detail_Master.objects.filter(IsDelete=False,EmpID=EmpID, Salary_title_id = salary.id,OrganizationID=OrganizationID)
            if SC.exists():
                    salary.Permonth = SC[0].Permonth
                    salary.Perannum = SC[0].Perannum
 
    empemergencydata=EmployeeEmergencyInformationDetails.objects.filter(
        OrganizationID=OrganizationID, IsDelete=False, EmpID=EmpID
    ).first()
   
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
       
    verbal_warnings = VerbalWarningmoduls.objects.filter(OrganizationID=OrganizationID,IsDelete=False,emp_code= EC)
    written_warnings = WrittenWarningModul.objects.filter(OrganizationID=OrganizationID,IsDelete=False,employee_no= EC)
    final_warnings = FinalWarningModule.objects.filter(OrganizationID=OrganizationID,IsDelete=False,employee_no= EC)
   
    warnings = []
    for warning in verbal_warnings:
        warnings.append({
            'type': 'Verbal',
            'data': warning
        })
    for warning in written_warnings:
        warnings.append({
            'type': 'Written',
            'data': warning
        })
    for warning in final_warnings:
        warnings.append({
            'type': 'Final',
            'data': warning
        })
       
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID, OrganizationID)
        EC = Emobj.EmployeeCode if Emobj else None  # Safeguard if Emobj is None
       
    UNI = UniformInformation.objects.filter(
        EmployeeCode=EC, OrganizationID=OrganizationID, IsDelete=False
    ).first()  # Use .first() to get a Unmarried object
 
    UnDetails = []
    if UNI:  # Check if UNI exists
        UnDetails = UniformDetails.objects.filter(
            UniformInformation=UNI, OrganizationID=OrganizationID, IsDelete=False
        )
 
    checkemps = HREmployeeChecklistMaster.objects.filter(IsDelete=False)
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID, OrganizationID)
        EC = Emobj.EmployeeCode if Emobj else None
        try:
            checkemp = HREmployeeChecklist_Entry.objects.get(
                EmpCode=EC, OrganizationID=OrganizationID, IsDelete=False
            )
 
            for cl in checkemps:
                cl.ReceivedStatus = 0
                clearance_items = HREmployeeChecklist_Details.objects.filter(
                    HREmployeeChecklist_Entry=checkemp, HREmployeeChecklistMaster=cl
                )
                if clearance_items.exists():
                    cl.ReceivedStatus = clearance_items[0].ReceivedStatus
        except HREmployeeChecklist_Entry.DoesNotExist:
            checkemp = None
    else:
        checkemps = []
 
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
       
     # Do not chagne this part  
    Emp_objs  = None  
    Emp_objs = Emp_Confirmation_Master.objects.filter(OrganizationID = OrganizationID,IsDelete=False,EmpCode=EC).first()  
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
       
     # Do not chagne this part  
    Emp_objspromotions  = None  
    Emp_objspromotions = PromotionLetterEmployeeDetail.objects.filter(OrganizationID = OrganizationID,IsDelete=False,emp_code=EC).first()
   
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID, OrganizationID)
        LeaveTypes = Leave_Type_Master.objects.filter(IsDelete=False)
        for Leave in LeaveTypes:
            Leave.Balance = 0
            if Emobj:
                LT = Emp_Leave_Balance_Master.objects.filter(
                    OrganizationID=OrganizationID, CreatedBy=UserID,
                    Leave_Type_Master_id=Leave.id, Emp_code=Emobj.EmployeeCode)
                if LT.exists():
                    Leave.Balance = LT[0].Balance
   
    EmpHistroy = EmployeeDetailHistroy(EmpID, OrganizationID, EC)
    if EmpHistroy:
        Salaryhis = EmpHistroy['Salaryhis']
        Designationhis = EmpHistroy['Designationhis']
        Appointment  =  EmpHistroy['Appointment']
        SalaryIncreament  = EmpHistroy['SalaryIncreament']
        Confirmation  = EmpHistroy['Confirmation']
        Promotion  = EmpHistroy['Promotion']
        tenure_till_today = EmpHistroy['tenure_till_today']

   
    context = {
       
        'organization_logos':organization_logos,
        'current_datetime':current_datetime,
         'Leave_datetime': datetime.now().strftime('%d-%m-%Y'),
        'Emppersonal':Emppersonal,
       
        'empaddress':empaddress,
        'empIdentity':empIdentity,
        'empqualifications':empqualifications,
        'emppreviouswork':emppreviouswork,
        'empworkdata':empworkdata,
        'organization_logo':organization_logo,
        'empbankdata':empbankdata,
        'SalaryTitles':SalaryTitles,
        'empfamily':empfamily,
        'empchilddata':empchilddata,
        'empemergencydata':empemergencydata,
        'warnings':warnings,
        'UnDetails':UnDetails,
        'checkemps':checkemps,
        'Emp_objs':Emp_objs,
        'PRIMG':PRIMG,
        'Emp_objspromotions':Emp_objspromotions,
        'LeaveTypes':LeaveTypes,
        'Designationhis':Designationhis,'Salaryhis':Salaryhis,'SalaryIncreament':SalaryIncreament,'Confirmation':Confirmation,'Appointment':Appointment,'Promotion':Promotion,'tenure_till_today':tenure_till_today
 
    }
 
   
    return generate_pdf( 'HR/EmpView.html',context)
     


from app.views import OrganizationList


def DataMissingReport(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    memOrg  = OrganizationList(OrganizationID)
     
    # if OrganizationID == 3:
    #     memOrg = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1).values(
    #         'OrganizationID', 'OrganizationName', 'OrganizationDomainCode', 'ShortDisplayLabel'
    #     )
    # else:
    #     memOrg = OrganizationMaster.objects.filter(
    #         OrganizationID=OrganizationID, IsDelete=False, Activation_status=1
    #     ).values(
    #         'OrganizationID', 'OrganizationName', 'OrganizationDomainCode', 'ShortDisplayLabel'
    #     )
 
    
   
    Departments = OnRollDepartmentMaster.objects.filter(IsDelete=False).order_by('DepartmentName')
 
   
    selected_org_id = request.GET.get("OrganizationID",OrganizationID)
   
    selected_department = request.GET.get("Department","AllDepartment")
 
    
    # Fetch Employee Personal Details with incomplete profiles and a valid EmpStatus
    Empobjs = EmployeePersonalDetails.objects.filter(
        IsDelete=False, 
        OrganizationID=selected_org_id, 
        IsEmployeeCreated=True, 
        ProfileCompletion__lt=100
    ).values(
        'EmpID', 'EmployeeCode', 'Prefix', 'FirstName', 'MiddleName', 'LastName',
        'Gender', 'MobileNumber', 'ProfileImageFileName', 'CovidVaccination', 'DetailsofIllness',
        'ProfileCompletion', 'MissingFields'
    )

   
    work_details = EmployeeWorkDetails.objects.filter(
        IsDelete=False,IsSecondary=False,
        OrganizationID=selected_org_id, 
        EmpStatus__in=["On Probation", "Not Confirmed", "Confirmed"]
    ).values(
        'EmpID', 'Designation', 'Department', 'DateofJoining', 'EmpStatus'
    )

    if selected_department and selected_department != "AllDepartment":
        work_details = work_details.filter(Department=selected_department)
 

  
    work_details_dict = {wd['EmpID']: wd for wd in work_details}

  
    combined_Empobj_data = [
        {
            **emp,
            'Department': work_details_dict.get(emp['EmpID'], {}).get('Department', 'N/A'),
            'Designation': work_details_dict.get(emp['EmpID'], {}).get('Designation', 'N/A'),
            'DateofJoining': work_details_dict.get(emp['EmpID'], {}).get('DateofJoining', 'N/A'),
            'EmpStatus': work_details_dict.get(emp['EmpID'], {}).get('EmpStatus', 'N/A'),
        }
        for emp in Empobjs if emp['EmpID'] in work_details_dict
    ]

   
    context = {
        'Empobjs': combined_Empobj_data,'memOrg':memOrg,'Departments':Departments,'selected_department':selected_department,'selected_org_id':selected_org_id
    }

    return render(request, 'HR/DataMissingReport.html', context)






def KraReport(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID
     UserID = str(request.session["UserID"])   
   
     encrypted_id = request.GET.get('EmpID')
     EmpID = decrypt_id(encrypted_id)
     Succcess = False
     Emobj    = None    
     if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OrganizationID)
        EC  = Emobj.EmployeeCode
     
     current_year = datetime.now().year
     years = [current_year + 1, current_year, current_year - 1, current_year - 2, current_year - 3]
     selected_year = int(request.GET.get('year', current_year))
    
     with connection.cursor() as cursor:
            cursor.execute("EXEC sp_GetKraYearlyReport @OrganizationID=%s,  @EmployeeCode = %s, @SelectedYear=%s", [ OrganizationID , EC, selected_year])
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
     rowslist = [dict(zip(columns, row)) for row in rows]

     context = {
        'years': years,
        'selected_year': selected_year,
        'Emobj':Emobj,
        'EmpID':EmpID,'EC':EC,
        'rowslist': rowslist,
        'OrganizationID':OrganizationID
     }
    
     return render(request, 'HR/EmployeeDashboard/KraReport.html', context)





from urllib.parse import urlencode
def Change_Reporting_To(request):
    if 'OrganizationID' not in request.session or 'UserID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    SessionOrganizationID = int(OrganizationID)
    UserID = request.session.get("UserID")

    SessionDepartment = request.session.get("Department_Name")
    # print("SessionDepartment", SessionDepartment)

    memOrg = OrganizationList(OrganizationID)

    Departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    # Designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    DottedLineDesignations = CorporateDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    MergedReportingtoDesignation = chain(Designations, DottedLineDesignations)

    SelectedDepartment = request.GET.get('Department')
    SelectedDesignation = request.GET.get('Designation')

    # Organizaton ------>
    
    # Get selected organization from query param
    SelectedOrganizationID_str = request.GET.get('OrganizationID', OrganizationID)
    SelectedOrganizationID = int(SelectedOrganizationID_str) if SelectedOrganizationID_str != 'All' else None

    # Filter organization options based on session org
    if SessionOrganizationID == 3:
        orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1)
        work_details = EmployeeWorkDetails.objects.filter(
            IsDelete=False, 
            IsSecondary=False, 
            EmpStatus__in=["Confirmed","Not Confirmed","On Probation"]
        )
    else:
        orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1, OrganizationID=SessionOrganizationID)
        work_details = EmployeeWorkDetails.objects.filter(
            OrganizationID=SessionOrganizationID,
            IsDelete=False, 
            IsSecondary=False, 
            EmpStatus__in=["Confirmed","Not Confirmed","On Probation"]
        )

    if SelectedOrganizationID is not None:
        work_details = work_details.filter(OrganizationID=SelectedOrganizationID)
    else:
        work_details = work_details.filter(OrganizationID=SessionOrganizationID)

    # if SelectedOrganizationID is not None:
    #     work_details = work_details.filter(OrganizationID=SelectedOrganizationID)

    if SelectedDepartment is not None:
        work_details = work_details.filter(Department=SelectedDepartment)
        department_id = Departments.filter(DepartmentName=SelectedDepartment).values_list('id', flat=True).first()
        print("department_id",department_id)
        if department_id:
            Designations = Designations.filter(OnRollDepartmentMaster=department_id)


    if SelectedDesignation is not None:
        work_details = work_details.filter(ReportingtoDesignation=SelectedDesignation)


    employee_data = []
    for work in work_details:
        personal_details = EmployeePersonalDetails.objects.filter(EmpID=work.EmpID).first()
        employee_data.append({
            'EmpID': work.EmpID,
            'EmpStatus': work.EmpStatus,
            'Level': work.Level,
            'Designation': work.Designation,
            'Department': work.Department,
            'ReportingtoDesignation': work.ReportingtoDesignation,

            'EmployeeCode': personal_details.EmployeeCode if personal_details else None,
            'FirstName': personal_details.FirstName if personal_details else None,
            'MiddleName': personal_details.MiddleName if personal_details else None,
            'LastName': personal_details.LastName if personal_details else None,

            'personal_OrganizationID': personal_details.OrganizationID if personal_details else None,
            'work_OrganizationID': work.OrganizationID if work else None,
        })

    if request.method == "POST":
        ReportingtoDesignation = request.POST.get('ReportingToDesignation')
        ReportingtoDepartment = request.POST.get('ReportingToDesignationDepartment')
        ReportingtoLevel = request.POST.get('ReportingToDesignationLevel')

        selected_employees = request.POST.getlist('all_emp_codes[]')

        for emp in selected_employees:
            employee_code, emp_id, emp_organization = emp.split('|')

            # You can now use emp_id to update each employee's reporting fields
            work_record = EmployeeWorkDetails.objects.filter(EmpID=emp_id, IsDelete=False, OrganizationID=emp_organization).first()
            if work_record:
                work_record.ReportingtoDesignation = ReportingtoDesignation
                work_record.ReportingtoDepartment = ReportingtoDepartment
                work_record.ReportingtoLevel = ReportingtoLevel
                work_record.save()
        
        # if ReportingtoDepartment is not None:
        #     Reporting_Department_Id = Departments.filter(DepartmentName=ReportingtoDepartment).values_list('id', flat=True).first()
        #     if department_id:
        #         Reporting_Designations = Designations.filter(OnRollDepartmentMaster=department_id)

        params = {
            'OrganizationID':SelectedOrganizationID,
            'Department':ReportingtoDepartment,
            'Designation':ReportingtoDesignation,
            # 'Department':Reporting_Department_Id,
            # 'Designation':Reporting_Designations,
            'Success': 'True',
            'message': 'Reporting To is updated successfully!'
        }
        url = f"{reverse('Change_Reporting_To')}?{urlencode(params)}"
        return redirect(url)



    # print("reporting_person_data::",reporting_person_data)
    context = {
        'memOrg': memOrg,
        'Departments': Departments,
        'Designations': Designations,
        # 'Lavelsdatas': Lavelsdatas,
        
        'OrganizationID': OrganizationID,
        'work_details': work_details,
        'employee_data': employee_data,
        'SelectedDepartment':SelectedDepartment,
        'SelectedDesignation':SelectedDesignation,

        # 'reporting_person_data': reporting_person_data,

        'MergedReportingtoDesignation': MergedReportingtoDesignation,

        # Ogranization Dropdown
        'SessionOrganizationID': SessionOrganizationID,  # Correct
        'orgs': orgs,
        'selectedOrganizationID': SelectedOrganizationID_str,  # String to match dropdown value
    }

    return render(request, 'HR/Change_Reporting/Change_Reporting_To.html', context)










# ------------------------ New Salary System


# def  SalaryDetails_Settlement.html(request):
# def  Salary_Details_Settlement(request,EmpID,OID):

#     UserID = str(request.session["UserID"])   

#     if EmpID is None and OID is None:
#         print("provide the EmpID and OID first")
#     # EmpID = decrypt_id(encrypted_id)

#     print("the OID is here", OID)
#     print("the EmpID is here", EmpID)

#     EmpID = 7656
#     Success  =  False
#     Emobj    = None  
       
#     if EmpID:
#         Emobj = EmployeeCardDetails(EmpID,OID)
#         SalaryTitles  = SalaryTitle_Master.objects.filter(IsDelete=False, HotelID=OID).order_by('TypeOrder','TitleOrder')


#     if request.method == "POST":
#         # Soft delete old salary rows
#         SC = Salary_Detail_Master.objects.filter(
#             IsDelete=False, EmpID=EmpID, OrganizationID=OID
#         )
#         for s in SC:
#             s.IsDelete = True
#             s.ModifyBy = UserID
#             s.save()

#         Total_Title = int(request.POST['Total_Title'])
#         effective_from = request.POST.get("EffectiveFrom")

#         total_ctc = 0

#         # 1Create Effective record first
#         effective_record = Salary_Details_Effective.objects.create(
#             EmpID=EmpID,
#             EffectiveFrom=effective_from,
#             CTC="0",  # temporary, will update after loop
#             OrganizationID=OID,
#             CreatedBy=UserID
#         )

#         # 2Create salary rows linked to effective record
#         for i in range(Total_Title + 1):
#             TitleID = request.POST[f'TitleID_{i}']
#             Permonth = request.POST[f'Permonth_{i}']
#             Perannum = request.POST[f'Perannum_{i}']

#             # accumulate total for CTC
#             try:
#                 total_ctc += float(Perannum)
#             except:
#                 pass

#             Salary_Detail_Master.objects.create(
#                 EmpID=EmpID,
#                 Salary_title_id=TitleID,
#                 Permonth=Permonth,
#                 Perannum=Perannum,
#                 Effective=effective_record,   # link here
#                 OrganizationID=OID,
#                 CreatedBy=UserID
#             )

#         # 3 Update CTC inside Effective record
#         effective_record.CTC = str(total_ctc)
#         effective_record.save()

#         # (optional) also call your existing UpdateCTC if it handles more things
#         # UpdateCTC(EmpID, OID, UserID)

#         Success = True
#         encrypted_id = encrypt_id(EmpID)
#         url = reverse('SalaryDetailsPage')
#         redirect_url = f"{url}?EmpID={encrypted_id}&OID={OID}&Success={Success}"
#         return redirect(redirect_url)
  

#     context = {
#         'Emobj':Emobj,
#         'EmpID':EmpID,
#         'Success':Success, 
#         'SalaryTitles':SalaryTitles,
#         'OrganizationID':OID
#     }
#     return render(request, 'HR/EmployeeDashboard/SalaryDetails_Settlement.html', context)



from django.utils import timezone
from django.db import transaction
from django.shortcuts import render, redirect
from .models import Salary_Details_Effective, Salary_Detail_Master, SalaryTitle_Master
from datetime import date

@transaction.atomic
def Salary_Details_Settlement(request,EmpID,OID):
    Session_Org_ID = request.session["OrganizationID"] or 0
    userID = request.session["UserID"] or 0

    if not OID:
        OID = Session_Org_ID

    # EmpID = 6321  
    if not EmpID:
        return HttpResponse("No Employee Id found")

    if request.method == "POST":
        effective_from = request.POST.get("EffectiveFrom")

        # Create Effective record first
        effective_obj = Salary_Details_Effective.objects.create(
            EmpID=EmpID,
            EffectiveFrom=effective_from,
            CTC="0",  # You can calculate CTC after inserting masters
            OrganizationID=OID,
            CreatedBy=userID,
        )

        total_titles = int(request.POST.get("Total_Title", -1)) + 1

        for i in range(total_titles):
            title_id = request.POST.get(f"TitleID_{i}")
            permonth = request.POST.get(f"Permonth_{i}", 0) or 0
            perannum = request.POST.get(f"Perannum_{i}", 0) or 0

            if title_id:
                Salary_Detail_Master.objects.create(
                    EmpID=EmpID,
                    Salary_title_id=title_id,
                    Permonth=permonth,
                    Perannum=perannum,
                    Effective=effective_obj,  
                    OrganizationID=OID,
                    CreatedBy=userID,
                )

        # Optionally update effective_obj.CTC = total salary
        ctc_title = SalaryTitle_Master.objects.filter(
            Title="CTC (A+C)", IsDelete=False, OrganizationID=OID
        ).first() 
        
        if ctc_title:
            # Step 2: Get the Salary_Detail_Master for this effective and CTC title
            ctc_detail = Salary_Detail_Master.objects.filter(
                Effective=effective_obj,
                Salary_title=ctc_title
            ).first()

            # Step 3: Store the Perannum value into effective_obj.CTC
            if ctc_detail:
                effective_obj.CTC = ctc_detail.Permonth
                effective_obj.save()

        encrypted_id = encrypt_id(EmpID)
        url = reverse('SalaryDetailsPage')
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OID}"
        return redirect(redirect_url)
        # return redirect("some-success-page")  # or render success template

    Emobj = None  

       
    if EmpID:
        Emobj = EmployeeCardDetails(EmpID,OID)
        SalaryTitles  = SalaryTitle_Master.objects.filter(IsDelete=False, OrganizationID=OID).order_by('TypeOrder','TitleOrder')
        print("SalaryTitles obj::,",SalaryTitles)


    current_date = date.today().strftime("%Y-%m-%d")
    # print(current_date)  # Output: 2025-10-04 (YYYY-MM-DD)
    context = {
        'Emobj':Emobj,
        'EmpID':EmpID,
        # 'Success':Success, 
        'SalaryTitles':SalaryTitles,
        'OrganizationID':OID,
        'current_date':current_date
    }
    return render(request, "HR/EmployeeDashboard/SalaryDetails_Settlement.html", context)




@transaction.atomic
def Update_Salary_Details_Settlement(request, EmpID, OID, SettleID):
    Session_Org_ID = request.session["OrganizationID"]
    userID = 1
    if not OID:
        OID = Session_Org_ID

    if not EmpID:
        return redirect("SalaryDetailsPage")

    if request.method == "POST":
        effective_from = request.POST.get("EffectiveFrom")
        effective_id = request.POST.get("EffectiveID")  

        # Get existing Effective object
        # print("Before effective_obj")
        # effective_obj = get_object_or_404(Salary_Details_Effective, id=effective_id)
        effective_obj = Salary_Details_Effective.objects.get(
            id=effective_id,
            IsDelete=False
        )
        # print("After effective_obj")
        

        # Update Effective object
        effective_obj.EffectiveFrom = effective_from
        effective_obj.ModifiedBy = userID
        effective_obj.save()
        
        # print("Before For loop at salary details")

        total_titles = int(request.POST.get("Total_Title", -1)) + 1

        for i in range(total_titles):
            title_id = request.POST.get(f"TitleID_{i}")
            permonth = request.POST.get(f"Permonth_{i}", 0) or 0
            perannum = request.POST.get(f"Perannum_{i}", 0) or 0
            
            # print(f"-- Title_ID:{title_id}, -- permonth: {permonth}, -- perannum:{perannum}")

            if title_id:
                # fetch existing salary detail 
                detail = Salary_Detail_Master.objects.filter(
                    EmpID=EmpID,
                    Salary_title_id=title_id,
                    Effective=effective_obj,
                    OrganizationID=OID,
                    IsDelete=False
                ).first()

                if not detail:
                    detail = Salary_Detail_Master.objects.create(
                        EmpID=EmpID,
                        Salary_title_id=title_id,
                        Effective=effective_obj,
                        OrganizationID=OID,
                        CreatedBy=userID,
                        IsDelete=False
                    )


                # Update the fields
                detail.Permonth = permonth
                detail.Perannum = perannum
                detail.ModifiedBy = userID
                detail.save()

        # CTC 
        ctc_title = SalaryTitle_Master.objects.filter(
            Title="CTC (A+C)", IsDelete=0, HotelID=OID
        ).first()

        if ctc_title:
            ctc_detail = Salary_Detail_Master.objects.filter(
                Effective=effective_obj,
                Salary_title=ctc_title
            ).first()

            if ctc_detail:
                effective_obj.CTC = ctc_detail.Permonth
                effective_obj.save()

        encrypted_id = encrypt_id(EmpID)
        url = reverse('SalaryDetailsPage')
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OID}"
        return redirect(redirect_url)


    # GET request → Data from get request
    Emobj = EmployeeCardDetails(EmpID, OID)
    SalaryTitles  = SalaryTitle_Master.objects.filter(IsDelete=False, HotelID=OID).order_by('TypeOrder','TitleOrder')
    effective_obj = None
    Salary_Detail_Data = None

    if SettleID:
        effective_obj = Salary_Details_Effective.objects.get(
            EmpID=EmpID,
            id=SettleID,
            OrganizationID=OID,
            IsDelete=False
        )
        # print("the effecive object is here::", effective_obj)
        if effective_obj:
            Salary_Detail_Data = Salary_Detail_Master.objects.filter(
                Effective = effective_obj,
                IsDelete=False
            ).values('Salary_title_id', 'Permonth', 'Perannum')
            
            if Salary_Detail_Data: 
                salary_map = {s['Salary_title_id']: s for s in Salary_Detail_Data}

                for salary in SalaryTitles:
                    detail = salary_map.get(salary.id)
                    if detail:
                        salary.Permonth = detail['Permonth']
                        salary.Perannum = detail['Perannum']
                    else:
                        salary.Permonth = 0
                        salary.Perannum = 0
            else:
                print("No object of Salary_Detail_Data::")
                Salary_Detail_Data = None
        else:
            print("No object of effective_obj::")
            effective_obj = None
    else:
        # fallback: create new effective_obj if SettleID not provided
        SettleID = None


    # print("Here is (SalaryTitles) details page::", SalaryTitles)
    context = {
        'Emobj': Emobj,
        'EmpID': EmpID,
        'SalaryTitles': SalaryTitles,
        'OrganizationID': OID,
        'effective_obj_Update': effective_obj,
        'Salary_Detail_Data': Salary_Detail_Data,
        'SettleID': SettleID,
    }
    return render(request, "HR/EmployeeDashboard/Update_SalaryDetails_Settlement.html", context)



# ------ Delete the Settlement
# @transaction.atomic
# def Delete_Details_Settlement(request, EmpID, OID, SettleID):
#     Session_Org_ID = request.session["OrganizationID"]
#     userID = 1
#     if not OID:
#         OID = Session_Org_ID

#     if not EmpID:
#         return redirect("SalaryDetailsPage")

#     SalaryTitles  = SalaryTitle_Master.objects.filter(IsDelete=False, HotelID=OID).order_by('TypeOrder','TitleOrder')
#     effective_obj = None
#     Salary_Detail_Data = None

#     if SettleID:
#         effective_obj = Salary_Details_Effective.objects.get(
#             EmpID=EmpID,
#             id=SettleID,
#             OrganizationID=OID,
#             IsDelete=False
#         )


#         # # print("the effecive object is here::", effective_obj)
#         # if effective_obj:
#         #     Salary_Detail_Data = Salary_Detail_Master.objects.filter(
#         #         Effective = effective_obj,
#         #         IsDelete=False
#         #     ).values('Salary_title_id', 'Permonth', 'Perannum')
            
#         #     if Salary_Detail_Data: 
#         #         salary_map = {s['Salary_title_id']: s for s in Salary_Detail_Data}

#         #         for salary in SalaryTitles:
#         #             detail = salary_map.get(salary.id)
#         #             if detail:
#         #                 salary.Permonth = detail['Permonth']
#         #                 salary.Perannum = detail['Perannum']
#         #             else:
#         #                 salary.Permonth = 0
#         #                 salary.Perannum = 0
#         #     else:
#         #         print("No object of Salary_Detail_Data::")
#         #         Salary_Detail_Data = None
#         # else:
#         #     print("No object of effective_obj::")
#         #     effective_obj = None
#         if effective_obj:
#             effective_obj.IsDelete = True
#             effective_obj.save()

#         # encrypted_id = encrypt_id(EmpID)
#         # url = reverse('SalaryDetailsPage')
#         # redirect_url = f"{url}?EmpID={encrypted_id}&OID={OID}"
#         # return redirect(redirect_url)
#     else:
#         # fallback: create new effective_obj if SettleID not provided
#         SettleID = None

    
#     return HttpResponse("data deleteed successfully")


#     # print("Here is (SalaryTitles) details page::", SalaryTitles)
#     # context = {
#     #     'EmpID': EmpID,
#     #     'SalaryTitles': SalaryTitles,
#     #     'OrganizationID': OID,
#     #     'effective_obj_Update': effective_obj,
#     #     'Salary_Detail_Data': Salary_Detail_Data,
#     #     'SettleID': SettleID,
#     # }
#     # return render(request, "HR/EmployeeDashboard/Update_SalaryDetails_Settlement.html", context)




# views.py
from django.http import JsonResponse

from django.http import JsonResponse

# def recalculate_salary(request):
#     if request.method == "POST":
#         try:
#             total_titles = int(request.POST.get("Total_Title", 0))
#             salary_data = {}

#             # Collect all per-month values
#             for i in range(total_titles + 1):
#                 title_id = request.POST.get(f"TitleID_{i}")
#                 permonth = request.POST.get(f"Permonth_{i}", "0")
#                 try:
#                     permonth = float(permonth) if permonth else 0
#                 except:
#                     permonth = 0
#                 salary_data[title_id] = permonth

#             # Example: get required components by TitleID or index
#             basic = salary_data.get("1", 0)   # assume ID 1 is Basic
#             hra = 0.8 * basic
#             conveyance = salary_data.get("2", 0)  # example
#             other_allowance = salary_data.get("3", 0)
#             gross = basic + hra + conveyance + other_allowance

#             pt = salary_data.get("4", 0)
#             employee_pf = 0.12 * basic
#             esic = 0.0075 * gross
#             meals = salary_data.get("5", 0)
#             accommodation = salary_data.get("6", 0)
#             deductions = pt + employee_pf + esic + meals + accommodation

#             employer_pf = 0.13 * basic
#             company_esic = salary_data.get("7", 0)
#             bonus = salary_data.get("8", 0)
#             company_contrib = employer_pf + company_esic + bonus

#             ctc = gross + company_contrib

#             # Build response with recalculated per-annum values
#             updated_values = {}
#             for i in range(total_titles + 1):
#                 permonth = request.POST.get(f"Permonth_{i}", "0")
#                 try:
#                     permonth = float(permonth) if permonth else 0
#                 except:
#                     permonth = 0
#                 updated_values[f"Perannum_{i}"] = round(permonth * 12, 2)

#             # also send calculated summary
#             updated_values.update({
#                 "Gross": round(gross, 2),
#                 "Deductions": round(deductions, 2),
#                 "CTC": round(ctc, 2),
#             })

#             return JsonResponse({
#                 "success": True,
#                 "updated_values": updated_values,
#                 "message": "Recalculated successfully"
#             })
#         except Exception as e:
#             return JsonResponse({"success": False, "error": str(e)})




# ----------------- Salary Effective Data
def get_salary_effective_data(request, EmpID, OID):
    
    if not EmpID and not OID:
        print("Please provide Empid and OID")

    effective_data = Salary_Details_Effective.objects.filter(
        IsDelete=0,
        OrganizationID=OID,
        EmpID=EmpID
    ).order_by("-CreatedDateTime").values("id", "EffectiveFrom", "CTC", "EmpID", "OrganizationID")

    return JsonResponse(list(effective_data), safe=False)



# views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction

@csrf_exempt  # if you’re using AJAX POST without CSRF token, remove this if you include CSRF in frontend
@transaction.atomic
def delete_salary_effective(request, EmpID, OID, SettleID):
    if request.method == "POST":  # ensure only POST allowed
        try:
            effective_obj = Salary_Details_Effective.objects.get(
                EmpID=EmpID,
                id=SettleID,
                OrganizationID=OID,
                IsDelete=False
            )
            effective_obj.IsDelete = True
            effective_obj.save()

            return JsonResponse({"status": "success", "message": "Record deleted successfully"})
        except Salary_Details_Effective.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Record not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)









# @transaction.atomic
# def Salary_Details_Settlement(request,EmpID,OID, UserID):
#     if request.method == "POST":
#         effective_from = request.POST.get("EffectiveFrom")

#         # Create Effective record first
#         effective_obj = Salary_Details_Effective.objects.create(
#             EmpID=EmpID,
#             EffectiveFrom=effective_from,
#             CTC="0",  # You can calculate CTC after inserting masters
#             OrganizationID=OID,
#             CreatedBy=UserID,
#         )

#         total_titles = int(request.POST.get("Total_Title", -1)) + 1

#         for i in range(total_titles):
#             title_id = request.POST.get(f"TitleID_{i}")
#             permonth = request.POST.get(f"Permonth_{i}", 0) or 0
#             perannum = request.POST.get(f"Perannum_{i}", 0) or 0

#             if title_id:
#                 Salary_Detail_Master.objects.create(
#                     EmpID=EmpID,
#                     Salary_title_id=title_id,
#                     Permonth=permonth,
#                     Perannum=perannum,
#                     Effective=effective_obj,  
#                     OrganizationID=OID,
#                     CreatedBy=UserID,
#                 )

#         # Optionally update effective_obj.CTC = total salary
#         ctc_title = SalaryTitle_Master.objects.filter(
#             Title="CTC (A+C)", IsDelete=False, OrganizationID=OID
#         ).first() 
        
#         if ctc_title:
#             # Step 2: Get the Salary_Detail_Master for this effective and CTC title
#             ctc_detail = Salary_Detail_Master.objects.filter(
#                 Effective=effective_obj,
#                 Salary_title=ctc_title
#             ).first()

#             # Step 3: Store the Perannum value into effective_obj.CTC
#             if ctc_detail:
#                 effective_obj.CTC = ctc_detail.Permonth
#                 effective_obj.save()

#     return True

