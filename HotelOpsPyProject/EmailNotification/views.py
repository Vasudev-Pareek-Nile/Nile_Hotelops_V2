# from django.shortcuts import redirect
# from django.http import JsonResponse
# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage
# from django.conf import settings
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from app.models import OrganizationMaster, EmployeeMaster 
# from hotelopsmgmtpy.GlobalConfig import MasterAttribute

# @api_view(['POST'])
# def EmployeeJoining(request):
   
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     token = request.headers.get('hotel-api-token')
#     if token != hotelapitoken:
#         return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)
    
   
   
    
#     try:
#         NileID = 3 
#         organization = OrganizationMaster.objects.get(OrganizationID=NileID)
#         OrganizationLogo = organization.OrganizationLogo
#     except OrganizationMaster.DoesNotExist:
#         return Response({"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)

#     EmployeeCode = request.data.get('EmployeeCode')
   
#     OrganizationID = request.data.get('OrganizationID')
  
#     if not EmployeeCode:
#         return Response({"error": "EmployeeCode is required"}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         EmployeeDetails = EmployeeMaster.objects.get(
#             EmployeeCode=EmployeeCode,
#             OrganizationID=OrganizationID,
#             IsDelete=False
#         )
#     except EmployeeMaster.DoesNotExist:
#         return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

#     EmployeeName = EmployeeDetails.EmpName
#     ReportingtoDesigantion = EmployeeDetails.ReportingtoDesigantion

#     try:
#         HodDetails = EmployeeMaster.objects.get(
#             OrganizationID=OrganizationID,
#             IsDelete=False,
#             Designation=ReportingtoDesigantion
#         )
#     except EmployeeMaster.DoesNotExist:
#         return Response({"error": "HOD not found"}, status=status.HTTP_404_NOT_FOUND)

#     HodEmailOffical = [HodDetails.OfficalMailAddress]
#     EmployeeEmailOffical = EmployeeDetails.OfficalMailAddress
#     EmployeeEmail = EmployeeDetails.EmailMailAddress

#     subject = 'New employee has joined in our organization'
#     Heading = 'New employee has joined in our organization'

#     message = render_to_string('Joining/EmployeeJoining.html', {
#         'EmployeeName': EmployeeName,
       
#         'Department': EmployeeDetails.Department,
#         'Designation': EmployeeDetails.Designation,
#         'OrganizationLogo': OrganizationLogo,
#         'Heading': Heading,
#         'JoiningDate': EmployeeDetails.DateofJoining
#     })

#     email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, HodEmailOffical)
#     email.content_subtype = "html"

#     try:
#         email.send()
#         print("Email sent successfully.")
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#         return Response({"error": f"Failed to send email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     return Response({"success": "Email sent successfully."}, status=status.HTTP_200_OK)






# import json

# @api_view(['POST'])
# def EmployeeITRequest(request):
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     token = request.headers.get('hotel-api-token')
#     if token != hotelapitoken:
#         return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)
    
#     try:
#         NileID = 3
#         organization = OrganizationMaster.objects.get(OrganizationID=NileID)
#         OrganizationLogo = organization.OrganizationLogo
#     except OrganizationMaster.DoesNotExist:
#         return Response({"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)

#     EmployeeCode = request.data.get('EmployeeCode')
#     OrganizationID = request.data.get('OrganizationID')

#     if not EmployeeCode:
#         return Response({"error": "EmployeeCode is required"}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         EmployeeDetails = EmployeeMaster.objects.get(
#             EmployeeCode=EmployeeCode,
#             OrganizationID=OrganizationID,
#             IsDelete=False
#         )
#     except EmployeeMaster.DoesNotExist:
#         return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

#     EmployeeName = EmployeeDetails.EmpName
#     ReportingtoDesigantion = EmployeeDetails.ReportingtoDesigantion

#     try:
#         HodDetails = EmployeeMaster.objects.get(
#             OrganizationID=OrganizationID,
#             IsDelete=False,
#             Designation=ReportingtoDesigantion
#         )
#     except EmployeeMaster.DoesNotExist:
#         return Response({"error": "HOD not found"}, status=status.HTTP_404_NOT_FOUND)

#     HodEmailOffical = [HodDetails.OfficalMailAddress]
#     EmployeeEmailOffical = EmployeeDetails.OfficalMailAddress
#     EmployeeEmail = EmployeeDetails.EmailMailAddress

#     subject = 'Request for IT Equipment'
#     Heading = 'New IT Equipment Request'

  
   

#     message = render_to_string('IT/EmployeeITRequest.html', {
#         'EmployeeName': EmployeeName,
      
#         'Department': EmployeeDetails.Department,
#         'Designation': EmployeeDetails.Designation,
#         'OrganizationLogo': OrganizationLogo,
#         'Heading': Heading,
#         'JoiningDate': EmployeeDetails.DateofJoining,
       
#     })

#     email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, HodEmailOffical)
#     email.content_subtype = "html"

#     try:
#         email.send()
#         print("Email sent successfully.")
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#         return Response({"error": f"Failed to send email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     return Response({"success": "Email sent successfully."}, status=status.HTTP_200_OK)










# @api_view(['POST'])
# def EmployeeUniformRequest(request):
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     token = request.headers.get('hotel-api-token')
#     if token != hotelapitoken:
#         return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)
    
#     try:
#         NileID = 3
#         organization = OrganizationMaster.objects.get(OrganizationID= NileID)
#         OrganizationLogo = organization.OrganizationLogo
#     except OrganizationMaster.DoesNotExist:
#         return Response({"error": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)

#     EmployeeCode = request.data.get('EmployeeCode')
#     OrganizationID = request.data.get('OrganizationID')

#     if not EmployeeCode:
#         return Response({"error": "EmployeeCode is required"}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         EmployeeDetails = EmployeeMaster.objects.get(
#             EmployeeCode=EmployeeCode,
#             OrganizationID=OrganizationID,
#             IsDelete=False
#         )
#     except EmployeeMaster.DoesNotExist:
#         return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

#     EmployeeName = EmployeeDetails.EmpName
#     ReportingtoDesigantion = EmployeeDetails.ReportingtoDesigantion

#     try:
#         HodDetails = EmployeeMaster.objects.get(
#             OrganizationID=OrganizationID,
#             IsDelete=False,
#             Designation=ReportingtoDesigantion
#         )
#     except EmployeeMaster.DoesNotExist:
#         return Response({"error": "HOD not found"}, status=status.HTTP_404_NOT_FOUND)

#     HodEmailOffical = [HodDetails.OfficalMailAddress]
#     EmployeeEmailOffical = EmployeeDetails.OfficalMailAddress
#     EmployeeEmail = EmployeeDetails.EmailMailAddress

#     subject = 'Request for Uniform'
#     Heading = 'New Uniform Request'

    
   

#     message = render_to_string('Housekeeping/EmployeeUniformRequest.html', {
#         'EmployeeName': EmployeeName,
        
#         'Department': EmployeeDetails.Department,
#         'Designation': EmployeeDetails.Designation,
#         'OrganizationLogo': OrganizationLogo,
#         'Heading': Heading,
#         'JoiningDate': EmployeeDetails.DateofJoining,
       
#     })

#     email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, HodEmailOffical)
#     email.content_subtype = "html"

#     try:
#         email.send()
#         print("Email sent successfully.")
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#         return Response({"error": f"Failed to send email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     return Response({"success": "Email sent successfully."}, status=status.HTTP_200_OK)


from django.shortcuts import redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.models import OrganizationMaster, EmployeeMaster
from .models import NotificationMessageDump
from hotelopsmgmtpy.GlobalConfig import MasterAttribute ,OrganizationDetail
import logging
from app.views import EmployeeDataSelect,EmployeeUserLoginTokenMobile,HOD_Details
logger = logging.getLogger(__name__)
import urllib.parse
NILE_ID = 3
INVALID_API_TOKEN_ERROR = {"error": "Invalid API token"}
ORGANIZATION_NOT_FOUND_ERROR = {"error": "Organization not found"}
EMPLOYEE_NOT_FOUND_ERROR = {"error": "Employee not found"}
HOD_NOT_FOUND_ERROR = {"error": "HOD not found"}
EMPLOYEE_CODE_REQUIRED_ERROR = {"error": "EmployeeCode is required"}

def validate_token(request):
    hotel_api_token = MasterAttribute.HotelAPIkeyToken
    token = request.headers.get('hotel-api-token')
    return token == hotel_api_token

def get_organization_logo():
    try:
        organization = OrganizationMaster.objects.get(OrganizationID=NILE_ID)
        return organization.OrganizationLogo
    except OrganizationMaster.DoesNotExist:
        return None





def save_notification(subject, message, email_list,ModuleName,AppTitle,AppBody,OrganizationID,UserID,AppUserID):
    try:
        notification = NotificationMessageDump(
            ModuleName=ModuleName,
            EmailMessageBody=message,
            AppUserID = AppUserID,
            AppTitle=AppTitle,
            AppBody=AppBody,
            DashboardTitle=subject,
            DashboardBody=subject,
            RetrunUrl='' ,
            OrganizationID= OrganizationID,
            CreatedBy = UserID
        )
        notification.set_emails(email_list)
        notification.save()
    except Exception as e:
        logger.error(f"Failed to save notification: {e}")




from firebase_admin import messaging
def send_fcm_notification(token, title, body):
  
  
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=token,
    )
    response = messaging.send(message)
    print('Successfully sent FCM message', response)


@api_view(['POST'])
def EmployeeJoining(request):
    if not validate_token(request):
        return JsonResponse(INVALID_API_TOKEN_ERROR, status=status.HTTP_403_FORBIDDEN)

    organization_logo = get_organization_logo()
    if organization_logo is None:
        return Response(ORGANIZATION_NOT_FOUND_ERROR, status=status.HTTP_404_NOT_FOUND)

    EmployeeCode = request.data.get('EmployeeCode')
    OrganizationID = request.data.get('OrganizationID')
    UserID = request.data.get('UserID')
    if not EmployeeCode:
        return Response(EMPLOYEE_CODE_REQUIRED_ERROR, status=status.HTTP_400_BAD_REQUEST)

  
   
    EmployeeDetails  = EmployeeDataSelect(EmployeeCode=EmployeeCode,OrganizationID=OrganizationID)
   
    if EmployeeDetails:


            EmployeeName = EmployeeDetails[0]['EmpName']
            ReportingtoDesigantion = EmployeeDetails[0]['ReportingtoDesigantion']

    
    HodDetails = EmployeeDataSelect(OrganizationID=OrganizationID,ReportingtoDesignation=ReportingtoDesigantion)
  
    if HodDetails:


        HodEmailOffical = [HodDetails[0]['OfficalMailAddress']]
        HodEmployeeCode = HodDetails[0]['EmployeeCode']
        print(HodEmployeeCode)
    

        subject = 'New employee has joined in our organization'
        Heading = 'New employee has joined in our organization'

        message = render_to_string('Joining/EmployeeJoining.html', {
            'EmployeeName': EmployeeName,
            'Department': EmployeeDetails[0]['Department'],
            'Designation': EmployeeDetails[0]['Designation'],
            'OrganizationLogo': organization_logo,
            'Heading': Heading,
            'JoiningDate': EmployeeDetails[0]['DateofJoining']
        })

        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, HodEmailOffical)
        email.content_subtype = "html"

        try:
            email.send()
            logger.info("Email sent successfully.")
            ModuleName = "HR"
        

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return Response({"error": f"Failed to send email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
           
            fcmobj = EmployeeUserLoginTokenMobile(OrganizationID=OrganizationID,EmployeeCode=HodEmployeeCode)
            fcm_token = fcmobj[0]['Token']
         
            AppUserID = fcmobj[0]['UserID']
          
            logger.info("Notification sent successfully.")     
            notification_title = 'New employee'
            notification_body = f'{EmployeeName} has joined as.'+EmployeeDetails[0]['Designation']

            send_fcm_notification(fcm_token, notification_title, notification_body)
        except Exception as e:
            logger.error(f"Failed to send Notification: {e}")
            return Response({"error": f"Failed to send notification: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        save_notification(subject, message, HodEmailOffical,ModuleName,AppTitle= notification_title ,AppBody =  notification_body,OrganizationID=OrganizationID,UserID=UserID,AppUserID = AppUserID)
        return Response({"success": "Notification sent successfully."}, status=status.HTTP_200_OK)








@api_view(['POST'])
def EmployeeITRequestHOD(request):
    if not validate_token(request):
        return JsonResponse(INVALID_API_TOKEN_ERROR, status=status.HTTP_403_FORBIDDEN)

    organization_logo = get_organization_logo()
    if organization_logo is None:
        return Response(ORGANIZATION_NOT_FOUND_ERROR, status=status.HTTP_404_NOT_FOUND)

    EmployeeCode = request.data.get('EmployeeCode')
    OrganizationID = request.data.get('OrganizationID')
    UserID = request.data.get('UserID')
    if not EmployeeCode:
        return Response(EMPLOYEE_CODE_REQUIRED_ERROR, status=status.HTTP_400_BAD_REQUEST)

  
   
    EmployeeDetails  = EmployeeDataSelect(EmployeeCode=EmployeeCode,OrganizationID=OrganizationID)
   
    if EmployeeDetails:


            EmployeeName = EmployeeDetails[0]['EmpName']
            ReportingtoDesigantion = EmployeeDetails[0]['ReportingtoDesigantion']

    
    HodDetails = EmployeeDataSelect(OrganizationID=OrganizationID,ReportingtoDesignation=ReportingtoDesigantion)
  
    if HodDetails:


        HodEmailOffical = [HodDetails[0]['OfficalMailAddress']]
        HodEmployeeCode = HodDetails[0]['EmployeeCode']
        print(HodEmployeeCode)
    

        subject = f'IT request  for  {EmployeeName}'
        Heading = f'IT request  for  {EmployeeName}'

        message = render_to_string('IT/EmployeeITRequestHOD.html', {
            'EmployeeName': EmployeeName,
            'Department': EmployeeDetails[0]['Department'],
            'Designation': EmployeeDetails[0]['Designation'],
            'OrganizationLogo': organization_logo,
            'Heading': Heading,
            'JoiningDate': EmployeeDetails[0]['DateofJoining']
        })

        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, HodEmailOffical)
        email.content_subtype = "html"

        try:
            email.send()
            logger.info("Email sent successfully.")
            ModuleName = "HR"
        

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return Response({"error": f"Failed to send email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
           
            fcmobj = EmployeeUserLoginTokenMobile(OrganizationID=OrganizationID,EmployeeCode=HodEmployeeCode)
            fcm_token = fcmobj[0]['Token']
         
            AppUserID = fcmobj[0]['UserID']
          
            logger.info("Notification sent successfully.")     
            notification_title = 'IT request'
            notification_body = f'IT request  for  {EmployeeName}.'

            send_fcm_notification(fcm_token, notification_title, notification_body)
        except Exception as e:
            logger.error(f"Failed to send Notification: {e}")
            return Response({"error": f"Failed to send notification: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        save_notification(subject, message, HodEmailOffical,ModuleName,AppTitle= notification_title ,AppBody =  notification_body,OrganizationID=OrganizationID,UserID=UserID,AppUserID = AppUserID)
        return Response({"success": "Notification sent successfully."}, status=status.HTTP_200_OK)



from HumanResources.views import EmployeeCardDetails

@api_view(['POST'])
def EmployeeUniformRequestHOD(request):
    if not validate_token(request):
        return JsonResponse(INVALID_API_TOKEN_ERROR, status=status.HTTP_403_FORBIDDEN)

    organization_logo = get_organization_logo()
    if organization_logo is None:
        return Response(ORGANIZATION_NOT_FOUND_ERROR, status=status.HTTP_404_NOT_FOUND)

    EmployeeCode = request.data.get('EmployeeCode')
    OrganizationID = request.data.get('OrganizationID')
    UserID = request.data.get('UserID')
    if not EmployeeCode:
        return Response(EMPLOYEE_CODE_REQUIRED_ERROR, status=status.HTTP_400_BAD_REQUEST)

  
   
    EmployeeDetails  = EmployeeDataSelect(EmployeeCode=EmployeeCode,OrganizationID=OrganizationID)
   
    if EmployeeDetails:


            EmployeeName = EmployeeDetails[0]['EmpName']
            ReportingtoDesigantion = EmployeeDetails[0]['ReportingtoDesigantion']

    
    HodDetails = EmployeeDataSelect(OrganizationID=OrganizationID,ReportingtoDesignation=ReportingtoDesigantion)
  
    if HodDetails:


        HodEmailOffical = [HodDetails[0]['OfficalMailAddress']]
        HodEmployeeCode = HodDetails[0]['EmployeeCode']
        print(HodEmployeeCode)
    

        subject = f'Uniform approval request  for  {EmployeeName}'
        Heading = f'Uniform approval request  for  {EmployeeName}'

        message = render_to_string('Housekeeping/EmployeeUniformRequestHOD.html', {
            'EmployeeName': EmployeeName,
            'Department': EmployeeDetails[0]['Department'],
            'Designation': EmployeeDetails[0]['Designation'],
            'OrganizationLogo': organization_logo,
            'Heading': Heading,
            'JoiningDate': EmployeeDetails[0]['DateofJoining']
        })

        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, HodEmailOffical)
        email.content_subtype = "html"

        try:
            email.send()
            logger.info("Email sent successfully.")
            ModuleName = "HR"
        

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return Response({"error": f"Failed to send email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
           
            fcmobj = EmployeeUserLoginTokenMobile(OrganizationID=OrganizationID,EmployeeCode=HodEmployeeCode)
            fcm_token = fcmobj[0]['Token']
         
            AppUserID = fcmobj[0]['UserID']
          
            logger.info("Notification sent successfully.")     
            notification_title = 'Uniform  approval request'
            notification_body = f'Uniform approval request  for  {EmployeeName}.'

            send_fcm_notification(fcm_token, notification_title, notification_body)
        except Exception as e:
            logger.error(f"Failed to send Notification: {e}")
            return Response({"error": f"Failed to send notification: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        save_notification(subject, message, HodEmailOffical,ModuleName,AppTitle= notification_title ,AppBody =  notification_body,OrganizationID=OrganizationID,UserID=UserID,AppUserID = AppUserID)
        return Response({"success": "Notification sent successfully."}, status=status.HTTP_200_OK)






@api_view(['POST'])
def EmployeeITRequest(request):
   
    if not validate_token(request):
        return JsonResponse(INVALID_API_TOKEN_ERROR, status=status.HTTP_403_FORBIDDEN)

    organization_logo = get_organization_logo()
    if organization_logo is None:
        return Response(ORGANIZATION_NOT_FOUND_ERROR, status=status.HTTP_404_NOT_FOUND)

    EmployeeCode = request.data.get('EmployeeCode')
    OrganizationID = request.data.get('OrganizationID')
    UserID = request.data.get('UserID')
    if not EmployeeCode:
        return Response(EMPLOYEE_CODE_REQUIRED_ERROR, status=status.HTTP_400_BAD_REQUEST)

  
   
    EmployeeDetails  = EmployeeDataSelect(EmployeeCode=EmployeeCode,OrganizationID=OrganizationID)
   
    if EmployeeDetails:


            EmployeeName = EmployeeDetails[0]['EmpName']
            # ReportingtoDesigantion = EmployeeDetails[0]['ReportingtoDesigantion']
    IT_Levels = ['M2', 'M', 'E', 'A']
                                                                    
    for Level in IT_Levels:
        HodDetails = HOD_Details(OrganizationID=OrganizationID, Department='INFORMATION & SYSTEMS', Level=Level)
        
        if HodDetails:
            break
        

    if HodDetails:

        print(HodDetails[0]['EmpName'])
        HodEmailOffical = [HodDetails[0]['OfficalMailAddress']]
        HodEmployeeCode = HodDetails[0]['EmployeeCode']
        subject = 'Request for IT Equipment'
        Heading = 'New IT Equipment Request'
       
       
       
       

      
        message = render_to_string('IT/EmployeeITRequest.html', {
            'EmployeeName': EmployeeName,
            'Department': EmployeeDetails[0]['Department'],
            'Designation': EmployeeDetails[0]['Designation'],
            'OrganizationLogo': organization_logo,
            'Heading': Heading,
            'JoiningDate': EmployeeDetails[0]['DateofJoining'],
           
        })

        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, HodEmailOffical)
        email.content_subtype = "html"

        try:
            email.send()
            logger.info("Email sent successfully.")
            ModuleName = "IT"
        

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return Response({"error": f"Failed to send email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        try:
            fcmobj = EmployeeUserLoginTokenMobile(OrganizationID=OrganizationID,EmployeeCode=HodEmployeeCode)
            fcm_token = fcmobj[0]['Token']
            AppUserID = fcmobj[0]['UserID']
            logger.info("Notification sent successfully.")     
            notification_title = 'New IT Request'
            notification_body = f'New IT Equipment Request for {EmployeeName}.'

            send_fcm_notification(fcm_token, notification_title, notification_body)
        except Exception as e:
            logger.error(f"Failed to send Notification: {e}")
            return Response({"error": f"Failed to send notification: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        save_notification(subject, message, HodEmailOffical,ModuleName,AppTitle= notification_title ,AppBody =  notification_body,OrganizationID=OrganizationID,UserID=UserID,AppUserID = AppUserID)
        return Response({"success": "Email sent successfully."}, status=status.HTTP_200_OK)






@api_view(['POST'])
def EmployeeUniformRequest(request):


    if not validate_token(request):
        return JsonResponse(INVALID_API_TOKEN_ERROR, status=status.HTTP_403_FORBIDDEN)

    organization_logo = get_organization_logo()
    if organization_logo is None:
        return Response(ORGANIZATION_NOT_FOUND_ERROR, status=status.HTTP_404_NOT_FOUND)

    EmployeeCode = request.data.get('EmployeeCode')
    OrganizationID = request.data.get('OrganizationID')
    UserID = request.data.get('UserID')
    if not EmployeeCode:
        return Response(EMPLOYEE_CODE_REQUIRED_ERROR, status=status.HTTP_400_BAD_REQUEST)

  
   
    EmployeeDetails  = EmployeeDataSelect(EmployeeCode=EmployeeCode,OrganizationID=OrganizationID)
   
    if EmployeeDetails:


            EmployeeName = EmployeeDetails[0]['EmpName']
            # ReportingtoDesigantion = EmployeeDetails[0]['ReportingtoDesigantion']
    Housekeeping_Levels = ['M2','M1','M']
                                                                    
    for Level in Housekeeping_Levels:
        HodDetails = HOD_Details(OrganizationID=OrganizationID, Department='Housekeeping', Level=Level)
      
        if HodDetails:
            break
            

    if HodDetails:

        print(HodDetails[0]['EmpName'])
        HodEmailOffical = [HodDetails[0]['OfficalMailAddress']]
        HodEmployeeCode = HodDetails[0]['EmployeeCode']
       
        subject = 'Request for Uniform'
        Heading = 'New Uniform Request'

        returnurl= ''
        message = render_to_string('Housekeeping/EmployeeUniformRequest.html', {
            'EmployeeName': EmployeeName,
            'Department': EmployeeDetails[0]['Department'],
            'Designation': EmployeeDetails[0]['Designation'],
            'OrganizationLogo': organization_logo,
            'Heading': Heading,
            'JoiningDate': EmployeeDetails[0]['DateofJoining'],
            'returnurl': returnurl
        })

        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, HodEmailOffical)
        email.content_subtype = "html"

        try:
            email.send()
            logger.info("Email sent successfully.")
            ModuleName = "Uniform"
        

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return Response({"error": f"Failed to send email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        try:
          
            fcmobj = EmployeeUserLoginTokenMobile(OrganizationID=OrganizationID,EmployeeCode=HodEmployeeCode)
           
            fcm_token = fcmobj[0]['Token']
            AppUserID = fcmobj[0]['UserID']
            logger.info("Notification sent successfully.")     
            notification_title = 'New Uniform Request'
            notification_body = f'New Uniform Request for {EmployeeName}.'

            send_fcm_notification(fcm_token, notification_title, notification_body)
        except Exception as e:
            logger.error(f"Failed to send Notification: {e}")
            return Response({"error": f"Failed to send notification: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        save_notification(subject, message, HodEmailOffical,ModuleName,AppTitle= notification_title ,AppBody =  notification_body,OrganizationID=OrganizationID,UserID=UserID,AppUserID = AppUserID)
        return Response({"success": "Email sent successfully."}, status=status.HTTP_200_OK)





@api_view(['GET'])
def Notification(request):
    try:
        if not validate_token(request):
            return JsonResponse(INVALID_API_TOKEN_ERROR, status=status.HTTP_403_FORBIDDEN)
        
        OrganizationID = request.query_params.get('OrganizationID')
         
        AppUserID = request.query_params.get('AppUserID')

        if not AppUserID:
            return Response({'error': 'AppUserID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            notifications = NotificationMessageDump.objects.filter(OrganizationID=OrganizationID,AppUserID= AppUserID,IsDelete=False).order_by('-id')
        except NotificationMessageDump.DoesNotExist:
            return Response({'error': 'No notifications found for the given OrganizationID'}, status=status.HTTP_404_NOT_FOUND)

        NotificationData = [{'id':no.id,'AppTitle': no.AppTitle, 'AppBody': no.AppBody,'Date':no.CreatedDateTime} for no in notifications]

        return Response(NotificationData)
    
    except Exception as e:
        
        return Response({'error': 'An error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


