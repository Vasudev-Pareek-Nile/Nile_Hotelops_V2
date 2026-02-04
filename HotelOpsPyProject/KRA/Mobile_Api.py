from .models import KRA, TargetAssignMasterDetails
from django.db.models import OuterRef, Subquery
from django.template.loader import get_template
from django.db.models import Count, Case, When
# from django.db.models import Count, Case, When
from rest_framework.decorators import api_view
# from rest_framework.decorators import api_view
# from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.response import Response
# from rest_framework.response import Response
from .models import KraEntryMasterDetails
from app.models import OrganizationMaster
from django.http import JsonResponse
# from django.http import JsonResponse
from django.http import HttpResponse
from collections import defaultdict
# from rest_framework import status
from django.utils import timezone
# from django.utils import timezone
# from rest_framework import status
from rest_framework import status
from django.conf import settings
from django.db import connection
from django.db.models import F
import calendar
import pdfkit




@api_view(['GET'])
def kra_summary_api(request):
    """
    KRA Summary API
    Filters:
    - OrganizationID
    - SubmittedYear
    - SubmittedMonth
    """
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
    ALLOWED_USER_IDS = ['20201212180048', '20251209112591']

    if not UserID:
        return JsonResponse({'error': 'UserID is required'}, status=400)

    if UserID not in ALLOWED_USER_IDS:
        return JsonResponse({'error': 'Invalid UserID'}, status=404)
    # -------------------------------
    
    OID = request.GET.get('OID')
    UserType = request.GET.get('UserType', '').lower()
    SessionOID = request.GET.get('SOID')
    
    # OID checks
    if not OID:
        return JsonResponse({'error': 'OID is required'}, status=400)
    if OID != '333333' and not OrganizationMaster.objects.filter(OrganizationID=OID).exists():
        return JsonResponse({'error': 'Invalid OrganizationID'}, status=400)

    # organization_id = request.GET.get('organization_id', 601)
    # Current_year = timezone.now().year
    # Current_month = timezone.now().month
    year = request.GET.get('year', 2025)
    month = request.GET.get('month', 1)

    # kra_title_sq = KRA.objects.filter(
    #     id=OuterRef('KRAID')
    # ).values('Title')[:1]

    base_filters = {
        "KraEntryMaster__SubmittedYear": year,
        "KraEntryMaster__SubmittedMonth": month,
        "KraEntryMaster__IsDelete": 0,
        "IsDelete": False,
    }

    # if UserType != "ceo" and SessionOID != 333333:
    #     base_filters["KraEntryMaster__OrganizationID"] = OID
    
    if UserType == "ceo":
        # CEO can filter by OID if provided
        if OID and OID != '333333':
            base_filters["KraEntryMaster__OrganizationID"] = OID
    else:
        # Non-CEO must be restricted to their organization
        if not OID:
            return JsonResponse({'error': 'OID is required'}, status=400)
        base_filters["KraEntryMaster__OrganizationID"] = OID
        
    qs = (
        KraEntryMasterDetails.objects
        .filter(**base_filters)
        .values(
            'KraEntryMaster__OrganizationID',
            'TargetAssignMasterDetails__AssignMaster__AssignToEmployeeCode'
        )
        .annotate(
            total=Count('id',distinct=True),

            # outstanding=Count(
            #     Case(When(Actual__isnull=True, then=1))
            # ),

            outstanding=Count(
                Case(When(Actual='Outstanding', then=1))
            ),
            
            met=Count(
                Case(When(Actual='Met', then=1))
            ),

            exceeds_expectation=Count(
                Case(When(Actual='Exceeds Expectation', then=1))
            ),

            not_met=Count(
                Case(When(Actual='Not Met', then=1))
            ),
        )
    )

    applied_ids = {r['KraEntryMaster__OrganizationID'] for r in qs}

    org_filters = {
        "IsDelete": False,
        "IsNileHotel": 1,
        "Activation_status": 1
    }

    if UserType == "ceo":
        org_filters["OrganizationID__in"] = applied_ids
    else:
        org_filters["OrganizationID"] = OID

    orgs = OrganizationMaster.objects.filter(**org_filters).values(
        "OrganizationID", "ShortDisplayLabel"
    )
    
    org_map = {o["OrganizationID"]: o["ShortDisplayLabel"] for o in orgs}


    result = []

    for r in qs:
        total = r['total'] or 0
        org_id = r['KraEntryMaster__OrganizationID']
        # EmpCode = r['KraEntryMaster__TargetAssignMasterDetails__AssignMaster_AssignToEmployeeCode']
        EmpCode = r[
            'TargetAssignMasterDetails__AssignMaster__AssignToEmployeeCode'
        ]
        hotel_name = org_map.get(org_id, "Unknown")

        exceeds_pct = round((r['exceeds_expectation'] * 100) / total, 2) if total else 0
        outstanding_pct = round((r['outstanding'] * 100) / total, 2) if total else 0
        met_pct = round((r['met'] * 100) / total, 2) if total else 0
        not_met_pct = round((r['not_met'] * 100) / total, 2) if total else 0

        result.append({
            "HTL_Goals": f"{hotel_name} ({total})",
            "HTL": hotel_name,
            "OID": org_id,
            "EmpCode": EmpCode,
            # "Exceeds Expectation": f"{r['Exceeds Expectation']} / {exceeds_pct}%",
            "Exceeds Expectation": f"{r['exceeds_expectation']} / {exceeds_pct}%",
            "Outstanding": f"{r['outstanding']} / {outstanding_pct}%",
            "Met": f"{r['met']} / {met_pct}%",
            "Not_Met": f"{r['not_met']} / {not_met_pct}%",
            "Status": "Met" if (met_pct + exceeds_pct) >= 80 else "Not Met"
        })


    return Response({
        "status": True,
        "data": result
    }, status=status.HTTP_200_OK)






@api_view(['GET'])
def kra_entry_select_api(request):
    """
    API: KRA Entry Select
    Params:
    - OID (OrganizationID)
    - year
    - month
    - UserID
    - EmpCode
    """
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    # Token checks
    if not AccessToken:
        return JsonResponse({'error': 'Token not found'}, status=400)
    if AccessToken != Fixed_Token:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    # -------------------------------
    OrganizationID = request.GET.get('OID')
    
    # OID checks
    if not OrganizationID:
        return JsonResponse({'error': 'OID is required'}, status=400)
    if OrganizationID != '333333' and not OrganizationMaster.objects.filter(OrganizationID=OrganizationID).exists():
        return JsonResponse({'error': 'Invalid OrganizationID'}, status=400)

    OrganizationID = request.GET.get('OID')
    year = request.GET.get('year')
    month = request.GET.get('month')
    UserID = request.GET.get('UserID')
    EmpCode = request.GET.get('EmpCode')

    # ------------------ Validation ------------------
    if not all([OrganizationID, year, month, UserID, EmpCode]):
        return Response(
            {"status": False, "error": "Missing required parameters"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                EXEC KRA_Entry_Select_Revised
                    @OrganizationID=%s,
                    @EntryYear=%s,
                    @EntryMonth=%s,
                    @UserID=%s,
                    @UID=%s,
                    @EmpCode=%s
                """,
                [
                    OrganizationID,
                    year,
                    month,
                    UserID,
                    UserID,   # UID same as UserID
                    EmpCode
                ]
            )

            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            # rowslist = [dict(zip(columns, row)) for row in rows]


        data = [dict(zip(columns, row)) for row in rows]
        ALLOWED_FIELDS = {
            "id",
            "Task",
            "Standard",
            "Actual",
            "ActualValue",
            "Defination",
        }

        filtered_data = [
            {key: row[key] for key in ALLOWED_FIELDS if key in row}
            for row in data
        ]

        return Response(
            {
                "status": True,
                "count": len(filtered_data),
                "data": filtered_data
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {
                "status": False,
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )





@api_view(['GET'])
def kra_entry_PDF_api(request):
    """
    API: KRA Entry Select PDF API
    Params:
    - OID (OrganizationID)
    - year
    - month
    - UserID
    - EmpCode
    """
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    # Token checks
    if not AccessToken:
        return JsonResponse({'error': 'Token not found'}, status=400)
    if AccessToken != Fixed_Token:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    # -------------------------------
    OrganizationID = request.GET.get('OID')
    
    # OID checks
    if not OrganizationID:
        return JsonResponse({'error': 'OID is required'}, status=400)
    if OrganizationID != '333333' and not OrganizationMaster.objects.filter(OrganizationID=OrganizationID).exists():
        return JsonResponse({'error': 'Invalid OrganizationID'}, status=400)

    OrganizationID = request.GET.get('OID')
    year = request.GET.get('year')
    month = request.GET.get('month')
    UserID = request.GET.get('UserID')
    EmpCode = request.GET.get('EmpCode')
    
    Org_Name = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).only("OrganizationName").first()
    month_name = calendar.month_name[int(month)]
    Current_Date = timezone.now().date()
    
    # template = "KRA/KraEnrty_View_PDF.html"

    # ------------------ Validation ------------------
    if not all([OrganizationID, year, month, UserID, EmpCode]):
        return Response(
            {"status": False, "error": "Missing required parameters"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # try:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            EXEC KRA_Entry_Select
                @OrganizationID=%s,
                @EntryYear=%s,
                @EntryMonth=%s,
                @UserID=%s,
                @UID=%s,
                @EmpCode=%s
            """,
            [
                OrganizationID,
                year,
                month,
                UserID,
                UserID,   # UID same as UserID
                EmpCode
            ]
        )

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        # rowslist = [dict(zip(columns, row)) for row in rows]


    data = [dict(zip(columns, row)) for row in rows]
    ALLOWED_FIELDS = {
        "id",
        "Task",
        "Standard",
        "Actual",
        "ActualValue",
        "Defination",
    }

    filtered_data = [
        {key: row[key] for key in ALLOWED_FIELDS if key in row}
        for row in data
    ]


    context = {
        "data": filtered_data,
        "Org_Name":Org_Name,
        "month_name":month_name,
        "Current_Date":Current_Date
    }

    template = get_template(
        "KRA/KraEnrty_View_PDF.html"
    )
    html = template.render(context)
    
    # Create PDF
    wkhtmltopdf_path = getattr(settings, 'WKHTMLTOPDF_CMD', None)

    if not wkhtmltopdf_path:
        raise Exception("WKHTMLTOPDF_CMD is not configured in settings.py")

    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    pdf = pdfkit.from_string(
        html,
        False,
        configuration=config
    )

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="KRA_Report_{Org_Name}_{month_name}_{year}.pdf"'
    )
    return response






@api_view(['GET'])
def kra_target_summary_api(request):
    """
    KRA Summary API
    Filters:
    - OrganizationID
    - SubmittedYear
    - SubmittedMonth
    """
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
    ALLOWED_USER_IDS = ['20201212180048', '20251209112591']

    if not UserID:
        return JsonResponse({'error': 'UserID is required'}, status=400)

    if UserID not in ALLOWED_USER_IDS:
        return JsonResponse({'error': 'Invalid UserID'}, status=404)
    # -------------------------------
    
    OID = request.GET.get('OID')
    UserType = request.GET.get('UserType', '').lower()
    SessionOID = request.GET.get('SOID')
    AssignBy = request.GET.get('AssignBy')
    
    # OID checks
    if not OID:
        return JsonResponse({'error': 'OID is required'}, status=400)
    if OID != '333333' and not OrganizationMaster.objects.filter(OrganizationID=OID).exists():
        return JsonResponse({'error': 'Invalid OrganizationID'}, status=400)

    # organization_id = request.GET.get('organization_id', 601)
    Current_year = timezone.now().year
    Current_month = timezone.now().month
    year = request.GET.get('year', Current_year)
    month = request.GET.get('month', Current_month)

    base_filters = {
        "AssignMaster__AssignYear": year,
        "AssignMaster__AssignMonth": month,
        "AssignMaster__IsDelete": 0,
        "IsDelete": False,
        # "AssignMaster__AssignByEmployeeCode": AssignBy,
    }

    if UserType == "ceo":
        # CEO can filter by OID if provided
        if OID and OID != '333333':
            base_filters["AssignMaster__OrganizationID"] = OID
    else:
        # Non-CEO must be restricted to their organization
        if not OID:
            return JsonResponse({'error': 'OID is required'}, status=400)
        base_filters["AssignMaster__OrganizationID"] = OID

    if AssignBy and AssignBy != '':
        base_filters["AssignMaster__AssignByEmployeeCode"] = AssignBy
        
    qs = (
        TargetAssignMasterDetails.objects
        .filter(**base_filters)
        .values(
            'AssignMaster__OrganizationID',
            'AssignMaster__AssignToEmployeeCode',
            'AssignMaster__AssignToName',
            'AssignMaster__AssignByEmployeeCode'
        )
        .annotate(
            total=Count('id',distinct=True)
        )
    )

    applied_ids = {r['AssignMaster__OrganizationID'] for r in qs}

    org_filters = {
        "IsDelete": False,
        "IsNileHotel": 1,
        "Activation_status": 1
    }

    if UserType == "ceo":
        org_filters["OrganizationID__in"] = applied_ids
    else:
        org_filters["OrganizationID"] = OID

    orgs = OrganizationMaster.objects.filter(**org_filters).values(
        "OrganizationID", "ShortDisplayLabel"
    )
    
    org_map = {o["OrganizationID"]: o["ShortDisplayLabel"] for o in orgs}

    result = []

    for r in qs:
        total = r['total'] or 0

        org_id = r['AssignMaster__OrganizationID']
        EmpCode = r['AssignMaster__AssignToEmployeeCode']
        AssignByEmpCode = r['AssignMaster__AssignByEmployeeCode']
        EmpName = r['AssignMaster__AssignToName']

        hotel_name = org_map.get(org_id, "Unknown")
        result.append({
            "HTL_Goals": f"{hotel_name} ({total})",
            "HTL": hotel_name,
            "OID": org_id,
            "AssignByEmpCode": AssignByEmpCode,
            "EmpCode": EmpCode,
            "EmpName": EmpName,
        })


    return Response({
        "status": True,
        "data": result
    }, status=status.HTTP_200_OK)







@api_view(['GET'])
def kra_target_detail_api(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    # Token checks
    if not AccessToken:
        return JsonResponse({'error': 'Token not found'}, status=400)
    if AccessToken != Fixed_Token:
        return JsonResponse({'error': 'Invalid token'}, status=400)

    month = request.GET.get('month')
    UserType = request.GET.get('UserType', '').lower()
    year = request.GET.get('year')
    assign_to = request.GET.get('AssignTo')
    assign_by = request.GET.get('AssignBy')
    oid = request.GET.get('OID')

    if not all([month, year, assign_to, assign_by, oid]):
        return Response(
            {"status": False, "error": "Missing required parameters"},
            status=400
        )

    qs = (
        TargetAssignMasterDetails.objects
        .filter(
            AssignMaster__AssignMonth=month,
            AssignMaster__AssignYear=year,
            AssignMaster__AssignToEmployeeCode=assign_to,
            AssignMaster__AssignByEmployeeCode=assign_by,
            AssignMaster__OrganizationID=oid,
            AssignMaster__IsDelete=False,
            IsDelete=False
        )
        .values(
            title=F('KRA__Title'),
            assign_to_name=F('AssignMaster__AssignToName'),
            oid=F('AssignMaster__OrganizationID'),
        )
    )

    orgs = OrganizationMaster.objects.filter(
        IsDelete=False,
        IsNileHotel=1,
        Activation_status=1
    ).values("OrganizationID", "ShortDisplayLabel")

    org_map = {o["OrganizationID"]: o["ShortDisplayLabel"] for o in orgs}

    result = []
    for r in qs:
        result.append({
            "HTL": org_map.get(r['oid'], "Unknown"),
            "Title": r['title'],
            "Name": r['assign_to_name'],
        })

    return Response({
        "status": True,
        "count": len(result),
        "data": result
    }, status=200)







@api_view(['GET'])
def kra_target_summary_Exp_api(request):
    """
    Combined KRA + Target Summary API
    """

    # ---------------- TOKEN CHECK ----------------
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization')

    if not AccessToken:
        return JsonResponse({'error': 'Token not found'}, status=400)
    if AccessToken != Fixed_Token:
        return JsonResponse({'error': 'Invalid token'}, status=400)

    # ---------------- ACCESS CHECK ----------------
    UserID = request.GET.get("UserID")
    ALLOWED_USER_IDS = ['20201212180048', '20251209112591']

    # if not UserID:
    #     return JsonResponse({'error': 'UserID is required'}, status=400)
    # if UserID not in ALLOWED_USER_IDS:
    #     return JsonResponse({'error': 'Invalid UserID'}, status=404)

    # ---------------- INPUT PARAMS ----------------
    OID = request.GET.get('OID')
    UserType = request.GET.get('UserType', '').lower()
    AssignBy = request.GET.get('AssignBy')

    if not OID:
        return JsonResponse({'error': 'OID is required'}, status=400)

    if OID != '333333' and not OrganizationMaster.objects.filter(OrganizationID=OID).exists():
        return JsonResponse({'error': 'Invalid OrganizationID'}, status=400)

    year = request.GET.get('year', timezone.now().year)
    month = request.GET.get('month', timezone.now().month)

    # ======================================================
    # 1️⃣ TARGET ASSIGN SUMMARY (SECOND API LOGIC)
    # ======================================================
    target_filters = {
        "AssignMaster__AssignYear": year,
        "AssignMaster__AssignMonth": month,
        "AssignMaster__IsDelete": 0,
        "IsDelete": False,
    }

    # if UserType == "ceo":
    if UserID in ALLOWED_USER_IDS:
        if OID != '333333':
            target_filters["AssignMaster__OrganizationID"] = OID
    else:
        target_filters["AssignMaster__OrganizationID"] = OID
        
    if UserID in ALLOWED_USER_IDS:
        UserType = "ceo"
        if AssignBy:
            target_filters["AssignMaster__AssignByEmployeeCode"] = AssignBy

    qs = (
        TargetAssignMasterDetails.objects
        .filter(**target_filters)
        .values(
            'AssignMaster__OrganizationID',
            'AssignMaster__AssignToEmployeeCode',
            'AssignMaster__AssignToName',
            'AssignMaster__AssignByEmployeeCode'
        )
        .annotate(total=Count('id', distinct=True))
    )

    # ======================================================
    # 2️⃣ ORGANIZATION MAP
    # ======================================================
    applied_org_ids = {r['AssignMaster__OrganizationID'] for r in qs}

    org_filters = {
        "IsDelete": False,
        "IsNileHotel": 1,
        "Activation_status": 1
    }

    if UserType != "ceo":
        org_filters["OrganizationID"] = OID

    orgs = OrganizationMaster.objects.filter(**org_filters).values(
        "OrganizationID", "ShortDisplayLabel"
    )

    org_map = {o["OrganizationID"]: o["ShortDisplayLabel"] for o in orgs}


    # ======================================================
    # 3️⃣ KRA SUMMARY (FIRST API LOGIC)
    # ======================================================
    kra_filters = {
        "KraEntryMaster__SubmittedYear": year,
        "KraEntryMaster__SubmittedMonth": month,
        "KraEntryMaster__IsDelete": 0,
        "IsDelete": False,
    }

    if UserType == "ceo":
        if OID != '333333':
            kra_filters["KraEntryMaster__OrganizationID"] = OID
    else:
        kra_filters["KraEntryMaster__OrganizationID"] = OID

    kra_qs = (
        KraEntryMasterDetails.objects
        .filter(**kra_filters)
        .values(
            'KraEntryMaster__OrganizationID',
            'TargetAssignMasterDetails__AssignMaster__AssignToEmployeeCode'
        )
        .annotate(
            total=Count('id', distinct=True),
            outstanding=Count(Case(When(Actual='Outstanding', then=1))),
            met=Count(Case(When(Actual='Met', then=1))),
            exceeds=Count(Case(When(Actual='Exceeds Expectation', then=1))),
            not_met=Count(Case(When(Actual='Not Met', then=1))),
        )
    )
    target_map = defaultdict(list)

    kra_map = {}
    for k in kra_qs:
        total = k['total'] or 0

        exceeds_pct = round((k['exceeds'] * 100) / total, 2) if total else 0
        outstanding_pct = round((k['outstanding'] * 100) / total, 2) if total else 0
        met_pct = round((k['met'] * 100) / total, 2) if total else 0
        not_met_pct = round((k['not_met'] * 100) / total, 2) if total else 0

        kra_map[
            (
                k['KraEntryMaster__OrganizationID'],
                k['TargetAssignMasterDetails__AssignMaster__AssignToEmployeeCode']
            )
        ] = {
            "Exceeds Expectation": f"{k['exceeds']} / {exceeds_pct}%",
            "Outstanding": f"{k['outstanding']} / {outstanding_pct}%",
            "Met": f"{k['met']} / {met_pct}%",
            "Not_Met": f"{k['not_met']} / {not_met_pct}%",
            "Status": "Met" if (met_pct + exceeds_pct) >= 80 else "Not Met"
        }

    DEFAULT_KRA = {
        "Exceeds Expectation": "0 / 0%",
        "Outstanding": "0 / 0%",
        "Met": "0 / 0%",
        "Not_Met": "0 / 0%",
        "Status": "Not Met"
    }


    target_map = defaultdict(list)
    for r in qs:
        target_map[r['AssignMaster__OrganizationID']].append(r)

    result = []
    for org_id, org_name in org_map.items():

        # Case 1️⃣: Organization HAS target data
        if org_id in target_map:
            for r in target_map[org_id]:
                emp_code = r['AssignMaster__AssignToEmployeeCode']

                row = {
                    "HTL_Goals": f"{org_name} ({r['total']})",
                    "HTL": org_name,
                    "OID": org_id,
                    "AssignByEmpCode": r['AssignMaster__AssignByEmployeeCode'],
                    "EmpCode": emp_code,
                    "EmpName": r['AssignMaster__AssignToName'],
                }

                row.update(kra_map.get((org_id, emp_code), DEFAULT_KRA))
                result.append(row)

        # Case 2️⃣: Organization has NO target assigned
        else:
            row = {
                "HTL_Goals": f"{org_name} (0)",
                "HTL": org_name,
                "OID": org_id,
                "AssignByEmpCode": "",
                "EmpCode": "",
                "EmpName": "",
            }

            row.update(DEFAULT_KRA)
            result.append(row)

    return Response(
        {"status": True, "data": result},
        status=status.HTTP_200_OK
    )
