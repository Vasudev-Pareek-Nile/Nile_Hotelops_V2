import uuid
from django.db import models
from datetime import datetime
from app.models import OrganizationMaster

from django.utils import timezone




class ReferenceDetails(models.Model):
    
    candidate_name = models.CharField(max_length=255,null=True,blank=True)
    candidate_department = models.CharField(max_length=255,null=True,blank=True)
    Inteview_AssementID  =   models.IntegerField(null=True,blank=True)    
    
    Ref1_name = models.CharField(max_length=255,null=True,blank=True)
    Ref1_email = models.EmailField(null=True,blank=True)
    Ref1_mobile_number = models.CharField(max_length=15,null=True,blank=True)
    Ref1_Organization = models.CharField(max_length=255,null=True,blank=True)
    Ref1_Designation = models.CharField(max_length=255,null=True,blank=True)
    ref1_unique_id = models.CharField(max_length=20,null=True,blank=True)
    ref1_status=models.IntegerField(default=0,null=True,blank=True)
    Ref1_candidate_Designation = models.CharField(max_length=255,null=True,blank=True)



    
    
    Ref2_name = models.CharField(max_length=255,null=True,blank=True)
    Ref2_email = models.EmailField(null=True,blank=True)
    Ref2_mobile_number = models.CharField(max_length=15,null=True,blank=True)
    Ref2_Organization = models.CharField(max_length=255,null=True,blank=True)
    Ref2_Designation = models.CharField(max_length=255,null=True,blank=True)
    ref2_unique_id = models.CharField(max_length=20,null=True,blank=True) 
    ref2_status=models.IntegerField(default=0,null=True,blank=True)
    Ref2_candidate_Designation = models.CharField(max_length=255,null=True,blank=True)
   
    
    
    Ref3_name = models.CharField(max_length=255,null=True,blank=True)
    Ref3_email = models.EmailField(null=True,blank=True)
    Ref3_mobile_number = models.CharField(max_length=15,null=True,blank=True)
    Ref3_Organization = models.CharField(max_length=255,null=True,blank=True)
    Ref3_Designation = models.CharField(max_length=255,null=True,blank=True)
    ref3_unique_id = models.CharField(max_length=20,null=True,blank=True)  
    ref3_status=models.IntegerField(default=0,null=True,blank=True)
    Ref3_candidate_Designation = models.CharField(max_length=255,null=True,blank=True)
     
    
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)




    def __str__(self):
        return self.candidate_name    
    
    def get_organization_logo(self):
        try:
            organization = OrganizationMaster.objects.get(OrganizationID=self.OrganizationID)
            return organization.OrganizationLogo
        except OrganizationMaster.DoesNotExist:
            return None
     
    def get_organization_name(self):
        try:
            organization = OrganizationMaster.objects.get(OrganizationID=self.OrganizationID)
            return organization.OrganizationName
        except OrganizationMaster.DoesNotExist:
            return None    
    
class Reference_check(models.Model):
    ReferenceDetails = models.ForeignKey('ReferenceDetails', on_delete=models.CASCADE)
    ref_unique_id  =  models.CharField(max_length=250, null=True,blank=True)
    name = models.CharField(max_length=250, null=True,blank=True)
    relationship = models.TextField()
    contact_informations = models.TextField()
    this_company = models.BooleanField(default=False)
    employment_from_date = models.DateField(null=True, blank=True)
    employment_to_date = models.DateField(null=True, blank=True)

    
    # job_duties = models.TextField()
    job_performance = models.CharField(max_length=250, null=True,blank=True)
    interpersonal_skills = models.CharField(max_length=250, null=True,blank=True)
    attendance_work = models.CharField(max_length=250, null=True,blank=True)
    leave_company = models.CharField(max_length=250, null=True,blank=True)
    rehire = models.BooleanField(default=False)
    anything_else = models.TextField()
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class OrganizationNameList(models.Model):
    Hotal_name = models.CharField(max_length=250, null=True,blank=True)


class DesignationNameList(models.Model):
    Designation_name = models.CharField(max_length=250, null=True,blank=True)    
