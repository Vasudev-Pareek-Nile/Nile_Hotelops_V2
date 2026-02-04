from django.db import models
from datetime import date 
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.contrib.auth.models import User

# Emp Appointment letter model
class LETTEROFCONFIRMATION(models.Model):
    
    name =  models.CharField(max_length=50,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    data = RichTextField()
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# Emp Details  Model
class LETTEROFCONFIRMATIONEmployeeDetail(models.Model):
    
    prefix = models.CharField(max_length=50,null=True,blank=True)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    emp_code = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    
    
    date_of_appointment =  models.DateField(default=timezone.now)
    date_of_confirmation =  models.DateField(default=timezone.now)
    
    department = models.CharField(max_length=50,null=True,blank=True)
    designation = models.CharField(max_length=100,null=True,blank=True)
    
    
    Issuing_manager_name = models.CharField(max_length=255,null=True,blank=True)
    Issuing_designation = models.CharField(max_length=255,null=True,blank=True)
    
    file_id = models.CharField(max_length=200,null=True)
    file_name = models.CharField(max_length=200, null=True)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class LETTEROFCONFIRMATIONDeletedFileofEmployee(models.Model):
    LETTEROFCONFIRMATIONEmployeeDetail = models.ForeignKey(LETTEROFCONFIRMATIONEmployeeDetail, on_delete=models.CASCADE)
    file_id = models.CharField(max_length=200,null=True)
    file_name = models.CharField(max_length=200, null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.file_id
