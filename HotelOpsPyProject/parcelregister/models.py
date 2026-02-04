from django.db import models
from datetime import date

# For Registering Class Message and Parcel Register
class Message_Parcel_Register(models.Model):
    Type_Of_Article = models.CharField(max_length=100)
    Room_No = models.IntegerField()
    Guest_Name = models.CharField(max_length=100)
    Date_Of_Arrival = models.DateField(default = date.today)
    Received_From = models.CharField(max_length=100)
    Contact_No = models.CharField(max_length=12)
    Received_By = models.CharField(max_length=100)
    Date_Of_Delivery = models.DateField(default = date.today)
    Given_By = models.CharField(max_length=100)
    Handed_Over_To = models.CharField(max_length=100)
    Remarks = models.TextField()
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Guest_Name
    
