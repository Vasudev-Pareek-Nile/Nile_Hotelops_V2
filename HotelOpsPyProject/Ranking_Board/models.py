from django.db import models
from django.utils import timezone

# Create your models here.
class Hotel_Ranking(models.Model):
    HotelName = models.CharField(max_length=255,null=True,blank=True)
    HotelID = models.BigIntegerField(default=0,db_index=True)
    date = models.DateField() 

    # TripAdvisor
    ta_ranking = models.CharField(max_length=10,null=True,blank=True)
    ta_nrr = models.CharField(max_length=10,null=True,blank=True)

    # Google Review
    google_ranking = models.CharField(max_length=10,null=True,blank=True)
    google_nrr = models.CharField(max_length=10,null=True,blank=True)

    # MMT
    mmt_ranking = models.CharField(max_length=10,null=True,blank=True)
    mmt_nrr = models.CharField(max_length=10,null=True,blank=True)

    # Booking.com
    booking_ranking = models.CharField(max_length=10,null=True,blank=True)
    booking_nrr = models.CharField(max_length=10,null=True,blank=True)
    
    # booking_ranking = models.IntegerField(null=True, blank=True)
    # booking_nrr = models.FloatField(null=True, blank=True)

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(null=True,blank=True)
    IsDelete = models.BooleanField(default=False,db_index=True)

    class Meta:
        unique_together = ('HotelID', 'date')  # Ensure one entry per hotel per date
        ordering = ['date', 'HotelID']

    def __str__(self):
        return f"{self.hotel.name} - {self.date}"