from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.shortcuts import render,redirect
from django.utils.timezone import now
from .models import Item_Master, Entry_Master, Entry_Details
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

from datetime import datetime, date
from django.urls import reverse








logger = logging.getLogger(__name__)

def GuestVoice_Dashboard(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    UserDepartment = request.session["Department_Name"]
    UserType = request.session["UserType"]
    EmpCode=request.session["EmployeeCode"]

    # Fetch organization list from API
    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching organizations: {e}")
        memOrg = []

    #  **Fetch filter parameters from GET request**
    selected_organization = request.GET.get('hotel_name') 
    selected_date = request.GET.get('start_date')  # Selected Date

    # print("Hotel Name is:", selected_organization)
    # **Convert selected_date to date object**

    try:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date() if selected_date else date.today()
    except ValueError:
        selected_date = date.today()

    
    if not selected_organization:
        selected_organization = request.session.get("OrganizationID")

    if selected_organization:
        try:
            selected_organization = int(selected_organization)  # Convert to int
        except ValueError:
            selected_organization = None  # Handle invalid input

    # **Get organizations from database**
    if OrganizationID == '3':
        OrganizationNameDetail = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1).values('OrganizationName', 'OrganizationID')
    else:
        # Fetch only the selected organization if available
        OrganizationNameDetail = OrganizationMaster.objects.filter(
            IsDelete=False, IsNileHotel=1, Activation_status=1, OrganizationID=OrganizationID
        ).values('OrganizationName', 'OrganizationID')

    # OrganizationNameDetail = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1).values('OrganizationName', 'OrganizationID')

    # **Fetch or Create `Entry_Master` for Selected Organization & Date**
    entry_master = Entry_Master.objects.filter(
        OrganizationID=selected_organization,
        EntryDate=selected_date
    ).first()


    if not entry_master:
        entry_master = Entry_Master.objects.create(
            OrganizationID=selected_organization,
            CreatedBy=UserID,
            EntryDate=selected_date,
            CreatedDateTime=datetime.now()
        )

    # **Fetch all items**
    items = Item_Master.objects.all()

    # **Fetch existing values for the selected organization & date**
    existing_values = {
        detail.Item_Master.id: detail.Value
        for detail in Entry_Details.objects.filter(Entry_Master=entry_master)
    }

    # **Handle Form Submission**
    if request.method == "POST":
        if 'submit_GuestValue' in request.POST:
            if not selected_organization and not selected_date:
                messages.error(request, "Please select a valid organization and date.")
                return redirect("GuestVoice_Dashboard")

            values_added = False
            for key, value in request.POST.items():
                if key.startswith("value_") and value.strip():
                    item_id = key.split("_")[1]
                    try:
                        item_instance = Item_Master.objects.get(id=item_id)
                    except Item_Master.DoesNotExist:
                        messages.error(request, f"Item ID {item_id} does not exist.")
                        continue

                    #  **Check if entry exists**
                    entry_detail, created = Entry_Details.objects.get_or_create(
                        Entry_Master=entry_master,
                        Item_Master=item_instance,
                        defaults={
                            "Value": value,
                            "CreatedBy": UserID,
                            "ModifyBy": UserID,
                            "CreatedDateTime": datetime.now(),
                            "ModifyDateTime": datetime.now(),
                            "OrganizationID":selected_organization,
                        }
                    )

                    if not created:
                        # **Update existing entry**
                        entry_detail.Value = value
                        entry_detail.ModifyBy = UserID
                        entry_detail.ModifyDateTime = datetime.now()
                        entry_detail.save()

                    values_added = True

            if values_added:
                messages.success(request, "Entries updated successfully!")
            else:
                messages.warning(request, "No values were provided!")


            # return redirect("GuestVoice_Dashboard")

            # return redirect(f"/GuestVoice_Dashboard/?hotel_name={selected_organization}&start_date={selected_date}")
            url = f"{reverse('GuestVoice_Dashboard')}?hotel_name={selected_organization}&start_date={selected_date}"
            return redirect(url)

        
    ReviewPro = 'Hide'
    Medallia = 'Hide'
    Custom_messages = ''
    organization = OrganizationMaster.objects.get(
        IsDelete=False, IsNileHotel=1, Activation_status=1, OrganizationID=selected_organization
    )
    # print("Software Name::", organization.ReviewSoftware)
    if organization.ReviewSoftware == "reviewPro":
        ReviewPro = 'Show'
    elif organization.ReviewSoftware == "Medallia":
       Medallia = 'Show'
    else:
        Custom_messages = 'No Software Found'
        # return HttpResponse("No Software Found")
    # **Pass all data to the template**
    context = {
        "items": items,
        "existing_values": existing_values,
        "selected_date": selected_date,
        "selected_organization": selected_organization,  # Ensure dropdown retains selection
        "memOrg": memOrg,
        "OrganizationNameDetail": OrganizationNameDetail,
        'ReviewPro':ReviewPro,
        'Medallia':Medallia,
        'Custom_messages':Custom_messages
        # "user_organization_name":user_organization_name,
    }

    return render(request, "GuestVoice/GuestVoice_Dashboard.html", context)





# ---------------- Review System Code ------>



def landing_page(request):
    OrganizationID = request.session["OrganizationID"]
    # OrganizationID = request.session["OrganizationID"]
    # OrganizationID = 1  #review Pro
    # OrganizationID = 1001  #review Pro
    # OrganizationID = 1901  # Medallia
    print("Organization id is here::", OrganizationID)

    try:
        organization = OrganizationMaster.objects.get(
            IsDelete=False, IsNileHotel=1, Activation_status=1, OrganizationID=OrganizationID
        )
        print("Software Name::", organization.ReviewSoftware)
        if organization.ReviewSoftware == "reviewPro":
            return redirect("ReviewPro_Data_List")
        elif organization.ReviewSoftware == "Medallia":
            return redirect("Medallia_Data_List")
        else:
            return HttpResponse("No Software Found")
            # render(request, "GuestVoice/Error Page/Medallia_Data_List.html")
    except OrganizationMaster.DoesNotExist:
        return HttpResponse("No Organization Found")
        # return render(request, "GuestVoice/Error Page/error-404.html")



def Medallia_Data_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    Session_OrganizationID = request.session["OrganizationID"]
    selected_organization = request.GET.get('OID') 
    if not selected_organization:
        selected_organization = Session_OrganizationID

    # if OrganizationID == '3':
    #     Medallia_Data = MedalliaData.objects.filter(IsDelete=False)
    # else:
    #     Medallia_Data = MedalliaData.objects.filter(IsDelete=False, OrganizationID=OrganizationID)


    # if OrganizationID == '3':
    #     Medallia_Data = MedalliaData.objects.filter(IsDelete=False)
    # else:
    Medallia_Data = MedalliaData.objects.filter(IsDelete=False, OrganizationID=selected_organization)

    # organization = OrganizationMaster.objects.filter(
    #     IsDelete=False, IsNileHotel=1, Activation_status=1, OrganizationID=OrganizationID
    # ).first()  # OR use `.get()` if you're sure there is only one matching record

    # # Get the name if the record exists
    # OrganizationName = organization.OrganizationName if organization else None

    # print(OrganizationName)


    # Handling File Upload

    context = {
        'Medallia_Data': Medallia_Data,
        'selected_organization':selected_organization
    }
    return render(request, "GuestVoice/Medallia/Medallia_Data_List.html", context)



def ReviewPro_Data_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    Session_OrganizationID = request.session["OrganizationID"]
    selected_organization = request.GET.get('OID') 

    if not selected_organization:
        selected_organization = Session_OrganizationID

    
    # ReviewProData = ReviewPro.objects.filter(IsDelete=False)

    # if OrganizationID == '3':
    #     ReviewProData = ReviewPro.objects.filter(IsDelete=False)
    # else:

    ReviewProData = ReviewPro.objects.filter(IsDelete=False, OrganizationID=selected_organization)


    context = {
        'ReviewProData': ReviewProData,
        'selected_organization':selected_organization
    }
    return render(request, "GuestVoice/ReviewPro/ReviewPro_Data_List.html", context)





def Medallia_Add_Data(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    # OrganizationID = request.session["OrganizationID"]
    OrganizationID = request.GET.get('OID') 
    UserID = str(request.session["UserID"])
    UserDepartment = request.session["Department_Name"]
    UserType = request.session["UserType"]
    EmpCode=request.session["EmployeeCode"]

    # Fetch a single organization name
    organization = OrganizationMaster.objects.filter(
        IsDelete=False, IsNileHotel=1, Activation_status=1, OrganizationID=OrganizationID
    ).first()  # OR use `.get()` if you're sure there is only one matching record

    # Get the name if the record exists
    OrganizationName = organization.OrganizationName if organization else None

    # print(OrganizationName)

    # Medallia_Data = MedalliaData.objects.all()

    if request.method == "POST":
        guest_name = request.POST.get('Guest_Name')
        month = request.POST.get('month')
        check_in = request.POST.get('CheckIn')
        check_in_process = request.POST.get('CheckInProcess')
        cleanliness = request.POST.get('Cleanliness')
        condition_of_hotel = request.POST.get('ConditionOfHotel')
        woh_program_experience = request.POST.get('WOHProgramExperience')
        helpfulness_of_staff = request.POST.get('HelpfulnessofStaff')

        room_no = request.POST.get('room_no')
        response_date = request.POST.get('response_date')
        check_out = request.POST.get('check_out')
        working_order = request.POST.get('working_order')
        customer_service = request.POST.get('customer_service')
        breakfast_experience = request.POST.get('breakfast_experience')
        spa_experience = request.POST.get('spa_experience')
        hk_services = request.POST.get('hk_services')

        nps = request.POST.get('nps')
        staff_responsiveness = request.POST.get('staff_responsiveness')
        woh_app_experience = request.POST.get('woh_app_experience')
        fnb_experience = request.POST.get('fnb_experience')
        guest_needs = request.POST.get('guest_needs')
        satisfaction_lp_benefits = request.POST.get('Satisfaction_lp_benefits')
        comments = request.POST.get('comments')


        MedalliaData.objects.create(
            # EntryDate = 
            # PropertyName = 'nile',
            PropertyName = OrganizationName,
            OrganizationID = OrganizationID,
            CreatedBy = UserID,

            GuestName = guest_name, 
            Month = month, 
            CheckInDate = check_in, 
            CheckInProcess = check_in_process, 
            Cleanliness = cleanliness, 
            ConditionOfHotel = condition_of_hotel, 
            WohProgramExperience = woh_program_experience, 
            StaffHelpfulness = helpfulness_of_staff, 
            RoomNo = room_no, 
            ResponseDate = response_date, 
            CheckOutDate = check_out, 
            WorkingOrder = working_order, 
            CustomerService = customer_service, 
            BreakfastExperience = breakfast_experience, 
            SpaExperience = spa_experience, 
            DeliveryHkServices = hk_services, 
            NPS = nps, 
            StaffResponsiveness = staff_responsiveness, 
            WohAppExperience = woh_app_experience, 
            OverallFnbExperience = fnb_experience, 
            PropertyAnticipatedGuestNeeds = guest_needs, 
            LpMemberSatisfaction = satisfaction_lp_benefits, 
            Comments = comments, 
        )


        params = {
            'OID':OrganizationID
        }
        url = f"{reverse('Medallia_Data_List')}?{urlencode(params)}"
        return redirect(url)

        # return redirect("Medallia_Data_List")
    
    return render(request, "GuestVoice/Medallia/Medallia_Add_Data.html")




def ReviewPro_Add_Data(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    # OrganizationID = request.session["OrganizationID"]
    OrganizationID = request.GET.get('OID') 
    UserID = str(request.session["UserID"])
    UserDepartment = request.session["Department_Name"]
    UserType = request.session["UserType"]
    EmpCode=request.session["EmployeeCode"]

    if request.method == "POST":
        # EntryDate = request.POST.get('')
        Reviewer = request.POST.get('reviewer')
        Month = request.POST.get('month')

        ReviewRating = request.POST.get('review_rating')
        Classification = request.POST.get('classification')
        Cleanliness = request.POST.get('cleanliness')
        Location = request.POST.get('location')
        LocationScore = request.POST.get('location_score')
        Room = request.POST.get('room')
        RoomScore = request.POST.get('room_score')

        GriTM = request.POST.get('gri')
        PublishedDate = request.POST.get('published_date')
        RatingScale = request.POST.get('rating_scale')
        Service = request.POST.get('service')
        CleanlinessScore = request.POST.get('cleanliness_score')
        Value = request.POST.get('value')
        ValueScore = request.POST.get('value_score')
        Gastronomy = request.POST.get('gastronomy')
        GastronomyScore = request.POST.get('gastronomy_score')

        Country = request.POST.get('country')
        Source = request.POST.get('source')
        ReviewScore = request.POST.get('review_score')
        ServiceScore = request.POST.get('service_score')
        DepartmentRatingScale = request.POST.get('department_rating')
        ReviewTitle = request.POST.get('review_title')
        ReviewText = request.POST.get('review_text')

        ReviewPro.objects.create(
            # EntryDate = 
            Reviewer = Reviewer,
            Month = Month,
            ReviewRating = ReviewRating,
            Classification = Classification,
            Cleanliness = Cleanliness,
            Location = Location,
            LocationScore = LocationScore,
            Room = Room,
            RoomScore = RoomScore,
            GriTM = GriTM,
            PublishedDate = PublishedDate,
            RatingScale = RatingScale,
            Service = Service,
            CleanlinessScore = CleanlinessScore,
            Value = Value,
            ValueScore = ValueScore,
            Gastronomy = Gastronomy,
            GastronomyScore = GastronomyScore,
            Country = Country,
            Source = Source,
            ReviewScore = ReviewScore,
            ServiceScore = ServiceScore,
            DepartmentRatingScale = DepartmentRatingScale,
            ReviewTitle = ReviewTitle,
            ReviewText = ReviewText,

            OrganizationID = OrganizationID,
            CreatedBy = UserID,
        )

        params = {
            'OID':OrganizationID
        }
        url = f"{reverse('ReviewPro_Data_List')}?{urlencode(params)}"
        return redirect(url)

        # return redirect("ReviewPro_Data_List")
        # return HttpResponse("ReviewPro data inserted successfully")

    return render(request, "GuestVoice/ReviewPro/ReviewPro_Add_Data.html")





# --------------- Review Pro Bulk Upload
import pandas as pd
from django.shortcuts import render, redirect
# from .models import Review
from datetime import datetime
from django.contrib import messages

# def bulk_upload_reviews(request):
#     print("Enter In bulk_upload_reviews function")
#     if request.method == "POST" and request.FILES.get("excel_file_upload"):
#         print("Enter In Post Checking")

#         file = request.FILES["excel_file_upload"]
#         try:
#             print("Enter In Try Block")

#             df = pd.read_excel(file)

#             model_fields = [field.name for field in ReviewPro._meta.get_fields() if field.name != "id"]
#             print("model_fields", model_fields)


#             for index, row in df.iterrows():
#                 data = {}
#                 for column in df.columns:
#                     if column in model_fields:
#                         data[column] = row[column]

#                 # Handle missing or blank PublishedDate
#                 if not data.get("PublishedDate") or pd.isna(data.get("PublishedDate")):
#                     data["PublishedDate"] = datetime.now()

#                 # Optional: clean/convert other date fields
#                 if isinstance(data.get("EntryDate"), pd.Timestamp):
#                     data["EntryDate"] = data["EntryDate"].date()
#                 if isinstance(data.get("PublishedDate"), pd.Timestamp):
#                     data["PublishedDate"] = data["PublishedDate"].date()

#                 ReviewPro.objects.create(**data)

#             print("Bulk upload successful!")
#             messages.success(request, "Bulk upload successful!")
#         except Exception as e:
#             print("Upload failed")
#             messages.error(request, f"Upload failed: {str(e)}")

#     return redirect('ReviewPro_Data_List')

# def bulk_upload_reviews(request):
#     print("Enter In bulk_upload_reviews function")
#     if request.method == "POST" and request.FILES.get("excel_file_upload"):
#         print("Enter In Post Checking")

#         file = request.FILES["excel_file_upload"]
#         try:
#             print("Enter In Try Block")

#             df = pd.read_excel(file)

#             model_fields = [field.name for field in ReviewPro._meta.get_fields() if field.name != "id"]
#             print("model_fields", model_fields)


#             for index, row in df.iterrows():
#                 data = {}
#                 for column in df.columns:
#                     if column in model_fields:
#                         data[column] = row[column]

#                 # Optional: clean/convert datetime columns
#                 if isinstance(data.get("EntryDate"), pd.Timestamp):
#                     data["EntryDate"] = data["EntryDate"].date()
#                 if isinstance(data.get("PublishedDate"), pd.Timestamp):
#                     data["PublishedDate"] = data["PublishedDate"].date()

#                 ReviewPro.objects.create(**data)

#             print("Bulk upload successful!")
#             messages.success(request, "Bulk upload successful!")
#         except Exception as e:
#             print("Upload failed")
#             messages.error(request, f"Upload failed: {str(e)}")

#     return redirect('ReviewPro_Data_List')


from datetime import datetime
import pandas as pd

from decimal import Decimal
import pandas as pd

def clean_row_data(row_data):
    decimal_fields = [
        'GriTM', 'ReviewScore', 'ServiceScore', 'CleanlinessScore',
        'LocationScore', 'ValueScore', 'GastronomyScore', 'RoomScore'
    ]

    for field in decimal_fields:
        value = row_data.get(field)

        if pd.isna(value) or value in ['nan', '', None]:
            row_data[field] = None
        else:
            if isinstance(value, str):
                value = value.strip().replace('%', '')
            try:
                row_data[field] = Decimal(str(value))
            except:
                row_data[field] = None  # or log if needed

    # Convert other NaNs to None
    for key, value in row_data.items():
        if pd.isna(value):
            row_data[key] = None

    return row_data



def clean_row_data_madallia(row_data):
    decimal_fields = [
        'DeliveryHkServices', 'NPS', 'CustomerService', 'ConditionOfHotel',
        'WohProgramExperience', 'SpaExperience', 'StaffHelpfulness', 'PropertyAnticipatedGuestNeeds',
        'StaffResponsiveness', 'LpMemberSatisfaction', 'WohAppExperience', 'OverallFnbExperience'
    ]

    for field in decimal_fields:
        value = row_data.get(field)

        if pd.isna(value) or value in ['nan', '', None]:
            row_data[field] = None
        else:
            if isinstance(value, str):
                value = value.strip().replace('%', '')
            try:
                row_data[field] = Decimal(str(value))
            except:
                row_data[field] = None  # or log if needed

    # Convert other NaNs to None
    for key, value in row_data.items():
        if pd.isna(value):
            row_data[key] = None

    return row_data



# ------------------------ 100 % Working Code --- File Upload -----

# def bulk_upload_reviews(request):
#     if request.method == "POST" and request.FILES.get("excel_file_upload"):
#         file = request.FILES["excel_file_upload"]

#         # Read the Excel file into a DataFrame
#         DateTimeObj = datetime.now()
#         # df = pd.read_excel(file)
#         df = pd.read_excel(file, header=3)
#         df.columns = df.columns.str.strip()

#         Column_Rename = {
#             'Month ': 'Month',
#             'GRI™': 'GriTM',
#             'Reviewer': 'Reviewer',
#             'Country': 'Country',
#             'Published Date': 'PublishedDate',  
#             'Source': 'Source',
#             'Review Rating': 'ReviewRating',
#             'Rating Scale': 'RatingScale',
#             'Review Score': 'ReviewScore',
#             'Classification': 'Classification',
#             'SERVICE': 'Service',
#             'SERVICE - Score': 'ServiceScore',
#             'CLEANLINESS': 'Cleanliness',
#             'CLEANLINESS - Score': 'CleanlinessScore',
#             'LOCATION': 'Location',
#             'LOCATION - Score': 'LocationScore',
#             'VALUE': 'Value',
#             'VALUE - Score': 'ValueScore',
#             'GASTRONOMY': 'Gastronomy',
#             'GASTRONOMY - Score': 'GastronomyScore',
#             'ROOM': 'Room',
#             'ROOM - Score': 'RoomScore',
#             'Department Rating Scale': 'DepartmentRatingScale',
#             'Review Title': 'ReviewTitle',
#             'Review Text': 'ReviewText',
#         }

#         # Rename to match model
#         df.rename(columns=Column_Rename, inplace=True)
#         print(" --------- Column Renamed ----------: ")  # for debugging


        
#         # Convert PublishedDate to YYYY-MM-DD
#         if 'PublishedDate' in df.columns:
#             df['PublishedDate'] = pd.to_datetime(df['PublishedDate'], format='%d/%m/%Y', errors='coerce')



#         # Only keep columns that match model fields
#         model_fields = [f.name for f in ReviewPro._meta.get_fields() if f.name != "id"]
#         df = df[[col for col in df.columns if col in model_fields]]
#         # print("df Columns value -----:", df)  # for debugging
#         print(" ---------------------------------------------------: ")  # for debugging


#         # Fill EntryDate or PublishedDate if missing
#         # df["EntryDate"] = df["EntryDate"].fillna(DateTimeObj)
#         # First, ensure PublishedDate is properly parsed
#         if 'PublishedDate' in df.columns:
#             df['PublishedDate'] = pd.to_datetime(df['PublishedDate'], format='%d/%m/%Y', errors='coerce')

#         # Then set EntryDate = PublishedDate
#         df['EntryDate'] = df['PublishedDate']

#         # Save rows
#         # for _, row in df.iterrows():
#         #     ReviewPro.objects.create(**row.to_dict())
#         print(' --------------- Reached at top of loop-------------------')  # for debugging

#         # Clean percentage strings
#         percent_fields = ['GriTM', 'ReviewScore', 'ServiceScore', 'GastronomyScore', 'LocationScore', 'RoomScore', 'ValueScore', 'CleanlinessScore']
#         for field in percent_fields:
#             if field in df.columns:
#                 df[field] = df[field].replace('%', '', regex=True)
#                 df[field] = pd.to_numeric(df[field], errors='coerce')

#         # Replace NaN/NaT with None
#         # df = df.where(pd.notnull(df), None)

#         df = df.where(pd.notnull(df), None)
#         for _, row in df.iterrows():
#             row_data = row.to_dict()

#             # Assign missing EntryDate from PublishedDate
#             row_data["EntryDate"] = row_data.get("PublishedDate")

#             # Default values
#             row_data["OrganizationID"] = 0
#             row_data["CreatedBy"] = request.user.id if request.user.is_authenticated else 0
#             row_data["CreatedDateTime"] = DateTimeObj
#             row_data["ModifyBy"] = 0
#             row_data["ModifyDateTime"] = DateTimeObj
#             row_data["IsDelete"] = False

#             # Clean and normalize
#             row_data = clean_row_data(row_data)

#             try:
#                 ReviewPro.objects.create(**row_data)
#             except Exception as e:
#                 print("❌ Row insert failed:")
#                 print("Error:", e)
                
#                 for key, value in row_data.items():
#                     print(f" - {key}: {value} (type: {type(value)})")
#                 for key, value in row_data.items():
#                     try:
#                         field = ReviewPro._meta.get_field(key)
#                         field.clean(value, None)
#                     except Exception as ve:
#                         print(f"⚠️ Field '{key}' caused error: {ve}")

#         # Get all column names
#         # excel_columns = list(df.columns)
#         # print("Excel Columns:", excel_columns)  # for debugging

#         # Optionally, return or render them
#         # return render(request, "upload.html", {"columns": excel_columns})
#         return redirect('ReviewPro_Data_List')


#     return redirect('ReviewPro_Data_List')




# ------------------------- Try Of File Upload

from urllib.parse import urlencode
from django.urls import reverse

def bulk_upload_reviews(request):
    if request.method == "POST" and request.FILES.get("excel_file_upload"):
        file = request.FILES["excel_file_upload"]
        UserID = str(request.session["UserID"])
        # OrganizationID = request.session["OrganizationID"]
        OrganizationID = request.GET.get('OID')

        # Read the Excel file into a DataFrame
        DateTimeObj = datetime.now()
        DateAndTime =  DateTimeObj.date()

        # df = pd.read_excel(file)
        # df = pd.read_excel(file, header=3)
        df = pd.read_excel(file, header=6)
        df.columns = df.columns.str.strip()


        print("##########################################################")
        print("Requested Column Names::",  df.columns)
        
        df = df.dropna(how='all')

        Column_Rename = {
            # 'Month': 'Month',
            'GRI™': 'GriTM',
            'Reviewer': 'Reviewer',
            'Country': 'Country',
            'Published Date': 'PublishedDate',  
            'Source': 'Source',
            'Review Rating': 'ReviewRating',
            'Rating Scale': 'RatingScale',
            'Review Score': 'ReviewScore',
            'Classification': 'Classification',
            'SERVICE': 'Service',
            'SERVICE - Score': 'ServiceScore',
            'CLEANLINESS': 'Cleanliness',
            'CLEANLINESS - Score': 'CleanlinessScore',
            'LOCATION': 'Location',
            'LOCATION - Score': 'LocationScore',
            'VALUE': 'Value',
            'VALUE - Score': 'ValueScore',
            'GASTRONOMY': 'Gastronomy',
            'GASTRONOMY - Score': 'GastronomyScore',
            'ROOM': 'Room',
            'ROOM - Score': 'RoomScore',
            'Department Rating Scale': 'DepartmentRatingScale',
            'Review Title': 'ReviewTitle',
            'Review Text': 'ReviewText',
        }



        # --- Column validation ---
        expected_columns = set(Column_Rename.keys())
        uploaded_columns = set(df.columns)

        missing_columns = expected_columns - uploaded_columns
        extra_columns = uploaded_columns - expected_columns

        print("-----------------------------------------------------------------")
        print("missing_columns Column Names::",  missing_columns)

        print("##########################################################")
        print("extra_columns Column Names::",  extra_columns)

        if missing_columns:
            messages.error(request, f"Excel file is missing required columns: {', '.join(missing_columns)}")
            print("Excel file is missing required columns")
            SuccessType = False
            message = 'Missing Required Columns'
            if extra_columns:
                messages.info(request, f"Extra columns found (ignored): {', '.join(extra_columns)}")
            params = {
                'Success': SuccessType,
                'action': 'submit',
                'message': message
            }
            url = f"{reverse('ReviewPro_Data_List')}?{urlencode(params)}"
            return redirect(url)
            # return redirect('Medallia_Data_List')


        # Rename to match model
        df.rename(columns=Column_Rename, inplace=True)
        print(" --------- Column Renamed ----------: ")  # for debugging


        
        if 'PublishedDate' in df.columns:
            df['PublishedDate'] = pd.to_datetime(df['PublishedDate'], format='%d/%m/%Y', errors='coerce')


        # Only keep columns that match model fields
        model_fields = [f.name for f in ReviewPro._meta.get_fields() if f.name != "id"]
        df = df[[col for col in df.columns if col in model_fields]]
        # print("df Columns value -----:", df)  # for debugging
        print(" ---------------------------------------------------: ")  # for debugging


        # Fill EntryDate or PublishedDate if missing
        # df["EntryDate"] = df["EntryDate"].fillna(DateTimeObj)
        # First, ensure PublishedDate is properly parsed
        if 'PublishedDate' in df.columns:
            df['PublishedDate'] = pd.to_datetime(df['PublishedDate'], format='%d/%m/%Y', errors='coerce')

        # Then set EntryDate = PublishedDate
        # df['EntryDate'] = df['PublishedDate']

        if 'PublishedDate' in df.columns:
            df['PublishedDate'] = pd.to_datetime(
                df['PublishedDate'],
                format='%d-%m-%Y %H:%M:%S',  # ← exact match for "31-10-2025 23:43:39"
                errors='coerce'
            )


        df['EntryDate'] = df['PublishedDate'].apply(
            lambda x: x if pd.notnull(x) else DateAndTime
        )


        print(' --------------- Reached at top of loop-------------------')  

        # Clean percentage strings
        percent_fields = ['GriTM', 'ReviewScore', 'ServiceScore', 'GastronomyScore', 'LocationScore', 'RoomScore', 'ValueScore', 'CleanlinessScore']
        for field in percent_fields:
            if field in df.columns:
                df[field] = df[field].replace('%', '', regex=True)
                df[field] = pd.to_numeric(df[field], errors='coerce')


        # Convert NaN to '' 
        for col in df.columns:
            if df[col].dtype == 'object':  
                df[col] = df[col].fillna('')
            else:
                df[col] = df[col].where(pd.notnull(df[col]), None)

        for _, row in df.iterrows():
            row_data = row.to_dict()

            # row_data["EntryDate"] = row_data.get("PublishedDate")

            entry_date = row_data.get("PublishedDate")

            if not pd.notnull(entry_date): 
                entry_date = DateAndTime

            row_data["EntryDate"] = entry_date

            row_data["Month"] = entry_date.month if hasattr(entry_date, "month") else None

            row_data["OrganizationID"] = OrganizationID
            row_data["CreatedBy"] = UserID if UserID else 0
            row_data["CreatedDateTime"] = DateTimeObj
            row_data["ModifyBy"] = 0
            row_data["ModifyDateTime"] = DateTimeObj
            row_data["IsDelete"] = False

            row_data = clean_row_data(row_data)

            try:
                ReviewPro.objects.create(**row_data)
                print("Row data inserted Successfully.")
                SuccessType = True
                message = 'Excel File Uploaded Successfully'

            except Exception as e:
                print("Row insert failed:")
                print("Error:", e)
                SuccessType = False
                message = 'Some Error Occured'

                for key, value in row_data.items():
                    print(f" - {key}: {value} (type: {type(value)})")
                for key, value in row_data.items():
                    try:
                        field = ReviewPro._meta.get_field(key)
                        field.clean(value, None)
                    except Exception as ve:
                        print(f"Field '{key}' caused error: {ve}")

        params = {
            'Success': SuccessType,
            'action': 'submit',
            'message': message,
            'OID':OrganizationID
        }
        url = f"{reverse('ReviewPro_Data_List')}?{urlencode(params)}"
        return redirect(url)


    return redirect('ReviewPro_Data_List')


def bulk_upload_medallia(request):
    if request.method == "POST" and request.FILES.get("excel_file_upload"):
        file = request.FILES["excel_file_upload"]
        UserID = str(request.session["UserID"])
        # OrganizationID = request.session["OrganizationID"]
        OrganizationID = request.GET.get('OID') 

        DateTimeObj = datetime.now()
        DateAndTime =  DateTimeObj.date()

        df = pd.read_excel(file, header=2)
        df.columns = df.columns.str.strip()


        # df = pd.read_excel(file, keep_default_na=False, na_values=[''])
        # df = pd.read_excel(file)
        df.columns = df.columns.str.strip()
        df = df.dropna(how='all')

        print("##########################################################")
        print("Requested Column Names::",  df.columns)


        Column_Rename = {
            # 'Month':'Month',
            'Response Date':'ResponseDate',
            'Property':'PropertyName',
            'Guest Name':'GuestName',
            'Checkin date': 'CheckInDate',
            'Checkout date':'CheckOutDate',
            'Room Number':'RoomNo',
            'NPS Segment - GSS':'NPS',
            'Cleanliness of Room and bathroom - Y/N':'Cleanliness',
            'Working Order':'WorkingOrder',
            'Customer Service':'CustomerService',
            'Check-In Process':'CheckInProcess',
            'Condition of Hotel':'ConditionOfHotel',    
            'Overall Breakfast Experience':'BreakfastExperience',
            'Overall WOH Program Experience':'WohProgramExperience',   
            'Overall F&B Experience':'OverallFnbExperience',
            'Spa Experience':'SpaExperience',
            'Helpfulness Of Staff':'StaffHelpfulness',
            'Property Anticipated Guest Needs':'PropertyAnticipatedGuestNeeds',
            'Staff Responsiveness To Guest Needs':'StaffResponsiveness',
            'Satisfaction with LP Member Benefits':'LpMemberSatisfaction',
            'WOH App Experience':'WohAppExperience',
            'Overall Delivery Of Housekeeping Services':'DeliveryHkServices',
            'Comment':'Comments'
        }


        expected_columns = set(Column_Rename.keys())
        uploaded_columns = set(df.columns)

        missing_columns = expected_columns - uploaded_columns
        extra_columns = uploaded_columns - expected_columns


        print("------------------------------------------------")
        print("missing_columns Column Names::",  missing_columns)
        print("------------------------------------------------")


        if missing_columns:
            messages.error(request, f"Excel file is missing required columns: {', '.join(missing_columns)}")
            print("Excel file is missing required columns")
            SuccessType = False
            message = 'Missing Required Columns'
            if extra_columns:
                messages.info(request, f"Extra columns found (ignored): {', '.join(extra_columns)}")
                # print("Extra columns found (ignored)")
                # SuccessType = False
                # message = 'Extra columns found (ignored)'
            params = {
                'Success': SuccessType,
                'action': 'submit',
                'message': message
            }
            url = f"{reverse('Medallia_Data_List')}?{urlencode(params)}"
            return redirect(url)
            # return redirect('Medallia_Data_List')

        df.rename(columns=Column_Rename, inplace=True)


        model_fields = [f.name for f in MedalliaData._meta.get_fields() if f.name != "id"]
        df = df[[col for col in df.columns if col in model_fields]]


        df.rename(columns=Column_Rename, inplace=True)
        # print(" --------- Column Renamed ----------: ")  

        model_fields = [f.name for f in MedalliaData._meta.get_fields() if f.name != "id"]
        df = df[[col for col in df.columns if col in model_fields]]
        # print(" ---------------------------------------------------: ")  


        if 'ResponseDate' in df.columns:
            df['ResponseDate'] = pd.to_datetime(df['ResponseDate'], format='%d.%m.%Y', errors='coerce')

        if 'CheckOutDate' in df.columns:
            df['CheckOutDate'] = pd.to_datetime(df['CheckOutDate'], format='%d.%m.%Y', errors='coerce')

        if 'CheckInDate' in df.columns:
            df['CheckInDate'] = pd.to_datetime(df['CheckInDate'], format='%d.%m.%Y', errors='coerce')


        df['ResponseDate'] = df['ResponseDate'].where(pd.notnull(df['ResponseDate']), None)

        if 'ResponseDate' in df.columns:
            df['ResponseDate'] = pd.to_datetime(
                df['ResponseDate'],
                format='%d-%m-%Y %H:%M:%S',  # ← exact match for "31-10-2025 23:43:39"
                errors='coerce'
            )


        # df['EntryDate'] = df['ResponseDate'].apply(
        #     lambda x: x.strftime('%d/%m/%Y') if pd.notnull(x) else ''
        # )

        df['EntryDate'] = df['ResponseDate'].apply(
            lambda x: x if pd.notnull(x) else DateAndTime
        )

        # Convert NaN to '' 
        for col in df.columns:
            if df[col].dtype == 'object':  
                df[col] = df[col].fillna('')
                # df[col] = df[col].fillna("N/A")
            else:
                df[col] = df[col].where(pd.notnull(df[col]), None)
                # df[col] = df[col].fillna(-1) 

        # for col in df.columns:
        #     if df[col].dtype == 'object':  
        #         # leave "N/A" as-is, replace only empty cells with NULL
        #         df[col] = df[col].replace('', None)
        #     else:
        #         df[col] = df[col].where(pd.notnull(df[col]), None)


        for _, row in df.iterrows():
            row_data = row.to_dict()
            entry_date = row_data.get("ResponseDate")
            if not pd.notnull(entry_date):  
                entry_date = DateAndTime
                
            row_data["EntryDate"] = entry_date

            row_data["Month"] = entry_date.month if hasattr(entry_date, "month") else None

            row_data["OrganizationID"] = OrganizationID
            row_data["CreatedBy"] = UserID if UserID else 0
            row_data["CreatedDateTime"] = DateTimeObj
            row_data["ModifyBy"] = 0
            row_data["ModifyDateTime"] = DateTimeObj
            row_data["IsDelete"] = False

            row_data = clean_row_data_madallia(row_data)

            try:
                MedalliaData.objects.create(**row_data)
                print("Row data inserted Successfully.")
                SuccessType = True
                message = 'Excel File Uploaded Successfully'

            except Exception as e:
                print("Row insert failed:")
                print("Error:", e)
                SuccessType = False
                message = 'Some Error Occured'
                
                for key, value in row_data.items():
                    print(f" - {key}: {value} (type: {type(value)})")
                for key, value in row_data.items():
                    try:
                        field = MedalliaData._meta.get_field(key)
                        field.clean(value, None)
                    except Exception as ve:
                        print(f"Field '{key}' caused error: {ve}")

        # return redirect('Medallia_Data_List')
        params = {
            'Success': SuccessType,
            'action': 'submit',
            'message': message,
            'OID':OrganizationID
        }
        url = f"{reverse('Medallia_Data_List')}?{urlencode(params)}"
        return redirect(url)

    return redirect('Medallia_Data_List')


