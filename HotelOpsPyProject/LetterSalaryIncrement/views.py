from django.shortcuts import render,redirect
from .models import *
# Create your views here.
from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail
import io ,os

from pathlib import Path
import mimetypes
from django.contrib import messages

from .azure import upload_file_to_blob,ALLOWED_EXTENTIONS,download_blob

from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse,Http404
from requests import Session, post
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from . import forms
from django.contrib.auth.models import Group
from .models import LETTEROFSALARYINCREAMENTEmployeeDetail,LETTEROFSALARYINCREAMENT,LETTEROFSALARYINCREAMENTDeletedFileofEmployee
from django.shortcuts import render,redirect
from xhtml2pdf import pisa
from django.template.loader import get_template
from datetime import datetime
from HumanResources.views import ManagerNameandDesignation,HrManagerNameandDesignation,EmployeeDetailsData, UpdateEmployeeSalaryGridByIncreamnet,EmployeeNameOnTheBasisofDesignation,HrNameOnTheBasisofDesignation
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from django.urls import reverse
from Manning_Guide.models import OnRollDesignationMaster
from HumanResources.models import Salary_Detail_Master,SalaryTitle_Master,SalaryHistory,EmployeePersonalDetails

from django.db.models import Subquery, OuterRef
from LetteofPromotion.views import get_latest_effective_salary

def entryEmp(request):
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
    LOI_ID = request.GET.get('LOI_ID')
    DepartmentName = request.GET.get('DepartmentName')
    Page = request.GET.get('Page')

    ManagerNames =  EmployeeNameOnTheBasisofDesignation( DepartmentName,OrganizationID)
    HRManagerNames  = HrNameOnTheBasisofDesignation(OrganizationID)

    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    Increamentobj   = None
    SalHistory = None
    if EmpCode is not None:
        if LOI_ID is not None:
               Increamentobj = LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(id = LOI_ID,emp_code = EmpCode,OrganizationID = OrganizationID,IsDelete=False).first()
               SalHistory  = SalaryHistory.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID=EmpID,SalaryID=LOI_ID).first()

        if Increamentobj is not None:
            DataFromIncreamentobj  = 'Increamentobj'
            SalaryTitles  = SalaryTitle_Master.objects.filter(IsDelete=False, OrganizationID=OID).order_by('TypeOrder','TitleOrder')
            for salary in SalaryTitles:
                    SC = IncreamentSalaryDetails.objects.filter(IsDelete=False,Salary_title_id = salary.id,LETTEROFSALARYINCREAMENTEmployeeDetail=Increamentobj,OrganizationID=OrganizationID)
                    if SC.exists():
                            salary.PresentEmoluments = SC[0].PresentSal
                            salary.RevisedSalary = SC[0].RevisedSal
        else:
            DataFromIncreamentobj  = 'IncreamentobjHR'
            EmpDetails  = EmployeeDetailsData(EmpID,OrganizationID)
            Effective_Obj = get_latest_effective_salary(EmpID, OID)
            # print("effeitve_obj::", Effective_Obj)
          
            SalaryTitles  = SalaryTitle_Master.objects.filter(IsDelete=False, OrganizationID=OID).order_by('TypeOrder','TitleOrder')
            for salary in SalaryTitles:
                salary.PresentEmoluments = 0
                salary.RevisedSalary = 0
            
                SC = Salary_Detail_Master.objects.filter(Effective=Effective_Obj, IsDelete=False,EmpID=EmpID, Salary_title_id = salary.id,OrganizationID=OID)
                if SC.exists():
                        salary.PresentEmoluments = SC[0].Permonth
         

            Increamentobj  =   {
                'emp_code' : EmpDetails.EmployeeCode,
                'prefix' : EmpDetails.Prefix,
                'first_name': (EmpDetails.FirstName + " " + EmpDetails.MiddleName) if EmpDetails.MiddleName else EmpDetails.FirstName,
                'last_name' : EmpDetails.LastName,
                'department' : EmpDetails.Department,
                'designation' : EmpDetails.Designation,
                "CTC":EmpDetails.CTC
            }

        if LOI_ID:
               CTCEmpDetails  = EmployeeDetailsData(EmpID,OrganizationID)
          
        if request.method == "POST":
                emp_code = request.POST['emp_code']
                prefix = request.POST['prefix']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
             
                department = request.POST['department']
                designation = request.POST['designation']
                CTC = request.POST['CTC']
                date_of_salary_increament = request.POST['date_of_salary_increament']
              
                Issuing_manager_name = request.POST['Issuing_manager_name']
                Issuing_designation = request.POST['Issuing_designation']
                
                if DataFromIncreamentobj == "Increamentobj" and LOI_ID:
                        Increamentobj.emp_code = emp_code
                        Increamentobj.prefix = prefix
                        Increamentobj.first_name = first_name
                        Increamentobj.last_name = last_name
                        Increamentobj.department = department
                        Increamentobj.designation = designation
                        Increamentobj.CTC = CTC
                        Increamentobj.date_of_salary_increament = date_of_salary_increament

                        Increamentobj.Issuing_manager_name = Issuing_manager_name
                        Increamentobj.Issuing_designation = Issuing_designation
                        Increamentobj.ModifyBy  =  UserID    
                        
                        Increamentobj.save()
                        
                        # print(SalHistory ,'= SalHistory')
                        if SalHistory is not None:
                            PreviousSalHistory = SalaryHistory.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID=EmpID).order_by('-id')
                            if PreviousSalHistory.count() >= 2:
                                pr = PreviousSalHistory[1]
                                pr.Effective_to = date_of_salary_increament
                                pr.ModifyBy =  UserID
                                pr.save()
                            
                            
                            SalHistory.Effective_from = date_of_salary_increament
                            SalHistory.ToSalary = CTC
                            SalHistory.ModifyBy = UserID
                            SalHistory.save()

                        else:
                            PreviousSalHistory = SalaryHistory.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID=EmpID).order_by('-id').first()
                            if PreviousSalHistory:
                                PreviousSalHistory.Effective_to = date_of_salary_increament
                                PreviousSalHistory.ModifyBy =  UserID
                                PreviousSalHistory.save()
                                
                            FromSalary =   CTCEmpDetails.CTC
                            ToSalary = CTC
                            SalaryHistoryobj  =   SalaryHistory.objects.create(EmpID=EmpID,Effective_from = date_of_salary_increament,OrganizationID = OrganizationID,FromSalary=FromSalary,ToSalary=ToSalary,SalaryID=LOI_ID)
      
                        SC = IncreamentSalaryDetails.objects.filter(IsDelete=False,LETTEROFSALARYINCREAMENTEmployeeDetail=Increamentobj,OrganizationID=OrganizationID)
                        for s in SC:
                                s.IsDelete = True
                                s.ModifyBy  = UserID
                                s.save()
                        Total_Title = request.POST['Total_Title']
                        for i in range(int(Total_Title) + 1):
                            TitleID = request.POST[f'TitleID_{i}']
                            PresentSal = request.POST[f'PresentEmoluments_{i}']
                            RevisedSal = request.POST[f'RevisedSalary_{i}']

                            salaryObj = IncreamentSalaryDetails.objects.create(
                                LETTEROFSALARYINCREAMENTEmployeeDetail=Increamentobj,
                                Salary_title_id=TitleID,
                                PresentSal=PresentSal,
                                RevisedSal=RevisedSal,
                                OrganizationID=OrganizationID,
                                CreatedBy=UserID
                            )
                        # salaryupdate = UpdateEmployeeSalaryGridByIncreamnet(EmpID, Increamentobj, OrganizationID, UserID)
                        UpdateEmployeeSalaryGridByIncreamnet(EmpID, Increamentobj, OrganizationID, UserID)

                else:
                   
                    Increamentobj = LETTEROFSALARYINCREAMENTEmployeeDetail.objects.create(
                        emp_code=emp_code,
                        prefix=prefix,
                        first_name=first_name,
                        last_name=last_name,
                        department=department,
                        designation=designation,
                        CTC   = CTC,
                        date_of_salary_increament = date_of_salary_increament,
                     
                        Issuing_manager_name=Issuing_manager_name,
                        Issuing_designation=Issuing_designation,
                        CreatedBy  = UserID,OrganizationID = OrganizationID
                     )
                    PreviousSalHistory = SalaryHistory.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID=EmpID).order_by('-id').first()
                    if PreviousSalHistory:
                         PreviousSalHistory.Effective_to = date_of_salary_increament
                         PreviousSalHistory.ModifyBy =  UserID
                         PreviousSalHistory.save()
		
                    
                         
                    FromSalary =   EmpDetails.CTC
                    ToSalary = CTC
                    SalaryHistoryobj = SalaryHistory.objects.create(EmpID=EmpID,Effective_from = date_of_salary_increament,OrganizationID = OrganizationID,FromSalary=FromSalary,ToSalary=ToSalary,SalaryID=Increamentobj.id)


                    Total_Title = request.POST['Total_Title']
                    for i in range(int(Total_Title) + 1):
                        TitleID = request.POST[f'TitleID_{i}']
                        PresentSal = request.POST[f'PresentEmoluments_{i}']
                        RevisedSal = request.POST[f'RevisedSalary_{i}']

                        salaryObj = IncreamentSalaryDetails.objects.create(
                                LETTEROFSALARYINCREAMENTEmployeeDetail=Increamentobj,
                                Salary_title_id=TitleID,
                                PresentSal=PresentSal,
                                RevisedSal=RevisedSal,
                                OrganizationID=OrganizationID,
                                CreatedBy=UserID
                            )  

                    # salaryupdate = UpdateEmployeeSalaryGridByIncreamnet(EmpID, Increamentobj, OrganizationID, UserID)
                    UpdateEmployeeSalaryGridByIncreamnet(EmpID, Increamentobj, OrganizationID, UserID)
                if Page:
                     return redirect('emplistlsi')
                
                Success = True        
                encrypted_id = encrypt_id(EmpID)
                url = reverse('EmployeeLetters')  
                redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
                return redirect(redirect_url)
        
    context  = {
        'Increamentobj':Increamentobj,
        'ManagerNames':ManagerNames,
        'HRManagerNames':HRManagerNames,
        'Designations':Designations,
        'SalaryTitles':SalaryTitles
    }
    return  render(request,"letterse/entryemp.html",context)




from app.views import OrganizationList

import inflect 
def emplist(request):
  
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    UserType = request.session.get("UserType")

    OrganizationID =request.session["OrganizationID"]
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
    
    IncreamentLetters = LETTEROFSALARYINCREAMENTEmployeeDetail.objects.filter(IsDelete=False,OrganizationID= I).annotate(
        EmpID=emp_id_subquery
    ).order_by('-CreatedDateTime','-ModifyDateTime').values()
    context  = { 'IncreamentLetters':IncreamentLetters,'memOrg':memOrg,'I':I}
    return render(request,"letterse/emplist.html",context)

from app.models import OrganizationMaster
# For generate_appointment_letter
def generate_Letter_of_Salary_Increment(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID =request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID   
     HotelName = ''
     if OrganizationMaster:
          hotelobj = OrganizationMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).first()
          if hotelobj:
               HotelName = hotelobj.OrganizationName
               

     head = True

     if 'head' in request.GET:
            head = request.GET.get('head') 
     print('head = ',head)   
   
     
     id = request.GET["LOI_ID"]
     EmpID =  request.GET["EmpID"]


     template_path = "letterse/lsiview.html"
    # NileLogo=MasterAttribute.NileLogo
    
     get_data = LETTEROFSALARYINCREAMENTEmployeeDetail.objects.get(id=id)
     editor = LETTEROFSALARYINCREAMENT.objects.filter(
        OrganizationID=OrganizationID,
        user=1
     )

     if not editor.exists():
        editor = LETTEROFSALARYINCREAMENT.objects.filter(user=1)


     if editor.exists():
        data_field = editor[0].data
        get_data.data = data_field
        get_data.save() 
     
     
  
     get_data.date_of_salary_increament = get_data.date_of_salary_increament.strftime('%d/%m/%y')
     get_data.data=get_data.data.replace("@@date_of_salary_increament@@",str(get_data.date_of_salary_increament))
     
     get_data.data=get_data.data.replace("@@prefix@@",get_data.prefix)
     get_data.data=get_data.data.replace("@@firstname@@",get_data.first_name)
     get_data.data=get_data.data.replace("@@lastname@@",get_data.last_name)
     
     get_data.data=get_data.data.replace("@@Designation@@",get_data.designation)
     get_data.data=get_data.data.replace(" @@HotelName@@",HotelName)

     
     
     get_data.data=get_data.data.replace("@@Department@@",get_data.department)
     your_number=get_data.CTC
     p = inflect.engine()

    # Convert the number to the Indian number format
     text_number = p.number_to_words(your_number, andword="and", zero="zero").replace(",", "")

     get_data.data=get_data.data.replace("@@CTC@@",your_number)
     get_data.data=get_data.data.replace("@@CTC_Word@@",text_number)
     

     get_data.data=get_data.data.replace("@@Issuing_manager_name@@",get_data.Issuing_manager_name)
     get_data.data=get_data.data.replace("@@Issuing_designation@@",get_data.Issuing_designation)

     
   
     
     
     
     
     od =OrganizationDetail(get_data.OrganizationID)
     OLogo=od.get_OrganizationLogo()
     if od.get_MComLogo()==1:
        NileLogo=MasterAttribute.NileLogoURL
      
    
     SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=False, OrganizationID=OID).order_by('TypeOrder', 'TitleOrder')
     s = "" 

        
     s = '<div ></div> <h1 style="text-align:center"></h1><table id="tblSal" style="width:100%;" class="table table-bordered"> <thead><tr style="background-color:#E9E3D6"><th style="background-color:#F6F1E4">Components</th><th style="background-color:#F6F1E4" align="center">Present Emoluments</th><th style="background-color:#F6F1E4" align="center">Revised Salary</th></tr></thead><tbody>'

       
    #  for salary in SalaryTitles:
    #         salary.PresentEmoluments = 0
    #         salary.RevisedSalary = 0
            
    #         if EmpID:
    #             sd = IncreamentSalaryDetails.objects.filter(IsDelete=False, LETTEROFSALARYINCREAMENTEmployeeDetail  = get_data, Salary_title_id=salary.id, OrganizationID=OrganizationID)
    #             if sd.exists():
    #                 salary.PresentEmoluments = sd[0].PresentSal
    #                 salary.RevisedSalary = sd[0].RevisedSal
                
             
    #             if sd[0].Salary_title.IsBold:
    #                 s += "<tr style='background-color:#F5F5F6'><td width='250px'>{}</td><td align='right'>{}</td><td align='right'>{}</td></tr>".format(
    #                     salary.Title, salary.PresentEmoluments, salary.RevisedSalary
    #                 )
    #             else:
    #                 s += "<tr><td>{}</td><td align='right'>{}</td><td align='right'>{}</td></tr>".format(
    #                     salary.Title, salary.PresentEmoluments, salary.RevisedSalary
    #                 )
     for salary in SalaryTitles:
        salary.PresentEmoluments = 0
        salary.RevisedSalary = 0

        if EmpID:
            sd = IncreamentSalaryDetails.objects.filter(
                IsDelete=False,
                LETTEROFSALARYINCREAMENTEmployeeDetail=get_data,
                Salary_title_id=salary.id,
                OrganizationID=OrganizationID
            )
            if sd.exists():
                salary.PresentEmoluments = sd[0].PresentSal
                salary.RevisedSalary = sd[0].RevisedSal

                if sd[0].Salary_title.IsBold:
                    s += "<tr style='background-color:#F5F5F6'><td width='250px'>{}</td><td align='right'>{}</td><td align='right'>{}</td></tr>".format(
                        salary.Title, salary.PresentEmoluments, salary.RevisedSalary
                    )
                else:
                    s += "<tr><td>{}</td><td align='right'>{}</td><td align='right'>{}</td></tr>".format(
                        salary.Title, salary.PresentEmoluments, salary.RevisedSalary
                    )
            else:
                # Handle the case where there is no matching record in IncreamentSalaryDetails
                s += "<tr><td>{}</td><td align='right'>{}</td><td align='right'>{}</td></tr>".format(
                    salary.Title, salary.PresentEmoluments, salary.RevisedSalary
                )


      
     s += "</tbody></table>"
     header=""
     if head == True:
            header='<table class="noborder" width="100%"><tr><td  align="left"> <img height="150px" src="'+OLogo+'"/> </td> <td  align="center" valign="bottom"></td> <td  align="right"><img src="'+NileLogo+'"  height="150px"/></td></tr></table>'
     

       
     get_data.data = get_data.data.replace("@@SalaryDetails@@", s)

     mydict={'Ed':get_data,'header':header}

    # context = {'myvar': 'this is your template context','p':varM}

    # Create a Django response object, and specify content_type as pdf
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'filename="report gcc club.pdf"'
    # find the template and render it.
     template = get_template(template_path)
     html = template.render(mydict)
     result = BytesIO()
  
     pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
      
     if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
     return None










def upload_file(request):
    EmpID = request.GET.get('EmpID')
    OID  = request.GET.get('OID')
    Page = request.GET.get('Page')

    if OID:
            OrganizationID= OID   
    id = request.GET.get('LOI_ID')
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix

        new_file = upload_file_to_blob(file,id)
        if not new_file:
            messages.warning(request, f"{ext} not allowed only accept {', '.join(ext.lower()for ext in ALLOWED_EXTENTIONS)} ")
            return render(request, "letterse/upload_file.html", {}) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()
        if Page:
                     return redirect('emplistlsi')
        Success = 'Uploaded'        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('EmployeeLetters')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
        return redirect(redirect_url)
   
    return render(request, "letterse/upload_file.html")






def download_file(request):
    id = request.GET.get('LOI_ID')
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID   

    file = LETTEROFSALARYINCREAMENTEmployeeDetail.objects.get(pk=id)
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
    id = request.GET.get('LOI_ID')    
    
    empdetail = LETTEROFSALARYINCREAMENTEmployeeDetail.objects.get(id=id)
    empdetail.IsDelete=True
    empdetail.ModifyBy = UserID
    empdetail.save()

    sal_history = SalaryHistory.objects.filter(
        OrganizationID=OrganizationID,
        IsDelete=False,
        EmpID=EmpID
    ).order_by('-Effective_from')
    for sal in sal_history:
         print(sal.Effective_from)
    if sal_history.exists() and sal_history.count() >= 2:
        last_sal_history = sal_history[0]
        last_sal_history.IsDelete = True
        last_sal_history.ModifyBy = UserID
        last_sal_history.save()

        second_last_sal_history = sal_history[1]
        second_last_sal_history.Effective_to = None
        second_last_sal_history.ModifyBy = UserID
        second_last_sal_history.save()

    
    
    Success = 'Deleted'        
    encrypted_id = encrypt_id(EmpID)
    url = reverse('EmployeeLetters')  
    redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
    return redirect(redirect_url)
    




def repalce_file(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID =request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    Page = request.GET.get('Page')

    if OID:
            OrganizationID= OID   
    UserID =str(request.session["UserID"])    
    id = request.GET.get('LOI_ID')
    EmpID = request.GET.get('EmpID')
    file = LETTEROFSALARYINCREAMENTEmployeeDetail.objects.get(pk=id)
    file_id = file.file_id
    file_name = file.file_name
    EmployeeDetail = LETTEROFSALARYINCREAMENTEmployeeDetail.objects.get(pk=id)
    
    deletefile = LETTEROFSALARYINCREAMENTDeletedFileofEmployee.objects.create(LETTEROFSALARYINCREAMENTEmployeeDetail= EmployeeDetail,file_id = file_id,file_name = file_name)
          
    file = LETTEROFSALARYINCREAMENTEmployeeDetail.objects.get(pk=id)
    file.file_name = None
    file.file_id = None
    file.ModifyBy  = UserID
    file.save()
    if Page:
                     return redirect('emplistlsi')
    Success = 'Deleted'        
    encrypted_id = encrypt_id(EmpID)
    url = reverse('EmployeeLetters')  
    redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
    return redirect(redirect_url)  
