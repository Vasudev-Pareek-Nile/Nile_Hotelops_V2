from django.db import models
from datetime import date 

 

class SalesEventCalendar(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=False,blank=False)
    start = models.DateField(null=False,blank=False)
    end = models.DateField(null=True,blank=True)            
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

    class Meta:  
        db_table = "saleseventscalendar"

    def __str__(self):
        return self.name