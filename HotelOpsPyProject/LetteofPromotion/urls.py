from django.urls import path
from .import views

urlpatterns = [



    path('entryemppl/',views.entryEmp,name='entryemppl'),
    path('emplistpl/',views.emplist,name='emplistpl'),
    
    path('generate_Letter_of_promotion/',views.generate_Letter_of_promotion,name='generate_Letter_of_promotion'),
    path('empdeletepl/',views.empdelete,name='empdeletepl'),
   
    path('upload_filepl/', views.upload_file, name="upload_filepl"),
     path('download_filepl/', views.download_file, name="download_filepl"),
     path('repalce_filepl/', views.repalce_file, name="repalce_filepl"),

]
