from django.urls import path
from .views import Exit_Add,Exit_list,Exitdelete,Exit_Detail,Exit_Edit
urlpatterns = [
     path('Exit_Add/',Exit_Add,name="Exit_Add"),
     path('Exit_list/',Exit_list,name="Exit_list"),
     path('Exitdelete/',Exitdelete,name="Exitdelete"),
      path('exit/detail/<int:exit_id>/', Exit_Detail, name='exit_detail'),
      path('exit/edit/', Exit_Edit, name='Exit_Edit'),
]
