from django.db import models
from django.utils import timezone

# Create your models here.
# class PT_Config(models.Model):
#     # Title = models.CharField(null=True,blank=True,max_length=255)
#     Type  = models.CharField(null=True,blank=True,max_length=255)
#     State  = models.CharField(null=True,blank=True,max_length=255)

#     Hotel_ID = models.BigIntegerField(default=0, db_index=True)
#     Gender = models.CharField(max_length=10, null=True, blank=True)  
#     Salary_From = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
#     Salary_To = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
#     PT_Amount = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
#     Last_Month = models.IntegerField(null=True, blank=True)
#     # Last_Month = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
#     Last_Month_Value = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
#     IsActive = models.BooleanField(default=True, db_index=True)


#     # Audit fields 
#     OrganizationID = models.BigIntegerField(default=0, db_index=True)
#     CreatedBy = models.BigIntegerField(default=0)
#     CreatedDateTime = models.DateTimeField(default=timezone.now)
#     ModifyBy = models.BigIntegerField(default=0)
#     ModifyDateTime = models.DateTimeField(default=timezone.now)
#     IsDelete = models.BooleanField(default=False, db_index=True)

#     def __str__(self):
#         return f"{self.State} | {self.Salary_From}-{self.Salary_To} => {self.PT_Amount}"
    