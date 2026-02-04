from django.db import models
from django.utils import timezone
from datetime import date,timedelta

class EmployeePersonalDetails(models.Model):
    EmpID  = models.AutoField(unique=True,editable=False,primary_key=True,db_index=True)
    EmployeeCode  =  models.CharField(null=True,blank=True,max_length=255,db_index=True)
    Prefix  = models.CharField(null=True,blank=True,max_length=255)
    FirstName = models.CharField(null=True,blank=True,max_length=255)
    MiddleName = models.CharField(null=True,blank=True,max_length=255)
    LastName = models.CharField(null=True,blank=True,max_length=255)
    Gender = models.CharField(null=True,blank=True,max_length=255)
    MaritalStatus = models.CharField(null=True,blank=True,max_length=255)
    DateofBirth = models.DateField(null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    MobileNumber = models.CharField(null=True,blank=True,max_length=255)
    EmailAddress = models.EmailField( null=True,blank=True,max_length=254)
    ProfileImageFileName = models.CharField(null=True,blank=True,max_length=255)
    ProfileImageFileTitle = models.CharField(null=True,blank=True,max_length=255)
    CovidVaccination  = models.CharField(null=True,blank=True,max_length=255)
    DetailsofIllness = models.CharField(null=True,blank=True,max_length=255)

    InterviewAssessmentID = models.BigIntegerField(default=0, null=True,blank=True) 
    Source = models.CharField(null=True,blank=True,max_length=255)

    ProfileCompletion = models.IntegerField(default=0) 
    MissingFields = models.TextField(null=True,blank=True)

    IsEmployeeCreated = models.BooleanField(default=False)
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)

from datetime import date, timedelta


class EmployeeWorkDetails(models.Model):
    EmpID                   = models.BigIntegerField(null=False,blank=False,db_index=True)
    EmpStatus               = models.CharField(null=True,blank=True,max_length=255,default="On Probation")
    Designation             = models.CharField(null=True,blank=True,max_length=255)
    Department              = models.CharField(null=True,blank=True,max_length=255) 
    Division                = models.CharField(null=True,blank=True,max_length=255)   
    Level                   = models.CharField(null=True,blank=True,max_length=255)
    ReportingtoDivision     = models.CharField(null=True,blank=True,max_length=255)  
    ReportingtoDesignation  = models.CharField(null=True,blank=True,max_length=255)
    ReportingtoDepartment   = models.CharField(null=True,blank=True,max_length=255)
    ReportingtoLevel        = models.CharField(null=True,blank=True,max_length=255)
    DottedLine              = models.CharField(null=True,blank=True,max_length=255)
    IsSecondary             = models.BooleanField(default=False,null=True,blank=True)
    
    OfficialEmailAddress    = models.EmailField( null=True,blank=True,max_length=254)
    OfficialMobileNo        = models.CharField(null=True,blank=True,max_length=255)
    DateofJoining           = models.DateField(null=True,blank=True)
    CompanyAccommodation    = models.CharField(null=True,blank=True, max_length=255)
    AccommodationFlatNumber = models.CharField(null=True,blank=True, max_length=255)
    Locker                  = models.CharField(null=True,blank=True, max_length=255)
    LockerType              = models.CharField(null=True,blank=True, max_length=255)
    LockerNumber            = models.CharField(null=True,blank=True, max_length=255)
    EmploymentType          = models.CharField(null=True,blank=True, max_length=255)
    ContractStartDate       = models.DateField(null=True,blank=True)
    ContractEndDate         = models.DateField(null=True,blank=True)

    Salary                  = models.DecimalField(max_digits=20, decimal_places=2,default=0)
    VipCheckbox             = models.BooleanField(default=False)
    OrganizationID          = models.BigIntegerField(default=0,db_index=True)
    CreatedBy               = models.BigIntegerField(default=0)
    CreatedDateTime         = models.DateTimeField(default=timezone.now)
    ModifyBy                = models.BigIntegerField(default=0)
    ModifyDateTime          = models.DateTimeField(default=timezone.now)
    IsDelete                = models.BooleanField(default=False,db_index=True)
    WeekOffDay              = models.CharField(default="Sunday",null=True,blank=True,max_length=15)
  

    def tenure_till_today(self):
        if self.DateofJoining:
            today = date.today()

            # Check if the Date of Joining is in the future
            if self.DateofJoining > today:
                return "Date of Joining is in the future"

            tenure_years = today.year - self.DateofJoining.year
            tenure_months = today.month - self.DateofJoining.month
            tenure_days = today.day - self.DateofJoining.day

            # Adjust tenure calculation if necessary
            if tenure_days < 0:
                # Borrow days from the previous month
                previous_month_last_day = (today.replace(day=1) - timedelta(days=1)).day
                tenure_days += previous_month_last_day
                tenure_months -= 1

            if tenure_months < 0:
                tenure_years -= 1
                tenure_months += 12

            # Construct the tenure string based on values
            result = []
            if tenure_years > 0:
                result.append(f"{tenure_years} years")
            if tenure_months > 0:
                result.append(f"{tenure_months} months")
            if tenure_days > 0 or (tenure_years == 0 and tenure_months == 0):
                result.append(f"{tenure_days} days")

            return ', '.join(result) if result else "No tenure"
        return "Date of Joining not available"







class EmployeeFamilyDetails(models.Model):
    EmpID = models.BigIntegerField(null=False,blank=False,db_index=True)
    SpouseName = models.CharField(null=True,blank=True,max_length=255)
    SpouseDateofBirth = models.DateField(null=True,blank=True)
    SpouseAge  = models.CharField(null=True,blank=True,max_length=3)
    SpouseContactNo  = models.CharField(null=True,blank=True,max_length=255)

    MotherName = models.CharField(null=True,blank=True,max_length=255)
    MotherDateofBirth = models.DateField(null=True,blank=True)
    MotherAge  = models.CharField(null=True,blank=True,max_length=3)
    MotherContactNo  = models.CharField(null=True,blank=True,max_length=255)

    FatherName = models.CharField(null=True,blank=True,max_length=255)
    FatherDateofBirth = models.DateField(null=True,blank=True)
    FatherAge  = models.CharField(null=True,blank=True,max_length=3)
    FatherContactNo  = models.CharField(null=True,blank=True,max_length=255)
    
    LandlineNo = models.CharField(null=True,blank=True,max_length=255)


    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)




class EmployeeChildDetails(models.Model):
    FamilyID = models.BigIntegerField(null=False,blank=False)
    Name = models.CharField(null=True,blank=True,max_length=255)
    Age  = models.BigIntegerField(default=0)
    Relation = models.CharField(null=True,blank=True,max_length=255)


    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)







class EmployeeEmergencyInformationDetails(models.Model):
    EmpID = models.BigIntegerField(null=False,blank=False,db_index=True)
    Prefix  = models.CharField(null=True,blank=True,max_length=255)
    FirstName = models.CharField(null=True,blank=True,max_length=255)
    MiddleName = models.CharField(null=True,blank=True,max_length=255)
    LastName = models.CharField(null=True,blank=True,max_length=255)
    Relation = models.CharField(null=True,blank=True,max_length=255)
    EmergencyContactNumber_1 = models.CharField(null=True,blank=True,max_length=255)
    EmergencyContactNumber_2 = models.CharField(null=True,blank=True,max_length=255)
    ProvidentFundNumber  = models.CharField(null=True,blank=True,max_length=255)
    ESINumber = models.CharField(null=True,blank=True,max_length=255)
    BloodGroup = models.CharField(null=True,blank=True,max_length=255)


    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)





class EmployeeQualificationDetails(models.Model):
    EmpID = models.BigIntegerField(null=False,blank=False,db_index=True)
    EducationType = models.CharField(null=True,blank=True,max_length=255)
    Degree_Course  = models.CharField(null=True,blank=True,max_length=255)
    NameoftheInstitution = models.CharField(null=True,blank=True,max_length=255)
    Year =  models.BigIntegerField(default=0)
    Percentage = models.BigIntegerField(default=0)
    FileName = models.CharField(null=True,blank=True,max_length=255)
    FileTitle = models.CharField(null=True,blank=True,max_length=255)

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)






class EmployeePreviousWorkInformationDetails(models.Model):
    EmpID = models.BigIntegerField(null=False,blank=False,db_index=True)
    Company = models.CharField(null=True,blank=True,max_length=255)
    Position  = models.CharField(null=True,blank=True,max_length=255)
    FromDate = models.DateField(null=True,blank=True)
    ToDate =  models.DateField(null=True,blank=True)
    
    # IsPresent = models.BooleanField(default=False)
    
    FileName = models.CharField(null=True,blank=True,max_length=255)
    FileTitle = models.CharField(null=True,blank=True,max_length=255)
    Salary = models.BigIntegerField(default=0)

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)







class EmployeeAddressInformationDetails(models.Model):
    EmpID = models.BigIntegerField(null=False,blank=False,db_index=True)
    Permanent_Address  = models.CharField(null=True,blank=True,max_length=255)
    Permanent_City   = models.CharField(null=True,blank=True,max_length=255)
    Permanent_State  = models.CharField(null=True,blank=True,max_length=255)
    Permanent_Pincode  = models.BigIntegerField(default=0)
    Permanent_HousePhoneNumber  = models.CharField(null=True,blank=True,max_length=255)
    Permanent_Landline  = models.CharField(null=True,blank=True,max_length=255)


    Temporary_Address  = models.CharField(null=True,blank=True,max_length=255)
    Temporary_City   = models.CharField(null=True,blank=True,max_length=255)
    Temporary_State  = models.CharField(null=True,blank=True,max_length=255)
    Temporary_Pincode  = models.BigIntegerField(default=0)
    Temporary_HousePhoneNumber  = models.CharField(null=True,blank=True,max_length=255)
    Temporary_Landline  = models.CharField(null=True,blank=True,max_length=255)


   
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)









class EmployeeIdentityInformationDetails(models.Model):
    EmpID = models.BigIntegerField(null=False,blank=False,db_index=True)
    PANNo = models.CharField(null=True,blank=True,max_length=255)
    PanFileName = models.CharField(null=True,blank=True,max_length=255)
    PanFileTitle = models.CharField(null=True,blank=True,max_length=255)

    AadhaarNumber   = models.CharField(null=True,blank=True,max_length=255)
    AadhaarFileName = models.CharField(null=True,blank=True,max_length=255)
    AadhaarFileTitle = models.CharField(null=True,blank=True,max_length=255)

    DrivingLicenceNo   = models.CharField(null=True,blank=True,max_length=255)
    DrivingFileName = models.CharField(null=True,blank=True,max_length=255)
    DrivingFileTitle = models.CharField(null=True,blank=True,max_length=255)


    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)




class EmployeeBankInformationDetails(models.Model):
    EmpID = models.BigIntegerField(null=False,blank=False,db_index=True)
    BankAccountNumber = models.CharField(null=True,blank=True,max_length=255)
    NameofBank   = models.CharField(null=True,blank=True,max_length=255)
    BankBranch   = models.CharField(null=True,blank=True,max_length=255)
    IFSCCode   = models.CharField(null=True,blank=True,max_length=255)


    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)







class EmployeeDocumentsInformationDetails(models.Model):
    EmpID = models.BigIntegerField(null=False,blank=False,db_index=True)
    Title = models.CharField(null=True,blank=True,max_length=255)
    FileName = models.CharField(null=True,blank=True,max_length=255)
    FileTitle = models.CharField(null=True,blank=True,max_length=255)

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)



class SalaryTitle_Master(models.Model):
    Title = models.CharField(null=True,blank=True,max_length=255)

    Type  = models.CharField(null=True,blank=True,max_length=255)
    TypeOrder = models.SmallIntegerField()
    TitleOrder = models.SmallIntegerField()
   
    Display_Names = models.CharField(null=True,blank=True,max_length=255)
    Salary_Code = models.CharField(null=True,blank=True,max_length=255)
    Formula_Expression = models.CharField(null=True,blank=True,max_length=255)
    Calculation_Basis_Type = models.CharField(null=True,blank=True,max_length=255)
    # Category  = models.CharField(null=True,blank=True,max_length=255)
    HotelID = models.BigIntegerField(default=0,db_index=True)

    Category = models.CharField(
        max_length=20,
        choices=[
            ('EARNING', 'Earning'),
            ('DEDUCTION', 'Deduction'),
            ('CONTRIBUTION', 'Contribution'),
            ('TOTAL', 'Total'),
        ],
        null=True,
        blank=True
    )

    IsBold  = models.BooleanField(default=False)
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)


class Salary_Detail_Master(models.Model):
    EmpID = models.BigIntegerField(null=False,blank=False,db_index=True)
    Salary_title = models.ForeignKey(SalaryTitle_Master, on_delete=models.CASCADE)
    Permonth = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    Perannum = models.DecimalField(max_digits=15, decimal_places=2, null=True,blank=True)
    Salary_title_Old_Id = models.BigIntegerField(default=0,db_index=True, null=True,blank=True)
    
    Effective = models.ForeignKey("Salary_Details_Effective",on_delete=models.CASCADE,null=True,blank=True)

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)
    





class EmployeeUrlMaster(models.Model):
    UrlName  = models.CharField(max_length=255)
    sortorder = models.IntegerField()

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)



class SalaryHistory(models.Model):
    EmpID = models.BigIntegerField(null=False,blank=False,db_index=True)
    FromSalary =  models.CharField(max_length=200, null=True, blank=True)
    ToSalary = models.CharField(max_length=200, null=True, blank=True)
    Effective_from = models.DateField(null=True, blank=True)
    Effective_to = models.DateField(null=True, blank=True)  
    SalaryID  = models.BigIntegerField(null=True,blank=True)
    SourceType  = models.CharField(max_length=200, null=True, blank=True,default='Salary Increment')
    
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)





class DesignationHistory(models.Model):
    EmpID = models.BigIntegerField(null=False,blank=False,db_index=True)
    FromDesignation = models.CharField(max_length=200, null=True, blank=True)
    FromDepartment = models.CharField(max_length=200, null=True, blank=True)

    ToDesignation = models.CharField(max_length=200, null=True, blank=True)
    ToDepartment = models.CharField(max_length=200, null=True, blank=True)


    Effective_from = models.DateField(null=True, blank=True)
    Effective_to = models.DateField(null=True, blank=True)  
    PromotionID = models.BigIntegerField(null=True,blank=True)
    SalaryID  = models.BigIntegerField(null=True,blank=True)

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)

  

class PT_Config(models.Model):
    # Title = models.CharField(null=True,blank=True,max_length=255)
    Type  = models.CharField(null=True,blank=True,max_length=255)
    State  = models.CharField(null=True,blank=True,max_length=255)

    Hotel_ID = models.BigIntegerField(default=0, db_index=True)
    Gender = models.CharField(max_length=10, null=True, blank=True)  
    Salary_From = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    Salary_To = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    PT_Amount = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    Last_Month = models.IntegerField(null=True, blank=True)
    # Last_Month = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    Last_Month_Value = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    IsActive = models.BooleanField(default=True, db_index=True)


    # Audit fields 
    OrganizationID = models.BigIntegerField(default=0, db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"{self.State} | {self.Salary_From}-{self.Salary_To} => {self.PT_Amount}"
    




# -------------- New Data.
class Salary_Details_Effective(models.Model):
    EmpID  = models.BigIntegerField(default=0, null=True,blank=True) 
    EffectiveFrom  = models.DateField(null=True, blank=True)
    EffectiveTo  = models.DateField(null=True, blank=True)
    CTC = models.CharField(max_length=10, null=True, blank=True)  

    # Audit fields 
    OrganizationID = models.BigIntegerField(default=0, db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False, db_index=True)

    