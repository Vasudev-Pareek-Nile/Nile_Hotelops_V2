from django.urls import path
from .import views

urlpatterns = [
    path('',views.home_view,name=''),
    
    path('EmpTerminationEntry/', views.EmpTerminationEntry,name='EmpTerminationEntry'),
    path("EmpTerminationList/",views.EmpTerminationList,name="EmpTerminationList"),
    path("EmpTerminationDelete/",views.EmpTerminationDelete,name="EmpTerminationDelete"),
    path("EmpTerminationPDF/",views.EmpTerminationPDF,name="EmpTerminationPDF"),
]