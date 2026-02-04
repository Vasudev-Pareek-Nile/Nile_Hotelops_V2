from io import BytesIO
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse, HttpResponseRedirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from . import forms
from django.contrib.auth.models import Group
from .models import *
from django.shortcuts import render,redirect
from xhtml2pdf import pisa
from django.template.loader import get_template
from scantybaggage import link_callback 


def home_view(request):
    return render(request,'IRD/index.html')

# Inserting Pay Master Form
def IRDCleranceRegisrtration(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
    IRDCleranceForm=forms.IRDCleranceForm()
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    mydict={'IRDCleranceForm':IRDCleranceForm,'d':d}
    if request.method=='POST':
        # userForm=forms.DoctorUserForm(request.POST)
        
        IRDCleranceForm=forms.IRDCleranceForm(request.POST,request.FILES)
        
        # print(IRDCleranceForm.is_valid())
        if IRDCleranceForm.is_valid():
            IRDCleranceForm=IRDCleranceForm.save(commit=False)
            IRDCleranceForm=IRDCleranceForm.save()
            # my_doctor_group = Group.objects.get_or_create(name='CakeOrder')
          
        return HttpResponseRedirect('IRDCleranceList')
    return render(request,'IRD/irdcleranceform.html',context=mydict) 


#For Showing List Of the Pay Master  
def IRDCleranceList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
        OrganizationID =request.session["OrganizationID"]
        
        all_data = IRD_Clerance.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
        
        return render(request,"IRD/irdcleranceformlist.html",{'key1':all_data})


#For Editing The Pay Master List
def IRDCleranceEditList(request):
    
       id = request.GET["id"]
   
       get_data = IRD_Clerance.objects.get(id=id)
       
       IRDCleranceForm=forms.IRDCleranceForm()
     
       
       mydict={'IRDCleranceForm':IRDCleranceForm,'Ed':get_data}
       
       return render(request,"IRD/irdcleranceformedit.html",context=mydict)
 
       
#For 
# ing the Pay Master List
def IRDCleranceUpdateData(request):
        print(request)
        id = request.POST["ID"]
        # print(id)
        IRDCleranceForm =  IRD_Clerance.objects.get(id=id)
          
        Date = request.POST["Date"]
        IRDCleranceForm.Date=Date
          
        Clerance_time = request.POST["Clerance_time"]
        IRDCleranceForm.Clerance_time=Clerance_time
        
        Remarks = request.POST["Remarks"]
        IRDCleranceForm.Remarks=Remarks
        
        
        IRDCleranceForm.save()
        
        return redirect('IRDCleranceList')

#For Deleting The Pay Master List
def IRDCleranceDeleteData(request):
       id = request.GET["id"]
  
       student = IRD_Clerance.objects.get(id=id)
       student.IsDelete=True;
       student.save();
       return redirect('IRDCleranceList')   
   
# For Showing Pdf View Of Pay Master  
def IRDClerance_pdf_view(request):
     id = request.GET["id"]
     template_path = "IRD/irdcleranceformviewlist.html"
    # NileLogo=MasterAttribute.NileLogo
     get_data =IRD_Clerance.objects.get(id=id) 
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
   
   