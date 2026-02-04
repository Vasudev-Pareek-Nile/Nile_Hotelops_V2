from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import Group
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from . import forms
from django.shortcuts import render,redirect
from .models import *
from xhtml2pdf import pisa
from django.template.loader import get_template
from scantybaggage import link_callback 

def home_view(request):
    return render(request,'app/index.html')


#CasualManpowerRequisistion
def CasualManPowerRequisition(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    print("Message : casualmanpowerrequisition")
    CasualManpowerRequisition=forms.CasualManpowerRequisition()
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}

    mydict={'CasualManpowerRequisition':CasualManpowerRequisition,'d':d}
    if request.method=='POST':
        print("Message : POST")
        # userForm=forms.DoctorUserForm(request.POST)
        CasualManpowerRequisition=forms.CasualManpowerRequisition(request.POST,request.FILES)
        print(CasualManpowerRequisition.is_valid())
        if CasualManpowerRequisition.is_valid():
         
            CasualManpower=CasualManpowerRequisition.save(commit=False)
            # doctor.user=user
            CasualManpower=CasualManpower.save()
            # my_doctor_group = Group.objects.get_or_create(name='CasualManpower')
            
        return HttpResponseRedirect('CasualManPowerList')
   
        
    return render(request,'app/casualmanpowerrequisition.html',context=mydict) 

# For Showing List   
def CasualManPowerList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    # for fetching all data from table
    OrganizationID =request.session["OrganizationID"]
    set_data = Casual_Manpower_Requisition.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
    return render(request,"app/casualmanpowerlist.html",{'key1':set_data})

# For Edit the Data List
def CasualManPowerEditList(request):
    
       id = request.GET["id"]
       
       get_data = Casual_Manpower_Requisition.objects.get(id=id)
       
       CasualManpowerRequisition=forms.CasualManpowerRequisition()

       mydict={'CasualManpowerRequisition':CasualManpowerRequisition,'Ed':get_data}
       
       return render(request,"app/casualmanpowereditlist.html",context=mydict)
   
# For Updating the Casual Manpower Requisition Data
def UpdateCasualManPowerData(request):
        # print(request)
        # print(id)
        id = request.POST["ID"]
        print("id")
        CasualManpowerRequisition = Casual_Manpower_Requisition.objects.get(id=id)
          
        Date = request.POST["Date"]
        CasualManpowerRequisition.Date=Date
        
        Prepared_By = request.POST["Prepared_By"]
        CasualManpowerRequisition.Prepared_By=Prepared_By
        
        Department = request.POST["Department"]
        CasualManpowerRequisition.Department=Department
        
        Numbers_Required = request.POST["Numbers_Required"]
        CasualManpowerRequisition.Numbers_Required=Numbers_Required
        
        Reason = request.POST["Reason"]
        CasualManpowerRequisition.Reason=Reason
        
        Function = request.POST["Function"]
        CasualManpowerRequisition.Function=Function
        
        Rate = request.POST["Rate"]
        CasualManpowerRequisition.Rate=Rate
        
        No_Of_Pax = request.POST["No_Of_Pax"]
        CasualManpowerRequisition.No_Of_Pax=No_Of_Pax
        
        Date_Required = request.POST["Date_Required"]
        CasualManpowerRequisition.Date_Required=Date_Required
        
        Est_Sales_Volume = request.POST["Est_Sales_Volume"]
        CasualManpowerRequisition.Est_Sales_Volume=Est_Sales_Volume
        
        Reporting_Time = request.POST["Reporting_Time"]
        CasualManpowerRequisition.Reporting_Time=Reporting_Time
        
        CasualManpowerRequisition.save()
        
        return redirect('CasualManPowerList')
   
   

   
   
#For Deleting The Cake Order Data
def CasualManPowerDeleteData(request):
       id = request.GET["id"]
  
       casualmanpower = Casual_Manpower_Requisition.objects.get(id=id)
       casualmanpower.IsDelete=True;
       casualmanpower.save();
       return redirect('CasualManPowerList')
   
   
# For Showing Pdf View Of Your Casual Manpower Requisition Form 
def CasualManpower_pdf_view(request):
    
     id = request.GET["id"]
    
     template_path = "app/casualmanpowerview.html"
    # NileLogo=MasterAttribute.NileLogo
     get_data =Casual_Manpower_Requisition.objects.get(id=id)
    
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

