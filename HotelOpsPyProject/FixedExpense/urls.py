from django.urls import path
from .import views

urlpatterns = [
    # path('APITest/' , views.APITest , name = 'APITest'),
    path('FixedExpenseHotelYearlyReport/' , views.FixedExpenseHotelYearlyReport , name = 'FixedExpenseHotelYearlyReport'),
    path('FixedExpenseHotelCombineMontlyReport/' , views.FixedExpenseHotelCombineMontlyReport , name = 'FixedExpenseHotelCombineMontlyReport'),
    path('FixedExpenseList/' , views.FixedExpenseList , name = 'FixedExpenseList'),
    path('FixedExpenseEntry/' ,views.FixedExpenseEntry , name= 'FixedExpenseEntry'),
    path('delete_FixedExpense/<int:id>/' , views.delete_FixedExpense , name ='delete_FixedExpense'),
    path('FixedExpenseEdit/<int:id>/' ,views.FixedExpenseEdit , name = 'FixedExpenseEdit'),
    path('FixedExpenseView/<int:id>/', views.FixedExpenseviewdata , name = 'FixedExpenseView'),
    # path('FixedExpenseManageMaster/' , views.FixedExpenseManageMaster , name = 'FixedExpenseManageMaster'),
    # path('update_order/', views.update_order, name='update_order')
    
]
