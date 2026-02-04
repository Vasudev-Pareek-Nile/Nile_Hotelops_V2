from django.urls import path
from .import views

urlpatterns = [
    path('entryemplsi/',views.entryEmp,name='entryemplsi'),
    path('emplistlsi/',views.emplist,name='emplistlsi'),
    
    path('generate_Letter_of_Salary_Increment/',views.generate_Letter_of_Salary_Increment,name='generate_Letter_of_Salary_Increment'),
    path('empdeletelsi/',views.empdelete,name='empdeletelsi'),

    path('upload_filelsi/', views.upload_file, name="upload_filelsi"),
    path('download_filelsi', views.download_file, name="download_filelsi"),
    path('repalce_filelsi', views.repalce_file, name="repalce_filelsi"),
]
