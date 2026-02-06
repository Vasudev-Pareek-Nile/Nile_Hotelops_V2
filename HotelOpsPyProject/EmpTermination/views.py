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


def home_view(request):
    return render(request,'final/index.html')

from app.views import OrganizationList
from django.db.models import Subquery, OuterRef
from HumanResources.models import EmployeePersonalDetails
from app.Global_Api import get_organization_list

#For Showing List Of the Equipment Trolley Inventory  
def EmpTerminationList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
       
    UserType = request.session.get("UserType")

    OrganizationID =request.session["OrganizationID"]
    I = request.GET.get('I',OrganizationID)

    # if UserType == 'CEO' and request.GET.get('I') is None:
    #     I = 401

    memorg = get_organization_list(OrganizationID)
    
    emp_id_subquery = Subquery(
        EmployeePersonalDetails.objects.filter(
            EmployeeCode=OuterRef('Emp_Code'),
            IsDelete=False
        ).values('EmpID')[:1]
    )

    if I == 'all':
        Terminations = EmpTerminationModel.objects.filter(IsDelete=False).annotate(EmpID=emp_id_subquery)
    else:
        Terminations = EmpTerminationModel.objects.filter(OrganizationID=I,IsDelete=False).annotate(EmpID=emp_id_subquery)
    
    return render(request,"EmpTerminationTemp/EmpTerminationList.html",{'Terminations':Terminations,'memorg':memorg,'I':I})




# # Inserting Equipment Trolley Inventory Form
# def EmpTerminationEntry(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
  
#     EmpTerminationForm=forms.EmpTerminationForm()
    
#     OrganizationID =request.session["OrganizationID"]
#     UserID =str(request.session["UserID"])
#     d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
#     mydict={'EmpTerminationForm':EmpTerminationForm,'d':d}
    
#     if request.method=='POST':
#         print("EmpTerminationEntry Post")
#         EmpTerminationForm=forms.EmpTerminationForm(request.POST)
#         #if EmpTerminationForm.is_valid():
            
#         ss=EmpTerminationForm.save(commit=False)
        
#         ss.save()
#         cursor = connection.cursor()
#         try:
#             EmpCode =request.POST["Emp_Code"]
#             sql = 'EXEC [dbo].[HR_SP_EmployeeMaster_Emp_Status_Update] @EmpCode=%s,@OrganizationID=%s, @Status=%s, @UserID=%s'
#             params = (EmpCode,OrganizationID, 'Terminate', UserID)
#             cursor.execute(sql, params)
#             print("test data1")
#         finally:
#             cursor.close()
#         return HttpResponseRedirect('/EmpTermination/EmpTerminationList')
#     return render(request,'EmpTerminationTemp/EmpTerminationEntry.html',context=mydict) 


# #For Editing The Equipment Trolley Inventory List
# def EmpTerminationEdit(request):
    
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
    
#     if request.method=='POST':
#         id = request.POST["ID"]
#         book = get_object_or_404(EmpTerminationModel, pk=id)
#         EmpTerminationForm=forms.EmpTerminationForm(request.POST,instance=book)
#         #if EmpTerminationForm.is_valid():
#         # ss=EmpTerminationForm.save(commit=False)
#         EmpTerminationForm.save()
#         return HttpResponseRedirect('/EmpTermination/EmpTerminationList/')
#     else :
       
#        id = request.GET["id"]
   
#        get_data = EmpTerminationModel.objects.get(id=id)
       
#        EmpTerminationForm=forms.EmpTerminationForm(instance=get_data)
     
       
#        mydict={'EmpTerminationForm':EmpTerminationForm,'Ed':get_data}
#        return render(request,'EmpTerminationTemp/EmpTerminationEdit.html',context=mydict) 






from django.urls import reverse
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from HumanResources.views import EmployeeDetailsData,HrManagerNameandDesignation,ManagerNameandDesignation,EmployeeNameandDesignation


# def EmpTerminationEntry(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
    
#     OrganizationID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])
#     EmpCode = request.GET.get('EC')
#     EmpID = request.GET.get('EmpID')
#     TID = request.GET.get('TID')
    
#     EmployeeNames = EmployeeNameandDesignation(request, OrganizationID)
#     Terminationstobj = None

#     if EmpCode is not None:
#         if TID is not None:
#             Terminationstobj = EmpTerminationModel.objects.filter(id=TID, Emp_Code=EmpCode, OrganizationID=OrganizationID, IsDelete=False).first()
#             print(Terminationstobj.Remarks)
#         if Terminationstobj is not None:
#             DataFromTerminationstobj = 'Terminationstobj'
#         else:
#             DataFromTerminationstobj = 'TerminationstobjHR'
#             EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
            
#             Terminationstobj = {
#                 'Emp_Code': EmpDetails.EmployeeCode,
#                 'Name': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
#                 'Dept': EmpDetails.Department,
#                 'Designation': EmpDetails.Designation,
#                 'DOJ': EmpDetails.DateofJoining,
#             }
    
#     if request.method == 'POST':
#         Name = request.POST.get('name')
#         Emp_Code = request.POST.get('emp_code')
#         Dept = request.POST.get('dept')
#         Designation = request.POST.get('designation')
#         Date_Of_Termination = request.POST.get('date_of_termination')
#         IsWarningIssued = request.POST.get('is_warning_issued')
#         LastWarningLatter = request.POST.get('last_warning_letter')
#         Remarks = request.POST.get('remarks')

#         if DataFromTerminationstobj == "Terminationstobj" and TID:
#             Terminationstobj.Name = Name
#             Terminationstobj.Dept = Dept
#             Terminationstobj.Designation = Designation
#             Terminationstobj.Date_Of_Termination = Date_Of_Termination
#             Terminationstobj.IsWarningIssued = IsWarningIssued
#             Terminationstobj.LastWarningLatter = LastWarningLatter
#             Terminationstobj.Remarks = Remarks
#             Terminationstobj.ModifyBy = UserID
#             Terminationstobj.ModifyDateTime = date.today()
#             Terminationstobj.save()
#         else:
#             Terminationstobj = EmpTerminationModel.objects.create(
#                 Name=Name,
#                 Emp_Code=Emp_Code,
#                 Dept=Dept,
#                 Designation=Designation,
#                 DOJ=EmpDetails.DateofJoining,  
#                 Date_Of_Termination=Date_Of_Termination,
#                 IsWarningIssued=IsWarningIssued,
#                 LastWarningLatter=LastWarningLatter,
#                 Remarks=Remarks,
#                 OrganizationID=OrganizationID,
#                 CreatedBy=UserID,
#                 CreatedDateTime=date.today(),
#             )
        
#         Success = True        
#         encrypted_id = encrypt_id(EmpID)
#         url = reverse('Termination')  
#         redirect_url = f"{url}?EmpID={encrypted_id}&Success={Success}" 
#         return redirect(redirect_url)
   
#     context = {
#         'Terminationstobj': Terminationstobj,
#         'EmployeeNames': EmployeeNames
#     }
#     return render(request, 'EmpTerminationTemp/EmpTerminationEntry.html', context)


from HumanResources.models import EmployeeWorkDetails
 
from django.urls import reverse
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from HumanResources.views import EmployeeDetailsData,HrManagerNameandDesignation,ManagerNameandDesignation,EmployeeNameandDesignation,EmployeeNameOnTheBasisofDesignation
def EmpTerminationEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
   
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID = str(request.session["UserID"])
    EmpCode = request.GET.get('EC')
    EmpID = request.GET.get('EmpID')
    TID = request.GET.get('TID')
    DepartmentName = request.GET.get('DepartmentName')
    Page = request.GET.get('Page')

    
    ManagerNames =  EmployeeNameOnTheBasisofDesignation(DepartmentName,OrganizationID)
    # ManagerNames  = ManagerNameandDesignation(request,OrganizationID)
    
    
    HRManagerNames  = HrManagerNameandDesignation(request,OrganizationID)
    
    
    EmployeeNames = EmployeeNameandDesignation(request, OrganizationID)



    Terminationstobj = None
 
    if EmpCode is not None:
        if TID is not None:
            Terminationstobj = EmpTerminationModel.objects.filter(id=TID, Emp_Code=EmpCode, OrganizationID=OrganizationID, IsDelete=False).first()
        if Terminationstobj is not None:
            DataFromTerminationstobj = 'Terminationstobj'
        else:
            DataFromTerminationstobj = 'TerminationstobjHR'
            EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
           
            Terminationstobj = {
                'Emp_Code': EmpDetails.EmployeeCode,
                'Name': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
                'Dept': EmpDetails.Department,
                'Designation': EmpDetails.Designation,
                'DOJ': EmpDetails.DateofJoining,
            }
   
    if request.method == 'POST':
        Name = request.POST.get('name')
        Emp_Code = request.POST.get('emp_code')
        Dept = request.POST.get('dept')
        Designation = request.POST.get('designation')
        Date_Of_Termination = request.POST.get('date_of_termination')
        IsWarningIssued = request.POST.get('is_warning_issued')
        LastWarningLatter = request.POST.get('last_warning_letter')
        Remarks = request.POST.get('remarks')
        reviewed_manager_name = request.POST['reviewed_manager_name']
        reviewed_designation = request.POST['reviewed_designation']
        if DataFromTerminationstobj == "Terminationstobj" and TID:
            Terminationstobj.Name = Name
            Terminationstobj.Dept = Dept
            Terminationstobj.Designation = Designation
            Terminationstobj.Date_Of_Termination = Date_Of_Termination
            Terminationstobj.IsWarningIssued = IsWarningIssued
            Terminationstobj.LastWarningLatter = LastWarningLatter
            Terminationstobj.Remarks = Remarks
            Terminationstobj.reviewed_manager_name=reviewed_manager_name
            Terminationstobj.reviewed_designation=reviewed_designation
            Terminationstobj.ModifyBy = UserID
            Terminationstobj.ModifyDateTime = date.today()
            Terminationstobj.save()
        else:
            Terminationstobj = EmpTerminationModel.objects.create(
                Name=Name,
                Emp_Code=Emp_Code,
                Dept=Dept,
                Designation=Designation,
                DOJ=EmpDetails.DateofJoining,  
                Date_Of_Termination=Date_Of_Termination,
                IsWarningIssued=IsWarningIssued,
                LastWarningLatter=LastWarningLatter,
                Remarks=Remarks,
                reviewed_manager_name=reviewed_manager_name,
                reviewed_designation=reviewed_designation,
                OrganizationID=OrganizationID,
                CreatedBy=UserID,
                CreatedDateTime=date.today(),
            )
            try:
                employee_work_details = EmployeeWorkDetails.objects.get(
                    EmpID=EmpID, OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False)
                employee_work_details.EmpStatus = "Terminate"
                employee_work_details.ModifyBy = UserID
            
                employee_work_details.save()
            except EmployeeWorkDetails.DoesNotExist:
                print("EmployeeWorkDetails record not found.")
        if Page:
            return redirect('EmpTerminationList')
        
        Success = True        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('Termination')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}"
        return redirect(redirect_url)
   
    context = {
        'Terminationstobj': Terminationstobj,
        'EmployeeNames': EmployeeNames,
        'ManagerNames':ManagerNames,'HRManagerNames':HRManagerNames
    }
    return render(request, 'EmpTerminationTemp/EmpTerminationEntry.html', context)
   

       
def EmpTerminationDelete(request):
       if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
    
       OrganizationID = request.session["OrganizationID"]
       UserID = str(request.session["UserID"])
       EmpCode = request.GET.get('EC')
       EmpID = request.GET.get('EmpID')
       id = request.GET["TID"]
  
       Final = EmpTerminationModel.objects.get(id=id)
       Final.IsDelete=True
       Final.ModifyBy = UserID
       Final.save()
       Success = 'Deleted'        
       encrypted_id = encrypt_id(EmpID)
       url = reverse('Termination')  
       redirect_url = f"{url}?EmpID={encrypted_id}&Success={Success}" 
       return redirect(redirect_url) 
   
from app.models  import OrganizationMaster
def EmpTerminationPDF(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID
     UserID = str(request.session["UserID"])
    
     id = request.GET["TID"]
     base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
     organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
     organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
     organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
     organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
    
    
     template_path = "EmpTerminationTemp/EmpTerminationView.html"
     get_data =EmpTerminationModel.objects.get(id=id)

     
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