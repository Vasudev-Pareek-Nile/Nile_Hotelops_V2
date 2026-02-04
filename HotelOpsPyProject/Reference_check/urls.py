from django.urls import path
from .import views
urlpatterns = [

     path('Reference_add/<str:unique_link>/', views.Reference_add, name='Reference_add'),
    
     path('Reference_delete/',views.Reference_delete,name="Reference_delete"),
     path('Reference_report/',views.Reference_report,name="Reference_report"),
     path('Reference_pdf/',views.Reference_pdf,name="Reference_pdf"),

     path('search/', views.search_autocomplete, name='search_autocomplete'),
     
     path('designation-autocomplete/', views.designation_autocomplete, name='designation-autocomplete'),

     path('thanku/',views.thanku,name="thanku"),
     path('already/',views.already,name="already"),

       
    path('references/filter/', views.reference_filter, name='reference_filter'),
   path('Reference_form/', views.Reference_form, name='Reference_form'),
   path('Referenceformlist/', views.Referenceformlist, name='Referenceformlist'),
   path('ReferenceCheckView/', views.ReferenceCheckView, name='ReferenceCheckView'),





   
]