from io import BytesIO
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse, HttpResponseRedirect
from requests import Session, post
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from . import forms
from django.contrib.auth.models import Group
from .models import *
from django.shortcuts import render,redirect
from xhtml2pdf import pisa
from django.template.loader import get_template
from scantybaggage import link_callback 


def home_view(request):
    return render(request,'equipment/index.html')

# Inserting Equipment Trolley Inventory Form
def EquipmentAndTrolleyForm(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
    EquipmentInventoryForm=forms.EquipmentInventoryForm()
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    mydict={'EquipmentInventoryForm':EquipmentInventoryForm,'d':d}
    
    if request.method=='POST':
        # userForm=forms.DoctorUserForm(request.POST)
        EquipmentInventoryForm=forms.EquipmentInventoryForm(request.POST,request.FILES)
        print(EquipmentInventoryForm.is_valid())
        
        if EquipmentInventoryForm.is_valid():
            EquipmentTrolley=EquipmentInventoryForm.save(commit=False)
            EquipmentTrolley=EquipmentTrolley.save()
            # my_doctor_group = Group.objects.get_or_create(name='CakeOrder')
          
        return HttpResponseRedirect('EquipmentAndTrolleyList')
    return render(request,'equipment/EquipmentForm.html',context=mydict) 


#For Showing List Of the Equipment Trolley Inventory  
def EquipmentAndTrolleyList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        OrganizationID =request.session["OrganizationID"]
        all_data = Equipment_Inventory.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
        return render(request,"equipment/Equipmentlist.html",{'key1':all_data})


#For Editing The Equipment Trolley Inventory List
def EquipmentEditList(request):
    
       id = request.GET["id"]
   
       get_data = Equipment_Inventory.objects.get(id=id)
       
       EquipmentInventoryForm=forms.EquipmentInventoryForm()
     
       
       mydict={'EquipmentInventoryForm':EquipmentInventoryForm,'Ed':get_data}
       
       return render(request,"equipment/Equipmenteditlist.html",context=mydict)
 
       
#For Updating the Equipment Trolley Inventory List
def EquipmentUpdateData(request):
        print(request)
        id = request.POST["ID"]
        # print(id)
        EquipmentInventoryForm =  Equipment_Inventory.objects.get(id=id)
          
        Date = request.POST["Date"]
        EquipmentInventoryForm.Date=Date
          
        Equipment_Name = request.POST["Equipment_Name"]
        EquipmentInventoryForm.Equipment_Name=Equipment_Name
        
        Brand_Name = request.POST["Brand_Name"]
        EquipmentInventoryForm.Brand_Name=Brand_Name
        
        Model_No = request.POST["Model_No"]
        EquipmentInventoryForm.Model_No=Model_No
        
        In_Working_Condition = request.POST["In_Working_Condition"]
        EquipmentInventoryForm.In_Working_Condition=In_Working_Condition
        
        Last_Servicing_Date = request.POST["Last_Servicing_Date"]
        EquipmentInventoryForm.Last_Servicing_Date=Last_Servicing_Date
        
        AMC_Covered = request.POST["AMC_Covered"]
        EquipmentInventoryForm.AMC_Covered=AMC_Covered
        
        Serial_No = request.POST["Serial_No"]
        EquipmentInventoryForm.Serial_No=Serial_No
        
        
        Remarks = request.POST["Remarks"]
        EquipmentInventoryForm.Remarks=Remarks
        
        
        EquipmentInventoryForm.save()
        
        return redirect('EquipmentAndTrolleyList')

#For Deleting The Equipment Trolley Inventory List
def EquipmentDeleteData(request):
       id = request.GET["id"]
  
       Equipment = Equipment_Inventory.objects.get(id=id)
       Equipment.IsDelete=True;
       Equipment.save();
       return redirect('EquipmentAndTrolleyList')
   
   
   
# For Showing Pdf View Of Pay Master  
def EquipmentList_pdf_view(request):
    
     id = request.GET["id"]
    
     template_path = "equipment/Equipmentviewlist.html"
    # NileLogo=MasterAttribute.NileLogo
     get_data =Equipment_Inventory.objects.get(id=id)
    
    #  ScantyBaggageForm=forms.ScantyBaggageForm()
     
     mydict={'Ed':get_data}

    # context = {'myvar': 'this is your template context','p':varM}
    
    # Create a Django response object, and specify content_type as pdf
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'filename="report gcc club.pdf"'
    # find the template and render it.
     template = get_template(template_path)
     html = template.render(mydict)

    # create a pdf
     result = BytesIO()
    #  pisa_status = pisa.CreatePDF(
     pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        # html, dest=response, link_callback=link_callback)
    # if error then show some funny view
     if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
     return None 
   
   
