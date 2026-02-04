
from .views import *
from django.urls import path
from .Issue_And_Clearance import Issue_view, Clearance_view, Hod_Approve_Request, Hod_Hold_Request, Hod_Approve_Request_Clearance

urlpatterns = [


    path('HumanResourcesDashboard/',HumanResourcesDashboard,name='HumanResourcesDashboard'),

    path('api/human-resources-dashboard/', api_human_resources_dashboard, name='api_human_resources_dashboard'),


    # path('NewEmployeeAdd/',NewEmployeeAdd,name='NewEmployeeAdd'),
    path('Humanview_file/',Humanview_file,name='Humanview_file'),
    path('EmployeeList/',EmployeeList,name='EmployeeList'),
    path('get-departments/', get_departments_by_division, name='get_departments'),
    path('EmpView/', EmpView, name='EmpView'),
    path('EditEmployee/',EditEmployee,name='EditEmployee'),


    path('PersonalDetails/',PersonalDetails,name='PersonalDetails'),
    path('EmployeeWorkDetailsPage/',EmployeeWorkDetailsPage,name='EmployeeWorkDetailsPage'),

    
    path('LeaveDetails/',LeaveDetails,name='LeaveDetails'),
    path('EmergencyInfoPage/',EmergencyInfoPage,name='EmergencyInfoPage'),
    path('AddressPage/',AddressPage,name='AddressPage'),
    path('IdentityPage/',IdentityPage,name='IdentityPage'),
    path('BankDetailsPage/',BankDetailsPage,name='BankDetailsPage'),
    path('SalaryDetailsPage/',SalaryDetailsPage,name='SalaryDetailsPage'),   #+------------------ here

    path('DocumentinfoPage/',DocumentinfoPage,name='DocumentinfoPage'),

    path('PreviousworkinfoPage/',PreviousworkinfoPage,name='PreviousworkinfoPage'),

    path('QualificationinfoPage/',QualificationinfoPage,name='QualificationinfoPage'),
    
    path('FamilyinfoPage/',FamilyinfoPage,name='FamilyinfoPage'),
    
    path('EmployeeLetters/',EmployeeLetters,name='EmployeeLetters'),

    # Employee Add Form 

    path('CheckEmployeeCode/', CheckEmployeeCode, name='CheckEmployeeCode'),

    path('NewEmployeeDataForm/', NewEmployeeDataForm, name='NewEmployeeDataForm'),
    path('NewEmployeePersonalData/', NewEmployeePersonalData, name='NewEmployeePersonalData'),
    path('NewEmployeeWorkData/', NewEmployeeWorkData, name='NewEmployeeWorkData'),
    path('NewEmployeeFamilyinfo/', NewEmployeeFamilyinfo, name='NewEmployeeFamilyinfo'),
    path('NewEmployeeEmergencyinfo/', NewEmployeeEmergencyinfo, name='NewEmployeeEmergencyinfo'),
    path('NewEmployeeQualificationinfo/', NewEmployeeQualificationinfo, name='NewEmployeeQualificationinfo'),
    path('NewEmployeePreviousWorkinfo/', NewEmployeePreviousWorkinfo, name='NewEmployeePreviousWorkinfo'),
    path('NewEmployeeAddressinfo/', NewEmployeeAddressinfo, name='NewEmployeeAddressinfo'),
    path('NewEmployeeIdentityinfo/', NewEmployeeIdentityinfo, name='NewEmployeeIdentityinfo'),
    path('NewEmployeeBankinfo/', NewEmployeeBankinfo, name='NewEmployeeBankinfo'),
    path('NewEmployeeSalaryDetailsData/', NewEmployeeSalaryDetailsData, name='NewEmployeeSalaryDetailsData'),
    path('NewEmployeeLeaveDetailsData/', NewEmployeeLeaveDetailsData, name='NewEmployeeLeaveDetailsData'),
    path('NewEmployeeDocumentinfo/', NewEmployeeDocumentinfo, name='NewEmployeeDocumentinfo'),

    path('Warning_Letters/', Warning_Letters, name='Warning_Letters'),

    path('Clearance_From/', Clearance_From, name='Clearance_From'),
    path('ExitInterview/', ExitInterview, name='ExitInterview'),
    path('JobDescriptions/', JobDescriptions, name='JobDescriptions'),
 
 
    path('ProbationConfirmation/', ProbationConfirmation, name='ProbationConfirmation'),
    path('Termination/', Termination, name='Termination'),
    path('Resigantion/', Resigantion, name='Resigantion'),
    path('Absconding/', Absconding, name='Absconding'),
    # New -- For --> Absconding Revoke
    path('Absconding_Revoke/', Absconding_Revoke_View, name='Absconding_Revoke'),

    
    path('IT/', IT, name='IT'), 
    path('Uniform/', Uniform, name='Uniform'),
    path('FullandFinal/', FullandFinal, name='FullandFinal'),
    path('PADP/', PADP, name='PADP'),

    path('Checklist/', Checklist, name='Checklist'),
    path('CodeConduct/', CodeConduct, name='CodeConduct'),
    path('DataMissingReport/', DataMissingReport, name='DataMissingReport'),
    path('KraReport/', KraReport, name='KraReport'),
    
    # New Urls
    # Reporting To Change
    path('Change_Reporting_To/', Change_Reporting_To, name='Change_Reporting_To'),
    path('EmployeeList_StatusFormHandle/', EmployeeList_StatusFormHandle, name='EmployeeList_StatusFormHandle'),
    
 

    # New Salary System
    path('Salary_Details_Settlement/<int:EmpID>/<str:OID>/', Salary_Details_Settlement, name='Salary_Details_Settlement'),

    path('api/salary_effective/<int:EmpID>/<str:OID>/', get_salary_effective_data, name='get_salary_effective_data'),

    path('Update_Salary_Details_Settlement/<int:EmpID>/<str:OID>/<int:SettleID>/', Update_Salary_Details_Settlement, name='Update_Salary_Details_Settlement'),
    path('delete_salary_effective/<int:EmpID>/<str:OID>/<int:SettleID>/', delete_salary_effective, name='delete_salary_effective'),


    # path("recalculate-salary/", recalculate_salary, name="recalculate_salary"),
    
    path('Issue/', Issue_view, name='Issue_view'),
    path('Clearance/', Clearance_view, name='Clearance_view'),
    
    path('hod/approve/', Hod_Approve_Request, name='Hod_Approve_Request'),
    path('hod/approve_clearance/', Hod_Approve_Request_Clearance, name='Hod_Approve_Request_Clearance'),
    path('hod/hold/', Hod_Hold_Request, name='Hod_Hold_Request'),   
]
