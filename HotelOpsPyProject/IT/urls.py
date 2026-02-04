from django.urls import path
from .views import ITRequest,DeleteIT,ItManagerList,HrRequest,ItHodApprovalListApi,ITHodApprovalApi, IT_Return_Request, IT_Return_Request_API


urlpatterns = [
    

   
    path('ItManagerList/',ItManagerList,name='ItManagerList'),
    path('ITRequest/',ITRequest,name='ITRequest'),
    path('HrRequest/',HrRequest,name='HrRequest'),

    path('DeleteIT/',DeleteIT,name='DeleteIT'),
    
    path('ItHodApprovalListApi/',ItHodApprovalListApi,name='ItHodApprovalListApi'),
    
    path('ITHodApprovalApi/',ITHodApprovalApi,name='ITHodApprovalApi'),


    # New Urls
    # path('ITRequest_ViewOnly/',ITRequest_ViewOnly,name='ITRequest_ViewOnly'),
    path('IT_Return_Request/',IT_Return_Request,name='IT_Return_Request'),
    # path('IT_Return_Request_From/',IT_Return_Request_From_View,name='IT_Return_Request_From'),
    path("IT/return/api/",IT_Return_Request_API,name='IT_Return_Request_API'),
]
