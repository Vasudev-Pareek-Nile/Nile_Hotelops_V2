from django.db import models
from datetime import datetime
import qrcode
import base64
import uuid
from django.utils import timezone
from io import BytesIO
# Create your models here.
class IT_Inventory(models.Model):
    type=models.CharField(max_length=255,blank=True,null=True)
    Description=models.CharField(max_length=255,blank=True,null=True)
    SerialNo=models.CharField(max_length=255,blank=True,null=True)
    Make=models.CharField(max_length=255,blank=True,null=True)
    Model_No=models.CharField(max_length=255,blank=True,null=True)
    Commissioning_Date=models.CharField(max_length=255,blank=True,null=True)
    Area=models.CharField(max_length=255,blank=True,null=True)
    Remarks=models.CharField(max_length=255,blank=True,null=True)
    computer_name=models.CharField(max_length=255,blank=True,null=True)
    ip=models.CharField(max_length=255,blank=True,null=True)
    Warrantiy_Status=models.CharField(max_length=255,blank=True,null=True)
    Warrantiy_start=models.CharField(max_length=255,blank=True,null=True)
    Warrantiy_end=models.CharField(max_length=255,blank=True,null=True)
    amctype=models.CharField(max_length=255,blank=True,null=True)
    amcstart=models.CharField(max_length=255,blank=True,null=True)
    amcend=models.CharField(max_length=255,blank=True,null=True)
    hardware_AMC_Yearly_Expense=models.CharField(max_length=255,blank=True,null=True)
    AMC_Status=models.CharField(max_length=255,blank=True,null=True)
    
    hardware_quantity=models.CharField(max_length=255,blank=True,null=True)
    hardware_unit_price=models.CharField(max_length=255,blank=True,null=True)
    

    Inventory_Type=models.CharField(max_length=255,blank=True,null=True)   # Determine Hardware or Software
    

    
    softwaretype=models.CharField(max_length=255,blank=True,null=True)
    softwarename=models.CharField(max_length=255,blank=True,null=True)
    Quantity=models.CharField(max_length=255,blank=True,null=True)
    software_AMC_Start=models.CharField(max_length=255,blank=True,null=True)
    software_AMC_end=models.CharField(max_length=255,blank=True,null=True)
    software_AMC_Type=models.CharField(max_length=255,blank=True,null=True)
    Software_Quantity=models.CharField(max_length=255,blank=True,null=True)
    Software_unit_price=models.CharField(max_length=255,blank=True,null=True)
    software_AMC_Status=models.CharField(max_length=255,blank=True,null=True)
    software_AMC_Yearly_Expense=models.CharField(max_length=255,blank=True,null=True)

    
   

    

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

   
    qr_code_id = models.UUIDField(default=uuid.uuid4, editable=False)

   
    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"http://127.0.0.1:8000/IT_Inventory/Qr_details/?qr_code_id="+str(self.qr_code_id))  
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)
        return buffer.getvalue()

    
    def get_qr_code_base64(self):
        qr_code_data = self.generate_qr_code()
        return base64.b64encode(qr_code_data).decode()

    def __str__(self):
     return f"{self.SerialNo} - {self.softwaretype}"



class Master_Category(models.Model):
    Category_Type=models.CharField(max_length=255,blank=True,null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.Category_Type


class Master_Company(models.Model):
    Company_name=models.CharField(max_length=255,blank=True,null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.Company_name



class Master_Area(models.Model):
    Area_name=models.CharField(max_length=255,blank=True,null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.Area_name



class Master_Software_type(models.Model):
    software_name=models.CharField(max_length=255,blank=True,null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.software_name