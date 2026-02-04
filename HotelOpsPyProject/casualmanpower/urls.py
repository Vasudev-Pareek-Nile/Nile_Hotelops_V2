from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('CasualManPowerRequisition', views.CasualManPowerRequisition,name='CasualManPowerRequisition'),
    
    path("CasualManPowerList/",views.CasualManPowerList,name="CasualManPowerList"),
    
    path("CasualManPowerEditList/",views.CasualManPowerEditList,name="CasualManPowerEditList"),
    
    path("UpdateCasualManPowerData/",views.UpdateCasualManPowerData,name="UpdateCasualManPowerData"),
    
    path("CasualManPowerDeleteData/",views.CasualManPowerDeleteData,name="CasualManPowerDeleteData"),
    
    path("CasualManpower_pdf_view/",views.CasualManpower_pdf_view,name="CasualManpower_pdf_view"),
    
    
]
