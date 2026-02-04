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
    return render(request,'pass/index.html')

# Inserting Visitor Pass Form
def VisitorPassForm(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
    VisitorPassForm=forms.VisitorPassForm()
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    mydict={'VisitorPassForm':VisitorPassForm,'d':d}
    if request.method=='POST':
        # userForm=forms.DoctorUserForm(request.POST)
        VisitorPassForm=forms.VisitorPassForm(request.POST,request.FILES)
        print(VisitorPassForm.is_valid())
        if VisitorPassForm.is_valid():
            VisitorPass=VisitorPassForm.save(commit=False)
            VisitorPass=VisitorPass.save()
            # my_doctor_group = Group.objects.get_or_create(name='CakeOrder')
          
        return HttpResponseRedirect('VisitorPassList')
    return render(request,'pass/visitorpassform.html',context=mydict) 


#For Showing List Of the Visitor Pass
def VisitorPassList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        OrganizationID =request.session["OrganizationID"]
        all_data = Visitor_Pass.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
        return render(request,"pass/visitorpasslist.html",{'key1':all_data})


#For Editing The Cake Visitor Pass List
def VisitorPassEditData(request):
    
       id = request.GET["id"]
   
       get_data = Visitor_Pass.objects.get(id=id)
       
       VisitorPassForm=forms.VisitorPassForm()
     
       
       mydict={'VisitorPassForm':VisitorPassForm,'Ed':get_data}
       
       return render(request,"pass/visitorpasseditlist.html",context=mydict)
 
       
#For Updating the Visitor Pass List
def VisitorPassUpdateData(request):
        print(request)
        id = request.POST["ID"]
        # print(id)
        VisitorPassForm =  Visitor_Pass.objects.get(id=id)
          
        Date = request.POST["Date"]
        VisitorPassForm.Date=Date
          
        In_Time = request.POST["In_Time"]
        VisitorPassForm.In_Time=In_Time
        
        Name = request.POST["Name"]
        VisitorPassForm.Name=Name
        
        Purpose_Of_Visite = request.POST["Purpose_Of_Visite"]
        VisitorPassForm.Purpose_Of_Visite=Purpose_Of_Visite
        
        
        VisitorPassForm.save()
        
        return redirect('VisitorPassList')

#For Deleting The Visitor Pass list
def VisitorPassDeleteData(request):
       id = request.GET["id"]
  
       visitorpass = Visitor_Pass.objects.get(id=id)
       visitorpass.IsDelete=True;
       visitorpass.save();
       return redirect('VisitorPassList')
   
   
# # For Showing Your Visitor Pass Page
# def VisitotPassView(request):
      
#        id = request.GET["id"]
  
#        get_data = Visitor_Pass.objects.get(id=id)
  
#        VisitorPassForm=forms.VisitorPassForm()
     
#        mydict={'VisitorPassForm':VisitorPassForm,'Ed':get_data}
       
#        return render(request,"pass/visitorpassview.html",context=mydict)
   
   
# For Showing Pdf View Of Pay Master  
def VisitorPass_pdf_view(request):
    
     id = request.GET["id"]
    
     template_path = "pass/visitorpassview.html"
    # NileLogo=MasterAttribute.NileLogo
     get_data =Visitor_Pass.objects.get(id=id)
    
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
     pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funny view
     if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
     return response  