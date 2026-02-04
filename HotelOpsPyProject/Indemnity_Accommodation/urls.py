from django.urls import path
from .import views

urlpatterns = [
    path('Indemnity_Accommodation_Entry_Emp/',views.Indemnity_Accommodation_Entry_Emp,name='Indemnity_Accommodation_Entry_Emp'),
    path('Indemnity_Accommodation_Emp_List/',views.Indemnity_Accommodation_Emp_List,name='Indemnity_Accommodation_Emp_List'),
    
    path('Generate_Letter_of_Indemnity_Accommodation/',views.Generate_Letter_of_Indemnity_Accommodation,name='Generate_Letter_of_Indemnity_Accommodation'),
    path('Indemnity_Accommodation_Emp_Delete/',views.Indemnity_Accommodation_Emp_Delete,name='Indemnity_Accommodation_Emp_Delete'),

    path('Indemnity_Accommodation_Upload_File/', views.Indemnity_Accommodation_Upload_File, name="Indemnity_Accommodation_Upload_File"),
    path('Indemnity_Accommodation_Download_File/', views.Indemnity_Accommodation_Download_File, name="Indemnity_Accommodation_Download_File"),
    path('Indemnity_Accommodation_Repalce_File/', views.Indemnity_Accommodation_Repalce_File, name="Indemnity_Accommodation_Repalce_File"),
]
