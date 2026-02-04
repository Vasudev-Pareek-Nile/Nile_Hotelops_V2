from django.shortcuts import render,redirect
from .models import *
from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail
from django.shortcuts import render
from hashlib import new
from pathlib import Path
import mimetypes
from django.contrib import messages
from .azure import upload_file_to_blob,ALLOWED_EXTENTIONS,download_blob
from io import BytesIO
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,Http404
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from .models import PromotionLetter,PromotionLetterDeletedFileofEmployee,PromotionLetterEmployeeDetail,PromotionSalaryDetails
from xhtml2pdf import pisa
from django.template.loader import get_template
from HumanResources.views import ManagerNameandDesignation,HrManagerNameandDesignation,EmployeeDetailsData,UpdateEmployeeDesignation,UpdateEmployeeSalaryGridByPromotion,HrNameOnTheBasisofDesignation,EmployeeNameOnTheBasisofDesignation, Salary_Details_Effective
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from django.urls import reverse
from Manning_Guide.models import OnRollDesignationMaster
from HumanResources.models import Salary_Detail_Master,SalaryTitle_Master,EmployeeWorkDetails,DesignationHistory,SalaryHistory,EmployeePersonalDetails

from django.db.models import Subquery, OuterRef


def get_latest_effective_salary(emp_id, org_id):
    record = Salary_Details_Effective.objects.filter(
        EmpID=emp_id,
        OrganizationID=org_id,
        IsDelete=False
    ).order_by('-EffectiveFrom').first()

    if not record:
        raise ValueError("No effective salary found")

    return record


# For Adding Emp Details
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
    Page = request.GET.get('Page')
    

    LOP_ID = request.GET.get('LOP_ID')
    PreviousSalary = False
    DepartmentName = request.GET.get('DepartmentName')
    ManagerNames  = EmployeeNameOnTheBasisofDesignation(DepartmentName,OrganizationID)
    HRManagerNames  = HrNameOnTheBasisofDesignation(OrganizationID)

    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    if LOP_ID:
        if EmpID != '':
            CTCEmpDetails  = EmployeeDetailsData(EmpID,OrganizationID)  
        else:
            EmpIDobj  = EmployeePersonalDetails.objects.filter(OrganizationID=OrganizationID,EmployeeCode=EmpCode,IsDelete=False).first()
            if EmpIDobj:
                EmpID = EmpIDobj.EmpID
                CTCEmpDetails  = EmployeeDetailsData(EmpIDobj.EmpID,OrganizationID)  

    
    Promotionobj   = None
    if EmpCode is not None:
        if LOP_ID is not None:
            Promotionobj = PromotionLetterEmployeeDetail.objects.filter(id = LOP_ID,emp_code = EmpCode,OrganizationID = OrganizationID,IsDelete=False).first()
        
            if Promotionobj:
                if Promotionobj.PWI == False:
                    PreviousSalary  = True
                        
            DesHistory  = DesignationHistory.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID=EmpID,PromotionID=LOP_ID).first()
            SalHistory  = SalaryHistory.objects.filter(OrganizationID=OID,IsDelete=False,EmpID=EmpID,SalaryID=LOP_ID).first()


        if Promotionobj is not None:
            DataFromPromotionobj  = 'Promotionobj'
            SalaryTitles  = SalaryTitle_Master.objects.filter(IsDelete=False, OrganizationID=OID).order_by('TypeOrder','TitleOrder')
            for salary in SalaryTitles:
                SC = PromotionSalaryDetails.objects.filter(IsDelete=False,Salary_title_id = salary.id,PromotionLetterEmployeeDetail=Promotionobj,OrganizationID=OrganizationID)
                if SC.exists():
                        salary.PresentEmoluments = SC[0].PresentSal
                        salary.RevisedSalary = SC[0].RevisedSal

        else:
            DataFromPromotionobj  = 'PromotionobjHR'
            EmpDetails  = EmployeeDetailsData(EmpID,OrganizationID)

            Effective_Obj = get_latest_effective_salary(EmpID, OID)
            
            SalaryTitles  = SalaryTitle_Master.objects.filter(IsDelete=False, OrganizationID=OID).order_by('TypeOrder','TitleOrder')
            for salary in SalaryTitles:
                salary.PresentEmoluments = 0
                salary.RevisedSalary = 0
            
                SC = Salary_Detail_Master.objects.filter(Effective=Effective_Obj, IsDelete=False,EmpID=EmpID, Salary_title_id = salary.id,OrganizationID=OID)
                if SC.exists():
                        salary.PresentEmoluments = SC[0].Permonth
         

            Promotionobj  =   {
                'emp_code' : EmpDetails.EmployeeCode,
                'prefix' : EmpDetails.Prefix,
                # 'first_name' : EmpDetails.FirstName + EmpDetails.MiddleName or '',
                'first_name': (EmpDetails.FirstName + " " + EmpDetails.MiddleName) if EmpDetails.MiddleName else EmpDetails.FirstName,
                'last_name' : EmpDetails.LastName,
                'department' : EmpDetails.Department,
                'designation' : EmpDetails.Designation,
                'Promotiondesignation':EmpDetails.Designation,
            }

        if PreviousSalary == True:
            Effective_Obj =  get_latest_effective_salary(EmpID, OID)
            
            SalaryTitles  = SalaryTitle_Master.objects.filter(IsDelete=False, OrganizationID=OID).order_by('TypeOrder','TitleOrder')
            for salary in SalaryTitles:
                salary.PresentEmoluments = 0
                salary.RevisedSalary = 0
            
                SC = Salary_Detail_Master.objects.filter(Effective=Effective_Obj, IsDelete=False,EmpID=EmpID, Salary_title_id = salary.id,OrganizationID=OID)
                if SC.exists():
                    salary.PresentEmoluments = SC[0].Permonth
                 
                 
        if request.method == "POST":
            emp_code = request.POST['emp_code']
            prefix = request.POST['prefix']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            Promotiondesignation  = request.POST['promotion_designation']
            Promotiondepartment = request.POST['promotion_department']
            date_of_promtion  = request.POST['date_of_promotion']
            CTC = request.POST['CTC']
            PWI = request.POST.get('PWI')

            PWIStatus = True if PWI == 'P' else False
            
            department = request.POST['department']
            designation = request.POST['designation']
            
            Issuing_manager_name = request.POST['Issuing_manager_name']
            Issuing_designation = request.POST['Issuing_designation']
            
            if DataFromPromotionobj == "Promotionobj" and LOP_ID:
                Promotionobj.emp_code = emp_code
                Promotionobj.prefix = prefix
                Promotionobj.first_name = first_name
                Promotionobj.last_name = last_name
                Promotionobj.department = department
                Promotionobj.designation = designation
                Promotionobj.date_of_promtion  = date_of_promtion
                Promotionobj.Promotiondesignation  = Promotiondesignation
                Promotionobj.Promotiondepartment  = Promotiondepartment

                Promotionobj.Issuing_manager_name = Issuing_manager_name
                Promotionobj.Issuing_designation = Issuing_designation
                Promotionobj.ModifyBy  =  UserID  
                Promotionobj.PWI  = PWIStatus                         
                Promotionobj.save()

                UpdateEmployeeDesignation(EmpID,Promotiondesignation,OrganizationID,UserID)

                if DesHistory is not None:
                    PreviousDesHistory = DesignationHistory.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID=EmpID).order_by('-id')
                    
                    if PreviousDesHistory.count() >= 2 :
                        pr = PreviousDesHistory[1]
                        pr.Effective_to = date_of_promtion
                        pr.ModifyBy =  UserID
                        pr.save()

                    DesHistory.Effective_from = date_of_promtion
                    DesHistory.Designation = Promotiondesignation
                    DesHistory.ModifyBy = UserID
                    DesHistory.save()
                else:
                    PreviousDesHistory = DesignationHistory.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID=EmpID).order_by('-Effective_from').first()
                    if PreviousDesHistory:
                        PreviousDesHistory.Effective_to = date_of_promtion
                        PreviousDesHistory.ModifyBy =  UserID
                        PreviousDesHistory.save()

                    DesignationHistoryobj = DesignationHistory.objects.create(EmpID=EmpID,Effective_from = date_of_promtion,OrganizationID = OrganizationID,FromDesignation = Promotiondesignation,SalaryID=LOP_ID)

                if PWIStatus == True:
                    SC = PromotionSalaryDetails.objects.filter(IsDelete=False,PromotionLetterEmployeeDetail=Promotionobj,OrganizationID=OrganizationID)
                    for s in SC:
                            s.IsDelete = True
                            s.ModifyBy  = UserID
                            s.save()
                            
                    Total_Title = request.POST['Total_Title']
                    for i in range(int(Total_Title) + 1):
                        TitleID = request.POST[f'TitleID_{i}']
                        PresentSal = request.POST[f'PresentEmoluments_{i}']
                        RevisedSal = request.POST[f'RevisedSalary_{i}']

                        PromotionSalaryDetails.objects.create(
                            PromotionLetterEmployeeDetail=Promotionobj,
                            Salary_title_id=TitleID,
                            PresentSal=PresentSal,
                            RevisedSal=RevisedSal,
                            OrganizationID=OrganizationID,
                            CreatedBy=UserID
                        )
                        
                    UpdateEmployeeSalaryGridByPromotion(EmpID,Promotionobj,OrganizationID,UserID)
                    
                    if SalHistory is not None:
                        PreviousSalHistory = SalaryHistory.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID=EmpID).order_by('-id')
                        if PreviousSalHistory.count() >= 2:
                            pr = PreviousSalHistory[1]
                            pr.Effective_to = date_of_promtion
                            pr.ModifyBy =  UserID
                            pr.save()
                    
                            SalHistory.Effective_from = date_of_promtion
                            SalHistory.ToSalary = CTC
                            SalHistory.ModifyBy = UserID
                            SalHistory.save()

                    else:
                        PreviousSalHistory = SalaryHistory.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID=EmpID).order_by('-id').first()
                        if PreviousSalHistory:
                            PreviousSalHistory.Effective_to = date_of_promtion
                            PreviousSalHistory.ModifyBy =  UserID
                            PreviousSalHistory.save()
                            
                        FromSalary =   CTCEmpDetails.CTC  if CTCEmpDetails else 0
                        ToSalary = CTC
                        SalaryHistory.objects.create(EmpID=EmpID,Effective_from = date_of_promtion,OrganizationID = OrganizationID,FromSalary=FromSalary,ToSalary=ToSalary,SalaryID=LOP_ID,SourceType = 'Promotion with increment')
            else:
                Promotionobj = PromotionLetterEmployeeDetail.objects.create(
                    emp_code=emp_code,
                    prefix=prefix,
                    first_name=first_name,
                    last_name=last_name,
                    department=department,
                    designation=designation,
                    Promotiondesignation = Promotiondesignation,
                    Promotiondepartment = Promotiondepartment,
                    date_of_promtion  = date_of_promtion,
                    Issuing_manager_name=Issuing_manager_name,
                    Issuing_designation=Issuing_designation,
                    PWI=PWIStatus,
                    CreatedBy  = UserID,OrganizationID = OrganizationID
                )
                
                # promotion Histroy
                PreviousDesiHistory = DesignationHistory.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID=EmpID).order_by('-id').first()
                if PreviousDesiHistory:
                        PreviousDesiHistory.Effective_to = date_of_promtion
                        PreviousDesiHistory.ModifyBy =  UserID
                        PreviousDesiHistory.save()

                FromDesignation = designation
                FromDepartment =  department
                ToDesignation = Promotiondesignation
                ToDepartment =   Promotiondepartment
                
                DesignationHistoryobj  =   DesignationHistory.objects.create(EmpID=EmpID,Effective_from = date_of_promtion,OrganizationID = OrganizationID,PromotionID=Promotionobj.id,FromDesignation=FromDesignation,FromDepartment = FromDepartment,ToDepartment=ToDepartment,ToDesignation=ToDesignation)
                if  DesignationHistoryobj:
                        UpdateEmployeeDesignation(EmpID,Promotiondesignation,OrganizationID,UserID)
                
                
                # print("CTC = ",CTC)
                if PWIStatus == True:
                        Total_Title = request.POST['Total_Title']
                        for i in range(int(Total_Title) + 1):
                            TitleID = request.POST[f'TitleID_{i}']
                            PresentSal = request.POST[f'PresentEmoluments_{i}']
                            RevisedSal = request.POST[f'RevisedSalary_{i}']

                            salaryObj = PromotionSalaryDetails.objects.create(
                                    PromotionLetterEmployeeDetail=Promotionobj,
                                    Salary_title_id=TitleID,
                                    PresentSal=PresentSal,
                                    RevisedSal=RevisedSal,
                                    OrganizationID=OrganizationID,
                                    CreatedBy=UserID
                                )  
                            
                        UpdateEmployeeSalaryGridByPromotion(EmpID,Promotionobj,OrganizationID,UserID)
                        
                        # salart  histroy 
                        PreviousSalHistory = SalaryHistory.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmpID=EmpID).order_by('-id').first()
                        if PreviousSalHistory:
                            PreviousSalHistory.Effective_to = date_of_promtion
                            PreviousSalHistory.ModifyBy =  UserID
                            PreviousSalHistory.save()

                        FromSalary =   EmpDetails.CTC
                        ToSalary = CTC
                        SalaryHistory.objects.create(EmpID=EmpID,Effective_from = date_of_promtion,OrganizationID = OrganizationID,FromSalary=FromSalary,ToSalary=ToSalary,SalaryID=Promotionobj.id,SourceType = 'Promotion with increment')
                        
                if Page:
                     return redirect('emplistpl')

                Success = True        
                encrypted_id = encrypt_id(EmpID)
                url = reverse('EmployeeLetters')  
                redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
                return redirect(redirect_url)
        
    context  = {
        'Promotionobj':Promotionobj,
        'ManagerNames':ManagerNames,
        'HRManagerNames':HRManagerNames,
        'Designations':Designations,
        'SalaryTitles':SalaryTitles
    }
    return  render(request,"letterpl/entryemp.html",context)








# import requests
# def emplist(request):
    
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
#         OrganizationID =request.session["OrganizationID"]

#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     headers = {
#         'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
#     }
#     api_url = "http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID=" + str(OrganizationID)

#     try:
#         response = requests.get(api_url, headers=headers)
#         response.raise_for_status()  
#         memOrg = response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error occurred: {e}")   
#     I = request.GET.get('I',OrganizationID)
   
#     empdetails = PromotionLetterEmployeeDetail.objects.filter(IsDelete=False,OrganizationID=I).order_by('-CreatedDateTime','-ModifyDateTime').values()
    
#     context  = { 'empdetails':empdetails,'memOrg':memOrg,'I':I}
#     return render(request,"letterpl/emplist.html",context)



from django.db.models import Max
from app.views import OrganizationList

import requests
def emplist(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        OrganizationID =request.session["OrganizationID"]

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
   
    PromotionLetters = PromotionLetterEmployeeDetail.objects.filter(IsDelete=False,OrganizationID=I).order_by('-emp_code').annotate(
        EmpID=emp_id_subquery)
    for pr in  PromotionLetters:
        employeeletters  = PromotionLetterEmployeeDetail.objects.filter(IsDelete=False,OrganizationID=I,emp_code=pr.emp_code).order_by('-emp_code')
        last_Promotion_id = None
        if employeeletters.count() > 0 :
            last_Promotion_id = employeeletters.aggregate(Max('id'))['id__max']
        pr.last_Promotion_id  = last_Promotion_id
        pr.save()
    
    context  = { 'PromotionLetters':PromotionLetters,'memOrg':memOrg,'I':I,}
    return render(request,"letterpl/emplist.html",context)






# For generate_appointment_letter
def generate_Letter_of_promotion(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
     OrganizationID =request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID   
     
     id = request.GET["LOP_ID"]
     EmpID =  request.GET["EmpID"]

     template_path = "letterpl/plview.html"
    #  NileLogo=MasterAttribute.NileLogo
     get_data = PromotionLetterEmployeeDetail.objects.get(id=id)
     editor = PromotionLetter.objects.filter(user=1)
     head = True

     if 'head' in request.GET:
            head = request.GET.get('head') 
     print('head = ',head)   


     if editor.exists():
        data_field = editor[0].data
        get_data.data = data_field
        get_data.save() 



    
     
     get_data.data=get_data.data.replace("@@emp_code@@",str(get_data.emp_code))
     get_data.data=get_data.data.replace("@@date_of_promtion@@",str(get_data.date_of_promtion.strftime('%d/%m/%y')))
     
     get_data.data=get_data.data.replace("@@prefix@@",get_data.prefix)
     get_data.data=get_data.data.replace("@@firstname@@",get_data.first_name)
     get_data.data=get_data.data.replace("@@lastname@@",get_data.last_name)
     
     get_data.data=get_data.data.replace("@@Designation@@",get_data.designation)
     get_data.data=get_data.data.replace("@@Promotiondesignation@@",get_data.Promotiondesignation)
     
     
     get_data.data=get_data.data.replace("@@Department@@",get_data.department)
     get_data.data=get_data.data.replace("@@Issuing_manager_name@@",get_data.Issuing_manager_name)
     get_data.data=get_data.data.replace("@@Issuing_designation@@",get_data.Issuing_designation)



     od =OrganizationDetail(get_data.OrganizationID)
     OLogo=od.get_OrganizationLogo()
     if od.get_MComLogo()==1:
        NileLogo=MasterAttribute.NileLogoURL
      
    
     SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=False).order_by('TypeOrder', 'TitleOrder')
     s = "" 
     s = '<div ></div> <h1 style="text-align:center"></h1><table id="tblSal" style="width:100%;" class="table table-bordered"> <thead><tr style="background-color:#E9E3D6"><th style="background-color:#F6F1E4">Components</th><th style="background-color:#F6F1E4" align="center">Present Emoluments</th><th style="background-color:#F6F1E4" align="center">Revised Salary</th></tr></thead><tbody>'
   
        
     
     for salary in SalaryTitles:
            salary.PresentEmoluments = 0
            salary.RevisedSalary = 0
            
            if EmpID:
                sd = PromotionSalaryDetails.objects.filter(IsDelete=False, PromotionLetterEmployeeDetail  = get_data, Salary_title_id=salary.id, OrganizationID=OrganizationID)
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

      
     s += "</tbody></table>"
     header=""

    
     if head == True:
            header='<table class="noborder" width="100%"><tr><td  align="left"> <img height="150px" src="'+OLogo+'"/> </td> <td  align="center" valign="bottom"></td> <td  align="right"><img src="'+NileLogo+'"  height="150px"/></td></tr></table>'
      
      

       
     get_data.data = get_data.data.replace("@@Salary_Details@@", s)

     mydict={'Ed':get_data,'header':header}


     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'filename="report gcc club.pdf"'
     template = get_template(template_path)
     html = template.render(mydict)
     result = BytesIO()
  
     pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
      
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
    id = request.GET.get('LOP_ID')    
    empdetail = PromotionLetterEmployeeDetail.objects.get(id=id)
    empdetail.IsDelete=True
    empdetail.ModifyBy=UserID

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
    UserID =str(request.session["UserID"])
    Page = request.GET.get('Page')
    

    EmpID = request.GET.get('EmpID')
    id = request.GET.get('LOP_ID')    
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix

        new_file = upload_file_to_blob(file,id)
        if not new_file:
            messages.warning(request, f"{ext} not allowed only accept {', '.join(ext.lower()for ext in ALLOWED_EXTENTIONS)} ")
            return render(request, "letterpl/upload_file.html", {}) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()
        if Page:
                     return redirect('emplistpl')
      
        Success = 'Uploaded'        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('EmployeeLetters')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
        return redirect(redirect_url)
        
    
    return render(request, "letterpl/upload_file.html")


def download_file(request):
    id = request.GET.get('LOP_ID')
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID       
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
    EmpID = request.GET.get('EmpID')
    id = request.GET.get('LOP_ID')    
    
    file = PromotionLetterEmployeeDetail.objects.get(pk=id)
    file_id = file.file_id
    file_name = file.file_name
    EmployeeDetail = PromotionLetterEmployeeDetail.objects.get(pk=id)
    
    deletefile = PromotionLetterDeletedFileofEmployee.objects.create(PromotionLetterEmployeeDetail= EmployeeDetail,file_id = file_id,file_name = file_name)
   
    file = PromotionLetterEmployeeDetail.objects.get(pk=id)
    file.file_name = None
    file.file_id = None
    file.ModifyBy = UserID
    file.save()
    if Page:
                     return redirect('emplistpl')
    Success = 'Deleted'        
    encrypted_id = encrypt_id(EmpID)
    url = reverse('EmployeeLetters')  
    redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
    return redirect(redirect_url)  
    