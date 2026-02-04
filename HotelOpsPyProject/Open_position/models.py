from django.db import models
from datetime import datetime
from datetime import datetime, date
from django.utils import timezone
from ckeditor.fields import RichTextField
from app.models import OrganizationMaster
from Job_Description.models import JobDescription
from django.utils.text import slugify
from django.utils import timezone
from datetime import datetime
from django.db import models
from .azure import upload_file_to_blob
import uuid
from InterviewAssessment.models import Assessment_Master

from django.utils.text import slugify
from django.utils import timezone
from django.db import models
from datetime import datetime

base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"

class OpenPosition(models.Model):
    Position = models.CharField(max_length=255, blank=True, null=True,db_index=True)
    OpenDepartment = models.CharField(max_length=255, blank=True, null=True)
    OpenDivision = models.CharField(null=True,blank=True,max_length=255)      # New Field Added
    OpenLevel = models.CharField(null=True,blank=True,max_length=255)         # New Field Added
    Job_Type = models.CharField(max_length=255, blank=True, null=True)
    Salary = models.CharField(max_length=255, blank=True, null=True)
    Locations = models.CharField(max_length=255, blank=True, null=True,db_index=True)
    Number = models.CharField(max_length=255, blank=True, null=True)
    Opened_On = models.DateField(blank=True, null=True)  
   
    Status = models.BooleanField(default=True,db_index=True)  
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedByUserID = models.BigIntegerField(default=0)
    CreatedByUsername = models.CharField(max_length=255, blank=True, null=True)
    CreatedDateTime = models.DateTimeField(default=datetime.now)
    ModifyByUserID = models.BigIntegerField(default=0)
    ModifyByUsername = models.CharField(max_length=255, blank=True, null=True)
    ModifyDateTime = models.DateTimeField(default=datetime.now)
    IsDelete = models.BooleanField(default=False,db_index=True)
    PositionImage = models.URLField(max_length=1024, blank=True, null=True)
    

    def get_ProposedDOJ_Name(self):
        AppliedFor = self.Locations
        Department = self.OpenDepartment
        position = self.Position
        
        # print("Searching for:", AppliedFor, Department, position, self.Opened_On)
    
        obj = Assessment_Master.objects.filter(
            AppliedFor=AppliedFor,
            Department=Department,
            position=position,
            LOIStatus="Accepted",
            LastApporvalStatus="Approved",
            # IsEmployeeCreated=True,
            ProposedDOJ__gte=self.Opened_On,
 
            IsDelete=False
        ).order_by('-LastLoistatusModifyDate')#.first()  # Sabse latest LOI accepted record milega
        # print("Searching for:", AppliedFor, Department, position, self.Opened_On)
        # print("Found:", obj)
        # print("Matching entries count:", obj.count())
        # for i in obj:
        #     print("Candidate:", i.Name, "DOJ:", i.ProposedDOJ)

        if obj.exists():
            obj= obj.first()
            if obj:
                proposed_doj = obj.ProposedDOJ.strftime('%d %b %Y').upper() if obj.ProposedDOJ else ''
                return f"{proposed_doj} / {obj.Name}"
 
        return ''
 

    
    
    class Meta:
        indexes = [
            models.Index(fields=['Locations', 'Position', 'OpenDepartment']),
        ]
    def get_organization_name(self):
        try:
            organization = OrganizationMaster.objects.get(OrganizationID=self.Locations)
            return organization.ShortDisplayLabel
        except OrganizationMaster.DoesNotExist:
            return None
        
    def get_organization_full_name(self):
        try:
            organization = OrganizationMaster.objects.get(OrganizationID=self.Locations)
            return organization.OrganizationName
        except OrganizationMaster.DoesNotExist:
            return None    

    def __str__(self):
        return self.Position
    
    def get_formatted_salary(self):
        if self.Salary:
            return f"INR {self.Salary}"
        return "Salary details not available"
    
    def days_ago(self):
        if self.Opened_On:
            delta = timezone.now().date() - self.Opened_On
            days = delta.days
            if days == 0:
                return {"text": "Today", "is_red": False}
            elif days == 1:
                return {"text": "1 Day(s)", "is_red": False}
            else:
                return {"text": f"{days} Day(s)", "is_red": days > 30}
        return {"text": "Unknown", "is_red": False}

        
    def job_title(self):
        if self.Position and self.OpenDepartment:
            return f"{self.Position} - {self.OpenDepartment}"
        elif self.Position:
            return self.Position
        else:
            return "Unknown"

    def url_slug(self):
        if self.Position and self.Locations and self.id:
            OrgName = self.get_organization_full_name()
            base_slug = f"{self.Position} {OrgName}"
            
            formatted_slug = base_slug.replace(' ', '_').lower()
            
            return f"{formatted_slug}_{self.id}"
        else:
            return "unknown_url"
        
    def organization_logo(self):
        try:
            organization = OrganizationMaster.objects.get(OrganizationDomainCode=self.Locations)
            return organization.OrganizationLogo.name
        except OrganizationMaster.DoesNotExist:
            return None

    def logo_image(self):
        try:
            organization = OrganizationMaster.objects.get(OrganizationDomainCode=self.Locations)
            if organization.OrganizationLogo:
                return f"{base_url}{organization.OrganizationLogo.name}"
        except OrganizationMaster.DoesNotExist:
            return None
        
    def description(self):
        job_title = self.job_title()
        return f"If you are looking for a Job for {job_title}"

    def get_full_location_name(self):
        try:
            organization = OrganizationMaster.objects.get(ShortDisplayLabel=self.Locations)
            return organization.OrganizationName
        except OrganizationMaster.DoesNotExist:
            return self.Locations 
        
        
         
class Exportopen(models.Model):
    Remark = RichTextField()
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)


from django.core.files.storage import default_storage

import uuid
import os

class CareerResume(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    job_title = models.CharField(max_length=150, blank=True, null=True,db_index=True)
    location = models.CharField(max_length=100, blank=True, null=True,db_index=True)
    resume = models.FileField(blank=True, null=True)  
    resume_url = models.URLField(max_length=500, blank=True, null=True)
    NetProjectID =  models.BigIntegerField(default=0,blank=True,null=True,db_index=True)
    OpenPositionID =  models.BigIntegerField(default=0,blank=True,null=True,db_index=True)
    Department = models.CharField(max_length=100, blank=True, null=True,db_index=True)
    

    # def get_organization_name(self):
    #     try:
    #         organization = OrganizationMaster.objects.get(OrganizationID=self.location)
    #         return organization.OrganizationName
    #     except OrganizationMaster.DoesNotExist:
    #         return None

    
    email = models.EmailField(blank=True, null=True)
    AppliedDate = models.DateTimeField(default=timezone.now,db_index=True)
    campaign_source = models.CharField(max_length=255, blank=True, null=True) 
    IsDelete = models.BooleanField(default=False,db_index=True)

    # Traning Data Fields
    Middle_Name = models.CharField(max_length=100, blank=True, null=True)
    Candidate_Address  = models.CharField(null=True,blank=True,max_length=255)
    College  = models.CharField(null=True,blank=True,max_length=255)
    email  = models.EmailField(blank=True, null=True)
    Placement_Coordinator_Name  = models.CharField(null=True,blank=True,max_length=255)
    Placement_Coordinator_Email  = models.CharField(null=True,blank=True,max_length=255)
    Placement_Coordinator_Phone  = models.CharField(null=True,blank=True,max_length=255)
    Department_Of_Preference  = models.CharField(null=True,blank=True,max_length=255)

    profile_photo = models.ImageField(upload_to='Resume_Profile/', blank=True, null=True)
    profile_photo_url = models.URLField(max_length=500, blank=True, null=True)


    Is_Training_Data = models.BooleanField(default=False,db_index=True, blank=True, null=True)
    OrganizationID = models.BigIntegerField(default=0,db_index=True, blank=True, null=True)
    CreatedBy = models.BigIntegerField(default=0, blank=True, null=True)
    CreatedDateTime = models.DateTimeField(default=timezone.now, blank=True, null=True)
    ModifyBy = models.BigIntegerField(default=0, blank=True, null=True)
    ModifyDateTime = models.DateTimeField(default=timezone.now, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # def save(self, *args, **kwargs):
    #     if self.resume and not self.resume_url:
    #         file_stream = self.resume.read()  
    #         file_name = f"{uuid.uuid4()}_{self.resume.name}"  
    #         self.resume_url = upload_file_to_blob(file_stream, file_name)  
    #     super().save(*args, **kwargs)


    def save(self, *args, **kwargs):
        # Handle resume upload to blob
        if self.resume and not self.resume_url:
            file_stream = self.resume.read()
            file_name = f"{uuid.uuid4()}_{self.resume.name}"
            # file_name = f"Resumes/{uuid.uuid4()}_{self.resume.name}"
            self.resume_url = upload_file_to_blob(file_stream, file_name)

        # Handle profile photo upload to blob
        if self.profile_photo:
            if not hasattr(self, "profile_photo_url") or not self.profile_photo_url:
                file_stream = self.profile_photo.read()
                # file_name = f"{uuid.uuid4()}_{self.profile_photo.name}"
                file_name = f"Resume_Profile/{uuid.uuid4()}_{self.profile_photo.name}"
                self.profile_photo_url = upload_file_to_blob(file_stream, file_name)

        super().save(*args, **kwargs)


from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

class ActionsResume(models.Model):
    action = models.CharField(max_length=100)
    ca_resume = models.ForeignKey('CareerResume', on_delete=models.CASCADE)
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedByUserID = models.BigIntegerField(default=0)
    CreatedByUsername = models.CharField(max_length=255, blank=True, null=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)
    reason = models.TextField(blank=True, null=True)
    reason_date = models.DateTimeField(default=timezone.now)  


from django.db import models
from django.utils import timezone

class QRCode(models.Model):
   
    qr_type = models.CharField(max_length=50, choices=[('linkedin', 'LinkedIn'), ('facebook', 'Facebook'), ('twitter', 'Twitter'), ('instagram', 'Instagram'),('college', 'College'),('other', 'Other')])
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    OrganizationID = models.BigIntegerField(default=0)
   
    CreatedByUsername = models.CharField(max_length=255, blank=True, null=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.qr_type}'



from django.utils import timezone

class NotificationSchedule(models.Model):
    open_positions = models.ForeignKey('OpenPosition', on_delete=models.CASCADE)
    Departmetdata = models.CharField(max_length=255, blank=True, null=True)
    levelsfor = models.CharField(max_length=255, blank=True, null=True)
    Statusschedule = models.BooleanField(default=True)  
    Schedule_date = models.DateField(blank=True, null=True) 
    OrganizationID = models.BigIntegerField(default=0)
    
    CreatedByUsername = models.CharField(max_length=255, blank=True, null=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)


from django.db import models

class NotificationHistory(models.Model):
    notification = models.ForeignKey(NotificationSchedule, on_delete=models.CASCADE)
    EmpID = models.BigIntegerField(null=False,blank=False)
    phone_number = models.CharField(max_length=20)
    employee_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('error', 'Error')])
    message_id = models.CharField(max_length=50, null=True, blank=True)
    CreatedByUsername = models.CharField(max_length=255, blank=True, null=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for {self.employee_name} - Status: {self.status}"








# class Training_Data(models.Model):
#     first_name = models.CharField(max_length=100, blank=True, null=True)
#     last_name = models.CharField(max_length=100, blank=True, null=True)
#     Middle_Name = models.CharField(max_length=100, blank=True, null=True)
#     phone = models.CharField(max_length=30, blank=True, null=True)

#     Candidate_Address  = models.CharField(null=True,blank=True,max_length=255)
#     College  = models.CharField(null=True,blank=True,max_length=255)
#     email  = models.EmailField(blank=True, null=True)
#     Placement_Coordinator_Name  = models.CharField(null=True,blank=True,max_length=255)
#     Placement_Coordinator_Email  = models.CharField(null=True,blank=True,max_length=255)
#     Placement_Coordinator_Phone  = models.CharField(null=True,blank=True,max_length=255)
#     Department_Of_Preference  = models.CharField(null=True,blank=True,max_length=255)
#     profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
#     Is_Training_Data = models.BooleanField(default=True,db_index=True)


#     # resume = models.FileField(blank=True, null=True)  
#     # resume_url = models.URLField(max_length=500, blank=True, null=True)
#     # campaign_source = models.CharField(max_length=255, blank=True, null=True) 
#     # AppliedDate = models.DateTimeField(default=timezone.now,db_index=True)


#     OrganizationID = models.BigIntegerField(default=0,db_index=True)
#     CreatedBy = models.BigIntegerField(default=0)
#     CreatedDateTime = models.DateTimeField(default=timezone.now)
#     ModifyBy = models.BigIntegerField(default=0)
#     ModifyDateTime = models.DateTimeField(default=timezone.now)
#     IsDelete = models.BooleanField(default=False,db_index=True)


#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

#     def save(self, *args, **kwargs):
#         if self.resume and not self.resume_url:
#             file_stream = self.resume.read()  
#             file_name = f"{uuid.uuid4()}_{self.resume.name}"  
#             self.resume_url = upload_file_to_blob(file_stream, file_name)  
#         super().save(*args, **kwargs)
