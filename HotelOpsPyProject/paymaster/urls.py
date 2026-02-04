from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('PaymasterForm', views.PaymasterForm,name='PaymasterForm'),
    
    path("PaymasterList/",views.PaymasterList,name="PaymasterList"),
    
    path("PaymasterEditList/",views.PaymasterEditList,name="PaymasterEditList"),
    
    path("PayMasterUpdateData/",views.PayMasterUpdateData,name="PayMasterUpdateData"),
    
    path("PayMasterDeleteData/",views.PayMasterDeleteData,name="PayMasterDeleteData"),
    
    path("PayMaster_pdf_view/",views.PayMaster_pdf_view,name="PayMaster_pdf_view"),
    

]