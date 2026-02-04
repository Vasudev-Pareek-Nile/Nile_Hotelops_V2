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

# For Showing Home View
def home_view(request):
    return render(request,'hlp/index.html')

# For Registering The New Uniform Inventory form
def DailyHlpRegistrationForm(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    DbItemMaster = Category_Item_Master.objects.select_related("ItemID")
    
    DailyHlpReportForm=forms.DailyHlpReportForm()
    
    OrganizationID =request.session["OrganizationID"]
    
    UserID =str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}

    mydict={'DailyHlpReportForm':DailyHlpReportForm,'DbItemMaster':DbItemMaster,'d':d}
    
    if request.method=='POST':
        # userForm=forms.DoctorUserForm(request.POST)
        DailyHlpReportForm=forms.DailyHlpReportForm(request.POST,request.FILES)
        if DailyHlpReportForm.is_valid():
         
            DailyHlpReportForm=DailyHlpReportForm.save(commit=False)
            # doctor.user=user
            cs=DailyHlpReportForm.save()

            TotalItem = int((request.POST["TotalItem"]))
            for i in  range (TotalItem):
                # print(Totalitem)
                ItemID = request.POST["ItemID_"+str(i)]
                Current_Year = request.POST["Current_Year_"+str(i)]
                Last_Year = request.POST["Last_Year_"+str(i)]
                Amount = request.POST["Amount_"+str(i)]
                # ReceivedBy = request.POST["ReceivedBy_"+str(i)]
                Category_Item_detail.objects.create(
                    Current_Year=Current_Year,
                    Last_Year=Last_Year,
                    Amount=Amount,
                    # ReceivedBy=ReceivedBy,
                    Category_Item_Master_id = ItemID,
                    Dailyhlpreportform_id = DailyHlpReportForm.instance.id,
                )

            
            return HttpResponseRedirect('DailyHlpList')
   
        
    return render(request,'hlp/Dailyhlpreportform.html',context=mydict) 

#For Showing List   
def DailyHlpList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    #for fetching all data from table
    OrganizationID =request.session["OrganizationID"]
    set_data = Dailyhlpreportform.objects.filter(OrganizationID=OrganizationID)
    return render(request,"hlp/Dailyhlpreportlist.html",{'key1':set_data})

# #For Edit the Data List
# def UniformInventoryEditList(request):
    
#        id = request.GET["id"]
       
#        get_data = Uniform_Inventory_Sheet.objects.get(id=id)
       
#        DbItemMaster = Uniform_Item_Master.objects.all()
#        DbItemMaster = Uniform_Item_detail.objects.filter(Uniform_Inventory_Sheet_id=id).select_related('Uniform_Item_Master')
#     #    DbItemMaster = Uniform_Item_detail.objects.filter(Uniform_Inventory_Sheet_id=id).select_related('Uniform_Item_Master')
       
#        UniformInventoryForm=forms.UniformInventoryForm()
     
#        mydict={'UniformInventoryForm':UniformInventoryForm,'Ed':get_data,'DbItemMaster':DbItemMaster}
#        mydict['form']= get_data
       
#        return render(request,"uniform/uniforminventoryedit.html",context=mydict)
   
# #For Updating the Casual Manpower Requisition Data
# def UpdateUniformInventorylist(request):
#         # print(request)
#         # print(id)
#         id = request.POST["ID"]
#         UniformInventoryForm = Uniform_Inventory_Sheet.objects.get(id=id)
          
#         From = request.POST["From"]
#         UniformInventoryForm.From = From
        
#         To = request.POST["To"]
#         UniformInventoryForm.To = To
        
#         UniformInventoryForm.save()
        
        
#         TotalItem = int((request.POST["TotalItem"]))
#         for i in  range (TotalItem):
               
#                 IDs = request.POST["ID_"+str(i)]
#                 print(IDs)
#                 ItemID = request.POST["ItemID_"+str(i)]
#                 Fresh = request.POST["Fresh_"+str(i)]
#                 Soiled = request.POST["Soiled_"+str(i)]
#                 Total = request.POST["Total_"+str(i)]
#                 cd = Uniform_Item_detail.objects.get(id=IDs)
#                 cd.Fresh=Fresh
#                 cd.Soiled=Soiled
#                 cd.Total=Total
#                 cd.save()
                
               

#         return redirect('list')
   
# #For Deleting The Cake Order Data
# def DeleteUniformInventory(request):
#        id = request.GET["id"]
  
#        student = Uniform_Inventory_Sheet.objects.get(id=id)
#        student.delete()
#        return redirect('list')


# # # For Showing Your Order Page
# # def UniformInventoryViewData(request):
    
# #        id = request.GET["id"]
  
# #        get_data = Uniform_Inventory_Sheet.objects.get(id=id)
        
# #        DbItemMaster = Uniform_Item_Master.objects.all()
       
# #        DbItemMaster = Uniform_Item_detail.objects.filter(Uniform_Inventory_Sheet_id=id).select_related('Uniform_Item_Master')
  
# #        UniformInventoryForm=forms.UniformInventoryForm()
     
# #        mydict={'UniformInventoryForm':UniformInventoryForm,'Ed':get_data,'DbItemMaster':DbItemMaster}
       
# #        return render(request,"uniform/uniforminventoryview.html",context=mydict)
   
   

   
# # For Showing List Of Linen Item Master 
# def UniformItemMasterlist(request):
#     #for fetching all data from table
#     set_data = Uniform_Item_Master.objects.all()
#     print(set_data)
#     return render(request,"uniform/uniformitemmasterlist.html",{'key2':set_data})


# # For Showing Pdf View Of Uniform Inventory Sheet 
# def UniformInventory_pdf_view(request):
    
#      id = request.GET["id"]
    
#      template_path = "uniform/uniforminventoryview.html"
#     # NileLogo=MasterAttribute.NileLogo
#      get_data =Uniform_Inventory_Sheet.objects.get(id=id)
    
#     #  ScantyBaggageForm=forms.ScantyBaggageForm()
     
#      mydict={'Ed':get_data}

#     # context = {'myvar': 'this is your template context','p':varM}
    
#     # Create a Django response object, and specify content_type as pdf
#      response = HttpResponse(content_type='application/pdf')
#      response['Content-Disposition'] = 'filename="report gcc club.pdf"'
#     # find the template and render it.
#      template = get_template(template_path)
#      html = template.render(mydict)

#     # create a pdf
#      pisa_status = pisa.CreatePDF(
#         html, dest=response, link_callback=link_callback)
#     # if error then show some funny view
#      if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#      return response  