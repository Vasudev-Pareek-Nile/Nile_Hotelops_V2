from datetime import date
from django.db import models


# For Creating Model Scanty Baggage
class Scanty_Baggage_Register_Form(models.Model):
    Date  = models.DateField(default = date.today)
    Room_No = models.CharField(max_length=100)
    Guest_Name =  models.CharField(max_length=100)
    Arrival_Date = models.DateField(default = date.today)
    Departure_Date = models.DateField(default = date.today)
    Deposite =  models.DecimalField(max_digits=6, decimal_places=2,blank=True)
    Comment =  models.TextField()
    Front_Desk_Associate =  models.CharField(max_length=100)
    Duty_Manager = models.CharField(max_length=100)
    Remarks =  models.TextField()
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Guest_Name