from django.db import models
from datetime import date 
# from django.utils.timezone import now
from django.utils import timezone

# Create your models here.
class KRA(models.Model):
    Title = models.TextField(null=False,blank=False)
    Standard = models.TextField(null=True, blank=True)
    # Standard = models.TextField(null=False,blank=False)
    Defination = models.TextField(null=False,blank=False)
    Type = models.CharField(max_length=255,null=False,blank=False)
    Source = models.CharField(max_length=255,null=False,blank=False)
    SortOrder  = models.BigIntegerField(default=999) 
    ComparisonType = models.CharField(
    max_length=10,
    choices=[
        ('higher', 'Higher is better'),
        ('lower', 'Lower is better'),
        ('equal', 'Exact match'),
    ],
    default='higher'
    )
    Select_Value_Type = models.CharField(
        max_length=10,
        choices=[
            ('number', 'Number'),
            ('percentage', 'Percentage'),
            ('decimal', 'Decimal'),
            ('text', 'Text'),
        ],
        default='number'
    )

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)


class HotelKRAStandard(models.Model):
    OrganizationID = models.BigIntegerField(default=0)   # Hotel ID
    KRAID = models.BigIntegerField(default=0)            # Reference to KRA ID
    StandardValue = models.CharField(max_length=255,null=True, blank=True)
    CompareWithValue = models.CharField(max_length=255, null=True, blank=True)
    IsApplicable = models.BooleanField(default=True, null=True,blank=True)
    
    
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.OrganizationID} - KRA {self.KRAID} = {self.StandardValue}"


class TargetAssignMaster(models.Model):
    AssignByName = models.CharField(max_length=255, null=True, blank=True)
    AssignByEmployeeCode = models.CharField(max_length=255, null=True, blank=True)
    AssignByDesignation = models.CharField(max_length=255, null=True, blank=True)

    AssignToName = models.CharField(max_length=255, null=True, blank=True)
    AssignToEmployeeCode = models.CharField(max_length=255, null=True, blank=True)
    AssignToDesignation = models.CharField(max_length=255, null=True, blank=True)


    AssignToDoj = models.CharField(max_length=255, null=True, blank=True)   # New Field

   

    AssignYear = models.IntegerField(null=True, blank=True)  
    AssignMonth = models.IntegerField(null=True, blank=True)  
    
    AssignToYear = models.IntegerField(null=True, blank=True)  
    AssignToMonth = models.IntegerField(null=True, blank=True)  
    
    Status = models.CharField(max_length=50, default="Pending")  
    
    CreatedByUserName = models.CharField(max_length=255, null=True, blank=True)
    AssignDate = models.DateField(null=True, blank=True)  

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

  


class TargetAssignMasterDetails(models.Model):
    AssignMaster = models.ForeignKey(TargetAssignMaster, on_delete=models.CASCADE)
    KRA = models.ForeignKey(KRA, on_delete=models.CASCADE)
  
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

  

class KraEntryMaster(models.Model):
    SubmittedByName = models.CharField(max_length=255, null=True, blank=True)
    SubmittedByEmployeeCode = models.CharField(max_length=255, null=True, blank=True)
    SubmittedByDesignation = models.CharField(max_length=255, null=True, blank=True)

    SubmittedYear = models.IntegerField(null=True, blank=True)  
    SubmittedMonth  =  models.IntegerField(null=True, blank=True) 

    IsSave = models.BooleanField(default=False,null=True,blank=True)
    IsFinalSubmit = models.BooleanField(default=False,null=True,blank=True) 

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)


class KraEntryMasterDetails(models.Model):
    KraEntryMaster = models.ForeignKey(KraEntryMaster, on_delete=models.CASCADE)
    TargetAssignMasterDetails = models.ForeignKey(TargetAssignMasterDetails, on_delete=models.CASCADE)
    Actual = models.CharField(max_length=255, null=True, blank=True)
    ActualValue  = models.CharField(max_length=255, null=True, blank=True)
    
    KRAID = models.BigIntegerField(default=0)            # Reference to KRA ID
    StandardValue = models.CharField(max_length=255,null=True, blank=True)

    # IsSave = models.BooleanField(default=False,null=True,blank=True)
    # IsFinalSubmit = models.BooleanField(default=False,null=True,blank=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)



