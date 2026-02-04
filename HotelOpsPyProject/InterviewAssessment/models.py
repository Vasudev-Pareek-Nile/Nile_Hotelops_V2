
from django.db import models
from datetime import datetime

from app.models import OrganizationMaster
from django.utils import timezone



class UserTypeFlow(models.Model):
    UserType = models.CharField(max_length=255,null=True,blank=False)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
  


class DepartmentLevelConfig(models.Model):
    Department =  models.CharField(max_length=255,null=True,blank=True)
    HeadDepartment =  models.CharField(max_length=255,null=True,blank=True)
    Level = models.CharField(max_length=255,null=True,blank=True)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def get_organization_name(self):
        try:
            organization = OrganizationMaster.objects.get(OrganizationID=self.OrganizationID)
            return organization.OrganizationName
        except OrganizationMaster.DoesNotExist:
            return None

    


class DepartmentLevelConfigDetails(models.Model):
    DepartmentLevelConfig = models.ForeignKey(DepartmentLevelConfig, on_delete=models.CASCADE, null=True)
    LevelSortOrder = models.CharField(max_length=255,null=True,blank=True)
    UserType = models.CharField(max_length=255,null=True,blank=True)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

from django.db.models import Q
 
    

class Assessment_Master(models.Model):
    # Interview Details
    InterviewDate = models.DateField(null=True, blank=True)
    Department = models.CharField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    Level = models.CharField(max_length=255, null=True, blank=True)

    # Candidate Details
    Prefix = models.CharField(max_length=255, null=True, blank=True) 
    Name = models.CharField(max_length=255, null=True, blank=True)
    workexperience = models.CharField(max_length=255, null=True, blank=True)
    reference = models.CharField(max_length=255, null=True, blank=True)  
    familybackground =  models.TextField(null=True, blank=True)
    pre_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    exp_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    Presentdesignation = models.CharField(max_length=255, null=True, blank=True)
    Expecteddesignation = models.CharField(max_length=255, null=True, blank=True)


    ContactNumber = models.CharField(max_length=255, null=True, blank=True)
    Email  = models.EmailField(max_length=254,null=True,blank=True)
    ProposedDOJ = models.DateField(null=True, blank=True)
    AppliedFor = models.BigIntegerField(null=True, blank=True)
    


    ResumeID = models.BigIntegerField(null=True, blank=True)
    HireFor = models.CharField(max_length=255, null=True, blank=True)

    # Assessment Status
    Status = models.IntegerField(null=True, blank=True)
    
    
    hr_as = models.CharField(max_length=255, null=True, blank=True)
    hr_as_remarks =  models.TextField(null=True, blank=True)
    hod_as = models.CharField(max_length=255, null=True, blank=True)
    hod_as_remarks =  models.TextField(null=True, blank=True)
    rd_as = models.CharField(max_length=255, null=True, blank=True)
    rd_as_remarks =  models.TextField(null=True, blank=True)
    gm_as = models.CharField(max_length=255, null=True, blank=True)
    gm_as_remarks = models.TextField(null=True, blank=True)
    ceo_as = models.CharField(max_length=255, null=True, blank=True)
    ceo_as_remarks =  models.TextField(null=True, blank=True)



    hr_UserID = models.BigIntegerField(default=0,null=True, blank=True)
    hod_UserID = models.BigIntegerField(default=0,null=True, blank=True)
    gm_UserID = models.BigIntegerField(default=0,null=True, blank=True)
    rd_UserID = models.BigIntegerField(default=0,null=True, blank=True)
    ceo_UserID = models.BigIntegerField(default=0,null=True, blank=True)


    # Action Dates
    hr_actionOn = models.DateField(null=True, blank=True)
    hr_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    
    hod_actionOn = models.DateField(null=True, blank=True)
    hod_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    
    rd_actionOn = models.DateField(null=True, blank=True)
    rd_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    
    gm_actionOn = models.DateField(null=True, blank=True)
    gm_actionOnDatetime = models.DateTimeField(null=True, blank=True)

    ceo_actionOn = models.DateField(null=True, blank=True)
    ceo_actionOnDatetime = models.DateTimeField(null=True, blank=True)

    # Employment Data
    IsEmpDataReceived = models.BooleanField(default=False)
    EmpDataReceivedID = models.BigIntegerField(null=True, blank=True)
    IsEmployeeCreated = models.BooleanField(default=False)
    GenerateLink = models.BooleanField(default=False)

    # Status Updates
    LOIStatus = models.CharField(max_length=255, null=True, blank=True,default="Pending")
    LastLoistatusModifyDate = models.DateTimeField(default=timezone.now, null=True, blank=True)
    
    ResignationStatus = models.CharField(max_length=255, null=True, blank=True,default="Pending")
    DOJStatus = models.CharField(max_length=255, null=True, blank=True)
    
    LastApporvalStatus = models.CharField(max_length=255, null=True, blank=True,default="Pending")
    LastStatusUpdateBy = models.BigIntegerField(null=True, blank=True)
    LastStatusUpdateOn = models.DateTimeField(null=True, blank=True)

    # Position Details
    PositionOpenedOn = models.DateField(null=True, blank=True)

    # File Details
    FileTitle = models.CharField(max_length=255, null=True, blank=True)
    FileName = models.CharField(max_length=255, null=True, blank=True)
    

   
   
    
    # Timestamps
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def get_organization_name(self):
        try:
            organization = OrganizationMaster.objects.get(OrganizationID=self.AppliedFor)
            return organization.OrganizationDomainCode
        except OrganizationMaster.DoesNotExist:
            return None
    
    
    
    
    
    def LoiStatus(self):
        status = self.LOIStatus
        last_modified_date = self.LastLoistatusModifyDate

        if status == "Pending":
            return f'<strong style="color: #f8ac59;">Pending</strong>'

        elif status == "Draft":
            if last_modified_date:
                days = self.days_pending(last_modified_date)
                return f'<strong style="color: #f8ac59;">Draft since {days} days</strong>'
            return f'<strong style="color: #f8ac59;">Draft</strong>'

        elif status == "Shared":
            if last_modified_date:
                days = self.days_pending(last_modified_date)
                return (f'<strong style="color: #1ab394;">Shared on {last_modified_date.strftime("%d %b")} <br>'
                        f'<strong style="color: #ED5565;">Acceptance Pending <br> from {days} days</strong>')
            return f'<strong style="color: #1ab394;">Shared</strong>'

        elif status == "Accepted":
            if last_modified_date:
                return f'<strong style="color: #1ab394;">Accepted on {last_modified_date.strftime("%d %b")}</strong>'
            return f'<strong style="color: #1ab394;">Accepted</strong>'

        elif status == "Rejected":
            if last_modified_date:
                return f'<strong style="color: #ed5565;">Rejected on {last_modified_date.strftime("%d %b")}</strong>'
            return f'<strong style="color: #ed5565;">Rejected</strong>'

        return '<strong>Status not recognized</strong>'


    
    def Approval_stage(self):
            stages = [
                ("HR", self.hr_as, self.hr_actionOnDatetime),
                ("HOD", self.hod_as, self.hod_actionOnDatetime),
                ("GM", self.gm_as, self.gm_actionOnDatetime),
                ("RD", self.rd_as, self.rd_actionOnDatetime),
                ("CEO", self.ceo_as, self.ceo_actionOnDatetime),
            ]

            latest_stage = None
            latest_datetime = None

            for role, assessment, action_date in stages:
                if action_date:  # Ensure the action date is present
                    if latest_datetime is None or action_date > latest_datetime:
                        latest_datetime = action_date
                        latest_stage = (role, assessment, action_date)

            if latest_stage:  # Ensure that a latest stage has been found
                role, assessment, action_date = latest_stage
                color = "#1ab394" if assessment == "Approved" else "#ED5565" if assessment == "Rejected" else "black"

                if role == 'HR':
                    return f'<strong style="color: green;">Generated by <br></strong>{role} on {action_date.strftime("%d %b")}'
                else:
                    approval_message = f'<strong style="color: {color};">{assessment} by <br></strong> {role}  on {action_date.strftime("%d %b")}'
                    if self.LastApporvalStatus == "Approved":
                        return f'<strong style="color: #1ab394;">{self.LastApporvalStatus}</strong>'
                    if self.LastApporvalStatus == "Rejected":
                        return f'<strong style="color: #ED5565;">{self.LastApporvalStatus}</strong>'
                    if self.LastApporvalStatus == "Closed":
                        return f'<strong style="color: #f8ac59;">{self.LastApporvalStatus}</strong>'
                    
                    return approval_message

            elif self.LastApporvalStatus == "Approved":
                        return f'<strong style="color: #1ab394;">{self.LastApporvalStatus}</strong>'
            elif self.LastApporvalStatus == "Rejected":
                        return f'<strong style="color: #ED5565;">{self.LastApporvalStatus}</strong>'
            elif self.LastApporvalStatus == "Closed":
                        return f'<strong style="color: #f8ac59;">{self.LastApporvalStatus}</strong>'
            return ''

    
    def Approval_stage_mobile_responce(self):
            stages = [
                ("HR", self.hr_as, self.hr_actionOnDatetime),
                ("HOD", self.hod_as, self.hod_actionOnDatetime),
                ("GM", self.gm_as, self.gm_actionOnDatetime),
                ("RD", self.rd_as, self.rd_actionOnDatetime),
                ("CEO", self.ceo_as, self.ceo_actionOnDatetime),
            ]

            latest_stage = None
            latest_datetime = None

            for role, assessment, action_date in stages:
                if action_date:  # Ensure the action date is present
                    if latest_datetime is None or action_date > latest_datetime:
                        latest_datetime = action_date
                        latest_stage = (role, assessment, action_date)

            if latest_stage:  # Ensure that a latest stage has been found
                role, assessment, action_date = latest_stage
                # color = "#1ab394" if assessment == "Approved" else "#ED5565" if assessment == "Rejected" else "black"

                if role == 'HR':
                    return f'Generated by {role} on {action_date.strftime("%d %b")}'
                else:
                    approval_message = f'{assessment} by {role} on {action_date.strftime("%d %b")}'
                    if self.LastApporvalStatus == "Approved":
                        return self.LastApporvalStatus
                    if self.LastApporvalStatus == "Rejected":
                        return self.LastApporvalStatus
                    if self.LastApporvalStatus == "Closed":
                        return self.LastApporvalStatus
                    
                    return approval_message

            elif self.LastApporvalStatus == "Approved":
                        return self.LastApporvalStatus
            elif self.LastApporvalStatus == "Rejected":
                        return self.LastApporvalStatus
            elif self.LastApporvalStatus == "Closed":
                        return self.LastApporvalStatus
            return ''




    
    def days_pending(self, action_datetime):
        if action_datetime:
          
            if isinstance(action_datetime, datetime):
                action_date = action_datetime.date()
            else:
                action_date = action_datetime

            today = datetime.now().date()
            delta = today - action_date
            return delta.days
        return None
    
    
    # def pending_status(self):
    #     stages_order = self.get_stages_order()  
        
    
    #     stages = {
    #         "HR": self.hr_actionOnDatetime,
    #         "HOD": self.hod_actionOnDatetime,
    #         "GM": self.gm_actionOnDatetime,
    #         "RD": self.rd_actionOnDatetime,
    #         "CEO": self.ceo_actionOnDatetime,
    #     }

      
    #     current_stage = None
    #     latest_datetime = None

      
    #     for role in stages_order:
    #         action_datetime = stages.get(role)
    #         if action_datetime:
    #             if latest_datetime is None or action_datetime > latest_datetime:
    #                 latest_datetime = action_datetime
    #                 current_stage = role

    #     if current_stage and current_stage in stages_order:
    #         current_index = stages_order.index(current_stage)
    #         if current_index + 1 < len(stages_order):
    #             next_stage = stages_order[current_index + 1]
                
    #             if self.LastApporvalStatus == 'Pending':
                
    #                 days_pending = self.days_pending(latest_datetime)
    #                 return f'<strong style="color: #f8ac59;">Pending from </strong> {next_stage} <br> since {days_pending} days'
        
    #     elif self.LastApporvalStatus == 'Pending':
    #         return f'<strong style="color: #1ab394;">{self.LastApporvalStatus}</strong>'
    #     return ''
    def pending_status(self):
            stages_order = self.get_stages_order()  

            stages = {
                "HR": self.hr_actionOnDatetime,
                "HOD": self.hod_actionOnDatetime,
                "GM": self.gm_actionOnDatetime,
                "RD": self.rd_actionOnDatetime,
                "CEO": self.ceo_actionOnDatetime,
            }

            current_stage = None
            latest_datetime = None

            # Iterate through stages in the specified order
            for role in stages_order:
                action_datetime = stages.get(role)
                if action_datetime:
                    if latest_datetime is None or action_datetime > latest_datetime:
                        latest_datetime = action_datetime
                        current_stage = role

            # If current stage is found and approval is pending
            if current_stage and current_stage in stages_order:
                current_index = stages_order.index(current_stage)
                if current_index + 1 < len(stages_order):
                    next_stage = stages_order[current_index + 1]

                    if self.LastApporvalStatus == 'Pending' and latest_datetime:
                        days_pending = self.days_pending(latest_datetime)
                        return (
                            f'<strong style="color: #f8ac59;">Pending from </strong> <br>'
                            f'{next_stage}  since {days_pending} days'
                        )

            # Fallback for cases where no specific stage is determined
            if self.LastApporvalStatus == 'Pending':
                return f'<strong style="color: #1ab394;">{self.LastApporvalStatus}</strong>'
            return ''

    def pending_status_mobile_responce(self):
            stages_order = self.get_stages_order()  

            stages = {
                "HR": self.hr_actionOnDatetime,
                "HOD": self.hod_actionOnDatetime,
                "GM": self.gm_actionOnDatetime,
                "RD": self.rd_actionOnDatetime,
                "CEO": self.ceo_actionOnDatetime,
            }

            current_stage = None
            latest_datetime = None

            # Iterate through stages in the specified order
            for role in stages_order:
                action_datetime = stages.get(role)
                if action_datetime:
                    if latest_datetime is None or action_datetime > latest_datetime:
                        latest_datetime = action_datetime
                        current_stage = role

            # If current stage is found and approval is pending
            if current_stage and current_stage in stages_order:
                current_index = stages_order.index(current_stage)
                if current_index + 1 < len(stages_order):
                    next_stage = stages_order[current_index + 1]

                    if self.LastApporvalStatus == 'Pending' and latest_datetime:
                        days_pending = self.days_pending(latest_datetime)
                        return (
                            f'Pending from '
                            f'{next_stage} since {days_pending} days'
                        )

            # Fallback for cases where no specific stage is determined
            if self.LastApporvalStatus == 'Pending':
                return self.LastApporvalStatus
            return ''

   
    def get_stages_order(self):
        department = self.Department
        level = self.Level
        org_id = self.OrganizationID  # Assuming OrganizationID is accessible

        def get_department_level_details(dept, level, org_id):
            dept_level = DepartmentLevelConfig.objects.filter(
                Department=dept,
                Level__icontains=level,
                OrganizationID=org_id,
                IsDelete=False
            ).first()
            return dept_level

        deptLevel = get_department_level_details(department, level, org_id)
        
        if not deptLevel:
            deptLevel = get_department_level_details(department, level, 3) 

        if not deptLevel:
            deptLevel = get_department_level_details('All', level, 3) 

        if deptLevel:
            stages = DepartmentLevelConfigDetails.objects.filter(
                Q(DepartmentLevelConfig__Department=department),
                DepartmentLevelConfig__Level__contains=level,IsDelete=False,OrganizationID=org_id
            ).values('UserType').order_by('LevelSortOrder')

            if not stages.exists():
                stages = DepartmentLevelConfigDetails.objects.filter(
                    Q(DepartmentLevelConfig__Department='All'),
                    DepartmentLevelConfig__Level__contains=level,IsDelete=False
                ).values('UserType').order_by('LevelSortOrder')

            stages_order = [stage['UserType'] for stage in stages]
            return stages_order
        else:
            return []  

 
    def block_lower_level_edit(self):
        stages = [
            ("HR", self.hr_as),
            ("HOD", self.hod_as),
            ("GM", self.gm_as),
            ("RD", self.rd_as),
            ("CEO", self.ceo_as),
        ]

        blocked_user_types = []

        for i, (role, assessment) in enumerate(stages):
            if assessment == "Approved":
                for j in range(i):
                    if stages[j][0] not in blocked_user_types:
                        blocked_user_types.append(stages[j][0])

        return blocked_user_types




class Assessment_Factor_Details(models.Model):
    MasterID = models.BigIntegerField(null=True, blank=True)
    OrganizationID = models.BigIntegerField(null=True, blank=True)
    factor = models.CharField(max_length=255, null=True, blank=True)
    CategoryID = models.BigIntegerField(null=True, blank=True)

 
    hr_rating = models.CharField( max_length=255,null=True,blank=True)
    hr_remarks =  models.TextField(null=True, blank=True)
    hod_rating = models.CharField( max_length=255,null=True,blank=True)
    hod_remarks = models.TextField(null=True, blank=True)
    gm_rating = models.CharField( max_length=255,null=True,blank=True)
    gm_remarks =  models.TextField(null=True, blank=True)
    rd_rating = models.CharField( max_length=255,null=True,blank=True)
    rd_remarks =  models.TextField(null=True, blank=True)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    
   





class Assessment_MasterDeletedFile(models.Model):
    Assessment_Master = models.ForeignKey(Assessment_Master, on_delete=models.CASCADE)
    FileTitle = models.CharField(max_length=255, null=True, blank=True)
    FileName = models.CharField(max_length=255, null=True, blank=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime =  models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime =  models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.FileName


class Factors(models.Model):
    Title = models.CharField(max_length=255, null=True, blank=True)
    Decription = models.TextField(null=True, blank=True)
    Item = models.JSONField(null=True, blank=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)



class EmployeeDataRequest_Master(models.Model):
    InterviewID  =models.BigIntegerField(default=0)
    TokenKey = models.CharField(null=True,blank=True,max_length=255)
    IsActive = models.BooleanField(default=False)
    ExpiryDate = models.DateField(null=True,blank=True)
    IsEmpDataReceived =  models.BooleanField(default=False)
    LOIStatus =  models.BooleanField(default=False)
    ResignationStatus = models.CharField(null=True,blank=True,max_length=255)
    DOJStatus = models.CharField(null=True,blank=True,max_length=255)
    LastStatusUpdateBy = models.BigIntegerField(default=0)
    LastStatusUpdateOn = models.DateField(null=True,blank=True)


    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)



class EmployeePersonalData(models.Model):
    DataMasterID = models.BigIntegerField(default=0)
    Prefix  = models.CharField(null=True,blank=True,max_length=255)
    FirstName = models.CharField(null=True,blank=True,max_length=255)
    MiddleName = models.CharField(null=True,blank=True,max_length=255)
    LastName = models.CharField(null=True,blank=True,max_length=255)
    Gender = models.CharField(null=True,blank=True,max_length=255)
    MaritalStatus = models.CharField(null=True,blank=True,max_length=255)
    DateofBirth = models.DateField(null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    MobileNumber = models.CharField(null=True,blank=True,max_length=255)
    EmailAddress = models.EmailField( null=True,blank=True,max_length=254)
    FileName = models.CharField(null=True,blank=True,max_length=255)
    FileTitle = models.CharField(null=True,blank=True,max_length=255)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)







class EmployeePersonalDataDeletedFile(models.Model):
    EmployeePersonalData = models.ForeignKey(EmployeePersonalData, on_delete=models.CASCADE)
    FileTitle = models.CharField(max_length=255, null=True, blank=True)
    FileName = models.CharField(max_length=255, null=True, blank=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime =  models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime =  models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.FileName



class EmployeeFamilyData(models.Model):
    MasterID = models.BigIntegerField(default=0)
    SpouseName = models.CharField(null=True,blank=True,max_length=255)
    SpouseDateofBirth = models.DateField(null=True,blank=True)
    SpouseAge  = models.IntegerField(default=0)
    SpouseContactNo  = models.CharField(null=True,blank=True,max_length=255)

    MotherName = models.CharField(null=True,blank=True,max_length=255)
    MotherDateofBirth = models.DateField(null=True,blank=True)
    MotherAge  = models.IntegerField(default=0)
    MotherContactNo  = models.CharField(null=True,blank=True,max_length=255)

    FatherName = models.CharField(null=True,blank=True,max_length=255)
    FatherDateofBirth = models.DateField(null=True,blank=True)
    FatherAge  = models.IntegerField(default=0)
    FatherContactNo  = models.CharField(null=True,blank=True,max_length=255)
    
    LandlineNo = models.CharField(null=True,blank=True,max_length=255)


    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)




class EmployeeChildData(models.Model):
    FamilyID = models.BigIntegerField(default=0)
    Name = models.CharField(null=True,blank=True,max_length=255)
    Age  = models.BigIntegerField(default=0)
    Relation = models.CharField(null=True,blank=True,max_length=255)


    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)




class EmployeeEmergencyInfoData(models.Model):
    MasterID = models.BigIntegerField(default=0)
    Prefix  = models.CharField(null=True,blank=True,max_length=255)
    FirstName = models.CharField(null=True,blank=True,max_length=255)
    MiddleName = models.CharField(null=True,blank=True,max_length=255)
    LastName = models.CharField(null=True,blank=True,max_length=255)
    Relation = models.CharField(null=True,blank=True,max_length=255)
    EmergencyContactNumber_1 = models.CharField(null=True,blank=True,max_length=255)
    EmergencyContactNumber_2 = models.CharField(null=True,blank=True,max_length=255)
    ProvidentFundNumber  = models.CharField(null=True,blank=True,max_length=255)
    ESINumber = models.CharField(null=True,blank=True,max_length=255)
    BloodGroup = models.CharField(null=True,blank=True,max_length=255)


    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)


class EmployeeEducationData(models.Model):
    MasterID = models.BigIntegerField(default=0)
    EducationType = models.CharField(null=True,blank=True,max_length=255)
    Degree_Course  = models.CharField(null=True,blank=True,max_length=255)
    NameoftheInstitution = models.CharField(null=True,blank=True,max_length=255)
    Year =  models.BigIntegerField(default=0)
    Percentage = models.BigIntegerField(default=0)
    FileName = models.CharField(null=True,blank=True,max_length=255)
    FileTitle = models.CharField(null=True,blank=True,max_length=255)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)




class EmployeePreviousWorkData(models.Model):
    MasterID = models.BigIntegerField(default=0)
    Company = models.CharField(null=True,blank=True,max_length=255)
    Position  = models.CharField(null=True,blank=True,max_length=255)
    FromDate = models.DateField(null=True,blank=True)
    ToDate =  models.DateField(null=True,blank=True)
    
    # IsPresent = models.BooleanField(default=False)

    FileName = models.CharField(null=True,blank=True,max_length=255)
    FileTitle = models.CharField(null=True,blank=True,max_length=255)
    Salary = models.BigIntegerField(default=0)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)




class EmployeeAddressInfoData(models.Model):
    MasterID = models.BigIntegerField(default=0)
    Permanent_Address  = models.CharField(null=True,blank=True,max_length=255)
    Permanent_City   = models.CharField(null=True,blank=True,max_length=255)
    Permanent_State  = models.CharField(null=True,blank=True,max_length=255)
    Permanent_Pincode  = models.BigIntegerField(default=0)
    Permanent_HousePhoneNumber  = models.CharField(null=True,blank=True,max_length=255)

    Temporary_Address  = models.CharField(null=True,blank=True,max_length=255)
    Temporary_City   = models.CharField(null=True,blank=True,max_length=255)
    Temporary_State  = models.CharField(null=True,blank=True,max_length=255)
    Temporary_Pincode  = models.BigIntegerField(default=0)
    Temporary_HousePhoneNumber  = models.CharField(null=True,blank=True,max_length=255)


    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)





class EmployeeIdentityInfoData(models.Model):
    MasterID = models.BigIntegerField(default=0)
    PANNo = models.CharField(null=True,blank=True,max_length=255)
    PanFileName = models.CharField(null=True,blank=True,max_length=255)
    PanFileTitle = models.CharField(null=True,blank=True,max_length=255)

    AadhaarNumber   = models.CharField(null=True,blank=True,max_length=255)
    AadhaarFileName = models.CharField(null=True,blank=True,max_length=255)
    AadhaarFileTitle = models.CharField(null=True,blank=True,max_length=255)

    DrivingLicenceNo   = models.CharField(null=True,blank=True,max_length=255)
    DrivingFileName = models.CharField(null=True,blank=True,max_length=255)
    DrivingFileTitle = models.CharField(null=True,blank=True,max_length=255)


    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)




class EmployeeBankInfoData(models.Model):
    MasterID = models.BigIntegerField(default=0)
    BankAccountNumber = models.CharField(null=True,blank=True,max_length=255)
    NameofBank   = models.CharField(null=True,blank=True,max_length=255)
    BankBranch   = models.CharField(null=True,blank=True,max_length=255)
    IFSCCode   = models.CharField(null=True,blank=True,max_length=255)


    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)







class EmployeeDocumentsInfoData(models.Model):
    MasterID = models.BigIntegerField(default=0)
    Title = models.CharField(null=True,blank=True,max_length=255)
    FileName = models.CharField(null=True,blank=True,max_length=255)
    FileTitle = models.CharField(null=True,blank=True,max_length=255)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)



class CandidateUrlMaster(models.Model):
    UrlName  = models.CharField(max_length=255)
    sortorder = models.IntegerField()

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
