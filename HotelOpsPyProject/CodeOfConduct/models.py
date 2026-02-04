from django.db import models
from django.utils import timezone
from .azuree import upload_file_to_azure






import os
import re
from django.utils import timezone

class EmpCodeofConductDocMaster(models.Model):
    Empcode = models.CharField(max_length=255, blank=True, null=True)
    FileName = models.CharField(max_length=255, blank=True, null=True)  
    FileTitle = models.CharField(max_length=255, blank=True, null=True)  
    Conductdate = models.DateField(null=True, blank=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.FileName:
            uploaded_file_name = upload_file_to_azure(self.FileName)
            if uploaded_file_name:
                self.FileName = uploaded_file_name

            
            if not self.FileTitle:  
                
                file_name = os.path.basename(uploaded_file_name)

                
                cleaned_file_name = re.sub(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', '', file_name)

               
                self.FileTitle = cleaned_file_name.replace('__', '_').strip('_')

        super(EmpCodeofConductDocMaster, self).save(*args, **kwargs)



class Docmaster(models.Model):
    samplefile = models.CharField(max_length=255, blank=True, null=True)  
