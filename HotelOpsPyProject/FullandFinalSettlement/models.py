from datetime import date
from django.db import models
from django.utils import timezone


    
class Full_and_Final_Settltment(models.Model):
    Name = models.CharField(max_length=250, null=True, blank=True)
    Emp_Code = models.CharField(max_length=250, null=True, blank=True)
    DOJ = models.DateField(default=timezone.now, blank=True, null=True)
    Date_Of_Leaving = models.DateField(default=timezone.now)
    Dept = models.CharField(max_length=250, null=True, blank=True)
    Designation = models.CharField(max_length=250, null=True, blank=True)

    EmpStatus = models.CharField(max_length=250, null=True, blank=True)
    Emp_Resignation_Date = models.CharField(max_length=250, null=True, blank=True)

    # Exit Reason Flags
    Absconding = models.CharField(max_length=50, null=True, blank=True)             # Yes/NO
    Resignation = models.CharField(max_length=50, null=True, blank=True)            # Yes/NO
    Notice_Days_Served = models.CharField(max_length=50, null=True, blank=True)     # Yes/NO
    Confirmed = models.CharField(max_length=50, null=True, blank=True)              # Yes/NO
    Terminated = models.CharField(max_length=50, null=True, blank=True)             # Yes/NO
    Laid_Off = models.CharField(max_length=250, null=True, blank=True)              # Yes/NO
    Deduction_from_salary_PL_Boolean = models.CharField(max_length=250, null=True, blank=True)   # Yes/NO

    # Salary & Leave
    Deduction_from_salary_PL = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)     # No use
    Current_Salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    PL_Basic_Salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    NPP_Gross = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Leave Summary
    LS_Period = models.DateField(default=timezone.now, null=True, blank=True)  # No use

    LS_Opening_Balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    LS_Leaved_Earned = models.CharField(max_length=250, null=True, blank=True)
    LS_Leaved_Availed = models.CharField(max_length=250, null=True, blank=True)
    LS_PL_Bal = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # New Two fields
    Employee_PF_Amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    PT_Amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)


    # PL Payment
    PL_Total_PL = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    PL_Rate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    PL_Amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    Total_PL_Balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Notice Period Pay
    NPP_Total_Notice_Pay_Days = models.CharField(max_length=250, null=True, blank=True)
    NPP_Rate = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    NPP_Net_Amount_Paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
        # New Field
    Total_Notice_Days_Served = models.CharField(max_length=250, null=True, blank=True)

    # Gratuity Payment
    GP_No_Of_Years = models.CharField(max_length=250, null=True, blank=True)
    GP_Last_Basics = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    GP_Graturity_Days = models.CharField(max_length=250, null=True, blank=True) # Graturity Days Per year
    GP_Graturity_Payments = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    FFPS_Pending_Salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Final Inputs
    FFPS_PL = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)           # PL Payment
    FFPS_Gratuity = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)     # Graturity Payments
    FFPS_Grand_Total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # Final Payable Amount
    FFPS_Deductions = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)   # TOTAL DEDUCTION
    FFPS_Uniform_Deductions = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # Uniform Deductions
    FFPS_Payable_Amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)       # No data add

    OrganizationID = models.BigIntegerField(null=True, blank=True)
    CreatedBy = models.BigIntegerField(default=0, null=True, blank=True)
    CreatedDateTime = models.DateField(default=timezone.now, null=True, blank=True)
    ModifyBy = models.BigIntegerField(default=0, null=True, blank=True)
    ModifyDateTime = models.DateField(default=timezone.now, null=True, blank=True)
    IsDelete = models.BooleanField(default=False)


    PaymentStatus = models.CharField(max_length=50, null=True, blank=True)          # in use
    
    # Not in use
    PaymentPaidAmount = models.DecimalField(max_digits=12, blank=True, null=True, decimal_places=2)
    PaymentPaidDate = models.DateField(default=None, blank=True, null=True)
    PaymentRemarks = models.CharField(max_length=250, default=None, blank=True, null=True)
    

    FinalStatus = models.CharField(max_length=50, default='Pending', null=True, blank=True)
    FinalStatusUpdateDate = models.DateField(default=timezone.now, null=True, blank=True)
    
    AuditedBy = models.CharField(max_length=50, null=True, blank=True) # used in "Auditor" select - option dropdown

    # New Field
        # AuditedBy
    AuditedByHR = models.CharField(max_length=50, null=True, blank=True)
    AuditedByHR_Date_Time = models.DateField(default=timezone.now, null=True, blank=True)

    AuditedByFinance = models.CharField(max_length=50, null=True, blank=True)
    AuditedByFinance_Date_Time = models.DateField(default=timezone.now, null=True, blank=True)

    AuditedByGM = models.CharField(max_length=50, null=True, blank=True)
    AuditedByGM_Date_Time = models.DateField(default=timezone.now, null=True, blank=True)

    PaymentStatus = models.CharField(max_length=50, null=True, blank=True)
    PaymentStatus_Date_Time = models.CharField(max_length=50, null=True, blank=True)

        #existing Field
    AuditedBy_Auditor = models.CharField(max_length=50, null=True, blank=True) # used in "Auditor" select - option dropdown
    AuditedBy_Auditor_Date_Time = models.CharField(max_length=50, null=True, blank=True)


    # New Field
    Leave_PL_From_Date = models.DateField(null=True, blank=True)
    Leave_PL_To_Date = models.DateField(null=True, blank=True)

        # Earnings
    LTA_Amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Other_Earnings = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Pending_Salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Total_Earning = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

        # Deductions
    OtherDeductions = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Notice_Period_Deductions = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Advance_Salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Total_Deductions = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # as FFPS_Deductions

        # Advance Salary **
    Total_Advance_Taken = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Total_Advance_Paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Remaining_Amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

        # Bank Details **
    Bank_Name = models.CharField(max_length=100, null=True, blank=True)
    Branch_Name = models.CharField(max_length=100, null=True, blank=True)
    Accounts_Number = models.CharField(max_length=50, null=True, blank=True)
    IFSCCode = models.CharField(max_length=20, null=True, blank=True)

        # Leave Travel Entitlement **
    # TOTALMONTHSWORKED = models.IntegerField(null=True, blank=True)
    # LTARATE = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # TOTALDAYSWORKED = models.IntegerField(null=True, blank=True)
    # PRORATABASISPAYMENT = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

        # Leave Travel Entitlement **
    Total_Months_Worked = models.IntegerField(null=True, blank=True)
    LTA_Rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Total_Days_Worked = models.IntegerField(null=True, blank=True)
    Pro_Rata_Basis_Payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    # Remarks
    LTA_Remarks = models.TextField(null=True, blank=True)
    Final_PL_Payment_Remarks = models.TextField(null=True, blank=True)
    Other_Earnings_Remarks = models.TextField(null=True, blank=True)
    Pending_Salary_Remarks = models.TextField(null=True, blank=True)
    Total_Earning_Remarks = models.TextField(null=True, blank=True)
    Uniform_Deductions_Remarks = models.TextField(null=True, blank=True)
    Other_Deductions_Remarks = models.TextField(null=True, blank=True)
    Notice_Period_Deductions_Remarks = models.TextField(null=True, blank=True)
    Advance_Salary_Remarks = models.TextField(null=True, blank=True)
    Total_Deductions_Remarks = models.TextField(null=True, blank=True)
    Graturity_Payments_Earning_Remarks = models.TextField(null=True, blank=True)
    PT_Amount_Remarks = models.TextField(null=True, blank=True)
    Employee_PF_Amount_Remarks = models.TextField(null=True, blank=True)


    file_id = models.CharField(max_length=200,null=True, blank=True)
    file_name = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.Name
    