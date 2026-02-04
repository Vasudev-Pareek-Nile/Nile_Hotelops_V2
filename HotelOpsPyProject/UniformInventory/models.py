from django.db import models
from django.utils import timezone


class UniformInformation(models.Model):
    EmpID = models.BigIntegerField(default=0, null=True, blank=True)
    EmployeeName = models.CharField(max_length=255, null=True)
    EmployeeCode = models.CharField(max_length=255, null=True)
    DesignationGrade = models.CharField(max_length=255, null=True)
    Department = models.CharField(max_length=255, null=True)

    HrStatus = models.CharField(max_length=255, null=True, default='0')
    HrComment = models.CharField(max_length=255, null=True)

    HousekeppingStatus = models.CharField(max_length=255, null=True, default='0')
    HousekeppingComment = models.CharField(max_length=255, null=True)

    HodStatus = models.CharField(max_length=255, null=True, default='0')
    HodComment = models.CharField(max_length=255, null=True)
   
    ReportingtoDesigantion=models.CharField(max_length=255,null=False,blank=False)
   
    Return = models.BooleanField(default=False)
    ReturnAmount = models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=True)
    
    HR = models.BooleanField(default=False)
    HRCreatedBy = models.BigIntegerField(default=0)
    
    IssuedDate = models.DateField(default=timezone.now)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)




class UniformItemMaster(models.Model):
    ItemName = models.CharField(max_length=255, null=True)
    Price = models.DecimalField( max_digits=12, decimal_places=2)
    Year = models.IntegerField(null=False,blank=False)  
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)





class UniformDetails(models.Model):
    UniformInformation = models.ForeignKey(UniformInformation, on_delete=models.CASCADE)
    UniformItemMaster = models.ForeignKey(UniformItemMaster, on_delete=models.CASCADE)
    
    NewQuantity =  models.IntegerField(null=True,blank=True)
    AlteredQuantity = models.IntegerField(null=True,blank=True)
    IssuedQuantity = models.IntegerField(null=True,blank=True)

    ReturnNewQuantity = models.IntegerField(null=True,blank=True)
    ReturnAlteredQuantity = models.IntegerField(null=True,blank=True)
    ReturnIssuedQuantity = models.IntegerField(null=True,blank=True)
    
    NewVariance = models.IntegerField(null=True,blank=True)
    AlterVariance  = models.IntegerField(null=True,blank=True)
    IssueVariance  = models.IntegerField(null=True,blank=True) 
    
    TotalCharged = models.DecimalField( max_digits=12, decimal_places=2,null=True,blank=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)




