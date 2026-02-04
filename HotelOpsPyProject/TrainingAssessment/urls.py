from django.urls import path
from .import views

urlpatterns = [
    # path('APITest/' , views.APITest , name = 'APITest'),
    path('TrainingAssessmentList/' , views.TrainingAssessmentList , name = 'TrainingAssessmentList'),
    path('TrainingAssessmentEntry/' ,views.TrainingAssessmentEntry , name= 'TrainingAssessmentEntry'),
    path('delete_TrainingAssessment/<int:id>/' , views.delete_TrainingAssessment , name ='delete_TrainingAssessment'),
    path('TrainingAssessmentEdit/<int:id>/' ,views.TrainingAssessmentEdit , name = 'TrainingAssessmentEdit'),
    path('TrainingAssessmentView/<int:id>/', views.TrainingAssessmentviewdata , name = 'TrainingAssessmentView'),
    
]
