from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    
    path('cleranceformAPI', views.cleranceformAPI,name='cleranceformAPI'),
    
    path('cleranceform', views.cleranceform,name='cleranceform'),
    
    path("cleranceformlist/",views.cleranceformlist,name="cleranceformlist"),
    
    path("CleranceFormEditList/",views.CleranceFormEditList,name="CleranceFormEditList"),
    
    path("UpdateCleranceForm/",views.UpdateCleranceForm,name="UpdateCleranceForm"),
    
    path("CleranceFormDeleteData/",views.CleranceFormDeleteData,name="CleranceFormDeleteData"),
    
    path("CleranceForm_pdf_view/",views.CleranceForm_pdf_view,name="CleranceForm_pdf_view"),
    
    path("cleranceitemmasterlist/",views.cleranceitemmasterlist,name="cleranceitemmasterlist"),
    
    
]