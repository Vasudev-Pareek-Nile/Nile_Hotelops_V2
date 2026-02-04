from django.urls import path
from .import views

urlpatterns = [
    path('homepage/' , views.homepage , name ='homepage'),
    
    path('', views.index , name = 'HBindex'),
    path('outlet/', views.index , name = 'HBindex'),
    path('add/',views.add , name ='add'),
    path('delete/<int:id>/' , views.delete , name = 'HBdelete'),
    path('update/<int:id>/',views.update,name= "update"),
    path('update/updata/<int:id>/',views.updata , name = "updata"),
    
    path('expenses/', views.expenses , name = 'HBexpenses'),
    path('add_expenses', views.add_expenses , name = 'HBadd_expenses'),
    path('delete_expenses/<int:id>/' , views.delete_expenses , name = 'HBdelete_expenses'),
    path('update_expenses/<int:id>/',views.update_expenses , name= "update_expenses"),
    # path('update_expenses/updata_expenses/<int:id>/',views.updata_expenses , name = "updata_expenses"),
    
    path('PayrollExpenses/', views.payrollExpenses, name='PayrollExpenses'),
    path('add_payrollExpenses/' , views.add_payrollExpenses, name ='add_payrollExpenses'),
    path('delete_payrollExpenses/<int:id>/' ,views.delete_payrollExpenses, name = 'HBdelete_payrollExpenses'),
    path('update_payrollExpenses/<int:id>/', views.update_payrollExpenses , name = 'HBupdate_payrollExpenses'),
    
    path('PayrollExpenseEntry/', views.PayrollExpenseEntry, name='PayrollExpenseEntry'),
      

    path('PLUtilitiesEntry/', views.PutilitiesEntry, name='HBPLUtilitiesEntry'),
    path('PLUtilitiesList/' , views.PLUtilitiesList , name = 'HBPLUtilitiesList'),
    path('delete_PLUtilities/<int:id>/', views.delete_PLUtilities , name = 'HBdelete_PLUtilities'),
    path('PLUtilitiesEdit/<int:id>/' , views.PLUtilitiesEdit , name ='HBPLUtilitiesEdit'),
    path('PLUtilitiesView/<int:id>/' ,views.PLUtilitiesView , name = 'HBPLUtilitiesView'),
     
    
    path('PL_Engineering_Master/' , views.PL_Engineering_Master, name = 'HBPL_Engineering_Master'),
    path('PL_Engineering_Entry/', views.PL_EngineeringEntry, name = 'HBPL_Engineering_Entry'),
    path('EngineeringList/', views.EngList, name='HBEngineeringList'),
    path('EngListEdit/<int:id>/' , views.EngListEdit , name ='HBEngListEdit'),
    path('EngListDelete/<int:id>/' , views.EngListDelete , name = 'HBEngListDelete'),
    path('Engviewdata/<int:id>/' , views.Engviewdata , name = 'HBEngviewdata'),
  
     
    path('AG_SecurityEntry/', views.AG_SecurityEntry , name = 'HBAG_SecurityEntry'),
    path('AG_SecurityList/' , views.AG_SecurityList , name = 'HBAG_Security'),
    path('AG_SecurityEdit/<int:id>/', views.AG_SecurityEdit , name = 'HBAG_SecurityEdit'),
    path('AG_SecurityDelete/<int:id>/' , views.AG_SecurityDelete , name = 'HBAG_SecurityDelete'),
    path('AG_Securityviewdata/<int:id>/' , views.AG_Securityviewdata , name='HBAG_Securityviewdata'),
    
    
    path('AG_HREntry/' ,views.AG_HREntry , name = 'HBAG_HREntry'),
    path('AG_HRList/' , views.AG_HRList , name ='AG_HRList'),
    path('AG_HREdit/<int:id>/' , views.AG_HREdit , name = 'HBAG_HREdit'),
    path('AG_HRDelete/<int:id>/' , views.AG_HRDelete , name = 'HBAG_HRDelete'),
    path('AG_HRviewdata/<int:id>/' ,views.AG_HRviewdata , name = 'HBAG_HRviewdata'),
    
    
    
    path('Total_AGEntry/' , views.Total_AGEntry , name = 'HBTotal_AGEntry'),
    path('Total_AGList/' , views.Total_AGList , name ='HBTotal_AGList'),
    path('Total_AGDelete/<int:id>/' , views.Total_AGDelete , name = 'HBTotal_AGDelete/'),
    path('Total_AGEdit/<int:id>/' ,views.Total_AGEdit , name ='HBTotal_AGEdit'),
    path('Total_AGviewdata/<int:id>/' , views.Total_AGviewdata , name='HBTotal_AGviewdata'),
       
    path('SMList/' , views.SMList, name = 'HBSMList'),
    path('SMEntry/' , views.SMEntry , name = 'HBSMEntry'),
    path('SMDelete/<int:id>/' , views.SMDelete , name = 'HBSMDelete'),
    path('SMEdit/<int:id>/' , views.SMEdit , name = 'HBSMEdit'), 
    path('SMviewdata/<int:id>/' , views.SMviewdata , name ='SMviewdata'),
     
    
    path('ITList/' , views.ITList , name = 'HBITList'),
    path('ITEntry/' , views.ITEntry , name ='HBITEntry'),
    path('ITDelete/<int:id>/' , views.ITDelete , name = 'HBITDelete'),
    path('ITEdit/<int:id>/' , views.ITEdit , name ='ITEdit'),
    
    
    path('AG_AnalysisList/', views.AG_AnalysisList , name = 'HBAG_AnalysisList'),
    path('AG_AnalysisEntry/' , views.AG_AnalysisEntry , name = 'HBAG_AnalysisEntry'),
    path('AG_AnalysisDelete/<int:id>/' , views.AG_AnalysisDelete , name ='HGAG_AnalysisDelete'),
    path('AG_AnalysisEdit/<int:id>/' , views.AG_AnalysisEdit , name = 'HBAG_AnalysisEdit'),
    path('AG_Analysisviewdata/<int:id>/', views.AG_Analysisviewdata , name ='HGAG_Analysisviewdata'),
    
    
    
    
    path('Rental_IncomeList/' , views.Rental_IncomeList , name ='HBRental_IncomeList'),
    path('Rental_IncomeEntry/' , views.Rental_IncomeEntry , name ='HBRental_IncomeEntry'),
    path('Rental_IncomeDelete/<int:id>/' ,views.Rental_IncomeDelete , name ='HBRental_IncomeDelete'),
    path('Rental_IncomeEdit/<int:id>/' , views.Rental_IncomeEdit , name ='HBRental_IncomeEdit'),
    path('Rental_Incomeviewdata/<int:id>/', views.Rental_Incomeviewdata , name = 'HBRental_Incomeviewdata'),
    
    
       
    path('OOD_LaundryList/' , views.OOD_LaundryList , name ='HBOOD_LaundryList'),
    path('OOD_LaundryEntry/' , views.OOD_LaundryEntry , name ='HBOOD_LaundryEntry'),
    path('OOD_LaundryDelete/<int:id>/' , views.OOD_LaundryDelete, name = 'HBOOD_LaundryDelete'),
    path('OOD_LaundryEdit/<int:id>/' , views.OOD_LaundryEdit , name ='HBOOD_LaundryEdit'),
    path('OOD_Laundryviewdata/<int:id>/' , views.OOD_Laundryviewdata , name = 'HBOOD_Laundryviewdata'),
        
      
    path('OOD_TransportList/', views.OOD_TransportList , name ='HBOOD_TransportList'),
    path('OOD_TransportEntry/' , views.OOD_TransportEntry , name = 'HBOOD_TransportEntry'),
    path('OOD_TransportDelete/<int:id>/' , views.OOD_TransportDelete , name = 'HBOOD_TransportDelete'),
    path('OOD_TransportEdit/<int:id>/' , views.OOD_TransportEdit , name = 'HBOOD_TransportEdit'),
    path('OOD_Transportviewdata/<int:id>/' , views.OOD_Transportviewdata , name = 'HBOOD_Transportviewdata'),
    
    
    path('OOD_HealthList/' , views.OOD_HealthList , name = 'HBOOD_HealthList'),
    path('OOD_HealthEntry/', views.OOD_HealthEntry , name='HBOOD_HealthEntry'),
    path('OOD_HealthDelete/<int:id>/' , views.OOD_HealthDelete , name = 'HBOOD_HealthDelete'),
    path('OOD_HealthEdit/<int:id>/' , views.OOD_HealthEdit , name = 'HBOOD_HealthEdit'),
    path('OOD_Healthviewdata/<int:id>/' , views.OOD_Healthviewdata , name ='HBOOD_Healthviewdata'),
    
    
    path('FB_BanquetList/', views.FB_BanquetList , name='HBFB_BanquetList'),
    path('FB_BanquetEntry/' , views.FB_BanquetEntry , name='HBFB_BanquetEntry'),
    path('FB_BanquetDelete/<int:id>/' , views.FB_BanquetDelete , name ='HBFB_BanquetDelete'),
    path('FB_BanquetEdit/<int:id>/' , views.FB_BanquetEdit , name ='HBFB_BanquetEdit'),  
    path('FB_Banquetviewdata/<int:id>/', views.FB_Banquetviewdata , name='HBFB_Banquetviewdata'),
     
    
    path('FB_IRDList/' , views.FB_IRDList , name = 'HBFB_IRDList'),
    path('FB_IRDEntry/' , views.FB_IRDEntry , name = 'HBFB_IRDEntry'),
    path('FB_IRDDelete/<int:id>/' , views.FB_IRDDelete , name = 'HBFB_IRDDelete'),
    path('FB_IRDEdit/<int:id>/' , views.FB_IRDEdit , name = 'HBFB_IRDEdit'),   
    path('FB_IRDviewdata/<int:id>/' ,views.FB_IRDviewdata , name = 'HBFB_IRDviewdata'),
    
    
    path('Outlet_1List/' , views.Outlet_1List , name ='HBOutlet_1List'),
    path('Outlet_1Entry/' , views.Outlet_1Entry , name = 'HBOutlet_1Entry'),
    path('Outlet_1Delete/<int:id>/' , views.Outlet_1Delete , name= 'HBOutlet_1Delete'),
    path('Outlet_1Edit/<int:id>/' , views.Outlet_1Edit , name='HBOutlet_1Edit'),
    path('Outlet_1viewdata/<int:id>/',views.Outlet_1viewdata , name='HBOutlet_1viewdata'),
    
       
    path('Outlet_2List/' , views.Outlet_2List , name ='HBOutlet_2List'),
    path('Outlet_2Entry/' , views.Outlet_2Entry , name = 'HBOutlet_2Entry'),
    path('Outlet_2Delete/<int:id>/' , views.Outlet_2Delete , name ='HBOutlet_2Delete'),
    path('Outlet_2Edit/<int:id>/' , views.Outlet_2Edit , name = 'HBOutlet_2Edit'),
    path('Outlet_2viewdata/<int:id>/' ,views.Outlet_2viewdata , name ='HBOutlet_2viewdata'),
    
    
    path('Outlet_3List/' , views.Outlet_3List , name ='HBOutlet_3List'),
    path('Outlet_3Entry/' , views.Outlet_3Entry , name = 'HBOutlet_3Entry'),
    path('Outlet_3Delete/<int:id>/' , views.Outlet_3Delete , name ='HBOutlet_3Delete'),
    path('Outlet_3Edit/<int:id>/' , views.Outlet_3Edit , name = 'HBOutlet_3Edit'),
    path('Outlet_3viewdata/<int:id>/' ,views.Outlet_3viewdata , name ='HBOutlet_3viewdata'),
    
    
       
    path('Outlet_4List/' , views.Outlet_4List , name ='HBOutlet_4List'),
    path('Outlet_4Entry/' , views.Outlet_4Entry , name = 'HBOutlet_4Entry'),
    path('Outlet_4Delete/<int:id>/' , views.Outlet_4Delete , name ='HBOutlet_4Delete'),
    path('Outlet_4Edit/<int:id>/' , views.Outlet_4Edit , name = 'HBOutlet_4Edit'),
    path('Outlet_4viewdata/<int:id>/',views.Outlet_4viewdata , name = 'HBOutlet_4viewdata'), 
    
      
    
    path('Outlet_5List/' , views.Outlet_5List , name ='HBOutlet_5List'),
    path('Outlet_5Entry/' , views.Outlet_5Entry , name = 'HBOutlet_5Entry'),
    path('Outlet_5Delete/<int:id>/' , views.Outlet_5Delete , name ='HBOutlet_5Delete'),
    path('Outlet_5Edit/<int:id>/' , views.Outlet_5Edit , name = 'HBOutlet_5Edit'), 
    path('Outlet_5viewdata/<int:id>/' ,views.Outlet_5viewdata , name ='HBOutlet_5viewdata'),  
    
    
    path('PL_RoomsList/' , views.PL_RoomsList , name ='HBPL_RoomsList'),
    path('PL_RoomsEntry/' , views.PL_RoomsEntry , name = 'HBPL_RoomsEntry'),
    path('PL_RoomsDelete/<int:id>/' , views.PL_RoomsDelete , name ='HBPL_RoomsDelete'),
    path('PL_RoomsEdit/<int:id>/' , views.PL_RoomsEdit , name = 'HBPL_RoomsEdit'),   
    path('PL_Roomsviewdata/<int:id>/' , views.PL_Roomsviewdata , name = 'HBPL_Roomsviewdata'),
    
    
    path('Total_OODList/' , views.Total_OODList , name = 'HBTotal_OODList'),
    path('Total_OODEntry/' , views.Total_OODEntry , name = 'HBTotal_OODEntry'),
    path('Total_OODDelete/<int:id>/' , views.Total_OODDelete , name = 'HBTotal_OODDelete'),
    path('Total_OODEdit/<int:id>/' , views.Total_OODEdit , name = 'HBTotal_OODEdit'),
    path('Total_OODviewdata/<int:id>/',views.Total_OODviewdata, name ='HBTotal_OODviewdata'),
    
    
    path('PL_SummaryList/' , views.PL_SummaryList , name = 'HBPL_SummaryList'),
    path('PL_SummaryEntry/', views.PL_SummaryEntry , name = 'HBPL_SummaryEntry'),
    path('PL_SummaryDelete/<int:id>/', views.PL_SummaryDelete , name ='HBPL_SummaryDelete'),
    path('PL_SummaryEdit/<int:id>/',views.PL_SummaryEdit , name ='HBPL_SummaryEdit'),
    path('PL_Summaryviewdata/<int:id>/' ,views.PL_Summaryviewdata , name = 'HBPL_Summaryviewdata'),
    
    
    path('Total_FBList/' , views.Total_FBList , name ='HBTotal_FBList'),
    path('Total_FBEntry/' , views.Total_FBEntry , name = 'HBTotal_FBEntry'),
    path('Total_FBDelete/<int:id>/',views.Total_FBDelete , name='HBTotal_FBDelete'),
    
]