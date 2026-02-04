from django.urls import path,include
from .views import *
from .models import *


urlpatterns = [
    path("", AdvanceSalaryHome, name="AdvanceSalaryLetter"),
    path("download_Advance_Salary_pdf", download_Advance_Salary_pdf, name="download_Advance_Salary_pdf"),
]
