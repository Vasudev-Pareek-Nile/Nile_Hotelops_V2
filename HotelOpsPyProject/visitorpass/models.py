from django.db import models
from datetime import date

class Visitor_Pass(models.Model):
    Date = models.DateField(default = date.today)
    In_Time = models.TimeField()
    Name = models.CharField(max_length=100)
    Purpose_Of_Visite = models.TextField()
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.Name
    
    
    
    
