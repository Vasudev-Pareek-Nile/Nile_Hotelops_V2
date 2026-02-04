from django.db import models
from datetime import date 
from ckeditor.fields import RichTextField

from django.contrib.auth.models import User

# Emp Appointment letter model
class PromotionLetter(models.Model):
    name =  models.CharField(max_length=50,null=False,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    data = RichTextField()
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# Emp Details  Model
class PromotionLetterEmployeeDetail(models.Model):
    emp_code = models.CharField(max_length=200,null=False,blank=False)
    choice_prefix = (("Mr.","Mr."),("Mrs.","Mrs."),("Miss.","Miss.")
                     )
    prefix = models.CharField(choices=choice_prefix,max_length=20,default="Mr.")
    first_name = models.CharField(max_length=200,null=False,blank=False)
    last_name = models.CharField(max_length=200,null=False,blank=False)
    
    date_of_promtion  = models.DateField(default=date.today)
    
    department = models.CharField(max_length=200,null=False,blank=False)
    designation = models.CharField(max_length=100,blank=False,null=False)
    Promotiondesignation = models.CharField(max_length=100,blank=False,null=False)
    
    
    
    general_manager_name = models.CharField(max_length=200)
    data = RichTextField()
    # For File 
    file_id = models.CharField(max_length=200,null=True)
    file_name = models.CharField(max_length=200, null=True)
    
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class PromotionLetterDeletedFileofEmployee(models.Model):
    PromotionLetterEmployeeDetail = models.ForeignKey(PromotionLetterEmployeeDetail, on_delete=models.CASCADE)
    file_id = models.CharField(max_length=200,null=True)
    file_name = models.CharField(max_length=200, null=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.file_id
    