from django.urls import path
from .import views

urlpatterns = [
    path('Debit_Note_Entry_Emp/',views.Debit_Note_Entry_Emp,name='Debit_Note_Entry_Emp'),
    path('Debit_Note_Emp_List/',views.Debit_Note_Emp_List,name='Debit_Note_Emp_List'),
    
    path('Generate_Letter_of_Debit_Note/',views.Generate_Letter_of_Debit_Note,name='Generate_Letter_of_Debit_Note'),
    path('Debit_Note_Emp_Delete/',views.Debit_Note_Emp_Delete,name='Debit_Note_Emp_Delete'),

    path('Debit_Note_Upload_File/', views.Debit_Note_Upload_File, name="Debit_Note_Upload_File"),
    path('Debit_Note_Download_File/', views.Debit_Note_Download_File, name="Debit_Note_Download_File"),
    path('Debit_Note_Repalce_File/', views.Debit_Note_Repalce_File, name="Debit_Note_Repalce_File"),
]
