from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('MessageAndParcelForm', views.MessageAndParcelForm,name='MessageAndParcelForm'),
    
    path("MessageAndParcelList/",views.MessageAndParcelList,name="MessageAndParcelList"),
    
    path("MessageAndParcelEditList/",views.MessageAndParcelEditList,name="MessageAndParcelEditList"),
    
    path("MessageAndParcelUpdateData/",views.MessageAndParcelUpdateData,name="MessageAndParcelUpdateData"),
    
    path("MessageAndParcelDeleteData/",views.MessageAndParcelDeleteData,name="MessageAndParcelDeleteData"),
    
    path("ParcelList_pdf_view/",views.ParcelList_pdf_view,name="ParcelList_pdf_view"),
  
  
]