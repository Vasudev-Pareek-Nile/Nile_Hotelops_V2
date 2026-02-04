from django.urls import path
from .import views

urlpatterns = [
   path('homeMedia/',views.homeMedia,name='homeMedia'),
   path('view_download_Media/<int:id>/',views.view_download_Media,name='view_download_Media'),
   path('media_delete/<int:id>/',views.media_delete,name='media_delete'),
    path('edit_media/<int:id>/',views.edit_media,name='edit_media'),
   path('upload_media/',views.upload_media,name='upload_media'),
   path('download_media/<int:id>/<str:resolution>/', views.download_media, name='download_media'),

]
 