
from datetime import datetime, timedelta, date
from django.core.mail import send_mail
from django.conf import settings
from .models import IT_Inventory

# def send_expiry_reminders():
#     today = date.today()
#     reminder_date = today + timedelta(days=30)   # 1 month before expiry
#     to_email = "Vasudev.Pareek@nilehospitality.com"

#     expiring_items = []

#     for item in IT_Inventory.objects.filter(IsDelete=False):
#         # --- Handle hardware AMC expiry ---
#         if item.amcend:
#             try:
#                 amc_end = datetime.strptime(item.amcend, "%Y-%m-%d").date()
#                 if amc_end == reminder_date:
#                     expiring_items.append((item, "Hardware AMC", amc_end))
#             except:
#                 pass  # skip invalid date formats

#         # --- Handle software AMC expiry ---
#         if item.software_AMC_end:
#             try:
#                 sw_amc_end = datetime.strptime(item.software_AMC_end, "%Y-%m-%d").date()
#                 if sw_amc_end == reminder_date:
#                     expiring_items.append((item, "Software AMC", sw_amc_end))
#             except:
#                 pass

#         # --- Handle warranty expiry ---
#         if item.Warrantiy_end:
#             try:
#                 warranty_end = datetime.strptime(item.Warrantiy_end, "%Y-%m-%d").date()
#                 if warranty_end == reminder_date:
#                     expiring_items.append((item, "Warranty", warranty_end))
#             except:
#                 pass

#     # --- Send email if any expiring ---
#     if expiring_items:
#         subject = "Reminder: AMC/Warranty Expiry Alert"
#         body_lines = ["The following items will expire in 30 days:\n"]
#         for inv, inv_type, exp_date in expiring_items:
#             body_lines.append(f"- {inv.Description or inv.SerialNo} ({inv_type}) → Expiry: {exp_date}")
#         body = "\n".join(body_lines)

#         send_mail(
#             subject,
#             body,
#             settings.DEFAULT_FROM_EMAIL,
#             [to_email],
#             fail_silently=False,
#         )


from datetime import datetime, timedelta, date
from django.core.mail import send_mail
from django.conf import settings
from .models import IT_Inventory

from django.utils.timezone import now
import logging


# def send_expiry_reminders():
#     logging.warning(f"Reminder task started at {now()}")
#     today = date.today()
#     reminder_date = today + timedelta(days=30)   # check items expiring in 30 days
#     to_email = "Vasudev.Pareek@nilehospitality.com"

#     expiring_items = []

#     for item in IT_Inventory.objects.filter(IsDelete=False):
#         logging.warning(f"Checking item: {item}")
#         # --- Handle hardware AMC expiry ---
#         if item.amcend:
#             try:
#                 amc_end = datetime.strptime(item.amcend, "%d/%m/%Y").date()
#                 if amc_end == reminder_date:
#                     expiring_items.append((item, "Hardware AMC", amc_end))
#             except ValueError:
#                 pass  # skip invalid date formats

#         # --- Handle software AMC expiry ---
#         if item.software_AMC_end:
#             try:
#                 sw_amc_end = datetime.strptime(item.software_AMC_end, "%d/%m/%Y").date()
#                 if sw_amc_end == reminder_date:
#                     expiring_items.append((item, "Software AMC", sw_amc_end))
#             except ValueError:
#                 pass

#         # --- Handle warranty expiry ---
#         if item.Warrantiy_end:
#             try:
#                 warranty_end = datetime.strptime(item.Warrantiy_end, "%d/%m/%Y").date()
#                 if warranty_end == reminder_date:
#                     expiring_items.append((item, "Warranty", warranty_end))
#             except ValueError:
#                 pass

#     # --- Send email if any expiring ---
#     if expiring_items:
#         logging.warning(f"Found {len(expiring_items)} expiring items.")

#         subject = "Reminder: AMC/Warranty Expiry Alert"
#         body_lines = ["The following items will expire in 30 days:\n"]
#         for inv, inv_type, exp_date in expiring_items:
#             body_lines.append(
#                 f"- {inv.Description or inv.SerialNo} ({inv_type}) → Expiry: {exp_date.strftime('%d/%m/%Y')}"
#             )
#         body = "\n".join(body_lines)

#         send_mail(
#             subject,
#             body,
#             settings.DEFAULT_FROM_EMAIL,
#             [to_email],
#             fail_silently=False,
#         )
#     else:
#         logging.warning("No expiring items found → no email sent")




from datetime import date, timedelta
from django.core.mail import send_mail
from django.conf import settings
# from .models import SoftwareInventory

# def send_expiry_reminders():
#     today = date.today()
#     reminder_date = today + timedelta(days=30)

#     expiring_items = SoftwareInventory.objects.filter(
#         IsDelete=False
#     ).filter(
#         # Either AMC or Warranty expiry falls between today and +30 days
#         (Q(AMC_Expiry__range=[today, reminder_date]) |
#          Q(Warranty_Expiry__range=[today, reminder_date]))
#     )

#     if expiring_items.exists():
#         subject = "Reminder: Upcoming AMC/Warranty Expiries"
#         message = "The following items are expiring soon:\n\n"

#         for inv in expiring_items:
#             message += f"• {inv.ItemName} - "
#             if inv.AMC_Expiry and today <= inv.AMC_Expiry <= reminder_date:
#                 message += f"AMC Expiry: {inv.AMC_Expiry} "
#             if inv.Warranty_Expiry and today <= inv.Warranty_Expiry <= reminder_date:
#                 message += f"Warranty Expiry: {inv.Warranty_Expiry} "
#             message += "\n"

#         send_mail(
#             subject,
#             message,
#             settings.DEFAULT_FROM_EMAIL,
#             ["Vasudev.Pareek@nilehospitality.com"],  # Replace with recipient list
#             fail_silently=False,
#         )



# import logging
# from datetime import date, timedelta
# from django.core.mail import send_mail
# from django.conf import settings
# from django.utils.timezone import now
# from .models import IT_Inventory
from datetime import datetime, date
from app.models import OrganizationMaster

def parse_date(value):
    """Convert string or date to a date object (YYYY-MM-DD)."""
    if isinstance(value, date):
        return value
    if not value:
        return None
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except ValueError:
        return None

def send_expiry_reminders():
    logging.warning(f"Reminder task started at {now()}")

    today = date.today()
    reminder_date_Thirty = today + timedelta(days=30)   # look 30 days ahead
    reminder_date_Fifteen = today + timedelta(days=15)   # look 30 days ahead
    reminder_date = today + timedelta(days=30)   # look 30 days ahead
    to_email = "Vasudev.Pareek@nilehospitality.com"

    expiring_items = []

    for item in IT_Inventory.objects.filter(IsDelete=False):
        orgs = OrganizationMaster.objects.filter(
            IsDelete=False, 
            Activation_status=1, 
            OrganizationID=item.OrganizationID
        ).values("OrganizationName").first()

        if orgs:
            org_name = orgs["OrganizationName"]
            # print(f"OrganizationName: {org_name}")

        # --- Hardware AMC ---
        if item.amcend:
            # print("the amc date is here", item.amcend)
            amc_start = item.amcstart if hasattr(item, "amcstart") else None
            amc_end = parse_date(item.amcend)
            # print("the amc date is here amc_end object -----", amc_end)
            if amc_end and today <= amc_end <= reminder_date:
                expiring_items.append((
                    item, 
                    "Hardware AMC", 
                    # amc_end,
                    amc_start,
                    amc_end,
                ))

        # --- Software AMC ---
        if item.software_AMC_end:
            # print("the amc date is here", item.amcend)
            sw_amc_start = item.software_AMC_start if hasattr(item, "software_AMC_start") else None
            # print("the amc date is here", item.software_AMC_end)
            # sw_amc_end = item.software_AMC_end if isinstance(item.software_AMC_end, date) else None
            sw_amc_end = parse_date(item.software_AMC_end)
            # print("the amc date is here amc_end object -----", sw_amc_end)
            if sw_amc_end and today <= sw_amc_end <= reminder_date:
                expiring_items.append((
                    item, 
                    "Software AMC", 
                    # sw_amc_end
                    sw_amc_start,
                    sw_amc_end,
                ))

        # --- Warranty ---
        # if item.Warrantiy_end:
        #     warranty_start = item.Warrantiy_start if hasattr(item, "Warrantiy_start") else None
        #     warranty_end = item.Warrantiy_end if isinstance(item.Warrantiy_end, date) else None
        #     if warranty_end and today <= warranty_end <= reminder_date:
        #         expiring_items.append((
        #             item, 
        #             "Warranty", 
        #             # warranty_end
        #             warranty_start,
        #             warranty_end,
        #         ))

    # --- Send email if found ---
    if expiring_items:
        logging.warning(f"Found {len(expiring_items)} expiring items.")

        subject = "Reminder: AMC Expiry Alert"
        # subject = "Reminder: AMC/Warranty Expiry Alert"
        body_lines = ["The following items are expiring within 30 days:\n"]
        for inv, inv_type,start_date, end_date  in expiring_items:
            display_name = inv.Description or inv.SerialNo or "Unknown Item"
            # print("the Description name", display_name)
            print("the start_date", start_date)
            # formatted_start = start_date.strftime("%d/%m/%Y") if start_date else "N/A"
            if start_date:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")  # parse string
                formatted_start = start_date_obj.strftime("%d/%m/%Y")
                print("the formatted_start", formatted_start)
            else:
                formatted_start = "N/A"
            # print("the formatted_start", formatted_start)
            Body_Data = f"""
                Item Name (Description):{display_name}
                Inventory Type: {inv_type}
                Expiry: {end_date.strftime('%d/%m/%Y')}
                Organization Name: {org_name}
                AMC Period: {formatted_start if formatted_start else 'N/A'} 
                        To {end_date.strftime('%d/%m/%Y')}
            """
            # body_lines.append(f"- {display_name} ({inv_type}) → Expiry: {exp_date.strftime('%d/%m/%Y')}")
            body_lines.append(Body_Data)

        body = "\n".join(body_lines)

        # send_mail(
        #     subject,
        #     body,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [to_email],
        #     fail_silently=False,
        # )

        recipients = ["Vasudev.Pareek@nilehospitality.com"]  


        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            recipients,
            fail_silently=False,
        )
    else:
        logging.warning("No expiring items found → no email sent")



# def send_expiry_reminders():
#     logging.warning(f"Reminder task started at {now()}")

#     # 👇 Just testing hello email
#     subject = "Hello from HotelOps System"
#     body = (
#         "Hi Vasudev,\n\n"
#         "This is a test email from the automatic notification system.\n"
#         "Once this is working, we’ll replace it with the expiry reminder.\n\n"
#         "Best regards,\n"
#         "HotelOps System"
#     )

#     to_email = "Vasudev.Pareek@nilehospitality.com"
#     recipients = ["Vasudev.Pareek@nilehospitality.com"]  

    
#     send_mail(
#         subject,
#         body,
#         settings.EMAIL_HOST_USER,
#         recipients,
#         fail_silently=False,
#     )

#     logging.warning("Hello email sent successfully ✅")




def send_expiry_reminders_SecondOne():
    logging.warning(f"Reminder task started at {now()}")

    today = date.today()
    # reminder_date_Thirty = today + timedelta(days=30)   # look 30 days ahead
    reminder_date_Fifteen = today + timedelta(days=15)   # look 30 days ahead
    # reminder_date = today + timedelta(days=30)   # look 30 days ahead
    to_email = "Vasudev.Pareek@nilehospitality.com"

    expiring_items = []

    for item in IT_Inventory.objects.filter(IsDelete=False):
        orgs = OrganizationMaster.objects.filter(
            IsDelete=False, 
            Activation_status=1, 
            OrganizationID=item.OrganizationID
        ).values("OrganizationName").first()

        if orgs:
            org_name = orgs["OrganizationName"]
            # print(f"OrganizationName: {org_name}")

        # --- Hardware AMC ---
        if item.amcend:
            # print("the amc date is here", item.amcend)
            amc_start = item.amcstart if hasattr(item, "amcstart") else None
            amc_end = parse_date(item.amcend)
            # print("the amc date is here amc_end object -----", amc_end)
            if amc_end and today <= amc_end <= reminder_date_Fifteen:
                expiring_items.append((
                    item, 
                    "Hardware AMC", 
                    # amc_end,
                    amc_start,
                    amc_end,
                ))

        # --- Software AMC ---
        if item.software_AMC_end:
            # print("the amc date is here", item.amcend)
            sw_amc_start = item.software_AMC_start if hasattr(item, "software_AMC_start") else None
            # print("the amc date is here", item.software_AMC_end)
            # sw_amc_end = item.software_AMC_end if isinstance(item.software_AMC_end, date) else None
            sw_amc_end = parse_date(item.software_AMC_end)
            # print("the amc date is here amc_end object -----", sw_amc_end)
            if sw_amc_end and today <= sw_amc_end <= reminder_date_Fifteen:
                expiring_items.append((
                    item, 
                    "Software AMC", 
                    # sw_amc_end
                    sw_amc_start,
                    sw_amc_end,
                ))

        # --- Warranty ---
        # if item.Warrantiy_end:
        #     warranty_start = item.Warrantiy_start if hasattr(item, "Warrantiy_start") else None
        #     warranty_end = item.Warrantiy_end if isinstance(item.Warrantiy_end, date) else None
        #     if warranty_end and today <= warranty_end <= reminder_date_Fifteen:
        #         expiring_items.append((
        #             item, 
        #             "Warranty", 
        #             # warranty_end
        #             warranty_start,
        #             warranty_end,
        #         ))

    # --- Send email if found ---
    if expiring_items:
        logging.warning(f"Found {len(expiring_items)} expiring items.")

        subject = "Reminder: AMC Expiry Alert"
        # subject = "Reminder: AMC/Warranty Expiry Alert"
        body_lines = ["The following items are expiring within 30 days:\n"]
        for inv, inv_type,start_date, end_date  in expiring_items:
            display_name = inv.Description or inv.SerialNo or "Unknown Item"
            # print("the Description name", display_name)
            print("the start_date", start_date)
            # formatted_start = start_date.strftime("%d/%m/%Y") if start_date else "N/A"
            if start_date:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")  # parse string
                formatted_start = start_date_obj.strftime("%d/%m/%Y")
                print("the formatted_start", formatted_start)
            else:
                formatted_start = "N/A"
            # print("the formatted_start", formatted_start)
            Body_Data = f"""
                Item Name (Description):{display_name}
                Inventory Type: {inv_type}
                Expiry: {end_date.strftime('%d/%m/%Y')}
                Organization Name: {org_name}
                AMC Period: {formatted_start if formatted_start else 'N/A'} 
                        To {end_date.strftime('%d/%m/%Y')}
            """
            # body_lines.append(f"- {display_name} ({inv_type}) → Expiry: {exp_date.strftime('%d/%m/%Y')}")
            body_lines.append(Body_Data)

        body = "\n".join(body_lines)

        # send_mail(
        #     subject,
        #     body,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [to_email],
        #     fail_silently=False,
        # )

        recipients = ["Vasudev.Pareek@nilehospitality.com"]  


        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            recipients,
            fail_silently=False,
        )
    else:
        logging.warning("No expiring items found → no email sent")




from HumanResources.models import EmployeeWorkDetails
from django.http import JsonResponse

# get_organization_hr_email
def get_organization_it_emails(organization_ids):
    """
    Returns list of IT emails for given organization IDs
    """
    if not organization_ids:
        return []

    emails_qs = EmployeeWorkDetails.objects.filter(
        EmpStatus__in=['Confirmed', 'On Probation', 'Not Confirmed'],
        Department="Information & Systems",
        # OrganizationID='1001',
        OrganizationID__in=organization_ids,
        IsSecondary=False,
        IsDelete=False
    ).exclude(
        OfficialEmailAddress__isnull=True
    ).exclude(
        OfficialEmailAddress=""
    ).values_list("OfficialEmailAddress", flat=True)
    # print("emails is here:", emails)
    # print("organization_ids is here:", organization_ids)

    # return list(set(emails))  # unique emails
    emails = list(emails_qs)

    # Add extra email
    extra_emails = ['Dinesh@nilehospitality.com']
    emails.extend(extra_emails)

    # Optional: remove duplicates
    emails = list(set(emails))

    return emails

