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
    return render(request,'cake/index.html')

# Inserting Cake Order Form
def CakeOrder(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
    CakeOrderForm=forms.CakeOrderForm()
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    mydict={'CakeOrderForm':CakeOrderForm,'d':d}
    if request.method=='POST':
        # userForm=forms.DoctorUserForm(request.POST)
        CakeOrderForm=forms.CakeOrderForm(request.POST,request.FILES)
        print(CakeOrderForm.is_valid())
        if CakeOrderForm.is_valid():
            CakeOrder=CakeOrderForm.save(commit=False)
            CakeOrder=CakeOrder.save()
            # my_doctor_group = Group.objects.get_or_create(name='CakeOrder')
          
        return HttpResponseRedirect('CakeOrderList')
    return render(request,'cake/CakeOrder.html',context=mydict) 


#For Showing List Of the CakeOrder    
def CakeOrderList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        OrganizationID =request.session["OrganizationID"]
        all_data = Cake_Order_Form.objects.filter(OrganizationID=OrganizationID,IsDelete=False).order_by("CreatedDateTime")
        return render(request,"cake/cakeorderlist.html",{'key1':all_data})


#For Editing The Cake Order Data
def CakeOrderEditData(request):
    
       id = request.GET["id"]
   
       get_data = Cake_Order_Form.objects.get(id=id)
       
       CakeOrderForm=forms.CakeOrderForm()
     
       
       mydict={'CakeOrderForm':CakeOrderForm,'Ed':get_data}
       
       return render(request,"cake/cakeordereditdata.html",context=mydict)
 
       
#For Updating the Order Data
def CakeOrderUpdateData(request):
        print(request)
        id = request.POST["ID"]
        # print(id)
        CakeOrderForm =  Cake_Order_Form.objects.get(id=id)
          
        To = request.POST["To"]
        CakeOrderForm.To=To
          
        Date = request.POST["Date"]
        CakeOrderForm.Date=Date
        
        From = request.POST["From"]
        CakeOrderForm.From=From
        
        Time = request.POST["Time"]
        CakeOrderForm.Time=Time
        
        Guest_Name = request.POST["Guest_Name"]
        CakeOrderForm.Guest_Name=Guest_Name
        
        To_Be_Prepared_For = request.POST["To_Be_Prepared_For"]
        CakeOrderForm.To_Be_Prepared_For=To_Be_Prepared_For
        
        Size = request.POST["Size"]
        CakeOrderForm.Size=Size
        
        Type_Of_Cake = request.POST["Type_Of_Cake"]
        CakeOrderForm.Type_Of_Cake=Type_Of_Cake
        
        Required_Date = request.POST["Required_Date"]
        CakeOrderForm.Required_Date=Required_Date
        
        Required_Time = request.POST["Required_Time"]
        CakeOrderForm.Required_Time=Required_Time
        
        Packing = request.POST["Packing"]
        CakeOrderForm.Packing=Packing
        
        Selling_Price = request.POST["Selling_Price"]
        CakeOrderForm.Selling_Price=Selling_Price
        
        Message_On_Cake = request.POST["Message_On_Cake"]
        CakeOrderForm.Message_On_Cake=Message_On_Cake
        
        Complimentory = request.POST["Complimentory"]
        CakeOrderForm.Complimentory=Complimentory
        
        Authorised_By = request.POST["Authorised_By"]
        CakeOrderForm.Authorised_By=Authorised_By
         
        
        CakeOrderForm.save()
        
        return redirect('CakeOrderList')

#For Deleting The Cake Order Data
def Delete(request):
       id = request.GET["id"]
  
       cakeorder = Cake_Order_Form.objects.get(id=id)
       cakeorder.IsDelete=True;
       cakeorder.save();
       return redirect('CakeOrderList')

   
   
# For Showing Pdf View Of Your Cake Order 
def CakeOrderList_pdf_view(request):
    
     id = request.GET["id"]
    
     template_path = "cake/cakeorderviewdata.html"
    # NileLogo=MasterAttribute.NileLogo
     get_data =Cake_Order_Form.objects.get(id=id)
    
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
