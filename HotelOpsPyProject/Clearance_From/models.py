from django.db import models
from django.utils import timezone
# Create your models here.

class MasterClearanceItem(models.Model):
    ApprovedItem = models.CharField(max_length=255, blank=True, null=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.ApprovedItem

class MasterReturnItem(models.Model):
    ItemTitle = models.CharField(max_length=255, blank=True, null=True)
    Department = models.CharField(max_length=255, blank=True, null=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.ItemTitle

class ClearenceEmp(models.Model):
    EmpCode = models.CharField(max_length=255, blank=True, null=True)
    Name = models.CharField(max_length=255, blank=True, null=True)
    Position = models.CharField(max_length=255, blank=True, null=True)  
    SeparationDate = models.DateField(blank=True, null=True)   
    FinishingTime = models.TimeField(blank=True, null=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)     
    def __str__(self):
        return self.Name


class ClearanceItemDetail(models.Model):
    MasterClearanceItem=models.ForeignKey(MasterClearanceItem,on_delete=models.CASCADE)
    ClearenceEmp=models.ForeignKey(ClearenceEmp,on_delete=models.CASCADE)
    ItemStatus=models.CharField(max_length=255,blank=True,null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)    
    

class ReturnItemDetail(models.Model):
    MasterReturnItem=models.ForeignKey(MasterReturnItem,on_delete=models.CASCADE)
    ClearenceEmp=models.ForeignKey(ClearenceEmp,on_delete=models.CASCADE)
    ReturndataStatus=models.CharField(max_length=255,blank=True,null=True)
    ReceivedName=models.CharField(max_length=255,blank=True,null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)    
        
   
    