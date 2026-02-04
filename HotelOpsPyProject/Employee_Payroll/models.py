from django.db import models
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.utils import timezone
import datetime


class Organization_Details(models.Model):
    OID_Code =  models.CharField(max_length=255,null=True,blank=True)
    OID = models.CharField(max_length=255,null=True,blank=True)
    
    UploadFormatType = models.CharField(max_length=255,null=True,blank=True)
    DownloadFormat = models.FileField(upload_to="Employee_Payroll/DownloadFormat", max_length=100,null=True,blank=True)
    EndDate =  models.IntegerField(null=False,blank=False)

    TotalDutyGraceHours =models.DecimalField(default=0,blank=True,null=True,max_digits=5,decimal_places=2)
    TotalMinimumDutyHours =models.DecimalField(default=0,blank=True,null=True,max_digits=5,decimal_places=2)
    IsESICCalculate =  models.BooleanField(default=True,blank=True,null=True)

    Biometric_Machine_Name = models.CharField(max_length=255,null=True,blank=True)

    OrgUrl  = models.TextField(null=True, blank=True)
    cid =  models.CharField(max_length=255,null=True,blank=True)


    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)

    def __str__(self):
        return f'{self.OID_Code}   {self.OID}'




class AlifCSVPunchRecord(models.Model):
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    emp_code = models.CharField(max_length=10)
    employee_name = models.CharField(max_length=255)
    punch_limit = models.IntegerField()
    working_hours = models.CharField(max_length=10,blank=True,null=True)
    punch_date = models.DateField()
    attend_code = models.CharField(max_length=5)
    first_in_punch = models.TimeField(blank=True,null=True)
    last_out_punch = models.TimeField(blank=True,null=True)
    worked_hours = models.CharField(max_length=10,blank=True,null=True)
    opr_id = models.CharField(max_length=10)
    opr_date = models.DateField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)

    def __str__(self):
        return f"{self.emp_code} - {self.employee_name}"


class AlifCSVPunchRecord_Log(models.Model):
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    emp_code = models.CharField(max_length=10)
    employee_name = models.CharField(max_length=255)
    punch_limit = models.IntegerField()
    working_hours = models.CharField(max_length=10,blank=True,null=True)
    punch_date = models.DateField()
    attend_code = models.CharField(max_length=5)
    first_in_punch = models.TimeField(blank=True,null=True)
    last_out_punch = models.TimeField(blank=True,null=True)
    worked_hours = models.CharField(max_length=10,blank=True,null=True)
    opr_id = models.CharField(max_length=10)
    opr_date = models.DateField()
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)

    def __str__(self):
        return f"{self.emp_code} - {self.employee_name}"


from django.utils import timezone

class APILog(models.Model):
    TimeStamp = models.DateTimeField(default=timezone.now)
    Url = models.URLField(max_length=1000)
    Status_Code = models.IntegerField()
    Response_Time = models.FloatField()
    Message = models.TextField()
    
    
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)

    


class Raw_Attendance_Data_File(models.Model):
    File_Name = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    Attendance_Date = models.DateField(db_index=True)
    
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)






class Raw_Attendance_Data(models.Model):
    EmployeeCode = models.CharField(max_length=255,db_index=True)
    Date =models.CharField(max_length=255,null=True,blank=True,db_index=True)
    Time = models.CharField(max_length=255,null=True,blank=True)
    Status = models.CharField(max_length=255,null=True,blank=True,db_index=True)

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)




# ------------ New Table 
class Raw_Attendance_Data_log(models.Model):
    EmployeeCode = models.CharField(max_length=255,db_index=True)
    Date =models.CharField(max_length=255,null=True,blank=True,db_index=True)
    Time = models.CharField(max_length=255,null=True,blank=True)
    Status = models.CharField(max_length=255,null=True,blank=True,db_index=True)

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)

    



class Attendance_Data(models.Model):
    EmployeeCode       = models.CharField(max_length=255,db_index=True)
    EmpID              = models.BigIntegerField(null=True,blank=True, default=0)
    Date               = models.DateField(db_index=True)
    In_Time            = models.CharField(max_length=255,null=True,blank=True)
    Out_Time           = models.CharField(max_length=255,null=True,blank=True)
    S_In_Time          = models.CharField(max_length=255,null=True,blank=True)
    S_Out_Time         = models.CharField(max_length=255,null=True,blank=True)

    Duty_Hour          = models.CharField(max_length=255,null=True,blank=True)
    Status             = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    IsUpload           = models.BooleanField(default=False,db_index=True) 
    LeaveID            = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    Is_WeekOff         = models.BooleanField(default=False,null=True,blank=True)
    Is_Leave           = models.BooleanField(default=False,null=True,blank=True)
    IsUpload_WeekOff   = models.BooleanField(default=False,null=True,blank=True)
    IsUpload_Biometric = models.BooleanField(default=False,null=True,blank=True)
    
    OrganizationID     = models.BigIntegerField(default=0,db_index=True)
    CreatedBy          = models.BigIntegerField(default=0)
    CreatedDateTime    = models.DateTimeField(default=timezone.now)
    ModifyBy           = models.BigIntegerField(default=0)
    ModifyDateTime     = models.DateTimeField(default=timezone.now)
    IsDelete           = models.BooleanField(default=False,db_index=True)
    ActionBy           = models.BigIntegerField(default=0,blank=True,null=True)
    ActionByName       = models.CharField(max_length=255,null=True,blank=True)
    ActionDateTime     = models.DateTimeField(null=True,blank=True)


class Attendance_Data_Log(models.Model):
    EmployeeCode = models.CharField(max_length=255,db_index=True)
    Date = models.DateField(db_index=True)
    In_Time =  models.CharField(max_length=255,null=True,blank=True)
    Out_Time = models.CharField(max_length=255,null=True,blank=True)

    S_In_Time =  models.CharField(max_length=255,null=True,blank=True)
    S_Out_Time = models.CharField(max_length=255,null=True,blank=True)


    Duty_Hour  = models.CharField(max_length=255,null=True,blank=True)
    Status = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    IsUpload = models.BooleanField(default=False,db_index=True)
    
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)
    ActionBy=models.BigIntegerField(default=0,blank=True,null=True)
    ActionByName=models.CharField(max_length=255,null=True,blank=True)
    ActionDateTime = models.DateTimeField(null=True,blank=True)

    
class AttendanceLock(models.Model):
    EmpID = models.BigIntegerField(null=True,blank=True, default=0)
    EmployeeCode = models.CharField(max_length=255)
    month = models.IntegerField()
    year = models.IntegerField()
    month_name = models.CharField(max_length=255,null=True,blank=True) 
    total_no_Days_in_month = models.CharField(max_length=255)
    PaiDays  = models.CharField(max_length=255)

    IsLock = models.BooleanField(default=False)
    IsGenerated = models.BooleanField(default=False)
    IsAttendanceMoved = models.BooleanField(default=False)
    IsHR_Verified = models.BooleanField(default=False)
    IsFC_Verified = models.BooleanField(default=False)

    
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)




class AttendanceSalaryFile(models.Model):
    Type = models.CharField(max_length=255,null=True,blank=True)
    Month = models.CharField(max_length=255,null=True,blank=True)
    Year = models.CharField(max_length=255,null=True,blank=True)
   
    FileName = models.CharField(null=True,blank=True,max_length=255)
    FileTitle = models.CharField(null=True,blank=True,max_length=255)
    
    PdfFileName = models.CharField(null=True,blank=True,max_length=255)
    PdfFileTitle = models.CharField(null=True,blank=True,max_length=255)
    
    
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)




class SalarySlip(models.Model):
    EmployeeCode = models.CharField(max_length=255)
    Emp_Name = models.CharField(max_length=255,null=True,blank=True)
    
    month = models.IntegerField()
    year = models.IntegerField()
    month_name = models.CharField(max_length=255,null=True,blank=True) 
    
    generated = models.BooleanField(default=False)
    HrVerify = models.BooleanField(default=False)
    FcVerify =  models.BooleanField(default=False)
    
    Desingation = models.CharField(max_length=255,null=True,blank=True)
    Department = models.CharField(max_length=255,null=True,blank=True)
    DOJ = models.CharField(max_length=255,null=True,blank=True)
    DOB = models.CharField(max_length=255,null=True,blank=True)
    
    total_no_Days_in_month =   models.CharField(max_length=255,null=True,blank=True)
    no_of_days =   models.CharField(max_length=255,null=True,blank=True)
    no_of_absent = models.CharField(max_length=255,null=True,blank=True)
    
    fixed_basic =   models.CharField(max_length=255,null=True,blank=True)
    fixed_HRA =  models.CharField(max_length=255,null=True,blank=True)
    ConveyanceAllowance = models.CharField(max_length=255,null=True,blank=True)
    CCA	 = models.CharField(max_length=255,null=True,blank=True)
    OtherAllowance = models.CharField(max_length=255,null=True,blank=True)
    gross_salary =   models.CharField(max_length=255,null=True,blank=True)
    
    
    Earned_Basic =   models.CharField(max_length=255,null=True,blank=True)
    Earned_HRA =   models.CharField(max_length=255,null=True,blank=True)
    Arrear =  models.CharField(max_length=255,null=True,blank=True)
    RewardIncentive	 =  models.CharField(max_length=255,null=True,blank=True)
    Earned_Total_Allowance = models.CharField(max_length=255,null=True,blank=True)

    
    ESIC =   models.CharField(max_length=255,null=True,blank=True)
    EPFO =   models.CharField(max_length=255,null=True,blank=True)
    PT	= models.CharField(max_length=255,null=True,blank=True)
    Meals	=models.CharField(max_length=255,null=True,blank=True)
    Accommodation	= models.CharField(max_length=255,null=True,blank=True)
    AdvanceLoan	= models.CharField(max_length=255,null=True,blank=True)
    TaxDeduction	= models.CharField(max_length=255,null=True,blank=True)
    OtherDeduction	= models.CharField(max_length=255,null=True,blank=True)


    EmployeePF = 	models.CharField(max_length=255,null=True,blank=True)
    CompanyContributionToESIC =	models.CharField(max_length=255,null=True,blank=True)
    TotalCompanyContribution =	models.CharField(max_length=255,null=True,blank=True)
    CTC = models.CharField(max_length=255,null=True,blank=True)

    
    Total_Earning =   models.CharField(max_length=255,null=True,blank=True)
    Total_Deduction =  models.CharField(max_length=255,null=True,blank=True)
    Net_salary =   models.CharField(max_length=255,null=True,blank=True)
    Net_salary_In_Words =   models.CharField(max_length=255,null=True,blank=True) 
    
    ProvidentFundNumber = models.CharField(max_length=255,null=True,blank=True)
    ESINumber = models.CharField(max_length=255,null=True,blank=True)
    BankAccountNumber = models.CharField(max_length=255,null=True,blank=True)
    PayMode =  models.CharField(max_length=255,null=True,blank=True)
    BankName =   models.CharField(max_length=255,null=True,blank=True)
    BankIFSCCode =   models.CharField(max_length=255,null=True,blank=True)
    BankBranch = models.CharField(max_length=255,null=True,blank=True)

    Earned_ConveyanceAllowance = models.CharField(max_length=255,null=True,blank=True)
    Earned_CCA	 = models.CharField(max_length=255,null=True,blank=True)
    Earned_OtherAllowance = models.CharField(max_length=255,null=True,blank=True)


    IsLocked = models.BooleanField(default=True)
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)


    def get_approval_status_html(self):
        if not self.HrVerify and not self.FcVerify:
            return '<p style="color: #f8ac59;">Pending from HR</p>'
        if self.HrVerify and not self.FcVerify:
            return '<p style="color: #f8ac59;">Approved by HR <br> Pending from Finance</p>'
        elif self.HrVerify and self.FcVerify:
            return '<p style="color: #1ab394;">Approved</p>'
        else:
            return ''
        
    @property
    def CTC_calculated(self):
        try:
            return int(float(self.Total_Earning)) + int(float(self.TotalCompanyContribution))
        except (ValueError, TypeError):
            return 0



    

class Update_Attendance_Request(models.Model):
    Attendance_Data = models.ForeignKey(Attendance_Data,on_delete=models.CASCADE)
    # SalaryAttendance = models.ForeignKey(SalaryAttendance,on_delete=models.CASCADE)

    Reason = models.TextField(null= True,blank= True)
    Apporve_status = models.CharField(max_length=255,null=True,blank=True,default=0) 
    
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)





class SalaryEmails(models.Model):
    EmpCode = models.CharField(max_length=255) 
    email = models.CharField(max_length=255)

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)




class WeekOffDetails(models.Model):
    Emp_Code = models.CharField(max_length=255,null=False,blank=False)
    WeekoffDate  = models.DateField(null=False,blank=False)
    
     
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)


class ShfitMaster(models.Model):
    EmployeeCode = models.CharField(max_length=255,null=False,blank=False)
    ShfitType = models.CharField(max_length=255,null=False,blank=False,default="General")
     
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)
    


class PayrollErrorLog(models.Model):
    ErrorMessage  = models.CharField(max_length=255,null=False,blank=False)
    ErrorPage = models.CharField(max_length=255,null=False,blank=False)
    ErrorFucntion = models.CharField(max_length=255,null=False,blank=False)
   

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)








# -- Payroll Moved Attendance Data
class SalaryAttendance(models.Model):
    EmpID = models.BigIntegerField(null=False,blank=False,db_index=True)
    EmployeeCode = models.CharField(max_length=255,db_index=True)
    Date = models.DateField(db_index=True)
    In_Time =  models.CharField(max_length=255,null=True,blank=True)
    Out_Time = models.CharField(max_length=255,null=True,blank=True)

    S_In_Time =  models.CharField(max_length=255,null=True,blank=True)
    S_Out_Time = models.CharField(max_length=255,null=True,blank=True)
    Duty_Hour  = models.CharField(max_length=255,null=True,blank=True)
    
    Over_Time = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    Late_Hour = models.CharField(max_length=255,null=True,blank=True,db_index=True)

    Status = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    ActualStatus  = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    LeaveID  = models.CharField(max_length=255,null=True,blank=True,db_index=True)  
    Remarks = models.CharField(max_length=255,null=True,blank=True,db_index=True)

    From_Date = models.DateField(null=True, blank=True)
    To_Date = models.DateField(null=True, blank=True)  

    month = models.IntegerField(null=True,blank=True)
    year = models.IntegerField(null=True,blank=True)
    month_name = models.CharField(max_length=255,null=True,blank=True) 

    # Flags
    IsAdvancePosting = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    IsPresent =  models.BooleanField(default=False,db_index=True)
    IsUpload =  models.BooleanField(default=False,db_index=True, null=True,blank=True)
    PresentValue = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    IsAttendanceMoved = models.BooleanField(default=False,db_index=True, null=True,blank=True)
    IsAttendanceModified = models.BooleanField(default=False,db_index=True, null=True,blank=True)

    HotelID = models.BigIntegerField(default=0,db_index=True)
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    IsDelete = models.BooleanField(default=False,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    ActionBy=models.BigIntegerField(default=0,blank=True,null=True)
    ActionByName=models.CharField(max_length=255,null=True,blank=True)
    ActionDateTime = models.DateTimeField(null=True,blank=True)



class Update_Attendance_Request_V1(models.Model):
    SalaryAttendance = models.ForeignKey(SalaryAttendance,on_delete=models.CASCADE)
    Reason = models.TextField(null= True,blank= True)
    Apporve_status = models.CharField(max_length=255,null=True,blank=True,default=0) 
    
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)




class PayrollProgress(models.Model):
    task_id = models.CharField(max_length=50, unique=True)
    total = models.IntegerField(default=0)
    processed = models.IntegerField(default=0)
    inserted = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default="running")  # running, done, error
    created_at = models.DateTimeField(auto_now_add=True)



class Payroll_Bulk_Lock_Progress(models.Model):
    task_id = models.CharField(max_length=50, unique=True)
    total = models.IntegerField(default=0)
    processed = models.IntegerField(default=0)
    inserted = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default="running")  # running, done, error
    created_at = models.DateTimeField(auto_now_add=True)






class Salary_Slip_V1(models.Model):
    # Personal Info
    EmployeeCode = models.CharField(max_length=255)
    EmpID = models.BigIntegerField(null=True,blank=True, default=0)
    Emp_Name = models.CharField(max_length=255,null=True,blank=True)
    Designation = models.CharField(max_length=255,null=True,blank=True)
    Department = models.CharField(max_length=255,null=True,blank=True)
    EmpStatus = models.CharField(max_length=255,null=True,blank=True)
    # DOB = models.CharField(max_length=255,null=True,blank=True)
    DOJ = models.CharField(max_length=255,null=True,blank=True)
    Pan_No = models.CharField(max_length=255,null=True,blank=True)
    

 
    # Field to stay --------
    # Fix Salary Field
    CTC = models.CharField(max_length=255,null=True,blank=True)
    Gross_Salary_Fixed =   models.CharField(max_length=255,null=True,blank=True)
    Basic_Salary_Fixed =   models.CharField(max_length=255,null=True,blank=True)
    HRA_Fixed =   models.CharField(max_length=255,null=True,blank=True)
    Conveyance_Fixed =   models.CharField(max_length=255,null=True,blank=True)
    CCA_Fixed =   models.CharField(max_length=255,null=True,blank=True)
    Other_Allowance_Fixed =   models.CharField(max_length=255,null=True,blank=True)
    Total_Fixed =   models.CharField(max_length=255,null=True,blank=True)

    # Actual_Attendance
    # Actual_Attendance_Days =   models.CharField(max_length=255,null=True,blank=True)

    # Earnings Salry Field
    Basic_Salary_Earned =   models.CharField(max_length=255,null=True,blank=True)
    HRA_Earned =   models.CharField(max_length=255,null=True,blank=True)
    Conveyance_Earned =   models.CharField(max_length=255,null=True,blank=True)
    CCA_Earned =   models.CharField(max_length=255,null=True,blank=True)
    Other_Allowance_Earned =   models.CharField(max_length=255,null=True,blank=True)
    Arrers =   models.CharField(max_length=255,null=True,blank=True)
    Total_Earning =   models.CharField(max_length=255,null=True,blank=True)


    # Deductions Salry Field
    PF_Employee_Deduction =   models.CharField(max_length=255,null=True,blank=True)
    PF_Employer_Deduction =   models.CharField(max_length=255,null=True,blank=True)
    ESIC =   models.CharField(max_length=255,null=True,blank=True)
    PT =   models.CharField(max_length=255,null=True,blank=True)
    Meals	=models.CharField(max_length=255,null=True,blank=True)
    Accommodation	= models.CharField(max_length=255,null=True,blank=True)
    Advance_Loan	= models.CharField(max_length=255,null=True,blank=True)
    Tax_Deduction	= models.CharField(max_length=255,null=True,blank=True)
    Other_Deduction =   models.CharField(max_length=255,null=True,blank=True)
    Total_Deduction =   models.CharField(max_length=255,null=True,blank=True)
    Bonus =   models.CharField(max_length=255,null=True,blank=True)
    
    # Company Contribution
    Total_Company_Contribution =   models.CharField(max_length=255,null=True,blank=True)

    # Net
    Net_Payable =  models.CharField(max_length=255,null=True,blank=True)
    Net_Payable_In_Words =  models.CharField(max_length=255,null=True,blank=True)
    # ---------------
    
    month = models.IntegerField()
    year = models.IntegerField()
    month_name = models.CharField(max_length=255,null=True,blank=True) 
    Total_No_Days_In_Month =   models.CharField(max_length=255,null=True,blank=True)
    Present_Days =   models.CharField(max_length=255,null=True,blank=True)
    Absent_Days = models.CharField(max_length=255,null=True,blank=True)
    
    # Flags
    IsGenerated = models.BooleanField(default=False)
    HrVerify = models.BooleanField(default=False)
    FcVerify =  models.BooleanField(default=False)
    IsLocked = models.BooleanField(default=True)
    IsDelete = models.BooleanField(default=False,db_index=True)

    Provident_Fund_Number = models.CharField(max_length=255,null=True,blank=True)
    ESIC_Number = models.CharField(max_length=255,null=True,blank=True)
    Bank_Account_Number = models.CharField(max_length=255,null=True,blank=True)
    Pay_Mode =  models.CharField(max_length=255,null=True,blank=True)
    Bank_Name =   models.CharField(max_length=255,null=True,blank=True)
    Bank_IFSC_Code =   models.CharField(max_length=255,null=True,blank=True)
    Bank_Branch = models.CharField(max_length=255,null=True,blank=True)

    
    # Other Fields
    HotelID = models.BigIntegerField(default=0,db_index=True)
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)




class Salary_Earning_Details(models.Model):
    Date = models.DateField(db_index=True,null=True,blank=True)
    EmpID = models.BigIntegerField(null=True,blank=True, default=0)
    EmpCode = models.CharField(max_length=255,null=True,blank=True) 
    

    # SalaryAttendance = models.ForeignKey(SalaryAttendance,on_delete=models.CASCADE)
    SalaryTitle = models.CharField(max_length=255,null=True,blank=True) 
    SalaryTitleID = models.CharField(max_length=255,null=True,blank=True) 
    Type = models.CharField(max_length=255,null=True,blank=True) 
    TypeOrder = models.SmallIntegerField(null=True,blank=True)
    TitleOrder = models.SmallIntegerField(null=True,blank=True)
   
    Amount = models.DecimalField(max_digits=30, decimal_places=18, default=0.0) 
    month = models.IntegerField(null=True,blank=True)
    year = models.IntegerField(null=True,blank=True)

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)



class Salary_Deduction_Details(models.Model):
    Date = models.DateField(db_index=True)

    SalaryAttendance = models.ForeignKey(SalaryAttendance,on_delete=models.CASCADE)
    SalaryTitle = models.CharField(max_length=255,null=True,blank=True) 
    SalaryTitleID = models.CharField(max_length=255,null=True,blank=True) 
    Type = models.CharField(max_length=255,null=True,blank=True) 
    TypeOrder = models.SmallIntegerField(null=True,blank=True)
    TitleOrder = models.SmallIntegerField(null=True,blank=True)
   
    Amount = models.DecimalField(max_digits=30, decimal_places=18, default=0.0) 

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)



class Salary_Fixed_Details(models.Model):
    Date = models.DateField(db_index=True)

    SalaryAttendance = models.ForeignKey(SalaryAttendance,on_delete=models.CASCADE)
    SalaryTitle = models.CharField(max_length=255,null=True,blank=True) 
    SalaryTitleID = models.CharField(max_length=255,null=True,blank=True) 
    TypeOrder = models.SmallIntegerField(null=True,blank=True)
    TitleOrder = models.SmallIntegerField(null=True,blank=True)
   
    Type = models.CharField(max_length=255,null=True,blank=True) 
    Amount = models.DecimalField(max_digits=30, decimal_places=18, default=0.0) 

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)


class Salary_Company_Contribution_Details(models.Model):
    Date = models.DateField(db_index=True)

    SalaryAttendance = models.ForeignKey(SalaryAttendance,on_delete=models.CASCADE)
    SalaryTitle = models.CharField(max_length=255,null=True,blank=True) 
    SalaryTitleID = models.CharField(max_length=255,null=True,blank=True) 
    TypeOrder = models.SmallIntegerField(null=True,blank=True)
    TitleOrder = models.SmallIntegerField(null=True,blank=True)
   
    Type = models.CharField(max_length=255,null=True,blank=True) 
    Amount = models.DecimalField(max_digits=30, decimal_places=18, default=0.0) 

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)




# Response_Page_Generate_Slip
class Response_Data_Generate_Slip(models.Model):
    Month_No = models.CharField(max_length=255,null=True,blank=True) 
    Year = models.CharField(max_length=255,null=True,blank=True) 
    Emp_Name = models.CharField(max_length=255,null=True,blank=True) 
    Emp_ID = models.BigIntegerField(null=True,blank=True, default=0)
    Emp_Code = models.CharField(max_length=255,null=True,blank=True) 
    Response_Status = models.CharField(max_length=255,null=True,blank=True) 
    Response_Message = models.CharField(max_length=255,null=True,blank=True) 
   

    Hotel_Id = models.BigIntegerField(default=0,db_index=True)

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)
    
    
    
class Excel_Attendance_Upload_Punch_Record(models.Model):
    EmployeeCode         = models.CharField(max_length=255,db_index=True)
    Date                 = models.DateField(db_index=True)
    In_Time              = models.CharField(max_length=255,null=True,blank=True)
    Out_Time             = models.CharField(max_length=255,null=True,blank=True)
    Duty_Hour            = models.CharField(max_length=255,null=True,blank=True)
    Status               = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    LeaveID              = models.CharField(max_length=255,null=True,blank=True,db_index=True, default=0)  
    IsUpload             = models.BooleanField(default=False,db_index=True)
    IsAttendanceModified = models.BooleanField(default=False,db_index=True)
    
    # Is_Leave             = models.BooleanField(default=False)
    # IsUpload_Biometric   = models.BooleanField(default=False)
    
    OrganizationID       = models.BigIntegerField(default=0,db_index=True)
    CreatedBy            = models.BigIntegerField(default=0)
    CreatedDateTime      = models.DateTimeField(default=timezone.now)
    ModifyBy             = models.BigIntegerField(default=0)
    ModifyDateTime       = models.DateTimeField(default=timezone.now)
    IsDelete             = models.BooleanField(default=False,db_index=True)

    def __str__(self):
        return self.EmployeeCode
    
    
class Excel_Attendance_Upload_Punch_Record_Log(models.Model):
    EmployeeCode         = models.CharField(max_length=255,db_index=True)
    Date                 = models.DateField(db_index=True)
    In_Time              = models.CharField(max_length=255,null=True,blank=True)
    Out_Time             = models.CharField(max_length=255,null=True,blank=True)
    Duty_Hour            = models.CharField(max_length=255,null=True,blank=True)
    Status               = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    LeaveID              = models.CharField(max_length=255,null=True,blank=True,db_index=True, default=0)  
    
    # Is_Leave             = models.BooleanField(default=False)
    # IsUpload_Biometric   = models.BooleanField(default=False)
    
    OrganizationID       = models.BigIntegerField(default=0,db_index=True)
    CreatedBy            = models.BigIntegerField(default=0)
    CreatedDateTime      = models.DateTimeField(default=timezone.now)
    ModifyBy             = models.BigIntegerField(default=0)
    ModifyDateTime       = models.DateTimeField(default=timezone.now)
    IsDelete             = models.BooleanField(default=False,db_index=True)

    def __str__(self):
        return self.EmployeeCode

