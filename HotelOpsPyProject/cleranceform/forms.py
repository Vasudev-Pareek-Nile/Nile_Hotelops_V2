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


class RadioInput(forms.RadioSelect):
    input_type = 'radio'



class ClearanceForm(forms.ModelForm):
    class Meta:
        model=models.clearnce_form
        fields=['Name','EmpCode','Separation_Date','Position','Finishing_Time','Resignation_Letter','Acc_Of_Resign','Notice_Period_Served','Notice_Period_Waived_Off','Exit_Interview_By_Hr','Full_And_Final_Settlement',"OrganizationID","CreatedBy"]
        widgets = {
            'Date': DateInput,
            'Separation_Date': DateInput,
            'Finishing_Time':TimeInput,
            'Resignation_Letter':RadioInput,
            'Acc_Of_Resign':RadioInput,
            'Notice_Period_Served':RadioInput,
            'Notice_Period_Waived_Off':RadioInput,
            'Exit_Interview_By_Hr':RadioInput,
            'Full_And_Final_Settlement':RadioInput,  
        } 
        
        
        