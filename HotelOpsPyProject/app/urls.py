from django.urls import path
from .import views
from .views import UserSessionViewSet
from . import Global_Api
from . import Global_Mobile_Api as GmApi
user_session_detail = UserSessionViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    # path('',views.netlogredre,name=''),
    path('home_view/',views.home_view,name=''),
    path('',views.LoginPage,name='LoginPage'),
    path('logout/', views.logout_view, name='logout'),
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('netlogredre',views.netlogredre,name='netlogredre'),
    path('api/user-session/<str:user_id>/', user_session_detail, name='user-session-detail'),
     path('get_cached_data',views.get_cached_data,name='get_cached_data'),
    # path('organizationclick', views.organizationclick_view),
    
    # path('cakeorderclick', views.cakeorderclick_view),
    
    # path('cakeorder', views.cakeorder,name='cakeorder'),
    
    # path("showpage/",views.ShowPage,name="showpage"),
    
    # path("edit/",views.EditData,name="editpage"),
    
    # path("update/",views.UpdateData,name="update"),
    
    # path("delete/",views.Delete,name="delete"),
    
    # path("view/",views.ViewData,name="ViewData"),
  


  
    path('Show_Department_Api/', Global_Api.Show_Department_Api, name='Show_Department_Api'),
    path('Show_Division_Api/', Global_Api.Show_Division_Api, name='Show_Division_Api'),
    path('Show_Department_By_DivisionName_Api/', Global_Api.Show_Department_By_DivisionName_Api, name='Show_Department_By_DivisionName_Api'),
    path('Show_Department_By_DivisionName_Api/<str:DivisionName>/', Global_Api.Show_Department_By_DivisionName_Api, name='Show_Department_By_DivisionName_Api'),

    path('Show_Designations_Api/', Global_Api.Show_Designations_Api, name='Show_Designations_Api'),
    path('Show_Designations_Complete_Api/', Global_Api.Show_Designations_Complete_Api, name='Show_Designations_Complete_Api'),
    path('MonthList_Api/', Global_Api.MonthList_Api, name='MonthList_Api'),
    path('EmployeeStatusList_Api/', Global_Api.EmployeeStatusList_Api, name='EmployeeStatusList_Api'),
    path('Global_Api/Leave_Type_Data_Api/', Global_Api.Leave_Type_Data_Api, name='Leave_Type_Data_Api'),
    path('Global_Api/Leave_Type_Name_Api/', Global_Api.Leave_Type_Name_Api, name='Leave_Type_Name_Api'),
    # path('OrganizationList_Api/', Global_Api.OrganizationList_Api, name='OrganizationList_Api'),

    path('api/OrganizationList_Api/<str:OrganizationID>/', Global_Api.OrganizationList_Api, name='OrganizationList_Api'),
    path('api/OrganizationList_All_Mobile_Api/<str:OrganizationID>/', Global_Api.OrganizationList_All_Mobile_Api, name='OrganizationList_All_Mobile_Api'),

    path('Lavel_Show_Data_Api/', Global_Api.Lavel_Show_Data_Api, name='Lavel_Show_Data_Api'),
    
    path('api/New_Joiners_Api/', Global_Api.New_Joiners_Api, name='New_Joiners_Api'),
    path('api/Resignation_Mobile_Api/', Global_Api.Resignation_Mobile_Api, name='Resignation_Mobile_Api'),
    
    # path('api/Get_Employee_Master_Data_By_Code/', Global_Api.Resignation_Mobile_Api, name='Get_Employee_Master_Data_By_Code'),
    path('api/Get_Emp_Personal_Data_Mobile_Api/', GmApi.Get_Emp_Personal_Data_Mobile_Api, name='Get_Emp_Personal_Data_Mobile_Api'),
    path('api/Get_Emp_Bank_Info_Mobile_Api/', GmApi.Get_Emp_Bank_Info_Mobile_Api, name='Get_Emp_Bank_Info_Mobile_Api'),
    path('api/employee/Get_photo/<str:Code>/<int:OID>/', GmApi.get_employee_profile_photo, name='get_employee_profile_photo'),
    path('api/employee/Get_Documents/<str:Code>/<int:OID>/', GmApi.get_employee_Documents, name='get_employee_Documents'),
    path('api/employee/View_Documents/<int:document_id>/<str:DocType>/', GmApi.view_employee_document, name='view_employee_document'),
    

]
