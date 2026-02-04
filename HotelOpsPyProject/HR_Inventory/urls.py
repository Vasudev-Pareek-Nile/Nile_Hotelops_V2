from django.urls import path
from .views import HR_Inventory_Request,HR_Inventory_Return_Request
urlpatterns = [
    path('HR_Inventory_Request/',HR_Inventory_Request,name="HR_Inventory_Request"),
    path('HR_Inventory_Return_Request/',HR_Inventory_Return_Request,name="HR_Inventory_Return_Request"),
    
    # path('housekeeping_returns_pdf_api/',housekeeping_returns_pdf_api,name="housekeeping_returns_pdf_api"),
]
