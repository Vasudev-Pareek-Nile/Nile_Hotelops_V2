from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.http import HttpResponse, JsonResponse, response
from django.db import transaction, IntegrityError
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.contrib import messages
from urllib.parse import urlencode
from django.urls import reverse
from datetime import datetime
from xhtml2pdf import pisa
import requests

from Employee_Payroll.models import Organization_Details
from .models import TravelRequest, TravelEntry
from app.models import OrganizationMaster
from .decorators import user_id_required


# Create your views here.

# Travel_Details_List -------->
@user_id_required
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

    employee_ids = EmployeeDataSelect(OrganizationID=OrganizationID)

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
        'success_message': request.GET.get('message') if request.GET.get('success') == 'True' else None,
        'error_message': request.GET.get('message') if request.GET.get('error') == 'True' else None,
        "employees": employee_ids,
    }

    return render(request, 'Travel_Details/Travel_Details_List.html', context)


from django.db  import connection, transaction
def EmployeeDataSelect(OrganizationID=None, EmployeeCode=None,Designation =None,ReportingtoDesignation =None):
    with connection.cursor() as cursor:
        cursor.execute("EXEC SP_EmployeeMaster_For_Leave @OrganizationID=%s, @EmployeeCode=%s, @Designation=%s, @ReportingtoDesignation=%s", [OrganizationID, EmployeeCode,Designation,ReportingtoDesignation])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    rowslist = [dict(zip(columns, row)) for row in rows]
    return rowslist

# Create Travel Request Entrt -------- ---->
@user_id_required
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

    # print("RunLoop is here:", RunLoop)
    employee_ids = EmployeeDataSelect(OrganizationID=OrganizationID)

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

                    messages.success(request, "Travel request and entries updated successfully.")
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
                    messages.success(request, "Travel request and entries created successfully.")

            params = urlencode({'success': 'True', 'message': 'Travel request saved successfully.'})
            return redirect(f"{reverse('Travel_Details_List')}?{params}")

        except (IntegrityError, ValueError) as e:
            messages.error(request, f"Error: {e}")
            params = urlencode({'error': 'True', 'message': str(e)})
            return redirect(f"{reverse('Create_Travel_Request')}?{params}")
        except Exception as e:
            messages.error(request, "An unexpected error occurred while saving the travel request.")
            params = urlencode({'error': 'True', 'message': 'Unexpected error occurred.'})
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
        'RunLoop':RunLoop,
        "employees": employee_ids,
    }
    return render(request, "Travel_Details/Travel_Details_Form.html", context)



# Delete Travel Request Entry -------->
@user_id_required
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
            travel_request.deleted_by = UserID
            travel_request.save()

            # Soft delete children
            entries = TravelEntry.objects.filter(
                organization_id=User_OrganizationID,
                travel_request_id=Travel_Entry_ID,
                is_delete=False
            )
            for entry in entries:
                entry.is_delete = True
                entry.deleted_by = UserID
                entry.save()

            messages.success(request, "Travel request and entries deleted successfully.")
            params = urlencode({'success': 'True', 'message': 'Travel request deleted successfully.'})
            return redirect(f"{reverse('Travel_Details_List')}?{params}")

        except TravelRequest.DoesNotExist:
            messages.error(request, "Travel request not found.")
            params = urlencode({'error': 'True', 'message': 'Travel request not found.'})
            return redirect(f"{reverse('Travel_Details_List')}?{params}")
    
    messages.error(request, "Invalid travel request ID.")
    params = urlencode({'error': 'True', 'message': 'Invalid travel entry.'})
    return redirect(f"{reverse('Travel_Details_List')}?{params}")



# Delete Single Travel Request Entry -------->
@user_id_required
def Delete_Travel_Single_Entry(request):
    OrganizationID = request.session.get("OrganizationID")
    UserID = str(request.session.get("UserID"))

    Travel_Entry_ID_str = request.GET.get('Travel_Entry_ID', '')
    Travel_Entry_ID = int(Travel_Entry_ID_str) if Travel_Entry_ID_str else None

    TravelRequest_ID_str = request.GET.get('Travel_TravelRequest_ID', '')
    TravelRequest_ID = int(TravelRequest_ID_str) if TravelRequest_ID_str else None

    User_OrganizationID = request.GET.get('OID', '')

    if Travel_Entry_ID:
        try:
            # Soft delete the single TravelEntry by its ID
            entry = TravelEntry.objects.get(
                id=Travel_Entry_ID,
                organization_id=User_OrganizationID,
                is_delete=False
            )
            entry.is_delete = True
            entry.deleted_by = UserID
            entry.save()
            messages.success(request, "Travel entry deleted successfully.")

        except TravelEntry.DoesNotExist:
            messages.error(request, "Travel entry not found.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect(f"{reverse('Create_Travel_Request')}?Travel_Entry_ID={TravelRequest_ID}&OID={User_OrganizationID}")

    # If Travel_Entry_ID was invalid
    messages.error(request, "Invalid travel entry ID.")
    return redirect(f"{reverse('Create_Travel_Request')}?Travel_Entry_ID={TravelRequest_ID}&OID={User_OrganizationID}")



# Pdf Generation ------------>
@user_id_required
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



# views.py

from rest_framework import viewsets
from .models import TravelRequest, TravelEntry
from .serializers import TravelRequestSerializer, TravelEntrySerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone




class TravelRequestViewSet(viewsets.ModelViewSet):
    queryset = TravelRequest.objects.filter(is_delete=False)
    serializer_class = TravelRequestSerializer

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.is_delete = True
    #     instance.deleted_by = request.user.id if request.user.is_authenticated else None
    #     instance.deleted_datetime = timezone.now()
    #     instance.save()
    #     return Response({"detail": "Soft deleted."}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_delete = True
            instance.deleted_by = request.user.id if request.user.is_authenticated else None
            instance.deleted_datetime = timezone.now()
            instance.save()
            return Response({"Detail": "Record Deleted Successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(f"[Soft Delete Error]: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({"detail": "Travel request created successfully."}, status=status.HTTP_201_CREATED)
    
    def update(self, instance, validated_data):
        entries_data = validated_data.pop('entries', [])
        
        # Update TravelRequest fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Track existing entry IDs to update
        existing_ids = [entry.id for entry in instance.entries.all()]
        sent_ids = [entry.get('id') for entry in entries_data if entry.get('id')]

        # Delete removed entries
        for entry in instance.entries.all():
            if entry.id not in sent_ids:
                entry.delete()

        # Update or create entries
        for entry_data in entries_data:
            entry_id = entry_data.get('id', None)
            if entry_id:
                try:
                    entry = TravelEntry.objects.get(id=entry_id, travel_request=instance)
                    for attr, value in entry_data.items():
                        setattr(entry, attr, value)
                    entry.save()
                except TravelEntry.DoesNotExist:
                    # Entry not found, create it
                    TravelEntry.objects.create(travel_request=instance, **entry_data)
            else:
                # Create new entry
                TravelEntry.objects.create(travel_request=instance, **entry_data)

        return instance


    

class TravelEntryViewSet(viewsets.ModelViewSet):
    queryset = TravelEntry.objects.filter(is_delete=False)
    serializer_class = TravelEntrySerializer

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.is_delete = True
    #     instance.deleted_by = request.user.id if request.user.is_authenticated else None
    #     instance.deleted_datetime = timezone.now()
    #     instance.save()
    #     return Response({"detail": "Soft deleted."}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_delete = True
            instance.deleted_by = request.user.id if request.user.is_authenticated else None
            instance.deleted_datetime = timezone.now()
            instance.save()
            return Response({"Detail": "Record Deleted Successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(f"[Soft Delete Error]: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)

    #     return Response({"detail": "Travel entry created successfully."}, status=status.HTTP_201_CREATED)



