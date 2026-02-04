from django.urls import path
from .views import UniformHrRequest,ManagerList,UniformDelete,HouseKeepingRequest,HouseKeepingReturnRequest,UniformHodApprovalApi,UniformHodApprovalListApi, housekeeping_returns_pdf_api
urlpatterns = [
    path('UniformHrRequest/',UniformHrRequest,name="UniformHrRequest"),
    path('ManagerList/',ManagerList,name="ManagerList"),
    path('UniformDelete/',UniformDelete,name="UniformDelete"),
    path('HouseKeepingRequest/',HouseKeepingRequest,name="HouseKeepingRequest"),
    path('HouseKeepingReturnRequest/',HouseKeepingReturnRequest,name="HouseKeepingReturnRequest"),
    path('UniformHodApprovalApi/',UniformHodApprovalApi,name="UniformHodApprovalApi"),
    path('UniformHodApprovalListApi/',UniformHodApprovalListApi,name="UniformHodApprovalListApi"),
    
    
    path('housekeeping_returns_pdf_api/',housekeeping_returns_pdf_api,name="housekeeping_returns_pdf_api"),
]
