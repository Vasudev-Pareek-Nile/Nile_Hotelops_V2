from django.urls import path
from .import views
from .utils import get_organization_it_emails
urlpatterns = [
     
         path('Inventory_Add/',views.Inventory_Add,name="Inventory_Add"),
         path('Inventory_list/',views.Inventory_list,name="Inventory_list"),
         path('Inventory_delete/',views.Inventory_delete,name="Inventory_delete"),

        #master urls
        path('Type_category/',views.Type_category,name="Type_category"),
        path('Type_category_list/',views.Type_category_list,name="Type_category_list"),
        path('categorys_delete/',views.categorys_delete,name="categorys_delete"),


        path('Master_company_add/',views.Master_company_add,name="Master_company_add"),
        path('Master_company_list/',views.Master_company_list,name="Master_company_list"),
        path('company_delete/',views.company_delete,name="company_delete"),


        path('Master_Area_add/',views.Master_Area_add,name="Master_Area_add"),
        path('Master_Area_list/',views.Master_Area_list,name="Master_Area_list"),
        path('area_delete/',views.area_delete,name="area_delete"),

        path('Master_software_type/',views.Master_software_type,name="Master_software_type"),
        path('Master_software_type_list/',views.Master_software_type_list,name="Master_software_type_list"),
        path('sftware_delete/',views.sftware_delete,name="sftware_delete"),


        path('Qr_details/', views.Qr_details, name='Qr_details'),


        path('inventory_report/', views.inventory_report, name='inventory_report'),


        
        # New Urls --->
        path('Software_List/',views.Software_List,name="Software_List"),
        path('Hardware_List/',views.Hardware_List,name="Hardware_List"),
        path('IT_Inventory_Data_PDF/',views.IT_Inventory_Data_PDF, name="IT_Inventory_Data_PDF"),
        
        path('api/get_organization_it_emails/',get_organization_it_emails, name="IT_Inventory_Data_PDF"),
]