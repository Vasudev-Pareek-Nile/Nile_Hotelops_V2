from django.urls import path
from .import views

urlpatterns = [
    path('homepage/' , views.homepage , name ='homepage'),
    
    path('HPLUtilitiesList/' , views.HPLUtilitiesList , name = 'HPLUtilitiesList'),
    path('delete_HPLUtilities/<int:id>/' ,views.delete_HPLUtilities , name='delete_HPLUtilities'),
    path('HPLUtilitiesEntry/' , views.HPLUtilitiesEntry , name='HPLUtilitiesEntry'),
    path('HPLUtilitiesEdit/<int:id>/' , views.HPLUtilitiesEdit , name='HPLUtilitiesEdit'),
    path('HPLUtilitiesView/<int:id>/' ,views.HPLUtilitiesView , name= 'HPLUtilitiesView'),
    
    path('HEngList/', views.HEngList, name='HEngList'),
    path('HEngEntry/', views.HEngEntry, name = 'HEngEntry'),
    path('HEngListDelete/<int:id>/' , views.HEngListDelete , name = 'HEngListDelete'),
    path('HEngListEdit/<int:id>/' , views.HEngListEdit , name ='HEngListEdit'),
    path('HEngviewdata/<int:id>/' , views.HEngviewdata , name = 'HEngviewdata'),
    
    path('HSMList/' , views.HSMList, name = 'HSMList'),
    path('HSMEntry/' , views.HSMEntry , name = 'HSMEntry'),
    path('HSMDelete/<int:id>/' , views.HSMDelete , name = 'HSMDelete'),
    path('HSMEdit/<int:id>/' , views.HSMEdit , name = 'HSMEdit'), 
    path('HSMviewdata/<int:id>/' , views.HSMviewdata , name ='HSMviewdata'),      
       
    path('HITList/' , views.HITList , name = 'HITList'),
    path('HITEntry/' , views.HITEntry , name ='HITEntry'),
    path('HITDelete/<int:id>/' , views.HITDelete , name = 'HITDelete'),
    path('HITEdit/<int:id>/' , views.HITEdit , name ='HITEdit'),
    path('HITView/<int:id>/' , views.HITView , name = 'HITView'),
    
    
    path('HAG_SecurityList/' , views.HAG_SecurityList , name = 'HAG_SecurityList'),
    path('HAG_SecurityEntry/', views.HAG_SecurityEntry , name = 'HAG_SecurityEntry'),
    path('HAG_SecurityEdit/<int:id>/', views.HAG_SecurityEdit , name = 'HAG_SecurityEdit'),
    path('HAG_SecurityDelete/<int:id>/' , views.HAG_SecurityDelete , name = 'HAG_SecurityDelete'),
    path('HAG_Securityviewdata/<int:id>/' , views.HAG_Securityviewdata , name='HAG_Securityviewdata'),
    
    path('HAG_HRList/' , views.HAG_HRList , name ='HAG_HRList'),
    path('HAG_HREntry/' ,views.HAG_HREntry , name = 'HAG_HREntry'),
    path('HAG_HREdit/<int:id>/' , views.HAG_HREdit , name = 'HAG_HREdit'),
    path('HAG_HRDelete/<int:id>/' , views.HAG_HRDelete , name = 'HAG_HRDelete'),
    path('HAG_HRviewdata/<int:id>/' ,views.HAG_HRviewdata , name = 'HAG_HRviewdata'),
    
    path('HAG_AnalysisList/', views.HAG_AnalysisList , name = 'HAG_AnalysisList'),
    path('HAG_AnalysisEntry/' , views.HAG_AnalysisEntry , name = 'HAG_AnalysisEntry'),
    path('HAG_AnalysisDelete/<int:id>/' , views.HAG_AnalysisDelete , name ='HAG_AnalysisDelete'),
    path('HAG_AnalysisEdit/<int:id>/' , views.HAG_AnalysisEdit , name = 'HAG_AnalysisEdit'),
    path('HAG_Analysisviewdata/<int:id>/', views.HAG_Analysisviewdata , name ='HAG_Analysisviewdata'),
    
    path('HTotal_AGList/' , views.HTotal_AGList , name ='HTotal_AGList'), 
    path('HTotal_AGEntry/' , views.HTotal_AGEntry , name = 'HTotal_AGEntry'),
    path('HTotal_AGDelete/<int:id>/' , views.HTotal_AGDelete , name = 'HTotal_AGDelete/'),
    path('HTotal_AGEdit/<int:id>/' ,views.HTotal_AGEdit , name ='HTotal_AGEdit'),
    path('HTotal_AGviewdata/<int:id>/' , views.HTotal_AGviewdata , name='HTotal_AGviewdata'),
    
    path('HRental_IncomeList/' , views.HRental_IncomeList , name ='HRental_IncomeList'),
    path('HRental_IncomeEntry/' , views.HRental_IncomeEntry , name ='HRental_IncomeEntry'),
    path('HRental_IncomeDelete/<int:id>/' ,views.HRental_IncomeDelete , name ='HRental_IncomeDelete'),
    path('HRental_IncomeEdit/<int:id>/' , views.HRental_IncomeEdit , name ='HRental_IncomeEdit'),
    path('HRental_Incomeviewdata/<int:id>/', views.HRental_Incomeviewdata , name = 'HRental_Incomeviewdata'),
    
    
    path('MinorGuestList/' , views.MinorGuestList , name = 'MinorGuestList'),
    path('MinorGuestEntry/' , views.MinorGuestEntry , name ='MinorGuestEntry'),
    path('Minor_GuestEdit/<int:id>/' ,views.Minor_GuestEdit , name ='Minor_GuestEdit'),
    path('Minor_GuestDelete/<int:id>/',views.Minor_GuestDelete , name ='Minor_GuestDelete'),
    path('Minor_Guestviewdata/<int:id>/' ,views.Minor_Guestviewdata , name='Minor_Guestviewdata'),
    
    path('OODBusinessList/', views.OODBusinessList , name = 'OODBusinessList'),
    path('OODBusinessEntry/',views.OODBusinessEntry , name = 'OODBusinessEntry'),
    path('OODBusinessEdit/<int:id>/' , views.OODBusinessEdit , name = 'OODBusinessEdit'),
    path('OODBusiness_Delete/<int:id>/' ,views.OODBusiness_Delete , name = 'OODBusiness_Delete'),
    path('OODBusinessView/<int:id>/' ,views.OODBusinessView , name = 'OODBusinessView'),
    
    path('HOOD_LaundryList/' , views.HOOD_LaundryList , name = 'HOOD_LaundryList'),
    path('HOOD_LaundryEntry/', views.HOOD_LaundryEntry , name = 'HOOD_LaundryEntry'),
    path('HOOD_LaundryEdit/<int:id>' , views.HOOD_LaundryEdit , name = 'HOOD_LaundryEdit'),
    path('HOOD_LaundryDelete/<int:id>/' ,views.HOOD_LaundryDelete , name ='HOOD_LaundryDelete'),
    path('HOOD_Laundryviewdata/<int:id>/',views.HOOD_Laundryviewdata , name = 'HOOD_Laundryviewdata'),
    
    path('HOOD_TransportList/', views.HOOD_TransportList , name = 'HOOD_TransportList'),
    path('HOOD_TransportEntry/',views.HOOD_TransportEntry , name ='HOOD_TransportEntry'),
    path('HOOD_TransportEdit/<int:id>/',views.HOOD_TransportEdit , name = 'HOOD_TransportEdit'),
    path('HOOD_TransportDelete/<int:id>/', views.HOOD_TransportDelete , name = 'HOOD_TransportDelete'),
    path('HOOD_Transportviewdata/<int:id>/' , views.HOOD_Transportviewdata , name = 'HOOD_Transportviewdata'),
    
    
    path('HOOD_HealthList/' , views.HOOD_HealthList , name = 'HOOD_HealthList'),
    path('HOOD_HealthEntry/', views.HOOD_HealthEntry , name='HOOD_HealthEntry'),
    path('HOOD_HealthDelete/<int:id>/' , views.HOOD_HealthDelete , name ='HOOD_HealthDelete'),
    path('HOOD_HealthEdit/<int:id>/' , views.HOOD_HealthEdit , name = 'HOOD_HealthEdit'),
    path('HOOD_Healthviewdata/<int:id>/' , views.HOOD_Healthviewdata , name ='HOOD_Healthviewdata'),
     
     
    path('FB_ODCList/' ,views.FB_ODCList , name = 'FB_ODCList'),
    path('FB_ODCEntry/' , views.FB_ODCEntry , name = 'FB_ODCEntry'),
    path('FB_ODCDelete/<int:id>/' , views.FB_ODCDelete , name = 'FB_ODCDelete'),
    path('FB_ODCEdit/<int:id>/' , views.FB_ODCEdit , name = 'FB_ODCEdit'),
    path('FB_ODCView/<int:id>/' , views.FB_ODCView , name = 'FB_ODCView'),
    
    
    path('HFB_BanquetList/' , views.HFB_BanquetList , name = 'HFB_BanquetList'),
    path('HFB_BanquetEntry/', views.HFB_BanquetEntry , name = 'HFB_BanquetEntry'),
    path('FB_BanquetDelete/<int:id>/',views.FB_BanquetDelete , name = 'FB_BanquetDelete' ),
    path('HFB_BanquetEdit/<int:id>/', views.HFB_BanquetEdit , name = 'HFB_BanquetEdit'),
    path('HFB_BanquetView/<int:id>/', views.HFB_BanquetView , name = 'HFB_BanquetView'),
    
    path('FB_MiniBarList/' , views.FB_MiniBarList , name = 'FB_MiniBarList'),
    path('FB_MiniBarEntry/' , views.FB_MiniBarEntry , name = 'FB_MiniBarEntry'),
    path('FB_MiniBarDelete/<int:id>/' , views.FB_MiniBarDelete , name = 'FB_MiniBarDelete'),
    path('FB_MiniBarEdit/<int:id>/' , views.FB_MiniBarEdit , name = 'FB_MiniBarEdit'),
    path('FB_MiniBarView/<int:id>/',views.FB_MiniBarView , name = 'FB_MiniBarView'),
    
    
    path('HFB_IRDList/' , views.HFB_IRDList , name = 'HFB_IRDList'),
    path('HFB_IRDEntry/' , views.HFB_IRDEntry , name = 'HFB_IRDEntry'),
    path('HFB_IRDDelete/<int:id>/',views.HFB_IRDDelete , name = 'HFB_IRDDelete'),
    path('HFB_IRDEdit/<int:id>/', views.HFB_IRDEdit , name = 'HFB_IRDEdit'),
    path('HFB_IRDView/<int:id>/' , views.HFB_IRDView , name = 'HFB_IRDView'),
    
    path('HOutlet1_List/' , views.HOutlet1_List , name = 'HOutlet1_List'),
    path('HOutlet1_Entry/' , views.HOutlet1_Entry , name='HOutlet1_Entry'),
    path('HOutlet1_Delete/<int:id>/',views.HOutlet1_Delete , name = 'HOutlet1_Delete'),
    path('HOutlet1_Edit/<int:id>/' , views.HOutlet1_Edit , name = 'HOutlet1_Edit'),
    path('HOutlet1_View/<int:id>/', views.HOutlet1_View , name = 'HOutlet1_View'),
        
    path('HOutlet2_List/' , views.HOutlet2_List , name = 'HOutlet2_List'),
    path('HOutlet2_Entry/' , views.HOutlet2_Entry , name='HOutlet2_Entry'),
    path('HOutlet2_Delete/<int:id>/',views.HOutlet2_Delete , name = 'HOutlet2_Delete'),
    path('HOutlet2_Edit/<int:id>/' , views.HOutlet2_Edit , name = 'HOutlet2_Edit'),
    path('HOutlet2_View/<int:id>/', views.HOutlet2_View , name = 'HOutlet2_View'),
    
    
    path('HOutlet3_List/' , views.HOutlet3_List , name = 'HOutlet3_List'),
    path('HOutlet3_Entry/' , views.HOutlet3_Entry , name='HOutlet3_Entry'),
    path('HOutlet3_Delete/<int:id>/',views.HOutlet3_Delete , name = 'HOutlet3_Delete'),
    path('HOutlet3_Edit/<int:id>/' , views.HOutlet3_Edit , name = 'HOutlet3_Edit'),
    path('HOutlet3_View/<int:id>/', views.HOutlet3_View , name = 'HOutlet3_View'),
    
    
    path('HOutlet4_List/' , views.HOutlet4_List , name = 'HOutlet4_List'),
    path('HOutlet4_Entry/' , views.HOutlet4_Entry , name='HOutlet4_Entry'),
    path('HOutlet4_Delete/<int:id>/',views.HOutlet4_Delete , name = 'HOutlet4_Delete'),
    path('HOutlet4_Edit/<int:id>/' , views.HOutlet4_Edit , name = 'HOutlet4_Edit'),
    path('HOutlet4_View/<int:id>/', views.HOutlet4_View , name = 'HOutlet4_View'),
    
    path('HOutlet5_List/' , views.HOutlet5_List , name = 'HOutlet5_List'),
    path('HOutlet5_Entry/' , views.HOutlet5_Entry , name='HOutlet5_Entry'),
    path('HOutlet5_Delete/<int:id>/',views.HOutlet5_Delete , name = 'HOutlet5_Delete'),
    path('HOutlet5_Edit/<int:id>/' , views.HOutlet5_Edit , name = 'HOutlet5_Edit'),
    path('HOutlet5_View/<int:id>/', views.HOutlet5_View , name = 'HOutlet5_View'),
    
    path('PL_FB_Outlet_List/',views.PL_FB_Outlet_List , name = 'PL_FB_Outlet_List'),
    path('PL_FB_Outlet_Entry/' , views.PL_FB_Outlet_Entry , name = 'PL_FB_Outlet_Entry'),
    path('PL_FB_Outlet_Delete/<int:id>/',views.PL_FB_Outlet_Delete , name = 'PL_FB_Outlet_Delete'),
    path('PL_FB_Outlet_Edit/<int:id>/' ,views.PL_FB_Outlet_Edit , name = 'PL_FB_Outlet_Edit'),
    path('PL_FB_Outlet_View/<int:id>/' , views.PL_FB_Outlet_View , name = 'PL_FB_Outlet_View'),
    
    
    
    path('RoomWorkSheetEntry/' , views.RoomWorkSheetEntry , name='RoomWorkSheetEntry'),
    path('RoomWorksheet_List/', views.RoomWorksheet_List , name ='RoomWorksheet_List'),
    path('RoomWorksheet_Delete/<int:id>/' ,views.RoomWorksheet_Delete , name = 'RoomWorksheet_Delete'),
    path('RoomWorksheet_Edit/<int:id>/' , views.RoomWorksheet_Edit , name='RoomWorksheet_Edit'),
    path('RoomWorksheet_View/<int:id>/' , views.RoomWorksheet_View , name = 'RoomWorksheet_View'),
    
    
    path('HTotalFB_List/',views.HTotalFB_List , name = 'HTotalFB_List'),
    path('HTotalFB_Entry/' , views.HTotalFB_Entry , name = 'HTotalFB_Entry'),
    path('HTotalFB_Delete/<int:id>/' , views.HTotalFB_Delete , name = 'HTotalFB_Delete'),
    path('HTotalFB_Edit/<int:id>/' , views.HTotalFB_Edit , name = 'HTotalFB_Edit'),
    path('HTotalFB_View/<int:id>/' , views.HTotalFB_View , name = 'HTotalFB_View'),
    
    
    path('FB_WorksheetList/' , views.FB_WorksheetList , name = 'FB_WorksheetList'),
    path('FB_WorksheetEntry/' , views.FB_WorksheetEntry , name = 'FB_WorksheetEntry'),
    path('FB_WorksheetDelete/<int:id>/',views.FB_WorksheetDelete , name = 'FB_WorksheetDelete'),
    path('FB_WorksheetEdit/<int:id>/' , views.FB_WorksheetEdit , name = 'FB_WorksheetEdit'),
    path('FB_WorksheetView/<int:id>/' , views.FB_WorksheetView , name = 'FB_WorksheetView'),
    
    path('YearlyReport/' , views.YearlyReport , name = 'YearlyReport'),
]
