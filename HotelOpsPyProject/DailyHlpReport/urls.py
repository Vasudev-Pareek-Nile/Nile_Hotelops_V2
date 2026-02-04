from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('DailyHlpRegistrationForm', views.DailyHlpRegistrationForm,name='DailyHlpRegistrationForm'),
    
    path("DailyHlpList/",views.DailyHlpList,name="DailyHlpList"),
    
    # path("UniformInventoryEditList/",views.UniformInventoryEditList,name="UniformInventoryEditList"),
    
    # path("UpdateUniformInventorylist/",views.UpdateUniformInventorylist,name="UpdateUniformInventorylist"),
    
    # path("DeleteUniformInventory/",views.DeleteUniformInventory,name="DeleteUniformInventory"),
    
    # path("UniformInventory_pdf_view/",views.UniformInventory_pdf_view,name="UniformInventory_pdf_view"),
    
    # path("UniformItemMasterlist/",views.UniformItemMasterlist,name="UniformItemMasterlist"),
       
    
]