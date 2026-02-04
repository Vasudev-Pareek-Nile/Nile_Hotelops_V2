from django.urls import path

from .import views
urlpatterns = [
      path('YearlyBudget_list',views.YearlyBudget_list,name='YearlyBudget_list'),
     
      path('YearlyBudget_Entry_Details',views.YearlyBudget_Entry_Details,name='YearlyBudget_Entry_Details'),
      path('YearlyBudget_View/<int:id>',views.YearlyBudget_View,name='YearlyBudget_View'),

]
