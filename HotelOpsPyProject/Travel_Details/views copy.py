from django.shortcuts import render, redirect
from .models import TravelRequest, TravelEntry
from django.utils import timezone
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.urls import reverse
# Create your views here.

# def Travel_Details_List(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
    
#     OrganizationID = request.session["OrganizationID"] 
#     UserID = str(request.session["UserID"])

#     # travel_requests  = TravelRequest.objects.filter(is_delete=False)
#     travel_requests  = TravelRequest.objects.filter(organization_id=OrganizationID, is_delete=False)

#     # Build a list of dicts with travel request and its travel entries
#     travel_details = []
#     for travel_request in travel_requests:
#         entries = TravelEntry.objects.filter(
#             organization_id=OrganizationID,
#             is_delete=False,
#             travel_request_id=travel_request.id
#         )
#         Total_Amount = 0
#         for Total in entries:
#             print("Total In Entries:", Total.fare)
#             Total_Amount = Total_Amount + Total.fare

#         travel_details.append({
#             'id': travel_request.id,
#             'booked_by': travel_request.booked_by,
#             'name': travel_request.name,
#             'booking_date': travel_request.booking_date,
#             'travels': entries,  # Queryset of related travel entries
#             'Total_Amount':Total_Amount,
#         })
    
#     context = {
#         'travel_details': travel_details,
#     }
#     return render(request, 'Travel_Details/Travel_Details_List.html', context)

from datetime import datetime
from django.db.models import Q

# def Travel_Details_List(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
    
#     OrganizationID = request.session["OrganizationID"]
#     travel_requests = TravelRequest.objects.filter(organization_id=OrganizationID, is_delete=False)

#     # --- Filtering logic ---
#     booked_by = request.GET.get('BookedBy', '')
#     name = request.GET.get('BookingForName', '')
#     booking_date = request.GET.get('BookingDate', '')
#     billing = request.GET.get('Billing', '')
#     month = request.GET.get('month', '')
#     travel_mode = request.GET.get('travel_mode', '')

#     if booked_by:
#         travel_requests = travel_requests.filter(booked_by__icontains=booked_by)
#     if name:
#         travel_requests = travel_requests.filter(name__icontains=name)
#     if booking_date:
#         travel_requests = travel_requests.filter(booking_date=booking_date)
#     if month:
#         try:
#             month_num = datetime.strptime(month, "%B").month
#             travel_requests = travel_requests.filter(booking_date__month=month_num)
#         except:
#             pass

#     if billing or travel_mode:
#         entry_filters = Q()
#         if billing:
#             entry_filters &= Q(billing__icontains=billing)
#         if travel_mode:
#             entry_filters &= Q(travel_mode=travel_mode)

#         matching_ids = TravelEntry.objects.filter(entry_filters, is_delete=False, organization_id=OrganizationID).values_list('travel_request_id', flat=True)
#         travel_requests = travel_requests.filter(id__in=matching_ids)

#     # Build a list of dicts with travel request and its travel entries
#     travel_details = []
#     for travel_request in travel_requests:
#         entries = TravelEntry.objects.filter(
#             organization_id=OrganizationID,
#             is_delete=False,
#             travel_request_id=travel_request.id
#         )
#         Total_Amount = sum([entry.fare for entry in entries])
#         travel_details.append({
#             'id': travel_request.id,
#             'booked_by': travel_request.booked_by,
#             'name': travel_request.name,
#             'booking_date': travel_request.booking_date,
#             'travels': entries,
#             'Total_Amount': Total_Amount,
#         })
    
#     months = [
#         "January", "February", "March", "April", "May", "June",
#         "July", "August", "September", "October", "November", "December"
#     ]

#     travel_modes = ["Train", "Bus", "Flight", "By Road"]

#     context = {
#         'travel_details': travel_details,
#         'selected_month': datetime.now().month,
#         'filter_data': {
#             'BookedBy': booked_by,
#             'BookingForName': name,
#             'BookingDate': booking_date,
#             'Billing': billing,
#             'month': month,
#             'travel_mode': travel_mode
#         },
#         'months': months,  
#         'travel_modes': travel_modes, 
#     }
#     return render(request, 'Travel_Details/Travel_Details_List.html', context)

from datetime import datetime
import calendar
import requests
# from .models import Organization_Details

from Employee_Payroll.models import Organization_Details

def Travel_Details_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])

    # Get filter parameters
    booked_by = request.GET.get('BookedBy', '').strip()
    name = request.GET.get('BookingForName', '').strip()
    booking_date = request.GET.get('BookingDate', '').strip()
    billing = request.GET.get('Billing', '').strip()
    month = request.GET.get('month', '').strip()
    travel_mode = request.GET.get('travel_mode', '').strip()

    # Base queryset
    travel_requests = TravelRequest.objects.filter(organization_id=OrganizationID, is_delete=False).order_by('-created_datetime')

    # Apply filters
    if booked_by:
        travel_requests = travel_requests.filter(booked_by__icontains=booked_by)

    if name:
        travel_requests = travel_requests.filter(name__icontains=name)

    if booking_date:
        travel_requests = travel_requests.filter(booking_date=booking_date)

    if month:
        try:
            month_number = datetime.strptime(month, "%B").month
            travel_requests = travel_requests.filter(booking_date__month=month_number)
        except:
            pass  # Invalid month name, ignore

    # Now filter TravelEntry-level fields
    # We’ll filter these manually inside the loop for 'billing' and 'travel_mode'

    travel_details = []
    grand_total = 0

    for travel_request in travel_requests:
        entries = TravelEntry.objects.filter(
            organization_id=OrganizationID,
            is_delete=False,
            travel_request_id=travel_request.id
        )

        if billing:
            entries = entries.filter(billing__icontains=billing)

        if travel_mode:
            entries = entries.filter(travel_mode=travel_mode)

        if not entries.exists():
            continue  # Skip requests with no matching entries

        Total_Amount = sum(entry.fare for entry in entries)
        grand_total += Total_Amount

        travel_details.append({
            'id': travel_request.id,
            'booked_by': travel_request.booked_by,
            'name': travel_request.name,
            'booking_date': travel_request.booking_date,
            'travels': entries,
            'Total_Amount': Total_Amount,
        })
        # print('CurrentYear', datetime.now().year)

    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
        'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = "http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID=" + str(OrganizationID)

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")   

    # orgconfig = Organization_Details.objects.filter(OID = I,IsDelete = False)
    
    # context = {'orgconfig':orgconfig,'I':I,'memOrg':memOrg,'OrganizationID':OrganizationID}
    # return render(request, "EMP_PAY/OrgConfig/OrgConfigList.html", context)

    context = {
        'travel_details': travel_details,
        'selected_month': datetime.now().month,
        'CurrentYear': datetime.now().year,
        'filter_data': {
            'BookedBy': booked_by,
            'BookingForName': name,
            'BookingDate': booking_date,
            'Billing': billing,
            'month': month,
            'travel_mode': travel_mode
        },
        'months': [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ],
        'travel_modes': ["Train", "Bus", "Flight", "By Road"],
        'grand_total':grand_total,
        'memOrg':memOrg,
    }

    return render(request, 'Travel_Details/Travel_Details_List.html', context)


# Fully Working Code ------->
# def create_travel_request(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
    
#     OrganizationID = request.session["OrganizationID"] 
#     UserID = str(request.session["UserID"])

#     if request.method == 'POST':
#         # 1. Create the main TravelRequest instance
#         booked_by = request.POST.get('booked_by')
#         name = request.POST.get('name')
#         booking_date = request.POST.get('booking_date')

#         travel_request = TravelRequest.objects.create(
#             booked_by=booked_by,
#             name=name,
#             booking_date=booking_date,
#             created_by = UserID,
#             organization_id = OrganizationID
#         )

#         # 2. Collect multiple TravelEntry rows
#         travel_dates_from = request.POST.getlist('travel_Date_from[]')
#         travel_dates_to = request.POST.getlist('travel_Date_to[]')
#         travel_routes_from = request.POST.getlist('travel_route_from[]')
#         travel_routes_to = request.POST.getlist('travel_route_to[]')
#         fares = request.POST.getlist('fare[]')
#         travel_modes = request.POST.getlist('travel_mode[]')
#         pnrs = request.POST.getlist('pnr[]')
#         comments = request.POST.getlist('comment[]')
#         billings = request.POST.getlist('billing[]')

#         # 3. Create TravelEntry objects in a loop
#         for i in range(len(travel_dates_from)):
#             TravelEntry.objects.create(
#                 travel_request=travel_request,
#                 travel_Date_from=travel_dates_from[i] or None,
#                 travel_Date_to=travel_dates_to[i] or None,
#                 travel_route_from=travel_routes_from[i] or '',
#                 travel_route_to=travel_routes_to[i] or '',
#                 fare=fares[i] or 0,
#                 travel_mode=travel_modes[i] or '',
#                 pnr=pnrs[i] or '',
#                 comment=comments[i] or '',
#                 billing=billings[i] or '',
#                 organization_id = OrganizationID,
#                 created_by = UserID
#             )
        
#         print("Sucessfully Submit the form")

#         return redirect(f"{reverse('Travel_Details_List')}?success=True")
#     return render(request, "Travel_Details/Travel_Details_Form.html")


# def create_travel_request(request):
#     if request.method == 'POST':
#         # 1. Create the main TravelRequest instance
#         booked_by = request.POST.get('booked_by')
#         name = request.POST.get('name')
#         booking_date = request.POST.get('booking_date')

#         travel_request = TravelRequest.objects.create(
#             booked_by=booked_by,
#             name=name,
#             booking_date=booking_date,
#             CreatedDateTime=timezone.now(),
#             ModifyDateTime=timezone.now(),
#         )

#         # 2. Collect multiple TravelEntry rows
#         travel_dates_from = request.POST.getlist('travel_Date_from[]')
#         travel_dates_to = request.POST.getlist('travel_Date_to[]')
#         travel_routes_from = request.POST.getlist('travel_route_from[]')
#         travel_routes_to = request.POST.getlist('travel_route_to[]')
#         fares = request.POST.getlist('fare[]')
#         travel_modes = request.POST.getlist('travel_mode[]')
#         pnrs = request.POST.getlist('pnr[]')
#         comments = request.POST.getlist('comment[]')
#         billings = request.POST.getlist('billing[]')

#         # 3. Create TravelEntry objects in a loop
#         for i in range(len(travel_dates_from)):
#             TravelEntry.objects.create(
#                 travel_request=travel_request,
#                 travel_Date_from=travel_dates_from[i] or None,
#                 travel_Date_to=travel_dates_to[i] or None,
#                 travel_route_from=travel_routes_from[i] or '',
#                 travel_route_to=travel_routes_to[i] or '',
#                 fare=fares[i] or 0,
#                 travel_mode=travel_modes[i] or '',
#                 pnr=pnrs[i] or '',
#                 comment=comments[i] or '',
#                 billing_file=billings[i] or '',
#                 CreatedDateTime=timezone.now(),
#                 ModifyDateTime=timezone.now(),
#             )

#         return redirect('Success_Page')  # Redirect after saving
#     return render(request, "Travel_Details/Travel_Details_Form.html")



# Experimental Code ---->

from django.db import transaction, IntegrityError
from urllib.parse import urlencode


# def create_travel_request(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)

#     OrganizationID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])

#     Travel_Entry_ID = request.GET.get('Travel_Entry_ID', '')
#     # OrganizationID = request.GET.get('OID', '')

#     # travel_requestObj = TravelRequest.objects.filter(OrganizationID=OrganizationID, id=Travel_Entry_ID, is_delete=False)
#     # EntriesObj = TravelEntry.objects.filter(
#     #     organization_id=OrganizationID,
#     #     is_delete=False,
#     #     travel_request_id=Travel_Entry_ID
#     # )
    
#     if request.method == 'POST':
#         try:
#             with transaction.atomic():
#                 # Validate and collect basic data
#                 booked_by = request.POST.get('booked_by')
#                 name = request.POST.get('name')
#                 booking_date = request.POST.get('booking_date')



#                 if not all([booked_by, name, booking_date]):
#                     raise ValueError("Please fill in all required fields.")
                
#                 # if Travel_Entry_ID is not None and travel_requestObj:
#                 #     travel_requestObj.booked_by =  booked_by
#                 #     travel_requestObj.name = name
#                 #     travel_requestObj.booking_date = booking_date
#                 # else:
#                 travel_request = TravelRequest.objects.create(
#                     booked_by=booked_by,
#                     name=name,
#                     booking_date=booking_date,
#                     created_by=UserID,
#                     organization_id=OrganizationID
#                 )

#                 # Get list values
#                 travel_dates_from = request.POST.getlist('travel_Date_from[]')
#                 travel_dates_to = request.POST.getlist('travel_Date_to[]')
#                 travel_routes_from = request.POST.getlist('travel_route_from[]')
#                 travel_routes_to = request.POST.getlist('travel_route_to[]')
#                 fares = request.POST.getlist('fare[]')
#                 travel_modes = request.POST.getlist('travel_mode[]')
#                 pnrs = request.POST.getlist('pnr[]')
#                 comments = request.POST.getlist('comment[]')
#                 billings = request.POST.getlist('billing[]')

                
#                 # if Travel_Entry_ID is not None and EntriesObj:
#                 #     EntriesObj.travel_Date_from = travel_dates_from
#                 #     EntriesObj.travel_Date_to = travel_dates_to
#                 #     EntriesObj.travel_route_from = travel_routes_from
#                 #     EntriesObj.travel_route_to = travel_routes_to
#                 #     EntriesObj.fare = fares
#                 #     EntriesObj.travel_mode = travel_modes
#                 #     EntriesObj.pnr = pnrs
#                 #     EntriesObj.comment = comments
#                 #     EntriesObj.billing = billings

#                     # EntriesObj.save()
#                 # else:

#                 entry_count = len(travel_dates_from)

#                 for i in range(entry_count):
#                     TravelEntry.objects.create(
#                         travel_request=travel_request,
#                         travel_Date_from=travel_dates_from[i] or None,
#                         travel_Date_to=travel_dates_to[i] or None,
#                         travel_route_from=travel_routes_from[i] or '',
#                         travel_route_to=travel_routes_to[i] or '',
#                         fare=fares[i] or 0,
#                         travel_mode=travel_modes[i] or '',
#                         pnr=pnrs[i] or '',
#                         comment=comments[i] or '',
#                         billing=billings[i] or '',
#                         organization_id=OrganizationID,
#                         created_by=UserID
#                     )

#             return redirect(f"{reverse('Travel_Details_List')}?success=True")

#         except (IntegrityError, ValueError) as e:
#             error_message = str(e)
#         except Exception as e:
#             error_message = "Unexpected error occurred while saving data."

#         # Redirect back with error message
#         params = urlencode({'error': 'True', 'message': error_message})
#         return redirect(f"{reverse('Create_Travel_Request')}?{params}")
    
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken

#     headers = {
#         'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
#     }
#     api_url = "http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID=" + str(OrganizationID)

#     try:
#         response = requests.get(api_url, headers=headers)
#         response.raise_for_status()  # Optional: Check for any HTTP errors
#         memOrg = response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error occurred: {e}")  

#     print("Organizatoins:", memOrg)
#     context={
#         'memOrg':memOrg
#     }
#     return render(request, "Travel_Details/Travel_Details_Form.html", context)


def create_travel_request(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])

    Travel_Entry_ID_str = request.GET.get('Travel_Entry_ID', '')
    Travel_Entry_ID = int(Travel_Entry_ID_str) if Travel_Entry_ID_str else None
    User_OrganizationID = request.GET.get('OID', '')

    if Travel_Entry_ID:
        try:
            travel_request = TravelRequest.objects.get(organization_id=User_OrganizationID, id=Travel_Entry_ID, is_delete=False)
        except TravelRequest.DoesNotExist:
            travel_request = None

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Validate and collect basic data
                booked_by = request.POST.get('booked_by')
                name = request.POST.get('name')
                booking_date = request.POST.get('booking_date')



                if not all([booked_by, name, booking_date]):
                    raise ValueError("Please fill in all required fields.")
                
                if travel_request and Travel_Entry_ID:
                    travel_request.booked_by =  booked_by
                    travel_request.name = name
                    travel_request.booking_date = booking_date
                    travel_request.modify_by = UserID

                    travel_request.save()
                else:
                    travel_request = TravelRequest.objects.create(
                        booked_by=booked_by,
                        name=name,
                        booking_date=booking_date,
                        created_by=UserID,
                        organization_id=OrganizationID
                    )
                    
                    Travel_Entry_ID = travel_request.id

                # Get list values
                travel_dates_from = request.POST.getlist('travel_Date_from[]')
                travel_dates_to = request.POST.getlist('travel_Date_to[]')
                travel_routes_from = request.POST.getlist('travel_route_from[]')
                travel_routes_to = request.POST.getlist('travel_route_to[]')
                fares = request.POST.getlist('fare[]')
                travel_modes = request.POST.getlist('travel_mode[]')
                pnrs = request.POST.getlist('pnr[]')
                comments = request.POST.getlist('comment[]')
                billings = request.POST.getlist('billing[]')

                # Travel_Entry_ID = travel_request.id if travel_request else None

                EntriesObj = TravelEntry.objects.filter(
                        organization_id=OrganizationID,
                        is_delete=False,
                        travel_request_id=Travel_Entry_ID
                )

                
                if EntriesObj.exists() and Travel_Entry_ID:
                    for i, entry in enumerate(EntriesObj):
                        entry.travel_Date_from = travel_dates_from[i] or None

                        # EntriesObj.travel_Date_from = travel_dates_from
                        entry.travel_Date_to = travel_dates_to[i] or None
                        entry.travel_route_from = travel_routes_from[i] or None
                        entry.travel_route_to = travel_routes_to[i] or None
                        entry.fare = fares[i] or None
                        entry.travel_mode = travel_modes[i] or None
                        entry.pnr = pnrs[i] or None
                        entry.comment = comments[i] or None
                        entry.billing = billings[i] or None
                        entry.modify_by = UserID

                        entry.save()
                else:

                    entry_count = len(travel_dates_from)

                    for i in range(entry_count):
                        TravelEntry.objects.create(
                            travel_request=travel_request,
                            travel_Date_from=travel_dates_from[i] or None,
                            travel_Date_to=travel_dates_to[i] or None,
                            travel_route_from=travel_routes_from[i] or '',
                            travel_route_to=travel_routes_to[i] or '',
                            fare=fares[i] or 0,
                            travel_mode=travel_modes[i] or '',
                            pnr=pnrs[i] or '',
                            comment=comments[i] or '',
                            billing=billings[i] or '',
                            organization_id=OrganizationID,
                            created_by=UserID
                        )

            return redirect(f"{reverse('Travel_Details_List')}?success=True")

        except (IntegrityError, ValueError) as e:
            error_message = str(e)
        except Exception as e:
            error_message = "Unexpected error occurred while saving data."

        # Redirect back with error message
        params = urlencode({'error': 'True', 'message': error_message})
        return redirect(f"{reverse('Create_Travel_Request')}?{params}")
    
    hotelapitoken = MasterAttribute.HotelAPIkeyToken

    headers = {
        'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = "http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID=" + str(OrganizationID)

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")  

    # print("Organizatoins:", memOrg)
    context={
        'memOrg':memOrg,
        # 'travel_request':travel_request
    }
    return render(request, "Travel_Details/Travel_Details_Form.html", context)



from datetime import datetime
from datetime import date,timedelta, timezone
from app.models import OrganizationMaster
from django.template.loader import get_template
from django.http import HttpResponse, JsonResponse
from xhtml2pdf import pisa

# def Travel_Details_Data_PDF(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")


#     booked_by = request.GET.get('BookedBy', None)
#     booking_date = request.GET.get('BookingDate', None)
#     billing = request.GET.get('Billing', None)
    
#     OrganizationID = request.session["OrganizationID"] 
#     UserID = str(request.session["UserID"])

#     # travel_requests  = TravelRequest.objects.filter(is_delete=False)
#     # if booked_by is None
#     travel_requests  = TravelRequest.objects.filter(organization_id=OrganizationID, is_delete=False, booked_by=booked_by, booking_date=booking_date)

#     # Build a list of dicts with travel request and its travel entries
#     travel_details = []
#     for travel_request in travel_requests:
#         entries = TravelEntry.objects.filter(
#             organization_id=OrganizationID,
#             is_delete=False,
#             travel_request_id=travel_request.id,
#             billing=billing,
#         )

#         Total_Amount = 0
#         for Total in entries:
#             print("Total In Entries:", Total.fare)
#             Total_Amount = Total_Amount + Total.fare

#         travel_details.append({
#             'id': travel_request.id,
#             'booked_by': travel_request.booked_by,
#             'name': travel_request.name,
#             'booking_date': travel_request.booking_date,
#             'travels': entries,  # Queryset of related travel entries
#             'Total_Amount':Total_Amount,
#         })

#     base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
#     organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
#     organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

#     organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
#     organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
#     organization_logo = organizations.OrganizationName
#     # print(organization_logo)

#     current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
#     context = {
#          'travel_details': travel_details,
#         'organization_logo': organization_logo,
#         'organization_logos':organization_logos,
#         'current_datetime':current_datetime,
#     }

#     template_path = 'Travel_Details/Travel_Details_Data_PDF.html'
#     # template_path = 'LMS/APOOVAL/EmpLeaveDataPdf.html'
#     template = get_template(template_path)
#     html = template.render(context).encode("UTF-8")

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="Travel_Details_{organization_logo}.pdf"'
#     # response['Content-Disposition'] = f'attachment; filename="{organization_logo}_{start_date}__To__{end_date}.pdf"'

#     pisa_status = pisa.CreatePDF(html, dest=response, encoding="UTF-8")

#     if pisa_status.err:
#         return HttpResponse("Error generating PDF", status=500)

#     return response



def Travel_Details_Data_PDF(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])

    # Get filter parameters
    booked_by = request.GET.get('BookedBy', '').strip()
    name = request.GET.get('BookingForName', '').strip()
    booking_date = request.GET.get('BookingDate', '').strip()
    billing = request.GET.get('Billing', '').strip()
    month = request.GET.get('month', '').strip()
    travel_mode = request.GET.get('travel_mode', '').strip()

    # Base queryset
    travel_requests = TravelRequest.objects.filter(organization_id=OrganizationID, is_delete=False)

    # Apply filters
    if booked_by:
        travel_requests = travel_requests.filter(booked_by__icontains=booked_by)

    if name:
        travel_requests = travel_requests.filter(name__icontains=name)

    if booking_date:
        travel_requests = travel_requests.filter(booking_date=booking_date)

    if month:
        try:
            month_number = datetime.strptime(month, "%B").month
            travel_requests = travel_requests.filter(booking_date__month=month_number)
        except:
            pass  # Invalid month name, ignore

    # Now filter TravelEntry-level fields
    # We’ll filter these manually inside the loop for 'billing' and 'travel_mode'

    travel_details = []
    for travel_request in travel_requests:
        entries = TravelEntry.objects.filter(
            organization_id=OrganizationID,
            is_delete=False,
            travel_request_id=travel_request.id
        )

        if billing:
            entries = entries.filter(billing__icontains=billing)

        if travel_mode:
            entries = entries.filter(travel_mode=travel_mode)

        if not entries.exists():
            continue  # Skip requests with no matching entries

        Total_Amount = sum(entry.fare for entry in entries)

        travel_details.append({
            'id': travel_request.id,
            'booked_by': travel_request.booked_by,
            'name': travel_request.name,
            'booking_date': travel_request.booking_date,
            'travels': entries,
            'Total_Amount': Total_Amount,
        })

    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

    organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    organization_logo = organizations.OrganizationName
    # print(organization_logo)

    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    context = {
        'travel_details': travel_details,
        'organization_logo': organization_logo,
        'organization_logos':organization_logos,
        'current_datetime':current_datetime,
        'travel_details': travel_details,
        'selected_month': datetime.now().month,
        'filter_data': {
            'BookedBy': booked_by,
            'BookingForName': name,
            'BookingDate': booking_date,
            'Billing': billing,
            'month': month,
            'travel_mode': travel_mode
        },
        'months': [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ],
        'travel_modes': ["Train", "Bus", "Flight", "By Road"]
    }

    template_path = 'Travel_Details/Travel_Details_Data_PDF.html'
    # template_path = 'LMS/APOOVAL/EmpLeaveDataPdf.html'
    template = get_template(template_path)
    html = template.render(context).encode("UTF-8")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Travel_Details_{organization_logo}.pdf"'
    # response['Content-Disposition'] = f'attachment; filename="{organization_logo}_{start_date}__To__{end_date}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response, encoding="UTF-8")

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response


