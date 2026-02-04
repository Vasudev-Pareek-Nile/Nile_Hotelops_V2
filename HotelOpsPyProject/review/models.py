from django.db import models
from datetime import date

class upload_data(models.Model):
    hotel= models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    service = models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    room = models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    value =models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    cleanliness = models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    location =models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    review_text = models.TextField(null=True, blank=True)
    classification = models.TextField(null=True, blank=True)
    review_title = models.CharField(max_length=255, null=True, blank=True)
    management_response = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=100, null=True, blank=True)
    reply_date = models.DateField(blank=True, null=True)
    reviewer=  models.CharField(max_length=255, null=True, blank=True)
    OrganizationID =models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FileUpload(models.Model):
    OrganizationID = models.CharField(max_length=255)
    data = models.JSONField()  
    averages = models.JSONField()
    source_counts = models.JSONField()
    classification_counts = models.JSONField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    


class OrganizationUrls(models.Model):
    OrganizationID = models.BigIntegerField()
    makemytrip_url = models.URLField(max_length=2000,blank=True)
    tripadvisor_url = models.URLField(max_length=2000,blank=True)
    booking_url = models.URLField(max_length=2000,blank=True)
    agoda_url= models.URLField(max_length=2000,blank=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f"Organization {self.OrganizationID}"

class PartnerRating(models.Model):
    OrganizationID = models.BigIntegerField()
    partner_type=models.CharField(max_length=200, null=False, blank=True)
    overall_rating=models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    service = models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    room = models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    value = models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    cleanliness = models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    location = models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    facilities=models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    food=models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    wifi=models.DecimalField(null=True, blank=True,decimal_places =2,max_digits=12)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
