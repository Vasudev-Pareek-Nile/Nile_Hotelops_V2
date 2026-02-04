from django.db import models
from datetime import date
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from HumanResources.models import SalaryTitle_Master
from django.utils import timezone
from datetime import date,timedelta
# Emp Appointment letter model
class LETTEROFINTENT(models.Model):
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
from app.models import EmployeeMaster
class LETTEROFINTENTEmployeeDetail(models.Model):

    # choice_prefix = (("Mr.","Mr."),("Ms.","Ms."),("Mrs.","Mrs."),("Miss.","Miss.")
    #                  )
    
    prefix = models.CharField(max_length=20,null=False,blank=False)
    emp_name = models.CharField(max_length=50,null=False,blank=False)
    InterviewID = models.CharField(max_length=50,null=False,blank=False)
   
    date_of_intent  = models.DateField(default=date.today)
    date_of_joining = models.DateField()
    department = models.CharField(max_length=50,null=False,blank=False)
    designation = models.CharField(max_length=100,blank=False,null=False)

    ctc = models.IntegerField(null=False,blank=False)
    address = models.TextField(null=False,blank=False)
   


    Issuing_manager_name = models.CharField(max_length=255,null=False,blank=False)
    Issuing_designation = models.CharField(max_length=255,null=False,blank=False)

    Reporting_Manager = models.CharField(max_length=255,null=True,blank=True)


    # data = RichTextField()
    
    # choice_vsb = (("Yes","Yes"),("No","No"))
    visible_salary_breakup=models.CharField(max_length=10,null=False,blank=False)
    visible_ctc=models.CharField(max_length=10,null=False,blank=False)

    
    file_id = models.CharField(max_length=200,null=True)
    file_name = models.CharField(max_length=200, null=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    ReIssue = models.BooleanField(default=False)
    def __str__(self):
        return self.emp_name


class LETTEROFINTENTDeletedFileofEmployee(models.Model):
    LETTEROFINTENTEmployeeDetail = models.ForeignKey(LETTEROFINTENTEmployeeDetail, on_delete=models.CASCADE)

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



# class SalaryDetails(models.Model):
#     LETTEROFINTENTEmployeeDetail = models.ForeignKey(LETTEROFINTENTEmployeeDetail, on_delete=models.CASCADE)
#     TitleID = models.BigIntegerField(default=0)
#     Title = models.CharField(default='',blank=True,null=True,max_length=200)
#     Type = models.CharField(default='',blank=True,null=True,max_length=200)
#     Monthly =models.DecimalField(default=0,blank=True,null=True,max_digits=10, decimal_places=2)
#     Annum =models.DecimalField(default=0,blank=True,null=True,max_digits=10, decimal_places=2)
#     OrderBy =models.IntegerField(default=0,blank=True,null=True)

#     OrganizationID = models.BigIntegerField(default=0)
#     CreatedBy = models.BigIntegerField(default=0)
#     CreatedDateTime = models.DateField(default = date.today)
#     ModifyBy = models.BigIntegerField(default=0)
#     ModifyDateTime = models.DateField(default = date.today)
#     IsDelete = models.BooleanField(default=False)

#     def __str__(self):
#         return self.Title



class SalaryDetails(models.Model):
    LETTEROFINTENTEmployeeDetail = models.ForeignKey(LETTEROFINTENTEmployeeDetail, on_delete=models.CASCADE)
    Salary_title = models.ForeignKey(SalaryTitle_Master, on_delete=models.CASCADE)
    Permonth = models.DecimalField(max_digits=10, decimal_places=2)
    Perannum = models.DecimalField(max_digits=15, decimal_places=2)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)






