from django import forms
from .models import LOALETTEROFAPPOINTMENTEmployeeDetail
from ckeditor.fields import RichTextFormField
class EmpDetailsForm(forms.ModelForm):
    class Meta:
        model = LOALETTEROFAPPOINTMENTEmployeeDetail
        fields = ['emp_code','prefix','first_name','last_name','mobile_number','email','date_of_appointment','date_of_joining','department','designation','Reporting_to_designation','hr_manager_name','general_manager_name','grade','level','basic_salary','address',"OrganizationID","CreatedBy",'data']
        widgets =  {
            'OrganizationID':forms.HiddenInput(),
            'CreatedBy':forms.HiddenInput(),
            'emp_code':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Emp Code'}),
            'prefix':forms.Select(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),
            'mobile_number':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Mobile Number'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Email'}),
            'date_of_appointment': forms.NumberInput(attrs={'class':'form-control','type': 'date', }),
            'date_of_joining':forms.NumberInput(attrs={'class':'form-control','type': 'date', }),
            'department':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Department'}),
            'designation':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Designation'}),
            'Reporting_to_designation':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Reporting to Designation'}),
            
            'hr_manager_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Hr Manager Name'}) ,
            'general_manager_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter  GM Name'}) ,

            'grade':forms.HiddenInput(attrs={'class':'form-control'}),
            'level':forms.Select(attrs={'class':'form-control'}),
            'basic_salary':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Basic Salary'}),
            'address':forms.Textarea(attrs={'class':'form-control','style':'height:50px','placeholder':'Enter Address'}),
            'data':RichTextFormField(),
        }