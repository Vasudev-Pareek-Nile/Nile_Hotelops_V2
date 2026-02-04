from django.db import models
from datetime import datetime

from ckeditor.fields import RichTextField
from django.utils.text import slugify

from django.utils import timezone

class JobDescription(models.Model):
    
    JD_Title = models.CharField(max_length=255, blank=True, null=True)
    Department = models.CharField(max_length=255, blank=True, null=True)
    Division = models.CharField(max_length=255, blank=True, null=True)
    Position = models.CharField(max_length=255, blank=True, null=True)
    Report_To = models.CharField(max_length=255, blank=True, null=True)
    Level = models.CharField(max_length=255, blank=True, null=True)
    Signatory = models.CharField(max_length=255, blank=True, null=True)
    Effective_Date = models.DateField(default=timezone.now)
    JD_Approved_By = models.CharField(max_length=255, blank=True, null=True)
    Job_Scope = RichTextField()
    Duties_Responsibilities = RichTextField()
    Job_Knowledge_Skills = RichTextField()
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    Reference_No = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def generate_reference_number(self):
        
        department_prefix = (self.Department[:3] if self.Department else 'GEN').upper()
        position_words = self.Position.split() if self.Position else []
        position_prefix = ''.join(word[:1].upper() for word in position_words)
        position_prefix = position_prefix if position_prefix else 'POS'
        
        
        reference_prefix = f"JD-{department_prefix}-{position_prefix}"
        
       
        last_reference = JobDescription.objects.filter(
            Department=self.Department,  
            Reference_No__startswith=f"JD-{department_prefix}-"  
        ).order_by('-id').first()

        if last_reference:
            
            last_number = int(last_reference.Reference_No.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        
        return f"{reference_prefix}-{new_number:03d}"

    def save(self, *args, **kwargs):
        if not self.Reference_No:
            self.Reference_No = self.generate_reference_number()
        super(JobDescription, self).save(*args, **kwargs)