from django.urls import path
from .import views
urlpatterns = [
    path('Master_Add/',views.Master_Add,name="Master_Add"),
    path('Master_list/',views.Master_list,name="Master_list"),
    path('Master_delet/',views.Master_delet,name="Master_delet"),



    path('Master_location1/',views.Master_location1,name="Master_location1"),
   


    path('add_project/',views.add_project,name="add_project"),

    path('list_project/',views.list_project,name="list_project"),
    path('project_delet/',views.project_delet,name="project_delet"),

    path('project_pdf/',views.project_pdf,name="project_pdf"),

    # front of tha house
    path('Front_ad/',views.Front_ad,name="Front_ad"),
    path('front_add/',views.front_add,name="front_add"),
    path('front/',views.front,name="front"),


    path('Front_admin_list/',views.Front_admin_list,name="Front_admin_list"),
    path('front_delet/',views.front_delet,name="front_delet"),

    path('Front_list/',views.Front_list,name="Front_list"),


    path('admin/',views.admin,name="admin"),
    path('admin_list/',views.admin_list,name="admin_list"),
    path('admin_delet/',views.admin_delet,name="admin_delet"),


    path('admin_subchild_list/',views.admin_subchild_list,name="admin_subchild_list"),
    path('admin_subchild_add/',views.admin_subchild_add,name="admin_subchild_add"),
    path('admin_subchild_delet/',views.admin_subchild_delet,name="admin_subchild_delet"),
    

    path('admin_child_list/',views.admin_child_list,name="admin_child_list"),
     path('admin_child_add/',views.admin_child_add,name="admin_child_add"),
     path('admin_child_delete/',views.admin_child_delete,name="admin_child_delete"),


     path('front_pdf/',views.front_pdf,name="front_pdf"),

      path('publicarea/',views.publicarea,name="publicarea"),
      path('publicarea_list/',views.publicarea_list,name="publicarea_list"),

      path('administrative_add/',views.administrative_add,name="administrative_add"),
      path('administrative_list/',views.administrative_list,name="administrative_list"),
    
    #  Notes admin
   
path('notes1_add/',views.notes1_add,name="notes1_add"),
path('notes1_list/',views.notes1_list,name="notes1_list"),

path('Notes2_add/',views.Notes2_add,name="Notes2_add"),
path('Notes2_list/',views.Notes2_list,name="Notes2_list"),


path('notes3_add/',views.notes3_add,name="notes3_add"),
path('notes3_list/',views.notes3_list,name="notes3_list"),

path('notes4_add/',views.notes4_add,name="notes4_add"),
path('notes4_list/',views.notes4_list,name="notes4_list"),

path('notes5_add/',views.notes5_add,name="notes5_add"),
path('notes5_list/',views.notes5_list,name="notes5_list"),
    




]
