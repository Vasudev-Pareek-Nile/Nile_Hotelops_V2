from django.urls import path
from .import views
from .views import Objective_Master_List,Objective_Master_Add,Objective_Master_Delete,Attribute_Master_List,Attribute_Master_Add,Attribute_Master_Delete,Ineffective_Indicators_List,Ineffective_Indicators_Delete,Ineffective_Indicators_Add,Effective_Indicators_List,Effective_Indicators_Add,Effective_Indicators_Delete,PADP_View,List_PADP,PADP_Delete,Aprroval_PADP,Apporve_Padp_View,CEO_Approval_List,Hr_PADP_View_List,PADPERDC,PADPApprove,Padpceoapprove,Makecopy,Effective_Indicators_Bulk_Delete,Ineffective_Indicators_Bulk_Delete, Refresh_Salary_Data_PADP, Refresh_Salary_Data_Master
from .Papd import PADP_Add, Refresh_MangerLevel_View
from .Mobile_Api import *

urlpatterns = [
   # Objective_Master  
   path('',List_PADP,name="List_PADP"),
   #  
   path('Objective_Master_List/',Objective_Master_List,name="Objective_Master_List"), 
   path('Objective_Master_Add/',Objective_Master_Add,name="Objective_Master_Add"),
   path('Makecopy/',Makecopy,name="Makecopy"),

   path('Objective_Master_Delete/',Objective_Master_Delete,name="Objective_Master_Delete"),

   # Attribute_Master_List
   path('Attribute_Master_List/',Attribute_Master_List,name="Attribute_Master_List"), 
   path('Attribute_Master_Add/',Attribute_Master_Add,name="Attribute_Master_Add"), 
   path('Attribute_Master_Delete/',Attribute_Master_Delete,name="Attribute_Master_Delete"), 
   
   # Ineffective_Indicators
   path('Ineffective_Indicators_List/',Ineffective_Indicators_List,name="Ineffective_Indicators_List"),
   path('Ineffective_Indicators_Delete/',Ineffective_Indicators_Delete,name="Ineffective_Indicators_Delete"),
   
   path('Ineffective_Indicators_Bulk_Delete/',Ineffective_Indicators_Bulk_Delete,name="Ineffective_Indicators_Bulk_Delete"),

   path('Ineffective_Indicators_Add/',Ineffective_Indicators_Add,name="Ineffective_Indicators_Add"),
    
  # Effective_Indicators
  path('Effective_Indicators_List/',Effective_Indicators_List,name="Effective_Indicators_List"),
  path('Effective_Indicators_Add/',Effective_Indicators_Add,name="Effective_Indicators_Add"),
  path('Effective_Indicators_Delete/',Effective_Indicators_Delete,name="Effective_Indicators_Delete"), 
  path('Effective_Indicators_Bulk_Delete/',Effective_Indicators_Bulk_Delete,name="Effective_Indicators_Bulk_Delete"), 

  

  # PADP_Add

  # path('PADP_Add/',PADP_Add,name="PADP_Add"),
   path('PADP_Add/',PADP_Add,name="PADP_Add"),

  
  path('PADP_View/',PADP_View,name="PADP_View"),
  path('List_PADP/',List_PADP,name="List_PADP"),
  
  path('Aprroval_PADP/',Aprroval_PADP,name="Aprroval_PADP"),
  path('PADP_Delete/',PADP_Delete,name="PADP_Delete"),
  # Aprroval
  path('Apporve_Padp_View/',Apporve_Padp_View,name="Apporve_Padp_View"),
  # path('Approve_PADP/',Approve_PADP,name="Approve_PADP"),
  path('CEO_Approval_List/',CEO_Approval_List,name="CEO_Approval_List"),
  # Hr_PADP_View_List
  path('Hr_PADP_View_List/',Hr_PADP_View_List,name="Hr_PADP_View_List"),
  
  path('PADPERDC/',PADPERDC,name="PADPERDC"),
  
  path('PADPApprove/',PADPApprove,name="PADPApprove"),
  path('Padpceoapprove/',Padpceoapprove,name="Padpceoapprove"),






  # 
  path('PADPList/',views.PADPList,name="PADPList"),
  path('Userinfo/',views.Userinfo,name="Userinfo"),
  path('NewAPADP/',views.NewAPADP,name="NewAPADP"),
  path('apdpaDelete/',views.apdpaDelete,name="apdpaDelete"),
  path('ApadpPdf/',views.ApadpPdf,name="ApadpPdf"),
  # path('Padp_ceo_approve_api/',Padp_ceo_approve_api,name="Padp_ceo_approve_api"),    # New
  



  # path('Refresh/<int:apadp_id>/<int:EmpID>/<str:OID>/<str:EmpCode>/',views.Refresh_View, name="Refresh"),
  path('Refresh/<int:apadp_id>/', views.Refresh_View, name="Refresh"),


  # path('Refresh/<int:apadp_id>/', views.Refresh_View, name="Refresh"),
  # path('Refresh/<int:apadp_id>/', views.Refresh_View, name="Refresh"),
  path('Refresh_Manger_Level/<int:apadp_id>/', Refresh_MangerLevel_View, name="Refresh_Manger_Level"),
  # path('Refresh_Salary_Data_PADP/<int:apadp_id>/<int:EmpID>/str:OID>', Refresh_MangerLevel_View, name="Refresh_Manger_Level"),
  # path('Refresh_Salary_Data_PADP/<int:apadp_id>/<int:EmpID>/<str:OID>/<str:EmpCode>/',Refresh_Salary_Data_PADP,name="Refresh_Salary_Data_PADP"),
  path('Refresh_Salary_Data_PADP/<int:apadp_id>/',Refresh_Salary_Data_PADP,name="Refresh_Salary_Data_PADP"),
  path('Refresh_Salary_Data_Master/<int:Padpid>/',Refresh_Salary_Data_Master,name="Refresh_Salary_Data_Master"),
  # path('Refresh_Salary_Data_PADP/<int:apadp_id>/<str:OID>/<str:EmpCode>/',Refresh_Salary_Data_PADP,name="Refresh_Salary_Data_PADP"),
  # path('Refresh_Salary_Data_Master/<int:Padpid>/<int:OID>/<str:EmpCode>/',Refresh_Salary_Data_Master,name="Refresh_Salary_Data_Master"),
  
  
  # path('Refresh_Salary_Data_Master/<int:Padpid>/',Refresh_Salary_Data_Master,name="Refresh_Salary_Data_Master"),
  path("api/approve/", PADP_Approve_Mobile_API.as_view()),
  path('api/Padp_ceo_approve_api/',Padp_ceo_approve_api,name="Padp_ceo_approve_api"),
  path('api/PADP_View_Manager/',PADP_View_Manager,name="PADP_View_Manager"),

  path("api/Send_Notification/", Send_Notification_PADP_Approve_Mobile_API.as_view()),
  # path("api/get_organization_hr_email/", get_organization_hr_email, name="get_organization_hr_email"),
]
