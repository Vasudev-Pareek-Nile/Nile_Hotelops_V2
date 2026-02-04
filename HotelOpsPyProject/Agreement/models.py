from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Master_title(models.Model):
    artical_number = models.CharField(max_length=20,blank=True ,null=True)
    name_artical = models.CharField(max_length=500,blank=True ,null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.artical_number 
    


class Master_subartical(models.Model):
    subartical_number = models.CharField(max_length=30,blank=True ,null=True)
    sub_artical = models.CharField(max_length=4000,blank=True ,null=True)

    Master_title = models.ForeignKey(Master_title, on_delete=models.CASCADE)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.subartical_number 
    

from django.utils import timezone
class Master_childartical(models.Model):
    childartical_number = models.CharField(max_length=20,blank=True ,null=True)
    child_artical = models.CharField(max_length=4000,blank=True ,null=True)

    Master_subartical = models.ForeignKey(Master_subartical, on_delete=models.CASCADE)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.childartical_number   
    

class Master_subchildartical(models.Model):
    childsubartical_number = models.CharField(max_length=20,blank=True ,null=True)
    childsub_artical = models.CharField(max_length=4000,blank=True ,null=True)

    Master_childartical = models.ForeignKey(Master_childartical, on_delete=models.CASCADE)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.childsubartical_number       


class agreement(models.Model):
    company_name = models.CharField(max_length=255,blank=True ,null=True)
    address = models.CharField(max_length=255,blank=True ,null=True)
    pan_number = models.CharField(max_length=255,blank=True ,null=True)
    Director_Name=models.CharField(max_length=255,blank=True ,null=True)
    Near_Location=models.CharField(max_length=255,blank=True ,null=True)
    Name_of_Hotel=models.CharField(max_length=255,blank=True ,null=True)
    Number_of_Room=models.CharField(max_length=255,blank=True ,null=True)
    Years=models.CharField(max_length=255,blank=True ,null=True)
    percentage=models.CharField(max_length=255,blank=True ,null=True)
    sum_of_inr=models.CharField(max_length=255,blank=True ,null=True) 
    license_fee =models.CharField(max_length=255,blank=True ,null=True) 
    Management_Services_N_N =models.CharField(max_length=255,blank=True ,null=True)
    
    start_date=models.DateField(default=timezone.now)
    end_date=models.DateField(default=timezone.now)
    status = models.IntegerField(default=0)
    Owner_Attention=models.CharField(max_length=255,blank=True ,null=True)
    Owner_Address=models.CharField(max_length=255,blank=True ,null=True)
    Owner_Tel_No=models.CharField(max_length=255,blank=True ,null=True)
    Owner_Fax_No=models.CharField(max_length=255,blank=True ,null=True)
    Owner_Email_Id=models.CharField(max_length=255,blank=True ,null=True)
    Operator_Attention=models.CharField(max_length=255,blank=True ,null=True)
    Operator_Address=models.CharField(max_length=255,blank=True ,null=True)
    Operator_Tel_No=models.CharField(max_length=255,blank=True ,null=True)
    Operator_Fax_No=models.CharField(max_length=255,blank=True ,null=True)
    Operator_Email_Id =models.CharField(max_length=255,blank=True ,null=True)
    Authorized_Director=models.CharField(max_length=255,blank=True ,null=True)
    Name_Witness1=models.CharField(max_length=255,blank=True ,null=True) 
    Name_Witness2=models.CharField(max_length=255,blank=True ,null=True)
    

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.company_name
    
import os
from uuid import uuid4
from django.db import models
from django.utils import timezone

class uplodede(models.Model):
    def unique_file_path(instance, filename):
        """Generate a unique filename for the uploaded file."""
        base_filename, file_extension = os.path.splitext(filename)
        unique_identifier = uuid4().hex
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        new_filename = f"{timestamp}_{unique_identifier}{file_extension}"
        return os.path.join('static', 'Images', 'agreement', new_filename)    
    
    agreement = models.ForeignKey(agreement, on_delete=models.CASCADE)
    pdf_filenn = models.FileField(upload_to=unique_file_path, blank=True, null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return f"Uplodede ID: {self.id}" 
    



def update_expired_agreements():
        now = timezone.now().date()
        expired_count = agreement.objects.filter(end_date__lt=now)

        for exp in expired_count:
            exp.status = -1
            exp.save()    