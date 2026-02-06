from django.shortcuts import render, redirect
from .models import VerbalWarningmoduls,WrittenWarningModul,FinalWarningModule,WarningMasterDetail
# Create your views here.
from django.contrib import messages
from HumanResources.views import EmployeeDetailsData
from itertools import chain



# def VerbalWarning(request):
#     if 'OrganizationID' not in request.session:
#         return redirect('MasterAttribute.Host')

#     OrganizationID = request.session.get("OrganizationID")
#     UserID = request.session.get("UserID")
#     username = request.session.get("FullName")
    
#     warning_instance = None
#     warning_id = request.GET.get('ID')  

#     if warning_id:
#         warning_instance = VerbalWarningmoduls.objects.filter(id=warning_id, OrganizationID=OrganizationID).first()
#         if not warning_instance:
#             messages.error(request, 'Verbal Warning not found!')
#             return redirect('WarningList')
#     else:
#         EmpID = 1  
#         EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
#         warning_instance = {
#             'emp_code': EmpDetails.EmployeeCode,
#             'emp_name': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
#             'department': EmpDetails.Department,
#             'designation': EmpDetails.Designation,
#         }
       

#     if request.method == 'POST':
#         emp_code = request.POST.get('emp_code')
#         emp_name = request.POST.get('emp_name')
#         department = request.POST.get('department')
#         designation = request.POST.get('designation')
#         problems = request.POST.get('problems')
#         improvements = request.POST.get('improvements')
#         from_date = request.POST.get('from_date')
#         to_date = request.POST.get('to_date')
#         time = request.POST.get('time')
#         venue = request.POST.get('venue')
#         verbally_warned = request.POST.get('verbally_warned')
#         appeal_explained = request.POST.get('appeal_explained')
#         appeal = request.POST.get('appeal')
#         reviewed_by = request.POST.get('reviewed_by')
#         associate_signature_date = request.POST.get('associate_signature_date')
#         manager_signature_date = request.POST.get('manager_signature_date')

#         if warning_instance and isinstance(warning_instance, VerbalWarningmoduls):
#             warning_instance.emp_code = emp_code
#             warning_instance.emp_name = emp_name
#             warning_instance.department = department
#             warning_instance.designation = designation
#             warning_instance.problems = problems
#             warning_instance.improvements = improvements
#             warning_instance.from_date = from_date
#             warning_instance.to_date = to_date
#             warning_instance.time = time
#             warning_instance.venue = venue
#             warning_instance.verbally_warned = verbally_warned
#             warning_instance.appeal_explained = appeal_explained
#             warning_instance.appeal = appeal
#             warning_instance.reviewed_by = reviewed_by
#             warning_instance.associate_signature_date = associate_signature_date
#             warning_instance.manager_signature_date = manager_signature_date
#             warning_instance.ModifyBy = UserID
#             warning_instance.save()
#             messages.success(request, 'Verbal Warning updated successfully!')
#         else:
#             VerbalWarningmoduls.objects.create(
#                 emp_code=emp_code,
#                 emp_name=emp_name,
#                 department=department,
#                 designation=designation,
#                 problems=problems,
#                 improvements=improvements,
#                 from_date=from_date,
#                 to_date=to_date,
#                 time=time,
#                 venue=venue,
#                 verbally_warned=verbally_warned,
#                 appeal_explained=appeal_explained,
#                 appeal=appeal,
#                 reviewed_by=reviewed_by,
#                 associate_signature_date=associate_signature_date,
#                 manager_signature_date=manager_signature_date,
#                 OrganizationID=OrganizationID,
#                 CreatedBy=UserID
#             )
#             messages.success(request, 'Verbal Warning created successfully!')

        
#         warning_master_instance = WarningMasterDetail.objects.filter(Empcode=emp_code, OrganizationID=OrganizationID).first()

#         if warning_master_instance:
            
#             warning_master_instance.Lastwarningtype = 'Verbal_Warning' 
#             warning_master_instance.CreatedByUsername=username,   
#             warning_master_instance.ModifyBy = UserID
           
#             warning_master_instance.save()
#         else:
            
#             WarningMasterDetail.objects.create(
#                 Empcode=emp_code,
#                 Lastwarningtype='Verbal_Warning',
#                 CreatedByUsername=username,  
#                 OrganizationID=OrganizationID,
#                 CreatedBy=UserID,
               
                
               
#             )

#         return redirect('WarningList')

#     context = {
#         'warning': warning_instance,
#         'today': timezone.now().date()
#     }
#     return render(request, 'Warning/VerbalWarning.html', context)
from django.urls import reverse
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from HumanResources.views import EmployeeNameandDesignation
from HumanResources.models import EmployeeWorkDetails,EmployeePersonalDetails
from django.db.models import OuterRef, Subquery, Value, F
from django.db.models.functions import Concat
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.db.models import OuterRef, Subquery, Value, F
from django.db.models.functions import Concat

def EmployeesByStatus(request, OrganizationID):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    # Employment statuses to filter
    allowed_statuses = ['On Probation', 'Confirmed']

    # Subquery to fetch `EmpStatus` from `EmployeeWorkDetails`
    work_status = EmployeeWorkDetails.objects.filter(
        EmpID=OuterRef('EmpID'),
        IsDelete=False,
        OrganizationID=OrganizationID,
        EmpStatus__in=allowed_statuses  # Filter statuses
    ).values('EmpStatus')[:1]

    # Fetch employees with matching status
    employees = EmployeePersonalDetails.objects.annotate(
        emp_status=Subquery(work_status),
        full_name=Concat(
            F('FirstName'), Value(' '), F('MiddleName'), Value(' '), F('LastName')
        )
    ).filter(
        IsDelete=False,
        OrganizationID=OrganizationID,
        emp_status__isnull=False  # Ensure there's a matching status
    ).values_list('full_name', flat=True)  # Return only names

    return employees if employees else None

from HumanResources.views import EmployeeNameonTheBasisofDepartment
def VerbalWarning(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID = request.session.get("UserID")
    username = request.session.get("FullName")
    
    warning_instance = None
    Page = request.GET.get('Page')  # Fetch the Page Parameter
    warning_id = request.GET.get('ID')  # Fetch the warning ID from GET parameters
    EmpID = request.GET.get('EmpID')  # Fetch the EmpID from GET parameters
    # EmployeeNames = EmployeesByStatus(request, OrganizationID)
    Department  = request.GET.get('DepartmentName')
    EmployeeNames = EmployeeNameonTheBasisofDepartment(Department, OrganizationID)
   
    if not EmpID:
        messages.error(request, 'Employee ID is required!')
        return redirect('WarningList')  # Redirect if no EmpID is provided

    # Fetch employee details based on EmpID
    EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)

    if warning_id:
        warning_instance = VerbalWarningmoduls.objects.filter(id=warning_id, OrganizationID=OrganizationID).first()
        if not warning_instance:
            messages.error(request, 'Verbal Warning not found!')
            return redirect('WarningList')
    else:
        # Set default employee details
        warning_instance = {
            'emp_code': EmpDetails.EmployeeCode,
            'emp_name': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
            'department': EmpDetails.Department,
            'designation': EmpDetails.Designation,
        }

        if request.method == 'POST':
            emp_code = request.POST.get('emp_code')
            emp_name = request.POST.get('emp_name')
            department = request.POST.get('department')
            designation = request.POST.get('designation')
            problems = request.POST.get('problems')
            improvements = request.POST.get('improvements')
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            time = request.POST.get('time')
            venue = request.POST.get('venue')
            verbally_warned = request.POST.get('verbally_warned')
            appeal_explained = request.POST.get('appeal_explained')
            appeal = request.POST.get('appeal')
            reviewed_by = request.POST.get('reviewed_by')
            associate_signature_date = request.POST.get('associate_signature_date')
            manager_signature_date = request.POST.get('manager_signature_date')

            if warning_instance and isinstance(warning_instance, VerbalWarningmoduls):
                # Update the existing warning instance
                warning_instance.emp_code = emp_code
                warning_instance.emp_name = emp_name
                warning_instance.department = department
                warning_instance.designation = designation
                warning_instance.problems = problems
                warning_instance.improvements = improvements
                warning_instance.from_date = from_date
                warning_instance.to_date = to_date
                warning_instance.time = time
                warning_instance.venue = venue
                warning_instance.verbally_warned = verbally_warned
                warning_instance.appeal_explained = appeal_explained
                warning_instance.appeal = appeal
                warning_instance.reviewed_by = reviewed_by
                warning_instance.associate_signature_date = associate_signature_date
                warning_instance.manager_signature_date = manager_signature_date
                warning_instance.ModifyBy = UserID
                warning_instance.save()
                messages.success(request, 'Verbal Warning updated successfully!')
            else:
                # Create a new warning instance
                VerbalWarningmoduls.objects.create(
                    emp_code=emp_code,
                    emp_name=emp_name,
                    department=department,
                    designation=designation,
                    problems=problems,
                    improvements=improvements,
                    from_date=from_date,
                    to_date=to_date,
                    time=time,
                    venue=venue,
                    verbally_warned=verbally_warned,
                    appeal_explained=appeal_explained,
                    appeal=appeal,
                    reviewed_by=reviewed_by,
                    associate_signature_date=associate_signature_date,
                    manager_signature_date=manager_signature_date,
                    OrganizationID=OrganizationID,
                    CreatedBy=UserID
                )
                
                warning_master = WarningMasterDetail.objects.create(
                Empcode=emp_code,
                OrganizationID=OrganizationID,
                CreatedBy=UserID,
                CreatedByUsername=request.user.username,
                Lastwarningtype='Verbal Warning',
                ModifyBy=UserID,
                ModifyDateTime=datetime.now().date()
                )

                messages.success(request, 'Verbal Warning created successfully!')

            if Page == "Warning_Employee_List":
                params = {
                    'Page':Page,
                    'Success': 'True',
                    'message': 'Verbal Warning created successfully!'
                }
                url = f"{reverse('WarningList')}?{urlencode(params)}"
                return redirect(url)
            else:
                # Encrypt EmpID and redirect
                Success = True
                encrypted_id = encrypt_id(EmpID)
                url = reverse('Warning_Letters')  # Use the appropriate URL name for Clearance Form
                redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}"
                return redirect(redirect_url)

    context = {
        'warning': warning_instance,
        'today': timezone.now().date(),
        'EmpID': EmpID  ,
        'EmployeeNames':EmployeeNames
    }
    return render(request, 'Warning/VerbalWarning.html', context)













from django.shortcuts import render, redirect
from .models import WarningMasterDetail, VerbalWarningmoduls, WrittenWarningModul, FinalWarningModule
from app.views import OrganizationList
from app.Global_Api import get_organization_list
from HumanResources.views import get_employee_name_designation_by_EmployeeCode_For_Waring,get_employee_designation_by_EmployeeCode_For_Waring

def WarningList(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    
    memOrg =  get_organization_list(OrganizationID)

    OID  = request.GET.get('OID')
    if not OID:
            OID= OrganizationID

    
    warning_master_details = WarningMasterDetail.objects.filter(IsDelete=False)

    if OID != "all":
        warning_master_details = warning_master_details.filter(OrganizationID=OID)
        

    for warning in warning_master_details:    
        EmployeeCode = warning.Empcode
        org_id = warning.OrganizationID if OID == "all" else OID
        # print(EmployeeCode)
        if EmployeeCode:
           EmployeeName = get_employee_name_designation_by_EmployeeCode_For_Waring(org_id, EmployeeCode)
           Designation = get_employee_designation_by_EmployeeCode_For_Waring(org_id, EmployeeCode)
           if EmployeeName and  Designation:
                 warning.EmployeeName = EmployeeName
                 warning.Designation = Designation

    context = {
        'warning_details': warning_master_details,
        'memOrg': memOrg,
        'OID': OID, 
       
    }

    return render(request, 'Warning/WarningList.html', context)





from datetime import datetime
from django.utils import timezone  

# def Written_Warning(request):
#     if 'OrganizationID' not in request.session:
#         return redirect('MasterAttribute.Host')

#     OrganizationID = request.session.get("OrganizationID")
#     UserID = request.session.get("UserID")
#     warning_instance = None
#     warning_id = request.GET.get('ID')  

#     if warning_id:
#         warning_instance = WrittenWarningModul.objects.filter(id=warning_id, OrganizationID=OrganizationID).first()
#         if not warning_instance:
#             messages.error(request, 'Written Warning not found!')
#             return redirect('WarningList')
#     else:
#         EmpID = 1  
#         EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
#         warning_instance = {
#             'employee_no': EmpDetails.EmployeeCode,
#             'name': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
#             'department': EmpDetails.Department,
#             'designation': EmpDetails.Designation,
#         }
      

#     if request.method == 'POST':
#         employee_no = request.POST.get('employee_no')
#         name = request.POST.get('name')
#         department = request.POST.get('department')
#         designation = request.POST.get('designation')
#         warnings = request.POST.get('warnings')

#         problems = request.POST.get('problems')
#         written_warning = request.POST.get('written_warning')
#         improvements = request.POST.get('improvements')

#         period_from_str = request.POST.get('from')
#         period_to_str = request.POST.get('to')

#         warning_date_str = request.POST.get('date')
#         warning_time = request.POST.get('time')
#         witnesses = request.POST.get('witnesses')
#         appeal = request.POST.get('appeal')
#         agree_with_warning = request.POST.get('agree') == 'agree_with_warning'
#         disagree_with_warning = request.POST.get('disagree') == 'disagree_with_warning'
#         supervisor_signature_date_str = request.POST.get('supervisor_signature_date')
#         associate_signature_date_str = request.POST.get('associate_signature_date')
#         reviewed_by = request.POST.get('reviewed_by')
#         seen_by = request.POST.get('seen_by')
#         DepartmentManager = request.POST.get('DepartmentManager')
#         hr_manager_signature_date_str = request.POST.get('HR_Manager')

#         try:
#             period_from = datetime.strptime(period_from_str, '%Y-%m-%d').date()
#             period_to = datetime.strptime(period_to_str, '%Y-%m-%d').date()
#             warning_date = datetime.strptime(warning_date_str, '%Y-%m-%d').date()
#             supervisor_signature_date = datetime.strptime(supervisor_signature_date_str, '%Y-%m-%d').date()
#             associate_signature_date = datetime.strptime(associate_signature_date_str, '%Y-%m-%d').date()
#             hr_manager_signature_date = datetime.strptime(hr_manager_signature_date_str, '%Y-%m-%d').date()
#         except ValueError as e:
#             return render(request, 'Warning/Written_Warning.html', {'error': 'Invalid date format', 'warning': warning_instance})

       
#         if warning_instance and isinstance(warning_instance, WrittenWarningModul):
#             warning_instance.employee_no = employee_no
#             warning_instance.name = name
#             warning_instance.department = department
#             warning_instance.designation = designation
#             warning_instance.warnings = warnings
#             warning_instance.problems = problems
#             warning_instance.written_warning = written_warning
#             warning_instance.improvements = improvements
#             warning_instance.period_from = period_from
#             warning_instance.period_to = period_to
#             warning_instance.warning_date = warning_date
#             warning_instance.warning_time = warning_time
#             warning_instance.witnesses = witnesses
#             warning_instance.appeal = appeal
#             warning_instance.agree_with_warning = agree_with_warning
#             warning_instance.disagree_with_warning = disagree_with_warning
#             warning_instance.supervisor_signature_date = supervisor_signature_date
#             warning_instance.associate_signature_date = associate_signature_date
#             warning_instance.reviewed_by = reviewed_by
#             warning_instance.seen_by = seen_by
#             warning_instance.DepartmentManager = DepartmentManager
#             warning_instance.hr_manager_signature_date = hr_manager_signature_date
#             warning_instance.ModifyBy = UserID
#             warning_instance.save()
#             messages.success(request, 'Written Warning updated successfully!')
#         else:
#             WrittenWarningModul.objects.create(
#                 employee_no=employee_no,
#                 name=name,
#                 department=department,
#                 designation=designation,
#                 warnings=warnings,
#                 problems=problems,
#                 written_warning=written_warning,
#                 improvements=improvements,
#                 period_from=period_from,
#                 period_to=period_to,
#                 warning_date=warning_date,
#                 warning_time=warning_time,
#                 witnesses=witnesses,
#                 appeal=appeal,
#                 agree_with_warning=agree_with_warning,
#                 disagree_with_warning=disagree_with_warning,
#                 supervisor_signature_date=supervisor_signature_date,
#                 associate_signature_date=associate_signature_date,
#                 reviewed_by=reviewed_by,
#                 seen_by=seen_by,
#                 DepartmentManager=DepartmentManager,
#                 hr_manager_signature_date=hr_manager_signature_date,
#                 OrganizationID=OrganizationID,
#                 CreatedBy=UserID
#             )
#             messages.success(request, 'Written Warning created successfully!')

        
#         warning_master, created = WarningMasterDetail.objects.get_or_create(
#             Empcode=employee_no,
#             OrganizationID=OrganizationID,
#             defaults={'CreatedBy': UserID, 'CreatedByUsername': request.user.username}
#         )
#         warning_master.Lastwarningtype = 'Written Warning'
#         warning_master.ModifyBy = UserID
#         warning_master.ModifyDateTime = datetime.now().date()
#         warning_master.save()

#         return redirect('WarningList')

#     context = {
#         'warning': warning_instance,
#         'today': timezone.now().date()
#     }
#     return render(request, 'Warning/Written_Warning.html', context)

def Written_Warning(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')  
    OrganizationID = request.session.get("OrganizationID")
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID

    Page = request.GET.get('Page')  # Fetch the Page Parameter

    UserID = request.session.get("UserID")
    warning_instance = None
    warning_id = request.GET.get('ID')
    EmpID = request.GET.get('EmpID')
    Department = request.GET.get('DepartmentName')   
    # EmployeeNames = EmployeesByStatus(request, OrganizationID)
    EmployeeNames = EmployeeNameonTheBasisofDepartment(Department, OrganizationID)
   
    if warning_id:
        
        warning_instance = WrittenWarningModul.objects.filter(id=warning_id, OrganizationID=OrganizationID).first()
        if not warning_instance:
            messages.error(request, 'Written Warning not found!')
            return redirect('WarningList')
    else:
        
        EmpID = request.GET.get('EmpID')
        if not EmpID:
            messages.error(request, 'Employee ID is required!')
            return redirect('WarningList')

        
        EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
        warning_instance = {
            'employee_no': EmpDetails.EmployeeCode,
            'name': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
            'department': EmpDetails.Department,
            'designation': EmpDetails.Designation,
        }

    
    if request.method == 'POST':
       
        employee_no = request.POST.get('employee_no')
        name = request.POST.get('name')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        warnings = request.POST.get('warnings') or ''

        problems = request.POST.get('problems')
        written_warning = request.POST.get('written_warning')
        improvements = request.POST.get('improvements')

        period_from_str = request.POST.get('from')
        period_to_str = request.POST.get('to')

        warning_date_str = request.POST.get('date')
        warning_time = request.POST.get('time')
        witnesses = request.POST.get('witnesses')
        appeal = request.POST.get('appeal')
        agree_with_warning = request.POST.get('agree') == 'agree_with_warning'
        disagree_with_warning = request.POST.get('disagree') == 'disagree_with_warning'
        supervisor_signature_date_str = request.POST.get('supervisor_signature_date')
        associate_signature_date_str = request.POST.get('associate_signature_date')
        reviewed_by = request.POST.get('reviewed_by')
        seen_by = request.POST.get('seen_by')
        DepartmentManager = request.POST.get('DepartmentManager')
        hr_manager_signature_date_str = request.POST.get('HR_Manager')

       
        try:
            period_from = datetime.strptime(period_from_str, '%Y-%m-%d').date()
            period_to = datetime.strptime(period_to_str, '%Y-%m-%d').date()
            warning_date = datetime.strptime(warning_date_str, '%Y-%m-%d').date()
            supervisor_signature_date = datetime.strptime(supervisor_signature_date_str, '%Y-%m-%d').date()
            associate_signature_date = datetime.strptime(associate_signature_date_str, '%Y-%m-%d').date()
            hr_manager_signature_date = datetime.strptime(hr_manager_signature_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format')
            return render(request, 'Warning/Written_Warning.html', {'error': 'Invalid date format', 'warning': warning_instance})

        
        if warning_instance and isinstance(warning_instance, WrittenWarningModul):
            
            warning_instance.employee_no = employee_no
            warning_instance.name = name
            warning_instance.department = department
            warning_instance.designation = designation
            warning_instance.warnings = warnings
            warning_instance.problems = problems
            warning_instance.written_warning = written_warning
            warning_instance.improvements = improvements
            warning_instance.period_from = period_from
            warning_instance.period_to = period_to
            warning_instance.warning_date = warning_date
            warning_instance.warning_time = warning_time
            warning_instance.witnesses = witnesses
            warning_instance.appeal = appeal
            warning_instance.agree_with_warning = agree_with_warning
            warning_instance.disagree_with_warning = disagree_with_warning
            warning_instance.supervisor_signature_date = supervisor_signature_date
            warning_instance.associate_signature_date = associate_signature_date
            warning_instance.reviewed_by = reviewed_by
            warning_instance.seen_by = seen_by
            warning_instance.DepartmentManager = DepartmentManager
            warning_instance.hr_manager_signature_date = hr_manager_signature_date
            warning_instance.ModifyBy = UserID
            
            warning_instance.save()
            messages.success(request, 'Written Warning updated successfully!')
        else:
           
            WrittenWarningModul.objects.create(
                employee_no=employee_no,
                name=name,
                department=department,
                designation=designation,
                warnings=warnings,
                problems=problems,
                written_warning=written_warning,
                improvements=improvements,
                period_from=period_from,
                period_to=period_to,
                warning_date=warning_date,
                warning_time=warning_time,
                witnesses=witnesses,
                appeal=appeal,
                agree_with_warning=agree_with_warning,
                disagree_with_warning=disagree_with_warning,
                supervisor_signature_date=supervisor_signature_date,
                associate_signature_date=associate_signature_date,
                reviewed_by=reviewed_by,
                seen_by=seen_by,
                DepartmentManager=DepartmentManager,
                hr_manager_signature_date=hr_manager_signature_date,
                OrganizationID=OrganizationID,
                CreatedBy=UserID
            )
            messages.success(request, 'Written Warning created successfully!')

        
            warning_master_instance = WarningMasterDetail.objects.filter(Empcode=employee_no, OrganizationID=OrganizationID).first()
            if warning_master_instance:
                warning_master_instance.Lastwarningtype = 'Written Warning'
                warning_master_instance.ModifyBy = UserID
                warning_master_instance.ModifyDateTime = datetime.now().date()
                warning_master_instance.save()

        if Page == "Warning_Employee_List":
            params = {
                'Page':Page,
                'Success': 'True',
                'message': 'Written Warning created successfully!'
            }
            url = f"{reverse('WarningList')}?{urlencode(params)}"
            return redirect(url)
        else:
            Success = True
            encrypted_id = encrypt_id(EmpID)  
            url = reverse('Warning_Letters')  
            redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}"
            return redirect(redirect_url)

    
    context = {
        'warning': warning_instance,
        'today': timezone.now().date(),
          'EmployeeNames':EmployeeNames
    }
    return render(request, 'Warning/Written_Warning.html', context)



from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import FinalWarningModule, WarningMasterDetail

def FinalWarning(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID

    Page = request.GET.get('Page')  # Fetch the Page Parameter

    UserID = request.session.get("UserID")
    warning_instance = None
    warning_id = request.GET.get('ID')
    EmpID = request.GET.get('EmpID')
    # EmployeeNames = EmployeesByStatus(request, OrganizationID)
    Department  = request.GET.get('DepartmentName')
    EmployeeNames = EmployeeNameonTheBasisofDepartment(Department, OrganizationID)
   
    # Dynamically get the EmpID (from form, URL, etc.)
    EmpID = request.GET.get('EmpID', 1)  # Defaulting to 1 if EmpID is not provided in GET parameters

    if warning_id:
        warning_instance = FinalWarningModule.objects.filter(id=warning_id, OrganizationID=OrganizationID).first()
        if not warning_instance:
            messages.error(request, 'Final Warning not found!')
            return redirect('WarningList')
    else:
        # Fetch dynamic EmpDetails using EmpID
        EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
        warning_instance = {
            'employee_no': EmpDetails.EmployeeCode,
            'name': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
            'department': EmpDetails.Department,
            'designation': EmpDetails.Designation,
        }

    if request.method == 'POST':
        employee_no = request.POST.get('employee_no')
        name = request.POST.get('name')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        warning_type = request.POST.get('warning_type')
        employee_problem = request.POST.get('employee_problem')
        written_warning = request.POST.get('written_warning')
        improvement_standard = request.POST.get('improvement_standard')
        improvement_period_from = request.POST.get('improvement_period_from')
        improvement_period_to = request.POST.get('improvement_period_to')
        warning_date = request.POST.get('warning_date')
        warning_time = request.POST.get('warning_time')
        witness = request.POST.get('witness')
        appeal = request.POST.get('appeal')
        agree_warning = request.POST.get('agree_warning') == 'on'
        disagree_warning = request.POST.get('disagree_warning') == 'on'
        supervisor_signature_date = request.POST.get('supervisor_signature_date')
        associate_signature_date = request.POST.get('associate_signature_date')
        reviewed_by = request.POST.get('reviewed_by')
        department_signature_date = request.POST.get('department_signature_date')
        hr_manager_signature = request.POST.get('hr_manager_signature')

        if warning_instance and isinstance(warning_instance, FinalWarningModule):
            warning_instance.employee_no = employee_no
            warning_instance.name = name
            warning_instance.department = department
            warning_instance.designation = designation
            warning_instance.warning_type = warning_type
            warning_instance.employee_problem = employee_problem
            warning_instance.written_warning = written_warning
            warning_instance.improvement_standard = improvement_standard
            warning_instance.improvement_period_from = improvement_period_from
            warning_instance.improvement_period_to = improvement_period_to
            warning_instance.warning_date = warning_date
            warning_instance.warning_time = warning_time
            warning_instance.witness = witness
            warning_instance.appeal = appeal
            warning_instance.agree_warning = agree_warning
            warning_instance.disagree_warning = disagree_warning
            warning_instance.supervisor_signature_date = supervisor_signature_date
            warning_instance.associate_signature_date = associate_signature_date
            warning_instance.reviewed_by = reviewed_by
            warning_instance.department_signature_date = department_signature_date
            warning_instance.hr_manager_signature = hr_manager_signature
            warning_instance.ModifyBy = UserID
            warning_instance.save()
            messages.success(request, 'Final Warning updated successfully!')
        else:
            FinalWarningModule.objects.create(
                employee_no=employee_no,
                name=name,
                department=department,
                designation=designation,
                warning_type=warning_type,
                employee_problem=employee_problem,
                written_warning=written_warning,
                improvement_standard=improvement_standard,
                improvement_period_from=improvement_period_from,
                improvement_period_to=improvement_period_to,
                warning_date=warning_date,
                warning_time=warning_time,
                witness=witness,
                appeal=appeal,
                agree_warning=agree_warning,
                disagree_warning=disagree_warning,
                supervisor_signature_date=supervisor_signature_date,
                associate_signature_date=associate_signature_date,
                reviewed_by=reviewed_by,
                department_signature_date=department_signature_date,
                hr_manager_signature=hr_manager_signature,
                OrganizationID=OrganizationID,
                CreatedBy=UserID
            )
            messages.success(request, 'Final Warning created successfully!')

        # Update the warning master record
        warning_master_instance = WarningMasterDetail.objects.filter(Empcode=employee_no, OrganizationID=OrganizationID).first()
        if warning_master_instance:
            warning_master_instance.Lastwarningtype = 'Final Warning'
            warning_master_instance.ModifyBy = UserID
            warning_master_instance.ModifyDateTime = datetime.now().date()

            warning_master_instance.save()
            
        if Page == "Warning_Employee_List":
            params = {
                'Page':Page,
                'Success': 'True',
                'message': 'Final Warning created successfully !'
            }
            url = f"{reverse('WarningList')}?{urlencode(params)}"
            return redirect(url)
        else:
            Success = True
            encrypted_id = encrypt_id(EmpID)  
            url = reverse('Warning_Letters')  
            redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}"
            return redirect(redirect_url)

    context = {
        'warning': warning_instance,
        'today': timezone.now().date(),
        'EmployeeNames':EmployeeNames
    }
    return render(request, 'Warning/FinalWarning.html', context)




# def FinalWarning(request):
#     if 'OrganizationID' not in request.session:
#         return redirect('MasterAttribute.Host')

#     OrganizationID = request.session.get("OrganizationID")
#     UserID = request.session.get("UserID")
#     warning_instance = None
#     warning_id = request.GET.get('ID')

#     if warning_id:
#         warning_instance = FinalWarningModule.objects.filter(id=warning_id, OrganizationID=OrganizationID).first()
#         if not warning_instance:
#             messages.error(request, 'Final Warning not found!')
#             return redirect('WarningList')
#     else:
#         EmpID = 1  
#         EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
#         warning_instance = {
#             'employee_no': EmpDetails.EmployeeCode,
#             'name': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
#             'department': EmpDetails.Department,
#             'designation': EmpDetails.Designation,
#         }
#         warning_instance = {
#             'employee_no': 1023657,
#             'name': "Darpan",
#             'department': "hr",
#             'designation': "HR",
#         }
    
#     if request.method == 'POST':
#         employee_no = request.POST.get('employee_no')
#         name = request.POST.get('name')
#         department = request.POST.get('department')
#         designation = request.POST.get('designation')
#         warning_type = request.POST.get('warning_type')
#         employee_problem = request.POST.get('employee_problem')
#         written_warning = request.POST.get('written_warning')
#         improvement_standard = request.POST.get('improvement_standard')
#         improvement_period_from = request.POST.get('improvement_period_from')
#         improvement_period_to = request.POST.get('improvement_period_to')
#         warning_date = request.POST.get('warning_date')
#         warning_time = request.POST.get('warning_time')
#         witness = request.POST.get('witness')
#         appeal = request.POST.get('appeal')
#         agree_warning = request.POST.get('agree_warning') == 'on'
#         disagree_warning = request.POST.get('disagree_warning') == 'on'
#         supervisor_signature_date = request.POST.get('supervisor_signature_date')
#         associate_signature_date = request.POST.get('associate_signature_date')
#         reviewed_by = request.POST.get('reviewed_by')
#         department_signature_date = request.POST.get('department_signature_date')
#         hr_manager_signature = request.POST.get('hr_manager_signature')

#         if warning_instance and isinstance(warning_instance, FinalWarningModule):
#             warning_instance.employee_no = employee_no
#             warning_instance.name = name
#             warning_instance.department = department
#             warning_instance.designation = designation
#             warning_instance.warning_type = warning_type
#             warning_instance.employee_problem = employee_problem
#             warning_instance.written_warning = written_warning
#             warning_instance.improvement_standard = improvement_standard
#             warning_instance.improvement_period_from = improvement_period_from
#             warning_instance.improvement_period_to = improvement_period_to
#             warning_instance.warning_date = warning_date
#             warning_instance.warning_time = warning_time
#             warning_instance.witness = witness
#             warning_instance.appeal = appeal
#             warning_instance.agree_warning = agree_warning
#             warning_instance.disagree_warning = disagree_warning
#             warning_instance.supervisor_signature_date = supervisor_signature_date
#             warning_instance.associate_signature_date = associate_signature_date
#             warning_instance.reviewed_by = reviewed_by
#             warning_instance.department_signature_date = department_signature_date
#             warning_instance.hr_manager_signature = hr_manager_signature
#             warning_instance.ModifyBy = UserID
#             warning_instance.save()
#             messages.success(request, 'Final Warning updated successfully!')
#         else:
#             FinalWarningModule.objects.create(
#                 employee_no=employee_no,
#                 name=name,
#                 department=department,
#                 designation=designation,
#                 warning_type=warning_type,
#                 employee_problem=employee_problem,
#                 written_warning=written_warning,
#                 improvement_standard=improvement_standard,
#                 improvement_period_from=improvement_period_from,
#                 improvement_period_to=improvement_period_to,
#                 warning_date=warning_date,
#                 warning_time=warning_time,
#                 witness=witness,
#                 appeal=appeal,
#                 agree_warning=agree_warning,
#                 disagree_warning=disagree_warning,
#                 supervisor_signature_date=supervisor_signature_date,
#                 associate_signature_date=associate_signature_date,
#                 reviewed_by=reviewed_by,
#                 department_signature_date=department_signature_date,
#                 hr_manager_signature=hr_manager_signature,
#                 OrganizationID=OrganizationID,
#                 CreatedBy=UserID
#             )
#             messages.success(request, 'Final Warning created successfully!')

#         warning_master_instance = WarningMasterDetail.objects.filter(Empcode=employee_no, OrganizationID=OrganizationID).first()
#         if warning_master_instance:
#             warning_master_instance.Lastwarningtype = 'Final Warning'
#             warning_master_instance.ModifyBy = UserID
#             warning_master_instance.save()
            
#         return redirect('WarningList')

#     context = {
#         'warning': warning_instance,
#         'today': timezone.now().date()
#     }
#     return render(request, 'Warning/FinalWarning.html', context)












from django.http import HttpResponse
from io import BytesIO    
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, get_object_or_404
from .models import VerbalWarningmoduls, WrittenWarningModul, FinalWarningModule






from django.shortcuts import render, get_object_or_404
from .models import VerbalWarningmoduls, WrittenWarningModul, FinalWarningModule

def warning_detail_view(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    EC = request.GET.get('EC')
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID

    verbal_warnings = VerbalWarningmoduls.objects.filter(emp_code=EC,OrganizationID=OrganizationID)
    written_warnings = WrittenWarningModul.objects.filter(employee_no=EC,OrganizationID=OrganizationID)
    final_warnings = FinalWarningModule.objects.filter(employee_no=EC,OrganizationID=OrganizationID)

    
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

    context = {
        'warnings': warnings
    }
    return render(request, 'Warning/warning_detail.html', context)


def WarningPdf(request):
    return render(request, 'Warning/WarningPdf.html')


from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from django.template.loader import get_template
from xhtml2pdf import pisa  
from app.models import OrganizationMaster
def generate_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def verbal_warning_pdf(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    id  = request.GET.get('id')
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    warning = get_object_or_404(VerbalWarningmoduls, id=id,)
    
    context = {'warning': warning,'organization_logos':organization_logos,'current_datetime':current_datetime,'organization_logo':organization_logo}
    return generate_pdf('Warning/verbal_warning_pdf.html', context)



def written_warning_pdf(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    OID  = request.GET.get('OID')
    id  = request.GET.get('id')

    IsRadisson = 'Hide'
    if OrganizationID == '20180612060935':
        IsRadisson = 'Show'
    else:
        IsRadisson = 'Hide'
         
    if OID:
            OrganizationID= OID
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

    warning = get_object_or_404(WrittenWarningModul, id=id)
    context = {'warning': warning,'organization_logos':organization_logos,'current_datetime':current_datetime,'organization_logo':organization_logo, 'IsRadisson':IsRadisson }
    return generate_pdf('Warning/written_warning_pdf.html', context)

def final_warning_pdf(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    OID  = request.GET.get('OID')
    id  = request.GET.get('id')
    if OID:
            OrganizationID= OID
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
    organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
    warning = get_object_or_404(FinalWarningModule, id=id)
    context = {'warning': warning,'organization_logos':organization_logos,'current_datetime':current_datetime,'organization_logo':organization_logo}
    return generate_pdf('Warning/final_warning_pdf.html', context)



from Manning_Guide.models import OnRollDepartmentMaster
from Manning_Guide.models import OnRollDesignationMaster,CorporateDesignationMaster
from urllib.parse import urlencode
def Warning_Employee_List(request):
    if 'OrganizationID' not in request.session or 'UserID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    SessionOrganizationID = int(OrganizationID)
    UserID = request.session.get("UserID")

    SessionDepartment = request.session.get("Department_Name")
    SessionEmployeeCode = request.session.get("EmployeeCode")
    UserType=request.session["UserType"]
    print("UserType", UserType)
    print("SessionDepartment", SessionDepartment)

    for key, value in request.session.items():
        print(f"{key} => {value}")


    memOrg = OrganizationList(OrganizationID)

    Departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    # Designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    DottedLineDesignations = CorporateDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    MergedReportingtoDesignation = chain(Designations, DottedLineDesignations)


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



    if UserType == "GM" or SessionDepartment == "HR":
        # HR GM – full access
        pass
    else:
        # Get EmpID using session EmployeeCode
        emp = EmployeePersonalDetails.objects.filter(
            EmployeeCode=SessionEmployeeCode,
            IsDelete=False
        ).first()

        if emp:
            emp_work = EmployeeWorkDetails.objects.filter(
                EmpID=emp.EmpID,
                IsDelete=False
            ).first()

            if emp_work:
                user_designation = emp_work.Designation
                work_details = work_details.filter(ReportingtoDesignation=user_designation)

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

    Departments_Dropdown = sorted(set(emp['Department'].strip() for emp in employee_data if emp['Department']))
    Designations_Dropdown = sorted(set(emp['Designation'].strip() for emp in employee_data if emp['Designation']))

    print("Departments_Dropdown",Departments_Dropdown)
    print("Designations_Dropdown",Designations_Dropdown)


    # print("reporting_person_data::",reporting_person_data)
    context = {
        'memOrg': memOrg,
        'Departments': Departments,
        'Designations': Designations,
        # 'Lavelsdatas': Lavelsdatas,
        'OrganizationID': OrganizationID,
        'work_details': work_details,
        'employee_data': employee_data,
        'Departments_Dropdown': Departments_Dropdown,
        'Designations_Dropdown': Designations_Dropdown,
        'MergedReportingtoDesignation': MergedReportingtoDesignation,

        # Ogranization Dropdown
        'SessionOrganizationID': SessionOrganizationID,  # Correct
        'orgs': orgs,
        'selectedOrganizationID': SelectedOrganizationID_str,  # String to match dropdown value
    }

    return render(request, 'Warning\Employee List\Employee_Warning_List.html', context)

