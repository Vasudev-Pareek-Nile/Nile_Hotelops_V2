from django.db import models
from datetime import datetime,date
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.utils import timezone

# Leave Type
class Leave_Type_Master(models.Model):
    Type = models.CharField(max_length=255, null=False, blank=False,db_index=True)
    FullName = models.CharField(max_length=255, null=False, blank=False)
    Description = models.TextField()
    Is_Active =models.BooleanField(default=False,db_index=True) 
    
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)

    def __str__(self):
        return f'{self.id} ==> {self.Type}'  

    class Meta:
        ordering = ['-id']
        

# National Holidays
class  National_Holidays(models.Model):
    Name = models.CharField(max_length=255,null=False,blank=False)
    Date = models.DateField()
    Description = models.TextField()
    Is_Active =models.BooleanField(default=False)
    HotelID = models.BigIntegerField(default=0)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.Name}  ---  {self.Date}'
    

# State Holidays
class State_Holidays(models.Model):
    Name = models.CharField(max_length=255,null=False,blank=False)
    Date = models.DateField()
    Description = models.TextField()
    Is_Active =models.BooleanField(default=False)
    HotelID = models.BigIntegerField(default=0)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.Name}  ---  {self.Date}'
    



# Optional Holidays
class  Optional_Holidays(models.Model):
    Name = models.CharField(max_length=255,null=False,blank=False)
    Date = models.DateField()
    Description = models.TextField()
    Is_Active =models.BooleanField(default=False)
    
    HotelID = models.BigIntegerField(default=0)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.Name}  ---  {self.Date}'

            

# Leave Config Details Master 
class Leave_Config_Details(models.Model):
    Leave_Type_Master = models.ForeignKey(Leave_Type_Master,on_delete=models.CASCADE)
    
    Monitor_Balance =  models.BooleanField(default=False)     
    Carry_FWD =  models.BooleanField(default=False)   
    Encash = models.BooleanField(default=False)   
    
    Financial_Year_Start_Date =  models.DateField()
    Financial_Year_End_Date = models.DateField()
    
    YearlyLeave = models.DecimalField(max_digits=5, decimal_places=2) 
    MonthlyLeave = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True) 
    
    Appn_Times = models.DecimalField(max_digits=5, decimal_places=2) 
    Apply_Max = models.DecimalField(max_digits=5, decimal_places=2) 
    Apply_Min = models.DecimalField(max_digits=5, decimal_places=2) 
    
    # Overdaft = models.DecimalField(max_digits=5, decimal_places=2) 
    Maximum_Accumulation =models.DecimalField(max_digits=5, decimal_places=2) 
    IsMonthly = models.BooleanField(default=False)
    
    IsDate = models.BooleanField(default=False,db_index=True)

    IsConfirmed = models.BooleanField(default=False)
    IsAutoCredit = models.BooleanField(default=False)

    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
    
    
    class Meta:
        ordering = ['-id']    


# Leave Process Master
class  Leave_Process_Master(models.Model):
    Leave_Type_Master = models.ForeignKey( Leave_Type_Master,on_delete=models.CASCADE)
    Credit = models.DecimalField(max_digits=5, decimal_places=2) 
    
    Status  = models.BooleanField(default=False,db_index=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)
    def __str__(self):
        return f'{self.Leave_Type_Master.Type}'
    class Meta:
        ordering = ['-id'] 

from HumanResources.models import EmployeePersonalDetails
# Leave Process Details
class  Leave_Process_Details(models.Model):
    Leave_Process_Master =models.ForeignKey(Leave_Process_Master,on_delete=models.CASCADE)
    Emp_code =  models.CharField(max_length=255,null=False,blank=False)
      
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)

    IsDelete = models.BooleanField(default=False)
    
    # def getEmpName(Emp_code,OrganizationID):
        
    #     Emp_code = Emp_code
    #     OrganizationID=OrganizationID
    #     ed = EmployeePersonalDetails.objects.filter(IsDelete=False,EmployeeCode=Emp_code,OrganizationID=OrganizationID)
    #     EmpName=""
    #     if ed.exists():
    #         EmpName=ed.first().FirstName+" "+ed.first().LastName
    #     return EmpName
    def __str__(self):
        return f'{self.Leave_Process_Master.id} {self.Leave_Process_Master.Leave_Type_Master.Type} {self.Emp_code}'

    class Meta:
        ordering = ['-id']        


# Emp Leave Balance Master1
class Emp_Leave_Balance_Master(models.Model):
    Leave_Type_Master =models.ForeignKey(Leave_Type_Master,on_delete=models.CASCADE)
    Emp_code =  models.CharField(max_length=255,null=False,blank=False,db_index=True)
    Balance = models.DecimalField(max_digits=5, decimal_places=2) 
      
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now) 
    IsDelete = models.BooleanField(default=False,db_index=True)

    def __str__(self):
        return f'{self.Leave_Type_Master.Type} {self.Emp_code}  {self.Balance}'

    class Meta:
        ordering = ['-id']
            


# EmpMonthLevelCreditMaster	
class EmpMonthLevelCreditMaster(models.Model):
    Leave_Type_Master =models.ForeignKey(Leave_Type_Master,on_delete=models.CASCADE)
    Emp_code =  models.CharField(max_length=255,null=False,blank=False)
    credit = models.DecimalField(max_digits=5, decimal_places=2) 
      
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)
    def __str__(self):
        return f'{self.Leave_Type_Master.Type} {self.Emp_code}  {self.credit}'

    class Meta:
        ordering = ['-id']        	

# EmpMonthLevelDebitMaster

class EmpMonthLevelDebitMaster(models.Model):
    Leave_Type_Master =models.ForeignKey(Leave_Type_Master,on_delete=models.CASCADE)
    Emp_code =  models.CharField(max_length=255,null=False,blank=False,db_index=True)
    debit = models.DecimalField(max_digits=5, decimal_places=2) 
      
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)
    def __str__(self):
        return f'{self.Leave_Type_Master.Type} {self.Emp_code}  {self.debit}'

    class Meta:
        ordering = ['-id']





class CompoffLogMaster(models.Model): 
    EmployeeCode = models.CharField(max_length=255,null=False,blank=False,db_index=True)
    CompoffDate  = models.DateField(null=False,blank=False)
    Remarks = models.TextField(null=True,blank=True)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(auto_now_add=True)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(auto_now_add=True)
    IsDelete = models.BooleanField(default=False)

class CompOffApplication(models.Model):
    Emp_Code =models.CharField(max_length=30,null=True,blank=True)
    CompOff_Date = models.DateField()
    Reason = models.TextField()
    ReportingtoDesigantion =models.CharField(max_length=255,null=True,blank=True)
    Status = models.CharField(max_length=50, default="Pending")  # Pending, Approved, Rejected
    ApprovedBy = models.BigIntegerField(default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(auto_now_add=True)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(auto_now_add=True)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f"Comp Off Application - {self.Emp_Code} - {self.CompOff_Date}"
    
# Leave Application
class Leave_Application(models.Model):
    Leave_Type_Master      = models.ForeignKey(Leave_Type_Master,on_delete=models.CASCADE)
    Emp_code               = models.CharField(max_length=255,null=False,blank=False,db_index=True)
    Start_Date             = models.DateField()
    From_1st_Half          = models.BooleanField(default=False)
    From_2nd_Half          = models.BooleanField(default=False)
    
    End_Date               = models.DateField()
    To_1st_Half            = models.BooleanField(default=False)
    To_2nd_Half            = models.BooleanField(default=False)
    Reason                 = models.TextField(null=False, blank=False)
    Status                 = models.IntegerField()
    Total_credit           = models.DecimalField(max_digits=5, decimal_places=2)
    Remark                 = models.TextField(null=True,blank=True)
    ReportingtoDesigantion = models.CharField(max_length=255,null=False,blank=False)

    OrganizationID         = models.BigIntegerField(default=0,db_index=True)
    CreatedBy              = models.BigIntegerField(default=0)
    CreatedDateTime        = models.DateTimeField(default=timezone.now)
    ModifyBy               = models.BigIntegerField(default=0)
    ModifyDateTime         = models.DateTimeField(default=timezone.now)
    IsDelete               = models.BooleanField(default=False)

    ActionBy=models.BigIntegerField(default=0,blank=True,null=True)
    ActionByName=models.CharField(max_length=255,null=True,blank=True)
    ActionDateTime = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f'{self.Leave_Type_Master.Type} {self.Emp_code}  {self.Total_credit}'


    class Meta:
        ordering = ['-id']








# Leave Type
class Comp_Off_Assign_Logs(models.Model):
    Leave_Type_Master =models.ForeignKey(Leave_Type_Master,on_delete=models.CASCADE)
    EmpID = models.CharField(max_length=255, null=True, blank=True,db_index=True)
    EmployeeCode = models.CharField(max_length=255, null=True, blank=True,db_index=True)
    Message = models.CharField(max_length=255, null=True, blank=True)
    Year = models.CharField(max_length=255, null=True, blank=True)
    Month = models.CharField(max_length=255, null=True, blank=True)
    Is_Assigned =models.BooleanField(default=False,db_index=True) 
    
    OrganizationID = models.BigIntegerField(default=0,db_index=True)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False,db_index=True)
