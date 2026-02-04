from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from app.models import OrganizationMaster
from EmailNotification.models import NotificationMessageDump
from firebase_admin import messaging
import logging
from app.views import EmployeeDataSelect, EmployeeUserLoginTokenMobile

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Send probation period ending notifications to employees'

    def handle(self, *args, **kwargs):
        # orgs = OrganizationMaster.objects.filter(IsDelete=False)
        
        # for org in orgs:
        #     OrganizationID = org.OrganizationID
            OrganizationID = 1001    
            today = timezone.now().date()

            empobj = EmployeeDataSelect(OrganizationID=OrganizationID)
            employees = []
            for emp in empobj:
                if emp['EmpStatus'] == 'On Probation':
                    employees.append(emp)

            for employee in employees:
                probation_end_date = employee['DateofJoining'] + timedelta(days=180)
                days_until_end = (probation_end_date - today).days
                if days_until_end in [30, 15, 0]:
                    self.send_notifications(employee, probation_end_date, OrganizationID)

            self.stdout.write(self.style.SUCCESS('Probation period notifications sent successfully.'))

    def send_notifications(self, employee, probation_end_date, OrganizationID):
        subject = 'Probation Period Ending Soon'
        message = render_to_string('Probation/ProbationNotification.html', {
            'EmployeeName': employee['EmpName'],
            'Department': employee['Department'],
            'Designation': employee['Designation'],
            'ProbationEndDate': probation_end_date
        })

        recipient_list = [employee['OfficalMailAddress'], employee['EmailMailAddress']]

        try:
            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            email.content_subtype = 'html'
            email.send()
            logger.info("Email sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

        notification_title = 'Probation Period Ending Soon'
        notification_body = f"Dear {employee['EmpName']}, your probation period is ending soon."
        AppUserID = None

        try:
            fcmobj = EmployeeUserLoginTokenMobile(OrganizationID=OrganizationID, EmployeeCode=employee['EmployeeCode'])
            fcm_token = fcmobj[0]['Token']
            AppUserID = fcmobj[0]['UserID']
            send_fcm_notification(fcm_token, notification_title, notification_body)
            logger.info("Notification sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send Notification: {e}")

        save_notification(subject, message, email_list=recipient_list, ModuleName='Hr', AppTitle=notification_title,
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
