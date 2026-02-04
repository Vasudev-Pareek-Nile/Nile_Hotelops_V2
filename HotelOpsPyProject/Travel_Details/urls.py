from django.urls import path,include
from .views import *
from .models import *
from rest_framework.routers import DefaultRouter
from .views import TravelRequestViewSet, TravelEntryViewSet

router = DefaultRouter()
router.register(r'travel-requests', TravelRequestViewSet)
router.register(r'travel-entries', TravelEntryViewSet)

urlpatterns = [
    path("Create_Travel_Request/", create_travel_request, name="Create_Travel_Request"),

    path("Delete_Travel_Request/", Delete_Travel_Request, name="Delete_Travel_Request"),
    path("Delete_Travel_Single_Entry/", Delete_Travel_Single_Entry, name="Delete_Travel_Single_Entry"),

    path("Travel_Details_List/", Travel_Details_List, name="Travel_Details_List"),
    path("Travel_Details_Data_PDF/", Travel_Details_Data_PDF, name="Travel_Details_Data_PDF"),

    path('api/', include(router.urls)),
]
