# from django import forms
# from .models import LETTEROFSALARYINCREAMENTEmployeeDetail
# from ckeditor.fields import RichTextFormField
# class EmpDetailsForm(forms.ModelForm):
#     class Meta:
#         model = LETTEROFSALARYINCREAMENTEmployeeDetail
#         fields = ['emp_code','prefix','first_name','last_name','date_of_salary_increament','department','designation','general_manager_name','CTC',"OrganizationID","CreatedBy",'data']
#         widgets =  {
#             'OrganizationID':forms.HiddenInput(),
#             'CreatedBy':forms.HiddenInput(),
#             'emp_code':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Emp Code'}),
#             'prefix':forms.Select(attrs={'class':'form-control'}),
#             'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),
#             'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),
            
            
#             'date_of_salary_increament': forms.NumberInput(attrs={'class':'form-control','type': 'date', }),
            
#             'department':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Department'}),
#             'designation':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Designation'}),
            
#             'general_manager_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter  GM Name'}) ,
#             'CTC':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter  CTC'}) ,
#             'data':RichTextFormField(),
#         }