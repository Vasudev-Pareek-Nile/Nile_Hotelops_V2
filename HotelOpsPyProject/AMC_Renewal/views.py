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
    print("Dashboard 1.0")
    OrganizationID = request.session.get("OrganizationID", 0)
    UserID = str(request.session.get("UserID", 0))

    selected_date = request.GET.get('start_date')
    Mode = request.GET.get('Mode')

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
    else:
        print("Id is missing")
        # print("Dashboard 3.0")
        

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
                # print("All fields are required! ---- error comes")
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
        "Mode": Mode if Mode else 'Submit',
        # "startDate":startDate
    }
    return render(request, "AMC_Renewal/AMC_Dashboard.html", context)





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
    




from django.db.models import Count, Q, OuterRef, Subquery, Value, F
from django.http import JsonResponse
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status

# def pending_status_counts(request):
#     data = (
#         AMC_Entry_Master.objects
#         .filter(is_delete=False)  # Exclude deleted records
#         .values('OrganizationID')
#         .annotate(
#             CEO_Pending_Count=Count('id', filter=Q(CEO_Status='Pending')),
#             FC_Pending_Count=Count('id', filter=Q(FC_Status='Pending')),
#             GM_Pending_Count=Count('id', filter=Q(GM_Status='Pending')),
#         )
#         .order_by('OrganizationID')
#     )

#     return JsonResponse(list(data), safe=False)





#  ----------------------- 100% Working ------------
def pending_status_counts_Demo_Three(request):
    OrganizationID_Session = request.GET.get('OID_Session')
    OrganizationID = request.GET.get('OID')
    UserType = request.GET.get('UserType', '').lower()

    if not OrganizationID:
        return Response({"error": "OrganizationID is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not UserType:
        return Response({"error": "UserType is required"}, status=status.HTTP_400_BAD_REQUEST)

    if OrganizationID != 'all' and not OrganizationMaster.objects.filter(OrganizationID=OrganizationID).exists():
        return Response({"error": f"Invalid OrganizationID: {OrganizationID}"}, status=status.HTTP_404_NOT_FOUND)

    AMC_filter = {'is_delete': False, 'Final_Status': 'Pending'}
    if UserType == 'ceo':
        OrganizationID = 'all'


    if OrganizationID != 'all':
        AMC_filter['OrganizationID'] = OrganizationID

    # Subquery to get hotel name from OrganizationMaster
    org_name_subquery = OrganizationMaster.objects.filter(
        OrganizationID=OuterRef('OrganizationID'),
        IsDelete=False,
        Activation_status=1
    ).values('ShortDisplayLabel')[:1]

    AMC_obj = (
        AMC_Entry_Master.objects
        .filter(**AMC_filter)
        .values('OrganizationID')
        .annotate(
            Hotel=Subquery(org_name_subquery),
            # CEO Pending = CEO is Pending AND FC & GM are Approved
            CEO_Pending_Count=Count('id', filter=Q(
                CEO_Status='Pending',
                FC_Status='Approved',
                GM_Status='Approved'
            )),

            # GM Pending = GM is Pending AND FC is Approved
            GM_Pending_Count=Count('id', filter=Q(
                GM_Status='Pending',
                FC_Status='Approved'
            )),

            # FC Pending = FC is Pending
            FC_Pending_Count=Count('id', filter=Q(
                FC_Status='Pending'
            )),
        )
        .order_by('OrganizationID')
    )

    return JsonResponse(list(AMC_obj), safe=False)




def pending_status_counts_Demo_Four(request):
    OrganizationID = request.GET.get('OID')
    UserType = request.GET.get('UserType', '').lower()

    if not OrganizationID:
        return Response({"error": "OrganizationID is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not UserType:
        return Response({"error": "UserType is required"}, status=status.HTTP_400_BAD_REQUEST)

    # CEO with OID=3 sees all organizations
    if UserType == 'ceo' and str(OrganizationID) == '3':
        org_filter = {'IsDelete': False, 'Activation_status': 1, 'IsNileHotel':1}
    elif OrganizationID == 'all':
        org_filter = {'IsDelete': False, 'Activation_status': 1, 'IsNileHotel':1}
    else:
        if not OrganizationMaster.objects.filter(OrganizationID=OrganizationID).exists():
            return Response({"error": f"Invalid OrganizationID: {OrganizationID}"}, status=status.HTTP_404_NOT_FOUND)
        org_filter = {'IsDelete': False, 'Activation_status': 1, 'OrganizationID': OrganizationID}

    # Get base list of all organizations
    all_orgs = OrganizationMaster.objects.filter(**org_filter).values('OrganizationID', 'ShortDisplayLabel')

    # Pre-calculate counts from AMC_Entry_Master
    amc_counts = AMC_Entry_Master.objects.filter(
        is_delete=False, Final_Status='Pending'
    ).values('OrganizationID').annotate(
        CEO_Pending_Count=Count('id', filter=Q(
            CEO_Status='Pending',
            FC_Status='Approved',
            GM_Status='Approved'
        )),
        GM_Pending_Count=Count('id', filter=Q(
            GM_Status='Pending',
            FC_Status='Approved'
        )),
        FC_Pending_Count=Count('id', filter=Q(
            FC_Status='Pending'
        ))
    )

    # Convert AMC counts to a dictionary for quick lookup
    amc_dict = {item['OrganizationID']: item for item in amc_counts}

    # Merge counts into all_orgs list
    result = []
    for org in all_orgs:
        org_id = org['OrganizationID']
        if org_id in amc_dict:
            result.append({
                'OrganizationID': org_id,
                'ShortDisplayLabel': org['ShortDisplayLabel'],
                'CEO_Pending_Count': amc_dict[org_id]['CEO_Pending_Count'],
                'GM_Pending_Count': amc_dict[org_id]['GM_Pending_Count'],
                'FC_Pending_Count': amc_dict[org_id]['FC_Pending_Count'],
            })
        else:
            result.append({
                'OrganizationID': org_id,
                'ShortDisplayLabel': org['ShortDisplayLabel'],
                'CEO_Pending_Count': 0,
                'GM_Pending_Count': 0,
                'FC_Pending_Count': 0,
            })

    return JsonResponse(result, safe=False)







# --------------- AMC pdf download mobile api --------------->



# def download_AMC_View_Data_pdf_mobile_api(request):

#     equipment_id = request.GET.get('equipment_id')
#     OrganizationID = request.GET.get('OrganizationID')

#     if not equipment_id:
#         return HttpResponse("Equipment ID not provided", status=400)

#     # Base filter query

#     base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
#     organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
#     organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

#     organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
#     organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
#     organization_logo = organizations.OrganizationName


#     # equipment = get_object_or_404(AMC_Entry_Master, id=equipment_id)
#     equipment_data = get_equipment_details_AMC_List(id=equipment_id)
#     print("equipment_data in mobile api", equipment_data)

#     current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
#     # Prepare context for the PDF template
#     context = {
#         "equipment_data":equipment_data,
#         'organization_logo': organization_logo,
#         'organization_logos':organization_logos,
#         'current_datetime':current_datetime,
#     }

#     template_path = 'AMC_Renewal/AMC_View_Data_PDF.html'
#     template = get_template(template_path)
#     html = template.render(context).encode("UTF-8")

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{organization_logo}_Equipment_Report.pdf"'

#     pisa_status = pisa.CreatePDF(html, dest=response, encoding="UTF-8")

#     if pisa_status.err:
#         return HttpResponse("Error generating PDF", status=500)

#     return response


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
# from Organization.models import OrganizationMaster
# from AMC.utils import get_equipment_details_AMC_List  # Adjust import to your helper's location

def download_AMC_View_Data_pdf_mobile_api(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'

    # UserType_Session = request.headers.get('UserType', '').lower()
    AccessToken = request.headers.get('Authorization', '')


    if not AccessToken:
        return HttpResponse('Token Not Found, Please Provide Correct Token.',content_type='text/plain')

    if AccessToken != Fixed_Token:
        return HttpResponse('Please Provide The Correct Token, Token Not Match.',content_type='text/plain')
    # Validate UserType

    # Read required params from query
    equipment_id = request.GET.get("equipment_id")
    organization_id = request.GET.get("organization_id")
    record_id = request.GET.get("id")  # optional: internal primary key

    if not equipment_id or not organization_id:
        return HttpResponse("equipment_id and organization_id are required", status=400)

    try:
        equipment_id = int(equipment_id)
        organization_id = int(organization_id)
        if record_id:
            record_id = int(record_id)
    except ValueError:
        return HttpResponse("Invalid ID values", status=400)

    # Logos
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"

    # Static org (ID=3)
    org_static = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{org_static.OrganizationLogo}" if org_static and org_static.OrganizationLogo else None

    # Actual org from param
    org_actual = OrganizationMaster.objects.filter(OrganizationID=organization_id).first()
    if not org_actual:
        return HttpResponse("Organization not found", status=404)

    organization_logo_url = f"{base_url}{org_actual.OrganizationLogo}" if org_actual.OrganizationLogo else None
    organization_name = org_actual.OrganizationName

    # Call your helper function with all three args
    equipment_data = get_equipment_details_AMC_List(
        id=record_id,
        equipment_id=equipment_id,
        organization_id=organization_id
    )

    if not equipment_data:
        return HttpResponse("No equipment data found", status=404)

    # Prepare PDF context
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    context = {
        "equipment_data": equipment_data,
        'organization_logo': organization_name,
        'organization_logos': organization_logos,
        'current_datetime': current_datetime,
    }

    # Render HTML template to PDF
    template_path = 'AMC_Renewal/AMC_View_Data_PDF.html'
    template = get_template(template_path)
    html = template.render(context).encode("UTF-8")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{organization_name}_Equipment_Report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response, encoding="UTF-8")

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response






from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .models import AMC_Entry_Master
from .serializers import AMCEntryMasterSerializer


@api_view(['GET'])
def AMC_Entry_List_API_Edit(request):
    EquipmentID = request.GET.get("EpID")
    OrganizationID = request.GET.get("OID")


    filters = {
        "EquipmentID": EquipmentID,
        # "OrganizationID": OrganizationID,
        "is_delete": False
    }

    # if OrganizationID != '3':
    #     filters["OrganizationID"] = OrganizationID

    # if today_only == "true":
    #     today = timezone.now().date()
    #     filters["AMC_End_Date__gte"] = today

    queryset = AMC_Entry_Master.objects.filter(**filters).order_by("-created_date_time")

    serializer = AMCEntryMasterSerializer(queryset, many=True)

    return Response({
        "status": True,
        "count": queryset.count(),
        "data": serializer.data
    }, status=status.HTTP_200_OK)







from django.shortcuts import redirect
from django.contrib import messages

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# @api_view(['DELETE'])
@api_view(['POST'])
def delete_amc_entry_api(request):
    print("the delete entry is called")
    equipment_id = request.data.get('EquipmentID')
    OrganizationID = request.data.get('OrganizationID')
    UserID = request.data.get('UserID')
    
    print("-----------------------------------------")
    print("equipment_id::",equipment_id)
    print("OrganizationID::",OrganizationID)
    print("UserID::",UserID)
    print("-----------------------------------------")

    if not equipment_id or not OrganizationID:
        return Response(
            {"error": "EquipmentID and OrganizationID are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    amc_entry = AMC_Entry_Master.objects.filter(
        EquipmentID=equipment_id,
        OrganizationID=OrganizationID
    ).first()

    if not amc_entry:
        return Response(
            {"error": "AMC record not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # amc_entry.delete()
    amc_entry.is_delete = 1
    amc_entry.save()
    amc_entry.modify_by = UserID
    amc_entry.modify_date_time = timezone.now()

    return Response(
        {"message": "AMC record deleted successfully"},
        status=status.HTTP_200_OK
    )
