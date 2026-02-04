from django.db import models
from datetime import date

# For Creating Model Of Uniform Inventory Sheet


class Uniform_Inventory_Sheet(models.Model):
    From = models.DateField()
    To = models.DateField()
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=date.today)
    IsDelete = models.BooleanField(default=False)


# For Creating Model of item Master
class Uniform_Item_Master(models.Model):
    Item_Title_Name = models.CharField(max_length=100)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.Item_Title_Name

# For Creating Model of item Master


class Uniform_Item_detail(models.Model):
    Uniform_Inventory_Sheet = models.ForeignKey(
        Uniform_Inventory_Sheet, on_delete=models.CASCADE)
    Uniform_Item_Master = models.ForeignKey(
        Uniform_Item_Master, on_delete=models.CASCADE)
    Fresh = models.CharField(max_length=100)
    Soiled = models.CharField(max_length=100)
    Total = models.CharField(max_length=100)

    # def __str__(self):
    #     return self.Uniform_Item_Master
