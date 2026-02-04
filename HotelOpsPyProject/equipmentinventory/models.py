from django.db import models
from datetime import date


# For Creating class Equipment Inventory
class Equipment_Inventory(models.Model):
    Date = models.DateField(default = date.today)
    Equipment_Name = models.CharField(max_length=100)
    Brand_Name = models.CharField(max_length=100)
    Model_No = models.CharField(max_length=100)
    type = (
        ('Yes','Yes'),
        ('No','No'),
    )
    In_Working_Condition = models.CharField(max_length=50,choices=type)
    Last_Servicing_Date = models.DateField(default = date.today)
    type = (
        ('Yes','Yes'),
        ('No','No'),
    )
    AMC_Covered = models.CharField(max_length=50,choices=type)
    Serial_No =  models.CharField(max_length=100)
    Remarks  = models.TextField()
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Equipment_Name
    
    
    
