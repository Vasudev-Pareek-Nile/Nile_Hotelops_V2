from django.urls import path
from .import views

urlpatterns = [
    path('Trainees_Entry_Emp/',views.Trainees_Entry_Emp,name='Trainees_Entry_Emp'),
    path('Trainees_Emp_List/',views.Trainees_Emp_List,name='Trainees_Emp_List'),
    
    path('Generate_Letter_of_Trainees_Experience/',views.Generate_Letter_of_Trainees_Experience,name='Generate_Letter_of_Trainees_Experience'),
    path('Trainees_Emp_Delete/',views.Trainees_Emp_Delete,name='Trainees_Emp_Delete'),

    path('Trainees_Upload_File/', views.Trainees_Upload_File, name="Trainees_Upload_File"),
    path('Trainees_Download_File/', views.Trainees_Download_File, name="Trainees_Download_File"),
    path('Trainees_Repalce_File/', views.Trainees_Repalce_File, name="Trainees_Repalce_File"),
]
