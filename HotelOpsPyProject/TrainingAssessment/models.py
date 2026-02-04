from datetime import date
from django.db import models

# Create your models here.

    
class  TrainingAssessmentMaster(models.Model):
    title = models.CharField(max_length = 200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
   
    
class TrainingAssessmentEntryMaster(models.Model):
    TrainingDate =models.DateField(default = date.today)
    EmpCode = models.CharField(max_length=200,blank=True,default='')
    EmpName = models.CharField(max_length=200,blank=True,default='')
    EmpDesignation = models.CharField(max_length=200,blank=True,default='')
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
  
class TrainingAssessmentEntryDetails(models.Model):
    TrainingAssessmentMaster =models.ForeignKey(TrainingAssessmentMaster, on_delete=models.CASCADE)
    TrainingAssessmentEntryMaster =models.ForeignKey(TrainingAssessmentEntryMaster, on_delete=models.CASCADE)
    Statustype = (
        ('Good','Good'),
        ('Poor','Poor'),
        ('Average','Average'),
    )
    Status = models.CharField(max_length=50,choices=Statustype)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
