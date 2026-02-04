from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('EquipmentAndTrolleyForm', views.EquipmentAndTrolleyForm,name='EquipmentAndTrolleyForm'),
    
    path("EquipmentAndTrolleyList/",views.EquipmentAndTrolleyList,name="EquipmentAndTrolleyList"),
    
    path("EquipmentEditList/",views.EquipmentEditList,name="EquipmentEditList"),
    
    path("EquipmentUpdateData/",views.EquipmentUpdateData,name="EquipmentUpdateData"),
    
    path("EquipmentDeleteData/",views.EquipmentDeleteData,name="EquipmentDeleteData"),
    
    path("EquipmentList_pdf_view/",views.EquipmentList_pdf_view,name="EquipmentList_pdf_view"),
    
   
  
  
]