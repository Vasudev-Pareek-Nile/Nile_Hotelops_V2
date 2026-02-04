from django.templatetags.static import static

from django.shortcuts import render,redirect
from Manning_Guide.models import OnRollDepartmentMaster, OnRollDesignationMaster, OnRollDivisionMaster
from .models import *
from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail
from HumanResources.models import SalaryTitle_Master
from pathlib import Path
import mimetypes
from django.contrib import messages
from .azure import upload_file_to_blob,ALLOWED_EXTENTIONS,download_blob
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse,Http404
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from .models import LETTEROFINTENTEmployeeDetail,LETTEROFINTENT,LETTEROFINTENTDeletedFileofEmployee,SalaryDetails
from django.shortcuts import render,redirect
from xhtml2pdf import pisa
from django.template.loader import get_template
from InterviewAssessment.models import Assessment_Master,EmployeeDataRequest_Master
from django.shortcuts import render, redirect
from .models import SalaryTitle_Master, SalaryDetails

from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa

from hotelopsmgmtpy.utils import decrypt_id,encrypt_id
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from HumanResources.views  import GetMailofHR, ManagerNameandDesignation,EmployeeNameOnTheBasisofDesignation

from app.views import OrganizationName,OrganizationLogo

from PublicAccess.models import PublicAccessUrl  
from hotelopsmgmtpy.GlobalConfig import MasterAttribute

from app.models import OrganizationEmailMaster
from django.conf import settings

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




def InterviewAssessmentCandidate(request,OrganizationID,InterviewID):

    if InterviewID:
        IObj = Assessment_Master.objects.filter(IsDelete=False, OrganizationID=OrganizationID, id=InterviewID).first()
        
        if IObj is not None:
            IDict = {
                'ID':IObj.id,
                'emp_name': IObj.Name,
                'prefix': IObj.Prefix,
                'designation': IObj.position,
                'department': IObj.Department,
                'Email':IObj.Email,
                'ContactNumber':IObj.ContactNumber,
                'AppliedFor':IObj.AppliedFor,
                'TokenKey':encrypt_id(InterviewID),


                'ctc': IObj.exp_salary,
                'date_of_joining': IObj.ProposedDOJ
            }
            return IDict
        else:
            return None
    else:
        return "InterviewID is None"



def entryEmp(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    InterviewID = request.GET.get('InterviewID')
    DepartmentName = request.GET.get('DepartmentName')
    OID = request.GET.get('OID')
    Page  = request.GET.get('Page')

    if not OID:
        OID = OrganizationID
    

    # ManagerNames  = ManagerNameandDesignation(request,OrganizationID)
    
    ManagerNames =  EmployeeNameOnTheBasisofDesignation( DepartmentName,OrganizationID)
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    
    IntentObj  = None
   
    if InterviewID is not None:
        IntentObj = LETTEROFINTENTEmployeeDetail.objects.filter(OrganizationID =OrganizationID,InterviewID = InterviewID,IsDelete=False,ReIssue=False).first()
        if IntentObj is not None:
            DataFromIntentObj  = "IntentObj"

            SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=False, OrganizationID=OrganizationID).order_by('TypeOrder', 'TitleOrder')
            for salary in SalaryTitles:
                salary.Permonth = 0
                salary.Perannum = 0
                SC = SalaryDetails.objects.filter(IsDelete=False,LETTEROFINTENTEmployeeDetail=IntentObj, Salary_title_id = salary.id,OrganizationID=OrganizationID)
                if SC.exists():
                    salary.Permonth = SC[0].Permonth
                    salary.Perannum = SC[0].Perannum
        else:
            IntentObj =  InterviewAssessmentCandidate(request,OrganizationID,InterviewID)
            DataFromIntentObj  = "InterviewAssessmentCandidate"
            SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=False, OrganizationID=OrganizationID).order_by('TypeOrder', 'TitleOrder')
            for salary in SalaryTitles:
               salary.Permonth = 0
               salary.Perannum = 0
        
        
        
    candidatedata  = {}
   
    if request.method  == "POST":
        BtnValue  = request.POST['BtnValue'] 
        prefix =  request.POST['prefix']
        emp_name = request.POST['emp_name']
        date_of_intent  =  request.POST['date_of_intent']
        date_of_joining =  request.POST['date_of_joining']
        department =  request.POST['department']
        designation =  request.POST['designation']
        ctc = int(float(request.POST['ctc']))

        address =  request.POST['address']
        Issuing_manager_name =  request.POST['Issuing_manager_name']
        Issuing_designation =  request.POST['Issuing_designation']
        Reporting_Manager =  request.POST['Reporting_Manager']
        visible_salary_breakup = request.POST['visible_salary_breakup']
        
        visible_ctc = request.POST['visible_ctc']
        Reissue = request.POST.get('Reissue')
        print("Reissue = ",Reissue)

        


        if DataFromIntentObj == "IntentObj"  :
            if Reissue == "Yes":
                ReissueIntentObj  = LETTEROFINTENTEmployeeDetail.objects.create(
                    InterviewID = InterviewID ,
                    OrganizationID = OrganizationID,
                    CreatedBy = UserID,
                    prefix = prefix,
                    emp_name = emp_name,
                    date_of_intent = date_of_intent,
                    date_of_joining=date_of_joining,
                    department = department,
                    designation = designation ,
                    Issuing_designation = Issuing_designation ,
                    Issuing_manager_name = Issuing_manager_name,
                    visible_salary_breakup = visible_salary_breakup,
                    visible_ctc=visible_ctc,
                    ctc  = ctc ,
                    address  = address,
                    Reporting_Manager = Reporting_Manager
                )
            
                
                Total_Title = request.POST['Total_Title']
                for i in range(int(Total_Title) + 1):
                    TitleID = request.POST[f'TitleID_{i}']
                    Permonth = request.POST[f'Permonth_{i}']
                    Perannum = request.POST[f'Perannum_{i}']

                    salaryObj = SalaryDetails.objects.create(
                        LETTEROFINTENTEmployeeDetail=ReissueIntentObj,
                        Salary_title_id=TitleID,
                        Permonth=Permonth,
                        Perannum=Perannum,
                        OrganizationID=OrganizationID,
                        CreatedBy=UserID
                    )
                IntentObj.ReIssue = True
                IntentObj.IsDelete = True

                IntentObj.save()

            else:    
                IntentObj.prefix =  prefix
                IntentObj.emp_name = emp_name
                IntentObj.date_of_intent  =  date_of_intent
                IntentObj.date_of_joining =  date_of_joining
                IntentObj.department =  department
                IntentObj.designation =  designation
                IntentObj.ctc = ctc
                IntentObj.address = address
                IntentObj.Issuing_manager_name =   Issuing_manager_name
                IntentObj.Issuing_designation =  Issuing_designation
                IntentObj.visible_salary_breakup = visible_salary_breakup
                IntentObj.visible_ctc = visible_ctc
                IntentObj.Reporting_Manager = Reporting_Manager

                IntentObj.ModifyBy = UserID
                IntentObj.save()
                SC = SalaryDetails.objects.filter(IsDelete=False,LETTEROFINTENTEmployeeDetail=IntentObj,OrganizationID=OrganizationID)
                for s in SC:
                        s.IsDelete = True
                        s.ModifyBy  = UserID
                        s.save()
                
                
                Total_Title  =  request.POST['Total_Title']
                
                for i in range(int(Total_Title)+1):
                    TitleID = request.POST[f'TitleID_{i}']
                    Permonth  =  request.POST[f'Permonth_{i}']
                    Perannum  = request.POST[f'Perannum_{i}']
                
                    salaryObj = SalaryDetails.objects.create(
                        LETTEROFINTENTEmployeeDetail=IntentObj,
                        Salary_title_id = TitleID,
                        Permonth=Permonth,
                        Perannum=Perannum,
                        OrganizationID=OrganizationID,
                        CreatedBy  = UserID
                    )
        else:
            IntentObj  = LETTEROFINTENTEmployeeDetail.objects.create(
                InterviewID = InterviewID ,
                OrganizationID = OrganizationID,
                CreatedBy = UserID,
                prefix = prefix,
                emp_name = emp_name,
                date_of_intent = date_of_intent,
                date_of_joining=date_of_joining,
                department = department,
                designation = designation ,
                Issuing_designation = Issuing_designation ,
                Issuing_manager_name = Issuing_manager_name,
                visible_salary_breakup = visible_salary_breakup,
                visible_ctc=visible_ctc,
                ctc  = ctc ,
                address  = address,
                Reporting_Manager = Reporting_Manager
            )
           
            
            Total_Title = request.POST['Total_Title']
            for i in range(int(Total_Title) + 1):
                TitleID = request.POST[f'TitleID_{i}']
                Permonth = request.POST[f'Permonth_{i}']
                Perannum = request.POST[f'Perannum_{i}']

                salaryObj = SalaryDetails.objects.create(
                    LETTEROFINTENTEmployeeDetail=IntentObj,
                    Salary_title_id=TitleID,
                    Permonth=Permonth,
                    Perannum=Perannum,
                    OrganizationID=OrganizationID,
                    CreatedBy=UserID
                )
        
        
        IObj = Assessment_Master.objects.filter(IsDelete=False, OrganizationID=OrganizationID, id=InterviewID).first()
        if BtnValue == "Save":
            IObj.LOIStatus  = 'Draft'
            IObj.LastLoistatusModifyDate = datetime.datetime.now()
            IObj.save()
            if Page:
                return redirect('emplistloi')
        
            return redirect('InterviewAssessmentList')
       
        if BtnValue == "Save and Send Email":

            if IntentObj:
                AssessmentDetails  = InterviewAssessmentCandidate(request,OrganizationID,InterviewID)
                LID =  IntentObj.id
                if AssessmentDetails:
                    candidatedata = {
                                    'PreviewID':InterviewID,
                                    'Name':AssessmentDetails['emp_name'],
                                    'Email':AssessmentDetails['Email'],
                                    'ContactNumber':AssessmentDetails['ContactNumber'],
                                    'LOID':LID
                                }

    context = {
        'IntentObj':IntentObj,
        'ManagerNames':ManagerNames,
        'SalaryTitles':SalaryTitles, 
        'candidatedata': candidatedata,
        'Designations': Designations,
    }
    return render(request, "letter/entryEmp.html", context)






# For generate_appointment_letter
def generate_letter_of_intent_Email_Pdf(request,InterviewID):
     

     template_path = "letter/loiview.html"
    # NileLogo=MasterAttribute.NileLogo
     get_data =LETTEROFINTENTEmployeeDetail.objects.filter( InterviewID = InterviewID,IsDelete=False,ReIssue=False).first()
     editor = LETTEROFINTENT.objects.filter(user=1)

     if editor.exists():
        data_field = editor[0].data
        get_data.data = data_field
        get_data.save() 

     sd = SalaryDetails.objects.filter(LETTEROFINTENTEmployeeDetail=get_data,IsDelete=0)

     od =OrganizationDetail(get_data.OrganizationID)

    #  print("i found od is here::",od)
     OLogo=od.get_OrganizationLogo()
     NileLogo=''
     if od.get_MComLogo()==1:
        NileLogo=MasterAttribute.NileLogoURL
     
     get_data.data=get_data.data.replace("@@HotelLogo",OLogo)
     get_data.data=get_data.data.replace("@@hotelname@@",od.get_Organization_name())
     get_data.data=get_data.data.replace("{hotelname}",od.get_Organization_name())
     get_data.data=get_data.data.replace("@@date_of_intent@@",str(get_data.date_of_intent.strftime("%d-%B-%Y")))
     
     get_data.data=get_data.data.replace("@@prefix@@",get_data.prefix)
     get_data.data=get_data.data.replace("@@firstname@@",get_data.emp_name)
     get_data.data=get_data.data.replace("@@lastname@@",'')
     
     get_data.data=get_data.data.replace("@@Designation@@",get_data.designation)
     get_data.data=get_data.data.replace("@@Date_of_Joining@@",str(get_data.date_of_joining.strftime("%d-%B-%Y")))
     
     if get_data.visible_ctc == 'Yes':
        ctcstr  = f', your remuneration will be <strong>Rs {get_data.ctc}/- CTC </strong>per month.'
        get_data.data=get_data.data.replace("@@ctc@@",ctcstr)
     else:
        get_data.data=get_data.data.replace("@@ctc@@",'.')
            
     
     get_data.data=get_data.data.replace("@@Department@@",GetDivionName(get_data.designation,get_data.department))
     

     
     get_data.data=get_data.data.replace("@@Issuing_manager_name@@",'<br/><br/><br/>'+get_data.Issuing_manager_name)
     get_data.data=get_data.data.replace("@@Issuing_designation@@",''+get_data.Issuing_designation)

     get_data.data=get_data.data.replace("@@reporting_Manager@@",get_data.Reporting_Manager)


     s=""
     header=""
     header='<table class="noborder" width="100%"><tr><td  align="left"> <img height="150px" src="'+OLogo+'"/> </td> <td  align="center" valign="bottom"><h1 style="font-size:23px">Letter of Intent</h1></td> <td  align="right"><img src="'+NileLogo+'"  height="150px"/></td></tr></table>'
     
    
     if get_data.visible_salary_breakup=="Yes":
    
        
        s = '<div style="page-break-before: always;"></div> <h1 style="text-align:center">Annexure<h1><table id="tblSal" style="width:100%;" class="table table-bordered"> <thead><tr style="background-color:#E9E3D6"><th style="background-color:#F6F1E4">Components</th><th style="background-color:#F6F1E4" align="center">Per Month</th><th style="background-color:#F6F1E4" align="center">Per Annum</th></tr></thead><tbody>'
        for x in sd:
          
            if x.Salary_title.IsBold  == True:  
           
                s+="<tr style='background-color:#F5F5F6'><td width='250px'>"+  x.Salary_title.Title +"</td> <td align='right'>"+str(x.Permonth)+"</td> <td align='right'>"+str(x.Perannum)+"</td></tr>"
            else:
                s+="<tr><td>"+  x.Salary_title.Title +"</td> <td align='right'>"+str(x.Permonth)+"</td> <td align='right'>"+str(x.Perannum)+"</td></tr>"
            
        s+="</table>"


    
        get_data.data=get_data.data.replace('@@Annexure@@','A detailed compensation structure is attached as <strong>Annexure</strong>.')
        get_data.data = get_data.data.replace("@@SalaryBreak@@", '')

     else:
            get_data.data = get_data.data.replace("@@SalaryBreak@@", '')
            get_data.data=get_data.data.replace('@@Annexure@@','')
     
     
     get_data.data=get_data.data+ s

     mydict={'Ed':get_data,'header':header}


     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'filename="report gcc club.pdf"'
     template = get_template(template_path)
     html = template.render(mydict)

     result = BytesIO()
     template = get_template(template_path)
     html = template.render(mydict)

    #  pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)


     if not pdf.err:
        result.seek(0) 
        return result  
     return None


@csrf_protect
def Acceptloi(request):
    Tokenkey = request.GET.get('ID')
    if Tokenkey:
        InterviewID = decrypt_id(Tokenkey)
        if request.method == "POST":
            LOIStatus = request.POST.get('LOIStatus') 
            if InterviewID:
                IObj = Assessment_Master.objects.filter(IsDelete=False, id=InterviewID).first()
                if IObj:
                    IObj.LOIStatus = LOIStatus  
                    IObj.save()
                    if LOIStatus == "Accepted":
                         GenerateDataLink(request,IObj.OrganizationID,InterviewID)

                    return HttpResponse(f"LOI has been {LOIStatus.lower()}.")  
        else:
            IObj = Assessment_Master.objects.filter(IsDelete=False, id=InterviewID).values('LOIStatus').first()
            return render(request, 'letter/Acceptloi.html', {'IObj': IObj})
    return HttpResponse("Invalid request.")
       
import datetime


import uuid

def GenerateDataLink(request,OrganizationID,IND):
    print("IND =",IND)
    
    obj = EmployeeDataRequest_Master.objects.create(
        InterviewID=IND,
        OrganizationID=OrganizationID,
        TokenKey=str(uuid.uuid4()),
        ExpiryDate=datetime.date.today() + timedelta(5),
        CreatedBy=0,
       
    )
    assobj = Assessment_Master.objects.filter(id=IND, IsDelete=False, OrganizationID=OrganizationID).first()
    if assobj:
        assobj.GenerateLink=True
        assobj.save()
        

   
    Link = f'{MasterAttribute.PyHost}InterviewAssessment/CandidateDataForm/?ID={obj.TokenKey}'
    SendGenrateToCandidate(request,OrganizationID,IND,Link)
    # config url

def SendGenrateToCandidate(request,OrganizationID,IND,Link):
        default_bcc = "rajshree@nilehospitality.com"
        bcc_list = [default_bcc]
        HR_EmailAddress= GetMailofHR(OrganizationID)

        # if HR_EmailAddress:  
        #     bcc_list.append(HR_EmailAddress) 

        if HR_EmailAddress:
            if isinstance(HR_EmailAddress, (list, tuple)):
                bcc_list.extend(HR_EmailAddress)  
            else:
                bcc_list.append(HR_EmailAddress)  

        # print("bcc list is here::", bcc_list)
        # print("HR_EmailAddress is here::", HR_EmailAddress)

        AssessmentDetails  = InterviewAssessmentCandidate(request,OrganizationID,IND)
        if AssessmentDetails:
                    candidatedata = {
                        'Name':AssessmentDetails['emp_name'],
                        'Email':AssessmentDetails['Email'],
                        'ContactNumber':AssessmentDetails['ContactNumber'],
                        'designation':AssessmentDetails['designation'],
                        'department':AssessmentDetails['department'],
                        'AppliedFor':AssessmentDetails['AppliedFor'],
                        'TokenKey':AssessmentDetails['TokenKey']
                    }

                    if candidatedata:
                        AppliedFor = candidatedata['AppliedFor']
                        TokenKey = candidatedata['TokenKey']
 
                        if AppliedFor:
                            orgName = OrganizationName(AppliedFor)
                            orgLogo = OrganizationLogo(AppliedFor)

        
        email_settings = OrganizationEmailMaster.objects.filter(OrganizationID=OrganizationID, IsDelete=False).first()

        if OrganizationEmailMaster.DoesNotExist:
            email_settings = OrganizationEmailMaster.objects.filter(OrganizationID=3, IsDelete=False).first()

        if email_settings:
            settings.EMAIL_HOST = email_settings.email_host
            settings.EMAIL_PORT = email_settings.email_port
            settings.EMAIL_USE_TLS = email_settings.email_use_tls
            settings.EMAIL_HOST_USER = email_settings.email_host_user
            settings.EMAIL_HOST_PASSWORD = email_settings.email_host_password

            email_subject = 'Candidate Details'
            email_body = render_to_string('letter/GenerateDataLink.html', {
                'name': candidatedata['Name'],
                'candidate_name':  candidatedata['Name'],
                'candidate_designation': candidatedata['designation'],  
                'candidate_department': candidatedata['department'],  
                'HotelName':orgName,
                'Logo':orgLogo,
                'Link':Link
            })

            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [AssessmentDetails['Email']],
                  bcc=bcc_list
            )

            email.content_subtype = 'html'

            # email.send(fail_silently=False)
            try:
                email.send(fail_silently=False)

                return JsonResponse({'status': 'success', 'message': 'Email sent successfully!'})
            
            except Exception as e:
                import traceback
                print("Error sending email:", str(e))
                print(traceback.format_exc())  # shows full stack trace in the console/log
                return JsonResponse({
                    'status': 'error',
                    'message': f'Error sending email: {str(e)}'
                }, status=500)
             
          
@csrf_exempt  
def SendMailToCandidate(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
   
    if request.method == "POST":
        print("iam reaced at method post")
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        previewId = request.POST.get('previewId')  

        # print("DEBUG POST DATA:", name, email, phone, previewId)
        
        default_bcc = "rajshree@nilehospitality.com"
        bcc_list = [default_bcc]
        HR_EmailAddress= GetMailofHR(OrganizationID)
        # if HR_EmailAddress:  
        #     bcc_list.append(HR_EmailAddress)

        if HR_EmailAddress:
            if isinstance(HR_EmailAddress, (list, tuple)):
                bcc_list.extend(HR_EmailAddress)  
            else:
                bcc_list.append(HR_EmailAddress)   

        AssessmentDetails  = InterviewAssessmentCandidate(request,OrganizationID,previewId)
        if AssessmentDetails:
                    candidatedata = {
                                    'ID':AssessmentDetails['ID'],
                                    'Name':AssessmentDetails['emp_name'],
                                    'Email':AssessmentDetails['Email'],
                                    'ContactNumber':AssessmentDetails['ContactNumber'],
                                    'designation':AssessmentDetails['designation'],
                                    'department':AssessmentDetails['department'],
                                    'AppliedFor':AssessmentDetails['AppliedFor'],
                                    'TokenKey':AssessmentDetails['TokenKey']
                                }
                    if candidatedata:
                        AppliedFor = candidatedata['AppliedFor']
                        TokenKey = candidatedata['TokenKey']
                        ID = candidatedata['ID']
                        EID = encrypt_id(ID)
 
                        if AppliedFor:
                            orgName = OrganizationName(AppliedFor)
                            orgLogo = OrganizationLogo(AppliedFor)

                        Linkobj  = PublicAccessUrl.objects.create(ModelName='Assessment_Master',AppName = 'InterviewAssessment' ,InstanceId= EID)        

        IObj = Assessment_Master.objects.filter(IsDelete=False, OrganizationID=OrganizationID, id=previewId).first()
        # IObj.LastLoistatusModifyDate = datetime.datetime.now()
        IObj.LastLoistatusModifyDate = timezone.now()
            
        IObj.LOIStatus  = 'Shared'
        IObj.save()   
        email_settings = OrganizationEmailMaster.objects.filter(OrganizationID=OrganizationID, IsDelete=False).first()
        if OrganizationEmailMaster.DoesNotExist:
            email_settings = OrganizationEmailMaster.objects.filter(OrganizationID=3, IsDelete=False).first()

        if email_settings:
            settings.EMAIL_HOST = email_settings.email_host
            settings.EMAIL_PORT = email_settings.email_port
            settings.EMAIL_USE_TLS = email_settings.email_use_tls
            settings.EMAIL_HOST_USER = email_settings.email_host_user
            settings.EMAIL_HOST_PASSWORD = email_settings.email_host_password

            email_subject = 'Letter of Intent'
            email_body = render_to_string('letter/SendMailToCandidate.html', {
                'name': name,
                'candidate_name': name,
                'candidate_designation': candidatedata['designation'],  
                'candidate_department': candidatedata['department'],  
                'OrganizationName':orgName,
                'Logo':orgLogo,
                'Link':f'{MasterAttribute.PyHost}/Url/Accept/{Linkobj.UniqueToken}'
            })

            # print("we have the link here ------------------------------------------------")
            # print("Link:", f'{MasterAttribute.PyHost}/Url/Accept/{Linkobj.UniqueToken}')
            # print("Closed Here ------------------------------------------------")

          
            # print("the email is here", email, "and the type of email", type(email))
            # print("the bcc_list is here", bcc_list, "and the type of email", type(bcc_list))
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [email],
                bcc=bcc_list
            )

            email.content_subtype = 'html'

            pdf_file = generate_letter_of_intent_Email_Pdf(request, InterviewID=previewId)  

            if pdf_file:
                email.attach('Letter_of_Intent.pdf', pdf_file.read(), 'application/pdf')
                pdf_file.close() 
           
            try:
                email.send(fail_silently=False)
                # update Loi status 

                return JsonResponse({'status': 'success', 'message': 'Email sent successfully!'})
             
            # except Exception as e:
            #     return JsonResponse({'status': 'error', 'message': 'Error sending email.'}, status=500)
            except Exception as e:
                import traceback
                print("Error sending email:", str(e))
                print(traceback.format_exc())  # shows full stack trace in the console/log
                return JsonResponse({
                    'status': 'error',
                    'message': f'Error sending email: {str(e)}'
                }, status=500)
        else:
            return JsonResponse({'status': 'error', 'message': 'No email settings found.'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)



import requests
def emplist(request):

    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        OrganizationID =request.session["OrganizationID"]
    
    UserType = request.session.get("UserType")
    
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
    
    if UserType == 'CEO' and request.GET.get('I') is None:
        I = 401
    
    empdetails = LETTEROFINTENTEmployeeDetail.objects.filter(IsDelete=False,OrganizationID=I).order_by('-CreatedDateTime','-ModifyDateTime').values()
    context  = { 'empdetails':empdetails,'I':I,'memOrg':memOrg}
    return render(request,"letter/emplist.html",context)


def GetDivionName(Designation,Department):
    # 
    # OnRollDivisionMaster
    Division_Name=''
    if Department=="Housekeeping" or Department=="Front Office":
        Division_Name =Department
    else:
        des =OnRollDesignationMaster.objects.filter(IsDelete=False,OnRollDepartmentMaster__DepartmentName=Department,designations=Designation)
        if des.exists():  # Check if the QuerySet has any results
            first_object = des.first() 
            Division_Name= first_object.OnRollDivisionMaster.DivisionName;
    return Division_Name


from django.templatetags.static import static
# For generate_appointment_letter
def generate_letter_of_intent(request):
     InterviewID = request.GET["InterviewID"]
     LOID = request.GET["LOID"]

     template_path = "letter/loiview.html"
    # NileLogo=MasterAttribute.NileLogo
     
     get_data =LETTEROFINTENTEmployeeDetail.objects.filter(InterviewID = InterviewID,id=LOID).first()
     editor = LETTEROFINTENT.objects.filter(user=1)
     head = True

     if 'head' in request.GET:
            head = request.GET.get('head') 
     print('head = ',head)   
     if editor.exists():
        data_field = editor[0].data
        get_data.data = data_field
        get_data.save() 

     sd = SalaryDetails.objects.filter(LETTEROFINTENTEmployeeDetail=get_data,IsDelete=0)
     
    
     od =OrganizationDetail(get_data.OrganizationID)
     OLogo=od.get_OrganizationLogo()
     NileLogo = ""  # Default value
     if od.get_MComLogo()==1:
        NileLogo=MasterAttribute.NileLogoURL
         
     if not NileLogo:
        print("Inside NileLogo Condition")
        NileLogo = request.build_absolute_uri(static('assets/img/NileLogo/NileWhite.jpg'))

     print("NileLogoMasterAttribute", NileLogo)

     get_data.data=get_data.data.replace("@@HotelLogo",OLogo)
     get_data.data=get_data.data.replace("@@hotelname@@",od.get_Organization_name())
     get_data.data=get_data.data.replace("{hotelname}",od.get_Organization_name())
     get_data.data=get_data.data.replace("@@date_of_intent@@",str(get_data.date_of_intent.strftime("%d-%B-%Y")))
     
     get_data.data=get_data.data.replace("@@prefix@@",get_data.prefix)
     get_data.data=get_data.data.replace("@@firstname@@",get_data.emp_name)
     get_data.data=get_data.data.replace("@@lastname@@",'')
     
     get_data.data=get_data.data.replace("@@Designation@@",get_data.designation)

    #  print("Reporting Manager:", get_data.Reporting_Manager)
    #  if         
     get_data.data=get_data.data.replace("@@reporting_Manager@@",get_data.Reporting_Manager)

     get_data.data=get_data.data.replace("@@Date_of_Joining@@",str(get_data.date_of_joining.strftime("%d-%B-%Y")))
     

     if get_data.visible_ctc == 'Yes':
        ctcstr  = f', your remuneration will be <strong>Rs {get_data.ctc} /- CTC </strong>per month.'
        get_data.data=get_data.data.replace("@@ctc@@",ctcstr)
     else:
        get_data.data=get_data.data.replace("@@ctc@@",'.')
            
     
     get_data.data=get_data.data.replace("@@Department@@",GetDivionName(get_data.designation,get_data.department))
     

     
     get_data.data=get_data.data.replace("@@Issuing_manager_name@@",'<br/><br/><br/>'+get_data.Issuing_manager_name)
     get_data.data=get_data.data.replace("@@Issuing_designation@@",''+get_data.Issuing_designation)

     s=""
     header=""
     if head == True:
            # header='<table class="noborder" width="100%"><tr><td  align="left"> <img height="150px" src="'+OLogo+'"/> </td> <td  align="center" valign="bottom"></td> <td  align="right"><img src="{NileLogo}" height="150px"/></td></tr></table>'
            header = f'''
                <table class="noborder" width="100%">
                    <tr>
                        <td align="left">
                            <img height="150px" src="{OLogo}"/>
                        </td>
                        <td align="center" valign="bottom"></td>
                        <td align="right">
                            <img height="150px" src="{NileLogo}"/>
                        </td>
                    </tr>
                </table>
            '''
    
    #  if get_data.visible_salary_breakup=="Yes":
    
        
    #     s = '<div style="page-break-before: always;"></div> <h1 style="text-align:center">Annexure<h1><table id="tblSal" style="width:100%;" class="table table-bordered"> <thead><tr style="background-color:#E9E3D6"><th style="background-color:#F6F1E4">Components</th><th style="background-color:#F6F1E4" align="center">Per Month</th><th style="background-color:#F6F1E4" align="center">Per Annum</th></tr></thead><tbody>'
    #     for x in sd:
          
    #         if x.Salary_title.IsBold  == True:  
           
    #             s+="<tr style='background-color:#F5F5F6'><td width='250px'>"+  x.Salary_title.Title +"</td> <td align='right'>"+str(x.Permonth)+"</td> <td align='right'>"+str(x.Perannum)+"</td></tr>"
    #         else:
    #             s+="<tr><td>"+  x.Salary_title.Title +"</td> <td align='right'>"+str(x.Permonth)+"</td> <td align='right'>"+str(x.Perannum)+"</td></tr>"
            
    #     s+="</table>"


    
    #     get_data.data=get_data.data.replace("@@SalaryBreak@@",'')
    #  else:
    #     get_data.data=get_data.data.replace("@@SalaryBreak@@",'')
     if get_data.visible_salary_breakup == "Yes":
    
        s = '''
        <div style="page-break-before: always;"></div>  <br/><br/><br/> <br/><br/>
        <h1 style="text-align:center">Annexure</h1>
        <table id="tblSal" style="width:100%; font-size:12px;" class="table table-bordered"> 
            <thead>
                <tr style="background-color:#9f9c9b">
                    <th >Components</th>
                    <th align="center">Per Month</th>
                    <th  align="center">Per Annum</th>
                </tr>
            </thead>
            <tbody>
        '''
        for x in sd:
            if x.Salary_title.IsBold:
                s += "<tr ><td width='250px'>" + x.Salary_title.Title + "</td>"
                s += "<td align='right'>" + str(x.Permonth) + "</td>"
                s += "<td align='right'>" + str(x.Perannum) + "</td></tr>"
            else:
                s += "<tr><td>" + x.Salary_title.Title + "</td>"
                s += "<td align='right'>" + str(x.Permonth) + "</td>"
                s += "<td align='right'>" + str(x.Perannum) + "</td></tr>"
        
        s += "</tbody></table>"

        get_data.data=get_data.data.replace('@@Annexure@@','A detailed compensation structure is attached as <strong>Annexure</strong>.')
        get_data.data = get_data.data.replace("@@SalaryBreak@@", '')

     else:
        get_data.data = get_data.data.replace("@@SalaryBreak@@", '')
        get_data.data=get_data.data.replace('@@Annexure@@','')


     
     get_data.data=get_data.data+ s
    #  print(name)
    #  ScantyBaggageForm=forms.ScantyBaggageForm()

     mydict={'Ed':get_data,'header':header,'head':head}

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
     pdf  = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        # html, dest=response, link_callback=link_callback)
    # if error then show some funny view
     if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
     return None






def empdelete(request):
    id = request.GET["id"]
    empdetail = LETTEROFINTENTEmployeeDetail.objects.get(id=id)
    empdetail.IsDelete=True
    empdetail.save()
    return redirect('emplistloi')








def upload_file(request,id):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix

        new_file = upload_file_to_blob(file,id)
        if not new_file:
            messages.warning(request, f"{ext} not allowed only accept {', '.join(ext.lower()for ext in ALLOWED_EXTENTIONS)} ")
            return render(request, "letter/upload_file.html", {}) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()
        messages.success(request, f"{file.name} was successfully uploaded")
        return redirect('emplistloi')
    
    file = LETTEROFINTENTEmployeeDetail.objects.get(id=id)
    context = {'file':file}
    return render(request, "letter/upload_file.html", context)


def download_file(request, id):
    file = LETTEROFINTENTEmployeeDetail.objects.get(pk=id)
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
    file = LETTEROFINTENTEmployeeDetail.objects.get(pk=id)
    file_id = file.file_id
    file_name = file.file_name
    EmployeeDetail = LETTEROFINTENTEmployeeDetail.objects.get(pk=id)
    
    
    deletefile = LETTEROFINTENTDeletedFileofEmployee.objects.create(LETTEROFINTENTEmployeeDetail= EmployeeDetail,file_id = file_id,file_name = file_name)
    
    
    
        
          
    file = LETTEROFINTENTEmployeeDetail.objects.get(pk=id)
    file.file_name = None
    file.file_id = None
    file.save()
    messages.success(request, f"{file_name} was successfully deleted")
    return redirect('emplistloi')    
