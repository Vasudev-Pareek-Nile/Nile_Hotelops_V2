from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MicrosoftCredentialsMail(models.Model):
    tenant_id = models.CharField(max_length=255, unique=True)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    authority = models.URLField(max_length=255)
    scope = models.CharField(max_length=255)  
    OrganizationID =models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.tenant_id    
    
    
class UserSession(models.Model):
    user_id = models.CharField(max_length=2000, blank=True, null=True)
    auth_token = models.TextField(max_length=2000, blank=True, null=True)
    session_key = models.CharField(max_length=2000, blank=True, null=True)
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    domain_code = models.CharField(max_length=50, blank=True, null=True)
    organization_logo = models.URLField(blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    employee_code = models.CharField(max_length=50, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    department_name = models.CharField(max_length=255, blank=True, null=True)

    emp_id = models.CharField(max_length=50, blank=True, null=True)             # New Field
    division_name = models.CharField(max_length=255, blank=True, null=True)     # New Field
    Designation = models.CharField(max_length=255, blank=True, null=True)       # New Field
    
    user_type = models.CharField(max_length=50, blank=True, null=True)

    organization_id = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.user_id})"

class ReportModuleMaster(models.Model):
    Module_Name = models.CharField(max_length=255, blank=True, null=True)
    Report_title = models.CharField(max_length=255, blank=True, null=True)
    IsDelete = models.BooleanField(default=False)


class OrganizationMaster(models.Model):
    OrganizationID =models.BigIntegerField()
    OrganizationName =  models.CharField(max_length=250,null=True,blank=True)
    OrganizationLogo =  models.CharField(max_length=50,null=True,blank=True)
    Address =  models.TextField(null=True,blank=True)
    Activation_status =  models.CharField(max_length=50,null=True,blank=True)
    OrganizationDomainCode =  models.CharField(max_length=50,null=True,blank=True)
    ShortDisplayLabel =  models.CharField(max_length=50,null=True,blank=True)
    IsNileHotel =  models.BooleanField(max_length=50,null=True,blank=True)
    FinancialYearStart =  models.IntegerField(null=True,blank=True)
    GSTNumber =  models.CharField(max_length=250,null=True,blank=True)
    MComLogo =  models.BooleanField(default =True)
    ReviewSoftware = models.CharField(default='',null=True,blank=True,max_length=60)
    
    Career_Share_Logo =  models.CharField(max_length=250,null=True,blank=True)

    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ShortDisplayLabel
class MonthListMaster(models.Model):
    MonthName=models.CharField(max_length=20)

# Create class Cake order form
class Cake_Order_Form(models.Model):
    To = models.CharField(max_length=100)
    Date = models.DateField()
    From = models.CharField(max_length=100)
    Time = models.TimeField(max_length=20)
    Guest_Name = models.CharField(max_length=100)
    To_Be_Prepared_For = models.CharField(max_length=100)
    Size = models.CharField(max_length=100)
    Type_Of_Cake = models.CharField(max_length=100)
    Required_Date = models.DateField()
    Required_Time = models.TimeField(max_length=20)
    type = (
        ('Yes','Yes'),
        ('No','No'),
    )
    Packing = models.CharField(max_length=50,choices=type)
    Selling_Price =  models.DecimalField(max_digits=6, decimal_places=2)
    Message_On_Cake = models.CharField(max_length=100)
    type = (
        ('Yes','Yes'),
        ('No','No'),
    )
    Complimentory = models.CharField(max_length=50,choices=type)
    Authorised_By = models.CharField(max_length=100)
    
    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.Guest_Name
    
    
    

class DepartmentMaster(models.Model):
    OrganizationID =models.BigIntegerField()
    Department =  models.CharField(max_length=250,null=True,blank=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.Department

class DesignationMaster(models.Model):
    OrganizationID =models.BigIntegerField()
    Designation =  models.CharField(max_length=250,null=True,blank=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.Designation


class EmployeeMaster(models.Model):
    EmployeeCode = models.CharField(max_length=250,null=True,blank=True)
    EmpName = models.CharField(max_length=250,null=True,blank=True)
    Department = models.CharField(max_length=250,null=True,blank=True)
    Designation = models.CharField(max_length=250,null=True,blank=True)
    DateofJoining =models.DateField(null=True,blank=True)
    ReportingtoDesigantion = models.CharField(max_length=250,null=True,blank=True)
    ReportingtoLevel = models.CharField(max_length=250,null=True,blank=True)
    Level = models.CharField(max_length=250,null=True,blank=True)
    EmpStatus = models.CharField(max_length=250,null=True,blank=True)
    Gender = models.CharField(max_length=250,null=True,blank=True)
    OfficalMailAddress = models.EmailField(max_length=254,null=True,blank=True)
    EmailMailAddress = models.EmailField(max_length=254,null=True,blank=True)
    EmpPhoto = models.CharField(max_length=500,null=True,blank=True)

    EmpID = models.CharField(max_length=250,null=True,blank=True)
    Division = models.CharField(max_length=250,null=True,blank=True)
    IsSecondary = models.BooleanField(default=False,null=True,blank=True)

    DOB = models.DateField(null=True,blank=True)
    BloodGroup = models.CharField(max_length=255,null=True,blank=True)
    EmergencyContact = models.CharField(max_length=255,null=True,blank=True) 
     

    OrganizationID =models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    

class City_Location_Master(models.Model):
    Village=models.CharField(max_length=255, blank=True, null=True)
    OfficeName=models.CharField(max_length=255, blank=True, null=True)
    PinCode=models.CharField(max_length=255, blank=True, null=True)
    SubDistName=models.CharField(max_length=255, blank=True, null=True)
    DistrictName=models.CharField(max_length=255, blank=True, null=True)
    StateName=models.CharField(max_length=255, blank=True, null=True)   


class HumanResourcesEmployeeMaster(models.Model):
    EmployeeCode = models.CharField(max_length=250,null=True,blank=True)
    EmpName = models.CharField(max_length=250,null=True,blank=True)
    Department = models.CharField(max_length=250,null=True,blank=True)
    Designation = models.CharField(max_length=250,null=True,blank=True)
    DateofJoining =models.DateField(null=True,blank=True)
    ReportingtoDesigantion = models.CharField(max_length=250,null=True,blank=True)
    ReportingtoLevel = models.CharField(max_length=250,null=True,blank=True)
    Level = models.CharField(max_length=250,null=True,blank=True)
    EmpStatus = models.CharField(max_length=250,null=True,blank=True)
    Gender = models.CharField(max_length=250,null=True,blank=True)
    OfficalMailAddress = models.EmailField(max_length=254,null=True,blank=True)
    EmailMailAddress = models.EmailField(max_length=254,null=True,blank=True)
    EmpPhoto = models.CharField(max_length=500,null=True,blank=True)
    DottedLine = models.CharField(max_length=250,null=True,blank=True)

    DOB = models.DateField(null=True,blank=True)
    BloodGroup = models.CharField(max_length=255,null=True,blank=True)
    EmergencyContact = models.CharField(max_length=255,null=True,blank=True) 
    Salary = models.BigIntegerField(null=True,blank=True)

    OrganizationID =models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)   



class OrganizationEmailMaster(models.Model):
    email_backend = models.CharField(max_length=255, default='django.core.mail.backends.smtp.EmailBackend')
    email_host = models.CharField(max_length=255, default='smtp.office365.com')
    email_port = models.IntegerField(default=587)
    email_use_tls = models.BooleanField(default=True)
    email_host_user = models.EmailField()
    email_host_password = models.CharField(max_length=255)
    OrganizationID =models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)   
    def __str__(self):
        return f"Email settings for {self.email_host_user}"  
    


class WhatsappSmsConfig(models.Model):
    url = models.URLField()
    api_key = models.CharField(max_length=255)
    template_id = models.CharField(max_length=100)
    sender = models.CharField(max_length=20)
    webHookDNId = models.CharField(max_length=20)  
    OrganizationID =models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False) 






class ModuleUserRights(models.Model):
    UserID = models.CharField(max_length=250,null=True,blank=True)
    Module_Name = models.CharField(max_length=250,null=True,blank=True)
    Is_Access = models.BooleanField(default=False)
    Is_Full_Access = models.BooleanField(default=False)

    OrganizationID = models.BigIntegerField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    IsActive = models.BooleanField(default=True)

    