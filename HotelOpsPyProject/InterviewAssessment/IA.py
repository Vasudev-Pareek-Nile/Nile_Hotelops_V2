
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
# from datetime import datetime
from datetime import date
from django.utils import timezone

def InterviewAssessmentCreate(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")


    for key, value in request.session.items():
            print(f"{key} => {value}")


    

    # Object None 
    blocked_user_types  = None
    Designations  = None
    Resumeobj   = None     
    appliedFor  = None
    position  = None    
    AM_obj = None
    HrData = 'None'
    Department = ''


    # Designations  List For Drop Down
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')



    # Session Details  
    OrganizationID = request.session.get("OrganizationID")
    # OrganizationList for Drop down on the basis of OrganizationID
    orgs = OrganizationList(OrganizationID)
    UserID = str(request.session.get("UserID"))
    UserType = request.session.get("UserType")
    UserType = str(UserType).lower()
    EmployeeCode = request.session.get("EmployeeCode")




    # Login User Department List if Employee Code is  Found
    from HumanResources.views import MultipleDepartmentofEmployee,EmployeeIsRD
    DepartmentList = []
    if EmployeeCode:
        EmployeeDepartmentobj  = MultipleDepartmentofEmployee(OrganizationID, EmployeeCode)
        if  EmployeeDepartmentobj:
             DepartmentList = EmployeeDepartmentobj
             
        
        else:    
            return Error(request, "Employee Details not Found.Update in Human Resources")
    else:
        return Error(request, "Employee Code is required. Please update it in User Details.") 

    # On the Basis of OrganizationID , UserType and DepartmentList Final UserType and Department

    if OrganizationID == '3' and UserType == 'hod':
        # print("sessions organization id::", OrganizationID)
        # print("sessions UserType id::", UserType)
        Rdobj = EmployeeIsRD(request, OrganizationID, EmployeeCode)
        if Rdobj == True:
            UserType = 'rd'
        
        # print("User type after conversion::", UserType)

    # Get Details for IA and open positions 

    AID = request.GET.get('AID')
    OPID=request.GET.get('OPID')
    
   


    # IA and  Factor Details on the basis of AID

    factor_details = {}
    Datafrom =''
    if AID:
        AM_obj = Assessment_Master.objects.filter(
            IsDelete=False, id=AID
        ).first()
        position = AM_obj.position
        blocked_user_types = AM_obj.block_lower_level_edit()
        
     
        Datafrom  = 'DatafromAssessment'
                  
        if not  AM_obj:
            return Error(request, f"Interview Assessment is not Found.")   
    
        if AM_obj:
            appliedFor = AM_obj.AppliedFor
            
           
            factor_details = Assessment_Factor_Details.objects.filter(MasterID=AID).values(
                'CategoryID', 'factor', 'hr_rating', 'hr_remarks', 
                'hod_rating', 'hod_remarks', 'gm_rating', 
                'gm_remarks', 'rd_rating', 'rd_remarks'
            )

          
            factor_details = {f['CategoryID']: f for f in factor_details}
        MasterID = AID


    # Resume Details when IA in created  from Open position

    if OPID:
         Resumeobj  = CareerResume.objects.filter(id=OPID).first()
         if not  Resumeobj:
            return Error(request, f"Resume not Found.")   
    
         if Resumeobj:
              AM_obj =  {
                   'Name':Resumeobj.first_name + " "+ Resumeobj.last_name,
                   'AppliedFor':AppliedForORGID(Resumeobj.location),
                   'position':Resumeobj.job_title,
                   'ContactNumber':Resumeobj.phone,
                   'Email':Resumeobj.email


              }
              Datafrom  = 'DatafromResume'
            
              if int(OrganizationID) != 3:
                appliedFor = OrganizationID
              else:
                  
                   appliedFor = AppliedForORGID(Resumeobj.location)
           
              position = Resumeobj.job_title
             

    
    # if New IA is created and below condtions works then UserType = 'hr' UserType = 'hod'
    # if AM_obj == None  and  ('Human Resources' in DepartmentList  or  "Executive Office" in DepartmentList or   "Talent Acquisition and Development" in DepartmentList or   "Corporate Office" in DepartmentList):
    #         UserType = 'hr'
    

    if 'Human Resources' in DepartmentList:
            Department = 'hr'
    



    # if  when Hr it self  is hod
    if AM_obj is not None and AID :
       
            if AM_obj.Department in DepartmentList:
                HrData = 'Show'

     
    if request.method == "POST":
       
        HireFor = request.POST.get('hire')
        InterviewDate = request.POST.get('dateOfInterview')
        AssessmentDepartment = request.POST.get('department')
        position = request.POST.get('positionAppliedFor')
        Level = request.POST.get('level')
        Prefix = request.POST.get('Prefix')
        Name = request.POST.get('name')
        workexperience = request.POST.get('experienceType')
       
        if workexperience == "experience":
            Years = request.POST.get('Years') or 0
            Months = request.POST.get('Months') or 0
            workexperience = f'{Years} Years {Months} Months'
        familybackground = request.POST.get('familyBackground')
        pre_salary = request.POST.get('presentSalary') or 0
        exp_salary = request.POST.get('expectedSalary') or 0

        Presentdesignation = request.POST.get('Presentdesignation') or ''
        Expecteddesignation = request.POST.get('Expecteddesignation') or ''

        ContactNumber = request.POST.get('contactNumber')
        Email = request.POST.get('Email')

        ProposedDOJ = request.POST.get('proposedDoj')
        AppliedFor = request.POST.get('appliedFor')
        ResumeID = request.POST.get('ResumeID') or 0

        resume = request.FILES.get('resume')
        
        hr_as = hr_as_remarks = ''
        hod_as = hod_as_remarks = ''
        rd_as = rd_as_remarks = ''
        gm_as = gm_as_remarks = ''

      
        



        if Datafrom == 'DatafromAssessment'  :
            Hodobj = HODLevel(AM_obj.Level, AM_obj.Department,OrganizationID)
            if Hodobj:
                        HOD = Hodobj['hod_found']
                        print("HOD Found = ",HOD)
            
       


        # HR Rating
        if 'hr_final_rating' and 'hr_final_remarks' in request.POST:
            hr_as = request.POST['hr_final_rating'] 
            hr_as_remarks = request.POST['hr_final_remarks'] 



        # HOD Raing 
        if 'hod_final_rating' in request.POST and 'hod_final_remarks' in request.POST:
                if Datafrom == 'DatafromAssessment':  
                        if  Department != 'hr'    and HOD and UserType == "hod":
                            print("Inside IF  hod_final_rating")
                            hod_as = request.POST['hod_final_rating'] 
                            hod_as_remarks = request.POST['hod_final_remarks']
                        elif HOD and Department == 'hr' and AssessmentDepartment  in DepartmentList and UserType == "hod":
                            print("Inside elif  hod_final_rating")
                            hod_as = request.POST['hod_final_rating'] 
                            hod_as_remarks = request.POST['hod_final_remarks']
                                


        # RD Rating
        
        if 'rd_final_rating' and 'rd_as_remarks' in request.POST:
        
            rd_as = request.POST['rd_final_rating'] 
            rd_as_remarks = request.POST['rd_as_remarks'] 


        # GM Rating     
        
        if 'gm_final_rating' and 'gm_as_remarks' in request.POST:
            gm_as = request.POST['gm_final_rating'] 
            gm_as_remarks = request.POST['gm_as_remarks'] 
        
        # print("The real date is here::",date.today())
        if AID:
            if Department == 'hr':
                AM_obj.HireFor = HireFor
                AM_obj.InterviewDate = InterviewDate
                AM_obj.Department = AssessmentDepartment
                AM_obj.position = position
                AM_obj.Level = Level
                AM_obj.Prefix = Prefix
                AM_obj.Name = Name
                AM_obj.workexperience = workexperience
                AM_obj.familybackground = familybackground
                AM_obj.pre_salary = pre_salary
                AM_obj.exp_salary = exp_salary
                AM_obj.Presentdesignation = Presentdesignation
                AM_obj.Expecteddesignation = Expecteddesignation
                AM_obj.ContactNumber = ContactNumber
                AM_obj.Email = Email
                AM_obj.ProposedDOJ = ProposedDOJ
                AM_obj.AppliedFor = AppliedFor
                AM_obj.ResumeID = ResumeID
            
            if hr_as != '' and hr_as_remarks != '' and Department == 'hr':
                AM_obj.hr_as = hr_as
                AM_obj.hr_as_remarks = hr_as_remarks
                AM_obj.hr_UserID  = UserID
            
            if hod_as != '' and hod_as_remarks != '' and  UserType == "hod" :

                AM_obj.hod_as = hod_as
                AM_obj.hod_as_remarks = hod_as_remarks
                AM_obj.hod_UserID  = UserID
            
            if gm_as != '' and gm_as_remarks != '' and UserType == "gm":
            
                AM_obj.gm_as = gm_as
                AM_obj.gm_as_remarks = gm_as_remarks
                AM_obj.gm_UserID  = UserID
            
            if rd_as != '' and rd_as_remarks != '' and UserType == "rd":

                AM_obj.rd_as = rd_as
                AM_obj.rd_as_remarks = rd_as_remarks
                AM_obj.rd_UserID  = UserID
            
          

            # Hod Action Date Time 

            if Datafrom == 'DatafromAssessment':  
                     if  Department != 'hr'    and HOD and UserType == "hod":
                            print("Inside if  hod_actionOn")
                            AM_obj.hod_actionOn =  date.today()
                            AM_obj.hod_actionOnDatetime = timezone.now()
                     elif HOD and Department == 'hr' and AssessmentDepartment  in DepartmentList and UserType == "hod":
                            print("Inside elif  hod_actionOn")
                            AM_obj.hod_actionOn =  date.today()
                            AM_obj.hod_actionOnDatetime = timezone.now()

            # GM Action Date Time 
            if UserType == 'gm':
                AM_obj.gm_actionOn =  date.today()
                AM_obj.gm_actionOnDatetime = timezone.now()
            # RD Action Date Time  
            if UserType == 'rd':
                AM_obj.rd_actionOn =  date.today()
                AM_obj.rd_actionOnDatetime = timezone.now()
            


            # AppovalStage 
            LastApprovalStage = LastApprovalStageFun(AM_obj.Level,AM_obj.Department,AM_obj.OrganizationID)
            if not  LastApprovalStage:
                    return Error(request, f"ApprovalStage not Found.")   
    

            if str(LastApprovalStage).lower() == "rd" and  UserType  == str(LastApprovalStage).lower():
                    AM_obj.rd_as = rd_as
                    AM_obj.rd_as_remarks = rd_as_remarks
                    AM_obj.rd_actionOn =  date.today()
                    AM_obj.rd_actionOnDatetime = timezone.now()
                    AM_obj.LastApporvalStatus  = rd_as
                 
           
            if str(LastApprovalStage).lower() == "gm" and  UserType  == str(LastApprovalStage).lower():
          
                   
                    AM_obj.gm_as = gm_as
                    AM_obj.gm_as_remarks = gm_as_remarks
                    AM_obj.gm_actionOn =  date.today()
                    AM_obj.gm_actionOnDatetime = timezone.now()
                    AM_obj.LastApporvalStatus  = gm_as
                  
                          




            AM_obj.LastStatusUpdateBy = UserID
            AM_obj.LastStatusUpdateOn = date.today()
            AM_obj.ModifyBy = UserID
            AM_obj.save()

            if resume:
                repalce_file(AID,"Assessment_Master")
                upload_file(resume, AID,"Resumes","Assessment_Master")
        else:
            Assessment_obj = Assessment_Master.objects.create(
                OrganizationID=OrganizationID,
                CreatedBy=UserID,
                HireFor=HireFor,
                InterviewDate=InterviewDate,
                Department=AssessmentDepartment,
                position=position,
                Level=Level,
                Prefix=Prefix,
                Name=Name,
                workexperience=workexperience,
                familybackground=familybackground,
                pre_salary=pre_salary,
                exp_salary=exp_salary,
                Presentdesignation = Presentdesignation,
                Expecteddesignation = Expecteddesignation,

                ContactNumber=ContactNumber,
                Email = Email,
                ProposedDOJ=ProposedDOJ,
                AppliedFor=AppliedFor,
                ResumeID=ResumeID,
                hod_as =hod_as,
                hod_as_remarks =hod_as_remarks,
                gm_as = gm_as,
                gm_as_remarks = gm_as_remarks,
                rd_as = rd_as,
                rd_as_remarks = rd_as_remarks,
                hr_as=hr_as,
                hr_as_remarks=hr_as_remarks,
                hod_UserID  =  UserID,
                hr_actionOn =  date.today(),
                hr_actionOnDatetime = timezone.now(),
                

            )

            if resume is not None:
                upload_file(resume, Assessment_obj.id,"Resumes","Assessment_Master")
            else:
               
                if Resumeobj:
                        file_content, file_type = CopyFileResume(Resumeobj.resume_url)
                        
                        file_io = BytesIO(file_content)
                        
                        file_io.name = str(Resumeobj.resume)
                        
                        upload_file(file_io, Assessment_obj.id, "Resumes", "Assessment_Master")



                
      
            MasterID = Assessment_obj.id
        
        for category_id in range(1, 11):
            category_id_str = str(category_id)
            
            selected_factors = request.POST.getlist(f'factor_{category_id_str}')
            factor_string = ', '.join(selected_factors) if selected_factors else None
            
            hr_rating = request.POST.get(f'hr_rating_{category_id_str}')
            hr_remarks = request.POST.get(f'hr_remarks_{category_id_str}')
            hod_rating = request.POST.get(f'hod_rating_{category_id_str}')
            hod_remarks = request.POST.get(f'hod_remarks_{category_id_str}')
            gm_rating = request.POST.get(f'gm_rating_{category_id_str}')
            gm_remarks = request.POST.get(f'gm_remarks_{category_id_str}')
            rd_rating = request.POST.get(f'rd_rating_{category_id_str}')
            rd_remarks = request.POST.get(f'rd_remarks_{category_id_str}')

           
            assessment_detail, created = Assessment_Factor_Details.objects.get_or_create(
                MasterID=MasterID,
                OrganizationID=OrganizationID,
              
                CategoryID=category_id_str,
                defaults={'CreatedBy': UserID}
            )


            if factor_string:
                assessment_detail.factor = factor_string
            else:
                assessment_detail.factor = ''

            if hr_rating :
                assessment_detail.hr_rating = hr_rating
            else:
                assessment_detail.hr_rating = ''
 
            
            if hr_remarks :
                assessment_detail.hr_remarks = hr_remarks
            else:
                assessment_detail.hr_remarks = ''    
            
            if hod_rating :
                assessment_detail.hod_rating = hod_rating
            else:
                assessment_detail.hod_rating = ''     
            
            if hod_remarks :
                assessment_detail.hod_remarks = hod_remarks
            else:
                assessment_detail.hod_remarks = '' 
            
            if gm_rating :
                assessment_detail.gm_rating = gm_rating
            else:
                assessment_detail.gm_rating = ''     
            if gm_remarks :
                assessment_detail.gm_remarks = gm_remarks
            else:
                assessment_detail.gm_remarks = '' 
            if rd_rating :
                assessment_detail.rd_rating = rd_rating
            else:
                assessment_detail.rd_rating = ''     
            if rd_remarks :
                assessment_detail.rd_remarks = rd_remarks
            else:
                assessment_detail.rd_remarks = ''   
           
             
           
            assessment_detail.ModifyBy = UserID
            assessment_detail.save()
        
        messages.success(request, 'Assessment details saved successfully.')
        return redirect('InterviewAssessmentList')
   
    # print("UserType = ",UserType)
    # print("Department = ",Department)
    # print("HrData = ",HrData)

    session_data = dict(request.session)
    print("The all session value is here::", session_data)


    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    context = {
        'orgs': orgs,
      'appliedFor': appliedFor if appliedFor is not None else OrganizationID,

        'AM_obj': AM_obj,
        'HrData':HrData,
        'Designations': Designations,
        'position':position,
        'UserType': UserType,
        'OrganizationID':OrganizationID,

        'Department': Department,
        'factor_details': factor_details,
        'hotelapitoken':hotelapitoken,
        'Resumeobj':Resumeobj,
       
       'blocked_user_types': json.dumps(blocked_user_types),



      
    }
    return render(request, 'InterviewAssessment/InterviewAssessmentCreate.html', context)














from datetime import datetime
import calendar
from HumanResources.views import MultipleDepartmentofEmployee

def InterviewAssessmentList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    # print("the path is here:", request.path_info)

    year = request.GET.get('year')
    if year:
        year = int(year)
    else:
        year = datetime.now().year

    month_no = request.GET.get('month_no')
    if month_no and month_no != 'All':
        month_no = int(month_no)
    else:
        month_no = None  

    month_name = "All Months" if not month_no else calendar.month_name[month_no]

    today = datetime.today()
    CYear = today.year
    CMonth = today.month

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    SessionOrganizationID = int(OrganizationID)
    EmployeeCode = request.session.get("EmployeeCode")
    UserType = str(request.session.get("UserType", '')).lower()
    I = request.GET.get('I',OrganizationID)

    # print("UserType f this currect employee:: ", UserType)

    # UserType = 'HOD'

    # print("I ", I)
    # print("OrganizationID type", type(OrganizationID))
    # print("OrganizationID ", OrganizationID)
    # print("UserID ", UserID)
    # print("SessionOrganizationID ", SessionOrganizationID)
    # print("EmployeeCode ", EmployeeCode)
    # print("year ", year)
    # print("month_no ", month_no)

    Department =''
    DepartmentList = []
    if EmployeeCode:

        Departmentobj = MultipleDepartmentofEmployee(OrganizationID, EmployeeCode)
        # print("the department object is here:",Departmentobj)

        if Departmentobj:  
            DepartmentList = Departmentobj
            # print("DepartmentList=",DepartmentList)
            
        else:
            return Error(request, "Employee Details not Found.Update in Human Resources")    
    else:
        return Error(request, "Employee Code is required. Please update it in User Details.")
                 
    if 'Human Resources' in DepartmentList:
            Department = 'hr'
    

    # UserType = str(request.session.get("UserType", '')).lower()
    # print("UserType ", UserType)
    if OrganizationID == '3' and UserType == 'hod':
        UserType = 'rd'


    # I = request.GET.get('I',OrganizationID)
    # print("I ", I)

    if OrganizationID == "3":
        I = request.GET.get('I') or 'All'

    if OrganizationID == '3':
        orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1)
    else:
        orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1, OrganizationID=OrganizationID)


    # orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1)
    Levels = LavelAdd.objects.filter(IsDelete=False)

     
        
    Level = request.GET.get('Level') or 'All'
    Status = request.GET.get('Status') or 'All'
    LOIstatus = request.GET.get('LOIstatus') or 'All'

    # print("Level ", Level)
    # print("Status ", Status)
    # print("LOIstatus ", LOIstatus)

    assessments_filter = {
        'IsDelete': False,
        'InterviewDate__year': year,
    }

    if month_no:  
        assessments_filter['InterviewDate__month'] = month_no

    
    if I != 'All':
        assessments_filter['AppliedFor'] = I
        # assessments_filter['OrganizationID'] = I
    if Level != 'All':  
        assessments_filter['Level'] = Level
    if Status != 'All':
        assessments_filter['LastApporvalStatus'] = Status
    if Status == 'All':
        STATUS_CHOICES = ['Approved', 'Pending']
        assessments_filter['LastApporvalStatus__in'] = STATUS_CHOICES
 
        
    if LOIstatus != 'All':
        assessments_filter['LOIStatus'] = LOIstatus
    

    Assessments = Assessment_Master.objects.filter(**assessments_filter).order_by('-CreatedDateTime')

    AssessmentsList = []
    for Assessment in Assessments:
        ref = 'Fresher'
        if Assessment.workexperience != 'Fresher': 
            ref = 0
            if Assessment.reference:
                refobj = ReferenceDetails.objects.filter(IsDelete=False, OrganizationID=OrganizationID, Inteview_AssementID=Assessment.id).first()
                if refobj and refobj.ref1_status == 1:
                    ref = 1
                if isinstance(Assessment.reference, str):
                    ref = 1   
        Assessment.ref = ref
        AssessmentDepartment = Assessment.Department
        head_department_obj = CheckHeadDepartment(AssessmentDepartment,Assessment.Level, OrganizationID)
        head_department = ''
        if  head_department_obj:
            # return Error(request, f"{AssessmentDepartment} head department not Found.Update in Admin of Interview Assessment")    
            head_department =  head_department_obj.HeadDepartment 
       
       
        ApprovalStageFunobj = ApprovalStageFun(Assessment.Level,Assessment.Department,Assessment.OrganizationID)
       
        Found = False
        if UserID=='20230110136226':
            Found = True
        if not ApprovalStageFunobj:
            # if((Department == 'Human Resources' or Department == "Executive Office" or Department == "Talent Acquisition and Development" or Department == "Corporate Office")):
            if ('Human Resources' in DepartmentList  or  "Executive Office" in DepartmentList or   "Talent Acquisition and Development" in DepartmentList or   "Corporate Office" in DepartmentList):
                Found=True
            else:     
                Found=False
        
       
        
        # if (Department == 'Human Resources' or Department == "Executive Office" or Department == "Talent Acquisition and Development" or Department == "Corporate Office"):
        if 'Human Resources' in DepartmentList  or  "Executive Office" in DepartmentList or   "Talent Acquisition and Development" in DepartmentList or   "Corporate Office" in DepartmentList:
            Found=True
        else:
            if UserType.lower() in [item.lower() for item in ApprovalStageFunobj]:
                Found = True
       

        if UserType != "ceo":
         
            # if (Found == True) and (Department == 'Human Resources' or Department == "Executive Office" or Department == "Talent Acquisition and Development" or  Department == "Corporate Office"):
            if (Found == True) and ('Human Resources' in DepartmentList  or  "Executive Office" in DepartmentList or   "Talent Acquisition and Development" in DepartmentList or   "Corporate Office" in DepartmentList or UserID=='20230110136226'):
                    AssessmentsList.append(Assessment)
            # elif (Department.strip() == AssessmentDepartment.strip() or Department.strip() == head_department.strip()) and   Found == True:
            elif  AssessmentDepartment.strip() in DepartmentList or  head_department.strip() in DepartmentList and   Found == True:
            
                    AssessmentsList.append(Assessment)
        
        elif  Found == True:
              AssessmentsList.append(Assessment)
                
    
    context = {
        'Assessments': AssessmentsList,
        'orgs': orgs,
        'I': I,
        'Levels': Levels,
        'Level': Level,
        'hotelapitoken': MasterAttribute.HotelAPIkeyToken,
        'Status': Status,
        'LOIstatus':LOIstatus,
        'SessionOrganizationID': SessionOrganizationID,
        'CYear': list(range(CYear, 2020, -1)),
        'CMonth': CMonth,
        'month_no': month_no if month_no else "All",
        'month_name': month_name,
        'year': year,
        'Department':Department
    }

    return render(request, 'InterviewAssessment/InterviewAssessmentList.html', context) 


