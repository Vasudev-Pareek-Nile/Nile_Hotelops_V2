
from Manning_Guide.models import OnRollDepartmentMaster,OnRollDesignationMaster, OnRollDivisionMaster
from HumanResources.models import EmployeeWorkDetails, Salary_Detail_Master, EmployeeBankInformationDetails, EmployeePersonalDetails
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
    if DivisionName and DivisionName != "all":
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


# -- Global Api for Organization List
def OrganizationList_All_Mobile_Api(OrganizationID):
    print("OrganizationList_All_Api: OID:-:",OrganizationID)
    try:
        qs = OrganizationMaster.objects.filter(
            IsDelete=False,
            IsNileHotel=1,
            Activation_status=1
        ).values('OrganizationID', 'OrganizationName', 'ShortDisplayLabel')

        # Convert QuerySet to list
        organizations = list(qs)

        # If "all" (or super org like 3), add All option
        if OrganizationID in ["all", "3"]:
            organizations.insert(0, {
                "OrganizationID": "all",
                "OrganizationName": "All",
                "ShortDisplayLabel": "All"
            })
        else:
            organizations = [
                org for org in organizations
                if str(org["OrganizationID"]) == str(OrganizationID)
            ]

        return JsonResponse(organizations, safe=False)

    except Exception as e:
        print(f"An error occurred: {e}")
        return JsonResponse({"error": str(e)}, status=500)


from django.http import JsonResponse

def get_organization_list(OrganizationID):
    qs = OrganizationMaster.objects.filter(
        IsDelete=False,
        IsNileHotel=1,
        Activation_status=1
    ).values('OrganizationID', 'OrganizationName', 'ShortDisplayLabel')

    organizations = list(qs)

    if OrganizationID in ["all", "All", "3"]:
        organizations.insert(0, {
            "OrganizationID": "all",
            "OrganizationName": "All",
            "ShortDisplayLabel": "All"
        })
    else:
        organizations = [
            org for org in organizations
            if str(org["OrganizationID"]) == str(OrganizationID)
        ]

    return organizations




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

    if AccessToken:
        if AccessToken == Fixed_Token:
            pass
        else:
            # return Response({'error': 'Please Provide The Correct Token, Token Not Match.'}, status)
            return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)
    else:
        # return Response({'error': 'Token Not Found, Please Provide Correct Token.'}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)

    # -------------------------------
    # NEW ACCESS CHECK
    UserID = request.GET.get("UserID")
    ALLOWED_USER_IDS = ['20201212180048', '20251209112591']

    if not UserID:
        return JsonResponse({'error': 'UserID is required'}, status=400)

    if UserID not in ALLOWED_USER_IDS:
        return JsonResponse({'error': 'Not found'}, status=404)
    # -------------------------------

    OID = request.GET.get('OID')
    S_LoiStatus = request.GET.get('LoiStatus')
    S_Level = request.GET.get('Level')

    if not OID:
        # return Response({"error": "OrganizationID (OID) is required"}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)
    
    if OID != '333333':
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
        if OID and OID != '333333':
            print("yes iam here")
            filters['AppliedFor'] = OID
        else:
            print("Not avail....")
            

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

    # return JsonResponse({"error": f"No Data Found"}, status=400)




# ----------- Resignation_Mobile_Api

from datetime import date

def calculate_tenure(doj, dor):
    if not doj or not dor:
        return ""

    # Convert to date if it's datetime
    if hasattr(doj, 'date'):
        doj = doj.date()
    if hasattr(dor, 'date'):
        dor = dor.date()

    # Calculate year and month difference
    years = dor.year - doj.year
    months = dor.month - doj.month

    if dor.day < doj.day:
        months -= 1  # Adjust if incomplete month

    if months < 0:
        years -= 1
        months += 12

    # Always show both years and months
    year_text = f"{years} Year" + ("s" if years != 1 else "")
    month_text = f"{months} Month" + ("s" if months != 1 else "")

    return f"{year_text} {month_text}"


def format_date(date_obj):
    if not date_obj:
        return ""
    return f"{date_obj.day:02d} {date_obj.strftime('%b')} {str(date_obj.year)[-2:]}"


from EmpResignation.models import EmpResigantionModel



def tenure_in_months(doj, dor):
    if hasattr(doj, 'date'):
        doj = doj.date()
    if hasattr(dor, 'date'):
        dor = dor.date()

    years = dor.year - doj.year
    months = dor.month - doj.month

    if dor.day < doj.day:
        months -= 1

    if months < 0:
        years -= 1
        months += 12

    return years * 12 + months



def Resignation_Mobile_Api(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    # Token checks
    if not AccessToken:
        return JsonResponse({'error': 'Token not found'}, status=400)
    if AccessToken != Fixed_Token:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    
    # -------------------------------
    # NEW ACCESS CHECK
    # UserID = request.GET.get("UserID")
    # ALLOWED_USER_IDS = ['20201212180048', '20251209112591']

    # if not UserID:
    #     return JsonResponse({'error': 'UserID is required'}, status=400)

    # if UserID not in ALLOWED_USER_IDS:
    #     return JsonResponse({'error': 'Invalid UserID'}, status=404)
    # -------------------------------

    OID = request.GET.get('OID')
    S_Level = request.GET.get('Level')
    
    # OID checks
    if not OID:
        return JsonResponse({'error': 'OID is required'}, status=400)
    if OID != '333333' and not OrganizationMaster.objects.filter(OrganizationID=OID).exists():
        return JsonResponse({'error': 'Invalid OrganizationID'}, status=400)

    try:
        filters = {'IsDelete': False}
        if OID != '333333':
            filters['OrganizationID'] = OID
            
        if S_Level:
            levels = [lvl.strip() for lvl in S_Level.split(',')]

            if levels: 
                filters['Level__in'] = levels

        Resignations = (
            EmpResigantionModel.objects
            .filter(**filters)
            .order_by('Date_Of_res')
            .values(
                "Name", "Dept", "Designation", "DOJ",
                "OrganizationID", "Date_Of_res",'Emp_Code','Level'
            )
        )

        Resignations_list = list(Resignations)

        # Fetch org short names
        applied_ids = {j['OrganizationID'] for j in Resignations_list}
        orgs = OrganizationMaster.objects.filter(
            OrganizationID__in=applied_ids,
            IsDelete=False,
            IsNileHotel=1,
            Activation_status=1
        ).values("OrganizationID", "ShortDisplayLabel")

        org_map = {o["OrganizationID"]: o["ShortDisplayLabel"] for o in orgs}
        
                
        equal_years = request.GET.get("TenureYears")
        equal_months = request.GET.get("TenureMonths")

        # Convert empty strings to None
        equal_years = equal_years if equal_years not in [None, ""] else None
        equal_months = equal_months if equal_months not in [None, ""] else None

        equal_total_months = None

        if equal_years is not None and equal_months is not None:
            equal_total_months = int(equal_years) * 12 + int(equal_months)
        elif equal_years is not None:
            equal_total_months = int(equal_years) * 12
        elif equal_months is not None:
            equal_total_months = int(equal_months)


        final_list = []

        for j in Resignations_list:

            doj = j["DOJ"]
            dor = j["Date_Of_res"]
            Code = j["Emp_Code"]
            OID = j["OrganizationID"]

            total_months = tenure_in_months(doj, dor)
            # Level = Get_Level_From_Code(Code, OID)

            # FILTER: Exact match
            if equal_total_months is not None:
                if total_months != equal_total_months:
                    continue   # skip non-matching employees

            tenure = calculate_tenure(doj, dor)

            final_list.append({
                "SDL": org_map.get(OID),
                "Name": j["Name"],
                "Desi": j["Designation"],
                "Dept": j["Dept"],
                "Tenure": tenure,
                "Level": j["Level"],
                "DOR": format_date(dor),
                "DOJ": format_date(doj),
            })

        return JsonResponse(final_list, safe=False)

    except Exception as e:
        print("Error in Resignation_Mobile_Api:", e)
        return JsonResponse({"error": str(e)}, status=500)
    
    # return JsonResponse({'error': 'Data Not Found'}, status=400)
    


def Get_Level_From_Code(Code, OID):
    return EmployeeMaster.objects.filter(
        EmployeeCode=Code,
        OrganizationID=OID
    ).values_list("Level", flat=True).first()




from app.models import EmployeeMaster




def Get_Employee_Master_Data(emp_id, org_id):
    """
    Returns employee information from EmployeeMaster
    and fills Salary from Salary_Detail_Master if missing or zero.
    """

    try:
        employee = EmployeeMaster.objects.filter(
            EmpID=emp_id,
            OrganizationID=org_id,
            IsDelete=False
        ).first()

        if not employee:
            return None

        # --- Salary Fallback Logic ---
        salary = employee.Salary

        if not salary or salary == 0:
            ctc_obj = Salary_Detail_Master.objects.filter(
                Salary_title__Title='CTC (A+C)',
                EmpID=emp_id,
                OrganizationID=org_id,
                IsDelete=False
            ).order_by('-id').first()

            if ctc_obj:
                employee.Salary = ctc_obj.Permonth
            else:
                employee.Salary = 0  # no fallback available

        return employee

    except Exception as e:
        print("Error while fetching EmployeeMaster data:", e)
        return None
    
def Get_Employee_Master_Data_with_EmpID(emp_id, org_id):
    """
    Returns employee information from EmployeeMaster
    and fills Salary from Salary_Detail_Master if missing or zero.
    """

    try:
        employee = EmployeeMaster.objects.filter(
            EmpID=emp_id,
            OrganizationID=org_id,
            IsDelete=False
        ).first()

        if not employee:
            return None

        return employee

    except Exception as e:
        print("Error while fetching EmployeeMaster data:", e)
        return None

def Get_Employee_Master_Data_By_Code(Code, org_id):
    """
    Returns employee information from EmployeeMaster
    and fills Salary from Salary_Detail_Master if missing or zero.
    """

    try:
        employee = EmployeeMaster.objects.filter(
            EmployeeCode=Code,
            OrganizationID=org_id,
            IsDelete=False
        ).first()

        if not employee:
            return None

        return employee

    except Exception as e:
        print("Error while fetching EmployeeMaster data:", e)
        return None




def Get_Employee_ID_Data_By_Code(Code, org_id):
    EmpData = EmployeePersonalDetails.objects.filter(          
        EmployeeCode=Code,
        OrganizationID=org_id,
        IsDelete=False,
        IsEmployeeCreated=True
    ).only('EmpID').first()

    return EmpData.EmpID
    
    
    
    