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
        
#For Cake Order Form
# class CakeOrderForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','username','password']
#         widgets = {
#         'password': forms.PasswordInput()
#         }

class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class CakeOrderForm(forms.ModelForm):
    class Meta:
        model=models.Cake_Order_Form
        fields=['To','Date','From','Time','Guest_Name','To_Be_Prepared_For','Size','Type_Of_Cake','Required_Date','Required_Time','Packing','Selling_Price','Message_On_Cake','Complimentory','Authorised_By',"OrganizationID","CreatedBy"]
        widgets = {
            'Date': DateInput,
            'Required_Date': DateInput,
            'Time':TimeInput,
            'Required_Time':TimeInput
        }