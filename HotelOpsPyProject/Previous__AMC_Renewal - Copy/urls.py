from django.urls import path,include
from .views import *
from .models import *


# urlpatterns = [
#     path("", AMC_Renewal_Dashboard, name="AMC_Renewal_Dashboard"),
#     path('equipment-profile/<int:id>/', equipment_profile_view, name='equipment_profile'),
# ]


# urlpatterns = [
#     path("", AMC_Renewal_Dashboard, name="AMC_Renewal_Dashboard"),
#     path("dashboard/<int:id>/", AMC_Renewal_Dashboard, name="AMC_Renewal_Dashboard_With_ID"),  # Pass ID
#     path("equipment-profile/<int:id>/", equipment_profile_view, name="equipment_profile"),
# ]

urlpatterns = [
    path("dashboard/<int:id>/", AMC_Renewal_Dashboard, name="AMC_Renewal_Dashboard_With_ID"),    # craate page and function
    # path("dashboard/<int:id>/", AMC_Renewal_Dashboard, name="AMC_Renewal_Dashboard_With_ID"),
    path("equipment-profile/<int:id>/", equipment_profile_view, name="equipment_profile"),  # Api 

    # path("AMC_View_Data/", AMC_View_Data, name="AMC_View_Data"),
    path("AMC_View_Data/<int:id>/", AMC_View_Data, name="AMC_View_Data"),


    path("AMC_Data_List/", AMC_Data_List, name="AMC_Data_List"),
    path("AMC_List_equipment_view/", AMC_List_equipment_view, name="AMC_List_equipment_view"),
    path("AMC_List_Equipment_Mobile_Api/", AMC_List_Equipment_Mobile_Api, name="AMC_List_Equipment_Mobile_Api"),
    path("AMC_Pending_Count_Api/", AMC_Pending_Count_Api, name="AMC_Pending_Count_Api"),
    path("AMC_Details_equipment_Mobile_Api/", AMC_Details_equipment_Mobile_Api, name="AMC_Details_equipment_Mobile_Api"),
    path("AMC_Action_Mobile_Api/", AMC_Action_Mobile_Api, name="AMC_Action_Mobile_Api"),


    path("api/pending_status_counts_Demo_Three/", pending_status_counts_Demo_Three, name="pending_status_counts_Demo_Three"),

    path("api/pending_status_counts_Demo_Four/", pending_status_counts_Demo_Four, name="pending_status_counts_Demo_Four"),

    # Atteched Document
    path("AMC_Document_Mobile_Api/", AMC_Document_Mobile_Api, name="AMC_Document_Mobile_Api"),



    path("download_AMC_View_Data_pdf/<int:equipment_id>/", download_AMC_View_Data_pdf, name="download_AMC_View_Data_pdf"),
    path("download_AMC_View_Data_pdf_mobile_api/", download_AMC_View_Data_pdf_mobile_api, name="download_AMC_View_Data_pdf_mobile_api"),
    
    
    path("api/AMC_Entry_List_API_Edit/", AMC_Entry_List_API_Edit, name="AMC_Entry_List_API_Edit"),
    
    # path('All_equipment_List/', equipment_profile_list_view, name='All_equipment_List'),
    # path("AMC_Renewal/create/", create_amc_entry, name="create_amc_entry"),
    # path("AMC_Renewal/update-status/<int:id>/", update_status, name="update_status"),
]
