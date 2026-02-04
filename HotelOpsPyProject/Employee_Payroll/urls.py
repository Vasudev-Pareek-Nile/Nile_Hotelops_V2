from django.urls import path
# from .views import Payroll_List,Alifupload_csv,View_Attendance,View_Emmployee_Salary_Details,Generate_Salary_Slip,Update_Attendance,UpdateRequest,UpdateRequestlist,UpdateRequestlist_HR,Employees_Payroll_List,Upload_Attendace,Update_Attendance_HR,Daily_Attendace,Upload_Attendance_List,AttendanceProcess,OrgConfigList,AddConfig,index,all_events,ConfigDelete,SalaryList,DumpAttendace,SalarySendEmails,update_verification,AttendaceMonthlyReport,AttendanceLockView,UpdateStatus,add_event,remove,download_weekoff,upload_weekoff,ShfitList,UpdateShift,IntialShfitCreate,AttendaceCorrectEtmExlUp,UploadAttendanceSalaryFile,download_file,AttendanceSalaryList,attendance_report,UnlockAttendanceLock
# ,GenerateWeekoff
from .views import *
from .MoveToPayroll_View import *
from .ReportsApi import *
# from .views import SalarySlipV1ListAPIView, SalarySlipV1DetailAPIVie
from .serializers_Api import SalarySlipV1ListAPIView, SalarySlipV1DetailAPIView

urlpatterns = [
    
    # path('newhomebase/', newhomebase, name='newhomebase'),

    path('Alifupload_csv/', Alifupload_csv, name='Alifupload_csv'),
    path('View_Attendance/', View_Attendance, name='View_Attendance'),
    path('', View_Attendance, name='View_Attendance'),                  # usable
    path('AttendaceCorrectEtmExlUp/', AttendaceCorrectEtmExlUp, name='AttendaceCorrectEtmExlUp'),
    path('UploadAttendanceSalaryFile/', UploadAttendanceSalaryFile, name='UploadAttendanceSalaryFile'),
    path('download_file/', download_file, name='download_file'),
    path('AttendanceSalaryList/', AttendanceSalaryList, name='AttendanceSalaryList'),


    
    
    # path('ReadAttendanceFromAzure/', ReadAttendanceFromAzure, name='ReadAttendanceFromAzure'),

    
    # path('get_leave_application/', get_leave_application, name='get_leave_application'),
    # path('GetAttendance/', GetAttendance, name='GetAttendance'),


    path('Payroll_List/',Payroll_List,name = "Payroll_List"),
    path('View_Emmployee_Salary_Details/', View_Emmployee_Salary_Details, name='View_Emmployee_Salary_Details'),
    # path('Generate_Salary_Slip/', Generate_Salary_Slip, name='Generate_Salary_Slip'),
    path('Update_Attendance/', Update_Attendance, name='Update_Attendance'),
    # path('Update_Attendance_HR/', Update_Attendance_HR, name='Update_Attendance_HR'),
    path('UpdateRequest/', UpdateRequest, name='UpdateRequest'),
    path('UpdateRequestlist/', UpdateRequestlist, name='UpdateRequestlist'),
    path('UpdateRequestlist_HR/', UpdateRequestlist_HR, name='UpdateRequestlist_HR'),               # useful link
    path('Employees_Payroll_List/', Employees_Payroll_List, name='Employees_Payroll_List'),
    path('UnlockAttendanceLock/', UnlockAttendanceLock, name='UnlockAttendanceLock'),
    
    
    path('Upload_Attendace/', Upload_Attendace, name='Upload_Attendace'),
    path('AttendaceMonthlyReport/', AttendaceMonthlyReport, name='AttendaceMonthlyReport'),
    
    path('Daily_Attendace/', Daily_Attendace, name='Daily_Attendace'),                      # useful link
    path('AttendanceLockView/', AttendanceLockView, name='AttendanceLockView'),
    # path('GenerateWeekoff/', GenerateWeekoff, name='GenerateWeekoff'),



    path('UpdateStatus/', UpdateStatus, name='UpdateStatus'),

    
    path('Upload_Attendance_List/', Upload_Attendance_List, name='Upload_Attendance_List'),

    path('SalaryList/', SalaryList, name='SalaryList'),
    path('update_verification/', update_verification, name='update_verification'),

    


    # Usable Links
    # path('AttendanceProcess/', AttendanceProcess, name='AttendanceProcess'),
    
    path('DumpAttendace/', DumpAttendace, name='DumpAttendace'),


    #  OrgConfig
    path('OrgConfigList/', OrgConfigList, name='OrgConfigList'),
    path('AddConfig/', AddConfig, name='AddConfig'),
    path('ConfigDelete/', ConfigDelete, name='ConfigDelete'),

    


    # Weekoff Mapping 
    # path('index', index, name='index'), 
    path('all_events/', all_events, name='all_events'), 
    path('add_event/', add_event, name='add_event'), 
    path('remove/', remove, name='remove'),
    path('download_weekoff/', download_weekoff, name='download_weekoff'),
    path('upload_weekoff/', upload_weekoff, name='upload_weekoff'),


    # shfit 
    
    path('ShfitList/', ShfitList, name='ShfitList'),
    path('IntialShfitCreate/', IntialShfitCreate, name='IntialShfitCreate'),
    path('UpdateShift/', UpdateShift, name='UpdateShift'),


    path('attendance-report/', attendance_report, name='attendance_report'),
 

    # SendEmails    
    path('SalarySendEmails/', SalarySendEmails, name='SalarySendEmails'),


    # New Urls
    path('Salary_List_Pdf/', Salary_List_Pdf, name='Salary_List_Pdf'),
    # path('Unlock_Employee_Salary_Details/', Unlock_Employee_Salary_Details, name='Unlock_Employee_Salary_Details'),
    path('Unlock_Employee_Salary_Details/<int:slip_id>', Unlock_Employee_Salary_Details, name='Unlock_Employee_Salary_Details'),


    path("api/upload-csv/", AlifUploadCSVApi.as_view(), name="alif-upload-csv"),

    # old Generate Salary Slip
    path('Generate_Salary_Slip/', Generate_Salary_Slip, name='Generate_Salary_Slip'),

    # Dummy unused Salary APIs
    # Recalculate Salary Dummy 
    path('salary/recalculate/', recalc_salary, name='recalc_salary'),
    path('salary/SalaryFormData/', recalc_salary, name='SalaryFormData'),
    # Salary Slip -- Dummy 
    path('api/salary-slips/', SalarySlipV1ListAPIView.as_view(), name='salary-slip-list'),
    path('api/salary-slips/<int:pk>/', SalarySlipV1DetailAPIView.as_view(), name='salary-slip-detail'),
    path('download/Salary-Slip-Pdf-Download/', Salary_Slip_Pdf_Download, name='Salary_Slip_Pdf_Download'),              # Page Render
    


    # Move to Payroll View
    path('MoveToPayroll/', MoveToPayroll_View, name='MoveToPayroll'),     # Page Render
    path('start-move-to-payroll/', start_move_to_payroll, name='start_move_to_payroll'),   # Ajax Entry Point to move to payroll
    path('payroll_progress/<str:task_id>/', payroll_progress, name='payroll_progress'),     # To check progress of move to payroll task


    # Attendence lock
    path('Attendance-Lock-Payroll/', Attendance_Lock_Payroll_View, name='Attendance_Lock_Payroll'),              # Page Render
    path("api/Employees_Payroll_List_API/", Employees_Payroll_List_API, name="Employees_Payroll_List_API"),      # Employee List API for Lock Attendance
    path('api/Attendance_Lock_View_Get_Api/', Attendance_Lock_View_Get_Api, name='Attendance_Lock_View_Get_Api'), # Attendance Locked data View API
    path('api/Attendance_Lock_Post_API/', Attendance_Lock_Post_API, name='Attendance_Lock_Post_API'),             # Attendance Lock Post API
    path("api/Attendance_UnLock_Post_API/", Attendance_UnLock_Post_API, name="Attendance_UnLock_Post_API"),        # Attendance UnLock Post API
    path("api/Bulk_Lock_Attendence/", Bulk_Lock_Attendence, name="Bulk_Lock_Attendence"),                          # Bulk Lock Attendence API


    # Generate Salary Process Daily Earning
    path('Generte-Salary-View/', Generte_Salary_View, name='Generte_Salary_View'),             # Page Render 
    path("api/process_daily_earning/", process_daily_earning, name="process_daily_earning"),   # Entry Point to generate salary slip
    path('api/Show_Salary_Slip_PDF/<int:EmpID>/<str:OID>/<int:Year>/<int:Month>/<str:Action>/', Show_Salary_Slip_PDF, name='Show_Salary_Slip_PDF'),  # show Generated salary and can update manual fields
    path("api/Generate_Salary_Employee_List_API/", Generate_Salary_Employee_List_API, name="Generate_Salary_Employee_List_API"),   # Employee List for Salary Generation
    path("update_salary_slip_manual_fields/", update_salary_slip_manual_fields, name="update_salary_slip_manual_fields"),
    path("api/Bulk_Generate_Salary_Process/", Bulk_Generate_Salary_Process, name="Bulk_Generate_Salary_Process"),

    # path("Response/Response_Page_Generate_Slip/", Response_Page_Generate_Slip, name="Response_Page_Generate_Slip"),
    path("Api/Response/Response_Data_Slip_Api/", Response_Data_Slip_Api, name="Response_Data_Slip_Api"),
    path("Verify_Salary_Slip/", Verify_Salary_Slip, name="Verify_Salary_Slip"),
    path("api/Verify_Salary_Slip_API/", Verify_Salary_Slip_API, name="Verify_Salary_Slip_API"),

    path("api/Bulk_Verify_Salary_Slip/", Bulk_Verify_Salary_Slip, name="Bulk_Verify_Salary_Slip"),


    # update_salary_slip_manual_fields
    # path('api/Show_Salary_Slip_PDF/<int:SlipId>/', Show_Salary_Slip_PDF, name='Show_Salary_Slip_PDF'),

    path('Export_Salary_Slip_Excel/<int:EmpID>/<int:OID>/<int:Year>/<int:Month>/', Export_Salary_Slip_Excel, name='Export_Salary_Slip_Excel'),


    # Reports - ---
    # Attendence Report
    path("Reports/MonthlyAttendenceReport_Pdf_View/", MonthlyAttendenceReport_Pdf_View, name="MonthlyAttendenceReport_Pdf_View"),
    path("Audit_Attendance_Report/", Audit_Attendance_Report, name="Audit_Attendance_Report"),
    # path("Reports/Api/Audit_Attendance_Report_Api/", Audit_Attendance_Report_Api, name="Audit_Attendance_Report_Api"),
    path("Reports/Audit_Attendance_Report_PDF_View/", Audit_Attendance_Report_PDF_View, name="Audit_Attendance_Report_PDF_View"),

    path('api/payroll_employee_data/', Payroll_Employee_Data_API.as_view(), name='payroll_employee_data'),
    


    # path('Excel_Attendance_Upload/', Excel_Attendance_Upload_View, name='Excel_Attendance_Upload'),
    # path('Excel_Attendance_Upload_CSV/', Excel_Attendance_Upload_CSV_Api, name='Excel_Attendance_Upload_CSV'),
    # path("api/Excel_Attendance_Upload_CSV/", Excel_Attendance_Upload_CSV_Api.as_view(), name="Excel_Attendance_Upload_CSV"),
]
 

 