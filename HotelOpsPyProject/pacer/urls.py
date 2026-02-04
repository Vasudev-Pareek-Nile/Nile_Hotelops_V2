from django.urls import path
from .import views

urlpatterns = [
    path('task_add/',views.task_add,name="task_add"),

    path('task_list/',views.task_list,name="task_list"),
    path('task_delet/',views.task_delet,name="task_delet"),
    path('updatestuts/',views.updatestuts,name="updatestuts"),

    path('filtertask/',views.filtertask,name="filtertask"),

    # path('masterlist/',views.masterlist,name="masterlist"),
     path('masteradd/',views.masteradd,name="masteradd"),
     path('masterlist/',views.masterlist,name="masterlist"),
     path('masterdelete/',views.masterdelete,name="masterdelete"),

 path('deshboard_hod/',views.deshboard_hod,name="deshboard_hod"),
   
    

    
  
]