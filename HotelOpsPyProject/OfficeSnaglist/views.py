from io import BytesIO
from django.shortcuts import render
from .models import *
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from . import forms
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from xhtml2pdf import pisa
from django.template.loader import get_template
from scantybaggage import link_callback 

# For Showing Home View
def home_view(request):
    return render(request,'Snag/index.html')

# For Registering The New Clerance Form
def OfficeSnagRegistration(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    DbItemMaster = Snag_Category_Master.objects.all()
    
    OfficeSnagForm=forms.OfficeSnagForm()
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}

    mydict={'OfficeSnagForm':OfficeSnagForm,'DbItemMaster':DbItemMaster,'d':d}
    if request.method=='POST':
        # userForm=forms.DoctorUserForm(request.POST)
        OfficeSnagForm=forms.OfficeSnagForm(request.POST,request.FILES)
        
        if OfficeSnagForm.is_valid():
         
            Office=OfficeSnagForm.save(commit=False)
            # doctor.user=user
            Office=Office.save()

            TotalItem = int((request.POST["TotalItem"]))
            for i in  range (TotalItem):
                ItemID = request.POST["ItemID_"+str(i)]
                Status = request.POST["Status_"+str(i)]
                Remarks = request.POST["Remarks_"+str(i)]
                
                Snag_Category_details.objects.create(
                    Status=Status,
                    Remarks=Remarks,
                   
                    Snag_Category_Master_id=ItemID,
                    Office_Snag_Registration_Form_id=OfficeSnagForm.instance.id,
                 )

            
            return HttpResponseRedirect('OfficeSnagList')
   
        
    return render(request,'Snag/OfficeSnagRegistration.html',context=mydict) 

#For Showing List   
def OfficeSnagList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    #for fetching all data from table
    OrganizationID =request.session["OrganizationID"]
    
    set_data = Office_Snag_Registration_Form.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
    
    return render(request,"Snag/OfficeSnaglist.html",{'key1':set_data})

#For Edit the Data List
def SnagEditList(request):
    
       id = request.GET["id"]
       
       get_data = Office_Snag_Registration_Form.objects.get(id=id)
       
    #    DbItemMaster = Clerance_Item_Master.objects.all()
       DbItemMaster = Snag_Category_details.objects.filter(Office_Snag_Registration_Form_id=id).select_related('Snag_Category_Master')
       
       OfficeSnagForm=forms.OfficeSnagForm()
     
       mydict={'OfficeSnagForm':OfficeSnagForm,'Ed':get_data,'DbItemMaster':DbItemMaster}
       mydict['form']= get_data
       
       return render(request,"Snag/officeSnageditlist.html",context=mydict)
   
#For Updating the Casual Manpower Requisition Data
def UpdateOfficeSnagForm(request):
        # print(request)
        # print(id)
        id = request.POST["ID"]
        OfficeSnagForm = Office_Snag_Registration_Form.objects.get(id=id)
          
        Area = request.POST["Area"]
        OfficeSnagForm.Area = Area
        
        Date = request.POST["Date"]
        OfficeSnagForm.Date = Date
        
        
        
        OfficeSnagForm.save()
        
        

        TotalItem = int((request.POST["TotalItem"]))
        for i in  range (TotalItem):
               
                IDs = request.POST["ID_"+str(i)]
                print(IDs)
                ItemID = request.POST["ItemID_"+str(i)]
                ReturnStatus = request.POST["Status_"+str(i)]
                ReturnRemarks = request.POST["Remarks_"+str(i)]
                # print(ReturnHabits)
                cd = Snag_Category_details.objects.get(id=IDs)
                cd.Status=ReturnStatus
                cd.Remaks=ReturnRemarks
                cd.save()
                
             
        return redirect('OfficeSnagList')
   
   



#For Deleting The Cake Order Data
def OfficeSnagDeleteList(request):
       id = request.GET["id"]
  
       officesnag = Office_Snag_Registration_Form.objects.get(id=id)
       officesnag.IsDelete=True;
       officesnag.save();
       return redirect('OfficeSnagList')
   

# For Showing Pdf View Of Clerance Form 
def OfficeSnagForm_pdf_view(request):
    
     id = request.GET["id"]
    
     template_path = "Snag/OfficeSnagViewlist.html"
    # NileLogo=MasterAttribute.NileLogo
     get_data =Office_Snag_Registration_Form.objects.get(id=id)
    
    # #    DbItemMaster = Clerance_Item_Master.objects.all()
    #  DbItemMaster = Snag_Category_details.objects.filter(Office_Snag_Registration_Form_id=id).select_related('Snag_Category_Master')
       
    #  OfficeSnagForm=forms.OfficeSnagForm()
     
     mydict={'Ed':get_data}
    #  mydict['form']= get_data
    #  print(DbItemMaster)

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
