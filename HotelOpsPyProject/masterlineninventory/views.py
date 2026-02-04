from django.shortcuts import render
from django.contrib.auth.models import Group
from .models import *
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from . import forms
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect

# For Showing Home View
def home_view(request):
    return render(request,'linen/index.html')

# For Registering The New Linen Inventory form
def LinenInventorySheet(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    DbItemMaster = Linen_Item_Master.objects.all()
    LinenInventoryForm=forms.LinenInventoryForm()
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID":OrganizationID,"UserID":UserID}

    mydict={'LinenInventoryForm':LinenInventoryForm,'DbItemMaster':DbItemMaster,'d':d}
    if request.method=='POST':
        # userForm=forms.DoctorUserForm(request.POST)
        LinenInventoryForm=forms.LinenInventoryForm(request.POST,request.FILES)
        if LinenInventoryForm.is_valid():
         
            lineninventoryform=LinenInventoryForm.save(commit=False)
            # doctor.user=user
            cs=lineninventoryform.save()

            TotalItem = int((request.POST["TotalItem"]))
            for i in  range (TotalItem):
                # print(Totalitem)
                ItemID = request.POST["ItemID_"+str(i)]
                Laundry = request.POST["Laundry_"+str(i)]
                Linen_Room = request.POST["Linen_Room_"+str(i)]
                Stores = request.POST["Stores_"+str(i)]
                Missing = request.POST["Missing_"+str(i)]
                Total = request.POST["Total_"+str(i)]
                # ReceivedBy = request.POST["ReceivedBy_"+str(i)]
                Linen_Item_Details.objects.create(
                    Laundry=Laundry,
                    Linen_Room=Linen_Room,
                    Stores=Stores,
                    Missing=Missing,
                    Total=Total,
                    # ReceivedBy=ReceivedBy,
                    Linen_Item_Master_id=ItemID,
                    Linen_Inventory_Sheet_id=LinenInventoryForm.instance.id,
                )

            
            return HttpResponseRedirect('masterlinenlist')
   
        
    return render(request,'linen/lineninventoryform.html',context=mydict) 

#For Showing List   
def MasterLinenInventoryList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    #for fetching all data from table
    OrganizationID =request.session["OrganizationID"]
    set_data = Linen_Inventory_Sheet.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
    return render(request,"linen/lineninventorylist.html",{'key1':set_data})


#For Edit the Data List
def LinenInventoryEditList(request):
    
       id = request.GET["id"]
       
       get_data = Linen_Inventory_Sheet.objects.get(id=id)
       
       DbItemMaster = Linen_Item_Master.objects.all()
       DbItemMaster = Linen_Item_Details.objects.filter(Linen_Inventory_Sheet_id=id).select_related('Linen_Item_Master')
    #    DbItemMaster = Uniform_Item_detail.objects.filter(Uniform_Inventory_Sheet_id=id).select_related('Uniform_Item_Master')
       
       LinenInventoryForm=forms.LinenInventoryForm()
     
       mydict={'LinenInventoryForm':LinenInventoryForm,'Ed':get_data,'DbItemMaster':DbItemMaster}
       mydict['form']= get_data
       
       return render(request,"linen/lineninventoryedit.html",context=mydict)
   
   
#For Updating Linen Inventory Data
def UpdateLinenInventoryData(request):
        # print(request)
        # print(id)
        id = request.POST["ID"]
        LinenInventoryForm = Linen_Inventory_Sheet.objects.get(id=id)
          
        From = request.POST["From"]
        LinenInventoryForm.From = From
        
        To = request.POST["To"]
        LinenInventoryForm.To = To
        
        LinenInventoryForm.save()
        
        
        TotalItem = int((request.POST["TotalItem"]))
        for i in  range (TotalItem):
               
                IDs = request.POST["ID_"+str(i)]
                # print(IDs)
                ItemID = request.POST["ItemID_"+str(i)]
                Laundry = request.POST["Laundry_"+str(i)]
                Linen_Room = request.POST["Linen_Room_"+str(i)]
                Stores = request.POST["Stores_"+str(i)]
                Missing = request.POST["Missing_"+str(i)]
                Total = request.POST["Total_"+str(i)]
                cd = Linen_Item_Details.objects.get(id=IDs)
                cd.Laundry=Laundry
                cd.Linen_Room=Linen_Room
                cd.Stores=Stores
                cd.Missing=Missing
                cd.Total=Total
                cd.save()
                
                # clearnce_formdetails.objects.create(
                #     ReturnedTo=ReturnReturnedTo,
                #     ReceivedBy=ReceivedBy,
                #     Clerance_Item_Master_id=ItemID,
                #     clearnce_form_id=id,
                # )

        return redirect('masterlinenlist')

#For Deleting The Cake Order Data
def DeleteLinenInventoryData(request):
       id = request.GET["id"]
  
       Linen = Linen_Inventory_Sheet.objects.get(id=id)
       Linen.IsDelete=True;
       Linen.save();
       return redirect('masterlinenlist')
   
   
# For Showing Your Order Page
def LinenInventoryViewData(request):
    
       id = request.GET["id"]
  
       get_data = Linen_Inventory_Sheet.objects.get(id=id)
        
       DbItemMaster = Linen_Item_Master.objects.all()
       
       DbItemMaster = Linen_Item_Details.objects.filter(Linen_Inventory_Sheet_id=id).select_related('Linen_Item_Master')
  
       LinenInventoryForm=forms.LinenInventoryForm()
     
       mydict={'LinenInventoryForm':LinenInventoryForm,'Ed':get_data,'DbItemMaster':DbItemMaster}
       
       return render(request,"linen/lineninventoryview.html",context=mydict)
   
   
# For Showing List Of Linen Item Master 
def ItemMasterList(request):
    #for fetching all data from table
    set_data = Linen_Item_Master.objects.all()
    print(set_data)
    return render(request,"linen/linenitemmasterlist.html",{'key2':set_data})


# # For Showing Pdf View Of Pay Master  
# def LinenInventory_pdf_view(request):
    
#      id = request.GET["id"]
    
#      template_path = "pay/PayMasterViewList.html"
#     # NileLogo=MasterAttribute.NileLogo
#      get_data =Pay_Master.objects.get(id=id)
    
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


