from datetime import date
from django.db import models

# For Creating Models for Office Snag List
class Office_Snag_Registration_Form(models.Model):
    Area = models.CharField(max_length=100)
    Date =models.DateField(default = date.today)
    # Remarks = models.TextField()
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.Area
    
    
 # For Making class For Office Snag Master
class Snag_Category_Master(models.Model):
    
    Category_Name  = models.CharField(max_length=100)
    Category_Title_Name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.Category_Name
    
    
# For Creating Reference Form Details
class Snag_Category_details(models.Model):
    Office_Snag_Registration_Form = models.ForeignKey(Office_Snag_Registration_Form, on_delete=models.CASCADE)
    Snag_Category_Master = models.ForeignKey(Snag_Category_Master, on_delete=models.CASCADE)
    # Category_Title_Name = models.CharField(max_length=100)
    type = (
        ('Yes','Yes'),
        ('NA','NA'),
    )
    Status = models.CharField(max_length=50,choices=type,blank=False, null=False)
    Remarks = models.TextField()
    
    
    
    # def __str__(self):
    #     return self.Habits

    
