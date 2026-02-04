# from django.shortcuts import render,redirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute


from xhtml2pdf import pisa
from django.core.mail import send_mail
import uuid
import json
from datetime import datetime
from .models import Reference_check, ReferenceDetails
from .filters import apply_filters




from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.contrib import messages
from .models import ReferenceDetails, Reference_check,OrganizationNameList,DesignationNameList
import json
import uuid
from xhtml2pdf import pisa  
from InterviewAssessment.models import Assessment_Master

# def Reference_form(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")

#     OrganizationID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])
#     Hotelsnames = OrganizationNameList.objects.all().order_by("Hotal_name")
#     Designationnames = DesignationNameList.objects.all().order_by("Designation_name")
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     AID  = request.GET.get('AID')
#     if AID is not None:
#         Interviewobj   = Assessment_Master.objects.filter(id=AID,IsDelete=False).first()
#     if request.method == "POST":
#         candidate_name = request.POST.get('candidate_name')
#         candidate_department = request.POST.get('candidate_department')
        
        
#         Ref1_name = request.POST.get('Ref1_name')
#         Ref1_email = request.POST.get('Ref1_email')
#         Ref1_mobile_number = request.POST.get('Ref1_mobile_number')
#         Ref1_Organization = request.POST.get('Ref1_Organization')
#         Ref1_Designation = request.POST.get('Ref1_Designation')

        
#         Ref2_name = request.POST.get('Ref2_name')
#         Ref2_email = request.POST.get('Ref2_email')
#         Ref2_mobile_number = request.POST.get('Ref2_mobile_number')
#         Ref2_Organization = request.POST.get('Ref2_Organization')
#         Ref2_Designation = request.POST.get('Ref2_Designation')

       
#         Ref3_name = request.POST.get('Ref3_name')
#         Ref3_email = request.POST.get('Ref3_email')
#         Ref3_mobile_number = request.POST.get('Ref3_mobile_number')
#         Ref3_Organization = request.POST.get('Ref3_Organization')
#         Ref3_Designation = request.POST.get('Ref3_Designation')

        
#         ref1_unique_id = uuid.uuid4().hex[:10]  
#         ref2_unique_id = uuid.uuid4().hex[:10]
#         ref3_unique_id = uuid.uuid4().hex[:10]

       
#         reference_detail = ReferenceDetails.objects.create(
#             candidate_name=candidate_name,
#             candidate_department=candidate_department,
#             Inteview_AssementID = AID,
#             Ref1_name=Ref1_name,
#             Ref1_email=Ref1_email,
#             Ref1_mobile_number=Ref1_mobile_number,
#             Ref1_Organization=Ref1_Organization,
#             Ref1_Designation=Ref1_Designation,
#             Ref2_name=Ref2_name,
#             Ref2_email=Ref2_email,
#             Ref2_mobile_number=Ref2_mobile_number,
#             Ref2_Organization=Ref2_Organization,
#             Ref2_Designation=Ref2_Designation,
#             Ref3_name=Ref3_name,
#             Ref3_email=Ref3_email,
#             Ref3_mobile_number=Ref3_mobile_number,
#             Ref3_Organization=Ref3_Organization,
#             Ref3_Designation=Ref3_Designation,
#             ref1_unique_id=ref1_unique_id,
#             ref2_unique_id=ref2_unique_id,
#             ref3_unique_id=ref3_unique_id
#         )

        
#         references = [
#             {'name': Ref1_name, 'email': Ref1_email, 'unique_id': ref1_unique_id},
#             {'name': Ref2_name, 'email': Ref2_email, 'unique_id': ref2_unique_id},
#             {'name': Ref3_name, 'email': Ref3_email, 'unique_id': ref3_unique_id},
#         ]

#         for ref in references:
#             link = f"{request.build_absolute_uri('/')}Reference_check/Reference_add/{ref['unique_id']}/"

#             email_subject = 'Reference Check'
#             email_body = render_to_string('reference_email_template.html', {
#                 'name': ref['name'],
#                 'candidate_name': candidate_name,
#                 'candidate_department': candidate_department,
#                 'link': link
#             })

#             email = EmailMessage(
#                 email_subject,
#                 email_body,
#                 settings.EMAIL_HOST_USER,
#                 [ref['email']],
#             )
#             email.content_subtype = 'html'
#             email.send(fail_silently=False)

#         Interviewobj.reference = reference_detail.id
#         Interviewobj.save()
#         return redirect('InterviewAssessmentList')  
#     context = {'OrganizationID':OrganizationID,'hotelapitoken':hotelapitoken,'Hotelsnames':Hotelsnames,'Designationnames':Designationnames}
#     return render(request, 'check/Reference_form.html',context)
# views.py

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from app.models import  OrganizationEmailMaster
import uuid
from hotelopsmgmtpy.GlobalConfig import MasterAttribute


# def Reference_form(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")

#     OrganizationID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])
    
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     AID = request.GET.get('AID')

#     if AID is not None:
#         Interviewobj = Assessment_Master.objects.filter(id=AID, IsDelete=False).first()

#     if request.method == "POST":
#         candidate_name = request.POST.get('candidate_name')
#         candidate_department = request.POST.get('candidate_department')

#         Ref1_name = request.POST.get('Ref1_name')
#         Ref1_email = request.POST.get('Ref1_email')
#         Ref1_mobile_number = request.POST.get('Ref1_mobile_number')
#         Ref1_Organization = request.POST.get('Ref1_Organization')
#         Ref1_Designation = request.POST.get('Ref1_Designation')

#         Ref2_name = request.POST.get('Ref2_name')
#         Ref2_email = request.POST.get('Ref2_email')
#         Ref2_mobile_number = request.POST.get('Ref2_mobile_number')
#         Ref2_Organization = request.POST.get('Ref2_Organization')
#         Ref2_Designation = request.POST.get('Ref2_Designation')

#         Ref3_name = request.POST.get('Ref3_name')
#         Ref3_email = request.POST.get('Ref3_email')
#         Ref3_mobile_number = request.POST.get('Ref3_mobile_number')
#         Ref3_Organization = request.POST.get('Ref3_Organization')
#         Ref3_Designation = request.POST.get('Ref3_Designation')

#         ref1_unique_id = uuid.uuid4().hex[:10]
#         ref2_unique_id = uuid.uuid4().hex[:10]
#         ref3_unique_id = uuid.uuid4().hex[:10]

#         reference_detail = ReferenceDetails.objects.create(
#             candidate_name=candidate_name,
#             candidate_department=candidate_department,
#             Inteview_AssementID=AID,
#             Ref1_name=Ref1_name,
#             Ref1_email=Ref1_email,
#             Ref1_mobile_number=Ref1_mobile_number,
#             Ref1_Organization=Ref1_Organization,
#             Ref1_Designation=Ref1_Designation,
#             Ref2_name=Ref2_name,
#             Ref2_email=Ref2_email,
#             Ref2_mobile_number=Ref2_mobile_number,
#             Ref2_Organization=Ref2_Organization,
#             Ref2_Designation=Ref2_Designation,
#             Ref3_name=Ref3_name,
#             Ref3_email=Ref3_email,
#             Ref3_mobile_number=Ref3_mobile_number,
#             Ref3_Organization=Ref3_Organization,
#             Ref3_Designation=Ref3_Designation,
#             ref1_unique_id=ref1_unique_id,
#             ref2_unique_id=ref2_unique_id,
#             ref3_unique_id=ref3_unique_id,
#             OrganizationID = OrganizationID
#         )

#         references = [
#             {'name': Ref1_name, 'email': Ref1_email, 'unique_id': ref1_unique_id},
#             {'name': Ref2_name, 'email': Ref2_email, 'unique_id': ref2_unique_id},
#             {'name': Ref3_name, 'email': Ref3_email, 'unique_id': ref3_unique_id},
#         ]

       
#         email_settings = OrganizationEmailMaster.objects.filter(OrganizationID=OrganizationID, IsDelete=False).first()
#         if OrganizationEmailMaster.DoesNotExist:
#             email_settings = OrganizationEmailMaster.objects.filter(OrganizationID=3, IsDelete=False).first()


        
#         if email_settings:
            
#             settings.EMAIL_HOST = email_settings.email_host
#             settings.EMAIL_PORT = email_settings.email_port
#             settings.EMAIL_USE_TLS = email_settings.email_use_tls
#             settings.EMAIL_HOST_USER = email_settings.email_host_user
#             settings.EMAIL_HOST_PASSWORD = email_settings.email_host_password

#             for ref in references:
#                 link = f"{MasterAttribute.Host}Reference_check/Reference_add/{ref['unique_id']}"
#                 email_subject = 'Reference Check'
#                 email_body = render_to_string('reference_email_template.html', {
#                     'name': ref['name'],
#                     'candidate_name': candidate_name,
#                     'candidate_department': candidate_department,
#                     'link': link,
#                 })

#                 email = EmailMessage(
#                     email_subject,
#                     email_body,
#                     settings.EMAIL_HOST_USER,  
#                     [ref['email']],  
#                 )
                
#                 email.content_subtype = 'html'  

#                 try:
#                     email.send(fail_silently=False)  
#                 except Exception as e:
#                     print(f"Error sending email to {ref['email']}: {e}")
#         else:
#             print("No email settings found for the organization.")

#         Interviewobj.reference = reference_detail.id
#         Interviewobj.save()
#         return redirect('InterviewAssessmentList')

#     context = {
#         'OrganizationID': OrganizationID,
#         'hotelapitoken': hotelapitoken,
       
#     }
#     return render(request, 'check/Reference_form.html', context)


def Reference_form(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    from HumanResources.views import GetMailofHR

    OrganizationID = request.session["OrganizationID"]
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


    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    AID = request.GET.get('AID')

    Interviewobj = None
    if AID is not None:
        Interviewobj = Assessment_Master.objects.filter(id=AID, IsDelete=False).first()

    if request.method == "POST":
        candidate_name = request.POST.get('candidate_name')
        candidate_department = request.POST.get('candidate_department')

        # Ref1 details (mandatory)
        Ref1_name = request.POST.get('Ref1_name')
        Ref1_email = request.POST.get('Ref1_email')
        Ref1_mobile_number = request.POST.get('Ref1_mobile_number')
        Ref1_Organization = request.POST.get('Ref1_Organization')
        Ref1_Designation = request.POST.get('Ref1_Designation')

        # Optional Ref2 and Ref3 details
        Ref2_name = request.POST.get('Ref2_name')
        Ref2_email = request.POST.get('Ref2_email')
        Ref2_mobile_number = request.POST.get('Ref2_mobile_number')
        Ref2_Organization = request.POST.get('Ref2_Organization')
        Ref2_Designation = request.POST.get('Ref2_Designation')

        Ref3_name = request.POST.get('Ref3_name')
        Ref3_email = request.POST.get('Ref3_email')
        Ref3_mobile_number = request.POST.get('Ref3_mobile_number')
        Ref3_Organization = request.POST.get('Ref3_Organization')
        Ref3_Designation = request.POST.get('Ref3_Designation')

        Ref1_candidate_Designation = request.POST.get('Ref1_candidate_Designation') or ''
        Ref2_candidate_Designation = request.POST.get('Ref2_candidate_Designation') or ''
        Ref3_candidate_Designation = request.POST.get('Ref3_candidate_Designation') or ''



        # Generate unique IDs for each reference
        ref1_unique_id = uuid.uuid4().hex[:10]
        ref2_unique_id = uuid.uuid4().hex[:10] if Ref2_name else None
        ref3_unique_id = uuid.uuid4().hex[:10] if Ref3_name else None

        # Create the ReferenceDetails object
        reference_detail = ReferenceDetails.objects.create(
            candidate_name=candidate_name,
            candidate_department=candidate_department,
            Inteview_AssementID=AID,
            Ref1_name=Ref1_name,
            Ref1_email=Ref1_email,
            Ref1_mobile_number=Ref1_mobile_number,
            Ref1_Organization=Ref1_Organization,
            Ref1_Designation=Ref1_Designation,
            ref1_unique_id=ref1_unique_id,
            Ref2_name=Ref2_name or '',
            Ref2_email=Ref2_email or '',
            Ref2_mobile_number=Ref2_mobile_number or '',
            Ref2_Organization=Ref2_Organization or '',
            Ref2_Designation=Ref2_Designation or '',
            ref2_unique_id=ref2_unique_id or '',
            Ref3_name=Ref3_name or '',
            Ref3_email=Ref3_email or '',
            Ref3_mobile_number=Ref3_mobile_number or '',
            Ref3_Organization=Ref3_Organization or '',
            Ref3_Designation=Ref3_Designation or '',
            ref3_unique_id=ref3_unique_id or '',

            Ref1_candidate_Designation = Ref1_candidate_Designation,
            Ref2_candidate_Designation = Ref2_candidate_Designation,
            Ref3_candidate_Designation = Ref3_candidate_Designation,


            OrganizationID=OrganizationID
        )

        references = [{'name': Ref1_name, 'email': Ref1_email, 'unique_id': ref1_unique_id}]
        if Ref2_name:
            references.append({'name': Ref2_name, 'email': Ref2_email, 'unique_id': ref2_unique_id})
        if Ref3_name:
            references.append({'name': Ref3_name, 'email': Ref3_email, 'unique_id': ref3_unique_id})

        # Email settings
        email_settings = OrganizationEmailMaster.objects.filter(OrganizationID=OrganizationID, IsDelete=False).first()
        if not email_settings:
            email_settings = OrganizationEmailMaster.objects.filter(OrganizationID=3, IsDelete=False).first()

        if email_settings:
            settings.EMAIL_HOST = email_settings.email_host
            settings.EMAIL_PORT = email_settings.email_port
            settings.EMAIL_USE_TLS = email_settings.email_use_tls
            settings.EMAIL_HOST_USER = email_settings.email_host_user
            settings.EMAIL_HOST_PASSWORD = email_settings.email_host_password

            for ref in references:
                link = f"{MasterAttribute.PyHost}/Reference_check/Reference_add/{ref['unique_id']}"
                email_subject = 'Reference Check'
                email_body = render_to_string('reference_email_template.html', {
                    'name': ref['name'],
                    'candidate_name': candidate_name,
                    'candidate_department': candidate_department,
                    'link': link,
                    'Logo':reference_detail.get_organization_logo(),
                    'OrganizationName':reference_detail.get_organization_name(),
                })

                email = EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [ref['email']],
                    bcc_list
                )
                email.content_subtype = 'html'
                try:
                    email.send(fail_silently=False)
                except Exception as e:
                    print(f"Error sending email to {ref['email']}: {e}")
        else:
            print("No email settings found for the organization.")

        if Interviewobj:
            Interviewobj.reference = reference_detail.id
            Interviewobj.save()
        return redirect('InterviewAssessmentList')

    context = {'OrganizationID': OrganizationID, 'hotelapitoken': hotelapitoken}
    return render(request, 'check/Reference_form.html', context)




from django.http import JsonResponse
from .models import OrganizationNameList

def search_autocomplete(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        qs = OrganizationNameList.objects.filter(Hotal_name__icontains=term)
        names = list(qs.values('id', 'Hotal_name'))  
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)

def designation_autocomplete(request):
    if 'term' in request.GET:
        qs = DesignationNameList.objects.filter(Designation_name__icontains=request.GET['term'])
        designation_names = list(qs.values_list('Designation_name', flat=True))
        return JsonResponse(designation_names, safe=False)
    return JsonResponse([], safe=False)




def Referenceformlist(request):
    references = ReferenceDetails.objects.all()
    context = {
        'references': references
    }
    return render(request, 'check/Referenceformlist.html', context)



def parse_year_month(year_month_str):
    if year_month_str:
        return datetime.strptime(year_month_str + "-01", '%Y-%m-%d').date()
    return None

def Reference_add(request, unique_link):
    ref_detail = None
    ref_name = None
    ref_contact = None
    ref_unique_id =  unique_link
    AppliedDepartment = None
    ApplicantName = None
    

    ref_detail = ReferenceDetails.objects.filter(ref1_unique_id=unique_link, IsDelete=False).first()
    Logo =None
    OrganizationName=""
    try:
        Logo  = ref_detail.get_organization_logo()
        OrganizationName  = ref_detail.get_organization_name()
    except:
        print()
    

    if ref_detail:
        print("Type = ",type(ref_detail.ref1_status))
        if ref_detail.ref1_status == 1:
            return redirect('already')
        ref_name = ref_detail.Ref1_name
        ref_contact = ref_detail.Ref1_mobile_number
    else:
        ref_detail = ReferenceDetails.objects.filter(ref2_unique_id=unique_link, IsDelete=False).first()
        if ref_detail:
            print("Type = ",type(ref_detail.ref1_status))
            if ref_detail.ref2_status == 1:
                return redirect('already')
            ref_name = ref_detail.Ref2_name
            ref_contact = ref_detail.Ref2_mobile_number
        else:
            ref_detail = ReferenceDetails.objects.filter(ref3_unique_id=unique_link, IsDelete=False).first()
            print("Type = ",type(ref_detail.ref1_status))
            if ref_detail:
                if ref_detail.ref3_status == 1:
                    return redirect('already')
                ref_name = ref_detail.Ref3_name
                ref_contact = ref_detail.Ref3_mobile_number
            else:
                return render(request, 'check/reference_not_found.html')
    if ref_detail:
        AppliedDepartment  = ref_detail.candidate_department
        ApplicantName = ref_detail.candidate_name

   
    if request.method == 'POST':
      
        name = request.POST.get('name')
        relationship = request.POST.get('relationship')
        contact_informations = request.POST.get('contact_informations')
        employment_from_date = request.POST.get('employment_from_date')
        employment_to_date = request.POST.get('employment_to_date')
        employment_from_date_parsed = parse_year_month(employment_from_date)
        employment_to_date_parsed = parse_year_month(employment_to_date)

        job_performance = request.POST.get('job_performance')
        interpersonal_skills = request.POST.get('interpersonal_skills')
        attendance_work = request.POST.get('attendance_work')
        leave_company = request.POST.get('leave_company')
        anything_else = request.POST.get('anything_else')
        this_companyid = request.POST.get('this_company')
        this_company = False
        if this_companyid == '1':
            this_company = True
        
        rehireid = request.POST.get('rehire')
        rehire = False
        if rehireid == '1':
            rehire = True




        
        reference_check = Reference_check.objects.create(
            ReferenceDetails=ref_detail,
            name=name,
            ref_unique_id = ref_unique_id,
            relationship=relationship,
            contact_informations=contact_informations,
            employment_from_date = employment_from_date_parsed,
            employment_to_date = employment_to_date_parsed,
         
            job_performance=job_performance,
            interpersonal_skills=interpersonal_skills,
            attendance_work=attendance_work,
            leave_company=leave_company,
            anything_else=anything_else,
            this_company=this_company,
            rehire=rehire
        )

       
        if ref_detail.ref1_unique_id == unique_link:
            ref_detail.ref1_status = 1
        elif ref_detail.ref2_unique_id == unique_link:
            ref_detail.ref2_status = 1
        elif ref_detail.ref3_unique_id == unique_link:
            ref_detail.ref3_status = 1

        ref_detail.save()  

        return redirect('thanku')

    return render(request, 'check/Reference_add.html', {'ref_detail': ref_detail,'ref_name': ref_name,'AppliedDepartment':AppliedDepartment,'ApplicantName':ApplicantName,
        'ref_contact': ref_contact,
        'OrganizationName':OrganizationName,
        'Logo':Logo
        })


def Reference_list(request):
   
    return render(request, 'check/Reference_list.html')


def reference_filter(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            filter_criteria = data.get('filters', [])

            
            references = Reference_check.objects.all()
            references = apply_filters(references, filter_criteria)  

            
            references_data = list(references.values(
                'id', 'name', 'relationship', 'contact_informations', 'this_company', 'date_of_employment'
            ))
            return JsonResponse({'references': references_data})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method or content type'}, status=400)



def Reference_delete(request):
    id = request.GET.get("ID")
    check = get_object_or_404(Reference_check, id=id)
    check.IsDelete = True
    check.save()
    return redirect('Reference_report')  


def Reference_report(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)  
    
    OrganizationID = request.session["OrganizationID"]
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    name = request.GET.get('name')
    
    queryset = Reference_check.objects.filter(IsDelete=False)

    filter_args = {}
    if start_date and end_date:
        filter_args['date_of_employment__range'] = [start_date, end_date]
    if name:
        filter_args['name'] = name

    queryset = queryset.filter(**filter_args)
    context = {'checks': queryset, 'start_date': start_date, 'end_date': end_date}
    return render(request, 'check/Reference_report.html', context)


def Reference_pdf(request):
    id = request.GET.get('ID')
    check = get_object_or_404(Reference_check, id=id)
    template_path = 'check/Reference_pdf.html'
    
    # Fetching ReferenceDetails related to the check
    reference_details = check.ReferenceDetails
    
    context = {
        'check': check,
        'candidate_name': reference_details.candidate_name,
        'candidate_department': reference_details.candidate_department,
    }
   
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
   
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



from app.models import OrganizationMaster

def ReferenceCheckView(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)  
    OrganizationID = request.session["OrganizationID"]
    NileLOGO  = None
    OrganizationLogo  = None
    NileID = 3
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    if OrganizationID != NileID:
        Nileobj  = OrganizationMaster.objects.filter(OrganizationID=3).first()
        NileLOGO  = f"{base_url}{Nileobj.OrganizationLogo}"
        orgobj = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
        OrganizationLogo  = f"{base_url}{orgobj.OrganizationLogo}"
  
    
    RID = request.GET.get('RID')
    if RID:
        refobj  = ReferenceDetails.objects.filter(id=RID,IsDelete=False).first()
        if refobj:
            checks = Reference_check.objects.filter(ReferenceDetails=refobj,IsDelete=False)
        
    
   
    
    context = {
        'checks': checks,
        'candidate_name': refobj.candidate_name,
        'candidate_department': refobj.candidate_department,
         'NileLOGO': NileLOGO,
        'OrganizationLogo': OrganizationLogo,
    }
   
    template_path = 'check/ReferenceCheckView.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
   
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response







def generate_reference_link(request):
    new_uuid = uuid.uuid4()
    return render(request, 'check/generate_reference_link.html', {'uuid': new_uuid})


def thanku(request):
    return render(request, 'check/thanku.html')


def already(request):
    return render(request, 'check/already.html')




#     selected_organization = next((org for org in memOrg if str(org['OrganizationID']) == selectedOrganizationID), None)
#     selectedOrganizationName = selected_organization['Organization_name'] if selected_organization else "Unknown Organization"
#     base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
   
#     organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
#     organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
#     organization = OrganizationMaster.objects.filter(OrganizationID=selectedOrganizationID).first()
#     organization_logo = f"{base_url}{organization.OrganizationLogo}" if organization and organization.OrganizationLogo else None
 
#  'organization_logos': organization_logos,
#         'organization_logo': organization_logo,
 