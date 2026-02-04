from django.db import models
from datetime import date

# For Making Model
class clearnce_form(models.Model):
    Name = models.CharField(max_length=100)
    Separation_Date = models.DateField()
    Position = models.CharField(max_length=100)
    EmpCode = models.CharField(max_length=100,blank=True,null=True,default=None)
    Finishing_Time = models.TimeField(blank=True,null=True,default=None)
    type = (
        ('Yes','Yes'),
        ('NA','NA'),
    )
    Resignation_Letter = models.CharField(max_length=50,choices=type,blank=False, null=False)
    type = (
        ('Yes','Yes'),
        ('NA','NA'),
    )
    Acc_Of_Resign =  models.CharField(max_length=50,choices=type,blank=False, null=False)
    type = (
        ('Yes','Yes'),
        ('NA','NA'),
    )
    Notice_Period_Served = models.CharField(max_length=50,choices=type,blank=False, null=False)
    type = (
        ('Yes','Yes'),
        ('NA','NA'),
    )
    Notice_Period_Waived_Off =  models.CharField(max_length=50,choices=type,blank=False, null=False)
    type = (
        ('Yes','Yes'),
        ('NA','NA'),
    )
    Exit_Interview_By_Hr = models.CharField(max_length=50,choices=type,blank=False, null=False)
    type = (
        ('Yes','Yes'),
        ('NA','NA'),
    )
    Full_And_Final_Settlement = models.CharField(max_length=50,choices=type,blank=False, null=False)
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    

    
    def __str__(self):
        return self.Name
    
 
# For Making Clerance Item Master  
class Clerance_Item_Master(models.Model):
    ItemTitle = models.CharField(max_length=100)
    type = (
        ('HR','HR'),
        ('Finance','Finance'),
        ('IT','IT'),
        ('House Keeping','House Keeping'),
        ('Security','Security'),
        ('Purchase','Purchase'),
    )
    
    Department = models.CharField(max_length=50,choices=type)
    
    def __str__(self):
        return self.ItemTitle 

    
# For Creating Clerance Form Details
class clearnce_formdetails(models.Model):
    clearnce_form = models.ForeignKey(clearnce_form, on_delete=models.CASCADE)
    Clerance_Item_Master = models.ForeignKey(Clerance_Item_Master, on_delete=models.CASCADE)
    ReturnedTo = models.CharField(max_length=100)
    ReceivedBy = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.Clerance_Item_Master