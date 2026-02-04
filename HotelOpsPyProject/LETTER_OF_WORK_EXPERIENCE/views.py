from django.shortcuts import render,redirect
from .models import *
# Create your views here.
from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail
import io ,os

# Azure.
from hashlib import new
from pathlib import Path
import mimetypes
from django.contrib import messages
from .azure import upload_file_to_blob,ALLOWED_EXTENTIONS,download_blob
# Azure.

from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse,Http404
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from .models import LETTEROFEXPERIENCE,LETTEROFEXPERIENCEEmployeeDetail,LETTEROFEXPERIENCEDeletedFileofEmployee
from django.shortcuts import render,redirect
from xhtml2pdf import pisa
from django.template.loader import get_template


from HumanResources.views import ManagerNameandDesignation,HrManagerNameandDesignation,EmployeeDetailsData,HrNameOnTheBasisofDesignation,EmployeeNameOnTheBasisofDesignation
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from django.urls import reverse
from HumanResources.models import EmployeePersonalDetails

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
    EmpCode = request.GET.get('EC')
    EmpID = request.GET.get('EmpID')
    LOE_ID = request.GET.get('LOE_ID')
    Page  = request.GET.get('Page')

    DepartmentName = request.GET.get('DepartmentName')
    DepartmentName = request.GET.get('DepartmentName')

    
    
    # ManagerNames  = ManagerNameandDesignation(request,OrganizationID)
    # HRManagerNames  = HrManagerNameandDesignation(request,OrganizationID)



    ManagerNames =  EmployeeNameOnTheBasisofDesignation( DepartmentName,OrganizationID)
    HRManagerNames  = HrNameOnTheBasisofDesignation(OrganizationID)
 

    Experienceobj = None

    if EmpCode is not None:
        if LOE_ID is not None:
            Experienceobj = LETTEROFEXPERIENCEEmployeeDetail.objects.filter(id=LOE_ID, emp_code=EmpCode, OrganizationID=OrganizationID, IsDelete=False).first()
        else:
            Experienceobj = LETTEROFEXPERIENCEEmployeeDetail.objects.filter(emp_code=EmpCode, OrganizationID=OrganizationID, IsDelete=False).first()

        if Experienceobj is not None:
            DataFromExperienceobj = 'Experienceobj'
        else:
            DataFromExperienceobj = 'ExperienceobjHR'
            EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
            Experienceobj = {
                'emp_code': EmpDetails.EmployeeCode,
                'prefix': EmpDetails.Prefix,
               'first_name': (EmpDetails.FirstName + " " + EmpDetails.MiddleName) if EmpDetails.MiddleName else EmpDetails.FirstName,
 
                'last_name': EmpDetails.LastName,
                'date_of_joining': EmpDetails.DateofJoining,
                'department': EmpDetails.Department,
                'designation': EmpDetails.Designation,
            }

    if request.method == "POST":
        # Retrieve form data
        emp_code = request.POST['emp_code']
        prefix = request.POST['prefix']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        generate_date = request.POST['generate_date']
        date_of_joining = request.POST['date_of_joining']
        date_of_last_working = request.POST.get('date_of_last_working')  # Optional
        department = request.POST['department']
        designation = request.POST['designation']
        Hr_Name = request.POST['Hr_Name']
        Hr_Designation = request.POST['Hr_Designation']

        # Update existing record or create a new one
        if DataFromExperienceobj == "Experienceobj" and LOE_ID:
            Experienceobj.emp_code = emp_code
            Experienceobj.prefix = prefix
            Experienceobj.first_name = first_name
            Experienceobj.last_name = last_name
            Experienceobj.generate_date = generate_date
            Experienceobj.date_of_joining = date_of_joining
            Experienceobj.date_of_last_working = date_of_last_working
            Experienceobj.department = department
            Experienceobj.designation = designation
            Experienceobj.Hr_Name = Hr_Name
            Experienceobj.Hr_Designation = Hr_Designation
            Experienceobj.ModifyBy = UserID
            Experienceobj.save()

        else:
            Experienceobj = LETTEROFEXPERIENCEEmployeeDetail.objects.create(
                emp_code=emp_code,
                prefix=prefix,
                first_name=first_name,
                last_name=last_name,
                generate_date=generate_date,
                date_of_joining=date_of_joining,
                date_of_last_working=date_of_last_working,
                department=department,
                designation=designation,
                Hr_Name=Hr_Name,
                Hr_Designation=Hr_Designation,
                CreatedBy=UserID,
                OrganizationID=OrganizationID
            )
        if Page == 'emplistloe':
                     return redirect('emplistloe')

        # Redirect with success message
        Success = True
        encrypted_id = encrypt_id(EmpID)
        url = reverse('EmployeeLetters')
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}"
        return redirect(redirect_url)
    context = {'Experienceobj': Experienceobj, 'ManagerNames': ManagerNames, 'HRManagerNames': HRManagerNames}
    return render(request, "letterofexp/entryemp.html", context)



from django.db.models import Subquery, OuterRef
from app.views import OrganizationList
def emplist(request):
 
    if 'OrganizationID' not in request.session:

        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    UserType = request.session.get("UserType")

    OrganizationID =request.session["OrganizationID"]
    memOrg = OrganizationList(OrganizationID)  


    
    I = request.GET.get('I',OrganizationID)
    
    if UserType == 'CEO' and request.GET.get('I') is None:
        I = 401
    
    emp_id_subquery = Subquery(
        EmployeePersonalDetails.objects.filter(
            EmployeeCode=OuterRef('emp_code'),
            IsDelete=False
        ).values('EmpID')[:1]
        )

    ExperienceLetters = LETTEROFEXPERIENCEEmployeeDetail.objects.filter(IsDelete=False,OrganizationID= I).annotate(
        EmpID=emp_id_subquery
    ).order_by('-CreatedDateTime','-ModifyDateTime').values()
    context  = { 
        'ExperienceLetters':ExperienceLetters,
        'I':I,
        'memOrg':memOrg
        }
    return render(request,"letterofexp/emplist.html",context)

# For generate_appointment_letter
def generate_letter_of_experience(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID =request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID   
     template_path = "letterofexp/letterofexpview.html"
    #  NileLogo=MasterAttribute.NileLogo
        
     id = request.GET["LOE_ID"]
     EmpID =  request.GET["EmpID"]
     head = True

     if 'head' in request.GET:
            head = request.GET.get('head') 
     print('head = ',head)   
   

     get_data =LETTEROFEXPERIENCEEmployeeDetail.objects.get(id=id)
     editor = LETTEROFEXPERIENCE.objects.filter(user=1)

     if editor.exists():
        data_field = editor[0].data
        get_data.data = data_field
        get_data.save() 

    
     od =OrganizationDetail(get_data.OrganizationID)
     OLogo=od.get_OrganizationLogo()
     if od.get_MComLogo()==1:
        NileLogo=MasterAttribute.NileLogoURL
     get_data.data=get_data.data.replace("@@generate_date@@",str(get_data.generate_date.strftime('%d-%b-%Y')))
     get_data.data=get_data.data.replace("@@emp_code@@",str(get_data.emp_code))
     get_data.data=get_data.data.replace("@@prefix@@",get_data.prefix)

     get_data.data=get_data.data.replace("@@firstname@@",get_data.first_name)
     get_data.data=get_data.data.replace("@@lastname@@",get_data.last_name)
     
     get_data.data=get_data.data.replace("@@Designation@@",get_data.designation)
     get_data.data=get_data.data.replace("@@date_of_joining@@",str(get_data.date_of_joining.strftime('%d-%b-%Y')))
     get_data.data=get_data.data.replace("@@date_of_last_working@@",str(get_data.date_of_last_working.strftime('%d-%b-%Y')))
     get_data.data=get_data.data.replace("@@HotelName@@",od.get_Organization_name())
     get_data.data=get_data.data.replace("@@Department@@",get_data.department)
     

     
     get_data.data=get_data.data.replace("@@Hr_manager_name@@",get_data.Hr_Name or '')
     get_data.data=get_data.data.replace("@@Hr_manager_designation@@",get_data.Hr_Designation or '')                               

     prefix = (get_data.prefix or "").strip().lower()
     get_data.data = " ".join(get_data.data.split())

     if prefix in ['miss', 'miss.', 'mrs', 'mrs.', 'ms.', 'ms']:
        get_data.data = get_data.data.replace(" his ", " her ")
        get_data.data = get_data.data.replace(" him ", " her ")
     elif prefix in ['mr', 'mr.']:
        # Male - no change needed, but retained for symmetry
        get_data.data = get_data.data.replace(" his ", " his ")
        get_data.data = get_data.data.replace(" him ", " him ")
     else:
        # Unknown, other, or blank
        get_data.data = get_data.data.replace(" his ", " his/her ")
        get_data.data = get_data.data.replace(" him ", " him/her ")
     
     header=""
     if head == True:
            header='<table class="noborder" width="100%"><tr><td  align="left"> <img height="150px" src="'+OLogo+'"/> </td> <td  align="center" valign="bottom"></td> <td  align="right"><img src="'+NileLogo+'"  height="150px"/></td></tr></table>'
     

      

     mydict={'Ed':get_data,'header':header}

     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'filename="report gcc club.pdf"'
     template = get_template(template_path)
     html = template.render(mydict)

     result = BytesIO()
     pdf  = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
       
     if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
     return None




def empdelete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID =request.session["OrganizationID"]
        OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID   
    UserID =str(request.session["UserID"])
    EmpID = request.GET.get('EmpID')
    id = request.GET.get('LOE_ID') 
    empdetail = LETTEROFEXPERIENCEEmployeeDetail.objects.get(id=id)
    empdetail.IsDelete=True
    empdetail.ModifyBy = UserID
    empdetail.save()
    Success = 'Deleted'        
    encrypted_id = encrypt_id(EmpID)
    url = reverse('EmployeeLetters')  
    redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
    return redirect(redirect_url)




def upload_file(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID =request.session["OrganizationID"]
        OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID   
    EmpID = request.GET.get('EmpID')
    Page  = request.GET.get('Page')
    id = request.GET.get('LOE_ID')    
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix

        new_file = upload_file_to_blob(file,id)
        if not new_file:
            messages.warning(request, f"{ext} not allowed only accept {', '.join(ext.lower()for ext in ALLOWED_EXTENTIONS)} ")
            return render(request, "letterofexp/upload_file.html", {}) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()
        if Page == 'emplistloe':
                     return redirect('emplistloe')
      
        Success = 'Uploaded'        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('EmployeeLetters')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
        return redirect(redirect_url)
    
    
    return render(request, "letterofexp/upload_file.html")


def download_file(request):
    id = request.GET.get('LOE_ID')
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID   
    file = LETTEROFEXPERIENCEEmployeeDetail.objects.get(pk=id)
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
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
        OrganizationID =request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    Page  = request.GET.get('Page')
    if OID:
            OrganizationID= OID   
    UserID =str(request.session["UserID"])
    EmpID = request.GET.get('EmpID')
    id = request.GET.get('LOE_ID')     
    file = LETTEROFEXPERIENCEEmployeeDetail.objects.get(pk=id)
    file_id = file.file_id
    file_name = file.file_name
    EmployeeDetail = LETTEROFEXPERIENCEEmployeeDetail.objects.get(pk=id)
    
    
    deletefile = LETTEROFEXPERIENCEDeletedFileofEmployee.objects.create(LETTEROFEXPERIENCEEmployeeDetail= EmployeeDetail,file_id = file_id,file_name = file_name)

    file = LETTEROFEXPERIENCEEmployeeDetail.objects.get(pk=id)
    file.file_name = None
    file.file_id = None
    file.ModifyBy = UserID
    file.save()
    if Page == 'emplistloe':
                     return redirect('emplistloe')
    Success = 'Deleted'        
    encrypted_id = encrypt_id(EmpID)
    url = reverse('EmployeeLetters')  
    redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
    return redirect(redirect_url)
    
