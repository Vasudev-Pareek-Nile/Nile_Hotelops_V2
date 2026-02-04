from django.db import models
from datetime import date
from django.utils import timezone 

# Create your models here.
class AdvanceSalaryForm(models.Model):
    Application_Form_No = models.AutoField(primary_key=True)
    # EmpID = models.BigIntegerField(default=0)
    EmpID =  models.CharField(max_length=200,null=False,blank=False)
    emp_code =  models.CharField(max_length=200,null=False,blank=False)
    EmployeeName = models.CharField(max_length=255,null=True,blank=True)
    Designation = models.CharField(max_length=255,null=True,blank=True)
    Department = models.CharField(max_length=255,null=True,blank=True)
    DateofLoan = models.DateField(null=True,blank=True)
    LoanAmount = models.BigIntegerField(default=0)
    No_Of_Installments = models.BigIntegerField(default=0)
    BankACNo = models.BigIntegerField(default=0)
    Reasons_For_Request  = models.CharField(max_length=255,null=True,blank=True)

    # ACCOUNTS DEPARTMENT
    Prev_Loan_Taken = models.BigIntegerField(default=0)
    Dues_Repayment = models.BigIntegerField(default=0)
    Prev_No_Of_Installments = models.BigIntegerField(default=0)
    Reason_For_PreviousLoan = models.CharField(max_length=255,null=True,blank=True)

    # HUMAN RESOURCES DEPARTMENT
    Current_Salary =  models.CharField(max_length=255,null=True,blank=True)
    Recommendation =  models.CharField(max_length=255,null=True,blank=True)
    DateofJoining = models.DateField(null=True,blank=True)

    # Importnat 
    OrganizationID = models.BigIntegerField(default=0)
    created_by = models.BigIntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)
    modify_by = models.BigIntegerField(default=0)
    modify_date_time = models.DateTimeField(default=timezone.now)
    is_delete = models.BooleanField(default=False)


