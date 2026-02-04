from django.db import models

from datetime import date 
from datetime import datetime


class Designation(models.Model):
    keyword = models.CharField(max_length=100)


    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.keyword


class EmailMessage(models.Model):
    MessageID = models.CharField(max_length=1000,default='', blank=True, null = True)
    To = models.CharField(max_length=1000,default='', blank=True, null= True)
    Subject = models.CharField(max_length=1000,default='', blank=True, null= True)
    Sender = models.CharField(max_length=1000,default='', blank=True, null= True)
    ReceivedTime = models.CharField(max_length=1000,default='', blank=True, null= True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default = datetime.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default = datetime.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.keyword

class Resume(models.Model):
    MessageID = models.CharField(max_length=1000,default='', blank=True, null = True)
    name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    designation = models.ManyToManyField(Designation)
    
    
    file_id = models.CharField(max_length=200,null=True)
    file_name = models.CharField(max_length=200, null=True)


    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)


    def __str__(self):
        return self.name

