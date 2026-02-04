from io import BytesIO
from django.shortcuts import render
from django.contrib.auth.models import Group
from .models import *
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from . import forms
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from xhtml2pdf import pisa
from django.template.loader import get_template
from scantybaggage import link_callback 
from django.views.decorators.csrf import csrf_exempt

# For Showing Home View
def home_view(request):
    return render(request,'form/index.html')



# For Registering The New Clerance Form

def cleranceformAPI(request):
    
    # if 'OrganizationID' not in request.session:
    #     return redirect(MasterAttribute.Host)
    # else:
    #     print("Show Page Session")
    
    DbItemMaster = Clerance_Item_Master.objects.all()
    ClearanceForm=forms.ClearanceForm()
    
    OrganizationID =request.GET["O"]
    UserID =str(request.GET["U"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}

    mydict={'ClearanceForm':ClearanceForm,'DbItemMaster':DbItemMaster,'d':d}
    if request.method=='POST':
        # userForm=forms.DoctorUserForm(request.POST)
        ClearanceForm=forms.ClearanceForm(request.POST,request.FILES)
        if ClearanceForm.is_valid() or 1==1:
         
            cleranceform=ClearanceForm.save(commit=False)
            # doctor.user=user
            cs=cleranceform.save()

            TotalItem = int((request.POST["TotalItem"]))
            for i in  range (TotalItem):
                ItemID = request.POST["ItemID_"+str(i)]
                ReturnReturnedTo = request.POST["ReturnedTo_"+str(i)]
                ReceivedBy = request.POST["ReceivedBy_"+str(i)]
                clearnce_formdetails.objects.create(
                    ReturnedTo=ReturnReturnedTo,
                    ReceivedBy=ReceivedBy,
                    Clerance_Item_Master_id=ItemID,
                    clearnce_form_id=ClearanceForm.instance.id,
                )
            e = request.GET.get('E', "")
            if e!='':
                EC = request.GET.get('EC', "")
                O = request.GET.get('O', "")
                return redirect(MasterAttribute.CurrentHost+"/HR/Home/EmpProfile?E="+e+"&Q=clearanceform&EC="+EC+"&O="+O+"")
            return HttpResponseRedirect('cleranceformlist')
   
        
    return render(request,'form/cleranceformAPI.html',context=mydict) 


# For Registering The New Clerance Form
def cleranceform(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    DbItemMaster = Clerance_Item_Master.objects.all()
    ClearanceForm=forms.ClearanceForm()
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}

    mydict={'ClearanceForm':ClearanceForm,'DbItemMaster':DbItemMaster,'d':d}
    if request.method=='POST':
        # userForm=forms.DoctorUserForm(request.POST)
        ClearanceForm=forms.ClearanceForm(request.POST,request.FILES)
        if ClearanceForm.is_valid():
         
            cleranceform=ClearanceForm.save(commit=False)
            # doctor.user=user
            cs=cleranceform.save()

            TotalItem = int((request.POST["TotalItem"]))
            for i in  range (TotalItem):
                ItemID = request.POST["ItemID_"+str(i)]
                ReturnReturnedTo = request.POST["ReturnedTo_"+str(i)]
                ReceivedBy = request.POST["ReceivedBy_"+str(i)]
                clearnce_formdetails.objects.create(
                    ReturnedTo=ReturnReturnedTo,
                    ReceivedBy=ReceivedBy,
                    Clerance_Item_Master_id=ItemID,
                    clearnce_form_id=ClearanceForm.instance.id,
                )

            
            return HttpResponseRedirect('cleranceformlist')
   
        
    return render(request,'form/cleranceform.html',context=mydict) 

#For Showing List   
def cleranceformlist(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    #for fetching all data from table
    OrganizationID =request.session["OrganizationID"]
    set_data = clearnce_form.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
    return render(request,"form/cleranceformlist.html",{'key1':set_data})

#For Edit the Data List
def CleranceFormEditList(request):
    
       id = request.GET["id"]
       
       get_data = clearnce_form.objects.get(id=id)
       
    #    DbItemMaster = Clerance_Item_Master.objects.all()
       DbItemMaster = clearnce_formdetails.objects.filter(clearnce_form_id=id).select_related('Clerance_Item_Master')
       
       ClearanceForm=forms.ClearanceForm()
     
       mydict={'ClearanceForm':ClearanceForm,'Ed':get_data,'DbItemMaster':DbItemMaster}
       mydict['form']= get_data
       
       return render(request,"form/cleranceformedit.html",context=mydict)
   
#For Updating the Casual Manpower Requisition Data
def UpdateCleranceForm(request):
        # print(request)
        # print(id)
        id = request.POST["ID"]
        ClearanceForm = clearnce_form.objects.get(id=id)
          
        Name = request.POST["Name"]
        ClearanceForm.Name = Name
        
        Separation_Date = request.POST["Separation_Date"]
        ClearanceForm.Separation_Date = Separation_Date
        
        Position = request.POST["Position"]
        ClearanceForm.Position = Position
        
        Finishing_Time = request.POST["Finishing_Time"]
        ClearanceForm.Finishing_Time = Finishing_Time
        
        Resignation_Letter = request.POST["Resignation_Letter"]
        ClearanceForm.Resignation_Letter = Resignation_Letter
        print(Resignation_Letter)
        
        Acc_Of_Resign = request.POST["Acc_Of_Resign"]
        ClearanceForm.Acc_Of_Resign = Acc_Of_Resign
        
        Notice_Period_Served = request.POST["Notice_Period_Served"]
        ClearanceForm.Notice_Period_Served = Notice_Period_Served
        
        Notice_Period_Waived_Off = request.POST["Notice_Period_Waived_Off"]
        ClearanceForm.Notice_Period_Waived_Off = Notice_Period_Waived_Off
        
        Exit_Interview_By_Hr = request.POST["Exit_Interview_By_Hr"]
        ClearanceForm.Exit_Interview_By_Hr = Exit_Interview_By_Hr
        
        Full_And_Final_Settlement = request.POST["Full_And_Final_Settlement"]
        ClearanceForm.Full_And_Final_Settlement = Full_And_Final_Settlement
        ClearanceForm.save()
        
        

        TotalItem = int((request.POST["TotalItem"]))
        for i in  range (TotalItem):
               
                IDs = request.POST["ID_"+str(i)]
                print(IDs)
                ItemID = request.POST["ItemID_"+str(i)]
                ReturnReturnedTo = request.POST["ReturnedTo_"+str(i)]
                print(ReturnReturnedTo)
                ReceivedBy = request.POST["ReceivedBy_"+str(i)]
                print(ReceivedBy)
                cd = clearnce_formdetails.objects.get(id=IDs)
                cd.ReturnedTo=ReturnReturnedTo
                cd.ReceivedBy=ReceivedBy
                cd.save()
                
             
        return redirect('cleranceformlist')
   
   



#For Deleting The Cake Order Data
def CleranceFormDeleteData(request):
       id = request.GET["id"]
  
       clerance = clearnce_form.objects.get(id=id)
       clerance.IsDelete=True;
       clerance.save();
       return redirect('cleranceformlist')
   

   
# For Showing List Of Linen Item Master 
def cleranceitemmasterlist(request):
    #for fetching all data from table
    set_data = Clerance_Item_Master.objects.all()
    print(set_data)
    return render(request,"form/cleranceitemmasterlist.html",{'key2':set_data})


# For Showing Pdf View Of Clerance Form 
def CleranceForm_pdf_view(request):
    
     id = request.GET["id"]
    
     template_path = "form/cleranceformview.html"
    # NileLogo=MasterAttribute.NileLogo
     get_data =clearnce_form.objects.get(id=id)
    
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

