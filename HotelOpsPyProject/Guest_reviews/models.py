from django.db import models
from datetime import datetime
from app.models import OrganizationMaster
import uuid
from django.utils import timezone

# Create your models here.
class HotelStay(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    hotel = models.ForeignKey(OrganizationMaster, on_delete=models.CASCADE)
    sources = models.TextField()  # Storing sources as comma-separated values
    date = models.DateField(default=timezone.now)
    gm_date = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to="static\Images\GuestReview", blank=True,null=True)
    room_no = models.CharField(max_length=20,blank=True ,null=True)
    guest_name = models.CharField(max_length=255,blank=True,null=True)
    stay_days = models.PositiveIntegerField(blank=True,null=True)
    complaint = models.TextField(blank=True,null=True)
    process_lapse = models.TextField(blank=True,null=True)
    gm_comment = models.TextField(blank=True,null=True)
    status = models.IntegerField(default=0)
    Action_Plan=models.TextField(blank=True,null=True)
    
    
    # OrganizationID = models.ForeignKey(OrganizationMaster, on_delete=models.CASCADE)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.guest_name}'s stay at {self.hotel} - Room {self.room_no}"