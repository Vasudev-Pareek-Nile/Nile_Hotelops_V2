from django.db import models
from datetime import date

# For Creating Models of IRD Clerance Form
class IRD_Clerance(models.Model):
    Date  = models.DateField(default = date.today)
    Clerance_time = models.TextField()
    Remarks = models.TextField()
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    # def __str__(self):
    #     return self.Date