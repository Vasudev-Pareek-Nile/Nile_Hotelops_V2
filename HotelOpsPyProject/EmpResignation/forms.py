from django import forms
from . import models

#for admin signup
        

class DateInput(forms.DateInput):
    input_type = 'date'


class HiddenInput(forms.HiddenInput):
    input_type = 'hidden'


# class TimeInput(forms.TimeInput):
#     input_type = 'time'


class EmpResigantionForm(forms.ModelForm):
    class Meta:
        model=models.EmpResigantionModel
        fields=['Name','Emp_Code','DOJ','Date_Of_res','Dept','Designation','TypeofRes','Res_Reason','NoticePeriod','Ressubmittedto','LastWorkingDays','Res_acceptance_Date','Res_acceptance_By',"OrganizationID","CreatedBy"]
        widgets = {
            'DOJ': DateInput,
            'Date_Of_res': DateInput,
            'LastWorkingDays': DateInput,
            'Res_acceptance_Date' : DateInput,
            'OrganizationID':HiddenInput,
            'CreatedBy':HiddenInput
            
        }