from django.urls import path
from .import views


urlpatterns = [
    path('homepage/' , views.homepage , name ='homepage'),
    
    
    path('MarketSegmentList/' , views.MarketSegmentList , name = 'MarketSegmentList'),
    path('MarketSegmentEntry/' ,views.MarketSegmentEntry , name='MarketSegmentEntry'),
    path('delete_MarketSegment/<int:id>/' , views.delete_MarketSegment , name ='delete_MarketSegment'),
    path('MarketSegmentEdit/<int:id>/' ,views.MarketSegmentEdit , name='MarketSegmentEdit'),
    path('MarketSegmentView/<int:id>/' ,views.MarketSegmentviewdata , name = 'MarketSegmentView'),
    
    
    path('SourceList/' , views.SourceList , name = 'SourceList'),
    path('SourceEntry/' , views.SourceEntry , name ='SourceEntry'),
    path('delete_Source/<int:id>/' ,views.delete_Source , name ='delete_Source'),
    path('SourceEdit/<int:id>/' , views.SourceEdit , name ='SourceEdit'),
    path('SourceView/<int:id>/' ,views.SourceView , name ='SourceView'),
    
    
    path('OTAList/' , views.OTAList , name ='OTAList'),
    path('OTAEntry/', views.OTAEntry , name='OTAEntry'),
    path('delete_OTA/<int:id>/' ,views.delete_OTA , name='delete_OTA'),
    path('OTAEdit/<int:id>/' , views.OTAEdit , name ='OTAEdit'),
    path('OTAView/<int:id>/' , views.OTAView , name = 'OTAView'),
    
    
    path('TravelAgentList/' , views.TravelAgentList , name = 'TravelAgentList'),
    path('TravelAgentEntry/' , views.TravelAgentEntry , name='TravelAgentEntry'),
    path('delete_TravelAgent/<int:id>/',views.delete_TravelAgent , name='delete_TravelAgent'),
    path('TravelAgentEdit/<int:id>/' , views.TravelAgentEdit , name='TravelAgentEdit'),
    path('TravelAgentView/<int:id>/' ,views.TravelAgentView , name='TravelAgentView'),
    
    
    path('CompanyProList/' , views.CompanyProList , name='CompanyProList'),
    path('CompanyProEntry/' , views.CompanyProEntry , name='CompanyProEntry'),
    path('delete_CompanyPro/<int:id>/' ,views.delete_CompanyPro , name ='delete_CompanyPro'),
    path('CompanyProEdit/<int:id>/' ,views.CompanyProEdit , name='CompanyProEdit'),
    path('CompanyProView/<int:id>/' , views.CompanyProView , name ='CompanyProView'),
  
]
