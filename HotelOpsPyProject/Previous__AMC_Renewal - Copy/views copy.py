from django.http import HttpResponse, JsonResponse
from django.db import connection
from datetime import datetime, date
# Create your views here.
from .models import AMC_Entry_Master # Ensure your model is correctly imported
from app.models import OrganizationMaster  # Ensure your model is correctly imported
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now
from django.utils import timezone


def EmployeeDataSelect(OrganizationID=None, EmployeeCode=None,Designation =None,ReportingtoDesignation =None):
    with connection.cursor() as cursor:
        cursor.execute("EXEC SP_EmployeeMaster_For_Leave @OrganizationID=%s, @EmployeeCode=%s, @Designation=%s, @ReportingtoDesignation=%s", [OrganizationID, EmployeeCode,Designation,ReportingtoDesignation])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    rowslist = [dict(zip(columns, row)) for row in rows]
    return rowslist



# def AMC_View_Data(request, id=7000):
def AMC_View_Data(request, id):

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    Emp_code = request.session["EmployeeCode"]
    UserDepartment = request.session["Department_Name"]
    UserType = request.session["UserType"]

    entry = AMC_Entry_Master.objects.filter(EquipmentID=id).first()  
    

    if entry:  
        AMCType = entry.AMCType
        AMCAmount = entry.AMC_Amount
        AMC_Start_Date = entry.AMC_Start_Date
        AMC_End_Date = entry.AMC_End_Date
        FC_Status = entry.FC_Status
        GM_Status = entry.GM_Status
        CEO_Status = entry.CEO_Status
        EquipmentID = entry.id
        # EquipmentID = entry.EquipmentID EquipmentID

    else: 
        AMCType = None
        AMCAmount = None
        AMC_Start_Date = None
        AMC_End_Date = None
        FC_Status = None
        GM_Status = None
        CEO_Status = None
        EquipmentID = None


    # entry = AMC_Entry_Master.objects.filter(EquipmentID=id).first()
    formatted_datetime = timezone.now()

    if request.method == "POST":
            status = request.POST.get("status")  
            remarks = request.POST.get("remarks")  
            print("Page status:", status)
            print("Page remark:", remarks)

            if entry: 
                if status: 
                    if UserType.lower() =="gm":
                        entry.GM_Status = status
                        entry.GM_ActionBy = UserID
                        entry.Remarks = remarks
                        entry.GM_ActionDateTime = formatted_datetime
                        messages.success(request, "GM Status updated successfully!")

                    elif UserType.lower() =="hod" and UserDepartment.lower() =="finance":
                        entry.FC_Status = status
                        entry.FC_ActionBy = UserID
                        entry.Remarks = remarks
                        entry.FC_ActionDateTime = formatted_datetime
                        messages.success(request, "FC Status updated successfully!")

                    elif UserType.lower() == "ceo":
                        entry.CEO_Status = status
                        entry.CEO_ActionBy = UserID
                        entry.Remarks = remarks
                        entry.CEO_ActionDateTime = formatted_datetime
                        # if status == "Approved":
                        entry.Final_Status = status
                        messages.success(request, "CEO Status updated successfully!")

                    entry.save() 
                    # update_amc_details(id=1, equipment_id=101, organization_id=5, user_id=200)
                    if status == "Approved" and UserType.lower() == "ceo":
                        update_amc_details(id=entry.id, equipment_id=id, organization_id=OrganizationID, user_id=UserID)
                else:
                    messages.error(request, "No valid status received.!")
            else:
                messages.error(request, f"No entry found for EquipmentID: {id}")

            return redirect("AMC_Data_List")  


    Context = {
        "equipment_id": id,
        "AMCType": AMCType,
        "AMCAmount": AMCAmount,
        "AMC_Start_Date": AMC_Start_Date,
        "AMC_End_Date": AMC_End_Date,
        "FC_Status":FC_Status,
        "GM_Status":GM_Status,
        "CEO_Status":CEO_Status,
        "EquipmentID":EquipmentID,
    }
    return render(request, "AMC_Renewal/AMC_View_Data.html", Context)


# Stored Procedure For AMC_View_Data function ---->
def update_amc_details(id, equipment_id, organization_id, user_id):
    with connection.cursor() as cursor:
        cursor.execute("EXEC SP_EquipmentMGMT_AMCDetails_Update %s, %s, %s, %s", 
                       [id, equipment_id, organization_id, user_id])
        
# End Stored Procedure / ---->



def AMC_Data_List(request):
    OrganizationID = request.session.get("OrganizationID")  
    if not OrganizationID:
        return HttpResponse("OrganizationID not found in session", status=400)

    # Fetch session details
    UserDepartment = request.session.get("Department_Name", "").lower()
    UserType = request.session.get("UserType", "").lower()

    # print('UserType:', UserType)
    # print('UserDepartment:', UserDepartment)

    # Fetching all organizations for dropdown
    if OrganizationID=='3':
        OrganizationNameDetail = OrganizationMaster.objects.filter(IsDelete=False,Activation_status=1,IsNileHotel=True).values('OrganizationName', 'OrganizationID')
    else:
        OrganizationNameDetail = OrganizationMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID,Activation_status=1,IsNileHotel=True).values('OrganizationName', 'OrganizationID')

    # Get filters from request parameters
    selected_status = request.GET.get('status', 'Pending') 
    if selected_status=='':
        selected_status="Pending"

    selected_organization = request.GET.get('hotel_name', OrganizationID) 
    # selected_organization = 3

    # print("selected_organization --------->")
    # print(selected_organization)

    # Convert selected organization to integer (if valid)
    try:
        selected_organization = int(selected_organization)
        # selected_organization = int(selected_organization) if selected_organization else OrganizationID
    except ValueError:
        selected_organization = OrganizationID  

    # Define allowed status filters
    status_filter = {"Pending", "Approved", "Rejected", "Return"}  

    # Fetch data based on user type and their approval logic
    equipment_data = None

    if UserType == "gm":
        equipment_data = get_equipment_details_AMC_List(
            organization_id=selected_organization,
            fc_status="Approved",  
            gm_status=selected_status if selected_status in status_filter else None  # Apply status filter
        )
    elif UserType == "hod" and UserDepartment == "finance":
        equipment_data = get_equipment_details_AMC_List(
            organization_id=selected_organization,
            fc_status=selected_status if selected_status in status_filter else "Pending"
        )
    elif UserType == "ceo":
        # equipment_data = get_equipment_details_AMC_List(
        #     organization_id=selected_organization,
        #     gm_status="Approved",
        #     ceo_status=selected_status if selected_status in status_filter else "Pending"
        # )
        if selected_organization != 3:
            # equipment_data = get_equipment_details_AMC_List(organization_id=selected_organization)
            equipment_data = get_equipment_details_AMC_List(
                organization_id=selected_organization,
                gm_status="Approved",
                ceo_status=selected_status if selected_status in status_filter else "Pending"
            )
        else:
            # equipment_data = get_equipment_details_AMC_List(organization_id=OrganizationID)
            equipment_data = get_equipment_details_AMC_List(
                # organization_id=OrganizationID,
                gm_status="Approved",
                ceo_status=selected_status if selected_status in status_filter else "Pending"
            )
    else:
        # Other users only see their organization’s data (without status filtering)
        equipment_data = get_equipment_details_AMC_List(organization_id=selected_organization)

        # Other users see only their organization's data unless they explicitly select another
        # if selected_organization != OrganizationID:
        #     equipment_data = get_equipment_details_AMC_List(organization_id=selected_organization)
        # else:
        #     equipment_data = get_equipment_details_AMC_List(organization_id=OrganizationID)


    # Ensure an empty list is returned if no data is found
    if not equipment_data:
        equipment_data = []
    
    # Pass data to template
    Context = {
        'equipment_data': equipment_data,
        "OrganizationNameDetail": OrganizationNameDetail,
        "selected_status": selected_status,  # Maintain selected value in dropdown
        "selected_organization": selected_organization,  # Maintain selected org
    }
        
    return render(request, 'AMC_Renewal/AMC_Data_List.html', Context)



# Call Store Procedure for AMC_Data_List -- This is only API.
def AMC_List_equipment_view(request):
    OrganizationID = request.session.get("OrganizationID")  # Use .get() to avoid KeyError
    if not OrganizationID:
        return HttpResponse("OrganizationID not found in session", status=400)
    
    equipment_data = get_equipment_details_AMC_List(organization_id=OrganizationID)  # Example: Fetch details for OrganizationID=1
    return JsonResponse({'data': equipment_data})


# Call Store Procedure for AMC_Data_List.
def get_equipment_details_AMC_List(id=0, equipment_id=0, organization_id=0, fc_status='', gm_status='', ceo_status=''):
    with connection.cursor() as cursor:
        sql = """
            EXEC SP_EquipmentMGMT_EntryMaster_Details 
            @ID=%s, @EquipmentID=%s, @OrganizationID=%s, 
            @FCStatus=%s, @GMStatus=%s, @CEOStatus=%s
        """
        cursor.execute(sql, [id, equipment_id, organization_id, fc_status, gm_status, ceo_status])
        result = cursor.fetchall()

        # Fetch column names
        columns = [col[0] for col in cursor.description]

        # print("DEBUG: Data received from SQL procedure ->", result)

    # Convert the result to a list of dictionaries
    data = [dict(zip(columns, row)) for row in result]
    
    return data


def get_equipment_profile(id):
    with connection.cursor() as cursor:
        cursor.execute("EXEC SP_EquipmentMGMT_Profile_Select %s", [id])  # ✅ Use EXEC
        result = cursor.fetchall()

        # Fetch column names
        columns = [col[0] for col in cursor.description]

        # Convert result into list of dictionaries
        data = [dict(zip(columns, row)) for row in result]

    return data



def equipment_profile_view(request, id):
    """Fetch equipment details based on ID and return as JSON."""
    # print(f"Fetching data for ID: {id}")  # Debugging: Print ID
    data = get_equipment_profile(id)

    # print("Fetched Data:", data)  # Debugging: Print Data

    return JsonResponse(data, safe=False)



# For get the form value ----------->





# Download pdf --------------->
from django.template.loader import get_template
from xhtml2pdf import pisa
from collections import defaultdict
from django.shortcuts import render, get_object_or_404

def download_AMC_View_Data_pdf(request, equipment_id):
    EmployeeCode = request.GET.get('EmployeeCode')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    leave_type = request.GET.get('leave_type')
    leave_status = request.GET.get('status')
    total_credit = request.GET.get('total_credit')
    OrganizationID = request.session.get("OrganizationID")


    # Base filter query

    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

    organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    organization_logo = organizations.OrganizationName


    # equipment = get_object_or_404(AMC_Entry_Master, id=equipment_id)
    equipment_data = get_equipment_details_AMC_List(id=equipment_id)

    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    # Prepare context for the PDF template
    context = {
        "equipment_data":equipment_data,
        'organization_logo': organization_logo,
        'organization_logos':organization_logos,
        'start_date':start_date,
        'end_date':end_date,
        'current_datetime':current_datetime,
        # 'entry':entry,
    }

    template_path = 'AMC_Renewal/AMC_View_Data_PDF.html'
    template = get_template(template_path)
    html = template.render(context).encode("UTF-8")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{organization_logo}_Equipment_Report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response, encoding="UTF-8")

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response


# Dashboard and store in Azure blob storage.
from .azure import upload_file_to_blob, ALLOWED_EXTENTIONS
from pathlib import Path

def AMC_Renewal_Dashboard(request, id=None):
    """Render template and handle AMC form submission."""
    
    OrganizationID = request.session.get("OrganizationID", 0)
    UserID = str(request.session.get("UserID", 0))

    selected_date = request.GET.get('start_date')

    # Convert selected_date string to date object
    if selected_date:
        try:
            selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            selected_date = date.today()  # Default to today's date
    else:
        selected_date = date.today()

    
    amc_entry = None  

    # Retrieve existing AMC entry if available
    if id:
        amc_entry = AMC_Entry_Master.objects.filter(
            EquipmentID=id, OrganizationID=OrganizationID
        ).first()

    # Handle Form Submission
    if request.method == "POST":
        if 'Submit_AMC_Value' in request.POST:
            EquipmentID = id  # Get Equipment ID from URL
            AMC_Start_Date = request.POST.get("AMC_Start_Date")
            AMC_End_Date = request.POST.get("AMC_End_Date")
            AMCType = request.POST.get("AMCMode")  # Capturing AMC Type
            AMC_Amount = float(request.POST.get("AMCAmount") or 0)  # Storing Amount in float

            VendorName = request.POST.get("VendorName")
            VendorEmailAddress = request.POST.get("VendorEmailAddress")
            VendorMobileNumber = request.POST.get("VendorMobileNumber")  
            VendorSecondMobileNumber = request.POST.get("VendorSecondMobileNumber")  
            VendorLandlineNumber = request.POST.get("VendorLandlineNumber")  
            vendorCity = request.POST.get("vendorCity")  
            VendorState = request.POST.get("VendorState")  
            VendorPinCode = request.POST.get("VendorPinCode")  
            VendorAdress = request.POST.get("VendorAdress")

            Documentfile = request.FILES.get('UploadDocument')

            if Documentfile:
                ext = Path(Documentfile.name).suffix.lower()
                print(f"Extension: {ext}")

            # Check for missing required fields
            if not (AMC_Start_Date and AMC_End_Date and AMCType):
                messages.error(request, "All fields are required!")
            else:
                # Try to fetch existing record
                amc_entry, created = AMC_Entry_Master.objects.update_or_create(
                    EquipmentID=EquipmentID,
                    OrganizationID=OrganizationID,
                    defaults={
                        "AMC_Start_Date": AMC_Start_Date,
                        "AMC_End_Date": AMC_End_Date,
                        "AMCType": AMCType,
                        "AMC_Amount": AMC_Amount,
                        "created_by": UserID,

                        "VendorName": VendorName,
                        "VendorEmailAddress": VendorEmailAddress,
                        "VendorMobileNumber": VendorMobileNumber,
                        "VendorSecondMobileNumber": VendorSecondMobileNumber,
                        "VendorLandlineNumber": VendorLandlineNumber,
                        "VendorAddress": VendorAdress,
                        "VendorCity": vendorCity,
                        "VendorState": VendorState,
                        "VendorPincode": VendorPinCode,
                    }
                )
                # startDate = amc_entry.AMC_Start_Date

                if created:
                    messages.success(request, "AMC Entry Created Successfully!")
                else:
                    messages.success(request, "AMC Entry Updated Successfully!")

                # Upload document to Azure and store file path in DB
                if Documentfile:
                    uploaded_file = upload_file_to_blob(Documentfile, amc_entry.id)
                    if uploaded_file:
                        messages.success(request, f"{Documentfile.name} uploaded successfully!")
                    else:
                        messages.warning(request, f"File format not supported. Allowed: {', '.join(ALLOWED_EXTENTIONS)}")
                    # return redirect('emplistloi')

                return redirect(request.path)

    context = {
        "equipment_id": id,
        "selected_date": selected_date,
        "OrganizationID": OrganizationID,
        "UserID": UserID,
        "amc_entry": amc_entry,
        # "startDate":startDate
    }
    return render(request, "AMC_Renewal/AMC_Dashboard.html", context)




# Not working But usable
# def AMC_Renewal_Dashboard(request, id=None):
#     """Render template and handle AMC form submission."""
    
#     OrganizationID = request.session.get("OrganizationID", 0)
#     UserID = str(request.session.get("UserID", 0))

#     selected_date = request.GET.get('start_date')

#     # Convert selected_date string to date object
#     if selected_date:
#         try:
#             selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
#         except ValueError:
#             selected_date = date.today()  # Default to today's date
#     else:
#         selected_date = date.today()

    
#     amc_entry = None  

#     # Retrieve existing AMC entry if available
#     if id:
#         amc_entry = AMC_Entry_Master.objects.filter(
#             EquipmentID=id, OrganizationID=OrganizationID
#         ).first()

#     # # Handle Form Submission
#     # if request.method == "POST":
#     #     if 'Submit_AMC_Value' in request.POST:
#     #         EquipmentID = id  # Get Equipment ID from URL
#     #         AMC_Start_Date = request.POST.get("AMC_Start_Date")
#     #         AMC_End_Date = request.POST.get("AMC_End_Date")
#     #         AMCType = request.POST.get("AMCMode")  # Capturing AMC Type
#     #         AMC_Amount = request.POST.get("AMCAmount", 0)  # Storing Amount
#     #         Documentfile = request.FILES.get('UploadDocument')

#     #         VendorName = request.POST.get("VendorName")
#     #         VendorEmailAddress = request.POST.get("VendorEmailAddress")
#     #         VendorMobileNumber= request.POST.get("VendorMobileNumber")  
#     #         VendorSecondMobileNumber= request.POST.get("VendorSecondMobileNumber")  
#     #         VendorLandlineNumber= request.POST.get("VendorLandlineNumber")  
#     #         vendorCity= request.POST.get("vendorCity")  
#     #         VendorState= request.POST.get("VendorState")  
#     #         VendorPinCode= request.POST.get("VendorPinCode")  
#     #         VendorAdress= request.POST.get("VendorAdress")
            

#     #         if Documentfile:
#     #             # print("The code reach at Document file")
#     #             # file = request.FILES['file']
#     #             print("The code reach at Document file")
#     #             ext = Path(Documentfile.name).suffix.lower()
#     #             print(ext)

#     #             new_file = upload_file_to_blob(Documentfile,id)

#     #             if not new_file:
#     #                 messages.warning(request, f"{ext} not allowed only accept {', '.join(ext.lower()for ext in ALLOWED_EXTENTIONS)} ")
#     #                 return render(request, "letter/upload_file.html", {}) 
#     #             new_file.FileName = Documentfile.name
#     #             new_file.file_extention = ext
#     #             new_file.save()
#     #             messages.success(request, f"{Documentfile.name} was successfully uploaded")
#     #             # return redirect('emplistloi')

#     #         # if Documentfile:
#     #         #     print("The code reached at Document file")
                
#     #         #     ext = Path(Documentfile.name).suffix 
#     #         #     print(f"Extension: {ext}")

#     #         #     if ext not in ALLOWED_EXTENTIONS:
#     #         #         messages.warning(request, f"{ext} not allowed. Only accept {', '.join(ext for ext in ALLOWED_EXTENTIONS)}")
#     #         #         return render(request, "letter/upload_file.html", {})

#     #         #     # Upload the file (your custom function)
#     #         #     new_file = upload_file_to_blob(Documentfile, id)

#     #         #     if not new_file:
#     #         #         messages.error(request, "File upload failed. Please try again.")
#     #         #         return render(request, "letter/upload_file.html", {})

#     #         #     # Assuming `new_file` is a model instance
#     #         #     new_file.FileName = Documentfile.name
#     #         #     new_file.file_extention = ext
#     #         #     new_file.save()

#     #         #     messages.success(request, f"{Documentfile.name} was successfully uploaded.")
#     #         #     # return redirect('emplistloi')

#     #         # Documentfile = AMC_Entry_Master.objects.get(id=id)


#     #         # Check for missing required fields
#     #         if not (AMC_Start_Date and AMC_End_Date and AMCType):
#     #             messages.error(request, "All fields are required!")
#     #         else:
#     #             # Try to fetch existing record
#     #             amc_entry, created = AMC_Entry_Master.objects.update_or_create(
#     #                 EquipmentID=EquipmentID,
#     #                 OrganizationID=OrganizationID,
#     #                 defaults={
#     #                     "AMC_Start_Date": AMC_Start_Date,
#     #                     "AMC_End_Date": AMC_End_Date,
#     #                     "AMCType": AMCType,
#     #                     "AMC_Amount": AMC_Amount,
#     #                     "created_by": UserID,

#     #                     "VendorName": VendorName,
#     #                     "VendorEmailAddress": VendorEmailAddress,
#     #                     "VendorMobileNumber": VendorMobileNumber,
#     #                     "VendorSecondMobileNumber": VendorSecondMobileNumber,
#     #                     "VendorLandlineNumber": VendorLandlineNumber,
#     #                     "VendorAddress": VendorAdress,
#     #                     "VendorCity": vendorCity,
#     #                     "VendorState": VendorState,
#     #                     "VendorPincode": VendorPinCode,
#     #                 }
#     #             )
#     #             # startDate = amc_entry.AMC_Start_Date

#     #             if created:
#     #                 messages.success(request, "Data Submitted Successfully!")
#     #             else:
#     #                 messages.success(request, "Data Updated Successfully!")

#     #             return redirect(request.path)

#     if request.method == "POST":
#         if 'Submit_AMC_Value' in request.POST:
#             EquipmentID = id
#             AMC_Start_Date = request.POST.get("AMC_Start_Date")
#             AMC_End_Date = request.POST.get("AMC_End_Date")
#             AMCType = request.POST.get("AMCMode")
#             AMC_Amount = request.POST.get("AMCAmount", 0)
#             Documentfile = request.FILES.get('UploadDocument')

#             VendorName = request.POST.get("VendorName")
#             VendorEmailAddress = request.POST.get("VendorEmailAddress")
#             VendorMobileNumber = request.POST.get("VendorMobileNumber")  
#             VendorSecondMobileNumber = request.POST.get("VendorSecondMobileNumber")  
#             VendorLandlineNumber = request.POST.get("VendorLandlineNumber")  
#             vendorCity = request.POST.get("vendorCity")  
#             VendorState = request.POST.get("VendorState")  
#             VendorPinCode = request.POST.get("VendorPinCode")  
#             VendorAdress = request.POST.get("VendorAdress")

#             # Validate required fields
#             if not (AMC_Start_Date and AMC_End_Date and AMCType):
#                 messages.error(request, "All fields are required!")
#             else:
#                 # Upload document if exists
#                 if Documentfile:
#                     ext = Path(Documentfile.name).suffix.lower()
#                     print(f"Extension: {ext}")

#                     if ext not in ALLOWED_EXTENTIONS:
#                         messages.warning(request, f"{ext} not allowed. Only accept: {', '.join(ALLOWED_EXTENTIONS)}")
#                         return render(request, "AMC_Renewal/AMC_Dashboard.html", {
#                             "equipment_id": id,
#                             "selected_date": selected_date,
#                             "OrganizationID": OrganizationID,
#                             "UserID": UserID,
#                             "amc_entry": amc_entry,
#                         })

#                     # Upload
#                     new_file = upload_file_to_blob(Documentfile, id)

#                     if new_file:
#                         new_file.FileName = Documentfile.name
#                         new_file.file_extention = ext
#                         new_file.save()
#                         messages.success(request, f"{Documentfile.name} uploaded successfully.")
#                     else:
#                         messages.error(request, "File upload failed.")
#                         return render(request, "AMC_Renewal/AMC_Dashboard.html", context)

#                 # Save AMC data
#                 amc_entry, created = AMC_Entry_Master.objects.update_or_create(
#                     EquipmentID=EquipmentID,
#                     OrganizationID=OrganizationID,
#                     defaults={
#                         "AMC_Start_Date": AMC_Start_Date,
#                         "AMC_End_Date": AMC_End_Date,
#                         "AMCType": AMCType,
#                         "AMC_Amount": AMC_Amount,
#                         "created_by": UserID,
#                         "VendorName": VendorName,
#                         "VendorEmailAddress": VendorEmailAddress,
#                         "VendorMobileNumber": VendorMobileNumber,
#                         "VendorSecondMobileNumber": VendorSecondMobileNumber,
#                         "VendorLandlineNumber": VendorLandlineNumber,
#                         "VendorAddress": VendorAdress,
#                         "VendorCity": vendorCity,
#                         "VendorState": VendorState,
#                         "VendorPincode": VendorPinCode,
#                     }
#                 )

#                 messages.success(request, "Data Submitted Successfully!" if created else "Data Updated Successfully!")
#                 return redirect(request.path)

#     context = {
#         "equipment_id": id,
#         "selected_date": selected_date,
#         "OrganizationID": OrganizationID,
#         "UserID": UserID,
#         "amc_entry": amc_entry,
#         # "startDate":startDate

#         # 'Documentfile':Documentfile,
#     }
#     return render(request, "AMC_Renewal/AMC_Dashboard.html", context)


