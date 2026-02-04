from django.db import models
from datetime import date

# For Register in Pay Master
class Pay_Master(models.Model):
    PM_Number = models.CharField(max_length=100)
    PM_Date =models.DateField(default = date.today)
    Name = models.CharField(max_length=100)
    Amount =  models.DecimalField(max_digits=6, decimal_places=2,blank=True)
    Employee_Name = models.CharField(max_length=100)
    Reason = models.TextField()
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Employee_Name
  
