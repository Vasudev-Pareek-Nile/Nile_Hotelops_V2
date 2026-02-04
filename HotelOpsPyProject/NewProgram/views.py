from django.shortcuts import render,redirect
from .models import  area,Location,project_review,Front_admin,front_perent,Notes1,Notes2,Notes3,Notes4,Notes5,front_subchild,publicarea_details,administrative_details,metting_details,lobby,front_child,Frontss_details,Front_of_House,front_public_area,front_administrative,guest_room,Notes6
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.shortcuts import get_object_or_404
# Create your views here.
def Master_Add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    add_id = request.GET.get('ID')
    add = None
    if add_id is not None:
        add = get_object_or_404(area,id=add_id,OrganizationID=OrganizationID)

    if request.method == "POST":
        if add_id is not None:
             add.area_name = request.POST['area_name']
             add.ModifyBy=UserID
             add.save()
        else:
            area_name = request.POST['area_name']
            s = area.objects.create(area_name=area_name,OrganizationID=OrganizationID,CreatedBy=UserID)

        return redirect('Master_list')
    context={'add':add}
    return render(request,'program/Master_Add.html',context)
    
       
       
        



def Master_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    


    # add = area.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    arenn = Location.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'arenn':arenn}
    return render(request,'program/Master_list.html',context)

def Master_delet(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    a=Location.objects.get(id=id)
    a.IsDelete=True
    a.ModifyBy=UserID
    a.save()
    return redirect('Master_list')


def Master_location1(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    prolist = area.objects.filter(IsDelete=False)
    are_id = request.GET.get('ID')
    are = None
    if are_id is not None:
        are = get_object_or_404(Location,id=are_id,OrganizationID=OrganizationID)
    if request.method == "POST":
        if are_id is not None:
            are.location_name = request.POST['location_name']
            are.arean = request.POST['arean']
            are.ModifyBy=UserID
            are.save()
            return redirect('Master_list')
           
        else:
            location_name = request.POST['location_name']
            arean = request.POST['arean']
            s = Location.objects.create(location_name=location_name,arean=arean,OrganizationID=OrganizationID,CreatedBy=UserID)
            return redirect('Master_list')
    context={'prolist':prolist,'are':are}
    return render(request,'program/Master_location1.html',context)



def list_project(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    project_area = project_review.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'project_area':project_area}
    return render(request,'program/list_project.html',context)



def project_delet(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    project=project_review.objects.get(id=id)
    project.IsDelete=True
    project.ModifyBy=UserID
    project.save()
    return redirect('list_project')

    


    
def add_project(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    arenn = Location.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    
    pro_id = request.GET.get('ID')
    pro = None
    if pro_id is not None:
        pro = get_object_or_404(project_review,id=pro_id,OrganizationID=OrganizationID)
    if request.method =="POST":
        if pro_id is not None:
            pro.title=request.POST['title']
            pro.project= request.POST['project']
            pro.height_bulding=request.POST['height_bulding']
            pro.structure_type=request.POST['structure_type']
            pro.total_area=request.POST['total_area']
            pro.structure_levels=request.POST['structure_levels']
            pro.built_area=request.POST['built_area']
            pro.no_of_room=request.POST['no_of_room']
            pro.guest_size=request.POST['guest_size']
            pro.room_mix=request.POST['room_mix']
            pro.lenth=request.POST['lenth']
            pro.barth=request.POST['barth']
            pro.net=request.POST['net']
            
            pro.ModifyBy=UserID
            pro.save()
            return redirect('list_project')
            
        else:
            title=request.POST['title']
            project= request.POST['project']
            height_bulding=request.POST['height_bulding']
            structure_type=request.POST['structure_type']
            total_area=request.POST['total_area']
            structure_levels=request.POST['structure_levels']
            built_area=request.POST['built_area']
            no_of_room=request.POST['no_of_room']
            guest_size=request.POST['guest_size']
            room_mix=request.POST['room_mix']
            
            lenth = request.POST.getlist('lenth')
            barth = request.POST.getlist('barth')
            net = request.POST.getlist('net')

            # Check if lengths of lists match
            if len(lenth) != len(barth) or len(barth) != len(net):
                print("Error: Lengths of lists don't match")
            else:
                for i in range(len(lenth)):
                    len_val = lenth[i]
                    barth_val = barth[i]
                    net_val = net[i]
                    
                    print(f"length: {len_val}, barth: {barth_val}, net: {net_val}")
            pro = project_review.objects.create(project=project,height_bulding=height_bulding,structure_type=structure_type,
                                                total_area=total_area,structure_levels=structure_levels,
                                                built_area=built_area,no_of_room=no_of_room,guest_size=guest_size,room_mix=room_mix,
                                                title=title,lenth=lenth,barth=barth,net=net,OrganizationID=OrganizationID,CreatedBy=UserID)
            return redirect('list_project')

    context={'pro':pro,'arenn':arenn}
    return render(request,'program/add_project.html',context)   




from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
import uuid
from datetime import datetime



def project_pdf(request):
    id = request.GET.get('ID')
    if id is None:
        return HttpResponse("ID parameter is missing.")
    
    try:
        check = project_review.objects.get(id=id)
    except project_review.DoesNotExist:
        return HttpResponse("Project review with provided ID does not exist.")
    
    OrganizationID = request.session.get("OrganizationID")
    arenn = Location.objects.filter(IsDelete=False, OrganizationID=OrganizationID)
    title =""
    for a in arenn:
        if title=="" or a.arean!=title:
            a.title=a.arean
            title=a.arean
        else:
            a.title=""
    template_path = 'program/project_pdf.html'
    context = {'check': check, 'arenn': arenn}
   
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    
    pisa_status = pisa.CreatePDF(html, dest=response)
   
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
      


def front_add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    Fronts = Front_admin.objects.filter(IsDelete=False, OrganizationID=OrganizationID)
   
    
    perents = front_perent.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    subchilds = front_subchild.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    
    childs = front_child.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    public = front_public_area.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    admini = front_administrative.objects.filter(IsDelete=False,OrganizationID=OrganizationID)

   
    fron_id = request.GET.get('ID')
    fron = None
    if fron_id is not None:
        fron = get_object_or_404(Front_of_House,id=fron_id,OrganizationID=OrganizationID)
    if request.method=="POST":
        if fron_id is not None:
            fron.date = request.POST['date']
            fron.location = request.POST['location']
            fron.project_number = request.POST['project_number']
            fron.hotel_key = request.POST['hotel_key']
            fron.guest_room_floors = request.POST['guest_room_floors']
            fron.hotel_bays = request.POST['hotel_bays']
            fron.reqvered_parking_spaces = request.POST['reqvered_parking_spaces']
           
            fron.Region_name = request.POST['Region_name']
            fron.Location_Index = request.POST['Location_Index']
            fron.Parking_Required = request.POST['Parking_Required']
            fron.Swimming_Pool = request.POST['Swimming_Pool']
            fron.Parking_Levels = request.POST['Parking_Levels']
            fron.Structural_System = request.POST['Structural_System']
            fron.Corridor_Requirements = request.POST['Corridor_Requirements']
            fron.Security_Requirements = request.POST['Security_Requirements']
            fron.Meeting_Space = request.POST['Meeting_Space']
            fron.Feed_Employees = request.POST['Feed_Employees']
            fron.Stairwells = request.POST['Stairwells']
            fron.Laundry_Services = request.POST['Laundry_Services']
            fron.Guest_Transportation = request.POST['Guest_Transportation']
            fron.Uniform_Distribution = request.POST['Uniform_Distribution']
            fron.ModifyBy=UserID
            fron.save()
        else:

            date = request.POST['date']
            location = request.POST['location']
            project_number = request.POST['project_number']
            hotel_key = request.POST['hotel_key']
            guest_room_floors = request.POST['guest_room_floors']
            hotel_bays = request.POST['hotel_bays']
            reqvered_parking_spaces = request.POST['reqvered_parking_spaces']

            totalroom=request.POST['totalroom']
            totalkey=request.POST['totalkey']
            guestroom=request.POST['guestroom']
            lobbytotal=request.POST['lobbytotal']
            mettingtotal=request.POST['mettingtotal']
            additionaltotal=request.POST['additionaltotal']
            administrativetotal=request.POST['administrativetotal']


            
            Region_name = request.POST['Region_name']
            Location_Index = request.POST['Location_Index']
            Parking_Required = request.POST['Parking_Required']
            Swimming_Pool = request.POST['Swimming_Pool']
            Parking_Levels = request.POST['Parking_Levels']
            Structural_System = request.POST['Structural_System']
            Corridor_Requirements = request.POST['Corridor_Requirements']
            Security_Requirements = request.POST['Security_Requirements']
            Meeting_Space = request.POST['Meeting_Space']
            Feed_Employees = request.POST['Feed_Employees']
            Stairwells = request.POST['Stairwells']
            Laundry_Services = request.POST['Laundry_Services']
            Guest_Transportation = request.POST['Guest_Transportation']
            Uniform_Distribution = request.POST['Uniform_Distribution']
            s = Front_of_House.objects.create(date=date,location=location,project_number=project_number,hotel_key=hotel_key,guest_room_floors=guest_room_floors,
                                            hotel_bays=hotel_bays,reqvered_parking_spaces=reqvered_parking_spaces,totalroom=totalroom,
                                            Region_name=Region_name,Location_Index=Location_Index,Parking_Required=Parking_Required,
                                            Swimming_Pool=Swimming_Pool,Parking_Levels=Parking_Levels,Structural_System=Structural_System,Corridor_Requirements=Corridor_Requirements,
                                            Security_Requirements=Security_Requirements,Meeting_Space=Meeting_Space,Feed_Employees=Feed_Employees,Stairwells=Stairwells,
                                            Laundry_Services=Laundry_Services,totalkey=totalkey,guestroom=guestroom,lobbytotal=lobbytotal,mettingtotal=mettingtotal,Guest_Transportation=Guest_Transportation,Uniform_Distribution=Uniform_Distribution,
                                            additionaltotal=additionaltotal,administrativetotal=administrativetotal,OrganizationID=OrganizationID,CreatedBy=UserID)
            Total = int(request.POST["Total"])
            for i in range(Total + 1):
                Fronts_key = "Fronts_ID_" + str(i)
                Fronts_value = request.POST.get(Fronts_key)
                FA = Front_admin.objects.get(id=Fronts_value,OrganizationID=OrganizationID,CreatedBy=UserID)
                squermitter_key = "squermitter_" + str(i) 
                squermitter_value = request.POST.get(squermitter_key) or 0
                
                print("_____")
                print(Fronts_key)
                print(Fronts_value)
                squer = Frontss_details.objects.create(
                                                   Front_admin=FA,Front_of_House=s,squermitter=squermitter_value,OrganizationID=OrganizationID,CreatedBy=UserID )
                                                        
                                                        
                                                                        
                
            Totalroom = int(request.POST["Totalroom"])
            for i in range(Totalroom+1):
                perents_key = "perents_ID_" + str(i)
                perents_value = request.POST.get(perents_key)
                Fp = front_perent.objects.get(id=perents_value,OrganizationID=OrganizationID,CreatedBy=UserID)

                roomkey_key = "roomkey_" + str(i)
                roomkey_value = request.POST.get(roomkey_key)
                totalSquer_key = "totalSquer_" + str(i)
                totalSquer_value = request.POST.get(totalSquer_key) 
                roomtotal = guest_room.objects.create( front_perent=Fp,Front_of_House=s,roomkey=roomkey_value,totalSquer=totalSquer_value,OrganizationID=OrganizationID,CreatedBy=UserID)



            totallobby = int(request.POST["totallobby"])
            for i in range(totallobby+1):
                subchilds_key = "subchilds_ID_" + str(i)
                subchilds_value = request.POST.get(subchilds_key)
                subchildss = front_subchild.objects.get(id=subchilds_value,OrganizationID=OrganizationID,CreatedBy=UserID)

                lobbysquermeter_key = "lobbysquermeter_" + str(i)
                lobbysquermeter_value = request.POST.get(lobbysquermeter_key)
                
                lobbytotal = lobby.objects.create( front_subchild=subchildss,Front_of_House=s,lobbysquermeter=lobbysquermeter_value,OrganizationID=OrganizationID,CreatedBy=UserID)

            Totalmetting = int(request.POST["Totalmetting"])
            for i in range(Totalmetting+1):
                childs_key = "childs_ID_" + str(i)
                childs_value = request.POST.get(childs_key)
                child = front_child.objects.get(id=childs_value,OrganizationID=OrganizationID,CreatedBy=UserID)

                mettingsquer_key =  "mettingsquer_" + str(i)
                mettingsquer_value = request.POST.get(mettingsquer_key)
                metting = metting_details.objects.create(front_child=child,Front_of_House=s,mettingsquer=mettingsquer_value,OrganizationID=OrganizationID,CreatedBy=UserID)


            Totalpublic = int(request.POST["Totalpublic"])
            for i in range(Totalpublic+1):
                public_key = "public_ID_" + str(i)
                public_value = request.POST.get(public_key)
                publics = front_public_area.objects.get(id=public_value,OrganizationID=OrganizationID,CreatedBy=UserID)

                public_squermeter_key =  "public_squermeter_" + str(i)
                public_squermeter_value = request.POST.get(public_squermeter_key)
                pub = publicarea_details.objects.create(front_public_area=publics,Front_of_House=s,public_squermeter=public_squermeter_value,OrganizationID=OrganizationID,CreatedBy=UserID)
            
            TotalAdmini = int(request.POST["TotalAdmini"])
            for i in range(TotalAdmini+1):
                admini_key = "admini_ID_" + str(i)
                admini_value = request.POST.get(admini_key)
                ad = front_administrative.objects.get(id=admini_value,OrganizationID=OrganizationID,CreatedBy=UserID)

                administartive_squermeter_key =  "administartive_squermeter_" + str(i)
                administartive_squermeter_value = request.POST.get(administartive_squermeter_key)
                admi = administrative_details.objects.create(front_administrative=ad,Front_of_House=s,administartive_squermeter=administartive_squermeter_value,OrganizationID=OrganizationID,CreatedBy=UserID)
                return redirect('Front_list')
                     
            

            
    context={'fron':fron,'Fronts':Fronts,'perents':perents,'subchilds':subchilds,'childs':childs,'public':public,'admini':admini}
    return render(request,'program/front_add.html',context)



def Front_ad(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    
    front_id = request.GET.get('ID')
    front = None
    if front_id is not None:
        front = get_object_or_404(Front_admin,id=front_id,OrganizationID=OrganizationID)
    if request.method == "POST":
        if front_id is not None:
            front.Title = request.POST['Title']
            front.name = request.POST['name']
            front.ModifyBy=UserID
            front.save()
            return redirect('Front_admin_list')
           
        else:
            Title = request.POST['Title']
            name = request.POST['name']
            s = Front_admin.objects.create(Title=Title,name=name,OrganizationID=OrganizationID,CreatedBy=UserID)
            return redirect('Front_admin_list')
    context={'front':front}
    

    return render(request,'program/Front_admin.html',context)


def Front_admin_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    Front = Front_admin.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'Front':Front}
    return render(request,'program/Front_admin_list.html',context)



def front_delet(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    front=Front_admin.objects.get(id=id)
    front.IsDelete=True
    front.ModifyBy=UserID
    front.save()
    return redirect('Front_admin_list')



 
    
def Front_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    house = Front_of_House.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'house':house}
    return render(request,'program/Front_list.html',context)
    
        
def front(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    front=Front_of_House.objects.get(id=id)
    front.IsDelete=True
    front.ModifyBy=UserID
    front.save()
    return redirect('Front_list')








        

   
       
        
def admin(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    if request.method=="POST":
        name = request.POST['name']
        s = front_perent.objects.create(name=name,OrganizationID=OrganizationID,CreatedBy=UserID)
        return redirect('admin_list')


    return render(request,'program/admin.html')



def admin_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    add_list = front_perent.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'add_list':add_list}
    return render(request,'program/admin_list.html',context)

def admin_delet(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    front=front_perent.objects.get(id=id)
    front.IsDelete=True
    front.ModifyBy=UserID
    front.save()
    return redirect('admin_list')



def admin_subchild_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    add_subchild = front_subchild.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'add_subchild':add_subchild}
    return render(request,'program/admin_subchild_list.html',context)


def admin_subchild_delet(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    subchild=front_subchild.objects.get(id=id)
    subchild.IsDelete=True
    subchild.ModifyBy=UserID
    subchild.save()
    return redirect('admin_list')


def admin_subchild_add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
   
    if request.method=="POST":
        Sub_name = request.POST['Sub_name']
        name1 = request.POST['name1']
        s = front_subchild.objects.create(Sub_name=Sub_name,name1=name1,OrganizationID=OrganizationID,CreatedBy=UserID)
        return redirect('admin_list')

    return render(request,'program/admin_subchild_add.html')

def admin_child_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    add_child = front_child.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'add_child':add_child,}


    return render(request,'program/admin_child_list.html',context)



def admin_child_add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    if request.method=="POST":
        child_name = request.POST['child_name']
        s = front_child.objects.create(child_name=child_name,OrganizationID=OrganizationID,CreatedBy=UserID)
        return redirect('admin_list')
    return render(request,'program/admin_child_add.html')



def admin_child_delete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    front=front_child.objects.get(id=id)
    front.IsDelete=True
    front.ModifyBy=UserID
    front.save()
    return redirect('admin_list')


def front_pdf(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    FOH=Front_of_House.objects.get(id=id)

    Fronts = Front_admin.objects.filter(IsDelete=False, OrganizationID=OrganizationID)
    
    
    Fron = Frontss_details.objects.filter(Front_of_House=FOH,IsDelete=False,OrganizationID=OrganizationID)

    


    perents = front_perent.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    room = guest_room.objects.filter(Front_of_House=FOH,IsDelete=False,OrganizationID=OrganizationID)



    subchilds = front_subchild.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    Suport_area = lobby.objects.filter(Front_of_House=FOH,IsDelete=False,OrganizationID=OrganizationID)



    childs = front_child.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    metting = metting_details.objects.filter(Front_of_House=FOH,IsDelete=False,OrganizationID=OrganizationID)





    publics = front_public_area.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    publicareas = publicarea_details.objects.filter(Front_of_House=FOH,IsDelete=False,OrganizationID=OrganizationID)

    admins = front_administrative.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    offices = administrative_details.objects.filter(Front_of_House=FOH,IsDelete=False,OrganizationID=OrganizationID)
    

    Facilities = Notes1.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    guestroom = Notes2.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    lobbynotes = Notes3.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    meetingnotes = Notes4.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    publicnotes = Notes5.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    officesnotes = Notes6.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    template_path = 'program/front_pdf.html'
    context = {'FOH': FOH,'Fronts':Fronts,'perents':perents,'subchilds':subchilds,'childs':childs,
               'publics':publics,'admins':admins,'Fron':Fron,'room':room,'Suport_area':Suport_area,'metting':metting,'publicareas':publicareas,'offices':offices,'Facilities':Facilities,'guestroom':guestroom,'lobbynotes':lobbynotes,'meetingnotes':meetingnotes,'publicnotes':publicnotes,'officesnotes':officesnotes}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

   
    pisa_status = pisa.CreatePDF(
    html, dest=response, listview=Front_list)
    
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


    
    
    
   
   

    








   


def publicarea(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    if request.method=="POST":
        public1 = request.POST['public1']
        public2 = request.POST['public2']
        s = front_public_area.objects.create(public1=public1,public2=public2,OrganizationID=OrganizationID,CreatedBy=UserID)
        return redirect('publicarea_list')
    return render(request,'program/publicarea.html')


def publicarea_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    add_public = front_public_area.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'add_public':add_public}
    return render(request,'program/publicarea_list.html',context)



def administrative_add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    if request.method=="POST":
        administrative = request.POST['administrative']
        
        s = front_administrative.objects.create(administrative=administrative,OrganizationID=OrganizationID,CreatedBy=UserID)
        return redirect('administrative_list')

    return render(request,'program/administrative_add.html')



def administrative_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    admini = front_administrative.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'admini':admini}
    return render(request,'program/administrative_list.html',context)





def notes1_add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    if request.method=="POST":
        Notes_name1 = request.POST['Notes_name1']
        
        s = Notes1.objects.create(Notes_name1=Notes_name1,OrganizationID=OrganizationID,CreatedBy=UserID)
        return redirect('notes1_list')

    return render(request,'program/notes1_add.html')


def notes1_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    Note1 = Notes1.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'Note1':Note1}
    return render(request,'program/notes1_list.html',context)




def Notes2_add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    if request.method=="POST":
        Notes_name2 = request.POST['Notes_name2']
        
        s = Notes2.objects.create(Notes_name2=Notes_name2,OrganizationID=OrganizationID,CreatedBy=UserID)
        return redirect('Notes2_list')

    return render(request,'program/Notes2_add.html')


def Notes2_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    Note2 = Notes2.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'Note2':Note2}
    return render(request,'program/Notes2_list.html',context)



def notes3_add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    if request.method=="POST":
        Notes_name3 = request.POST['Notes_name3']
        
        s = Notes3.objects.create(Notes_name3=Notes_name3,OrganizationID=OrganizationID,CreatedBy=UserID)
        return redirect('notes3_list')
    return render(request,'program/notes3_add.html')

def notes3_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    Note3 = Notes3.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'Note3':Note3}
    return render(request,'program/notes3_list.html',context)



def notes4_add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    if request.method=="POST":
        Notes_name4 = request.POST['Notes_name4']
        
        s = Notes4.objects.create(Notes_name4=Notes_name4,OrganizationID=OrganizationID,CreatedBy=UserID)
        return redirect('notes4_list')
    return render(request,'program/notes4_add.html')


def notes4_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    Note4 = Notes4.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'Note4':Note4}
    return render(request,'program/notes4_list.html',context)

def notes5_add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    if request.method=="POST":
        Notes_name5 = request.POST['Notes_name5']
        
        s = Notes5.objects.create(Notes_name5=Notes_name5,OrganizationID=OrganizationID,CreatedBy=UserID)
        return redirect('notes4_list')
    return render(request,'program/notes5_add.html')

def notes5_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    
    Note5 = Notes5.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    context={'Note5':Note5}
    return render(request,'program/notes5_list.html',context)
