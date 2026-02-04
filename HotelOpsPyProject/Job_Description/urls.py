from django.urls import path
from .import views
urlpatterns = [
    path('NewJobDescription',views.NewJobDescription,name="NewJobDescription"),
    path('JobDescriptionlist',views.JobDescriptionlist,name="JobDescriptionlist"),
    path('CopyJobDescription',views.CopyJobDescription,name="CopyJobDescription"),
    path('JobDescriptionPdf/id=<int:id>',views.JobDescriptionPdf,name="JobDescriptionPdf"),
    path('Mainpage',views.Mainpage,name="Mainpage"),
    path('jobs/<str:department_name>/', views.JobDescriptionListdepartment, name='JobDescriptionListdepartment'),
]