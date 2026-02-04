from django.urls import path
from .import views

urlpatterns = [
    path('homepage/' , views.homepage , name ='homepage'),
    
    path('FixedSigList/' , views.FixedSigList , name = 'FixedSigList'),
    # path('delete_FixedSig/<int:id>/' ,views.delete_FixedSig , name='delete_FixedSig'),
    path('FixedSigEntry/' , views.FixedSigEntry , name='FixedSigEntry'),
    # path('FixedSigEdit/<int:id>/' , views.FixedSigEdit , name='FixedSigEdit'),
    # path('FixedSigView/<int:id>/' ,views.FixedSigView , name= 'FixedSigView'),
    
    path('ProImpPlanList/' , views.ProImpPlanList , name = 'ProImpPlanList'),
    path('ProImpPlanEntry/' , views.ProImpPlanEntry , name='ProImpPlanEntry'),
    
    
    path('SnagEntry/' , views.SnagEntry , name = 'SnagEntry'),
    path('SnagSectionEntry/<int:id>/' , views.SnagSectionEntry , name = 'SnagSectionEntry'),
    path('SnagList/' , views.SnagList , name = 'SnagList'),
    path('ReportPendingTask/' , views.ReportPendingTask , name = 'ReportPendingTask'),
    path('ReportPendingTaskExport/' , views.ReportPendingTaskExport , name = 'ReportPendingTaskExport'),

    
    
    path('SnagListEntry/<int:id>/' , views.SnagListEntry , name='SnagListEntry'),
    path('delete_SnagList/<int:id>/' ,views.delete_SnagList , name='delete_SnagList'),
    path('SnagListEdit/<int:id>/' , views.SnagListEdit , name='SnagListEdit'),
    path('SectionMasterList' , views.SectionMasterList , name = 'SectionMasterList'),
    path('SectionMasterEntry' , views.SectionMasterEntry , name = 'SectionMasterEntry'),
    path('SectionMasterEdit/<int:id>/' , views.SectionMasterEdit , name = 'SectionMasterEdit'),
    path('delete_Divison/<int:id>/', views.delete_Divison , name = 'delete_Divison'),
    path('delete_Section/<int:id>/' , views.delete_Section , name = 'delete_Section'),
    path('DivisonEdit/<int:id>/' , views.DivisonEdit , name = 'DivisonEdit'),
    path('DivisionEntry' , views.DivisionEntry , name = 'DivisionEntry'),
    path('DivisonMasterList' , views.DivisonMasterList , name = 'DivisonMasterList'),
    
    # path('SnagListView/<int:id>/' ,views.SnagListView , name= 'SnagListView'),
    
    
    path('ProImpProcessList/' ,views.ProImpProcessList ,name = 'ProImpProcessList'),
    path('ProImpProcessEntry/' ,views.ProImpProcessEntry ,name = 'ProImpProcessEntry'),
    path('ProImpProcessEdit/<int:id>/' ,views.ProImpProcessEdit ,name = 'ProImpProcessEdit'),
    path('delete_ProImpProcess/<int:id>/' ,views.delete_ProImpProcess ,name = 'delete_ProImpProcess'),
    path('ProImpProcessView/<int:id>/' , views.ProImpProcessView , name='ProImpProcessView'),
    
    path('HotelHandoverList/' ,views.HotelHandoverList ,name = 'HotelHandoverList'),
    path('HotelHandoverEntry/' ,views.HotelHandoverEntry ,name = 'HotelHandoverEntry'),
]
