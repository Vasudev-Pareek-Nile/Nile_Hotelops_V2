from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from app.models import EmployeeMaster
from django.db import connection
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.models import OrganizationMaster
from EmailNotification.models import NotificationMessageDump
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
import logging
from app.views import EmployeeUserLoginTokenMobile,HOD_Details
from firebase_admin import messaging

logger = logging.getLogger(__name__)


# class Command(BaseCommand):
#     help = 'Send probation period ending notifications to HR managers'

#     def handle(self, *args, **kwargs):
#         OrganizationID = 1001
#         sql_query = """
#             SELECT EmpName, DATEADD(day, 180, DateofJoining) AS pDate 
#             FROM app_employeemaster 
#             WHERE OrganizationID = %s
#             AND YEAR(DATEADD(day, 180, DateofJoining)) = YEAR(GETDATE())
#             AND MONTH(DATEADD(day, 180, DateofJoining)) = MONTH(GETDATE());
#         """
#         with connection.cursor() as cursor:
#             cursor.execute(sql_query, [OrganizationID])
#             rows = cursor.fetchall()

#         employee_list = [{'EmpName': row[0], 'pDate': row[1]} for row in rows]
        
       
         
#         HR_Levels = ['M2', 'M', 'E']
                                                                    
#         for Level in HR_Levels:
#             HodDetails = HOD_Details(OrganizationID=OrganizationID,  Department='Human Resources', Level=Level)
          
#             if HodDetails:
#                 HrEmailsList =[HodDetails[0]['OfficalMailAddress']]
#                 print(HrEmailsList)
#                 break
        
#         self.send_email_to_hr(employee_list, HrEmailsList,OrganizationID,employee=HodDetails)

#         self.stdout.write(self.style.SUCCESS('Probation period notifications sent successfully.'))

#     def send_email_to_hr(self, employee_list, hr_manager_emails,OrganizationID,employee):
#         subject = 'Probation Upcoming Soon'
#         message = render_to_string('Probation/HRSendProbationNotifications.html', {'employee_list': employee_list})

#         try:
#             email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, hr_manager_emails)
#             email.content_subtype = 'html'  
#             email.send()
#             logger.info("Email sent successfully.")
#             ModuleName = "HR"
        
#         except Exception as e:
#             logger.error(f"Failed to send email: {e}")
#             return Response({"error": f"Failed to send email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

       


#         try:
#             fcmobj = EmployeeUserLoginTokenMobile(OrganizationID=OrganizationID, EmployeeCode=employee['EmployeeCode'])
#             fcm_token = fcmobj[0]['Token']
#             AppUserID = fcmobj[0]['UserID']
#             notification_title = 'Probation Period Ending Soon'
            
#             table_header = f"{'Employee Name':<20}{'Probation End Date':<20}\n"
#             table_body = "\n".join([f"{emp['EmpName']:<20}{emp['pDate'].strftime('%d-%m-%Y'):<20}" for emp in employee_list])
#             notification_body = f"The following employees' probation period is Ending soon:\n\n{table_header}{table_body}"
#             send_fcm_notification(fcm_token, notification_title, notification_body)
#             logger.info("Notification sent successfully.")
#         except Exception as e:
#             logger.error(f"Failed to send Notification: {e}")

#         save_notification(subject, message, email_list=hr_manager_emails, ModuleName='Hr', AppTitle=notification_title,
#                           AppBody=notification_body, OrganizationID=OrganizationID, AppUserID=AppUserID)













# def save_notification(subject, message, email_list, ModuleName, AppTitle, AppBody, OrganizationID, AppUserID):
#     try:
#         notification = NotificationMessageDump(
#             ModuleName=ModuleName,
#             EmailMessageBody=message,
#             AppUserID=AppUserID,
#             AppTitle=AppTitle,
#             AppBody=AppBody,
#             DashboardTitle=subject,
#             DashboardBody=subject,
#             RetrunUrl='',
#             OrganizationID=OrganizationID
#         )
#         notification.set_emails(email_list)
#         notification.save()
#     except Exception as e:
#         logger.error(f"Failed to save notification: {e}")


# from firebase_admin import messaging

# def send_fcm_notification(token, title, body):
#     message = messaging.Message(
#         notification=messaging.Notification(title=title, body=body),
#         token=token,
#     )
#     response = messaging.send(message)
#     print('Successfully sent FCM message', response)

class Command(BaseCommand):
    help = 'Send probation period ending notifications to HR managers'

    def handle(self, *args, **kwargs):
        
        # orgs = OrganizationMaster.objects.filter(IsDelete=False)
        
        # for org in orgs:
        #     OrganizationID = org.OrganizationID
        
            OrganizationID =1001
            sql_query = """
                SELECT EmpName, DATEADD(day, 180, DateofJoining) AS pDate 
                FROM app_employeemaster 
                WHERE OrganizationID = %s
                AND YEAR(DATEADD(day, 180, DateofJoining)) = YEAR(GETDATE())
                AND MONTH(DATEADD(day, 180, DateofJoining)) = MONTH(GETDATE());
            """
            with connection.cursor() as cursor:
                cursor.execute(sql_query, [OrganizationID])
                rows = cursor.fetchall()

            employee_list = [{'EmpName': row[0], 'pDate': row[1]} for row in rows]

            HR_Levels = ['M2', 'M', 'E']
            for Level in HR_Levels:
                HodDetails = HOD_Details(OrganizationID=OrganizationID, Department='Human Resources', Level=Level)
                if HodDetails:
                    HrEmailsList = [HodDetails[0]['OfficalMailAddress']]
                    print(HrEmailsList)
                    break

            self.send_email_to_hr(employee_list, HrEmailsList, OrganizationID, employee=HodDetails)

            self.stdout.write(self.style.SUCCESS('Probation period notifications sent successfully.'))

    def send_email_to_hr(self, employee_list, hr_manager_emails, OrganizationID, employee):
        subject = 'Probation Upcoming Soon'
        message = render_to_string('Probation/HRSendProbationNotifications.html', {'employee_list': employee_list})

        # Initialize these variables
        notification_title = 'Probation Period Ending Soon'
        notification_body = ''
        AppUserID = None

        try:
            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, hr_manager_emails)
            email.content_subtype = 'html'
            email.send()
            logger.info("Email sent successfully.")
            ModuleName = "HR"
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return Response({"error": f"Failed to send email: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            fcmobj = EmployeeUserLoginTokenMobile(OrganizationID=OrganizationID, EmployeeCode=employee['EmployeeCode'])
            fcm_token = fcmobj[0]['Token']
            AppUserID = fcmobj[0]['UserID']

            table_header = f"{'Employee Name':<20}{'Probation End Date':<20}\n"
            table_body = "\n".join([f"{emp['EmpName']:<20}{emp['pDate'].strftime('%d-%m-%Y'):<20}" for emp in employee_list])
            notification_body = f"The following employees' probation period is ending soon:\n\n{table_header}{table_body}"
            send_fcm_notification(fcm_token, notification_title, notification_body)
            logger.info("Notification sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send Notification: {e}")

        save_notification(subject, message, email_list=hr_manager_emails, ModuleName='Hr', AppTitle=notification_title,
                          AppBody=notification_body, OrganizationID=OrganizationID, AppUserID=AppUserID)

def save_notification(subject, message, email_list, ModuleName, AppTitle, AppBody, OrganizationID, AppUserID):
    try:
        notification = NotificationMessageDump(
            ModuleName=ModuleName,
            EmailMessageBody=message,
            AppUserID=AppUserID,
            AppTitle=AppTitle,
            AppBody=AppBody,
            DashboardTitle=subject,
            DashboardBody=subject,
            RetrunUrl='',
            OrganizationID=OrganizationID
        )
        notification.set_emails(email_list)
        notification.save()
    except Exception as e:
        logger.error(f"Failed to save notification: {e}")

def send_fcm_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=token,
    )
    response = messaging.send(message)
    print('Successfully sent FCM message', response)
