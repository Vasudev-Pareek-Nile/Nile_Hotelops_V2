from datetime import datetime
from django.db.models import Q
from rest_framework import status
from app.models import OrganizationMaster
# import all models & helper methods used below

# def run_padp_notification(
#     UserID,
#     OrganizationID,
#     UserType="hr",
#     Department=None,
#     Designation=None,
#     SI=None,
#     Status="Pending",
#     year=None,
#     month="All",
# ):
#     if SI is None:
#         SI = []

#     ALLOWED_USER_IDS = ['20201212180048', '20251209112591']

#     I = OrganizationID
#     current_year = datetime.now().year
#     selected_year = year or current_year
#     selected_month = month

#     PRIVILEGED_ROLES = ['hr', 'gm']

#     # % filters
#     conditions = Q()
#     if '3%' in SI:
#         conditions |= Q(per_3=True)
#     if '5%' in SI:
#         conditions |= Q(per_5=True)
#     if '8%' in SI:
#         conditions |= Q(per_8=True)
#     if '10%' in SI:
#         conditions |= Q(per_10=True)

#     padp_filter = {}
#     if I != 'All':
#         padp_filter['OrganizationID'] = I

#     if Status == 'Pending':
#         padp_filter['LastApporvalStatus__in'] = ['Pending', 'Submitted']
#     elif Status != 'All':
#         padp_filter['LastApporvalStatus'] = Status

#     # ---- APADP QUERY ----
#     if selected_month == 'All':
#         apdp_query = APADP.objects.filter(IsDelete=False, **padp_filter)
#     else:
#         apdp_query = APADP.objects.filter(
#             IsDelete=False,
#             CreatedDateTime__month=selected_month,
#             **padp_filter
#         )

#     if UserID in ALLOWED_USER_IDS and OrganizationID == "3":
#         apdpdetas = apdp_query.filter(hr_ar="Audited")
#     elif UserType in PRIVILEGED_ROLES:
#         apdpdetas = apdp_query
#     else:
#         apdpdetas = apdp_query.filter(ReportingtoDesigantion=Designation)

#     final_results = []

#     ratings = FinalPerformancerating.objects.filter(
#         APADP__in=apdpdetas,
#         IsDelete=False
#     )

#     for rating in ratings:
#         performance_rating = rating.rating or "Not Rated"

#         if UserID in ALLOWED_USER_IDS and performance_rating != "Not Rated":
#             continue

#         final_results.append({
#             "Code": rating.APADP.EmployeeCode,
#             "OID": rating.APADP.OrganizationID,
#             "Name": rating.APADP.EmpName,
#             "FPR": performance_rating,
#             "CreatedOnRaw": rating.CreatedDateTime,
#         })

#     # ---- SEND EMAIL ----
#     org_ids = {r["OID"] for r in final_results if r.get("OID")}
#     Emails = get_organization_hr_emails(org_ids)

#     send_padp_pending_email(final_results, recipients=Emails)

#     return {
#         "status": "success",
#         "count": len(final_results)
#     }

from ..utils import *
from ..models import *
# from models import *
from rest_framework.response import Response
from collections import defaultdict

def run_padp_notification(
    UserID='20201212180048',
    OrganizationID = '3',
    UserType="hod",
    Designation=None,
    month="All",
    I='333333',
):
    ALLOWED_USER_IDS = ['20201212180048','20251209112591']

    if not I or I == '':
        I = OrganizationID
                
    # current_year = datetime.now().year
    # current_month = datetime.now().strftime('%m')
    # selected_year = year
    # selected_month = month
    
    # if not selected_year or selected_year == '':
    #     selected_year = current_year
        
    PRIVILEGED_ROLES = ['hr', 'gm']

    
    if OrganizationID == "3" and I == "333333":
        I = 'All'
        
    # PADP filters
    padp_filter = {}
    padp_filter['LastApporvalStatus__in'] = ['Pending', 'Submitted']

    apdp_query = APADP.objects.filter(
        IsDelete=False,
        # CreatedDateTime__year=selected_year,
        **padp_filter
    )
    
    # if UserType == "ceo" and OrganizationID == "3":
    if UserID in ALLOWED_USER_IDS and OrganizationID == "3":
        apdpdetas = apdp_query.filter(hr_ar="Audited")

    elif UserType in PRIVILEGED_ROLES:
        apdpdetas = apdp_query

    else:
        apdpdetas = apdp_query.filter(
            ReportingtoDesigantion=Designation
        )

    final_results = []

    ratings = FinalPerformancerating.objects.filter(
        APADP__in=apdpdetas,
        IsDelete=False
    )

    for rating in ratings: 
        
        # ------------- KRA Start
        kra_message = get_kra_message(
            rating.APADP.OrganizationID,
            rating.APADP.EmployeeCode,
            rating.APADP.review_from_date,
            rating.APADP.review_to_date
        )
        # ------------- / KRA
        
        performance_rating = rating.rating

        if not performance_rating or performance_rating.strip() == "":
            performance_rating = "Not Rated"

        # skip for allowed users
        if UserID in ALLOWED_USER_IDS and performance_rating != "Not Rated":
            continue
        
        # review_from = format_date_properly(rating.APADP.review_from_date)
        # review_to = format_date_properly(rating.APADP.review_to_date)
        salary_increment_option = rating.SalaryIncrementOption
        if salary_increment_option == "Salary Correction":
            salary_increment_option = f"Correction From {rating.SalaryCorrectionFrom} To {rating.SalaryCorrectionTo}"
        elif salary_increment_option == "Promotion":
            salary_increment_option = f"Promotion From {rating.PromotionFrom} To {rating.PromotionTo}"
        elif salary_increment_option == "Promotion with Increase":
            salary_increment_option = f"Promotion with Increase {rating.SalaryCorrectionFrom} To {rating.SalaryCorrectionTo}, {rating.PromotionFrom} To {rating.PromotionTo}"

        final_results.append({
            "Code": rating.APADP.EmployeeCode,
            "OID": rating.APADP.OrganizationID,
            "Lvl": rating.APADP.Level,
            "Name": rating.APADP.EmpName,
            "CS": rating.APADP.Current_Salary,
            "Desi": rating.APADP.Designation,
            "Dept": rating.APADP.Department,
            "KRA_Message": kra_message["message"],
        })
        
    # Entry Master Query
    entry_query = Entry_Master.objects.filter(
        IsDelete=False,
        # CreatedDateTime__year=selected_year,
        **padp_filter
    )
        
            
    # if UserType == "ceo":
    if UserID in ALLOWED_USER_IDS:
        entry_records = entry_query.filter(
            Q(hr_ar="Audited") |
            (Q(ep_as="Submitted") & Q(Aprraise_Level="M5"))
        )

    elif UserType in PRIVILEGED_ROLES:
        entry_records = entry_query

    else:
        entry_records = entry_query.filter(
            Q(ReportingtoDesigantion=Designation) |
            Q(DottedLine=Designation)
        )

    for entry in entry_records:
        final_perf_record = FINAL_PERFORMANCE_RATING.objects.filter(
            Entry_Master=entry
        ).first()

        if final_perf_record:
            performance_rating = (
                "Outstanding" if final_perf_record.OUTSTANDING else
                "Above Standard" if final_perf_record.ABOVE_STANDARD else
                "Meets Expectation" if final_perf_record.MEETS_EXPECTATION else
                "Below Standard" if final_perf_record.BELOW_STANDARD else
                "Deficient" if final_perf_record.DEFICIENT else
                "Not Rated"
            )

            salary_increment = (
                "No Correction" if final_perf_record.NO_CORRECTION else
                "3 %" if final_perf_record.per_3 else
                "5 %" if final_perf_record.per_5 else
                "8 %" if final_perf_record.per_8 else
                "10 %" if final_perf_record.per_10 else
                f"Correction {final_perf_record.FromSalary} To {final_perf_record.ToSalary}" if final_perf_record.SALARY_CORRECTION else 
                f"Promotion {final_perf_record.FromPosition} To {final_perf_record.ToPosition}" if final_perf_record.PROMOTION else 
                f"Promotion With Increament \n{final_perf_record.FromSalary} To {final_perf_record.ToSalary}, {final_perf_record.FromPosition} To {final_perf_record.ToPosition}" if final_perf_record.PROMOTION_WITH_INCREASE else "Action Pending"
            )
        else:
            performance_rating = "Not Rated"
            salary_increment = "Not Specified"
            
            
        performance_rating = performance_rating

        if not performance_rating or performance_rating.strip() == "":
            performance_rating = "Not Rated"

        # skip for allowed users
        if UserID in ALLOWED_USER_IDS and performance_rating != "Not Rated":
            continue
            
        # ------------- KRA Start
        kra_message = get_kra_message(
            entry.OrganizationID,
            entry.EmployeeCode,
            entry.FromReviewDate,
            entry.ToReviewDate
        )
        # ------------- / KRA
            
        final_results.append({
            "Code": entry.EmployeeCode,
            "OID": entry.OrganizationID,
            "Lvl": entry.Aprraise_Level,
            "Desi": entry.Aprraisee_position,
            "Dept": entry.Department,
            "Name": entry.Appraisee_Name,
            "KRA": kra_message["KRA"],
            "KRA_Message": kra_message["message"],
        })
        
    org_wise_data = defaultdict(list)

    for record in final_results:
        org_wise_data[record["OID"]].append(record)
        
    # Collect unique Organization IDs from results
    # org_ids = {r["OID"] for r in final_results if r.get("OID")}

    # Fetch HR emails
    # Emails = get_organization_hr_emails(org_ids)

    # Send mail
    # send_padp_pending_email(final_results, recipients=["Vasudev.Pareek@nilehospitality.com"])
    # send_padp_pending_email(final_results, recipients=Emails)

    for org_id, padp_list in org_wise_data.items():
        emails = get_organization_hr_emails([org_id])

        if not emails:
            continue

        send_padp_pending_email(
            padp_list=padp_list,
            recipients=emails
        )

    return {
        "status": "success",
        "count": len(final_results)
    }