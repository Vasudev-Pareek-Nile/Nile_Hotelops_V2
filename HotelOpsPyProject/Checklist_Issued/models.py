from django.db import models
from django.utils import timezone
# Create your models here.

class HREmployeeChecklistMaster(models.Model):
    Checklist = models.CharField(max_length=255, blank=True, null=True)

    
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.Checklist
    
class HREmployeeChecklist_Entry(models.Model):
    EmpCode = models.CharField(max_length=255, blank=True, null=True)
    Name = models.CharField(max_length=255, blank=True, null=True)
    Department = models.CharField(max_length=255, blank=True, null=True)
    Designtions = models.CharField(max_length=255, blank=True, null=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.EmpCode    



class HREmployeeChecklist_Details(models.Model):
    HREmployeeChecklist_Entry=models.ForeignKey(HREmployeeChecklist_Entry,on_delete=models.CASCADE)
    HREmployeeChecklistMaster=models.ForeignKey(HREmployeeChecklistMaster,on_delete=models.CASCADE)
    ReceivedStatus=models.CharField(max_length=255,blank=True,null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    