from django.urls import path
from .views import EmployeeJoining,EmployeeITRequest,EmployeeUniformRequest,Notification,EmployeeUniformRequestHOD,EmployeeITRequestHOD
urlpatterns = [
     path('EmployeeJoining/',EmployeeJoining,name='EmployeeJoining'),
     path('Notification/',Notification,name='Notification'),
     
     path('EmployeeITRequest/',EmployeeITRequest,name='EmployeeITRequest'),
     path('EmployeeUniformRequest/',EmployeeUniformRequest,name='EmployeeUniformRequest'),
     path('EmployeeUniformRequestHOD/',EmployeeUniformRequestHOD,name='EmployeeUniformRequestHOD'),
     path('EmployeeITRequestHOD/',EmployeeITRequestHOD,name='EmployeeITRequestHOD'),





]
