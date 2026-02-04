
from Manning_Guide.models import OnRollDepartmentMaster,OnRollDesignationMaster, OnRollDivisionMaster
from HumanResources.models import EmployeeWorkDetails, Salary_Detail_Master, EmployeeBankInformationDetails, EmployeePersonalDetails, EmployeeQualificationDetails, EmployeeDocumentsInformationDetails
from .models import *
from Leave_Management_System.models import  Leave_Type_Master
from django.http import JsonResponse
from django.contrib import messages
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from django.db import connection
from app.views import EmployeeDataSelect
from Manning_Guide.models import LavelAdd
from datetime import date
from InterviewAssessment.models import Assessment_Master

from django.http import JsonResponse
from django.forms.models import model_to_dict

# def Get_Emp_Personal_Data_Mobile_Api(request):
#     """
#     Returns employee information from EmployeeMaster
#     and fills Salary from Salary_Detail_Master if missing or zero.
#     """
#     # Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
#     # AccessToken = request.headers.get('Authorization', '')

#     OID = request.GET.get('OID')
#     Code = request.GET.get('Code')
    
#     EmpData = EmployeePersonalDetails.objects.filter(          
#         EmployeeCode=Code,
#         OrganizationID=OID,
#         IsDelete=False,
#         IsEmployeeCreated=True
#     ).only('EmpID','ProfileCompletion').first()



#     # Token checks
#     # if not AccessToken:
#     #     return JsonResponse({'error': 'Token not found'}, status=400)
#     # if AccessToken != Fixed_Token:
#     #     return JsonResponse({'error': 'Invalid token'}, status=400)

#     # OID checks
#     if not OID:
#         return JsonResponse({'error': 'OID is required'}, status=400)
#     if OID != '333333' and not OrganizationMaster.objects.filter(OrganizationID=OID).exists():
#         return JsonResponse({'error': 'Invalid OrganizationID'}, status=400)

#     employee = EmployeeMaster.objects.filter(
#         EmployeeCode=Code,
#         OrganizationID=OID,
#         IsDelete=False
#     ).first()

#     if not employee:
#         return JsonResponse({'error': 'Employee not found'}, status=404)
#     # Fields to exclude
#     exclude_fields = [
#         'OrganizationID',
#         'CreatedBy',
#         'CreatedDateTime',
#         'ModifyBy',
#         'ModifyDateTime',
#         'IsDelete',
#         'IsSecondary',
#     ]

#     # Convert model to dict and exclude unwanted fields
#     emp_data = model_to_dict(employee, exclude=exclude_fields)
#     # Convert model to dictionary
#     # emp_data = model_to_dict(employee)

#     return JsonResponse(emp_data, safe=False)


# from django.http import JsonResponse
# from django.forms.models import model_to_dict

def Get_Emp_Personal_Data_Mobile_Api(request):
    
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    OID = request.GET.get('OID')
    Code = request.GET.get('Code')

    # Token checks
    if not AccessToken:
        return JsonResponse({'error': 'Token not found'}, status=400)
    if AccessToken != Fixed_Token:
        return JsonResponse({'error': 'Invalid token'}, status=400)

    if not OID:
        return JsonResponse({'error': 'OID is required'}, status=400)

    if OID != '333333' and not OrganizationMaster.objects.filter(OrganizationID=OID).exists():
        return JsonResponse({'error': 'Invalid OrganizationID'}, status=400)

    EmpData = EmployeePersonalDetails.objects.filter(
        EmployeeCode=Code,
        OrganizationID=OID,
        IsDelete=False,
        IsEmployeeCreated=True
    ).values('ProfileCompletion').first()

    employee = EmployeeMaster.objects.filter(
        EmployeeCode=Code,
        OrganizationID=OID,
        IsDelete=False
    ).first()

    if not employee:
        return JsonResponse({'error': 'Employee not found'}, status=404)

    exclude_fields = [
        'OrganizationID',
        'CreatedBy',
        'CreatedDateTime',
        'ModifyBy',
        'ModifyDateTime',
        'IsDelete',
        'IsSecondary',
    ]

    emp_data = model_to_dict(employee, exclude=exclude_fields)

    contact = emp_data.get("EmergencyContact")
    if contact:
        emp_data["EmergencyContact"] = "******" + contact[-4:]

    profile_completion = EmpData.get('ProfileCompletion') if EmpData else None

    final_response = {
        "EmployeeInfo": emp_data,
        "ProfileCompletion": profile_completion,
    }

    return JsonResponse(final_response, safe=False)


from .Global_Api import Get_Employee_ID_Data_By_Code

def Get_Emp_Bank_Info_Mobile_Api(request):
    """
    Returns employee information from EmployeeMaster
    and fills Salary from Salary_Detail_Master if missing or zero.
    """
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    OID = request.GET.get('OID')
    Code = request.GET.get('Code')

    # Token checks
    if not AccessToken:
        return JsonResponse({'error': 'Token not found'}, status=400)
    if AccessToken != Fixed_Token:
        return JsonResponse({'error': 'Invalid token'}, status=400)

    # OID checks
    if not OID:
        return JsonResponse({'error': 'OID is required'}, status=400)
    if OID != '333333' and not OrganizationMaster.objects.filter(OrganizationID=OID).exists():
        return JsonResponse({'error': 'Invalid OrganizationID'}, status=400)
    
    Data = Get_Employee_ID_Data_By_Code(Code, OID)
    
    if Data:
        employee = EmployeeBankInformationDetails.objects.filter(
            EmpID=Data,
            OrganizationID=OID,
            IsDelete=False
        ).first()

        if not employee:
            return JsonResponse({'error': 'Employee not found'}, status=404)
        # Fields to exclude
        exclude_fields = [
            'OrganizationID',
            'CreatedBy',
            'CreatedDateTime',
            'ModifyBy',
            'ModifyDateTime',
            'IsDelete',
            'id',
        ]

        # Convert model to dict and exclude unwanted fields
        emp_data = model_to_dict(employee, exclude=exclude_fields)
        
        BankAccountNumber = emp_data.get("BankAccountNumber")
        if BankAccountNumber:
            emp_data["BankAccountNumber"] = "******" + BankAccountNumber[-4:]
        
        IFSCCode = emp_data.get("IFSCCode")
        if IFSCCode:
            emp_data["IFSCCode"] = "******" + IFSCCode[-4:]

        return JsonResponse(emp_data, safe=False)



from HumanResources.azure import download_blob
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, Http404
import mimetypes

@api_view(['GET'])
def get_employee_profile_photo(request, Code,OID):
    # ====== TOKEN CHECKS ======
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    if not AccessToken:
        return Response(
            {"error": "Token not found"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if AccessToken != Fixed_Token:
        return Response(
            {"error": "Invalid token"},
            status=status.HTTP_400_BAD_REQUEST
        )
    # ====== END TOKEN CHECK ======

    Data = Get_Employee_ID_Data_By_Code(Code, OID)
    
    if not Data:
        return Response(
            {"detail": "Employee code is invalid"},
            status=status.HTTP_400_BAD_REQUEST
        )

    employee = EmployeePersonalDetails.objects.filter(EmpID=Data).first()
    if not employee:
        return Response(
            {"detail": "Employee not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    file_id = employee.ProfileImageFileName
    file_name = employee.ProfileImageFileTitle

    if not file_id:
        return Response(
            {"detail": "Profile image not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    file_type, _ = mimetypes.guess_type(file_id)
    if file_type is None:
        file_type = 'application/octet-stream'
    
    try:
        blob_content = download_blob(file_id)
    except Exception as e:
        return Response(
            {"detail": "Error downloading file", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    if not blob_content:
        return Response(
            {"detail": "File content not found"},
            status=status.HTTP_404_NOT_FOUND
        )


    response = HttpResponse(blob_content.readall(), content_type=file_type)
    response['Content-Disposition'] = f'inline; filename=\"{file_name}\"'
    return response



@api_view(['GET'])
def get_employee_Documents(request, Code, OID):

    # ====== TOKEN CHECKS ======
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    if not AccessToken:
        return Response({"error": "Token not found"}, status=400)

    if AccessToken != Fixed_Token:
        return Response({"error": "Invalid token"}, status=400)
    # ======================================


    # Get Employee ID
    EmpID = Get_Employee_ID_Data_By_Code(Code, OID)

    if not EmpID:
        return Response({"detail": "Employee code is invalid"}, status=400)


    qualification_docs = list(
        EmployeeQualificationDetails.objects.filter(EmpID=EmpID)
        .values('id','EmpID','EducationType','Degree_Course')
    )

    document_info_docs = list(
        EmployeeDocumentsInformationDetails.objects.filter(EmpID=EmpID)
        .values('id','EmpID','Title')
    )

    if not qualification_docs and not document_info_docs:
        return Response(
            {"detail": "No documents found for this employee"},
            status=404
        )

    return Response({
        "QualificationDocuments": qualification_docs,
        "EmployeeDocuments": document_info_docs,
    })


@api_view(['GET'])
def view_employee_document(request, document_id, DocType):

    # ====== TOKEN CHECKS ======
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    if not AccessToken:
        return Response({"error": "Token not found"}, status=400)

    if AccessToken != Fixed_Token:
        return Response({"error": "Invalid token"}, status=400)
    # ======================================

    DocType = DocType.lower()

    if DocType == 'qualification':
        doc = EmployeeQualificationDetails.objects.filter(id=document_id, IsDelete=False).first()

    elif DocType == 'other':
        doc = EmployeeDocumentsInformationDetails.objects.filter(id=document_id, IsDelete=False).first()

    else:
        return Response(
            {"detail": "Invalid DocType. Use 'qualification' or 'other'."},
            status=400
        )

    if not doc:
        return Response({"detail": "Document not found"}, status=404)

    file_id = doc.FileName
    file_title = doc.FileTitle or "document"

    if not file_id:
        return Response({"detail": "File not found"}, status=404)

    file_type, _ = mimetypes.guess_type(file_id)
    if file_type is None:
        file_type = 'application/octet-stream'

    try:
        blob = download_blob(file_id)
    except Exception as e:
        return Response(
            {"detail": "Error downloading file", "error": str(e)},
            status=500
        )

    if not blob:
        return Response({"detail": "File content not found"}, status=404)

    response = HttpResponse(blob.readall(), content_type=file_type)
    response['Content-Disposition'] = f'inline; filename="{file_title}"'
    return response


