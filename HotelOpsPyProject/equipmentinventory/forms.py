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


class EquipmentInventoryForm(forms.ModelForm):
    class Meta:
        model=models.Equipment_Inventory
        fields=['Date','Equipment_Name','Brand_Name','Model_No','In_Working_Condition','Last_Servicing_Date','AMC_Covered','Serial_No','Remarks',"OrganizationID","CreatedBy"]
        widgets = {
            'Date': DateInput,
        }