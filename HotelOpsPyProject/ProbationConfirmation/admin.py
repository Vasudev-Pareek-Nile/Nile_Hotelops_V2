from django.contrib import admin
from .models import  Category_Master,Item_Master,Emp_Confirmation_Master,Emp_Confirmation_Details,Confirm_Date

List_Display =  [Category_Master,Item_Master,Emp_Confirmation_Master,Emp_Confirmation_Details,Confirm_Date]
admin.site.register(List_Display)


