from django.urls import path
from .views2 import *






urlpatterns = [
    # path("Master_EmployeeDetails/", Master_EmployeeDetails, name="Master_EmployeeDetails"),

    # Employee_Dashboard 
    path("",Master_Employee_Dashboard,name="Master_Employee_Dashboard"),
    path("Master_Employee_Dashboard/",Master_Employee_Dashboard,name="Master_Employee_Dashboard"),
    path("Master_all_leaves/",Master_all_leaves,name="Master_all_leaves"),
    path("Master_all_leavesDate/",Master_all_leavesDate,name="Master_all_leavesDate"),
    
    path('Master_download-leave-status-pdf/', Master_download_leave_status_pdf, name='Master_download_leave_status_pdf'),


    # CEO Dashboard
    path("Master_CEO_Dashboard/", Master_CEO_Dashboard, name="Master_CEO_Dashboard"),
    path("Master_CEO_Dashboard_Iframe/", Master_CEO_Dashboard_Iframe, name="Master_CEO_Dashboard_Iframe"),
    path("Master_all_leaves_ceo/", Master_all_leaves_ceo, name="Master_all_leaves_ceo"),

    # Hr Dashboard
    path("Master_Hr_Dashboard/", Master_Hr_Dashboard, name="Master_Hr_Dashboard"),
    path("Master_all_leaves_hr/", Master_all_leaves_hr, name="Master_all_leaves_hr"),

    
    # Leave_Application
    path("Master_Leave_Application/", Master_Leave_Application_view, name="Master_Leave_Application"),
    path("Master_CompOffRequest/", Master_CompOffRequest_view, name="Master_CompOffRequest"),
    path("Master_CompOffClaim_Status/", Master_CompOffClaim_Status,name="Master_CompOffClaim_Status"),
    path("Master_CompOfffApproval_list/", Master_CompOfffApproval_list, name="Master_CompOfffApproval_list"),
    path("Master_CompOffApprove_Leave/", Master_CompOffApprove_Leave, name="Master_CompOffApprove_Leave"),
  
 
    
    path("Master_ombinedLeaveInfo/", Master_CombinedLeaveInfo, name="Master_CombinedLeaveInfo"),
    path("Master_Leave__Appication_Cancel/ID=<int:id>", Master_Leave__Appication_Cancel, name="Master_Leave__Appication_Cancel"),
    
    # Leave Type Master
    path("Master_Leave_Type_Add/", Master_Leave_Type_Add, name="Master_Leave_Type_Add"),
    path("Master_Leave_Type_List/", Master_Leave_Type_List, name="Master_Leave_Type_List"),        
    path("Master_Leave_Type_Delete/ID=<int:id>", Master_Leave_Type_Delete, name="Master_Leave_Type_Delete"),
             
    # Leave Confif Details
    path("Master_Leave_Config_List/ID=<int:id>", Master_Leave_Config_List, name="Master_Leave_Config_List"),  
    path("Master_Leave_Config_Add/", Master_Leave_Config_Add, name="Master_Leave_Config_Add"),
    path("Master_Leave_Config_Delete/ID=<int:id>", Master_Leave_Config_Delete, name="Master_Leave_Config_Delete"),    

    # Leave Process
    path("Master_Leave_Process/", Master_Leave_Process,name="Master_Leave_Process"), 
    path("Master_LeaveProcessDetails/", Master_LeaveProcessDetails,name="Master_LeaveProcessDetails"), 
    
    
    path("Master_Approval_list/", Master_Approval_list, name="Master_Approval_list"),
    path("Master_Approve_Leave/", Master_Approve_Leave, name="Master_Approve_Leave"),
    path("Master_RejectLeave/", Master_RejectLeave, name="Master_RejectLeave"),
    
    path("Master_RevokeLeave/", Master_RevokeLeave, name="Master_RevokeLeave"),


    path("Master_Leave_Status/", Master_Leave_Status, name="Master_Leave_Status"),

    # Leave Balace
    path("Master_Employee_Leave_Balance/", Master_Employee_Leave_Balance, name="Master_Employee_Leave_Balance"),
    path("Master_Employee_Leave_Apply/", Master_Employee_Leave_Apply, name="Master_Employee_Leave_Apply"),
    
    path("Master_Employee_Leave_Status/", Master_Employee_Leave_Status, name="Master_Employee_Leave_Status"),

    
    path("Master_Employee_Leave_Application_view/", Master_Employee_Leave_Application_view, name="Master_Employee_Leave_Application_view"),


    path("Master_Employee_Leave_Balance_view/", Master_Employee_Leave_Balance_view, name="Master_Employee_Leave_Balance_view"),
    

    # National_Holidays
    
    path("Master_National_Holidays_ADD/", Master_National_Holidays_ADD, name="Master_National_Holidays_ADD"),
    path("Master_National_Holidays_List/", Master_National_Holidays_List, Master_name="Master_National_Holidays_List"),
    path("Master_National_Holidays_Delete/", Master_National_Holidays_Delete, Master_name="Master_National_Holidays_Delete"),

    # Optional Holidays
    path("Master_Optional_Holidays_ADD/", Master_Optional_Holidays_ADD,name="Master_Optional_Holidays_ADD"),
    path("Master_Optional_Holidays_List/", Master_Optional_Holidays_List,name="Master_Optional_Holidays_List"),
    path("Master_Optional_Holidays_Delete/", Master_Optional_Holidays_Delete,name="Master_Optional_Holidays_Delete"),

   
    path("Master_HolidayList/", Master_HolidayList, name="Master_HolidayList"),

    # Hr Manager List 
    
    # path("Master_HR_Manager_List/", Master_HR_Manager_List, name="Master_HR_Manager_List"),

    path('Master_LeaveType/', Master_LeaveType.as_view(),  name='Master_LeaveType'),
    path('Master_LeaveBalance/', Master_LeaveBalance.as_view(),  name='Master_LeaveBalance'),
    path('Master_LeaveApply/', Master_LeaveApply.as_view(),  name='Master_LeaveApply'),
    path('Master_Apporval/', Master_Apporval.as_view(),  name='Master_Apporval'),

    path("Master_leave-report/", Master_employee_leave_report, name="Master_leave-report"),

]
