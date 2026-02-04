from django.urls import path
from .import views

urlpatterns = [
    path('entryemploi/',views.entryEmp,name='entryemploi'),
    path('emplistloi/',views.emplist,name='emplistloi'),
    
    path('generate_letter_of_intent/',views.generate_letter_of_intent,name='generate_letter_of_intent'),
    path('empdeleteloi/',views.empdelete,name='empdeleteloi'),

     path('upload_fileloi/<int:id>/', views.upload_file, name="upload_fileloi"),
     path('download_fileloi/<int:id>/', views.download_file, name="download_fileloi"),
     path('repalce_fileloi/<int:id>/', views.repalce_file, name="repalce_fileloi"),
     
     path('InterviewAssessmentCandidate/', views.InterviewAssessmentCandidate, name="InterviewAssessmentCandidate"),
     path('SendMailToCandidate/', views.SendMailToCandidate, name="SendMailToCandidate"),
     path('Acceptloi/', views.Acceptloi, name="Acceptloi"),



    

   



]
