from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('ScantyBaggageForm', views.ScantyBaggageForm,name='ScantyBaggageForm'),
    
    path("ScantyBaggageList/",views.ScantyBaggageList,name="ScantyBaggageList"),
    
    path("ScantyBaggageEditList/",views.ScantyBaggageEditList,name="ScantyBaggageEditList"),
    
    path("ScantyBaggageUpdateData/",views.ScantyBaggageUpdateData,name="ScantyBaggageUpdateData"),
    
    path("ScantyBaggageDeleteData/",views.ScantyBaggageDeleteData,name="ScantyBaggageDeleteData"),
    
    path("ScantyBaggage_pdf_view/",views.ScantyBaggage_pdf_view,name="ScantyBaggage_pdf_view"),
    
    
]