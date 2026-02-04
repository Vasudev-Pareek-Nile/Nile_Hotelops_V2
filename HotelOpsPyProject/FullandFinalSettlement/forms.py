# from django import forms
# from django.contrib.auth.models import User
# from . import models

# #for admin signup
# class AdminSigupForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','username','password']
#         widgets = {
#         'password': forms.PasswordInput()
#         }
        

# class DateInput(forms.DateInput):
#     input_type = 'date'


# # class TimeInput(forms.TimeInput):
# #     input_type = 'time'


# class FullandFinalSettlementForm(forms.ModelForm):
#     class Meta:
#         model=models.Full_and_Final_Settltment
#         fields=['Name','Emp_Code','DOJ','Date_Of_Leaving','Dept','Designation','Absconding','Notice_Days_Served','Resignation','Deduction_from_salary_PL','Confirmed','Current_Salary','Terminated','Laid_Off',
#             'LS_Period','LS_Opening_Balance','LS_Leaved_Earned','LS_Leaved_Availed','LS_PL_Bal','PL_Total_PL','PL_Basic_Salary','PL_Rate','PL_Amount','NPP_Total_Notice_Pay_Days','NPP_Gross','NPP_Rate',
#                 'NPP_Net_Amount_Paid','GP_No_Of_Years','GP_Last_Basics','GP_Graturity_Days','GP_Graturity_Payments','FFPS_Pending_Salary','FFPS_PL','FFPS_Gratuity','FFPS_Grand_Total','FFPS_Deductions','FFPS_Uniform_Deductions','FFPS_Payable_Amount',"OrganizationID","CreatedBy",
#                 'AuditedBy','PaymentStatus','PaymentPaidAmount','PaymentPaidDate','PaymentRemarks','FinalStatus']
#         widgets = {
#             'DOJ': DateInput,
#             'Date_Of_Leaving': DateInput,
#             'LS_Period' : DateInput,
#             'PaymentPaidDate':DateInput
            
#         }