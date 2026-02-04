from io import BytesIO
from django.db import connection
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
from django.core.mail import send_mail
from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail

def home_view(request):
    return render(request,'final/index.html')

from django.db.models import Subquery, OuterRef
from HumanResources.models import EmployeePersonalDetails
from HumanResources.views import OrganizationList


def EmpResigantionList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    UserType = request.session.get("UserType")
       
    OrganizationID =request.session["OrganizationID"]
    I  = request.GET.get('I',OrganizationID)
    if UserType == 'CEO' and request.GET.get('I') is None:
        I = 401
    memorg = OrganizationList(OrganizationID=OrganizationID)
    emp_id_subquery = Subquery(
        EmployeePersonalDetails.objects.filter(
            EmployeeCode=OuterRef('Emp_Code'),
            IsDelete=False
        ).values('EmpID')[:1]
    )
   
    Resigantions = EmpResigantionModel.objects.filter(OrganizationID=I,IsDelete=False).annotate(
        EmpID=emp_id_subquery)
    
    return render(request,"EmpResigantionTemp/EmpResigantionList.html",{'Resigantions':Resigantions,'memorg':memorg,'I':I})


# def EmpResigantionEntry(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
  
#     EmpResigantionForm=forms.EmpResigantionForm()
    
#     OrganizationID =request.session["OrganizationID"]
#     UserID =str(request.session["UserID"])
#     d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
#     mydict={'EmpResigantionForm':EmpResigantionForm,'d':d}
    
#     if request.method=='POST':
       
#         EmpResigantionForm=forms.EmpResigantionForm(request.POST)
            
#         ss=EmpResigantionForm.save(commit=False)
        
#         ss.save()
#         cursor = connection.cursor()
#         try:
#             EmpCode =request.POST["Emp_Code"]
#             sql = 'EXEC [dbo].[HR_SP_EmployeeMaster_Emp_Status_Update] @EmpCode=%s,@OrganizationID=%s, @Status=%s, @UserID=%s'
#             params = (EmpCode,OrganizationID, 'Resigned', UserID)
#             cursor.execute(sql, params)
#             print("test data1")
#         finally:
#             cursor.close()
#         od =OrganizationDetail(OrganizationID)
#         Orgnam=od.OrganizationName
#         subject = 'New Resignation  '+Orgnam
#         message =  ss.Name+" "+ss.Designation+" "+ss.Dept+"  has resigned from "+Orgnam+". "
#         from_email = 'info@hotelops.in'
#         DHeadEmail =  DivisonHeadEmail.objects.filter(Department=ss.Dept).first()
        
#         recipient_list = ['Ayesha@nilehospitality.com']
#         if   DHeadEmail:
#             recipient_list.append(DHeadEmail.Email)
          
            
#         print(recipient_list)
        
#         bcc_email = ['vishal@hotelops.in']
#         var =send_mail(subject, message, from_email, recipient_list)
#         print("email sent")
#         e = request.POST["E"]
#         print(e)
#         if e!='':
#                 EC = request.POST["Emp_Code"]
#                 O =  request.POST["OrganizationID"]
#                 od = OrganizationDetail(OrganizationID)
#                 DomainCode=od.get_OrganizationDomainCode()
#                 newd = MasterAttribute.CurrentHost.replace("http://hotelops.in","http://"+DomainCode+".hotelops.in")
#                 return redirect(newd+"/HR/Home/EmpProfile?E="+e+"&Q=empresigantion&EC="+EC+"&O="+O+"") 
         
        
#     return render(request,'EmpResigantionTemp/EmpResigantionEntry.html',context=mydict) 





# def EmpResigantionEdit(request):
    
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
    
#     if request.method=='POST':
#         id = request.POST["ID"]
#         book = get_object_or_404(EmpResigantionModel, pk=id)
#         EmpResigantionForm=forms.EmpResigantionForm(request.POST,instance=book)
#         #if EmpResigantionForm.is_valid():
#         # ss=EmpResigantionForm.save(commit=False)
#         EmpResigantionForm.save()
#         return HttpResponseRedirect('/EmpResignation/EmpResigantionList/')
#     else :
       
#        id = request.GET["id"]
   
#        get_data = EmpResigantionModel.objects.get(id=id)
       
#        EmpResigantionForm=forms.EmpResigantionForm(instance=get_data)
     
       
#        mydict={'EmpResigantionForm':EmpResigantionForm,'Ed':get_data}
#        return render(request,'EmpResigantionTemp/EmpResigantionEdit.html',context=mydict) 
 






from django.urls import reverse
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from HumanResources.views import EmployeeDetailsData,HrManagerNameandDesignation,ManagerNameandDesignation,EmployeeNameandDesignation,EmployeeNameonTheBasisofDepartment

# def EmpResigantionEntry(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
  
    
    
#     OrganizationID =request.session["OrganizationID"]
#     UserID =str(request.session["UserID"])
#     EmpCode  = request.GET.get('EC')
#     EmpID  = request.GET.get('EmpID')
#     RID = request.GET.get('RID')
   
#     EmployeeNames = EmployeeNameandDesignation(request,OrganizationID)
    
#     Resigantiontobj   = None
#     if EmpCode is not None:
#         if RID is not None:
#                Resigantiontobj = EmpResigantionModel.objects.filter(id = RID,Emp_Code = EmpCode,OrganizationID = OrganizationID,IsDelete=False).first()

    

#         if Resigantiontobj is not None:
#             DataFromResigantiontobj  = 'Resigantiontobj'
          
#         else:
         

#             DataFromResigantiontobj  = 'ResigantiontobjHR'
#             EmpDetails  = EmployeeDetailsData(EmpID,OrganizationID)
         

#             Resigantiontobj  =   {
#                                 'Emp_Code' : EmpDetails.EmployeeCode,
                              
#                                 'Name' : EmpDetails.FirstName + " " + EmpDetails.MiddleName + " " + EmpDetails.LastName,
                                
#                                 'Dept' : EmpDetails.Department,
#                                 'Designation' : EmpDetails.Designation,
#                                 'DOJ' : EmpDetails.DateofJoining,

#                                }
    
#     if request.method=='POST':
       
#         Name = request.POST.get('name')
#         Emp_Code = request.POST.get('emp_code')
#         Dept = request.POST.get('dept')
#         Designation = request.POST.get('designation')
#         Date_Of_res = request.POST.get('date_of_resignation')
#         TypeofRes = request.POST.get('TypeofRes')
#         NoticePeriod = request.POST.get('notice_period')
#         Res_Reason = request.POST.get('res_reason')
#         Ressubmittedto = request.POST.get('ressubmittedto')
#         LastWorkingDays = request.POST.get('last_working_day')
#         Res_acceptance_Date = request.POST.get('res_acceptance_date')
#         Res_acceptance_By = request.POST.get('res_acceptance_by')

     
       
#         if DataFromResigantiontobj == "Resigantiontobj" and RID:
                            
           
#                 Resigantiontobj.Name = Name
#                 Resigantiontobj.Dept = Dept
#                 Resigantiontobj.Designation = Designation
#                 Resigantiontobj.Date_Of_res = Date_Of_res
#                 Resigantiontobj.TypeofRes = TypeofRes
#                 Resigantiontobj.NoticePeriod = NoticePeriod
#                 Resigantiontobj.Res_Reason = Res_Reason
#                 Resigantiontobj.Ressubmittedto = Ressubmittedto
#                 Resigantiontobj.LastWorkingDays = LastWorkingDays
#                 Resigantiontobj.Res_acceptance_Date = Res_acceptance_Date
#                 Resigantiontobj.Res_acceptance_By = Res_acceptance_By
#                 Resigantiontobj.ModifyBy  = UserID
#                 Resigantiontobj.save()
#         else:
#            Resigantiontobj =  EmpResigantionModel.objects.create(
#                 Name=Name,
#                 Emp_Code=Emp_Code,
#                 Dept=Dept,
#                 Designation=Designation,
#                 DOJ=EmpDetails.DateofJoining,
#                 Date_Of_res=Date_Of_res,
#                 TypeofRes=TypeofRes,
#                 NoticePeriod=NoticePeriod,
#                 Res_Reason=Res_Reason,
#                 Ressubmittedto=Ressubmittedto,
#                 LastWorkingDays=LastWorkingDays,
#                 Res_acceptance_Date=Res_acceptance_Date,
#                 Res_acceptance_By=Res_acceptance_By,
#                 CreatedBy = UserID,
#                 OrganizationID = OrganizationID
#             )
       
       
#         Success = True        
#         encrypted_id = encrypt_id(EmpID)
#         url = reverse('Resigantion')  
#         redirect_url = f"{url}?EmpID={encrypted_id}&Success={Success}" 
#         return redirect(redirect_url) 
#     context = {'Resigantiontobj':Resigantiontobj,'EmployeeNames':EmployeeNames}    
#     return render(request,'EmpResigantionTemp/EmpResigantionEntry.html',context) 




from HumanResources.views import EmployeeDetailsData,HrManagerNameandDesignation,ManagerNameandDesignation,EmployeeNameandDesignation,EmployeeNameOnTheBasisofDesignation

from HumanResources.models import EmployeeWorkDetails
def EmpResigantionEntry(request):
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
    RID = request.GET.get('RID')
    Department  = request.GET.get('DepartmentName')

    Page  = request.GET.get('Page')
    
 
    EmployeeNames = EmployeeNameonTheBasisofDepartment(Department, OrganizationID)
   
    # EmployeeNameOnTheBasisofDesignation
    Resigantiontobj = None
 
    if EmpCode is not None:
        if RID is not None:
            Resigantiontobj = EmpResigantionModel.objects.filter(
                id=RID, Emp_Code=EmpCode, OrganizationID=OrganizationID, IsDelete=False).first()
 
        if Resigantiontobj is not None:
            DataFromResigantiontobj = 'Resigantiontobj'
        else:
            DataFromResigantiontobj = 'ResigantiontobjHR'
            EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
            # EmpDetails = Get_Employee_Master_Data(EmpID, OrganizationID)
            
 
            Resigantiontobj = {
                'Emp_Code': EmpDetails.EmployeeCode,
                'Name': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
                'Dept': EmpDetails.Department,
                'Designation': EmpDetails.Designation,
                'DOJ': EmpDetails.DateofJoining,
                'LastEmpStatus': EmpDetails.EmpStatus,
                'Level': EmpDetails.Level,
            }
            print("Employee Level is here::", EmpDetails.Level)
 
    if request.method == 'POST':
        Name = request.POST.get('name')
        Emp_Code = request.POST.get('emp_code')
        Dept = request.POST.get('dept')
        Designation = request.POST.get('designation')
        Date_Of_res = request.POST.get('date_of_resignation')
        TypeofRes = request.POST.get('TypeofRes')
        NoticePeriod = request.POST.get('notice_period')
        Res_Reason = request.POST.get('res_reason')
        Ressubmittedto = request.POST.get('ressubmittedto')
        LastWorkingDays = request.POST.get('last_working_day')
        Res_acceptance_Date = request.POST.get('res_acceptance_date')
        Res_acceptance_By = request.POST.get('res_acceptance_by')
        LastEmpStatus = request.POST.get('LastEmpStatus')
        ResignationRevoke = request.POST.get('ResignationRevoke')
        Level = request.POST.get('Level')
        
        IsRevoke = False
        if ResignationRevoke == "Revoke":
            IsRevoke = True
            
        if DataFromResigantiontobj == "Resigantiontobj" and RID:
            Resigantiontobj.Name = Name
            Resigantiontobj.Dept = Dept
            Resigantiontobj.Designation = Designation
            Resigantiontobj.Date_Of_res = Date_Of_res
            Resigantiontobj.LastEmpStatus = LastEmpStatus
            Resigantiontobj.IsRevoke = IsRevoke


            Resigantiontobj.TypeofRes = TypeofRes
            Resigantiontobj.NoticePeriod = NoticePeriod
            Resigantiontobj.Res_Reason = Res_Reason
            
            Resigantiontobj.Ressubmittedto = Ressubmittedto
            Resigantiontobj.Res_acceptance_By = Res_acceptance_By

            Resigantiontobj.LastWorkingDays = LastWorkingDays
            Resigantiontobj.Level = Level
            Resigantiontobj.Res_acceptance_Date = Res_acceptance_Date
            Resigantiontobj.ModifyBy = UserID
            Resigantiontobj.ModifyDateTime = date.today()

            Resigantiontobj.save()

            employee_work_details = EmployeeWorkDetails.objects.get(
                        EmpID=EmpID, 
                        OrganizationID=OrganizationID, 
                        IsDelete=False,
                        IsSecondary=False
            )
            employee_work_details.EmpStatus = "Resigned"
            employee_work_details.ModifyBy = UserID
            employee_work_details.ModifyDateTime = date.today()

        
            employee_work_details.save()
            if IsRevoke == True:

                try:
                    employee_work_details = EmployeeWorkDetails.objects.get(
                        EmpID=EmpID, 
                        OrganizationID=OrganizationID, 
                        IsDelete=False,
                        IsSecondary=False
                    )
                    employee_work_details.EmpStatus = Resigantiontobj.LastEmpStatus
                    employee_work_details.ModifyBy = UserID
                    employee_work_details.ModifyDateTime = date.today()

                
                    employee_work_details.save()
                except EmployeeWorkDetails.DoesNotExist:
                    print("EmployeeWorkDetails record not found.")
        else:
            Resigantiontobj = EmpResigantionModel.objects.create(
                Name=Name,
                Emp_Code=Emp_Code,
                Dept=Dept,
                Designation=Designation,
                DOJ=EmpDetails.DateofJoining,
                LastEmpStatus= LastEmpStatus,
                Date_Of_res=Date_Of_res,
                TypeofRes=TypeofRes,
                NoticePeriod=NoticePeriod,
                Res_Reason=Res_Reason,
                Ressubmittedto=Ressubmittedto,
                LastWorkingDays=LastWorkingDays,
                Res_acceptance_Date=Res_acceptance_Date,
                Level=Level,
                Res_acceptance_By=Res_acceptance_By,
                CreatedBy=UserID,
                OrganizationID=OrganizationID
            )
 
       
            try:
                employee_work_details = EmployeeWorkDetails.objects.get(
                    EmpID=EmpID, 
                    OrganizationID=OrganizationID, 
                    IsDelete=False,
                    IsSecondary=False
                )
                employee_work_details.EmpStatus = "Resigned"
                employee_work_details.ModifyBy = UserID
                employee_work_details.ModifyDateTime = date.today()

            
                employee_work_details.save()
            except EmployeeWorkDetails.DoesNotExist:
                print("EmployeeWorkDetails record not found.")
        if Page:
            return redirect('EmpResigantionList')
        
        Success = True
        encrypted_id = encrypt_id(EmpID)
        url = reverse('Resigantion')
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}"
        return redirect(redirect_url)
 
    context = {
        'Resigantiontobj': Resigantiontobj, 
        'EmployeeNames': EmployeeNames
    }
    return render(request, 'EmpResigantionTemp/EmpResigantionEntry.html', context)
 


def EmpResigantionDelete(request):
       if 'OrganizationID' not in request.session:
           return redirect(MasterAttribute.Host)
       else:
            print("Show Page Session")
       OrganizationID =request.session["OrganizationID"]
       OID  = request.GET.get('OID')
       if OID:
            OrganizationID= OID
       UserID =str(request.session["UserID"])
       id = request.GET["RID"]
       EmpCode  = request.GET.get('EC')
       EmpID  = request.GET.get('EmpID')
       
       Final = EmpResigantionModel.objects.filter(id=id,OrganizationID=OrganizationID,IsDelete=False).first()
       Final.IsDelete = True
       Final.ModifyBy = UserID
       Final.ModifyDateTime =date.today()

       Final.save()
       Success = 'Deleted'        
       encrypted_id = encrypt_id(EmpID)
       url = reverse('Resigantion')  
       redirect_url = f"{url}?EmpID={encrypted_id}&Success={Success}" 
       return redirect(redirect_url)   
   
   
from app.models import OrganizationMaster   
def EmpResigantionPDF(request):
     if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
          OrganizationID= OID
     UserID = str(request.session["UserID"])  
    
    
     id = request.GET["RID"]
     base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
     organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
     organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
     organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
     organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
    
     template_path = "EmpResigantionTemp/EmpResigantionView.html"
     get_data =EmpResigantionModel.objects.get(id=id)
    
     
    
     mydict={'Ed':get_data, 'organization_logos':organization_logos,
        'organization_logo':organization_logo,
             
             }

    
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'filename="report gcc club.pdf"'
     template = get_template(template_path)
     html = template.render(mydict)

     result = BytesIO()
     pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
     return None 