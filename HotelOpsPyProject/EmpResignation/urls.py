from django.urls import path
from .views import EmpResigantionDelete,EmpResigantionPDF,EmpResigantionList,EmpResigantionEntry

urlpatterns = [
    path('EmpResigantionEntry',EmpResigantionEntry,name='EmpResigantionEntry'),
    path("EmpResigantionList/",EmpResigantionList,name="EmpResigantionList"),
    path("EmpResigantionDelete/",EmpResigantionDelete,name="EmpResigantionDelete"),
    path("EmpResigantionPDF/",EmpResigantionPDF,name="EmpResigantionPDF"),
]