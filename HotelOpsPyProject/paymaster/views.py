from io import BytesIO
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse, HttpResponseRedirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from . import forms
from .models import *
from django.shortcuts import render,redirect
from xhtml2pdf import pisa
from django.template.loader import get_template
from scantybaggage import link_callback 


def home_view(request):
    return render(request,'pay/index.html')

# Inserting Pay Master Form
def PaymasterForm(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
    PayMasterForm=forms.PayMasterForm()
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    mydict={'PayMasterForm':PayMasterForm,'d':d}
    if request.method=='POST':
        # userForm=forms.DoctorUserForm(request.POST)
        PayMasterForm=forms.PayMasterForm(request.POST,request.FILES)
        print(PayMasterForm.is_valid())
        if PayMasterForm.is_valid():
            PayMaster=PayMasterForm.save(commit=False)
            PayMaster=PayMaster.save()
            # my_doctor_group = Group.objects.get_or_create(name='CakeOrder')
          
        return HttpResponseRedirect('PaymasterList')
    return render(request,'pay/PayMasterform.html',context=mydict) 


#For Showing List Of the Pay Master  
def PaymasterList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        OrganizationID =request.session["OrganizationID"]
        all_data = Pay_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
        return render(request,"pay/PayMasterlist.html",{'key1':all_data})


#For Editing The Pay Master List
def PaymasterEditList(request):
    
       id = request.GET["id"]
   
       get_data = Pay_Master.objects.get(id=id)
       
       PayMasterForm=forms.PayMasterForm()
     
       
       mydict={'PayMasterForm':PayMasterForm,'Ed':get_data}
       
       return render(request,"pay/PayMasterEditList.html",context=mydict)
 
       
#For Updating the Pay Master List
def PayMasterUpdateData(request):
        print(request)
        id = request.POST["ID"]
        # print(id)
        PayMasterForm =  Pay_Master.objects.get(id=id)
          
        PM_Number = request.POST["PM_Number"]
        PayMasterForm.PM_Number=PM_Number
          
        PM_Date = request.POST["PM_Date"]
        PayMasterForm.PM_Date=PM_Date
        
        Name = request.POST["Name"]
        PayMasterForm.Name=Name
        
        Amount = request.POST["Amount"]
        PayMasterForm.Amount=Amount
        
        Employee_Name = request.POST["Employee_Name"]
        PayMasterForm.Employee_Name=Employee_Name
        
        Reason = request.POST["Reason"]
        PayMasterForm.Reason=Reason
        
        
        
        PayMasterForm.save()
        
        return redirect('PaymasterList')

#For Deleting The Pay Master List
def PayMasterDeleteData(request):
       id = request.GET["id"]
  
       Paymaster = Pay_Master.objects.get(id=id)
       Paymaster.IsDelete=True;
       Paymaster.save();
       return redirect('PaymasterList')   
   
# For Showing Pdf View Of Pay Master  
def PayMaster_pdf_view(request):
     id = request.GET["id"]
     template_path = "pay/PayMasterViewList.html"
    # NileLogo=MasterAttribute.NileLogo
     get_data =Pay_Master.objects.get(id=id) 
     mydict={'Ed':get_data}
     print('Ed')
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
   
   
