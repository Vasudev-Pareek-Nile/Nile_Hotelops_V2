from django.db import models
from datetime import date
from django.utils import timezone

# For Making Model 
class Linen_Inventory_Sheet(models.Model):
    From = models.DateField()
    To =  models.DateField()
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
# For Creating Master Model
class Linen_Item_Master(models.Model):
    Item_Title_Name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.Item_Title_Name
    
# For Creating Model Of Linen Item Master
class Linen_Item_Details(models.Model):
    Linen_Inventory_Sheet = models.ForeignKey(Linen_Inventory_Sheet, on_delete=models.CASCADE)
    Linen_Item_Master = models.ForeignKey(Linen_Item_Master, on_delete=models.CASCADE)
    Laundry = models.CharField(max_length=100)
    Linen_Room = models.CharField(max_length=100)
    Stores = models.CharField(max_length=100)
    Missing = models.CharField(max_length=100)
    Total = models.CharField(max_length=100)
    
    
    # def __str__(self):
    #     return self.Item_Title_Name
    
    

