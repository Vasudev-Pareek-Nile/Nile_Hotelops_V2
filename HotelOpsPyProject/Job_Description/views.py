from django.shortcuts import render
from Manning_Guide.models import OnRollDepartmentMaster,OnRollDesignationMaster

from .models import  JobDescription
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib import messages





def NewJobDescription(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID = str(request.session["UserID"])

    Departments = OnRollDepartmentMaster.objects.filter(IsDelete=False).order_by('DepartmentName')
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')

    Description_id = request.GET.get('ID')
    Description = None
    if Description_id is not None:
        Description = get_object_or_404(JobDescription, id=Description_id, OrganizationID=OrganizationID)

    if request.method == "POST":
        JD_Title = request.POST.get('JD_Title', '')
        Departments_list = request.POST.getlist('Department')
        Division = request.POST.get('Division', '')
        Positions_list = request.POST.getlist('Position')
        Report_To = request.POST.get('Report_To', '')
        Level = request.POST.get('Level', '')
        Signatory = request.POST.get('Signatory', '')
        Effective_Date_str = request.POST.get('Effective_Date', '')
        JD_Approved_By = request.POST.get('JD_Approved_By', '')
        Job_Scope = request.POST.get('Job_Scope', '')
        Duties_Responsibilities = request.POST.get('Duties_Responsibilities', '')
        Job_Knowledge_Skills = request.POST.get('Job_Knowledge_Skills', '')

        try:
            Effective_Date = parse_date(Effective_Date_str)
            if Effective_Date is None:
                raise ValidationError("Invalid date format. It must be in YYYY-MM-DD format.")
        except ValidationError as e:
            return HttpResponse(f"Error: {e}", status=400)

        if Description_id is not None:
            if Description:
                Description.JD_Title = JD_Title
                Description.Department = ', '.join(Departments_list)
                Description.Division = Division
                Description.Position = ', '.join(Positions_list)
                Description.Report_To = Report_To
                Description.Level = Level
                Description.Signatory = Signatory
                Description.Effective_Date = Effective_Date
                Description.JD_Approved_By = JD_Approved_By
                Description.Job_Scope = Job_Scope
                Description.Duties_Responsibilities = Duties_Responsibilities
                Description.Job_Knowledge_Skills = Job_Knowledge_Skills
                Description.ModifyBy = UserID
                Description.save()
            else:
                return HttpResponse("Error: Job description not found.")
        else:
            JobDescription.objects.create(
                JD_Title=JD_Title,
                Department=', '.join(Departments_list),
                Division=Division,
                Position=', '.join(Positions_list),
                Report_To=Report_To,
                Level=Level,
                Signatory=Signatory,
                Effective_Date=Effective_Date,
                JD_Approved_By=JD_Approved_By,
                Job_Scope=Job_Scope,
                Duties_Responsibilities=Duties_Responsibilities,
                Job_Knowledge_Skills=Job_Knowledge_Skills,
                OrganizationID=OrganizationID,
                CreatedBy=UserID
            )
            messages.success(request, 'Job Description added successfully!')
        return redirect('JobDescriptionlist')

    context = {
        'Departments': Departments,
        'Designations': Designations,
        'Description': Description
    }
    return render(request, 'NewJob/NewJobDescription.html', context)



 

def JobDescriptionlist(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    joblists = JobDescription.objects.filter(IsDelete=False)  
    context={'joblists':joblists}
    return render(request, 'NewJob/JobDescriptionlist.html',context)



from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError

from django.http import HttpResponse
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
def CopyJobDescription(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])

    Departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

    Description_id = request.GET.get('ID')
    Description = None
    if Description_id is not None:
        Description = get_object_or_404(JobDescription, id=Description_id, OrganizationID=OrganizationID)

    if request.method == "POST":
        JD_Title = request.POST.get('JD_Title', '')
        Departments_list = request.POST.getlist('Department')
        Division = request.POST.get('Division', '')
        Positions_list = request.POST.getlist('Position')
        Report_To = request.POST.get('Report_To', '')
        Level = request.POST.get('Level', '')
        Signatory = request.POST.get('Signatory', '')
        Effective_Date_str = request.POST.get('Effective_Date', '')
        JD_Approved_By = request.POST.get('JD_Approved_By', '')
        Job_Scope = request.POST.get('Job_Scope', '')
        Duties_Responsibilities = request.POST.get('Duties_Responsibilities', '')
        Job_Knowledge_Skills = request.POST.get('Job_Knowledge_Skills', '')

        try:
            Effective_Date = parse_date(Effective_Date_str)
            if Effective_Date is None:
                raise ValidationError("Invalid date format. It must be in YYYY-MM-DD format.")
        except ValidationError as e:
            return HttpResponse(f"Error: {e}", status=400)

        JobDescription.objects.create(
            JD_Title=JD_Title,
            Department=', '.join(Departments_list),
            Division=Division,
            Position=', '.join(Positions_list),
            Report_To=Report_To,
            Level=Level,
            Signatory=Signatory,
            Effective_Date=Effective_Date,
            JD_Approved_By=JD_Approved_By,
            Job_Scope=Job_Scope,
            Duties_Responsibilities=Duties_Responsibilities,
            Job_Knowledge_Skills=Job_Knowledge_Skills,
            OrganizationID=OrganizationID,
            CreatedBy=UserID
        )
        
        return redirect('JobDescriptionlist')

    context = {
        'Departments': Departments,
        'Designations': Designations,
        'Description': Description
    }
    return render(request, 'NewJob/CopyJobDescription.html', context)


from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime

from app.models import OrganizationMaster


def JobDescriptionPdf(request, id):
    if 'OrganizationID' not in request.session:
         return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID = str(request.session["UserID"])  
  
    try:
        data = JobDescription.objects.get(id=id,IsDelete=False)
    except JobDescription.DoesNotExist:
        raise Http404("Job description does not exist")

    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
   
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
    organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
   
    template_path = 'NewJob/JobDescriptionPdf.html'

    
    context = {
        'data': data,
        'current_datetime': current_datetime,
          'organization_logos':organization_logos,
             'organization_logo':organization_logo,
    }

    
    template = get_template(template_path)
    html = template.render(context)

    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="JobDescription.pdf"'

    
    pisa_status = pisa.CreatePDF(html, dest=response)

   
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response








from django.db.models import Q

def Mainpage(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    UserType = "GM".lower()  

    user_department = request.session.get("Department_Name", "").lower()  

    
    all_departments = JobDescription.objects.values('Department').distinct()

    
    if UserType in ["gm", "ceo"]:
        department_descriptions = all_departments
    else:
        
        department_descriptions = all_departments.filter(
            Q(Department=user_department) | Q(Department="general")
        ) if user_department else all_departments

    context = {
        'department_descriptions': department_descriptions,
        'selected_department': user_department
    }
    
    return render(request, 'main/Mainpage.html', context)














def JobDescriptionListdepartment(request, department_name):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
   
    job_descriptions = JobDescription.objects.filter(Department=department_name, IsDelete=False)
    
    context = {
        'department_name': department_name,
        'job_descriptions': job_descriptions
    }
    
    return render(request, 'main/JobDescriptionListdepartment.html', context)