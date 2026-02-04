from HumanResources.models import EmployeeWorkDetails
from django.db  import connection, transaction
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings


def send_padp_pending_email(padp_list, recipients):
    if not padp_list or not recipients:
        return

    subject = "PADP Action Required – Final Rating Pending"

    message = "Following PADP needs action:\n\n"

    for idx, r in enumerate(padp_list, start=1):
        message += f"""
        PADP {idx}:
        Employee Name : {r['Name']}
        Employee Code : {r['Code']}
        Department    : {r['Dept']}
        Designation   : {r['Desi']}
        Action Needed : Please fill goals or KRA details and Final Performance Rating Pending 
        """

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipients,
        fail_silently=False,
    )


def get_organization_hr_emails(organization_ids):
    """
    Returns list of HR emails for given organization IDs
    """
    if not organization_ids:
        return []

    emails = EmployeeWorkDetails.objects.filter(
        EmpStatus__in=['Confirmed', 'On Probation', 'Not Confirmed'],
        Department="Human Resources",
        OrganizationID__in=organization_ids,
        IsSecondary=False,
        IsDelete=False
    ).exclude(
        OfficialEmailAddress__isnull=True
    ).exclude(
        OfficialEmailAddress=""
    ).values_list("OfficialEmailAddress", flat=True)
    print("emails is here:", emails)
    print("organization_ids is here:", organization_ids)

    return list(set(emails))  # unique emails




def get_kra_message(org_id, emp_code, from_date, to_date):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                EXEC sp_GetKraYearlyReportForPadp 
                    @OrganizationID=%s, 
                    @EmployeeCode=%s, 
                    @FromYear=%s, 
                    @FromMonth=%s, 
                    @ToYear=%s, 
                    @ToMonth=%s
            """, [
                org_id,
                emp_code,
                from_date.year,
                from_date.month,
                to_date.year,
                to_date.month
            ])

            rows = cursor.fetchall()
            if rows:
                message = 'KRA details found'
                KRA = True
            else:
                message = 'No KRA details found for the selected period.'
                KRA = False
            
            data = {
                "message":message,
                "KRA":KRA
            }
                
            return data

    except Exception:
        data = {
            "message":"No KRA details found",
            "KRA":False
        }
        return data 
