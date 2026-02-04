from django.db import models

from django.db import models
from datetime import date 
from ckeditor.fields import RichTextField

from django.contrib.auth.models import User

class RevealingLetter(models.Model):
    name =  models.CharField(max_length=50,null=False,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    data = RichTextField()
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    
# Emp Details  Model
class  RevealingLetterEmployeeDetail(models.Model):
    emp_code = models.CharField(max_length=200,null=False,blank=False)


    prefix = models.CharField(max_length=20,null=False,blank=False)
    first_name = models.CharField(max_length=200,null=False,blank=False)
    last_name = models.CharField(max_length=200,null=False,blank=False)
    mobile_number = models.CharField(max_length=250)
    email = models.EmailField(max_length=254,null=False,blank=False)
    date_of_joining = models.DateField()
    date_of_Revealing = models.DateField(null=True,blank=True)
    date_of_last_working = models.DateField(null=True,blank=True)

    department = models.CharField(max_length=200,null=False,blank=False)
    designation = models.CharField(max_length=200,blank=False,null=False)
    Reporting_to_designation = models.CharField(max_length=200,blank=True,null=True)
    
    level = models.CharField(max_length=200,null=False,blank=False)
    basic_salary = models.IntegerField(null=False,blank=False)
    address = models.TextField()
   

    file_id = models.CharField(max_length=200,null=True)
    file_name = models.CharField(max_length=200, null=True)
     
    Hr_Name = models.CharField(max_length=255,null=False,blank=False)
    Hr_Designation = models.CharField(max_length=255,null=False,blank=False)
    
    Issuing_manager_name = models.CharField(max_length=255,null=False,blank=False)
    Issuing_designation = models.CharField(max_length=255,null=False,blank=False)
    
   
     

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    




class RevealingLetterDeletedFile(models.Model):
    RevealingLetterEmployeeDetail = models.ForeignKey(RevealingLetterEmployeeDetail, on_delete=models.CASCADE)
    file_id = models.CharField(max_length=200,null=True)
    file_name = models.CharField(max_length=200, null=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.file_id
