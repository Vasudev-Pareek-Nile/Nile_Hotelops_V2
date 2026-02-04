from django.urls import path
from .import views

urlpatterns = [
   

    path('UploadResume',views.upload_resume,name='UploadResume'),
    path('TestEmail',views.TestEmail,name='TestEmail'),

    path('resume_list',views.resume_list,name='resume_list'),
    path('download_resume/<int:id>/', views.download_resume, name="download_resume"),

]
