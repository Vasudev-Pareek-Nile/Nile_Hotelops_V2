from django.urls import path
from .import views

urlpatterns = [
    path('entryempcl/',views.entryEmp,name='entryempcl'),
    path('emplistcl/',views.emplist,name='emplistcl'),
    
    path('generate_Confirmation_Letter/',views.generate_Confirmation_Letter,name='generate_Confirmation_Letter'),
    path('empupdatecl/<str:pk>',views.empupdate,name='empupdatecl'),
    path('empdeletecl/',views.empdelete,name='empdeletecl'),
    
    path('upload_filecl/', views.upload_file, name="upload_filecl"),
     path('download_filecl/', views.download_file, name="download_filecl"),
     path('repalce_filecl/', views.repalce_file, name="repalce_filecl"),


]
