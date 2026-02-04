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


class MessageAndParcelForm(forms.ModelForm):
    class Meta:
        model=models.Message_Parcel_Register
        fields=['Type_Of_Article','Room_No','Guest_Name','Date_Of_Arrival','Received_From','Contact_No','Received_By','Date_Of_Delivery','Given_By','Handed_Over_To','Remarks',"OrganizationID","CreatedBy"]
        widgets = {
            'Date_Of_Arrival': DateInput,
            'Date_Of_Delivery':DateInput,
        }