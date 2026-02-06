from django.urls import path
# from .views import HotelKRAStandardList, KraList,KraAdd,TargetAssign,KraEnrty,TargetAssignList,KraYearlyReport,KRAViewSet,kra_page, kra_standard_page, organization_list, get_kra_yearly_report_json, Delete_Targeted_Assign
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .Mobile_Api import *

router = DefaultRouter()
router.register(r'kra', KRAViewSet, basename='kra')



urlpatterns = [
    path('api/', include(router.urls)), 
    path('kra-page/', kra_page, name='kra_page'),
    path("kra-standard/", kra_standard_page,name='kra_standard'),
    path('api/organizations/', organization_list),
    path('api/hotel-kra/<int:org_id>/', HotelKRAStandardList.as_view()),
    path('api/hotel-kra/', HotelKRAStandardList.as_view()),  # POST
    path("Kra/",KraList,name='KraList'),
    path("KraAdd/",KraAdd,name='KraAdd'),
    path("KraEnrty/",KraEnrty,name='KraEnrty'),
    path("TargetAssign/",TargetAssign,name='TargetAssign'),
    path("TargetAssignList/",TargetAssignList,name='TargetAssignList'),
    path("KraYearlyReport/",KraYearlyReport,name='KraYearlyReport'),
    path("KraYearlyReportPrevious/",KraYearlyReportPrevious,name='KraYearlyReportPrevious'),

    # New Urls
    path("Delete_Targeted_Assign/",Delete_Targeted_Assign,name='Delete_Targeted_Assign'),
    
        # new api url
    path('api/kra-yearly-previous-report/<int:organization_id>/<str:employee_code>/<int:selected_year>/', get_kra_yearly_previous_report_json),
    path('api/kra-yearly-report/<str:organization_id>/<str:employee_code>/<str:from_year_str>/<str:to_year_str>/', get_kra_yearly_report_json),


    # path('Yearly_Report_Generate_Pdf/', Yearly_Report_Generate_Pdf, name='Yearly_Report_Generate_Pdf')
    
    
    path('api/kra-summary/', kra_summary_api, name='kra-summary'),
    path('api/kra-entry-select/', kra_entry_select_api, name='kra-entry-select'),
    path('api/kra-entry-PDF-api/', kra_entry_PDF_api, name='kra-entry-PDF-api'),
    path("Bulk_TargetAssign/",Bulk_TargetAssign,name='Bulk_TargetAssign'),


    path('api/kra-target-summary/', kra_target_summary_api, name='kra-target-summary'),
    path('api/kra-target-detail/', kra_target_detail_api, name='kra-target-detail'),


    path('api/kra-target-summary-Exp/', kra_target_summary_Exp_api, name='kra-target-summary-Exp'),
    # path('api/Kra_Entry_mobile_api/', Kra_Entry_mobile_api, name='Kra_Entry_mobile_api'),
    # path('api/Kra_Entry_mobile_api_revised/', Kra_Entry_mobile_api_revised, name='Kra_Entry_mobile_api_revised'),
    
    
    path("KRA_Target_Report_View/", KRA_Target_Report_View, name="KRA_Target_Report_View"),
    path("api/KRA_Target_Report_Api/", KRA_Target_Report_Api_View.as_view(), name="KRA_Target_Report_Api_View"),
]
