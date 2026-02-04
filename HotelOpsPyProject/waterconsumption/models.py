from django.db import models
from datetime import date
# Model For Water Consumption
class waterconsumptionreport(models.Model):
    EnteryDate = models.DateField(default=date.today)
    RawWaterPPM = models.CharField(max_length=100)
    RawWaterpH = models.CharField(max_length=100)
    RawWaterTDS = models.CharField(max_length=100)
    SoftWaterPPM = models.CharField(max_length=100)
    SoftWaterpH = models.CharField(max_length=100)
    SoftWaterTDS = models.CharField(max_length=100)
    ROWaterPPM = models.CharField(max_length=100)
    ROWaterpH = models.CharField(max_length=100)
    ROWaterTDS = models.CharField(max_length=100)
    LaundryWaterPPM = models.CharField(max_length=100)
    LaundryWaterpH = models.CharField(max_length=100)
    LaundryWaterTDS = models.TextField(max_length=100)
    
    
    def __str__(self):
        return self.LaundryWaterTDS
    
    
    
    