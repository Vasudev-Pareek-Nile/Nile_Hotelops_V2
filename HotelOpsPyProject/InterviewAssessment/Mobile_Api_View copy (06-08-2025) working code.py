from datetime import datetime
import calendar
from HumanResources.views import MultipleDepartmentofEmployee
from django.shortcuts import render,redirect,render
from app.views import OrganizationList,Error
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from .models import Assessment_Master,Assessment_Factor_Details,Assessment_MasterDeletedFile,UserTypeFlow,DepartmentLevelConfig,DepartmentLevelConfigDetails,Factors,EmployeeDataRequest_Master,EmployeePersonalDataDeletedFile,EmployeePersonalData, EmployeeFamilyData, EmployeeEmergencyInfoData
from Manning_Guide.models import OnRollDepartmentMaster,LavelAdd,OnRollDesignationMaster
from .azure import upload_file_to_blob,download_blob
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
import datetime
from Open_position.models import CareerResume
from InterviewAssessment.views import AppliedForORGID,HODLevel,LastApprovalStageFun,repalce_file,upload_file,CopyFileResume,CheckHeadDepartment,ApprovalStageFun
from io import BytesIO

from app.models import OrganizationMaster

from Reference_check.models import ReferenceDetails

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import calendar
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status as rest_status
import calendar
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status as rest_status
from datetime import datetime, date
from django.utils import timezone

from .serializers import *


# ------------------------------------- / 100 % Working Code --------------------------------------------------------------------
import re

def strip_html_tags(text):
    if text is None:
        return ''
    return re.sub('<[^<]+?>', '', text)


@api_view(['GET'])
def InterviewAssessment_Mobile_List_Api(request):
    OrganizationID_Session = request.query_params.get('OrganizationID_Session')
    OrganizationID = request.query_params.get('OrganizationID')
    Level = request.query_params.get('Level', 'All')
    Status = request.query_params.get('Status', 'All')
    LOIstatus = request.query_params.get('LOIstatus', 'All')
    month_no = request.query_params.get('month_no')
    year = request.query_params.get('year')
    # UserType = str(request.session.get("UserType", '')).lower()
    UserType = request.query_params.get("UserType", '').lower()
    UserID = request.query_params.get("UserID")
    EmployeeCode = request.query_params.get("EmployeeCode")

    ActionButton = False
    if UserType:
        if UserType == "ceo":
            ActionButton = True
    else:
        print("UserType is not CEO")


    # print("New ------------------------------------------------")
    # print("UserType ", UserType)
    # print("I ", OrganizationID)
    # print("OrganizationID type", type(OrganizationID))
    # print("OrganizationID ", OrganizationID)
    # print("UserID ", UserID)
    # print("SessionOrganizationID ", SessionOrganizationID)
    # print("EmployeeCode ", EmployeeCode)
    # print("year ", year)
    # print("month_no ", month_no)
    # print("Level ", Level)
    # print("Status ", Status)
    # print("LOIstatus ", LOIstatus)
    # print("/ End ------------------------------------------------")

    if OrganizationID_Session == "3" and (OrganizationID == '' or None):
        OrganizationID = OrganizationID_Session



    # year = request.query_params.get('year')
    year = int(year) if year else datetime.now().year

    # month_no = request.query_params.get('month_no')
    month_no = int(month_no) if month_no and month_no != 'All' else None
    month_name = "All Months" if not month_no else calendar.month_name[month_no]

    today = datetime.today()
    CYear = today.year
    CMonth = today.month


    DepartmentList = []
    if EmployeeCode:
        Departmentobj = MultipleDepartmentofEmployee(OrganizationID_Session, EmployeeCode)
        if Departmentobj:
            DepartmentList = Departmentobj
        else:
            return Response({'error': 'Employee Details not Found. Update in Human Resources.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Employee Code is required.'}, status=status.HTTP_400_BAD_REQUEST)

    Department = 'hr' if 'Human Resources' in DepartmentList else ''
    # UserType = str(request.session.get("UserType", '')).lower()
    if OrganizationID == '3' and UserType == 'hod':
        UserType = 'rd'

    I = OrganizationID
    if OrganizationID == "3":
        I = 'All'

    assessments_filter = {'IsDelete': False, 'InterviewDate__year': year}
    if month_no:
        assessments_filter['InterviewDate__month'] = month_no
    if I != 'All':
        assessments_filter['OrganizationID'] = I
    if Level != 'All':
        assessments_filter['Level'] = Level
    if Status != 'All':
        assessments_filter['LastApporvalStatus'] = Status
    else:
        assessments_filter['LastApporvalStatus__in'] = ['Approved', 'Pending']
    if LOIstatus != 'All':
        assessments_filter['LOIStatus'] = LOIstatus

    Assessments = Assessment_Master.objects.filter(**assessments_filter).order_by('-CreatedDateTime')

    AssessmentsList = []

    for Assessment in Assessments:
        ref = 'Fresher'
        if Assessment.workexperience != 'Fresher':
            ref = 0
            if Assessment.reference:
                refobj = ReferenceDetails.objects.filter(
                    IsDelete=False, OrganizationID=OrganizationID, Inteview_AssementID=Assessment.id
                ).first()
                if refobj and refobj.ref1_status == 1:
                    ref = 1
                if isinstance(Assessment.reference, str):
                    ref = 1
        Assessment.ref = ref

        AssessmentDepartment = Assessment.Department
        head_department_obj = CheckHeadDepartment(AssessmentDepartment, Assessment.Level, OrganizationID)
        head_department = head_department_obj.HeadDepartment if head_department_obj else ''

        ApprovalStageFunobj = ApprovalStageFun(Assessment.Level, Assessment.Department, Assessment.OrganizationID)

        Found = False
        if UserID == '20230110136226':
            Found = True
        elif not ApprovalStageFunobj:
            if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
                Found = True
        else:
            if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
                Found = True
            elif UserType.lower() in [item.lower() for item in ApprovalStageFunobj]:
                Found = True

        if UserType != "ceo":
            if Found and (
                any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]) or UserID == '20230110136226'
            ):
                AssessmentsList.append(Assessment)
            elif AssessmentDepartment.strip() in DepartmentList or head_department.strip() in DepartmentList:
                if Found:
                    AssessmentsList.append(Assessment)
        elif Found:
            AssessmentsList.append(Assessment)
        

    # Serialize the assessments into basic dictionaries
    assessment_data = []
    for ass in AssessmentsList:
        org = OrganizationMaster.objects.filter(
            IsDelete=False, Activation_status=1, OrganizationID=ass.OrganizationID
        ).values_list('ShortDisplayLabel', flat=True).first()

        assessment_data.append({
            'id': ass.id,
            'Hotel':org,
            'CandidateName': f"{ass.Prefix or ''} {ass.Name or ''}".strip(),
            'Designation':ass.position,
            'hr_as':ass.hr_as,
            'hod_as':ass.hod_as,
            'rd_as':ass.rd_as,
            'gm_as':ass.gm_as,
            'ceo_as':ass.ceo_as,
            # 'CandidateName': ass.Name,
            # 'InterviewDate': ass.InterviewDate.strftime("%Y-%m-%d") if ass.InterviewDate else None,
            # 'Department': ass.Department,
            'Level': ass.Level,
            'LastApporvalStatus': ass.LastApporvalStatus,
            # 'LOIStatus': ass.LOIStatus,
            # 'ref': ass.ref,
            'OrganizationID':ass.OrganizationID,
            'ActionButtons':ActionButton,
            'Status': {
                "Approved  From": ass.Approval_stage_mobile_responce(),
                "Pending From": ass.pending_status_mobile_responce(),
            },
        })

    return JsonResponse({
        'Assessments': assessment_data,
    })



# ------------------------------------- Trial Version (count API) --------------------------------------------------------------------

@api_view(['GET'])
def InterviewAssessment_Mobile_Count_Api(request):
    OrganizationID_Session = request.query_params.get('OrganizationID_Session')
    OrganizationID = request.query_params.get('OrganizationID')
    Level = request.query_params.get('Level', 'All')
    Status = request.query_params.get('Status', 'All')
    LOIstatus = request.query_params.get('LOIstatus', 'All')
    month_no = request.query_params.get('month_no')
    year = request.query_params.get('year')
    # UserType = str(request.session.get("UserType", '')).lower()
    UserType = request.query_params.get("UserType", '').lower()
    UserID = request.query_params.get("UserID")
    EmployeeCode = request.query_params.get("EmployeeCode")


    if OrganizationID_Session == "3" and (OrganizationID == '' or None):
        OrganizationID = OrganizationID_Session



    # year = request.query_params.get('year')
    year = int(year) if year else datetime.now().year

    # month_no = request.query_params.get('month_no')
    month_no = int(month_no) if month_no and month_no != 'All' else None
    month_name = "All Months" if not month_no else calendar.month_name[month_no]

    # today = datetime.today()
    # CYear = today.year
    # CMonth = today.month
    
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)
    today_yesterday_count = 0


    DepartmentList = []
    if EmployeeCode:
        Departmentobj = MultipleDepartmentofEmployee(OrganizationID_Session, EmployeeCode)
        if Departmentobj:
            DepartmentList = Departmentobj
        else:
            return Response({'error': 'Employee Details not Found. Update in Human Resources.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Employee Code is required.'}, status=status.HTTP_400_BAD_REQUEST)

    Department = 'hr' if 'Human Resources' in DepartmentList else ''
    # UserType = str(request.session.get("UserType", '')).lower()
    if OrganizationID == '3' and UserType == 'hod':
        UserType = 'rd'

    I = OrganizationID
    if OrganizationID == "3":
        I = 'All'

    assessments_filter = {'IsDelete': False, 'InterviewDate__year': year}
    if month_no:
        assessments_filter['InterviewDate__month'] = month_no
    if I != 'All':
        assessments_filter['OrganizationID'] = I
    if Level != 'All':
        assessments_filter['Level'] = Level
    if Status != 'All':
        assessments_filter['LastApporvalStatus'] = Status
    else:
        assessments_filter['LastApporvalStatus__in'] = ['Approved', 'Pending']
    if LOIstatus != 'All':
        assessments_filter['LOIStatus'] = LOIstatus

    Assessments = Assessment_Master.objects.filter(**assessments_filter).order_by('-CreatedDateTime')

    AssessmentsList = []


    for Assessment in Assessments:
        ref = 'Fresher'
        if Assessment.workexperience != 'Fresher':
            ref = 0
            if Assessment.reference:
                refobj = ReferenceDetails.objects.filter(
                    IsDelete=False, OrganizationID=OrganizationID, Inteview_AssementID=Assessment.id
                ).first()
                if refobj and refobj.ref1_status == 1:
                    ref = 1
                if isinstance(Assessment.reference, str):
                    ref = 1
        Assessment.ref = ref

        AssessmentDepartment = Assessment.Department
        head_department_obj = CheckHeadDepartment(AssessmentDepartment, Assessment.Level, OrganizationID)
        head_department = head_department_obj.HeadDepartment if head_department_obj else ''

        ApprovalStageFunobj = ApprovalStageFun(Assessment.Level, Assessment.Department, Assessment.OrganizationID)

        Found = False
        if UserID == '20230110136226':
            Found = True
        elif not ApprovalStageFunobj:
            if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
                Found = True
        else:
            if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
                Found = True
            elif UserType.lower() in [item.lower() for item in ApprovalStageFunobj]:
                Found = True

        if UserType != "ceo":
            if Found and (
                any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]) or UserID == '20230110136226'
            ):
                AssessmentsList.append(Assessment)
            elif AssessmentDepartment.strip() in DepartmentList or head_department.strip() in DepartmentList:
                if Found:
                    AssessmentsList.append(Assessment)
        elif Found:
            AssessmentsList.append(Assessment)
        
            # 👇 Count today or yesterday
        if Assessment.InterviewDate and Assessment.CreatedDateTime.date() in [today, yesterday]:
            today_yesterday_count += 1

    # Serialize the assessments into basic dictionaries
    assessment_data = []
    for ass in AssessmentsList:
        org = OrganizationMaster.objects.filter(
            IsDelete=False, Activation_status=1, OrganizationID=ass.OrganizationID
        ).values_list('ShortDisplayLabel', flat=True).first()

        assessment_data.append({
            'id': ass.id,
            'Hotel':org,
            'CandidateName': f"{ass.Prefix or ''} {ass.Name or ''}".strip(),
            'Designation':ass.position,
            # 'CandidateName': ass.Name,
            # 'InterviewDate': ass.InterviewDate.strftime("%Y-%m-%d") if ass.InterviewDate else None,
            # 'Department': ass.Department,
            'Level': ass.Level,
            'LastApporvalStatus': ass.LastApporvalStatus,
            # 'LOIStatus': ass.LOIStatus,
            # 'ref': ass.ref,
            'OrganizationID':ass.OrganizationID,
        })

    return JsonResponse({
        # 'Assessments': assessment_data,
        'total_count': len(assessment_data),
        'today_yesterday_count': today_yesterday_count
    })



#  ---------------- Trial Version of Filters api's ------------
@api_view(['GET'])
def InterviewAssessment_Filters_Api(request):
    # Fixed_Token = 'xyz'
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'

    # AccessToken = request.query_params.get('Token')
    AccessToken = request.headers.get('Authorization', '')

    if AccessToken:
        if AccessToken == Fixed_Token:
            pass
        else:
            return Response({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Token Not Found, Please Provide Correct Token.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        OrganizationID = request.query_params.get("OrganizationID")
        # UserID = request.query_params.get("UserID")
        # EmployeeCode = request.query_params.get("EmployeeCode")
        # Status = request.query_params.get("status", '').lower()
        # UserType = request.query_params.get("UserType", '').lower()
        # I = request.query_params.get('I', OrganizationID)
        

        # if not OrganizationID:
        #     return Response({'error': 'Organization ID is required.'}, status=status.HTTP_400_BAD_REQUEST)


        # year = datetime.now().year
        today = datetime.today()
        CYear = today.year
        CMonth = today.month


        # if OrganizationID == '3' and UserType == 'hod':
        #     UserType = 'rd'

        # if OrganizationID == "3" and Status == 'all':
        #     OrganizationID = request.query_params.get('I') or ''

        if OrganizationID == '3':
            orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1)
        else:
            orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1, OrganizationID=OrganizationID)

        org_list = list(orgs.values('OrganizationID', 'ShortDisplayLabel'))

        if not org_list:
            org_list = 'No Organization data found.'

        levels = list(LavelAdd.objects.filter(IsDelete=False).values('id', 'lavelname'))

        if not levels:
            levels = 'No level data found.'

        context = {
            'Selected_Organization':OrganizationID,
            'Organizations': org_list,
            'Levels': levels,
            'Status': ['All', 'Pending', 'Approved', 'Rejected', 'Closed'],  
            'LOI_status': ['All', 'Pending', 'Accepted', 'Rejected', 'Shared', 'Draft'],      
            'Current_Month': CMonth,
            'Month_Name_List': ['All','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
            'Current_Year': CYear,
            'Year_List': list(range(CYear, 2020, -1)),
        }

        return Response(context, status=rest_status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
    




@api_view(['POST'])
def InterviewAssessment_CEO_Action_Api(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    # AccessToken = request.query_params.get('Token')
    # UserType_Session = request.query_params.get("UserType", '').lower()
    # AccessToken = request.headers.get('Token')  # OR 'Authorization'
    # UserType_Session = request.headers.get('UserType', '').lower()

    UserType_Session = request.headers.get('UserType', '').lower()
    AccessToken = request.headers.get('Authorization', '')

    print("Token from header:", AccessToken)
    print("Expected token   :", Fixed_Token)

    if not AccessToken:
        return Response({'error': 'Token Not Found, Please Provide Correct Token.'}, status=status.HTTP_400_BAD_REQUEST)

    if AccessToken != Fixed_Token:
        return Response({'error': 'Please Provide The Correct Token, Token Not Match.'}, status=status.HTTP_400_BAD_REQUEST)
    # Validate UserType

    if not UserType_Session:
        return Response({'error': 'UserType Not Found, Please Provide Correct UserType.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if UserType_Session != 'ceo':
        return Response({'error': 'Please Provide The Correct UserType, UserType Not Match.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        Assessment_Id = request.data.get('AID')
        Assessment_OrganizationID = request.data.get('OID')
        StatusValue = request.data.get('Status', '').strip().lower()
        Remarks = request.data.get('Remarks', '').strip()
        UserID = request.data.get('UserID')

        if not Assessment_Id or not StatusValue or not Assessment_OrganizationID:
            return Response({'message': 'Missing required parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        obj = Assessment_Master.objects.filter(id=Assessment_Id, IsDelete=False).first()
        if not obj:
            return Response({'message': 'Assessment not found.'}, status=status.HTTP_404_NOT_FOUND)

        obj.ceo_as = StatusValue
        obj.ceo_as_remarks = Remarks
        obj.ceo_actionOn = date.today()
        obj.ceo_actionOnDatetime = timezone.now()

        LastApprovalStage = LastApprovalStageFun(obj.Level, obj.Department, Assessment_OrganizationID)
        if LastApprovalStage and LastApprovalStage.lower() == "ceo":
            obj.LastApporvalStatus = StatusValue

        obj.ModifyBy = UserID
        obj.save()

        Raw_Data = {
            "AID": Assessment_Id,
            "OID": Assessment_OrganizationID,
            "Status": StatusValue,
            "Remarks": Remarks,
            "UserID": UserID,
            "UserType": UserType_Session
        }

        return Response({'message': f'{StatusValue} successfully'}, status=status.HTTP_200_OK)
        # return Response({'message': f'{StatusValue} successfully', 'data': Raw_Data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
def InterviewAssessment_Entire_List_Api(request):
    emp_id = request.GET.get('id')  # or 'EmpID'
    # org_id = request.GET.get('OID')  # or 'OrganizationID'

    if not emp_id:
        return Response({'error': 'Missing parameters'}, status=400)

    assessments = Assessment_Master.objects.filter(id=emp_id, IsDelete=False)
    serializer = AssessmentMasterMinimalSerializer(assessments, many=True)
    return Response(serializer.data)




from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Assessment_Master, Assessment_Factor_Details
# from MasterSettings.models import MasterAttribute
from .views import MasterJSON

def InterviewAssessment_Mobile_Api_Pdf(request):
    AID = request.GET.get('AID')

    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    # AccessToken = request.query_params.get('Token')
    # UserType_Session = request.query_params.get("UserType", '').lower()
    # AccessToken = request.headers.get('Token')  # OR 'Authorization'
    # UserType_Session = request.headers.get('UserType', '').lower()

    UserType_Session = request.headers.get('UserType', '').lower()
    AccessToken = request.headers.get('Authorization', '')

    # print("Token from header:", AccessToken)
    # print("Expected token   :", Fixed_Token)

    if not AccessToken:
        return HttpResponse('Token Not Found, Please Provide Correct Token.',content_type='text/plain')

    if AccessToken != Fixed_Token:
        return HttpResponse('Please Provide The Correct Token, Token Not Match.',content_type='text/plain')
    # Validate UserType

    if not UserType_Session:
        return HttpResponse('UserType Not Found, Please Provide Correct UserType.', content_type='text/plain')
    

    if not AID:
        return HttpResponse("Assessment ID is required", content_type='text/plain')

    AM_obj = Assessment_Master.objects.filter(IsDelete=False, id=AID).first()
    if not AM_obj:
        return HttpResponse("Invalid Assessment ID", content_type='text/plain')

    UserList = ApprovalStageFun(AM_obj.Level, AM_obj.Department, AM_obj.AppliedFor)

    # print("UserList = ", UserList)
    factor_details = Assessment_Factor_Details.objects.filter(
        MasterID=AID,
        hr_rating__isnull=False,
        hod_rating__isnull=False,
        gm_rating__isnull=False,
        rd_rating__isnull=False
    ).values(
        'CategoryID', 'factor', 'hr_rating', 'hr_remarks',
        'hod_rating', 'hod_remarks', 'gm_rating',
        'gm_remarks', 'rd_rating', 'rd_remarks'
    )

    factor_details_dict = {}
    for factor in factor_details:
        category_id = factor['CategoryID']
        if category_id not in factor_details_dict:
            factor_details_dict[category_id] = []
        factor_details_dict[category_id].append(factor)

    # Fill missing factors from MasterJSON
    for category in MasterJSON:
        category_id = category['CategoryID']
        if category_id not in factor_details_dict:
            factor_details_dict[category_id] = []

        for item in category['Item']:
            # If the factor is missing, add it from MasterJSON
            matching_factor = next(
                (f for f in factor_details_dict[category_id] if f.get('factor') == item['Title']),
                None
            )
            if not matching_factor or not matching_factor.get('factor'):
                factor_details_dict[category_id].append({
                    'CategoryID': category_id,
                    'factor': item['Title'],
                    'hr_rating': None,
                    'hr_remarks': None,
                    'hod_rating': None,
                    'hod_remarks': None,
                    'gm_rating': None,
                    'gm_remarks': None,
                    'rd_rating': None,
                    'rd_remarks': None
                })
    from django.forms.models import model_to_dict
    # print("AM_obj is here::", AM_obj)
    data = model_to_dict(AM_obj)
    # print(data)

    Organization_Name = None
    if AM_obj.OrganizationID:
        Organization_Name = OrganizationMaster.objects.filter(
            IsDelete=False,
            Activation_status=1,
            OrganizationID=AM_obj.OrganizationID
        ).values_list('OrganizationName', flat=True).first()

    # Attach to AM_obj for template use
    AM_obj.OrganizationName = Organization_Name

    context = {
        'AM_obj': AM_obj,
        'factor_details_dict': factor_details_dict,
        'MasterJSON': MasterJSON,
        'UserList': UserList
    }

    template_path = 'InterviewAssessment/Mobile_View_Pdf/IA_view_Pdf_Mobile.html'  
    # template_path = 'InterviewAssessment/InterviewAssessmentPdf.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="InterviewAssessment.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error generating PDF', content_type='text/plain')





# --------------------------- Trail Api ::: 04-08-2025 ----


@api_view(['GET'])
def InterviewAssessment_Mobile_List_Api_Ceo_Pending(request):

    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    # AccessToken = request.query_params.get('Token')
    # UserType_Session = request.query_params.get("UserType", '').lower()
    # AccessToken = request.headers.get('Token')  # OR 'Authorization'
    # UserType_Session = request.headers.get('UserType', '').lower()

    UserType = request.headers.get('UserType', '').lower()
    AccessToken = request.headers.get('Authorization', '')

    # print("Token from header:", AccessToken)
    # print("Expected token   :", Fixed_Token)

    if not AccessToken:
        return HttpResponse('Token Not Found, Please Provide Correct Token.',content_type='text/plain')

    if AccessToken != Fixed_Token:
        return HttpResponse('Please Provide The Correct Token, Token Not Match.',content_type='text/plain')
    # Validate UserType

    if not UserType:
        return HttpResponse('UserType Not Found, Please Provide Correct UserType.', content_type='text/plain')
    

    OrganizationID_Session = request.query_params.get('OrganizationID_Session')
    OrganizationID = request.query_params.get('OrganizationID')
    Level = request.query_params.get('Level', 'All')
    Status = request.query_params.get('Status', 'All').lower()
    LOIstatus = request.query_params.get('LOIstatus', 'All')
    month_no = request.query_params.get('month_no')
    year = request.query_params.get('year')
    # UserType = str(request.session.get("UserType", '')).lower()
    # UserType = request.query_params.get("UserType", '').lower()
    UserID = request.query_params.get("UserID")
    EmployeeCode = request.query_params.get("EmployeeCode")

    ActionButton = False
    if UserType:
        if UserType == "ceo":
            ActionButton = True
    else:
        print("UserType is not CEO")


    if OrganizationID_Session == "3" and (OrganizationID == '' or None):
        OrganizationID = OrganizationID_Session

    # year = request.query_params.get('year')
    year = int(year) if year else datetime.now().year

    # month_no = request.query_params.get('month_no')
    month_no = int(month_no) if month_no and month_no != 'All' else None
    month_name = "All Months" if not month_no else calendar.month_name[month_no]

    today = datetime.today()
    CYear = today.year
    CMonth = today.month


    DepartmentList = []
    if EmployeeCode:
        Departmentobj = MultipleDepartmentofEmployee(OrganizationID_Session, EmployeeCode)
        if Departmentobj:
            DepartmentList = Departmentobj
        else:
            return Response({'error': 'Employee Details not Found. Update in Human Resources.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Employee Code is required.'}, status=status.HTTP_400_BAD_REQUEST)

    Department = 'hr' if 'Human Resources' in DepartmentList else ''
    # UserType = str(request.session.get("UserType", '')).lower()
    if OrganizationID == '3' and UserType == 'hod':
        UserType = 'rd'

    I = OrganizationID
    if OrganizationID == "3":
        I = 'all'

    assessments_filter = {'IsDelete': False, 'InterviewDate__year': year}
    if month_no:
        assessments_filter['InterviewDate__month'] = month_no
    if I != 'all':
        assessments_filter['OrganizationID'] = I
    if Level != 'all':
        assessments_filter['Level'] = Level
    else:
        assessments_filter['Level__in'] = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']

    if Status != 'all':
        assessments_filter['LastApporvalStatus'] = Status
    else:
        # assessments_filter['LastApporvalStatus__in'] = ['Approved', 'Pending']
        assessments_filter['LastApporvalStatus__in'] = ['Pending']
    if LOIstatus != 'all':
        assessments_filter['LOIStatus'] = LOIstatus
    
    # assessments_filter['Level__in'] = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']

    Assessments = Assessment_Master.objects.filter(**assessments_filter).order_by('-CreatedDateTime')

    AssessmentsList = []

    for Assessment in Assessments:
        ref = 'Fresher'
        if Assessment.workexperience != 'Fresher':
            ref = 0
            if Assessment.reference:
                refobj = ReferenceDetails.objects.filter(
                    IsDelete=False, OrganizationID=OrganizationID, Inteview_AssementID=Assessment.id
                ).first()
                if refobj and refobj.ref1_status == 1:
                    ref = 1
                if isinstance(Assessment.reference, str):
                    ref = 1
        Assessment.ref = ref

        AssessmentDepartment = Assessment.Department
        head_department_obj = CheckHeadDepartment(AssessmentDepartment, Assessment.Level, OrganizationID)
        head_department = head_department_obj.HeadDepartment if head_department_obj else ''

        ApprovalStageFunobj = ApprovalStageFun(Assessment.Level, Assessment.Department, Assessment.OrganizationID)

        Found = False
        if UserID == '20230110136226':
            Found = True
        elif not ApprovalStageFunobj:
            if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
                Found = True
        else:
            if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
                Found = True
            elif UserType.lower() in [item.lower() for item in ApprovalStageFunobj]:
                Found = True

        if UserType != "ceo":
            if Found and (
                any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]) or UserID == '20230110136226'
            ):
                AssessmentsList.append(Assessment)
            elif AssessmentDepartment.strip() in DepartmentList or head_department.strip() in DepartmentList:
                if Found:
                    AssessmentsList.append(Assessment)
        elif Found:
            AssessmentsList.append(Assessment)
        

    # Serialize the assessments into basic dictionaries
    assessment_data = []
    for ass in AssessmentsList:
        org = OrganizationMaster.objects.filter(
            IsDelete=False, Activation_status=1, OrganizationID=ass.OrganizationID
        ).values_list('ShortDisplayLabel', flat=True).first()

        assessment_data.append({
            'id': ass.id,
            'Hotel':org,
            'CandidateName': f"{ass.Prefix or ''} {ass.Name or ''}".strip(),
            'Designation':ass.position,
            'hr_as':ass.hr_as,
            'hod_as':ass.hod_as,
            'rd_as':ass.rd_as,
            'gm_as':ass.gm_as,
            'ceo_as':ass.ceo_as,
            # 'CandidateName': ass.Name,
            'InterviewDate': ass.InterviewDate.strftime("%Y-%m-%d") if ass.InterviewDate else None,
            # 'Department': ass.Department,
            'Level': ass.Level,
            'LastApporvalStatus': ass.LastApporvalStatus,
            # 'LOIStatus': ass.LOIStatus,
            # 'ref': ass.ref,
            'OrganizationID':ass.OrganizationID,
            'ActionButtons':ActionButton,
            'Status': {
                "Approved_From": ass.Approval_stage_mobile_responce(),
                "Pending_From": ass.pending_status_mobile_responce(),
            },
        })

    return JsonResponse({
        'Assessments': assessment_data,
        'total_count': len(assessment_data),
    })



# @api_view(['GET'])
# def InterviewAssessment_Mobile_List_Api_Ceo_Pending_Count_Api(request):

#     Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
#     # AccessToken = request.query_params.get('Token')
#     # UserType_Session = request.query_params.get("UserType", '').lower()
#     # AccessToken = request.headers.get('Token')  # OR 'Authorization'
#     # UserType_Session = request.headers.get('UserType', '').lower()

#     UserType_Session = request.headers.get('UserType', '').lower()
#     AccessToken = request.headers.get('Authorization', '')

#     # print("Token from header:", AccessToken)
#     # print("Expected token   :", Fixed_Token)

#     if not AccessToken:
#         return HttpResponse('Token Not Found, Please Provide Correct Token.',content_type='text/plain')

#     if AccessToken != Fixed_Token:
#         return HttpResponse('Please Provide The Correct Token, Token Not Match.',content_type='text/plain')
#     # Validate UserType

#     if not UserType_Session:
#         return HttpResponse('UserType Not Found, Please Provide Correct UserType.', content_type='text/plain')
    

#     OrganizationID_Session = request.query_params.get('OrganizationID_Session')
#     OrganizationID = request.query_params.get('OrganizationID')
#     Level = request.query_params.get('Level', 'All')
#     Status = request.query_params.get('Status', 'All').lower()
#     LOIstatus = request.query_params.get('LOIstatus', 'All')
#     month_no = request.query_params.get('month_no')
#     year = request.query_params.get('year')
#     # UserType = str(request.session.get("UserType", '')).lower()
#     UserType = request.query_params.get("UserType", '').lower()
#     UserID = request.query_params.get("UserID")
#     EmployeeCode = request.query_params.get("EmployeeCode")

#     ActionButton = False
#     if UserType:
#         if UserType == "ceo":
#             ActionButton = True
#     else:
#         print("UserType is not CEO")


#     if OrganizationID_Session == "3" and (OrganizationID == '' or None):
#         OrganizationID = OrganizationID_Session

#     # year = request.query_params.get('year')
#     year = int(year) if year else datetime.now().year

#     # month_no = request.query_params.get('month_no')
#     month_no = int(month_no) if month_no and month_no != 'All' else None
#     month_name = "All Months" if not month_no else calendar.month_name[month_no]

#     today = datetime.today()
#     CYear = today.year
#     CMonth = today.month


#     DepartmentList = []
#     if EmployeeCode:
#         Departmentobj = MultipleDepartmentofEmployee(OrganizationID_Session, EmployeeCode)
#         if Departmentobj:
#             DepartmentList = Departmentobj
#         else:
#             return Response({'error': 'Employee Details not Found. Update in Human Resources.'}, status=status.HTTP_404_NOT_FOUND)
#     else:
#         return Response({'error': 'Employee Code is required.'}, status=status.HTTP_400_BAD_REQUEST)

#     Department = 'hr' if 'Human Resources' in DepartmentList else ''
#     # UserType = str(request.session.get("UserType", '')).lower()
#     if OrganizationID == '3' and UserType == 'hod':
#         UserType = 'rd'

#     I = OrganizationID
#     if OrganizationID == "3":
#         I = 'all'

#     assessments_filter = {'IsDelete': False, 'InterviewDate__year': year}
#     if month_no:
#         assessments_filter['InterviewDate__month'] = month_no
#     if I != 'all':
#         assessments_filter['OrganizationID'] = I
#     if Level != 'all':
#         assessments_filter['Level'] = Level
#     else:
#         assessments_filter['Level__in'] = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']

#     if Status != 'all':
#         assessments_filter['LastApporvalStatus'] = Status
#     else:
#         # assessments_filter['LastApporvalStatus__in'] = ['Approved', 'Pending']
#         assessments_filter['LastApporvalStatus__in'] = ['Pending']
#     if LOIstatus != 'all':
#         assessments_filter['LOIStatus'] = LOIstatus
    
#     # assessments_filter['Level__in'] = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']

#     Assessments = Assessment_Master.objects.filter(**assessments_filter).order_by('-CreatedDateTime')

#     AssessmentsList = []

#     for Assessment in Assessments:
#         ref = 'Fresher'
#         if Assessment.workexperience != 'Fresher':
#             ref = 0
#             if Assessment.reference:
#                 refobj = ReferenceDetails.objects.filter(
#                     IsDelete=False, OrganizationID=OrganizationID, Inteview_AssementID=Assessment.id
#                 ).first()
#                 if refobj and refobj.ref1_status == 1:
#                     ref = 1
#                 if isinstance(Assessment.reference, str):
#                     ref = 1
#         Assessment.ref = ref

#         AssessmentDepartment = Assessment.Department
#         head_department_obj = CheckHeadDepartment(AssessmentDepartment, Assessment.Level, OrganizationID)
#         head_department = head_department_obj.HeadDepartment if head_department_obj else ''

#         ApprovalStageFunobj = ApprovalStageFun(Assessment.Level, Assessment.Department, Assessment.OrganizationID)

#         Found = False
#         if UserID == '20230110136226':
#             Found = True
#         elif not ApprovalStageFunobj:
#             if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
#                 Found = True
#         else:
#             if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
#                 Found = True
#             elif UserType.lower() in [item.lower() for item in ApprovalStageFunobj]:
#                 Found = True

#         if UserType != "ceo":
#             if Found and (
#                 any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]) or UserID == '20230110136226'
#             ):
#                 AssessmentsList.append(Assessment)
#             elif AssessmentDepartment.strip() in DepartmentList or head_department.strip() in DepartmentList:
#                 if Found:
#                     AssessmentsList.append(Assessment)
#         elif Found:
#             AssessmentsList.append(Assessment)
        

#     # Serialize the assessments into basic dictionaries
#     assessment_data = []
#     for ass in AssessmentsList:
#         org = OrganizationMaster.objects.filter(
#             IsDelete=False, Activation_status=1, OrganizationID=ass.OrganizationID
#         ).values_list('ShortDisplayLabel', flat=True).first()

#         assessment_data.append({
#             'id': ass.id,
#             'Hotel':org,
#             'CandidateName': f"{ass.Prefix or ''} {ass.Name or ''}".strip(),
#             'Designation':ass.position,
#             'hr_as':ass.hr_as,
#             'hod_as':ass.hod_as,
#             'rd_as':ass.rd_as,
#             'gm_as':ass.gm_as,
#             'ceo_as':ass.ceo_as,
#             # 'CandidateName': ass.Name,
#             'InterviewDate': ass.InterviewDate.strftime("%Y-%m-%d") if ass.InterviewDate else None,
#             # 'Department': ass.Department,
#             'Level': ass.Level,
#             'LastApporvalStatus': ass.LastApporvalStatus,
#             # 'LOIStatus': ass.LOIStatus,
#             # 'ref': ass.ref,
#             'OrganizationID':ass.OrganizationID,
#             'ActionButtons':ActionButton,
#             'Status': {
#                 "Approved_From": ass.Approval_stage_mobile_responce(),
#                 "Pending_From": ass.pending_status_mobile_responce(),
#             },
#         })

#     return JsonResponse({
#         'Assessments': assessment_data,
#     })



@api_view(['GET'])
def InterviewAssessment_Mobile_List_Api_Total_Pending(request):
    OrganizationID_Session = request.query_params.get('OrganizationID_Session')
    OrganizationID = request.query_params.get('OrganizationID')
    Level = request.query_params.get('Level', 'All')
    Status = request.query_params.get('Status', 'All').lower()
    LOIstatus = request.query_params.get('LOIstatus', 'All')
    month_no = request.query_params.get('month_no')
    year = request.query_params.get('year')
    # UserType = str(request.session.get("UserType", '')).lower()
    UserType = request.query_params.get("UserType", '').lower()
    UserID = request.query_params.get("UserID")
    EmployeeCode = request.query_params.get("EmployeeCode")

    ActionButton = False
    if UserType:
        if UserType == "ceo":
            ActionButton = True
    else:
        print("UserType is not CEO")


    if OrganizationID_Session == "3" and (OrganizationID == '' or None):
        OrganizationID = OrganizationID_Session


    # year = request.query_params.get('year')
    year = int(year) if year else datetime.now().year

    # month_no = request.query_params.get('month_no')
    month_no = int(month_no) if month_no and month_no != 'All' else None
    month_name = "All Months" if not month_no else calendar.month_name[month_no]

    today = datetime.today()
    CYear = today.year
    CMonth = today.month


    DepartmentList = []
    if EmployeeCode:
        Departmentobj = MultipleDepartmentofEmployee(OrganizationID_Session, EmployeeCode)
        if Departmentobj:
            DepartmentList = Departmentobj
        else:
            return Response({'error': 'Employee Details not Found. Update in Human Resources.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Employee Code is required.'}, status=status.HTTP_400_BAD_REQUEST)

    Department = 'hr' if 'Human Resources' in DepartmentList else ''
    # UserType = str(request.session.get("UserType", '')).lower()
    if OrganizationID == '3' and UserType == 'hod':
        UserType = 'rd'

    I = OrganizationID
    if OrganizationID == "3":
        I = 'all'

    assessments_filter = {'IsDelete': False, 'InterviewDate__year': year}
    if month_no:
        assessments_filter['InterviewDate__month'] = month_no
    if I != 'all':
        assessments_filter['OrganizationID'] = I

    if Level != 'all':
        if Level == 'ceo':
            assessments_filter['Level__in'] = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']
        else:
            assessments_filter['Level'] = Level
    # elif Level == 'ceo':

    if Status != 'all':
        assessments_filter['LastApporvalStatus'] = Status
    else:
        # assessments_filter['LastApporvalStatus__in'] = ['Approved', 'Pending']
        assessments_filter['LastApporvalStatus__in'] = ['Pending']

    if LOIstatus != 'all':
        assessments_filter['LOIStatus'] = LOIstatus
    
    # assessments_filter['Level__in'] = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']

    Assessments = Assessment_Master.objects.filter(**assessments_filter).order_by('-CreatedDateTime')

    AssessmentsList = []

    for Assessment in Assessments:
        ref = 'Fresher'
        if Assessment.workexperience != 'Fresher':
            ref = 0
            if Assessment.reference:
                refobj = ReferenceDetails.objects.filter(
                    IsDelete=False, OrganizationID=OrganizationID, Inteview_AssementID=Assessment.id
                ).first()
                if refobj and refobj.ref1_status == 1:
                    ref = 1
                if isinstance(Assessment.reference, str):
                    ref = 1
        Assessment.ref = ref

        AssessmentDepartment = Assessment.Department
        head_department_obj = CheckHeadDepartment(AssessmentDepartment, Assessment.Level, OrganizationID)
        head_department = head_department_obj.HeadDepartment if head_department_obj else ''

        ApprovalStageFunobj = ApprovalStageFun(Assessment.Level, Assessment.Department, Assessment.OrganizationID)

        Found = False
        if UserID == '20230110136226':
            Found = True
        elif not ApprovalStageFunobj:
            if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
                Found = True
        else:
            if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
                Found = True
            elif UserType.lower() in [item.lower() for item in ApprovalStageFunobj]:
                Found = True

        if UserType != "ceo":
            if Found and (
                any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]) or UserID == '20230110136226'
            ):
                AssessmentsList.append(Assessment)
            elif AssessmentDepartment.strip() in DepartmentList or head_department.strip() in DepartmentList:
                if Found:
                    AssessmentsList.append(Assessment)
        elif Found:
            AssessmentsList.append(Assessment)
        

    # Serialize the assessments into basic dictionaries
    assessment_data = []
    for ass in AssessmentsList:
        org = OrganizationMaster.objects.filter(
            IsDelete=False, Activation_status=1, OrganizationID=ass.OrganizationID
        ).values_list('ShortDisplayLabel', flat=True).first()

        assessment_data.append({
            'id': ass.id,
            'Hotel':org,
            'CandidateName': f"{ass.Prefix or ''} {ass.Name or ''}".strip(),
            'Designation':ass.position,
            'hr_as':ass.hr_as,
            'hod_as':ass.hod_as,
            'rd_as':ass.rd_as,
            'gm_as':ass.gm_as,
            'ceo_as':ass.ceo_as,
            # 'CandidateName': ass.Name,
            'InterviewDate': ass.InterviewDate.strftime("%Y-%m-%d") if ass.InterviewDate else None,
            # 'Department': ass.Department,
            'Level': ass.Level,
            'LastApporvalStatus': ass.LastApporvalStatus,
            # 'LOIStatus': ass.LOIStatus,
            # 'ref': ass.ref,
            'OrganizationID':ass.OrganizationID,
            'ActionButtons':ActionButton,
            'Status': {
                "Approved_From": ass.Approval_stage_mobile_responce(),
                "Pending_From": ass.pending_status_mobile_responce(),
            },
        })

    return JsonResponse({
        'Assessments': assessment_data,
    })









# ----------------- demo count
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status

# @api_view(['GET'])
# def InterviewAssessment_Mobile_List_Api_Ceo_Pending_Count_Api(request):
#     # Fixed_Token = 'ujhj45ON8BKl!...'  # truncated for clarity
#     Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'

#     UserType_Session = request.headers.get('UserType', '').lower()
#     AccessToken = request.headers.get('Authorization', '')

#     if not AccessToken:
#         return HttpResponse('Token Not Found, Please Provide Correct Token.', content_type='text/plain')
#     if AccessToken != Fixed_Token:
#         return HttpResponse('Please Provide The Correct Token, Token Not Match.', content_type='text/plain')
#     if not UserType_Session:
#         return HttpResponse('UserType Not Found, Please Provide Correct UserType.', content_type='text/plain')

#     OrganizationID_Session = request.query_params.get('OrganizationID_Session')
#     OrganizationID = request.query_params.get('OrganizationID')
#     # Level = request.query_params.get('Level', 'All')
#     # Status = request.query_params.get('Status', 'All').lower()
#     # LOIstatus = request.query_params.get('LOIstatus', 'All')
#     month_no = request.query_params.get('month_no')
#     year = request.query_params.get('year')
#     UserID = request.query_params.get("UserID")
#     EmployeeCode = request.query_params.get("EmployeeCode")

#     if OrganizationID_Session == "3" and (not OrganizationID or OrganizationID == ''):
#         OrganizationID = OrganizationID_Session

#     year = int(year) if year else datetime.now().year
#     month_no = int(month_no) if month_no and month_no != 'All' else None

#     today = datetime.today().date()
#     yesterday = today - timedelta(days=1)

#     DepartmentList = []
#     if EmployeeCode:
#         Departmentobj = MultipleDepartmentofEmployee(OrganizationID_Session, EmployeeCode)
#         if Departmentobj:
#             DepartmentList = Departmentobj
#         else:
#             return JsonResponse({'error': 'Employee Details not Found. Update in Human Resources.'}, status=404)
#     else:
#         return JsonResponse({'error': 'Employee Code is required.'}, status=400)

#     if OrganizationID == '3' and UserType_Session == 'hod':
#         UserType_Session = 'rd'

#     I = OrganizationID
#     if OrganizationID == "3":
#         I = 'all'

#     # --- Apply base filters ---
#     assessments_filter = {'IsDelete': False, 'InterviewDate__year': year}
#     # if month_no:
#     #     assessments_filter['InterviewDate__month'] = month_no
#     # if I != 'all':
#     #     assessments_filter['OrganizationID'] = I
#     # if Level != 'all':
#     #     assessments_filter['Level'] = Level
#     # else:
#     #     assessments_filter['Level__in'] = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']
#     # if Status != 'all':
#     #     assessments_filter['LastApporvalStatus'] = Status
#     # else:
#     #     assessments_filter['LastApporvalStatus__in'] = ['Pending']
#     # if LOIstatus != 'all':
#     #     assessments_filter['LOIStatus'] = LOIstatus

#     assessments_filter['Level__in'] = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']


#     Assessments = Assessment_Master.objects.filter(**assessments_filter)

#     # Count based on date
#     total_count = 0
#     today_count = 0
#     yesterday_count = 0

#     for Assessment in Assessments:
#         AssessmentDepartment = Assessment.Department
#         head_department_obj = CheckHeadDepartment(AssessmentDepartment, Assessment.Level, OrganizationID)
#         head_department = head_department_obj.HeadDepartment if head_department_obj else ''
#         ApprovalStageFunobj = ApprovalStageFun(Assessment.Level, Assessment.Department, Assessment.OrganizationID)

#         Found = False
#         if UserID == '20230110136226':
#             Found = True
#         elif not ApprovalStageFunobj:
#             if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
#                 Found = True
#         else:
#             if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
#                 Found = True
#             elif UserType_Session.lower() in [item.lower() for item in ApprovalStageFunobj]:
#                 Found = True

#         include = False
#         if UserType_Session != "ceo":
#             if Found and (
#                 any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]) or UserID == '20230110136226'
#             ):
#                 include = True
#             elif AssessmentDepartment.strip() in DepartmentList or head_department.strip() in DepartmentList:
#                 if Found:
#                     include = True
#         elif Found:
#             include = True

#         if include:
#             total_count += 1
#             interview_date = Assessment.InterviewDate
#             if interview_date:
#                 if interview_date == today:
#                     today_count += 1
#                 elif interview_date == yesterday:
#                     yesterday_count += 1

#     Today_Yesterday_Count = 0
#     if today_count and yesterday_count:
#         Today_Yesterday_Count = yesterday_count+today_count

#     return JsonResponse({
#         'total_count': total_count,
#         'today_count': today_count,
#         'yesterday_count': yesterday_count,
#         'today_yesterday_count': Today_Yesterday_Count,
#     })





# @api_view(['GET'])
# def InterviewAssessment_Mobile_List_Api_Ceo_Pending_Count_Api(request):

#     Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
#     # AccessToken = request.query_params.get('Token')
#     # UserType_Session = request.query_params.get("UserType", '').lower()
#     # AccessToken = request.headers.get('Token')  # OR 'Authorization'
#     # UserType_Session = request.headers.get('UserType', '').lower()

#     UserType_Session = request.headers.get('UserType', '').lower()
#     AccessToken = request.headers.get('Authorization', '')

#     # print("Token from header:", AccessToken)
#     # print("Expected token   :", Fixed_Token)

#     if not AccessToken:
#         return HttpResponse('Token Not Found, Please Provide Correct Token.',content_type='text/plain')

#     if AccessToken != Fixed_Token:
#         return HttpResponse('Please Provide The Correct Token, Token Not Match.',content_type='text/plain')
#     # Validate UserType

#     if not UserType_Session:
#         return HttpResponse('UserType Not Found, Please Provide Correct UserType.', content_type='text/plain')
    

#     OrganizationID_Session = request.query_params.get('OrganizationID_Session')
#     OrganizationID = request.query_params.get('OrganizationID')
#     Level = request.query_params.get('Level', 'All')
#     Status = request.query_params.get('Status', 'All').lower()
#     LOIstatus = request.query_params.get('LOIstatus', 'All')
#     month_no = request.query_params.get('month_no')
#     year = request.query_params.get('year')
#     # UserType = str(request.session.get("UserType", '')).lower()
#     UserType = request.query_params.get("UserType", '').lower()
#     UserID = request.query_params.get("UserID")
#     EmployeeCode = request.query_params.get("EmployeeCode")

#     ActionButton = False
#     if UserType:
#         if UserType == "ceo":
#             ActionButton = True
#     else:
#         print("UserType is not CEO")


#     if OrganizationID_Session == "3" and (OrganizationID == '' or None):
#         OrganizationID = OrganizationID_Session

#     # year = request.query_params.get('year')
#     year = int(year) if year else datetime.now().year

#     # month_no = request.query_params.get('month_no')
#     month_no = int(month_no) if month_no and month_no != 'All' else None
#     month_name = "All Months" if not month_no else calendar.month_name[month_no]

#     today = datetime.today()
#     CYear = today.year
#     CMonth = today.month


#     DepartmentList = []
#     if EmployeeCode:
#         Departmentobj = MultipleDepartmentofEmployee(OrganizationID_Session, EmployeeCode)
#         if Departmentobj:
#             DepartmentList = Departmentobj
#         else:
#             return Response({'error': 'Employee Details not Found. Update in Human Resources.'}, status=status.HTTP_404_NOT_FOUND)
#     else:
#         return Response({'error': 'Employee Code is required.'}, status=status.HTTP_400_BAD_REQUEST)

#     Department = 'hr' if 'Human Resources' in DepartmentList else ''
#     # UserType = str(request.session.get("UserType", '')).lower()
#     if OrganizationID == '3' and UserType == 'hod':
#         UserType = 'rd'

#     I = OrganizationID
#     if OrganizationID == "3":
#         I = 'all'

#     assessments_filter = {'IsDelete': False, 'InterviewDate__year': year}
#     if month_no:
#         assessments_filter['InterviewDate__month'] = month_no
#     if I != 'all':
#         assessments_filter['OrganizationID'] = I
#     if Level != 'all':
#         assessments_filter['Level'] = Level
#     else:
#         assessments_filter['Level__in'] = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']

#     if Status != 'all':
#         assessments_filter['LastApporvalStatus'] = Status
#     else:
#         # assessments_filter['LastApporvalStatus__in'] = ['Approved', 'Pending']
#         assessments_filter['LastApporvalStatus__in'] = ['Pending']
#     if LOIstatus != 'all':
#         assessments_filter['LOIStatus'] = LOIstatus
    
#     # assessments_filter['Level__in'] = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']

#     Assessments = Assessment_Master.objects.filter(**assessments_filter).order_by('-CreatedDateTime')

#     AssessmentsList = []

#     for Assessment in Assessments:
#         ref = 'Fresher'
#         if Assessment.workexperience != 'Fresher':
#             ref = 0
#             if Assessment.reference:
#                 refobj = ReferenceDetails.objects.filter(
#                     IsDelete=False, OrganizationID=OrganizationID, Inteview_AssementID=Assessment.id
#                 ).first()
#                 if refobj and refobj.ref1_status == 1:
#                     ref = 1
#                 if isinstance(Assessment.reference, str):
#                     ref = 1
#         Assessment.ref = ref

#         AssessmentDepartment = Assessment.Department
#         head_department_obj = CheckHeadDepartment(AssessmentDepartment, Assessment.Level, OrganizationID)
#         head_department = head_department_obj.HeadDepartment if head_department_obj else ''

#         ApprovalStageFunobj = ApprovalStageFun(Assessment.Level, Assessment.Department, Assessment.OrganizationID)

#         Found = False
#         if UserID == '20230110136226':
#             Found = True
#         elif not ApprovalStageFunobj:
#             if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
#                 Found = True
#         else:
#             if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
#                 Found = True
#             elif UserType.lower() in [item.lower() for item in ApprovalStageFunobj]:
#                 Found = True

#         if UserType != "ceo":
#             if Found and (
#                 any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]) or UserID == '20230110136226'
#             ):
#                 AssessmentsList.append(Assessment)
#             elif AssessmentDepartment.strip() in DepartmentList or head_department.strip() in DepartmentList:
#                 if Found:
#                     AssessmentsList.append(Assessment)
#         elif Found:
#             AssessmentsList.append(Assessment)
        

#     # Serialize the assessments into basic dictionaries
#     assessment_data = []
#     for ass in AssessmentsList:
#         org = OrganizationMaster.objects.filter(
#             IsDelete=False, Activation_status=1, OrganizationID=ass.OrganizationID
#         ).values_list('ShortDisplayLabel', flat=True).first()

#         assessment_data.append({
#             'id': ass.id,
#             'Hotel':org,
#             'CandidateName': f"{ass.Prefix or ''} {ass.Name or ''}".strip(),
#             'Designation':ass.position,
#             'hr_as':ass.hr_as,
#             'hod_as':ass.hod_as,
#             'rd_as':ass.rd_as,
#             'gm_as':ass.gm_as,
#             'ceo_as':ass.ceo_as,
#             # 'CandidateName': ass.Name,
#             'InterviewDate': ass.InterviewDate.strftime("%Y-%m-%d") if ass.InterviewDate else None,
#             # 'Department': ass.Department,
#             'Level': ass.Level,
#             'LastApporvalStatus': ass.LastApporvalStatus,
#             # 'LOIStatus': ass.LOIStatus,
#             # 'ref': ass.ref,
#             'OrganizationID':ass.OrganizationID,
#             'ActionButtons':ActionButton,
#             'Status': {
#                 "Approved_From": ass.Approval_stage_mobile_responce(),
#                 "Pending_From": ass.pending_status_mobile_responce(),
#             },
#         })

#     return JsonResponse({
#         'Assessments': assessment_data,
#         'total_count': len(assessment_data),
#     })



@api_view(['GET'])
def InterviewAssessment_Mobile_List_Api_Ceo_Pending_Count_Api(request):

    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    # AccessToken = request.query_params.get('Token')
    # UserType_Session = request.query_params.get("UserType", '').lower()
    # AccessToken = request.headers.get('Token')  # OR 'Authorization'
    # UserType_Session = request.headers.get('UserType', '').lower()

    UserType = request.headers.get('UserType', '').lower()
    AccessToken = request.headers.get('Authorization', '')

    # print("Token from header:", AccessToken)
    # print("Expected token   :", Fixed_Token)

    if not AccessToken:
        return HttpResponse('Token Not Found, Please Provide Correct Token.',content_type='text/plain')

    if AccessToken != Fixed_Token:
        return HttpResponse('Please Provide The Correct Token, Token Not Match.',content_type='text/plain')
    # Validate UserType

    if not UserType:
        return HttpResponse('UserType Not Found, Please Provide Correct UserType.', content_type='text/plain')
    

    OrganizationID_Session = request.query_params.get('OrganizationID_Session')
    OrganizationID = request.query_params.get('OrganizationID')
    Level = request.query_params.get('Level', 'All')
    Status = request.query_params.get('Status', 'All').lower()
    LOIstatus = request.query_params.get('LOIstatus', 'All')
    month_no = request.query_params.get('month_no')
    year = request.query_params.get('year')
    # UserType = str(request.session.get("UserType", '')).lower()
    # UserType = request.query_params.get("UserType", '').lower()
    UserID = request.query_params.get("UserID")
    EmployeeCode = request.query_params.get("EmployeeCode")

    ActionButton = False
    if UserType:
        if UserType == "ceo":
            ActionButton = True
    else:
        print("UserType is not CEO")


    if OrganizationID_Session == "3" and (OrganizationID == '' or None):
        OrganizationID = OrganizationID_Session

    # year = request.query_params.get('year')
    year = int(year) if year else datetime.now().year

    # month_no = request.query_params.get('month_no')
    month_no = int(month_no) if month_no and month_no != 'All' else None
    month_name = "All Months" if not month_no else calendar.month_name[month_no]

    today = datetime.today()
    # CYear = today.year
    # CMonth = today.month

    today = datetime.today().date()
    yesterday = today - timedelta(days=1)
    today_yesterday_count = 0


    DepartmentList = []
    if EmployeeCode:
        Departmentobj = MultipleDepartmentofEmployee(OrganizationID_Session, EmployeeCode)
        if Departmentobj:
            DepartmentList = Departmentobj
        else:
            return Response({'error': 'Employee Details not Found. Update in Human Resources.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Employee Code is required.'}, status=status.HTTP_400_BAD_REQUEST)

    Department = 'hr' if 'Human Resources' in DepartmentList else ''
    # UserType = str(request.session.get("UserType", '')).lower()
    if OrganizationID == '3' and UserType == 'hod':
        UserType = 'rd'

    I = OrganizationID
    if OrganizationID == "3":
        I = 'all'

    assessments_filter = {'IsDelete': False, 'InterviewDate__year': year}
    if month_no:
        assessments_filter['InterviewDate__month'] = month_no
    if I != 'all':
        assessments_filter['OrganizationID'] = I

    if Level != 'all':
        assessments_filter['Level'] = Level
    else:
        assessments_filter['Level__in'] = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']

    if Status != 'all':
        assessments_filter['LastApporvalStatus'] = Status
    else:
        # assessments_filter['LastApporvalStatus__in'] = ['Approved', 'Pending']
        assessments_filter['LastApporvalStatus__in'] = ['Pending']
    if LOIstatus != 'all':
        assessments_filter['LOIStatus'] = LOIstatus
    
    # assessments_filter['Level__in'] = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']

    Assessments = Assessment_Master.objects.filter(**assessments_filter).order_by('-CreatedDateTime')

    AssessmentsList = []

    for Assessment in Assessments:
        ref = 'Fresher'
        if Assessment.workexperience != 'Fresher':
            ref = 0
            if Assessment.reference:
                refobj = ReferenceDetails.objects.filter(
                    IsDelete=False, OrganizationID=OrganizationID, Inteview_AssementID=Assessment.id
                ).first()
                if refobj and refobj.ref1_status == 1:
                    ref = 1
                if isinstance(Assessment.reference, str):
                    ref = 1
        Assessment.ref = ref

        AssessmentDepartment = Assessment.Department
        head_department_obj = CheckHeadDepartment(AssessmentDepartment, Assessment.Level, OrganizationID)
        head_department = head_department_obj.HeadDepartment if head_department_obj else ''

        ApprovalStageFunobj = ApprovalStageFun(Assessment.Level, Assessment.Department, Assessment.OrganizationID)

        Found = False
        if UserID == '20230110136226':
            Found = True
        elif not ApprovalStageFunobj:
            if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
                Found = True
        else:
            if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
                Found = True
            elif UserType.lower() in [item.lower() for item in ApprovalStageFunobj]:
                Found = True

        if UserType != "ceo":
            if Found and (
                any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]) or UserID == '20230110136226'
            ):
                AssessmentsList.append(Assessment)
            elif AssessmentDepartment.strip() in DepartmentList or head_department.strip() in DepartmentList:
                if Found:
                    AssessmentsList.append(Assessment)
        elif Found:
            AssessmentsList.append(Assessment)
        
        if Assessment.InterviewDate and Assessment.CreatedDateTime.date() in [today, yesterday]:
            today_yesterday_count += 1

    # Serialize the assessments into basic dictionaries
    assessment_data = []
    for ass in AssessmentsList:
        org = OrganizationMaster.objects.filter(
            IsDelete=False, Activation_status=1, OrganizationID=ass.OrganizationID
        ).values_list('ShortDisplayLabel', flat=True).first()

        assessment_data.append({
            'id': ass.id,
            'Hotel':org,
            'CandidateName': f"{ass.Prefix or ''} {ass.Name or ''}".strip(),
            'Designation':ass.position,
            'hr_as':ass.hr_as,
            'hod_as':ass.hod_as,
            'rd_as':ass.rd_as,
            'gm_as':ass.gm_as,
            'ceo_as':ass.ceo_as,
            # 'CandidateName': ass.Name,
            'InterviewDate': ass.InterviewDate.strftime("%Y-%m-%d") if ass.InterviewDate else None,
            # 'Department': ass.Department,
            'Level': ass.Level,
            'LastApporvalStatus': ass.LastApporvalStatus,
            # 'LOIStatus': ass.LOIStatus,
            # 'ref': ass.ref,
            'OrganizationID':ass.OrganizationID,
            'ActionButtons':ActionButton,
            # 'Status': {
            #     "Approved_From": ass.Approval_stage_mobile_responce(),
            #     "Pending_From": ass.pending_status_mobile_responce(),
            # },
        })

    return JsonResponse({
        # 'Assessments': assessment_data,
        'total_count': len(assessment_data),
        'today_yesterday_count': today_yesterday_count

    })





@api_view(['GET'])
def InterviewAssessment_Mobile_List_Api_Total_Pending_count(request):
    OrganizationID_Session = request.query_params.get('OrganizationID_Session')
    OrganizationID = request.query_params.get('OrganizationID')
    Level = request.query_params.get('Level', 'All')
    Status = request.query_params.get('Status', 'All').lower()
    LOIstatus = request.query_params.get('LOIstatus', 'All')
    month_no = request.query_params.get('month_no')
    year = request.query_params.get('year')
    # UserType = str(request.session.get("UserType", '')).lower()
    UserType = request.query_params.get("UserType", '').lower()
    UserID = request.query_params.get("UserID")
    EmployeeCode = request.query_params.get("EmployeeCode")

    ActionButton = False
    if UserType:
        if UserType == "ceo":
            ActionButton = True
    else:
        print("UserType is not CEO")


    if OrganizationID_Session == "3" and (OrganizationID == '' or None):
        OrganizationID = OrganizationID_Session


    # year = request.query_params.get('year')
    year = int(year) if year else datetime.now().year

    # month_no = request.query_params.get('month_no')
    month_no = int(month_no) if month_no and month_no != 'All' else None
    month_name = "All Months" if not month_no else calendar.month_name[month_no]

    today = datetime.today()
    # CYear = today.year
    # CMonth = today.month

    today = datetime.today().date()
    yesterday = today - timedelta(days=1)
    today_yesterday_count = 0




    DepartmentList = []
    if EmployeeCode:
        Departmentobj = MultipleDepartmentofEmployee(OrganizationID_Session, EmployeeCode)
        if Departmentobj:
            DepartmentList = Departmentobj
        else:
            return Response({'error': 'Employee Details not Found. Update in Human Resources.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Employee Code is required.'}, status=status.HTTP_400_BAD_REQUEST)

    Department = 'hr' if 'Human Resources' in DepartmentList else ''
    # UserType = str(request.session.get("UserType", '')).lower()
    if OrganizationID == '3' and UserType == 'hod':
        UserType = 'rd'

    I = OrganizationID
    if OrganizationID == "3":
        I = 'all'

    assessments_filter = {'IsDelete': False, 'InterviewDate__year': year}
    if month_no:
        assessments_filter['InterviewDate__month'] = month_no
    if I != 'all':
        assessments_filter['OrganizationID'] = I

    if Level != 'all':
        if Level == 'ceo':
            assessments_filter['Level__in'] = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']
        else:
            assessments_filter['Level'] = Level
    # elif Level == 'ceo':

    if Status != 'all':
        assessments_filter['LastApporvalStatus'] = Status
    else:
        # assessments_filter['LastApporvalStatus__in'] = ['Approved', 'Pending']
        assessments_filter['LastApporvalStatus__in'] = ['Pending']

    if LOIstatus != 'all':
        assessments_filter['LOIStatus'] = LOIstatus
    
    # assessments_filter['Level__in'] = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']

    Assessments = Assessment_Master.objects.filter(**assessments_filter).order_by('-CreatedDateTime')

    AssessmentsList = []

    for Assessment in Assessments:
        ref = 'Fresher'
        if Assessment.workexperience != 'Fresher':
            ref = 0
            if Assessment.reference:
                refobj = ReferenceDetails.objects.filter(
                    IsDelete=False, OrganizationID=OrganizationID, Inteview_AssementID=Assessment.id
                ).first()
                if refobj and refobj.ref1_status == 1:
                    ref = 1
                if isinstance(Assessment.reference, str):
                    ref = 1
        Assessment.ref = ref

        AssessmentDepartment = Assessment.Department
        head_department_obj = CheckHeadDepartment(AssessmentDepartment, Assessment.Level, OrganizationID)
        head_department = head_department_obj.HeadDepartment if head_department_obj else ''

        ApprovalStageFunobj = ApprovalStageFun(Assessment.Level, Assessment.Department, Assessment.OrganizationID)

        Found = False
        if UserID == '20230110136226':
            Found = True
        elif not ApprovalStageFunobj:
            if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
                Found = True
        else:
            if any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]):
                Found = True
            elif UserType.lower() in [item.lower() for item in ApprovalStageFunobj]:
                Found = True

        if UserType != "ceo":
            if Found and (
                any(dept in DepartmentList for dept in ['Human Resources', "Executive Office", "Talent Acquisition and Development", "Corporate Office"]) or UserID == '20230110136226'
            ):
                AssessmentsList.append(Assessment)
            elif AssessmentDepartment.strip() in DepartmentList or head_department.strip() in DepartmentList:
                if Found:
                    AssessmentsList.append(Assessment)
        elif Found:
            AssessmentsList.append(Assessment)
        
        if Assessment.InterviewDate and Assessment.CreatedDateTime.date() in [today, yesterday]:
            today_yesterday_count += 1

    # Serialize the assessments into basic dictionaries
    assessment_data = []
    for ass in AssessmentsList:
        org = OrganizationMaster.objects.filter(
            IsDelete=False, Activation_status=1, OrganizationID=ass.OrganizationID
        ).values_list('ShortDisplayLabel', flat=True).first()

        assessment_data.append({
            'id': ass.id,
            'Hotel':org,
            'CandidateName': f"{ass.Prefix or ''} {ass.Name or ''}".strip(),
            'Designation':ass.position,
            'hr_as':ass.hr_as,
            'hod_as':ass.hod_as,
            'rd_as':ass.rd_as,
            'gm_as':ass.gm_as,
            'ceo_as':ass.ceo_as,
            # 'CandidateName': ass.Name,
            'InterviewDate': ass.InterviewDate.strftime("%Y-%m-%d") if ass.InterviewDate else None,
            # 'Department': ass.Department,
            'Level': ass.Level,
            'LastApporvalStatus': ass.LastApporvalStatus,
            # 'LOIStatus': ass.LOIStatus,
            # 'ref': ass.ref,
            'OrganizationID':ass.OrganizationID,
            'ActionButtons':ActionButton,
            'Status': {
                "Approved_From": ass.Approval_stage_mobile_responce(),
                "Pending_From": ass.pending_status_mobile_responce(),
            },
        })

    return JsonResponse({
        'total_count': len(assessment_data),
        'today_yesterday_count': today_yesterday_count
    })

