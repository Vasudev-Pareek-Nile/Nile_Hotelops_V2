from django.db import models
from datetime import date



    
class  FixedExpenseDepartmentMaster(models.Model):
    title = models.CharField(max_length = 200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    sort_order =models.IntegerField()

    
class  FixedExpenseMaster(models.Model):
    FixedExpenseDepartmentMaster =models.ForeignKey(FixedExpenseDepartmentMaster, on_delete=models.CASCADE)
    sort_order =models.IntegerField()
    title = models.CharField(max_length = 200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
   
    
class FixedExpenseEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    Total = models.DecimalField(decimal_places=2,max_digits=12 )
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
  
class FixedExpenseEntryDetails(models.Model):
    FixedExpenseMaster =models.ForeignKey(FixedExpenseMaster, on_delete=models.CASCADE)
    FixedExpenseEntryMaster =models.ForeignKey(FixedExpenseEntryMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    type = (
        ('Yes','Yes'),
        ('N/A','N/A'),
    )
    Isapplicable = models.CharField(max_length=50,choices=type)
    Remakrs = models.CharField(max_length=500)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
