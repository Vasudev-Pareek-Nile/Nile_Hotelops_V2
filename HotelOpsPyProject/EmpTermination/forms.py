# from django import forms
# from . import models

# #for admin signup
        

# class DateInput(forms.DateInput):
#     input_type = 'date'


# class HiddenInput(forms.HiddenInput):
#     input_type = 'hidden'


# # class TimeInput(forms.TimeInput):
# #     input_type = 'time'


# class EmpTerminationForm(forms.ModelForm):
#     class Meta:
#         model=models.EmpTerminationModel
#         fields=['Name','Emp_Code','DOJ','Date_Of_Termination','Dept','Designation','IsWarningIssued','LastWarningLatter','Remarks',"OrganizationID","CreatedBy"]
#         widgets = {
#             'DOJ': DateInput,
#             'Date_Of_Termination': DateInput,
#             'OrganizationID':HiddenInput,
#             'CreatedBy':HiddenInput
            
#         }