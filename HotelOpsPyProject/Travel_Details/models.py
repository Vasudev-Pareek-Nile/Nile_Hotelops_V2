from django.db import models
from datetime import date,timedelta
from django.utils import timezone

# Create your models here.
class TravelRequest(models.Model):
    booked_by = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    booking_date = models.DateField()

    organization_id = models.BigIntegerField(default=0)
    created_by = models.BigIntegerField(default=0)
    created_datetime = models.DateTimeField(default=timezone.now)
    modify_by = models.BigIntegerField(default=0, null=True,blank=True)
    modify_datetime = models.DateTimeField(default=timezone.now)
    is_delete = models.BooleanField(default=False)
    deleted_by = models.BigIntegerField(default=0, null=True,blank=True)
    deleted_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.booking_date}"
    

class TravelEntry(models.Model):
    TRAVEL_MODE_CHOICES = [
        ('Train', 'Train'),
        ('Bus', 'Bus'),
        ('Flight', 'Flight'),
        ('By Road', 'By Road'),
    ]

    travel_request = models.ForeignKey(TravelRequest, on_delete=models.CASCADE, related_name='entries')
    travel_Date_from = models.DateField(null=True,blank=True)
    travel_Date_to = models.DateField(null=True, blank=True)
    travel_route_from = models.CharField(null=True,blank=True, max_length=255)
    travel_route_to = models.CharField(null=True,blank=True, max_length=255)
    fare = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    travel_mode = models.CharField(null=True, blank=True, max_length=10, choices=TRAVEL_MODE_CHOICES)
    pnr = models.CharField(null=True,blank=True,max_length=255)
    comment = models.TextField(blank=True, null=True)
    billing = models.CharField(null=True,blank=True, max_length=255)
    # billing_file = models.FileField(upload_to='billings/', null=True, blank=True)

    organization_id = models.BigIntegerField(default=0)
    created_by = models.BigIntegerField(default=0)
    created_datetime = models.DateTimeField(default=timezone.now)
    modify_by = models.BigIntegerField(default=0, null=True, blank=True)
    modify_datetime = models.DateTimeField(default=timezone.now)
    is_delete = models.BooleanField(default=False)
    deleted_by = models.BigIntegerField(default=0, null=True,blank=True)
    deleted_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.travel_route_from} {self.travel_route_to} - {self.travel_mode}"
