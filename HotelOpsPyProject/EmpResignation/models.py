from datetime import date
from django.db import models
from django.utils import timezone

# Creating Models For Full and Final Settlement
class EmpResigantionModel(models.Model):
    Name = models.CharField(max_length=100)
    Emp_Code = models.CharField(max_length=100)
    DOJ =  models.DateField(default = date.today)
    Date_Of_res =  models.DateField(default = date.today)
    Dept = models.CharField(max_length=100)
    Designation = models.CharField(max_length=100,default='',blank=True,null=True)
    
   

    TypeofRes = models.CharField(max_length=250,null=True,blank=True)
    NoticePeriod = models.CharField(max_length=250,null=True,blank=True)
    Level = models.CharField(max_length=100,null=True,blank=True)


    Res_Reason = models.CharField(max_length=250,null=True,blank=True)
    LastEmpStatus = models.CharField(max_length=250,null=True,blank=True)
    IsRevoke =  models.BooleanField(default=False)

    Ressubmittedto = models.CharField(max_length=50)
    LastWorkingDays =  models.DateField(default = date.today)
    Res_acceptance_Date = models.DateField(default = date.today)
    Res_acceptance_By = models.CharField(max_length=50)

   
    HotelID = models.BigIntegerField(default=0)
    HR = models.BooleanField(default=False)
    HRCreatedBy = models.BigIntegerField(default=0)
    HRCreatedDateTime = models.DateField(default=timezone.now)
    
    HK = models.BooleanField(default=False)
    HKCreatedBy = models.BigIntegerField(default=0)
    HKCreatedDateTime = models.DateField(default=timezone.now)
    
    IT = models.BooleanField(default=False)
    ITCreatedBy = models.BigIntegerField(default=0)
    ITCreatedDateTime = models.DateField(default=timezone.now)
    
    FNB = models.BooleanField(default=False)
    FNBCreatedBy = models.BigIntegerField(default=0)
    FNBCreatedDateTime = models.DateField(default=timezone.now)
    
    Finance = models.BooleanField(default=False)
    FinanceCreatedBy = models.BigIntegerField(default=0)
    FinanceCreatedDateTime = models.DateField(default=timezone.now)
    
    IsDEPT = models.BooleanField(default=False)
    DEPTCreatedBy = models.BigIntegerField(default=0)
    DEPTCreatedDateTime = models.DateField(default=timezone.now)

    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.Name
    
    
    



class DivisonHeadEmail(models.Model):
    Department = models.CharField(null=True,blank=True,max_length=500)
    FullName = models.CharField(null=True,blank=True,max_length=500)
    Email= models.CharField(null=True,blank=True,max_length=500)


    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    


