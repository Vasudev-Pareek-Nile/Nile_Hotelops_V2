from django.db import models
from datetime import date 
from ckeditor.fields import RichTextField

from django.contrib.auth.models import User

# Emp Appointment letter model
class Letter_Of_Trainees_Experience(models.Model):
    name =  models.CharField(max_length=50,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
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
class Trainees_Experience_Employee_Detail(models.Model):
    
    emp_code = models.CharField(max_length=250,null=True,blank=True)

    prefix = models.CharField(max_length=20,null=True,blank=True)
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    
    generate_date = models.DateField(default=date.today)
    date_of_joining = models.DateField()
    date_of_last_working = models.DateField()
    department = models.CharField(max_length=50,null=True,blank=True)
    designation = models.CharField(max_length=100,blank=False,null=False)
    
    Hr_Name = models.CharField(max_length=255,null=True,blank=True)
    Hr_Designation = models.CharField(max_length=255,null=True,blank=True)  
  
    
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


# Letter_Of_Trainees_Experience
class Trainees_Experience_Deleted_File_Of_Employee(models.Model):
    Trainees_Experience_Employee_Detail = models.ForeignKey(Trainees_Experience_Employee_Detail, on_delete=models.CASCADE)
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
