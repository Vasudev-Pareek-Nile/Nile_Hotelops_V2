from .models import Entry_Master, FINAL_PERFORMANCE_RATING, APADP, FinalPerformancerating, APADP_Master_Log, Entry_Master_Log
from HumanResources.views import get_employee_designation_by_EmployeeCode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from datetime import datetime
from app.models import OrganizationMaster
from app.send_notification import *
from .models import Objective_Master,Attribute_Master,Ineffective_Indicators_Master,Effective_Indicators_Master,Entry_Master,Leadership_Details,Leadership_AttributeDetails,Effective_Indicators_Details_Appraisee,Effective_Indicators_Details_Appraisor,Ineffective_Indicators_Details_Appraisee,Ineffective_Indicators_Details_Appraisor,SPECIFIC_MEASURABLE_ACHIEVABLE,SPECIFIC_MEASURABLE_ACHIEVABLE_Details,SUMMARY_AND_ACKNOWLEDGEMENT,Approval_Submit_Status_PADP,FINAL_PERFORMANCE_RATING,calculate_appraisal_date, calculate_next_date,Get_next_approval_level, Entry_Master_Log, APADP_Master_Log


def format_date_properly(date_str):
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d %b %Y')
    except Exception as e:
        return date_str  # fallback to original string


class PADP_Approve_Mobile_API(APIView):
    """
    PADP Approve API
    Supports:
    - GET  → Fetch PADP data
    - POST → Bulk approval (CEO only)
    """

    def get(self, request):
        Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
        AccessToken = request.headers.get('Authorization', '')

        # Token checks
        if not AccessToken:
            return JsonResponse({'error': 'Token not found'}, status=400)
        if AccessToken != Fixed_Token:
            return JsonResponse({'error': 'Invalid token'}, status=400)
        
        # -------------------------------
        # # NEW ACCESS CHECK
        # UserID = request.GET.get("UserID")
        # ALLOWED_USER_IDS = ['20201212180048']

        # if not UserID:
        #     return JsonResponse({'error': 'UserID is required'}, status=400)

        # if UserID not in ALLOWED_USER_IDS:
        #     return JsonResponse({'error': 'Invalid UserID'}, status=404)
        # -------------------------------

        OrganizationID = request.GET.get('SessionOID')
        UserID = request.GET.get('UserID')
        UserType = request.GET.get('UserType').lower()
        Department = request.GET.get('Dpt')
        Designation = request.GET.get('Desi')
        # Departmentsession = Department.lower() if Department else ''
        Departmentsession = Department if Department else ''
        SI = request.query_params.getlist('SI')
        Status = request.GET.get('Status', 'Pending')
        I = request.GET.get('OID')
        
        
        # print(f"Designation name is here:", Designation)
        # print(f"Department name is here:", Department)
        # print(f"Departmentsession name is here:", Departmentsession)
        # print(f"UserType name is here:", UserType)
        # print(f"OrganizationID name is here:", OrganizationID)
        # print(f"I name is here:", I)
        
        if not I or I == '':
            I = OrganizationID
                        
        
        current_year = datetime.now().year
        current_month = datetime.now().strftime('%m')
        selected_year = request.GET.get('year', current_year)
        selected_month = request.GET.get('month', 'All')
        
        PRIVILEGED_ROLES = ['hr', 'gm', 'ceo']

        

        if OrganizationID == "3":
            # I = request.query_params.get('I', 'All')
            I = request.GET.get('OID', 'All')


        # % filters
        conditions = Q()
        if '3%' in SI:
            conditions |= Q(per_3=True)
        if '5%' in SI:
            conditions |= Q(per_5=True)
        if '8%' in SI:
            conditions |= Q(per_8=True)
        if '10%' in SI:
            conditions |= Q(per_10=True)

        # PADP filters
        padp_filter = {}
        if I != 'All':
            padp_filter['OrganizationID'] = I

        if Status == 'Pending':
            padp_filter['LastApporvalStatus__in'] = ['Pending', 'Submitted']
        elif Status != 'All':
            padp_filter['LastApporvalStatus'] = Status

        # 🔍 APADP Query
        if selected_month == 'All':
            apdp_query = APADP.objects.filter(
                IsDelete=False,
                CreatedDateTime__year=selected_year,
                **padp_filter
            )
        else:
            apdp_query = APADP.objects.filter(
                IsDelete=False,
                CreatedDateTime__year=selected_year,
                CreatedDateTime__month=selected_month,
                **padp_filter
            )

        # EmpCode = request.session["EmployeeCode"]
        # EmpCode = request.GET.get("EmployeeCode")
        # ReportingtoDesigantion = get_employee_designation_by_EmployeeCode(
        #     OrganizationID, EmpCode
        # )
        # ReportingtoDesigantion = Designation

        # if UserType == "ceo" and OrganizationID == "3":
        #     apdpdetas = apdp_query.filter(hr_ar="Audited")
        # elif Departmentsession == 'hr':
        #     apdpdetas = apdp_query
        # else:
        #     apdpdetas = apdp_query.filter(
        #         ReportingtoDesigantion=ReportingtoDesigantion
        #     )
                
        if UserType == "ceo" and OrganizationID == "3":
            apdpdetas = apdp_query.filter(hr_ar="Audited")

        elif UserType in PRIVILEGED_ROLES:
            apdpdetas = apdp_query

        else:
            apdpdetas = apdp_query.filter(
                ReportingtoDesigantion=Designation
                # ReportingtoDesigantion=ReportingtoDesigantion
            )
            print("apdpdetas:",apdpdetas)

            # Apply department filter ONLY for non HR/GM/CEO
            # if Departmentsession:
            #     apdpdetas = apdpdetas.filter(Department__iexact=Departmentsession)


        final_results = []

        ratings = FinalPerformancerating.objects.filter(
            APADP__in=apdpdetas,
            IsDelete=False
        )

        for rating in ratings:
            if UserType == "ceo":
                if rating.rating == "Not Rated":
                    continue   # skip this record
                
            review_from = format_date_properly(rating.APADP.review_from_date)
            review_to = format_date_properly(rating.APADP.review_to_date)
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
                "Period": f"{review_from} To {review_to}",
                "FPR": rating.rating,
                # "SIO": rating.SalaryIncrementOption,
                "SIO": salary_increment_option,
                "Approval": rating.APADP.Approval_stage_Mobile_Api(),
                "CreatedOnRaw": rating.CreatedDateTime,
                "id": rating.APADP.id,
                "Type": "A",
                "URL": f"https://hotelops.in:8080/PADP/ApadpPdf/?ID={rating.APADP.id}&Page=PADPApprove"   
            })
            
        # 🔍 Entry Master Query
        if selected_month == 'All':
            entry_query = Entry_Master.objects.filter(
                IsDelete=False,
                CreatedDateTime__year=selected_year,
                **padp_filter
            )
        else:
            entry_query = Entry_Master.objects.filter(
                IsDelete=False,
                CreatedDateTime__year=selected_year,
                CreatedDateTime__month=selected_month,
                **padp_filter
            )
            
        # if UserType == "ceo":
        #     entry_records = entry_query.filter(
        #         Q(hr_ar="Audited") |
        #         (Q(ep_as="Submitted") & Q(Aprraise_Level="M5"))
        #     )
        # elif Departmentsession == 'hr':
        #     entry_records = entry_query
        # else:
        #     entry_records = entry_query.filter(
        #         Q(ReportingtoDesigantion=ReportingtoDesigantion) |
        #         Q(DottedLine=ReportingtoDesigantion)
        #     )
                
        if UserType == "ceo":
            entry_records = entry_query.filter(
                Q(hr_ar="Audited") |
                (Q(ep_as="Submitted") & Q(Aprraise_Level="M5"))
            )

        elif UserType in PRIVILEGED_ROLES:
            entry_records = entry_query

        else:
            # entry_records = entry_query.filter(
            #     Q(ReportingtoDesigantion=ReportingtoDesigantion) |
            #     Q(DottedLine=ReportingtoDesigantion)
            # )
            entry_records = entry_query.filter(
                Q(ReportingtoDesigantion=Designation) |
                Q(DottedLine=Designation)
            )

            # Apply department filter ONLY for non HR/GM/CEO
            # if Departmentsession:
            #     entry_records = entry_records.filter(
            #         Department__iexact=Departmentsession
            #     )


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
                
            # EXCLUDE NOT RATED
            if UserType == "ceo":
                if performance_rating == "Not Rated":
                    continue
    
            final_results.append({
                "Code": entry.EmployeeCode,
                "OID": entry.OrganizationID,
                "Lvl": entry.Aprraise_Level,
                "Desi": entry.Aprraisee_position,
                "Dept": entry.Department,
                "Name": entry.Appraisee_Name,
                "CS": entry.Current_Salary,
                "Period": f"{entry.FromReviewDate:%d %b %Y} To {entry.ToReviewDate:%d %b %Y}",
                "FPR": performance_rating,
                "SIO": salary_increment,
                "Approval": entry.Approval_stage_Mobile_Api(),
                "LAS": entry.LastApporvalStatus,
                # "ceo_as": entry.ceo_as,
                "CreatedOnRaw": entry.CreatedDateTime,
                "id": entry.id,
                "Type": "M",   
                "Url": f"https://hotelops.in:8080/PADP/api/PADP_View_Manager/?ID={entry.id}&Page=PADPApprove"   
            })
            
        applied_ids = {r["OID"] for r in final_results if r.get("OID")}

        # 🔹 Fetch org names
        orgs = OrganizationMaster.objects.filter(
            OrganizationID__in=applied_ids,
            IsDelete=False,
            IsNileHotel=1,
            Activation_status=1
        ).values("OrganizationID", "ShortDisplayLabel")

        # 🔹 Build map
        org_map = {
            o["OrganizationID"]: o["ShortDisplayLabel"]
            for o in orgs
        }
        
        for r in final_results:
            r.setdefault("CreatedOnRaw", datetime.min)
            r["HTL"] = org_map.get(r["OID"], "")

        final_results.sort(
            key=lambda x: x["CreatedOnRaw"],
            reverse=True
        )

        return Response({
            "status": "success",
            "count": len(final_results),
            "data": final_results
        }, status=status.HTTP_200_OK)






from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO    
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import JsonResponse
from django.db  import connection, transaction

# padp ceo approval --- Padp_ceo_approve_api
def Padp_ceo_approve_api(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    # Token checks
    if not AccessToken:
        return JsonResponse({'error': 'Token not found'}, status=400)
    if AccessToken != Fixed_Token:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    
    # -------------------------------
    # NEW ACCESS CHECK
    UserID = request.GET.get("UserID")
    ALLOWED_USER_IDS = ['20201212180048']

    if not UserID:
        return JsonResponse({'error': 'UserID is required'}, status=400)

    if UserID not in ALLOWED_USER_IDS:
        return JsonResponse({'error': 'Invalid UserID'}, status=404)
    # -------------------------------

    
    OrganizationID = request.GET.get('OID')
    # UserID = request.GET.get('UserID')
    # UserType = request.GET.get('UserType').lower()
    UserType = (request.GET.get('UserType') or '').lower()
    
    PADP_Type = request.GET.get('PADPType')
    PADP_ID = request.GET.get('PADPID')
    Status = request.GET.get('Status')
    Remarks = request.GET.get('Remarks')
    
    if not PADP_ID or not Status:
        response_data = {
            'message': 'Invalid parameters'
        }
        return JsonResponse(response_data, status=400)
    
    try:
        Padp_ID = int(PADP_ID)
    except ValueError:
        return JsonResponse({'message': 'Invalid PADPID'}, status=400)

    hops_id = 0
    OID = 0
    Emp_Code = ''
    EmpName = ''
    
    if PADP_Type not in ["A", "M"]:
        return JsonResponse({'message': 'Invalid PADPType'}, status=400)

    if PADP_Type == "A":
        APADPobj = APADP.objects.filter(IsDelete=False, id=Padp_ID).first()
        if APADPobj is None:
            return JsonResponse({'message': 'Object not found'}, status=404)

        hops_id = APADPobj.id
        OID = APADPobj.OrganizationID
        Emp_Code = APADPobj.EmployeeCode
        EmpName = APADPobj.EmpName

        if APADPobj is None:
            response_data = {
                'message': 'Object not found'
            }
            return JsonResponse(response_data, status=404)
        
        if APADPobj:
            APADP_Master_Log.objects.create(
                APADP=APADPobj,
                LastApporvalStatus = APADPobj.LastApporvalStatus,
                hr_as = APADPobj.hr_as,
                ar_as = APADPobj.ar_as,
                hr_ar = APADPobj.hr_ar,
                ceo_as = APADPobj.ceo_as,
                ceo_as_remarks = APADPobj.ceo_as_remarks,
                hr_actionOnDatetime = APADPobj.hr_actionOnDatetime,
                ar_actionOnDatetime = APADPobj.ar_actionOnDatetime,
                hr_ar_actionOnDatetime = APADPobj.hr_ar_actionOnDatetime,
                ceo_actionOnDatetime = APADPobj.ceo_actionOnDatetime,

                OrganizationID = APADPobj.OrganizationID,
                CreatedBy = APADPobj.CreatedBy,
            )
        else:
            print("Log is not maintianed and created")

        APADPobj.LastApporvalStatus = Status
        APADPobj.ceo_as = Status
        APADPobj.ceo_as_remarks = Remarks
        APADPobj.ceo_actionOnDatetime =  datetime.now()

        
        APADPobj.save()
    # if "M_" in PADPID :
    if PADP_Type == "M":
        Entry_Masterobj  = Entry_Master.objects.filter(IsDelete=False,id=Padp_ID).first()
        hops_id = Entry_Masterobj.id or 0
        OID = Entry_Masterobj.OrganizationID or 0
        Emp_Code = Entry_Masterobj.EmployeeCode
        EmpName = Entry_Masterobj.Appraisee_Name

        if Entry_Masterobj is None:
            response_data = {
                'message': 'Object not found'
            }
            return JsonResponse(response_data, status=404)
        
        if Entry_Masterobj:
                Entry_Master_Log.objects.create(
                    Entry_Master = Entry_Masterobj,
                    LastApporvalStatus = Entry_Masterobj.LastApporvalStatus,
                    hr_as = Entry_Masterobj.hr_as,
                    ep_as = Entry_Masterobj.ep_as,
                    ar_as = Entry_Masterobj.ar_as,
                    rd_as = Entry_Masterobj.rd_as,
                    hr_ar = Entry_Masterobj.hr_ar,
                    ceo_as = Entry_Masterobj.ceo_as,
                    ceo_as_remarks = Entry_Masterobj.ceo_as_remarks,
                    hr_actionOnDatetime = Entry_Masterobj.hr_actionOnDatetime,
                    ep_actionOnDatetime = Entry_Masterobj.ep_actionOnDatetime,
                    ar_actionOnDatetime = Entry_Masterobj.ar_actionOnDatetime,
                    rd_actionOnDatetime = Entry_Masterobj.rd_actionOnDatetime,
                    hr_ar_actionOnDatetime = Entry_Masterobj.hr_ar_actionOnDatetime,
                    ceo_actionOnDatetime = Entry_Masterobj.ceo_actionOnDatetime,
                    OrganizationID = Entry_Masterobj.OrganizationID,
                    CreatedByUsername = Entry_Masterobj.CreatedByUsername,
                    CreatedBy = Entry_Masterobj.CreatedBy,
                )
        Entry_Masterobj.LastApporvalStatus = Status
        Entry_Masterobj.ceo_as = Status
        Entry_Masterobj.ceo_as_remarks = Remarks
        Entry_Masterobj.ceo_actionOnDatetime =  datetime.now()

        Entry_Masterobj.save()

    # print('we are reached here', OID,Emp_Code)
    Send_Leave_Approval_Notification(
        organization_id=OID,
        EmpCode=Emp_Code,
        title="PADP Approved",
        message=f"{EmpName}, your PADP has been {Status}",
        module_name="PADP",
        action="Approved",
        hopsId=hops_id,
        user_type="admin",
        priority="high"
    )

    response_data = {
        'message': f'PADP {Status} successfully'
    }
    return JsonResponse(response_data, status=200)









# manager pdf -- PADP_View_Manager
def PADP_View_Manager(request):
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    SessionOID = request.GET.get('SessionOID')
    UserID = request.GET.get('UserID')
    # UserType = request.GET.get('UserType').lower()

    padp_id = request.GET.get('ID')
    padp =None
    sum_data = None
    columns  = None
    rowslist = None
    print("apaid is here:", padp_id)

    if padp_id is not None:
        padp = Entry_Master.objects.filter(IsDelete =False,id = padp_id).first()
        print("the padp is here::", padp)
        
        if padp:
            OrganizationID = padp.OrganizationID
        
        selected_from_year =  padp.FromReviewDate.year
        selected_from_month = padp.FromReviewDate.month  
        selected_to_year =  padp.ToReviewDate.year 
        selected_to_month =  padp.ToReviewDate.month 
        
        try:
            with connection.cursor() as cursor:
                # Update the SQL query to use the correct stored procedure and parameters
                cursor.execute("""
                    EXEC sp_GetKraYearlyReportForPadp 
                        @OrganizationID=%s, 
                        @EmployeeCode=%s, 
                        @FromYear=%s, 
                        @FromMonth=%s, 
                        @ToYear=%s, 
                        @ToMonth=%s
                    """, [
                        padp.OrganizationID, 
                        padp.EmployeeCode, 
                        selected_from_year, 
                        selected_from_month, 
                        selected_to_year, 
                        selected_to_month
                    ])
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                rowslist = [dict(zip(columns, row)) for row in rows]
                columns = list(rowslist[0].keys()) if rowslist else []

        except Exception as e:
                    print("No Kra Details is not Found")

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    EXEC sp_GetKraOverallRatingForPadp 
                        @OrganizationID=%s, 
                        @EmployeeCode=%s, 
                        @FromYear=%s, 
                        @FromMonth=%s, 
                        @ToYear=%s, 
                        @ToMonth=%s
                """, [
                    padp.OrganizationID, 
                    padp.EmployeeCode, 
                    selected_from_year, 
                    selected_from_month, 
                    selected_to_year, 
                    selected_to_month
                ])
                result = cursor.fetchone()
                
                if result:
                    OverallRating = result[0]  
                else:
                    OverallRating = None  
        except Exception as e:
                    print("No Overall Rating Details is not Found")
    
    Leadership_Detail = Leadership_Details.objects.filter(Entry_Master=padp,IsDelete =False).first()
    sum_data = SUMMARY_AND_ACKNOWLEDGEMENT.objects.filter(Entry_Master=padp,IsDelete =False).first()
    
    Sal_data = FINAL_PERFORMANCE_RATING.objects.filter(Entry_Master=padp,IsDelete =False).first()
    sal = 'False'
    if Sal_data:
        if Sal_data.SALARY_CORRECTION or  Sal_data.PROMOTION_WITH_INCREASE or  Sal_data.PROMOTION_WITH_INCREASE:
            sal = 'True' 
    
    objs =  Objective_Master.objects.filter(IsDelete=False,Level= padp.Aprraise_Level)
    for m in objs:
        attr1= Attribute_Master.objects.filter(IsDelete=False,Objective_Master=m)
        m.Attibutes = attr1
        Effect1 = Effective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
        m.Effectives = Effect1
        Infect1 = Ineffective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
        m.Ineffectives = Infect1

    SPE_MEA_ACH_Detail = SPECIFIC_MEASURABLE_ACHIEVABLE_Details.objects.filter(SPECIFIC_MEASURABLE_ACHIEVABLE__Entry_Master = padp,IsDelete =False)
    Goal  = 'False' 
    
    if SPE_MEA_ACH_Detail:
        Goal = 'True'

    for m in objs:
        m.LD= Leadership_Details.objects.filter(Entry_Master=padp,Objective_Master=m,IsDelete =False)
        attr1= Attribute_Master.objects.filter(IsDelete=False,Objective_Master=m)
        m.Attibutes = attr1
        
        for a in attr1:
                k = Leadership_AttributeDetails.objects.filter(
                    IsDelete =False,
                    Leadership_Details__Objective_Master=m,
                    Attribute_Master=a,
                    Leadership_Details__Entry_Master = padp
                )
                a.detailatt = k

        Effect1 = Effective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
        m.Effectives = Effect1
        
        for eff in  Effect1:
            c = Effective_Indicators_Details_Appraisee.objects.filter(IsDelete =False,Entry_Master=padp,Objective_Master=m,Effective_Indicators_Master=eff,)
            
            eff.effdetail_Appee = c
            d = Effective_Indicators_Details_Appraisor.objects.filter(IsDelete =False,Entry_Master=padp,Objective_Master=m,Effective_Indicators_Master=eff)
            eff.effdetail_Appor = d
            
        Infect1 = Ineffective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
        m.Ineffectives = Infect1

        for inff in Infect1:
            kl = Ineffective_Indicators_Details_Appraisee.objects.filter(IsDelete =False,Entry_Master=padp,Objective_Master=m,Ineffective_Indicators_Master=inff)    
            inff.inffdetailAppee =  kl
            ml = Ineffective_Indicators_Details_Appraisor.objects.filter(IsDelete =False,Entry_Master=padp,Objective_Master=m,Ineffective_Indicators_Master=inff)    
            inff.inffdetailAppor =  ml

    template_path = "PADPAPP/PADP/PADPVIEW.html"
    # NileLogo=MasterAttribute.NileLogo
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

    organizations = OrganizationMaster.objects.filter(OrganizationID=padp.EmployeeOrganizationID).first()
    if organizations:
        OrganizationName = organizations.OrganizationName  
        
    organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    Kra_Found  =  'False'
    
    if columns and rowslist:
        Kra_Found  = 'True'

    
    mydict={
        'objs':objs,
        'padp':padp,
        'sum_data':sum_data,
        'SPE_MEA_ACH_Detail':SPE_MEA_ACH_Detail,
        'organization_logos':organization_logos,
        'organization_logo':organization_logo,
        'OrganizationName':OrganizationName,
        'rowslist':rowslist,
        'columns':columns,
        'OverallRating':OverallRating ,
        'Sal_data':Sal_data ,
        'Kra_Found':Kra_Found,
        'Goal':Goal ,
        'sal':sal    
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="padp.pdf"'
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
    pdf  = pisa.pisaDocument(BytesIO(html.encode("utf8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None   
