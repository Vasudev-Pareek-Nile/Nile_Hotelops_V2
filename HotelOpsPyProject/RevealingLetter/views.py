from django.shortcuts import render,redirect
from .models import *

from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail
from django.db import connection
# Azure.
from pathlib import Path
import mimetypes
from django.contrib import messages
from .azure import upload_file_to_blob,ALLOWED_EXTENTIONS,download_blob
# Azure.

from io import BytesIO
from django.shortcuts import render
from django.urls import reverse

from django.http import HttpResponse,Http404
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from .models import RevealingLetterEmployeeDetail,RevealingLetter,RevealingLetterDeletedFile
from django.shortcuts import render,redirect
from xhtml2pdf import pisa
from django.template.loader import get_template




from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from HumanResources.views import EmployeeDetailsData,HrManagerNameandDesignation,ManagerNameandDesignation,EmployeeDetailHistroy,HrNameOnTheBasisofDesignation,EmployeeNameOnTheBasisofDesignation

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
    R_ID = request.GET.get('R_ID')
    DepartmentName = request.GET.get('DepartmentName')
    
    
    # ManagerNames  = ManagerNameandDesignation(request,OrganizationID)
    # HRManagerNames  = HrManagerNameandDesignation(request,OrganizationID)



    ManagerNames =  EmployeeNameOnTheBasisofDesignation( DepartmentName,OrganizationID)
    HRManagerNames  = HrNameOnTheBasisofDesignation(OrganizationID)
 

    EmpHistroy = EmployeeDetailHistroy(EmpID, OrganizationID, EmpCode)
    if EmpHistroy:
        Salaryhis = EmpHistroy['Salaryhis']
        Designationhis = EmpHistroy['Designationhis']
        Appointment  =  EmpHistroy['Appointment']
        SalaryIncreament  = EmpHistroy['SalaryIncreament']
        Confirmation  = EmpHistroy['Confirmation']
        Promotion  = EmpHistroy['Promotion']
        tenure_till_today = EmpHistroy['tenure_till_today']



    
                  
    Revealingobj   = None
    if EmpCode is not None:
        if R_ID is not None:
               Revealingobj = RevealingLetterEmployeeDetail.objects.filter(id = R_ID,emp_code = EmpCode,OrganizationID = OrganizationID,IsDelete=False).first()

     

        
        if Revealingobj is not None:
            DataFromRevealingobj  = 'Revealingobj'
          
        else:
         

            DataFromRevealingobj  = 'RevealingobjHR'
            EmpDetails  = EmployeeDetailsData(EmpID,OrganizationID)
         

            Revealingobj  =   {
                                'emp_code' : EmpDetails.EmployeeCode,
                                'prefix' : EmpDetails.Prefix,
                                'first_name' : EmpDetails.FirstName + EmpDetails.MiddleName or '',
                                'last_name' : EmpDetails.LastName,
                                'mobile_number' : EmpDetails.MobileNumber,
                                'email' : EmpDetails.EmailAddress,
                                'date_of_joining' : EmpDetails.DateofJoining,
                                'department' : EmpDetails.Department,
                                'designation' : EmpDetails.Designation,
                                'Reporting_to_designation' : EmpDetails.ReportingtoDesignation,
                                'level' : EmpDetails.Level,
                                'basic_salary' : EmpDetails.BasicSalary,
                                'address' : EmpDetails.Address,

                               }
     
        if request.method == "POST":
                emp_code = request.POST['emp_code']
                prefix = request.POST['prefix']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                mobile_number = request.POST['mobile_number']
                email = request.POST['email']
                date_of_Revealing = request.POST['date_of_Revealing']
                date_of_last_working = request.POST['date_of_last_working']
                date_of_joining = request.POST['date_of_joining']
                department = request.POST['department']
                designation = request.POST['designation']
                Reporting_to_designation = request.POST.get('reporting_to_designation')  
                level = request.POST['level']
                basic_salary = int(float(request.POST.get('basic_salary')))

                address = request.POST['address']
                Hr_Name = request.POST['Hr_Name']
                Hr_Designation = request.POST['Hr_Designation']
                Issuing_manager_name = request.POST['Issuing_manager_name']
                Issuing_designation = request.POST['Issuing_designation']
                
                if DataFromRevealingobj == "Revealingobj" and R_ID:
                        print("R_ID =",R_ID)
                       
                        Revealingobj.emp_code = emp_code
                        Revealingobj.prefix = prefix
                        Revealingobj.first_name = first_name
                        Revealingobj.last_name = last_name
                        Revealingobj.mobile_number = mobile_number
                        Revealingobj.email = email
                        Revealingobj.date_of_Revealing = date_of_Revealing
                        Revealingobj.date_of_joining = date_of_joining
                        Revealingobj.date_of_last_working = date_of_last_working 
                        Revealingobj.department = department
                        Revealingobj.designation = designation
                        Revealingobj.Reporting_to_designation = Reporting_to_designation
                        Revealingobj.level = level
                        Revealingobj.basic_salary = basic_salary
                        Revealingobj.address = address
                        Revealingobj.Hr_Name = Hr_Name
                        Revealingobj.Hr_Designation = Hr_Designation
                        Revealingobj.Issuing_manager_name = Issuing_manager_name
                        Revealingobj.Issuing_designation = Issuing_designation
                        Revealingobj.ModifyBy  =  UserID    
                        
                        Revealingobj.save()

                else:
                   
                    Revealingobj = RevealingLetterEmployeeDetail.objects.create(
                        emp_code=emp_code,
                        prefix=prefix,
                        first_name=first_name,
                        last_name=last_name,
                        mobile_number=mobile_number,
                        email=email,
                        date_of_Revealing=date_of_Revealing,
                        date_of_joining=date_of_joining,
                        date_of_last_working = date_of_last_working,
                        department=department,
                        designation=designation,
                        Reporting_to_designation=Reporting_to_designation,
                        level=level,
                        basic_salary=basic_salary,
                        address=address,
                        Hr_Name=Hr_Name,
                        Hr_Designation=Hr_Designation,
                        Issuing_manager_name=Issuing_manager_name,
                        Issuing_designation=Issuing_designation,
                        CreatedBy  = UserID,OrganizationID = OrganizationID
                     )
              
                Success = True        
                encrypted_id = encrypt_id(EmpID)
                url = reverse('EmployeeLetters')  
                redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
                return redirect(redirect_url)
    
    
    
    context  = {'Revealingobj':Revealingobj,'ManagerNames':ManagerNames,'HRManagerNames':HRManagerNames,'Designationhis':Designationhis,'Salaryhis':Salaryhis,'SalaryIncreament':SalaryIncreament,'Confirmation':Confirmation,'Appointment':Appointment,'Promotion':Promotion,'tenure_till_today':tenure_till_today}
    return  render(request,"RevealingLetter/entryemp.html",context)



from app.views import OrganizationList
from HumanResources.models import EmployeePersonalDetails
from django.db.models import Subquery, OuterRef




# For generate_Revealing_letter
def Generate_Revealing_Letter(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID =request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID   
     
     id = request.GET["R_ID"]
     EmpID =  request.GET["EmpID"]
     EmpCode = request.GET["EC"]
     EmpHistroy = EmployeeDetailHistroy(EmpID, OrganizationID, EmpCode)
     if EmpHistroy:
        Salaryhis = EmpHistroy['Salaryhis']
        Designationhis = EmpHistroy['Designationhis']
        Appointment  =  EmpHistroy['Appointment']
        SalaryIncreament  = EmpHistroy['SalaryIncreament']
        Confirmation  = EmpHistroy['Confirmation']
        Promotion  = EmpHistroy['Promotion']
        tenure_till_today = EmpHistroy['tenure_till_today']

     template_path = "RevealingLetter/rlview.html"
    #  NileLogo=MasterAttribute.NileLogo
     get_data =RevealingLetterEmployeeDetail.objects.filter(id=id).first()
     editor = RevealingLetter.objects.filter(user=1)
     head = True

     if 'head' in request.GET:
            head = request.GET.get('head') 
     print('head = ',head)   

     if editor.exists():
        data_field = editor[0].data
        get_data.data = data_field
        get_data.save() 
    
    
     get_data.data=get_data.data.replace("@@date_of_Revealing@@",str(get_data.date_of_Revealing.strftime("%d-%B-%Y")))
     get_data.data=get_data.data.replace("@@emp_code@@",str(get_data.emp_code))
     get_data.data=get_data.data.replace("@@prefix@@",get_data.prefix)
     get_data.data=get_data.data.replace("@@firstname@@",get_data.first_name)
     get_data.data=get_data.data.replace("@@lastname@@",get_data.last_name)
     get_data.data=get_data.data.replace("@@MobNo@@",get_data.mobile_number)
     get_data.data=get_data.data.replace("@@Email@@",get_data.email)
     
     get_data.data=get_data.data.replace("@@Designation@@",get_data.designation)
     if get_data.Reporting_to_designation  is not None:
        get_data.data=get_data.data.replace("@@ReportingTo_Designation@@",get_data.Reporting_to_designation)
     
     get_data.data=get_data.data.replace("@@Date_of_Joining@@",str(get_data.date_of_joining.strftime("%d-%B-%Y")))
     get_data.data=get_data.data.replace("@@date_of_last_working@@",str(get_data.date_of_last_working.strftime("%d-%B-%Y")))

     get_data.data=get_data.data.replace("@@Grade@@",get_data.level)
     get_data.data=get_data.data.replace("@@Basic_Salary@@",str(get_data.basic_salary))
     
     get_data.data=get_data.data.replace("@@Department@@",get_data.department)
     
     get_data.data=get_data.data.replace("@@Issuing_manager_name@@",get_data.Issuing_manager_name)
     get_data.data=get_data.data.replace("@@Issuing_designation@@",get_data.Issuing_designation)

     
     get_data.data=get_data.data.replace("@@Hr_Name@@",get_data.Hr_Name)
     get_data.data=get_data.data.replace("@@Hr_Designation@@",get_data.Hr_Designation)


     get_data.data=get_data.data.replace("@@Address@@",get_data.address)
     get_data.data=get_data.data.replace("@@PageBreak@@",'<div style="page-break-after:always"></div>')
     
     
    
    
     
     
   
    

     od =OrganizationDetail(get_data.OrganizationID)
     OLogo=od.get_OrganizationLogo()
     if od.get_MComLogo()==1:
        NileLogo=MasterAttribute.NileLogoURL
     get_data.data=get_data.data.replace("{hotelname}",od.get_Organization_name()) 
     get_data.data=get_data.data.replace("@@hotelname@@",od.get_Organization_name()) 
     header=""
     if head == True:
            header='<table class="noborder" width="100%"><tr><td  align="left"> <img height="150px" src="'+OLogo+'"/> </td> <td  align="center" valign="bottom"><h1 style="font-size:23px">Letter of Relieving</h1></td> <td  align="right"><img src="'+NileLogo+'"  height="150px"/></td></tr></table>'
     

      
      
   

     mydict={'Ed':get_data,'header':header,'Designationhis':Designationhis,'Salaryhis':Salaryhis,'SalaryIncreament':SalaryIncreament,'Confirmation':Confirmation,'Appointment':Appointment,'Promotion':Promotion,'tenure_till_today':tenure_till_today}

   

   
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
    id = request.GET.get('R_ID') 
    empdetail = RevealingLetterEmployeeDetail.objects.get(id=id)
    empdetail.IsDelete=True
    empdetail.ModifyBy = UserID
    empdetail.save()
    Success = 'Deleted'        
    encrypted_id = encrypt_id(EmpID)
    url = reverse('EmployeeLetters')  
    redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
    return redirect(redirect_url)  



def upload_file(request):
    EmpID = request.GET.get('EmpID')
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID   
    id = request.GET.get('R_ID') 
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix

        new_file = upload_file_to_blob(file,id)
        if not new_file:
            messages.warning(request, f"{ext} not allowed only accept {', '.join(ext.lower()for ext in ALLOWED_EXTENTIONS)} ")
            return render(request, "RevealingLetter/upload_file.html", {}) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()
        Success = 'Uploaded'        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('EmployeeLetters')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
        return redirect(redirect_url)
    
    
    return render(request, "RevealingLetter/upload_file.html")


def download_file(request):
    id = request.GET.get('R_ID')
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID    
    file = RevealingLetterEmployeeDetail.objects.get(pk=id)
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
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID       
    id = request.GET.get('R_ID')
    EmpID = request.GET.get('EmpID')
    file = RevealingLetterEmployeeDetail.objects.get(pk=id)
    file_id = file.file_id
    file_name = file.file_name
    EmployeeDetail = RevealingLetterEmployeeDetail.objects.get(pk=id)
    
    
    deletefile = RevealingLetterDeletedFile.objects.create(RevealingLetterEmployeeDetail= EmployeeDetail,file_id = file_id,file_name = file_name)

    file = RevealingLetterEmployeeDetail.objects.get(pk=id)
    file.file_name = None
    file.file_id = None
    file.ModifyBy = UserID
    file.save()
    Success = 'Deleted'        
    encrypted_id = encrypt_id(EmpID)
    url = reverse('EmployeeLetters')  
    redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
    return redirect(redirect_url)  

    

