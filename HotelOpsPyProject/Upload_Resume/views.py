from django.shortcuts import render

from django.shortcuts import render, redirect
from django.utils import timezone
from django.shortcuts import render, redirect
from django.utils import timezone
# from .models import Training_Data
from Open_position.models import CareerResume
from django.http import HttpResponse, Http404
import logging
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.
from Manning_Guide.models import OnRollDepartmentMaster,OnRollDesignationMaster



def Upload_Resume_View(request):
    context = {}
    return render(request, 'Upload_Resume/Upload_Resume_Temp.html', context)




logger = logging.getLogger(__name__)
def add_trainee(request):
    if 'OrganizationID' not in request.session or 'UserID' not in request.session:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')
    
    UserID = request.session.get("UserID")
    OrganizationID = request.session.get("OrganizationID")


    if request.method == "POST":
        # Collect form data
        first_name = request.POST.get("Firstname")
        middle_name = request.POST.get("MiddleName")
        last_name = request.POST.get("LastName")
        CandidatePhone = request.POST.get("CandidateContact")
        CandidateEmail = request.POST.get("CandidateEmailAddress")
        candidate_address = request.POST.get("CandidateAddress")
        college = request.POST.get("College")
        # school = request.POST.get("School")
        coordinator_name = request.POST.get("CoordinatorName")
        coordinator_email = request.POST.get("CoordinatorEmail")
        coordinator_phone = request.POST.get("CoordinatorPhone")
        preference_department = request.POST.get("DepartmentOfPreference")
        Designations = request.POST.get("Designations")
        
        resume_file = request.FILES.get("ResumeUpload")  
        photo_file = request.FILES.get("CandidatePhoto")     

        Departmentsfilter = OnRollDepartmentMaster.objects.filter(IsDelete=False,id=preference_department).values('DepartmentName')
        designationsFilter = OnRollDesignationMaster.objects.filter(IsDelete=False, id=Designations).values("designations")

        # Create and save instance
        trainee = CareerResume(
            first_name=first_name,
            Middle_Name=middle_name,
            last_name=last_name,
            phone=CandidatePhone,
            email=CandidateEmail,
            Candidate_Address=candidate_address,
            College=college,
            Placement_Coordinator_Name=coordinator_name,
            Placement_Coordinator_Email=coordinator_email,
            Placement_Coordinator_Phone=coordinator_phone,
            Department_Of_Preference=Departmentsfilter,
            Department=Departmentsfilter,
            job_title = designationsFilter,
            resume=resume_file,
            profile_photo=photo_file,
            campaign_source = "Trainees",
            OrganizationID=OrganizationID,  
            CreatedBy=UserID,
            CreatedDateTime=timezone.now(),
            AppliedDate = timezone.now(),
            Is_Training_Data = True,
        )

        # trainee.save()
        try:
            trainee.save()  
            messages.success(request, "Resume uploaded successfully!")  
            return redirect("ResumeShorting")  
        except Exception as e:
            messages.error(request, "Resume Not Uploded successfully!")  
            return redirect("Upload_Resume_View")  



# def Show_Department_Api(request):
#     Departmentsfilter = OnRollDepartmentMaster.objects.filter(IsDelete=False).order_by('DepartmentName')
#     data = Departmentsfilter.values("id", "DepartmentName")
#     return JsonResponse(list(data), safe=False)


# def Show_Designations_Api(request):
#     dept_id = request.GET.get("department_id")
#     print("the department id is:", dept_id)
#     if dept_id:
#         designations = OnRollDesignationMaster.objects.filter(
#             IsDelete=False,
#             OnRollDepartmentMaster=dept_id
#         ).order_by("designations")
#     else:
#         designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by("designations")

#     data = designations.values("id", "designations")
#     return JsonResponse(list(data), safe=False)