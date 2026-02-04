from django.urls import path
from .import views
urlpatterns = [
     path('reviews_add/',views.reviews_add,name="reviews_add"),
     path('reviews_list/',views.reviews_list,name="reviews_list"),
     path('reviews_edit/',views.reviews_edit,name="reviews_edit"),
     path('Gm_list/',views.Gm_list,name="Gm_list"),
    
]