from django.shortcuts import render,redirect
from .models import  IT_Inventory,Master_Category,Master_Company,Master_Area,Master_Software_type
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse
from urllib.parse import urlencode
from .utils import get_organization_it_emails

# Create your views here.
def Inventory_Add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
    software_inventory = request.GET.get('SoftwareInventory') == 'True'
    Hardware_Inventory = request.GET.get('HardwareInventory') == 'True'
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    Session_FullName =str(request.session["FullName"])
    Organization_Name =str(request.session["OrganizationName"])

    session_data = dict(request.session)
    # print("The all session value is here::", session_data)

    orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1)

    Categorys = Master_Category.objects.filter(IsDelete=False)
    companys = Master_Company.objects.filter(IsDelete=False)
    Areas = Master_Area.objects.filter(IsDelete=False)
    software_types = Master_Software_type.objects.filter(IsDelete=False)


    inventorys_id = request.GET.get('ID')
    action = ''
    inventorys = None
    if inventorys_id is not None:
        inventorys = get_object_or_404(IT_Inventory,id=inventorys_id,OrganizationID=OrganizationID)


    if request.method == "POST":
        # Inventory_Type_value = request.POST.get('SetInventoryType', '')
        # print("Inventory_Type_value",Inventory_Type_value)
        if inventorys_id is not None:
            inventorys.type = request.POST.get('type', '')
            inventorys.Inventory_Type = request.POST.get('SetInventoryType', '') # SetInventoryType -- Hardware or Software
            inventorys.Description = request.POST.get('Description', '')
            inventorys.SerialNo= request.POST.get('SerialNo', '')
            inventorys.Make= request.POST.get('Make', '')
            inventorys.Model_No=request.POST.get('Model_No', '')
            inventorys.Commissioning_Date=request.POST.get('Commissioning_Date', '')
            inventorys.Area=request.POST.get('Area', '')
            inventorys.computer_name=request.POST.get('computer_name', '')
            inventorys.ip=request.POST.get('ip', '')
            inventorys.Warrantiy_Status=request.POST.get('Warrantiy_Status', '')
            inventorys.Warrantiy_start=request.POST.get('Warrantiy_start', '')
            inventorys.Warrantiy_end=request.POST.get('Warrantiy_end', '')
            inventorys.amctype = request.POST.get('amctype', '')
            inventorys.amcstart=request.POST.get('amcstart', '')
            inventorys.amcend=request.POST.get('amcend', '')
            inventorys.hardware_AMC_Yearly_Expense=request.POST.get('hardware_AMC_Yearly_Expense', '')
            inventorys.AMC_Status=request.POST.get('AMC_Status', '')
            inventorys.Remarks=request.POST.get('Remarks', '')
            inventorys.hardware_quantity=request.POST.get('hardware_quantity', '')
            inventorys.hardware_unit_price=request.POST.get('hardware_unit_price', '')

            inventorys.softwaretype=request.POST.get('softwaretype', '')
            inventorys.softwarename=request.POST.get('softwarename', '')
            inventorys.Quantity=request.POST.get('Quantity', '')
            inventorys.software_AMC_Start=request.POST.get('software_AMC_Start', '')
            inventorys.software_AMC_end=request.POST.get('software_AMC_end', '')
            inventorys.software_AMC_Type=request.POST.get('software_AMC_Type', '')
            inventorys.Software_Quantity=request.POST.get('software_quantity', '')
            inventorys.Software_unit_price=request.POST.get('software_unit_price', '')
            inventorys.software_AMC_Status=request.POST.get('software_AMC_Status', '')
            inventorys.software_AMC_Yearly_Expense=request.POST.get('software_AMC_Yearly_Expense', '')
            inventorys.ModifyBy=UserID
            inventorys.save()
            action = 'Updated'
            messages.success(request, "IT Inventory Updates  Successfully !!!!")
            recipients = get_organization_it_emails([OrganizationID])
            send_inventory_email(inventorys, created_by=Session_FullName, recipients=recipients, useraction=action, OrgName=Organization_Name)
            # send_inventory_email(inventorys, created_by=Session_FullName, recipients=["Vasudev.Pareek@nilehospitality.com"], useraction=action, OrgName=Organization_Name)
            if software_inventory:
                params = urlencode({'success': 'True', 'message': 'Software Details saved successfully.'})
            elif Hardware_Inventory:
                params = urlencode({'success': 'True', 'message': 'Hardware Details saved successfully.'})
            else:
                params = urlencode({'success': 'True', 'message': 'Details saved successfully.'})
            return redirect(f"{reverse('Inventory_list')}?{params}")
            # return redirect('Inventory_list')
            
        else:
            Inventory_Type = request.POST.get('SetInventoryType', '')

            type = request.POST.get('type', '')
            Description = request.POST.get('Description', '')
            SerialNo= request.POST.get('SerialNo', '')
            Make= request.POST.get('Make', '')
            Model_No=request.POST.get('Model_No', '')
            Commissioning_Date=request.POST.get('Commissioning_Date', '')
            Area=request.POST.get('Area', '')
            computer_name=request.POST.get('computer_name', '')
            ip=request.POST.get('ip', '')
            Warrantiy_Status=request.POST.get('Warrantiy_Status', '')
            Warrantiy_start=request.POST.get('Warrantiy_start', '')
            Warrantiy_end=request.POST.get('Warrantiy_end', '')
            amctype = request.POST.get('amctype', '')
            amcstart=request.POST.get('amcstart', '')
            amcend=request.POST.get('amcend', '')
            hardware_AMC_Yearly_Expense=request.POST.get('hardware_AMC_Yearly_Expense', '')
            AMC_Status=request.POST.get('AMC_Status', '')
            Remarks=request.POST.get('Remarks', '')
            hardware_quantity=request.POST.get('hardware_quantity', '')
            hardware_unit_price=request.POST.get('hardware_unit_price', '')

            softwaretype=request.POST.get('softwaretype', '')
            softwarename=request.POST.get('softwarename', '')
            Quantity=request.POST.get('Quantity', '')
            software_AMC_Start=request.POST.get('software_AMC_Start', '')
            software_AMC_end=request.POST.get('software_AMC_end', '')
            software_AMC_Type=request.POST.get('software_AMC_Type', '')
            Software_Quantity=request.POST.get('software_quantity', '')
            Software_unit_price=request.POST.get('software_unit_price', '')
            software_AMC_Status=request.POST.get('software_AMC_Status', '')
            software_AMC_Yearly_Expense=request.POST.get('software_AMC_Yearly_Expense', '')

            # print("Software_Quantity",Software_Quantity )
            # print("Software_unit_price", Software_unit_price)


            inventory=IT_Inventory.objects.create(type=type, Description=Description, SerialNo=SerialNo, Make=Make, Model_No=Model_No, Commissioning_Date=Commissioning_Date, Area=Area, 
                                                  computer_name=computer_name, ip=ip, Warrantiy_Status=Warrantiy_Status, Warrantiy_start=Warrantiy_start, Warrantiy_end=Warrantiy_end, amctype=amctype, amcstart=amcstart, 
                                                  amcend=amcend,hardware_AMC_Yearly_Expense=hardware_AMC_Yearly_Expense, AMC_Status=AMC_Status, Remarks=Remarks, hardware_quantity=hardware_quantity, hardware_unit_price=hardware_unit_price, softwaretype=softwaretype ,
                                                  softwarename=softwarename, Quantity=Quantity, software_AMC_Start=software_AMC_Start,  software_AMC_end=software_AMC_end ,
                                                  software_AMC_Type=software_AMC_Type, Software_Quantity=Software_Quantity, Software_unit_price=Software_unit_price, software_AMC_Status=software_AMC_Status, software_AMC_Yearly_Expense=software_AMC_Yearly_Expense, OrganizationID=OrganizationID,CreatedBy=UserID, Inventory_Type=Inventory_Type)
            messages.success(request, "IT Inventory Register Successfully !!!!")
            action = 'Added'
            recipients = get_organization_it_emails([OrganizationID])
            send_inventory_email(inventory, created_by=Session_FullName, recipients=recipients, useraction=action, OrgName=Organization_Name)
            # send_inventory_email(inventory, created_by=Session_FullName, recipients=["Vasudev.Pareek@nilehospitality.com"], useraction=action, OrgName=Organization_Name)

            if software_inventory:             
                params = urlencode({'success': 'True', 'message': 'Software Details saved successfully.'})
            elif Hardware_Inventory:
                params = urlencode({'success': 'True', 'message': 'Hardware Details saved successfully.'})
            else:
                params = urlencode({'success': 'True', 'message': 'Details saved successfully.'})
                
            return redirect(f"{reverse('Inventory_list')}?{params}")

    context={
        'orgs': orgs,
        'inventorys':inventorys,
        'Categorys':Categorys,
        'companys':companys,
        'Areas':Areas,
        'software_types':software_types,
        'software_inventory': software_inventory,
        'Hardware_Inventory': Hardware_Inventory,
        }
    return render(request,'Inventory/Inventory_Add.html',context)



def Inventory_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    UserID = str(request.session["UserID"])
    OrganizationID = str(request.session.get("OrganizationID"))
    SessionOrganizationID = int(OrganizationID)

    # Get selected organization from query param
    SelectedOrganizationID_str = request.GET.get('OrganizationID', OrganizationID)
    SelectedOrganizationID = int(SelectedOrganizationID_str) if SelectedOrganizationID_str != 'All' else None

    # Special case for admin user override
    if UserID == "20201212180048":
        OrganizationID = 401

    # Filter IT Inventory
    itInventory = IT_Inventory.objects.filter(IsDelete=False)

    if SelectedOrganizationID is not None:
        itInventory = itInventory.filter(OrganizationID=SelectedOrganizationID)

    # Filter organization options based on session org
    if SessionOrganizationID == 3:
        orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1)
    else:
        orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1, OrganizationID=SessionOrganizationID)

    # Additional filters
    inventory_type = request.GET.get("InventoryType", "")
    Item_Type = request.GET.get("ItemType", "")
    serial_no = request.GET.get("SerialNo", "")
    make = request.GET.get("Make", "")
    warranty_status = request.GET.get("Warrantiy_Status", "")
    amc_status = request.GET.get("AMC_Status", "")

    if inventory_type:
        itInventory = itInventory.filter(Inventory_Type=inventory_type)
    if Item_Type:
        itInventory = itInventory.filter(type=Item_Type)
    if serial_no:
        itInventory = itInventory.filter(SerialNo=serial_no)
    if make:
        itInventory = itInventory.filter(Make=make)
    if warranty_status:
        itInventory = itInventory.filter(Warrantiy_Status=warranty_status)
    if amc_status:
        itInventory = itInventory.filter(AMC_Status=amc_status)

    # inventory_data = [{'inventory': i, 'qr_code_base64': i.get_qr_code_base64()} for i in itInventory]
    
    inventory_data = []
    for inventory in itInventory:
        qr_code_base64 = inventory.get_qr_code_base64()
        inventory_data.append({'inventory': inventory, 'qr_code_base64': qr_code_base64})


    if SelectedOrganizationID is None:
        SerialNoList = IT_Inventory.objects.filter(IsDelete=False).values("SerialNo").distinct()
    else:
        SerialNoList = IT_Inventory.objects.filter(IsDelete=False, OrganizationID=SelectedOrganizationID).values("SerialNo").distinct()

    context = {
        'inventory_data': inventory_data,
        'SessionOrganizationID': SessionOrganizationID,  # Correct
        'orgs': orgs,
        'selectedOrganizationID': SelectedOrganizationID_str,  # String to match dropdown value
        'SerialNoList': SerialNoList,
        # 'SerialNoList': IT_Inventory.objects.filter(IsDelete=False, OrganizationID=SelectedOrganizationID).values("SerialNo"),
        'Categorys': Master_Category.objects.filter(IsDelete=False),
        'companys': Master_Company.objects.filter(IsDelete=False),
        'Areas': Master_Area.objects.filter(IsDelete=False),
        'software_types': Master_Software_type.objects.filter(IsDelete=False),
        'inventory_type':inventory_type,
        'Item_Type':Item_Type,
        'serial_no':serial_no,
        'make':make,
        'warranty_status':warranty_status,
        'amc_status':amc_status,
    }

    return render(request, 'Inventory/Inventory_list.html', context)



def Software_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    # itInventory = IT_Inventory.objects.filter(IsDelete=False, OrganizationID=OrganizationID, Inventory_Type="Software").order_by('-CreatedDateTime')
    UserID = str(request.session["UserID"])
    OrganizationID = str(request.session.get("OrganizationID"))
    SessionOrganizationID = int(OrganizationID)

    # Get selected organization from query param
    SelectedOrganizationID_str = request.GET.get('OrganizationID', OrganizationID)
    SelectedOrganizationID = int(SelectedOrganizationID_str) if SelectedOrganizationID_str != 'All' else None

    # print("SelectedOrganizationID:", SelectedOrganizationID)

    # Special case for admin user override
    if UserID == "20201212180048":
        OrganizationID = 401

    # Filter IT Inventory
    itInventory = IT_Inventory.objects.filter(IsDelete=False, Inventory_Type="Software").order_by('-CreatedDateTime')

    if SelectedOrganizationID is not None:
        itInventory = itInventory.filter(OrganizationID=SelectedOrganizationID)

    # Filter organization options based on session org
    if SessionOrganizationID == 3 or SelectedOrganizationID == 'All':
        orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1)
    else:
        orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1, OrganizationID=SessionOrganizationID)

    # Additional filters
    SoftwareType = request.GET.get("SoftwareType", "")
    SoftwareName = request.GET.get("SoftwareName", "")
    software_AMC_Type = request.GET.get("software_AMC_Type", "")
    AMC_Status = request.GET.get("AMC_Status", "")


    if SoftwareType:
        itInventory = itInventory.filter(softwaretype=SoftwareType)
    if SoftwareName:
        itInventory = itInventory.filter(softwarename=SoftwareName)
    if software_AMC_Type:
        itInventory = itInventory.filter(software_AMC_Type=software_AMC_Type)
    if AMC_Status:
        itInventory = itInventory.filter(software_AMC_Status=AMC_Status)

    
    inventory_data = []
    for inventory in itInventory:
        qr_code_base64 = inventory.get_qr_code_base64()
        inventory_data.append({'inventory': inventory, 'qr_code_base64': qr_code_base64})

    Categorys = Master_Category.objects.filter(IsDelete=False)
    companys = Master_Company.objects.filter(IsDelete=False)
    Areas = Master_Area.objects.filter(IsDelete=False)
    software_types = Master_Software_type.objects.filter(IsDelete=False)

    if SelectedOrganizationID is None:
        SoftwareNames = IT_Inventory.objects.filter(IsDelete=False, Inventory_Type="Software").values("softwarename").distinct()
    else:
        SoftwareNames = IT_Inventory.objects.filter(IsDelete=False, Inventory_Type="Software", OrganizationID=SelectedOrganizationID).values("softwarename").distinct()

    context = {
        'orgs': orgs,
        'Categorys':Categorys,
        # 'SoftwareNames': IT_Inventory.objects.filter(IsDelete=False, OrganizationID=SelectedOrganizationID).values("softwarename"),
        'SoftwareNames': SoftwareNames,
        'companys':companys,
        'selectedOrganizationID': SelectedOrganizationID_str,
        'SessionOrganizationID': SessionOrganizationID,
        'Areas':Areas,
        'software_types':software_types,
        'inventory_data': inventory_data,
        'success_message': request.GET.get('message') if request.GET.get('success') == 'True' else None,
        'error_message': request.GET.get('message') if request.GET.get('error') == 'True' else None,
        'SoftwareType':SoftwareType,
        'SoftwareName':SoftwareName,
        'software_AMC_Type':software_AMC_Type,
        'AMC_Status':AMC_Status
    }
    return render(request, 'Inventory/Software_List.html', context)

def Hardware_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    UserID = str(request.session["UserID"])
    OrganizationID = str(request.session.get("OrganizationID"))
    SessionOrganizationID = int(OrganizationID)

    # Get selected organization from query param
    SelectedOrganizationID_str = request.GET.get('OrganizationID', OrganizationID)
    SelectedOrganizationID = int(SelectedOrganizationID_str) if SelectedOrganizationID_str != 'All' else None
    
    if UserID=="20201212180048":
        OrganizationID=401

    # Filter IT Inventory
    itInventory = IT_Inventory.objects.filter(IsDelete=False, Inventory_Type="Hardware").order_by('-CreatedDateTime')

    if SelectedOrganizationID is not None:
        itInventory = itInventory.filter(OrganizationID=SelectedOrganizationID)

    # Filter organization options based on session org
    if SessionOrganizationID == 3 or SelectedOrganizationID == 'All':
        orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1)
    else:
        orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1, OrganizationID=SessionOrganizationID)

    # Additional filters
    HardwareType = request.GET.get("HardwareType", "")
    SerialNo = request.GET.get("SerialNo", "")
    ModelNo = request.GET.get("ModelNo", "")
    Make = request.GET.get("Make", "")
    ComputerName = request.GET.get("ComputerName", "")
    warrantyStatus = request.GET.get("warrantyStatus", "")


    if HardwareType:
        itInventory = itInventory.filter(type=HardwareType)
    if SerialNo:
        itInventory = itInventory.filter(SerialNo=SerialNo)
    if ModelNo:
        itInventory = itInventory.filter(Model_No=ModelNo)
    if Make:
        itInventory = itInventory.filter(Make=Make)
    if ComputerName:
        itInventory = itInventory.filter(computer_name=ComputerName)
    if warrantyStatus:
        itInventory = itInventory.filter(Warrantiy_Status=warrantyStatus)


    inventory_data = []
    for inventory in itInventory:
        qr_code_base64 = inventory.get_qr_code_base64()
        inventory_data.append({'inventory': inventory, 'qr_code_base64': qr_code_base64})

    Categorys = Master_Category.objects.filter(IsDelete=False)
    companys = Master_Company.objects.filter(IsDelete=False)
    Areas = Master_Area.objects.filter(IsDelete=False)
    software_types = Master_Software_type.objects.filter(IsDelete=False)

    if SelectedOrganizationID is None:
        SerialNoList = IT_Inventory.objects.filter(IsDelete=False).values("SerialNo").distinct()
        ModelNoList = IT_Inventory.objects.filter(IsDelete=False).values("Model_No").distinct()
        ComputerNameList = IT_Inventory.objects.filter(IsDelete=False).values("computer_name").distinct()
    else:
        SerialNoList = IT_Inventory.objects.filter(IsDelete=False, OrganizationID=SelectedOrganizationID).values("SerialNo").distinct()
        ModelNoList = IT_Inventory.objects.filter(IsDelete=False, OrganizationID=SelectedOrganizationID).values("Model_No").distinct()
        ComputerNameList = IT_Inventory.objects.filter(IsDelete=False, OrganizationID=SelectedOrganizationID).values("computer_name").distinct()

    context = {
        'orgs': orgs,
        'selectedOrganizationID': SelectedOrganizationID_str,
        'SessionOrganizationID': SessionOrganizationID,
        'Categorys':Categorys,
        'companys':companys,
        'SerialNoList':SerialNoList,
        'ModelNoList':ModelNoList,
        'ComputerNameList':ComputerNameList,
        'Areas':Areas,
        'software_types':software_types,
        'inventory_data': inventory_data,
        'success_message': request.GET.get('message') if request.GET.get('success') == 'True' else None,
        'error_message': request.GET.get('message') if request.GET.get('error') == 'True' else None,
        'HardwareType':HardwareType,
        'SerialNo':SerialNo,
        'ModelNo':ModelNo,
        'Make':Make,
        'ComputerName':ComputerName,
        'warrantyStatus':warrantyStatus,
    }
    return render(request, 'Inventory/Hardware_List.html', context)



from django.template.loader import get_template
from Employee_Payroll.models import Organization_Details
from app.models import OrganizationMaster
from datetime import datetime
from xhtml2pdf import pisa
from django.http import HttpResponse, JsonResponse, response

def IT_Inventory_Data_PDF(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
    if UserID=="20201212180048":
        OrganizationID=401

    # itInventory = IT_Inventory.objects.filter(IsDelete=False, OrganizationID=OrganizationID, Inventory_Type="Hardware").order_by('-CreatedDateTime')
    

    # Get filter parameters
    # hardwareTypeInput = request.GET.get('hardwareTypeInput', '').strip()
    # serialNoInput = request.GET.get('serialNoInput', '').strip()
    # modelNoInput = request.GET.get('modelNoInput', '').strip()
    # makeInput = request.GET.get('makeInput', '').strip()
    # warrantyStatusInput = request.GET.get('warrantyStatusInput', '').strip()

    Inventory_Type = request.GET.get('Inventory_Type', '').strip()
    print("Inventory_Type",Inventory_Type)

    itInventory_data = IT_Inventory.objects.filter(IsDelete=False, OrganizationID=OrganizationID, Inventory_Type=Inventory_Type).order_by('-CreatedDateTime')

    print("itInventory_data ------>", itInventory_data)

    # print(organization_logo)
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

    organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    organization_logo = organizations.OrganizationName

    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    context = {
        'inventory_data': itInventory_data,
        'organization_logo': organization_logo,
        'organization_logos':organization_logos,
        'current_datetime':current_datetime,
        'Inventory_Type':Inventory_Type
    }

    if Inventory_Type == 'Software':
        template_path = 'Inventory/IT_Inventory_Software_PDF.html'
    elif Inventory_Type == 'Hardware':
        template_path = 'Inventory/IT_Inventory_Hardware_PDF.html'
    else:
        template_path = ''

    template = get_template(template_path)
    html = template.render(context).encode("UTF-8")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="IT_Inventory_Details_{organization_logo}.pdf"'
    # response['Content-Disposition'] = f'attachment; filename="{organization_logo}_{start_date}__To__{end_date}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response, encoding="UTF-8")

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response




def Qr_details(request):
    
    qr_code_id = request.GET.get('qr_code_id')
 
    print(qr_code_id)
    item = IT_Inventory.objects.get(qr_code_id = qr_code_id ,IsDelete=False)
    print(item.qr_code_id)
    context = {'item': item} 
    return render(request, 'Inventory/Qr_details.html', context)







from django.http import HttpResponseRedirect

def Inventory_delete(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
        
    id=request.GET.get('ID')
    it=IT_Inventory.objects.get(id=id)
    it.IsDelete=True
    it.ModifyBy=UserID
    it.save()
    # return redirect(Inventory_list) 

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return HttpResponseRedirect(referer)
    else:
        return redirect(Software_List)  



import requests     
def inventory_report(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID = request.session["OrganizationID"]

    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

    Categorys = Master_Category.objects.filter(IsDelete=False)
    companys = Master_Company.objects.filter(IsDelete=False)
    Areas = Master_Area.objects.filter(IsDelete=False)
    software_types = Master_Software_type.objects.filter(IsDelete=False)

    type = request.GET.get('type')
    softwaretype = request.GET.get('softwaretype')
    Warrantiy_Status = request.GET.get('Warrantiy_Status')
    Area = request.GET.get('Area')
    Make = request.GET.get('Make')
    AMC_Status = request.GET.get('AMC_Status')
    amctype = request.GET.get('amctype')
    software_AMC_Type = request.GET.get('software_AMC_Type')
    OrganizationID = request.GET.get('OrganizationID')

    
    queryset = IT_Inventory.objects.filter()

    filter_args = {}

    if type:
        filter_args['type'] = type

    if softwaretype:
        filter_args['softwaretype'] = softwaretype

    if Warrantiy_Status:
        filter_args['Warrantiy_Status'] = Warrantiy_Status

    if Area:
        filter_args['Area'] = Area

    if Make:
        filter_args['Make'] = Make

    if AMC_Status:
        filter_args['AMC_Status'] = AMC_Status

    if amctype:
        filter_args['amctype'] = amctype

    if software_AMC_Type:
        filter_args['software_AMC_Type'] = software_AMC_Type

    if OrganizationID:
         filter_args['OrganizationID'] = OrganizationID    

    
    queryset = queryset.filter(**filter_args)

    context = {
        'memOrg': memOrg,
        'itInventorys': queryset,
        'Categorys': Categorys,
        'companys': companys,
        'Areas': Areas,
        'software_types': software_types,
        'type': type,
        'softwaretype': softwaretype,
        'Warrantiy_Status': Warrantiy_Status,
        'Area': Area,
        'Make': Make,
        'AMC_Status': AMC_Status,
        'amctype': amctype,
        'software_AMC_Type': software_AMC_Type,
        'OrganizationID':OrganizationID
    }
    return render(request, 'Inventory/inventory_report.html', context)













def Type_category(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    category_id = request.GET.get('ID')
    category = None
    if category_id is not None:
        category = get_object_or_404(Master_Category,id=category_id,OrganizationID=OrganizationID)
    if request.method == "POST":
        if category_id is not None:
             category.Category_Type = request.POST['Category_Type']
             category.ModifyBy=UserID
             category.save()
             messages.success(request, "Category Name Update on list   Successfully !!!!")
             return redirect('Type_category_list')
        else:
             

            Category_Type = request.POST['Category_Type']
            category_type=Master_Category.objects.create(Category_Type=Category_Type,OrganizationID=OrganizationID,CreatedBy=UserID)
            messages.success(request, "Category Name add on list Successfully !!!!")
            return redirect('Type_category_list')
    context={'category':category}
    return render(request,'Inventory/Type_category.html',context)


def Type_category_list(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    categorys = Master_Category.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'categorys':categorys}

    return render(request,'Inventory/Type_category_list.html',context)
     

def categorys_delete(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
        
    id=request.GET.get('ID')
    C_t=Master_Category.objects.get(id=id)
    C_t.IsDelete=True
    C_t.ModifyBy=UserID
    C_t.save()
    return redirect(Type_category_list)      
     


def Master_company_add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    company_id = request.GET.get('ID')
    company = None
    if company_id is not None:
        company = get_object_or_404(Master_Company,id=company_id,OrganizationID=OrganizationID)
    if request.method == "POST":
        if company_id is not None:
             company.Company_name = request.POST['Company_name']
             company.ModifyBy=UserID
             company.save()
             messages.success(request, "Company Name Update on list   Successfully !!!!")
             return redirect('Master_company_list')
        else:
             

            Company_name = request.POST['Company_name']
            company_name=Master_Company.objects.create(Company_name=Company_name,OrganizationID=OrganizationID,CreatedBy=UserID)
            messages.success(request, "Company Name add on list Successfully !!!!")
            return redirect('Master_company_list')
    context={'company':company}
    return render(request,'Inventory/Master_company_add.html',context)
     
       

def Master_company_list(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    companys = Master_Company.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'companys':companys}
    return render(request,'Inventory/Master_company_list.html',context)



def company_delete(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
        
    id=request.GET.get('ID')
    com=Master_Company.objects.get(id=id)
    com.IsDelete=True
    com.ModifyBy=UserID
    com.save()
    return redirect(Master_company_list)  


def Master_Area_add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    area_id = request.GET.get('ID')
    area = None
    if area_id is not None:
        area = get_object_or_404(Master_Area,id=area_id,OrganizationID=OrganizationID)
    if request.method == "POST":
        if area_id is not None:
             area.Area_name = request.POST['Area_name']
             area.ModifyBy=UserID
             area.save()
             messages.success(request, "Area Name Update on list   Successfully !!!!")
             return redirect('Master_Area_list')
        else:
             

            Area_name = request.POST['Area_name']
            area_name=Master_Area.objects.create(Area_name=Area_name,OrganizationID=OrganizationID,CreatedBy=UserID)
            messages.success(request, "Area Name add on list Successfully !!!!")
            return redirect('Master_Area_list')
    context={'area':area}
    return render(request,'Inventory/Master_Area_add.html',context)



def Master_Area_list(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    areas = Master_Area.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'areas':areas}
    return render(request,'Inventory/Master_Area_list.html',context)

     


def area_delete(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
        
    id=request.GET.get('ID')
    are=Master_Area.objects.get(id=id)
    are.IsDelete=True
    are.ModifyBy=UserID
    are.save()
    return redirect(Master_Area_list)   




def Master_software_type_list(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    softwares = Master_Software_type.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'softwares':softwares}
    return render(request,'Inventory/Master_software_type_list.html',context)



def Master_software_type(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    Software_id = request.GET.get('ID')
    Software = None
    if Software_id is not None:
        Software = get_object_or_404(Master_Software_type,id=Software_id,OrganizationID=OrganizationID)
    if request.method == "POST":
        if Software_id is not None:
             Software.software_name = request.POST['software_name']
             Software.ModifyBy=UserID
             Software.save()
             messages.success(request, "Area Name Update on list   Successfully !!!!")
             return redirect('Master_software_type_list')
        else:
             

            software_name = request.POST['software_name']
            soft=Master_Software_type.objects.create(software_name=software_name,OrganizationID=OrganizationID,CreatedBy=UserID)
            messages.success(request, "Software Type add on list Successfully !!!!")
            return redirect('Master_software_type_list')
    context={'Software':Software}
    return render(request,'Inventory/Master_software_type.html',context)



def sftware_delete(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
        
    id=request.GET.get('ID')
    soft=Master_Software_type.objects.get(id=id)
    soft.IsDelete=True
    soft.ModifyBy=UserID
    soft.save()
    return redirect(Master_software_type_list)   

     


# ----- for email

# inventory/utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_inventory_email(inventory, created_by, recipients=None, useraction='', OrgName=''):
    subject = f"New IT Inventory {useraction}"
    # subject = f"New IT Inventory Added"
    message = f"""
        A new inventory item has been {useraction}:

        Type: {inventory.Inventory_Type}
        Description: {inventory.Description}
        Serial No: {inventory.SerialNo}
        Make: {inventory.Make}
        Model: {inventory.Model_No}
        Added By: {created_by}
        Organization Name: {OrgName}
    """

    if recipients is None:
        recipients = ["Vasudev.Pareek@nilehospitality.com"]  

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipients,
        fail_silently=False,
    )





# from datetime import datetime, timedelta, date
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import IT_Inventory

# def send_expiry_reminders():
#     today = date.today()
#     reminder_date = today + timedelta(days=30)   # 1 month before expiry
#     to_email = "Vasudev.Pareek@nilehospitality.com"

#     expiring_items = []

#     for item in IT_Inventory.objects.filter(IsDelete=False):
#         # --- Handle hardware AMC expiry ---
#         if item.amcend:
#             try:
#                 amc_end = datetime.strptime(item.amcend, "%Y-%m-%d").date()
#                 if amc_end == reminder_date:
#                     expiring_items.append((item, "Hardware AMC", amc_end))
#             except:
#                 pass  # skip invalid date formats

#         # --- Handle software AMC expiry ---
#         if item.software_AMC_end:
#             try:
#                 sw_amc_end = datetime.strptime(item.software_AMC_end, "%Y-%m-%d").date()
#                 if sw_amc_end == reminder_date:
#                     expiring_items.append((item, "Software AMC", sw_amc_end))
#             except:
#                 pass

#         # --- Handle warranty expiry ---
#         if item.Warrantiy_end:
#             try:
#                 warranty_end = datetime.strptime(item.Warrantiy_end, "%Y-%m-%d").date()
#                 if warranty_end == reminder_date:
#                     expiring_items.append((item, "Warranty", warranty_end))
#             except:
#                 pass

#     # --- Send email if any expiring ---
#     if expiring_items:
#         subject = "Reminder: AMC/Warranty Expiry Alert"
#         body_lines = ["The following items will expire in 30 days:\n"]
#         for inv, inv_type, exp_date in expiring_items:
#             body_lines.append(f"- {inv.Description or inv.SerialNo} ({inv_type}) → Expiry: {exp_date}")
#         body = "\n".join(body_lines)

#         send_mail(
#             subject,
#             body,
#             settings.DEFAULT_FROM_EMAIL,
#             [to_email],
#             fail_silently=False,
#         )
