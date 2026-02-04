from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

# class PublicAccessUrl(models.Model):
#     UniqueToken = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     ModelName = models.CharField(null=False, blank=False, max_length=255)
#     AppName = models.CharField(null=False, blank=False, max_length=255)
#     InstanceId = models.CharField(null=False, blank=False, max_length=255)
    
#     IsClicked = models.BooleanField(default=False)
#     LastClicked = models.DateTimeField(null=True, blank=True)
#     ExpiryDatetime = models.DateTimeField(default=timezone.now() + timedelta(days=7))  
#     def is_expired(self):
#         return timezone.now() > self.ExpiryDatetime



def default_expiry():
    return timezone.now() + timedelta(days=7)

class PublicAccessUrl(models.Model):
    UniqueToken = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    ModelName = models.CharField(null=False, blank=False, max_length=255)
    AppName = models.CharField(null=False, blank=False, max_length=255)
    InstanceId = models.CharField(null=False, blank=False, max_length=255)

    IsClicked = models.BooleanField(default=False)
    LastClicked = models.DateTimeField(null=True, blank=True)
    ExpiryDatetime = models.DateTimeField(default=default_expiry)

    def is_expired(self):
        return timezone.now() > self.ExpiryDatetime
