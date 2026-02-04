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


class IRDCleranceForm(forms.ModelForm):
    class Meta:
        model=models.IRD_Clerance
        fields=['Date','Clerance_time','Remarks',"OrganizationID","CreatedBy"]
        widgets = {
            'Date': DateInput,
            # 'Clerance_time':TimeInput,
        }
        
        