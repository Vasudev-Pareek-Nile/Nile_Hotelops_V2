from io import BytesIO
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse, HttpResponseRedirect
from requests import Session, post
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from . import forms
from django.contrib.auth.models import Group
from .models import *
from django.shortcuts import render,redirect
from xhtml2pdf import pisa
from django.template.loader import get_template
from scantybaggage import link_callback 
from django.urls import reverse
from app.models import OrganizationMaster
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from HumanResources.views import EmployeeDetailsData,HrManagerNameandDesignation,ManagerNameandDesignation,EmployeeNameOnTheBasisofDesignation


def home_view(request):
    return render(request,'final/index.html')



from django.db.models import Subquery, OuterRef
from HumanResources.models import EmployeePersonalDetails
from app.views import OrganizationList

def EmpAbscondingList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    UserType = request.session.get("UserType")
       
    OrganizationID =request.session["OrganizationID"]
    memorg = OrganizationList(OrganizationID=OrganizationID)
    I  = request.GET.get('I',OrganizationID)

    if UserType == 'CEO' and request.GET.get('I') is None:
        I = 401
        
    emp_id_subquery = Subquery(
        EmployeePersonalDetails.objects.filter(
            EmployeeCode=OuterRef('Emp_Code'),
            IsDelete=False
        ).values('EmpID')[:1]
    )
    
    Abscondings = EmpAbscondingModel.objects.filter(OrganizationID= I,IsDelete=False).annotate(
        EmpID=emp_id_subquery)
    
    
    return render(request,"EmpAbscondingTemp/EmpAbscondingList.html",{'Abscondings':Abscondings,'memorg':memorg,'I':I})
    

from HumanResources.models import EmployeeWorkDetails
from hotelopsmgmtpy.utils import encrypt_id,decrypt_id
from HumanResources.views import EmployeeDetailsData
def EmpAbscondingEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID =request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID =str(request.session["UserID"])
    EmpCode  = request.GET.get('EC')
    EmpID  = request.GET.get('EmpID')
    AID = request.GET.get('AID')
    Page = request.GET.get('Page')

    # ManagerNames  = ManagerNameandDesignation(request,OrganizationID)
    DepartmentName  = request.GET.get('DepartmentName')
    ManagerNames  =   EmployeeNameOnTheBasisofDesignation(DepartmentName, OrganizationID)


    HRManagerNames  = HrManagerNameandDesignation(request,OrganizationID)

   
  
    Abscondingobj   = None
    if EmpCode is not None:
        if AID is not None:
               Abscondingobj = EmpAbscondingModel.objects.filter(id = AID,Emp_Code = EmpCode,OrganizationID = OrganizationID,IsDelete=False).first()

    

        if Abscondingobj is not None:
            DataFromAbscondingobj  = 'Abscondingobj'
          
        else:
            DataFromAbscondingobj  = 'AbscondingobjHR'
            EmpDetails  = EmployeeDetailsData(EmpID,OrganizationID)
         
            Abscondingobj = {
                            'Emp_Code' : EmpDetails.EmployeeCode,
                            'Name' : EmpDetails.FirstName + " " + EmpDetails.MiddleName + " " + EmpDetails.LastName,
                            'Dept' : EmpDetails.Department,
                            'Designation' : EmpDetails.Designation,
                            'DOJ' : EmpDetails.DateofJoining,
                            'LastEmpStatus': EmpDetails.EmpStatus,
                        }    
    if request.method=='POST':
        Name = request.POST.get('name')
        Emp_Code = request.POST.get('emp_code')
        Dept = request.POST.get('dept')
        Designation = request.POST.get('designation')
        Date_Of_Absconding = request.POST.get('date_of_absconding')
        doj = request.POST.get('doj')

        Remarks = request.POST.get('remarks')
        Issuing_manager_name = request.POST['Issuing_manager_name']
        Issuing_designation = request.POST['Issuing_designation']
        # showcausechecked  = request.POST.get('showcause')
        LastEmpStatus = request.POST.get('LastEmpStatus')

        # showcause = False
        # if  showcausechecked == 'C':
        #     showcause = True
        
        # AbscondingRevoke_Checked = request.POST.get('AbscondingRevoke')

        # IsAbscondingRevoke = False
        # if AbscondingRevoke_Checked == "Revoke":
        #     IsAbscondingRevoke = True
     
       
        if DataFromAbscondingobj == "Abscondingobj" and AID:
                            
           
            Abscondingobj.Name = Name
            Abscondingobj.Emp_Code = Emp_Code
            Abscondingobj.Dept = Dept
            Abscondingobj.Designation = Designation
            Abscondingobj.Date_Of_Absconding = Date_Of_Absconding
            Abscondingobj.DOJ = doj
            Abscondingobj.Issuing_manager_name = Issuing_manager_name
            Abscondingobj.Issuing_designation = Issuing_designation
            # Abscondingobj.showcause = showcause
            Abscondingobj.LastEmpStatus = LastEmpStatus
            # Abscondingobj.AbscondingRevoke = IsAbscondingRevoke


            Abscondingobj.Remarks = Remarks
            Abscondingobj.ModifyBy = UserID
            Abscondingobj.ModifyDateTime = datetime.now()

            Abscondingobj.save()


        else:
            Abscondingobj = EmpAbscondingModel.objects.create(
                Name=Name,
                Emp_Code=Emp_Code,
                Dept=Dept,
                Designation=Designation,
                DOJ=doj,
                Date_Of_Absconding=Date_Of_Absconding,
                Remarks=Remarks,
                CreatedBy=UserID,
                OrganizationID=OrganizationID ,
                Issuing_designation = Issuing_designation,
                Issuing_manager_name= Issuing_manager_name,
                # showcause = showcause,
                LastEmpStatus= LastEmpStatus,
            )

            try:
                    employee_work_details = EmployeeWorkDetails.objects.get(
                        EmpID=EmpID, OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False)
                    employee_work_details.EmpStatus = "Absconding"
                    employee_work_details.ModifyBy = UserID
                    employee_work_details.ModifyDateTime = datetime.now()

                    
                    employee_work_details.save()
            except EmployeeWorkDetails.DoesNotExist:
                    print("EmployeeWorkDetails record not found.")
        
        if Page:
            return redirect('EmpAbscondingList') 
        
        Success = True        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('Absconding')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&OID={OrganizationID}&Success={Success}"  
        return redirect(redirect_url) 
    context = {'Abscondingobj':Abscondingobj,'ManagerNames':ManagerNames,'HRManagerNames':HRManagerNames}
    return render(request,'EmpAbscondingTemp/EmpAbscondingEntry.html',context) 


 
       
def EmpAbscondingDelete(request):
        if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
        else:
            print("Show Page Session")
        OrganizationID =request.session["OrganizationID"]
        OID  = request.GET.get('OID')
        if OID:
                OrganizationID= OID
        UserID =str(request.session["UserID"])
        EmpCode  = request.GET.get('EC')
        EmpID  = request.GET.get('EmpID')
        AID  = request.GET.get('AID')

        
        Final = EmpAbscondingModel.objects.filter(id=AID,OrganizationID=OrganizationID,IsDelete=False).first()
        Final.IsDelete = True
        Final.ModifyBy = UserID
        Final.ModifyDateTime = datetime.now()

        Final.save()
        Success = 'Deleted'        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('Absconding')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&OID={OrganizationID}&Success={Success}"  
        return redirect(redirect_url) 
      
    
   
   
from io import BytesIO
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from xhtml2pdf import pisa

def EmpAbscondingPDF(request):
      # Check if the session contains 'OrganizationID'
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    # Retrieve organization details and current date
    OrganizationID = request.session.get("OrganizationID")
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"

    # Get organization details for the current OrganizationID
    organization = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organization.OrganizationLogo}" if organization and organization.OrganizationLogo else None
    organization_name = organization.OrganizationName if organization else "Unknown Organization"

    # Get default organization details (with ID=3)
    default_organization = OrganizationMaster.objects.filter(OrganizationID=3).first()
    default_organization_logo = f"{base_url}{default_organization.OrganizationLogo}" if default_organization and default_organization.OrganizationLogo else None

    absconding_id = request.GET.get("AID")
    if not absconding_id:
        return HttpResponse("Invalid request. 'AID' parameter is missing.", status=400)

    # Fetch the absconding data from the database
    try:
        absconding_data = EmpAbscondingModel.objects.get(id=absconding_id)
    except EmpAbscondingModel.DoesNotExist:
        return Http404("Absconding record not found.")

    # Define the template path and context for rendering
    template_path = "EmpAbscondingTemp/EmpAbscondingView.html"
    context = {
        'absconding_data': absconding_data,
          'organization_logo': organization_logo,
        'organization_name': organization_name,  # Include the organization name
        'current_datetime': current_datetime,
        'default_organization_logo':default_organization_logo
    }

    # Render the template to HTML
    template = get_template(template_path)
    html_content = template.render(context)

    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Absconding_Report_{absconding_id}.pdf"'

    # Generate the PDF
    pdf_file = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), pdf_file)

    # Handle PDF generation errors
    if pdf.err:
        return HttpResponse("Error generating PDF. Please try again.", status=500)

    # Return the PDF file in the response
    return HttpResponse(pdf_file.getvalue(), content_type='application/pdf')


#  show casue notice ------------------------------------------


def EmpshowcausenoticeList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
       
    OrganizationID =request.session["OrganizationID"]
    memorg = OrganizationList(OrganizationID=OrganizationID)
    I  = request.GET.get('I',OrganizationID)
    emp_id_subquery = Subquery(
        EmployeePersonalDetails.objects.filter(
            EmployeeCode=OuterRef('Emp_Code'),
            IsDelete=False
        ).values('EmpID')[:1]
    )
    
    showcausenotice = Empshowcausenotice.objects.filter(OrganizationID= I,IsDelete=False).annotate(
        EmpID=emp_id_subquery)
    
    
    return render(request,"EmpshowcausenoticeTemp/EmpshowcausenoticeList.html",{'showcausenotice':showcausenotice,'memorg':memorg,'I':I})
  

def EmpshowcausenoticeEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID =request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    Page  = request.GET.get('Page')

    if OID:
            OrganizationID= OID
    UserID =str(request.session["UserID"])
    EmpCode  = request.GET.get('EC')
    EmpID  = request.GET.get('EmpID')
    AID = request.GET.get('AID')
    
    DepartmentName  = request.GET.get('DepartmentName')
    ManagerNames  =   EmployeeNameOnTheBasisofDesignation(DepartmentName, OrganizationID)
    
    # ManagerNames  = ManagerNameandDesignation(request,OrganizationID)
    
    
    HRManagerNames  = HrManagerNameandDesignation(request,OrganizationID)

    showcauseobj   = None
    if EmpCode is not None:
        if AID is not None:
               showcauseobj = Empshowcausenotice.objects.filter(id = AID,Emp_Code = EmpCode,OrganizationID = OrganizationID,IsDelete=False).first()

        if showcauseobj is not None:
            DataFromshowcauseobj  = 'showcauseobj'
          
        else:
            DataFromshowcauseobj  = 'showcauseobjHR'
            EmpDetails  = EmployeeDetailsData(EmpID,OrganizationID)

            showcauseobj = {
                            'Emp_Code' : EmpDetails.EmployeeCode,
                            'Name' : EmpDetails.FirstName + " " + EmpDetails.MiddleName + " " + EmpDetails.LastName,
                            'Dept' : EmpDetails.Department,
                            'Designation' : EmpDetails.Designation,
                            'DOJ' : EmpDetails.DateofJoining,
                        }    
    if request.method=='POST':
        Name = request.POST.get('name')
        Emp_Code = request.POST.get('emp_code')
        Dept = request.POST.get('dept')
        Designation = request.POST.get('designation')
        Date_Of_absence = request.POST.get('Date_Of_absence')
        doj = request.POST.get('doj')

        Remarks = request.POST.get('remarks')
        Issuing_manager_name = request.POST['Issuing_manager_name']
        Issuing_designation = request.POST['Issuing_designation']
        NoticeIssuingdate = request.POST['NoticeIssuingdate']
        NoticeCreateddate = request.POST['NoticeCreateddate']
       
        if DataFromshowcauseobj == "showcauseobj" and AID:
            showcauseobj.Name = Name
            showcauseobj.Emp_Code = Emp_Code
            showcauseobj.Dept = Dept
            showcauseobj.Designation = Designation
            showcauseobj.Date_Of_absence = Date_Of_absence
            showcauseobj.DOJ = doj
            showcauseobj.Issuing_manager_name = Issuing_manager_name
            showcauseobj.Issuing_designation = Issuing_designation
            showcauseobj.NoticeIssuingdate = NoticeIssuingdate
            showcauseobj.NoticeCreateddate = NoticeCreateddate
            showcauseobj.Remarks = Remarks
            showcauseobj.ModifyBy = UserID
            showcauseobj.save()
        else:
           showcauseobj = Empshowcausenotice.objects.create(
                Name=Name,
                Emp_Code=Emp_Code,
                Dept=Dept,
                Designation=Designation,
                DOJ=doj,
                Date_Of_absence=Date_Of_absence,
                Remarks=Remarks,
                NoticeIssuingdate=NoticeIssuingdate,
                NoticeCreateddate=NoticeCreateddate,
                CreatedBy=UserID,
                OrganizationID=OrganizationID  ,Issuing_designation = Issuing_designation,Issuing_manager_name= Issuing_manager_name 
            )
        try:
            employee_work_details = EmployeeWorkDetails.objects.get(
                EmpID=EmpID, OrganizationID=OrganizationID, IsDelete=False)
            employee_work_details.EmpStatus = "Absconding"
            employee_work_details.ModifyBy = UserID
          
            employee_work_details.save()
        except EmployeeWorkDetails.DoesNotExist:
            print("EmployeeWorkDetails record not found.")
        if Page == 'EmpshowcausenoticeList':
             return redirect('EmpshowcausenoticeList')
        Success = True        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('Absconding')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&OID={OrganizationID}&Success={Success}"  
        return redirect(redirect_url) 
    
    context = {
         'showcauseobj':showcauseobj,
         'ManagerNames':ManagerNames,
         'HRManagerNames':HRManagerNames
        }
    return render(request,'EmpshowcausenoticeTemp/EmpshowcausenoticeEntry.html',context) 
  

def Second_Show_Cause_Notice_Entry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID =request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    Page  = request.GET.get('Page')

    if OID:
            OrganizationID= OID
            
    UserID =str(request.session["UserID"])
    EmpCode  = request.GET.get('EC')
    EmpID  = request.GET.get('EmpID')
    AID = request.GET.get('AID')
    
    DepartmentName  = request.GET.get('DepartmentName')
    ManagerNames  =   EmployeeNameOnTheBasisofDesignation(DepartmentName, OrganizationID)
    
    
    HRManagerNames  = HrManagerNameandDesignation(request,OrganizationID)

    showcauseobj   = None
    if EmpCode is not None:
        if AID is not None:
               showcauseobj = Second_Show_Cause_Notice.objects.filter(id = AID,Emp_Code = EmpCode,OrganizationID = OrganizationID,IsDelete=False).first()

        if showcauseobj is not None:
            DataFromshowcauseobj  = 'showcauseobj'
          
        else:
            DataFromshowcauseobj  = 'showcauseobjHR'
            EmpDetails  = EmployeeDetailsData(EmpID,OrganizationID)

            showcauseobj = {
                'Emp_Code' : EmpDetails.EmployeeCode,
                'Name' : EmpDetails.FirstName + " " + EmpDetails.MiddleName + " " + EmpDetails.LastName,
                'Dept' : EmpDetails.Department,
                'Designation' : EmpDetails.Designation,
                'DOJ' : EmpDetails.DateofJoining,
            }    

    if request.method=='POST':
        Name = request.POST.get('name')
        Emp_Code = request.POST.get('emp_code')
        Dept = request.POST.get('dept')
        Designation = request.POST.get('designation')
        Date_Of_absence = request.POST.get('Date_Of_absence')
        doj = request.POST.get('doj')

        Remarks = request.POST.get('remarks')
        Issuing_manager_name = request.POST['Issuing_manager_name']
        Issuing_designation = request.POST['Issuing_designation']
        NoticeIssuingdate = request.POST['NoticeIssuingdate']
        NoticeCreateddate = request.POST['NoticeCreateddate']
       
        if DataFromshowcauseobj == "showcauseobj" and AID:
            showcauseobj.Name = Name
            showcauseobj.Emp_Code = Emp_Code
            showcauseobj.Dept = Dept
            showcauseobj.Designation = Designation
            showcauseobj.Date_Of_absence = Date_Of_absence
            showcauseobj.DOJ = doj
            showcauseobj.Issuing_manager_name = Issuing_manager_name
            showcauseobj.Issuing_designation = Issuing_designation
            showcauseobj.NoticeIssuingdate = NoticeIssuingdate
            showcauseobj.NoticeCreateddate = NoticeCreateddate
            showcauseobj.Remarks = Remarks
            showcauseobj.ModifyBy = UserID
            showcauseobj.save()
        else:
           showcauseobj = Second_Show_Cause_Notice.objects.create(
                Name=Name,
                Emp_Code=Emp_Code,
                Dept=Dept,
                Designation=Designation,
                DOJ=doj,
                Date_Of_absence=Date_Of_absence,
                Remarks=Remarks,
                NoticeIssuingdate=NoticeIssuingdate,
                NoticeCreateddate=NoticeCreateddate,
                CreatedBy=UserID,
                OrganizationID=OrganizationID  ,Issuing_designation = Issuing_designation,Issuing_manager_name= Issuing_manager_name 
            )
        try:
            employee_work_details = EmployeeWorkDetails.objects.get(
                EmpID=EmpID, OrganizationID=OrganizationID, IsDelete=False)
            employee_work_details.EmpStatus = "Absconding"
            employee_work_details.ModifyBy = UserID
          
            employee_work_details.save()
        except EmployeeWorkDetails.DoesNotExist:
            print("EmployeeWorkDetails record not found.")
            
        if Page == 'EmpshowcausenoticeList':
             return redirect('EmpshowcausenoticeList')
         
        Success = True        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('Absconding')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&OID={OrganizationID}&Success={Success}"  
        return redirect(redirect_url) 
    
    context = {
        'showcauseobj':showcauseobj,
        'ManagerNames':ManagerNames,
        'HRManagerNames':HRManagerNames
    }
    return render(request,'EmpshowcausenoticeTemp/Second_Show_Cause_Notice_Entry.html',context) 


 
       
def EmpshowcausenoticeDelete(request):
        if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
        else:
            print("Show Page Session")
        OrganizationID =request.session["OrganizationID"]
        OID  = request.GET.get('OID')
        if OID:
                OrganizationID= OID
        UserID =str(request.session["UserID"])
        EmpCode  = request.GET.get('EC')
        EmpID  = request.GET.get('EmpID')
        AID  = request.GET.get('AID')

        
        Final = Empshowcausenotice.objects.filter(id=AID,OrganizationID=OrganizationID,IsDelete=False).first()
        Final.IsDelete = True
        Final.ModifyBy = UserID
        Final.save()
        Success = 'Deleted'        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('Absconding')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&OID={OrganizationID}&Success={Success}"  
        return redirect(redirect_url) 
      
    
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from django.template.loader import get_template
from xhtml2pdf import pisa  
from app.models import OrganizationMaster  
   
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from datetime import datetime
from app.models import OrganizationMaster
def EmpshowcausenoticePDF(request):
    # Check if the session contains 'OrganizationID'
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    # Retrieve organization details and current date
    OrganizationID = request.session.get("OrganizationID")
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"

    # Get organization details for the current OrganizationID
    organization = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organization.OrganizationLogo}" if organization and organization.OrganizationLogo else None
    organization_name = organization.OrganizationName if organization else "Unknown Organization"

    # Get default organization details (with ID=3)
    default_organization = OrganizationMaster.objects.filter(OrganizationID=3).first()
    default_organization_logo = f"{base_url}{default_organization.OrganizationLogo}" if default_organization and default_organization.OrganizationLogo else None

    # Get employee show cause notice data
    notice_id = request.GET.get("AID")
    try:
        notice_data = Empshowcausenotice.objects.get(id=notice_id)
    except Empshowcausenotice.DoesNotExist:
        return HttpResponse("Show Cause Notice not found.", status=404)

    # Prepare template context
    template_path = "EmpshowcausenoticeTemp/EmpshowcausenoticeView.html"
    context = {
        'organization_logo': organization_logo,
        'organization_name': organization_name,  # Include the organization name
        'current_datetime': current_datetime,
        'notice': notice_data,
        'default_organization_logo': default_organization_logo
    }

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Show_Cause_Notice_{notice_id}.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # Create PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    # Handle PDF generation error
    return HttpResponse("Error generating PDF", status=500)
