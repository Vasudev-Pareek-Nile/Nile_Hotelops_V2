from django.db import models
from datetime import date


# Registering the Grooming Form
class Grooming_Registeration(models.Model):
    Date = models.DateField()
    AduittypeList = (
        ('Daily','Daily'),
        ('Weekly','Weekly'),
        ('Monthly','Monthly'),
    )
    Audit_Type =  models.CharField(max_length=50,choices=AduittypeList, default = 'Daily')
    Name  = models.CharField(max_length=100)
    type = (
        ('Yes','Yes'),
        ('No','No'),
    )
    Shoes =  models.CharField(max_length=50,choices=type)
    Shocks =  models.CharField(max_length=50,choices=type)
    Nails =  models.CharField(max_length=50,choices=type)
    Hair =  models.CharField(max_length=50,choices=type)
    Uniform =  models.CharField(max_length=50,choices=type)
    Name_Badge = models.CharField(max_length=50,choices=type)
    Brand_Pin = models.CharField(max_length=50,choices=type)
    Remarks = models.TextField()
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Name
    