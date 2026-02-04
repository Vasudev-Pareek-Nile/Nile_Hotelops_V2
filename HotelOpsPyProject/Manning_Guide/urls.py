from django.urls import path
from .import views
# from .Mobile_Api_View import variance_report_Mobile_api, variance_report_totals_api_v2
from .Mobile_Api_View import *
urlpatterns = [

     path('homedeta/',views.homedeta,name="homedeta"),
     path('OnRollDivisionAdd/',views.OnRollDivisionAdd,name="OnRollDivisionAdd"),
     path('add-department/', views.OnRollDepartmentAdd, name='OnRollDepartmentAdd'),
     path('OnRollDesignationAdd/', views.OnRollDesignationAdd, name='OnRollDesignationAdd'),
     path('division_delete/', views.division_delete, name='division_delete'),
     path('department_delete/', views.department_delete, name='department_delete'),
     path('designationadd_delete/', views.designationadd_delete, name='designationadd_delete'),
     path('divisions_list/', views.divisions_list, name='divisions_list'),
     path('departments_list/', views.departments_list, name='departments_list'),
     path('designation_details/', views.designation_details, name='designation_details'),
     path('move_up_viewdivisiononroll/<int:id>/', views.move_up_viewdivisiononroll, name='move_up_viewdivisiononroll'),
     path('move_down_viewdivisiononroll/<int:id>/', views.move_down_viewdivisiononroll, name='move_down_viewdivisiononroll'),

     path('move_up_departmentonroll/<int:id>/', views.move_up_departmentonroll, name='move_up_departmentonroll'),
     path('move_down_departmentonroll/<int:id>/', views.move_down_departmentonroll, name='move_down_departmentonroll'),
     path('move_up_designation_onroll/<int:id>/', views.move_up_designation_onroll, name='move_up_designation_onroll'),
    path('move_down_designation_onroll/<int:id>/', views.move_down_designation_onroll, name='move_down_designation_onroll'),
#      Master Manage Contract
     path('Managecontract/', views.Managecontract, name='Managecontract'),
     path('ContractDivisionAdd/', views.ContractDivisionAdd, name='ContractDivisionAdd'),
     path('ContractDepartmentAdd/', views.ContractDepartmentAdd, name='ContractDepartmentAdd'),
     path('ContractDesignationAdd/', views.ContractDesignationAdd, name='ContractDesignationAdd'),
     path('ContractDivision_delete/', views.ContractDivision_delete, name='ContractDivision_delete'),
     path('ContractDepartment_delete/', views.ContractDepartment_delete, name='ContractDepartment_delete'),
     path('ContractDesignation_delete/', views.ContractDesignation_delete, name='ContractDesignation_delete'),
      path('Contractdivisions_list/', views.Contractdivisions_list, name='Contractdivisions_list'),
      path('Contractdepartments_list/', views.Contractdepartments_list, name='Contractdepartments_list'),
      path('Contractdesignation_details/', views.Contractdesignation_details, name='Contractdesignation_details'),

      path('move_up_divisioncontract/<int:id>/', views.move_up_divisioncontract, name='move_up_divisioncontract'),
      path('move_down_divisioncontract/<int:id>/', views.move_down_divisioncontract, name='move_down_divisioncontract'),

      path('move_up_departmentContract/<int:id>/', views.move_up_departmentContract, name='move_up_departmentContract'),
      path('move_down_departmentContract/<int:id>/', views.move_down_departmentContract, name='move_down_departmentContract'),

      path('move_up_designationContract/<int:id>/', views.move_up_designationContract, name='move_up_designationContract'),
      path('move_down_designationContract/<int:id>/', views.move_down_designationContract, name='move_down_designationContract'),
#      Master Manage Shared Services  
     path('SharedServices/', views.SharedServices, name='SharedServices'),
     path('ServicesDivisionAdd/', views.ServicesDivisionAdd, name='ServicesDivisionAdd'),  
     path('ServicesDepartmentAdd/', views.ServicesDepartmentAdd, name='ServicesDepartmentAdd'),  
     path('ServicesDesignationAdd/', views.ServicesDesignationAdd, name='ServicesDesignationAdd'),
     path('ServicesDivision_delete/', views.ServicesDivision_delete, name='ServicesDivision_delete'),
     path('ServicesDepartment_delete/', views.ServicesDepartment_delete, name='ServicesDepartment_delete'),
     path('ServicesDesignation_delete/', views.ServicesDesignation_delete, name='ServicesDesignation_delete'),
     
     path('Servicesdivisions_list/', views.Servicesdivisions_list, name='Servicesdivisions_list'),
     path('Servicesdepartments_list/', views.Servicesdepartments_list, name='Servicesdepartments_list'),
     path('Servicesdesignation_details/', views.Servicesdesignation_details, name='Servicesdesignation_details'), 

     path('move_up_divisionservices/<int:id>/', views.move_up_divisionservices, name='move_up_divisionservices'),
     path('move_down_divisionservices/<int:id>/', views.move_down_divisionservices, name='move_down_divisionservices'),

      path('move_up_departmentservices/<int:id>/', views.move_up_departmentservices, name='move_up_departmentservices'),
      path('move_down_departmentservices/<int:id>/', views.move_down_departmentservices, name='move_down_departmentservices'),
      

     path('move_up_designationservices/<int:id>/', views.move_up_designationservices, name='move_up_designationservices'),
     path('move_down_designationservices/<int:id>/', views.move_down_designationservices, name='move_down_designationservices'),
#      Master Manage Lavel  
     path('Masterlavel/', views.Masterlavel, name='Masterlavel'),
     path('laveldeta/', views.laveldeta, name='laveldeta'),
     path('level_delete/', views.level_delete, name='level_delete'),
     path('level_Edit/', views.level_Edit, name='level_Edit'),

#      Master Manage Corporate 
     path('Corporate/', views.Corporate, name='Corporate'),
     path('CorporateDivisionAdd/', views.CorporateDivisionAdd, name='CorporateDivisionAdd'),
     path('CorporateDepartmentAdd/', views.CorporateDepartmentAdd, name='CorporateDepartmentAdd'),
     path('CorporateDesignationAdd/', views.CorporateDesignationAdd, name='CorporateDesignationAdd'),
     path('CorporateDivision_delete/', views.CorporateDivision_delete, name='CorporateDivision_delete'),
     path('CorporateDepartment_delete/', views.CorporateDepartment_delete, name='CorporateDepartment_delete'),
     path('CorporateDesignation_delete/', views.CorporateDesignation_delete, name='CorporateDesignation_delete'),

     path('Corporatedivisions_list/', views.Corporatedivisions_list, name='Corporatedivisions_list'),
     path('Corporatedepartments_list/', views.Corporatedepartments_list, name='Corporatedepartments_list'),
     path('Corporatedesignation_details/', views.Corporatedesignation_details, name='Corporatedesignation_details'),

     path('move_up_divisionCorporate/<int:id>/', views.move_up_divisionCorporate, name='move_up_divisionCorporate'),
     path('move_down_divisionCorporate/<int:id>/', views.move_down_divisionCorporate, name='move_down_divisionCorporate'),


      path('move_up_departmentCorporate/<int:id>/', views.move_up_departmentCorporate, name='move_up_departmentCorporate'),
      path('move_down_departmentCorporate/<int:id>/', views.move_down_departmentCorporate, name='move_down_departmentCorporate'),

     path('move_up_designationCorporate/<int:id>/', views.move_up_designationCorporate, name='move_up_designationCorporate'),
     path('move_down_designationCorporate/<int:id>/', views.move_down_designationCorporate, name='move_down_designationCorporate'),
     
     path('Module_Mapping/', views.Module_Mapping, name='Module_Mapping'),

     path('ModuleMappingAdd/', views.ModuleMappingAdd, name='ModuleMappingAdd'),
     path('ModuleMapping_delete/', views.ModuleMapping_delete, name='ModuleMapping_delete'),

     path('Module_Edit/', views.Module_Edit, name='Module_Edit'),

# Manage Budget On Roll

     path('ViewBudget/', views.ViewBudget, name='ViewBudget'),
     path('BudgetOndeta/', views.BudgetOndeta, name='BudgetOndeta'),
     path('BudgetContract/', views.BudgetContract, name='BudgetContract'),
   
     path('MealCost/', views.MealCost, name='MealCost'),
     path('InsuranceCost/', views.InsuranceCost, name='InsuranceCost'),
     path('SharedServicesbudget/', views.SharedServicesbudget, name='SharedServicesbudget'),

     path('ViewBudgetPdf/', views.ViewBudgetPdf, name='ViewBudgetPdf'),

# Entry Actual

    path('Entrymealcost/', views.Entrymealcost, name='Entrymealcost'),
    path('EntryInsurancesCost/', views.EntryInsurancesCost, name='EntryInsurancesCost'),
    path('EntryActualContractCost/', views.EntryActualContractCost, name='EntryActualContractCost'),
    path('EntrySharedServices/', views.EntrySharedServices, name='EntrySharedServices'),
    path('ViewActual/', views.ViewActual, name='ViewActual'),
    path('EntryActualPdf/', views.EntryActualPdf, name='EntryActualPdf'),

    path('VarianceReportView/', views.VarianceReportView, name='VarianceReportView'),
    path('variancepdf/', views.variancepdf, name='variancepdf'),

# Master Report  
    path('LevelWiseReport/', views.LevelWiseReport, name='LevelWiseReport'),  
    path('LevelWisePdf/', views.LevelWisePdf, name='LevelWisePdf'),  
    path('DeparmentsWiseReport/', views.DeparmentsWiseReport, name='DeparmentsWiseReport'),  
    path('DeparmentsWisePdf/', views.DeparmentsWisePdf, name='DeparmentsWisePdf'),  

#     path('DesignationWiseReport/', views.DesignationWiseReport, name='DesignationWiseReport'),  # DignationsWiseReport To DesignationWiseReport
    path('DesignationWiseReport/', views.DesignationWiseReport, name='DignationsWiseReport'),  # DignationsWiseReport To DesignationWiseReport
    path('DesignationWiseReportPdf/', views.DesignationWiseReportPdf, name='DesignationWiseReportPdf'), 

#     path('DignationsWiseReport/', views.DignationsWiseReport, name='DignationsWiseReport'),  # DignationsWiseReport To DesignationWiseReport
#     path('DignationsWisePdf/', views.DignationsWisePdf, name='DignationsWisePdf'), 
    path('MasterLevelwise/', views.MasterLevelwise, name='MasterLevelwise'), 

    

    path('api/departments/', views.get_departments, name='get_departments'),
    path('api/designations/', views.get_designations, name='get_designations'),
    path('api/levels/', views.get_levels, name='get_levels'),

    path('budget_filter/', views.budget_filter, name='budget_filter'),
    path('budget_master_pdf/', views.budget_master_pdf, name='budget_master_pdf'),

    path('ActualMasterReport/', views.ActualMasterReport, name='ActualMasterReport'),

    path('variance_details_report_experiment/', views.variance_details_report_experiment, name='variance_details_report_experiment'),
    path('Actualdata_filter/', views.Actualdata_filter, name='Actualdata_filter'),
    path('Actualdatapdf/', views.Actualdatapdf, name='Actualdatapdf'),
    path('get_departmentsActual/', views.get_departmentsActual, name='get_departmentsActual'),
    path('get_designationsActual/', views.get_designationsActual, name='get_designationsActual'),
    path('degntioncount/', views.degntioncount, name='degntioncount'),
    path('BudgetsalaryDesignation/', views.BudgetsalaryDesignation, name='BudgetsalaryDesignation'),
    path('ActualHeadCountDesignation/', views.ActualHeadCountDesignation, name='ActualHeadCountDesignation'),
    path('ActualsalaryDesignation/', views.ActualsalaryDesignation, name='ActualsalaryDesignation'),
    path('ActualHeadCountDesignationPDF/', views.ActualHeadCountDesignationPDF, name='ActualHeadCountDesignationPDF'),
    path('ActualsalaryDesignationPdf/', views.ActualsalaryDesignationPdf, name='ActualsalaryDesignationPdf'),
    path('degntioncountPdf/', views.degntioncountPdf, name='degntioncountPdf'),
     path('BudgetsalaryDesignationPDF/', views.BudgetsalaryDesignationPDF, name='BudgetsalaryDesignationPDF'),


     # New urls --  CEO Variance Report
     path('Variance_Ceo_Report/', views.Variance_Ceo_Report, name='Variance_Ceo_Report'),
     path('Variance_Ceo_Report_PDF/', views.Variance_Ceo_Report_PDF, name='Variance_Ceo_Report_PDF'),
     path('api/variance_report_api/', views.variance_report_api, name='variance_report_api'),

     # Mobile API Variance Report
     path('api/variance_report_Mobile_api/', variance_report_Mobile_api, name='variance_report_Mobile_api'),

     # example API for variance report totals
     # path('api/variance_report_totals_api_v2/', variance_report_totals_api_v2, name='variance_report_totals_api_v2'),
     path('api/variance_totals/', variance_totals, name='variance_totals'),
     path('api/variance_divisions/', variance_divisions, name='variance_divisions'),
     path('api/variance_departments/', variance_departments, name='variance_departments'),
     path('api/variance_Employee_Data/', variance_Employee_Data, name='variance_Employee_Data'),
     path('api/ManningGuideCorpoReport/', ManningGuideCorpoReport, name='ManningGuideCorpoReport'),   # active for mobile


     path('api/View_Actual_mobile_api/', View_Actual_mobile_api, name='View_Actual_mobile_api'),
     # path('api/ViewActual_mobile_api_Core_Part/', ViewActual_mobile_api_Core_Part, name='ViewActual_mobile_api_Core_Part'),

     # New And Testing
     path('api/DepartmentTotalsView_Demo_Api/', views.DepartmentTotalsView_Demo_Api, name='DepartmentTotalsView_Demo_Api'),
     path('api/DepartmentTotalsView_Demo_Api2/', views.DepartmentTotalsView_Demo_Api2, name='DepartmentTotalsView_Demo_Api2'),
     
     
     path('api/onroll-designation-list/', OnRollDesignationListAPI.as_view(), name='onroll-designation-list'),
     
     
     # new varience report view
     path('variance_details_report_experiment/', views.variance_details_report_experiment, name='variance_details_report_experiment'),
     path('api/variance_details_report/', variance_details_report, name='variance_details_report'),
     
     
     path('api/view-budget/', view_budget_api, name='view-budget-api'),
     path('api/view-budget_two/', view_budget_trial_two_api, name='view-budget-two-api'),
     
     path('api/Department_Totals_View/', Department_Totals_View, name='Department_Totals_View'),
     path('api/contract-manning/', contract_manning_api, name='contract-manning-api'),
     path('api/shared-service-manning/', shared_service_manning_api, name='shared-service-manning-api'),
     # path('api/budget-summary-api/', budget_summary_api, name='budget-summary-api'),
     path('api/budget_api/', budget_api, name='budget_api'),
     
     
     path('api/contract_varience_manning_api/', views.contract_varience_manning_api, name='contract_varience_manning_api'),
     path('api/shared_services_manning_api/', views.shared_services_manning_api, name='shared_services_manning_api'),
     path('api/budget_onroll_variance_totals_api/', views.budget_onroll_variance_totals_api, name='budget_onroll_variance_totals_api'),
]    
