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


class ScantyBaggageForm(forms.ModelForm):
    class Meta:
        model=models.Scanty_Baggage_Register_Form
        fields=['Date','Room_No','Guest_Name','Arrival_Date','Departure_Date','Deposite','Comment','Front_Desk_Associate','Duty_Manager','Remarks',"OrganizationID","CreatedBy"]
        widgets = {
            'PM_Date': DateInput,
            # 'In_Time':TimeInput,
        }