from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.http import HttpResponse, JsonResponse
from django.db import transaction, IntegrityError
from django.template.loader import get_template
from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.urls import reverse
from datetime import datetime
from xhtml2pdf import pisa
import requests

from app.models import OrganizationMaster
from Employee_Payroll.models import Organization_Details
from .models import TravelRequest, TravelEntry

# Create your views here.

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

        Total_Amount = sum(entry.fare or 0 for entry in entries)
        grand_total += Total_Amount

        travel_details.append({
            'id': travel_request.id,
            'booked_by': travel_request.booked_by,
            'organization_id':travel_request.organization_id,
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


# Experimental Code ---->
# def create_travel_request(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)

#     OrganizationID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])

#     Travel_Entry_ID_str = request.GET.get('Travel_Entry_ID', '')
#     Travel_Entry_ID = int(Travel_Entry_ID_str) if Travel_Entry_ID_str else None
#     User_OrganizationID = request.GET.get('OID', '')

#     if Travel_Entry_ID:
#         try:
#             travel_request = TravelRequest.objects.get(organization_id=User_OrganizationID, id=Travel_Entry_ID, is_delete=False)
#         except TravelRequest.DoesNotExist:
#             travel_request = None

            
#     EntriesObj = TravelEntry.objects.filter(organization_id=OrganizationID, is_delete=False, travel_request_id=Travel_Entry_ID)

#     if request.method == 'POST':
#         try:
#             with transaction.atomic():
#                 # Validate and collect basic data
#                 booked_by = request.POST.get('booked_by')
#                 name = request.POST.get('name')
#                 booking_date = request.POST.get('booking_date')



#                 if not all([booked_by, name, booking_date]):
#                     raise ValueError("Please fill in all required fields.")
                
#                 if travel_request and Travel_Entry_ID:
#                     travel_request.booked_by =  booked_by
#                     travel_request.name = name
#                     travel_request.booking_date = booking_date
#                     travel_request.modify_by = UserID

#                     travel_request.save()
#                 else:
#                     travel_request = TravelRequest.objects.create(
#                         booked_by=booked_by,
#                         name=name,
#                         booking_date=booking_date,
#                         created_by=UserID,
#                         organization_id=OrganizationID
#                     )

#                     Travel_Entry_ID = travel_request.id

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

#                 # Travel_Entry_ID = travel_request.id if travel_request else None


                
#                 if EntriesObj.exists() and Travel_Entry_ID:
#                     for i, entry in enumerate(EntriesObj):
#                         entry.travel_Date_from = travel_dates_from[i] or None

#                         # EntriesObj.travel_Date_from = travel_dates_from
#                         entry.travel_Date_to = travel_dates_to[i] or None
#                         entry.travel_route_from = travel_routes_from[i] or None
#                         entry.travel_route_to = travel_routes_to[i] or None
#                         entry.fare = fares[i] or None
#                         entry.travel_mode = travel_modes[i] or None
#                         entry.pnr = pnrs[i] or None
#                         entry.comment = comments[i] or None
#                         entry.billing = billings[i] or None
#                         entry.modify_by = UserID

#                         entry.save()
#                 else:

#                     entry_count = len(travel_dates_from)

#                     for i in range(entry_count):
#                         TravelEntry.objects.create(
#                             travel_request=travel_request,
#                             travel_Date_from=travel_dates_from[i] or None,
#                             travel_Date_to=travel_dates_to[i] or None,
#                             travel_route_from=travel_routes_from[i] or '',
#                             travel_route_to=travel_routes_to[i] or '',
#                             fare=fares[i] or 0,
#                             travel_mode=travel_modes[i] or '',
#                             pnr=pnrs[i] or '',
#                             comment=comments[i] or '',
#                             billing=billings[i] or '',
#                             organization_id=OrganizationID,
#                             created_by=UserID
#                         )

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

#     # print("Organizatoins:", memOrg)
#     context={
#         'memOrg':memOrg,
#         'travel_request':travel_request,
#         'EntriesObj':EntriesObj
#     }
#     return render(request, "Travel_Details/Travel_Details_Form.html", context)

# Create Travel Request Entrt -------- ---->
def create_travel_request(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])

    Travel_Entry_ID_str = request.GET.get('Travel_Entry_ID', '')
    Travel_Entry_ID = int(Travel_Entry_ID_str) if Travel_Entry_ID_str else None
    User_OrganizationID = request.GET.get('OID', '')

    RunLoop = "no"
    if Travel_Entry_ID is not None:
        RunLoop = "yes"

    print("RunLoop is here:", RunLoop)

    travel_request = None
    if Travel_Entry_ID:
        try:
            travel_request = TravelRequest.objects.get(
                organization_id=User_OrganizationID,
                id=Travel_Entry_ID,
                is_delete=False
            )
        except TravelRequest.DoesNotExist:
            travel_request = None

    if request.method == 'POST':
        try:
            with transaction.atomic():
                booked_by = request.POST.get('booked_by')
                name = request.POST.get('name')
                booking_date = request.POST.get('booking_date')

                if not all([booked_by, name, booking_date]):
                    raise ValueError("Please fill in all required fields.")

                if travel_request and Travel_Entry_ID:
                    travel_request.booked_by = booked_by
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

                travel_dates_from = request.POST.getlist('travel_Date_from[]')
                travel_dates_to = request.POST.getlist('travel_Date_to[]')
                travel_routes_from = request.POST.getlist('travel_route_from[]')
                travel_routes_to = request.POST.getlist('travel_route_to[]')
                fares = request.POST.getlist('fare[]')
                travel_modes = request.POST.getlist('travel_mode[]')
                pnrs = request.POST.getlist('pnr[]')
                comments = request.POST.getlist('comment[]')
                billings = request.POST.getlist('billing[]')

                EntriesObj = TravelEntry.objects.filter(
                    organization_id=OrganizationID,
                    is_delete=False,
                    travel_request_id=Travel_Entry_ID
                )

                if EntriesObj.exists() and Travel_Entry_ID:
                    for i, entry in enumerate(EntriesObj):
                        if i < len(travel_dates_from):
                            entry.travel_Date_from = travel_dates_from[i] or None
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
                    
                    # Create new entries if form has more entries than existing
                    if len(travel_dates_from) > EntriesObj.count():
                        for i in range(EntriesObj.count(), len(travel_dates_from)):
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

        params = urlencode({'error': 'True', 'message': error_message})
        return redirect(f"{reverse('Create_Travel_Request')}?{params}")

    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
        'hotel-api-token': hotelapitoken
    }
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    memOrg = []
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

    EntriesObj = TravelEntry.objects.filter(
        organization_id=OrganizationID,
        is_delete=False,
        travel_request_id=Travel_Entry_ID
    )

    print('EntriesObj', EntriesObj)
    context = {
        'memOrg': memOrg,
        'travel_request': travel_request,
        'EntriesObj': EntriesObj,
        'RunLoop':RunLoop
    }
    return render(request, "Travel_Details/Travel_Details_Form.html", context)


from django.contrib import messages

# Delete Travel Request Entry -------->
# def Delete_Travel_Request(request):
#     OrganizationID = request.session.get("OrganizationID")
#     UserID = str(request.session.get("UserID"))

#     Travel_Entry_ID_str = request.GET.get('Travel_Entry_ID', '')
#     Travel_Entry_ID = int(Travel_Entry_ID_str) if Travel_Entry_ID_str else None
#     User_OrganizationID = request.GET.get('OID', '')

#     if Travel_Entry_ID:
#         try:
#             travel_request = TravelRequest.objects.get(
#                 organization_id=User_OrganizationID,
#                 id=Travel_Entry_ID,
#                 is_delete=False
#             )
#             travel_request.is_delete = 1
#             travel_request.save()

#             EntriesObj = TravelEntry.objects.filter(
#                     organization_id=OrganizationID,
#                     is_delete=False,
#                     travel_request_id=Travel_Entry_ID
#             )

#             for i, entry in enumerate(EntriesObj):
#                 if i < len(travel_dates_from):
#                     entry.is_delete = 1
#                     entry.save()

#             messages.success(request, "The Travel Record is deleted successfully.")
#             return redirect(f"{reverse('Travel_Details_List')}?success=True")
#         except TravelRequest.DoesNotExist:
#             messages.error(request, "Travel request not found.")
#             return redirect(f"{reverse('Travel_Details_List')}?success=False")
#     else:
#         # messages.error(request, "Invalid travel entry.")
#         return redirect(f"{reverse('Travel_Details_List')}?success=False")

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

# Delete Travel Request Entry -------->
def Delete_Travel_Request(request):
    OrganizationID = request.session.get("OrganizationID")
    UserID = str(request.session.get("UserID"))

    Travel_Entry_ID_str = request.GET.get('Travel_Entry_ID', '')
    Travel_Entry_ID = int(Travel_Entry_ID_str) if Travel_Entry_ID_str else None
    User_OrganizationID = request.GET.get('OID', '')

    if Travel_Entry_ID:
        try:
            travel_request = TravelRequest.objects.get(
                organization_id=User_OrganizationID,
                id=Travel_Entry_ID,
                is_delete=False
            )

            # Soft delete parent
            travel_request.is_delete = True
            travel_request.save()

            # Soft delete children
            entries = TravelEntry.objects.filter(
                organization_id=User_OrganizationID,
                travel_request_id=Travel_Entry_ID,
                is_delete=False
            )
            for entry in entries:
                entry.is_delete = True
                entry.save()

            messages.success(request, "The Travel Record and its entries were deleted successfully.")
            return redirect(f"{reverse('Travel_Details_List')}?success=True")

        except TravelRequest.DoesNotExist:
            messages.error(request, "Travel request not found.")
            return redirect(f"{reverse('Travel_Details_List')}?success=False")

    messages.error(request, "Invalid travel entry.")
    return redirect(f"{reverse('Travel_Details_List')}?success=False")


# Pdf Generation ------------>

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


