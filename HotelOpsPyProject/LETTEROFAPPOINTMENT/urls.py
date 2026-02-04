from django.urls import path
from .import views

urlpatterns = [
    path('entryemploa/',views.entryEmp,name='entryemploa'),
    path('emplistloa/',views.emplist,name='emplistloa'),
    path('generate_appointment_letter/',views.Generate_Appointment_Letter,name='generate_appointment_letter'),
    
    # path('empupdateloa/<str:pk>',views.empupdate,name='empupdateloa'),
    path('empdeleteloa/',views.empdelete,name='empdeleteloa'),
     
    path('upload_fileloa/', views.upload_file, name="upload_fileloa"),
    path('download_fileloa/', views.download_file, name="download_fileloa"),
    path('repalce_fileloa/', views.repalce_file, name="repalce_fileloa"),

]
