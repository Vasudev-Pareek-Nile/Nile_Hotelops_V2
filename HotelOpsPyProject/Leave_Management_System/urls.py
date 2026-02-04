from django.urls import path,include
# from .views import CompOffApprove_Leave,CompOfffApproval_list,CompOffClaim_Status,Employee_Dashboard,Hr_Dashboard,Leave_Application_view,Leave_Type_Add,Leave_Config_Add,Leave_Type_List,Leave_Type_Delete,Leave_Config_Delete,Leave_Config_List,Approval_list,Approve_Leave,Leave_Status,Employee_Leave_Balance,Employee_Leave_Balance_view,all_leaves,all_leaves_ceo,CEO_Dashboard,all_leaves_hr,Leave__Appication_Cancel,National_Holidays_List,National_Holidays_Delete,National_Holidays_ADD,Optional_Holidays_List,Optional_Holidays_Delete,Optional_Holidays_ADD,CombinedLeaveInfo,RejectLeave,HolidayList,RevokeLeave,Leave_Process,LeaveProcessDetails,CEO_Dashboard_Iframe,Employee_Leave_Apply,Employee_Leave_Application_view,Employee_Leave_Status,CompOffRequest_view,delete_leave_process
from .views import *

from rest_framework import routers
from .views import LeaveType,LeaveBalance,LeaveApply,Apporval
from .Leave_Api import Employee_Data_API, Leave_Config_Details_Api, Leave_Monthly_Carry_Forward_View_Api,employee_leave_balance_api
from .Leave_Monthly import *
from .Attendance_Pages import *
from .ReportsApi import *
from .Mobile_Api import *

urlpatterns = [
    # path("EmployeeDetails/",EmployeeDetails,name="EmployeeDetails"),


    # Employee_Dashboard 
    path("",Employee_Dashboard,name="Employee_Dashboard"),

    path("Employee_Dashboard/",Employee_Dashboard,name="Employee_Dashboard"),

    # path("Employee_Dashboard_Data_Passing/", Employee_Dashboard_Data_Passing ,name="Employee_Dashboard_Data_Passing"),
    # path("all_leaves/",all_leaves,name="all_leaves"),
    # path("all_leavesData/",all_leavesDate,name="all_leavesData"),
    
    # path('download-leave-status-pdf/', download_leave_status_pdf, name='download_leave_status_pdf'),

    # Leave Status ----->
    path("Leave_Status/", Leave_Status, name="Leave_Status"),
    path('download-leave-status-pdf/', download_leave_status_pdf, name='download_leave_status_pdf'),

    # Master - Leave - Management - system ---->
    path("Master_Leave_Status/", Master_Leave_Status, name="Master_Leave_Status"),
    path('Master_download_leave_status_pdf/', Master_download_leave_status_pdf, name='Master_download_leave_status_pdf'),

    # Master - Report - Management -----> 
    path("Master_AR_Reports/", Master_AR_Reports, name="Master_AR_Reports"),
    path('Master_AR_Report_Pdf_download/', Master_AR_Report_Pdf_download, name='Master_AR_Report_Pdf_download'),

    # CEO Dashboard
    
    path("CEO_Dashboard/",CEO_Dashboard,name="CEO_Dashboard"),
    
    path("CEO_Dashboard_Iframe/",CEO_Dashboard_Iframe,name="CEO_Dashboard_Iframe"),

    path("all_leaves_ceo/",all_leaves_ceo,name="all_leaves_ceo"),

    # Hr Dashboard
    path("Hr_Dashboard/",Hr_Dashboard,name="Hr_Dashboard"),
    path("all_leaves_hr/",all_leaves_hr,name="all_leaves_hr"),

    
    # Leave_Application
    path("Leave_Application/",Leave_Application_view,name="Leave_Application"),
    path("CompOffRequest/",CompOffRequest_view,name="CompOffRequest"),
    path("CompOffClaim_Status/",CompOffClaim_Status,name="CompOffClaim_Status"),
    path("CompOfffApproval_list/",CompOfffApproval_list,name="CompOfffApproval_list"),
    path("CompOffApprove_Leave/",CompOffApprove_Leave,name="CompOffApprove_Leave"),
  
 
    
   path("CombinedLeaveInfo/",CombinedLeaveInfo,name="CombinedLeaveInfo"),

    path("Leave__Appication_Cancel/ID=<int:id>",Leave__Appication_Cancel,name="Leave__Appication_Cancel"),
    
    # Leave Type Master
    path("Leave_Type_Add/",Leave_Type_Add,name="Leave_Type_Add"),
    path("Leave_Type_List/",Leave_Type_List,name="Leave_Type_List"),        
    path("Leave_Type_Delete/ID=<int:id>",Leave_Type_Delete,name="Leave_Type_Delete"),        
    # Leave Confif Details
    path("Leave_Config_List/ID=<int:id>",Leave_Config_List,name="Leave_Config_List"),  
    path("Leave_Config_Add/",Leave_Config_Add,name="Leave_Config_Add"),
    path("Leave_Config_Delete/ID=<int:id>",Leave_Config_Delete,name="Leave_Config_Delete"),    

    # Leave Process
    path("Leave_Process/",Leave_Process,name="Leave_Process"), 
    path("LeaveProcessDetails/",LeaveProcessDetails,name="LeaveProcessDetails"), 
    path('leave-process/delete/<int:id>/', delete_leave_process, name='delete_leave_process'),

    path("Approval_list/",Approval_list,name="Approval_list"),
    path("Approve_Leave/",Approve_Leave,name="Approve_Leave"),
    path("RejectLeave/",RejectLeave,name="RejectLeave"),
    
    path("RevokeLeave/",RevokeLeave,name="RevokeLeave"),




    # Leave Balace
    path("Employee_Leave_Balance/",Employee_Leave_Balance,name="Employee_Leave_Balance"),
    path("Employee_Leave_Apply/",Employee_Leave_Apply,name="Employee_Leave_Apply"),
    
    path("Employee_Leave_Status/",Employee_Leave_Status,name="Employee_Leave_Status"),

    
    path("Employee_Leave_Application_view/",Employee_Leave_Application_view,name="Employee_Leave_Application_view"),


    path("Employee_Leave_Balance_view/",Employee_Leave_Balance_view,name="Employee_Leave_Balance_view"),
    

    # National_Holidays

    path("National_Holidays_ADD/",National_Holidays_ADD,name="National_Holidays_ADD"),
    path("National_Holidays_List/",National_Holidays_List,name="National_Holidays_List"),
    path("National_Holidays_Delete/",National_Holidays_Delete,name="National_Holidays_Delete"),

    # Optional Holidays
    path("Optional_Holidays_ADD/",Optional_Holidays_ADD,name="Optional_Holidays_ADD"),
    path("Optional_Holidays_List/",Optional_Holidays_List,name="Optional_Holidays_List"),
    path("Optional_Holidays_Delete/",Optional_Holidays_Delete,name="Optional_Holidays_Delete"),
    
    # State Holidays
    path("State_Holidays_ADD/",State_Holidays_ADD,name="State_Holidays_ADD"),
    path("State_Holidays_List/",State_Holidays_List,name="State_Holidays_List"),
    path("State_Holidays_Delete/",State_Holidays_Delete,name="State_Holidays_Delete"),

   
    path("HolidayList/",HolidayList,name="HolidayList"),

    # Hr Manager List 
    
    # path("HR_Manager_List/",HR_Manager_List,name="HR_Manager_List"),

    path('LeaveType/', LeaveType.as_view(), name='LeaveType'),
    path('LeaveBalance/', LeaveBalance.as_view(), name='LeaveBalance'),
    path('LeaveApply/', LeaveApply.as_view(), name='LeaveApply'),
    path('Apporval/', Apporval.as_view(), name='Apporval'),


    path("leave-report/", employee_leave_report, name="leave-report"),

    # Monthly Leave Process
    path("Monthly_Leave_Process/",Leave_Monthly_Carry_Forward_View,name="Monthly_Leave_Process"), 
    path("Monthly_Leave_Process_Details/",Leave_Monthly_Process_Details_View,name="Monthly_Leave_Process_Details"), 
    path('Monthly_Leave_Process/delete/<int:id>/', Delete_Monthly_Leave_Process, name='Monthly_Leave_Process'),
    path('api/employee-data/', Employee_Data_API.as_view(), name='employee-data-api'),
    path('api/Leave_Config_Details_Api/', Leave_Config_Details_Api, name='Leave_Config_Details_Api'),



    # Attendance_pages
    path('View_Attendance_Leave/', View_Attendance_Leave_View, name='View_Attendance_Leave'),
    path('Week_Off/', Week_Off_view, name='Week_Off'), 
    path('AttendaceMonthlyReport_Leave/', AttendaceMonthlyReport_Leave, name='AttendaceMonthlyReport_Leave'),
    path('AttendanceProcess/', AttendanceProcess, name='AttendanceProcess'),
    path('Daily_Attendace_Leave/', Daily_Attendace_Leave_View, name='Daily_Attendace_Leave'),   
    path('Update_Attendance_HR/', Update_Attendance_HR, name='Update_Attendance_HR'),
    path("Reports/Monthly_Attendence_Report_Leave_Pdf_View/", Monthly_Attendence_Report_Leave_Pdf_View, name="Monthly_Attendence_Report_Leave_Pdf_View"),

       
    # path('Upload_Attendace/', Upload_Attendace, name='Upload_Attendace'),
    path('Excel_Attendance_Upload/', Excel_Attendance_Upload_View, name='Excel_Attendance_Upload'),
    path('Excel_Attendance_Upload_CSV/', Excel_Attendance_Upload_CSV_Api, name='Excel_Attendance_Upload_CSV'),
    
    
    # Mobile Api
    path('api/Employee_Dashboard_Leave_API/', Employee_Dashboard_Leave_API, name='Employee_Dashboard_Leave_API'),
    path('api/Leave_Monthly_Carry_Forward_View_Api/', Leave_Monthly_Carry_Forward_View_Api, name='Leave_Monthly_Carry_Forward_View_Api'),
    path('api/employee_leave_balance_api/', employee_leave_balance_api, name='employee_leave_balance_api'),
    # path('api/process_previous_month_weekoff/', get_previous_month_weekoff_compoff, name='process_previous_month_weekoff'),
]
