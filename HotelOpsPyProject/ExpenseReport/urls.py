from django.urls import path
from .import views


urlpatterns = [
    
    path('homepage/' , views.homepage , name ='homepage'),
    

    path('PLUtilitiesList/' , views.PLUtilitiesList , name = 'PLUtilitiesList'),
    path('delete_PLUtilities/<int:id>/' ,views.delete_PLUtilities , name='delete_PLUtilities'),
    path('PLUtilitiesEntry/' , views.PutilitiesEntry , name='PLUtilitiesEntry'),
    path('PLUtilitiesEdit/<int:id>/' , views.PLUtilitiesEdit , name='PLUtilitiesEdit'),
    path('PLUtilitiesView/<int:id>/' ,views.PLUtilitiesView , name= 'PLUtilitiesView'),
    
    path('EngList/', views.EngList, name='EngList'),
    path('EngEntry/', views.PL_EngineeringEntry, name = 'EngEntry'),
    path('EngListEdit/<int:id>/' , views.EngListEdit , name ='EngListEdit'),
    path('EngListDelete/<int:id>/' , views.EngListDelete , name = 'EngListDelete'),
    path('Engviewdata/<int:id>/' , views.Engviewdata , name = 'Engviewdata'),
             
    path('SMList/' , views.SMList, name = 'SMList'),
    path('SMEntry/' , views.SMEntry , name = 'SMEntry'),
    path('SMDelete/<int:id>/' , views.SMDelete , name = 'SMDelete'),
    path('SMEdit/<int:id>/' , views.SMEdit , name = 'SMEdit'), 
    path('SMviewdata/<int:id>/' , views.SMviewdata , name ='SMviewdata'),
    
    path('ITList/' , views.ITList , name = 'ITList'),
    path('ITEntry/' , views.ITEntry , name ='ITEntry'),
    path('ITDelete/<int:id>/' , views.ITDelete , name = 'ITDelete'),
    path('ITEdit/<int:id>/' , views.ITEdit , name ='ITEdit'),
    path('ITviewdata/<int:id>/' ,views.ITviewdata , name = 'ITviewdata'),
 
       
    path('AG_SecurityEntry/', views.AG_SecurityEntry , name = 'AG_SecurityEntry'),
    path('AG_SecurityList/' , views.AG_SecurityList , name = 'AG_Security'),
    path('AG_SecurityEdit/<int:id>/', views.AG_SecurityEdit , name = 'AG_SecurityEdit'),
    path('AG_SecurityDelete/<int:id>/' , views.AG_SecurityDelete , name = 'AG_SecurityDelete'),
    path('AG_Securityviewdata/<int:id>/' , views.AG_Securityviewdata , name='AG_Securityviewdata'), 
    
    path('AG_HREntry/' ,views.AG_HREntry , name = 'AG_HREntry'),
    path('AG_HRList/' , views.AG_HRList , name ='AG_HRList'),
    path('AG_HREdit/<int:id>/' , views.AG_HREdit , name = 'AG_HREdit'),
    path('AG_HRDelete/<int:id>/' , views.AG_HRDelete , name = 'AG_HRDelete'),
    path('AG_HRviewdata/<int:id>/' ,views.AG_HRviewdata , name = 'AG_HRviewdata'),
    
    path('AG_AnalysisList/', views.AG_AnalysisList , name = 'AG_AnalysisList'),
    path('AG_AnalysisEntry/' , views.AG_AnalysisEntry , name = 'AG_AnalysisEntry'),
    path('AG_AnalysisDelete/<int:id>/' , views.AG_AnalysisDelete , name ='AG_AnalysisDelete'),
    path('AG_AnalysisEdit/<int:id>/' , views.AG_AnalysisEdit , name = 'AG_AnalysisEdit'),
    path('AG_Analysisviewdata/<int:id>/', views.AG_Analysisviewdata , name ='AG_Analysisviewdata'),
    
    
    path('Total_AGEntry/' , views.Total_AGEntry , name = 'Total_AGEntry'),
    path('Total_AGList/' , views.Total_AGList , name ='Total_AGList'),
    path('Total_AGDelete/<int:id>/' , views.Total_AGDelete , name = 'Total_AGDelete/'),
    path('Total_AGEdit/<int:id>/' ,views.Total_AGEdit , name ='Total_AGEdit'),
    path('Total_AGviewdata/<int:id>/' , views.Total_AGviewdata , name='Total_AGviewdata'),
       
    path('Rental_IncomeList/' , views.Rental_IncomeList , name ='Rental_IncomeList'),
    path('Rental_IncomeEntry/' , views.Rental_IncomeEntry , name ='Rental_IncomeEntry'),
    path('Rental_IncomeDelete/<int:id>/' ,views.Rental_IncomeDelete , name ='Rental_IncomeDelete'),
    path('Rental_IncomeEdit/<int:id>/' , views.Rental_IncomeEdit , name ='Rental_IncomeEdit'),
    path('Rental_Incomeviewdata/<int:id>/', views.Rental_Incomeviewdata , name = 'Rental_Incomeviewdata'),
    
         
    path('OOD_LaundryList/' , views.OOD_LaundryList , name ='OOD_LaundryList'),
    path('OOD_LaundryEntry/' , views.OOD_LaundryEntry , name ='OOD_LaundryEntry'),
    path('OOD_LaundryDelete/<int:id>/' , views.OOD_LaundryDelete, name = 'OOD_LaundryDelete'),
    path('OOD_LaundryEdit/<int:id>/' , views.OOD_LaundryEdit , name ='OOD_LaundryEdit'),
    path('OOD_Laundryviewdata/<int:id>/' , views.OOD_Laundryviewdata , name = 'OOD_Laundryviewdata'),
    
        
    path('OOD_TransportList/', views.OOD_TransportList , name ='OOD_TransportList'),
    path('OOD_TransportEntry/' , views.OOD_TransportEntry , name = 'OOD_TransportEntry'),
    path('OOD_TransportDelete/<int:id>/' , views.OOD_TransportDelete , name = 'OOD_TransportDelete'),
    path('OOD_TransportEdit/<int:id>/' , views.OOD_TransportEdit , name = 'OOD_TransportEdit'),
    path('OOD_Transportviewdata/<int:id>/' , views.OOD_Transportviewdata , name = 'OOD_Transportviewdata'),
    
    
    path('OOD_HealthList/' , views.OOD_HealthList , name = 'OOD_HealthList'),
    path('OOD_HealthEntry/', views.OOD_HealthEntry , name='OOD_HealthEntry'),
    path('OOD_HealthDelete/<int:id>/' , views.OOD_HealthDelete , name = 'OOD_HealthDelete'),
    path('OOD_HealthEdit/<int:id>/' , views.OOD_HealthEdit , name = 'OOD_HealthEdit'),
    path('OOD_Healthviewdata/<int:id>/' , views.OOD_Healthviewdata , name ='OOD_Healthviewdata'),
    
    path('Total_OODList/' , views.Total_OODList , name = 'Total_OODList'),
    path('Total_OODEntry/' , views.Total_OODEntry , name = 'Total_OODEntry'),
    path('Total_OODDelete/<int:id>/' , views.Total_OODDelete , name = 'Total_OODDelete'),
    path('Total_OODEdit/<int:id>/' , views.Total_OODEdit , name = 'Total_OODEdit'),
    path('Total_OODviewdata/<int:id>/',views.Total_OODviewdata, name ='Total_OODviewdata'),
    
    path('FB_BanquetList/', views.FB_BanquetList , name='FB_BanquetList'),
    path('FB_BanquetEntry/' , views.FB_BanquetEntry , name='FB_BanquetEntry'),
    path('FB_BanquetDelete/<int:id>/' , views.FB_BanquetDelete , name ='FB_BanquetDelete'),
    path('FB_BanquetEdit/<int:id>/' , views.FB_BanquetEdit , name ='FB_BanquetEdit'),  
    path('FB_Banquetviewdata/<int:id>/', views.FB_Banquetviewdata , name='FB_Banquetviewdata'),
    
     
    path('FB_IRDList/' , views.FB_IRDList , name = 'FB_IRDList'),
    path('FB_IRDEntry/' , views.FB_IRDEntry , name = 'FB_IRDEntry'),
    path('FB_IRDDelete/<int:id>/' , views.FB_IRDDelete , name = 'FB_IRDDelete'),
    path('FB_IRDEdit/<int:id>/' , views.FB_IRDEdit , name = 'FB_IRDEdit'),   
    path('FB_IRDviewdata/<int:id>/' ,views.FB_IRDviewdata , name = 'FB_IRDviewdata'),   
           
    path('Outlet_1List/' , views.Outlet_1List , name ='Outlet_1List'),
    path('Outlet_1Entry/' , views.Outlet_1Entry , name = 'Outlet_1Entry'),
    path('Outlet_1Delete/<int:id>/' , views.Outlet_1Delete , name= 'Outlet_1Delete'),
    path('Outlet_1Edit/<int:id>/' , views.Outlet_1Edit , name='Outlet_1Edit'),
    path('Outlet_1viewdata/<int:id>/',views.Outlet_1viewdata , name='Outlet_1viewdata'),
    
    path('Outlet_2List/' , views.Outlet_2List , name ='Outlet_2List'),   
    path('Outlet_2Entry/' , views.Outlet_2Entry , name = 'Outlet_2Entry'),
    path('Outlet_2Delete/<int:id>/' , views.Outlet_2Delete , name ='Outlet_2Delete'),
    path('Outlet_2Edit/<int:id>/' , views.Outlet_2Edit , name = 'Outlet_2Edit'),
    path('Outlet_2viewdata/<int:id>/' ,views.Outlet_2viewdata , name ='Outlet_2viewdata'),
    
    path('Outlet_3List/' , views.Outlet_3List , name ='Outlet_3List'),
    path('Outlet_3Entry/' , views.Outlet_3Entry , name = 'Outlet_3Entry'),
    path('Outlet_3Delete/<int:id>/' , views.Outlet_3Delete , name ='Outlet_3Delete'),
    path('Outlet_3Edit/<int:id>/' , views.Outlet_3Edit , name = 'Outlet_3Edit'),
    path('Outlet_3viewdata/<int:id>/' ,views.Outlet_3viewdata , name ='Outlet_3viewdata'),
    
    path('Outlet_4List/' , views.Outlet_4List , name ='Outlet_4List'),
    path('Outlet_4Entry/' , views.Outlet_4Entry , name = 'Outlet_4Entry'),
    path('Outlet_4Delete/<int:id>/' , views.Outlet_4Delete , name ='Outlet_4Delete'),
    path('Outlet_4Edit/<int:id>/' , views.Outlet_4Edit , name = 'Outlet_4Edit'),
    path('Outlet_4viewdata/<int:id>/',views.Outlet_4viewdata , name = 'Outlet_4viewdata'), 
    
    path('Outlet_5List/' , views.Outlet_5List , name ='Outlet_5List'),
    path('Outlet_5Entry/' , views.Outlet_5Entry , name = 'Outlet_5Entry'),
    path('Outlet_5Delete/<int:id>/' , views.Outlet_5Delete , name ='Outlet_5Delete'),
    path('Outlet_5Edit/<int:id>/' , views.Outlet_5Edit , name = 'Outlet_5Edit'), 
    path('Outlet_5viewdata/<int:id>/' ,views.Outlet_5viewdata , name ='Outlet_5viewdata'),  
    
       
    path('Total_FBList/' , views.Total_FBList , name ='Total_FBList'),
    path('Total_FBEntry/' , views.Total_FBEntry , name = 'Total_FBEntry'),
    path('Total_FBDelete/<int:id>/',views.Total_FBDelete , name='Total_FBDelete'),
    
      
    path('PL_RoomsList/' , views.PL_RoomsList , name ='PL_RoomsList'),
    path('PL_RoomsEntry/' , views.PL_RoomsEntry , name = 'PL_RoomsEntry'),
    path('PL_RoomsDelete/<int:id>/' , views.PL_RoomsDelete , name ='PL_RoomsDelete'),
    path('PL_RoomsEdit/<int:id>/' , views.PL_RoomsEdit , name = 'PL_RoomsEdit'),   
    path('PL_Roomsviewdata/<int:id>/' , views.PL_Roomsviewdata , name = 'PL_Roomsviewdata'),
    
        
    path('PL_SummaryList/' , views.PL_SummaryList , name = 'PL_SummaryList'),
    path('PL_SummaryEntry/', views.PL_SummaryEntry , name = 'PL_SummaryEntry'),
    path('PL_SummaryDelete/<int:id>/', views.PL_SummaryDelete , name ='PL_SummaryDelete'),
    path('PL_SummaryEdit/<int:id>/',views.PL_SummaryEdit , name ='PL_SummaryEdit'),
    path('PL_Summaryviewdata/<int:id>/' ,views.PL_Summaryviewdata , name = 'PL_Summaryviewdata'),
    
    
      
    
    
]