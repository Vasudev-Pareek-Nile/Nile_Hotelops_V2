from django.db import models
from datetime import datetime,date,timedelta

from app.models import OrganizationMaster 

from django.utils import timezone








# Objective_Master

class Objective_Master(models.Model):
    Level=models.CharField(max_length=255,null=False,blank=False)
    Title=models.CharField(max_length=255,null=False,blank=False)
    Definitions = models.TextField()
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Title



# Attribute Master
class Attribute_Master(models.Model):
    Objective_Master=models.ForeignKey(Objective_Master,on_delete=models.CASCADE)
    Title=models.CharField(max_length=255,null=False,blank=False)
    
    RL_H = models.BooleanField(default=False)
    RL_M = models.BooleanField(default=False)
    RL_L = models.BooleanField(default=False)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Title




# Ineffective Indicators Master
class Ineffective_Indicators_Master(models.Model):
    Objective_Master=models.ForeignKey(Objective_Master,on_delete=models.CASCADE)
    Title=models.CharField(max_length=255,null=False,blank=False)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.Title} {self.Objective_Master.Title}' 


# Effective Indicators Master
class Effective_Indicators_Master(models.Model):
    Objective_Master=models.ForeignKey(Objective_Master,on_delete=models.CASCADE)
    Title=models.CharField(max_length=255,null=False,blank=False)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)   
    
    def __str__(self):
        return f'{self.Title} {self.Objective_Master.Title}' 
 



# PADP_Approval_Master 
class  PADP_Approval_Mapping_Master(models.Model):
    Appraisee_Level = models.CharField(max_length =255,null=False,blank=False)
    Approval_Level = models.CharField(max_length =255,null=False,blank=False)
    Next_Aprroval_Level = models.CharField(max_length =255,null=False,blank=False)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self) -> str:
        return f'Appraisee_Level={str(self.Appraisee_Level)},Approval_Level={str(self.Approval_Level)},Next_Aprroval_Level=,{str(self.Next_Aprroval_Level)}'


    
def Get_next_approval_level(Appraisee_Level,Approval_Status):
    if Appraisee_Level == "M":
        Appraisee_Level = Appraisee_Level + "/"
    
    Next_Aprroval_Level = PADP_Approval_Mapping_Master.objects.get(Appraisee_Level__icontains=Appraisee_Level,Approval_Level__icontains= Approval_Status)
    return Next_Aprroval_Level.Next_Aprroval_Level





# Entry_Master
class Entry_Master(models.Model):
    EmployeeCode = models.CharField(max_length=255,null=False,blank=False)
    EmployeeOrganizationID = models.BigIntegerField(default=0)

    # Review_Date = models.DateField(default=date.today())
    Appraisee_Name = models.CharField(max_length=255,null=False,blank=False)
    Aprraisee_position = models.CharField(max_length=255,null=False,blank=False)
    Date_Joined_Company = models.DateField(default=timezone.now)
    Appraisor_Name = models.CharField(max_length=255,null=False,blank=False)
    Appraisor_Title  = models.CharField(max_length=255,null=False,blank=False)
    FromReviewDate = models.DateField(null=True, blank=True)
    ToReviewDate = models.DateField(null=True, blank=True)

    Current_Salary  = models.CharField(max_length=255,null=True,blank=True)
    Department  = models.CharField(max_length=255,null=True,blank=True)

    
    ReportingtoDesigantion = models.CharField(max_length=255,null=False,blank=False)
    
    DottedLine = models.CharField(max_length=255,null=False,blank=False)
    
    Aprraise_Level = models.CharField(max_length=255,null=False,blank=False)
    
    Status = models.IntegerField(null=True, blank=True)
    
    LastApporvalStatus = models.CharField(max_length=255, null=True, blank=True,default="Pending")
    hr_as = models.CharField(max_length=255, null=True, blank=True)
    ep_as = models.CharField(max_length=255, null=True, blank=True)
    ar_as = models.CharField(max_length=255, null=True, blank=True)
    rd_as = models.CharField(max_length=255, null=True, blank=True)
    hr_ar = models.CharField(max_length=255, null=True, blank=True)
    
    ceo_as = models.CharField(max_length=255, null=True, blank=True)
    ceo_as_remarks  =  models.TextField(null=True,blank=True)
   
    # Action Dates
    hr_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    ep_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    ar_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    rd_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    hr_ar_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    
    ceo_actionOnDatetime = models.DateTimeField(null=True, blank=True)


    # New fields
    Last_CEO_Action = models.CharField(max_length=255, null=True, blank=True)   # NEW FIELD
    Last_CEO_action_On = models.DateTimeField(null=True, blank=True)  # NEW FIELD
    Last_CEO_action_Remarks = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD

    Last_Action_By_EmpCode = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD
    Last_Action_By_Name = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD

    # Pending_From_Emp_Code = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD
    # Pending_From_Emp_Name = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD
    
    
    AuditedBy = models.CharField(max_length=255,null=True,blank=True)
    AuditedBy_Name = models.CharField(max_length=255,null= True,blank =True )
    HR_Manager_Name = models.CharField(max_length=255,null= True,blank =True )

    DraftBy=models.CharField(max_length=255,null= True,blank =True )
    DraftByName=models.CharField(max_length=255,null= True,blank =True )
    DraftByDateTime= models.DateTimeField(default=timezone.now, null= True,blank =True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedByUsername =  models.CharField(max_length=255,null=True,blank=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    DottedLine_Name = models.CharField(max_length=255,null= True,blank =True )
    
    def __str__(self):
        return self.Appraisee_Name
    
        
    def get_organization_name(self):
        try:
            organization = OrganizationMaster.objects.get(OrganizationID=self.OrganizationID)
            return organization.ShortDisplayLabel
        except OrganizationMaster.DoesNotExist:
            return None

    def get_first_last(name):
                if name:
                    parts = name.strip().split()
                    if len(parts) >= 2:
                        return f"{parts[0]} {parts[-1]}"
                    return parts[0]
                return None
    def get_role_name(self, role):
        def get_first_last(name):
            if name:
                parts = name.strip().split()
                if len(parts) >= 2:
                    return f"{parts[0]} {parts[-1]}"
                return parts[0]
            return None
        AppraisorTitle = self.Appraisor_Title
        DottedLineValue = self.DottedLine
        
        
        if role == 'EP':
            return get_first_last(self.Appraisee_Name) or "EP"

        elif role == 'AR':
            return get_first_last(self.Appraisor_Name) or "AR"

        elif role == 'HRA':
            if self.AuditedBy_Name:
                HRA_Action = get_first_last(self.AuditedBy_Name)
            else:
                HRA_Action = get_first_last(self.CreatedByUsername)
            return HRA_Action or "HRA"

        elif role == 'HR':
            return get_first_last(self.CreatedByUsername) or "HR"

        elif role == 'RD':
            if AppraisorTitle.strip().lower() == DottedLineValue.strip().lower():
                return get_first_last(self.Appraisor_Name) or "RD"

            try:
                matching_work = EmployeeWorkDetails.objects.filter(
                    EmpStatus__in=('Confirmed', 'On Probation', 'Not Confirmed'),
                    Designation__iexact=DottedLineValue,
                    OrganizationID=self.OrganizationID,
                    IsDelete=False,
                    IsSecondary=False
                ).values_list('EmpID', flat=True).first()

                if matching_work:
                    personal = EmployeePersonalDetails.objects.filter(EmpID=matching_work).first()
                    if personal:
                        return f"{personal.FirstName} {personal.LastName}"
            except Exception as e:
                print(f"Error in RD role name fetch: {e}")
            return "RD"

        return role
  

    def Approval_stage(self):
        # stages = [
        #     ("HR", self.hr_as, self.hr_actionOnDatetime, 1, 1 if self.hr_as == "Submitted" else 0),
        #     ("EP", self.ep_as, self.ep_actionOnDatetime, 2, 1 if self.ep_as == "Submitted" else 0),
        #     ("AR", self.ar_as, self.ar_actionOnDatetime, 3, 1 if self.ar_as == "Submitted" else 0),
        #     ("RD", self.rd_as, self.rd_actionOnDatetime, 4, 1 if self.rd_as == "Submitted" else 0),
        #     # ("HRA", self.hr_ar, self.hr_ar_actionOnDatetime, 5, 1 if self.hr_ar == "Audited" else 0),
        #     ("HRA", self.hr_ar, self.hr_ar_actionOnDatetime, 5, 1 if self.ceo_as in ["Audited", "Draft"] else 0),
        #     ("CEO", self.ceo_as, self.ceo_actionOnDatetime, 6, 1 if self.ceo_as in ["Approved", "Returned"] else 0),

        #     # ("CEO", self.ceo_as, self.ceo_actionOnDatetime, 6, 1 if self.ceo_as == "Approved" else 0),
        # ]

        stages = [
            ("HR", self.hr_as, self.hr_actionOnDatetime, 1, 1 if self.hr_as == "Submitted" else 0),
            ("EP", self.ep_as, self.ep_actionOnDatetime, 2, 1 if self.ep_as == "Submitted" else 0),
            ("AR", self.ar_as, self.ar_actionOnDatetime, 3, 1 if self.ar_as == "Submitted" else 0),
        ]

        # Conditionally include RD only when DottedLine ≠ Aprraisee_position
        if self.DottedLine.strip().lower() != self.Aprraisee_position.strip().lower():
            stages.append(("RD", self.rd_as, self.rd_actionOnDatetime, 4, 1 if self.rd_as == "Submitted" else 0))
            hra_order = 5
            ceo_order = 6
        else:
            hra_order = 4
            ceo_order = 5

        # Always include HRA and CEO stages
        stages.append(("HRA", self.hr_ar, self.hr_ar_actionOnDatetime, hra_order, 1 if self.hr_ar == "Audited" else 0))
        stages.append(("CEO", self.ceo_as, self.ceo_actionOnDatetime, ceo_order, 1 if self.ceo_as in ["Approved", "Returned"] else 0))

        # Sort stages by defined sequence
        stages.sort(key=lambda x: x[3])

        # Track latest submitted stage
        last_submitted = None
        pending_from = None
        latest_stage = None
        latest_datetime = None

        is_first_hr_action = self.hr_actionOnDatetime and self.hr_as == "Submitted"

        for role, status, action_date, order, flag in stages:
            # Track last submitted stage for pending logic
            if flag == 1:
                last_submitted = (role, action_date, status)

            elif flag == 0 and last_submitted and not pending_from:
                # pending_from = role
                # pending_from = (role, action_date)
                pending_from = (role, last_submitted[1])


            # Track latest stage based on datetime
            if action_date:
                if latest_datetime is None or action_date > latest_datetime:
                    latest_datetime = action_date
                    latest_stage = (role, status, action_date)

        # Construct final message parts
        submitted_msg = ""
        pending_msg = ""
        approval_msg = ""

        if last_submitted:
            role, date, status = last_submitted
            submitted_msg = f'<strong style="color: #1ab394;">{status} by <br></strong>{self.get_role_name(role)}'
            # submitted_msg = f'<strong style="color: #1ab394;">Submitted by </strong>{self.get_role_name(role)}'
            if date:
                submitted_msg += f' on {date.strftime("%d %b")}'

        # if pending_from:
        #     pending_msg = f'<strong style="color: #f8ac59;"><br>Pending from </strong>{self.get_role_name(pending_from)}'

        # if pending_from:
        #     role, date = pending_from
        #     days = self.days_pending(date)
        #     pending_msg = f'<strong style="color: #f8ac59; display:block;">Pending from <br></strong>{self.get_role_name(role)}'
        #     if days is not None:
        #         pending_msg += f' <strong>Since {days} day{"s" if days != 1 else ""}</strong>'


        if pending_from:
            role, date = pending_from
            days = self.days_pending(date)
            pending_status = ""  # will be either "Pending from" or "Draft by"

            # Get the actual status for this role
            status_lookup = {
                "HR": self.hr_as,
                "EP": self.ep_as,
                "AR": self.ar_as,
                "RD": self.rd_as,
                "HRA": self.hr_ar,
                "CEO": self.ceo_as,
            }

            current_status = status_lookup.get(role, "")

            if current_status == "Draft":
                pending_status = f'<strong style="color: #f8ac59; display:block;">Draft by <br></strong>'
            else:
                pending_status = f'<strong style="color: #f8ac59; display:block;">Pending from <br></strong>'

            pending_msg = pending_status + self.get_role_name(role)
            if days is not None:
                pending_msg += f' <strong>Since {days} day{"s" if days != 1 else ""}</strong>'



        if latest_stage:
            role, assessment, action_date = latest_stage
            color = "#1ab394" if assessment in ["Approved", "Submitted", "Audited"] else "#f8ac59" if assessment == "Draft" else "#ED5565"
            role_display_name = self.get_role_name(role)

            if role == "HR" and is_first_hr_action:
            # if role == self.CreatedByUsername and is_first_hr_action:
                approval_msg = f'<strong style="color: {color};">Created by </strong>{role_display_name}<br> on {action_date.strftime("%d %b")}'
            else:
                approval_msg = f'<strong style="color: {color};">{assessment} by </strong> {role_display_name}<br> on {action_date.strftime("%d %b")}'

        if self.LastApporvalStatus == "Approved":
            return f'<strong style="color: #1ab394;">{self.LastApporvalStatus}</strong>'
        elif self.LastApporvalStatus == "Rejected":
            return f'<strong style="color: #ED5565;">{self.LastApporvalStatus}</strong>'

        # Return either approval + pending, or fallback to just latest stage
        return submitted_msg + pending_msg if submitted_msg or pending_msg else approval_msg

    def Approval_stage_Mobile_Api(self):
        stages = [
            ("HR", self.hr_as, self.hr_actionOnDatetime, 1, 1 if self.hr_as == "Submitted" else 0),
            ("EP", self.ep_as, self.ep_actionOnDatetime, 2, 1 if self.ep_as == "Submitted" else 0),
            ("AR", self.ar_as, self.ar_actionOnDatetime, 3, 1 if self.ar_as == "Submitted" else 0),
        ]

        # Conditionally include RD only when DottedLine ≠ Aprraisee_position
        if self.DottedLine.strip().lower() != self.Aprraisee_position.strip().lower():
            stages.append(("RD", self.rd_as, self.rd_actionOnDatetime, 4, 1 if self.rd_as == "Submitted" else 0))
            hra_order = 5
            ceo_order = 6
        else:
            hra_order = 4
            ceo_order = 5

        # Always include HRA and CEO stages
        stages.append(("HRA", self.hr_ar, self.hr_ar_actionOnDatetime, hra_order, 1 if self.hr_ar == "Audited" else 0))
        stages.append(("CEO", self.ceo_as, self.ceo_actionOnDatetime, ceo_order, 1 if self.ceo_as in ["Approved", "Returned"] else 0))

        # Sort stages by defined sequence
        stages.sort(key=lambda x: x[3])

        # Track latest submitted stage
        last_submitted = None
        pending_from = None
        latest_stage = None
        latest_datetime = None

        is_first_hr_action = self.hr_actionOnDatetime and self.hr_as == "Submitted"

        for role, status, action_date, order, flag in stages:
            # Track last submitted stage for pending logic
            if flag == 1:
                last_submitted = (role, action_date, status)

            elif flag == 0 and last_submitted and not pending_from:
                # pending_from = role
                # pending_from = (role, action_date)
                pending_from = (role, last_submitted[1])


            # Track latest stage based on datetime
            if action_date:
                if latest_datetime is None or action_date > latest_datetime:
                    latest_datetime = action_date
                    latest_stage = (role, status, action_date)

        # Construct final message parts
        submitted_msg = ""
        pending_msg = ""
        approval_msg = ""

        if last_submitted:
            role, date, status = last_submitted
            submitted_msg = f'{status} by {self.get_role_name(role)}'
            # submitted_msg = f'<strong style="color: #1ab394;">Submitted by </strong>{self.get_role_name(role)}'
            if date:
                submitted_msg += f' on {date.strftime("%d %b")}'

        if pending_from:
            role, date = pending_from
            days = self.days_pending(date)
            pending_status = ""  # will be either "Pending from" or "Draft by"

            # Get the actual status for this role
            status_lookup = {
                "HR": self.hr_as,
                "EP": self.ep_as,
                "AR": self.ar_as,
                "RD": self.rd_as,
                "HRA": self.hr_ar,
                "CEO": self.ceo_as,
            }

            current_status = status_lookup.get(role, "")

            if current_status == "Draft":
                pending_status = f'Draft by '
            else:
                pending_status = f' Pending from '

            pending_msg = pending_status + self.get_role_name(role)
            if days is not None:
                pending_msg += f' Since {days} day{"s" if days != 1 else ""}'



        if latest_stage:
            role, assessment, action_date = latest_stage
            color = "#1ab394" if assessment in ["Approved", "Submitted", "Audited"] else "#f8ac59" if assessment == "Draft" else "#ED5565"
            role_display_name = self.get_role_name(role)

            if role == "HR" and is_first_hr_action:
            # if role == self.CreatedByUsername and is_first_hr_action:
                approval_msg = f'Created by {role_display_name} on {action_date.strftime("%d %b")}'
            else:
                approval_msg = f'{assessment} by {role_display_name} on {action_date.strftime("%d %b")}'

        if self.LastApporvalStatus == "Approved":
            return f'{self.LastApporvalStatus}'
        elif self.LastApporvalStatus == "Rejected":
            return f'{self.LastApporvalStatus}'

        # Return either approval + pending, or fallback to just latest stage
        return submitted_msg + pending_msg if submitted_msg or pending_msg else approval_msg

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

    def get_stages_order(self):
         return ["HR", "EP", "AR", "RD","HRA","CEO"]

    

# Log table for Entry_Master
# Need to comment while upload code to live
class Entry_Master_Log(models.Model):
    Entry_Master  = models.ForeignKey(Entry_Master,on_delete=models.CASCADE)
    LastApporvalStatus = models.CharField(max_length=255, null=True, blank=True,default="Pending")
    hr_as = models.CharField(max_length=255, null=True, blank=True)
    ep_as = models.CharField(max_length=255, null=True, blank=True)
    ar_as = models.CharField(max_length=255, null=True, blank=True)
    rd_as = models.CharField(max_length=255, null=True, blank=True)
    hr_ar = models.CharField(max_length=255, null=True, blank=True)
    
    ceo_as = models.CharField(max_length=255, null=True, blank=True)
    ceo_as_remarks  =  models.TextField(null=True,blank=True)
   
    # Action Dates
    hr_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    ep_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    ar_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    rd_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    hr_ar_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    
    ceo_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    

    OrganizationID = models.BigIntegerField(default=0)
    CreatedByUsername =  models.CharField(max_length=255,null=True,blank=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)


# Approval_Submit_Status
class Approval_Submit_Status_PADP(models.Model):
    Entry_Master  = models.ForeignKey(Entry_Master,on_delete=models.CASCADE)
    Approval_Status = models.CharField(max_length=255,null=False,blank=False)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False) 
    def __str__(self):
        return f'{self.Entry_Master.EmployeeCode }   {self.Entry_Master.Appraisee_Name} {self.id} {self.Approval_Status}'




# Leadership_Details
class Leadership_Details(models.Model):
    Entry_Master=models.ForeignKey(Entry_Master,on_delete=models.CASCADE)
    Objective_Master=models.ForeignKey(Objective_Master,on_delete=models.CASCADE)
    Appraise_Comments = models.TextField(null=False,blank=False)
    Appraisor_Comments = models.TextField(null=False,blank=False)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.Entry_Master.Review_Date} {self.Objective_Master}'
     


    
# Leadership_AttributeDetails

# Leadership_Details
class Leadership_AttributeDetails(models.Model):
    Leadership_Details=models.ForeignKey(Leadership_Details,on_delete=models.CASCADE)
    Attribute_Master=models.ForeignKey(Attribute_Master,on_delete=models.CASCADE)
    
    RL_L = models.BooleanField(default=False)
    RL_H = models.BooleanField(default=False)
    RL_M = models.BooleanField(default=False)

    Does_NOT_Appee = models.BooleanField(default=False)
    Does_NOT_Appor = models.BooleanField(default=False)
    
    Rarely_Appee = models.BooleanField(default=False)
    Rarely_Appor = models.BooleanField(default=False)

    Sometiems_Appee = models.BooleanField(default=False)
    Sometiems_Appor = models.BooleanField(default=False)

    Often_Appee = models.BooleanField(default=False)
    Often_Appor = models.BooleanField(default=False)
    
    Always_Appee = models.BooleanField(default=False)
    Always_Appor = models.BooleanField(default=False)
    
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.Leadership_Details} {self.Attribute_Master}'
    


# Effectieve Indicators  Details Appraisee 
class Effective_Indicators_Details_Appraisee(models.Model):
    Entry_Master=models.ForeignKey(Entry_Master,on_delete=models.CASCADE)
    Objective_Master=models.ForeignKey(Objective_Master,on_delete=models.CASCADE)
    Effective_Indicators_Master=models.ForeignKey(Effective_Indicators_Master,on_delete=models.CASCADE)
    Status = models.BooleanField(default=False) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)   
    
    def __str__(self):
        return f'{self.Entry_Master.Appraisee_Name} {self.Effective_Indicators_Master.Title}'
   

# Ineffective Indicators Details Appraisee
class Ineffective_Indicators_Details_Appraisee(models.Model):
    Entry_Master=models.ForeignKey(Entry_Master,on_delete=models.CASCADE)
    Objective_Master=models.ForeignKey(Objective_Master,on_delete=models.CASCADE)
    Ineffective_Indicators_Master=models.ForeignKey(Ineffective_Indicators_Master,on_delete=models.CASCADE)
    Status = models.BooleanField(default=False) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.Entry_Master.Appraisee_Name} {self.Ineffective_Indicators_Master.Title}'      
    



# Effectieve Indicators  Details Appraisor 
class Effective_Indicators_Details_Appraisor(models.Model):
    Entry_Master=models.ForeignKey(Entry_Master,on_delete=models.CASCADE)
    Objective_Master=models.ForeignKey(Objective_Master,on_delete=models.CASCADE)
    Effective_Indicators_Master=models.ForeignKey(Effective_Indicators_Master,on_delete=models.CASCADE)
    Status = models.BooleanField(default=False) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)   
    
    def __str__(self):
        return f'{self.Entry_Master.Appraisee_Name} {self.Effective_Indicators_Master.Title}'
   

# Ineffective Indicators Details Appraisor
class Ineffective_Indicators_Details_Appraisor(models.Model):
    Entry_Master=models.ForeignKey(Entry_Master,on_delete=models.CASCADE)
    Objective_Master=models.ForeignKey(Objective_Master,on_delete=models.CASCADE)
    Ineffective_Indicators_Master=models.ForeignKey(Ineffective_Indicators_Master,on_delete=models.CASCADE)
    Status = models.BooleanField(default=False) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.Entry_Master.Appraisee_Name} {self.Ineffective_Indicators_Master.Title}' 




# SPECIFIC_MEASURABLE_ACHIEVABLE

class SPECIFIC_MEASURABLE_ACHIEVABLE(models.Model):
    Entry_Master=models.ForeignKey(Entry_Master,on_delete=models.CASCADE)
    Objective_Master=models.ForeignKey(Objective_Master,on_delete=models.CASCADE)
    Month_View  = models.TextField(null=False,blank=False)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.Objective_Master.Title

# SPECIFIC_MEASURABLE_ACHIEVABLE_Details
class SPECIFIC_MEASURABLE_ACHIEVABLE_Details(models.Model):
    SPECIFIC_MEASURABLE_ACHIEVABLE = models.ForeignKey(SPECIFIC_MEASURABLE_ACHIEVABLE,on_delete=models.CASCADE)

    SMART_GOAL =  models.TextField(null=False,blank=False)
    ACTION_STEPS = models.TextField(null=False,blank=False)
    COMPLETION_DATE = models.CharField(null=False,blank=False,max_length=255)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.SPECIFIC_MEASURABLE_ACHIEVABLE} =>> {self.SMART_GOAL} =>> {self.ACTION_STEPS} ==> {self.COMPLETION_DATE}' 

# SUMMARY AND ACKNOWLEDGEMENT
class SUMMARY_AND_ACKNOWLEDGEMENT(models.Model):
    Entry_Master = models.ForeignKey(Entry_Master,on_delete=models.CASCADE) 
    
    SUMMARY_APPRAISEE = models.TextField(null=False,blank=False)
    SUMMARY_APPRAISOR = models.TextField(null=False,blank=False)
    SP_GM_Rating_Excellent = models.BooleanField(default =False)
    SP_GM_Rating_Good = models.BooleanField(default =False)
    SP_GM_Rating_Average = models.BooleanField(default =False)
    SP_GM_Rating_Poor = models.BooleanField(default =False)
    SP_GM_Rating_Needs_Improvement = models.BooleanField(default =False)
    SP_GM_Comment = models.TextField(null=False,blank=False)

    RD_Rating_Excellent = models.BooleanField(default =False)
    RD_Rating_Good = models.BooleanField(default =False)
    RD_Rating_Average = models.BooleanField(default =False)
    RD_Rating_Poor = models.BooleanField(default =False)
    RD_Rating_Needs_Improvement = models.BooleanField(default =False)
    RD_Comment = models.TextField(null=False,blank=False)


    Appraisee = models.CharField(max_length=255,null=False,blank=False)
    Appraisor = models.CharField(max_length=255,null=False,blank=False)
    HR_Manager = models.CharField(max_length=255,null=False,blank=False) 
    Appraisor_Mgr = models.CharField(max_length=255,null=False,blank=False)
    
    Anticipated_promotionffransfer_Date = models.DateField(null=True, blank=True)

    Position = models.CharField(max_length=255,null=False,blank=False)
    Alternative_Position = models.CharField(max_length=255,null=False,blank=False)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)


# FINAL PERFORMANCE RATING
class FINAL_PERFORMANCE_RATING(models.Model):
    Entry_Master = models.ForeignKey(Entry_Master,on_delete=models.CASCADE)
    DEFICIENT = models.BooleanField(default=False)
    BELOW_STANDARD = models.BooleanField(default=False)
    MEETS_EXPECTATION = models.BooleanField(default=False)
    ABOVE_STANDARD = models.BooleanField(default=False)
    OUTSTANDING = models.BooleanField(default=False)
    
    NO_CORRECTION = models.BooleanField(default=False)
    per_3 = models.BooleanField(default=False)
    per_5 = models.BooleanField(default=False)
    per_8 = models.BooleanField(default=False)
    per_10 = models.BooleanField(default=False)


    SALARY_CORRECTION = models.BooleanField(default=False)
    PROMOTION = models.BooleanField(default=False)
    PROMOTION_WITH_INCREASE = models.BooleanField(default=False)
    
    FromSalary =  models.DecimalField(max_digits=12, decimal_places=2,null= True,blank =True)
    ToSalary = models.DecimalField(max_digits=12, decimal_places=2,null= True,blank =True)
    FromPosition = models.CharField(max_length=255,null= True,blank =True )
    ToPosition = models.CharField(max_length=255,null= True,blank =True)
    JustificationComments = models.TextField(null=True,blank=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    

  
from datetime import datetime, timedelta

def calculate_appraisal_date(joining_date):
    if isinstance(joining_date, str):
        joining_date = datetime.strptime(joining_date, '%Y-%m-%d')
    else:
        joining_date = datetime.combine(joining_date, datetime.min.time())
        
    current_year = datetime.now().year
    appraisal_date = datetime(current_year, joining_date.month, joining_date.day)
    
    if appraisal_date <= joining_date:
        appraisal_date = datetime(current_year + 1, joining_date.month, joining_date.day)
    
    appraisal_date += timedelta(days=1)
    formatted_appraisal_date = appraisal_date.strftime('%Y-%m-%d')
    
    return formatted_appraisal_date

def days_in_current_year():
    current_year = datetime.now().year
    start_of_year = datetime(current_year, 1, 1)
    end_of_year = datetime(current_year, 12, 31)
    return (end_of_year - start_of_year).days + 1

def calculate_next_date(joining_date):
    if isinstance(joining_date, str):
        joining_date = datetime.strptime(joining_date, '%Y-%m-%d')
    else:
        joining_date = datetime.combine(joining_date, datetime.min.time())
    
    current_year = datetime.now().year
    next_date = datetime(current_year, joining_date.month, joining_date.day)
    
    if next_date <= joining_date:
        next_date = datetime(current_year + 1, joining_date.month, joining_date.day)
    
    Total_Days = days_in_current_year()
    next_date += timedelta(days=Total_Days) + timedelta(days=1)
    formatted_next_date = next_date.strftime('%Y-%m-%d')
    
    return formatted_next_date



class Master_APADP_Item(models.Model):
    ItemName = models.CharField(max_length=255,null= True,blank =True )
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.ItemName

class Master_APADP_SubItem(models.Model):
    Master_APADP_Item = models.ForeignKey(Master_APADP_Item,on_delete=models.CASCADE)
    SubItemName = models.CharField(max_length=255,null= True,blank =True )
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False) 


from HumanResources.views import EmployeePersonalDetails, EmployeeWorkDetails

class APADP(models.Model): 
    EmployeeCode = models.CharField(max_length=255,null= True,blank =True )
    EmpName = models.CharField(max_length=255,null= True,blank =True )
    Designation = models.CharField(max_length=255,null= True,blank =True )
    Department = models.CharField(max_length=255,null= True,blank =True )
    Level = models.CharField(max_length=255,null= True,blank =True )
    ReportingtoDesigantion = models.CharField(max_length=255,null= True,blank =True )
    ReportingtoLevel = models.CharField(max_length=255,null= True,blank =True )
    DateofJoining = models.CharField(max_length=255,null= True,blank =True )
    Tenure = models.CharField(max_length=255,null= True,blank =True )
    review_from_date = models.CharField(max_length=255,null= True,blank =True )
    review_to_date = models.CharField(max_length=255,null= True,blank =True )
    Development=models.CharField(max_length=255,null= True,blank =True )
    Reporting_To_Name=models.CharField(max_length=255,null= True,blank =True )
    HR_Manager=models.CharField(max_length=255,null= True,blank =True)


    Current_Salary  = models.CharField(max_length=255,null=True,blank=True)




    # Finalcomments = models.CharField(max_length=255,null= True,blank =True)
    
    Finalcomments = models.TextField(null= True,blank =True)


    Status = models.BooleanField(default=False)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedByUsername = models.CharField(max_length=255,null= True,blank =True )

    DraftBy=models.CharField(max_length=255,null= True,blank =True )
    DraftByName=models.CharField(max_length=255,null= True,blank =True )
    DraftByDateTime=models.DateTimeField(default=timezone.now, null= True,blank =True)

    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False) 

    AuditedBy = models.CharField(max_length=255,null=True,blank=True)
    AuditedBy_Name = models.CharField(max_length=255,null= True,blank =True )
    
    LastApporvalStatus = models.CharField(max_length=255, null=True, blank=True,default="Pending")
    
    hr_as = models.CharField(max_length=255, null=True, blank=True)
   
    ar_as = models.CharField(max_length=255, null=True, blank=True)
    hr_ar = models.CharField(max_length=255, null=True, blank=True)
    

    ceo_as = models.CharField(max_length=255, null=True, blank=True)
    ceo_as_remarks  =  models.TextField(null=True,blank=True)

    Last_CEO_Action = models.CharField(max_length=255, null=True, blank=True)   # NEW FIELD
    Last_CEO_action_On = models.DateTimeField(null=True, blank=True)  # NEW FIELD
    Last_CEO_action_Remarks = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD

    Last_Action_By_EmpCode = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD
    Last_Action_By_Name = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD

    # Pending_From_Emp_Code = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD
    # Pending_From_Emp_Name = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD

   
    # Action Dates

    hr_actionOnDatetime = models.DateTimeField(null=True, blank=True) 
    ar_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    hr_ar_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    ceo_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    
   
    def get_organization_name(self):
        try:
            organization = OrganizationMaster.objects.get(OrganizationID=self.OrganizationID)
            return organization.ShortDisplayLabel
        except OrganizationMaster.DoesNotExist:
            return None
    

    def get_role_name(self, role):
        def get_first_last(name):
            if name:
                parts = name.strip().split()
                if len(parts) >= 2:
                    return f"{parts[0]} {parts[-1]}"
                return parts[0]
            return None
        if role == 'EP' or role == 'EP Submitted':
            return get_first_last(self.EmpName) or "EP"
            
        if role == 'HRA' or role == 'HRA Audited':
            # return self.CreatedByUsername or "HRA"
            if self.AuditedBy_Name:
                HRA_Action = get_first_last(self.AuditedBy_Name)
            else:
                HRA_Action = get_first_last(self.CreatedByUsername)

            return HRA_Action or "HRA"
            
        
        elif role == 'HR':
            return get_first_last(self.CreatedByUsername) or "HR"
        
        elif role == 'AR' or role == 'AR Submitted':
            try:
                matching_work = EmployeeWorkDetails.objects.filter(
                    EmpStatus__in=('Confirmed', 'On Probation', 'Not Confirmed'),
                    Designation__iexact=self.ReportingtoDesigantion,
                    OrganizationID=self.OrganizationID,
                    IsDelete=False,
                    IsSecondary=False
                ).values_list('EmpID', flat=True).first()

                if matching_work:
                    # emp_id = work_detail.EmpID
                    personal = EmployeePersonalDetails.objects.filter(EmpID=matching_work).first()
                    if personal:
                        return f'{personal.FirstName} {personal.LastName}'
            except Exception:
                return "AR"
            return "AR"
        
        return role


    def __str__(self):
        return self.Appraisee_Name
            
        
    def Approval_stage(self):
        stages = [
            ("HR", self.hr_as, self.hr_actionOnDatetime, 1, 1 if self.hr_as == "Submitted" else 0),
            ("AR", self.ar_as, self.ar_actionOnDatetime, 2, 1 if self.ar_as == "Submitted" else 0),
            ("HRA", self.hr_ar, self.hr_ar_actionOnDatetime, 3, 1 if self.hr_ar == "Audited" else 0),
            ("CEO", self.ceo_as, self.ceo_actionOnDatetime, 4, 1 if self.ceo_as in ["Approved", "Returned"] else 0),
            # ("CEO", self.ceo_as, self.ceo_actionOnDatetime, 4, 1 if self.ceo_as == "Approved" else 0),
        ]

        # Sort by sequence
        stages.sort(key=lambda x: x[3])

        last_submitted = None
        pending_from = None

        for role, status, action_date, order, flag in stages:
            if flag == 1:
                last_submitted = (role, action_date, status)
            elif flag == 0 and last_submitted:
                # pending_from = role
                # pending_from = (role, action_date)
                pending_from = (role, last_submitted[1])
                break

        submitted_msg = ""
        pending_msg = ""

        if last_submitted:
            role, date, status = last_submitted
            # submitted_msg = f'<strong style="color: #1ab394;">Submitted by </strong>{self.get_role_name(role)}'
            submitted_msg = f'<strong style="color: #1ab394;">{status} by<br></strong>{self.get_role_name(role)}'
            if date:
                submitted_msg += f' on {date.strftime("%d %b")}'

        # if pending_from:
        #     pending_msg = f'<strong style="color: #f8ac59;"><br>Pending from </strong>{self.get_role_name(pending_from)}'
        
        if pending_from:
            role, date = pending_from
            days = self.days_pending(date)
            pending_msg = f'<strong style="color: #f8ac59; display:block;">Pending from<br></strong>{self.get_role_name(role)}'
            if days is not None:
                pending_msg += f' <strong>Since {days} day{"s" if days != 1 else ""}</strong>'

        return submitted_msg + pending_msg

        
    def Approval_stage_Mobile_Api(self):
        stages = [
            ("HR", self.hr_as, self.hr_actionOnDatetime, 1, 1 if self.hr_as == "Submitted" else 0),
            ("AR", self.ar_as, self.ar_actionOnDatetime, 2, 1 if self.ar_as == "Submitted" else 0),
            ("HRA", self.hr_ar, self.hr_ar_actionOnDatetime, 3, 1 if self.hr_ar == "Audited" else 0),
            ("CEO", self.ceo_as, self.ceo_actionOnDatetime, 4, 1 if self.ceo_as in ["Approved", "Returned"] else 0),
            # ("CEO", self.ceo_as, self.ceo_actionOnDatetime, 4, 1 if self.ceo_as == "Approved" else 0),
        ]

        # Sort by sequence
        stages.sort(key=lambda x: x[3])

        last_submitted = None
        pending_from = None

        for role, status, action_date, order, flag in stages:
            if flag == 1:
                last_submitted = (role, action_date, status)
            elif flag == 0 and last_submitted:
                # pending_from = role
                # pending_from = (role, action_date)
                pending_from = (role, last_submitted[1])
                break

        submitted_msg = ""
        pending_msg = ""

        if last_submitted:
            role, date, status = last_submitted
            # submitted_msg = f'<strong style="color: #1ab394;">Submitted by </strong>{self.get_role_name(role)}'
            submitted_msg = f'{status} by {self.get_role_name(role)}'
            if date:
                submitted_msg += f' on {date.strftime("%d %b")}'

        # if pending_from:
        #     pending_msg = f'<strong style="color: #f8ac59;"><br>Pending from </strong>{self.get_role_name(pending_from)}'
        
        if pending_from:
            role, date = pending_from
            days = self.days_pending(date)
            pending_msg = f' Pending from {self.get_role_name(role)}'
            if days is not None:
                pending_msg += f' Since {days} day{"s" if days != 1 else ""}'

        return submitted_msg + pending_msg


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
    

    def get_stages_order(self):
        #  return ["HR",  "AR", "HR","CEO"]
        return ["HR Submitted", "AR Submitted", "HR Audited", "CEO"]






# Need to comment while upload code to live
class APADP_Master_Log(models.Model): 
    APADP = models.ForeignKey(APADP,on_delete=models.CASCADE, null=True, blank=True)

    LastApporvalStatus = models.CharField(max_length=255, null=True, blank=True,default="Pending")
    
    hr_as = models.CharField(max_length=255, null=True, blank=True)
   
    ar_as = models.CharField(max_length=255, null=True, blank=True)
    hr_ar = models.CharField(max_length=255, null=True, blank=True)

    ceo_as = models.CharField(max_length=255, null=True, blank=True)
    ceo_as_remarks  =  models.TextField(null=True,blank=True)

    # Last_CEO_Action = models.CharField(max_length=255, null=True, blank=True)   # NEW FIELD
    # Last_CEO_action_On = models.DateTimeField(null=True, blank=True)  # NEW FIELD
    # Last_CEO_action_Remarks = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD

    # Last_Action_By_EmpCode = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD
    # Last_Action_By_Name = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD

    # Pending_From_Emp_Code = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD
    # Pending_From_Emp_Name = models.CharField(max_length=255, null=True, blank=True) # NEW FIELD

   
    # Action Dates
    hr_actionOnDatetime = models.DateTimeField(null=True, blank=True) 
    ar_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    hr_ar_actionOnDatetime = models.DateTimeField(null=True, blank=True)
    ceo_actionOnDatetime = models.DateTimeField(null=True, blank=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False) 

    
    


class Master_APADP_SubItemDetail(models.Model):
    Master_APADP_SubItem = models.ForeignKey(Master_APADP_SubItem,on_delete=models.CASCADE)
    APADP = models.ForeignKey(APADP,on_delete=models.CASCADE,null= True,blank =True)
  
    Performance=models.CharField(max_length=255,null= True,blank =True )
  
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False) 


class DevelopmentGoalsApdpa(models.Model):
    APADP = models.ForeignKey(APADP,on_delete=models.CASCADE)

    Goal=models.CharField(max_length=255,null= True,blank =True )
    Timeline=models.CharField(max_length=255,null= True,blank =True )
    Status=models.CharField(max_length=255,null= True,blank =True )
    Remarks=models.CharField(max_length=255,null= True,blank =True )
    GoalStartDate=models.CharField(max_length=255,null= True,blank =True )
    GoalCompletionDate=models.CharField(max_length=255,null= True,blank =True )


    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False) 


from django.utils import timezone
class  FinalPerformancerating(models.Model):

    APADP = models.ForeignKey(APADP,on_delete=models.CASCADE)
    rating = models.CharField(max_length=255,null= True,blank =True )
    SalaryIncrementOption=models.CharField(max_length=255,null= True,blank =True )
    SalaryCorrectionFrom=models.CharField(max_length=255,null= True,blank =True )
    SalaryCorrectionTo=models.CharField(max_length=255,null= True,blank =True )
    JustificationSalaryCorrection=models.TextField(null= True,blank =True)
    PromotionFrom=models.CharField(max_length=255,null= True,blank =True )
    PromotionTo=models.CharField(max_length=255,null= True,blank =True )
    JustificationPromotion=models.TextField(null= True,blank =True)

    OrganizationID = models.BigIntegerField(default=0)
   
    CreatedByUsername = models.CharField(max_length=255, blank=True, null=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)


