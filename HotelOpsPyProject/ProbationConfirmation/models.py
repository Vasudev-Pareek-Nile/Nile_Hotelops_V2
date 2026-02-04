from django.db import models
from datetime  import datetime

class Category_Master(models.Model):
    Category = models.CharField(max_length=255,null=True,blank=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=datetime.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=datetime.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.Category



class Item_Master(models.Model):
    Category =models.ForeignKey(Category_Master,on_delete=models.CASCADE)
    Item = models.TextField(null=True,blank=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=datetime.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=datetime.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.Item} == {self.Category}'



class Emp_Confirmation_Master(models.Model):
    EmpCode = models.CharField(max_length=255, null=True,blank = True)
    EmpName = models.CharField(max_length=255, null=True,blank = True)
    Position = models.CharField(max_length=255, null=True,blank = True)
    Department = models.CharField(max_length=255, null=True,blank = True) 
    JoiningDate =  models.DateField()
    ConfDate =  models.DateField()
    EmpConfirm =  models.BooleanField(default=False) 
    Extended = models.CharField(max_length=255, null=True,blank = True)  

    
    Strengths =  models.TextField(null=True,blank=True)
    Improvement = models.TextField(null=True,blank=True) 
    Guidelines = models.BooleanField(default=False) 
    Trainingattended  = models.TextField(null=True,blank=True) 
    LOC_ID   = models.IntegerField(null=True,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=datetime.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=datetime.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.EmpCode


class Emp_Confirmation_Details(models.Model):
    Emp_Confirmation_Master =  models.ForeignKey(Emp_Confirmation_Master,on_delete=models.CASCADE)
    Item_Master = models.ForeignKey(Item_Master,on_delete=models.CASCADE)
    IsYes =  models.BooleanField(default=False)
    Remarks = models.TextField(null=True,blank=True) 

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=datetime.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=datetime.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.Emp_Confirmation_Master.EmpCode






class Emp_Confirmation_Objective_Details(models.Model):
    Emp_Confirmation_Master =  models.ForeignKey(Emp_Confirmation_Master,on_delete=models.CASCADE)
    ObjectiveName = models.TextField()

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=datetime.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=datetime.now)
    IsDelete = models.BooleanField(default=False)



class Emp_Confirmation_Objective_Goals(models.Model):
    Emp_Confirmation_Objective_Details = models.ForeignKey(Emp_Confirmation_Objective_Details,on_delete=models.CASCADE)
    GoalName = models.TextField()
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=datetime.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=datetime.now)
    IsDelete = models.BooleanField(default=False)





class Confirm_Date(models.Model):
    Month = models.CharField(max_length=50,null=True,blank=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=datetime.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=datetime.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.Month
