from django.db import models
from datetime import datetime
# Create your models here.

from django.utils import timezone

class Rating(models.Model):
    rating_name = models.CharField(max_length=255, blank=True, null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.rating_name



class Experience(models.Model):
    experience_name = models.CharField(max_length=255, blank=True, null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)    
    def __str__(self):
        return self.experience_name



class Reason_for_Leaving(models.Model):
    Reason_Leaving_name = models.CharField(max_length=255, blank=True, null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)  
    def __str__(self):
        return self.Reason_Leaving_name


class Exitinterviewdata(models.Model):
    hotel = models.BigIntegerField(default=0,blank=True, null=True)
    Employee_Code = models.CharField(max_length=255, blank=True, null=True)
    EmpName = models.CharField(max_length=255, blank=True, null=True)
    
    Job_Title = models.CharField(max_length=255, blank=True, null=True)
    DateofJoining = models.CharField(max_length=255, blank=True, null=True)
    Department = models.CharField(max_length=255, blank=True, null=True)
    DateofLeaving = models.CharField(max_length=255, blank=True, null=True)
    NoticePeriod = models.CharField(max_length=255, blank=True, null=True)  
    ReasonForLeaving = models.CharField(max_length=255, blank=True, null=True) 
    FinalComment=models.CharField(max_length=255, blank=True, null=True) 
    Resign=models.CharField(max_length=255, blank=True, null=True)
    Termination=models.CharField(max_length=255, blank=True, null=True)

    rehire=models.BooleanField(default=True)  
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)    
    def __str__(self):
        return self.EmpName



class exitinterviewmaster(models.Model):
    Exitinterviewdata=models.ForeignKey(Exitinterviewdata,on_delete=models.CASCADE)
    Experience=models.ForeignKey(Experience,on_delete=models.CASCADE)
    chekdata=models.CharField(max_length=255,blank=True,null=True)
    remarkexit=models.CharField(max_length=255,blank=True,null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)    
    



class ExitRating(models.Model):
    Exitinterviewdata=models.ForeignKey(Exitinterviewdata,on_delete=models.CASCADE)
    Rating=models.ForeignKey(Rating,on_delete=models.CASCADE)
    remarks=models.CharField(max_length=255,blank=True,null=True)
   
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)    
    