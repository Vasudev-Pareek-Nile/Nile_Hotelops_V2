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


from LETTEROFAPPOINTMENT.models import LOALETTEROFAPPOINTMENTEmployeeDetail
from UniformInventory.models import UniformInformation
from django.db.models import Subquery, OuterRef
from IT.models import ItInformation
from app.Global_Api import get_organization_list

def Issue_view(request):
    OrganizationID = request.session["OrganizationID"] 
    OID  = request.GET.get('OID')
    memOrg = get_organization_list(OrganizationID)  
    
    if not OID:
        OID = OrganizationID
        
    # print("OID is here::", OID)

        
    query = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(IsDelete=False)

    if OID != "all":
        query = query.filter(OrganizationID=OID)

    AppoiLetters = query.values(
        'id',
        'first_name',
        'last_name',
        'department',
        'designation',
        'Reporting_to_designation', 
        'emp_code', 
        'HR',
        'HK',
        'IT',
        'DEPT',
        'OrganizationID',
        'HKCreatedBy',
        'ITCreatedBy',
        'DEPTCreatedBy'
    ).order_by('-CreatedDateTime')

    
    UN_subquery = UniformInformation.objects.filter(
        EmployeeCode=OuterRef("emp_code"),
        OrganizationID=OuterRef("OrganizationID")
    ).values("id")[:1]
    
    IT_subquery = ItInformation.objects.filter(
        EmployeeCode=OuterRef("emp_code"),
        OrganizationID=OuterRef("OrganizationID")
    ).values("id")[:1]
    
    HR_subquery = HR_Inventory_Information.objects.filter(
        EmployeeCode=OuterRef("emp_code"),
        OrganizationID=OuterRef("OrganizationID")
    ).values("id")[:1]


    merged_qs = AppoiLetters.annotate(
        uniform_info_id=Subquery(UN_subquery),
        it_info_id=Subquery(IT_subquery),
        hr_info_id=Subquery(HR_subquery)
    ).values(
        'id','first_name','last_name','department','designation','Reporting_to_designation', 'emp_code', 'HR','HK','IT','DEPT','OrganizationID','HKCreatedBy','HRCreatedBy','ITCreatedBy','DEPTCreatedBy',
        'uniform_info_id','it_info_id', 'hr_info_id'
    )
                
    Appointemet = 'Show'

    if AppoiLetters.count() >0:
        Appointemet = 'Hide'
        
    context={
        'AppointLetters':AppoiLetters,
        'merged_qs':merged_qs,
        'OID':OID,
        'memOrg':memOrg
    }
    return render(request, 'HR/Issue_And_Clearance/Issue_Page.html', context)


from EmpResignation.models import EmpResigantionModel
from HR_Inventory.models import HR_Inventory_Information

def Clearance_view(request):
    OrganizationID = request.session["OrganizationID"] 
    OID  = request.GET.get('OID')
    if OID:
        OrganizationID= OID
        
    # Resigantions = EmpResigantionModel.objects.filter(OrganizationID=OrganizationID,IsDelete=False).only('Name','Emp_Code','Dept','Designation','HR','HK','IT','IsDEPT','OrganizationID').order_by('-CreatedDateTime')

    Resigantions = EmpResigantionModel.objects.filter(
        OrganizationID=OrganizationID,
        IsDelete=False
    ).values(
        'id','Name','Emp_Code','Dept','Designation','HR','HK','IT','IsDEPT','OrganizationID','HKCreatedBy','ITCreatedBy','DEPTCreatedBy',
    ).order_by('-CreatedDateTime')

    UN_subquery = UniformInformation.objects.filter(
        EmployeeCode=OuterRef("Emp_Code"),
        OrganizationID=OuterRef("OrganizationID")
    ).values("id")[:1]
    
    IT_subquery = ItInformation.objects.filter(
        EmployeeCode=OuterRef("Emp_Code"),
        OrganizationID=OuterRef("OrganizationID")
    ).values("id")[:1]
    
    HR_subquery = HR_Inventory_Information.objects.filter(
        EmployeeCode=OuterRef("Emp_Code"),
        OrganizationID=OuterRef("OrganizationID")
    ).values("id")[:1]

    merged_qs = Resigantions.annotate(
        uniform_info_id=Subquery(UN_subquery),
        it_info_id=Subquery(IT_subquery),
        hr_info_id=Subquery(HR_subquery)
    ).values(
        'id','Name','Emp_Code','Dept','Designation','HR','HK','IT','IsDEPT','OrganizationID','HRCreatedBy', 'HKCreatedBy','ITCreatedBy','DEPTCreatedBy',
        'uniform_info_id','it_info_id', 'hr_info_id'
    )
                
    Appointemet = 'Show'

    if Resigantions.count() >0:
        Appointemet = 'Hide'
        
    context={
        'Resigantions':Resigantions,
        'merged_qs':merged_qs
    }
    return render(request, 'HR/Issue_And_Clearance/Clearance_Page.html', context)




def Hod_Approve_Request(request):
    id = request.GET.get("id")

    obj = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(id=id, IsDelete=False).first()
    if not obj:
        messages.error(request, "Record not found")
        return redirect("Issue_view")

    obj.DEPT = True
    obj.DEPTCreatedBy = request.session["UserID"]
    obj.DEPTCreatedDateTime = timezone.now()
    obj.save()

    messages.success(request, "Approved Successfully")
    return redirect("Issue_view")



def Hod_Hold_Request(request):
    id = request.GET.get("id")

    obj = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(id=id, IsDelete=False).first()
    if not obj:
        messages.error(request, "Record not found")
        return redirect("Issue_view")

    obj.DEPT = False
    obj.save()

    messages.success(request, "Put on Hold Successfully")
    return redirect("Issue_view")





def Hod_Approve_Request_Clearance(request):
    id = request.GET.get("id")

    obj = EmpResigantionModel.objects.filter(id=id, IsDelete=False).first()
    if not obj:
        messages.error(request, "Record not found")
        return redirect("Clearance_view")

    obj.IsDEPT = True
    obj.DEPTCreatedBy = request.session["UserID"]
    obj.DEPTCreatedDateTime = timezone.now()
    obj.save()

    messages.success(request, "Approved Successfully")
    return redirect("Clearance_view")

