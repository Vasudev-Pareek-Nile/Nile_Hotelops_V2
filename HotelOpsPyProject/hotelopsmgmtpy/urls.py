"""hotelopsmgmtpy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

# from django.conf.urls import handler404
# from django.conf.urls import handler500
# from django.shortcuts import render

# def custom_404_view(request, exception):
#     return render(request, 'HumanResources/templates/HR/Error_Page/error-404.html', status=404)

# def custom_500_view(request, exception):
#     return render(request, 'HumanResources/templates/HR/Error_Page/error-404.html', status=500)

# # HumanResources\templates\HR\Error_Page\error-404.html

# handler404 = custom_404_view
# handler500 = custom_404_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('app.urls')),
    path("casualmanpower/",include('casualmanpower.urls')),
    path("cleranceform/",include('cleranceform.urls')),
    path("uniforminventorysheet/",include('uniforminventorysheet.urls')),
    path("masterlineninventory/",include('masterlineninventory.urls')),
    path("cakeorder/",include('cakeorder.urls')),
    path("FullandFinalSettlement/",include('FullandFinalSettlement.urls')),
    path("EmpResignation/",include('EmpResignation.urls')),
    path("EmpTermination/",include('EmpTermination.urls')),
    path("EmpAbsconding/",include('EmpAbsconding.urls')),
    path("FixedExpense/",include('FixedExpense.urls')),
    # path("SalesWeeklyReview/",include('SalesWeeklyReview.urls')),
    # path("HBudgetReport/",include('HBudgetReport.urls')),
    path("PreOpeningDoc/",include('PreOpeningDoc.urls')),
    path("HotelBudget/",include('HotelBudget.urls')),
    path("TrainingAssessment/",include('TrainingAssessment.urls')),
    path("HrEvent/",include('HrEvent.urls')),
    path("ModRoasterCalendar/",include('ModRoasterCalendar.urls')),
    path("SalesEventCalendar/",include('SalesEventCalendar.urls')),
    path("LETTER_OF_WORK_EXPERIENCE/",include('LETTER_OF_WORK_EXPERIENCE.urls')),
    path("LetteofPromotion/",include('LetteofPromotion.urls')),
    path("LETTEROFAPPOINTMENT/",include('LETTEROFAPPOINTMENT.urls')),
    path("LetterOfConfirmation/",include('LetterOfConfirmation.urls')),
    path("Letterofintent/",include('Letterofintent.urls')),
    path("LetterSalaryIncrement/",include('LetterSalaryIncrement.urls')),
    path("EmailReader/",include('EmailReader.urls')),
    path("Manning_Guide/",include('Manning_Guide.urls')),

    path("YearlyBudget/",include('YearlyBudget.urls')),
    path("Leave_Management_System/",include('Leave_Management_System.urls')),
    path("Guest_reviews/",include('Guest_reviews.urls')),
    path("Hiring_Reporting_Performance_Review_Guidelines/",include('Hiring_Reporting_Performance_Review_Guidelines.urls')),
    path("Agreement/",include('Agreement.urls')),
    path("NewProgram/",include('NewProgram.urls')),
    path("Employee_Payroll/",include('Employee_Payroll.urls')),
    path("Project_Approvel_Templates/",include('Project_Approvel_Templates.urls')),
    path("pacer/",include('pacer.urls')),
    path("IT_Inventory/",include('IT_Inventory.urls')),
    path("review/",include('review.urls')),
    path("dashboard/",include('dashboard.urls')),
    path("InterviewAssessment/",include('InterviewAssessment.urls')),
    path("Reference_check/",include('Reference_check.urls')),
    path("HumanResources/",include('HumanResources.urls')),
    path("ProbationConfirmation/",include('ProbationConfirmation.urls')),
    path("EmailNotification/",include('EmailNotification.urls')),
    path("IT/",include('IT.urls')),
    path("PADP/",include('PADP.urls')),
    path("UniformInventory/",include('UniformInventory.urls')),
    path("Salary_Correction/",include('Salary_Correction.urls')),

    path("Manning_Guide/",include('Manning_Guide.urls')),
    path("Job_Description/",include('Job_Description.urls')),
    path("Open_position/",include('Open_position.urls')),
    path("ExitInterview/",include('ExitInterview.urls')),

    path("Warning_Letters/",include('Warning_Letters.urls')),
    path("Clearance_From/",include('Clearance_From.urls')),
    path("Checklist_Issued/",include('Checklist_Issued.urls')),

    path("KRA/",include('KRA.urls')),
    path("CodeOfConduct/",include('CodeOfConduct.urls')),

    path("Url/",include('PublicAccess.urls')),
    path("RevealingLetter/",include('RevealingLetter.urls')),



    path("GuestVoice/",include('GuestVoice.urls')),
    path("AMC_Renewal/",include('AMC_Renewal.urls')),
    path("AdvanceSalaryForm/",include('AdvanceSalaryForm.urls')),
    path("Travel_Details/",include('Travel_Details.urls')),
    path("Salary_Structure/",include('Salary_Structure.urls')),
    path("User_Rights_Module/",include('User_Rights_Module.urls')),

    path("Upload_Resume/",include('Upload_Resume.urls')),
    path("Ranking_Board/",include('Ranking_Board.urls')),
    path("HR_Inventory/",include('HR_Inventory.urls')),
    path("HR_Inventory/",include('HR_Inventory.urls')),
    path("Letter_Of_Trainees_Experience/",include('Letter_Of_Trainees_Experience.urls')),
    path("Policy_Data_Privacy/",include('Policy_Data_Privacy.urls')),
    path("Debit_Note/",include('Debit_Note.urls')),
    path("Policy_Posh/",include('Policy_Posh.urls')),
    path("Indemnity_Accommodation/",include('Indemnity_Accommodation.urls')),

    # path("Employee_Personal_Dashboard/",include('Employee_Personal_Dashboard.urls')),
    # path("HR_Dashboard/",include('HR_Dashboard.urls')),

    
    # path('api/', include('GuestVoice.urls')),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
#   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
