from django.shortcuts import render,redirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from Manning_Guide.models import OnRollDepartmentMaster,CorporateDesignationMaster,ContractDesignationMaster,OnRollDesignationMaster,OnRollDesignationMaster,LavelAdd,ManageBudgetOnRoll, CorporateDepartmentMaster, CorporateDivisionMaster
from datetime import datetime
from .models import OpenPosition,NotificationSchedule
from django.shortcuts import render, redirect
import requests
from app.models import OrganizationMaster,EmployeeMaster
from .models import OpenPosition,CareerResume
from .utils import generate_position_image  
import logging
from django.conf import settings
import os
from .utils import generate_position_image  




from django.contrib import messages

from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from datetime import datetime
import logging
from collections import OrderedDict


logger = logging.getLogger(__name__)

def OpenPositionAdd(request):
   
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    username = request.session.get("FullName")

    
    if not OrganizationID or not UserID:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')

    memOrg = OrganizationList(OrganizationID)
    
    Departments = OnRollDepartmentMaster.objects.filter(IsDelete=False).order_by('DepartmentName')  # Replace 'Name' with the actual field name for department name if needed
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).select_related('OnRollDepartmentMaster').order_by('designations')  # Replace 'Name' with the actual field name for designation name if needed
    
    Corporate_Designations = CorporateDesignationMaster.objects.filter(IsDelete=False).select_related('CorporateDepartmentMaster').order_by('designations') 
    Corporate_Departments = CorporateDepartmentMaster.objects.filter(IsDelete=False).order_by('DepartmentName')  
    
    selected_location = request.GET.get('location', OrganizationID)

    
    budget_hc_data = ManageBudgetOnRoll.objects.filter(
        on_roll_designation_master__in=Designations,
        hotel_name=selected_location,
        is_delete=False
    ).values('on_roll_designation_master', 'on_roll_department_master').annotate(total_budget_hc=Sum('head_count'))

    designation_list = Designations.values_list('designations', flat=True)
    department_list = Designations.values_list('OnRollDepartmentMaster__DepartmentName', flat=True)
    
    Corporate_Designation_list = Corporate_Designations.values_list('designations', flat=True)
    Corporate_Department_list = Corporate_Designations.values_list('CorporateDepartmentMaster__DepartmentName', flat=True)

    # all_departments = list(OrderedDict.fromkeys(
    #     list(department_list) + [f"{dept} (Corporate)" for dept in Corporate_Department_list]
    # ))

    # all_designations = list(designation_list) + [f"{desig} (Corporate)" for desig in Corporate_Designation_list]

    # OnRoll designation -> department
    # onroll_desig_to_dept = {
    #     desig.designations: desig.OnRollDepartmentMaster.DepartmentName
    #     for desig in Designations
    # }

    # Corporate designation -> department
    # corporate_desig_to_dept = {
    #     f"{desig.designations} (Corporate)": desig.CorporateDepartmentMaster.DepartmentName + " (Corporate)"
    #     for desig in Corporate_Designations
    # }

    # Merge both
    # designation_to_department = {**onroll_desig_to_dept, **corporate_desig_to_dept}

    # employee_hc_data = EmployeeMaster.objects.filter(
    #     Designation__in=Designations.values_list('designations', flat=True),
    #     Department__in=Designations.values_list('OnRollDepartmentMaster__DepartmentName', flat=True),
    #     OrganizationID=selected_location,
    #     EmpStatus__in = ['Confirmed','On Probation','Not Confirmed'],
    #     IsDelete=False
    # ).values('Designation', 'Department').annotate(actual_hc=Count('id'))

    employee_hc_data = EmployeeWorkDetails.objects.filter(
        Designation__in=designation_list,
        Department__in=department_list,
        OrganizationID=selected_location,
        EmpStatus__in=['Confirmed', 'On Probation', 'Not Confirmed'],
        IsDelete=False,
        EmpID__in=EmployeePersonalDetails.objects.filter(IsDelete=False,OrganizationID=selected_location).values_list('EmpID', flat=True)
    ).values('Designation', 'Department').annotate(actual_hc=Count('EmpID'))
   
    budget_hc_map = {
        (item['on_roll_designation_master'], item['on_roll_department_master']): item['total_budget_hc']
        for item in budget_hc_data
    }

    actual_hc_map = {
        (item['Designation'], item['Department']): item['actual_hc']
        for item in employee_hc_data
    }

    
    table_data = []
    for des in Designations:
        budget_hc = budget_hc_map.get((des.id, des.OnRollDepartmentMaster.id), 0)
        actual_hc = actual_hc_map.get((des.designations, des.OnRollDepartmentMaster.DepartmentName), 0)
        variance_hc = actual_hc - budget_hc

        table_data.append({
            'designation': des.designations,
            'department': des.OnRollDepartmentMaster.DepartmentName,
            'budget_hc': budget_hc,
            'actual_hc': actual_hc,
            'variance_hc': variance_hc

        })

    
    selected_designation = request.GET.get('selected_designation')
    if selected_designation:
        table_data = [row for row in table_data if row['designation'] == selected_designation]

    if request.method == 'POST':
        
        position = request.POST.get('Position')
        open_department = request.POST.get('OpenDepartment')
        job_type = request.POST.get('Job_Type')
        salary = request.POST.get('Salary')
        locations = request.POST.get('Locations')
        number = request.POST.get('Number')
        opened_on = request.POST.get('Opened_On')

       
        selected_designation = request.POST.get('Position')
        selected_department = None
        variance_hc = None

        is_corporate_position = selected_designation.strip().lower().endswith("(corporate)")

        if not is_corporate_position:
            for item in table_data:
                if item['designation'] == selected_designation:
                    selected_department = item['department']
                    variance_hc = item['variance_hc']
                    break

            # if not position.strip().lower().endswith("(corporate)"):
            if variance_hc is None or variance_hc >= 0:
                logger.error("Variance HC must be negative to create an open position.")
                messages.error(request, 'You have exceeded your budget, Please contact regional office..')  
                return render(request, 'OpenPositions/OpenPositionAdd.html', {
                    'memOrg': memOrg,
                    # 'Departments': Departments,
                    # 'Departments': all_departments,
                    # 'Designations': all_designations,
                    # 'Designations': Designations,
                    'Departments': Departments,
                    'Designations': all_designations,
                    'designation_to_department': designation_to_department,  # dict for JS

                    'table_data': table_data,
                    'error_message': 'You have exceeded your budget, Please contact regional office.',
                    'selected_location': selected_location,
                })

       # Safe calculation of number to open
        number_to_use = int(number)
        if not is_corporate_position and variance_hc is not None:
            number_to_use = min(int(number), abs(variance_hc))

        open_position = OpenPosition.objects.create(
            Position=position,
            OpenDepartment=open_department,
            Job_Type=job_type,
            Salary=salary,
            Locations=locations,
            Number=number_to_use,  
            # Number=min(int(number), abs(variance_hc)),  
            Opened_On=datetime.strptime(opened_on, '%d-%m-%Y').date(),  
            # Opened_On=datetime.strptime(opened_on, '%d %b %Y').date(),  
            OrganizationID=selected_location,
            CreatedByUserID=UserID,
            CreatedByUsername=username,
        )

        
        try:
            position_image_url = generate_position_image(position, "https://careersatnile.com/", locations)
            if "Error" in position_image_url:
                print(position_image_url)  
            else:
                print(f"Image URL: {position_image_url}")
        
                open_position.PositionImage = position_image_url
                open_position.save()
        except Exception as e:
            # Log the error
            logger.error(f"Failed to upload image to Azure: {str(e)}")
            # Optionally show the error in the UI or suppress it
            messages.warning(request, 'Open position created, but image upload failed.')

        messages.success(request, 'Open position created successfully!')
        return redirect('OpenPositionList')

   
    context = {
        'memOrg': memOrg,
        'Departments': Departments,
        'Designations': all_designations,
        # 'Designations': Designations,
        'designation_to_department': designation_to_department,  # dict for JS
        'table_data': table_data,
        'selected_location': selected_location,
        'error_message': request.GET.get('error_message'),
    }

    return render(request, 'OpenPositions/OpenPositionAdd.html', context)

# def get_designation_with_department_and_onroll(designation_name):
    
#     contract_designations = ContractDesignationMaster.objects.filter(designations=designation_name, IsDelete=False)
#     corporate_designations = CorporateDesignationMaster.objects.filter(designations=designation_name, IsDelete=False)
#     onroll_contract_designations = OnRollDesignationMaster.objects.filter(designations=designation_name, IsDelete=False)
#     onroll_corporate_designations = OnRollDesignationMaster.objects.filter(designations=designation_name, IsDelete=False)

#     designation_departments = []

    
#     for contract in contract_designations:
#         department_name = contract.ContractDepartmentMaster.DepartmentName
#         designation_departments.append({
#             'contract_division': contract.ContractDivisionMaster,
#             'department': department_name,
#             'designation': contract.designations
#         })

    
#     for corporate in corporate_designations:
#         department_name = corporate.CorporateDepartmentMaster.DepartmentName
#         designation_departments.append({
#             'corporate_division': corporate.CorporateDivisionMaster,
#             'department': department_name,
#             'designation': corporate.designations
#         })

    
#     for onroll_contract in onroll_contract_designations:
#         department_name = onroll_contract.OnRollDepartmentMaster.DepartmentName
#         designation_departments.append({
#             'onroll_contract_division': onroll_contract.OnRollDivisionMaster,
#             'department': department_name,
#             'designation': onroll_contract.designations
#         })

    
#     for onroll_corporate in onroll_corporate_designations:
#         department_name = onroll_corporate.OnRollDepartmentMaster.DepartmentName
#         designation_departments.append({
#             'onroll_corporate_division': onroll_corporate.OnRollDivisionMaster,
#             'department': department_name,
#             'designation': onroll_corporate.designations
#         })

#     return designation_departments






from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from Job_Description.models import JobDescription  

def get_job_description(request):
    designation = request.GET.get('designation')

    if not designation:
        return JsonResponse({'error': 'No designation provided'}, status=400)

    try:
        job_description = JobDescription.objects.filter(Position=designation).first()
        if job_description:
            data = {
             
                'Position': job_description.Position,
               
                'Job_Scope': job_description.Job_Scope,
                'Duties_Responsibilities': job_description.Duties_Responsibilities,
                'Job_Knowledge_Skills': job_description.Job_Knowledge_Skills,
              
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Job description not found for the selected designation'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



logger = logging.getLogger(__name__)

def EditOpenPosition(request, position_id):
    # Ensure session contains necessary data
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    username = request.session.get("FullName")

    if not OrganizationID or not UserID:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')

    
    memOrg = OrganizationList(OrganizationID)

    Departments = OnRollDepartmentMaster.objects.filter(IsDelete=False).order_by('DepartmentName')  # Replace 'Name' with the actual field name for department name if needed
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).select_related('OnRollDepartmentMaster').order_by('designations')  # Replace 'Name' with the actual field name for designation name if needed

    selected_location = request.GET.get('OrganizationID', OrganizationID)

    # Query budgeted and actual headcount data
    budget_hc_data = ManageBudgetOnRoll.objects.filter(
        on_roll_designation_master__in=Designations,
        hotel_name=selected_location,
        is_delete=False
    ).values('on_roll_designation_master', 'on_roll_department_master').annotate(total_budget_hc=Sum('head_count'))

    employee_hc_data = EmployeeWorkDetails.objects.filter(
        Designation__in=Designations.values_list('designations', flat=True),
        Department__in=Designations.values_list('OnRollDepartmentMaster__DepartmentName', flat=True),
        OrganizationID=selected_location,
        IsDelete=False
    ).values('Designation', 'Department').annotate(actual_hc=Count('id'))

    # Build headcount maps
    budget_hc_map = {
        (item['on_roll_designation_master'], item['on_roll_department_master']): item['total_budget_hc']
        for item in budget_hc_data
    }

    actual_hc_map = {
        (item['Designation'], item['Department']): item['actual_hc']
        for item in employee_hc_data
    }

    # Build table data
    table_data = []
    for des in Designations:
        budget_hc = budget_hc_map.get((des.id, des.OnRollDepartmentMaster.id), 0)
        actual_hc = actual_hc_map.get((des.designations, des.OnRollDepartmentMaster.DepartmentName), 0)
        variance_hc = actual_hc - budget_hc

        table_data.append({
            'designation': des.designations,
            'department': des.OnRollDepartmentMaster.DepartmentName,
            'budget_hc': budget_hc,
            'actual_hc': actual_hc,
            'variance_hc': variance_hc
        })

    selected_designation = request.GET.get('selected_designation')
    if selected_designation:
        table_data = [row for row in table_data if row['designation'] == selected_designation]

    # Get the open position object
    open_position = get_object_or_404(OpenPosition, id=position_id)

    if request.method == 'POST':
        position = request.POST.get('Position')
        open_department = request.POST.get('OpenDepartment')
        job_type = request.POST.get('Job_Type')
        salary = request.POST.get('Salary')
        locations = request.POST.get('Locations')
        number = request.POST.get('Number')
        opened_on = request.POST.get('Opened_On')

        # Parse opened_on date
        try:
            opened_on_date = datetime.strptime(opened_on, '%Y-%m-%d')
        except ValueError:
            opened_on_date = datetime.now()

        opened_days = (datetime.now() - opened_on_date).days

        # Validate variance headcount
        variance_hc_str = request.POST.get('variance_hc', '0')
        try:
            variance_hc = int(variance_hc_str)
        except ValueError:
            variance_hc = 0

        if variance_hc < 0:
            messages.error(request, 'Variance HC must be non-negative.')
            return render(request, 'OpenPositions/OpenPositionEdit.html', {
                'memOrg': memOrg,
                'Departments': Departments,
                'Designations': Designations,
                'table_data': table_data,
                'error_message': 'Variance HC must be non-negative.',
                'open_position': open_position
            })

        # Update the open position
        open_position.Position = position
        open_position.OpenDepartment = open_department
        open_position.Job_Type = job_type
        open_position.Salary = salary
        open_position.Locations = locations
        open_position.Number = number
        open_position.Opened_On = opened_on_date
        open_position.Opened_Days = opened_days
        open_position.OrganizationID = OrganizationID
        open_position.CreatedByUserID = UserID
        open_position.CreatedByUsername = username
        open_position.save()

        messages.success(request, 'Open position updated successfully!')
        return redirect('OpenPositionList')

    context = {
        'memOrg': memOrg,
        'Departments': Departments,
        'Designations': Designations,
        'table_data': table_data,
        'error_message': request.GET.get('error_message'),
        'open_position': open_position
    }

    return render(request, 'OpenPositions/OpenPositionEdit.html', context)


from app.views import OrganizationList
import random

from InterviewAssessment.models import Assessment_Master

from urllib.parse import quote

from django.utils.text import slugify
from django.shortcuts import redirect, render
import logging

from app.models import OrganizationMaster

def get_organization_name_from_location(location_value):
    try:
        # Check if the location value is numeric (OrganizationID)
        if location_value.isdigit():
            organization = OrganizationMaster.objects.get(OrganizationID=int(location_value))
        else:
            # If it's not numeric, assume it's a name and search by that
            organization = OrganizationMaster.objects.get(OrganizationName=location_value)
        
        return organization.OrganizationName
    except:
        # Return a default value if no matching organization is found
        return "Unknown Organization"
    
    

from django.db.models import Q

from django.db.models import Q

import logging
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.text import slugify

logger = logging.getLogger(__name__)
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.db.models import Q
from django.db.models import F, Func, Value
from django.db.models.functions import Cast


def OpenPositionList(request):
    if 'OrganizationID' not in request.session or 'UserID' not in request.session:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    username = request.session.get("FullName")

    memOrg = OrganizationList(OrganizationID)

    Departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False)
    Lavelsdatas = LavelAdd.objects.filter(IsDelete=False)

    OrganizationID = request.GET.get('OrganizationID', OrganizationID)
    OpenDepartment = request.GET.get('OpenDepartment')
    Position = request.GET.get('Position')
    Levels = request.GET.getlist('Level')
    Status = request.GET.get('Status', 'open')

    if OrganizationID == '3':
        queryset = OpenPosition.objects.filter(IsDelete=False).order_by('-CreatedDateTime')
    else:
        queryset = OpenPosition.objects.filter(IsDelete=False, OrganizationID=OrganizationID).order_by('-CreatedDateTime')

    if OpenDepartment:
        queryset = queryset.filter(OpenDepartment=OpenDepartment)

    if Position:
        queryset = queryset.filter(Position=Position)

    if Levels:
        queryset = queryset.filter(Level__in=Levels)

    if Status == 'open':
        queryset = queryset.filter(Status=True)
    elif Status == 'close':
        queryset = queryset.filter(Status=False)

    for position in queryset:
        position_slug = slugify(position.Position)
        organization_full_name = get_organization_name_from_location(position.Locations)
        organization_slug = slugify(organization_full_name)
        slug_url = f"{position_slug}-{organization_slug}-{position.id}"
        position.slug_url = slug_url
        position.save()

    
    
   
   

    context = {
        'memOrg': memOrg,
        'Departments': Departments,
        'Designations': Designations,
        'Lavelsdatas': Lavelsdatas,
        'positions': queryset,
        
        'OrganizationID': OrganizationID,
        'selected_levels': Levels,
        'filtered_positions': queryset,
        'selected_position': Position,
        'selected_department': OpenDepartment,
        'selected_status': Status,
    }

    return render(request, 'OpenPositions/OpenPositionList.html', context)






from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import OpenPosition

         
def toggle_position_status(request, position_id):
    position = OpenPosition.objects.get(id=position_id)
    position.Status = not position.Status
    position.save()

   
    status_message = "Position successfully closed!" if not position.Status else "Position successfully reopened!"
    messages.success(request, status_message)

    return redirect('OpenPositionList')



                    




def OpenPositionDelete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    authorized_user_ids = ['20201212178780', '']  

    
    if UserID not in authorized_user_ids:
        
         return redirect(OpenPositionList)  

   
    id = request.GET.get('ID')
    try:
        position = OpenPosition.objects.get(id=id)
        position.IsDelete = True
        position.ModifyBy = UserID
        position.save()
    except OpenPosition.DoesNotExist:
       
        pass

    return redirect(OpenPositionList)


from django.shortcuts import redirect, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import requests
from datetime import datetime
import logging




from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Exportopen
from django.utils import timezone

def ExportOpenPosition(request):
    if 'OrganizationID' not in request.session or 'UserID' not in request.session:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    username = request.session.get("FullName")

    memOrg = OrganizationList(OrganizationID)

    Departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False)
    Lavelsdatas = LavelAdd.objects.filter(IsDelete=False)
    

    Locations = request.GET.get('Locations',OrganizationID)
   
   
    Status = request.GET.get('Status', 'open')  

    
    queryset = OpenPosition.objects.filter(IsDelete=False).order_by('-id')

    
    if Locations:
        queryset = queryset.filter(Locations=Locations)

  

    
    if Status == 'open':
        queryset = queryset.filter(Status=True)
    elif Status == 'close':
        queryset = queryset.filter(Status=False)



        
    if request.method == 'POST':
        remark_text = request.POST.get('Remark', '').strip()
        
        if remark_text:
            
            remark_instance, created = Exportopen.objects.get_or_create(
                OrganizationID=OrganizationID,  
                defaults={
                    'Remark': remark_text,
                    'CreatedBy': UserID
                }
            )
            if not created:
                remark_instance.Remark = remark_text
                remark_instance.ModifyBy = UserID
                remark_instance.ModifyDateTime = timezone.now()
                remark_instance.save()

            return redirect('ExportOpenPosition')  

    
    remark_instance = Exportopen.objects.filter(OrganizationID=OrganizationID).first()

    context = {
        'Departments': Departments,
        'Designations': Designations,
        'Lavelsdatas': Lavelsdatas,
        'memOrg': memOrg,
        'postionsexport': queryset,
        'remark_instance': remark_instance,
        'selected_status': Status,  
        'selected_location': int(Locations),
    }

    return render(request, 'OpenPositions/ExportOpenPosition.html', context)



from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import requests
from datetime import datetime
import logging


logger = logging.getLogger(__name__)

def PositionsPdf(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")

    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}

    selectedOrganizationID = request.GET.get('Locations', OrganizationID)
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={selectedOrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while fetching organization data: {e}")
        memOrg = []

    
    selected_organization = next((org for org in memOrg if str(org['OrganizationID']) == selectedOrganizationID), None)
    selectedOrganizationName = selected_organization['Organization_name'] if selected_organization else "Unknown Organization"

    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    
    organization = OrganizationMaster.objects.filter(OrganizationID=selectedOrganizationID).first()
    organization_logo = f"{base_url}{organization.OrganizationLogo}" if organization and organization.OrganizationLogo else None


    ids = request.GET.get('ids', '')
    ids = ids.split(',') if ids else []

    queryset = OpenPosition.objects.filter(IsDelete=False, id__in=ids)

    Locations = request.GET.get('Locations')
    Status = request.GET.get('Status', 'open')

    if Locations:
        queryset = queryset.filter(Locations=Locations)

    if Status == 'open':
        queryset = queryset.filter(Status=True)
    elif Status == 'close':
        queryset = queryset.filter(Status=False)

    
    for position in queryset:
        domain_code = position.Locations
        if domain_code:
            organization = OrganizationMaster.objects.filter(OrganizationDomainCode=domain_code, IsDelete=False).first()
            if organization and organization.OrganizationLogo:
                position.organization_logo = f"{base_url}{organization.OrganizationLogo}"
            else:
                position.organization_logo = None

    exportopen_data = Exportopen.objects.all()

    context = {
        'current_datetime': datetime.now().strftime('%d %B %Y %H:%M:%S'),
        'UserID': UserID,
        'selectedOrganizationID': selectedOrganizationID,
        'selectedOrganizationName': selectedOrganizationName,
        'filtered_positions': queryset,
        'exportopen_data': exportopen_data,
        'organization_logos':organization_logos
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'

    template = get_template('OpenPositions/PositionsPdf.html')
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse(f'We had some errors <pre>{html}</pre>')

    return response




# API 



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .models import OpenPosition  

@permission_classes([AllowAny])
class LocationListView(APIView):
    def get(self, request, format=None):
        locations = OpenPosition.objects.values_list('Locations', flat=True).distinct()
        return Response(locations, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class DepartmentListView(APIView):
    def get(self, request, format=None):
        departments = OpenPosition.objects.values_list('OpenDepartment', flat=True).distinct()
        return Response(departments, status=status.HTTP_200_OK)
    

@permission_classes([AllowAny])
class PositionListView(APIView):
    def get(self, request, format=None):
        positions = OpenPosition.objects.values_list('Position', flat=True).distinct()
        return Response(positions, status=status.HTTP_200_OK)



from .models import OpenPosition
from .serializers import OpenPositionSerializer  

@permission_classes([AllowAny])
class PositionListAllView(APIView):
    def get(self, request, format=None):
        positions = OpenPosition.objects.all()  
        serializer = OpenPositionSerializer(positions, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)
    





import msal
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import CareerResumeSerializer
from django.conf import settings

from app.models import MicrosoftCredentialsMail

def get_microsoft_credentials():
   
    cred = MicrosoftCredentialsMail.objects.first()
    
    
    if not cred:
        print("No Microsoft credentials found.")
        return None

    
    tenant_id = cred.tenant_id
    client_id = cred.client_id
    client_secret = cred.client_secret
    authority = cred.authority
    scope = cred.scope

    
    if isinstance(scope, str):
        scope = [scope]

    return tenant_id, client_id, client_secret, authority, scope


def get_access_token():
   
    tenant_id, client_id, client_secret, authority, scope = get_microsoft_credentials()

    if not client_id or not client_secret:
        print("Credentials not found.")
        return None

   
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
    )
    
    
    result = app.acquire_token_for_client(scopes=scope)
    
    
    if 'access_token' in result:
        return result['access_token']
    else:
        print(f"Error acquiring token: {result.get('error_description')}")
        return None


def send_email_via_graph(email, first_name, last_name, job_title):
   
    access_token = get_access_token()
    
    if access_token:
        sender_email = "noreply@nilehospitality.com"  
        email_subject = 'Thank you for your interest at Nile Hospitality'
        email_body = render_to_string('EmailTemp.html', {
            'first_name': first_name,
            'last_name': last_name,
            'job_title': job_title,
        })

        # Email data
        email_data = {
            "message": {
                "subject": email_subject,
                "body": {
                    "contentType": "HTML",
                    "content": email_body
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": email
                        }
                    }
                ]
            }
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        
        response = requests.post(
            f'https://graph.microsoft.com/v1.0/users/{sender_email}/sendMail',
            json=email_data,
            headers=headers
        )

        
        if response.status_code == 202:
            print("Email sent successfully!")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    else:
        print("Failed to acquire access token.")


@api_view(['POST'])
@permission_classes([AllowAny])
def submit_resume(request):
    print("Request received")
    serializer = CareerResumeSerializer(data=request.data)
    
    
    if serializer.is_valid():
        print("Serializer is valid")
        serializer.save()

        
        email = serializer.validated_data.get('email','')
        if email:
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name','')
            job_title = serializer.validated_data.get('job_title','')

            
            send_email_via_graph(email, first_name, last_name, job_title)

        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from app.models import OrganizationMaster
from .azure import download_blob


def resume_submission_page(request):
    
    op = request.GET.get('op')  # This will print the value of the query parameter
    # Your logic to get organization and designations
    orgs = OrganizationMaster.objects.filter()
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')

    context = {
        'orgs': orgs,
        'Designations': Designations,
        'op':op
        
    }

    return render(request, 'submit_resume.html', context)

import mimetypes
from django.http import HttpResponse, Http404


# def view_Resume(request):
#     ID = request.GET.get('ID')
#     file = CareerResume.objects.get(id=ID)
#     file_id = file.resume_url
  
#     file_name = file.resume
#     file_type, _ = mimetypes.guess_type(file_id)

#     if file_type is None:
#         file_type = 'application/octet-stream'
    
#     blob_content = download_blob(file_id)
    
#     if blob_content:
#         response = HttpResponse(blob_content.readall(), content_type=file_type)
#         response['Content-Disposition'] = f'inline; filename="{file_name}"'
#         return response
#     else:
#         raise Http404("File content not found.")
from django.http import HttpResponse, Http404
import mimetypes

def view_Resume(request):
    try:
        ID = request.GET.get('ID')
        file = CareerResume.objects.get(id=ID)
        file_id = file.resume_url
        file_name = file.resume

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
    
    except CareerResume.DoesNotExist:
        raise Http404("Resume not found.")
    except Exception as e:
        # You can log the error for debugging purposes or handle it differently
        raise Http404(f"An error occurred: {str(e)}")




from rest_framework import status
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .models import OpenPosition
from .serializers import JobDetailsSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def job_details_view(request):
    url_slug = request.GET.get('url_slug')
    
    if not url_slug:
        return Response({"error": "URL slug parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        spitVal = url_slug.split("-")
        spitVal = spitVal[len(spitVal)-1]
        job = OpenPosition.objects.filter(id=spitVal)
        # job = OpenPosition.objects.get(id__in=[
        #     obj.id for obj in OpenPosition.objects.all()
        #     # if obj.id == spitVal
        # ])
    except OpenPosition.DoesNotExist:
        return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)
    if job.exists():
        job = job.first()
        serializer = JobDetailsSerializer(job)
        return Response({
            "status": True,
            "result": [serializer.data]
        }, status=status.HTTP_200_OK)
    return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

# Api End Start resume sorting



import logging
from django.db.models import Q





from django.shortcuts import render, redirect
from django.db.models import Q
import logging
from collections import defaultdict
logger = logging.getLogger(__name__)



from django.shortcuts import render, redirect
from django.db.models import Q, Count, F
from collections import defaultdict
from django.core.paginator import Paginator

from django.http import JsonResponse
from django.db.models import Count




from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Prefetch
def get_department_action_counts(request):
    # Mapping designations to departments
    designation_to_department = {
        item['designations']: item['OnRollDepartmentMaster__DepartmentName']
        for item in OnRollDesignationMaster.objects.filter(IsDelete=False).values('designations', 'OnRollDepartmentMaster__DepartmentName')
    }

    # Fetching resumes with related actions
    CareesResumes = CareerResume.objects.filter(IsDelete=False).prefetch_related(
        Prefetch('actionsresume_set', queryset=ActionsResume.objects.all(), to_attr='actions')
    )

    # Initializing action counts
    department_action_counts = defaultdict(lambda: {
        'Shortlisted': 0,
        'Rejected': 0,
        'Hired': 0,
        'Recommended': 0,
        'Re_dial': 0,
        'New': 0
    })

    # Iterating through resumes to calculate action counts
    for resume in CareesResumes:
        designation = resume.job_title
        department = designation_to_department.get(designation, None)
        if department:
            actions = resume.actions
            if not actions:
                department_action_counts[department]['New'] += 1
            for action in actions:
                if action.action in department_action_counts[department]:
                    department_action_counts[department][action.action] += 1

    # Filtering out departments with no actions
    filtered_department_action_counts = {
        dept: actions for dept, actions in department_action_counts.items()
        if any(actions.values())
    }

    # Returning the JSON response
    return JsonResponse({
        'departments': list(filtered_department_action_counts.keys()),
        'department_action_counts': filtered_department_action_counts
    })


def ResumeShorting(request):
    if 'OrganizationID' not in request.session or 'UserID' not in request.session:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    username = request.session.get("FullName")
    
    memOrg = OrganizationList(OrganizationID)

    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).only('designations', 'OnRollDepartmentMaster__DepartmentName').order_by('designations')
    departmentsfilters = OnRollDepartmentMaster.objects.filter(IsDelete=False).only('DepartmentName').order_by('DepartmentName')
    
    selected_job_title = request.GET.get('job_title', 'All Designations')
    selected_location = request.GET.get('location','')
    selected_action = request.GET.get('action', '')
    selected_department = request.GET.get('department', 'All Departments')
    search_term = request.GET.get('search', '')
    CareesResumes = CareerResume.objects.filter(IsDelete=False).only('id', 'job_title', 'location')

    if selected_job_title and selected_job_title != 'All Designations':
        CareesResumes = CareesResumes.filter(job_title=selected_job_title)

    if selected_location and selected_location != 'All Locations':
        CareesResumes = CareesResumes.filter(location=selected_location)

    if search_term:
        CareesResumes = CareesResumes.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(phone__icontains=search_term) |
            Q(email__icontains=search_term) |
            Q(job_title__icontains=search_term)|
            Q(campaign_source__icontains=search_term)
        )

    if selected_department and selected_department != 'All Departments':
        Designations = Designations.filter(OnRollDepartmentMaster__DepartmentName=selected_department)
        filtered_designation_names = Designations.values_list('designations', flat=True)
        CareesResumes = CareesResumes.filter(job_title__in=filtered_designation_names)

    if selected_action and selected_action != 'All Actions':
        if selected_action == 'New':
            CareesResumes = CareesResumes.filter(
                Q(id__in=ActionsResume.objects.filter(action__in=['New', 'Recommended', 'Shortlisted', 'Hired']).values_list('ca_resume_id', flat=True)) |
                Q(id__in=CareerResume.objects.exclude(id__in=ActionsResume.objects.values_list('ca_resume_id', flat=True)).values_list('id', flat=True))
            )
        else:
            CareesResumes = CareesResumes.filter(
                id__in=ActionsResume.objects.filter(action=selected_action).values_list('ca_resume_id', flat=True)
            )

    # Calculate the action counts for each action type (Shortlisted, New, Recommended, etc.)
    action_counts = ActionsResume.objects.filter(
        ca_resume_id__in=CareesResumes.values_list('id', flat=True)
    ).values('action').annotate(count=Count('id'))

    action_counts_dict = {action['action']: action['count'] for action in action_counts}
    action_counts_dict.setdefault('Shortlisted', 0)
    action_counts_dict.setdefault('Rejected', 0)
    action_counts_dict.setdefault('Hired', 0)
    action_counts_dict.setdefault('Recommended', 0)
    action_counts_dict.setdefault('Re_dial', 0)

    # Count resumes with no actions
    action_resumes_ids = ActionsResume.objects.filter(
        ca_resume_id__in=CareesResumes.values_list('id', flat=True)
    ).values_list('ca_resume_id', flat=True).distinct()

    no_action_resumes_count = CareesResumes.exclude(id__in=action_resumes_ids).count()

    resumes_count = CareesResumes.count()

    paginator = Paginator(CareesResumes.order_by('-AppliedDate'), 20)
    page_number = request.GET.get('page')
    resumes_page = paginator.get_page(page_number)

    context = {
        'memOrg': memOrg,
        'departmentsfilters': departmentsfilters,
        'search_term': search_term,
        'Designations': Designations,
        'CareesResumes': resumes_page,
        'resumes_count': resumes_count,
        'action_counts': action_counts_dict,
        'no_action_resumes_count': no_action_resumes_count,
        'selected_job_title': selected_job_title,
        'selected_location': selected_location,
        'selected_action': selected_action,
        'selected_department': selected_department,
        'paginator': paginator
    }

    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'action_counts': action_counts_dict,
            'no_action_resumes_count': no_action_resumes_count,
            'resumes_count': resumes_count,
        })

    return render(request, 'Resume/ResumeShorting.html', context)





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CareerResume, ActionsResume
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def perform_action(request):
    if 'OrganizationID' not in request.session or 'UserID' not in request.session:
        return JsonResponse({'status': 'error', 'message': 'Session expired or not found'})

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    username = request.session.get("FullName")

    if request.method == 'POST':
        action = request.POST.get('action')
        resume_id = request.POST.get('resume_id')

        if not action or not resume_id:
            return JsonResponse({'status': 'error', 'message': 'Action or Resume ID not provided'})

        try:
            resume = CareerResume.objects.get(id=resume_id)
            existing_action = ActionsResume.objects.filter(ca_resume=resume).first()

            if existing_action:
                existing_action.action = action
                existing_action.ModifyBy = UserID
                existing_action.ModifyDateTime = timezone.now()
                existing_action.save()
                response_message = 'Action updated'
            else:
                ActionsResume.objects.create(
                    action=action,
                    ca_resume=resume,
                    OrganizationID=OrganizationID,
                    CreatedByUserID=UserID,
                    CreatedByUsername=username,
                    CreatedBy=UserID,
                )
                response_message = 'Action created'

            return JsonResponse({
                'status': 'success',
                'message': response_message,
                'action': action,
                'resume_id': resume_id,
                'username': username,
                'date': timezone.now().strftime('%d %b %Y')
            })

        except CareerResume.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Resume not found'})
        except Exception as e:
            logger.error(f"Error saving ActionsResume: {e}")
            return JsonResponse({'status': 'error', 'message': 'An error occurred'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

from django.shortcuts import render

def resume_shorting_view(request):
    actions = ['Shortlisted', 'Rejected', 'Hired', 'Recommended', 'Re_dial']
    context = {
        'actions': actions,
        # Add other context data here
    }
    return render(request, 'your_template_name.html', context)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import CareerResume

def get_resume_details(request, resume_id):
    resume = get_object_or_404(CareerResume, id=resume_id)
    data = {
        'first_name': resume.first_name,
        'last_name': resume.last_name,
        'phone': resume.phone,
        'job_title': resume.job_title,
        'location': resume.location,
        'email': resume.email,
        'resume_url': resume.resume_url,  
    }
    
    return JsonResponse(data)



from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

def edit_resume(request, resume_id):
    resume = get_object_or_404(CareerResume, id=resume_id)
    memOrg = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1).values(
            'OrganizationID', 'OrganizationName', 'OrganizationDomainCode', 'ShortDisplayLabel'
        )
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    if request.method == 'POST':
        resume.first_name = request.POST.get('first_name')
        resume.last_name = request.POST.get('last_name')
        resume.phone = request.POST.get('phone')
        resume.job_title = request.POST.get('job_title')
        resume.location = request.POST.get('location')
        resume.email = request.POST.get('email')
        
       
        
        resume.save()
        return redirect('ResumeShorting')  

    
    return render(request, 'edit_resume.html', {'resume': resume,'Designations':Designations,'memOrg':memOrg})





import qrcode
from io import BytesIO
from django.core.files import File
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import QRCode
from PIL import Image, ImageDraw, ImageFont
from hotelopsmgmtpy.GlobalConfig import MasterAttribute


def Qrcodegenerated(request):
    if 'OrganizationID' not in request.session or 'UserID' not in request.session:
        return JsonResponse({'status': 'error', 'message': 'Session expired or not found'})

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    username = request.session.get("FullName")
    
    if request.method == 'POST':
        qr_type = request.POST.get('type')
        user = request.user
        host = MasterAttribute.Host
        
        url = f"https://careers.nilehospitality.com/apply.php?s-{qr_type}"
        
        
        # data = f"{qr_type} for {user.username} - {url}"
        data = url
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        
        img = qr.make_image(fill='black', back_color='white')

        
        img = img.convert("RGB")
        draw = ImageDraw.Draw(img)
        font_size = 2 
        font = ImageFont.truetype("arial.ttf", font_size)  
        
        text = f"{qr_type}"

        
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        
        image_width, image_height = img.size
        position = ((image_width - text_width) // 2, image_height - text_height - 10)
        draw.text(position, text, font=font, fill=(0, 0, 0))

        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        
        file_name = f'{qr_type}.png'
        file = File(buffer, name=file_name)

        
        qr_instance = QRCode.objects.create(
            CreatedBy=UserID,
            CreatedByUsername=username,
            OrganizationID=OrganizationID,
            qr_type=qr_type,
            qr_code=file
        )

        
        response = redirect('qr_download', qr_instance.id)
        return response

    return render(request, 'Resume/Qrcodegenerated.html')


from django.http import FileResponse

def qr_download(request, qr_id):
    qr_code_instance = QRCode.objects.get(id=qr_id)
    response = FileResponse(qr_code_instance.qr_code.open(), as_attachment=True)
    return response










from django.utils import timezone
from django.http import JsonResponse
from .models import OpenPosition, NotificationSchedule
from django.shortcuts import render, get_object_or_404, redirect
from .models import NotificationSchedule, OpenPosition


def Notification_Schedule(request):
    if 'OrganizationID' not in request.session or 'UserID' not in request.session:
        return JsonResponse({'status': 'error', 'message': 'Session expired or not found'})

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    username = request.session.get("FullName")
    Departmentsfilter = OnRollDepartmentMaster.objects.filter(IsDelete=False).order_by('DepartmentName')
    levelfilters = LavelAdd.objects.filter(IsDelete=False).order_by('lavelname')
    notification_id = request.POST.get('notification_id')
    position_id = request.POST.get('position_id') or request.GET.get('ID')

    if request.method == 'POST':
        
        Departmetdata = request.POST.getlist('Departmetdata')  
        levels_for = request.POST.getlist('levels_for')  
        Statusschedule = request.POST.get('Statusschedule', 'off') == 'on'
        Schedule_date = request.POST.get('Schedule_date')
        open_position = get_object_or_404(OpenPosition, id=position_id)

        if notification_id:
            notification = get_object_or_404(NotificationSchedule, id=notification_id)
            notification.Departmetdata = ','.join(Departmetdata) 
            notification.levelsfor = ','.join(levels_for)  
            notification.Schedule_date = Schedule_date
            notification.Statusschedule = Statusschedule
            notification.ModifyBy = UserID
            notification.ModifyDateTime = timezone.now()
            notification.save()
        else:
            NotificationSchedule.objects.create(
                open_positions=open_position,
                Departmetdata=','.join(Departmetdata),  
                levelsfor=','.join(levels_for),  
                Schedule_date=Schedule_date,
                Statusschedule=Statusschedule,
                OrganizationID=OrganizationID,
                CreatedByUsername=username,
                CreatedBy=UserID,
            )

        return redirect('Notification_Schedule_list')

    if not position_id:
        return JsonResponse({'status': 'error', 'message': 'Position ID is required'})

    position = get_object_or_404(OpenPosition, id=position_id)
    notification = NotificationSchedule.objects.filter(open_positions=position).first()

    
    selected_departments = notification.Departmetdata.split(',') if notification and notification.Departmetdata else []
    selected_levels = notification.levelsfor.split(',') if notification and notification.levelsfor else []

    return render(request, 'OpenPositions/Notification_Schedule.html', {
        'notification': notification,
        'position': position,
        'Departmentsfilter': Departmentsfilter,
        'levelfilters': levelfilters,
        'selected_departments': selected_departments,
        'selected_levels': selected_levels,
    })


from django.http import JsonResponse
from django.shortcuts import get_object_or_404

import requests
from django.conf import settings

import requests
# def send_sms(phone_number, message):
#     url = "https://rcmapi.instaalerts.zone/services/rcm/sendMessage"
#     api_key = "Bearer VD9PURH2WUK2OkNln9xatw=="  # Replace with your actual API key
    
#     payload = {
#         "phone_number": phone_number,
#         "message": message,
#         "api_key": api_key
#     }

#     headers = {
#         "Content-Type": "application/json",
#     }

#     response = requests.post(url, json=payload, headers=headers)
    
#     if response.status_code == 200:
#         return True
#     else:
#         print(f"Error sending SMS: {response.text}")
#         return False




from app.models import WhatsappSmsConfig
import requests
import json

# def send_sms(phone_number, message):
#     url = "https://rcmapi.instaalerts.zone/services/rcm/sendMessage"
#     api_key = "Bearer dCGW2gkdS6Q6WOt9jyIqaA=="  

#     payload = {
#         "message": {
#             "channel": "WABA",
#             "content": {
#                 "preview_url": False,  
#                 "type": "MEDIA_TEMPLATE",
#                 "mediaTemplate": {
#                     "templateId": "jobopenhtlempnotificationdyamicwithurl",
#                     "bodyParameterValues": {
#                         "0": "Assistant Manager Front Office",
#                         "1": "https://careersatnile.com/jobshare.php/assistant-manager--front-office-nile-hotel-management-company-2867?s=whatsapp_26_4"
#                     },
#                     "buttons": {
#                         "actions": [
#                             {
#                                 "type": "url",
#                                 "index": "0",
#                                 "payload": "assistant-manager--front-office-nile-hotel-management-company-2867?s=whatsapp_26_4"
#                             }
#                         ]
#                     },
#                     "media": {
#                         "type": "image",
#                         "url": "https://hotelopsblob.blob.core.windows.net/nilecareer/0/NileHMGMT_Assistant_Manager_-_Front_Office.jpg"
#                     }
#                 },
#                 "shorten_url": False  
#             },
#             "recipient": {
#                 "to": phone_number,
#                 "recipient_type": "individual",
#                 "reference": {
#                     "cust_ref": "1",
#                     "messageTag1": "1",
#                     "conversationId": "1"
#                 }
#             },
#             "sender": {
#                 "from": "919251657048"
#             },
#             "preferences": {
#                 "webHookDNId": "1001"
#             }
#         },
#         "metaData": {
#             "version": "v1.0.9"
#         }
#     }

#     headers = {
#         "Content-Type": "application/json",
#         "Authentication": api_key
#     }

#     try:
#         response = requests.post(url, json=payload, headers=headers)
#         response.raise_for_status()

#         response_data = response.json()
#         mid = response_data.get('mid')  
#         return {"status": "success", "mid": mid, "payload": json.dumps(payload)}  # Include payload in the response

#     except requests.exceptions.RequestException as e:
#         return {"status": "error", "mid": None, "payload": json.dumps(payload)}  # Include payload even on error
    
# def send_notification_sms(request, notification_id):
    
#     notification = get_object_or_404(NotificationSchedule, id=notification_id)

    
#     phone_number = '+919644580860'  
#     employee_name = 'Bhupendra'  
    
#     message = f"Hello {employee_name}, this is a notification regarding your department schedule."

    
#     success = send_sms(phone_number, message)
    
#     if success:
#         return JsonResponse({'status': 'success', 'message': 'SMS sent successfully!'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Failed to send SMS.'})

# In your views.py
# def send_notification_sms(request, notification_id):
#     if 'OrganizationID' not in request.session:
#         return redirect('MasterAttribute.Host')

#     OrganizationID = request.session.get("OrganizationID")
#     UserID = request.session.get("UserID")
#     username = request.session.get("FullName")
#     notification = get_object_or_404(NotificationSchedule, id=notification_id)

#     employee_details = get_employee_details_with_mobile()

#     if not employee_details:
#         return JsonResponse({'status': 'error', 'message': 'Employee not found.'})
#     for employee in employee_details:
#          EmpID = employee['EmpID']
#          phone_number = employee['MobileNumber']
#          employee_name = f"{employee['FirstName']} {employee['LastName']}"
#          department = employee['Department']
#          designation = employee['Designation']
#          level = employee['Level']
   

#     message = f"Hello {employee_name}, this is a notification regarding your department schedule."

#     # Send SMS and capture the response
#     sms_response = send_sms(phone_number, message)
#     mid = sms_response.get("mid")
#     status = sms_response.get("status")

#     # Save details to NotificationHistory
#     NotificationHistory.objects.create(
#         notification=notification,
#         phone_number=phone_number,
#         EmpID=EmpID,
#         employee_name=employee_name,
#         department=department,
#         designation=designation,
#         level=level,
#         message=message,
#         status=status,
#         CreatedBy=UserID,
#         CreatedByUsername=username,
#         message_id=mid  # Save the 'mid'
#     )

#     if status == "success":
#         return JsonResponse({'status': 'success', 'message': 'SMS sent successfully!'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Failed to send SMS.'})

from Open_position.utils import generate_position_image


from django.utils.text import slugify

from django.utils.text import slugify

def get_notification_details(notification_id):
    notification = get_object_or_404(NotificationSchedule, id=notification_id, IsDelete=False)

    notification_data = {
        "id": notification.id,
        "department": notification.Departmetdata,
        "levels": notification.levelsfor,
        "status": notification.Statusschedule,
        "schedule_date": notification.Schedule_date,
        "organization_id": notification.OrganizationID,
        "created_by_username": notification.CreatedByUsername,
        "created_by": notification.CreatedBy,
        "created_date_time": notification.CreatedDateTime,
        "modify_by": notification.ModifyBy,
        "modify_date_time": notification.ModifyDateTime,
    }

    # Slugify components
    position_slug = slugify(notification.open_positions.Position)
    organization_full_name = notification.open_positions.get_organization_full_name()
    organization_slug = slugify(organization_full_name)

    # Construct slug URL
    slug_url = f"{position_slug}-{organization_slug}-{notification.open_positions.id}"

    open_positions_data = {
        "id": notification.open_positions.id,
        "position_name": notification.open_positions.Position,
        "PositionImage": notification.open_positions.PositionImage,
        "Locations": organization_full_name,
        "slug_url": slug_url  # Use consistent slug formatting
    }

    return notification_data, open_positions_data




import re
import requests
import json




import json
import requests

def send_sms(phone_number, notification_id, message, request, EmpID):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    try:
        # Get notification details
        notification_data, open_positions_data = get_notification_details(notification_id)
        
        # Extract position and slug details
        position_name = open_positions_data.get("position_name")
        slug_url = open_positions_data.get("slug_url")
        PositionImage = open_positions_data.get("PositionImage")
        
        # Ensure config exists
        config = WhatsappSmsConfig.objects.filter(OrganizationID=OrganizationID, IsDelete=False).first()
        if not config:
            return {"status": "error", "message": "No configuration found for the given OrganizationID"}

       
        resume_url = f"https://HotelOps.in:8080/Open_position/submit-resume/?{slug_url}&s=whatsapp_{EmpID}"

       
        payload = {
            "message": {
                "channel": "WABA",
                "content": {
                    "type": "MEDIA_TEMPLATE",
                    "mediaTemplate": {
                        "templateId": config.template_id,
                        "bodyParameterValues": {
                            "0": position_name,  
                            "1": resume_url  
                        },
                        "buttons": {
                            "actions": [
                                {
                                    "type": "url",
                                    "index": "0",
                                    "payload": resume_url  
                                }
                            ]
                        },
                        "media": {
                            "type": "image",
                            "url": f"https://hotelopsdevstorage.blob.core.windows.net/data/{PositionImage}"  # Position image
                        }
                    }
                },
                "recipient": {
                    "to": phone_number
                },
                "sender": {
                    "from": config.sender
                }
            }
        }

        # Send the request to the SMS API
        headers = {
            "Content-Type": "application/json",
            "Authentication": config.api_key
        }

        response = requests.post(config.url, json=payload, headers=headers)
        response.raise_for_status()  # Check if the response is successful

        # Handle the response
        response_data = response.json()
        mid = response_data.get('mid')  # Message ID
        return {"status": "success", "mid": mid, "payload": json.dumps(payload)}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e), "payload": json.dumps(payload)}

from HumanResources.views import get_employee_details_with_mobile







from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import NotificationSchedule,NotificationHistory
from HumanResources.models import EmployeePersonalDetails, EmployeeWorkDetails
def get_employee_details_with_mobile():
    
    personal_details = EmployeePersonalDetails.objects.filter(IsDelete=False).values(
        'EmpID', 'FirstName', 'LastName', 'MobileNumber'
    )

   
    work_details = EmployeeWorkDetails.objects.filter(IsDelete=False).values(
        'EmpID', 'Department', 'Designation', 'Level'
    )

   
    work_details_dict = {wd['EmpID']: wd for wd in work_details}

    
    employee_details = []
    for pd in personal_details:
       
        wd = work_details_dict.get(pd['EmpID'], {})

        
        employee_details.append({
            'EmpID': pd['EmpID'],
            'FirstName': pd['FirstName'],
            'LastName': pd['LastName'],
            'MobileNumber': pd['MobileNumber'],
            'Department': wd.get('Department', 'N/A'),
            'Designation': wd.get('Designation', 'N/A'),
            'Level': wd.get('Level', 'N/A')
        })

    # Print the details for each employee (optional, as per your request)
    # for employee in employee_details:
    #     print(
    #         f"EmpID: {employee['EmpID']}, Name: {employee['FirstName']} {employee['LastName']}, "
    #         f"Mobile Number: {employee['MobileNumber']}, Department: {employee['Department']}, "
    #         f"Designation: {employee['Designation']}, Level: {employee['Level']}"
    #     )

    return employee_details








import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

from django.shortcuts import get_object_or_404
from .models import NotificationSchedule





def send_notification_sms(request, notification_id):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    username = request.session.get("FullName")

   
    notification = get_object_or_404(NotificationSchedule, id=notification_id)
    position_name = notification.open_positions.Position  

    
    employee_details = get_employee_details_with_mobile()
    if not employee_details:
        return JsonResponse({'status': 'error', 'message': 'No employees found.'})

   
    notification_department = notification.Departmetdata.split(",") if notification.Departmetdata else []
    notification_level = notification.levelsfor.split(",") if notification.levelsfor else []

    notification_results = []

    for employee in employee_details:
        EmpID = employee['EmpID']
        phone_number = employee['MobileNumber']
        employee_name = f"{employee['FirstName']} {employee['LastName']}"
        department = employee['Department']
        designation = employee['Designation']
        level = employee['Level']

        
        if (not notification_department or department in notification_department) and \
           (not notification_level or level in notification_level):
            
            
            message = f"Hello {employee_name}, your department is {department} with designation {designation}."

           
            sms_response = send_sms(phone_number, notification_id, message, request, EmpID)
            payload_json = sms_response.get("payload", None)  
            mid = sms_response.get("mid", None)
            status = sms_response.get("status", "error")

            
            NotificationHistory.objects.create(
                notification=notification,
                phone_number=phone_number,
                EmpID=EmpID,
                employee_name=employee_name,
                department=department,
                designation=designation,
                level=level,
                message=payload_json,
                status=status,
                CreatedBy=UserID,
                CreatedByUsername=username,
                message_id=mid
            )

            notification_results.append({
                'EmpID': EmpID,
                'phone_number': phone_number,
                'status': status,
                'message_id': mid
            })

            
            if status == "success":
                print(f"Notification sent successfully to {employee_name} ({department}, {designation}, {level})")
            else:
                print(f"Failed to send notification to {employee_name} ({department}, {designation}, {level})")

    
    success_count = sum(1 for result in notification_results if result['status'] == "success")
    error_count = len(notification_results) - success_count

    

   
    return JsonResponse({
        'status': 'complete',
        'message': f"Notifications sent: {success_count} success, {error_count} errors.",
        'position_name': position_name,
        'details': notification_results
    })



def Notification_Schedule_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    Notifications = NotificationSchedule.objects.filter(OrganizationID=OrganizationID, IsDelete=False).order_by('-id')
    open_positions = OpenPosition.objects.filter(OrganizationID=OrganizationID,IsDelete=False).order_by('-id')
    
    if OrganizationID == '3':  
        Notifications = NotificationSchedule.objects.filter(IsDelete=False).order_by('-id')
        open_positions = OpenPosition.objects.filter(IsDelete=False).order_by('-id')
    
    
    context = {
        'Notifications': Notifications,
        'OpenPositions': open_positions,  
    }
    return render(request, 'OpenPositions/Notification_Schedule_list.html', context)




def delete_notification_schedule(request, id):
    if 'OrganizationID' not in request.session or 'UserID' not in request.session:
        return JsonResponse({'status': 'error', 'message': 'Session expired or not found'})

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    notification = get_object_or_404(NotificationSchedule, id=id)
    notification.IsDelete = True
    notification.ModifyBy=UserID
    notification.save()
    return redirect('Notification_Schedule_list')

