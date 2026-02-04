from django.db import models
from datetime import date
# For Creating Model For Casual Manpower Requisition
class Casual_Manpower_Requisition(models.Model):
    Date = models.DateField(default = date.today)
    Prepared_By = models.CharField(max_length=100)
    Department =  models.CharField(max_length=100)
    Numbers_Required = models.CharField(max_length=100)
    Reason = models.TextField(max_length=100,blank=True)
    Function = models.CharField(max_length=100,blank=True, null=True)
    Rate =  models.DecimalField(max_digits=6, decimal_places=2,blank=True, null=True)
    No_Of_Pax = models.CharField(max_length=100,blank=True)
    Date_Required = models.DateField(null=True)
    Est_Sales_Volume =models.CharField(max_length=100,blank=True, null=True)
    Reporting_Time = models.TimeField(blank=True, null=True)
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Date