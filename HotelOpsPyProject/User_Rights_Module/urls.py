from django.urls import path
from .import views


urlpatterns = [
    path("User_Rights_View/",views.User_Rights_View,name="User_Rights_View"),
    path("User_Rights_Form_Handle/",views.User_Rights_Form_Handle, name="User_Rights_Form_Handle"),
]
