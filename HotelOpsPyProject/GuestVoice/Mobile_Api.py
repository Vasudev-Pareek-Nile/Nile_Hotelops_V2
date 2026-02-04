# from hotelopsmgmtpy.GlobalConfig import MasterAttribute
# from django.shortcuts import render,redirect
# from django.utils.timezone import now
# from .models import Item_Master, Entry_Master, Entry_Details
from django.contrib import messages
import requests
from rest_framework.views import APIView
from rest_framework import status
# from .serializers import EntryDetailsSerializer
from .serializers import EntryDetailsSerializer, MedalliaDataSerializer, ReviewProSerializer
from rest_framework.response import Response
from datetime import datetime, date
from app.models import OrganizationMaster
import logging

from django.http import HttpResponse
from .models import MedalliaData, ReviewPro
from django.db.models import Avg
from collections import defaultdict


from django.db.models import Count, Q, Avg
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from datetime import datetime





# Full Forms 
# "OID": -- OrganizationID
# "OName": -- Organization Name
# "ED": -- Entry Date
# "RR": -- Review Rating
# "CS": -- CustomerService
# "WO": -- Working Order
# "CLS": -- Cleanliness
# 'SW': -- Sowftware

# ----- ReviewPro and Medallia API ---->
def safe_avg(values):
    vals = [v for v in values if v is not None]
    return round(sum(vals) / len(vals), 2) if vals else 0


class Review_Medallia_Average_Mobile_API(APIView):
    def get(self, request):
        Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'

        AccessToken = request.headers.get('Authorization', '')
        OrganizationID = request.GET.get("OID")
        # entry_date_obj = request.GET.get("entry_date")
        From_entry_date_obj = request.GET.get("From")
        # To_entry_date_obj = request.GET.get("To") 
        To_entry_date_obj = request.GET.get("TO") or From_entry_date_obj

        if not AccessToken:
            return HttpResponse('Token Not Found, Please Provide Correct Token.', content_type='text/plain')

        if AccessToken != Fixed_Token:
            return HttpResponse('Please Provide The Correct Token, Token Not Match.', content_type='text/plain')


        # try:
        #     if entry_date_obj:
        #         entry_date = datetime.strptime(entry_date_obj, "%d-%m-%Y").date()
        #     else:
        #         return HttpResponse('Please Provide Date.', content_type='text/plain')
        # except ValueError:
        #     return HttpResponse('Date format must be DD-MM-YYYY.', content_type='text/plain')
        
        if not OrganizationID:
            return HttpResponse('error": "Organization ID is required.', content_type='text/plain')

        if not OrganizationMaster.objects.filter(OrganizationID=OrganizationID).exists():
            return HttpResponse('error": "Organization Not Found.', content_type='text/plain')


        try:
            if From_entry_date_obj:
                from_date_obj = datetime.strptime(From_entry_date_obj, "%d-%m-%Y").date()
                to_date_obj = datetime.strptime(To_entry_date_obj, "%d-%m-%Y").date() if To_entry_date_obj else from_date_obj
            else:
                return HttpResponse('error": "Both From and To dates are required.', content_type='text/plain')
        except ValueError:
            return None, Response({"error": "Date format must be DD-MM-YYYY"}, status=status.HTTP_400_BAD_REQUEST)

        # # ---------------- DATA FETCH ----------------
        # reviewpro_qs = ReviewPro.objects.filter(IsDelete=False, EntryDate=entry_date)
        # medallia_qs = MedalliaData.objects.filter(IsDelete=False, EntryDate=entry_date)

        reviewpro_qs = ReviewPro.objects.filter(
            IsDelete=False,
            EntryDate__range=(from_date_obj, to_date_obj)
        )
        medallia_qs = MedalliaData.objects.filter(
            IsDelete=False,
            EntryDate__range=(from_date_obj, to_date_obj)
        )


        reviewpro_data = reviewpro_qs.values("EntryDate", "ReviewRating", "OrganizationID", 'Cleanliness', 'Service')
        medallia_data = medallia_qs.values("EntryDate", "NPS", "OrganizationID", 'CustomerService', 'WorkingOrder', 'Cleanliness')

        # ---------------- NORMALIZE ----------------
        # medallia_normalized = []
        # nps_Data = ['promoters','passives']
        # for item in medallia_data:
        #     medallia_normalized.append({
        #         "EntryDate": item["EntryDate"],
        #         # "ReviewRating": float(item["NPS"]) if item["NPS"] is not None else None,
        #         "ReviewRating": 10 if item.get("NPS") == "Yes" else (0 if item.get("NPS") == "Detractors" else None),
        #         "OrganizationID": item["OrganizationID"],
        #         "CustomerService": float(item["CustomerService"]) if item["CustomerService"] is not None else None,
        #         "WorkingOrder": 1 if str(item.get("WorkingOrder", "")).lower() == "no" else None,
        #         "Cleanliness": 1 if str(item.get("Cleanliness", "")).lower() == "no" else None,

        #         "Cleanliness": 10 if item.get("Cleanliness") == "Yes" else (0 if item.get("Cleanliness") == "No" else None),
        #         "WorkingOrder": 10 if item.get("WorkingOrder") == "Yes" else (0 if item.get("WorkingOrder") == "No" else None),
        #     })

        # ---------------- NORMALIZE ----------------
        medallia_normalized = []

        for item in medallia_data:
            nps_value = str(item.get("NPS", "")).strip().lower()

            # Convert NPS text to numeric
            if nps_value == "promoters":
                review_rating = 10
            elif nps_value == "passives":
                review_rating = 5
            elif nps_value == "detractors":
                review_rating = 0
            else:
                review_rating = None

            medallia_normalized.append({
                "EntryDate": item["EntryDate"],
                "ReviewRating": review_rating,
                "OrganizationID": item["OrganizationID"],
                "CustomerService": float(item["CustomerService"]) if item["CustomerService"] not in [None, ""] else None,

                "Cleanliness": 10 if str(item.get("Cleanliness", "")).lower() == "yes" else (
                    0 if str(item.get("Cleanliness", "")).lower() == "no" else None
                ),
                "WorkingOrder": 10 if str(item.get("WorkingOrder", "")).lower() == "yes" else (
                    0 if str(item.get("WorkingOrder", "")).lower() == "no" else None
                ),
            })


        reviewpro_normalized = []
        for item in reviewpro_data:
            reviewpro_normalized.append({
                "EntryDate": item["EntryDate"],
                "ReviewRating": float(item["ReviewRating"]) if item["ReviewRating"] is not None else None,
                "OrganizationID": item["OrganizationID"],
                "CustomerService": float(item["Service"]) if item.get("Service") is not None else None,
                "WorkingOrder": 0,
                "Cleanliness": float(item["Cleanliness"]) if item.get("Cleanliness") is not None else None,
            })

        combined = medallia_normalized + reviewpro_normalized

        # ---------------- GROUP BY ORG ----------------
        group_map = defaultdict(list)
        for item in combined:
            key = item["OrganizationID"]
            group_map[key].append(item)

        calculated_results = {}
        for (org_id), items in group_map.items():
            avg_rating = safe_avg([i["ReviewRating"] for i in items])
            avg_customer_service = safe_avg([i["CustomerService"] for i in items])
            avg_working_order = safe_avg([i["WorkingOrder"] for i in items])  # No = 1
            avg_cleanliness = safe_avg([i["Cleanliness"] for i in items])    # No = 1


            org = OrganizationMaster.objects.filter(OrganizationID=org_id).first()
            org_name = org.ShortDisplayLabel if org else "Unknown"
            org_software = org.ReviewSoftware if org else "Unknown"

            calculated_results[org_id] = {
                "OID": org_id,
                "OName": org_name,
                "ED_From": from_date_obj,
                "ED_To": to_date_obj,
                "RR": round(avg_rating, 2),
                "CS": round(avg_customer_service, 2),
                "WO": round(avg_working_order, 2),
                "CLS": round(avg_cleanliness, 2),
                "SW": org_software,
                "ED_From": from_date_obj,
                "ED_To": to_date_obj,
            }

        # ---------------- FINAL: ALL ORGS ----------------
        if OrganizationID == '3':
            all_orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1, IsNileHotel=1)
        else:
            all_orgs = OrganizationMaster.objects.filter(OrganizationID=OrganizationID, IsDelete=False, Activation_status=1, IsNileHotel=1)


        lengthofhotels = all_orgs.count()
        print(f"Total Hotels: {lengthofhotels}")
            
        result = []

        for org in all_orgs:
            if org.OrganizationID in calculated_results:
                result.append(calculated_results[org.OrganizationID])
            else:
                # No data → default zero values
                result.append({
                    "OID": org.OrganizationID,
                    "OName": org.ShortDisplayLabel,
                    "RR": 0.0,
                    "CS": 0.0,
                    "WO": 0.0,
                    "CLS": 0.0,
                    "SW": org.ReviewSoftware,
                    "ED_From": from_date_obj,
                    "ED_To": to_date_obj,
                    # "ED_To": entry_date,
                })

        return Response(result, status=status.HTTP_200_OK)



import re
def prettify_column_name(name):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', name)


# -- Review Pro ---->

# Utility Function For ReviewPro API
def Get_Filtered_ReviewPro_Queryset(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
 
    AccessToken = request.headers.get('Authorization', '')
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    organization_id = request.GET.get("OID")

    if not AccessToken:
        # return HttpResponse('Token Not Found, Please Provide Correct Token.',content_type='text/plain')
        return None, Response({"error": "Token Not Found, Please Provide Correct Token."}, status=status.HTTP_400_BAD_REQUEST)
    

    if AccessToken != Fixed_Token:
        # return HttpResponse('Please Provide The Correct Token, Token Not Match.',content_type='text/plain')
        return None, Response({"error": "Please Provide The Correct Token, Token Not Match"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate UserType


    if not organization_id:
        return None, Response({"error": "Organization ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not from_date:
        return None, Response({"error": "Both from_date and to_date are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        from_date_obj = datetime.strptime(from_date, "%d-%m-%Y").date()
        to_date_obj = datetime.strptime(to_date, "%d-%m-%Y").date() if to_date else from_date_obj
    except ValueError:
        return None, Response({"error": "Date format must be DD-MM-YYYY"}, status=status.HTTP_400_BAD_REQUEST)

    if not OrganizationMaster.objects.filter(OrganizationID=organization_id).exists():
        return None, Response({"error": f"Organization Not Found: {organization_id}"}, status=status.HTTP_404_NOT_FOUND)

    queryset = ReviewPro.objects.filter(
        EntryDate__range=(from_date_obj, to_date_obj),
        OrganizationID=organization_id,
        IsDelete=False
    )

    if not queryset.exists():
        return None, Response({
            "message": f"No data found between {from_date} and {to_date} for organization ID {organization_id}"
        }, status=status.HTTP_404_NOT_FOUND)

    return queryset, None



# ALl data in one --- Review Pro
class ReviewPro_Entire_Data(APIView):
    def get(self, request):
        queryset, error_response = Get_Filtered_ReviewPro_Queryset(request)
        if error_response:
            return error_response

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date") or from_date

        rating_fields = [
            'GriTM', 'ReviewRating', 'RatingScale',
            'Service', 'Cleanliness', 'Location', 'Room', 'Value', 'Gastronomy','DepartmentRatingScale',

            'ReviewScore','ServiceScore', 'CleanlinessScore', 'LocationScore', 'RoomScore',
            'ValueScore', 'GastronomyScore'
        ]

        rating_fields_hundred = [
            'GriTM', 'ReviewScore',
            'ServiceScore', 'CleanlinessScore', 'LocationScore', 'RoomScore',
            'ValueScore', 'GastronomyScore'
        ]

        results = []
        for field in rating_fields:
            avg = queryset.aggregate(avg=Avg(field))['avg']

            if avg is None:
                avg = 0.0  
        
            percentage = float(avg)  


            if field == 'GriTM':
                field = 'GRIᵀᴹ'
            else:
                field = prettify_column_name(field)

            results.append({
                'Title': field,
                # 'Title': field,
                'Average': round(percentage, 2),  # percentage value
                'From': from_date,
                'To': to_date if to_date else from_date,
                'HasData': avg != 0.0
            })

        return Response(results, status=status.HTTP_200_OK)


# Comments Of guest (Guest Reviews)
class Guest_Reviews_ReviewPro(APIView):
    def get(self, request):
        queryset, error_response = Get_Filtered_ReviewPro_Queryset(request)
        if error_response:
            return error_response

        # from_date = request.GET.get("from_date")
        # to_date = request.GET.get("to_date") or from_date

        # print("From date is here", from_date)
        # print("To is here", to_date)


        results = list(queryset.values('ReviewTitle', 'ReviewText', 'PublishedDate', 'ReviewScore'))


        raw_results  = list(queryset.values('ReviewTitle', 'ReviewText', 'PublishedDate', 'ReviewScore', 'Reviewer', 'Classification'))

        # print("DEBUG:", queryset.query)
        # print("COUNT:", queryset.count())
        # print(list(queryset.values('id', 'ReviewTitle', 'Reviewer', 'PublishedDate')))

        results = []
        for r in raw_results:
            score = r.get("ReviewScore")
            score = round(score / 10, 1) if score is not None else None  # normalize score out of 10

            results.append({
                "Title": r.get("ReviewTitle") or "",   # normalize name
                "Text": r.get("ReviewText") or "",
                "Date": r.get("PublishedDate"),
                "Reviewer": r.get("Reviewer"),
                "Clf": r.get("Classification"),
                "Score": score
            })


        return Response(results, status=status.HTTP_200_OK)




# ALl data in one --- Medallia
class Medallia_Data_ByDate_APIView_Mobile(APIView):
    def get(self, request):
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        organization_id = request.GET.get("OID")

        # 1. Validate input
        if not organization_id:
            return Response({"error": "OrganizationID (OID) is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not from_date:
            return Response({"error": "Both from_date and to_date are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from_date_obj = datetime.strptime(from_date, "%d-%m-%Y").date()
            if from_date_obj:
                if to_date:
                    to_date_obj = datetime.strptime(to_date, "%d-%m-%Y").date()
                else:
                    to_date_obj = from_date_obj  # fallback
        except ValueError:
            return Response({"error": "Date format must be DD-MM-YYYY"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Validate organization
        if not OrganizationMaster.objects.filter(OrganizationID=organization_id).exists():
            return Response({"error": f"Invalid OrganizationID: {organization_id}"}, status=status.HTTP_404_NOT_FOUND)

        # 3. Filter ReviewPro records
        queryset = MedalliaData.objects.filter(
            EntryDate__range=(from_date_obj, to_date_obj),
            OrganizationID=organization_id,
            IsDelete=False
        )

        if not queryset.exists():
            return Response({
                "message": f"No data found between {from_date} and {to_date} for organization ID {organization_id}"
            }, status=status.HTTP_404_NOT_FOUND)

        rating_fields = [
            'CheckInProcess', 'ConditionOfHotel', 'WohProgramExperience', 'CustomerService',
            'BreakfastExperience', 'SpaExperience', 'DeliveryHkServices', 'NPS', 'StaffHelpfulness', 
            'WohAppExperience', 'OverallFnbExperience', 'PropertyAnticipatedGuestNeeds', 'LpMemberSatisfaction'
        ]

        results = []
        for field in rating_fields:
            avg = queryset.aggregate(avg=Avg(field))['avg']
            if avg is not None:

                if field == 'StaffHelpfulness':
                    percentage = float(avg)  
                else:
                    percentage = (float(avg) / 10.0) * 100  
                
                results.append({
                    'Title': prettify_column_name(field),
                    # 'Column_name': field,
                    'Average': round(percentage, 2),
                    'From': from_date,
                    'To': to_date if to_date else from_date,
                })

        return Response(results, status=status.HTTP_200_OK)
    



# ----------------- Parts Of Madallia -----------------

# Utility Function For Medallia API
def get_filtered_medallia_queryset(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
 
    AccessToken = request.headers.get('Authorization', '')
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    organization_id = request.GET.get("OID")

    if not AccessToken:
        # return HttpResponse('Token Not Found, Please Provide Correct Token.',content_type='text/plain')
        return None, Response({"error": "Token Not Found, Please Provide Correct Token."}, status=status.HTTP_400_BAD_REQUEST)
    

    if AccessToken != Fixed_Token:
        # return HttpResponse('Please Provide The Correct Token, Token Not Match.',content_type='text/plain')
        return None, Response({"error": "Please Provide The Correct Token, Token Not Match"}, status=status.HTTP_400_BAD_REQUEST)
    


    if not organization_id:
        return None, Response({"error": "Organization ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not from_date:
        return None, Response({"error": "Both from_date and to_date are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        from_date_obj = datetime.strptime(from_date, "%d-%m-%Y").date()
        to_date_obj = datetime.strptime(to_date, "%d-%m-%Y").date() if to_date else from_date_obj
    except ValueError:
        return None, Response({"error": "Date format must be DD-MM-YYYY"}, status=status.HTTP_400_BAD_REQUEST)

    if not OrganizationMaster.objects.filter(OrganizationID=organization_id).exists():
        return None, Response({"error": f"Organization Not Found: {organization_id}"}, status=status.HTTP_404_NOT_FOUND)

    print("from date obj is here::", from_date_obj)
    print("to date obj is here::", to_date_obj)
    print("organization id is here::", organization_id)
    queryset = MedalliaData.objects.filter(
        EntryDate__range=(from_date_obj, to_date_obj),
        OrganizationID=int(organization_id),
        IsDelete=False
    )

    if not queryset.exists():
        return None, Response({
            "message": f"No data found between {from_date} and {to_date} for organization ID {organization_id}"
        }, status=status.HTTP_404_NOT_FOUND)

    return queryset, None



# Medallia_Core_Metrics
# class Medallia_Core_Metrics(APIView):
#     def get(self, request):
#         queryset, error_response = get_filtered_medallia_queryset(request)
#         if error_response:
#             return error_response

#         from_date = request.GET.get("from_date")
#         to_date = request.GET.get("to_date") or from_date

#         yes_no_fields = ['Cleanliness', 'WorkingOrder']
#         numeric_fields = ['CustomerService', 'NPS']
#         Other_Filds = ['NPS']
#         results = []

#         for field in yes_no_fields:
#             total = queryset.count()
#             yes_count = queryset.filter(**{field: 'Yes'}).count()
#             Averge = (yes_count / total) * 10 if total > 0 else 0.0
            
#             results.append({
#                 'Column_name': prettify_column_name(field),
#                 # 'Average': round(percentage, 2),
#                 'Average': round(Averge, 2),
#                 # 'Average': yes_count,
#                 'From': from_date,
#                 'To': to_date,
#             })

#         if field == 'NPS' :
#             total = queryset.count()
#             data_filds = ['Promoters','Passives']
#             yes_count = queryset.filter(**{field: data_filds}).count()
#             Averge = (yes_count / total) * 10 if total > 0 else 0.0
            
#             results.append({
#                 'Column_name': prettify_column_name(field),
#                 # 'Average': round(percentage, 2),
#                 'Average': round(Averge, 2),
#                 # 'Average': yes_count,
#                 'From': from_date,
#                 'To': to_date,
#             })

#         for field in numeric_fields:
#             avg = queryset.aggregate(avg=Avg(field))['avg']
#             # if avg is not None:

#             if avg is None:
#                 avg = 0.0  

#             percentage = float(avg) 

#             if field == 'NPS':
#                 field = 'NPS'
#             else:
#                 field = prettify_column_name(field)

#             results.append({
#                 'Title': field,
#                 'Average': round(percentage, 2),
#                 'From': from_date,
#                 'To': to_date,
#             })

#         return Response({"CORE_METRICS": results}, status=status.HTTP_200_OK)


class Medallia_Core_Metrics(APIView):
    def get(self, request):
        queryset, error_response = get_filtered_medallia_queryset(request)
        if error_response:
            return error_response

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date") or from_date

        yes_no_fields = ['Cleanliness', 'WorkingOrder']
        numeric_fields = ['CustomerService']
        nps_field = 'NPS'  # handle NPS separately

        results = []

        for field in yes_no_fields:
            total = queryset.count()
            yes_count = queryset.filter(**{field: 'Yes'}).count()
            average = (yes_count / total) * 10 if total > 0 else 0.0

            results.append({
                'Column_name': prettify_column_name(field),
                'Average': round(average, 2),
                'From': from_date,
                'To': to_date,
            })

        # total = queryset.count()
        # nps_categories = ['Promoters', 'Passives']
        # nps_count = queryset.filter(**{f"{nps_field}__in": nps_categories}).count()
        # # print("nps count is here::", nps_count)
        # nps_average = (nps_count / total) * 10 if total > 0 else 0.0

        total = queryset.count()
        nps_count = queryset.filter(
            Q(NPS__iexact='promoters') | Q(NPS__iexact='passives')
        ).count()
        nps_average = (nps_count / total) * 10 if total > 0 else 0.0


        results.append({
            'Column_name': prettify_column_name(nps_field),
            'Average': round(nps_average, 2),
            'From': from_date,
            'To': to_date,
        })

        for field in numeric_fields:
            avg_value = queryset.aggregate(avg=Avg(field))['avg'] or 0.0

            results.append({
                'Title': prettify_column_name(field),
                'Average': round(float(avg_value), 2),
                'From': from_date,
                'To': to_date,
            })

        return Response({"CORE_METRICS": results}, status=status.HTTP_200_OK)


# Housekeeping and Engineering  -------------- >
class Medallia_Housekeeping_Engineering(APIView):
    def get(self, request):
        queryset, error_response = get_filtered_medallia_queryset(request)
        if error_response:
            return error_response

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date") or from_date

        rating_fields = [
            'DeliveryHkServices', 'ConditionOfHotel'
        ]

        results = []
        for field in rating_fields:
            avg = queryset.aggregate(avg=Avg(field))['avg']
            # if avg is not None:

            if avg is None:
                avg = 0.0  

            percentage = float(avg) 
            # percentage = (float(avg) / 10.0) * 100
            results.append({
                'Title': prettify_column_name(field),
                'Average': round(percentage, 2), 
                'From': from_date,
                'To': to_date if to_date else from_date,
            })

        
        # return Response(results, status=status.HTTP_200_OK)
        return Response({"House_Eng": results}, status=status.HTTP_200_OK)

    

# Front Office  -------------- >
class Medallia_Front_Office(APIView):
    def get(self, request):
        queryset, error_response = get_filtered_medallia_queryset(request)
        if error_response:
            return error_response

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date") or from_date

        rating_fields = [
            'StaffResponsiveness',
            'CustomerService',
            'CheckInProcess', 
            'StaffHelpfulness', 
        ]

        results = []
        for field in rating_fields:
            avg = queryset.aggregate(avg=Avg(field))['avg']
            # if avg is not None:

            if avg is None:
                avg = 0.0  
            
            percentage = float(avg) 

            results.append({
                'Title': prettify_column_name(field),
                'Average': round(percentage, 2),
                'From': from_date,
                'To': to_date if to_date else from_date,
            })

        
        # return Response(results, status=status.HTTP_200_OK)
        return Response({"Front_Office": results}, status=status.HTTP_200_OK)
    
    


# food and beverage  -------------- >
class Medallia_Food_And_Beverage(APIView):
    def get(self, request):
        queryset, error_response = get_filtered_medallia_queryset(request)
        if error_response:
            return error_response

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date") or from_date

        rating_fields = [
            'OverallFnbExperience',
            'BreakfastExperience',
        ]

        results = []
        for field in rating_fields:
            avg = queryset.aggregate(avg=Avg(field))['avg']
            # if avg is not None:

            if avg is None:
                avg = 0.0  

            percentage = float(avg) 
            # percentage = (float(avg) / 10.0) * 100
            results.append({
                'Title': prettify_column_name(field),
                'Average': round(percentage, 2), 
                'From': from_date,
                'To': to_date if to_date else from_date,
            })

        # return Response(results, status=status.HTTP_200_OK)
        return Response({"Food_Beverage": results}, status=status.HTTP_200_OK)

    

# Customer_Other_Services  -------------- >
class Medallia_Customer_Other_Services(APIView):
    def get(self, request):
        queryset, error_response = get_filtered_medallia_queryset(request)
        if error_response:
            return error_response

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date") or from_date

        rating_fields = [
            'SpaExperience',
            'WohAppExperience',
            'PropertyAnticipatedGuestNeeds',
            'LpMemberSatisfaction',
            'WohProgramExperience',
        ]

        results = []
        for field in rating_fields:
            avg = queryset.aggregate(avg=Avg(field))['avg']
            # if avg is not None:
                # percentage = (float(avg) / 10.0) * 100

            if avg is None:
                avg = 0.0  

            percentage = float(avg) 
            results.append({
                'Title': prettify_column_name(field),
                'Average': round(percentage, 2), 
                'From': from_date,
                'To': to_date if to_date else from_date,
            })

        # return Response(results, status=status.HTTP_200_OK)
        return Response({"Cust_Other_Serv": results}, status=status.HTTP_200_OK)
    
    

# Comments Of guest (Guest Reviews)
class Guest_Comment_Medallia_Mobile_Api(APIView):
    def get(self, request):
        queryset, error_response = get_filtered_medallia_queryset(request)
        if error_response:
            return error_response

        # from_date = request.GET.get("from_date")
        # to_date = request.GET.get("to_date") or from_date

        # ✅ Correct way to collect comments
        results = [
            {
            'Comment': obj.Comments or "",
            'Rating': obj.NPS,
            'Date': obj.ResponseDate,
            'Property': obj.PropertyName,
            'GName': obj.GuestName,
            'RoomNo': obj.RoomNo,
            }
            for obj in queryset
            # if obj.Comments  # Optional: skip empty comments
        ]

        # return Response(results, status=status.HTTP_200_OK)
        return Response({"Medallia_Comments": results}, status=status.HTTP_200_OK)
    


# Customer Service And Experience Drivers  -------------- >
class Medallia_Customer_Service_And_Experience_Drivers(APIView):
    def get(self, request):
        queryset, error_response = get_filtered_medallia_queryset(request)
        if error_response:
            return error_response

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date") or from_date

        rating_fields = [
            'CustomerService',
            'CheckInProcess', 
            'ConditionOfHotel', 
            'OverallFnbExperience',
            'BreakfastExperience', 
            'WohProgramExperience',
        ]

        results = []

        for field in rating_fields:
            total_count = queryset.exclude(**{f"{field}__isnull": True}).count()
            if total_count == 0:
                continue  # Skip if there's no data

            avg = queryset.aggregate(avg=Avg(field))[f'avg']

            # Count Detractors (< 5), Passives (5-7), Promoters (> 7)
            detractor_count = queryset.filter(**{f"{field}__lt": 5}).count()
            passive_count = queryset.filter(**{f"{field}__gte": 5, f"{field}__lte": 7}).count()
            promoter_count = queryset.filter(**{f"{field}__gt": 7}).count()

            # Calculate percentages
            # detractor_pct = round((detractor_count / total_count) * 100, 1)
            # passive_pct = round((passive_count / total_count) * 100, 1)
            # promoter_pct = round((promoter_count / total_count) * 100, 1)
            # avg_pct = round((float(avg) / 10.0) * 100, 1)

            # detractor_pct = detractor_count / total_count
            # passive_pct = passive_count / total_count
            # promoter_pct = promoter_count / total_count
            # avg_pct = float(avg)

            detractor_pct = detractor_count 
            passive_pct = passive_count 
            promoter_pct = promoter_count 
            avg_pct = float(avg)
            TotalReviewer = detractor_count+ passive_count + promoter_count

            results.append({
                'Title': prettify_column_name(field),
                'Detractor': detractor_pct,
                'Passive': passive_pct,
                'Promoter': promoter_pct,
                # 'Total': avg_pct,
                'Total': TotalReviewer,
                'From': from_date,
                'To': to_date
            })

        # return Response(results, status=status.HTTP_200_OK)
        return Response({"Cust_Ser_Exp_Driv": results}, status=status.HTTP_200_OK)
    


# Medallia_Top_Issues
class Medallia_Top_Issues(APIView):
    def get(self, request):
        queryset, error_response = get_filtered_medallia_queryset(request)
        if error_response:
            return error_response

        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date") or from_date

        yes_no_fields = ['Cleanliness', 'WorkingOrder']
        numeric_fields = [
            'CustomerService',
            'CheckInProcess', 
            'ConditionOfHotel', 
            'OverallFnbExperience',
            'BreakfastExperience', 
            'WohProgramExperience',
            'StaffHelpfulness',
        ]
        results = []

        for field in yes_no_fields:
            total = queryset.count()
            No_count = queryset.filter(**{field: 'No'}).count()
            # percentage = (yes_count / total) * 100 if total > 0 else 0.0

            results.append({
                'Title': prettify_column_name(field),
                'Issue_Count': No_count,
                'From': from_date,
                'To': to_date,
            })

        for field in numeric_fields:
            # avg = queryset.aggregate(avg=Avg(field))['avg']
            Issue_Count = queryset.filter(**{f"{field}__lt": 5}).count()
            if Issue_Count is not None:
                # percentage = (float(avg) / 10.0) * 100
                results.append({
                    'Title': prettify_column_name(field),
                    'Issue_Count': Issue_Count,
                    'From': from_date,
                    'To': to_date,
                })

        return Response({"Issues": results}, status=status.HTTP_200_OK)











#  ----------------- Old API For Softwares  ----------------------------------
# Only Medallia Data Show
class MedalliaDataByDateAPIView(APIView):
    def get(self, request):
        entry_date = request.GET.get("entry_date")
        organization_id = request.GET.get("OID")

        # Step 1: Validate required fields
        if not organization_id:
            return Response({"error": "OrganizationID (OID) is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not entry_date:
            return Response({"error": "entry_date is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Check if Organization exists
        org_exists = OrganizationMaster.objects.filter(OrganizationID=organization_id).exists()
        if not org_exists:
            return Response({"error": f"Invalid OrganizationID: {organization_id}"}, status=status.HTTP_404_NOT_FOUND)

        # Step 3: Query data
        queryset = MedalliaData.objects.filter(
            EntryDate=entry_date,
            OrganizationID=organization_id,
            IsDelete=False
        )

        if not queryset.exists():
            return Response({
                "message": f"No data found for entry_date {entry_date} and organization ID {organization_id}"
            }, status=status.HTTP_404_NOT_FOUND)

        # Step 4: Return data
        serialized_data = MedalliaDataSerializer(queryset, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)




# Only Review Pro data Show
class ReviewProDataByDateAPIView(APIView):
    def get(self, request):
        entry_date = request.GET.get("entry_date")
        organization_id = request.GET.get("OID")

        # Step 1: Validate required fields
        if not organization_id:
            return Response({"error": "OrganizationID (OID) is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not entry_date:
            return Response({"error": "entry_date is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Check if Organization exists
        org_exists = OrganizationMaster.objects.filter(OrganizationID=organization_id).exists()
        if not org_exists:
            return Response({"error": f"Invalid OrganizationID: {organization_id}"}, status=status.HTTP_404_NOT_FOUND)

        # Step 3: Fetch ReviewPro data
        queryset = ReviewPro.objects.filter(
            EntryDate=entry_date,
            OrganizationID=organization_id,
            IsDelete=False
        )

        if not queryset.exists():
            return Response({
                "message": f"No data found for entry_date {entry_date} and organization ID {organization_id}"
            }, status=status.HTTP_404_NOT_FOUND)

        # Step 4: Serialize and return
        serialized_data = ReviewProSerializer(queryset, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)

