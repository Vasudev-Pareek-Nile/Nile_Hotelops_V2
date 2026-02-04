# from django import forms
# from .models import LETTEROFINTENTEmployeeDetail
# from app.models import EmployeeMaster

# class EmpDetailsForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         org_id = kwargs.pop('initial', {}).get('OrganizationID', None)
#         super().__init__(*args, **kwargs)
#         if org_id:
#             self.fields['general_manager_name'].choices = self.get_choices(org_id)

#     def get_choices(self, org_id):
#         LevelList = ['M6', 'M4']
#         choices = EmployeeMaster.objects.filter(OrganizationID=org_id, Level__in=LevelList)
#         formatted_choices = [(f"{employee.EmpName} - {employee.Designation}", employee.EmpName) for employee in choices]
#         return formatted_choices

#     general_manager_name = forms.ChoiceField(
#         choices=[],  # Initialize with an empty list
#         label='Select General Manager',
#         widget=forms.Select(attrs={'class': 'form-control', 'id': 'general_manager_name'})
#     )
    
#     general_manager_Desigination = forms.CharField(
#         max_length=255,
#         label='Designation',
#         widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'general_manager_Desigination'})
#     )

#     class Meta:
#         model = LETTEROFINTENTEmployeeDetail
#         fields = [
#             'prefix', 'emp_name', 'date_of_intent', 'date_of_joining', 'department',
#             'designation', 'ctc', 'general_manager_name', 'general_manager_Desigination',
#             'OrganizationID', 'CreatedBy', 'visible_salary_breakup', 'InterviewID'
#         ]
#         widgets = {
#             'OrganizationID': forms.HiddenInput(),
#             'InterviewID': forms.HiddenInput(),
#             'CreatedBy': forms.HiddenInput(),
#             'prefix': forms.Select(attrs={'class': 'form-control'}),
#             'emp_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Employee Name'}),
#             'date_of_intent': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'date_of_joining': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#             'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department'}),
#             'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Designation'}),
#             'ctc': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Basic Salary'}),
#             'visible_salary_breakup': forms.Select(attrs={'class': 'form-control'}),
#         }
