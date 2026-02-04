from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('LinenInventorySheet', views.LinenInventorySheet,name='LinenInventorySheet'),
    
    path("MasterLinenInventoryList/",views.MasterLinenInventoryList,name="MasterLinenInventoryList"),
    
    path("LinenInventoryEditList/",views.LinenInventoryEditList,name="LinenInventoryEditList"),
    
    path("UpdateLinenInventoryData/",views.UpdateLinenInventoryData,name="UpdateLinenInventoryData"),
    
    path("DeleteLinenInventoryData/",views.DeleteLinenInventoryData,name="DeleteLinenInventoryData"),
    
    path("LinenInventoryViewData/",views.LinenInventoryViewData,name="LinenInventoryViewData"),
    
    path("ItemMasterList/",views.ItemMasterList,name="ItemMasterList"),
    
    # path("UpdateItemMasterData/",views.UpdateItemMasterData,name="UpdateItemMasterData"),
    
    
]