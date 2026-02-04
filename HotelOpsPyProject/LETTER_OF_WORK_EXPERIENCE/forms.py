# from django import forms
# from .models import LETTEROFEXPERIENCEEmployeeDetail
# from ckeditor.fields import RichTextFormField
# class EmpDetailsForm(forms.ModelForm):
#     class Meta:
#         model = LETTEROFEXPERIENCEEmployeeDetail 
#         fields = ['emp_code','prefix','first_name','last_name','generate_date','date_of_joining','date_of_last_working','department','designation',"Hr_manager_name","OrganizationID","CreatedBy",'data']
#         widgets =  {
#             'OrganizationID':forms.HiddenInput(),
#             'CreatedBy':forms.HiddenInput(),
#             'emp_code':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Emp Code'}),
#             'prefix':forms.Select(attrs={'class':'form-control'}),
#             'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),
#             'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),
            
            
#             'generate_date': forms.NumberInput(attrs={'class':'form-control','type': 'date', }),

#             'date_of_joining':forms.NumberInput(attrs={'class':'form-control','type': 'date', }),
            
#             'date_of_last_working':forms.NumberInput(attrs={'class':'form-control','type': 'date', }),

#             'department':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Department'}),
            
#             'designation':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Designation'}),
            
#             'Hr_manager_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter HR Manager Name'}),
            
            
            

#             'data':RichTextFormField(),
#         }