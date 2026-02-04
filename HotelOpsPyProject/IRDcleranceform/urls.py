from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('IRDCleranceRegisrtration', views.IRDCleranceRegisrtration,name='IRDCleranceRegisrtration'),
    
    path("IRDCleranceList/",views.IRDCleranceList,name="IRDCleranceList"),
    
    path("IRDCleranceEditList/",views.IRDCleranceEditList,name="IRDCleranceEditList"),
    
    path("IRDCleranceUpdateData/",views.IRDCleranceUpdateData,name="IRDCleranceUpdateData"),
    
    path("IRDCleranceDeleteData/",views.IRDCleranceDeleteData,name="IRDCleranceDeleteData"),
    
    path("IRDClerance_pdf_view/",views.IRDClerance_pdf_view,name="IRDClerance_pdf_view"),
    

]