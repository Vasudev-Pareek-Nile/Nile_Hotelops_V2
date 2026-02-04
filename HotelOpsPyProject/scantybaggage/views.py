from io import BytesIO
from django.shortcuts import render
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
    return render(request,'scanty/index.html')

# Inserting Scanty Baggage Form
def ScantyBaggageForm(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
    ScantyBaggageForm=forms.ScantyBaggageForm()
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    mydict={'ScantyBaggageForm':ScantyBaggageForm,'d':d}
    if request.method=='POST':
       
        ScantyBaggageForm=forms.ScantyBaggageForm(request.POST,request.FILES)
        print(ScantyBaggageForm.is_valid())
        if ScantyBaggageForm.is_valid():
            Scantybaggage=ScantyBaggageForm.save(commit=False)
            Scantybaggage=Scantybaggage.save()
           
          
        return HttpResponseRedirect('ScantyBaggageList')
    return render(request,'scanty/scantybaggageform.html',context=mydict) 


#For Showing List Of the ScantyBaggage    
def ScantyBaggageList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        OrganizationID =request.session["OrganizationID"]
        all_data = Scanty_Baggage_Register_Form.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
        return render(request,"scanty/scantybaggagelist.html",{'key1':all_data})


#For Editing The  ScantyBaggage Form  
def ScantyBaggageEditList(request):
    
       id = request.GET["id"]
   
       get_data = Scanty_Baggage_Register_Form.objects.get(id=id)
       
       ScantyBaggageForm=forms.ScantyBaggageForm()
     
       
       mydict={'ScantyBaggageForm':ScantyBaggageForm,'Ed':get_data}
       
       return render(request,"scanty/scantybaggageeditlist.html",context=mydict)
 
       
#For Updating the Scanty Baggage List
def ScantyBaggageUpdateData(request):
        print(request)
        id = request.POST["ID"]
        # print(id)
        ScantyBaggageForm =  Scanty_Baggage_Register_Form.objects.get(id=id)
          
        Date = request.POST["Date"]
        ScantyBaggageForm.Date=Date
          
        Room_No = request.POST["Room_No"]
        ScantyBaggageForm.Room_No=Room_No
        
        Guest_Name = request.POST["Guest_Name"]
        ScantyBaggageForm.Guest_Name=Guest_Name
        
        Arrival_Date = request.POST["Arrival_Date"]
        ScantyBaggageForm.Arrival_Date=Arrival_Date
        
        Departure_Date = request.POST["Departure_Date"]
        ScantyBaggageForm.Departure_Date=Departure_Date
        
        Deposite = request.POST["Deposite"]
        ScantyBaggageForm.Deposite=Deposite
        
        Comment = request.POST["Comment"]
        ScantyBaggageForm.Comment=Comment
        
        Front_Desk_Associate = request.POST["Front_Desk_Associate"]
        ScantyBaggageForm.Front_Desk_Associate=Front_Desk_Associate
        
        Duty_Manager = request.POST["Duty_Manager"]
        ScantyBaggageForm.Duty_Manager=Duty_Manager
        
        Remarks = request.POST["Remarks"]
        ScantyBaggageForm.Remarks=Remarks
        
        
        
        ScantyBaggageForm.save()
        
        return redirect('ScantyBaggageList')

#For Deleting The Scanty Baggage List
def ScantyBaggageDeleteData(request):
       id = request.GET["id"]
  
       scantybaggage = Scanty_Baggage_Register_Form.objects.get(id=id)
       scantybaggage.IsDelete=True;
       scantybaggage.save();
       return redirect('ScantyBaggageList')
   
    

# For Showing Pdf View Of Scanty Baggage  
def ScantyBaggage_pdf_view(request):
     id = request.GET["id"]
     template_path = "scanty/scantybaggageviewlist.html"
    # NileLogo=MasterAttribute.NileLogo
     get_data =Scanty_Baggage_Register_Form.objects.get(id=id)
     mydict={'Ed':get_data}
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

   


