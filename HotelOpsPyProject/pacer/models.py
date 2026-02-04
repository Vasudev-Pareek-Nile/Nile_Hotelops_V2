from django.db import models
from datetime import date 
from datetime import timedelta
from datetime import datetime, timedelta 
# Create your models here.
class HotelOpDetails(models.Model):
    opening_date = models.DateField(default = date.today)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    

class Task(models.Model):
    
    task_name = models.CharField(max_length=250)
    add_info = models.TextField(max_length=500,null=True,blank=True)
    DayBefore = models.PositiveIntegerField(blank=True,null=True)
    
    responsible_user = models.CharField(max_length=200,null=True,blank=True)
    department = models.CharField(max_length=200,null=True,blank=True)
    project= models.CharField(max_length=200,null=True,blank=True)
    link_of_project = models.URLField(max_length=200,null=True,blank=True)
    link_title = models.CharField(max_length=50,null=True,blank=True)
    contact_full_name =models.CharField(max_length=100)
    contact_email = models.EmailField(max_length=75 , null= True )
    status =models.CharField(max_length=200,null=True,blank=True)    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
   
    
    
    def __str__(self):
        return self.task_name
    


    def calculate_target_date(self):
        if self.DayBefore is not None:
            
            current_date = datetime.now().date()
            
            target_date = current_date + timedelta(days=self.DayBefore)
            return target_date
        else:
            return None

class projectss(models.Model):
    project_name = models.CharField(max_length=250)
    project_open_date = models.DateField(default = date.today)
    Location = models.CharField(max_length=250)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)


class user (models.Model):
    name = models.CharField(max_length=250) 
    userid = models.BigIntegerField(default=0)
    type = models.CharField(max_length=250)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)  
    def __str__(self):
        return self.name
    


