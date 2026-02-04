from django.db import models
from django.utils import timezone
import datetime


# # Create your models here.
class Item_Master(models.Model):
    Item = models.CharField(max_length=255,null=False,blank=False)

    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

class Entry_Master(models.Model):
    EntryDate = models.DateField(default=timezone.now)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)


class Entry_Details(models.Model):
    Item_Master = models.ForeignKey(Item_Master, on_delete=models.CASCADE)
    Entry_Master = models.ForeignKey(Entry_Master, on_delete=models.CASCADE)
    Value = models.CharField(max_length=255,null=False,blank=False)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)



class MedalliaData(models.Model):
    EntryDate = models.DateField(default=timezone.now)
    PropertyName = models.CharField(max_length=255)

    GuestName = models.CharField(max_length=255,null=True,blank=True)
    Month = models.CharField(max_length=255,null=True,blank=True) 
    CheckInDate = models.DateField(null=True, blank=True)
    CheckInProcess = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    Cleanliness = models.CharField(max_length=10, null=True, blank=True)
    ConditionOfHotel = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    WohProgramExperience = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    StaffHelpfulness = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    RoomNo = models.IntegerField(null=True, blank=True)
    ResponseDate = models.DateField(null=True, blank=True)
    CheckOutDate = models.DateField(null=True, blank=True)
    WorkingOrder = models.CharField(max_length=10,null=True, blank=True)
    CustomerService = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    BreakfastExperience = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    SpaExperience = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    DeliveryHkServices = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    NPS = models.CharField(max_length=255,null=True, blank=True)
    StaffResponsiveness = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    WohAppExperience = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    OverallFnbExperience = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    PropertyAnticipatedGuestNeeds =models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    LpMemberSatisfaction = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    Comments = models.TextField(null=True, blank=True)

    # Common Fields
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)


    # class Meta:
    #     db_table = 'MedalliaData'  # or the exact name returned in Step 1



class ReviewPro(models.Model):
    EntryDate = models.DateField(default=timezone.now)

    Reviewer = models.CharField(max_length=255)
    Month = models.CharField(max_length=255,null=True,blank=True) 
    ReviewRating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    Classification = models.CharField(max_length=50, null=True, blank=True)
    Cleanliness = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    Location = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    LocationScore = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    Room = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    RoomScore = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    GriTM = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    PublishedDate = models.DateField(default=timezone.now, null=True, blank=True)
    RatingScale = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    Service = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    CleanlinessScore = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    Value = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ValueScore = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    Gastronomy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    GastronomyScore = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    

    Country = models.CharField(max_length=100, null=True, blank=True)
    Source = models.CharField(max_length=255, null=True, blank=True)
    ReviewScore = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ServiceScore = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    DepartmentRatingScale = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ReviewTitle = models.CharField(max_length=255, null=True, blank=True)
    ReviewText = models.TextField(null=True, blank=True)

    # Common Fields
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
