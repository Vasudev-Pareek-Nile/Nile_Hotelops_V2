
# Mobile_Api
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import OnRollDivisionMaster, OnRollDepartmentMaster,LavelAdd,OnRollDesignationMaster,ContractDivisionMaster,ContractDepartmentMaster,ContractDesignationMaster,ModuleMapping,BudgetMealCost,BudgetInsuranceCost,EntryActualMealCost,EntryActualInsuranceCost,EntryActualContract,EntryActualSharedServices
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from app.views import Error
from django.db.models import OuterRef,Subquery
# manage Master - Level
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.db import connection

from app.models import EmployeeMaster,OrganizationMaster, EmployeeMaster

from django.http import JsonResponse
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from rest_framework import status
# from django.db import connection
from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
from HumanResources.models import EmployeeWorkDetails, EmployeePersonalDetails
from Manning_Guide.models import EntryActualContract, EntryActualSharedServices
import logging
from django.db.models import Count, Sum, Q, FloatField
from django.db.models import F, ExpressionWrapper




@api_view(['GET'])
def variance_report_Mobile_api(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    if AccessToken:
        if AccessToken == Fixed_Token:
            pass
        else:
            return Response({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=status.HTTP_400_BAD_REQUEST)
            # return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)
    else:
        return Response({'error': 'Token Not Found, Please Provide Correct Token.'}, status=status.HTTP_400_BAD_REQUEST)
        # return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)

    organization_id = request.GET.get('OID')
    exclude_zero_headcount_str = request.GET.get('Ex_zero', '0')  # default as string

    if not organization_id:
        return Response({"error": "OrganizationID (OID) is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not OrganizationMaster.objects.filter(OrganizationID=organization_id).exists():
        return Response({"error": f"Invalid OrganizationID: {organization_id}"}, status=status.HTTP_404_NOT_FOUND)

    try:
        exclude_zero_headcount = int(exclude_zero_headcount_str)
    except ValueError:
        exclude_zero_headcount = 0

    # print("organization_id::", organization_id)
    # print("exclude_zero_headcount::", exclude_zero_headcount)


    with connection.cursor() as cursor:
        try:
            cursor.execute("EXEC ManningGuide_SP_Variance_Master_Rerport %s, %s", [organization_id, exclude_zero_headcount])
            
            # Get column names
            columns = [col[0] for col in cursor.description]
            
            # Fetch all rows
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return JsonResponse({'status': True, 'data': data}, safe=False)
        except Exception as e:
            return JsonResponse({'status': False, 'error': str(e)}, status=500)





#  ----------------------- #### 100 % working code #### -----------------------

def call_variance_sp(organization_id, exe_zero=0):
    with connection.cursor() as cursor:
        cursor.execute("""
            EXEC ManningGuide_SP_Variance_Master_Rerport @OrganizationID=%s, @Exe_Zero=%s
        """, [organization_id, exe_zero])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


@api_view(['GET'])
def variance_totals(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    if AccessToken:
        if AccessToken == Fixed_Token:
            pass
        else:
            return Response({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=status.HTTP_400_BAD_REQUEST)
            # return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)
    else:
        return Response({'error': 'Token Not Found, Please Provide Correct Token.'}, status=status.HTTP_400_BAD_REQUEST)
        # return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)

    org_id = request.GET.get('HID') 
    data = call_variance_sp(org_id)

    total_row = next((row for row in data if row['Department_masterID'] == 0 and row['Division_masterID'] == 0), None)
    return Response(total_row)


@api_view(['GET'])
def variance_divisions(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    if AccessToken:
        if AccessToken == Fixed_Token:
            pass
        else:
            return Response({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=status.HTTP_400_BAD_REQUEST)
            # return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)
    else:
        return Response({'error': 'Token Not Found, Please Provide Correct Token.'}, status=status.HTTP_400_BAD_REQUEST)
        # return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)

    org_id = request.GET.get('HID') 
    data = call_variance_sp(org_id)

    division_summary = {}
    for row in data:
        if row['Department'] != 'Total':  
            div_id = row['Division_masterID']
            if div_id not in division_summary:
                division_summary[div_id] = {
                    'Division_masterID': div_id,
                    'Division': row['Division'],
                    'Bud_HC': 0,
                    'Bud_TotalCTC': 0,
                    'Act_HC': 0,
                    'Act_TotalCTC': 0,
                }
            division_summary[div_id]['Bud_HC'] += row['Bud_HC'] or 0
            division_summary[div_id]['Bud_TotalCTC'] += row['Bud_TotalCTC'] or 0
            division_summary[div_id]['Act_HC'] += row['Act_HC'] or 0
            division_summary[div_id]['Act_TotalCTC'] += row['Act_TotalCTC'] or 0

    # Calculate Avg and Variance for each Division
    for div in division_summary.values():
        div['Bud_AvgSal'] = div['Bud_TotalCTC'] / div['Bud_HC'] if div['Bud_HC'] > 0 else 0
        div['Act_AvgSal'] = div['Act_TotalCTC'] / div['Act_HC'] if div['Act_HC'] > 0 else 0
        div['Var_AvgSal'] = div['Act_AvgSal'] - div['Bud_AvgSal']
        div['Var_HC'] = div['Act_HC'] - div['Bud_HC']
        div['Var_TotalCTC'] = div['Act_TotalCTC'] - div['Bud_TotalCTC']

    return Response(list(division_summary.values()))


@api_view(['GET'])
def variance_departments(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    if AccessToken:
        if AccessToken == Fixed_Token:
            pass
        else:
            return Response({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=status.HTTP_400_BAD_REQUEST)
            # return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)
    else:
        return Response({'error': 'Token Not Found, Please Provide Correct Token.'}, status=status.HTTP_400_BAD_REQUEST)
        # return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)

    org_id = request.GET.get('HID') 
    division_id = request.GET.get('division_id')

    if not division_id:
        return Response({'error': 'division_id is required'}, status=400)

    data = call_variance_sp(org_id)

    # Filter for the given Division
    dept_data = [
        row for row in data
        if str(row['Division_masterID']) == str(division_id) and row['Department'] != 'Total'
    ]

    return Response(dept_data)






logger = logging.getLogger(__name__)
def View_Actual_mobile_api(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    if AccessToken:
        if AccessToken == Fixed_Token:
            pass
        else:
            return Response({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=status.HTTP_400_BAD_REQUEST)
            # return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)
    else:
        return Response({'error': 'Token Not Found, Please Provide Correct Token.'}, status=status.HTTP_400_BAD_REQUEST)
        # return JsonResponse({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=400)
    
    OrganizationID = request.GET.get('OID')
    selectedOrganizationID = request.GET.get('SOID', OrganizationID)
    exclude_zero_headcount = request.GET.get('Ex_zero', '0')

    # ---------------- ON ROLL ----------------
    employees = EmployeeWorkDetails.objects.filter(
        OrganizationID=selectedOrganizationID,
        IsDelete=False, IsSecondary=False,
        EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"]
    ).exclude(Department__isnull=True).exclude(Department='')

    employees = employees.values('Department', 'Designation').annotate(
        num_employees=Count('id'),
        avg_salary=ExpressionWrapper(
            Sum('Salary', filter=Q(Salary__isnull=False, Salary__gt=0)) / Count('id'),
            output_field=FloatField()
        )
    )

    grand_total_salary = 0
    grand_total_headcount = 0
    for emp in employees:
        num = emp['num_employees'] or 0
        avg = emp['avg_salary'] or 0
        grand_total_salary += avg * num
        grand_total_headcount += num

    grandsalarydivion = grand_total_salary / grand_total_headcount if grand_total_headcount else 0

    # ---------------- CONTRACT ----------------
    contract_qs = EntryActualContract.objects.filter(hotel_name=selectedOrganizationID, IsDelete=False).values(
        'contract_department_master__DepartmentName', 'contract_designation_master__designations'
    ).annotate(
        head_count=Sum('head_count'),
        avg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField())
    )

    grandContractdivisionmultiplication_result = 0
    Contractgrand_total_headcount = 0
    for row in contract_qs:
        num = row['head_count'] or 0
        avg = row['avg_salary'] or 0
        grandContractdivisionmultiplication_result += avg * num
        Contractgrand_total_headcount += num

    contractgrandsalarydivion = grandContractdivisionmultiplication_result / Contractgrand_total_headcount if Contractgrand_total_headcount else 0

    # ---------------- SERVICES ----------------
    services_qs = EntryActualSharedServices.objects.filter(hotel_name=selectedOrganizationID, IsDelete=False).values(
        'services_department_master__DepartmentName', 'services_designation_master__designations'
    ).annotate(
        head_count=Sum('head_count'),
        avg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField())
    )

    Servicesgranddivisionmultiplication_result = 0
    ServicesContractgrand_total_headcount = 0
    for row in services_qs:
        num = row['head_count'] or 0
        avg = row['avg_salary'] or 0
        Servicesgranddivisionmultiplication_result += avg * num
        ServicesContractgrand_total_headcount += num

    Servicesgrandsalarydivion = Servicesgranddivisionmultiplication_result / ServicesContractgrand_total_headcount if ServicesContractgrand_total_headcount else 0

    # ---------------- MEAL COST ----------------
    meal_cost_record = EntryActualMealCost.objects.filter(hotel_name=selectedOrganizationID, IsDelete=False).first()
    meal_cost = meal_cost_record.cafeteriamealcost if meal_cost_record else 0

    # ---------------- INSURANCE COST ----------------
    insurance_record = EntryActualInsuranceCost.objects.filter(hotel_name=selectedOrganizationID, IsDelete=False).first()
    insurance_cost = insurance_record.EmployeeInsurancecost if insurance_record else 0

    # ---------------- TOTAL BENEFITS ----------------
    Benefitesheadtotal = grand_total_headcount + Contractgrand_total_headcount + ServicesContractgrand_total_headcount
    Benefitetotalctc = grand_total_salary + grandContractdivisionmultiplication_result + Servicesgranddivisionmultiplication_result + meal_cost + insurance_cost

    Avgsalarytotalctc = Benefitetotalctc / Benefitesheadtotal if Benefitesheadtotal else 0
    Avgsalarymealcoat = meal_cost / Benefitesheadtotal if Benefitesheadtotal else 0

    insuranceheadcount = grand_total_headcount + ServicesContractgrand_total_headcount
    Avgsalaryinsurancecoat = insurance_cost / insuranceheadcount if insuranceheadcount else 0

    context = {
        "On_Roll": {
            "Avg_Sal": round(grandsalarydivion,2),
            "HC": grand_total_headcount,
            "Total_CTC": round(grand_total_salary,2),
        },
        "Contract": {
            "Avg_Sal": round(contractgrandsalarydivion,2),
            "HC": Contractgrand_total_headcount,
            "Total_CTC": round(grandContractdivisionmultiplication_result,2),
        },
        "Services": {
            "Avg_Sal": round(Servicesgrandsalarydivion,2),
            "HC": ServicesContractgrand_total_headcount,
            "Total_CTC": round(Servicesgranddivisionmultiplication_result,2),
        },
        "Meal_Cost": {
            "Avg_Sal": round(Avgsalarymealcoat,2),
            "Total_CTC": meal_cost,
        },
        "Insurance_Cost": {
            "Avg_Sal": round(Avgsalaryinsurancecoat,2),
            "Total_CTC": insurance_cost,
        },
        "Total_Wages_Benefits": {
            "Avg_Sal": round(Avgsalarytotalctc,2),
            "HC": Benefitesheadtotal,
            "Total_CTC": round(Benefitetotalctc,2),
        }
    }

    return JsonResponse(context, safe=False)



# ----------- Employee Details Mobile Api 100% working code --------------

from app.Global_Api import get_division_name, get_department_name

@api_view(['GET'])
def variance_Employee_Data(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    if not AccessToken:
        return Response({'error': 'Token Not Found, Please Provide Correct Token.'}, status=status.HTTP_400_BAD_REQUEST)
    if AccessToken != Fixed_Token:
        return Response({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=status.HTTP_400_BAD_REQUEST)

    org_id = request.GET.get('HID') 
    division_id = request.GET.get('division_id')
    department_id = request.GET.get('Dept_Id')
    print("org_id::", org_id, "division_id::", division_id, "department_id::", department_id)

    # Validate required parameters

    if not (org_id and division_id and department_id):
        return Response({'error': 'division_id, department_id and HID (Organization_id) are required'}, status=400)

    division_name = get_division_name(division_id)
    Department_name = get_department_name(department_id)

    if not division_name or not Department_name:
        return Response({'error': 'Invalid Division or Department ID'}, status=400)

    employees = EmployeeMaster.objects.filter(
        OrganizationID=org_id,
        IsDelete=False, 
        IsSecondary=False,
        Department=Department_name,
        Division=division_name,
        EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"]
    ).values('id', 'EmpName', 'EmployeeCode', 'Department', 'Designation', 'Level')

    return Response(list(employees))


# -------------------- Manning Guide Corporate Report Mobile Api ------------------
def ManningGuideCorpoReport(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    # Token checks
    if not AccessToken:
        return JsonResponse({'error': 'Token not found'}, status=400)
    if AccessToken != Fixed_Token:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    # -------------------------------
    OID = request.GET.get('OID') 
    
    # OID checks
    if not OID:
        return JsonResponse({'error': 'OrganizationID is required'}, status=400)
    if OID != '333333' and not OrganizationMaster.objects.filter(OrganizationID=OID).exists():
        return JsonResponse({'error': 'Invalid OrganizationID'}, status=400)
    
    # OID = request.GET.get('OID') 
    Level = request.GET.get('Level')
    Dept = request.GET.get('Dept')
    Divi = request.GET.get('Divi')
    UserType = request.GET.get('UserType')
    # print("the usertype is here::", UserType)
    # print("My OID::", OID, "My Level::", Level)

    with connection.cursor() as cursor:
        # cursor.execute("EXEC SP_ManningGuide_MobileAPI_Corporate_Varinace_Report_Select %s", [OID])
        cursor.execute("EXEC SP_ManningGuide_MobileAPI_Corporate_Varinace_Report_Select %s, %s, %s, %s , %s", [OID, Level, Dept, Divi, UserType])

        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        rowslist = [dict(zip(columns, row)) for row in rows]
        # return JsonResponse({"msg": "Reached here", "OID": OID, "Level": Level})
        return JsonResponse(rowslist, safe=False)

 
 
 
 
 

from .serializers import OnRollDesignationMasterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from collections import defaultdict


class OnRollDesignationListAPI(APIView):
    """
    GET → List active on-roll designations
    Division → Department → Designations
    """
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'

    def get(self, request):
        access_token = request.headers.get('Authorization')

        if not access_token:
            return Response(
                {"status": False, "message": "Token not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if access_token != self.Fixed_Token:
            return Response(
                {"status": False, "message": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        qs = (
            OnRollDesignationMaster.objects
            .filter(IsDelete=0)
            .values("Div", "Dept", "designations", "Lavel")
            .order_by("Order")
        )

        data_map = defaultdict(lambda: defaultdict(list))

        for row in qs:
            data_map[row["Div"]][row["Dept"]].append({
                "Designation Name": row["designations"],
                "Level": row["Lavel"]
            })

        final_data = []

        for division, departments in data_map.items():
            final_data.append({
                "Division": division,
                "Departments": [
                    {
                        "Department": dept,
                        "Designations": designations
                    }
                    for dept, designations in departments.items()
                ]
            })

        return Response(
            {
                "status": True,
                "count": len(final_data),
                "data": final_data
            },
            status=status.HTTP_200_OK
        )








from django.db import connection
from django.http import JsonResponse

def variance_details_report(request):
    # org_id = '401'
    org_id = request.GET.get("OrganizationID")
    Ex_zero = request.GET.get("Ex_zero", 0)
    
    # print(f"org_id:: {org_id}")
    # print(f"Ex_zero:: {Ex_zero}")

    with connection.cursor() as cursor:
        cursor.execute(
            "EXEC ManningGuide_SP_Variance_Details_Report_select %s, %s",
            [org_id, Ex_zero]
        )
        columns = [col[0] for col in cursor.description]
        data = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return JsonResponse({"data": data})








from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import (
    Sum, Count, F, FloatField, ExpressionWrapper, Prefetch
)
from django.db.models.functions import Trim
import requests
import logging

logger = logging.getLogger(__name__)

from .models import *

@api_view(['GET'])
def view_budget_api(request):
    # -----------------------------
    # 1. READ VALUES FROM URL
    # -----------------------------
    OrganizationID = request.GET.get('OID')
    Session_OID = request.GET.get('SOID')
    UserID = request.GET.get('user_id')
    UserType = request.GET.get('user_type')
    Department_Name = request.GET.get('department_name')

    if not OrganizationID or not UserID:
        return Response(
            {"error": "organization_id and user_id are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # -----------------------------
    # 2. ACCESS CONTROL
    # -----------------------------
    # if not (
    #     Session_OID == '3'
    #     or UserType == 'GM'
    #     or Department_Name == 'HR'
    # ):
    #     return Response(
    #         {"error": "No Access"},
    #         status=status.HTTP_403_FORBIDDEN
    #     )

    # -----------------------------
    # 3. ORGANIZATION API CALL
    # -----------------------------
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {'hotel-api-token': hotelapitoken}
    api_url = (
        "http://hotelops.in/API/PyAPI/OrganizationListSelect"
        f"?OrganizationID={OrganizationID}"
    )

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        memOrg = response.json()
    except Exception as e:
        logger.error(e)
        memOrg = None

    # -----------------------------
    # 4. FILTER PARAMS
    # -----------------------------
    selected_division = request.GET.get('divisionname')
    selected_department = request.GET.get('departmentname')
    selected_organization_id = request.GET.get('hotel_name', OrganizationID)
    exclude_zero_headcount = request.GET.get('exclude_zero_headcount', '1')

    if UserType == 'CEO' and request.GET.get('hotel_name') is None:
        selected_organization_id = 401

    # -----------------------------
    # 5. DIVISION / DEPARTMENT DATA
    # -----------------------------
    Divisiondatas = OnRollDivisionMaster.objects.filter(
        IsDelete=False
    ).order_by('Order')

    departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)

    if selected_division and selected_division != 'All Division':
        Divisiondatas = Divisiondatas.filter(
            DivisionName=selected_division
        )
        departments = departments.filter(
            OnRollDivisionMaster__DivisionName=selected_division
        )

    if selected_department and selected_department != 'All Department':
        departments = departments.filter(
            DepartmentName=selected_department
        )

    # -----------------------------
    # 6. MAIN BUDGET QUERY (ONROLL)
    # -----------------------------
    managebudget_department_designation = (
        ManageBudgetOnRoll.objects
        .annotate(clean_hotel_name=Trim('hotel_name'))
        .filter(
            clean_hotel_name=selected_organization_id,
            is_delete=False
        )
        .values(
            'on_roll_division_master__DivisionName',
            'on_roll_department_master__DepartmentName',
            'on_roll_designation_master__designations'
        )
        .annotate(
            head_count=F('head_count'),
            total_salary=Sum('avg_salary'),
            aavg_salary=ExpressionWrapper(
                Sum('avg_salary') / Count('id'),
                output_field=FloatField()
            ),
            budgetmultiplication_result=ExpressionWrapper(
                F('aavg_salary') * F('head_count'),
                output_field=FloatField()
            )
        )
        .order_by(
            'on_roll_division_master__DivisionName',
            'on_roll_department_master__DepartmentName',
            'on_roll_designation_master__designations'
        )
    )

    if exclude_zero_headcount == '1':
        managebudget_department_designation = (
            managebudget_department_designation.exclude(head_count=0)
        )

    # -----------------------------
    # 7. PROCESS DATA (SAME LOGIC)
    # -----------------------------
    budgets_dict = {}
    department_totals = {}
    division_totals = {}

    for budget in managebudget_department_designation:
        dept = budget['on_roll_department_master__DepartmentName']
        desig = budget['on_roll_designation_master__designations']

        budgets_dict.setdefault(dept, {})[desig] = {
            "head_count": budget['head_count'],
            "avg_salary": budget['aavg_salary'],
            "total": budget['budgetmultiplication_result'],
        }

    # -----------------------------
    # 8. RESPONSE
    # -----------------------------
    return Response(
        {
            "organization_id": selected_organization_id,
            "memOrg": memOrg,
            "filters": {
                "division": selected_division,
                "department": selected_department,
                "exclude_zero_headcount": exclude_zero_headcount
            },
            "budgets": budgets_dict,
            "raw_queryset": list(managebudget_department_designation),
        },
        status=status.HTTP_200_OK
    )




# @api_view(['GET'])
# def view_budget_api(request):
#     # -----------------------------
#     # 1. READ VALUES FROM URL
#     # -----------------------------
#     OrganizationID = request.GET.get('OID')
#     Session_OID = request.GET.get('SOID')
#     UserID = request.GET.get('user_id')
#     UserType = request.GET.get('user_type')
#     Department_Name = request.GET.get('department_name')

#     if not OrganizationID or not UserID:
#         return Response(
#             {"error": "organization_id and user_id are required"},
#             status=status.HTTP_400_BAD_REQUEST
#         )

@api_view(['GET'])
def view_budget_api(request):
    OrganizationID = request.GET.get('OID')
    Session_OID = request.GET.get('SOID')
    UserID = request.GET.get('user_id')
    UserType = request.GET.get('user_type')
    Department_Name = request.GET.get('department_name')
    
    # if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
    #     pass
    # else:
    #     return Response(
    #         {"detail": "OrganizationID is required"},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    print("oid is here:", OrganizationID)
    print("Session_OID is here:", Session_OID)
    print("UserID is here:", UserID)

    # if not OrganizationID:
    #     logger.error("OrganizationID not found in session or is empty.")
    #     return redirect('MasterAttribute.Host')

    # hotelapitoken = MasterAttribute.HotelAPIkeyToken
    # headers = {'hotel-api-token': hotelapitoken}
    # api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    # try:
    #     response = requests.get(api_url, headers=headers)
    #     response.raise_for_status()
    #     memOrg = response.json()
    # except requests.exceptions.RequestException as e:
    #     logger.error(f"Error occurred: {e}")
    #     memOrg = None

    selected_division = request.GET.get('divisionname')
    selected_department = request.GET.get('departmentname')
    selected_organization_id = request.GET.get('hotel_name', OrganizationID)
    exclude_zero_headcount = request.GET.get('exclude_zero_headcount','1')  

    if UserType == 'CEO' and request.GET.get('hotel_name') is None:
        selected_organization_id = 401

    
    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False)
    departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)

    if selected_division and selected_division != 'All Division':
        Divisiondatas = Divisiondatas.filter(DivisionName=selected_division)
        departments = OnRollDepartmentMaster.objects.filter(
            OnRollDivisionMaster__DivisionName=selected_division, IsDelete=False
        )
    if selected_department and selected_department != 'All Department':
        departments = departments.filter(DepartmentName=selected_department)

    
    filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

       
    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
            Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
            Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
        )
    
    filtered_contract_departments = ContractDepartmentMaster.objects.filter(IsDelete=False)
    filtered_contract_designations = ContractDesignationMaster.objects.filter(IsDelete=False)

    
    filtered_service_departments = ServicesDepartmentMaster.objects.filter(IsDelete=False)
    filtered_service_designations = ServicesDesignationMaster.objects.filter(IsDelete=False)

    
    contractdivisions = ContractDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('contractdepartmentmaster_set', queryset=filtered_contract_departments),
        Prefetch('contractdepartmentmaster_set__contractdesignationmaster_set', queryset=filtered_contract_designations)
    )

    
    Servicedivisions = ServicesDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('servicesdepartmentmaster_set', queryset=filtered_service_departments),
        Prefetch('servicesdepartmentmaster_set__servicesdesignationmaster_set', queryset=filtered_service_designations)
    )
    
    
    managebudget_department_designation = ManageBudgetOnRoll.objects.filter(OrganizationID=selected_organization_id)

    Contractbudget_department_designation = ManageBudgetContract.objects.filter(OrganizationID=selected_organization_id)
    if exclude_zero_headcount:  
        Contractbudget_department_designation = Contractbudget_department_designation.exclude(head_count=0)
   
    Servicesbudget_department_designation = ManageBudgetSharedServices.objects.filter(OrganizationID=selected_organization_id)
    if exclude_zero_headcount:  
        Servicesbudget_department_designation = Servicesbudget_department_designation.exclude(head_count=0)

    managebudget_department_designation = ManageBudgetOnRoll.objects.annotate(
        clean_hotel_name=Trim('hotel_name')  
    ).filter(
        clean_hotel_name=selected_organization_id,  
        is_delete=False
    ).values(
        'on_roll_division_master__DivisionName',
        'on_roll_department_master__DepartmentName',
        'on_roll_designation_master__designations'
    ).annotate(
        head_count=F('head_count'),
        total_salary=Sum('avg_salary'),
        aavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        budgetmultiplication_result=ExpressionWrapper(F('aavg_salary') * F('head_count'), output_field=FloatField())
    ).order_by(
        'on_roll_division_master__DivisionName',
        'on_roll_department_master__DepartmentName',
        'on_roll_designation_master__designations'
    )
    
    if exclude_zero_headcount == '1':  
        managebudget_department_designation = managebudget_department_designation.exclude(head_count=0)
    
    # print("exclude_zero_headcount value::", exclude_zero_headcount)
    
        
    budgets_dict = {}
    department_totals = {}
    division_totals = {}

    for budget in managebudget_department_designation:
        dept_id = budget['on_roll_department_master__DepartmentName']
        desig_id = budget['on_roll_designation_master__designations']

        if dept_id not in budgets_dict:
            budgets_dict[dept_id] = {}

        budgets_dict[dept_id][desig_id] = {
            'head_count': budget['head_count'],
            'aavg_salary': budget['aavg_salary'],
            'budgetmultiplication_result': budget['budgetmultiplication_result'],
        }

        if dept_id not in department_totals:
            department_totals[dept_id] = {
                'budgetmultiplication_result': 0,
                'total_headcount': 0,
                'salary_headcount_product': 0,
            }

        department_totals[dept_id]['budgetmultiplication_result'] += budget.get('budgetmultiplication_result', 0) or 0
        department_totals[dept_id]['total_headcount'] += budget.get('head_count', 0) or 0

       
        if department_totals[dept_id]['total_headcount'] > 0:
            department_totals[dept_id]['salary_headcount_product'] = (
                department_totals[dept_id]['budgetmultiplication_result'] / department_totals[dept_id]['total_headcount']
            )

        divisions_qs = OnRollDivisionMaster.objects.filter(
            onrolldepartmentmaster__DepartmentName=dept_id
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')

        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name and division_name not in division_totals:
            division_totals[division_name] = {
                'divisionmultiplication_result': 0,
                'divisiontotal_headcount': 0,
                'divisionsalary_headcount_product': 0,
            }

        if division_name:
            division_totals[division_name]['divisionmultiplication_result'] += budget.get('budgetmultiplication_result', 0) or 0
            division_totals[division_name]['divisiontotal_headcount'] += budget.get('head_count', 0) or 0

            
            if division_totals[division_name]['divisiontotal_headcount'] > 0:
                division_totals[division_name]['divisionsalary_headcount_product'] = (
                    division_totals[division_name]['divisionmultiplication_result'] / division_totals[division_name]['divisiontotal_headcount']
                )

    
    divisionmultiplication_result = sum(
         dept['divisionmultiplication_result'] for dept in division_totals.values() if 'divisionmultiplication_result' in dept
     )
    grand_total_headcount = sum(
         dept['divisiontotal_headcount'] for dept in division_totals.values() if 'divisiontotal_headcount' in dept
     )
    # grandsalarydivion = divisionmultiplication_result / grand_total_headcount
    if grand_total_headcount > 0:
        grandsalarydivion = divisionmultiplication_result / grand_total_headcount
    else:
        grandsalarydivion = 0  

    
# <!-- contract budget  -->

    Contractbudget_department_designation = ManageBudgetContract.objects.filter(
            hotel_name=selected_organization_id,
        ).values(
            'contract_department_master__DepartmentName',  
            'contract_designation_master__designations'      
        ).annotate(
            Contracthead_count=Sum('head_count'),
            Contracttotal_salary=Sum('avg_salary'),
            Contractavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
            Contractmultiplication_result=ExpressionWrapper(F('Contractavg_salary') * F('Contracthead_count'), output_field=FloatField())
        ).order_by(
            'contract_department_master__DepartmentName',    
            'contract_designation_master__designations'       
        )
    
        
    Contractbudgets_dict = {}
    Contractdepartment_totals = {}
    Contractdivision_totals = {}

        
    for Contractbudget in Contractbudget_department_designation:
            dept_id = Contractbudget['contract_department_master__DepartmentName']
            desig_id = Contractbudget['contract_designation_master__designations']

            if dept_id not in Contractbudgets_dict:
                Contractbudgets_dict[dept_id] = {}

            Contractbudgets_dict[dept_id][desig_id] = {
                'Contracthead_count': Contractbudget['Contracthead_count'],
                'Contractavg_salary': Contractbudget['Contractavg_salary'],
                'Contractmultiplication_result': Contractbudget['Contractmultiplication_result'],
            }

            if dept_id not in Contractdepartment_totals:
                Contractdepartment_totals[dept_id] = {
                    'Contractmultiplication_result': 0,
                    'Contracthead_count': 0,
                    'salary_headcount_contract': 0,
                }

            Contractdepartment_totals[dept_id]['Contractmultiplication_result'] += Contractbudget.get('Contractmultiplication_result', 0) or 0
            Contractdepartment_totals[dept_id]['Contracthead_count'] += Contractbudget.get('Contracthead_count', 0) or 0


            if Contractdepartment_totals[dept_id]['Contracthead_count'] > 0:
                Contractdepartment_totals[dept_id]['salary_headcount_contract'] = (
                    Contractdepartment_totals[dept_id]['Contractmultiplication_result'] / Contractdepartment_totals[dept_id]['Contracthead_count']
                )

            
            divisions_qs = ContractDivisionMaster.objects.filter(
                contractdepartmentmaster__DepartmentName=dept_id
            ).annotate(
                division_name=F('DivisionName')
            ).values('division_name')

            division_name = divisions_qs[0]['division_name'] if divisions_qs else None

            if division_name and division_name not in Contractdivision_totals:
                Contractdivision_totals[division_name] = {
                    'Contractdivisionmultiplication_result': 0,
                    'Contractdivisiontotal_headcount': 0,
                    'Contractdivisionsalary_headcount_product': 0,
                }

            if division_name:
                Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] += Contractbudget.get('Contractmultiplication_result', 0) or 0
                Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] += Contractbudget.get('Contracthead_count', 0) or 0

                if Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] > 0:
                    Contractdivision_totals[division_name]['Contractdivisionsalary_headcount_product'] = (
                        Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] / Contractdivision_totals[division_name]['Contractdivisiontotal_headcount']
                    )
    grandContractdivisionmultiplication_result = sum(
        dept['Contractdivisionmultiplication_result'] for dept in Contractdivision_totals.values() if 'Contractdivisionmultiplication_result' in dept
    )
    Contractgrand_total_headcount = sum(
        dept['Contractdivisiontotal_headcount'] for dept in Contractdivision_totals.values() if 'Contractdivisiontotal_headcount' in dept
    )

    
    if Contractgrand_total_headcount > 0:
        contractgrandsalarydivion = grandContractdivisionmultiplication_result / Contractgrand_total_headcount
    else:
        contractgrandsalarydivion = 0  

    

    # <!-- Shared Services Budget  -->
    Servicesbudget_department_designation = ManageBudgetSharedServices.objects.filter(
        hotel_name=selected_organization_id,
    ).values(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    ).annotate(
        Serviceshead_count=Sum('head_count'),
        Servicestotal_salary=Sum('avg_salary'),
        Servicesavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        Servicesmultiplication_result=F('Servicesavg_salary') * F('Serviceshead_count')
    ).order_by(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    )

    Servicesbudgets_dict = {}
    departmentservices_dict = {}
    divisionservices_dict = {}

    for Servicesbudget in Servicesbudget_department_designation:
        dept_id = Servicesbudget['services_department_master__DepartmentName']
        desig_id = Servicesbudget['services_designation_master__designations']

        if dept_id not in Servicesbudgets_dict:
            Servicesbudgets_dict[dept_id] = {}

        Servicesbudgets_dict[dept_id][desig_id] = {
            'Serviceshead_count': Servicesbudget['Serviceshead_count'],
            'Servicesavg_salary': Servicesbudget['Servicesavg_salary'],
            'Servicesmultiplication_result': Servicesbudget['Servicesmultiplication_result'],
        }


        if dept_id not in departmentservices_dict:
            departmentservices_dict[dept_id] = {
                'TotalServicesmultiplication_result': 0,
                'TotalServiceshead_count': 0,
                'TotalServicessalary_headcount_contract': 0,
            }

        departmentservices_dict[dept_id]['TotalServicesmultiplication_result'] += Servicesbudget.get('Servicesmultiplication_result', 0) or 0
        departmentservices_dict[dept_id]['TotalServiceshead_count'] += Servicesbudget.get('Serviceshead_count', 0) or 0

        if departmentservices_dict[dept_id]['TotalServiceshead_count'] > 0:
            departmentservices_dict[dept_id]['TotalServicessalary_headcount_contract'] = (
                departmentservices_dict[dept_id]['TotalServicesmultiplication_result'] / departmentservices_dict[dept_id]['TotalServiceshead_count']
            )

        divisions_qs = ServicesDivisionMaster.objects.filter(
            servicesdepartmentmaster__DepartmentName=dept_id
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')

        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name and division_name not in divisionservices_dict:
            divisionservices_dict[division_name] = {
                'Servicedivisionmultiplication_result': 0,
                'Servicedivisiontotal_headcount': 0,
                'Servicedivisionsalary_headcount_product': 0,
            }

        if division_name:
            divisionservices_dict[division_name]['Servicedivisionmultiplication_result'] += departmentservices_dict[dept_id]['TotalServicesmultiplication_result']
            divisionservices_dict[division_name]['Servicedivisiontotal_headcount'] += departmentservices_dict[dept_id]['TotalServiceshead_count']

            if divisionservices_dict[division_name]['Servicedivisiontotal_headcount'] > 0:
                divisionservices_dict[division_name]['Servicedivisionsalary_headcount_product'] = (
                    divisionservices_dict[division_name]['Servicedivisionmultiplication_result'] / divisionservices_dict[division_name]['Servicedivisiontotal_headcount']
                )

    
    Servicesgranddivisionmultiplication_result = sum(
        dept['Servicedivisionmultiplication_result'] for dept in divisionservices_dict.values() if 'Servicedivisionmultiplication_result' in dept
    )

    ServicesContractgrand_total_headcount = sum(
        dept['Servicedivisiontotal_headcount'] for dept in divisionservices_dict.values() if 'Servicedivisiontotal_headcount' in dept
    )

    if ServicesContractgrand_total_headcount > 0:
        Servicesgrandsalarydivion = Servicesgranddivisionmultiplication_result / ServicesContractgrand_total_headcount
    else:
        Servicesgrandsalarydivion = 0

   

    meal_cost_record = BudgetMealCost.objects.filter(hotel_name=selected_organization_id).first()

    if meal_cost_record:
        meal_cost = meal_cost_record.cafeteriamealcost
    else:
        meal_cost = 0

    Insurance_cost_record = BudgetInsuranceCost.objects.filter(hotel_name=selected_organization_id).first()

    # Ensure Insurance_cost is a valid number
    if Insurance_cost_record and Insurance_cost_record.EmployeeInsurancecost is not None:
        Insurance_cost = Insurance_cost_record.EmployeeInsurancecost
    else:
        Insurance_cost = 0

    # Calculate insuranceheadcount
    insuranceheadcount = (grand_total_headcount or 0) + (ServicesContractgrand_total_headcount or 0)

    # Safely calculate Avgsalaryinsurancecoat
    if insuranceheadcount > 0:
        Avgsalaryinsurancecoat = Insurance_cost / insuranceheadcount
    else:
        Avgsalaryinsurancecoat = 0

    
        
        
# benefites total 
    Benefitesheadtotal = (
        (grand_total_headcount or 0) +
        (Contractgrand_total_headcount or 0) +
        (ServicesContractgrand_total_headcount or 0)
    )

    Benefitetotalctc = (
        (divisionmultiplication_result or 0) +
        (grandContractdivisionmultiplication_result or 0) +
        (Servicesgranddivisionmultiplication_result or 0) +
        (meal_cost or 0) +
        (Insurance_cost or 0)
    )

    Benefitetotalctc = Benefitetotalctc or 0  # If None, default to 0
    meal_cost = meal_cost or 0               # If None, default to 0
    Benefitesheadtotal = Benefitesheadtotal or 0  # If None, default to 0

    # Calculate average salary for total CTC
    if Benefitesheadtotal > 0:
        Avgsalarytotalctc = Benefitetotalctc / Benefitesheadtotal
    else:
        Avgsalarytotalctc = 0

    # Calculate average meal cost
    if Benefitesheadtotal > 0:
        Avgsalarymealcoat = meal_cost / Benefitesheadtotal
    else:
        Avgsalarymealcoat = 0
    



    return Response( 
        {
            'selectedOrganizationID': selected_organization_id,
            'OrganizationID': OrganizationID,
            'Contractbudgets_dict':Contractbudgets_dict,
            'Servicesbudgets_dict':Servicesbudgets_dict,

            'budgets_dict': budgets_dict,
            'department_totals': department_totals,
            'division_totals': division_totals,
            'divisionmultiplication_result':divisionmultiplication_result,
            'grand_total_headcount': grand_total_headcount,
            'grandsalarydivion':grandsalarydivion,
            'Contractdepartment_totals':Contractdepartment_totals,
            'Contractdivision_totals':Contractdivision_totals,
            'grandContractdivisionmultiplication_result':grandContractdivisionmultiplication_result,
            'Contractgrand_total_headcount':Contractgrand_total_headcount,
            'contractgrandsalarydivion':contractgrandsalarydivion,
            'departmentservices_dict':departmentservices_dict,
            'divisionservices_dict':divisionservices_dict,
            'Servicesgranddivisionmultiplication_result':Servicesgranddivisionmultiplication_result,
            'ServicesContractgrand_total_headcount':ServicesContractgrand_total_headcount,
            'Servicesgrandsalarydivion':Servicesgrandsalarydivion,
            'meal_cost':meal_cost,
            'Insurance_cost':Insurance_cost,
            'Benefitesheadtotal':Benefitesheadtotal,
            'Benefitetotalctc':Benefitetotalctc,
            'Avgsalarytotalctc':Avgsalarytotalctc,
            'Avgsalarymealcoat':Avgsalarymealcoat,
            'Avgsalaryinsurancecoat':Avgsalaryinsurancecoat,
            'managebudget_department_designation': managebudget_department_designation,
            'exclude_zero_headcount': exclude_zero_headcount,
            'Contractbudget_department_designation':Contractbudget_department_designation
        },
        status=status.HTTP_200_OK
    )



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Case, When, IntegerField, Prefetch

@api_view(['GET'])
def view_budget_trial_two_api(request):
    OrganizationID = request.GET.get('OID')
    UserType = request.GET.get('user_type')
    Department_Name = request.GET.get('department_name')

    hotel_name = request.GET.get('hotel_name', OrganizationID)

    if UserType == 'CEO' and request.GET.get('hotel_name') is None:
        hotel_name = 401

    # Budget data
    budget_qs = ManageBudgetOnRoll.objects.filter(
        hotel_name=hotel_name,
        is_delete=False
    )

    budget_map = {
        b.on_roll_designation_master_id: {
            'avg_salary': b.avg_salary,
            'head_count': b.head_count or 0,
            'morning': b.morning,
            'general': b.general_deta,
            'afternoon': b.afternoon,
            'night': b.night,
            'm_break': b.m_break,
            'relievers': b.relievers,
            'total_ctc': b.total_ctc,
        }
        for b in budget_qs
    }

    filtered_designations = OnRollDesignationMaster.objects.filter(
        IsDelete=False
    ).annotate(
        level_order=Case(
            When(Lavel='M6', then=1),
            When(Lavel='M5', then=2),
            When(Lavel='M4', then=3),
            When(Lavel='M3', then=4),
            When(Lavel='M2', then=5),
            When(Lavel='M1', then=6),
            When(Lavel='M', then=7),
            When(Lavel='E', then=8),
            When(Lavel='T', then=9),
            When(Lavel='A', then=10),
            default=99,
            output_field=IntegerField()
        )
    ).order_by('level_order', 'Order')

    divisions = OnRollDivisionMaster.objects.filter(
        IsDelete=False
    ).order_by('Order').prefetch_related(
        Prefetch(
            'onrolldepartmentmaster_set',
            queryset=OnRollDepartmentMaster.objects.filter(IsDelete=False).order_by('Order')
        ),
        Prefetch(
            'onrolldepartmentmaster_set__onrolldesignationmaster_set',
            queryset=filtered_designations
        )
    )

    result = []

    for div in divisions:
        div_data = {
            'id': div.id,
            'name': div.DivisionName,
            'departments': []
        }

        for dept in div.onrolldepartmentmaster_set.all():
            dept_data = {
                'id': dept.id,
                'name': dept.DepartmentName,
                'designations': []
            }

            for des in dept.onrolldesignationmaster_set.all():
                dept_data['designations'].append({
                    'id': des.id,
                    'name': des.designations,
                    'level': des.Lavel,
                    'budget': budget_map.get(des.id, {
                        'avg_salary': 0,
                        'head_count': 0,
                        'morning': 0,
                        'general': 0,
                        'afternoon': 0,
                        'night': 0,
                        'm_break': 0,
                        'relievers': 0,
                        'total_ctc': 0,
                    })
                })

            div_data['departments'].append(dept_data)

        result.append(div_data)

    return Response({
        'hotel_name': hotel_name,
        'divisions': result
    }, status=status.HTTP_200_OK)





from django.db.models import Sum, F, FloatField, ExpressionWrapper
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def Department_Totals_View(request):
    selected_organization_id = request.GET.get('OID')

    # 1️⃣ Fetch all departments (master data)
    all_departments = OnRollDepartmentMaster.objects.filter(
        IsDelete=False
    ).values(
        'id',
        'DepartmentName'
    )

    # 2️⃣ Fetch aggregated budget data (department-wise)
    budget_qs = (
        ManageBudgetOnRoll.objects
        .filter(
            OrganizationID=selected_organization_id,
            is_delete=False
        )
        .values(
            'on_roll_department_master__DepartmentName'
        )
        .annotate(
            total_headcount=Sum('head_count'),
            morning=Sum('morning'),
            general_deta=Sum('general_deta'),
            afternoon=Sum('afternoon'),
            night=Sum('night'),
            m_break=Sum('m_break'),
            relievers=Sum('relievers'),
            total_ctc=Sum(
                F('avg_salary') * F('head_count'),
                output_field=FloatField()
            )
        )
    )

    # 3️⃣ Convert budget_qs to lookup dict
    budget_lookup = {
        row['on_roll_department_master__DepartmentName']: row
        for row in budget_qs
    }

    # 4️⃣ Build final response (ZERO-SAFE)
    department_totals = {}

    for dept in all_departments:
        dept_name = dept['DepartmentName']
        row = budget_lookup.get(dept_name, {})

        hc = row.get('total_headcount', 0) or 0
        ctc = row.get('total_ctc', 0) or 0

        department_totals[dept_name] = {
            'Avg_Sal': round(ctc / hc, 2) if hc else 0,
            'total_headcount': hc,
            'morning': row.get('morning', 0) or 0,
            'general_deta': row.get('general_deta', 0) or 0,
            'afternoon': row.get('afternoon', 0) or 0,
            'night': row.get('night', 0) or 0,
            'm_break': row.get('m_break', 0) or 0,
            'relievers': row.get('relievers', 0) or 0,
            'Total_CTC': ctc,
        }
        
    grand_total = {
        'Avg_Sal': 0,
        'total_headcount': 0,
        'morning': 0,
        'general_deta': 0,
        'afternoon': 0,
        'night': 0,
        'm_break': 0,
        'relievers': 0,
        'Total_CTC': 0,
    }

    for dept_data in department_totals.values():
        grand_total['total_headcount'] += dept_data['total_headcount']
        grand_total['morning'] += dept_data['morning']
        grand_total['general_deta'] += dept_data['general_deta']
        grand_total['afternoon'] += dept_data['afternoon']
        grand_total['night'] += dept_data['night']
        grand_total['m_break'] += dept_data['m_break']
        grand_total['relievers'] += dept_data['relievers']
        grand_total['Total_CTC'] += dept_data['Total_CTC']

    # Calculate Avg Salary safely
    if grand_total['total_headcount'] > 0:
        grand_total['Avg_Sal'] = round(
            grand_total['Total_CTC'] / grand_total['total_headcount'], 2
        )

    # return Response(department_totals, status=status.HTTP_200_OK)

    return Response({
        "department_totals": department_totals,
        "grand_total": grand_total
    }, status=status.HTTP_200_OK)



# @api_view(['GET'])
# def contract_manning_api(request):
#     selected_organization_id = request.GET.get('OID')
#     exclude_zero_headcount = request.GET.get('exclude_zero_headcount', '1')

#     qs = ManageBudgetContract.objects.filter(
#         hotel_name=selected_organization_id
#     ).values(
#         'contract_department_master__DepartmentName',
#         'contract_designation_master__designations',
#         'contract_designation_master__Lavel'
#     ).annotate(
#         head_count=Sum('head_count'),
#         avg_salary=ExpressionWrapper(
#             Sum('avg_salary') / Count('id'),
#             output_field=FloatField()
#         ),
#         total_ctc=ExpressionWrapper(
#             F('avg_salary') * F('head_count'),
#             output_field=FloatField()
#         )
#     )

#     if exclude_zero_headcount == '1':
#         qs = qs.exclude(head_count=0)

#     data = {}

#     # 1️⃣ Accumulate totals
#     for row in qs:
#         dept = row['contract_department_master__DepartmentName']

#         if dept not in data:
#             data[dept] = {
#                 "designations": [],
#                 "department_totals": {
#                     "head_count": 0,
#                     "total_ctc": 0
#                 }
#             }

#         data[dept]["designations"].append({
#             "designation": row['contract_designation_master__designations'],
#             "level": row['contract_designation_master__Lavel'],
#             "head_count": row['head_count'],
#             "avg_salary": row['avg_salary'],
#             "total_ctc": row['total_ctc'],
#             "morning": row['morning'],
#             "general_deta": row['general_deta'],
#             "afternoon": row['afternoon'],
#             "night": row['night'],
#             "m_break": row['m_break'],
#             "relievers": row['relievers'],
#         })

#         totals = data[dept]["department_totals"]
#         totals["head_count"] += row['head_count']
#         totals["total_ctc"] += row['total_ctc']

#     # 2️⃣ Compute Avg_Sal (weighted)
#     for dept, values in data.items():
#         totals = values["department_totals"]
#         hc = totals["head_count"]

#         totals["Avg_Sal"] = round(
#             totals["total_ctc"] / hc, 2
#         ) if hc > 0 else 0

#     return Response({
#         "organization_id": selected_organization_id,
#         "contract_manning": data
#     })

@api_view(['GET'])
def contract_manning_api(request):
    selected_organization_id = request.GET.get('OID')
    exclude_zero_headcount = request.GET.get('exclude_zero_headcount', '1')

    qs = (
        ManageBudgetContract.objects
        .filter(
            hotel_name=selected_organization_id,
            IsDelete=False
        )
        .annotate(
            row_ctc=ExpressionWrapper(
                F('avg_salary') * F('head_count'),
                output_field=FloatField()
            )
        )
        .values(
            'contract_department_master__DepartmentName',
            'contract_designation_master__designations',
            'contract_designation_master__Lavel'
        )
        .annotate(
            head_count=Sum('head_count'),
            morning=Sum('morning'),
            general_deta=Sum('general_deta'),
            afternoon=Sum('afternoon'),
            night=Sum('night'),
            m_break=Sum('m_break'),
            relievers=Sum('relievers'),
            total_ctc=Sum('row_ctc')
        )
    )

    if exclude_zero_headcount == '1':
        qs = qs.exclude(head_count=0)

    data = {}

    # 1️⃣ Accumulate department + designation data
    for row in qs:
        dept = row['contract_department_master__DepartmentName']

        if dept not in data:
            data[dept] = {
                "designations": [],
                "department_totals": {
                    "HC": 0,
                    "MORG": 0,
                    "GEN": 0,
                    "A_NOON": 0,
                    "NIGHT": 0,
                    "M_BREAK": 0,
                    "RELI": 0,
                    "Total_CTC": 0
                }
            }

        data[dept]["designations"].append({
            "designation": row['contract_designation_master__designations'],
            "level": row['contract_designation_master__Lavel'],
            "HC": row['head_count'] or 0,
            "MORG": row['morning'] or 0,
            "GEN": row['general_deta'] or 0,
            "A_NOON": row['afternoon'] or 0,
            "NIGHT": row['night'] or 0,
            "M_BREAK": row['m_break'] or 0,
            "RELI": row['relievers'] or 0,
            "Total_CTC": row['total_ctc'] or 0
        })

        totals = data[dept]["department_totals"]
        totals["HC"] += row['head_count'] or 0
        totals["MORG"] += row['morning'] or 0
        totals["GEN"] += row['general_deta'] or 0
        totals["A_NOON"] += row['afternoon'] or 0
        totals["NIGHT"] += row['night'] or 0
        totals["M_BREAK"] += row['m_break'] or 0
        totals["RELI"] += row['relievers'] or 0
        totals["Total_CTC"] += row['total_ctc'] or 0

    # 2️⃣ Compute weighted Avg Salary
    for dept, values in data.items():
        totals = values["department_totals"]
        hc = totals["HC"]
        totals["Avg_Sal"] = round(
            totals["Total_CTC"] / hc, 2
        ) if hc > 0 else 0

    return Response({
        "organization_id": selected_organization_id,
        "contract_manning": data
    })




# @api_view(['GET'])
# def shared_service_manning_api(request):
#     selected_organization_id = request.GET.get('OID')
#     exclude_zero_headcount = request.GET.get('ex_zero', '1')

#     qs = (
#         ManageBudgetSharedServices.objects
#         .filter(
#             hotel_name=selected_organization_id,
#             IsDelete=False
#         )
#         .annotate(
#             row_ctc=ExpressionWrapper(
#                 F('avg_salary') * F('head_count'),
#                 output_field=FloatField()
#             )
#         )
#         .values(
#             'services_department_master__DepartmentName',
#             'services_designation_master__designations',
#             'services_designation_master__Lavel'
#         )
#         .annotate(
#             head_count=Sum('head_count'),
#             morning=Sum('morning'),
#             general_deta=Sum('general_deta'),
#             afternoon=Sum('afternoon'),
#             night=Sum('night'),
#             m_break=Sum('m_break'),
#             relievers=Sum('relievers'),
#             total_ctc=Sum('row_ctc')
#         )
#     )

#     if exclude_zero_headcount == '1':
#         qs = qs.exclude(head_count=0)

#     data = {}

#     # 1️⃣ Accumulate department + designation data
#     for row in qs:
#         dept = row['services_department_master__DepartmentName']

#         if dept not in data:
#             data[dept] = {
#                 "designations": [],
#                 "department_totals": {
#                     "HC": 0,
#                     "MORG": 0,
#                     "GEN": 0,
#                     "A_NOON": 0,
#                     "NIGHT": 0,
#                     "M_BREAK": 0,
#                     "RELI": 0,
#                     "Total_CTC": 0
#                 }
#             }

#         data[dept]["designations"].append({
#             "designation": row['services_designation_master__designations'],
#             "level": row['services_designation_master__Lavel'],
#             "HC": row['head_count'] or 0,
#             "MORG": row['morning'] or 0,
#             "GEN": row['general_deta'] or 0,
#             "A_NOON": row['afternoon'] or 0,
#             "NIGHT": row['night'] or 0,
#             "M_BREAK": row['m_break'] or 0,
#             "RELI": row['relievers'] or 0,
#             "Total_CTC": row['total_ctc'] or 0
#         })

#         totals = data[dept]["department_totals"]
#         totals["HC"] += row['head_count'] or 0
#         totals["MORG"] += row['morning'] or 0
#         totals["GEN"] += row['general_deta'] or 0
#         totals["A_NOON"] += row['afternoon'] or 0
#         totals["NIGHT"] += row['night'] or 0
#         totals["M_BREAK"] += row['m_break'] or 0
#         totals["RELI"] += row['relievers'] or 0
#         totals["Total_CTC"] += row['total_ctc'] or 0

#     # 2️⃣ Compute weighted Avg Salary
#     for dept, values in data.items():
#         totals = values["department_totals"]
#         hc = totals["HC"]
#         totals["Avg_Sal"] = round(
#             totals["Total_CTC"] / hc, 2
#         ) if hc > 0 else 0

#     return Response({
#         "organization_id": selected_organization_id,
#         "ex_zero": exclude_zero_headcount,
#         "shared_service_manning": data
#     })



def build_shared_service_structure():
    structure = {}

    divisions = ServicesDivisionMaster.objects.filter(
        IsDelete=False
    ).order_by('Order').prefetch_related(
        'servicesdepartmentmaster_set__servicesdesignationmaster_set'
    )

    for div in divisions:
        structure[div.DivisionName] = {
            "departments": {},
            "division_totals": {
                "head_count": 0,
                "total_ctc": 0,
                "avg_salary": 0
            }
        }

        for dept in div.servicesdepartmentmaster_set.all():
            structure[div.DivisionName]["departments"][dept.DepartmentName] = {
                "designations": [],
                    "department_totals": {
                        "HC": 0,
                        "Total_CTC": 0,
                        "Avg_Sal": 0
                    }
            }

            for des in dept.servicesdesignationmaster_set.all():
                structure[div.DivisionName]["departments"][dept.DepartmentName]["designations"].append({
                    "designation": des.designations,
                    "level": des.Lavel,
                    "head_count": 0,
                    "avg_salary": 0,
                    "total_ctc": 0,
                    "morning": 0,
                    "general_deta": 0,
                    "afternoon": 0,
                    "night": 0,
                    "m_break": 0,
                    "relievers": 0,
                })

    return structure


from django.db.models.functions import NullIf
@api_view(['GET'])
def shared_service_manning_api(request):
    selected_organization_id = request.GET.get('OID')
    exclude_zero_headcount = request.GET.get('ex_zero', '1')

    # 1️⃣ Always build structure
    structure = build_shared_service_structure()

    # 2️⃣ Budget query
    qs = (
        ManageBudgetSharedServices.objects
        .filter(hotel_name=selected_organization_id, IsDelete=False)
        .annotate(
            row_ctc=ExpressionWrapper(
                F('avg_salary') * F('head_count'),
                output_field=FloatField()
            )
        )
        .values(
            'services_department_master__DepartmentName',
            'services_designation_master__designations',
            'services_designation_master__Lavel'
        )
        .annotate(
            head_count=Sum('head_count'),
            morning=Sum('morning'),
            general_deta=Sum('general_deta'),
            afternoon=Sum('afternoon'),
            night=Sum('night'),
            m_break=Sum('m_break'),
            relievers=Sum('relievers'),
            total_ctc=Sum('row_ctc'),

            # ✅ FIXED weighted average
            avg_salary=ExpressionWrapper(
                Sum('row_ctc') / NullIf(F('head_count'), 0),
                output_field=FloatField()
            )
        )
    )

    if exclude_zero_headcount == '1':
        qs = qs.exclude(head_count=0)

    # 3️⃣ Inject data into structure
    for row in qs:
        dept_name = row['services_department_master__DepartmentName']

        for div in structure.values():
            if dept_name not in div["departments"]:
                continue

            dept = div["departments"][dept_name]
            

            for des in dept["designations"]:
                if des["designation"] == row['services_designation_master__designations']:
                    des.update({
                        "HC": row['head_count'] or 0,
                        "MORG": row['morning'] or 0,
                        "GEN": row['general_deta'] or 0,
                        "A_NOON": row['afternoon'] or 0,
                        "NIGHT": row['night'] or 0,
                        "M_BREAK": row['m_break'] or 0,
                        "RELI": row['relievers'] or 0,
                        "Avg_Sal": round(row['avg_salary'], 2) if row['head_count'] else 0,
                        "Total_CTC": row['total_ctc'] or 0
                    })

                    dept["department_totals"]["HC"] += row['head_count'] or 0
                    dept["department_totals"]["Total_CTC"] += row['total_ctc'] or 0
                    break
                
    # print(dept["department_totals"])

    # 4️⃣ Compute department averages
    for div in structure.values():
        for dept in div["departments"].values():
            hc = dept["department_totals"]["HC"]
            dept["department_totals"]["Avg_Sal"] = (
                round(dept["department_totals"]["Total_CTC"] / hc, 2)
                if hc > 0 else 0
            )

    return Response({
        "organization_id": selected_organization_id,
        "ex_zero": exclude_zero_headcount,
        "shared_service_manning": structure
    })


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import F, Sum, Count, ExpressionWrapper, FloatField

@api_view(['GET'])
def budget_summary_api(request):
    selected_organization_id = request.GET.get('hotel_name', request.session.get("OrganizationID"))
    exclude_zero_headcount = request.GET.get('exclude_zero_headcount','1')  

    # ------------------ OnRoll Budget ------------------
    managebudget_qs = ManageBudgetOnRoll.objects.filter(OrganizationID=selected_organization_id)
    if exclude_zero_headcount == '1':
        managebudget_qs = managebudget_qs.exclude(head_count=0)

    division_totals = {}
    grand_total_headcount = 0
    divisionmultiplication_result = 0

    for budget in managebudget_qs:
        hc = budget.head_count or 0
        total = (budget.avg_salary or 0) * hc

        division_name = budget.on_roll_division_master.DivisionName if budget.on_roll_division_master else "Unknown"

        division_totals.setdefault(division_name, {'divisionmultiplication_result': 0, 'divisiontotal_headcount': 0})
        division_totals[division_name]['divisionmultiplication_result'] += total
        division_totals[division_name]['divisiontotal_headcount'] += hc

    divisionmultiplication_result = sum(d['divisionmultiplication_result'] for d in division_totals.values())
    grand_total_headcount = sum(d['divisiontotal_headcount'] for d in division_totals.values())
    grandsalarydivion = divisionmultiplication_result / grand_total_headcount if grand_total_headcount > 0 else 0

    # ------------------ Contract Budget ------------------
    contract_qs = ManageBudgetContract.objects.filter(hotel_name=selected_organization_id)
    if exclude_zero_headcount == '1':
        contract_qs = contract_qs.exclude(head_count=0)

    Contractdivision_totals = {}
    Contractgrand_total_headcount = 0
    grandContractdivisionmultiplication_result = 0

    for budget in contract_qs:
        hc = budget.head_count or 0
        total = (budget.avg_salary or 0) * hc

        division_name = budget.contract_department_master.on_roll_division_master.DivisionName if budget.contract_department_master else "Unknown"

        Contractdivision_totals.setdefault(division_name, {'Contractdivisionmultiplication_result': 0, 'Contractdivisiontotal_headcount': 0})
        Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] += total
        Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] += hc

    grandContractdivisionmultiplication_result = sum(d['Contractdivisionmultiplication_result'] for d in Contractdivision_totals.values())
    Contractgrand_total_headcount = sum(d['Contractdivisiontotal_headcount'] for d in Contractdivision_totals.values())
    contractgrandsalarydivion = grandContractdivisionmultiplication_result / Contractgrand_total_headcount if Contractgrand_total_headcount > 0 else 0

    # ------------------ Shared Services Budget ------------------
    services_qs = ManageBudgetSharedServices.objects.filter(hotel_name=selected_organization_id)
    if exclude_zero_headcount == '1':
        services_qs = services_qs.exclude(head_count=0)

    Servicesdivision_totals = {}
    ServicesContractgrand_total_headcount = 0
    Servicesgranddivisionmultiplication_result = 0

    for budget in services_qs:
        hc = budget.head_count or 0
        total = (budget.avg_salary or 0) * hc

        division_name = budget.services_department_master.servicesdivisionmaster.DivisionName if budget.services_department_master else "Unknown"

        Servicesdivision_totals.setdefault(division_name, {'Servicedivisionmultiplication_result': 0, 'Servicedivisiontotal_headcount': 0})
        Servicesdivision_totals[division_name]['Servicedivisionmultiplication_result'] += total
        Servicesdivision_totals[division_name]['Servicedivisiontotal_headcount'] += hc

    Servicesgranddivisionmultiplication_result = sum(d['Servicedivisionmultiplication_result'] for d in Servicesdivision_totals.values())
    ServicesContractgrand_total_headcount = sum(d['Servicedivisiontotal_headcount'] for d in Servicesdivision_totals.values())
    Servicesgrandsalarydivion = Servicesgranddivisionmultiplication_result / ServicesContractgrand_total_headcount if ServicesContractgrand_total_headcount > 0 else 0

    # ------------------ Meal & Insurance ------------------
    meal_cost = getattr(BudgetMealCost.objects.filter(hotel_name=selected_organization_id).first(), 'cafeteriamealcost', 0)
    Insurance_cost = getattr(BudgetInsuranceCost.objects.filter(hotel_name=selected_organization_id).first(), 'EmployeeInsurancecost', 0)

    Benefitesheadtotal = grand_total_headcount + Contractgrand_total_headcount + ServicesContractgrand_total_headcount
    Benefitetotalctc = divisionmultiplication_result + grandContractdivisionmultiplication_result + Servicesgranddivisionmultiplication_result + meal_cost + Insurance_cost

    Avgsalarytotalctc = Benefitetotalctc / Benefitesheadtotal if Benefitesheadtotal > 0 else 0
    Avgsalarymealcoat = meal_cost / Benefitesheadtotal if Benefitesheadtotal > 0 else 0
    Avgsalaryinsurancecoat = Insurance_cost / Benefitesheadtotal if Benefitesheadtotal > 0 else 0

    # ------------------ Response ------------------
    return Response({
        'grandsalarydivion':grandsalarydivion,
        'grand_total_headcount': grand_total_headcount,
        'divisionmultiplication_result':divisionmultiplication_result,

        'contractgrandsalarydivion':contractgrandsalarydivion,
        'Contractgrand_total_headcount':Contractgrand_total_headcount,
        'grandContractdivisionmultiplication_result':grandContractdivisionmultiplication_result,

        'Servicesgrandsalarydivion':Servicesgrandsalarydivion,
        'ServicesContractgrand_total_headcount':ServicesContractgrand_total_headcount,
        'Servicesgranddivisionmultiplication_result':Servicesgranddivisionmultiplication_result,

        'Avgsalarymealcoat':Avgsalarymealcoat,
        'meal_cost':meal_cost,

        'Avgsalaryinsurancecoat':Avgsalaryinsurancecoat,
        'Insurance_cost':Insurance_cost,

        'Avgsalarytotalctc':Avgsalarytotalctc,
        'Benefitesheadtotal':Benefitesheadtotal,
        'Benefitetotalctc':Benefitetotalctc,
    })




from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import F, Sum, Count, ExpressionWrapper, FloatField, Case, When, IntegerField
from django.db.models.functions import Trim, Coalesce

@api_view(['GET'])
def budget_api(request):
    # ------------------ Session & Access ------------------
    # OrganizationID = request.session.get("OID")
    UserID = str(request.session.get("UserID"))
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")

    # if OrganizationID == '3' or UserType == 'GM' or Department_Name == 'HR':
    #     pass
    # else:
    #     return Response({"error": "No Access"}, status=403)

    selected_division = "All Division"
    selected_department = "All Department"
    selected_organization_id = request.GET.get('OID')
    exclude_zero_headcount = request.GET.get('exclude_zero_headcount','1')  

    # if UserType == 'CEO' and request.GET.get('hotel_name') is None:
    #     selected_organization_id = 401

    # ------------------ Query Divisions & Departments ------------------
    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False)
    departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)

    if selected_division and selected_division != 'All Division':
        Divisiondatas = Divisiondatas.filter(DivisionName=selected_division)
        departments = OnRollDepartmentMaster.objects.filter(
            OnRollDivisionMaster__DivisionName=selected_division, IsDelete=False
        )

    if selected_department and selected_department != 'All Department':
        departments = departments.filter(DepartmentName=selected_department)

    # ------------------ Filter Designations ------------------
    filtered_designations = OnRollDesignationMaster.objects.filter(
        IsDelete=False
    ).annotate(
        level_order=Case(
            When(Lavel='M6', then=1),
            When(Lavel='M5', then=2),
            When(Lavel='M4', then=3),
            When(Lavel='M3', then=4),
            When(Lavel='M2', then=5),
            When(Lavel='M1', then=6),
            When(Lavel='M', then=7),
            When(Lavel='E', then=8),
            When(Lavel='T', then=9),
            When(Lavel='A', then=10),
            default=99,
            output_field=IntegerField()
        )
    ).order_by('level_order', 'Order')

    # ------------------ OnRoll Budget ------------------
    managebudget_department_designation = ManageBudgetOnRoll.objects.annotate(
        clean_hotel_name=Trim('hotel_name')  
    ).filter(
        clean_hotel_name=selected_organization_id,  
        is_delete=False
    ).values(
        'on_roll_division_master__DivisionName',
        'on_roll_department_master__DepartmentName',
        'on_roll_designation_master__designations'
    ).annotate(
        head_count=F('head_count'),
        total_salary=Sum('avg_salary'),
        aavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        budgetmultiplication_result=ExpressionWrapper(F('aavg_salary') * F('head_count'), output_field=FloatField())
    ).order_by(
        'on_roll_division_master__DivisionName',
        'on_roll_department_master__DepartmentName',
        'on_roll_designation_master__designations'
    )

    if exclude_zero_headcount == '1':
        managebudget_department_designation = managebudget_department_designation.exclude(head_count=0)

    # ------------------ Build Response Dicts ------------------
    budgets_dict = {}
    department_totals = {}
    division_totals = {}

    for budget in managebudget_department_designation:
        dept_id = budget['on_roll_department_master__DepartmentName']
        desig_id = budget['on_roll_designation_master__designations']

        budgets_dict.setdefault(dept_id, {})[desig_id] = {
            'head_count': budget['head_count'],
            'aavg_salary': budget['aavg_salary'],
            'budgetmultiplication_result': budget['budgetmultiplication_result'],
        }

        department_totals.setdefault(dept_id, {
            'budgetmultiplication_result': 0,
            'total_headcount': 0,
            'salary_headcount_product': 0,
        })

        department_totals[dept_id]['budgetmultiplication_result'] += budget.get('budgetmultiplication_result', 0) or 0
        department_totals[dept_id]['total_headcount'] += budget.get('head_count', 0) or 0

        if department_totals[dept_id]['total_headcount'] > 0:
            department_totals[dept_id]['salary_headcount_product'] = (
                department_totals[dept_id]['budgetmultiplication_result'] / department_totals[dept_id]['total_headcount']
            )

        # Division totals
        divisions_qs = OnRollDivisionMaster.objects.filter(
            onrolldepartmentmaster__DepartmentName=dept_id
        ).annotate(division_name=F('DivisionName')).values('division_name')
        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name:
            division_totals.setdefault(division_name, {
                'divisionmultiplication_result': 0,
                'divisiontotal_headcount': 0,
                'divisionsalary_headcount_product': 0,
            })

            division_totals[division_name]['divisionmultiplication_result'] += budget.get('budgetmultiplication_result', 0) or 0
            division_totals[division_name]['divisiontotal_headcount'] += budget.get('head_count', 0) or 0

            if division_totals[division_name]['divisiontotal_headcount'] > 0:
                division_totals[division_name]['divisionsalary_headcount_product'] = (
                    division_totals[division_name]['divisionmultiplication_result'] / division_totals[division_name]['divisiontotal_headcount']
                )

    divisionmultiplication_result = sum(d['divisionmultiplication_result'] for d in division_totals.values())
    grand_total_headcount = sum(d['divisiontotal_headcount'] for d in division_totals.values())
    grandsalarydivion = divisionmultiplication_result / grand_total_headcount if grand_total_headcount > 0 else 0

    # ------------------ Contract & Shared Services Budget ------------------
    # ...repeat same logic as OnRoll for Contract and Shared Services
    # ...for brevity, you can wrap into helper functions to avoid duplication

    # ------------------ Meal & Insurance ------------------
    meal_cost = BudgetMealCost.objects.filter(hotel_name=selected_organization_id).first()
    meal_cost = meal_cost.cafeteriamealcost if meal_cost else 0

    Insurance_cost_record = BudgetInsuranceCost.objects.filter(hotel_name=selected_organization_id).first()
    Insurance_cost = Insurance_cost_record.EmployeeInsurancecost if Insurance_cost_record and Insurance_cost_record.EmployeeInsurancecost else 0

    insuranceheadcount = grand_total_headcount  # + other budgets if needed
    Avgsalaryinsurancecoat = Insurance_cost / insuranceheadcount if insuranceheadcount > 0 else 0
    Avgsalarymealcoat = meal_cost / insuranceheadcount if insuranceheadcount > 0 else 0

    # ------------------ Final Response ------------------
    response = {
        'grandsalarydivion': grandsalarydivion,
        'grand_total_headcount': grand_total_headcount,
        'divisionmultiplication_result': divisionmultiplication_result,
        'Avgsalarymealcoat': Avgsalarymealcoat,
        'meal_cost': meal_cost,
        'Avgsalaryinsurancecoat': Avgsalaryinsurancecoat,
        'Insurance_cost': Insurance_cost,
    }

    return Response(response)

