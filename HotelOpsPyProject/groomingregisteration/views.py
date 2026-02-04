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
    return render(request,'groom/index.html')

# Inserting Grooming Registration Form
def GroomingRegisterationForm(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
    GroomingRegisterationForm=forms.GroomingRegisterationForm()
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    mydict={'GroomingRegisterationForm':GroomingRegisterationForm,'d':d}
    
    if request.method=='POST':
        # userForm=forms.DoctorUserForm(request.POST)
        GroomingRegisterationForm=forms.GroomingRegisterationForm(request.POST,request.FILES)
        print(GroomingRegisterationForm.is_valid())
        
        if GroomingRegisterationForm.is_valid():
            Grooming=GroomingRegisterationForm.save(commit=False)
            Grooming=Grooming.save()
            # my_doctor_group = Group.objects.get_or_create(name='CakeOrder')
          
        return HttpResponseRedirect('GroomingRegisterationList')
    return render(request,'groom/GroomingRegisterationform.html',context=mydict) 


#For Showing List Of the Grooming Registration  
def GroomingRegisterationList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        OrganizationID =request.session["OrganizationID"]
        all_data = Grooming_Registeration.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
        return render(request,"groom/GroomingList.html",{'key1':all_data})


#For Editing The Grooming Registration List
def GroomingEditList(request):
    
       id = request.GET["id"]
   
       get_data = Grooming_Registeration.objects.get(id=id)
       
       GroomingRegisterationForm=forms.GroomingRegisterationForm()
     
       
       mydict={'GroomingRegisterationForm':GroomingRegisterationForm,'Ed':get_data}
       
       return render(request,"groom/GroomingEditList.html",context=mydict)
 
       
#For Updating the Grooming Registration List
def GroomingUpdateData(request):
        print(request)
        id = request.POST["ID"]
        # print(id)
        GroomingRegisterationForm = Grooming_Registeration.objects.get(id=id)
          
        Date = request.POST["Date"]
        GroomingRegisterationForm.Date=Date
          
        Audit_Type = request.POST["Audit_Type"]
        GroomingRegisterationForm.Audit_Type=Audit_Type
        
        Name = request.POST["Name"]
        GroomingRegisterationForm.Name=Name
        
        Shoes = request.POST["Shoes"]
        GroomingRegisterationForm.Shoes=Shoes
        
        Shocks = request.POST["Shocks"]
        GroomingRegisterationForm.Shocks=Shocks
        
        Nails = request.POST["Nails"]
        GroomingRegisterationForm.Nails=Nails
        
        Hair = request.POST["Hair"]
        GroomingRegisterationForm.Hair=Hair
        
        Uniform = request.POST["Uniform"]
        GroomingRegisterationForm.Uniform=Uniform
        
        Name_Badge = request.POST["Name_Badge"]
        GroomingRegisterationForm.Name_Badge=Name_Badge
        
        Brand_Pin = request.POST["Brand_Pin"]
        GroomingRegisterationForm.Brand_Pin=Brand_Pin
        
        Remarks = request.POST["Remarks"]
        GroomingRegisterationForm.Remarks=Remarks
        
        
        GroomingRegisterationForm.save()
        
        return redirect('GroomingRegisterationList')

#For Deleting The Grooming Registration List
def GroomingDeleteData(request):
       id = request.GET["id"]
  
       Grooming = Grooming_Registeration.objects.get(id=id)
       Grooming.IsDelete=True;
       Grooming.save();
       return redirect('GroomingRegisterationList')
   
   

   
   
# For Showing Pdf View Of Pay Master  
def GroomingList_pdf_view(request):
    
     id = request.GET["id"]
    
     template_path = "groom/GroomingViewlist.html"
    # NileLogo=MasterAttribute.NileLogo
     get_data =Grooming_Registeration.objects.get(id=id)
    
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

