from django.urls import path
from .import views


urlpatterns = [
    path("Upload_Resume_View/",views.Upload_Resume_View,name="Upload_Resume_View"),
    path("add_trainee/",views.add_trainee,name="add_trainee"),

    # path('Show_Department_Api/', views.Show_Department_Api, name='Show_Department_Api'),
    # path('Show_Designations_Api/', views.Show_Designations_Api, name='Show_Designations_Api'),

]
