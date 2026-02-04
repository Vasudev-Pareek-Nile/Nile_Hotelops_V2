from django.shortcuts import render,redirect,render
from app.views import OrganizationList,Error
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from .models import Assessment_Master,Assessment_Factor_Details,Assessment_MasterDeletedFile,UserTypeFlow,DepartmentLevelConfig,DepartmentLevelConfigDetails,Factors,EmployeeDataRequest_Master,EmployeePersonalDataDeletedFile,EmployeePersonalData, EmployeeFamilyData, EmployeeEmergencyInfoData
from Manning_Guide.models import OnRollDepartmentMaster,LavelAdd,OnRollDesignationMaster
from .azure import upload_file_to_blob,download_blob
import mimetypes
from django.http import HttpResponse, Http404
from .models import EmployeeDataRequest_Master
import uuid
from django.http import JsonResponse
from rest_framework import status
from django.contrib import messages
from django.utils import timezone
import json
from geopy.geocoders import Nominatim
import requests
from app.models import OrganizationMaster
from Manning_Guide.models import LavelAdd
from Reference_check.models import Reference_check,ReferenceDetails
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import datetime
from datetime import timedelta
from app.models import OrganizationMaster
from Manning_Guide.models import LavelAdd
import calendar



def upload_file(file,id,folder_name,ModelName):
       
        if ModelName == "EmployeeIdentityInfoData_Pan":
            new_file = upload_file_to_blob(file,id,folder_name,ModelName)
            new_file.PanFileTitle = file.name
            new_file.save()
        elif ModelName == "EmployeeIdentityInfoData_Aadhaar":
            new_file = upload_file_to_blob(file,id,folder_name,ModelName)
            new_file.AadhaarFileTitle = file.name
            new_file.save()    
        elif ModelName == "EmployeeIdentityInfoData_License":
            new_file = upload_file_to_blob(file,id,folder_name,ModelName)
            new_file.DrivingFileTitle = file.name
            new_file.save()   
                 
            

        else:
         
            new_file = upload_file_to_blob(file,id,folder_name,ModelName)
            new_file.FileTitle = file.name
            new_file.save()

def view_file(request):
    ID = request.GET.get('ID')
    model_name = request.GET.get('model') 

    if model_name == 'Assessment_Master':
        try:
            file = Assessment_Master.objects.get(id=ID)
        except Assessment_Master.DoesNotExist:
            raise Http404("Assessment_Master record not found.")
    elif model_name == 'EmployeePersonalData':
        try:
            file = EmployeePersonalData.objects.get(id=ID)
        except EmployeePersonalData.DoesNotExist:
            raise Http404("EmployeePersonalData record not found.")
    elif model_name == 'EmployeeEducationData':
        try:
            file = EmployeeEducationData.objects.get(id=ID)
        except EmployeeEducationData.DoesNotExist:
            raise Http404("EmployeeEducationData record not found.")
    elif model_name == 'EmployeePreviousWorkData':
        try:
            file = EmployeePreviousWorkData.objects.get(id=ID)
        except EmployeePreviousWorkData.DoesNotExist:
            raise Http404("EmployeePreviousWorkData record not found.")    
    
    elif model_name == 'EmployeeDocumentsInfoData':
        try:
            file = EmployeeDocumentsInfoData.objects.get(id=ID)
        except EmployeeDocumentsInfoData.DoesNotExist:
            raise Http404("EmployeeDocumentsInfoData record not found.")
    elif model_name == 'EmployeeIdentityInfoData_Pan':
        try:
            file = EmployeeIdentityInfoData.objects.get(id=ID)
        except EmployeeIdentityInfoData.DoesNotExist:
            raise Http404("EmployeeIdentityInfoData record not found.")  
    elif model_name == 'EmployeeIdentityInfoData_Aadhaar':
        try:
            file = EmployeeIdentityInfoData.objects.get(id=ID)
        except EmployeeIdentityInfoData.DoesNotExist:
            raise Http404("EmployeeIdentityInfoData record not found.")
    elif model_name == 'EmployeeIdentityInfoData_License':
        try:
            file = EmployeeIdentityInfoData.objects.get(id=ID)
        except EmployeeIdentityInfoData.DoesNotExist:
            raise Http404("EmployeeIdentityInfoData record not found.")            



    else:
        raise Http404("Invalid model name.")

    if model_name == "EmployeeIdentityInfoData_Pan":
        file_id = file.PanFileName
        file_name = file.PanFileTitle
        file_type, _ = mimetypes.guess_type(file_id)
    elif model_name == "EmployeeIdentityInfoData_Aadhaar":
        file_id = file.AadhaarFileName
        file_name = file.AadhaarFileTitle
        file_type, _ = mimetypes.guess_type(file_id)
    elif model_name == "EmployeeIdentityInfoData_License":
        file_id = file.DrivingFileName
        file_name = file.DrivingFileTitle
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

def CopyFile(file_id):
  
    file_type, _ = mimetypes.guess_type(file_id)
    if file_type is None:
        file_type = 'application/octet-stream'
    
  
    blob_content = download_blob(file_id)
    
    if blob_content:
        return blob_content.readall(), file_type
    else:
        raise Http404("File content not found.")

from Open_position.azure import download_blob as DB
def CopyFileResume(file_id):
  
    file_type, _ = mimetypes.guess_type(file_id)
    if file_type is None:
        file_type = 'application/octet-stream'
    
  
    blob_content = DB(file_id)
    
    if blob_content:
        return blob_content.readall(), file_type
    else:
        raise Http404("File content not found.")




def repalce_file(ID,ModelName):
    if ModelName == "Assessment_Master":
        file = Assessment_Master.objects.get(id=ID)
        deletefile = Assessment_MasterDeletedFile.objects.create(Assessment_Master= file,FileName = file.FileName,FileTitle = file.FileTitle)
        file.FileName = None
        file.FileTitle = None
        file.save()
    if ModelName == "EmployeePersonalData":
        file = EmployeePersonalData.objects.get(id=ID)
        deletefile = EmployeePersonalDataDeletedFile.objects.create(EmployeePersonalData= file,FileName = file.FileName,FileTitle = file.FileTitle)
        file.FileName = None
        file.FileTitle = None
        file.save()


from app.models import City_Location_Master    

def get_location_details(request):
    pincode = request.GET.get('pincode')
    
    if not pincode:
        return JsonResponse({'error': 'Pincode is required'}, status=400)

    try:
        location = City_Location_Master.objects.filter(PinCode=pincode).first()
   
        if location:
           
            city =   location.DistrictName
            state =  location.StateName
           
            return JsonResponse({
                'city': city,
                'state': state
               
            })
        else:
            return JsonResponse({'error': 'Location not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_ifsc_details(request):
    ifsc_code = request.GET.get('ifsc_code')
    if not ifsc_code:
        return JsonResponse({'error': 'ifsc_code parameter is required'}, status=400)

    url = f"https://ifsc.razorpay.com/{ifsc_code}"
    response = requests.get(url)

    if response.status_code == 200:
        details = response.json()
        branch = f"{details['BRANCH']} - {details['CITY']} {details['STATE']} "  
        bank_name = details['BANK']
        return JsonResponse({'Bank Name': bank_name, 'Branch': branch})
    else:
        return JsonResponse({'error': 'No details found for ifsc_code'}, status=404)

from app.models import OrganizationMaster
def GetOrganizationID(OrganizationName):
    OrganizationID   = OrganizationMaster.objects.filter(IsDelete=False,OrganizationName=OrganizationName).first().OrganizationID
    return OrganizationID



def InterviewAssementCEO(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
    if request.method == "GET":
        AID = request.GET.get('AID')
        OID = request.GET.get('OID')

        Status = request.GET.get('Status')
        Remarks = request.GET.get('Remarks')


        if not AID or not Status or not Remarks:
            response_data = {
                'message': 'Invalid parameters'
            }
            return JsonResponse(response_data, status=400)
        
        obj = Assessment_Master.objects.filter(id=AID,IsDelete=False).first()
        
        if obj is None:
            response_data = {
                'message': 'Object not found'
            }
            return JsonResponse(response_data, status=404)
        
        obj.ceo_as = Status
        obj.ceo_as_remarks = Remarks
        obj.ceo_actionOn =  datetime.date.today()
        obj.ceo_actionOnDatetime = datetime.datetime.now()
        LastApprovalStage = LastApprovalStageFun(obj.Level,obj.Department,OID)
     
        UserType = "CEO"
   
        if UserType  == LastApprovalStage:
            if LastApprovalStage == "CEO":
                     obj.LastApporvalStatus  = Status

        obj.ModifyBy = UserID
        obj.save()

        response_data = {
            'message': f'{Status} successfully'
        }
        return JsonResponse(response_data, status=200)
    



def RejectInterviewAssement(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
    if request.method == "GET":
        AID = request.GET.get('AID')
        OID = request.GET.get('OID')


        if not AID:
            response_data = {
                'message': 'Invalid parameters'
            }
            return JsonResponse(response_data, status=400)
        
        obj = Assessment_Master.objects.filter(id=AID,IsDelete=False,OrganizationID=OID).first()
        
        if obj is None:
            response_data = {
                'message': 'Object not found'
            }
            return JsonResponse(response_data, status=404)
        obj.LOIStatus = "Rejected"
        obj.ModifyBy = UserID
        obj.LastLoistatusModifyDate = datetime.datetime.now()
        obj.save()

        response_data = {
            'message': f'Rejected successfully'
        }
        return JsonResponse(response_data, status=200)










def CloseInterviewAssement(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
    if request.method == "GET":
        AID = request.GET.get('AID')
        OID = request.GET.get('OID')


        if not AID:
            response_data = {
                'message': 'Invalid parameters'
            }
            return JsonResponse(response_data, status=400)
        
        obj = Assessment_Master.objects.filter(id=AID,IsDelete=False,OrganizationID=OID).first()
        
        if obj is None:
            response_data = {
                'message': 'Object not found'
            }
            return JsonResponse(response_data, status=404)
        obj.LastApporvalStatus = "Closed"
        obj.ModifyBy = UserID
    
        obj.save()

        response_data = {
            'message': f'Closed successfully'
        }
        return JsonResponse(response_data, status=200)




def AppliedForORGID(location):
     OID = OrganizationMaster.objects.filter(OrganizationName=location,IsDelete=False).first()
     if OID:
          return OID.OrganizationID
     else:
          return None
     


def LastApprovalStageFun(level, department, OrganizationID):
    if not level or not department:
        return {"error": "Level and Department are required parameters"}
    
    def get_department_level_details(dept, level, org_id):
        try:
            return DepartmentLevelConfig.objects.get(
                Department=dept,
                 Level__icontains=f"'{level}'",
                OrganizationID=org_id,
                IsDelete=False
            )
        except DepartmentLevelConfig.DoesNotExist:
            return None

    deptLevel = get_department_level_details(department, level, OrganizationID)
    
    if not deptLevel:
        deptLevel = get_department_level_details(department, level, 3)

    if not deptLevel:
        deptLevel = get_department_level_details('All', level, 3)

    if deptLevel:
        stages = DepartmentLevelConfigDetails.objects.filter(
            DepartmentLevelConfig=deptLevel,
            IsDelete=False
        ).values('UserType').order_by('LevelSortOrder')

        if stages.exists():
            return stages.last()['UserType']

    return []  



     
def ApprovalStageFun(level, department, OrganizationID):
    if not level or not department:
        return {"error": "Level and Department are required parameters"}
    
    def get_department_level_details(dept, level, org_id):
        try:
            return DepartmentLevelConfig.objects.get(
                Department=dept,
                Level__icontains=f"'{level}'",
                OrganizationID=org_id,
                IsDelete=False
            )
        except DepartmentLevelConfig.DoesNotExist:
            return None
        except:
            print("Error------",dept, level, org_id)

    deptLevel = get_department_level_details(department, level, OrganizationID)
    
    if not deptLevel:
        deptLevel = get_department_level_details(department, level, 3)

    if not deptLevel:
        deptLevel = get_department_level_details('All', level, 3)

    if deptLevel:
        stages = DepartmentLevelConfigDetails.objects.filter(
            DepartmentLevelConfig=deptLevel,
            IsDelete=False
        ).values('UserType').order_by('LevelSortOrder')

        if stages.exists():
            stages_order = [stage['UserType'] for stage in stages]
            return stages_order
            
    return []  


import _json

def HODLevel(Level, Department,OrganizationID):
    if not (Level and Department and OrganizationID):
        return False
    
    def get_department_level_details(dept, level, org_id):
        dept_level = DepartmentLevelConfig.objects.filter(
            Department=dept,
            Level__icontains=f"'{level}'",
            OrganizationID=org_id,
            IsDelete=False
        ).first()
        
        if dept_level:
            obj = DepartmentLevelConfigDetails.objects.filter(
                IsDelete=False,
                DepartmentLevelConfig=dept_level
            ).order_by('LevelSortOrder').values('LevelSortOrder', 'UserType')
            
            if obj.exists():
                return obj, dept_level

        return None, None

    obj, deptLevel = get_department_level_details(Department, Level, OrganizationID)

    if not obj:
        obj, deptLevel = get_department_level_details(Department, Level, 3)
     
    
    if not obj:
        obj, deptLevel = get_department_level_details("All", Level, 3)
      
    
    if not obj:
        return JsonResponse([], safe=False)

    hod_found = any(o['UserType'] == 'HOD' for o in obj)

   

    return {
        'hod_found': hod_found
    }


from io import BytesIO


from Open_position.models import CareerResume


# def InterviewAssessmentCreate(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
#     OrganizationID = request.session.get("OrganizationID")
#     UserID = str(request.session.get("UserID"))
#     Department = request.session.get("Department_Name")
#     EmployeeCode = request.session.get("EmployeeCode")
    
#     Departmentsession = str(Department).lower()

    
#     UserType = request.session.get("UserType")
#     UserType = str(UserType).lower()
#     blocked_user_types  = None
  
#     if OrganizationID == '3' and UserType == 'hod':

#         UserType = "rd"
     
    
#     # appliedFor = request.GET.get('positionAppliedFor')
#     orgs = OrganizationList(OrganizationID)
#     Designations  = None
#     Resumeobj   = None
#     Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')

#     AID = request.GET.get('AID')
#     OPID=request.GET.get('OPID')
    
      
#     appliedFor  = None
#     position  = None    
   
#     AM_obj = None
#     factor_details = {}
#     Datafrom =''
#     if AID:
#         AM_obj = Assessment_Master.objects.filter(
#             IsDelete=False, id=AID
#         ).first()
#         position = AM_obj.position
#         blocked_user_types = AM_obj.block_lower_level_edit()
        
     
#         Datafrom  = 'DatafromAssessment'
                  
#         if not  AM_obj:
#             return Error(request, f"Interview Assessment is not Found.")   
    
#         if AM_obj:
#             appliedFor = AM_obj.AppliedFor
            
           
#             factor_details = Assessment_Factor_Details.objects.filter(MasterID=AID).values(
#                 'CategoryID', 'factor', 'hr_rating', 'hr_remarks', 
#                 'hod_rating', 'hod_remarks', 'gm_rating', 
#                 'gm_remarks', 'rd_rating', 'rd_remarks'
#             )

          
#             factor_details = {f['CategoryID']: f for f in factor_details}
#         MasterID = AID
       
#     if OPID:
#          Resumeobj  = CareerResume.objects.filter(id=OPID).first()
#          if not  Resumeobj:
#             return Error(request, f"Resume not Found.")   
    
#          if Resumeobj:
#               AM_obj =  {
#                    'Name':Resumeobj.first_name + " "+ Resumeobj.last_name,
#                    'AppliedFor':AppliedForORGID(Resumeobj.location),
#                    'position':Resumeobj.job_title,
#                    'ContactNumber':Resumeobj.phone,
#                    'Email':Resumeobj.email


#               }
#               Datafrom  = 'DatafromResume'
            
#               if int(OrganizationID) != 3:
#                 appliedFor = OrganizationID
#               else:
                  
#                    appliedFor = AppliedForORGID(Resumeobj.location)
           

                   
#               position = Resumeobj.job_title
             
            
     
#     if request.method == "POST":
       
#         HireFor = request.POST.get('hire')
#         InterviewDate = request.POST.get('dateOfInterview')
#         Department = request.POST.get('department')
#         position = request.POST.get('positionAppliedFor')
#         Level = request.POST.get('level')
#         Prefix = request.POST.get('Prefix')
#         Name = request.POST.get('name')
#         workexperience = request.POST.get('experienceType')
       
#         if workexperience == "experience":
#             Years = request.POST.get('Years') or 0
#             Months = request.POST.get('Months') or 0
#             workexperience = f'{Years} Years {Months} Months'
#         familybackground = request.POST.get('familyBackground')
#         pre_salary = request.POST.get('presentSalary') or 0
#         exp_salary = request.POST.get('expectedSalary') or 0

#         Presentdesignation = request.POST.get('Presentdesignation') or ''
#         Expecteddesignation = request.POST.get('Expecteddesignation') or ''

#         ContactNumber = request.POST.get('contactNumber')
#         Email = request.POST.get('Email')

#         ProposedDOJ = request.POST.get('proposedDoj')
#         AppliedFor = request.POST.get('appliedFor')
#         ResumeID = request.POST.get('ResumeID') or 0

#         resume = request.FILES.get('resume')
        
#         hr_as = hr_as_remarks = ''
#         hod_as = hod_as_remarks = ''
#         rd_as = rd_as_remarks = ''
#         gm_as = gm_as_remarks = ''
#         if Datafrom == 'DatafromAssessment'  :
#             Hodobj = HODLevel(AM_obj.Level, AM_obj.Department,OrganizationID)
#             if Hodobj:
#                         HOD = Hodobj['hod_found']
            
#         if 'hr_final_rating' and 'hr_final_remarks' in request.POST:
#             hr_as = request.POST['hr_final_rating'] 
#             hr_as_remarks = request.POST['hr_final_remarks'] 
#         if 'hod_final_rating' in request.POST and 'hod_final_remarks' in request.POST:

            
#             if  Datafrom == 'DatafromAssessment':
#                 if Departmentsession != 'hr' or HOD:  
                
    
#                     hod_as = request.POST['hod_final_rating'] 
#                     hod_as_remarks = request.POST['hod_final_remarks'] 
#             else:
#                 hod_as = request.POST['hod_final_rating'] 
#                 hod_as_remarks = request.POST['hod_final_remarks'] 


#         if 'rd_final_rating' and 'rd_as_remarks' in request.POST:
        
#             rd_as = request.POST['rd_final_rating'] 
#             rd_as_remarks = request.POST['rd_as_remarks'] 
#         if 'gm_final_rating' and 'gm_as_remarks' in request.POST:
#             gm_as = request.POST['gm_final_rating'] 
#             gm_as_remarks = request.POST['gm_as_remarks'] 
        
        
#         if AID:
#             if Departmentsession == 'hr':
#                 AM_obj.HireFor = HireFor
#                 AM_obj.InterviewDate = InterviewDate
#                 AM_obj.Department = Department
#                 AM_obj.position = position
#                 AM_obj.Level = Level
#                 AM_obj.Prefix = Prefix
#                 AM_obj.Name = Name
#                 AM_obj.workexperience = workexperience
#                 AM_obj.familybackground = familybackground
#                 AM_obj.pre_salary = pre_salary
#                 AM_obj.exp_salary = exp_salary
#                 AM_obj.Presentdesignation = Presentdesignation
#                 AM_obj.Expecteddesignation = Expecteddesignation
#                 AM_obj.ContactNumber = ContactNumber
#                 AM_obj.Email = Email
#                 AM_obj.ProposedDOJ = ProposedDOJ
#                 AM_obj.AppliedFor = AppliedFor
#                 AM_obj.ResumeID = ResumeID
            
#             if hr_as != '' and hr_as_remarks != '':
#                 AM_obj.hr_as = hr_as
#                 AM_obj.hr_as_remarks = hr_as_remarks
#             if hod_as != '' and hod_as_remarks != '':

#                 AM_obj.hod_as = hod_as
#                 AM_obj.hod_as_remarks = hod_as_remarks
            
#             if gm_as != '' and gm_as_remarks != '':
            
#                 AM_obj.gm_as = gm_as
#                 AM_obj.gm_as_remarks = gm_as_remarks
            
#             if rd_as != '' and rd_as_remarks != '':

#                 AM_obj.rd_as = rd_as
#                 AM_obj.rd_as_remarks = rd_as_remarks
            
#             if  Datafrom == 'DatafromAssessment':
               
#                 Hodobj = HODLevel(AM_obj.Level, AM_obj.Department,OrganizationID)
#                 if Hodobj:
#                             HOD = Hodobj['hod_found']

#                 if UserType == 'hod'  and HOD:
#                     AM_obj.hod_actionOn =  datetime.date.today()
#                     AM_obj.hod_actionOnDatetime = datetime.datetime.now()

#             if UserType == 'gm':
#                 AM_obj.gm_actionOn =  datetime.date.today()
#                 AM_obj.gm_actionOnDatetime = datetime.datetime.now()

#             if UserType == 'rd':
#                 AM_obj.rd_actionOn =  datetime.date.today()
#                 AM_obj.rd_actionOnDatetime = datetime.datetime.now()     
            


#             # AppovalStage 
#             LastApprovalStage = LastApprovalStageFun(AM_obj.Level,AM_obj.Department,AM_obj.OrganizationID)
#             if not  LastApprovalStage:
#                     return Error(request, f"ApprovalStage not Found.")   
    

#             if str(LastApprovalStage).lower() == "rd" and  UserType  == str(LastApprovalStage).lower():
#                     AM_obj.rd_as = rd_as
#                     AM_obj.rd_as_remarks = rd_as_remarks
#                     AM_obj.rd_actionOn =  datetime.date.today()
#                     AM_obj.rd_actionOnDatetime = datetime.datetime.now()
#                     AM_obj.LastApporvalStatus  = rd_as
                 
           
#             if str(LastApprovalStage).lower() == "gm" and  UserType  == str(LastApprovalStage).lower():
          
                   
#                     AM_obj.gm_as = gm_as
#                     AM_obj.gm_as_remarks = gm_as_remarks
#                     AM_obj.gm_actionOn =  datetime.date.today()
#                     AM_obj.gm_actionOnDatetime = datetime.datetime.now()
#                     AM_obj.LastApporvalStatus  = gm_as
                  
                          




#             AM_obj.LastStatusUpdateBy = UserID
#             AM_obj.LastStatusUpdateOn = datetime.datetime.now()
#             AM_obj.ModifyBy = UserID
#             AM_obj.save()

#             if resume:
#                 repalce_file(AID,"Assessment_Master")
#                 upload_file(resume, AID,"Resumes","Assessment_Master")
#         else:
#             Assessment_obj = Assessment_Master.objects.create(
#                 OrganizationID=OrganizationID,
#                 CreatedBy=UserID,
#                 HireFor=HireFor,
#                 InterviewDate=InterviewDate,
#                 Department=Department,
#                 position=position,
#                 Level=Level,
#                 Prefix=Prefix,
#                 Name=Name,
#                 workexperience=workexperience,
#                 familybackground=familybackground,
#                 pre_salary=pre_salary,
#                 exp_salary=exp_salary,
#                 Presentdesignation = Presentdesignation,
#                 Expecteddesignation = Expecteddesignation,

#                 ContactNumber=ContactNumber,
#                 Email = Email,
#                 ProposedDOJ=ProposedDOJ,
#                 AppliedFor=AppliedFor,
#                 ResumeID=ResumeID,
#                 hod_as =hod_as,
#                 hod_as_remarks =hod_as_remarks,
#                 gm_as = gm_as,
#                 gm_as_remarks = gm_as_remarks,
#                 rd_as = rd_as,
#                 rd_as_remarks = rd_as_remarks,
#                 hr_as=hr_as,
#                 hr_as_remarks=hr_as_remarks,
#                 hr_actionOn =  datetime.date.today(),
#                 hr_actionOnDatetime = datetime.datetime.now(),
                

#             )

#             if resume is not None:
#                 upload_file(resume, Assessment_obj.id,"Resumes","Assessment_Master")
#             else:
               
#                 if Resumeobj:
#                         file_content, file_type = CopyFileResume(Resumeobj.resume_url)
                        
#                         file_io = BytesIO(file_content)
                        
#                         file_io.name = str(Resumeobj.resume)
                        
#                         upload_file(file_io, Assessment_obj.id, "Resumes", "Assessment_Master")



                
      
#             MasterID = Assessment_obj.id
        
#         for category_id in range(1, 11):
#             category_id_str = str(category_id)
            
#             selected_factors = request.POST.getlist(f'factor_{category_id_str}')
#             factor_string = ', '.join(selected_factors) if selected_factors else None
            
#             hr_rating = request.POST.get(f'hr_rating_{category_id_str}')
#             hr_remarks = request.POST.get(f'hr_remarks_{category_id_str}')
#             hod_rating = request.POST.get(f'hod_rating_{category_id_str}')
#             hod_remarks = request.POST.get(f'hod_remarks_{category_id_str}')
#             gm_rating = request.POST.get(f'gm_rating_{category_id_str}')
#             gm_remarks = request.POST.get(f'gm_remarks_{category_id_str}')
#             rd_rating = request.POST.get(f'rd_rating_{category_id_str}')
#             rd_remarks = request.POST.get(f'rd_remarks_{category_id_str}')

           
#             assessment_detail, created = Assessment_Factor_Details.objects.get_or_create(
#                 MasterID=MasterID,
#                 OrganizationID=OrganizationID,
              
#                 CategoryID=category_id_str,
#                 defaults={'CreatedBy': UserID}
#             )


#             if factor_string:
#                 assessment_detail.factor = factor_string
#             else:
#                 assessment_detail.factor = ''

#             if hr_rating :
#                 assessment_detail.hr_rating = hr_rating
#             else:
#                 assessment_detail.hr_rating = ''
 
            
#             if hr_remarks :
#                 assessment_detail.hr_remarks = hr_remarks
#             else:
#                 assessment_detail.hr_remarks = ''    
            
#             if hod_rating :
#                 assessment_detail.hod_rating = hod_rating
#             else:
#                 assessment_detail.hod_rating = ''     
            
#             if hod_remarks :
#                 assessment_detail.hod_remarks = hod_remarks
#             else:
#                 assessment_detail.hod_remarks = '' 
            
#             if gm_rating :
#                 assessment_detail.gm_rating = gm_rating
#             else:
#                 assessment_detail.gm_rating = ''     
#             if gm_remarks :
#                 assessment_detail.gm_remarks = gm_remarks
#             else:
#                 assessment_detail.gm_remarks = '' 
#             if rd_rating :
#                 assessment_detail.rd_rating = rd_rating
#             else:
#                 assessment_detail.rd_rating = ''     
#             if rd_remarks :
#                 assessment_detail.rd_remarks = rd_remarks
#             else:
#                 assessment_detail.rd_remarks = ''   
           
             
           
#             assessment_detail.ModifyBy = UserID
#             assessment_detail.save()
        
#         messages.success(request, 'Assessment details saved successfully.')
#         return redirect('InterviewAssessmentList')
#     HrData = 'None'
    
#     from HumanResources.views import MultipleDepartmentofEmployee

#     # if EmployeeCode:
#     #     EmployeeDepartment  = DepartmentofEmployee(request, OrganizationID, EmployeeCode)
#     #     if not EmployeeDepartment:
#     #         return Error(request, "Employee Details not Found.Update in Human Resources")
#     # else:
#     #     return Error(request, "Employee Code is required. Please update it in User Details.")
          

#     # if AM_obj is not None and AID :
#     #     if EmployeeDepartment:
#     #         if AM_obj.Department == EmployeeDepartment:
#     #             HrData = 'Show'



#         # get reportimg to desingtion  

#     from HumanResources.views import MultipleDepartmentofEmployee
#     EmployeeDepartmentList = []
#     if EmployeeCode:
#         EmployeeDepartmentobj  = MultipleDepartmentofEmployee(OrganizationID, EmployeeCode)
#         if  EmployeeDepartmentobj:
#              EmployeeDepartmentList = EmployeeDepartmentobj
             
        
#         else:    
#             return Error(request, "Employee Details not Found.Update in Human Resources")
#     else:
#         return Error(request, "Employee Code is required. Please update it in User Details.")
          

#     if AM_obj is not None and AID :
       
#             if AM_obj.Department in EmployeeDepartmentList:
#                 HrData = 'Show'



#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     context = {
#         'orgs': orgs,
#       'appliedFor': appliedFor if appliedFor is not None else OrganizationID,

#         'AM_obj': AM_obj,
#         'HrData':HrData,
#         'Designations': Designations,
#         'position':position,
#         'UserType': UserType,
#         'OrganizationID':OrganizationID,

#         'Department': Departmentsession,
#         'factor_details': factor_details,
#         'hotelapitoken':hotelapitoken,
#         'Resumeobj':Resumeobj,
       
#        'blocked_user_types': json.dumps(blocked_user_types),



      
#     }
#     return render(request, 'InterviewAssessment/InterviewAssessmentCreate.html', context)



def InterviewAssessmentView(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    AID = request.GET.get('AID')
    appliedFor = request.GET.get('positionAppliedFor', OrganizationID)
    orgs = OrganizationList(OrganizationID)
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
   

    AM_obj = None
    factor_details = {}

    if AID:
        AM_obj = Assessment_Master.objects.filter(
            IsDelete=False, id=AID
        ).first()
        position = AM_obj.position
        if AM_obj:
           
            factor_details = Assessment_Factor_Details.objects.filter(MasterID=AID).values(
                'CategoryID', 'factor', 'hr_rating', 'hr_remarks', 
                'hod_rating', 'hod_remarks', 'gm_rating', 
                'gm_remarks', 'rd_rating', 'rd_remarks'
            )

          
            factor_details = {f['CategoryID']: f for f in factor_details}
        MasterID = AID

      
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    context = {
        'AM_obj': AM_obj,
        'factor_details': factor_details,
         'appliedFor': appliedFor,
           'Designations': Designations,
            'orgs': orgs,
             'hotelapitoken':hotelapitoken,
        'OrganizationID':OrganizationID,

       
    }
    return render(request, 'InterviewAssessment/InterviewAssessmentView.html', context)




from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  # Install xhtml2pdf library if not already installed


MasterJSON = [
{
    "CategoryID": 1,
    "Title": "EDUCATIONAL BACKGROUND",
    "Item": [
        {
            "ItemID": 1,
            "Title": "",
            "ItemType": "checkbox",
            "ItemOption": ["10Th Pass", "12Th Pass", "Bachelor", "Masters", "Diploma"]
        }
    ]
},
{
    "CategoryID": 2,
    "Title": "KNOWLEDGE",
    "Item": [
        {
            "ItemID": 2,
            "Title": "",
            "ItemType": "checkbox",
            "ItemOption": ["Technical", "Hotel", "Current Awareness", "Software Knowledge"]
        }
    ]
},
{
    "CategoryID": 3,
    "Title": "WORK/RELATED EXPERIENCE",
    "Item": [
        {
            "ItemID": 3,
            "Title": "Total experience in relevant area.",
            "ItemType": "label",
        }
    ]
},
{
    "CategoryID": 4,
    "Title": "COMMUNICATION",
    "Item": [
        {
            "ItemID": 4,
            "Title": "",
            "ItemType": "checkbox",
            "ItemOption": ["Speech", "Non-Verbal", "Clarity", "Coherence"]
        }
    ]
},
{
    "CategoryID": 5,
    "Title": "PERSONALITY",
    "Item": [
        {
            "ItemID": 5,
            "Title": "As a new entrant in Team Meetings would you prefer to listen and execute or like to pitch in?",
            "ItemType": "li",
        },
        {
            "ItemID": 6,
            "Title": "How would you deal with unreasonable guests without compromising the organization?",
            "ItemType": "li",
        },
        {
            "ItemID": 7,
            "Title": " How would you deal with a non performing team member who is part of an assignment you are coordinating?",
            "ItemType": "li",
        }
    ]
},
{
    "CategoryID": 6,
    "Title": "ATTITUDE",
    "Decription":"Ability to maintain positive approach towards Work and people",
    "Item": [
        {
            "ItemID": 5,
            "Title": "your teammate is struggling and with overwork and your supervisor asks you to pitch in over and above your load.how will you approach this?",
            "ItemType": "li",
        },
        {
            "ItemID": 6,
            "Title": "your teammate is struggling and with overwork and your supervisor asks you to pitch in over and above your load.how will you approach this? <br/> your teammate is struggling and with overwork and your supervisor asks you to pitch in over and above your load.how will you approach this?",
            "ItemType": "li",
        },
    ]
},
{
    "CategoryID": 7,
    "Title": "POTENTIAL",
    "Decription": "To ascertain future growth & career development",
    "Item": [
        {
            "ItemID": 5,
            "Title": "Where do you see yourself in the next 5 years?",
            "ItemType": "li",
        },
        {
            "ItemID": 6,
            "Title": "And how do you see yourself getting there and what are you willing to sacrifice to do so ?",
            "ItemType": "li",
        },
    ]
},
{
    "CategoryID": 8,
    "Title": "GROOMING",
    "Decription": "Is suitably groomed to cater to our requirements",
    "Item": [
        {
            "ItemID": 5,
            "Title": "Why do you think grooming is important? in every job and particularly our industry?",
            "ItemType": "li",
        },
        {
            "ItemID": 6,
            "Title": "Why do you think grooming is important? in every job and particularly our industry?",
            "ItemType": "li",
        },
    ]
},
{
    "CategoryID": 9,
    "Title": "LEADERSHIP ABILITY",
    "Decription": "Displays appropriate leadership qualities",
    "Item": [
        {
            "ItemID": 5,
            "Title": "Your junior has been wrongly accused by a guest and that has gone viral.how will you protect him?",
            "ItemType": "li",
        },
        {
            "ItemID": 6,
            "Title": "Your Unit managing an event is falling apart and things are getting messy.How will you pull the situation back to manageable or rather try and exceed expectation?",
            "ItemType": "li",
        },
    ]
},
{
    "CategoryID": 10,
    "Title": "ANALYTICAL ABILITY",
    "Decription": "Possess skills to visualize & analyze",
    "Item": [
        {
            "ItemID": 5,
            "Title": "Imagine a restaurant with capacity of 50 reduced to 20 in these COVID-19 times. You have overbooked. How will you deal with it",
            "ItemType": "li",
        },
        {
            "ItemID": 6,
            "Title": "There is a lockdown announced last minute and you have guests who cannot leave and others arriving how will you deal with that ?",
            "ItemType": "li",
        },
    ]
}
]

# def InterviewAssessmentPdf(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)

 
#     AID = request.GET.get('AID')

#     if not AID:
#         return HttpResponse("Assessment ID is required", content_type='text/plain')

#     AM_obj = Assessment_Master.objects.filter(IsDelete=False, id=AID).first()
#     if not AM_obj:
#         return HttpResponse("Invalid Assessment ID", content_type='text/plain')
#     UserList = ApprovalStageFun(AM_obj.Level, AM_obj.Department, AM_obj.AppliedFor)
    
#     print("UserList = ",UserList)
#     factor_details = Assessment_Factor_Details.objects.filter(
#         MasterID=AID,
#         hr_rating__isnull=False,
#         hod_rating__isnull=False,
#         gm_rating__isnull=False,
#         rd_rating__isnull=False
#     ).values(
#         'CategoryID', 'factor', 'hr_rating', 'hr_remarks',
#         'hod_rating', 'hod_remarks', 'gm_rating',
#         'gm_remarks', 'rd_rating', 'rd_remarks'
#     )

#     factor_details_dict = {}
#     for factor in factor_details:
#         category_id = factor['CategoryID']
#         if category_id not in factor_details_dict:
#             factor_details_dict[category_id] = []
#         factor_details_dict[category_id].append(factor)

#     context = {
#         'AM_obj': AM_obj,
#         'factor_details_dict': factor_details_dict,
#         'MasterJSON': MasterJSON,
#         'UserList':UserList
      
#     }

#     template_path = 'InterviewAssessment/InterviewAssessmentPdf.html'  # Path to your template
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="InterviewAssessment.pdf"'
#     template = get_template(template_path)
#     html = template.render(context)

#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return HttpResponse('Error generating PDF', content_type='text/plain')


def InterviewAssessmentPdf(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    AID = request.GET.get('AID')

    if not AID:
        return HttpResponse("Assessment ID is required", content_type='text/plain')

    AM_obj = Assessment_Master.objects.filter(IsDelete=False, id=AID).first()
    if not AM_obj:
        return HttpResponse("Invalid Assessment ID", content_type='text/plain')

    UserList = ApprovalStageFun(AM_obj.Level, AM_obj.Department, AM_obj.AppliedFor)

    print("UserList = ", UserList)
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

    context = {
        'AM_obj': AM_obj,
        'factor_details_dict': factor_details_dict,
        'MasterJSON': MasterJSON,
        'UserList': UserList
    }

    template_path = 'InterviewAssessment/InterviewAssessmentPdf.html'  # Path to your template
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="InterviewAssessment.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error generating PDF', content_type='text/plain')


# def  InterviewAssessmentList(request):
#      if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#      else:
#         print("Show Page Session")
#      orgs  =  OrganizationMaster.objects.filter(IsDelete=False,Activation_status=1)
#      Levels  = LavelAdd.objects.filter(IsDelete=False)
#      OrganizationID = request.session["OrganizationID"] 
#      SessionOrganizationID =  int(OrganizationID)
   
#      hotelapitoken = MasterAttribute.HotelAPIkeyToken
#      I  = request.GET.get('I',OrganizationID)
#      Level  = request.GET.get('Level') or 'All'
#      Status  = request.GET.get('Status') or 'Pending'
    
    
#      UserID = str(request.session.get("UserID"))
#      DepartmentU = request.session.get("Department_Name")
#      Department = str(DepartmentU).lower()
     
#      UserType = request.session.get("UserType")
#      UserType = str(UserType).lower()
#      if OrganizationID == '3' and UserType == 'hod':
#          UserType = 'rd'
#      AssessmentsList = []
#      if Department == 'hr':
#          if Level != 'All' :
#             Assessments = Assessment_Master.objects.filter(IsDelete=False,OrganizationID=I,Level=Level, LastApporvalStatus = Status).order_by('-id')
            
#          else:
#             Assessments = Assessment_Master.objects.filter(IsDelete=False,OrganizationID=I, LastApporvalStatus = Status).order_by('-id')
           
     
#      elif UserType == "gm":
#          if Level != 'All' :
#             Assessments = Assessment_Master.objects.filter(IsDelete=False,OrganizationID=I,Level=Level, LastApporvalStatus = Status).order_by('-id')

#          else:
#              Assessments = Assessment_Master.objects.filter(IsDelete=False,OrganizationID=I, LastApporvalStatus = Status).order_by('-id')
     
#      elif  UserType == "rd":
#            if Level != 'All' :
#                Assessments = Assessment_Master.objects.filter(Department = DepartmentU,IsDelete=False,Level=Level,OrganizationID=I, LastApporvalStatus = Status).order_by('-id')
#            else:    
#                Assessments = Assessment_Master.objects.filter(Department = DepartmentU,IsDelete=False,OrganizationID=I, LastApporvalStatus = Status).order_by('-id')
#      elif UserType == "ceo":
#          if Level != 'All' :
#               Assessments = Assessment_Master.objects.filter(IsDelete=False,Level=Level,OrganizationID=I, LastApporvalStatus = Status).order_by('-id')
#          else:    
#               Assessments = Assessment_Master.objects.filter(IsDelete=False,OrganizationID=I, LastApporvalStatus = Status).order_by('-id')

     
         

#      else:
#         if Level != 'All':
#               Assessments = Assessment_Master.objects.filter(Department = DepartmentU,IsDelete=False,OrganizationID=I,Level=Level, LastApporvalStatus = Status).order_by('-id')
#         else:
#             Assessments = Assessment_Master.objects.filter(Department = DepartmentU,IsDelete=False,OrganizationID=I, LastApporvalStatus = Status).order_by('-id')
#      if Department != 'hr':
    
#         for Assessment in Assessments:
#                 AssessmentLevel = Assessment.Level
#                 AssessmentDepartment = Assessment.Department

#                 obj = Levelorder(AssessmentLevel,AssessmentDepartment,Assessment,UserType)
#                 if obj == True:
#                     AssessmentsList.append(Assessment.OrganizationID)  
#      else:
#          for Assessment in Assessments:
               
               
               
#                 AssessmentsList.append(Assessment)  
                       
#      context = {'Assessments':AssessmentsList,'orgs':orgs,'I':I,'Levels':Levels,'Status':Status,'Level':Level,'hotelapitoken':hotelapitoken,'SessionOrganizationID':SessionOrganizationID}
#      return render(request,'InterviewAssessment/InterviewAssessmentList.html',context)







def Levelorder(AssessmentLevel, AssessmentDepartment, Assessment, UserType):
    try:
        
        DepartmentLevelobj = DepartmentLevelConfig.objects.filter(
            Department=str(AssessmentDepartment),
            Level__icontains=f"'{AssessmentLevel}'",
            IsDelete=False
        ).first()
        
      
        if not DepartmentLevelobj:
            DepartmentLevelobj = DepartmentLevelConfig.objects.filter(
                Department="All",
                Level__icontains=f"'{AssessmentLevel}'",
                IsDelete=False
            ).first()

        if not DepartmentLevelobj:
          
            return None
        
        DepartmentLevelConfigID = DepartmentLevelobj.id
        
       
        objs = DepartmentLevelConfigDetails.objects.filter(
            IsDelete=False,
            DepartmentLevelConfig_id=DepartmentLevelConfigID
        )
        
        Status = {
            'HR': Assessment.hr_as,
            'HOD': Assessment.hod_as,
            'GM': Assessment.gm_as,
            'RD': Assessment.rd_as,
            'CEO': Assessment.ceo_as,
        }
        
        Append = False
        
        for obj in objs:
            if UserType.lower() == obj.UserType.lower():
                Level = obj.LevelSortOrder
                LevelNumber = int(Level.split()[1])
                
               
                previousLevel = DepartmentLevelConfigDetails.objects.filter(
                    IsDelete=False,
                    DepartmentLevelConfig_id=DepartmentLevelConfigID,
                    LevelSortOrder=f'Level {LevelNumber-1}'
                ).first()
                
                NextLevel = DepartmentLevelConfigDetails.objects.filter(
                    IsDelete=False,
                    DepartmentLevelConfig_id=DepartmentLevelConfigID,
                    LevelSortOrder=f'Level {LevelNumber+1}'
                ).first()

              
               
                if previousLevel and previousLevel.UserType:
                    previousUserType = previousLevel.UserType
                    if Status.get(previousUserType, '') == 'Approved':
                        Append = True
                        break
        
        return Append
    
    except Exception as e:
        print(f"Error in Levelorder: {e}")
        return None



# def InterviewAssessmentList(request):
#     from HumanResources.views import DepartmentofEmployee
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
    
#     #  year and month  setup
#     from datetime import datetime    
#     year = request.GET.get('year')
#     if year:
#         year = int(year)
#     else:
#         year = datetime.now().year



#     month_no =  request.GET.get('month_no')
#     if month_no:
#         month_no = int(month_no)
#     else:
#         month_no = datetime.now().month  
#     month_name = calendar.month_name[int(month_no)]              
#     today = datetime.today()
#     CYear = today.year
#     CMonth = today.month

    
    
    
#     OrganizationID = request.session.get("OrganizationID")
#     SessionOrganizationID =  int(OrganizationID)
#     EmployeeCode = request.session["EmployeeCode"]
#     Department = None
#     if EmployeeCode:
#         Departmentobj = DepartmentofEmployee(request, OrganizationID, EmployeeCode)
#         if Departmentobj :
#             Department =  Departmentobj['work_Department']
        
   
#     UserType = str(request.session.get("UserType", '')).lower()
    
#     if OrganizationID == '3' and UserType == 'hod':
#         UserType = 'rd'
    
#     orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1)
#     Levels = LavelAdd.objects.filter(IsDelete=False)

#     I  = request.GET.get('I',OrganizationID)
#     Level  = request.GET.get('Level') or 'All'
#     Status  = request.GET.get('Status') or 'All'
    
    
#     assessments_filter = {
#         'IsDelete': False,
#         'OrganizationID': I,
      
#         'InterviewDate__year': year,
#         'InterviewDate__month': month_no,
#     }
    
    
#     if Level != 'All':
#         assessments_filter['Level'] = Level
#     if Status != 'All':
#         assessments_filter['LastApporvalStatus'] =  Status
        
            
#     if Department is not None:
#         if UserType == 'rd':
#             assessments_filter['Department'] = Department
#         if UserType == 'hod' and Department != 'Human Resources':
#             assessments_filter['Department'] = Department
    
#     Assessments = Assessment_Master.objects.filter(**assessments_filter).order_by('-id')
#     for Assessment  in Assessments:
#         ref = 'Fresher'
#         if Assessment.workexperience != 'Fresher': 
#             ref = 0
#             if Assessment.reference:
#                 refobj  = ReferenceDetails.objects.filter(IsDelete=False,OrganizationID = OrganizationID,Inteview_AssementID=Assessment.id).first()
            
#                 if refobj:
                
#                     if refobj.ref1_status == 1  :
#                         ref = 1
#         Assessment.ref  = ref        
                   
              
    
                       

#     AssessmentsList = [
#     a for a in Assessments 
#     if (Department != 'Human Resources' and Levelorder(a.Level, a.Department, a, UserType)) or Department == 'Human Resources'
#     ]
    
    
#     context = {
#         'Assessments': AssessmentsList,
#         'orgs': orgs,
#         'I': I,
#         'Levels': Levels,
#         'Level': Level,
#         'hotelapitoken': MasterAttribute.HotelAPIkeyToken,
#         'Status':Status,
#         'SessionOrganizationID':SessionOrganizationID,
#         'CYear':range(CYear,2020,-1),'CMonth':CMonth,
#         'month_no':month_no,
#         'month_name':month_name,
#        'year':year,
#     }
    
#     return render(request, 'InterviewAssessment/InterviewAssessmentList.html', context)



# def InterviewAssessmentList(request):
#     from HumanResources.views import DepartmentofEmployee
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
    
#     # Year and Month Setup
#     from datetime import datetime
#     import calendar
    
#     year = request.GET.get('year')
#     if year:
#         year = int(year)
#     else:
#         year = datetime.now().year

#     month_no = request.GET.get('month_no')
#     if month_no and month_no != 'All':
#         month_no = int(month_no)
#     else:
#         month_no = None  # No specific month filter if "All" is selected

#     month_name = "All Months" if not month_no else calendar.month_name[month_no]

#     today = datetime.today()
#     CYear = today.year
#     CMonth = today.month

#     OrganizationID = request.session.get("OrganizationID")
#     SessionOrganizationID = int(OrganizationID)
#     EmployeeCode = request.session.get("EmployeeCode")
#     Department = None

#     if EmployeeCode:
#         Departmentobj = DepartmentofEmployee(request, OrganizationID, EmployeeCode)
#         if Departmentobj:
#             Department = Departmentobj['work_Department']
#     UserType = str(request.session.get("UserType", '')).lower()
#     if OrganizationID == '3' and UserType == 'hod':
#         UserType = 'rd'

#     orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1)
#     Levels = LavelAdd.objects.filter(IsDelete=False)

#     I = request.GET.get('I', OrganizationID)
#     Level = request.GET.get('Level') or 'All'
#     Status = request.GET.get('Status') or 'All'

#     # Build Assessments Filter
#     assessments_filter = {
#         'IsDelete': False,
#         'OrganizationID': I,
#         'InterviewDate__year': year,
#     }
#     if month_no:  # Only add this filter if a specific month is selected
#         assessments_filter['InterviewDate__month'] = month_no

#     if Level != 'All':
#         assessments_filter['Level'] = Level
#     if Status != 'All':
#         assessments_filter['LastApporvalStatus'] = Status

#     if Department is not None:
#         if UserType == 'rd':
#             assessments_filter['Department'] = Department
#         if UserType == 'hod' and Department != 'Human Resources':
#             assessments_filter['Department'] = Department
    
    
#     Assessments = Assessment_Master.objects.filter(**assessments_filter).order_by('-id')


#     for Assessment in Assessments:
        

#         ref = 'Fresher'
#         if Assessment.workexperience != 'Fresher': 
#             ref = 0
#             if Assessment.reference:
#                 refobj = ReferenceDetails.objects.filter(IsDelete=False, OrganizationID=OrganizationID, Inteview_AssementID=Assessment.id).first()
#                 if refobj and refobj.ref1_status == 1:
#                     ref = 1
#         Assessment.ref = ref

#     AssessmentsList = [
#         a for a in Assessments 
#         if (Department != 'Human Resources' and Levelorder(a.Level, a.Department, a, UserType)) or Department == 'Human Resources'
#     ]
    
#     context = {
#         'Assessments': AssessmentsList,
#         'orgs': orgs,
#         'I': I,
#         'Levels': Levels,
#         'Level': Level,
#         'hotelapitoken': MasterAttribute.HotelAPIkeyToken,
#         'Status': Status,
#         'SessionOrganizationID': SessionOrganizationID,
#         'CYear': list(range(CYear, 2020, -1)),
#         'CMonth': CMonth,
#         'month_no': month_no if month_no else "All",
#         'month_name': month_name,
#         'year': year,
#     }

#     return render(request, 'InterviewAssessment/InterviewAssessmentList.html', context)

def CheckHeadDepartment(Department, Level, OrganizationID):
    def get_department_level_details(dept, level, org_id):
        dept_level = DepartmentLevelConfig.objects.filter(
            Department=dept,
            Level__icontains=f"'{level}'",
            OrganizationID=org_id,
            IsDelete=False
        ).first()
        return dept_level

    deptLevel = get_department_level_details(Department, Level, OrganizationID)
    
    if not deptLevel:
        deptLevel = get_department_level_details(Department, Level, 3)
    
    if not deptLevel:
        deptLevel = get_department_level_details("All", Level, 3)

    return '' if not deptLevel else deptLevel


# def InterviewAssessmentList(request):
#     from HumanResources.views import DepartmentofEmployee
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
    
#     from datetime import datetime
#     import calendar
    
#     year = request.GET.get('year')
#     if year:
#         year = int(year)
#     else:
#         year = datetime.now().year

#     month_no = request.GET.get('month_no')
#     if month_no and month_no != 'All':
#         month_no = int(month_no)
#     else:
#         month_no = None  

#     month_name = "All Months" if not month_no else calendar.month_name[month_no]

#     today = datetime.today()
#     CYear = today.year
#     CMonth = today.month

#     OrganizationID = request.session.get("OrganizationID")
#     SessionOrganizationID = int(OrganizationID)
#     EmployeeCode = request.session.get("EmployeeCode")
    
#     Department = None
#     if EmployeeCode:
#         Departmentobj = DepartmentofEmployee(request, OrganizationID, EmployeeCode)
#         print("Found ",Departmentobj['work_Department'])
#         if Departmentobj:
#             Department = Departmentobj['work_Department']
            
#         else:
#             return Error(request, "Employee Details not Found.Update in Human Resources")    
#     else:
#         return Error(request, "Employee Code is required. Please update it in User Details.")
                 


#     UserType = str(request.session.get("UserType", '')).lower()
#     if OrganizationID == '3' and UserType == 'hod':
#         UserType = 'rd'

#     orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1)
#     Levels = LavelAdd.objects.filter(IsDelete=False)

#     I = request.GET.get('I',OrganizationID)
#     if OrganizationID == "3":
#         I = request.GET.get('I') or 'All'
     
        
#     Level = request.GET.get('Level') or 'All'
#     Status = request.GET.get('Status') or 'All'
#     LOIstatus = request.GET.get('LOIstatus') or 'All'


#     assessments_filter = {
#     'IsDelete': False,
   
#     'InterviewDate__year': year,
#         }

#     if month_no:  
#         assessments_filter['InterviewDate__month'] = month_no
    
#     if I != 'All':
#         assessments_filter['OrganizationID'] = I
#     if Level != 'All':  
#         assessments_filter['Level'] = Level
#     if Status != 'All':
#         assessments_filter['LastApporvalStatus'] = Status
#     if Status == 'All':
#         STATUS_CHOICES = ['Approved', 'Pending']
#         assessments_filter['LastApporvalStatus__in'] = STATUS_CHOICES
 
        
#     if LOIstatus != 'All':
#         assessments_filter['LOIStatus'] = LOIstatus
    

#     Assessments = Assessment_Master.objects.filter(**assessments_filter).order_by('-CreatedDateTime')

#     AssessmentsList = []
#     for Assessment in Assessments:
#         ref = 'Fresher'
#         if Assessment.workexperience != 'Fresher': 
#             ref = 0
#             if Assessment.reference:
#                 refobj = ReferenceDetails.objects.filter(IsDelete=False, OrganizationID=OrganizationID, Inteview_AssementID=Assessment.id).first()
#                 if refobj and refobj.ref1_status == 1:
#                     ref = 1
#                 if isinstance(Assessment.reference, str):
#                     ref = 1   
#         Assessment.ref = ref
#         AssessmentDepartment = Assessment.Department
#         head_department_obj = CheckHeadDepartment(AssessmentDepartment,Assessment.Level, OrganizationID)
#         head_department = ''
#         if  head_department_obj:
#             # return Error(request, f"{AssessmentDepartment} head department not Found.Update in Admin of Interview Assessment")    
#             head_department =  head_department_obj.HeadDepartment
       
       
#         ApprovalStageFunobj = ApprovalStageFun(Assessment.Level,Assessment.Department,Assessment.OrganizationID)
#         Found = False
#         if not ApprovalStageFunobj:
#             if((Department == 'Human Resources' or Department == "Executive Office" or Department == "Talent Acquisition and Development" or Department == "Corporate Office")):
#                 Found=True
#             else:     
#                 Found=False
  
       
        
#         if (Department == 'Human Resources' or Department == "Executive Office" or Department == "Talent Acquisition and Development" or Department == "Corporate Office"):
#             Found=True
#         else:
#             if UserType.lower() in [item.lower() for item in ApprovalStageFunobj]:
#                 Found = True


#         if UserType != "ceo":
#             if (Found == True) and (Department == 'Human Resources' or Department == "Executive Office" or Department == "Talent Acquisition and Development" or  Department == "Corporate Office"):
#                     AssessmentsList.append(Assessment)
#             elif (Department.strip() == AssessmentDepartment.strip() or Department.strip() == head_department.strip()) and   Found == True:
#                     AssessmentsList.append(Assessment)
        
#         elif  Found == True:
#               AssessmentsList.append(Assessment)
                        
    
#     context = {
#         'Assessments': AssessmentsList,
#         'orgs': orgs,
#         'I': I,
#         'Levels': Levels,
#         'Level': Level,
#         'hotelapitoken': MasterAttribute.HotelAPIkeyToken,
#         'Status': Status,
#         'LOIstatus':LOIstatus,
#         'SessionOrganizationID': SessionOrganizationID,
#         'CYear': list(range(CYear, 2020, -1)),
#         'CMonth': CMonth,
#         'month_no': month_no if month_no else "All",
#         'month_name': month_name,
#         'year': year,
#     }

#     return render(request, 'InterviewAssessment/InterviewAssessmentList.html', context) 





# def InterviewAssessmentList(request):
#     from HumanResources.views import MultipleDepartmentofEmployee
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
    
#     from datetime import datetime
#     import calendar
    
#     year = request.GET.get('year')
#     if year:
#         year = int(year)
#     else:
#         year = datetime.now().year

#     month_no = request.GET.get('month_no')
#     if month_no and month_no != 'All':
#         month_no = int(month_no)
#     else:
#         month_no = None  

#     month_name = "All Months" if not month_no else calendar.month_name[month_no]

#     today = datetime.today()
#     CYear = today.year
#     CMonth = today.month

#     OrganizationID = request.session.get("OrganizationID")
#     SessionOrganizationID = int(OrganizationID)
#     EmployeeCode = request.session.get("EmployeeCode")
#     DepartmentList = []
#     if EmployeeCode:
#         print("EmployeeCode 1-",EmployeeCode)
#         Departmentobj = MultipleDepartmentofEmployee(OrganizationID, EmployeeCode)

#         if Departmentobj:  
#             DepartmentList = Departmentobj
            

#         else:
#             return Error(request, "Employee Details not Found.Update in Human Resources")    
#     else:
#         return Error(request, "Employee Code is required. Please update it in User Details.")
                 


#     UserType = str(request.session.get("UserType", '')).lower()
#     if OrganizationID == '3' and UserType == 'hod':
#         UserType = 'rd'

#     orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1)
#     Levels = LavelAdd.objects.filter(IsDelete=False)

#     I = request.GET.get('I',OrganizationID)
#     if OrganizationID == "3":
#         I = request.GET.get('I') or 'All'
     
        
#     Level = request.GET.get('Level') or 'All'
#     Status = request.GET.get('Status') or 'All'

#     assessments_filter = {
#         'IsDelete': False,
     
#         'InterviewDate__year': year,
#     }
#     if month_no:  
#         assessments_filter['InterviewDate__month'] = month_no
    
#     if I != 'All':
#         assessments_filter['OrganizationID'] = I
#     if Level != 'All':  
#         assessments_filter['Level'] = Level
#     if Status != 'All':
#         assessments_filter['LastApporvalStatus'] = Status

#     Assessments = Assessment_Master.objects.filter(**assessments_filter).order_by('-CreatedDateTime')

#     AssessmentsList = []
#     for Assessment in Assessments:
#         ref = 'Fresher'
#         if Assessment.workexperience != 'Fresher': 
#             ref = 0
#             if Assessment.reference:
#                 refobj = ReferenceDetails.objects.filter(IsDelete=False, OrganizationID=OrganizationID, Inteview_AssementID=Assessment.id).first()
#                 if refobj and refobj.ref1_status == 1:
#                     ref = 1
#         Assessment.ref = ref
#         AssessmentDepartment = Assessment.Department
#         head_department_obj = CheckHeadDepartment(AssessmentDepartment,Assessment.Level, OrganizationID)
#         if not  head_department_obj:
#             return Error(request, f"{AssessmentDepartment} head department not Found.Update in Admin of Interview Assessment")    
#         head_department =  head_department_obj.HeadDepartment
#         ApprovalStageFunobj = ApprovalStageFun(Assessment.Level,Assessment.Department,Assessment.OrganizationID)
#         if not ApprovalStageFunobj:
#             return Error(request, "Approval Stage is not found.")
  
       
#         Found = False
#         if ('Human Resources' in DepartmentList  or  "Executive Office" in DepartmentList or   "Talent Acquisition and Development" in DepartmentList or   "Corporate Office" in DepartmentList):
#             Found=True
#         else:
#             if UserType.lower() in [item.lower() for item in ApprovalStageFunobj]:
#                 Found = True


#         if UserType != "ceo":
#             if (Found == True) and ('Human Resources' in DepartmentList  or  "Executive Office" in DepartmentList or   "Talent Acquisition and Development" in DepartmentList or   "Corporate Office" in DepartmentList):
#                     AssessmentsList.append(Assessment)
#             elif ( AssessmentDepartment.strip() in DepartmentList or  head_department.strip()) in DepartmentList and   Found == True:
#                     AssessmentsList.append(Assessment)
        
#         elif  Found == True:
#               AssessmentsList.append(Assessment)
                        
    
#     context = {
#         'Assessments': AssessmentsList,
#         'orgs': orgs,
#         'I': I,
#         'Levels': Levels,
#         'Level': Level,
#         'hotelapitoken': MasterAttribute.HotelAPIkeyToken,
#         'Status': Status,
#         'SessionOrganizationID': SessionOrganizationID,
#         'CYear': list(range(CYear, 2020, -1)),
#         'CMonth': CMonth,
#         'month_no': month_no if month_no else "All",
#         'month_name': month_name,
#         'year': year,
#     }

#     return render(request, 'InterviewAssessment/InterviewAssessmentList.html', context) 







# def InterviewAssessmentList(request):
#     from HumanResources.views import MultipleDepartmentofEmployee
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
    
#     from datetime import datetime
#     import calendar
    
#     year = request.GET.get('year')
#     if year:
#         year = int(year)
#     else:
#         year = datetime.now().year

#     month_no = request.GET.get('month_no')
#     if month_no and month_no != 'All':
#         month_no = int(month_no)
#     else:
#         month_no = None  

#     month_name = "All Months" if not month_no else calendar.month_name[month_no]

#     today = datetime.today()
#     CYear = today.year
#     CMonth = today.month

#     OrganizationID = request.session.get("OrganizationID")
#     SessionOrganizationID = int(OrganizationID)
#     EmployeeCode = request.session.get("EmployeeCode")
    
#     DepartmentList = []
#     if EmployeeCode:

#         Departmentobj = MultipleDepartmentofEmployee(OrganizationID, EmployeeCode)

#         if Departmentobj:  
#             DepartmentList = Departmentobj
#             print("DepartmentList=",DepartmentList)
            

#         else:
#             return Error(request, "Employee Details not Found.Update in Human Resources")    
#     else:
#         return Error(request, "Employee Code is required. Please update it in User Details.")
                 


#     UserType = str(request.session.get("UserType", '')).lower()
#     if OrganizationID == '3' and UserType == 'hod':
#         UserType = 'rd'

#     orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1)
#     Levels = LavelAdd.objects.filter(IsDelete=False)

#     I = request.GET.get('I',OrganizationID)
#     if OrganizationID == "3":
#         I = request.GET.get('I') or 'All'
     
        
#     Level = request.GET.get('Level') or 'All'
#     Status = request.GET.get('Status') or 'All'
#     LOIstatus = request.GET.get('LOIstatus') or 'All'


#     assessments_filter = {
#     'IsDelete': False,
   
#     'InterviewDate__year': year,
#         }

#     if month_no:  
#         assessments_filter['InterviewDate__month'] = month_no
    
#     if I != 'All':
#         assessments_filter['OrganizationID'] = I
#     if Level != 'All':  
#         assessments_filter['Level'] = Level
#     if Status != 'All':
#         assessments_filter['LastApporvalStatus'] = Status
#     if Status == 'All':
#         STATUS_CHOICES = ['Approved', 'Pending']
#         assessments_filter['LastApporvalStatus__in'] = STATUS_CHOICES
 
        
#     if LOIstatus != 'All':
#         assessments_filter['LOIStatus'] = LOIstatus
    

#     Assessments = Assessment_Master.objects.filter(**assessments_filter).order_by('-CreatedDateTime')

#     AssessmentsList = []
#     for Assessment in Assessments:
#         ref = 'Fresher'
#         if Assessment.workexperience != 'Fresher': 
#             ref = 0
#             if Assessment.reference:
#                 refobj = ReferenceDetails.objects.filter(IsDelete=False, OrganizationID=OrganizationID, Inteview_AssementID=Assessment.id).first()
#                 if refobj and refobj.ref1_status == 1:
#                     ref = 1
#                 if isinstance(Assessment.reference, str):
#                     ref = 1   
#         Assessment.ref = ref
#         AssessmentDepartment = Assessment.Department
#         head_department_obj = CheckHeadDepartment(AssessmentDepartment,Assessment.Level, OrganizationID)
#         head_department = ''
#         if  head_department_obj:
#             # return Error(request, f"{AssessmentDepartment} head department not Found.Update in Admin of Interview Assessment")    
#             head_department =  head_department_obj.HeadDepartment
       
       
#         ApprovalStageFunobj = ApprovalStageFun(Assessment.Level,Assessment.Department,Assessment.OrganizationID)
       
#         Found = False
#         if not ApprovalStageFunobj:
#             # if((Department == 'Human Resources' or Department == "Executive Office" or Department == "Talent Acquisition and Development" or Department == "Corporate Office")):
#             if ('Human Resources' in DepartmentList  or  "Executive Office" in DepartmentList or   "Talent Acquisition and Development" in DepartmentList or   "Corporate Office" in DepartmentList):
#                 Found=True
#             else:     
#                 Found=False
        
       
        
#         # if (Department == 'Human Resources' or Department == "Executive Office" or Department == "Talent Acquisition and Development" or Department == "Corporate Office"):
#         if 'Human Resources' in DepartmentList  or  "Executive Office" in DepartmentList or   "Talent Acquisition and Development" in DepartmentList or   "Corporate Office" in DepartmentList:
#             Found=True
#         else:
#             if UserType.lower() in [item.lower() for item in ApprovalStageFunobj]:
#                 Found = True
       

#         if UserType != "ceo":
         
#             # if (Found == True) and (Department == 'Human Resources' or Department == "Executive Office" or Department == "Talent Acquisition and Development" or  Department == "Corporate Office"):
#             if (Found == True) and ('Human Resources' in DepartmentList  or  "Executive Office" in DepartmentList or   "Talent Acquisition and Development" in DepartmentList or   "Corporate Office" in DepartmentList):
#                     AssessmentsList.append(Assessment)
#             # elif (Department.strip() == AssessmentDepartment.strip() or Department.strip() == head_department.strip()) and   Found == True:
#             elif ( AssessmentDepartment.strip() in DepartmentList or  head_department.strip()) in DepartmentList and   Found == True:
            
#                     AssessmentsList.append(Assessment)
        
#         elif  Found == True:
#               AssessmentsList.append(Assessment)
                
    
#     context = {
#         'Assessments': AssessmentsList,
#         'orgs': orgs,
#         'I': I,
#         'Levels': Levels,
#         'Level': Level,
#         'hotelapitoken': MasterAttribute.HotelAPIkeyToken,
#         'Status': Status,
#         'LOIstatus':LOIstatus,
#         'SessionOrganizationID': SessionOrganizationID,
#         'CYear': list(range(CYear, 2020, -1)),
#         'CMonth': CMonth,
#         'month_no': month_no if month_no else "All",
#         'month_name': month_name,
#         'year': year,
#     }

#     return render(request, 'InterviewAssessment/InterviewAssessmentList.html', context) 






def InterviewAssessmentDelete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    INID = request.GET.get('INID')
    if INID is not None:
        INobj = Assessment_Master.objects.filter(id=INID,IsDelete=False).first()
        INobj.IsDelete = True
        INobj.ModifyBy = UserID
        INobj.save()
        messages.warning(request,"Deleted Successfully")
        return redirect('InterviewAssessmentList')





def InterviewAssementCandidateDetails(request):
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    token = request.headers.get('hotel-api-token')
    
    if token != hotelapitoken:
        return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)

    OrganizationID = request.GET.get('OID')
    AID = request.GET.get('AID')

    if not OrganizationID or not AID:
        return JsonResponse({"error": "OrganizationID and EmployeeCode are required parameters"}, status=status.HTTP_400_BAD_REQUEST)
    
    CandidateDetails_obj = Assessment_Master.objects.filter(OrganizationID = OrganizationID,IsDelete = False,id=AID).first()
    CandidateDetails = {
        'Name':CandidateDetails_obj.Name,
        'Department':CandidateDetails_obj.Department
    }
    return JsonResponse(CandidateDetails, safe=False)








def UpdateLOIStatus(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
    if request.method == "GET":
        AID = request.GET.get('AID')
        Status = request.GET.get('Status')
        
        if not AID or not Status:
            response_data = {
                'message': 'Invalid parameters'
            }
            return JsonResponse(response_data, status=400)
        
        obj = Assessment_Master.objects.filter(id=AID,OrganizationID=OrganizationID).first()
        
        if obj is None:
            response_data = {
                'message': 'Object not found'
            }
            return JsonResponse(response_data, status=404)
        
        obj.LOIStatus = Status
        obj.ModifyBy = UserID
        obj.save()

        response_data = {
            'message': f'Status {Status} updated successfully'
        }
        return JsonResponse(response_data, status=200)




def ResignationStatus(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
    if request.method == "GET":
        AID = request.GET.get('AID')
        Status = request.GET.get('Status')
        
        if not AID or not Status:
            response_data = {
                'message': 'Invalid parameters'
            }
            return JsonResponse(response_data, status=400)
        
        obj = Assessment_Master.objects.filter(id=AID,OrganizationID=OrganizationID).first()
        
        if obj is None:
            response_data = {
                'message': 'Object not found'
            }
            return JsonResponse(response_data, status=404)
        
        obj.ResignationStatus = Status
        obj.ModifyBy = UserID
        obj.save()

        response_data = {
            'message': f'Status {Status} updated successfully'
        }
        return JsonResponse(response_data, status=200)



def UserTypeList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    userobjs = UserTypeFlow.objects.filter(IsDelete=False)
    context = {'userobjs':userobjs}
    return render(request,"InterviewAssessment/Admin/UserTypeList.html",context)


def UserTypeAddEdit(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session.get("OrganizationID")
    UserID = str(request.session.get("UserID"))
    UID = request.POST.get('UID') or request.GET.get('UID')

    if request.method == "POST":
        UserType = request.POST['UserType']
        if UID:  
            Uobj = UserTypeFlow.objects.filter(id=UID, IsDelete=False).first()
            if Uobj:
                Uobj.UserType = UserType
                Uobj.ModifyBy = UserID
                Uobj.save()
                messages.success(request, "User Type updated successfully")
            else:
                messages.error(request, "Invalid User Type ID.")
        else:
            UserTypeFlow.objects.create(UserType=UserType, OrganizationID=OrganizationID, CreatedBy=UserID)
            messages.success(request, "User Type created successfully")
        
        return redirect('UserTypeList')
    
    if UID:
        Uobj = UserTypeFlow.objects.filter(id=UID, IsDelete=False).first()
        if Uobj:
            return JsonResponse({'UserType': Uobj.UserType})
        else:
            return JsonResponse({'error': 'Invalid User Type ID.'}, status=400)
    
    return redirect('UserTypeList')


    



def UserTypeDelete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    UID = request.GET.get('UID')
    if UID is not None:
        Uobj = UserTypeFlow.objects.filter(id=UID,IsDelete=False).first()
        Uobj.IsDelete = True
        Uobj.ModifyBy = UserID
        Uobj.save()
        messages.warning(request,"Deleted Successfully")
        return redirect('UserTypeList')

from urllib.parse import unquote

def DepartmentLevelConfigList(request):
    # Ensure OrganizationID is in the session
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    Levels = LavelAdd.objects.filter(IsDelete=False)
    Departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    
    Department = unquote(request.GET.get('departmentSelect', 'All'))
    organizationSelect = request.GET.get('organizationSelect', OrganizationID)
    
    if Department != 'All':
        configs = DepartmentLevelConfig.objects.filter(IsDelete=False, Department=Department, OrganizationID=organizationSelect)
    else:
        configs = DepartmentLevelConfig.objects.filter(IsDelete=False, OrganizationID=organizationSelect)
    
    for config in configs:
        config.Found = DepartmentLevelConfigDetails.objects.filter(
            IsDelete=False,
            DepartmentLevelConfig=config
        ).exists()  
    


             

    orgs  = OrganizationList(OrganizationID)
    
    context = {'configs':configs,
               'Departments':Departments,
               'Department':Department,
               'Levels':Levels,
               'orgs':orgs,
               'organizationSelect':organizationSelect
               }
    return render(request,"InterviewAssessment/Admin/DepartmentLevelConfigList.html",context)





from urllib.parse import quote
def DepartmentLevelConfigAddEdit(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    DID = request.POST.get('DID') or request.GET.get('DID')

    if request.method == "POST":
        Department = request.POST['Department']
        HeadDepartment = request.POST['HeadDepartment']

        Level = request.POST.getlist('Level[]')
        OrganizationID = request.POST.get('I')  # Added to capture organization selection from form

        if DID:  # Update existing configuration
            Dobj = DepartmentLevelConfig.objects.filter(id=DID, IsDelete=False).first()
            if Dobj:
                Dobj.Department = Department
                Dobj.HeadDepartment = HeadDepartment

                Dobj.Level = Level
                Dobj.OrganizationID = OrganizationID
                Dobj.ModifyBy = UserID
                Dobj.ModifyDateTime = timezone.now()
                Dobj.save()
                messages.success(request, "Department Level Configuration updated successfully")
            else:
                messages.error(request, "Invalid Department Level Configuration ID.")
        else:  # Create new configuration
            DepartmentLevelConfig.objects.create(
                Department=Department,
                HeadDepartment = HeadDepartment,
                Level=Level,
                OrganizationID=OrganizationID,
                CreatedBy=UserID
            )
            messages.success(request, "Department Level Configuration created successfully")
        url = reverse('DepartmentLevelConfigList')
       
        redirect_url = f'{url}?departmentSelect={quote(Department)}&organizationSelect={OrganizationID}'
      
       
        return redirect(redirect_url)
       
    if DID:  # Fetch data for editing
        Dobj = DepartmentLevelConfig.objects.filter(id=DID, IsDelete=False).first()
        if Dobj:
            return JsonResponse({
                'Department': Dobj.Department,
                'HeadDepartment': Dobj.HeadDepartment,

                'Level': Dobj.Level,
                'OrganizationID': Dobj.OrganizationID,  # Send OrganizationID back to the modal
            })
        else:
            return JsonResponse({'error': 'Invalid Department Level Configuration ID.'}, status=400)

    return redirect('DepartmentLevelConfigList')

def DepartmentLevelConfigDelete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    DID = request.GET.get('DID')
    
    if DID is not None:
        Dobj = DepartmentLevelConfig.objects.filter(id=DID, IsDelete=False).first()
        if Dobj:
            Dobj.IsDelete = True
            Dobj.ModifyBy = UserID
            Dobj.save()

            related_details = DepartmentLevelConfigDetails.objects.filter(
                DepartmentLevelConfig=Dobj, IsDelete=False
            )
            for detail in related_details:
                detail.IsDelete = True
                detail.ModifyBy = UserID
                detail.save()

            messages.warning(request, "Deleted Successfully")
            url = reverse('DepartmentLevelConfigList')
            redirect_url = f'{url}?organizationSelect={Dobj.OrganizationID}'
            return redirect(redirect_url)




def DepartmentLevelConfigDetailsList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    configDetails =DepartmentLevelConfigDetails.objects.filter(IsDelete=False)
    context = {'configDetails':configDetails}
    return render(request,"InterviewAssessment/Admin/DepartmentLevelConfigDetailsList.html",context)



def DepartmentLevelConfigDetailsAdd(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    
    UserID = str(request.session["UserID"])
    DID = request.GET.get('DID')
    OrganizationID = request.GET.get('OID')

    usertypes = UserTypeFlow.objects.filter(IsDelete=False)
    deptLevel = None
    details = []

    if DID is not None:
        deptLevel = DepartmentLevelConfig.objects.filter(id=DID, IsDelete=False).first()
       
        details = list(DepartmentLevelConfigDetails.objects.filter(
        DepartmentLevelConfig_id=DID, IsDelete=False
        ).order_by('LevelSortOrder').values('id', 'LevelSortOrder', 'UserType'))

    if request.method == "POST":
        ids = request.POST.getlist('id[]')
        levelSortOrders = request.POST.getlist('levelSortOrder[]')
        userTypes = request.POST.getlist('userType[]')

       
        existing_ids = set([str(detail['id']) for detail in details])
        submitted_ids = set(ids)

      
        removed_ids = existing_ids - submitted_ids

      
        for removed_id in removed_ids:
            DepartmentLevelConfigDetails.objects.filter(id=removed_id).update(IsDelete=True)

    
        for i, (detail_id, sortOrder, userType) in enumerate(zip(ids, levelSortOrders, userTypes)):
            if detail_id: 
                detail = DepartmentLevelConfigDetails.objects.get(id=detail_id)
                detail.LevelSortOrder = sortOrder
                detail.UserType = userType
                detail.ModifyBy = UserID
                detail.ModifyDateTime = timezone.now()
                detail.save()
            else: 
                DepartmentLevelConfigDetails.objects.create(
                    DepartmentLevelConfig=deptLevel,
                    LevelSortOrder=sortOrder,
                    UserType=userType,
                    OrganizationID=OrganizationID,
                    CreatedBy=UserID,
                    ModifyBy=UserID,
                    CreatedDateTime=timezone.now(),
                    ModifyDateTime=timezone.now(),
                    IsDelete=False
                )
        url = reverse('DepartmentLevelConfigList')
        redirect_url = f'{url}?departmentSelect={quote(deptLevel.Department)}&organizationSelect={deptLevel.OrganizationID}'

       
        return redirect(redirect_url)

    context = {
        'deptLevel': deptLevel,
        'usertypes': usertypes,
        'details': details
    }
    return render(request, "InterviewAssessment/Admin/DepartmentLevelConfigDetailsAdd.html", context)






def FactorList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    Fobjs =Factors.objects.filter(IsDelete=False)
    context = {'Fobjs':Fobjs}
    return render(request,"InterviewAssessment/Admin/FactorList.html",context)



def FactorsAdd(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    FID = request.POST.get('FID') or request.GET.get('FID')

    if request.method == "POST":
        Title = request.POST.get('Title')
        Description = request.POST.get('Description')  # Corrected typo
        Item = request.POST.get('Item')
        
        try:
            # Parse the JSON data
            Item = json.loads(Item)
        except json.JSONDecodeError:
            # Handle JSON parsing error
            messages.error(request, "Invalid JSON format for Item.")
            return redirect('FactorList')
        
        if FID:  
            Fobj = Factors.objects.filter(id=FID, IsDelete=False).first()
            Fobj.Title = Title
            Fobj.Decription = Description
            Fobj.Item = Item
            Fobj.ModifyBy = UserID 
            Fobj.save()
            messages.success(request, "Factor updated successfully")
        else:
            Factors.objects.create(
                Title=Title,
                Description=Description,
                Item=Item
            )
            messages.success(request, "Factor created successfully")
        
        return redirect('FactorList')
    
    if FID:
        Fobj = Factors.objects.filter(id=FID, IsDelete=False).first()
        return JsonResponse({
                'Title': Fobj.Title,
                'Description': Fobj.Description,
                'Item': Fobj.Item
        })
    
    return redirect('FactorList')



def FactorDelete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    FID = request.GET.get('FID')
    if FID is not None:
        Fobj = Factors.objects.filter(id=FID,IsDelete=False).first()
        Fobj.IsDelete = True
        Fobj.ModifyBy = UserID
        Fobj.save()
        messages.warning(request,"Deleted Successfully")
        return redirect('FactorList')




def LevelWiseGrid(request):
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    token = request.headers.get('hotel-api-token')
    
    if token != hotelapitoken:
        return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)

    Level = request.GET.get('Level')
    raw_department = request.GET.get('Department')
    OrganizationID = request.GET.get('OrganizationID')
    
    Department = unquote(raw_department)
 

    if not (Level and Department and OrganizationID):
        return JsonResponse({"error": "Level, Department, and OrganizationID are required parameters"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_department_level_details(dept, level, org_id):
        dept_level = DepartmentLevelConfig.objects.filter(
            Department=dept,
          Level__icontains=f"'{level}'",
            OrganizationID=org_id,
            IsDelete=False
        ).first()
        
        if dept_level:
            obj = DepartmentLevelConfigDetails.objects.filter(
                IsDelete=False,
                DepartmentLevelConfig=dept_level
            ).order_by('LevelSortOrder').values('LevelSortOrder', 'UserType')
            
            if obj.exists():
                return obj, dept_level

        return None, None

    obj, deptLevel = get_department_level_details(Department, Level, OrganizationID)

    if not obj:
        obj, deptLevel = get_department_level_details(Department, Level, 3)
     
    
    if not obj:
        obj, deptLevel = get_department_level_details("All", Level, 3)
      
    
    if not obj:
        return JsonResponse([], safe=False)

    LevelFlow = [
        {
            'LevelSortOrder': o['LevelSortOrder'],
            'UserType': o['UserType']
        }
        for o in obj
    ]

    return JsonResponse(LevelFlow, safe=False)


def GenerateDataLink(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    IND = request.GET.get('IND')
    OrganizationID = request.session.get("OrganizationID")
    UserID = str(request.session.get("UserID"))

    obj = EmployeeDataRequest_Master.objects.create(
        InterviewID=IND,
        OrganizationID=OrganizationID,
        TokenKey=str(uuid.uuid4()),
        ExpiryDate=datetime.date.today() + timedelta(5),
        CreatedBy=UserID,
       
    )
    assobj  = Assessment_Master.objects.filter(id=IND,IsDelete=False).first()
    assobj.GenerateLink = True
    assobj.save()
    
    context = {
        'obj': obj
    }
    return render(request, 'InterviewAssessment/GenerateDataLink.html', context)




def ReGenerateDataLink(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    IND = request.GET.get('IND')
    OrganizationID = request.session.get("OrganizationID")
    UserID = str(request.session.get("UserID"))

    obj = EmployeeDataRequest_Master.objects.filter(
        InterviewID=IND).first()
    obj.OrganizationID=OrganizationID
    ExpiryDate = datetime.date.today() + timedelta(5)
    obj.ExpiryDate = ExpiryDate
    obj.ModifyBy = UserID
    obj.LastStatusUpdateBy = UserID
    obj.LastStatusUpdateOn = datetime.date.today()
    obj.save()

    assobj  = Assessment_Master.objects.filter(IsDelete=False,id=IND).first()
    assobj.IsEmpDataReceived  = False
    assobj.save()
    
    context = {
        'obj': obj
    }
    return render(request, 'InterviewAssessment/GenerateDataLink.html', context)



from .models import EmployeePersonalData,EmployeeFamilyData,EmployeeEmergencyInfoData,EmployeeChildData,EmployeeEducationData,EmployeePreviousWorkData,EmployeeDocumentsInfoData,EmployeeAddressInfoData,EmployeeIdentityInfoData,EmployeeBankInfoData






from .models import CandidateUrlMaster
from django.urls import reverse
def ActiveLink(EMPID,return_dict=False):
   
    Links = {
        'EMPIDActive': False,
        'FamilyIDActive': False,
        'EmergencyIDActive': False,
        'EducationsIDActive': False,
        'PreviousworkIDActive': False,
        'DocumentIDActive': False,
        'AddressIDActive': False,
        'IdentityIDActive': False,
        'BankIDActive': False
    }

   

    
    if EMPID is not None:
            Links['EMPIDActive'] = True    

            Emergencyobj = EmployeeEmergencyInfoData.objects.filter(MasterID=EMPID, IsDelete=False).first()
            if Emergencyobj is not None:
                Links['EmergencyIDActive'] = True

            Finfoobj = EmployeeFamilyData.objects.filter(MasterID=EMPID, IsDelete=False).first()
            if Finfoobj is not None:
                Links['FamilyIDActive'] = True

            Educations = EmployeeEducationData.objects.filter(MasterID=EMPID, IsDelete=False)
            if Educations.exists():
                Links['EducationsIDActive'] = True

            previousworks = EmployeePreviousWorkData.objects.filter(MasterID=EMPID, IsDelete=False)
            if previousworks.exists():
                Links['PreviousworkIDActive'] = True

            Documents = EmployeeDocumentsInfoData.objects.filter(MasterID=EMPID, IsDelete=False)
            if Documents.exists():
                Links['DocumentIDActive'] = True

            Addressinfo = EmployeeAddressInfoData.objects.filter(MasterID=EMPID, IsDelete=False).first()
            if Addressinfo is not None:
                Links['AddressIDActive'] = True

            IdentityInfo = EmployeeIdentityInfoData.objects.filter(MasterID=EMPID, IsDelete=False).first()
            if IdentityInfo is not None:
                Links['IdentityIDActive'] = True

            Bankinfo = EmployeeBankInfoData.objects.filter(MasterID=EMPID, IsDelete=False).first()
            if Bankinfo is not None:
                Links['BankIDActive'] = True

    if return_dict:
        return Links

    



def CandidateDataForm(request):
    ID = request.GET.get('ID')
    Mobj  =  EmployeeDataRequest_Master.objects.filter(TokenKey = ID,IsDelete=False).first()
    InterviewID  = Mobj.InterviewID
    orgname =  OrganizationName(Mobj.OrganizationID)
    Logo =  OrganizationLogo(Mobj.OrganizationID)

  
    EMPID = None
    Emobj = None  
    ActiveLinkDict  = None
   
   
   

    if ID is not None:
        Emobj = EmployeePersonalData.objects.filter(DataMasterID=InterviewID,IsDelete=False).first()
        
        if Emobj:
            EMPID = Emobj.id
        ActiveLinkDict = ActiveLink(EMPID= EMPID, return_dict=True)
           
        
    
    if InterviewID:
        assobj  = Assessment_Master.objects.filter(id=InterviewID,IsDelete=False).first()
        Linkobj = EmployeeDataRequest_Master.objects.filter(InterviewID=InterviewID,IsDelete=False).first()
        ExpiryDate = Linkobj.ExpiryDate
        TodayDate = datetime.date.today()
                  
        if ExpiryDate <= TodayDate:
            
                case_type  = "link_expiry"
                return redirect('notification_page', case_type=case_type) 
        
        if assobj.IsEmpDataReceived  == True:
       
            case_type = "data_submitted"
            return redirect('notification_page', case_type=case_type)  


        
     
    CurrentUrl = 'CandidatePersonalData'
    urlobj  = CandidateUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    if urlobj:
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = CandidateUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
    if request.method == "POST":
                # Personal Information
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
             
                

                if Emobj  is not None:
                    Em = EmployeePersonalData.objects.filter(id=EMPID ,IsDelete=False).first()
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
                    Em.save()
                    if ProfileImage:
                        repalce_file(Em.id,"EmployeePersonalData")
                        upload_file(ProfileImage,Em.id,"ProfileImage","EmployeePersonalData")
                else:
                    
                   

                
                    Em = EmployeePersonalData.objects.create(DataMasterID= InterviewID,Prefix=Prefix,FirstName = FirstName,MiddleName = MiddleName,LastName = LastName,Gender = Gender,MaritalStatus = MaritalStatus,DateofBirth = DateofBirth,age = age,MobileNumber = MobileNumber,EmailAddress = EmailAddress)
                    assobj.EmpDataReceivedID = Em.id
                  

                    assobj.save()
                    if ProfileImage:

                        
                        upload_file(ProfileImage,Em.id,"ProfileImage","EmployeePersonalData")
                
                    EMPID = Em.id
                url = reverse(Nexturl)  
                redirect_url = f"{url}?EMPID={EMPID}" 
                return redirect(redirect_url)
   
  
    context= {'Emobj':Emobj,'EMPID':EMPID,'InterviewID':InterviewID,'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl,
              'OrganizationName':orgname,
              'Logo':Logo
              
              } 
    return render(request, 'InterviewAssessment/CandidateData/CandidatePersonalData.html', context)


def CandidatePersonalData(request):
    EMPID = request.GET.get('EMPID')
    ActiveLinkDict  = None

   
    InterviewID = request.GET.get('InterviewID')
    InterviewID = request.GET.get('InterviewID')

    Emobj = None  
    if EMPID is not None and EMPID.isdigit():
       
        EMPID = int(EMPID)
        Emobj = EmployeePersonalData.objects.filter(id=EMPID,IsDelete=False).first()
  
        ActiveLinkDict = ActiveLink(EMPID = EMPID, return_dict=True)
      
        assobj  = Assessment_Master.objects.filter(id=InterviewID,IsDelete=False).first()
        if InterviewID is None:
              assobj  = Assessment_Master.objects.filter(EmpDataReceivedID=EMPID,IsDelete=False).first()
              if assobj.IsEmpDataReceived == True:
                    case_type = "data_submitted"
                    return redirect('notification_page', case_type=case_type) 
      
        
    CurrentUrl = 'CandidatePersonalData'
    urlobj  = CandidateUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    if urlobj:
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = CandidateUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
    if request.method == "POST":
                # Personal Information
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
             
                

                if Emobj  is not None:
                    Em = EmployeePersonalData.objects.filter(id=EMPID,IsDelete=False ).first()
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
                    Em.save()
                    if ProfileImage:
                        repalce_file(Em.id,"EmployeePersonalData")
                        upload_file(ProfileImage,Em.id,"ProfileImage","EmployeePersonalData")
                else:
                    
                   

                
                    Em = EmployeePersonalData.objects.create(DataMasterID= InterviewID,Prefix=Prefix,FirstName = FirstName,MiddleName = MiddleName,LastName = LastName,Gender = Gender,MaritalStatus = MaritalStatus,DateofBirth = DateofBirth,age = age,MobileNumber = MobileNumber,EmailAddress = EmailAddress)
                    assobj.EmpDataReceivedID = Em.id
                    assobj.IsEmpDataReceived = True

                    assobj.save()
                    if ProfileImage:
                        
                        upload_file(ProfileImage,Em.id,"ProfileImage","EmployeePersonalData")
                

                url = reverse(Nexturl)  
                redirect_url = f"{url}?EMPID={EMPID}" 
                return redirect(redirect_url)
    
   
    
    

    context= {'Emobj':Emobj,'EMPID':EMPID,'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl} 
    return render(request, 'InterviewAssessment/CandidateData/CandidatePersonalData.html', context)


def CandidateFamilyinfoPage(request):
    ActiveLinkDict  = None

    
    EMPID = request.GET.get('EMPID')
    Emobj = None  
    Finfoobj  = None
    childs  = None 
    ActiveLinkDict = None

    if EMPID is not None and EMPID.isdigit():
       
        EMPID = int(EMPID)
        
        Emobj = EmployeePersonalData.objects.filter(id=EMPID,IsDelete=False).first()
        if Emobj:
             EMPID = Emobj.id
             ActiveLinkDict = ActiveLink(EMPID = EMPID, return_dict=True)
           
             Finfoobj =  EmployeeFamilyData.objects.filter(MasterID = EMPID,IsDelete=False).first()
             if Finfoobj is not None:
                    childs  =  EmployeeChildData.objects.filter(IsDelete=False,FamilyID = Finfoobj.id)
             assobj  = Assessment_Master.objects.filter(EmpDataReceivedID=EMPID,IsDelete=False).first()
             if assobj.IsEmpDataReceived == True:
                    case_type = "data_submitted"
                    return redirect('notification_page', case_type=case_type) 
         
       
    CurrentUrl = 'CandidateFamilyinfoPage'

    urlobj  = CandidateUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = CandidateUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = CandidateUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName


    if request.method == "POST":
                
               
                SpouseName = request.POST.get('SpouseName', None)
                SpouseAge = request.POST.get('SpouseAge', 0)
                if SpouseAge == '' :
                     SpouseAge = 0 
                SpouseDOB = request.POST.get('SpouseDOB', None)
                if SpouseDOB == '':
                        SpouseDOB = None 
                SpouseContactNo = request.POST.get('SpouseContact', None)


                MotherName = request.POST.get('MotherName', None)
                MotherAge = request.POST.get('MotherAge', 0)
                if MotherAge == '' :
                     MotherAge = 0 
                MotherDOB = request.POST.get('MotherDOB', None)
                if MotherDOB == '':
                        MotherDOB = None 
                MotherContactNo = request.POST.get('MotherContact', None)

                FatherName = request.POST.get('FatherName', None)
                FatherAge = request.POST.get('FatherAge', 0)
                if FatherAge == '' :
                     FatherAge = 0 
                FatherDOB = request.POST.get('FatherDOB', None)
                if FatherDOB == '':
                        FatherDOB = None 
                FatherContactNo = request.POST.get('FatherContact', None)
                
                            
                LandlineNo = request.POST.get('LandlineNo', None)

                child_update_ids  = request.POST.getlist('child_ids[]')
             
                child_names = request.POST.getlist('childName[]')
                child_ages = request.POST.getlist('childAge[]')
                child_relations = request.POST.getlist('childrelations[]')

                removed_child_ids_str = request.POST.get('removed_child_ids[]')
              
                if removed_child_ids_str:
                    removed_child_ids = list(map(int, removed_child_ids_str.split(',')))
                else:
                    removed_child_ids = []
               
                    
              
               
                if Finfoobj  is not None:
                    Finfoobj.SpouseName = SpouseName
                    Finfoobj.SpouseDateofBirth = SpouseDOB

                    Finfoobj.SpouseAge = SpouseAge
                    Finfoobj.SpouseContactNo  = SpouseContactNo
                    Finfoobj.MotherName  = MotherName

                    Finfoobj.MotherName  = MotherName
                    Finfoobj.MotherDateofBirth  = MotherDOB

                    Finfoobj.MotherAge  = MotherAge
                    Finfoobj.MotherContactNo = MotherContactNo

                    Finfoobj.FatherName = FatherName
                    Finfoobj.FatherDateofBirth  = FatherDOB

                    Finfoobj.FatherAge = FatherAge
                    Finfoobj.FatherContactNo = FatherContactNo
                    
                    Finfoobj.save()
                    if len(removed_child_ids) > 0:
                        for rid in removed_child_ids:
                          
                            rdelete = EmployeeChildData.objects.filter(id=rid).first()
                          
                            rdelete.IsDelete  = True
                            rdelete.save()
                    
                    for id, name, age, relation in zip(child_update_ids, child_names, child_ages, child_relations):
                            if id.startswith('new_'):
                                    
                                EmployeeChildData.objects.create(
                                    FamilyID=Finfoobj.id,
                                    Name=name,
                                    Age=age,
                                    Relation=relation
                                )
                            else:
                                
                                EmployeeChildData.objects.filter(FamilyID=Finfoobj.id, id=id).update(
                                    Name=name,
                                    Age=age,
                                    Relation=relation
                                )


                    
                else:
                    Finfo =  EmployeeFamilyData.objects.create(MasterID = EMPID,
                                                               SpouseName = SpouseName,
                                                               SpouseAge  = SpouseAge ,
                                                               SpouseDateofBirth = SpouseDOB,
                                                               SpouseContactNo = SpouseContactNo,
                                                               MotherName = MotherName,
                                                               MotherDateofBirth = MotherDOB,
                                                               MotherAge = MotherAge,

                                                               MotherContactNo = MotherContactNo,
                                                               FatherName = FatherName,
                                                               FatherAge  = FatherAge,
                                                               FatherDateofBirth = FatherDOB,
                                                               FatherContactNo = FatherContactNo,
                                                               LandlineNo  = LandlineNo
                                                               )
                    
                    if len(child_names) > 0:
                        for name, age, relation in zip(child_names, child_ages, child_relations):
                                cobj  = EmployeeChildData.objects.create(
                                    FamilyID = Finfo.id,
                                    Name = name,
                                    Age = age,
                                    Relation = relation,
                                )

                url = reverse(Nexturl)  
                redirect_url = f"{url}?EMPID={EMPID}" 
                return redirect(redirect_url)
    
    SpouseChild = True 
   
    if Emobj.MaritalStatus ==  'Unmarried':
         SpouseChild = False 

    context= {'SpouseChild':SpouseChild,'Emobj':Emobj,'EMPID':EMPID,'Finfoobj':Finfoobj,'childs':childs,'PreviousUrl':PreviousUrl,'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl} 
    return render(request, 'InterviewAssessment/CandidateData/CandidateFamilyinfoPage.html', context)



def CandidateEmergencyinfoPage(request):
    
    EMPID = request.GET.get('EMPID')

    Emobj = None
    Emergencyobj = None 
    ActiveLinkDict = None

    if EMPID is not None and EMPID.isdigit():
       
        EMPID = int(EMPID)
       
        Emobj = EmployeePersonalData.objects.filter(id=EMPID,IsDelete=False).first()
        if Emobj:
              ActiveLinkDict = ActiveLink(EMPID = EMPID, return_dict=True)
            
              Emergencyobj = EmployeeEmergencyInfoData.objects.filter(MasterID = EMPID,IsDelete=False).first()
              EMPID = Emobj.id
              assobj  = Assessment_Master.objects.filter(EmpDataReceivedID=EMPID,IsDelete=False).first()
              if assobj.IsEmpDataReceived == True:
                    case_type = "data_submitted"
                    return redirect('notification_page', case_type=case_type) 
      
       
    CurrentUrl = 'CandidateEmergencyinfoPage'

    urlobj  = CandidateUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = CandidateUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = CandidateUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName


    if request.method == "POST":
                EmergencyFirstName =  request.POST['EmergencyFirstName']
                EmergencyMiddleName =  request.POST['EmergencyMiddleName']
                EmergencyLastName =  request.POST['EmergencyLastName']
                Relation =  request.POST['Relation']
                EmergencyContactNumber_1 = request.POST['EmergencyContactNumber_1']
                EmergencyContactNumber_2 =  request.POST['EmergencyContactNumber_2']
                ProvidentFundNumber  = request.POST['ProvidentFundNumber']
                ESINumber =  request.POST['ESINumber']
                BloodGroup =  request.POST['BloodGroup']     
                if Emergencyobj  is not None:
                    Emergencyobj.FirstName  = EmergencyFirstName
                    Emergencyobj.MiddleName  = EmergencyMiddleName
                    Emergencyobj.LastName  = EmergencyLastName
                    Emergencyobj.Relation  = Relation
                    Emergencyobj.EmergencyContactNumber_1  = EmergencyContactNumber_1
                    Emergencyobj.EmergencyContactNumber_2 = EmergencyContactNumber_2
                    Emergencyobj.ProvidentFundNumber = ProvidentFundNumber 
                    Emergencyobj.ESINumber  = ESINumber
                    Emergencyobj.BloodGroup  = BloodGroup
                    Emergencyobj.save()
                else:
                
                        Emergency = EmployeeEmergencyInfoData.objects.create(
                                                        MasterID =  EMPID,
                                                        FirstName = EmergencyFirstName,
                                                        MiddleName = EmergencyMiddleName,
                                                        LastName = EmergencyLastName,
                                                        Relation  = Relation,
                                                        EmergencyContactNumber_1  = EmergencyContactNumber_1,
                                                        EmergencyContactNumber_2 = EmergencyContactNumber_2,
                                                        ProvidentFundNumber  = ProvidentFundNumber,
                                                        ESINumber  = ESINumber,
                                                        BloodGroup  = BloodGroup
                                                    )

                url = reverse(Nexturl)  
                redirect_url = f"{url}?EMPID={EMPID}" 
                return redirect(redirect_url)
    
   
    context= {'Emobj':Emobj,'EMPID':EMPID,  'Emergencyobj':Emergencyobj,'PreviousUrl':PreviousUrl,'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl} 
    return render(request, 'InterviewAssessment/CandidateData/CandidateEmergencyinfoPage.html', context)





def CandidateQualificationinfoPage(request):
    EMPID = request.GET.get('EMPID')
    Emobj = None
    Educations = None
    ActiveLinkDict = None

    if EMPID is not None and EMPID.isdigit():
        EMPID = int(EMPID)
        Emobj = EmployeePersonalData.objects.filter(id=EMPID, IsDelete=False).first()

        if Emobj:
            EMPID = Emobj.id
            ActiveLinkDict = ActiveLink(EMPID=EMPID, return_dict=True)
            Educations = EmployeeEducationData.objects.filter(MasterID=EMPID, IsDelete=False)
            assobj = Assessment_Master.objects.filter(EmpDataReceivedID=EMPID, IsDelete=False).first()
            
            if assobj and assobj.IsEmpDataReceived:
                case_type = "data_submitted"
                return redirect('notification_page', case_type=case_type)

    CurrentUrl = 'CandidateQualificationinfoPage'
    urlobj = CandidateUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl

    if urlobj:
        # Next Url
        next_obj = CandidateUrlMaster.objects.filter(sortorder=urlobj.sortorder + 1).first()
        if next_obj:
            Nexturl = next_obj.UrlName
        # Previous Url
        prev_obj = CandidateUrlMaster.objects.filter(sortorder=urlobj.sortorder - 1).first()
        if prev_obj:
            PreviousUrl = prev_obj.UrlName

    if request.method == "POST":
        EducationType = request.POST.getlist('EducationType[]')
        DegreeCourse = request.POST.getlist('DegreeCourse[]')
        InstitutionName = request.POST.getlist('InstitutionName[]')
        Year = request.POST.getlist('Year[]')
        AttachmentsFile = request.FILES.getlist('AttachmentEducation[]')
        FID = request.POST.getlist('FID[]')
        Edu_ids = request.POST.getlist('Edu_ids[]')
        removed_Edu_ids_str = request.POST.get('removed_Edu_ids[]', '')

        # Convert removed education IDs to a list of integers
        removed_Edu_ids = [
            int(value) for value in removed_Edu_ids_str.split(',') if value.isdigit()
        ] if removed_Edu_ids_str else []

        # Handle removals (mark records as deleted)
        if removed_Edu_ids:
            EmployeeEducationData.objects.filter(id__in=removed_Edu_ids).update(IsDelete=True)

        i = 1  # Index for dynamic files
        for id, education, degree, institution, year in zip(Edu_ids, EducationType, DegreeCourse, InstitutionName, Year):
            if id.startswith('new_'):
                # Add new record
                Educationobj = EmployeeEducationData.objects.create(
                    MasterID=EMPID,
                    EducationType=education,
                    Degree_Course=degree,
                    NameoftheInstitution=institution,
                    Year=year,
                )
                # Handle new file upload
                key = f'FID_new_{i}'
                if key in FID:
                    file_index = FID.index(key)
                    if file_index is not None:
                        file = AttachmentsFile[file_index]
                        if file:
                            upload_file(file, Educationobj.id, "Education", "EmployeeEducationData")
                i += 1
            else:
                # Update existing record
                Educationobj = EmployeeEducationData.objects.filter(
                    MasterID=EMPID, IsDelete=False, id=id
                ).first()
                if Educationobj:
                    Educationobj.EducationType = education
                    Educationobj.Degree_Course = degree
                    Educationobj.NameoftheInstitution = institution
                    Educationobj.Year = year
                    Educationobj.save()

                    # Handle file replacement
                    key = f'FID_{id}'
                    if key in FID:
                        file_index = FID.index(key)
                        if file_index is not None:
                            file = AttachmentsFile[file_index]
                            if file:
                                repalce_file(Educationobj.id, "EmployeeEducationData")
                                upload_file(file, Educationobj.id, "Education", "EmployeeEducationData")

        url = reverse(Nexturl)
        redirect_url = f"{url}?EMPID={EMPID}"
        return redirect(redirect_url)

    context = {
        'PreviousUrl': PreviousUrl,
        'Educations': Educations,
        'EMPID': EMPID,
        'ActiveLinkDict': ActiveLinkDict,
        'CurrentUrl': CurrentUrl,
    }
    return render(request, 'InterviewAssessment/CandidateData/CandidateQualificationinfoPage.html', context)



        
def CandidatePreviousWorkinfoPage(request):
    EMPID = request.GET.get('EMPID')
    Emobj = None
    previousworks = None
    ActiveLinkDict = None

    if EMPID is not None and EMPID.isdigit():
        EMPID = int(EMPID)
        Emobj = EmployeePersonalData.objects.filter(id=EMPID, IsDelete=False).first()
        if Emobj:
            EMPID = Emobj.id
            ActiveLinkDict = ActiveLink(EMPID=EMPID, return_dict=True)
            previousworks = EmployeePreviousWorkData.objects.filter(MasterID=EMPID, IsDelete=False)
            assobj  = Assessment_Master.objects.filter(EmpDataReceivedID=EMPID,IsDelete=False).first()
            if assobj.IsEmpDataReceived == True:
                    case_type = "data_submitted"
                    return redirect('notification_page', case_type=case_type) 

    CurrentUrl = 'CandidatePreviousWorkinfoPage'

    urlobj = CandidateUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        Increament = urlobj.sortorder + 1
        nextobj = CandidateUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        Decreament = urlobj.sortorder - 1
        Prevtobj = CandidateUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName

    if request.method == "POST":
        Company = request.POST.getlist('Company[]')
        Position = request.POST.getlist('Position[]')
        FromDate = request.POST.getlist('FromDate[]')
        ToDate = request.POST.getlist('ToDate[]')
       
        # IsPresentHidden = request.POST.getlist('IsPresentHidden[]')
        Salary = request.POST.getlist('Salary[]')
        AttachmentPreviousWork = request.FILES.getlist('AttachmentPreviousWork[]')
        FID= request.POST.getlist('FID[]')
        
       
        Pre_ids = request.POST.getlist('Pre_ids[]')
       
        removed_Pre_ids_str = request.POST.get('removed_Pre_ids[]', '')

     


        if removed_Pre_ids_str:
            removed_Pre_ids = [
                int(value) for value in removed_Pre_ids_str.split(',')
                if value.isdigit()  
            ]
        else:
            removed_Pre_ids = []
        if removed_Pre_ids_str:
          
            if previousworks.exists() and len(removed_Pre_ids) > 0:
                for id in removed_Pre_ids:
                    previousdelete = EmployeePreviousWorkData.objects.filter(id=id).first()
                    if previousdelete:
                        previousdelete.IsDelete = True
                        previousdelete.save()
        if Pre_ids:
                
                for (id, company, position, fromDate, toDate,salary) in (zip(Pre_ids, Company, Position, FromDate, ToDate,Salary)):
                    
                    # Present  = False
                    # if IsPresent == "On":
                    #      Present = True
                    #      toDate = None

                    i = 1
                    if id.startswith('new_'):
                    
                        PreviousObject = EmployeePreviousWorkData.objects.create(
                            MasterID=EMPID,
                            Company=company,
                            Position=position,
                            FromDate=fromDate,
                            ToDate=toDate,
                            Salary=salary,
                            # IsPresent = Present
                        )
                        key = f'FID_new_{i}'

                        if key in FID:
                                FileIndex = FID.index(key)
                                if FileIndex is not None:
                                        File = AttachmentPreviousWork[FileIndex]
                                        if File:
                                            upload_file(File, PreviousObject.id, "PreviousWork", "EmployeePreviousWorkData")
                        
                    else:
                        PreviousObject = EmployeePreviousWorkData.objects.filter(id=id).first()
                        if PreviousObject:
                            PreviousObject.Company = company
                            PreviousObject.Position = position
                            PreviousObject.FromDate = fromDate
                            PreviousObject.ToDate = toDate
                            PreviousObject.Salary = salary
                            # PreviousObject.IsPresent = Present
                            PreviousObject.save()
                            key = f'FID_{id}'
                            if key in FID:
                                    FileIndex = FID.index(key)
                                    if FileIndex is not None:
                                            File = AttachmentPreviousWork[FileIndex]
                                            if File:
                                                repalce_file(PreviousObject.id, "EmployeePreviousWorkData")
                                                upload_file(File, PreviousObject.id, "PreviousWork", "EmployeePreviousWorkData")

                    i = i + 1
                
                

        else:
           
            for company, position, fromDate, toDate, salary, Attachment in zip(Company, Position, FromDate, ToDate,Salary, AttachmentPreviousWork):



                
                # Present  = False
                # if IsPresent == "On":
                #          Present = True
                #          ToDate = None    

                PreviousObject = EmployeePreviousWorkData.objects.create(
                    MasterID=EMPID,
                    Company=company,
                    Position=position,
                    FromDate=fromDate,
                    ToDate=toDate,
                    Salary=salary
                )
                if Attachment:
                    upload_file(Attachment, PreviousObject.id, "PreviousWork", "EmployeePreviousWorkData")
        
        url = reverse(Nexturl)
        redirect_url = f"{url}?EMPID={EMPID}"
        return redirect(redirect_url)
    
    context = {'PreviousUrl': PreviousUrl, 'previousworks': previousworks, 'EMPID': EMPID, 'ActiveLinkDict': ActiveLinkDict, 'CurrentUrl': CurrentUrl}
    return render(request, 'InterviewAssessment/CandidateData/CandidatePreviousWorkinfoPage.html', context)




def CandidateAddressinfoPage(request):
    EMPID = request.GET.get('EMPID')
    Emobj = None
    Addressinfo = None 
    ActiveLinkDict = None

    if EMPID is not None and EMPID.isdigit():
       
        EMPID = int(EMPID)
       
        Emobj = EmployeePersonalData.objects.filter(id=EMPID,IsDelete=False).first()
        if Emobj:
                EMPID = Emobj.id
                ActiveLinkDict = ActiveLink(EMPID = EMPID, return_dict=True)
                Addressinfo = EmployeeAddressInfoData.objects.filter(MasterID=EMPID, IsDelete=False).first()
                assobj  = Assessment_Master.objects.filter(EmpDataReceivedID=EMPID,IsDelete=False).first()
                if assobj.IsEmpDataReceived == True:
                    case_type = "data_submitted"
                    return redirect('notification_page', case_type=case_type) 
       
    CurrentUrl = 'CandidateAddressinfoPage'

    urlobj  = CandidateUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = CandidateUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = CandidateUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName


    if request.method == "POST":
                Permanent_Address  =  request.POST['Permanent_Address'] or ''
                Permanent_City   =  request.POST['Permanent_City'] or ''
                Permanent_State  =  request.POST['Permanent_State'] or ''
                Permanent_Pincode  =  request.POST['Permanent_Pincode'] or ''
                Permanent_HousePhoneNumber  =  request.POST['Permanent_HousePhoneNumber'] or ''

                Temporary_Address  =  request.POST['Temporary_Address'] or ''
                Temporary_City   =  request.POST['Temporary_City'] or ''
                Temporary_State  =  request.POST['Temporary_State'] or ''
                Temporary_Pincode  =  request.POST['Temporary_Pincode'] or ''
                Temporary_HousePhoneNumber  =  request.POST['Temporary_HousePhoneNumber'] or ''
                if Addressinfo is not None  :
                   
                        Addressinfo.Permanent_Address = Permanent_Address
                        Addressinfo.Permanent_City = Permanent_City
                        Addressinfo.Permanent_State  = Permanent_State
                        Addressinfo.Permanent_Pincode = Permanent_Pincode
                        Addressinfo.Permanent_HousePhoneNumber  = Permanent_HousePhoneNumber        
                        Addressinfo.Temporary_Address = Temporary_Address        
                        Addressinfo.Temporary_City  = Temporary_City        
                        Addressinfo.Temporary_Pincode = Temporary_Pincode        
                        Addressinfo.Temporary_HousePhoneNumber   = Temporary_HousePhoneNumber
                        Addressinfo.save()        
                        
                else:
                    Addressobject  = EmployeeAddressInfoData.objects.create(MasterID =  EMPID,Permanent_Address  = Permanent_Address,Permanent_City = Permanent_City,Permanent_State = Permanent_State,Permanent_Pincode = Permanent_Pincode,Permanent_HousePhoneNumber = Permanent_HousePhoneNumber,Temporary_Address = Temporary_Address,Temporary_City =Temporary_City,Temporary_State = Temporary_State,Temporary_Pincode=Temporary_Pincode,Temporary_HousePhoneNumber=Temporary_HousePhoneNumber)

                
                
                
                url = reverse(Nexturl)  
                redirect_url = f"{url}?EMPID={EMPID}" 
                return redirect(redirect_url)
    context= {'PreviousUrl':PreviousUrl,'Addressinfo':Addressinfo,'EMPID':EMPID,'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl} 
    return render(request, 'InterviewAssessment/CandidateData/CandidateAddressinfoPage.html', context)







def CandidateIdentityinfoPage(request):
    EMPID = request.GET.get('EMPID')
    Emobj = None
    IdentityInfo = None 
    ActiveLinkDict = None

    if EMPID is not None and EMPID.isdigit():
       
        EMPID = int(EMPID)
       
        Emobj = EmployeePersonalData.objects.filter(id=EMPID,IsDelete=False).first()
        if Emobj:
                EMPID = Emobj.id
                ActiveLinkDict = ActiveLink(EMPID = EMPID, return_dict=True)
                IdentityInfo = EmployeeIdentityInfoData.objects.filter(MasterID=EMPID, IsDelete=False).first()
                assobj  = Assessment_Master.objects.filter(EmpDataReceivedID=EMPID,IsDelete=False).first()
                if assobj.IsEmpDataReceived == True:
                    case_type = "data_submitted"
                    return redirect('notification_page', case_type=case_type) 
     
       
    CurrentUrl = 'CandidateIdentityinfoPage'

    urlobj  = CandidateUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = CandidateUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = CandidateUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName


    if request.method == "POST":
                PANNo = request.POST['PANNo'] or ''
                AadhaarNumber = request.POST['AadhaarNumber'] or ''
                DrivingLicenceNo = request.POST['DrivingLicenceNo'] or ''
                PANattachment = request.FILES.get('PANattachment')
                Aadhaarattachment = request.FILES.get('Aadhaarattachment')
                DrivingLicenceattachment = request.FILES.get('DrivingLicenceattachment')

                if IdentityInfo is not None:
                    IdentityInfo.PANNo  = PANNo
                    IdentityInfo.AadhaarNumber = AadhaarNumber
                    IdentityInfo.DrivingLicenceNo  = DrivingLicenceNo
                    IdentityInfo.save()
                    if PANattachment:
                                upload_file(PANattachment,IdentityInfo.id,"Docuemnts","EmployeeIdentityInfoData_Pan")
                    if Aadhaarattachment:
                                upload_file(Aadhaarattachment,IdentityInfo.id,"Docuemnts","EmployeeIdentityInfoData_Aadhaar")
                    if DrivingLicenceattachment:
                                upload_file(DrivingLicenceattachment,IdentityInfo.id,"Docuemnts","EmployeeIdentityInfoData_License")            
                                
                                            
                                            


                else:
                    IdentityInfo =  EmployeeIdentityInfoData.objects.create(   MasterID =  EMPID,
                            PANNo = PANNo,AadhaarNumber = AadhaarNumber,DrivingLicenceNo = DrivingLicenceNo
                        )
                    if PANattachment:
                                upload_file(PANattachment,IdentityInfo.id,"Docuemnts","EmployeeIdentityInfoData_Pan")
                    if Aadhaarattachment:
                                upload_file(Aadhaarattachment,IdentityInfo.id,"Docuemnts","EmployeeIdentityInfoData_Aadhaar")
                    if DrivingLicenceattachment:
                                upload_file(DrivingLicenceattachment,IdentityInfo.id,"Docuemnts","EmployeeIdentityInfoData_License") 
                
                
                url = reverse(Nexturl)  
                redirect_url = f"{url}?EMPID={EMPID}" 
                return redirect(redirect_url)
    context= {'PreviousUrl':PreviousUrl,'IdentityInfo':IdentityInfo,'EMPID':EMPID,'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl} 
    return render(request, 'InterviewAssessment/CandidateData/CandidateIdentityinfoPage.html', context)






def CandidateBankinfoPage(request):
    EMPID = request.GET.get('EMPID')
    Emobj = None
    Bankinfo = None 
    ActiveLinkDict = None

    if EMPID is not None and EMPID.isdigit():
       
        EMPID = int(EMPID)
       
        Emobj = EmployeePersonalData.objects.filter(id=EMPID,IsDelete=False).first()
        if Emobj:
                EMPID = Emobj.id
                ActiveLinkDict = ActiveLink(EMPID = EMPID, return_dict=True)
                Bankinfo = EmployeeBankInfoData.objects.filter(MasterID=EMPID, IsDelete=False).first()
                assobj  = Assessment_Master.objects.filter(EmpDataReceivedID=EMPID,IsDelete=False).first()
                if assobj.IsEmpDataReceived == True:
                    case_type = "data_submitted"
                    return redirect('notification_page', case_type=case_type) 
                    
    CurrentUrl = 'CandidateBankinfoPage'

    urlobj  = CandidateUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = CandidateUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = CandidateUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName


    if request.method == "POST":
                BankAccountNumber = request.POST['BankAccountNumber'] or ''
                NameofBank   = request.POST['NameofBank'] or ''
                BankBranch   = request.POST['BankBranch'] or ''
                IFSCCode   = request.POST['IFSCCode'] or ''
                if Bankinfo is not None:
                   Bankinfo.BankAccountNumber  = BankAccountNumber
                   Bankinfo.NameofBank   = NameofBank
                   Bankinfo.BankBranch  =BankBranch
                   Bankinfo.IFSCCode  = IFSCCode
                   Bankinfo.save()
                else:
                    Bankinfo = EmployeeBankInfoData.objects.create(MasterID =  EMPID,
                        BankAccountNumber  =BankAccountNumber,NameofBank  = NameofBank,BankBranch  = BankBranch,IFSCCode = IFSCCode
                    )
                
                
                url = reverse(Nexturl)  
                redirect_url = f"{url}?EMPID={EMPID}" 
                return redirect(redirect_url)
    context= {'PreviousUrl':PreviousUrl,'Bankinfo':Bankinfo,'EMPID':EMPID,'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl} 
    return render(request, 'InterviewAssessment/CandidateData/CandidateBankinfoPage.html', context)




from app.models import OrganizationEmailMaster
from app.views import OrganizationName,OrganizationLogo

from django.conf import settings
from django.template.loader import render_to_string



from django.core.mail import EmailMessage

def EmailToHr(request,InterviewID):
        if 'OrganizationID' not in request.session:
           return redirect(MasterAttribute.Host)
        
        from HumanResources.views  import GetMailofHR
      
        AssessmentDetails  = Assessment_Master.objects.filter(id=InterviewID,IsDelete=False).first()
        if AssessmentDetails:
                    
                    if AssessmentDetails:

                        AppliedFor = AssessmentDetails.AppliedFor
                        if AppliedFor:
                            orgName = OrganizationName(AppliedFor)
                            orgLogo = OrganizationLogo(AppliedFor)
                            OrganizationID = AppliedFor

                       
        default_bcc = "rajshree@nilehospitality.com"
        bcc_list = [default_bcc]
        HR_EmailAddress= GetMailofHR(OrganizationID)
        if HR_EmailAddress:  
            bcc_list.append(HR_EmailAddress)

        email_settings = OrganizationEmailMaster.objects.filter(OrganizationID=OrganizationID, IsDelete=False).first()
        if OrganizationEmailMaster.DoesNotExist:
            email_settings = OrganizationEmailMaster.objects.filter(OrganizationID=3, IsDelete=False).first()

        if email_settings:
            settings.EMAIL_HOST = email_settings.email_host
            settings.EMAIL_PORT = email_settings.email_port
            settings.EMAIL_USE_TLS = email_settings.email_use_tls
            settings.EMAIL_HOST_USER = email_settings.email_host_user
            settings.EMAIL_HOST_PASSWORD = email_settings.email_host_password

            email_subject = f'{AssessmentDetails.Name} has submitted the details'

            email_body = render_to_string('InterviewAssessment/EmailToHr.html', {
                'name': AssessmentDetails.Name,
                'candidate_name': AssessmentDetails.Name,
                'candidate_designation': AssessmentDetails.position,  
                'candidate_department': AssessmentDetails.Department,  
                'OrganizationName':orgName,
                'Logo':orgLogo,

               
        
            })


            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [email_settings.email_host],
                  bcc=HR_EmailAddress
            )

            email.content_subtype = 'html'

          
            try:
                email.send(fail_silently=False)
                return JsonResponse({'status': 'success', 'message': 'Email sent successfully!'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': 'Error sending email.'}, status=500)
        else:
            return JsonResponse({'status': 'error', 'message': 'No email settings found.'}, status=500)

   

def EmailToCandidate(request,InterviewID):
        if 'OrganizationID' not in request.session:
           return redirect(MasterAttribute.Host)
            
        OrganizationID = request.session["OrganizationID"]
        from HumanResources.views  import GetMailofHR
      
        default_bcc = "rajshree@nilehospitality.com"
        bcc_list = [default_bcc]
        HR_EmailAddress= GetMailofHR(OrganizationID)
        if HR_EmailAddress:  
            bcc_list.append(HR_EmailAddress)

        AssessmentDetails  = Assessment_Master.objects.filter(id=InterviewID,IsDelete=False,OrganizationID=OrganizationID).first()
        if AssessmentDetails:
                    
                    if AssessmentDetails:
                        AppliedFor = AssessmentDetails.AppliedFor
                        if AppliedFor:
                            orgName = OrganizationName(AppliedFor)
                            orgLogo = OrganizationLogo(AppliedFor)

                            email = AssessmentDetails.Email
                       
 
                       
        
        email_settings = OrganizationEmailMaster.objects.filter(OrganizationID=OrganizationID, IsDelete=False).first()
        if OrganizationEmailMaster.DoesNotExist:
            email_settings = OrganizationEmailMaster.objects.filter(OrganizationID=3, IsDelete=False).first()

        if email_settings:
            settings.EMAIL_HOST = email_settings.email_host
            settings.EMAIL_PORT = email_settings.email_port
            settings.EMAIL_USE_TLS = email_settings.email_use_tls
            settings.EMAIL_HOST_USER = email_settings.email_host_user
            settings.EMAIL_HOST_PASSWORD = email_settings.email_host_password

            email_subject = f'Your detail has been submitted'

            
            email_body = render_to_string('InterviewAssessment/EmailToCandidate.html', {
                'name': AssessmentDetails.Name,
                'candidate_name': AssessmentDetails.Name,
                'candidate_designation': AssessmentDetails.position,  
                'candidate_department': AssessmentDetails.Department,  
                'OrganizationName':orgName,
                'Logo':orgLogo
               
        
            })


            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [email],
             bcc=bcc_list, 
            )
             
            email.content_subtype = 'html'

          
            try:
                email.send(fail_silently=False)
                return JsonResponse({'status': 'success', 'message': 'Email sent successfully!'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': 'Error sending email.'}, status=500)
        else:
            return JsonResponse({'status': 'error', 'message': 'No email settings found.'}, status=500)


def CandidateDocumentinfoPage(request):
    EMPID = request.GET.get('EMPID')
    Emobj = None
    Documents = None 
    ActiveLinkDict = None

    if EMPID is not None and EMPID.isdigit():
       
        EMPID = int(EMPID)
       
        Emobj = EmployeePersonalData.objects.filter(id=EMPID,IsDelete=False).first()
        if Emobj:
                EMPID = Emobj.id
                ActiveLinkDict = ActiveLink(EMPID = EMPID, return_dict=True)
                Documents = EmployeeDocumentsInfoData.objects.filter(MasterID=EMPID, IsDelete=False)
                assobj  = Assessment_Master.objects.filter(EmpDataReceivedID=EMPID,IsDelete=False).first()
                if assobj.IsEmpDataReceived == True:
                    case_type = "data_submitted"
                    return redirect('notification_page', case_type=case_type) 
               
       
    CurrentUrl = 'CandidateDocumentinfoPage'

    urlobj  = CandidateUrlMaster.objects.filter(UrlName=CurrentUrl).first()
    Nexturl = CurrentUrl
    PreviousUrl = CurrentUrl
    if urlobj:
        # Next Url
        Increament = urlobj.sortorder
        Increament   = Increament + 1
        nextobj  = CandidateUrlMaster.objects.filter(sortorder=Increament).first()
        if nextobj:
            Nexturl = nextobj.UrlName
        # Previous Url
        Decreament = urlobj.sortorder
        Decreament   = Decreament - 1
        Prevtobj  = CandidateUrlMaster.objects.filter(sortorder=Decreament).first()
        if Prevtobj:
            PreviousUrl = Prevtobj.UrlName
        

    if request.method == "POST":
                
                Title = request.POST.getlist('Title[]')
              
                Doc_ids = request.POST.getlist('Doc_ids[]')
                AttachmentDocumenstsFile  = request.FILES.getlist('AttachmentDocumenstsFile[]')
                FID = request.POST.getlist('FID[]') 
                removed_Doc_ids_str = request.POST.get('removed_Doc_ids[]', '')

             

                if removed_Doc_ids_str:
                    removed_Doc_ids =  [
                int(value) for value in removed_Doc_ids_str.split(',')
                if value.isdigit()  
                  ]
                else:
                    removed_Doc_ids = []    

                if Doc_ids  is not None:
                    if len(removed_Doc_ids) > 0:
                      
                        for id in removed_Doc_ids:
                          
                            docdelete = EmployeeDocumentsInfoData.objects.filter(id=id).first()
                          
                            docdelete.IsDelete  = True
                            docdelete.save()
                            
                    for  id,title in zip(Doc_ids,Title):
                        i = 1 
                        if id.startswith('new_'):
                            DocObject  = EmployeeDocumentsInfoData.objects.create(
                                 MasterID =  EMPID,
                                Title = title

                            )
                            key = f'FID_new_{i}'

                            if key in FID:
                                    FileIndex = FID.index(key)
                                  
                                    if FileIndex is not None:
                                            File = AttachmentDocumenstsFile[FileIndex]
                                            if File:    
                                                 upload_file(File,DocObject.id,"Docuemnts","EmployeeDocumentsInfoData") 
                        else:
                            DocObject  = EmployeeDocumentsInfoData.objects.filter(IsDelete=False).first()
                            DocObject.Title  = title
                            DocObject.save()
                            key = f'FID_{id}'

                            if key in FID:
                                    FileIndex = FID.index(key)
                                  
                                    if FileIndex is not None:
                                            File = AttachmentDocumenstsFile[FileIndex]
                                            if File:    
                                                repalce_file(DocObject.id,"EmployeeDocumentsInfoData")
                                                upload_file(File,DocObject.id,"Docuemnts","EmployeeDocumentsInfoData")   
                        i = i + 1          
                else:
                    for  title,Attachment in zip(Title,AttachmentDocumenstsFile):
                            DocObject  = EmployeeDocumentsInfoData.objects.create(
                                 MasterID =  EMPID,
                                Title = title

                            )
                            if Attachment:
                                
                                  upload_file(Attachment,DocObject.id,"Docuemnts","EmployeeDocumentsInfoData")
             
              
                assobj  = Assessment_Master.objects.filter(EmpDataReceivedID=EMPID,IsDelete=False).first()
                if assobj:
                    assobj.IsEmpDataReceived = True
                    assobj.save()
                    Linkobj = EmployeeDataRequest_Master.objects.filter(InterviewID=assobj.id,IsDelete=False).first()
                    Linkobj.IsEmpDataReceived  = True
                    Linkobj.save()
                    EmailToHr(request,assobj.id)
                    EmailToCandidate(request,assobj.id)

                
               
                # return redirect(Nexturl)
                case_type = "thank_you"
                return redirect('notification_page', case_type=case_type) 
    
    context= {'PreviousUrl':PreviousUrl,'Documents':Documents,'EMPID':EMPID,'ActiveLinkDict':ActiveLinkDict,'CurrentUrl':CurrentUrl} 
    return render(request, 'InterviewAssessment/CandidateData/CandidateDocumentinfoPage.html', context)








def notification_page(request, case_type):
    context = {}
    
    if case_type == 'link_expiry':
        context['title'] = 'Link Expired'
        context['message'] = 'The link you are trying to access has expired. Please contact support if you need further assistance.'
        context['alert_class'] = 'alert-danger'
    elif case_type == 'data_submitted':
        context['title'] = 'Data Submitted'
        context['message'] = 'Your data has been successfully submitted.'
        context['alert_class'] = 'alert-success'
    elif case_type == 'thank_you':
        context['title'] = 'Thank You!'
        context['message'] = 'Thank you for submitting your information.'
        context['alert_class'] = 'alert-success'
      
    
    return render(request, 'InterviewAssessment/CandidateData/notification_page.html',context)     

from Reference_check.models import ReferenceDetails,Reference_check

def rehirstatus(ref_unique_id):
     if ref_unique_id:
          rehire_status  = Reference_check.objects.filter(ref_unique_id=ref_unique_id).first()
          if rehire_status:
               return rehire_status.rehire
          else:
            return False

def Reference(request):
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    token = request.headers.get('hotel-api-token')
    
    # Check if the token is valid
    if token != hotelapitoken:
        return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)

    RID = request.GET.get('RID')
   
    # Check if RID is provided
    if not RID:
        return JsonResponse({"error": "RID is a required parameter"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate if RID is an integer
    try:
        RID = int(RID)
    except ValueError:
        return JsonResponse({"error": f"Reference : {RID}"}, status=status.HTTP_400_BAD_REQUEST)
    
         
    obj = ReferenceDetails.objects.filter(IsDelete=False, id=RID).first()
    if obj is not None:
        data = {
            'candidate_name': obj.candidate_name,
            'candidate_department': obj.candidate_department,
            
            # Reference 1 details
            'ref1_name': obj.Ref1_name,
            'ref1_email': obj.Ref1_email,
            'ref1_mobile_number': obj.Ref1_mobile_number,
            'ref1_organization': obj.Ref1_Organization,
            'ref1_designation': obj.Ref1_Designation,
            'ref1_status': obj.ref1_status,
            'rehire_status1': rehirstatus(obj.ref1_unique_id),
            
            # Reference 2 details
            'ref2_name': obj.Ref2_name,
            'ref2_email': obj.Ref2_email,
            'ref2_mobile_number': obj.Ref2_mobile_number,
            'ref2_organization': obj.Ref2_Organization,
            'ref2_designation': obj.Ref2_Designation,
            'ref2_status': obj.ref2_status,
            'rehire_status2': rehirstatus(obj.ref2_unique_id),
            
            # Reference 3 details
            'ref3_name': obj.Ref3_name,
            'ref3_email': obj.Ref3_email,
            'ref3_mobile_number': obj.Ref3_mobile_number,
            'ref3_organization': obj.Ref3_Organization,
            'ref3_designation': obj.Ref3_Designation,
            'ref3_status': obj.ref3_status,
            'rehire_status3': rehirstatus(obj.ref3_unique_id),
            
            'id': obj.id
        }
    
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"error": "Reference not found"}, status=status.HTTP_404_NOT_FOUND)

from Letterofintent.models import LETTEROFINTENTEmployeeDetail
from django.http import JsonResponse
from datetime import date

def LetterofIntent(request):
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    token = request.headers.get('hotel-api-token')

    # Check if the token is valid
    if token != hotelapitoken:
        return JsonResponse({"error": "Invalid API token"}, status=403)

    InterviewID = request.GET.get('InterviewID')
    OrganizationID = request.GET.get('OrganizationID')

    if not InterviewID:
        return JsonResponse({"error": "InterviewID is a required parameter"}, status=400)

    lois = LETTEROFINTENTEmployeeDetail.objects.filter(InterviewID=InterviewID).order_by('-id')
    
    if lois.exists():
        data = []
        for loi in lois:
            data.append({
                "emp_name": loi.emp_name,
                "CreatedDateTime": loi.CreatedDateTime.strftime('%d-%m-%Y'),  # Format the date
                "id": loi.id,
                "InterviewID": InterviewID
            })
        return JsonResponse({"data": data})
    else:
        return JsonResponse({"error": "Reference not found"}, status=404)
