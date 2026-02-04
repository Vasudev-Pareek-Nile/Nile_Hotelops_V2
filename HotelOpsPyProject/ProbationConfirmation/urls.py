from django.urls import path
from .views import ListPC,NewPC,DeletePC,ViewPC,delete_goal,delete_objective
urlpatterns = [
    path('',ListPC,name="ListPC"),

    path('ListPC/',ListPC,name="ListPC"),
    path('NewPC/',NewPC,name="NewPC"),
    
    path('DeletePC/',DeletePC,name="DeletePC"),
    path('ViewPC/',ViewPC,name="ViewPC"),
    # path('submit_objectives/', submit_objectives, name='submit_objectives'),
    path('delete-objective/<int:objective_id>/', delete_objective, name='delete_objective'),
    path('delete-goal/<int:goal_id>/', delete_goal, name='delete_goal'),


    
]
