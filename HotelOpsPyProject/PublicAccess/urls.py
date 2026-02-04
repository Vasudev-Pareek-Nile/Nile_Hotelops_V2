from django.urls import path
from .views import Accept

urlpatterns = [
    path('Accept/<uuid:token>/', Accept, name='Accept'),
]
