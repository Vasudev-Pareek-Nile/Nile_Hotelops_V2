from django.urls import path
from .views import *

urlpatterns = [
  path('FullandFinalEntry',FullandFinalEntry,name='FullandFinalEntry'),
  path('FullandFinalList',FullandFinalList,name='FullandFinalList'),
  path('FullandFinalDelete',FullandFinalDelete,name='FullandFinalDelete'),
  path('FullandFinalPdfView',FullandFinalPdfView,name='FullandFinalPdfView'),


  path('FullAndFinal_Approval_List/',FullAndFinal_Approval_List,name='FullAndFinal_Approval_List'),
  path('Upload_Auditor_Approval_Upload_File/',Upload_Auditor_Approval_Upload_File,name='Upload_Auditor_Approval_Upload_File'),
  path('Auditor_Approval__Download_File/', Auditor_Approval_Download_File, name="Auditor_Approval__Download_File"),
    path('Auditor_Approval_Repalce_File/', Auditor_Approval_Repalce_File, name="Auditor_Approval_Repalce_File"),
  
  
  # path("FullandFinalExcelView/", FullandFinalExcelView, name="FullandFinalExcelView"),


  path('fandf/all/', get_all_fandf),
  path('fandf/get/', get_fandf_by_emp),
  path('fandf/get_oid/', get_fandf_by_OID),
]
