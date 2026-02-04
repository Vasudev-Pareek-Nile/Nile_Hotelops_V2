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


# class RadioInput(forms.RadioSelect):
#     input_type = 'radio'



class LinenInventoryForm(forms.ModelForm):
    class Meta:
        model=models.Linen_Inventory_Sheet
        fields=['From','To',"OrganizationID","CreatedBy"]
        widgets = {
            'From': DateInput,
            'To': DateInput, 
        } 
        
# class uniformitemmaster(forms.ModelForm):
#     class Meta:
#         model=models.Uniform_Item_Master
#         fields=['Item_Title_Name']