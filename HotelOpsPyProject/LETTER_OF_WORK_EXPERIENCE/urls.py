from django.urls import path
from .import views

urlpatterns = [
    path('entryemploe/',views.entryEmp,name='entryemploe'),
    path('emplistloe/',views.emplist,name='emplistloe'),
    
    path('generate_letter_of_experience/',views.generate_letter_of_experience,name='generate_letter_of_experience'),
    path('empdeleteloe/',views.empdelete,name='empdeleteloe'),

    path('upload_fileloe/', views.upload_file, name="upload_fileloe"),
    path('download_fileloe/', views.download_file, name="download_fileloe"),
    path('repalce_fileloe/', views.repalce_file, name="repalce_fileloe"),

]
