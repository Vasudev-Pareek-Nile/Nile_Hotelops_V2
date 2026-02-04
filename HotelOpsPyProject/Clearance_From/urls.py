from django.urls import path
from .import views

urlpatterns = [
  
     path('MasterClearanceApproved/', views.MasterClearanceApproved,name='MasterClearanceApproved'),
     path('add-item/', views.add_item, name='add_item'),
     path('MasterClearanceItemDelete/', views.MasterClearanceItemDelete, name='MasterClearanceItemDelete'),

     path('MasterReturnlist/', views.MasterReturnlist, name='MasterReturnlist'),
     path('ReturnAdd/', views.ReturnAdd, name='ReturnAdd'),  
     path('ReturnEdit/', views.ReturnEdit, name='ReturnEdit'),  
     path('ClearanceDelete/', views.ClearanceDelete, name='ClearanceDelete'),
     path('edit-clearance/', views.edit_clearance, name='edit_clearance'),
     path('ClearanceFrom/', views.ClearanceFrom, name='ClearanceFrom'),
     path('ClearanceFromlist/', views.ClearanceFromlist, name='ClearanceFromlist'),
     path('ClearancefromDelete/', views.ClearancefromDelete, name='ClearancefromDelete'),
     path('ClearancePdf/', views.ClearancePdf, name='ClearancePdf'),
]