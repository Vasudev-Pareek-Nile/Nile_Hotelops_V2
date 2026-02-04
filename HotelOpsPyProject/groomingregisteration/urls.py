from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('GroomingRegisterationForm', views.GroomingRegisterationForm,name='GroomingRegisterationForm'),
    
    path("GroomingRegisterationList/",views.GroomingRegisterationList,name="GroomingRegisterationList"),
    
    path("GroomingEditList/",views.GroomingEditList,name="GroomingEditList"),
    
    path("GroomingUpdateData/",views.GroomingUpdateData,name="GroomingUpdateData"),
    
    path("GroomingDeleteData/",views.GroomingDeleteData,name="GroomingDeleteData"),
    
    path("GroomingList_pdf_view/",views.GroomingList_pdf_view,name="GroomingList_pdf_view"),
    
   
  
  
]