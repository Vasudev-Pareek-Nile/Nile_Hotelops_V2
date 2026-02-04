from django.urls import path
from .import views 
from .views import LocationListView, DepartmentListView, PositionListView,PositionListAllView,submit_resume
from .Mobile_Api import *

urlpatterns = [
       path('OpenPositionAdd/',views.OpenPositionAdd,name="OpenPositionAdd"),
       path('OpenPositionList/',views.OpenPositionList,name="OpenPositionList"),
       path('OpenPositionDelete/',views.OpenPositionDelete,name="OpenPositionDelete"),
       path('edit-position/<int:position_id>/', views.EditOpenPosition, name='EditOpenPosition'),
       path('get-job-description/', views.get_job_description, name='get_job_description'),
       path('PositionsPdf/', views.PositionsPdf, name='PositionsPdf'),
       path('toggle-position-status/<int:position_id>/', views.toggle_position_status, name='toggle_position_status'),
       path('ExportOpenPosition/', views.ExportOpenPosition, name='ExportOpenPosition'),

      # path('fetch_resume_data/', views.fetch_resume_data, name='fetch_resume_data'),
      # path('get_action_counts/', views.get_action_counts, name='get_action_counts'),
      path('locations/', LocationListView.as_view(), name='location-list'),
      path('departments/', DepartmentListView.as_view(), name='department-list'),
      path('positions/', PositionListView.as_view(), name='position-list'),
      path('positions_list/', PositionListAllView.as_view(), name='position-list-all'),
      path('submit-resume/', views.resume_submission_page, name='submit_resume_with_slug'),

      path('api/job-details/', views.job_details_view, name='job-details'),
      path('api/get_department_action_counts/', views.get_department_action_counts,     name='get_department_action_counts'),
      path('api/submit-resume/', views.submit_resume, name='submit_resume'),
      path('perform_action/', views.perform_action, name='perform_action'), 

      path('ResumeShorting/', views.ResumeShorting, name='ResumeShorting'),
      path('view_Resume/', views.view_Resume, name='view_Resume'),
      path('view_Profile_Resume/', views.view_Profile_Resume, name='view_Profile_Resume'),
       
      path('get_resume_details/<int:resume_id>/', views.get_resume_details, name='get_resume_details'),

   
      path('edit_resume/<int:resume_id>/<int:PageNumber>/<str:isTraining>/', views.edit_resume, name='edit_resume'),
      path('Qrcodegenerated/', views.Qrcodegenerated, name='Qrcodegenerated'),
      path('send_notification_sms/<int:notification_id>/', views.send_notification_sms, name='send_notification_sms'),
      path('qr_download/<int:qr_id>/', views.qr_download, name='qr_download'),
      path('Notification_Schedule/', views.Notification_Schedule, name='Notification_Schedule'),
      path('Notification_Schedule_list/', views.Notification_Schedule_list, name='Notification_Schedule_list'),
      path('Notification_Schedule/delete/<int:id>/', views.delete_notification_schedule, name='delete_notification_schedule'),
      
      # Mobile api
      path("api/open-positions/", Open_Position_List_Mobile_API.as_view(), name="open-position-list"),
]
