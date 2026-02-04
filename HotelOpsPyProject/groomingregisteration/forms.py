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


class GroomingRegisterationForm(forms.ModelForm):
    class Meta:
        model=models.Grooming_Registeration
        fields=['Date','Audit_Type','Name','Shoes','Shocks','Nails','Hair','Uniform','Name_Badge','Brand_Pin','Remarks',"OrganizationID","CreatedBy"]
        widgets = {
            'Date': DateInput,
        }