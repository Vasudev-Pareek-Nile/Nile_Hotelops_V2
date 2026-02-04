from django.urls import path
from .views import ListSC,Correction,DeleteSC,ViewSC
urlpatterns = [
            path('',ListSC,name='ListSC'),
            
            path('ListSC/',ListSC,name='ListSC'),
            path('Correction/',Correction,name='Correction'),
            path('DeleteSC/',DeleteSC,name='DeleteSC'),

            path('ViewSC/',ViewSC,name='ViewSC'),



]
