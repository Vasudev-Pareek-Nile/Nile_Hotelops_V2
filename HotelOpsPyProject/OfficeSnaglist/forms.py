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


class OfficeSnagForm(forms.ModelForm):
    class Meta:
        model=models.Office_Snag_Registration_Form
        fields=['Area','Date',"OrganizationID","CreatedBy"]
        widgets = {
            'Date': DateInput,
        } 