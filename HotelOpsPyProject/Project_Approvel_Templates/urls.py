from django.urls import path
from .import views
urlpatterns = [

    
   path('Project_add/',views.Project_add,name="Project_add"),
   path('Project_list/',views.Project_list,name="Project_list"),
   path('project_delete/',views.project_delete,name="project_delete"),
   path('pdf/',views.pdf,name="pdf"),


]