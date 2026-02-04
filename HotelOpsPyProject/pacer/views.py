from django.shortcuts import render,redirect
from .models import Task,HotelOpDetails,projectss,user
from django.http import HttpResponse, HttpResponseRedirect
from requests import Session, post
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.db.models import Count, Q

# Create your views here.
def task_add(request):
    
    memOrg = {}  

    
    if 'OrganizationID' not in request.session:
        
        return redirect('MasterAttribute.Host') 
    else:
        print("Show Page Session")
        
        OrganizationID = request.session.get("OrganizationID")
    
    
    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {
        'hotel-api-token': hotelapitoken  
    }

   
    api_url = f"https://hotelops.in/api/PyAPI/ManningDepartment?OrganizationID={OrganizationID}"
    
    try:
        
        response = requests.get(api_url, headers=headers)
        response.raise_for_status() 
        memOrg = response.json() 
    except requests.exceptions.RequestException as e:
       
        print(f"Error occurred: {e}")
    
    
    UserID = request.session.get("UserID")
    prolist = projectss.objects.filter(IsDelete=False)
    Userlist = user.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
    task_id = request.GET.get('ID')
    task = None
    if task_id is not None:
        task = get_object_or_404(Task,id=task_id,OrganizationID=OrganizationID)
    if request.method=="POST":
        if task_id is not None:
            task.task_name= request.POST['task_name']
            task.add_info= request.POST['add_info']
            
            task.responsible_user= request.POST['responsible_user']
            task.department= request.POST['department']
            task.project= request.POST['project']
            task.link_of_project= request.POST['link_of_project']
            task.link_title= request.POST['link_title']
            task.contact_full_name= request.POST['contact_full_name']
            task.contact_email= request.POST['contact_email']
            task.status= request.POST['status']
            task.DayBefore= request.POST['DayBefore']
            task.ModifyBy =UserID
            task.save()
            return redirect('task_list')
        else:
            task_name= request.POST['task_name']
            add_info= request.POST['add_info']
           
            responsible_user= request.POST['responsible_user']
            department = request.POST.get('department')  
            if department: 
                try:
                
                  s = Task.objects.create(department=department)
                except Exception as e:
                 
                  print(f"Error occurred while creating task: {e}")
            project= request.POST['project']
            link_of_project= request.POST['link_of_project']
            link_title= request.POST['link_title']
            contact_full_name= request.POST['contact_full_name']
            contact_email= request.POST['contact_email']
            status= request.POST['status']
            DayBefore= request.POST['DayBefore']
            tasks =Task.objects.create(task_name=task_name,add_info=add_info,
                                    responsible_user=responsible_user,department=department,project=project,
                                    link_of_project=link_of_project,link_title=link_title,contact_full_name=contact_full_name,
                                    contact_email=contact_email,status=status,DayBefore=DayBefore,OrganizationID=OrganizationID,CreatedBy=UserID)
            
            return redirect('task_list')
        
    context={'task':task ,'memOrg':memOrg ,'prolist':prolist,  'Userlist':Userlist}            
    return render(request,'task/task_add.html',context)



def task_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID = request.session["OrganizationID"]

   
    department_api_url =  f"https://hotelops.in/api/PyAPI/ManningDepartment?OrganizationID={OrganizationID}"  # Replace with your department API URL
    try:
        department_response = requests.get(department_api_url)
        department_response.raise_for_status()
        department_data = department_response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching department data: {e}")
        department_data = []

    
    hotel_api_token = MasterAttribute.HotelAPIkeyToken
    headers = {'hotel-api-token': hotel_api_token}
    organization_api_url = f"https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    try:
        organization_response = requests.get(organization_api_url, headers=headers)
        organization_response.raise_for_status()
        memOrg = organization_response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching organization data: {e}")
        memOrg = {}

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    opening_dates = HotelOpDetails.objects.filter(OrganizationID=OrganizationID, IsDelete=False)

    is_ceo_or_gm = request.session.get('UserType') in ['CEO', 'GM']

    if is_ceo_or_gm:
        tasklist = Task.objects.filter(OrganizationID=OrganizationID, IsDelete=False)
    else:
        department_filter = request.GET.get('department')  
        if department_filter:
            tasklist = Task.objects.filter(OrganizationID=OrganizationID, department=department_filter, IsDelete=False).order_by('-id')  
        else:
            tasklist = Task.objects.filter(OrganizationID=OrganizationID, IsDelete=False).order_by('-id')  

    status = request.GET.get('status')
    project = request.GET.get('project')

    if status:
        tasklist = tasklist.filter(status=status)

    if project:
        tasklist = tasklist.filter(project=project)

    context = {'tasklist': tasklist, 'memOrg': memOrg, 'department_data': department_data}
    return render(request, 'task/task_list.html', context)



def task_delet(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    taskdelet=Task.objects.get(id=id)
    taskdelet.IsDelete=True
    taskdelet.ModifyBy=UserID
    taskdelet.save()
    return redirect('task_list')


def updatestuts(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    if request.method == 'POST':
       
        task_id = request.POST.get('task_id')
        new_status = request.POST.get('new_status')
        task = Task.objects.get(id=task_id)
        task.status = new_status
        task.save()
    else:
        return redirect('task_list')  
    return render(request, 'task/task_list.html')
        
       
        
       
        
       
    

from django.db.models import Count
import requests
from datetime import datetime, timedelta



def filtertask(request):
    # if 'OrganizationID' not in request.session:
    #     return redirect(MasterAttribute.Host)
    # else:
    #     OrganizationID = request.session["OrganizationID"]

    # # Check if user type is CEO or GM
    # UserType = request.session.get("UserType")
    # if UserType not in ['CEO', 'GM']:
    #     # Redirect the user to an unauthorized page or return an error response
    #     return HttpResponse("Unauthorized access")
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])

    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {'hotel-api-token': hotelapitoken}  
    api_url = f"https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

    UserID = str(request.session["UserID"])

   
    enddate = datetime.now().date()
    startdate = enddate - timedelta(days=7)

    opening_dates = HotelOpDetails.objects.get(OrganizationID=OrganizationID, IsDelete=False)
   
    location = projectss.objects.filter(OrganizationID=OrganizationID, IsDelete=False).count()
    tasks_within_period = Task.objects.filter(OrganizationID=OrganizationID, IsDelete=False, CreatedDateTime__gte=startdate, CreatedDateTime__lte=enddate).count()
    
    total_tasks = Task.objects.filter(OrganizationID=OrganizationID, IsDelete=False).count()
    completed_tasks = Task.objects.filter(OrganizationID=OrganizationID, IsDelete=False, status='Completed').count()
    
    if total_tasks > 0:
        remaining_tasks_percentage = ((total_tasks - completed_tasks) / total_tasks) * 100
    else:
        remaining_tasks_percentage = 100  

    total_contracts = Task.objects.filter(OrganizationID=OrganizationID, IsDelete=False).count()
   
    pending_tasks_countss = Task.objects.filter(OrganizationID=OrganizationID, IsDelete=False, status='Pending').count()

    inprogress_tasks_count = Task.objects.filter(OrganizationID=OrganizationID, IsDelete=False, status='In_Progress').count()
    due_soon_count = Task.objects.filter(OrganizationID=OrganizationID, IsDelete=False, status='Not_Started').count()

    departments = Task.objects.filter(OrganizationID=OrganizationID, IsDelete=False).values('department').annotate(task_count=Count('id'))

    department_tasks = {}
    for department in departments:
        department_name = department['department']
        tasks = Task.objects.filter(OrganizationID=OrganizationID, IsDelete=False, department=department_name)
        
        pending_tasks_count = tasks.filter(status='Pending').count()
        progres_tasks_count = tasks.filter(status='In_Progress').count()
        total_tasks_count = department['task_count']
        completed_tasks_count = tasks.filter(status='completed').count()
        
       

        department_tasks[department_name] = {
            'task_count': total_tasks_count, 
            'pending_task_count': pending_tasks_count,
            'progres_tasks_count': progres_tasks_count, 
            'completed_tasks_count': completed_tasks_count,
           
        }
    context = {
        'memOrg': memOrg,
        'total_contracts': total_contracts,
        'department_tasks': department_tasks,
        'remaining_tasks_percentage': remaining_tasks_percentage,
        'pending_tasks_countss': pending_tasks_countss,
        'inprogress_tasks_count': inprogress_tasks_count,
        'due_soon_count': due_soon_count,
        'opening_dates': opening_dates,
        'date_range': [{'startdate': startdate + timedelta(days=i), 'enddate': startdate + timedelta(days=i+1)} for i in range(7)],
        'tasks_within_period_count': tasks_within_period,
        'location':location
    }
    return render(request, 'task/filtertask.html', context)








def  masteradd(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
            OrganizationID =request.session["OrganizationID"]
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
        'hotel-api-token': hotelapitoken  
        }
    api_url = "https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID="+str(OrganizationID)
       

    try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  
            memOrg = response.json()
        
    except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
  
   
    
    UserID =str(request.session["UserID"])
    admin_id = request.GET.get('ID')
    admin = None
    if admin_id is not None:
        admin = get_object_or_404(projectss,id=admin_id,OrganizationID=OrganizationID)
    if request.method == "POST":
       if admin_id is not None:
            admin.project_open_date = request.POST['project_open_date']
            # admin.project_name = request.POST['project_name']
            admin.Location = request.POST['Location']
            admin.ModifyBy =UserID
            admin.save()
       else:
            project_open_date = request.POST['project_open_date']
            # project_name = request.POST['project_name']
            Location = request.POST['Location']
            admin = projectss.objects.create(project_open_date=project_open_date,  Location=Location, OrganizationID=OrganizationID,CreatedBy=UserID)
            return redirect('masterlist')
    context={'admin':admin, 'memOrg':memOrg}
    return render(request, 'task/masteradd.html',context)
        
        
       
            
        
        
            
    


def masterlist(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    adminlist=projectss.objects.filter(IsDelete=False,OrganizationID=OrganizationID) 
    context={'adminlist':adminlist}
    return render(request, 'task/masterlist.html',context)
        
def masterdelete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    delet=projectss.objects.get(id=id)
    delet.IsDelete=True
    delet.ModifyBy=UserID
    delet.save()
    return redirect('masterlist')




def deshboard_hod(request):
    # if 'OrganizationID' not in request.session:
    #     return redirect(MasterAttribute.Host)
    # elif request.session.get('UserType') != 'hod':
    #     # Redirect the user to an unauthorized page or return an error response
    #     return HttpResponse("Unauthorized access")

    OrganizationID = request.session.get("OrganizationID")
    
    
    opening_dates = HotelOpDetails.objects.get(OrganizationID=OrganizationID, IsDelete=False)
    hod_department = request.session.get("Department_Name")
    
   
    if not hod_department:
        return HttpResponse("Department information not found for the logged-in HOD")
    
    
    hod_tasks = Task.objects.filter(OrganizationID=OrganizationID,department=hod_department)
    
    total_tasks_count = hod_tasks.count()
    completed_tasks_count = hod_tasks.filter(status='Completed').count()
    pending_tasks_count = hod_tasks.filter(status='Pending').count()
    notStarted_tasks_count = hod_tasks.filter(status='Not_Started').count()
    notApplicable_tasks_count = hod_tasks.filter(status='Not_Applicable').count()
    pastdue_tasks_count = hod_tasks.filter(status='In_Completed').count()
    inprogess_tasks_count = hod_tasks.filter(status='In_Progress').count()

    if total_tasks_count > 0:
       completed_tasks_percentage = (completed_tasks_count / total_tasks_count) * 100
       pending_tasks_percentage = (pending_tasks_count / total_tasks_count) * 100
    else:
        completed_tasks_percentage = 0
        pending_tasks_percentage = 0
    
    return render(request, 'task/deshboard_hod.html', {
        'total_tasks_count': total_tasks_count,
        'completed_tasks_count': completed_tasks_count,
        'pending_tasks_count': pending_tasks_count,
        'notStarted_tasks_count': notStarted_tasks_count,
        'notApplicable_tasks_count': notApplicable_tasks_count,
        'opening_dates':opening_dates,
        'pastdue_tasks_count':pastdue_tasks_count,
        'inprogess_tasks_count':inprogess_tasks_count,
        'completed_tasks_percentage': completed_tasks_percentage,
        'pending_tasks_percentage': pending_tasks_percentage,
    })