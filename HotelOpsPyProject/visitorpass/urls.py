from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('VisitorPassForm', views.VisitorPassForm,name='VisitorPassForm'),
    
    path("VisitorPassList/",views.VisitorPassList,name="VisitorPassList"),
    
    path("VisitorPassEditData/",views.VisitorPassEditData,name="VisitorPassEditData"),
    
    path("VisitorPassUpdateData/",views.VisitorPassUpdateData,name="VisitorPassUpdateData"),
    
    path("VisitorPassDeleteData/",views.VisitorPassDeleteData,name="VisitorPassDeleteData"),
    
    path("VisitorPass_pdf_view/",views.VisitorPass_pdf_view,name="VisitorPass_pdf_view"),
  
  
]