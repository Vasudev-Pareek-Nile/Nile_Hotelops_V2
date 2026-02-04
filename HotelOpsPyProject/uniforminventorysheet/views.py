from django.shortcuts import render
from django.contrib.auth.models import Group
from .models import *
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from . import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from xhtml2pdf import pisa
from django.template.loader import get_template
from scantybaggage import link_callback

# For Showing Home View


def home_view(request):
    return render(request, 'uniform/index.html')

# For Registering The New Uniform Inventory form


def UniformInventorySheet(request):

    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    DbItemMaster = Uniform_Item_Master.objects.all()
    UniformInventoryForm = forms.UniformInventoryForm()
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    print((UserID))
    d = {"OrganizationID": OrganizationID, "UserID": UserID}

    mydict = {'UniformInventoryForm': UniformInventoryForm,
              'DbItemMaster': DbItemMaster, 'd': d}
    if request.method == 'POST':
        # userForm=forms.DoctorUserForm(request.POST)
        UniformInventoryForm = forms.UniformInventoryForm(
            request.POST, request.FILES)
        if UniformInventoryForm.is_valid():

            uniforminventoryform = UniformInventoryForm.save(commit=False)
            # doctor.user=user
            cs = uniforminventoryform.save()

            TotalItem = int((request.POST["TotalItem"]))
            for i in range(TotalItem):
                # print(Totalitem)
                ItemID = request.POST["ItemID_"+str(i)]
                Fresh = request.POST["Fresh_"+str(i)]
                Soiled = request.POST["Soiled_"+str(i)]
                Total = request.POST["Total_"+str(i)]
                # ReceivedBy = request.POST["ReceivedBy_"+str(i)]
                Uniform_Item_detail.objects.create(
                    Fresh=Fresh,
                    Soiled=Soiled,
                    Total=Total,
                    # ReceivedBy=ReceivedBy,
                    Uniform_Item_Master_id=ItemID,
                    Uniform_Inventory_Sheet_id=UniformInventoryForm.instance.id,
                )

            return HttpResponseRedirect('UniformInventoryList')

    return render(request, 'uniform/uniforminventoryform.html', context=mydict)

# For Showing List


def UniformInventoryList(request):

    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    # for fetching all data from table
    OrganizationID = request.session["OrganizationID"]
    set_data = Uniform_Inventory_Sheet.objects.filter(
        OrganizationID=OrganizationID, IsDelete=False)
    return render(request, "uniform/uniforminventorylist.html", {'key1': set_data})

# For Edit the Data List


def UniformInventoryEditList(request):

    id = request.GET["id"]

    get_data = Uniform_Inventory_Sheet.objects.get(id=id)

    DbItemMaster = Uniform_Item_Master.objects.all()
    DbItemMaster = Uniform_Item_detail.objects.filter(
        Uniform_Inventory_Sheet_id=id).select_related('Uniform_Item_Master')
    #    DbItemMaster = Uniform_Item_detail.objects.filter(Uniform_Inventory_Sheet_id=id).select_related('Uniform_Item_Master')

    UniformInventoryForm = forms.UniformInventoryForm()

    mydict = {'UniformInventoryForm': UniformInventoryForm,
              'Ed': get_data, 'DbItemMaster': DbItemMaster}
    mydict['form'] = get_data

    return render(request, "uniform/uniforminventoryedit.html", context=mydict)

# For Updating the Casual Manpower Requisition Data


def UpdateUniformInventorylist(request):
    # print(request)
    # print(id)
    id = request.POST["ID"]
    UniformInventoryForm = Uniform_Inventory_Sheet.objects.get(id=id)

    From = request.POST["From"]
    UniformInventoryForm.From = From

    To = request.POST["To"]
    UniformInventoryForm.To = To

    UniformInventoryForm.save()

    TotalItem = int((request.POST["TotalItem"]))
    for i in range(TotalItem):

        IDs = request.POST["ID_"+str(i)]
        print(IDs)
        ItemID = request.POST["ItemID_"+str(i)]
        Fresh = request.POST["Fresh_"+str(i)]
        Soiled = request.POST["Soiled_"+str(i)]
        Total = request.POST["Total_"+str(i)]
        cd = Uniform_Item_detail.objects.get(id=IDs)
        cd.Fresh = Fresh
        cd.Soiled = Soiled
        cd.Total = Total
        cd.save()

    return redirect('UniformInventoryList')

# For Deleting The Cake Order Data


def DeleteUniformInventory(request):
    id = request.GET["id"]

    uniform = Uniform_Inventory_Sheet.objects.get(id=id)
    uniform.IsDelete = True
    uniform.save()
    return redirect('UniformInventoryList')


# # For Showing Your Order Page
# def UniformInventoryViewData(request):

#        id = request.GET["id"]

#        get_data = Uniform_Inventory_Sheet.objects.get(id=id)

#        DbItemMaster = Uniform_Item_Master.objects.all()

#        DbItemMaster = Uniform_Item_detail.objects.filter(Uniform_Inventory_Sheet_id=id).select_related('Uniform_Item_Master')

#        UniformInventoryForm=forms.UniformInventoryForm()

#        mydict={'UniformInventoryForm':UniformInventoryForm,'Ed':get_data,'DbItemMaster':DbItemMaster}

#        return render(request,"uniform/uniforminventoryview.html",context=mydict)


# For Showing List Of Linen Item Master
def UniformItemMasterlist(request):
    # for fetching all data from table
    set_data = Uniform_Item_Master.objects.filter(IsDelete=False)
    print(set_data)
    return render(request, "uniform/uniformitemmasterlist.html", {'key2': set_data})


def DeleteUniformItemMaster(request):
    id = request.GET["id"]

    uniform = Uniform_Item_Master.objects.get(id=id)
    uniform.IsDelete = True
    uniform.save()
    return redirect('UniformItemMasterlist')


def UniformItemMasterNew(request):

    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    if request.method == 'POST':
        # userForm=forms.DoctorUserForm(request.POST)
        Itemid = request.POST["Itemid"]
        Item_Title_Name = request.POST["Item_Title_Name"]

        if int(Itemid) > 0:
            cs = Uniform_Item_Master.objects.get(id=Itemid)
            cs.Item_Title_Name = Item_Title_Name
            cs.save()
        else:
            cs = Uniform_Item_Master.objects.create(
                Item_Title_Name=Item_Title_Name)
            cs.save()
        return redirect('UniformItemMasterlist')
    DbItemMaster = [{"id": 0, "Item_Title_Name": ""}]
    if "id" in request.GET:
        id = request.GET["id"]
        DbItemMaster = Uniform_Item_Master.objects.filter(id=id)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    print((DbItemMaster))
    d = {"OrganizationID": OrganizationID, "UserID": UserID}

    mydict = {'DbItemMaster': DbItemMaster, 'd': d}
    return render(request, "uniform/UniformItemMasterNew.html", {'key2': mydict})


# For Showing Pdf View Of Uniform Inventory Sheet


def UniformInventory_pdf_view(request):

    id = request.GET["id"]

    template_path = "uniform/uniforminventoryview.html"
    # NileLogo=MasterAttribute.NileLogo
    get_data = Uniform_Inventory_Sheet.objects.get(id=id)

    #  ScantyBaggageForm=forms.ScantyBaggageForm()

    mydict = {'Ed': get_data}

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
