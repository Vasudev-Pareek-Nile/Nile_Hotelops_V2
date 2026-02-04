from django.shortcuts import render,redirect
from .models import *
# Create your views here.
# from .forms import EmpDetailsForm 
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
# from .models import LOALETTEROFAPPOINTMENTEmployeeDetail,LETTEROFAPPOINTMENT,LETTEROFAPPOINTMENTDeletedFileofEmployee
from django.shortcuts import render,redirect
from xhtml2pdf import pisa
from django.template.loader import get_template

from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from HumanResources.views import EmployeeDetailsData,HrManagerNameandDesignation,EmployeeNameOnTheBasisofDesignation,ManagerNameandDesignation,HrNameOnTheBasisofDesignation
from HumanResources.models import Salary_Detail_Master,SalaryTitle_Master,SalaryHistory,DesignationHistory,EmployeePersonalDetails
from django.db.models import Subquery, OuterRef
from Checklist_Issued.views import create_initial_checklist_entry, update_checklist_entry, run_background_checklist_tasks_with_creatiion, run_background_checklist_tasks

from datetime import datetime

def safe_date(value):
    if isinstance(value, str):
        # Try HTML format
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except:
            pass
        
        # Try your display format
        try:
            return datetime.strptime(value, "%d-%B-%Y").date()
        except:
            pass

    return value

def fmt(value):
    d = safe_date(value)
    return d.strftime("%d-%B-%Y") if d else ""


import threading

def dump_salary_details_for_loa_once(EmpID, OID, CreatedBy=0):
    
    # print("Data before Effective records")
    effective_record = Salary_Details_Effective.objects.filter(
        EmpID=EmpID,
        OrganizationID=OID,
        IsDelete=False
    ).order_by('-EffectiveFrom').first()


    if not effective_record:
        print("No effective salary found for this month")
        raise ValueError("No effective salary found for this month")
    
    salary_details = Salary_Detail_Master.objects.filter(
        IsDelete=False,
        Effective=effective_record,
        EmpID=EmpID,
        OrganizationID=OID
    ).select_related('Salary_title')

    for sd in salary_details:

        exists = Letter_Of_Appointment_Salary_Detail_Master.objects.filter(
            EmpID=EmpID,
            Salary_title=sd.Salary_title,
            OrganizationID=OID,
            IsDelete=False
        ).exists()

        if not exists:
            Letter_Of_Appointment_Salary_Detail_Master.objects.create(
                EmpID=EmpID,
                Salary_title=sd.Salary_title,
                Permonth=sd.Permonth,
                Perannum=sd.Perannum,
                Salary_title_Old_Id=sd.Salary_title_id,
                Effective=sd.Effective,
                OrganizationID=OID,
                CreatedBy=CreatedBy
            )



def  build_and_save_loa_html(EmpID, emp_code, OID, UserID):
    print("BUILD LOA HTML called", EmpID, emp_code, OID, UserID)

    get_data =LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(emp_code=emp_code, OrganizationID=OID, IsDelete=False).first()
    #  get_data =LOALETTEROFAPPOINTMENTEmployeeDetail.objects.get(id=id)
    editor = LETTEROFAPPOINTMENT.objects.filter(user=1)

    if editor.exists():
        data_field = editor[0].data
        get_data.data = data_field
        get_data.save() 

    get_data.data=get_data.data.replace("@@date_of_appointment@@",str(get_data.date_of_appointment.strftime("%d-%B-%Y")))
    get_data.data=get_data.data.replace("@@emp_code@@",str(get_data.emp_code))
    get_data.data=get_data.data.replace("@@prefix@@",get_data.prefix)
    get_data.data=get_data.data.replace("@@firstname@@",get_data.first_name)
    get_data.data=get_data.data.replace("@@lastname@@",get_data.last_name)
    get_data.data=get_data.data.replace("@@MobNo@@",get_data.mobile_number)
    get_data.data=get_data.data.replace("@@Email@@",get_data.email)
     
    get_data.data=get_data.data.replace("@@Designation@@",get_data.designation)
     
    #  print("the desingnation is here::", get_data.designation)
    if get_data.Reporting_to_designation  is not None:
        get_data.data=get_data.data.replace("@@ReportingTo_Designation@@",get_data.Reporting_to_designation)
     
    get_data.data=get_data.data.replace("@@Date_of_Joining@@",str(get_data.date_of_joining.strftime("%d-%B-%Y")))
    get_data.data=get_data.data.replace("@@Grade@@",get_data.level)
    get_data.data=get_data.data.replace("@@Basic_Salary@@",str(get_data.basic_salary))
     
    get_data.data=get_data.data.replace("@@Department@@",get_data.department)
     
    get_data.data=get_data.data.replace("@@Issuing_manager_name@@",get_data.Issuing_manager_name or '')
    get_data.data=get_data.data.replace("@@Issuing_designation@@",get_data.Issuing_designation or '')

     
    get_data.data=get_data.data.replace("@@Hr_Name@@",get_data.Hr_Name or '')
    get_data.data=get_data.data.replace("@@Hr_Designation@@",get_data.Hr_Designation or '')


    get_data.data=get_data.data.replace("@@Address@@",get_data.address)
    get_data.data=get_data.data.replace("@@PageBreak@@",'<div style="page-break-after:always"></div>')
     
    SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=False, OrganizationID=OID).order_by('TypeOrder', 'TitleOrder')
    s = "" 

        
    s = '<div></div> <h1 style="text-align:center"></h1><table id="tblSal" style="width:100%; border:1px solid #939191; border-collapse:collapse;" class="table"><thead><tr style="background-color:#E9E3D6"><th style="background-color:#F6F1E4">Components</th><th style="background-color:#F6F1E4" align="center">Per Month</th><th style="background-color:#F6F1E4" align="center">Per Annum</th></tr></thead><tbody>'


    salary_details = Letter_Of_Appointment_Salary_Detail_Master.objects.filter(
           IsDelete=False, EmpID=EmpID, OrganizationID=OID
    ).select_related('Salary_title')

        # Convert the queryset to a dictionary for fast lookups by Salary_title_id
    salary_details_dict = {sd.Salary_title_id: sd for sd in salary_details}

        # Loop through all SalaryTitles
    for salary in SalaryTitles:
        salary.Permonth = 0
        salary.Perannum = 0

            # Fetch the corresponding Salary_Detail_Master if it exists
        sd = salary_details_dict.get(salary.id)

        if sd:  # If the Salary_Detail_Master exists
            salary.Permonth = sd.Permonth
            salary.Perannum = sd.Perannum
            is_bold = sd.Salary_title.IsBold
        else:  # If no Salary_Detail_Master exists, default values
            is_bold = False

            # Generate the HTML row based on IsBold
        if is_bold:
            s += (
                "<tr style='background-color:#F5F5F6;'>"
                "<td width='250px'>{}</td><td align='right'>{}</td><td align='right'>{}</td></tr>"
                .format(salary.Title, salary.Permonth, salary.Perannum)
            )
        else:
            s += (
                "<tr><td>{}</td><td align='right'>{}</td><td align='right'>{}</td></tr>".format(
                    salary.Title, salary.Permonth, salary.Perannum
                )
            )   
      
    s += "</tbody></table>"

       
    get_data.data = get_data.data.replace("@@Salary_Details@@", s)

    od =OrganizationDetail(get_data.OrganizationID)
    OLogo=od.get_OrganizationLogo()
    NileLogo = ''
    if od.get_MComLogo()==1:
       NileLogo=MasterAttribute.NileLogoURL

    #  if od.get_Organization_name() == 'Radisson Delhi, MG Road':
    #  if od.get_Organization_name() == 'Radisson Delhi':
    if od.get_Organization_name() == 'Radisson Delhi, MG Road':
       HotelName = 'Radisson Delhi, MG Road (A unit of AKM Hotels Private Limited)'
        # print("hotel name is here::", HotelName)
    else:
       HotelName = od.get_Organization_name()

    #  print("hotel name is here::", HotelName)
     
    get_data.data=get_data.data.replace("{hotelname}",HotelName) 
    get_data.data=get_data.data.replace("@@hotelname@@",HotelName)
    header=""

    #  if NileLogo is None:
    #       NileLogo = ''

    head = True
    if head == True:
        header='<table class="noborder" width="100%"><tr><td  align="left"> </td> <td  align="center" valign="bottom"></td> <td  align="right"><img src="'+NileLogo+'"  height="150px"/></td></tr></table>'
      
     # Save the final HTML content in DB
    get_data.FinalHTML = get_data.data
    get_data.IsSaved = True
    get_data.save()


    return None


def run_all_background(emp_code, EmpID, OID, UserID):
    """Runs salary dump + HTML build in ONE thread"""
    dump_salary_details_for_loa_once(EmpID, OID, UserID)
    build_and_save_loa_html(EmpID, emp_code, OID, UserID)



def run_background_async(emp_code, EmpID, OID, UserID):
    thread = threading.Thread(
        target=run_all_background,
        args=(emp_code, EmpID, OID, UserID),
        daemon=True
    )
    thread.start()


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
    LOA_ID = request.GET.get('LOA_ID')
    DepartmentName = request.GET.get('DepartmentName')
    DepartmentName = request.GET.get('DepartmentName')
    Page  = request.GET.get('Page')
    
    Update=False
    if LOA_ID:
        Update=True

    ManagerNames =  EmployeeNameOnTheBasisofDesignation( DepartmentName,OrganizationID)
    HRManagerNames  = HrNameOnTheBasisofDesignation(OrganizationID)
 
    Issuing_designation =   ''
    Issuing_manager_name =  ''
    Hr_Designation =   ''
    Hr_Name =    ''

                  
    Appointmentobj   = None
    if EmpCode is not None:
        if LOA_ID is not None:
               Appointmentobj = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                   id = LOA_ID,
                   emp_code = EmpCode,
                   OrganizationID = OrganizationID,
                   IsDelete=False
                ).first()
               
               UpdateAppointmentobj = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(
                   id = LOA_ID,
                   emp_code = EmpCode,
                   OrganizationID = OrganizationID,
                   IsDelete=False
                ).first()
 
        
        if Appointmentobj is not None:
            DataFromAppointmentobj  = 'Appointmentobj'
            Issuing_designation =   Appointmentobj.Issuing_designation  
            Issuing_manager_name =   Appointmentobj.Issuing_manager_name 
            Hr_Designation =    Appointmentobj.Hr_Designation 
            Hr_Name =    Appointmentobj.Hr_Name 
        else:
            DataFromAppointmentobj  = 'AppointmentobjHR'

            
        EmpDetails  = EmployeeDetailsData(EmpID,OrganizationID)


        Appointmentobj  =   {
            'emp_code' : EmpDetails.EmployeeCode,
            'prefix' : EmpDetails.Prefix,
            'first_name': (EmpDetails.FirstName + " " + EmpDetails.MiddleName) if EmpDetails.MiddleName else EmpDetails.FirstName,
            'last_name' : EmpDetails.LastName,
            'mobile_number' : EmpDetails.MobileNumber,
            'email' : EmpDetails.EmailAddress,
            'date_of_joining' : EmpDetails.DateofJoining,
            'department' : EmpDetails.Department,
            'designation' : EmpDetails.Designation,
            'Reporting_to_designation' : EmpDetails.ReportingtoDesignation,
            'level' : EmpDetails.Level,
            'basic_salary' : EmpDetails.BasicSalary,
            'CTC':EmpDetails.CTC,
            'address' : EmpDetails.Address,
            'Issuing_designation': Issuing_designation ,
            'Issuing_manager_name':Issuing_manager_name,
            'Hr_Designation':Hr_Designation,
            'Hr_Name':Hr_Name,
        }

    if request.method == "POST":
            emp_code = request.POST['emp_code']
            prefix = request.POST['prefix']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            mobile_number = request.POST['mobile_number']
            email = request.POST['email']
            date_of_appointment = request.POST['date_of_appointment']
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
            
            if DataFromAppointmentobj == "Appointmentobj" and LOA_ID:
                    
                    UpdateAppointmentobj.emp_code = emp_code
                    UpdateAppointmentobj.prefix = prefix
                    UpdateAppointmentobj.first_name = first_name
                    UpdateAppointmentobj.last_name = last_name
                    UpdateAppointmentobj.mobile_number = mobile_number
                    UpdateAppointmentobj.email = email
                    UpdateAppointmentobj.date_of_appointment = date_of_appointment
                    UpdateAppointmentobj.date_of_joining = date_of_joining
                    UpdateAppointmentobj.department = department
                    UpdateAppointmentobj.designation = designation
                    UpdateAppointmentobj.Reporting_to_designation = Reporting_to_designation
                    UpdateAppointmentobj.level = level
                    UpdateAppointmentobj.basic_salary = basic_salary
                    UpdateAppointmentobj.address = address
                    UpdateAppointmentobj.Hr_Name = Hr_Name
                    UpdateAppointmentobj.Hr_Designation = Hr_Designation
                    UpdateAppointmentobj.Issuing_manager_name = Issuing_manager_name
                    UpdateAppointmentobj.Issuing_designation = Issuing_designation
                    UpdateAppointmentobj.ModifyBy  =  UserID    
                    UpdateAppointmentobj.save()
                    

                    if not UpdateAppointmentobj.IsSaved and not UpdateAppointmentobj.FinalHTML:
                        run_background_async(emp_code, EmpID, OrganizationID, UserID)
                        
                    if not UpdateAppointmentobj.IsChecklist_Created:
                        run_background_checklist_tasks_with_creatiion(EmpCode, OrganizationID, UserID)
            else:
                NewAppointmentobj = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.create(
                    emp_code=emp_code,
                    EmpID=EmpID if EmpID else 0,
                    prefix=prefix,
                    first_name=first_name,
                    last_name=last_name,
                    mobile_number=mobile_number,
                    email=email,
                    date_of_appointment=date_of_appointment,
                    date_of_joining=date_of_joining,
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
                    CreatedBy  = UserID,
                    OrganizationID = OrganizationID
                )
                run_background_async(emp_code, EmpID, OrganizationID, UserID)

                if NewAppointmentobj:
                    run_background_checklist_tasks_with_creatiion(EmpCode, OrganizationID, UserID)
                    
            if Page == 'emplistloa':
                    return redirect('emplistloa')
            Success = True        
            encrypted_id = encrypt_id(EmpID)
            url = reverse('EmployeeLetters')  
            redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
            return redirect(redirect_url)
 
 
    context  = {
        'Appointmentobj':Appointmentobj,
        'ManagerNames':ManagerNames,
        'Update':Update,
        'HRManagerNames':HRManagerNames
    }
    return  render(request,"letterloa/entryemp.html",context)



from app.views import OrganizationList


import requests
def emplist(request):
   
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        OrganizationID =request.session["OrganizationID"]
        
    UserType = request.session.get("UserType")

    memOrg = OrganizationList(OrganizationID)  


    I = request.GET.get('I',OrganizationID)

    if UserType == 'CEO' and request.GET.get('I') is None:
        I = 401
    
    AppointemetLetters = (
        LOALETTEROFAPPOINTMENTEmployeeDetail.objects
        .filter(IsDelete=False, OrganizationID=I)
        .order_by('-date_of_appointment')
    )

    context  = { 
        'AppointemetLetters':AppointemetLetters,
        'I':I,
        'memOrg':memOrg
    }
    return render(request,"letterloa/emplist.html",context)

# For generate_appointment_letter
from django.db.models import Prefetch

def  Generate_Appointment_Letter_Intitial(OrganizationID,OID,id,EmpID,head:bool):
     head = bool(head)

     if head:
            head = head 

     template_path = "letterloa/loaview.html"
    #  NileLogo=MasterAttribute.NileLogo
     get_data =LOALETTEROFAPPOINTMENTEmployeeDetail.objects.get(id=id)
     editor = LETTEROFAPPOINTMENT.objects.filter(user=1)

     if editor.exists():
        data_field = editor[0].data
        get_data.data = data_field
        get_data.save() 


    
     get_data.data=get_data.data.replace("@@date_of_appointment@@",str(get_data.date_of_appointment.strftime("%d-%B-%Y")))
     get_data.data=get_data.data.replace("@@emp_code@@",str(get_data.emp_code))
     get_data.data=get_data.data.replace("@@prefix@@",get_data.prefix)
     get_data.data=get_data.data.replace("@@firstname@@",get_data.first_name)
     get_data.data=get_data.data.replace("@@lastname@@",get_data.last_name)
     get_data.data=get_data.data.replace("@@MobNo@@",get_data.mobile_number)
     get_data.data=get_data.data.replace("@@Email@@",get_data.email)
     
     get_data.data=get_data.data.replace("@@Designation@@",get_data.designation)
     
    #  print("the desingnation is here::", get_data.designation)
     if get_data.Reporting_to_designation  is not None:
        get_data.data=get_data.data.replace("@@ReportingTo_Designation@@",get_data.Reporting_to_designation)
     
     get_data.data=get_data.data.replace("@@Date_of_Joining@@",str(get_data.date_of_joining.strftime("%d-%B-%Y")))
     get_data.data=get_data.data.replace("@@Grade@@",get_data.level)
     get_data.data=get_data.data.replace("@@Basic_Salary@@",str(get_data.basic_salary))
     
     get_data.data=get_data.data.replace("@@Department@@",get_data.department)
     
     get_data.data=get_data.data.replace("@@Issuing_manager_name@@",get_data.Issuing_manager_name or '')
     get_data.data=get_data.data.replace("@@Issuing_designation@@",get_data.Issuing_designation or '')

     
     get_data.data=get_data.data.replace("@@Hr_Name@@",get_data.Hr_Name or '')
     get_data.data=get_data.data.replace("@@Hr_Designation@@",get_data.Hr_Designation or '')


     get_data.data=get_data.data.replace("@@Address@@",get_data.address)
     get_data.data=get_data.data.replace("@@PageBreak@@",'<div style="page-break-after:always"></div>')
     
     SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=False, OrganizationID=OID).order_by('TypeOrder', 'TitleOrder')
     s = "" 

        
     s = '<div></div> <h1 style="text-align:center"></h1><table id="tblSal" style="width:100%; border:1px solid #939191; border-collapse:collapse;" class="table"><thead><tr style="background-color:#E9E3D6"><th style="background-color:#F6F1E4">Components</th><th style="background-color:#F6F1E4" align="center">Per Month</th><th style="background-color:#F6F1E4" align="center">Per Annum</th></tr></thead><tbody>'

    # print("Data before Effective records")
     effective_record = Salary_Details_Effective.objects.filter(
         EmpID=EmpID,
         OrganizationID=OID,
         IsDelete=False 
     ).order_by('-EffectiveFrom').first()


     if not effective_record:
        print("No effective salary found for this month")
        raise ValueError("No effective salary found for this month")
    
     salary_details = Salary_Detail_Master.objects.filter(
           Effective=effective_record, IsDelete=False, EmpID=EmpID, OrganizationID=OID
        ).select_related('Salary_title')

        # Convert the queryset to a dictionary for fast lookups by Salary_title_id
     salary_details_dict = {sd.Salary_title_id: sd for sd in salary_details}

        # Initialize the HTML string
        
        # Loop through all SalaryTitles
     for salary in SalaryTitles:
            salary.Permonth = 0
            salary.Perannum = 0

            # Fetch the corresponding Salary_Detail_Master if it exists
            sd = salary_details_dict.get(salary.id)

            if sd:  # If the Salary_Detail_Master exists
                salary.Permonth = sd.Permonth
                salary.Perannum = sd.Perannum
                is_bold = sd.Salary_title.IsBold
            else:  # If no Salary_Detail_Master exists, default values
                is_bold = False

            # Generate the HTML row based on IsBold
            if is_bold:
                s += (
                    "<tr style='background-color:#F5F5F6;'>"
                    "<td width='250px'>{}</td><td align='right'>{}</td><td align='right'>{}</td></tr>"
                    .format(salary.Title, salary.Permonth, salary.Perannum)
                )
            else:
                s += (
                    "<tr><td>{}</td><td align='right'>{}</td><td align='right'>{}</td></tr>".format(
                        salary.Title, salary.Permonth, salary.Perannum
                    )
                )   
      
     s += "</tbody></table>"

       
     get_data.data = get_data.data.replace("@@Salary_Details@@", s)

     od =OrganizationDetail(get_data.OrganizationID)
     OLogo=od.get_OrganizationLogo()
     NileLogo = ''
     if od.get_MComLogo()==1:
        NileLogo=MasterAttribute.NileLogoURL

    #  if od.get_Organization_name() == 'Radisson Delhi, MG Road':
    #  if od.get_Organization_name() == 'Radisson Delhi':
     if od.get_Organization_name() == 'Radisson Delhi, MG Road':
        HotelName = 'Radisson Delhi, MG Road (A unit of AKM Hotels Private Limited)'
        # print("hotel name is here::", HotelName)
     else:
        HotelName = od.get_Organization_name()

    #  print("hotel name is here::", HotelName)
     
     get_data.data=get_data.data.replace("{hotelname}",HotelName) 
     get_data.data=get_data.data.replace("@@hotelname@@",HotelName)
     header=""

    #  if NileLogo is None:
    #       NileLogo = ''

    
     if head == True:
            header='<table class="noborder" width="100%"><tr><td  align="left"> </td> <td  align="center" valign="bottom"></td> <td  align="right"><img src="'+NileLogo+'"  height="150px"/></td></tr></table>'
      
     # Save the final HTML content in DB
     get_data.FinalHTML = get_data.data
     get_data.save()


     mydict={'Ed':get_data,'header':header,'OID': OrganizationID,}

   

   
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'filename="report gcc club.pdf"'
   
     template = get_template(template_path)
     html = template.render(mydict)

 
     result = BytesIO()
  
     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
      
     if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
     return None



def Generate_Appointment_Letter(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    OID = request.GET.get("OID", OrganizationID)

    Loa_id = request.GET["LOA_ID"]
    EmpID = request.GET["EmpID"]
    # head = request.GET.get("head", "true") or "true"
    head = request.GET.get("head", "true").lower() == "true"

    

    get_data = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.get(id=Loa_id)
    
    # if not get_data.IsSaved and not get_data.FinalHTML:
    if not get_data.FinalHTML:
        return Generate_Appointment_Letter_Intitial(OrganizationID,OID,Loa_id,EmpID,head)
    else:
        html_content = get_data.FinalHTML

        # ---------- Header (Logo) ----------
        header_html = ""
        od = OrganizationDetail(get_data.OrganizationID)
        NileLogo = MasterAttribute.NileLogoURL if od.get_MComLogo() == 1 else ""

        if head:
            header_html = f"""
            <table width="100%">
                <tr>
                    <td></td>
                    <td align="center"></td>
                    <td align="right">
                        <img src="{NileLogo}" height="150px"/>
                    </td>
                </tr>
            </table>
            """

        context = {
            "html": html_content, 
            "header": header_html, 
            "OID": OID,
            "full_content": header_html + html_content  
        }

        # ---------- Render PDF ----------
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="Appointment_Letter.pdf"'

        template = get_template("letterloa/loaview.html")
        html = template.render(context)

        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')

        return None







# -------------------------------------------------------------------------------------------



# def  Generate_Appointment_Letter(EmpID, emp_code, OID):

#     get_data =LOALETTEROFAPPOINTMENTEmployeeDetail.objects.filter(emp_code=emp_code, OrganizationID=OID)
#     #  get_data =LOALETTEROFAPPOINTMENTEmployeeDetail.objects.get(id=id)
#     editor = LETTEROFAPPOINTMENT.objects.filter(user=1)

#     if editor.exists():
#         data_field = editor[0].data
#         get_data.data = data_field
#         get_data.save() 

#     get_data.data=get_data.data.replace("@@date_of_appointment@@",str(get_data.date_of_appointment.strftime("%d-%B-%Y")))
#     get_data.data=get_data.data.replace("@@emp_code@@",str(get_data.emp_code))
#     get_data.data=get_data.data.replace("@@prefix@@",get_data.prefix)
#     get_data.data=get_data.data.replace("@@firstname@@",get_data.first_name)
#     get_data.data=get_data.data.replace("@@lastname@@",get_data.last_name)
#     get_data.data=get_data.data.replace("@@MobNo@@",get_data.mobile_number)
#     get_data.data=get_data.data.replace("@@Email@@",get_data.email)
     
#     get_data.data=get_data.data.replace("@@Designation@@",get_data.designation)
     
#     #  print("the desingnation is here::", get_data.designation)
#     if get_data.Reporting_to_designation  is not None:
#         get_data.data=get_data.data.replace("@@ReportingTo_Designation@@",get_data.Reporting_to_designation)
     
#     get_data.data=get_data.data.replace("@@Date_of_Joining@@",str(get_data.date_of_joining.strftime("%d-%B-%Y")))
#     get_data.data=get_data.data.replace("@@Grade@@",get_data.level)
#     get_data.data=get_data.data.replace("@@Basic_Salary@@",str(get_data.basic_salary))
     
#     get_data.data=get_data.data.replace("@@Department@@",get_data.department)
     
#     get_data.data=get_data.data.replace("@@Issuing_manager_name@@",get_data.Issuing_manager_name or '')
#     get_data.data=get_data.data.replace("@@Issuing_designation@@",get_data.Issuing_designation or '')

     
#     get_data.data=get_data.data.replace("@@Hr_Name@@",get_data.Hr_Name or '')
#     get_data.data=get_data.data.replace("@@Hr_Designation@@",get_data.Hr_Designation or '')


#     get_data.data=get_data.data.replace("@@Address@@",get_data.address)
#     get_data.data=get_data.data.replace("@@PageBreak@@",'<div style="page-break-after:always"></div>')
     
#     SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=False, OrganizationID=OID).order_by('TypeOrder', 'TitleOrder')
#     s = "" 

        
#     s = '<div></div> <h1 style="text-align:center"></h1><table id="tblSal" style="width:100%; border:1px solid #939191; border-collapse:collapse;" class="table"><thead><tr style="background-color:#E9E3D6"><th style="background-color:#F6F1E4">Components</th><th style="background-color:#F6F1E4" align="center">Per Month</th><th style="background-color:#F6F1E4" align="center">Per Annum</th></tr></thead><tbody>'


#     salary_details = Letter_Of_Appointment_Salary_Detail_Master.objects.filter(
#            IsDelete=False, EmpID=EmpID, OrganizationID=OID
#     ).select_related('Salary_title')

#         # Convert the queryset to a dictionary for fast lookups by Salary_title_id
#     salary_details_dict = {sd.Salary_title_id: sd for sd in salary_details}

#         # Loop through all SalaryTitles
#     for salary in SalaryTitles:
#         salary.Permonth = 0
#         salary.Perannum = 0

#             # Fetch the corresponding Salary_Detail_Master if it exists
#         sd = salary_details_dict.get(salary.id)

#         if sd:  # If the Salary_Detail_Master exists
#             salary.Permonth = sd.Permonth
#             salary.Perannum = sd.Perannum
#             is_bold = sd.Salary_title.IsBold
#         else:  # If no Salary_Detail_Master exists, default values
#             is_bold = False

#             # Generate the HTML row based on IsBold
#         if is_bold:
#             s += (
#                 "<tr style='background-color:#F5F5F6;'>"
#                 "<td width='250px'>{}</td><td align='right'>{}</td><td align='right'>{}</td></tr>"
#                 .format(salary.Title, salary.Permonth, salary.Perannum)
#             )
#         else:
#             s += (
#                 "<tr><td>{}</td><td align='right'>{}</td><td align='right'>{}</td></tr>".format(
#                     salary.Title, salary.Permonth, salary.Perannum
#                 )
#             )   
      
#     s += "</tbody></table>"

       
#     get_data.data = get_data.data.replace("@@Salary_Details@@", s)

#     od =OrganizationDetail(get_data.OrganizationID)
#     OLogo=od.get_OrganizationLogo()
#     NileLogo = ''
#     if od.get_MComLogo()==1:
#        NileLogo=MasterAttribute.NileLogoURL

#     #  if od.get_Organization_name() == 'Radisson Delhi, MG Road':
#     #  if od.get_Organization_name() == 'Radisson Delhi':
#     if od.get_Organization_name() == 'Radisson Delhi, MG Road':
#        HotelName = 'Radisson Delhi, MG Road (A unit of AKM Hotels Private Limited)'
#         # print("hotel name is here::", HotelName)
#     else:
#        HotelName = od.get_Organization_name()

#     #  print("hotel name is here::", HotelName)
     
#     get_data.data=get_data.data.replace("{hotelname}",HotelName) 
#     get_data.data=get_data.data.replace("@@hotelname@@",HotelName)
#     header=""

#     #  if NileLogo is None:
#     #       NileLogo = ''

#     head = True
#     if head == True:
#         header='<table class="noborder" width="100%"><tr><td  align="left"> </td> <td  align="center" valign="bottom"></td> <td  align="right"><img src="'+NileLogo+'"  height="150px"/></td></tr></table>'
      
#      # Save the final HTML content in DB
#     get_data.FinalHTML = get_data.data
#     get_data.save()


#     return None

# -------------------------------------------------------------------------------------------



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
    id = request.GET.get('LOA_ID') 
    empdetail = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.get(id=id)
    sal_history = SalaryHistory.objects.filter(
        OrganizationID=OrganizationID,
        IsDelete=False,
        EmpID=EmpID,
        SalaryID = id
    )
    for sal in sal_history:
        sal.IsDelete =  True
        sal.ModifyBy = UserID
        sal.save()

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
    Page = request.GET.get('Page')
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    id = request.GET.get('LOA_ID') 
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix

        new_file = upload_file_to_blob(file,id)
        if not new_file:
            messages.warning(request, f"{ext} not allowed only accept {', '.join(ext.lower()for ext in ALLOWED_EXTENTIONS)} ")
            return render(request, "letterloa/upload_file.html", {}) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()
        if Page == 'emplistloa':
                     return redirect('emplistloa')
        Success = 'Uploaded'        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('EmployeeLetters')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
        return redirect(redirect_url)
    
    
    return render(request, "letterloa/upload_file.html")


def download_file(request):
    id = request.GET.get('LOA_ID')
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID 
    file = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.get(pk=id)
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
    Page = request.GET.get('Page')
    if OID:
            OrganizationID= OID    
    id = request.GET.get('LOA_ID')
    EmpID = request.GET.get('EmpID')
    file = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.get(pk=id)
    file_id = file.file_id
    file_name = file.file_name
    EmployeeDetail = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.get(pk=id)
    
    
    deletefile = LETTEROFAPPOINTMENTDeletedFileofEmployee.objects.create(LETTEROFEXPERIENCEEmployeeDetail= EmployeeDetail,file_id = file_id,file_name = file_name)

    file = LOALETTEROFAPPOINTMENTEmployeeDetail.objects.get(pk=id)
    file.file_name = None
    file.file_id = None
    file.ModifyBy = UserID
    file.save()
    if Page == 'emplistloa':
         return redirect('emplistloa')
    
    Success = 'Deleted'        
    encrypted_id = encrypt_id(EmpID)
    url = reverse('EmployeeLetters')  
    redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
    return redirect(redirect_url)  

    




