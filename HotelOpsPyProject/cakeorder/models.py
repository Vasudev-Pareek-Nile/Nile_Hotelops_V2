from datetime import date
from django.db import models
from django.contrib.auth.models import User



# Create class Cake order form
class Cake_Order_Form(models.Model):
    To = models.CharField(max_length=100)
    Date = models.DateField()
    From = models.CharField(max_length=100)
    Time = models.TimeField(max_length=20)
    Guest_Name = models.CharField(max_length=100)
    To_Be_Prepared_For = models.CharField(max_length=100)
    Size = models.CharField(max_length=100)
    Type_Of_Cake = models.CharField(max_length=100)
    Required_Date = models.DateField()
    Required_Time = models.TimeField(max_length=20)
    type = (
        ('Yes','Yes'),
        ('No','No'),
    )
    Packing = models.CharField(max_length=50,choices=type)
    Selling_Price =  models.DecimalField(max_digits=6, decimal_places=2)
    Message_On_Cake = models.CharField(max_length=100)
    type = (
        ('Yes','Yes'),
        ('No','No'),
    )
    Complimentory = models.CharField(max_length=50,choices=type)
    Authorised_By = models.CharField(max_length=100)
    
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Guest_Name
    
