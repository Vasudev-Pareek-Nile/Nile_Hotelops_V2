from django.urls import path
from .views import InterviewAssementCandidateDetails,view_file,UserTypeList,UserTypeAddEdit,UserTypeDelete,DepartmentLevelConfigAddEdit,DepartmentLevelConfigDelete,DepartmentLevelConfigList,DepartmentLevelConfigDetailsAdd,InterviewAssessmentDelete,UpdateLOIStatus,ResignationStatus,FactorList,FactorsAdd,FactorDelete,LevelWiseGrid,GenerateDataLink,get_location_details,get_ifsc_details,Reference,InterviewAssementCEO,InterviewAssessmentView,CandidateDataForm,CandidatePersonalData,CandidateFamilyinfoPage,CandidateEmergencyinfoPage,CandidateQualificationinfoPage,CandidatePreviousWorkinfoPage,CandidateAddressinfoPage,CandidateIdentityinfoPage,CandidateBankinfoPage,CandidateDocumentinfoPage,ReGenerateDataLink,notification_page,RejectInterviewAssement,LetterofIntent,CloseInterviewAssement,InterviewAssessmentPdf

from .Mobile_Api_View import *


from .IA import InterviewAssessmentCreate,InterviewAssessmentList

urlpatterns = [
    path('InterviewAssessmentList/',InterviewAssessmentList,name='InterviewAssessmentList'),
    path('',InterviewAssessmentList,name='InterviewAssessmentList'),

    path('InterviewAssessmentCreate/',InterviewAssessmentCreate,name='InterviewAssessmentCreate'),
    path('InterviewAssessmentDelete/',InterviewAssessmentDelete,name='InterviewAssessmentDelete'),
    
    path('RejectInterviewAssement/',RejectInterviewAssement,name='RejectInterviewAssement'),
    path('CloseInterviewAssement/',CloseInterviewAssement,name='CloseInterviewAssement'),

    
    path('LetterofIntent/',LetterofIntent,name='LetterofIntent'),




    path('UpdateLOIStatus/',UpdateLOIStatus,name='UpdateLOIStatus'),
    path('ResignationStatus/',ResignationStatus,name='ResignationStatus'),

   
    
    path('GenerateDataLink/', GenerateDataLink, name='GenerateDataLink'),
    path('ReGenerateDataLink/', ReGenerateDataLink, name='ReGenerateDataLink'),

    
   

    path('get_location/', get_location_details, name='get_location_details'),
    path('get_ifsc_details/', get_ifsc_details, name='get_ifsc_details'),

    path('InterviewAssementCandidateDetails/',InterviewAssementCandidateDetails,name='InterviewAssementCandidateDetails'),
    path('view_file/', view_file, name='view_file'),
    
    path('UserTypeList/', UserTypeList, name='UserTypeList'),
    path('UserTypeAddEdit/', UserTypeAddEdit, name='UserTypeAddEdit'),
    path('UserTypeDelete/', UserTypeDelete, name='UserTypeDelete'),

    path('DepartmentLevelConfigAddEdit/', DepartmentLevelConfigAddEdit, name='DepartmentLevelConfigAddEdit'),
    path('DepartmentLevelConfigDelete/', DepartmentLevelConfigDelete, name='DepartmentLevelConfigDelete'),
    path('DepartmentLevelConfigList/', DepartmentLevelConfigList, name='DepartmentLevelConfigList'),
    
    path('DepartmentLevelConfigDetailsAdd/', DepartmentLevelConfigDetailsAdd, name='DepartmentLevelConfigDetailsAdd'),
    path('FactorList/', FactorList, name='FactorList'),
    path('FactorsAdd/', FactorsAdd, name='FactorsAdd'),
    
    path('FactorDelete/', FactorDelete, name='FactorDelete'),
    path('LevelWiseGrid/', LevelWiseGrid, name='LevelWiseGrid'),
    path('Reference/', Reference, name='Reference'),

    path('InterviewAssementCEO/', InterviewAssementCEO, name='InterviewAssementCEO'),
    
    path('InterviewAssessmentView/', InterviewAssessmentView, name='InterviewAssessmentView'),
    path('InterviewAssessmentPdf/', InterviewAssessmentPdf, name='InterviewAssessmentPdf'),


    # Candidate Data

    path('CandidateDataForm/', CandidateDataForm, name='CandidateDataForm'),
    path('CandidatePersonalData/', CandidatePersonalData, name='CandidatePersonalData'),
    path('CandidateFamilyinfoPage/', CandidateFamilyinfoPage, name='CandidateFamilyinfoPage'),
    
    path('CandidateEmergencyinfoPage/', CandidateEmergencyinfoPage, name='CandidateEmergencyinfoPage'),
    path('CandidateQualificationinfoPage/', CandidateQualificationinfoPage, name='CandidateQualificationinfoPage'),
    path('CandidatePreviousWorkinfoPage/', CandidatePreviousWorkinfoPage, name='CandidatePreviousWorkinfoPage'),
    path('CandidateAddressinfoPage/', CandidateAddressinfoPage, name='CandidateAddressinfoPage'),

    path('CandidateIdentityinfoPage/', CandidateIdentityinfoPage, name='CandidateIdentityinfoPage'),

    path('CandidateBankinfoPage/', CandidateBankinfoPage, name='CandidateBankinfoPage'),
    path('CandidateDocumentinfoPage/', CandidateDocumentinfoPage, name='CandidateDocumentinfoPage'),

 
    path('notification/<str:case_type>/', notification_page, name='notification_page'),


    # New Urls --  Mobile APi's
    # InterviewAssessment_Mobile_List_Api
    # path('InterviewAssessment_Mobile_List_Api/', InterviewAssessment_Mobile_List_Api, name='InterviewAssessment_Mobile_List_Api'),
    # path('/interview-assessments-list/', InterviewAssessment_Mobile_List_Api, name='interview-assessments-list-api'),
    # path('/InterviewAssessment_Mobile_List_Api_my/', InterviewAssessment_Mobile_List_Api_my, name='InterviewAssessment_Mobile_List_Api_my')
    # path('InterviewAssessment_Mobile_List_Api_my/', InterviewAssessment_Mobile_List_Api_my, name='InterviewAssessment_Mobile_List_Api_my'),

    # path('InterviewAssessment_Mobile_List_Api/', InterviewAssessment_Mobile_List_Api, name='InterviewAssessment_Mobile_List_Api'),
    # path('InterviewAssessment_Mobile_Count_Api/', InterviewAssessment_Mobile_Count_Api, name='InterviewAssessment_Mobile_Count_Api'),

    path('InterviewAssessment_Filters_Api/', InterviewAssessment_Filters_Api, name='InterviewAssessment_Filters_Api'),
    path('InterviewAssessment_CEO_Action_Api/', InterviewAssessment_CEO_Action_Api, name='InterviewAssessment_CEO_Action_Api'),
    
    path('InterviewAssessment_Entire_List_Api/', InterviewAssessment_Entire_List_Api, name='InterviewAssessment_Entire_List_Api'),

    # path('generate-pdf/<int:id>/', generate_pdf_view, name='generate_pdf'),
    path('InterviewAssessment_Mobile_Api_Pdf/', InterviewAssessment_Mobile_Api_Pdf, name='InterviewAssessment_Mobile_Api_Pdf'),


    # ------- Tesiting 04-08-2025
    path('InterviewAssessment_Mobile_List_Api_Ceo_Pending/', InterviewAssessment_Mobile_List_Api_Ceo_Pending, name='InterviewAssessment_Mobile_List_Api_Ceo_Pending'),
    # path('InterviewAssessment_Mobile_List_Api_Total_Pending/', InterviewAssessment_Mobile_List_Api_Total_Pending, name='InterviewAssessment_Mobile_List_Api_Total_Pending'),
    path('InterviewAssessment_Mobile_List_Api_Ceo_Pending_Count_Api/', InterviewAssessment_Mobile_List_Api_Ceo_Pending_Count_Api, name='InterviewAssessment_Mobile_List_Api_Ceo_Pending_Count_Api'),
    # path('InterviewAssessment_Mobile_List_Api_Total_Pending_count/', InterviewAssessment_Mobile_List_Api_Total_Pending_count, name='InterviewAssessment_Mobile_List_Api_Total_Pending_count'),




    # ----  Revised Api for reducing time
    path('InterviewAssessment_Mobile_List_Api_Total_Pending_count_Revised/', InterviewAssessment_Mobile_List_Api_Total_Pending_count_Revised, name='InterviewAssessment_Mobile_List_Api_Total_Pending_count_Revised'),
    path('InterviewAssessment_Mobile_List_Api_Total_Pending_Revised/', InterviewAssessment_Mobile_List_Api_Total_Pending_Revised, name='InterviewAssessment_Mobile_List_Api_Total_Pending_Revised'),


    path('IA_Pending_Count_Api/', IA_Pending_Count_Api, name='IA_Pending_Count_Api'),
    path('IA_Total_Pending_Api/', IA_Total_Pending_Api, name='IA_Total_Pending_Api'),



    # path('InterviewAssessment_Mobile_List_Api_Total_Pending_Revised_Modified/', InterviewAssessment_Mobile_List_Api_Total_Pending_Revised_Modified, name='InterviewAssessment_Mobile_List_Api_Total_Pending_Revised'),
]
