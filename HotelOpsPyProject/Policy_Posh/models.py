from django.db import models
from datetime import date 
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.contrib.auth.models import User



class Policy_Posh_Employee_Detail(models.Model):
    emp_code = models.CharField(max_length=250,null=True,blank=True)

    prefix = models.CharField(max_length=20,null=True,blank=True)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    
    generate_date = models.DateField(default=timezone.now)
    date_of_joining = models.DateField()
    date_of_last_working = models.DateField()
    department = models.CharField(max_length=50,null=True,blank=True)
    designation = models.CharField(max_length=100,blank=False,null=False)
    
    Hr_Name = models.CharField(max_length=255,null=True,blank=True)
    Hr_Designation = models.CharField(max_length=255,null=True,blank=True)  
  
    
    file_id = models.CharField(max_length=200,null=True)
    file_name = models.CharField(max_length=200, null=True)
    
    HotelID = models.BigIntegerField(default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


# Letter_Of_Data_PrivacyExperience
class Policy_Posh_Deleted_File_Of_Employee(models.Model):
    Data_PrivacyExperience_Employee_Detail = models.ForeignKey(Policy_Posh_Employee_Detail, on_delete=models.CASCADE)
    file_id = models.CharField(max_length=200,null=True)
    file_name = models.CharField(max_length=200, null=True, blank=True)

    HotelID = models.BigIntegerField(default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.file_id
