from datetime import date
from django.db import models
from django.utils import timezone

# Creating Models For Full and Final Settlement
class EmpAbscondingModel(models.Model):
    Name = models.CharField(max_length=100)
    Emp_Code = models.CharField(max_length=100)
    DOJ =  models.DateField(default=timezone.now)
    Date_Of_Absconding =  models.DateField(default=timezone.now)
    Dept = models.CharField(max_length=100)
    Designation = models.CharField(max_length=100)
    # Remarks = models.CharField(max_length=2000)
    Remarks = models.TextField(null=True,blank=True)
    showcause = models.BooleanField(default=False)
    
    Issuing_manager_name = models.CharField(max_length=255,null=False,blank=False)
    Issuing_designation = models.CharField(max_length=255,null=False,blank=False)
    
    # new added Last-Employee-Status
    LastEmpStatus = models.CharField(max_length=250,null=True,blank=True)
    AbscondingRevoke =  models.BooleanField(default=False)


    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.Name
    
    
class Empshowcausenotice (models.Model):
    Name = models.CharField(max_length=100)
    Emp_Code = models.CharField(max_length=100)
    DOJ =  models.DateField(default=timezone.now)
    Date_Of_absence =  models.DateField(default=timezone.now)
    Dept = models.CharField(max_length=100)
    Designation = models.CharField(max_length=100)
    # Remarks = models.CharField(max_length=2000)
    Remarks = models.TextField(null=True,blank=True)

    Issuing_manager_name = models.CharField(max_length=255,null=False,blank=False)
    Issuing_designation = models.CharField(max_length=255,null=False,blank=False)
    NoticeIssuingdate = models.DateField(default=timezone.now) 
    NoticeCreateddate = models.DateField(default=timezone.now)

    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.Name        
    
    
class Second_Show_Cause_Notice(models.Model):
    Name = models.CharField(max_length=100)
    Emp_Code = models.CharField(max_length=100)
    DOJ =  models.DateField(default=timezone.now)
    Date_Of_absence =  models.DateField(default=timezone.now)
    Dept = models.CharField(max_length=100)
    Designation = models.CharField(max_length=100)
    Remarks = models.TextField(null=True,blank=True)

    Issuing_manager_name = models.CharField(max_length=255,null=False,blank=False)
    Issuing_designation = models.CharField(max_length=255,null=False,blank=False)
    NoticeIssuingdate = models.DateField(default=timezone.now) 
    NoticeCreateddate = models.DateField(default=timezone.now)

    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.Name        