from django.urls import path
from .import views

urlpatterns = [
    path('', views.home_view, name=''),

    path('UniformInventorySheet', views.UniformInventorySheet,
         name='UniformInventorySheet'),

    path("UniformInventoryList/", views.UniformInventoryList,
         name="UniformInventoryList"),

    path("UniformInventoryEditList/", views.UniformInventoryEditList,
         name="UniformInventoryEditList"),

    path("UpdateUniformInventorylist/", views.UpdateUniformInventorylist,
         name="UpdateUniformInventorylist"),

    path("DeleteUniformInventory/", views.DeleteUniformInventory,
         name="DeleteUniformInventory"),

    path("UniformInventory_pdf_view/", views.UniformInventory_pdf_view,
         name="UniformInventory_pdf_view"),

    path("UniformItemMasterlist/", views.UniformItemMasterlist,
         name="UniformItemMasterlist"),
    path("UniformItemMasterNew/", views.UniformItemMasterNew,
         name="UniformItemMasterNew"),
    path("DeleteUniformItemMaster/", views.DeleteUniformItemMaster,
         name="DeleteUniformItemMaster"),



]
