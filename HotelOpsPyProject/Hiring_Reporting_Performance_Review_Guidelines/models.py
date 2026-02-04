from django.db import models
from datetime import datetime
# Create your models here.
class hiring_data_NEW(models.Model):
    department_division = models.CharField(max_length=255, null=True, blank=True)
    positions1=models.CharField(max_length=255, null=True, blank=True)
    positions2=models.CharField(max_length=255, null=True, blank=True)
    positions3=models.CharField(max_length=255, null=True, blank=True)
    positions4=models.CharField(max_length=255, null=True, blank=True)
    reporting = models.TextField( null=True, blank=True)
    Feedback_percent1 = models.TextField( null=True, blank=True)
    Feedback_percent2 = models.TextField( null=True, blank=True)
    Feedback_percent3 = models.TextField( null=True, blank=True)
    Feedback_percent4 = models.TextField( null=True, blank=True)
    Feedback_position1 = models.TextField( null=True, blank=True)
    Feedback_position2 = models.TextField( null=True, blank=True)
    Feedback_position3 = models.TextField( null=True, blank=True)
    Feedback_position4 = models.TextField( null=True, blank=True)
    hiring = models.TextField( null=True, blank=True)
    fairing = models.TextField( null=True, blank=True)
    property_transfer=models.TextField( null=True, blank=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(auto_now_add=True)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(auto_now_add=True)
    IsDelete = models.BooleanField(default = False)
    def __str__(self):
        return self.department_division
        