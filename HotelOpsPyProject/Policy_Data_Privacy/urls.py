from django.urls import path
from .import views

urlpatterns = [
    path('Data_Privacy_Entry_Emp/',views.Data_Privacy_Entry_Emp,name='Data_Privacy_Entry_Emp'),
    path('Data_Privacy_Emp_List/',views.Data_Privacy_Emp_List,name='Data_Privacy_Emp_List'),
    
    path('Generate_Letter_of_Data_Privacy/',views.Generate_Letter_of_Data_Privacy,name='Generate_Letter_of_Data_Privacy'),
    path('Data_Privacy_Emp_Delete/',views.Data_Privacy_Emp_Delete,name='Data_Privacy_Emp_Delete'),

    path('Data_Privacy_Upload_File/', views.Data_Privacy_Upload_File, name="Data_Privacy_Upload_File"),
    path('Data_Privacy_Download_File/', views.Data_Privacy_Download_File, name="Data_Privacy_Download_File"),
    path('Data_Privacy_Repalce_File/', views.Data_Privacy_Repalce_File, name="Data_Privacy_Repalce_File"),
    
    
    # path("Editor/Editor_list/", views.Policy_Data_Privacy_list, name="Policy_Data_Privacy_list"),
    # path("Policy_Data_Privacy/create/", views.Create_Policy_Data_Privacy, name="Create_Policy_Data_Privacy"),
    # path("Policy_Data_Privacy/edit/<int:pid>/", views.Edit_Policy_Data_Privacy, name="Edit_Policy_Data_Privacy"),
    
    
    path("editor/list/", views.Editor_List_View, name="editor_list"),
    path("editor/create/", views.Editor_Create_View, name="editor_create"),
    path("editor/<int:pid>/edit/", views.Editor_Edit_View, name="editor_edit"),
]
