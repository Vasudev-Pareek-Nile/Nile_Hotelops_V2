from django.urls import path
from .import views
urlpatterns = [
    path('HiringAdd/',views.HiringAdd,name='HiringAdd'),
    path('Reporting_list/',views.Reporting_list,name='Reporting_list'),
    path('Reporting_delet/',views.Reporting_delet,name='Reporting_delet'),
    path('hiring_report/',views.hiring_report,name='hiring_report'),
    path('report_pdf/',views.report_pdf,name='report_pdf'),
  
]