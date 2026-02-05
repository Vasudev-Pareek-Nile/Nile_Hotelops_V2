from django.shortcuts import render
from django.shortcuts import render,redirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
# Create your views here.
from .models import Reason_for_Leaving,Experience,Rating,Exitinterviewdata,exitinterviewmaster,ExitRating
from django.shortcuts import render, get_object_or_404
from app.models import EmployeeMaster,OrganizationMaster
import logging
from django.contrib import messages
from HumanResources.views import EmployeeDetailsData  
from django.urls import reverse
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Exitinterviewdata, Experience, Rating, exitinterviewmaster, ExitRating, Reason_for_Leaving


# def Exit_Add(request):
#     if 'OrganizationID' not in request.session:
#         return redirect('MasterAttribute.Host')

#     OrganizationID = request.session.get("OrganizationID")
#     UserID = request.session.get("UserID")
  
#     EmpID = request.GET.get('EmpID')
    
#     EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
#     warning_instance = {
#             'emp_code': EmpDetails.EmployeeCode,
#             'emp_name': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
#             'department': EmpDetails.Department,
#             'designation': EmpDetails.Designation,
#         }

#     reasons = Reason_for_Leaving.objects.filter(IsDelete=False)
#     experiencedatas = Experience.objects.filter(IsDelete=False)
#     ratingleveings = Rating.objects.filter(IsDelete=False)
    
#     if request.method == 'POST':
       
#         employee_code = request.POST.get('EmployeeCode')
#         EmpName = request.POST.get('EmpName')
#         job_title = request.POST.get('Designation')
#         date_of_joining = request.POST.get('DateofJoining')
#         department = request.POST.get('Department')
#         date_of_leaving = request.POST.get('DateofLeaving')
#         notice_period = request.POST.get('NoticePeriod')  
#         reason_for_leaving = request.POST.get('reasons')
#         final_comment = request.POST.get('FinalComment')
#         Resign = request.POST.get('Resign')
#         Termination = request.POST.get('Termination')
#         hotel=request.POST.get('hotel')
#         rehire = request.POST.get('rehire','no') == 'Yes'
        
#         exits = Exitinterviewdata.objects.create(
#             Employee_Code=employee_code,
#             EmpName=EmpName,
#             Job_Title=job_title,
#             DateofJoining=date_of_joining,
#             Department=department,
#             DateofLeaving=date_of_leaving,
#             NoticePeriod=notice_period,  
#             ReasonForLeaving=reason_for_leaving, 
#             FinalComment=final_comment,
#             rehire=rehire,
#             Resign=Resign,
#             Termination=Termination,
#             hotel=hotel,

#             OrganizationID=OrganizationID,
#             CreatedBy=UserID
           
#         )
#         TotalExitInterview = int(request.POST["TotalExitInterview"])
#         for i in range(TotalExitInterview + 1):
#                 experiencedata_key = "experiencedata_ID_" + str(i)
#                 experiencedata_value = request.POST.get(experiencedata_key)
#                 mexit = Experience.objects.get(id=experiencedata_value)

#                 chekdata_key = "chekdata_" + str(i)
#                 chekdata_value = request.POST.get(chekdata_key) or 0

#                 remarkexit_key = "remarkexit_" + str(i)
#                 remarkexit_value = request.POST.get(remarkexit_key) or 0

               

#                 detailssopex = exitinterviewmaster.objects.create(
#                     Experience=mexit, Exitinterviewdata=exits, chekdata=chekdata_value, remarkexit=remarkexit_value,
                   
#                     OrganizationID=OrganizationID, CreatedBy=UserID)
                
#         TotalRatingviewdata = int(request.POST["TotalRatingviewdata"])
#         for i in range(TotalRatingviewdata + 1):
#                 ratingleveing_key = "ratingleveing_ID_" + str(i)
#                 ratingleveing_value = request.POST.get(ratingleveing_key)
#                 rats = Rating.objects.get(id=ratingleveing_value)

#                 remarks_key = "remarks_" + str(i)
#                 remarks_value = request.POST.get(remarks_key) or 0

                

               

#                 ratesdata = ExitRating.objects.create(
#                     Rating=rats, Exitinterviewdata=exits, remarks=remarks_value, 
                   
#                     OrganizationID=OrganizationID, CreatedBy=UserID)
#         messages.success(request, 'Exit Interview Add successfully!!')        
#         Success = True
#         encrypted_id = encrypt_id(EmpID)  
#         url = reverse('Warning_Letters')  
#         redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}"
#         return redirect(redirect_url)        
#     context = {
#         'reasons': reasons,
#         'experiencedatas': experiencedatas,
#         'ratingleveings': ratingleveings,
       
#      }
#     return render(request, "Interview/Exit_add.html", context)


        
from HumanResources.models import EmployeeWorkDetails
 
def Exit_Add(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID = request.session.get("UserID")
  
    EmpID = request.GET.get('EmpID')
    
    
    EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
    warning_instance = {
        'EmployeeCode': EmpDetails.EmployeeCode,
        'EmpName': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
        'Department': EmpDetails.Department,
        'Designation': EmpDetails.Designation,
        'DateofJoining' : EmpDetails.DateofJoining,
        'OrganizationID':EmpDetails.OrganizationID,
    }
   
    reasons = Reason_for_Leaving.objects.filter(IsDelete=False)
    experiencedatas = Experience.objects.filter(IsDelete=False)
    ratingleveings = Rating.objects.filter(IsDelete=False)
    
    if request.method == 'POST':
       
        employee_code = request.POST.get('EmployeeCode')
        EmpName = request.POST.get('EmpName')
        job_title = request.POST.get('Designation')
        date_of_joining = request.POST.get('DateofJoining')
        department = request.POST.get('Department')
        date_of_leaving = request.POST.get('DateofLeaving')
        notice_period = request.POST.get('NoticePeriod')  
        reason_for_leaving = request.POST.get('reasons')
        final_comment = request.POST.get('FinalComment')
        Resign = request.POST.get('Resign')
        Termination = request.POST.get('Termination')
        hotel = request.POST.get('hotel')
        statusrehire = request.POST.get('rehire')
       
        rehire = False    
        if statusrehire == 'Yes':
            rehire = True
   
        
        exits = Exitinterviewdata.objects.create(
            Employee_Code=employee_code,
            EmpName=EmpName,
            Job_Title=job_title,
            DateofJoining=date_of_joining,
            Department=department,
            DateofLeaving=date_of_leaving,
            NoticePeriod=notice_period,  
            ReasonForLeaving=reason_for_leaving, 
            FinalComment=final_comment,
            rehire=rehire,
            Resign=Resign,
            Termination=Termination,
            hotel=hotel,
            OrganizationID=OrganizationID,
            CreatedBy=UserID
        )

        
        TotalExitInterview = int(request.POST["TotalExitInterview"])
        for i in range(TotalExitInterview + 1):
            experiencedata_key = f"experiencedata_ID_{i}"
            experiencedata_value = request.POST.get(experiencedata_key)

            if experiencedata_value:  
                mexit = Experience.objects.get(id=experiencedata_value)
                chekdata_value = request.POST.get(f"chekdata_{i}", 'no')
                remarkexit_value = request.POST.get(f"remarkexit_{i}", 'no')

                exitinterviewmaster.objects.create(
                    Experience=mexit,
                    Exitinterviewdata=exits,
                    chekdata=chekdata_value,
                    remarkexit=remarkexit_value,
                    OrganizationID=OrganizationID,
                    CreatedBy=UserID
                )

        
        TotalRatingviewdata = int(request.POST["TotalRatingviewdata"])
        for i in range(TotalRatingviewdata + 1):
            ratingleveing_key = f"ratingleveing_ID_{i}"
            ratingleveing_value = request.POST.get(ratingleveing_key)

            if ratingleveing_value:  
                rats = Rating.objects.get(id=ratingleveing_value)
                remarks_value = request.POST.get(f"remarks_{i}", 0)

                ExitRating.objects.create(
                    Rating=rats,
                    Exitinterviewdata=exits,
                    remarks=remarks_value,
                    OrganizationID=OrganizationID,
                    CreatedBy=UserID
                )
        try:
            employee_work_details = EmployeeWorkDetails.objects.get(
                    EmpID=EmpID, OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False)
            employee_work_details.EmpStatus = "Left"
            employee_work_details.ModifyBy = UserID
            employee_work_details.save()
        except EmployeeWorkDetails.DoesNotExist:
                print("EmployeeWorkDetails record not found.")
 
        messages.success(request, 'Exit Interview added successfully!')

        Success = True
        encrypted_id = encrypt_id(EmpID)  
        url = reverse('ExitInterview')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}"
        return redirect(redirect_url)

    
    context = {
        'reasons': reasons,
        'experiencedatas': experiencedatas,
        'ratingleveings': ratingleveings,
        'warning_instance': warning_instance  
    }

    return render(request, "Interview/Exit_add.html", context)






def Exit_Edit(request):

    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    id = request.GET.get('id')
    Page  = request.GET.get('Page')
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    
    UserID = request.session.get("UserID")

    exit_instance = get_object_or_404(Exitinterviewdata, id=id)
    reasons = Reason_for_Leaving.objects.filter(IsDelete=False)
    experiencedatas = Experience.objects.filter(IsDelete=False)
    ratingleveings = Rating.objects.filter(IsDelete=False)
    exit_interviews = exitinterviewmaster.objects.filter(Exitinterviewdata=exit_instance)

    # experiencedata_ids = exit_interviews.values_list('Experience_id', flat=True)
  
  
    EmpID = request.GET.get('EmpID')
   
    exit_ratings = {exit_rating.Rating.id: exit_rating.remarks for exit_rating in ExitRating.objects.filter(Exitinterviewdata=exit_instance)}

    experience_remarks = {exit.Experience_id: exit.remarkexit for exit in exit_interviews}
    experience_chekdata = {exit.Experience_id: exit.chekdata for exit in exit_interviews}
    
    
    if request.method == 'POST':
        employee_code = request.POST.get('EmployeeCode', '')
        EmpName = request.POST.get('EmpName', '')
        job_title = request.POST.get('Designation', '')
        date_of_joining = request.POST.get('DateofJoining', '')
        department = request.POST.get('Department', '')
        date_of_leaving = request.POST.get('DateofLeaving', '')
        notice_period = request.POST.get('NoticePeriod', '')  
        reason_for_leaving = request.POST.get('reasons', '')
        FinalComment = request.POST.get('FinalComment', '')
        Resign = request.POST.get('Resign', '')
        hotel= request.POST.get('hotel', '')
        Termination = request.POST.get('Termination', '')
        Absconding = request.POST.get('Absconding', '')
        statusrehire = request.POST.get('rehire')
       
        rehire = False    
        if statusrehire == 'Yes':
            rehire = True
   
   
        exit_instance.Employee_Code = employee_code
        exit_instance.EmpName = EmpName
        exit_instance.Job_Title = job_title
        exit_instance.DateofJoining = date_of_joining
        exit_instance.Department = department
        exit_instance.DateofLeaving = date_of_leaving
        exit_instance.NoticePeriod = notice_period
        exit_instance.ReasonForLeaving = reason_for_leaving
        exit_instance.FinalComment = FinalComment
        exit_instance.rehire = rehire
        exit_instance.Resign = Resign
        exit_instance.hotel = hotel
        exit_instance.Termination = Termination
        exit_instance.Absconding = Absconding
        exit_instance.ModifyBy = UserID
        exit_instance.ModifyDateTime = datetime.now()

        exit_instance.save()

       
        TotalExitInterview = int(request.POST.get("TotalExitInterview", 0))
        exitinterviewmaster.objects.filter(Exitinterviewdata=exit_instance).delete()  
        
        for i in range(TotalExitInterview + 1):
            experiencedata_key = "experiencedata_ID_" + str(i)
            experiencedata_value = request.POST.get(experiencedata_key)
            
            if experiencedata_value:
                try:
                    mexit = Experience.objects.get(id=experiencedata_value)

                    chekdata_key = "chekdata_" + str(i)
                    chekdata_value = request.POST.get(chekdata_key, 0)

                    remarkexit_key = "remarkexit_" + str(i)
                    remarkexit_value = request.POST.get(remarkexit_key, 0)

                    exitinterviewmaster.objects.create(
                        Experience=mexit, Exitinterviewdata=exit_instance, 
                        chekdata=chekdata_value, remarkexit=remarkexit_value,
                        OrganizationID=OrganizationID, CreatedBy=UserID
                    )
                except Experience.DoesNotExist:
                    print(f"Experience with id {experiencedata_value} does not exist.")  

        
        TotalRatingviewdata = int(request.POST.get("TotalRatingviewdata", 0))
        ExitRating.objects.filter(Exitinterviewdata=exit_instance).delete()  
        
        for i in range(TotalRatingviewdata + 1):
            ratingleveing_key = "ratingleveing_ID_" + str(i)
            ratingleveing_value = request.POST.get(ratingleveing_key)
            
            if ratingleveing_value:
                try:
                    rats = Rating.objects.get(id=ratingleveing_value)

                    remarks_key = "remarks_" + str(i)
                    remarks_value = request.POST.get(remarks_key, 0)

                    ExitRating.objects.create(
                        Rating=rats, Exitinterviewdata=exit_instance, 
                        remarks=remarks_value, OrganizationID=OrganizationID, CreatedBy=UserID
                    )
                except Rating.DoesNotExist:
                    print(f"Rating with id {ratingleveing_value} does not exist.")  
        try:
            employee_work_details = EmployeeWorkDetails.objects.get(
                    EmpID=EmpID, OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False)
            employee_work_details.EmpStatus = "Left"
            employee_work_details.ModifyBy = UserID
            employee_work_details.ModifyDateTime = datetime.now()

            employee_work_details.save()
        except EmployeeWorkDetails.DoesNotExist:
                print("EmployeeWorkDetails record not found.")
        messages.success(request, 'Exit Interview Edit successfully!') 
        if Page == 'Exit_list':
            return redirect('Exit_list')
        Success = True
        encrypted_id = encrypt_id(EmpID)  
        url = reverse('ExitInterview')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}"
        return redirect(redirect_url)

    context = {
        'reasons': reasons,
        'experiencedatas': experiencedatas,
        'ratingleveings': ratingleveings,
        'exit': exit_instance,
        'experience_chekdata': experience_chekdata,  
        'experience_remarks': experience_remarks,
        'exit_ratings': exit_ratings  
    }
    return render(request, "Interview/Exit_edit.html", context)




from django.db.models import Subquery, OuterRef
from HumanResources.models import EmployeePersonalDetails
from app.Global_Api import get_organization_list


def Exit_list(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    UserType = request.session.get("UserType")   
    
    print("Show Page Session")
   
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
   
    memOrg = get_organization_list(OrganizationID)  
    
    
    selectedOrganizationID = request.GET.get('hotel', str(OrganizationID))

    # if UserType == 'CEO' and request.GET.get('hotel') is None:
    #     selectedOrganizationID = 401
    
    emp_id_subquery = Subquery(
        EmployeePersonalDetails.objects.filter(
            EmployeeCode=OuterRef('Employee_Code'),
            IsDelete=False
        ).values('EmpID')[:1]
    )
    
    if selectedOrganizationID == 'all':
        exitinterviews = Exitinterviewdata.objects.filter(IsDelete=False).annotate(
        EmpID=emp_id_subquery).order_by('-id')
    else:
        exitinterviews = Exitinterviewdata.objects.filter(IsDelete=False, hotel=selectedOrganizationID).annotate(
        EmpID=emp_id_subquery).order_by('-id')

    context = {
        'exitinterviews': exitinterviews,
        'memOrg': memOrg,
        'selectedOrganizationID': selectedOrganizationID,
    }
    
    return render(request, "Interview/Exit_list.html", context)



def Exitdelete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    
    UserID =str(request.session["UserID"])
    EmpID = request.GET.get('EmpID')
    id=request.GET.get('ID')
    
    exit=Exitinterviewdata.objects.get(id=id)
    exit.IsDelete=True
    exit.ModifyBy=UserID
    exit.ModifyDateTime=datetime.now()

    exit.save()
    Success = 'Deleted'        
    encrypted_id = encrypt_id(EmpID)
    url = reverse('ExitInterview')  
    redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
    return redirect(redirect_url)   
   

    
    

from datetime import datetime

def Exit_Detail(request, exit_id):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    OID = request.GET.get('OID')
    if OID:
        OrganizationID = OID

    # Fetch the exit interview data
    exit_interview = Exitinterviewdata.objects.filter(id=exit_id, OrganizationID=OrganizationID).first()

    if not exit_interview:
        return redirect('Exit_list')

    # Format DateofLeaving
    formatted_date = None
    if exit_interview.DateofLeaving:
        try:
            formatted_date = datetime.strptime(exit_interview.DateofLeaving, "%Y-%m-%d").strftime("%d-%m-%Y")
        except ValueError:
            formatted_date = exit_interview.DateofLeaving  # If parsing fails, use the original value

    # Fetch related experiences and ratings
    experiences = exitinterviewmaster.objects.filter(Exitinterviewdata=exit_interview)
    ratings = ExitRating.objects.filter(Exitinterviewdata=exit_interview)

    # Pass formatted_date to context
    context = {
        'exit_interview': exit_interview,
        'experiences': experiences,
        'ratings': ratings,
        'formatted_date': formatted_date,  # Include the formatted date
    }

    return render(request, "Interview/Exit_detail.html", context)
