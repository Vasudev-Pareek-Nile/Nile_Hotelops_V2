from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('ReferenceCheck', views.ReferenceCheck,name='ReferenceCheck'),
    
    path("ReferenceChecklist/",views.ReferenceChecklist,name="ReferenceChecklist"),
    
    path("ReferenceEditList/",views.ReferenceEditList,name="ReferenceEditList"),
    
    path("UpdateReferenceForm/",views.UpdateReferenceForm,name="UpdateReferenceForm"),
    
    path("ReferenceDeleteList/",views.ReferenceDeleteList,name="ReferenceDeleteList"),
    
    path("ReferenceForm_pdf_view/",views.ReferenceForm_pdf_view,name="ReferenceForm_pdf_view"),
    
    # path("ReferenceMasterlist/",views.ReferenceMasterlist,name="ReferenceMasterlist"),
    
    
]