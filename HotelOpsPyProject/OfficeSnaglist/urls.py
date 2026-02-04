from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('OfficeSnagRegistration', views.OfficeSnagRegistration,name='OfficeSnagRegistration'),
    
    path("OfficeSnagList/",views.OfficeSnagList,name="OfficeSnagList"),
    
    path("SnagEditList/",views.SnagEditList,name="SnagEditList"),
    
    path("UpdateOfficeSnagForm/",views.UpdateOfficeSnagForm,name="UpdateOfficeSnagForm"),
    
    path("OfficeSnagDeleteList/",views.OfficeSnagDeleteList,name="OfficeSnagDeleteList"),
    
    path("OfficeSnagForm_pdf_view/",views.OfficeSnagForm_pdf_view,name="OfficeSnagForm_pdf_view"),
    
    # path("ReferenceMasterlist/",views.ReferenceMasterlist,name="ReferenceMasterlist"),
    
    
]