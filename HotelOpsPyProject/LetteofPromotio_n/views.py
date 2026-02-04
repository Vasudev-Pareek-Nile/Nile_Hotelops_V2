from django.shortcuts import render,redirect
from .models import *
# Create your views here.
from .forms import EmpDetailsForm 
from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail
import io ,os
from django.shortcuts import render

# Azure.
from hashlib import new
from pathlib import Path
import mimetypes
from django.contrib import messages
from .azure import upload_file_to_blob,ALLOWED_EXTENTIONS,download_blob
# Azure.

from io import BytesIO
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse, HttpResponseRedirect,Http404
from requests import Session, post
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from . import forms
from django.contrib.auth.models import Group
from .models import PromotionLetter,PromotionLetterDeletedFileofEmployee,PromotionLetterEmployeeDetail

from xhtml2pdf import pisa
from django.template.loader import get_template
from scantybaggage import link_callback
from django.db.models import Count



def homeview(request):

   
    return render(request,'letterpl/index.html')

# For Adding Emp Details
def entryEmp(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")


    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
   
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    editor = PromotionLetter.objects.filter(user = 1 )
    
    
    form = EmpDetailsForm(initial={'OrganizationID':OrganizationID,'CreatedBy':UserID,'data':editor[0].data})
    
    #form.cleaned_data["OrganizationID"]=OrganizationID
    # form["OrganizationID"]=OrganizationID
    # form["CreatedBy"]=UserID
    context= {'form':form,'d':d}
    if request.method == "POST":
        form = EmpDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            e = request.GET.get('E', "")
            if e!='':
                EC = request.GET.get('EC', "")
                O = request.GET.get('O', "")
                od =OrganizationDetail(OrganizationID)
                DomainCode=od.get_OrganizationDomainCode()
                newd = MasterAttribute.CurrentHost.replace("http://hotelops.in","http://"+DomainCode+".hotelops.in")
                return redirect(newd+"/HR/Home/EmpProfile?E="+e+"&Q=empworkexp&EC="+EC+"&O="+O+"")
            return  redirect('emplistpl')
    return  render(request,"letterpl/entryemp.html",context)

# def emplist(request):
    
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
#         OrganizationID =request.session["OrganizationID"]
#     empdetails = PromotionLetterEmployeeDetail.objects.filter(IsDelete=False,OrganizationID=OrganizationID).order_by('-CreatedDateTime','-ModifyDateTime').values()
    
#     context  = { 'empdetails':empdetails}
#     return render(request,"letterpl/emplist.html",context)




import requests
def emplist(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        OrganizationID =request.session["OrganizationID"]

    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
        'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = "http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID=" + str(OrganizationID)

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")   
    I = request.GET.get('I',OrganizationID)
   
    empdetails = PromotionLetterEmployeeDetail.objects.filter(IsDelete=False,OrganizationID=I).order_by('-CreatedDateTime','-ModifyDateTime').values()
    
    context  = { 'empdetails':empdetails,'memOrg':memOrg,'I':I}
    return render(request,"letterpl/emplist.html",context)









# For generate_appointment_letter
def generate_Letter_of_promotion(request):
     id = request.GET["id"]

     template_path = "letterpl/plview.html"
    # NileLogo=MasterAttribute.NileLogo
     get_data =PromotionLetterEmployeeDetail.objects.get(id=id)
     get_data.data=get_data.data.replace("@@emp_code@@",str(get_data.emp_code))
     get_data.data=get_data.data.replace("@@date_of_promtion@@",str(get_data.date_of_promtion.strftime('%d/%m/%y')))
     
     get_data.data=get_data.data.replace("@@prefix@@",get_data.prefix)
     get_data.data=get_data.data.replace("@@firstname@@",get_data.first_name)
     get_data.data=get_data.data.replace("@@lastname@@",get_data.last_name)
     
     get_data.data=get_data.data.replace("@@Designation@@",get_data.designation)
     get_data.data=get_data.data.replace("@@Promotiondesignation@@",get_data.Promotiondesignation)
     
     
     get_data.data=get_data.data.replace("@@Department@@",get_data.department)
     get_data.data=get_data.data.replace("@@general_manager_name@@",get_data.general_manager_name)
     

    
     
     
      
    #  print(name)
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


# For generate_letter_of_intent

def empupdate(request,pk):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID =request.session["OrganizationID"]
    data =PromotionLetterEmployeeDetail.objects.get(id=pk)
    form = EmpDetailsForm(instance=data)
    print(data)
    if request.method == "POST":
          form = EmpDetailsForm(request.POST,instance=data)
          if form.is_valid():
              form.save()
              e = request.GET.get('E', "")
              if e!='':
                  EC = request.GET.get('EC', "")
                  O = request.GET.get('O', "")
                  od =OrganizationDetail(OrganizationID)
                  DomainCode=od.get_OrganizationDomainCode()
                  newd = MasterAttribute.CurrentHost.replace("http://hotelops.in","http://"+DomainCode+".hotelops.in")
                  return redirect(newd+"/HR/Home/EmpProfile?E="+e+"&Q=empworkexp&EC="+EC+"&O="+O+"")
              return redirect('emplistpl')
    context = {'form':form}
    return render(request,"letterpl/empupdate.html",context)

def empdelete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID =request.session["OrganizationID"]
    id = request.GET["id"]
    empdetail = PromotionLetterEmployeeDetail.objects.get(id=id)
    empdetail.IsDelete=True
    empdetail.save()
    e = request.GET.get('E', "")
    if e!='':
        EC = request.GET.get('EC', "")
        O = request.GET.get('O', "")
        od =OrganizationDetail(OrganizationID)
        DomainCode=od.get_OrganizationDomainCode()
        newd = MasterAttribute.CurrentHost.replace("http://hotelops.in","http://"+DomainCode+".hotelops.in")
        return redirect(newd+"/HR/Home/EmpProfile?E="+e+"&Q=empworkexp&EC="+EC+"&O="+O+"")
    return redirect('emplistpl')



def upload_file(request,id):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID =request.session["OrganizationID"]
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix

        new_file = upload_file_to_blob(file,id)
        if not new_file:
            messages.warning(request, f"{ext} not allowed only accept {', '.join(ext for ext in ALLOWED_EXTENTIONS)} ")
            return render(request, "letterpl/upload_file.html", {}) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()
        messages.success(request, f"{file.name} was successfully uploaded")
        e = request.GET.get('E', "")
        if e!='':
            EC = request.GET.get('EC', "")
            O = request.GET.get('O', "")
            od =OrganizationDetail(OrganizationID)
            DomainCode=od.get_OrganizationDomainCode()
            newd = MasterAttribute.CurrentHost.replace("http://hotelops.in","http://"+DomainCode+".hotelops.in")
            return redirect(newd+"/HR/Home/EmpProfile?E="+e+"&Q=empworkexp&EC="+EC+"&O="+O+"")
        return redirect('emplistpl')
    
    
    return render(request, "letterpl/upload_file.html")


def download_file(request, id):
    file = PromotionLetterEmployeeDetail.objects.get(pk=id)
    file_id = file.file_id
    file_name = file.file_name
    
    file_type, _ = mimetypes.guess_type(file_id)
    
    
    blob_name = file_id
    blob_content = download_blob(blob_name)
    
    if blob_content:
        response = HttpResponse(blob_content.readall(), content_type=file_type)
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        messages.success(request, f"{file_name} was successfully downloaded")
        return response
    return Http404


def repalce_file(request, id):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID =request.session["OrganizationID"]
    file = PromotionLetterEmployeeDetail.objects.get(pk=id)
    file_id = file.file_id
    file_name = file.file_name
    EmployeeDetail = PromotionLetterEmployeeDetail.objects.get(pk=id)
    
    
    deletefile = PromotionLetterDeletedFileofEmployee.objects.create(PromotionLetterEmployeeDetail= EmployeeDetail,file_id = file_id,file_name = file_name)
    
    
    
        
          
    file = PromotionLetterEmployeeDetail.objects.get(pk=id)
    file.file_name = None
    file.file_id = None
    file.save()
    e = request.GET.get('E', "")
    if e!='':
        EC = request.GET.get('EC', "")
        O = request.GET.get('O', "")
        od =OrganizationDetail(OrganizationID)
        DomainCode=od.get_OrganizationDomainCode()
        newd = MasterAttribute.CurrentHost.replace("http://hotelops.in","http://"+DomainCode+".hotelops.in")
        return redirect(newd+"/HR/Home/EmpProfile?E="+e+"&Q=empworkexp&EC="+EC+"&O="+O+"")
    messages.success(request, f"{file_name} was successfully deleted")
    return redirect('emplistpl')    
    