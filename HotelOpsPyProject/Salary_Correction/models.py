from django.db import models
from datetime import datetime

class Salary_Correction(models.Model):
    Date = models.DateField()
    Name = models.CharField(max_length=255, null=True,blank = True)  
    EmployeeCode =  models.CharField(max_length=255, null=True,blank = True)
    Department  = models.CharField(max_length=255, null=True,blank = True)
    Designation = models.CharField(max_length=255, null=True,blank = True)
    Current_Salary = models.DecimalField(max_digits=12, decimal_places=2)
    Date_of_Last_salary_review =  models.DateField()
    Last_Increment_Amount  =models.DecimalField(max_digits=12, decimal_places=2)
    Last_Increment_Slab_3  = models.BooleanField(default=False)
    Last_Increment_Slab_5  = models.BooleanField(default=False)
    Last_Increment_Slab_8  = models.BooleanField(default=False)
    Last_Increment_Slab_None  = models.BooleanField(default=False)

    Proposed_Salary =models.DecimalField(max_digits=12, decimal_places=2)
    Effective_Date = models.DateField()
    Justification_Request =  models.TextField(null=True, blank=True)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=datetime.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=datetime.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.EmployeeCode
    







