from django.urls import path,include
from .views import *
from .models import *
from .Mobile_Api import *

urlpatterns = [
    path("",GuestVoice_Dashboard,name="GuestVoice_Dashboard"),

    # Add Data --->
    path("Medallia_Add_Data/", Medallia_Add_Data, name="Medallia_Add_Data"),
    path("Medallia_Data_List/", Medallia_Data_List, name="Medallia_Data_List"),

    path("ReviewPro_Add_Data/", ReviewPro_Add_Data, name="ReviewPro_Add_Data"),
    path("ReviewPro_Data_List/", ReviewPro_Data_List, name="ReviewPro_Data_List"),

    path("landing_page/", landing_page, name="landing_page"),

    # File_Upload -- ReviewPro
    path("bulk_upload_reviews/", bulk_upload_reviews, name="bulk_upload_reviews"),
    path("bulk_upload_medallia/", bulk_upload_medallia, name="bulk_upload_medallia"),


    # new api url ------
    # path('api/Review_Medallia_Average_API/', Review_Medallia_Average_API_View.as_view(), name='Review_Medallia_Average_API'),
    path("api/medallia-data/", MedalliaDataByDateAPIView.as_view(), name="medallia-data-api"),
    path("api/ReviewPro-data/", ReviewProDataByDateAPIView.as_view(), name="ReviewPro-data-api"),

    # Trial Api
    path("api/Review_Medallia_Average_Mobile_API/", Review_Medallia_Average_Mobile_API.as_view(), name="Review_Medallia_Average_Mobile_API"),
    # path("api/Review_Medallia_Average_API_View_Trial_Second/", Review_Medallia_Average_API_View_Trial_Second.as_view(), name="Review_Medallia_Average_API_View_Trial_Second"),

    # New And Working Api
    # path("api/ReviewPro-Revised-data/", ReviewPro_Data_ByDate_APIView_Mobile.as_view(), name="ReviewPro-Revised-data"),
    # path("api/Medallia-Revised-data/", Medallia_Data_ByDate_APIView_Mobile.as_view(), name="Medallia-Revised-data"),
    path("api/ReviewPro_Entire_Data/", ReviewPro_Entire_Data.as_view(), name="ReviewPro_Entire_Data"),
    path("api/Guest_Reviews_ReviewPro/", Guest_Reviews_ReviewPro.as_view(), name="Guest_Reviews_ReviewPro"),

    # Medallia In Parts 
    path("api/Medallia_Core_Metrics-data/", Medallia_Core_Metrics.as_view(), name="Medallia_Core_Metrics-data"),
    path("api/Medallia_Housekeeping_Engineering_data/", Medallia_Housekeeping_Engineering.as_view(), name="Medallia_Housekeeping_Engineering_data"),
    path("api/Medallia_Front_Office/", Medallia_Front_Office.as_view(), name="Medallia_Front_Office"),
    path("api/Medallia_Food_And_Beverage/", Medallia_Food_And_Beverage.as_view(), name="Medallia_Food_And_Beverage"),
    path("api/Medallia_Customer_Other_Services/", Medallia_Customer_Other_Services.as_view(), name="Medallia_Customer_Other_Services"),
    path("api/Medallia_Customer_Service_And_Experience_Drivers/", Medallia_Customer_Service_And_Experience_Drivers.as_view(), name="Medallia_Customer_Service_And_Experience_Drivers"),
    path("api/Guest_Comment_Medallia_Mobile_Api/", Guest_Comment_Medallia_Mobile_Api.as_view(), name="Guest_Comment_Medallia_Mobile_Api"),
    path("api/Medallia_Top_Issues/", Medallia_Top_Issues.as_view(), name="Medallia_Top_Issues"),

    # path('api/feedback/', CombinedReviewDataByDateAPIView.as_view(), name='combined-feedback'),
    # path("entry-details/", EntryDetailsByOrganizationAPIView.as_view(), name="entry-details-api"),
    # path('api/feedback/', CombinedFeedbackAPIView.as_view(), name='combined-feedback'),
]
