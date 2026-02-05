from django.shortcuts import render,redirect
from .models import *
# Create your views here.
from django.db.models import Subquery, OuterRef

import io ,os
from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail
from hashlib import new
from pathlib import Path
import mimetypes
from django.contrib import messages

from .azure import upload_file_to_blob,ALLOWED_EXTENTIONS,download_blob

from io import BytesIO
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse, HttpResponseRedirect,Http404
from requests import Session, post
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from . import forms
from django.contrib.auth.models import Group
from .models import LETTEROFCONFIRMATIONEmployeeDetail,LETTEROFCONFIRMATIONDeletedFileofEmployee,LETTEROFCONFIRMATION
from django.shortcuts import render,redirect
from xhtml2pdf import pisa
from django.template.loader import get_template
from scantybaggage import link_callback
from django.db.models import Count
from azure.storage.blob import BlobServiceClient

from .azure import upload_file_to_blob,ALLOWED_EXTENTIONS
from HumanResources.models import EmployeeWorkDetails,EmployeePersonalDetails

from dateutil.relativedelta import relativedelta
from HumanResources.views import ManagerNameandDesignation,HrManagerNameandDesignation,EmployeeDetailsData,HrNameOnTheBasisofDesignation,EmployeeNameOnTheBasisofDesignation
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from django.urls import reverse
from Manning_Guide.models import OnRollDesignationMaster
from LETTEROFAPPOINTMENT.models import LOALETTEROFAPPOINTMENTEmployeeDetail
from ProbationConfirmation.models import Emp_Confirmation_Master

# For Adding Emp Details
from app.views import Error
def entryEmp(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
          OrganizationID= OID
    UserID = str(request.session["UserID"])

    
    EmpCode  = request.GET.get('EC')
    EmpID  = request.GET.get('EmpID')
    if EmpID == 'None' or  EmpID == '':
            return Error(request, "Employee is not Found in Human Resources Data.")
        
   
    LOC_ID = request.GET.get('LOC_ID')
    Page = request.GET.get('Page')

    PC_ID = request.GET.get('ID')
    print("PC_ID = ",PC_ID)
    if PC_ID:
        PC  = Emp_Confirmation_Master.objects.filter(IsDelete=False,OrganizationID=OrganizationID,id=PC_ID).first()
            
    

    DepartmentName = request.GET.get('DepartmentName')
    
    
    # ManagerNames  = ManagerNameandDesignation(request,OrganizationID)
    # HRManagerNames  = HrManagerNameandDesignation(request,OrganizationID)



    ManagerNames =  EmployeeNameOnTheBasisofDesignation( DepartmentName,OrganizationID)
    HRManagerNames  = HrNameOnTheBasisofDesignation(OrganizationID)
 

    
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    Confirmationobj   = None
    if EmpCode is not None:
        date_of_appointment =  date.today()
        print("date_of_appointment=",date_of_appointment)
        DOA = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(emp_code=EmpCode, OrganizationID=OrganizationID, IsDelete=0).first()
        if DOA:
            date_of_appointment  = DOA.date_of_appointment
        date_of_confirmation = date_of_appointment + relativedelta(months=6)

        if LOC_ID is not None:
               Confirmationobj = LETTEROFCONFIRMATIONEmployeeDetail.objects.filter(id = LOC_ID,emp_code = EmpCode,OrganizationID = OrganizationID,IsDelete=False).first()


        if Confirmationobj is not None:
            DataFromConfirmationobj  = 'Confirmationobj'
           

        else:
            

            DataFromConfirmationobj  = 'ConfirmationobjHR'
            EmpDetails  = EmployeeDetailsData(EmpID,OrganizationID)
            if EmpDetails is None:
                    return Error(request, "Employee is not Found in Human Resources Data.")
    
          
           
         

            Confirmationobj  =   {
                                'emp_code' : EmpDetails.EmployeeCode,
                                'prefix' : EmpDetails.Prefix,
                                # 'first_name' : EmpDetails.FirstName + EmpDetails.MiddleName or '',
                                'first_name': (EmpDetails.FirstName + " " + EmpDetails.MiddleName) if EmpDetails.MiddleName else EmpDetails.FirstName,
 
                                'last_name' : EmpDetails.LastName,
                                
                               
                                'department' : EmpDetails.Department,
                                'designation' : EmpDetails.Designation,
                                'date_of_appointment':date_of_appointment ,
                                'date_of_confirmation':date_of_confirmation,


                                
                                
                               }
    if request.method == "POST":
                emp_code = request.POST['emp_code']
                prefix = request.POST['prefix']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                date_of_appointment  = request.POST['date_of_appointment']
                date_of_confirmation  = request.POST['date_of_confirmation']

                
                department = request.POST['department']
                designation = request.POST['designation']
                
            
                Issuing_manager_name = request.POST['Issuing_manager_name']
                Issuing_designation = request.POST['Issuing_designation']
                
                if DataFromConfirmationobj == "Confirmationobj" and LOC_ID:
                     
                       
                        Confirmationobj.emp_code = emp_code
                        Confirmationobj.prefix = prefix
                        Confirmationobj.first_name = first_name
                        Confirmationobj.last_name = last_name
                        Confirmationobj.department = department
                        Confirmationobj.designation = designation
                        Confirmationobj.date_of_appointment  = date_of_appointment
                        Confirmationobj.date_of_confirmation  = date_of_confirmation
                        Confirmationobj.Issuing_manager_name = Issuing_manager_name
                        Confirmationobj.Issuing_designation = Issuing_designation
                        Confirmationobj.ModifyBy  =  UserID    
                        
                        Confirmationobj.save()

                        

                else:
                   
                    Confirmationobj = LETTEROFCONFIRMATIONEmployeeDetail.objects.create(
                        emp_code=emp_code,
                        prefix=prefix,
                        first_name=first_name,
                        last_name=last_name,
                        department=department,
                        designation=designation,
                        date_of_appointment = date_of_appointment,
                        date_of_confirmation  = date_of_confirmation,
                        Issuing_manager_name=Issuing_manager_name,
                        Issuing_designation=Issuing_designation,
                        CreatedBy  = UserID,OrganizationID = OrganizationID
                     )
                     
                
                    if PC:
                        PC.LOC_ID =  Confirmationobj.id
                        PC.ModifyBy = UserID
                        PC.save()
                   
                    try:
                        employee_work_details = EmployeeWorkDetails.objects.get(
                            EmpID=EmpID, OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False)
                        employee_work_details.EmpStatus = "Confirmed"
                        employee_work_details.ModifyBy = UserID
                
                        employee_work_details.save()
                    except EmployeeWorkDetails.DoesNotExist:
                        print("EmployeeWorkDetails record not found.")
 
                if Page == "emplistcl" :
                     return redirect('emplistcl')
 
                if Page == "ListPC" :
                     return redirect('ListPC')
 

                Success = True        
                encrypted_id = encrypt_id(EmpID)
                url = reverse('ProbationConfirmation')  
                redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}"
                return redirect(redirect_url)
    context = {'ManagerNames':ManagerNames,'HRManagerNames':HRManagerNames,'Designations':Designations,'Confirmationobj':Confirmationobj}
    return  render(request,"lettercl/entryemp.html",context)


# def emplist(request):
#     # print(request.user)
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:   
#         print("Show Page Session")
#         OrganizationID =request.session["OrganizationID"]

#     Department_Name = request.session["Department_Name"]
#     Session_EmployeeCode = request.session["EmployeeCode"]
#     # Designation_Name = request.session["Designation"]
#     OrganizationID = request.session["OrganizationID"]
#     UserType =   request.session["UserType"]

#     print("department is here:", Department_Name)
#     # print("Designation_Name is here:", Designation_Name)

#     session_data = dict(request.session)
#     print("The all session value is here::", session_data)


#     emp_id_subquery = Subquery(
#         EmployeePersonalDetails.objects.filter(
#             EmployeeCode=OuterRef('emp_code'),
#             IsDelete=False
#         ).values('EmpID')[:1]
#     )
#     empdetails = LETTEROFCONFIRMATIONEmployeeDetail.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
#         EmpID=emp_id_subquery
#     ).order_by('-CreatedDateTime','-ModifyDateTime').values()

#     context  = { 
#         'empdetails':empdetails
#     }
#     return render(request,"lettercl/emplist.html",context)


from app.Global_Api import get_organization_list

def emplist(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session.get("OrganizationID")
    Department_Name = request.session.get("Department_Name", "")
    Session_EmployeeCode = request.session.get("EmployeeCode")
    UserType = request.session.get("UserType", "")
    OID  = request.GET.get('OID')
    
    memOrg = get_organization_list(OrganizationID)  
    
    if not OID:
        OID = OrganizationID

    empdetails_query = LETTEROFCONFIRMATIONEmployeeDetail.objects.filter(IsDelete=False)
    
    if OID != "all":
        empdetails_query = empdetails_query.filter(OrganizationID=OID)
        
    # HR sees all data
    if Department_Name and Department_Name.lower() == "hr":
        empdetails = empdetails_query

    # HOD sees only their department
    elif UserType and UserType.lower() == "hod":
        empdetails = empdetails_query.filter(department=Department_Name)

    # Others
    else:
        empdetails = empdetails_query.none()

    empdetails = empdetails.order_by('-CreatedDateTime', '-ModifyDateTime').values()
    
    context = {
        'empdetails': empdetails,
        'OID':OID,
        'memOrg':memOrg
    }

    return render(request, "lettercl/emplist.html", context)



# For generate_appointment_letter
def generate_Confirmation_Letter(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID =request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
          OrganizationID= OID
     
     id = request.GET["LOC_ID"]
     EmpID =  request.GET["EmpID"]

     template_path = "letterpl/plview.html"
    #  NileLogo=MasterAttribute.NileLogo
     get_data = LETTEROFCONFIRMATIONEmployeeDetail.objects.get(id=id)
    #  editor = LETTEROFCONFIRMATION.objects.filter(user=1)
     
     editor = LETTEROFCONFIRMATION.objects.filter(
        OrganizationID=OrganizationID,
        user=1
     )

     if not editor.exists():
        editor = LETTEROFCONFIRMATION.objects.filter(user=1)

     head = True

     if 'head' in request.GET:
            head = request.GET.get('head') 
     print('head = ',head)   

     if editor.exists():
        data_field = editor[0].data
        get_data.data = data_field
        get_data.save() 

     template_path = "lettercl/clview.html"
    # NileLogo=MasterAttribute.NileLogo
   
     get_data.data=get_data.data.replace("@@date_of_confirmation_date@@",str(get_data.date_of_confirmation.strftime("%d-%B-%Y")))
     get_data.data=get_data.data.replace("@@DateofAppointment@@",str(get_data.date_of_appointment.strftime("%d-%B-%Y")))
     
     get_data.data=get_data.data.replace("@@prefix@@",get_data.prefix)
     get_data.data=get_data.data.replace("@@firstname@@",get_data.first_name)
     get_data.data=get_data.data.replace("@@lastname@@",get_data.last_name)
     
     get_data.data=get_data.data.replace("@@Designation@@",get_data.designation)
     
     
     get_data.data=get_data.data.replace("@@Department@@",get_data.department)
     get_data.data=get_data.data.replace("@@general_manager_name@@",get_data.Issuing_manager_name or '')
     get_data.data=get_data.data.replace("@@Issuing_designation@@",get_data.Issuing_designation or '')

      
    
     od =OrganizationDetail(get_data.OrganizationID)
     OLogo=od.get_OrganizationLogo()
     if od.get_MComLogo()==1:
        NileLogo=MasterAttribute.NileLogoURL
     get_data.data=get_data.data.replace("{hotelname}",od.get_Organization_name()) 
     get_data.data=get_data.data.replace("@@hotelname@@",od.get_Organization_name()) 
     header=""
     if head == True:
            header='<table class="noborder" width="100%"><tr><td  align="left"> <img height="150px" src="'+OLogo+'"/> </td> <td  align="center" valign="bottom"></td> <td  align="right"><img src="'+NileLogo+'"  height="150px"/></td></tr></table>'
     
    
      
    #  print(name)
    #  ScantyBaggageForm=forms.ScantyBaggageForm()

     mydict={'Ed':get_data,'header':header}

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
    
    context = {'form':''}
    return render(request,"lettercl/empupdate.html",context)

def empdelete(request):
    id = request.GET["id"]
    empdetail = LETTEROFCONFIRMATIONEmployeeDetail.objects.get(id=id)
    empdetail.IsDelete=True
    empdetail.save()
    return redirect('emplistcl')





# def upload_file(request,id):
#     if request.method == 'POST' and request.FILES['file']:
#         file = request.FILES['file']
#         ext = Path(file.name).suffix

#         new_file = upload_file_to_blob(file,id)
#         if not new_file:
#             messages.warning(request, f"{ext} not allowed only accept {', '.join(ext.lower()for ext in ALLOWED_EXTENTIONS)} ")
#             return render(request, "lettercl/upload_file.html", {}) 
#         new_file.file_name = file.name
#         new_file.file_extention = ext
#         new_file.save()
#         messages.success(request, f"{file.name} was successfully uploaded")
#         return redirect('emplistcl')
    
#     file = LETTEROFCONFIRMATIONEmployeeDetail.objects.get(id=id)
#     context = {'file':file}
#     return render(request, "lettercl/upload_file.html", context)


# def download_file(request, id):
#     file = LETTEROFCONFIRMATIONEmployeeDetail.objects.get(pk=id)
#     file_id = file.file_id
#     file_name = file.file_name
    
#     file_type, _ = mimetypes.guess_type(file_id)
    
    
#     blob_name = file_id
#     blob_content = download_blob(blob_name)
    
#     if blob_content:
#         response = HttpResponse(blob_content.readall(), content_type=file_type)
#         response['Content-Disposition'] = f'attachment; filename={file_name}'
#         messages.success(request, f"{file_name} was successfully downloaded")
#         return response
#     return Http404



# def repalce_file(request, id):
#     file = LETTEROFCONFIRMATIONEmployeeDetail.objects.get(pk=id)
#     file_id = file.file_id
#     file_name = file.file_name
#     EmployeeDetail = LETTEROFCONFIRMATIONEmployeeDetail.objects.get(pk=id)
    
    
#     deletefile = LETTEROFCONFIRMATIONDeletedFileofEmployee.objects.create(LETTEROFCONFIRMATIONEmployeeDetail= EmployeeDetail,file_id = file_id,file_name = file_name)
    
    
    
        
          
#     file = LETTEROFCONFIRMATIONEmployeeDetail.objects.get(pk=id)
#     file.file_name = None
#     file.file_id = None
#     file.save()
#     messages.success(request, f"{file_name} was successfully deleted")
#     return redirect('emplistcl')    



def upload_file(request):
    EmpID = request.GET.get('EmpID')
    OID  = request.GET.get('OID')
    Page = request.GET.get('Page')
    if OID:
            OrganizationID= OID   
    id = request.GET.get('LOC_ID') 
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix

        new_file = upload_file_to_blob(file,id)
        if not new_file:
            messages.warning(request, f"{ext} not allowed only accept {', '.join(ext.lower()for ext in ALLOWED_EXTENTIONS)} ")
            return render(request, "lettercl/upload_file.html", {}) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()
        if Page == "emplistcl" :
                     return redirect('emplistcl')
 
        if Page == "ListPC" :
                     return redirect('ListPC')
 
        Success = 'Uploaded'        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('ProbationConfirmation')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
        return redirect(redirect_url)
    
    
    return render(request, "lettercl/upload_file.html")


def download_file(request):
    id = request.GET.get('LOC_ID')
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID    
    file = LETTEROFCONFIRMATIONEmployeeDetail.objects.get(pk=id)
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


def repalce_file(request):
    UserID =str(request.session["UserID"])
    Page = request.GET.get('Page')
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID       
    id = request.GET.get('LOC_ID')
    EmpID = request.GET.get('EmpID')
    file = LETTEROFCONFIRMATIONEmployeeDetail.objects.get(pk=id)
    file_id = file.file_id
    file_name = file.file_name
    EmployeeDetail = LETTEROFCONFIRMATIONEmployeeDetail.objects.get(pk=id)
    
    
    deletefile = LETTEROFCONFIRMATIONDeletedFileofEmployee.objects.create(LETTEROFCONFIRMATIONEmployeeDetail= EmployeeDetail,file_id = file_id,file_name = file_name)

    file = LETTEROFCONFIRMATIONEmployeeDetail.objects.get(pk=id)
    file.file_name = None
    file.file_id = None
    file.ModifyBy = UserID
    file.save()
    if Page == "emplistcl" :
                     return redirect('emplistcl')
 
    if Page == "ListPC" :
                     return redirect('ListPC')
 
    Success = 'Deleted'        
    encrypted_id = encrypt_id(EmpID)
    url = reverse('ProbationConfirmation')  
    redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
    return redirect(redirect_url)  

    

