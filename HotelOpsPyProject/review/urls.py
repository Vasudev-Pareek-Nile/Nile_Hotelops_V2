from django.urls import path
from . import views
from django.urls import re_path
urlpatterns = [
   
    path('upload/', views.upload_file, name='upload_file'),
    path('show_data', views.show_data, name='show_data'),
    path('', views.show_data, name='show_data'),
    path("selectOrganization", views.selectOrganization, name="selectOrganization"),
    # path('search/', search_results, name='search_results'),
    path('feedback/', views.feedback, name="feedback"),
    re_path(r'^reviews/(?P<OrganizationID>\d+)?/?$', views.upload_data_detail, name='upload_data_detail'),
    path('check-review-software/<str:org_id>/', views.check_review_software, name='check_review_software'),
]
