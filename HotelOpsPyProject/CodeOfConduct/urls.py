from django.urls import path
from .import views
urlpatterns = [
    
    path('codeconductlist/', views.codeconductlist, name='codeconductlist'),
    path('CodeDelete/', views.CodeDelete, name='CodeDelete'),
    path('upload/', views.upload_sample_file, name='upload_sample_file'),
    path('download/<int:doc_id>/', views.download_sample_file, name='download_sample_file'),
    path('download_pdf/<int:doc_id>/', views.download_sample_pdf_file, name='download_sample_pdf_file'),
    path('submit_emp_code_of_conduct/', views.submit_emp_code_of_conduct, name='submit_emp_code_of_conduct'),
    path('codeconduct/download/<int:conduct_id>/', views.download_codeconduct_file, name='download_codeconduct_file'),
    
    
    path('Employee_Details_Cover_Page_View/', views.Employee_Details_Cover_Page_View, name='Employee_Details_Cover_Page_View'),
]