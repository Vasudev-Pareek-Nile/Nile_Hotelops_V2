from django import forms
from django.contrib.auth.models import User
from . import models

#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        

class DateInput(forms.DateInput):
    input_type = 'date'


# class TimeInput(forms.TimeInput):
#     input_type = 'time'


class PayMasterForm(forms.ModelForm):
    class Meta:
        model=models.Pay_Master
        fields=['PM_Number','PM_Date','Name','Amount','Employee_Name','Reason',"OrganizationID","CreatedBy"]
        widgets = {
            'PM_Date': DateInput,
            # 'In_Time':TimeInput,
        }