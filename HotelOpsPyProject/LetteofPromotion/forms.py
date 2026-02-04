# from django import forms
# from .models import PromotionLetterEmployeeDetail
# from ckeditor.fields import RichTextFormField
# class EmpDetailsForm(forms.ModelForm):
#     class Meta:
#         model = PromotionLetterEmployeeDetail
#         fields = ['emp_code','prefix','first_name','last_name','date_of_promtion','department','designation','Promotiondesignation','general_manager_name',"OrganizationID","CreatedBy",'data']
#         widgets =  {
#             'OrganizationID':forms.HiddenInput(),
#             'CreatedBy':forms.HiddenInput(),
#             'emp_code':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter Emp Code'}),
#             'prefix':forms.Select(attrs={'class':'form-control'}),
#             'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),
#             'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),
            
            
#             'date_of_promtion': forms.NumberInput(attrs={'class':'form-control','type': 'date', }),
            
#             'department':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Department'}),
#             'designation':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Designation'}),
#             'Promotiondesignation':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Promotion Designation'}),
            
#             'general_manager_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter GM Name'}),

#             'data':RichTextFormField(),
#         }