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


class TimeInput(forms.TimeInput):
    input_type = 'time'


class CasualManpowerRequisition(forms.ModelForm):
    class Meta:
        model=models.Casual_Manpower_Requisition
        fields=['Date','Prepared_By','Department','Numbers_Required','Reason','Function','Rate','No_Of_Pax','Date_Required','Est_Sales_Volume','Reporting_Time',"OrganizationID","CreatedBy"]
        widgets = {
            'Date': DateInput,
            'Date_Required': DateInput,
            'Reporting_Time':TimeInput
        }
        # widgets = {
        #     'Required_Date': DateInput