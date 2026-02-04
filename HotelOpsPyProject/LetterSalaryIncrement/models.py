from django.db import models
from datetime import date 
from ckeditor.fields import RichTextField

from django.contrib.auth.models import User

# Emp Appointment letter model
class LETTEROFSALARYINCREAMENT(models.Model):
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
class LETTEROFSALARYINCREAMENTEmployeeDetail(models.Model):
    emp_code = models.CharField(max_length=200,null=False,blank=False)
    prefix = models.CharField(max_length=20,null=False,blank=False)
    first_name = models.CharField(max_length=50,null=False,blank=False)
    last_name = models.CharField(max_length=50,null=False,blank=False)
    
    date_of_salary_increament  = models.DateField(default=date.today)
    
    department = models.CharField(max_length=50,null=False,blank=False)
    designation = models.CharField(max_length=100,blank=False,null=False)
    
    CTC = models.CharField(max_length=50,null=True,blank=True)
    
    
    
    Issuing_manager_name = models.CharField(max_length=255,null=False,blank=False)
    Issuing_designation = models.CharField(max_length=255,null=False,blank=False)

    file_id = models.CharField(max_length=200,null=True)
    file_name = models.CharField(max_length=200, null=True)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class LETTEROFSALARYINCREAMENTDeletedFileofEmployee(models.Model):
    LETTEROFSALARYINCREAMENTEmployeeDetail = models.ForeignKey(LETTEROFSALARYINCREAMENTEmployeeDetail, on_delete=models.CASCADE)
    
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






from HumanResources.models import SalaryTitle_Master
class IncreamentSalaryDetails(models.Model):
    LETTEROFSALARYINCREAMENTEmployeeDetail = models.ForeignKey(LETTEROFSALARYINCREAMENTEmployeeDetail, on_delete=models.CASCADE)

    Salary_title = models.ForeignKey(SalaryTitle_Master, on_delete=models.CASCADE)
    PresentSal =models.DecimalField(default=0,blank=True,null=True,max_digits=10, decimal_places=2)
    RevisedSal =models.DecimalField(default=0,blank=True,null=True,max_digits=10, decimal_places=2)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
 
    # def __str__(self):
    #     return self.Salary_title    