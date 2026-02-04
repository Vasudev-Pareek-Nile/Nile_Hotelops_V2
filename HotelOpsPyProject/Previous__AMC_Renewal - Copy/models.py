from django.utils import timezone 
from django.db import models

# Create your models here.

class AMC_Entry_Master(models.Model):
    EquipmentID = models.BigIntegerField(default=0)
    AMC_Start_Date = models.DateField()
    AMC_End_Date = models.DateField()
    AMCType = models.CharField(max_length=255,null=True,blank=True)
    AMC_Amount = models.BigIntegerField(default=0,blank=True, null=True)
    Final_Status = models.CharField(max_length=50, default="Pending")
    FileName = models.CharField(max_length=255,null=True,blank=True)

    # FC - Finance Department
    FC_Status = models.CharField(max_length=50, default="Pending")  # Pending, Approved, Rejected
    FC_Action = models.CharField(max_length=50)
    FC_ActionBy =models.BigIntegerField(default=0,blank=True,null=True)
    FC_ActionDateTime = models.DateTimeField(null=True,blank=True)

    # GM - General Manager
    GM_Status = models.CharField(max_length=50, default="Pending")  # Pending, Approved, Rejected
    GM_Action = models.CharField(max_length=50)
    GM_ActionBy =models.BigIntegerField(default=0,blank=True,null=True)
    GM_ActionDateTime = models.DateTimeField(null=True,blank=True)

    # CEO - Chief Executive Officer
    CEO_Status = models.CharField(max_length=50, default="Pending")  # Pending, Approved, Rejected
    CEO_Action = models.CharField(max_length=50)
    CEO_ActionBy =models.BigIntegerField(default=0,blank=True,null=True)
    CEO_ActionDateTime = models.DateTimeField(null=True,blank=True)

    Remarks = models.CharField(max_length=255,null=True,blank=True)



    # Vendor Details Fields
    VendorName  =  models.CharField(null=True,blank=True,max_length=255)
    VendorEmailAddress = models.EmailField( null=True,blank=True,max_length=254)
    VendorMobileNumber = models.CharField(null=True,blank=True,max_length=255)
    VendorSecondMobileNumber = models.CharField(null=True,blank=True,max_length=255)
    VendorLandlineNumber = models.CharField(null=True,blank=True,max_length=255)
    VendorAddress  = models.CharField(null=True,blank=True,max_length=255)
    VendorCity   = models.CharField(null=True,blank=True,max_length=255)
    VendorState  = models.CharField(null=True,blank=True,max_length=255)
    VendorPincode  = models.CharField(max_length=255,null=True,blank=True)

    # Common Fields
    OrganizationID = models.BigIntegerField(default=0)
    created_by = models.BigIntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)
    modify_by = models.BigIntegerField(default=0)
    modify_date_time = models.DateTimeField(default=timezone.now)
    is_delete = models.BooleanField(default=False)



