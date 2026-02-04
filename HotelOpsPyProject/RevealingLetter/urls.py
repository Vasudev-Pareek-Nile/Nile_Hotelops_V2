from django.urls import path
from .views import entryEmp,Generate_Revealing_Letter,empdelete,upload_file,download_file,repalce_file
urlpatterns = [
    path('entryemprl/',entryEmp,name='entryemprl'),
   
    path('generate_revealing_letter/',Generate_Revealing_Letter,name='generate_revealing_letter'),
    
    # path('empupdaterl/<str:pk>',empupdate,name='empupdateloa'),
    path('empdeleterl/',empdelete,name='empdeleterl'),
     
    path('upload_filerl/', upload_file, name="upload_filerl"),
     path('download_filerl/', download_file, name="download_filerl"),
     path('repalce_filerl/', repalce_file, name="repalce_filerl"),
 
]
