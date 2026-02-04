from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('CakeOrder', views.CakeOrder,name='CakeOrder'),
    
    path("CakeOrderList/",views.CakeOrderList,name="CakeOrderList"),
    
    path("CakeOrderEditData/",views.CakeOrderEditData,name="CakeOrderEditData"),
    
    path("CakeOrderUpdateData/",views.CakeOrderUpdateData,name="CakeOrderUpdateData"),
    
    path("delete/",views.Delete,name="delete"),
    
    path("CakeOrderList_pdf_view/",views.CakeOrderList_pdf_view,name="CakeOrderList_pdf_view"),
  
  
]