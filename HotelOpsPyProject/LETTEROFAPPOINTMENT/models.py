from django.db import models
from datetime import date 
from ckeditor.fields import RichTextField

from django.contrib.auth.models import User
from django.utils import timezone

# Emp Appointment letter mod
class LETTEROFAPPOINTMENT(models.Model):
    name =  models.CharField(max_length=50,null=False,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    data = RichTextField()
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    
# Emp Details  Model
class LOALETTEROFAPPOINTMENTEmployeeDetail(models.Model):
    emp_code = models.CharField(max_length=200,null=False,blank=False)
    EmpID = models.CharField(max_length=200,null=True,blank=True, default=0)


    prefix = models.CharField(max_length=20,null=False,blank=False)
    first_name = models.CharField(max_length=200,null=False,blank=False)
    last_name = models.CharField(max_length=200,null=False,blank=False)
    mobile_number = models.CharField(max_length=250)
    email = models.EmailField(max_length=254,null=False,blank=False)
    date_of_appointment  = models.DateField(default=timezone.now)
    date_of_joining = models.DateField()
    department = models.CharField(max_length=200,null=False,blank=False)
    designation = models.CharField(max_length=200,blank=False,null=False)
    Reporting_to_designation = models.CharField(max_length=200,blank=True,null=True)
    # choice_grade = (("A","A"),("T","T"),("E","E"),("M","M"),("M1","M1"),("M2","M2"),("M3","M3"),("M4","M4"),("M5","M5"),("M6","M6"),
    #                  )
    
    # grade = models.CharField(choices=choice_grade,max_length=5,default="A")
    
    level = models.CharField(max_length=200,null=False,blank=False)
    basic_salary = models.IntegerField(null=False,blank=False)
    address = models.TextField()
   

    file_id = models.CharField(max_length=200,null=True)
    file_name = models.CharField(max_length=200, null=True)
     
    Hr_Name = models.CharField(max_length=255,null=False,blank=False)
    Hr_Designation = models.CharField(max_length=255,null=False,blank=False)
    
    Issuing_manager_name = models.CharField(max_length=255,null=False,blank=False)
    Issuing_designation = models.CharField(max_length=255,null=False,blank=False)
    FinalHTML = models.TextField(null=True, blank=True)
    IsSaved = models.BooleanField(default=False, null=True, blank=True)
    

   
    HotelID = models.BigIntegerField(default=0)
    IsChecklist_Created = models.BooleanField(default=False,null=True,blank=True)
    
    HR = models.BooleanField(default=False,null=True,blank=True)
    HRCreatedBy = models.BigIntegerField(default=0,null=True,blank=True)
    HRCreatedDateTime = models.DateField(default=timezone.now,null=True,blank=True)
    
    HK = models.BooleanField(default=False,null=True,blank=True)
    HKCreatedBy = models.BigIntegerField(default=0,null=True,blank=True)
    HKCreatedDateTime = models.DateField(default=timezone.now,null=True,blank=True)
    
    IT = models.BooleanField(default=False,null=True,blank=True)
    ITCreatedBy = models.BigIntegerField(default=0,null=True,blank=True)
    ITCreatedDateTime = models.DateField(default=timezone.now,null=True,blank=True)
    
    FNB = models.BooleanField(default=False,null=True,blank=True)
    FNBCreatedBy = models.BigIntegerField(default=0,null=True,blank=True)
    FNBCreatedDateTime = models.DateField(default=timezone.now,null=True,blank=True)
    
    Finance = models.BooleanField(default=False,null=True,blank=True)
    FinanceCreatedBy = models.BigIntegerField(default=0,null=True,blank=True)
    FinanceCreatedDateTime = models.DateField(default=timezone.now,null=True,blank=True)
    
    DEPT = models.BooleanField(default=False,null=True,blank=True)
    DEPTCreatedBy = models.BigIntegerField(default=0,null=True,blank=True)
    DEPTCreatedDateTime = models.DateField(default=timezone.now,null=True,blank=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    




class LETTEROFAPPOINTMENTDeletedFileofEmployee(models.Model):
    LETTEROFEXPERIENCEEmployeeDetail = models.ForeignKey(LOALETTEROFAPPOINTMENTEmployeeDetail, on_delete=models.CASCADE)
    file_id = models.CharField(max_length=200,null=True)
    file_name = models.CharField(max_length=200, null=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.file_id



LETTEROFAPPOINTMENT


from HumanResources.models import SalaryTitle_Master, Salary_Details_Effective


class Letter_Of_Appointment_Salary_Detail_Master(models.Model):
    EmpID = models.BigIntegerField(null=False,blank=False,db_index=True)
    Salary_title = models.ForeignKey(SalaryTitle_Master, on_delete=models.CASCADE)
    Permonth = models.DecimalField(max_digits=10, decimal_places=2)
    Perannum = models.DecimalField(max_digits=15, decimal_places=2)
    Salary_title_Old_Id = models.BigIntegerField(default=0,db_index=True, null=True,blank=True)
    
    Effective = models.ForeignKey(
        "HumanResources.Salary_Details_Effective",
        on_delete=models.SET_NULL,   
        null=True,
        blank=True
    )
    
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)
    