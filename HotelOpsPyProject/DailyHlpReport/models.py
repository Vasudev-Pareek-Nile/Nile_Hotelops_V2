from django.db import models
from datetime import date

# For Registering Model
class Dailyhlpreportform(models.Model):
    Date = models.DateField(default = date.today)
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
   
    
# For registering Category
class Category_Item_Master(models.Model):
    Category_Name = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.Category_Name
    
# For Creating Model of item Master
class Category_Item_detail(models.Model):
    Category_Item_Master = models.ForeignKey(Category_Item_Master, on_delete=models.CASCADE)
    ItemTitle =  models.CharField(max_length=100)
  

    
    

    
   