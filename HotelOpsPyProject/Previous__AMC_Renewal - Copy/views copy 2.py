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

    entry = AMC_Entry_Master.objects.filter(EquipmentID=id, is_delete=False).first()  
    

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

    # print("The Post method's value is here::", request.POST)

    if request.method == "POST":
            status = request.POST.get("status")  
            remarks = request.POST.get("remarks")  
            # print("Page status:", status)
            # print("Page remark:", remarks)

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


    # amc_entry = AMC_Entry_Master.objects.filter(
    #     EquipmentID=id, OrganizationID=OrganizationID
    # ).first()
    Context = {
        "amc_entry":entry,
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







# Api for mobile ----

# Call Store Procedure for AMC_Data_List -- This is only API.
# def AMC_List_Equipment_Mobile_Api(request):
#     user_OrganizationID = request.GET.get('OrganizationID')  
#     usertype = request.GET.get('UserType', '').strip().lower()    
#     statusfilter = request.GET.get('UserType', '').strip().capitalize()

#     if usertype == 'ceo' and user_OrganizationID == 3:
#         OrganizationID = 0
#     else:
#         OrganizationID = user_OrganizationID

#     # print("OrganizationID:", OrganizationID)
#     # print("UserType (raw):", usertype_type)
#     # print("UserType (processed):", usertype)

#     if user_OrganizationID is None:
#         return HttpResponse("OrganizationID not found in request", status=400)

#     if usertype is None:
#         return HttpResponse("usertype not found in request", status=400)
    
#     equipment_data = get_equipment_details_Mobile_Api(organization_id=OrganizationID, usertype=usertype)  # Example: Fetch details for OrganizationID=1
#     return JsonResponse({'data': equipment_data})


def AMC_List_Equipment_Mobile_Api(request):
    user_OrganizationID = request.GET.get('OrganizationID')  
    usertype_type = request.GET.get('UserType', '').strip().lower()      
    selected_status = request.GET.get('status', '').strip().capitalize()  # e.g., 'Approved', 'Pending', etc.
    user_department = request.GET.get('UserDepartment', '').strip().lower()

    if not user_OrganizationID or not usertype_type:
        return JsonResponse({'error': 'Missing OrganizationID or UserType'}, status=400)

    # Handle CEO for org 3
    # OrganizationID = 0 if usertype_type == 'ceo' and user_OrganizationID == '3' else user_OrganizationID


    # print("OrgID:", user_OrganizationID)
    # print("UserType:", usertype_type)
    # print("Status:", selected_status)
    # print("UserDepartment:", user_department)


    # Set status filters based on user type and selected status
    fc_status = ''
    gm_status = ''
    ceo_status = ''

    if usertype_type == "hod" and user_department == "finance":
        fc_status = selected_status or 'Pending'
    elif usertype_type == 'gm':
        fc_status = 'Approved'
        gm_status = selected_status or 'Pending'
    elif usertype_type == 'ceo':
        fc_status = 'Approved'
        gm_status = 'Approved'
        ceo_status = selected_status or 'Pending'

    print("Filter params passed:", fc_status, gm_status, ceo_status)

    # Fetch filtered data
    equipment_data = get_equipment_details_Mobile_Api(
        organization_id=user_OrganizationID,
        usertype=usertype_type,
        fc_status=fc_status,
        gm_status=gm_status,
        ceo_status=ceo_status
    )

    return JsonResponse({'data': equipment_data})


# Count API
def AMC_Pending_Count_Api(request):
    OrganizationID = request.GET.get('OrganizationID')
    usertype_type = request.GET.get('UserType', '').strip().lower()

    if usertype_type:
        usertype = usertype_type.lower()
    else:
        usertype = ''

    if not OrganizationID:
        return JsonResponse({'error': 'OrganizationID is required'}, status=400)

    # Call same procedure
    equipment_data = get_equipment_details_Mobile_Api(organization_id=OrganizationID, usertype=usertype)

    pending_count = len(equipment_data)  # Get count only

    return JsonResponse({'pending_count': pending_count})


# Details Api
def AMC_Details_equipment_Mobile_Api(request):
    Id = request.GET.get('Id')  
    OrganizationID = request.GET.get('OrganizationID')  
    EquipmentID = request.GET.get('EquipmentID')  

    if not Id:
        return JsonResponse({'error': 'Missing Id In Request'}, status=400)

    if not OrganizationID:
        return JsonResponse({'error': 'Missing OrganizationID  In Request'}, status=400)

    if not EquipmentID:
        return JsonResponse({'error': 'Missing EquipmentID  In Request'}, status=400)
    
    equipment_data = get_equipment_details_AMC_List(id=Id, equipment_id=EquipmentID, organization_id=OrganizationID)  # Example: Fetch details for OrganizationID=1
    return JsonResponse({'data': equipment_data})


# Call Store Procedure for AMC_Data_List.
def get_equipment_details_Mobile_Api(id=0, equipment_id=0, organization_id=0, fc_status='', gm_status='', ceo_status='', usertype=''):
    # print("Executing SP with params:", id, equipment_id, organization_id, fc_status, gm_status, ceo_status, usertype)
    with connection.cursor() as cursor:
        sql = """
            EXEC SP_EquipmentMGMT_EntryMaster_Mobile_Api_Details 
            @ID=%s, @EquipmentID=%s, @OrganizationID=%s, 
            @FCStatus=%s, @GMStatus=%s, @CEOStatus=%s, @UserType=%s
        """
        cursor.execute(sql, [id, equipment_id, organization_id, fc_status, gm_status, ceo_status, usertype])
        result = cursor.fetchall()

        # Fetch column names
        columns = [col[0] for col in cursor.description]

        # print("DEBUG: Data received from SQL procedure ->", result)

    # Convert the result to a list of dictionaries
    data = [dict(zip(columns, row)) for row in result]
    
    return data


# AMC Approve
def AMC_Action_Mobile_Api(request):
    Id = request.GET.get('Id')  
    EquipmentID = request.GET.get('EquipmentID')  
    OrganizationID = request.GET.get('OrganizationID')  
    status = request.GET.get('status', '').strip().capitalize()
    usertype = request.GET.get('UserType', '').strip().lower()         
    user_department = request.GET.get('UserDepartment', '').strip().lower()
    UserID = request.GET.get('UserID')          


    # Validate required fields
    if not all([Id, EquipmentID, OrganizationID, status, usertype, UserID]):
        return JsonResponse({'error': 'Missing required parameters'}, status=400)
    
    try:
        Id = int(Id)
        EquipmentID = int(EquipmentID)
        OrganizationID = int(OrganizationID)
        UserID = int(UserID)

        entry = AMC_Entry_Master.objects.filter(
            id=Id,
            EquipmentID=EquipmentID, 
            OrganizationID=OrganizationID, 
            is_delete=False
        ).first()

        if not entry:
            return JsonResponse({'error': f"No entry found for EquipmentID: {EquipmentID}"}, status=404)

        formatted_datetime = timezone.now()
        # usertype = usertype_type.lower()
        # user_department = UserDepartment.lower()
        # print("The user_department is", user_department)

        # Set status based on user role
        if usertype == "gm":
            entry.GM_Status = status
            entry.GM_ActionBy = UserID
            entry.GM_ActionDateTime = formatted_datetime
            message = "GM Status updated successfully!"

        elif usertype == "hod" and user_department == "finance":
            entry.FC_Status = status
            entry.FC_ActionBy = UserID
            entry.FC_ActionDateTime = formatted_datetime
            message = "FC Status updated successfully!"

        elif usertype == "ceo":
            entry.CEO_Status = status
            entry.CEO_ActionBy = UserID
            entry.CEO_ActionDateTime = formatted_datetime
            entry.Final_Status = status
            entry.Final_Status = status
            message = "CEO Status updated successfully!"

        else:
            return JsonResponse({'error': 'Invalid user type or department'}, status=400)
        
        entry.save()

        return JsonResponse({'message': message, 'status': status})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


from hotelopsmgmtpy.GlobalConfig import MasterAttribute
# from hotelopsmgmtpy.GlobalConfig import MasterAttribute

# # # AMC Atteched Document Opening:
# def AMC_Document_Mobile_Api(request):
#     Id = request.GET.get('Id')  
#     EquipmentID = request.GET.get('EquipmentID')
#     OrganizationID = request.GET.get('OrganizationID')

#     if not EquipmentID or not Id:
#         return JsonResponse({'error': 'Missing EquipmentID or Id'}, status=400)
    
#     if not OrganizationID:
#         return JsonResponse({'error': 'Missing OrganizationID'}, status=400)

#     try:
#         # Fetch the entry
#         entry = AMC_Entry_Master.objects.filter(
#             id = Id,
#             EquipmentID=EquipmentID,
#             OrganizationID=OrganizationID,
#             is_delete=False
#         ).first()

#         if not entry or not entry.FileName:
#             return JsonResponse({'error': 'Document not found'}, status=404)
        
#         print('entryfilename', entry.FileName)

#         # Construct Azure Blob URL
#         # container_name = "rmcuplodeddocuments"
#         # file_url = f"https://{MasterAttribute.azure_storage_account_name}.blob.core.windows.net/{entry.FileName}"
#         # file_url = f"https://{MasterAttribute.azure_storage_account_name}.blob.core.windows.net/{container_name}/{entry.FileName}"
#         # print('The container name is::', container_name)

#         container_name = "rmcuplodeddocuments"
#         blob_path = entry.FileName.split(f"{container_name}/", 1)[-1]  # remove container prefix if exists
#         file_url = f"https://{MasterAttribute.azure_storage_account_name}.blob.core.windows.net/{container_name}/{blob_path}"

#         print('entryfilename in Api', file_url)


#         return JsonResponse({
#             'file_url': file_url,
#             'original_file_name': entry.FileName,
#             'container_name':container_name,
#             'entryfilename':entry.FileName
#         })

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

from .azure import generate_sas_url  
from azure.storage.blob import BlobSasPermissions
from hotelopsmgmtpy.GlobalConfig import MasterAttribute

def AMC_Document_Mobile_Api(request):
    Id = request.GET.get('Id')  
    EquipmentID = request.GET.get('EquipmentID')
    OrganizationID = request.GET.get('OrganizationID')

    if not EquipmentID or not Id:
        return JsonResponse({'error': 'Missing EquipmentID or Id'}, status=400)
    
    if not OrganizationID:
        return JsonResponse({'error': 'Missing OrganizationID'}, status=400)

    try:
        # Fetch the entry
        entry = AMC_Entry_Master.objects.filter(
            id=Id,
            EquipmentID=EquipmentID,
            OrganizationID=OrganizationID,
            is_delete=False
        ).first()

        if not entry or not entry.FileName:
            return JsonResponse({'error': 'Document not found'}, status=404)

        # Ensure FileName doesn't include container prefix
        container_name = "rmcuplodeddocuments"
        # blob_name = entry.FileName
        # if blob_name.startswith(container_name + '/'):
        #     blob_name = blob_name[len(container_name) + 1:]

        blob_name = entry.FileName  # This should be "rmcuplodeddocuments/..."
        # file_url = generate_sas_url(blob_name)

        # ✅ Generate the SAS URL using your helper
        file_url = generate_sas_url(blob_name)

        return JsonResponse({
            'file_url': file_url,
            'original_file_name': entry.FileName,
            # 'container_name': container_name,
            # 'blob_name':blob_name
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)