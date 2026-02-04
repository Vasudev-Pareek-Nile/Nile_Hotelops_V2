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
    return render(request,'parcel/index.html')

# Inserting in Parcel Registration Form
def MessageAndParcelForm(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
    MessageAndParcelForm=forms.MessageAndParcelForm()
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    mydict={'MessageAndParcelForm':MessageAndParcelForm,'d':d}
    
    if request.method=='POST':
        # userForm=forms.DoctorUserForm(request.POST)
        MessageAndParcelForm=forms.MessageAndParcelForm(request.POST,request.FILES)
        print(MessageAndParcelForm.is_valid())
        
        if MessageAndParcelForm.is_valid():
            MessageAndParcel=MessageAndParcelForm.save(commit=False)
            MessageAndParcel=MessageAndParcel.save()
            # my_doctor_group = Group.objects.get_or_create(name='CakeOrder')
          
        return HttpResponseRedirect('MessageAndParcelList')
    return render(request,'parcel/MessageandParcelform.html',context=mydict) 


#For Showing List Of the Parcel Registration
def MessageAndParcelList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        OrganizationID =request.session["OrganizationID"]
        all_data = Message_Parcel_Register.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
        return render(request,"parcel/MessageandParcellist.html",{'key1':all_data})


#For Editing The Parcel Registration List
def MessageAndParcelEditList(request):
    
       id = request.GET["id"]
   
       get_data = Message_Parcel_Register.objects.get(id=id)
       
       MessageAndParcelForm=forms.MessageAndParcelForm()
     
       
       mydict={'MessageAndParcelForm':MessageAndParcelForm,'Ed':get_data}
       
       return render(request,"parcel/MessageandParceleditlist.html",context=mydict)
 
       
#For Updating theParcel Registration List
def MessageAndParcelUpdateData(request):
        print(request)
        id = request.POST["ID"]
        # print(id)
        MessageAndParcelForm =  Message_Parcel_Register.objects.get(id=id)
          
        Type_Of_Article = request.POST["Type_Of_Article"]
        MessageAndParcelForm.Type_Of_Article=Type_Of_Article
          
        Room_No = request.POST["Room_No"]
        MessageAndParcelForm.Room_No=Room_No
        
        Guest_Name = request.POST["Guest_Name"]
        MessageAndParcelForm.Guest_Name=Guest_Name
        
        Date_Of_Arrival = request.POST["Date_Of_Arrival"]
        MessageAndParcelForm.Date_Of_Arrival=Date_Of_Arrival
        
        Received_From = request.POST["Received_From"]
        MessageAndParcelForm.Received_From=Received_From
        
        Contact_No = request.POST["Contact_No"]
        MessageAndParcelForm.Contact_No=Contact_No
        
        Received_By = request.POST["Received_By"]
        MessageAndParcelForm.Received_By=Received_By
        
        Date_Of_Delivery = request.POST["Date_Of_Delivery"]
        MessageAndParcelForm.Date_Of_Delivery=Date_Of_Delivery
        
        Given_By = request.POST["Given_By"]
        MessageAndParcelForm.Given_By=Given_By
        
        Handed_Over_To = request.POST["Handed_Over_To"]
        MessageAndParcelForm.Handed_Over_To=Handed_Over_To
        
        Remarks = request.POST["Remarks"]
        MessageAndParcelForm.Remarks=Remarks
        
        
        MessageAndParcelForm.save()
        
        return redirect('MessageAndParcelList')

#For Deleting The Parcel Registration List
def MessageAndParcelDeleteData(request):
       id = request.GET["id"]
  
       Parcel = Message_Parcel_Register.objects.get(id=id)
       Parcel.IsDelete=True;
       Parcel.save();
       return redirect('MessageAndParcelList')
   
   
# For Showing Your Order Page
def MessageAndParcelView(request):
      
       id = request.GET["id"]
  
       get_data = Message_Parcel_Register.objects.get(id=id)
  
       MessageAndParcelForm=forms.MessageAndParcelForm()
     
       mydict={'MessageAndParcelForm':MessageAndParcelForm,'Ed':get_data}
       
       return render(request,"parcel/MessageandParcelview.html",context=mydict)
   
   
# For Showing Pdf View Of Parcel Register  
def ParcelList_pdf_view(request):
    
     id = request.GET["id"]
    
     template_path = "parcel/MessageandParcelview.html"
    # NileLogo=MasterAttribute.NileLogo
     get_data =Message_Parcel_Register.objects.get(id=id)
    
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
