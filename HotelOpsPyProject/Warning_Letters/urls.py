from django.urls import path
from .import views


urlpatterns = [
    
    path("WarningList/",views.WarningList,name="WarningList"),
    path("VerbalWarning/",views.VerbalWarning,name="VerbalWarning"),
    path("Written_Warning/",views.Written_Warning,name="Written_Warning"),
    path("FinalWarning/",views.FinalWarning,name="FinalWarning"),

    path("WarningPdf/",views.WarningPdf,name="WarningPdf"),
    path('warning_detail/', views.warning_detail_view, name='warning_detail'),


    path('verbal_warning_pdf/', views.verbal_warning_pdf, name='verbal_warning_pdf'),
    path('written_warning_pdf/', views.written_warning_pdf, name='written_warning_pdf'),
    path('final_warning_pdf/', views.final_warning_pdf, name='final_warning_pdf'),



    # New Warning Employee List
    path('Warning_Employee_List/', views.Warning_Employee_List, name='Warning_Employee_List'),
]
