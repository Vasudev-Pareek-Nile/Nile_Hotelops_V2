
from Manning_Guide.models import OnRollDepartmentMaster,OnRollDesignationMaster, OnRollDivisionMaster
from HumanResources.models import EmployeeWorkDetails
from .models import *
from Leave_Management_System.models import  Leave_Type_Master
from django.http import JsonResponse
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from app.views import EmployeeDataSelect
from Manning_Guide.models import LavelAdd
from datetime import date
from InterviewAssessment.models import Assessment_Master

# -- Global Apis for Manning Guide App
def Show_Division_Api(request):
    Divisionfilter = OnRollDivisionMaster.objects.filter(IsDelete=False).order_by('DivisionName')
    data = Divisionfilter.values("id", "DivisionName")
    return JsonResponse(list(data), safe=False)

def Show_Department_Api(request):
    Departmentsfilter = OnRollDepartmentMaster.objects.filter(IsDelete=False).order_by('DepartmentName')
    data = Departmentsfilter.values("id", "DepartmentName")
    return JsonResponse(list(data), safe=False)


def Show_Designations_Complete_Api(request):
    designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by("designations")
    data = designations.values("id", "designations")
    return JsonResponse(list(data), safe=False)


def Show_Designations_Api(request):
    dept_id = request.GET.get("department_id")
    # print("the department id is:", dept_id)
    if dept_id:
        designations = OnRollDesignationMaster.objects.filter(
            IsDelete=False,
            OnRollDepartmentMaster=dept_id
        ).order_by("designations")
    else:
        designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by("designations")

    data = designations.values("id", "designations")
    return JsonResponse(list(data), safe=False)



#  Helper functions to get names by ID
def get_division_name(divi_id):
    division = OnRollDivisionMaster.objects.filter(IsDelete=False, id=divi_id).values('DivisionName').first()
    return division['DivisionName'] if division else None


def get_department_name(dept_id):
    department = OnRollDepartmentMaster.objects.filter(IsDelete=False, id=dept_id).values('DepartmentName').first()
    return department['DepartmentName'] if department else None


def get_department_name_by_division_name(DiviName):
    # returns a list of department names in the division
    return list(
        OnRollDepartmentMaster.objects.filter(
            OnRollDivisionMaster__DivisionName=DiviName, IsDelete=False
        ).values_list('DepartmentName', flat=True)
    )


def get_designation_name(dept_id):
    department = OnRollDesignationMaster.objects.filter(IsDelete=False, id=dept_id).values('designations').first()
    return department['designations'] if department else None


# API wrapper for frontend use -- getting By Id
def Show_Division_By_Id_Api(request, divi_id):
    division_name = get_division_name(divi_id)
    return JsonResponse({'DivisionName': division_name} if division_name else {}, safe=False)


def Show_Department_By_Id_Api(request, dept_id):
    department_name = get_department_name(dept_id)
    return JsonResponse({'DepartmentName': department_name} if department_name else {}, safe=False)


def Show_Designations_By_Id_Api(request, desi_id):
    designations = OnRollDesignationMaster.objects.filter(IsDelete=False, id=desi_id).values("designations")
    return JsonResponse(list(designations), safe=False)


# API wrapper for frontend use -- getting By Name
def Show_Department_By_DivisionName_Api(request, DivisionName=None):
    if DivisionName:
        departments = get_department_name_by_division_name(DivisionName)
    else:
        # Return all departments
        departments = OnRollDepartmentMaster.objects.filter(IsDelete=False).order_by('DepartmentName').values_list("DepartmentName", flat=True)
    
    # Convert queryset/list of strings to list of objects
    data = [{"DepartmentName": dept} for dept in departments]
    return JsonResponse(data, safe=False)


# -- in bulk name
def get_department_bulk_names(ids):
    return list(
        OnRollDepartmentMaster.objects.filter(IsDelete=False, id__in=ids)
        .values_list('DepartmentName', flat=True)
    )

def get_designation_bulk_names(ids):
    return list(
        OnRollDesignationMaster.objects.filter(IsDelete=False, id__in=ids)
        .values_list('designations', flat=True)
    )




# -- Global Api for Organization List
def OrganizationList_Api(request, OrganizationID):
    try:
        if OrganizationID == "3":
            organizations = OrganizationMaster.objects.filter(
                IsDelete=False, IsNileHotel=1, Activation_status=1
            ).values('OrganizationID', 'OrganizationName','ShortDisplayLabel')
        else:
            organizations = OrganizationMaster.objects.filter(
                IsDelete=False, IsNileHotel=1, Activation_status=1,
                OrganizationID=OrganizationID
            ).values('OrganizationID', 'OrganizationName','ShortDisplayLabel')
        
        return JsonResponse(list(organizations), safe=False)
    except Exception as e:
        print(f"An error occurred: {e}")
        return JsonResponse({"error": str(e)}, status=500)




# -- Global Api for Month List
def MonthList_Api(request):
    months = [
        {"id": 1, "name": "January"},
        {"id": 2, "name": "February"},
        {"id": 3, "name": "March"},
        {"id": 4, "name": "April"},
        {"id": 5, "name": "May"},
        {"id": 6, "name": "June"},
        {"id": 7, "name": "July"},
        {"id": 8, "name": "August"},
        {"id": 9, "name": "September"},
        {"id": 10, "name": "October"},
        {"id": 11, "name": "November"},
        {"id": 12, "name": "December"},
    ]
    return JsonResponse(list(months), safe=False)


# -- Employee List Api
def EmployeeStatusList_Api(request):
    Status = [
        {"id": 'Confirmed', "name": "Confirmed"},
        {"id": 'Not Confirmed', "name": "Not Confirmed"},
        {"id": 'On Probation', "name": "On Probation"},
        {"id": 'Absconding', "name": "Absconding"},
        {"id": 'Archive', "name": "Archive"},
        {"id": 'F&F Completed', "name": "F&F Completed"},
        {"id": 'F&F In Completed', "name": "F&F In Completed"},
        {"id": 'F&F In process', "name": "F&F In process"},
        {"id": 'Left', "name": "Left"},
        {"id": 'Resigned', "name": "Resigned"},
        {"id": 'Terminate', "name": "Terminate"}
    ]
    return JsonResponse(list(Status), safe=False)



#  Complete Employee Data by some info
@api_view(['GET'])
def EmployeeDataApi(request):
    # Get query params
    OrganizationID = request.GET.get('OrganizationID')
    EmployeeCode = request.GET.get('EmployeeCode')
    Designation = request.GET.get('Designation')
    ReportingtoDesignation = request.GET.get('ReportingtoDesignation')
    
    data = EmployeeDataSelect(
        OrganizationID=OrganizationID,
        EmployeeCode=EmployeeCode,
        Designation=Designation,
        ReportingtoDesignation=ReportingtoDesignation
    )
    return Response({'status': True, 'data': data})


# Get Employee ID via Employee Code and organization id
@api_view(['GET'])
def Leave_Type_Data_Api(request):
    Leave_Data = Leave_Type_Master.objects.filter(
        Is_Active=True,
        IsDelete=False
    ).order_by('id').values("id","Type")
    return Response({'status': True, 'Leave_Data': Leave_Data})


@api_view(['GET'])
def Lavel_Show_Data_Api(request):
    Levels = LavelAdd.objects.filter(IsDelete=False).values_list("lavelname", flat=True)
    return Response({'status': True, 'Levels': Levels})


@api_view(['GET'])
def Lavel_Show_Data_Api(request):
    levels_qs = LavelAdd.objects.filter(IsDelete=False).values_list("lavelname", flat=True)
    
    levels_list = list(levels_qs)
    
    return Response({'status': True, 'Levels': levels_list})


# -------- Leave Type Name
@api_view(['GET'])
def Leave_Type_Name_Api(request, LeaveID):
    if LeaveID:
        Leave_Data = Leave_Type_Master.objects.filter(
            Is_Active=True,
            IsDelete=False,
            id=LeaveID
        ).order_by('id').values('id', 'Type')  # converts to list of dicts
    else:
        Leave_Data = Leave_Type_Master.objects.filter(
            Is_Active=True,
            IsDelete=False
        ).order_by('id').values('id', 'Type')
    
    return Response({'status': True, 'Leave_Data': list(Leave_Data)})



# ----------- New Joiners Api
def New_Joiners_Api(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    OID = request.GET.get('OID')
    S_LoiStatus = request.GET.get('LoiStatus')
    S_Level = request.GET.get('Level')
    # print("the first levels are here", S_Level)


    if AccessToken:
        if AccessToken == Fixed_Token:
            pass
        else:
            # return Response({'error': 'Please Provide The Correct Token, Token Not Match.'}, status)
            return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)
    else:
        # return Response({'error': 'Token Not Found, Please Provide Correct Token.'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)

    if not OID:
        # return Response({"error": "OrganizationID (OID) is required"}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)
    

    if not OrganizationMaster.objects.filter(OrganizationID=OID).exists():
        # return Response({"error": f"Invalid OrganizationID: {organization_id}"}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({"error": f"Invalid Organization Name"}, status=400)
    
    try:
        filters = {
            'IsDelete': False,
            'LastApporvalStatus': 'Approved',
            'ProposedDOJ__gt': date.today()
        }

        # If OID != 3
        if OID and OID != '3':
            filters['AppliedFor'] = OID

        if not S_LoiStatus:
            LoiStatus = ['Accepted', 'Shared']
        else:
            LoiStatus = [LS.strip() for LS in S_LoiStatus.split(',')]


        # print("Multiselect Loi Status are here::", LoiStatus)
        filters['LOIStatus__in'] = LoiStatus


        if S_Level:
            levels = [lvl.strip() for lvl in S_Level.split(',')]
            # print("Multiselect level are here::", levels)
            filters['Level__in'] = levels

        # Fetch joiners
        Joinnee = (Assessment_Master.objects
        .filter(**filters)
        .order_by('ProposedDOJ')
        .values(
            "Name", "Department", "position", "Level",
            "LOIStatus", "AppliedFor", "ProposedDOJ"
        ))

        joiners_list = list(Joinnee)

        # Fetch organization names for the AppliedFor IDs
        org_ids = {j['AppliedFor'] for j in joiners_list if j['AppliedFor']}
        orgs = OrganizationMaster.objects.filter(
            OrganizationID__in=org_ids,
            IsDelete=False,
            IsNileHotel=1,
            Activation_status=1
        ).values("OrganizationID", "ShortDisplayLabel")

        # Map org IDs to names
        org_map = {o["OrganizationID"]: o["ShortDisplayLabel"] for o in orgs}

        # Add organization name to each joiner
        for j in joiners_list:
            j["ShortDisplayLabel"] = org_map.get(j["AppliedFor"], "")

        return JsonResponse(joiners_list, safe=False)

    except Exception as e:
        print(f"Error in New_Joiners_Api: {e}")
        return JsonResponse({"error": str(e)}, status=500)



