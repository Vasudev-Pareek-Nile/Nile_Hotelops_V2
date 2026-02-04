from datetime import date
from django.db import models
 # IsWarningIssuedList = (
    #     ('Yes','Yes'),
    #     ('No','No'),
    # )
    # LastWarningLatterList = (
    #     ('Verbal','Verbal'),
    #     ('Written','Written'),
    #     ('Final','Final')
    # )
# Creating Models For Full and Final Settlement

class EmpTerminationModel(models.Model):
    Name = models.CharField(max_length=100)
    Emp_Code = models.CharField(max_length=100)
    DOJ =  models.DateField(default = date.today)
    Date_Of_Termination =  models.DateField(default = date.today)
    Dept = models.CharField(max_length=100)
    Designation = models.CharField(max_length=100)
   

    IsWarningIssued = models.CharField(max_length=250,null=True,blank=True)
    LastWarningLatter = models.CharField(max_length=250,null=True,blank=True)

    Remarks = models.TextField(null=True,blank=True)

    reviewed_manager_name = models.CharField(max_length=255,null=True,blank=True)
    reviewed_designation = models.CharField(max_length=255,null=True,blank=True)
 
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.Name
    
    
    