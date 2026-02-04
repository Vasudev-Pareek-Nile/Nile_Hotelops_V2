from django.urls import path
from .import views
urlpatterns = [
     path('Checklistadd/',views.Checklistadd,name="Checklistadd"),
     path('Checklistshow/',views.Checklistshow,name="Checklistshow"),
     path('EmpChecklist/',views.EmpChecklist,name="EmpChecklist"),
     path('ChecklistView/',views.ChecklistView,name="ChecklistView"),
     
    
]