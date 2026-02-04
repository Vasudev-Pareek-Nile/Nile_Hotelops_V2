from django.urls import path
from .views import *

urlpatterns = [
    path('', Ranking_Board_View, name='Ranking_Board'),
    path('Ranking_Board_Entry_View/', Ranking_Board_Entry_View, name='Ranking_Board_Entry_View'),
    path('api/hotel-ranking/', hotel_ranking_api, name='hotel-ranking-api'),
]
 

 