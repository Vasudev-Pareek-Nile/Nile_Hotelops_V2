from django.urls import path
from .import views

urlpatterns = [
    path('Policy_Posh_Entry_Emp/',views.Policy_Posh_Entry_Emp,name='Policy_Posh_Entry_Emp'),
    path('Policy_Posh_Emp_List/',views.Policy_Posh_Emp_List,name='Policy_Posh_Emp_List'),
    
    path('Generate_Letter_of_Policy_Posh/',views.Generate_Letter_of_Policy_Posh,name='Generate_Letter_of_Policy_Posh'),
    path('Policy_Posh_Emp_Delete/',views.Policy_Posh_Emp_Delete,name='Policy_Posh_Emp_Delete'),

    path('Policy_Posh_Upload_File/', views.Policy_Posh_Upload_File, name="Policy_Posh_Upload_File"),
    path('Policy_Posh_Download_File/', views.Policy_Posh_Download_File, name="Policy_Posh_Download_File"),
    path('Policy_Posh_Repalce_File/', views.Policy_Posh_Repalce_File, name="Policy_Posh_Repalce_File"),
]
