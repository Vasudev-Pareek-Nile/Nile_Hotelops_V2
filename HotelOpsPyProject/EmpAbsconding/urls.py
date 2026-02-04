from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('EmpAbscondingEntry/', views.EmpAbscondingEntry,name='EmpAbscondingEntry'),
    
    path("EmpAbscondingList/",views.EmpAbscondingList,name="EmpAbscondingList"),
    
    
    path("EmpAbscondingDelete/",views.EmpAbscondingDelete,name="EmpAbscondingDelete"),
    
    path("EmpAbscondingPDF/",views.EmpAbscondingPDF,name="EmpAbscondingPDF"),
    
    path('EmpshowcausenoticeEntry/', views.EmpshowcausenoticeEntry,name='EmpshowcausenoticeEntry'),
    
    path("EmpshowcausenoticeList/",views.EmpshowcausenoticeList,name="EmpshowcausenoticeList"),
    
    
    path("EmpshowcausenoticeDelete/",views.EmpshowcausenoticeDelete,name="EmpshowcausenoticeDelete"),
    
    path("EmpshowcausenoticePDF/",views.EmpshowcausenoticePDF,name="EmpshowcausenoticePDF"),
  
  
  
]