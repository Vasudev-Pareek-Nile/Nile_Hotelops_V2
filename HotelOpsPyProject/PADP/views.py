from django.shortcuts import render,redirect
from .models import Objective_Master,Attribute_Master,Ineffective_Indicators_Master,Effective_Indicators_Master,Entry_Master,Leadership_Details,Leadership_AttributeDetails,Effective_Indicators_Details_Appraisee,Effective_Indicators_Details_Appraisor,Ineffective_Indicators_Details_Appraisee,Ineffective_Indicators_Details_Appraisor,SPECIFIC_MEASURABLE_ACHIEVABLE,SPECIFIC_MEASURABLE_ACHIEVABLE_Details,SUMMARY_AND_ACKNOWLEDGEMENT,Approval_Submit_Status_PADP,FINAL_PERFORMANCE_RATING,calculate_appraisal_date, calculate_next_date,Get_next_approval_level, Entry_Master_Log, APADP_Master_Log

from hotelopsmgmtpy.GlobalConfig  import MasterAttribute
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db  import connection, transaction
from Manning_Guide.models import LavelAdd


from HumanResources.views import EmployeeDetailsData, Salary_Detail_Master
from django.http import JsonResponse



# Helper Function to Get Approver by Role
# def get_next_stage_approver(role, organization_id):
#     # from Master.models import Employee  # or wherever your Employee model is

#     role = role.upper()

#     try:
#         approver = EmployeeWorkDetails.objects.filter(
#             Designation__iexact=role,
#             OrganizationID=organization_id,
#             IsDelete=False
#         ).first()

#         approver_empcode = EmployeePersonalDetails.objects.filter(
#             EmpID=approver.EmpID,
#             OrganizationID=approver.OrganizationID,
#             IsEmployeeCreated = True,
#             IsDelete=False
#         ).first()

#         if approver:
#             full_name = f"{approver_empcode.FirstName} {approver_empcode.LastName}"
#             return approver_empcode.EmployeeCode, full_name
#             # return approver.EmpID,approver_empcode.EmployeeCode, approver_empcode.FirstName, approver_empcode.LastName
#     except Exception as e:
#         print("Approver lookup error:", e)
#         return None, None

#     return None, None

# def update_pending_info(entry):
#     stages_order = ["HR", "EP", "AR", "RD", "HRA", "CEO"]
#     stages = {
#         "HR": entry.hr_actionOnDatetime,
#         "EP": entry.ep_actionOnDatetime,
#         "AR": entry.ar_actionOnDatetime,
#         "RD": entry.rd_actionOnDatetime,
#         "HRA": entry.hr_ar_actionOnDatetime,
#         "CEO": entry.ceo_actionOnDatetime,
#     }

#     latest_stage = None
#     latest_datetime = None

#     for stage in stages_order:
#         if stages[stage]:
#             if not latest_datetime or stages[stage] > latest_datetime:
#                 latest_datetime = stages[stage]
#                 latest_stage = stage

#     if latest_stage:
#         current_index = stages_order.index(latest_stage)
#         if current_index + 1 < len(stages_order):
#             next_stage = stages_order[current_index + 1]
#             emp_code, emp_name = get_next_stage_approver(next_stage, entry.OrganizationID)
#             if emp_code:
#                 entry.Pending_From_Emp_Code = emp_code
#                 entry.Pending_From_Emp_Name = emp_name
#                 entry.save()

# Objective_Master_List
def Objective_Master_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])

    Ojbs =  Objective_Master.objects.filter(
                                            IsDelete=False
                                            )
    
    context = {'Ojbs':Ojbs}

    return render(request,"PADPAPP/MASTER/Objective_Master_List.html",context)

# Objective Master Add
@transaction.atomic
def Objective_Master_Add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    obj_id = request.GET.get("ID")
    o_data = None
    if obj_id is not None:
        o_data = get_object_or_404(Objective_Master,id=obj_id,IsDelete=False)
    Levels  =  LavelAdd.objects.filter(IsDelete=False)    
    with transaction.atomic():
        if request.method == "POST":
            # Edit of Objective_Master_Add
            if obj_id is not None:
                Level = request.POST['level']
                Title = request.POST['Objective']
                Definitions = request.POST['Definition']

                o_data.Level=Level
                o_data.Title=Title
                o_data.Definitions=Definitions
                o_data.ModifyBy=UserID
                o_data.save()
                messages.success(request,"Objective Master Updated Successfully")        
                return redirect('Objective_Master_List')

            else:    
                # ADD of Objective_Master_Add
                Level = request.POST['level']
                Title = request.POST['Objective']
                Definitions = request.POST['Definition']
                obj = Objective_Master.objects.create(
                                                    CreatedBy=UserID,Level=Level,Title=Title,Definitions=Definitions)
                messages.success(request,"Objective Master Added Successfully")        
                return redirect('Objective_Master_List')


    context ={'o_data':o_data,'Levels':Levels}
    return render(request,"PADPAPP/MASTER/Objective_Master_Add.html",context)


# Objective Master Delete


@transaction.atomic
def Objective_Master_Delete(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")

     OrganizationID = request.session["OrganizationID"]
     UserID = str(request.session["UserID"])
     id = request.GET.get("ID")
     with transaction.atomic():
        OBJ = Objective_Master.objects.get(id = id)
        OBJ.IsDelete =True
        OBJ.ModifyBy =  UserID
        OBJ.save()
        messages.warning(request,"Objective Master Deleted Succesfully")
        return redirect('Objective_Master_List')
     

# Attribute_Master

# Attribute_Master_List
def Attribute_Master_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    O_ID=request.GET.get('O_ID')

    attr =  Attribute_Master.objects.filter(IsDelete=False,Objective_Master_id=O_ID
                                            )
   

    context = {'attr':attr,'O_ID':O_ID}

    return render(request,"PADPAPP/MASTER/Attribute_Master_List.html",context)




# Attribute  Add
@transaction.atomic
def Attribute_Master_Add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    obj_id = request.GET.get("O_ID")
   
    obj = Objective_Master.objects.get(id=obj_id,IsDelete=False)
    obj_name = obj.Title
    attr_id = request.GET.get("ID")
    a_data = None
    if attr_id is not None:
        a_data = get_object_or_404(Attribute_Master,id=attr_id,IsDelete=False)
    with transaction.atomic():
        if request.method == "POST":
            # Edit of Attribute_Master_Add
            if attr_id is not None:
                Title =request.POST['Title']
                RL = request.POST.get('RL')
                
                RL_H = False
                RL_M = False
                RL_L = False

                if RL == "H":
                    RL_H = True
                elif RL == "M":
                    RL_M = True
                elif RL == "L":
                    RL_L = True

                a_data.RL_H = RL_H
                a_data.RL_M = RL_M
                a_data.RL_L = RL_L

                a_data.Title = Title
                a_data.Objective_Master = obj
                a_data.ModifyBy = UserID 
                a_data.save()
                messages.success(request,"Attribute Updated Successfully")

            else: 

                # Add Attribute_Master_Add   
                Title =request.POST['Title']

                RL = request.POST['RL']
               
                
                RL_H = False
                RL_M = False
                RL_L = False

                if RL == "H":
                    RL_H = True
                elif RL == "M":
                    RL_M = True
                elif RL == "L":
                    RL_L = True    

                Atr= Attribute_Master.objects.create(Title=Title,Objective_Master=obj,CreatedBy=UserID,RL_H=RL_H,RL_M= RL_M,RL_L=RL_L)
                
                messages.success(request,"Attribute Added Successfully")        
            return redirect("/PADP/Attribute_Master_List/?O_ID="+str(obj_id))


    context ={'a_data':a_data,'obj_name':obj_name}
    return render(request,"PADPAPP/MASTER/Attribute_Master_Add.html",context)




# Attribute Master Delete


@transaction.atomic
def Attribute_Master_Delete(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")

     OrganizationID = request.session["OrganizationID"]
     UserID = str(request.session["UserID"])
     id = request.GET.get("ID")
     with transaction.atomic():
        ATR = Attribute_Master.objects.get(id = id)
        ATR.IsDelete =True
        ATR.ModifyBy =  UserID
        obj_id = ATR.Objective_Master.id
        ATR.save()

        messages.warning(request,"Attribute Deleted Succesfully")
        return redirect("/PADP/Attribute_Master_List/?O_ID="+str(obj_id))
     




# Ineffective_Indicators_Add
@transaction.atomic
def Ineffective_Indicators_Add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    obj_id = request.GET.get("O_ID")
    
    obj = Objective_Master.objects.get(id=obj_id,IsDelete=False)
    obj_name = obj.Title
    IN_id = request.GET.get("ID")
    IN_data = None
    if IN_id is not None:
        IN_data = get_object_or_404(Ineffective_Indicators_Master,id=IN_id,IsDelete=False)
    with transaction.atomic():
        if request.method == "POST":
            # Edit Ineffective_Indicators_Add
            if IN_id is not None:
                Title =request.POST['Title']
                IN_data.Title = Title
                IN_data.Objective_Master = obj
                IN_data.ModifyBy = UserID 
                IN_data.save()
                messages.success(request,"Ineffective Indicators Updated Successfully")
            #  Add Ineffective_Indicators_Add
            else:    
                Title =request.POST['Title']
                INF= Ineffective_Indicators_Master.objects.create(Title=Title,Objective_Master=obj,CreatedBy=UserID)
                
                messages.success(request,"Ineffective Indicators Added Successfully")        
            return redirect("/PADP/Ineffective_Indicators_List/?O_ID="+str(obj_id))


    context ={'IN_data':IN_data,'obj_name':obj_name}
    return render(request,"PADPAPP/MASTER/Ineffective_Indicators_Add.html",context)


# Ineffective_Indicators_List
def Ineffective_Indicators_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    O_ID=request.GET.get('O_ID')

    Ineffective_Indicators =  Ineffective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master_id=O_ID
                                          )
    context = {'Ineffective_Indicators':Ineffective_Indicators,'O_ID':O_ID}

    return render(request,"PADPAPP/MASTER/Ineffective_Indicators_List.html",context)     




# Ineffective_Indicators_Delete
@transaction.atomic
def Ineffective_Indicators_Delete(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")

     OrganizationID = request.session["OrganizationID"]
     UserID = str(request.session["UserID"])
     id = request.GET.get("ID")
     with transaction.atomic():
        IN = Ineffective_Indicators_Master.objects.get(id = id)
        IN.IsDelete =True
        IN.ModifyBy =  UserID
        obj_id = IN.Objective_Master.id
        IN.save()

        messages.warning(request,"Ineffective Indicators Delete Succesfully")
        return redirect("/PADP/Ineffective_Indicators_List/?O_ID="+str(obj_id))





@transaction.atomic
def Ineffective_Indicators_Bulk_Delete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])

    if request.method == "POST":
        delete_ids = request.POST.getlist("delete_ids")
        
        if not delete_ids:
            messages.error(request, "No items selected for deletion.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        with transaction.atomic():
            for delete_id in delete_ids:
                try:
                    IN = Ineffective_Indicators_Master.objects.get(id=delete_id)
                    IN.IsDelete = True
                    IN.ModifyBy = UserID
                    obj_id = IN.Objective_Master.id
                    IN.save()
                except Ineffective_Indicators_Master.DoesNotExist:
                    messages.error(request, f"Item with ID {delete_id} does not exist.")
                    continue

        messages.success(request, "Selected Ineffective Indicators deleted successfully.")
        return redirect(f"/PADP/Ineffective_Indicators_List/?O_ID={obj_id}")








# Effective_Indicators_Add
@transaction.atomic
def Effective_Indicators_Add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    obj_id = request.GET.get("O_ID")
    
    obj = Objective_Master.objects.get(id=obj_id,IsDelete=False)
    obj_name = obj.Title
    EFF_id = request.GET.get("ID")
    EFF_data = None
    if EFF_id is not None:
        EFF_data = get_object_or_404(Effective_Indicators_Master,id=EFF_id,IsDelete=False)
    with transaction.atomic():
        if request.method == "POST":
            # Edit of   Effective_Indicators_Add
            if EFF_id is not None:
                Title =request.POST['Title']
                EFF_data.Title = Title
                EFF_data.Objective_Master = obj
                EFF_data.ModifyBy = UserID 
                EFF_data.save()
                messages.success(request,"Effective Indicators Updated Successfully")
            # Add of Effective_Indicators_Add
            else:    
                Title =request.POST['Title']
                EFF= Effective_Indicators_Master.objects.create(Title=Title,Objective_Master=obj,CreatedBy=UserID)
                
                messages.success(request,"Effective Indicators Added Successfully")        
            return redirect("/PADP/Effective_Indicators_List/?O_ID="+str(obj_id))


    context ={'EFF_data':EFF_data,'obj_name':obj_name}
    return render(request,"PADPAPP/MASTER/Effective_Indicators_Add.html",context)


# Effective_Indicators_List
def Effective_Indicators_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    O_ID=request.GET.get('O_ID')

    Effective_Indicators =  Effective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master_id=O_ID
                                          )
    context = {'Effective_Indicators':Effective_Indicators,'O_ID':O_ID}

    return render(request,"PADPAPP/MASTER/Effective_Indicators_List.html",context)       





# Effective_Indicators_Delete
@transaction.atomic
def Effective_Indicators_Delete(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")

     OrganizationID = request.session["OrganizationID"]
     UserID = str(request.session["UserID"])
     id = request.GET.get("ID")
     with transaction.atomic():
        EFF = Effective_Indicators_Master.objects.get(id = id)
        EFF.IsDelete =True
        EFF.ModifyBy =  UserID
        obj_id = EFF.Objective_Master.id
        EFF.save()

        messages.warning(request,"Effective Indicators Delete Succesfully")
        return redirect("/PADP/Effective_Indicators_List/?O_ID="+str(obj_id))
     


@transaction.atomic
def Effective_Indicators_Bulk_Delete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])

    if request.method == "POST":
        delete_ids = request.POST.getlist("delete_ids")
        
        if not delete_ids:
            messages.error(request, "No items selected for deletion.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        with transaction.atomic():
            for delete_id in delete_ids:
                try:
                    EFF = Effective_Indicators_Master.objects.get(id=delete_id)
                    EFF.IsDelete = True
                    EFF.ModifyBy = UserID
                    obj_id = EFF.Objective_Master.id
                    EFF.save()
                except Effective_Indicators_Master.DoesNotExist:
                    messages.error(request, f"Item with ID {delete_id} does not exist.")
                    continue

        messages.success(request, "Selected Effective Indicators deleted successfully.")
        return redirect(f"/PADP/Effective_Indicators_List/?O_ID={obj_id}")



from django.db.models import Q


from django.db.models import Q
from django.contrib import messages

def Makecopy(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
   
    UserID = str(request.session["UserID"])

    FromLevels = LavelAdd.objects.filter(
        IsDelete=False,
        lavelname__in=Objective_Master.objects.filter(IsDelete=False).values_list('Level', flat=True).distinct()
    ).order_by('lavelname')

    ToLevels = LavelAdd.objects.filter(
        IsDelete=False
    ).exclude(
        lavelname__in=Objective_Master.objects.filter(IsDelete=False).values_list('Level', flat=True).distinct()
    ).order_by('lavelname')
    
    if request.method == "POST":
        Fromlevel = request.POST.get("Fromlevel")
        Tolevel = request.POST.get("Tolevel")
        
        if not Fromlevel or not Tolevel:
            messages.error(request, "Both source level (Fromlevel) and target level (Tolevel) must be provided.")
            return redirect('Objective_Master_List')
        
        old_objectives = Objective_Master.objects.filter(Level=Fromlevel, IsDelete=False)
        
        
        for old_obj in old_objectives:
            Objective_Master.objects.create(
               CreatedBy=UserID,
                Level=Tolevel,
                Title=old_obj.Title,
                Definitions=old_obj.Definitions 
            )

        old_attributes = Attribute_Master.objects.filter(Objective_Master__Level=Fromlevel,Objective_Master__IsDelete=False, IsDelete=False)
       
        
        old_effective_indicators = Effective_Indicators_Master.objects.filter(Objective_Master__Level=Fromlevel, Objective_Master__IsDelete=False,IsDelete=False)
       
        old_ineffective_indicators = Ineffective_Indicators_Master.objects.filter(Objective_Master__Level=Fromlevel, Objective_Master__IsDelete=False,IsDelete=False)
       
        for old_attr in old_attributes:
            print(old_attr.Objective_Master.Title)
            new_obj_master = Objective_Master.objects.filter(Level=Tolevel, Title=old_attr.Objective_Master.Title, IsDelete=False).first()

            
            Attribute_Master.objects.create(
                Objective_Master=new_obj_master,
                Title=old_attr.Title,
                RL_H=old_attr.RL_H,
                RL_M=old_attr.RL_M,
                RL_L=old_attr.RL_L,
                CreatedBy=UserID,
            )
        
        
        for old_effective in old_effective_indicators:
            new_obj_master = Objective_Master.objects.filter( Level=Tolevel, Title=old_effective.Objective_Master.Title, IsDelete=False).first()
            
            Effective_Indicators_Master.objects.create(
               
                Objective_Master=new_obj_master,
                CreatedBy=UserID,
                Title=old_effective.Title
            )
        
       
        for old_ineffective in old_ineffective_indicators:
            new_obj_master = Objective_Master.objects.filter( Level=Tolevel, Title=old_ineffective.Objective_Master.Title, IsDelete=False).first()
            
            Ineffective_Indicators_Master.objects.create(
              
                Objective_Master=new_obj_master,
                CreatedBy=UserID,
                Title=old_ineffective.Title
            )

       
       
        messages.success(request, "Data copied successfully for the new level.")
        return redirect('Objective_Master_List')

    context = {'FromLevels': FromLevels, 'ToLevels': ToLevels}
    return render(request, "PADPAPP/MASTER/Makecopy.html", context)


from django.db import transaction

@transaction.atomic
def copy_previous_for_new_level(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
    new_level = request.POST.get("new_level")
    old_level = request.POST.get("old_level")
    
    if not new_level or not old_level:
        messages.error(request, "Both old level and new level must be provided.")
        return redirect('Objective_Master_List')
    
    old_objectives = Objective_Master.objects.filter(OrganizationID=OrganizationID, Level=old_level, IsDelete=False)
    
    for old_obj in old_objectives:
        Objective_Master.objects.create(
            OrganizationID=OrganizationID,
            CreatedBy=UserID,
            Level=new_level,
            Title=old_obj.Title,
            Definitions=old_obj.Definitions
        )

    old_attributes = Attribute_Master.objects.filter(Objective_Master__OrganizationID=OrganizationID, Objective_Master__Level=old_level, IsDelete=False)
    
    for old_attr in old_attributes:
        new_obj_master = Objective_Master.objects.get(OrganizationID=OrganizationID, Level=new_level, Title=old_attr.Objective_Master.Title, IsDelete=False)
        
        Attribute_Master.objects.create(
            OrganizationID=OrganizationID,
            CreatedBy=UserID,
            Objective_Master=new_obj_master,
            Title=old_attr.Title,
            RL_H=old_attr.RL_H,
            RL_M=old_attr.RL_M,
            RL_L=old_attr.RL_L
        )
    
    old_effective_indicators = Effective_Indicators_Master.objects.filter(Objective_Master__OrganizationID=OrganizationID, Objective_Master__Level=old_level, IsDelete=False)
    
    for old_effective in old_effective_indicators:
        new_obj_master = Objective_Master.objects.get(OrganizationID=OrganizationID, Level=new_level, Title=old_effective.Objective_Master.Title, IsDelete=False)
        
        Effective_Indicators_Master.objects.create(
            OrganizationID=OrganizationID,
            CreatedBy=UserID,
            Objective_Master=new_obj_master,
            Title=old_effective.Title
        )
    
    old_ineffective_indicators = Ineffective_Indicators_Master.objects.filter(Objective_Master__OrganizationID=OrganizationID, Objective_Master__Level=old_level, IsDelete=False)
    
    for old_ineffective in old_ineffective_indicators:
        new_obj_master = Objective_Master.objects.get(OrganizationID=OrganizationID, Level=new_level, Title=old_ineffective.Objective_Master.Title, IsDelete=False)
        
        Ineffective_Indicators_Master.objects.create(
            OrganizationID=OrganizationID,
            CreatedBy=UserID,
            Objective_Master=new_obj_master,
            Title=old_ineffective.Title
        )

    messages.success(request, "Data copied successfully for the new level.")
    return redirect('Objective_Master_List')


from pprint import pprint
import requests
# PADP 
from datetime import datetime, timedelta



@transaction.atomic
def PADP_Delete(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")

     OrganizationID = request.session["OrganizationID"]
     UserID = str(request.session["UserID"])
     EmpCode = request.GET.get('EmpCode')
     EmpID = request.GET.get('EmpID')

     id = request.GET.get('ID')
    #  print("id is here : = ", id)
     padp = Entry_Master.objects.get(id = id)
     padp.IsDelete =True
     padp.ModifyBy =  UserID
     padp.save()
     return redirect(f'/PADP/Userinfo?EmpCode={EmpCode}&EmpID={EmpID}') 



# List of PADP
def List_PADP(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    
    UserID = str(request.session["UserID"])
    Status = request.GET.get('Status')
    month = request.GET.get('month')
    if month is None:
        month = datetime.now().month
    if Status is None:
        Status = "False" 

    padp = Entry_Master.objects.filter(OrganizationID=OrganizationID, IsDelete=False,CreatedDateTime__month = month).order_by('-id')
    context ={'padp':padp,'Status':Status,'month':month}    
    return render(request,"PADPAPP/PADP/List_PADP.html",context)       

# CEO List


#  Approval Padp 
def Aprroval_PADP(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    
    UserID = str(request.session["UserID"]) 

    # Desigantion = request.session["Desigantion"]
    # Level = request.session["Level"]
    # Use for Filter Rights
    # padp = None 

    Status = request.GET.get('Status')
    month = request.GET.get('month')
    if month is None:
        month = datetime.now().month
    if Status is None:
        Status = "False"
    
    padp = Entry_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Submit_Status=1,CreatedDateTime__month = month)
       

    context ={'padp':padp,'Status':Status,'month':month}
    return render(request,"PADPAPP/APPROVAL/Aprroval_PADP.html",context)      


# CEO Approval List 
def CEO_Approval_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    
    UserID = str(request.session["UserID"]) 
    Level = request.session["Level"]
  
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

    I = request.GET.get('I')

    Status = request.GET.get('Status')
    month = request.GET.get('month')
    if month is None:
        month = datetime.now().month
    if Status is None:
        Status = "CEO"

    Next_Aprroval_Level = Status

    padp = None 
    if I:
        padp = Entry_Master.objects.filter(OrganizationID=I,IsDelete=False,Submit_Status=1,Next_Aprroval_Level=Next_Aprroval_Level,CreatedDateTime__month = month)
    
    else:    
        padp = Entry_Master.objects.filter(IsDelete=False,Submit_Status=1,Next_Aprroval_Level=Next_Aprroval_Level,CreatedDateTime__month = month)
        I = ""

    for entry in padp:
        for mem in memOrg:
            if entry.OrganizationID == mem['OrganizationID']:
                entry.hotel_name = mem['Organization_name']    
    context ={'padp':padp,'memOrg':memOrg,'I': I,'Status':Status,'month':month}
    return render(request,"PADPAPP/APPROVAL/CEO_Approval_List.html",context)   



# HR List To View 
def Hr_PADP_View_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    
    UserID = str(request.session["UserID"]) 
    Level = request.session["Level"]
    Status = request.GET.get('Status')
    month = request.GET.get('month')
    if month is None:
        month = datetime.now().month
    if Status is None:
        Status = "False"

    padp = Entry_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Submit_Status=1,CreatedDateTime__month = month)
    context ={'padp':padp,'Status':Status,'month':month}
    return render(request,"PADPAPP/APPROVAL/Hr_PADP_View_List.html",context)   


     

# Approval Level
def Apporve_Padp_View(request):
        if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
        else:
            print("Show Page Session")
        OrganizationID = request.session["OrganizationID"]
        
        UserID = str(request.session["UserID"])
        EmployeeCode = request.session["EmployeeCode"] 
        # Postion List
        hotelapitoken = MasterAttribute.HotelAPIkeyToken
        headers = {
        'hotel-api-token': hotelapitoken  
        }
        api_url = "http://hotelops.in/API/PyAPI/HREmployeeDataEmpCodeSelect?EmpCode="+str(EmployeeCode)+"&OID="+str(OrganizationID)
                    
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status() 
            emp_list = response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")

        Designation__url = "http://hotelops.in/api/PyAPI/ManningDesignation"
                    
        try:
            response = requests.get(Designation__url, headers=headers)
            response.raise_for_status() 
            Designations = response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")    




        joining_date_str=emp_list[0]["DateofJoining"]
        Date_of_Appraisal = calculate_appraisal_date(joining_date_str)
        emp_list[0]["Date_of_Appraisal"] = Date_of_Appraisal
        Next_Review_Date = calculate_next_date(joining_date_str)
        emp_list[0]["Next_Review_Date"] = Next_Review_Date
        
        objs =  Objective_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
        for m in objs:
            attr1= Attribute_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Objective_Master=m)
            m.Attibutes = attr1
            Effect1 = Effective_Indicators_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Objective_Master=m)
            m.Effectives = Effect1
            Infect1 = Ineffective_Indicators_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Objective_Master=m)
            m.Ineffectives = Infect1
        padp_id = request.GET.get('ID')
        padp =None
        sum_data = None
        Sal_data  =None
        Level = request.session["Level"]
        if padp_id is not None:
            if Level == "CEO":
                padp =  get_object_or_404(Entry_Master,IsDelete =False,id = padp_id)
            else:
                padp =  get_object_or_404(Entry_Master,OrganizationID =OrganizationID,IsDelete =False,id = padp_id)
            Leadership_Detail = Leadership_Details.objects.filter(Entry_Master=padp
                                                ,OrganizationID =OrganizationID,IsDelete =False)
            sum_data = get_object_or_404(SUMMARY_AND_ACKNOWLEDGEMENT,Entry_Master=padp
                                                ,OrganizationID =OrganizationID,IsDelete =False
                                                )
            Sal_data = get_object_or_404(FINAL_PERFORMANCE_RATING,Entry_Master=padp
                                              ,OrganizationID =OrganizationID,IsDelete =False) 
            
            
            for m in objs:
                
                m.LD= Leadership_Details.objects.filter(Entry_Master=padp,Objective_Master=m,
                                                OrganizationID =OrganizationID,IsDelete =False)
                
                m.SP_MEAS_ACHI = SPECIFIC_MEASURABLE_ACHIEVABLE.objects.filter(Entry_Master=padp,Objective_Master=m
                                                ,OrganizationID =OrganizationID,IsDelete =False)
                
                m.SPE_MEA_ACH_Detail = SPECIFIC_MEASURABLE_ACHIEVABLE_Details.objects.filter(SPECIFIC_MEASURABLE_ACHIEVABLE__Objective_Master=m,SPECIFIC_MEASURABLE_ACHIEVABLE__Entry_Master = padp,OrganizationID =OrganizationID,IsDelete =False)  
                
                

                
                attr1= Attribute_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Objective_Master=m)
                m.Attibutes = attr1
                for a in attr1:
                        k = Leadership_AttributeDetails.objects.filter(
                                                OrganizationID =OrganizationID,IsDelete =False,Leadership_Details__Objective_Master=m,Attribute_Master=a,Leadership_Details__Entry_Master = padp)
                        
                        a.detailatt = k

                Effect1 = Effective_Indicators_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Objective_Master=m)
                m.Effectives = Effect1
                for eff in  Effect1:
                    c = Effective_Indicators_Details_Appraisee.objects.filter(OrganizationID =OrganizationID,IsDelete =False,Entry_Master=padp,Objective_Master=m,Effective_Indicators_Master=eff,)
                
                    eff.effdetail_Appee = c
                
                    d = Effective_Indicators_Details_Appraisor.objects.filter(OrganizationID =OrganizationID,IsDelete =False,Entry_Master=padp,Objective_Master=m,Effective_Indicators_Master=eff)
                    eff.effdetail_Appor = d 
                Infect1 = Ineffective_Indicators_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Objective_Master=m)
                m.Ineffectives = Infect1
                for inff in Infect1:
                    kl = Ineffective_Indicators_Details_Appraisee.objects.filter(OrganizationID =OrganizationID,IsDelete =False,Entry_Master=padp,Objective_Master=m,Ineffective_Indicators_Master=inff
                    )    
                    inff.inffdetailAppee =  kl
                    ml = Ineffective_Indicators_Details_Appraisor.objects.filter(OrganizationID =OrganizationID,IsDelete =False,Entry_Master=padp,Objective_Master=m,Ineffective_Indicators_Master=inff
                    )    
                    inff.inffdetailAppor =  ml   
        
            


        
        
        context =    {'objs':objs,'padp':padp,'sum_data':sum_data,'padp_id':padp_id,'Sal_data':Sal_data,'emp_list':emp_list,'Designations':Designations}
        
        
        return render(request,"PADPAPP/APPROVAL/Apporve_Padp_View.html",context)      

# # Approve PADP
# def Approve_PADP(request):
#             if 'OrganizationID' not in request.session:
#                 return redirect(MasterAttribute.Host)
#             else:
#                 print("Show Page Session")
#             OrganizationID = request.session["OrganizationID"]
            
#             UserID = str(request.session["UserID"]) 
#             Level = request.session["Level"]
            
            
#             padp_id = request.GET.get('ID')
#             if Level == "CEO":
#                 padp =  Entry_Master.objects.get(IsDelete =False,id = padp_id)
#             else:    
#                 padp =  Entry_Master.objects.get(OrganizationID =OrganizationID,IsDelete =False,id = padp_id)
#             Status = request.GET.get('Status')

            
#             Approval_Status =  request.session["Level"]  
#             Appraisee_Level = padp.Aprraise_Level
#             print(padp.Aprraise_Level)
#             if Status:
#                 if Status == "1":
                    
                    
#                     Next_Aprroval_Level = Get_next_approval_level(Appraisee_Level,Approval_Status)
#                     padp.Final_Approve = False
#                     if Next_Aprroval_Level == "Apporved By CEO":
#                         padp.Final_Approve = True
#                     padp.Approval_Status = Approval_Status
#                     padp.Next_Aprroval_Level = Next_Aprroval_Level
#                 else:
#                     padp.Reject_CEO = True

#                 padp.save()
                            
                  
                
#                 ASP = Approval_Submit_Status_PADP.objects.create(Entry_Master= padp,Approval_Status= Approval_Status,OrganizationID =OrganizationID,CreatedBy=UserID) 
#                 messages.success(request,f'Aprroved By {Approval_Status}')
#                 return redirect('Aprroval_PADP')






from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO    
from xhtml2pdf import pisa
from django.template.loader import get_template
# For Showing Pdf View Of Your Cake Order 
# def PADP_View(request):
#         if 'OrganizationID' not in request.session:
#             return redirect(MasterAttribute.Host)
#         else:
#             print("Show Page Session")
#         OrganizationID = request.session["OrganizationID"]
        
#         UserID = str(request.session["UserID"]) 
        
#         objs =  Objective_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
#         for m in objs:
#             attr1= Attribute_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Objective_Master=m)
#             m.Attibutes = attr1
#             Effect1 = Effective_Indicators_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Objective_Master=m)
#             m.Effectives = Effect1
#             Infect1 = Ineffective_Indicators_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Objective_Master=m)
#             m.Ineffectives = Infect1
#         padp_id = request.GET.get('ID')
#         padp =None
#         sum_data = None
#         if padp_id is not None:
#             padp = Entry_Master.objects.filter(OrganizationID =OrganizationID,IsDelete =False,id = padp_id).first()
#             Leadership_Detail = Leadership_Details.objects.filter(Entry_Master=padp
#                                                 ,OrganizationID =OrganizationID,IsDelete =False)
#             sum_data = SUMMARY_AND_ACKNOWLEDGEMENT.objects.filter(Entry_Master=padp
#                                                 ,OrganizationID =OrganizationID,IsDelete =False).first()
            
            
#             for m in objs:
                
#                 m.LD= Leadership_Details.objects.filter(Entry_Master=padp,Objective_Master=m,
#                                                 OrganizationID =OrganizationID,IsDelete =False)
                
#                 m.SP_MEAS_ACHI = SPECIFIC_MEASURABLE_ACHIEVABLE.objects.filter(Entry_Master=padp,Objective_Master=m
#                                                 ,OrganizationID =OrganizationID,IsDelete =False)
                
#                 m.SPE_MEA_ACH_Detail = SPECIFIC_MEASURABLE_ACHIEVABLE_Details.objects.filter(SPECIFIC_MEASURABLE_ACHIEVABLE__Objective_Master=m,SPECIFIC_MEASURABLE_ACHIEVABLE__Entry_Master = padp,OrganizationID =OrganizationID,IsDelete =False)  
                
                

                
#                 attr1= Attribute_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Objective_Master=m)
#                 m.Attibutes = attr1
#                 for a in attr1:
#                         k = Leadership_AttributeDetails.objects.filter(
#                                                 OrganizationID =OrganizationID,IsDelete =False,Leadership_Details__Objective_Master=m,Attribute_Master=a,Leadership_Details__Entry_Master = padp)
                        
#                         a.detailatt = k

#                 Effect1 = Effective_Indicators_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Objective_Master=m)
#                 m.Effectives = Effect1
#                 for eff in  Effect1:
#                     c = Effective_Indicators_Details_Appraisee.objects.filter(OrganizationID =OrganizationID,IsDelete =False,Entry_Master=padp,Objective_Master=m,Effective_Indicators_Master=eff,)
                
#                     eff.effdetail_Appee = c
                
#                     d = Effective_Indicators_Details_Appraisor.objects.filter(OrganizationID =OrganizationID,IsDelete =False,Entry_Master=padp,Objective_Master=m,Effective_Indicators_Master=eff)
#                     eff.effdetail_Appor = d 
#                 Infect1 = Ineffective_Indicators_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Objective_Master=m)
#                 m.Ineffectives = Infect1
#                 for inff in Infect1:
#                     kl = Ineffective_Indicators_Details_Appraisee.objects.filter(OrganizationID =OrganizationID,IsDelete =False,Entry_Master=padp,Objective_Master=m,Ineffective_Indicators_Master=inff
#                     )    
#                     inff.inffdetailAppee =  kl
#                     ml = Ineffective_Indicators_Details_Appraisor.objects.filter(OrganizationID =OrganizationID,IsDelete =False,Entry_Master=padp,Objective_Master=m,Ineffective_Indicators_Master=inff
#                     )    
#                     inff.inffdetailAppor =  ml   
    
#         template_path = "PADPAPP/PADP/PADPVIEW.html"
#         # NileLogo=MasterAttribute.NileLogo
        
#         mydict={'objs':objs,'padp':padp,'sum_data':sum_data}
#         #  ScantyBaggageForm=forms.ScantyBaggageForm()
        
        
        

#         # context = {'myvar': 'this is your template context','p':varM}
        
#         # Create a Django response object, and specify content_type as pdf
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'filename="padp.pdf"'
#         # find the template and render it.
#         template = get_template(template_path)
#         html = template.render(mydict)

#         # create a pdf
#         result = BytesIO()
#         #  pisa_status = pisa.CreatePDF(
#         pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#             # html, dest=response, link_callback=link_callback)
#         # if error then show some funny view
#         if not pdf.err:
#             return HttpResponse(result.getvalue(), content_type = 'application/pdf')
#         return None   




def PADP_View(request):
        if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
        else:
            print("Show Page Session")
       
        UserID = str(request.session["UserID"]) 
        base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
   
        padp_id = request.GET.get('ID')
        padp =None
        sum_data = None
        columns  = None
        rowslist = None


        if padp_id is not None:
            padp = Entry_Master.objects.filter(IsDelete =False,id = padp_id).first()
            if padp:
                OrganizationID = padp.OrganizationID
            
            selected_from_year =  padp.FromReviewDate.year
            
            selected_from_month = padp.FromReviewDate.month  
           
            selected_to_year =  padp.ToReviewDate.year 
            selected_to_month =  padp.ToReviewDate.month 

           
            try:
                    with connection.cursor() as cursor:
                        # Update the SQL query to use the correct stored procedure and parameters
                        cursor.execute("""
                            EXEC sp_GetKraYearlyReportForPadp 
                                @OrganizationID=%s, 
                                @EmployeeCode=%s, 
                                @FromYear=%s, 
                                @FromMonth=%s, 
                                @ToYear=%s, 
                                @ToMonth=%s
                            """, [
                                padp.OrganizationID, 
                                padp.EmployeeCode, 
                                selected_from_year, 
                                selected_from_month, 
                                selected_to_year, 
                                selected_to_month
                            ])
                        rows = cursor.fetchall()
                        columns = [col[0] for col in cursor.description]
                        rowslist = [dict(zip(columns, row)) for row in rows]
                        columns = list(rowslist[0].keys()) if rowslist else []
                       
                       

            except Exception as e:
                        print("No Kra Details is not Found")

            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        EXEC sp_GetKraOverallRatingForPadp 
                            @OrganizationID=%s, 
                            @EmployeeCode=%s, 
                            @FromYear=%s, 
                            @FromMonth=%s, 
                            @ToYear=%s, 
                            @ToMonth=%s
                    """, [
                        padp.OrganizationID, 
                        padp.EmployeeCode, 
                        selected_from_year, 
                        selected_from_month, 
                        selected_to_year, 
                        selected_to_month
                    ])
                    result = cursor.fetchone()
                    
                    if result:
                        OverallRating = result[0]  
                    else:
                        OverallRating = None  
            except Exception as e:
                        print("No Overall Rating Details is not Found")
      
        Leadership_Detail = Leadership_Details.objects.filter(Entry_Master=padp
                                              ,IsDelete =False).first()
        sum_data = SUMMARY_AND_ACKNOWLEDGEMENT.objects.filter(Entry_Master=padp
                                              ,IsDelete =False).first()
        Sal_data = FINAL_PERFORMANCE_RATING.objects.filter(Entry_Master=padp
                                              ,IsDelete =False).first()
        sal = 'False'
        if Sal_data:
            if Sal_data.SALARY_CORRECTION or  Sal_data.PROMOTION_WITH_INCREASE or  Sal_data.PROMOTION_WITH_INCREASE:
                sal = 'True' 
        
        objs =  Objective_Master.objects.filter(IsDelete=False,Level= padp.Aprraise_Level)
        for m in objs:
            attr1= Attribute_Master.objects.filter(IsDelete=False,Objective_Master=m)
            m.Attibutes = attr1
            Effect1 = Effective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
            m.Effectives = Effect1
            Infect1 = Ineffective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
            m.Ineffectives = Infect1
        
          
        
            
        SPE_MEA_ACH_Detail = SPECIFIC_MEASURABLE_ACHIEVABLE_Details.objects.filter(SPECIFIC_MEASURABLE_ACHIEVABLE__Entry_Master = padp,IsDelete =False)
        Goal  = 'False' 
        if SPE_MEA_ACH_Detail:
            Goal = 'True'

       
        for m in objs:
            
            m.LD= Leadership_Details.objects.filter(Entry_Master=padp,Objective_Master=m,
                                              IsDelete =False)
            
            
            
            

            
            attr1= Attribute_Master.objects.filter(IsDelete=False,Objective_Master=m)
            m.Attibutes = attr1
            for a in attr1:
                    k = Leadership_AttributeDetails.objects.filter(
                                               IsDelete =False,Leadership_Details__Objective_Master=m,Attribute_Master=a,Leadership_Details__Entry_Master = padp)
                    
                    a.detailatt = k

            Effect1 = Effective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
            m.Effectives = Effect1
            for eff in  Effect1:
                c = Effective_Indicators_Details_Appraisee.objects.filter(IsDelete =False,Entry_Master=padp,Objective_Master=m,Effective_Indicators_Master=eff,)
               
                eff.effdetail_Appee = c
              
                d = Effective_Indicators_Details_Appraisor.objects.filter(IsDelete =False,Entry_Master=padp,Objective_Master=m,Effective_Indicators_Master=eff)
                eff.effdetail_Appor = d
               
            Infect1 = Ineffective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
            m.Ineffectives = Infect1

            for inff in Infect1:
                kl = Ineffective_Indicators_Details_Appraisee.objects.filter(IsDelete =False,Entry_Master=padp,Objective_Master=m,Ineffective_Indicators_Master=inff
                )    
                inff.inffdetailAppee =  kl
                ml = Ineffective_Indicators_Details_Appraisor.objects.filter(IsDelete =False,Entry_Master=padp,Objective_Master=m,Ineffective_Indicators_Master=inff
                )    
                inff.inffdetailAppor =  ml
    
        template_path = "PADPAPP/PADP/PADPVIEW.html"
        # NileLogo=MasterAttribute.NileLogo
        
        organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
        organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
        organizations = OrganizationMaster.objects.filter(OrganizationID=padp.EmployeeOrganizationID).first()
        if organizations:
            OrganizationName = organizations.OrganizationName  
        organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
        Kra_Found  =  'False'
        if columns and rowslist:
            Kra_Found  = 'True'
       

        
        
        mydict={'objs':objs,'padp':padp,'sum_data':sum_data,'SPE_MEA_ACH_Detail':SPE_MEA_ACH_Detail,'organization_logos':organization_logos,'organization_logo':organization_logo,'OrganizationName':OrganizationName,
        'rowslist':rowslist,'columns':columns,'OverallRating':OverallRating ,'Sal_data':Sal_data ,'Kra_Found':Kra_Found,'Goal':Goal ,'sal':sal    }
        #  ScantyBaggageForm=forms.ScantyBaggageForm()
        
        
        

        # context = {'myvar': 'this is your template context','p':varM}
        
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="padp.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(mydict)

        # create a pdf
        result = BytesIO()
        #  pisa_status = pisa.CreatePDF(
        pdf  = pisa.pisaDocument(BytesIO(html.encode("utf8")), result)
            # html, dest=response, link_callback=link_callback)
        # if error then show some funny view
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type = 'application/pdf')
        return None   





# Bhupendra Singh
from Manning_Guide.models import OnRollDepartmentMaster,OnRollDesignationMaster
from HumanResources.views import EmployeeNameandDesignation,EmployeeNameandDesignationFilter
from django.shortcuts import render, redirect

def PADPList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])

    # Departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)

    department_id = request.GET.get('department')
    emp_id = request.GET.get('EmployeeName')
    # print("employe name is here: ", emp_id)

    empNames = EmployeeNameandDesignationFilter(request, OrganizationID, department=department_id, emp_id=emp_id)

    # print(request.session.items())
    # print("Full name:",request.session["FullName"])

    context = {
        # 'Departments': Departments,
        'empNames': empNames
    }
    return render(request, "PADPAPP/PADPNEW/PADPList.html", context)



# from .models import EmployeePersonalDetails 
from HumanResources.models import EmployeePersonalDetails, EmployeeWorkDetails

def PADPERDC(request):

    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])

    EmpCode = request.session["EmployeeCode"]

    final_results = []
  

  
    apdpdetas = APADP.objects.filter(OrganizationID=OrganizationID, EmployeeCode=EmpCode, IsDelete=False)
    final_performance_ratings = FinalPerformancerating.objects.filter(
        APADP__in=apdpdetas, OrganizationID=OrganizationID, IsDelete=False
    )

    for rating in final_performance_ratings:
        final_results.append({
            'EmployeeCode': rating.APADP.EmployeeCode,
            'ReviewPeriod': f"From Date: {rating.APADP.review_from_date} To Date: {rating.APADP.review_to_date}",
            'FinalPerformanceRating': rating.rating,
            'SalaryIncrementOption': rating.SalaryIncrementOption,
            'Status': "Done" if rating.APADP.Status else "Pending",
            'CreatedOn': rating.CreatedDateTime.strftime('%d %b %Y'),
            'CreatedBy': rating.CreatedByUsername,
            'id': rating.APADP.id,
            'URl':'A'
        })

    entry_records = Entry_Master.objects.filter(
        OrganizationID=OrganizationID,
        EmployeeCode=EmpCode,
        IsDelete=False
    )

    for entry in entry_records:
        final_perf_record = FINAL_PERFORMANCE_RATING.objects.filter(
            Entry_Master=entry,
          
            IsDelete=False
        ).first()

        if final_perf_record:
            performance_rating = "Outstanding" if final_perf_record.OUTSTANDING  else \
                                "Above Standard" if final_perf_record.ABOVE_STANDARD else \
                                "Meets Expectation" if final_perf_record.MEETS_EXPECTATION else \
                                "Below Standard" if final_perf_record.BELOW_STANDARD else \
                                "Deficient" if final_perf_record.DEFICIENT else "Not Rated"

            
            salary_increment =  "No Correction" if final_perf_record.NO_CORRECTION   else \
                                "3 %" if final_perf_record.per_3 else  \
                                "5 %" if final_perf_record.per_5 else \
                                "8 %" if final_perf_record.per_8 else \
                                "10 %" if final_perf_record.per_10 else \
                                f"CORRECTION\n{final_perf_record.FromSalary}  To {final_perf_record.ToSalary}"  if final_perf_record.SALARY_CORRECTION else \
                                f"PROMOTION From \n{final_perf_record.FromPosition}  To {final_perf_record.ToPosition}" if final_perf_record.PROMOTION else \
                                f"PROMOTION WITH INCREAMENT \n{final_perf_record.FromSalary} To {final_perf_record.ToSalary} \n{final_perf_record.FromPosition} To\n{final_perf_record.ToPosition}" if final_perf_record.PROMOTION_WITH_INCREASE else  "Action Pending"   
        else:
            performance_rating = "Not Rated"
            salary_increment = "Not Specified"

        final_results.append({
            'EmployeeCode': entry.EmployeeCode,
            'ReviewPeriod': f"From: {entry.FromReviewDate.strftime('%d %b %Y')}\nTo: {entry.ToReviewDate.strftime('%d %b %Y')}",
            'FinalPerformanceRating': performance_rating,
            'SalaryIncrementOption': salary_increment,
            'Approval_stage': entry.Approval_stage() ,
            # 'pending_status': entry.pending_status(),
            'CreatedOn': entry.CreatedDateTime.strftime('%d %b %Y'),
            'CreatedBy': entry.CreatedByUsername,
            'id': entry.id,
            'URl':'M'
        })


    employees = EmployeePersonalDetails.objects.filter(
        IsDelete=False,
        OrganizationID=OrganizationID,
        EmployeeCode=EmpCode,
    ).values('EmpID').first()
    
    EmpID = employees['EmpID'] if employees else None

    # Correctly fetch EmpCodedetails like in Userinfo
    EmpCodedetails = EmployeeDetailsData(EmpID, OrganizationID)

    # session_data = dict(request.session)
    # print("The all session value is here::", session_data)
    context = {
        'EmpCode': EmpCode,
        'EmpCodedetails': EmpCodedetails,
        'final_results': final_results,
        'LoggedInUserID':UserID

        # 'empNames': empNames
       
    }

    

    return render(request, "PADPAPP/PADPNEW/PADPERDC.html", context)




from app.views   import  OrganizationList

from HumanResources.views import get_employee_designation_by_EmployeeCode
from django.db.models import Q


# def PADPApprove(request):

#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")

#     OrganizationID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])
#     orgs = OrganizationList(OrganizationID)
#     UserType = str(request.session["UserType"])
#     Department = request.session.get("Department_Name")
#     Departmentsession = str(Department).lower()
    
#     current_year = datetime.now().year
#     current_month = datetime.now().strftime('%m')
    
#     years = [current_year + 1, current_year, current_year - 1, current_year - 2, current_year - 3]
    
#     selected_year = request.GET.get('year', current_year)
#     selected_month = request.GET.get('month', int(current_month))
#     I = request.GET.get('I', OrganizationID)
#     SI = request.GET.getlist('SI')

#     per_3 = False
#     per_5 = False
#     per_8 = False
#     per_10 = False
#     per = []

#     if SI:
#         if '3%' in SI:
#             per_3 = True
#             p = '3%'
#             per.append(p)

#         if '5%' in SI:
#             per_5 = True
#             p = '5%'
#             per.append(p)
#         if '8%' in SI:
#             per_8 = True
#             p = '8%'
#             per.append(p)
#         if '10%' in SI:
#             per_10 = True
#             p = '10%'
#             per.append(p)

#     conditions = Q()

#     if per_3:
#         conditions |= Q(per_3=True)
#     if per_5:
#         conditions |= Q(per_5=True)
#     if per_8:
#         conditions |= Q(per_8=True)
#     if per_10:
#         conditions |= Q(per_10=True)
    
   
#     Status = request.GET.get('Status','Pending')
#     print(I,SI,Status,selected_year,selected_month)
    
#     if request.method == "POST":
#         if UserType == "CEO":
#             selected_ids = request.POST.getlist('checkbox_ids')
#             bulkAction = request.POST['bulkAction']
#             print('selected_ids = ',selected_ids)
#             if len(selected_ids)  >  0 : 
#                 for sid in selected_ids:
#                     parts = sid.split("_")

#                     if len(parts) > 1 and parts[1].isdigit():  
#                         Padp_ID = int(parts[1])
#                     else:
#                         Padp_ID = 0

#                     if "A_" in sid:
#                         print("SID  = ", sid ,  bulkAction)
#                         APADPobj  = APADP.objects.filter(IsDelete=False,id=Padp_ID).first()
#                         print(APADPobj.EmpName)
#                         APADPobj.LastApporvalStatus = bulkAction
#                         APADPobj.ceo_as = bulkAction
#                         APADPobj.ceo_actionOnDatetime =  datetime.now()
#                         APADPobj.save()
#                     if "M_" in sid:
#                         print("SID  = ", sid ,  bulkAction)
#                         Entry_Masterobj  = Entry_Master.objects.filter(IsDelete=False,id=Padp_ID).first()
#                         print(Entry_Masterobj.Appraisee_Name)
#                         Entry_Masterobj.LastApporvalStatus = bulkAction
#                         Entry_Masterobj.ceo_as = bulkAction
#                         Entry_Masterobj.ceo_actionOnDatetime =  datetime.now()

#                         Entry_Masterobj.save()
#                 return redirect('PADPApprove')

  
            
    
   

  
#     EmpCode = request.session["EmployeeCode"]
#     ReportingtoDesigantion  =   get_employee_designation_by_EmployeeCode(OrganizationID, EmpCode)
    

#     final_results = []

  
#     if UserType == "CEO" and OrganizationID == "3":
#         apdpdetas = APADP.objects.filter(IsDelete=False, CreatedDateTime__year=selected_year, CreatedDateTime__month=selected_month,LastApporvalStatus=Status,OrganizationID=I)

#         final_performance_ratings = FinalPerformancerating.objects.filter(
#             APADP__in=apdpdetas, IsDelete=False
#         )
#     elif  OrganizationID == "3":
#         apdpdetas = APADP.objects.filter(IsDelete=False,ReportingtoDesigantion= ReportingtoDesigantion,CreatedDateTime__year=selected_year, CreatedDateTime__month=selected_month,LastApporvalStatus=Status,OrganizationID=I)
       
#         final_performance_ratings = FinalPerformancerating.objects.filter(
#             APADP__in=apdpdetas, IsDelete=False
#         )
#     elif str(Departmentsession) == 'hr':    
#         apdpdetas = APADP.objects.filter(OrganizationID=OrganizationID, IsDelete=False,CreatedDateTime__year=selected_year, CreatedDateTime__month=selected_month,LastApporvalStatus=Status)

#         final_performance_ratings = FinalPerformancerating.objects.filter(
#             APADP__in=apdpdetas, OrganizationID=OrganizationID, IsDelete=False
#         )

    
#     else:    
#         apdpdetas = APADP.objects.filter(OrganizationID=OrganizationID, IsDelete=False,ReportingtoDesigantion= ReportingtoDesigantion,CreatedDateTime__year=selected_year, CreatedDateTime__month=selected_month,LastApporvalStatus=Status)
#         final_performance_ratings = FinalPerformancerating.objects.filter(
#             APADP__in=apdpdetas, OrganizationID=OrganizationID, IsDelete=False
#         )
#     if per != []:

#             for rating in final_performance_ratings.filter(SalaryIncrementOption__in=per)    :
#                 final_results.append({
#                     'EmployeeCode': rating.APADP.EmployeeCode,
#                     'Appraisee_Name' : rating.APADP.EmpName,
#                     'ReviewPeriod': f"From Date: {rating.APADP.review_from_date} <br> To Date: {rating.APADP.review_to_date}",
#                     'FinalPerformanceRating': rating.rating,
#                     'SalaryIncrementOption': rating.SalaryIncrementOption,
#                     'Approval_stage': rating.APADP.Approval_stage() ,
#                     'pending_status': rating.APADP.pending_status(),
#                     'CreatedOn': rating.CreatedDateTime.strftime('%d %b %Y'),
#                     'CreatedBy': rating.CreatedByUsername,
#                     'id': rating.APADP.id,
#                     'LastApporvalStatus':rating.APADP.LastApporvalStatus,
#                     'URl':'A',
#                     'get_organization_name':rating.APADP.get_organization_name()
#                 })
#     else:
#          for rating in final_performance_ratings    :
#                 if rating.SalaryIncrementOption == "Salary Correction":
#                     SalaryIncrementOption = f"SALARY CORRECTION  <br> From Sal. - {rating.SalaryCorrectionFrom}  To Sal. - {rating.SalaryCorrectionTo}"  

#                 elif rating.SalaryIncrementOption == "Promotion":
#                     f"PROMOTION <br> From P. - {rating.PromotionFrom}  To P. - {rating.PromotionTo}" 
#                 elif rating.SalaryIncrementOption == "Promotion with Increase":
#                     f"PROMOTION WITH INCREAMENT <br> From Sal. - {rating.SalaryCorrectionFrom}  To Sal. - {rating.SalaryCorrectionTo} <br> From P. - {rating.PromotionFrom}  To P. - {rating.PromotionTo}"   
#                 else:
#                     SalaryIncrementOption = rating.SalaryIncrementOption

#                 final_results.append({
#                     'EmployeeCode': rating.APADP.EmployeeCode,
#                     'Appraisee_Name' : rating.APADP.EmpName,
#                     'ReviewPeriod': f"From Date: {rating.APADP.review_from_date} <br> To Date: {rating.APADP.review_to_date}",
#                     'FinalPerformanceRating': rating.rating,
#                     'SalaryIncrementOption': SalaryIncrementOption,
#                     'Approval_stage': rating.APADP.Approval_stage() ,
#                     'pending_status': rating.APADP.pending_status(),
#                     'CreatedOn': rating.CreatedDateTime.strftime('%d %b %Y'),
#                     'CreatedBy': rating.CreatedByUsername,
#                     'id': rating.APADP.id,
#                       'LastApporvalStatus':rating.APADP.LastApporvalStatus,
#                     'URl':'A',
#                        'get_organization_name':rating.APADP.get_organization_name()
#                 })

        
#     if UserType == 'CEO' and  OrganizationID == "3":
#          entry_records = Entry_Master.objects.filter(
          
#             IsDelete=False,CreatedDateTime__year=selected_year, CreatedDateTime__month=selected_month,LastApporvalStatus=Status,OrganizationID=I
#         )
    
#     elif OrganizationID == "3": 
#         entry_records = Entry_Master.objects.filter(
          
#             IsDelete=False,CreatedDateTime__year=selected_year, CreatedDateTime__month=selected_month,LastApporvalStatus=Status,OrganizationID=I
#         ).filter(
#             Q(ReportingtoDesigantion=ReportingtoDesigantion) | Q(DottedLine=ReportingtoDesigantion)
#         )
#     elif str(Departmentsession) == 'hr':    
#         entry_records = Entry_Master.objects.filter(
#             OrganizationID=OrganizationID,
#             IsDelete=False,CreatedDateTime__year=selected_year, CreatedDateTime__month=selected_month,LastApporvalStatus=Status
#         )
    
#     else:
#         entry_records = Entry_Master.objects.filter(
#             OrganizationID=OrganizationID,
#             IsDelete=False,CreatedDateTime__year=selected_year, CreatedDateTime__month=selected_month,LastApporvalStatus=Status
#         ).filter(
#             Q(ReportingtoDesigantion=ReportingtoDesigantion) | Q(DottedLine=ReportingtoDesigantion)
#         )
#     final_perf_record_queryset  = FINAL_PERFORMANCE_RATING.objects.filter(
          
#         ).filter(conditions)
#     for entry in entry_records:
       

#         final_perf_record = final_perf_record_queryset.filter(Entry_Master=entry).first()

#         if final_perf_record:
#             performance_rating = "Outstanding" if final_perf_record.OUTSTANDING else \
#                                 "Above Standard" if final_perf_record.ABOVE_STANDARD else \
#                                 "Meets Expectation" if final_perf_record.MEETS_EXPECTATION else \
#                                 "Below Standard" if final_perf_record.BELOW_STANDARD else \
#                                 "Deficient" if final_perf_record.DEFICIENT else "Not Rated"

#             salary_increment =  "No Correction" if final_perf_record.NO_CORRECTION   else \
#                                 "3 %" if final_perf_record.per_3 else  \
#                                 "5 %" if final_perf_record.per_5 else \
#                                 "8 %" if final_perf_record.per_8 else \
#                                  "10 %" if final_perf_record.per_10 else \
#                                 f"SALARY CORRECTION   From Sal. - {final_perf_record.FromSalary}  To Sal. - {final_perf_record.ToSalary}"  if final_perf_record.SALARY_CORRECTION else \
#                                 f"PROMOTION From P. - {final_perf_record.FromPosition}  To P. - {final_perf_record.ToPosition}" if final_perf_record.PROMOTION else \
#                                 f"PROMOTION WITH INCREAMENT  From Sal. - {final_perf_record.FromSalary}  To Sal. - {final_perf_record.ToSalary} From P. - {final_perf_record.FromPosition}  To P. - {final_perf_record.ToPosition}" if final_perf_record.PROMOTION_WITH_INCREASE else  "Action Pending"   
#         else:
#             performance_rating = "Not Rated"
#             salary_increment = "Not Specified"

#         final_results.append({
#             'EmployeeCode': entry.EmployeeCode,
#             'Appraisee_Name' : entry.Appraisee_Name,
#              'ReviewPeriod': f"From Date: {entry.FromReviewDate.strftime('%d %b %Y')} <br> To Date: {entry.ToReviewDate.strftime('%d %b %Y')}",
#             'FinalPerformanceRating': performance_rating,
#             'SalaryIncrementOption': salary_increment,
#             'Approval_stage': entry.Approval_stage() ,
#             'pending_status': entry.pending_status(),
#              'get_organization_name':entry.get_organization_name(),
#                'LastApporvalStatus':entry.LastApporvalStatus,
           
#             'CreatedOn': entry.CreatedDateTime.strftime('%d %b %Y'),
#             'CreatedBy': entry.CreatedByUsername,
#             'id': entry.id,
#             'URl':'M'
#         })


 
#     context = {
#         'EmpCode': EmpCode,
       
#         'final_results': final_results,
#         'UserType':UserType,
#         'I':I,
#         'orgs':orgs,
#         'years': years,
#         'current_month': current_month,
#         'selected_year': selected_year,
#         'selected_month': selected_month,
#         'SI':SI,
#         'Status':Status
       
#     }
# '%d %b %Y'
    

#     return render(request, "PADPAPP/PADPNEW/PADPApprove.html", context)
# def format_date_properly(date_str):
#     try:
#         # Parse from '2021-11-01'
#         dt = datetime.strptime(date_str, '%Y-%m-%d')
#         # Format to '01 August 2025'
#         return dt.strftime('%d %B %Y')
#     except Exception as e:
#         print("Date format error:", date_str, e)
#         return date_str  # fallback to original string

from app.Global_Api import get_organization_list

def format_date_properly(date_str):
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d %b %Y')
    except Exception as e:
        return date_str  # fallback to original string


def PADPApprove(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    orgs = get_organization_list(OrganizationID)
    UserType = str(request.session["UserType"])
    Department = request.session.get("Department_Name")
    Departmentsession = str(Department).lower()

    current_year = datetime.now().year
    current_month = datetime.now().strftime('%m')
    years = [current_year + 1, current_year, current_year - 1, current_year - 2, current_year - 3]

    selected_year = request.GET.get('year', current_year)
    selected_month = request.GET.get('month', 'All')
    # selected_month = request.GET.get('month', int(current_month))
    # print("the return of month filter::", selected_month)
    I = request.GET.get('I',OrganizationID)
    if OrganizationID == "3":
        I = request.GET.get('I') or 'all'

    SI = request.GET.getlist('SI')

    per_3 = '3%' in SI
    per_5 = '5%' in SI
    per_8 = '8%' in SI
    per_10 = '10%' in SI
    per = [p for p in ['3%', '5%', '8%', '10%'] if p in SI]

    conditions = Q()
    if per_3:
        conditions |= Q(per_3=True)
    if per_5:
        conditions |= Q(per_5=True)
    if per_8:
        conditions |= Q(per_8=True)
    if per_10:
        conditions |= Q(per_10=True)

    # Status = request.GET.get('Status','All')
    Status = request.GET.get('Status','Pending')
    # print("the selected status is here::", Status)

    # Conditionally include filters based on the Status and I values
    padp_filter = {}
   
    if I != 'all':
        padp_filter['OrganizationID'] = I
    
    # if Status != 'All':
    #     padp_filter['LastApporvalStatus'] = Status

    if Status == 'Pending':  
        padp_filter['LastApporvalStatus__in'] = ['Pending', 'Submitted']
    elif Status != 'All':
        padp_filter['LastApporvalStatus'] = Status

        
    # Process POST Request for Bulk Actions
    if request.method == "POST":
        if UserType == "CEO":
            selected_ids = request.POST.getlist('checkbox_ids')
            bulkAction = request.POST['bulkAction']
            # print('selected_ids = ', selected_ids)
            if selected_ids:
                for sid in selected_ids:
                    parts = sid.split("_")
                    if len(parts) > 1 and parts[1].isdigit():
                        Padp_ID = int(parts[1])
                    else:
                        Padp_ID = 0

                    if "A_" in sid:
                        APADPobj = APADP.objects.filter(IsDelete=False, id=Padp_ID).first()
                        if APADPobj:
                            APADPobj.LastApporvalStatus = bulkAction
                            APADPobj.ceo_as = bulkAction
                            APADPobj.ceo_actionOnDatetime = datetime.now()
                            APADPobj.save()
                    if "M_" in sid:
                        Entry_Masterobj = Entry_Master.objects.filter(IsDelete=False, id=Padp_ID).first()
                        if Entry_Masterobj:
                            Entry_Masterobj.LastApporvalStatus = bulkAction
                            Entry_Masterobj.ceo_as = bulkAction
                            Entry_Masterobj.ceo_actionOnDatetime = datetime.now()
                            Entry_Masterobj.save()
                return redirect('PADPApprove')

    EmpCode = request.session["EmployeeCode"]
    ReportingtoDesigantion = get_employee_designation_by_EmployeeCode(OrganizationID, EmpCode)
    # print("ReportingtoDesigantion = ",ReportingtoDesigantion)

    final_results = []

    # Adjust queries based on filters and status
    # apdp_query = APADP.objects.filter(IsDelete=False, CreatedDateTime__year=selected_year,
    #                                 #   CreatedDateTime__month=selected_month,
    #                                   **padp_filter
    #                                )

    if selected_month == 'All':
        apdp_query = APADP.objects.filter(IsDelete=False, CreatedDateTime__year=selected_year, **padp_filter)
    else:
        apdp_query = APADP.objects.filter(IsDelete=False, CreatedDateTime__year=selected_year, CreatedDateTime__month=selected_month, **padp_filter)


    # if Status != 'All':
    #     apdp_query = apdp_query.filter(LastApporvalStatus=Status)


    # if (UserType == "CEO" or UserID == '20251209112591') and OrganizationID == "3":

    #     if apdp_query.filter(ReportingtoDesigantion="CEO").exists():
    #         apdpdetas = apdp_query.filter(ReportingtoDesigantion="CEO")
    #     else:
    #         apdpdetas = apdp_query.filter(hr_ar="Audited")


    if (UserType == "CEO" or UserID == '20251209112591') and OrganizationID == "3":
        apdpdetas = apdp_query.filter(
            Q(ReportingtoDesigantion="CEO") |
            Q(hr_ar="Audited")
        )

    elif str(Departmentsession) == 'hr':
        apdpdetas = apdp_query

    else:
        apdpdetas = apdp_query.filter(ReportingtoDesigantion=ReportingtoDesigantion)


    final_performance_ratings = FinalPerformancerating.objects.filter(APADP__in=apdpdetas, IsDelete=False)
    
    if per:
        for rating in final_performance_ratings.filter(SalaryIncrementOption__in=per):

            # print("the padp ceo status::", rating.APADP.ceo_as)
            # Inside your loop:
            review_from = format_date_properly(rating.APADP.review_from_date)
            review_to = format_date_properly(rating.APADP.review_to_date)
            final_results.append({
                'EmployeeCode': rating.APADP.EmployeeCode,
                'OrganizationID': rating.APADP.OrganizationID,
                'Aprraise_Level':rating.APADP.Level,
                'Aprraisee_position':rating.APADP.Designation,
                'Appraisee_Name': rating.APADP.EmpName,
                # 'ReviewPeriod': f"{rating.APADP.review_from_date} <br>To<br> {rating.APADP.review_to_date}",
                'ReviewPeriod': f"{review_from} <br>To<br> {review_to}",
                # 'ReviewPeriod': f"From Date: {rating.APADP.review_from_date} <br> To Date: {rating.APADP.review_to_date}",
                'FinalPerformanceRating': rating.rating,
                'SalaryIncrementOption': rating.SalaryIncrementOption,
                'Approval_stage': rating.APADP.Approval_stage(),
                # 'pending_status': rating.APADP.pending_status(),
                'CreatedOn': rating.CreatedDateTime.strftime('%d %b %Y'),
                'CreatedOnRaw': rating.CreatedDateTime,
                'CreatedBy': rating.CreatedByUsername,
                'id': rating.APADP.id,
                'LastApporvalStatus': rating.APADP.LastApporvalStatus,
                'ceo_as': rating.APADP.ceo_as,
                'URl': 'A',
                'get_organization_name': rating.APADP.get_organization_name(),
                'ceo_as_remarks':rating.APADP.ceo_as_remarks
            })
            
    else:
        for rating in final_performance_ratings:
            # print("the padp ceo status::", rating.APADP.ceo_as)

            review_from = format_date_properly(rating.APADP.review_from_date)
            review_to = format_date_properly(rating.APADP.review_to_date)
            salary_increment_option = rating.SalaryIncrementOption
            if salary_increment_option == "Salary Correction":
                salary_increment_option = f"Correction From \n {rating.SalaryCorrectionFrom}  To  {rating.SalaryCorrectionTo}"
            elif salary_increment_option == "Promotion":
                salary_increment_option = f"Promotion From \n {rating.PromotionFrom}  To  {rating.PromotionTo}"
            elif salary_increment_option == "Promotion with Increase":
                salary_increment_option = f"Promotion with Increase \n {rating.SalaryCorrectionFrom} To {rating.SalaryCorrectionTo} \n {rating.PromotionFrom}  To {rating.PromotionTo}"

            final_results.append({
                'EmployeeCode': rating.APADP.EmployeeCode,
                'OrganizationID': rating.APADP.OrganizationID,
                'Aprraise_Level':rating.APADP.Level,
                'Aprraisee_position':rating.APADP.Designation,
                'Appraisee_Name': rating.APADP.EmpName,
                # 'ReviewPeriod': f"{rating.APADP.review_from_date} <br>To<br> {rating.APADP.review_to_date}",
                'ReviewPeriod': f"{review_from} <br>To<br> {review_to}",
                # 'ReviewPeriod': f"From Date: {rating.APADP.review_from_date} <br> To Date: {rating.APADP.review_to_date}",
                'FinalPerformanceRating': rating.rating,
                'SalaryIncrementOption': salary_increment_option,
                'Approval_stage': rating.APADP.Approval_stage(),
                # 'pending_status': rating.APADP.pending_status(),
                'CreatedOn': rating.CreatedDateTime.strftime('%d %b %Y'),
                'CreatedOnRaw': rating.CreatedDateTime,  # for sorting
                'CreatedBy': rating.CreatedByUsername,
                'id': rating.APADP.id,
                'LastApporvalStatus': rating.APADP.LastApporvalStatus,
                'ceo_as': rating.APADP.ceo_as,
                'URl': 'A','ceo_as_remarks':rating.APADP.ceo_as_remarks,
                'get_organization_name': rating.APADP.get_organization_name()
            })

    if selected_month == 'All':
        entry_query = Entry_Master.objects.filter(
            IsDelete=False, 
            CreatedDateTime__year=selected_year,
            **padp_filter
        )
    else:
        entry_query = Entry_Master.objects.filter(
            IsDelete=False, 
            CreatedDateTime__year=selected_year, 
            CreatedDateTime__month=selected_month, 
            **padp_filter
        )

    # if Status != 'All':
    #     entry_query = entry_query.filter(LastApporvalStatus=Status)


    
    # if (UserType == "CEO" or UserID == "20251209112591"):
    #     entry_records = entry_query.filter(
    #         Q(hr_ar="Audited") | 
    #         (Q(ep_as="Submitted") & Q(Aprraise_Level="M5"))  
    #     )
    
    # if (UserType == "CEO" or UserID == "20251209112591"):
    #     if entry_query.filter(ReportingtoDesigantion="CEO").exists():
    #         pass
    #     else:
    #         entry_records = entry_query.filter(
    #             Q(hr_ar="Audited") | 
    #             (Q(ep_as="Submitted") & Q(Aprraise_Level="M5"))  
    #         )
    # elif str(Departmentsession) == 'hr':
    #     entry_records = entry_query
    # else:
    #     entry_records = entry_query.filter(
    #         Q(ReportingtoDesigantion=ReportingtoDesigantion) | Q(DottedLine=ReportingtoDesigantion)
    #     )
    
    
    if (UserType == "CEO" or UserID == "20251209112591"):
        entry_records = entry_query.filter(
            Q(hr_ar="Audited") | 
            (Q(ep_as="Submitted") & Q(Aprraise_Level="M5"))  
        )
    
    elif str(Departmentsession) == 'hr':
        entry_records = entry_query
    else:
        entry_records = entry_query.filter(
            Q(ReportingtoDesigantion=ReportingtoDesigantion) | Q(DottedLine=ReportingtoDesigantion)
        )
    


    # if conditions:
    #         print("if working")
    #         exclude_conditions = Q(SALARY_CORRECTION=True) | Q(PROMOTION=True) | Q(PROMOTION_WITH_INCREASE=True) | Q(PROMOTION_WITH_INCREASE=False) | Q(SALARY_CORRECTION=False) | Q(PROMOTION_WITH_INCREASE=False) | Q(NO_CORRECTION=False)  | Q(NO_CORRECTION=True)
    #         final_perf_record_queryset = FINAL_PERFORMANCE_RATING.objects.filter(conditions).exclude(exclude_conditions)
            
    # else:
    #         final_perf_record_queryset = FINAL_PERFORMANCE_RATING.objects.filter(conditions)




    for entry in entry_records:
        if conditions:
            exclude_conditions = Q(SALARY_CORRECTION=True) | Q(PROMOTION=True) | Q(PROMOTION_WITH_INCREASE=True) | Q(PROMOTION_WITH_INCREASE=False) | Q(SALARY_CORRECTION=False) | Q(PROMOTION_WITH_INCREASE=False) | Q(NO_CORRECTION=False)  | Q(NO_CORRECTION=True)
            final_perf_record = FINAL_PERFORMANCE_RATING.objects.filter(conditions,Entry_Master=entry).exclude(exclude_conditions).first()
            # print("the padp ceo status::", entry.ceo_as)
            
            if final_perf_record:
                performance_rating = "Outstanding" if final_perf_record.OUTSTANDING else \
                                    "Above Standard" if final_perf_record.ABOVE_STANDARD else \
                                    "Meets Expectation" if final_perf_record.MEETS_EXPECTATION else \
                                    "Below Standard" if final_perf_record.BELOW_STANDARD else \
                                    "Deficient" if final_perf_record.DEFICIENT else "Not Rated"

                salary_increment = "No Correction" if final_perf_record.NO_CORRECTION else \
                                "3 %" if final_perf_record.per_3 else \
                                "5 %" if final_perf_record.per_5 else \
                                "8 %" if final_perf_record.per_8 else \
                                "10 %" if final_perf_record.per_10 else \
                                f"Correction \n {final_perf_record.FromSalary} To {final_perf_record.ToSalary}" if final_perf_record.SALARY_CORRECTION else \
                                f"Promotion  \n{final_perf_record.FromPosition} To\n {final_perf_record.ToPosition}" if final_perf_record.PROMOTION else \
                                f"Promotion With Increament \n{final_perf_record.FromSalary} To {final_perf_record.ToSalary} \n {final_perf_record.FromPosition} To\n{final_perf_record.ToPosition}" if final_perf_record.PROMOTION_WITH_INCREASE else "Action Pending"
            
                final_results.append({
                    'EmployeeCode': entry.EmployeeCode,
                    'OrganizationID': entry.OrganizationID,
                    'Aprraise_Level':entry.Aprraise_Level,
                    'Aprraisee_position':entry.Aprraisee_position,
                    'Appraisee_Name': entry.Appraisee_Name,
                    'ReviewPeriod': f"{entry.FromReviewDate.strftime('%d %b %Y')} <br>To<br> {entry.ToReviewDate.strftime('%d %b %Y')}",
                    # 'ReviewPeriod': f"From Date: {entry.FromReviewDate.strftime('%d %b %Y')} <br> To Date: {entry.ToReviewDate.strftime('%d %b %Y')}",
                    'FinalPerformanceRating': performance_rating,
                    'SalaryIncrementOption': salary_increment,
                    'Approval_stage': entry.Approval_stage(),
                    'DraftBy':entry.DraftBy,
                    # 'pending_status': entry.pending_status(),
                    'get_organization_name': entry.get_organization_name(),
                    'LastApporvalStatus': entry.LastApporvalStatus,
                    'ceo_as': entry.ceo_as,
                    'CreatedOn': entry.CreatedDateTime.strftime('%d %b %Y'),
                    'CreatedOnRaw': entry.CreatedDateTime,  # for sorting
                    'CreatedBy': entry.CreatedByUsername,
                    'id': entry.id,
                    'URl': 'M'
                })
                # print("the employee organiztaion id is here:: ")
        else:
            final_perf_record = FINAL_PERFORMANCE_RATING.objects.filter(Entry_Master=entry).first()
            # print("the padp ceo status::", entry.ceo_as)


            if final_perf_record:
                performance_rating = "Outstanding" if final_perf_record.OUTSTANDING else \
                                    "Above Standard" if final_perf_record.ABOVE_STANDARD else \
                                    "Meets Expectation" if final_perf_record.MEETS_EXPECTATION else \
                                    "Below Standard" if final_perf_record.BELOW_STANDARD else \
                                    "Deficient" if final_perf_record.DEFICIENT else "Not Rated"

                salary_increment = "No Correction" if final_perf_record.NO_CORRECTION else \
                                "3 %" if final_perf_record.per_3 else \
                                "5 %" if final_perf_record.per_5 else \
                                "8 %" if final_perf_record.per_8 else \
                                "10 %" if final_perf_record.per_10 else \
                                f"Correction \nFrom - {final_perf_record.FromSalary}\nTo  {final_perf_record.ToSalary}" if final_perf_record.SALARY_CORRECTION else \
                                f"Promotion \nFrom  - {final_perf_record.FromPosition}\nTo  {final_perf_record.ToPosition}" if final_perf_record.PROMOTION else \
                                f"Promotion With Increament \n {final_perf_record.FromSalary} To {final_perf_record.ToSalary} \n {final_perf_record.FromPosition}  To \n{final_perf_record.ToPosition}" if final_perf_record.PROMOTION_WITH_INCREASE else "Action Pending"
            else:
                performance_rating = "Not Rated"
                salary_increment = "Not Specified"

            final_results.append({
                'EmployeeCode': entry.EmployeeCode,
                'OrganizationID': entry.OrganizationID,
                'Aprraise_Level':entry.Aprraise_Level,
                'Aprraisee_position':entry.Aprraisee_position,
                'Appraisee_Name': entry.Appraisee_Name,
                'ReviewPeriod': f"{entry.FromReviewDate.strftime('%d %b %Y')} <br>To<br> {entry.ToReviewDate.strftime('%d %b %Y')}",
                # 'ReviewPeriod': f"From Date: {entry.FromReviewDate.strftime('%d %b %Y')} <br> To Date: {entry.ToReviewDate.strftime('%d %b %Y')}",
                'FinalPerformanceRating': performance_rating,
                'SalaryIncrementOption': salary_increment,
                'Approval_stage': entry.Approval_stage(),
                'DraftBy':entry.DraftBy,
                # 'pending_status': entry.pending_status(),
                'get_organization_name': entry.get_organization_name(),
                'LastApporvalStatus': entry.LastApporvalStatus,
                'ceo_as': entry.ceo_as,
                'CreatedOn': entry.CreatedDateTime.strftime('%d %b %Y'),
                'CreatedOnRaw': entry.CreatedDateTime,  # for sorting
                'CreatedBy': entry.CreatedByUsername,
                
                'id': entry.id, 
                'URl': 'M'
            })        
    
    # session_data = dict(request.session)
    # print("The all session value is here::", session_data)
    for result in final_results:
        result.setdefault('CreatedOnRaw', datetime.min)
        
    final_results.sort(key=lambda x: x['CreatedOnRaw'], reverse=True)
    context = {
        'EmpCode': EmpCode,
        'final_results': final_results,
        'UserType': UserType,
        'I': I,
        'orgs': orgs,
        'years': years,
        'current_month': current_month,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'SI': SI,
        'Status': Status
    }

    return render(request, "PADPAPP/PADPNEW/PADPApprove.html", context)






from django.http import JsonResponse

def Padpceoapprove(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
    if request.method == "GET":
        PADPID = request.GET.get('PADPID')
        Status = request.GET.get('Status')
        Remarks = request.GET.get('Remarks')


        if not PADPID or not Status:
            response_data = {
                'message': 'Invalid parameters'
            }
            return JsonResponse(response_data, status=400)
        
        parts = PADPID.split("_")

        if len(parts) > 1 and parts[1].isdigit():  
            Padp_ID = int(parts[1])
        else:
            Padp_ID = 0

        hops_id = 0
        OID = 0
        Emp_Code = ''
        EmpName = ''

        if "A_" in PADPID:
            APADPobj  = APADP.objects.filter(IsDelete=False,id=Padp_ID).first()
            hops_id = APADPobj.id or 0
            OID = APADPobj.OrganizationID or 0
            Emp_Code = APADPobj.EmployeeCode
            EmpName = APADPobj.EmpName

            if APADPobj is None:
                response_data = {
                    'message': 'Object not found'
                }
                return JsonResponse(response_data, status=404)
            
            if APADPobj:
                APADP_Master_Log.objects.create(
                    APADP=APADPobj,
                    LastApporvalStatus = APADPobj.LastApporvalStatus,
                    hr_as = APADPobj.hr_as,
                    ar_as = APADPobj.ar_as,
                    hr_ar = APADPobj.hr_ar,
                    ceo_as = APADPobj.ceo_as,
                    ceo_as_remarks = APADPobj.ceo_as_remarks,
                    hr_actionOnDatetime = APADPobj.hr_actionOnDatetime,
                    ar_actionOnDatetime = APADPobj.ar_actionOnDatetime,
                    hr_ar_actionOnDatetime = APADPobj.hr_ar_actionOnDatetime,
                    ceo_actionOnDatetime = APADPobj.ceo_actionOnDatetime,

                    OrganizationID = APADPobj.OrganizationID,
                    CreatedBy = APADPobj.CreatedBy,
                )
            else:
                print("Log is not maintianed and created")

            APADPobj.LastApporvalStatus = Status
            APADPobj.ceo_as = Status
            APADPobj.ceo_as_remarks = Remarks
            APADPobj.ceo_actionOnDatetime =  datetime.now()

            
            APADPobj.save()
        if "M_" in PADPID :
            Entry_Masterobj  = Entry_Master.objects.filter(IsDelete=False,id=Padp_ID).first()
            hops_id = Entry_Masterobj.id or 0
            OID = Entry_Masterobj.OrganizationID or 0
            Emp_Code = Entry_Masterobj.EmployeeCode
            EmpName = Entry_Masterobj.Appraisee_Name

            if Entry_Masterobj is None:
                response_data = {
                    'message': 'Object not found'
                }
                return JsonResponse(response_data, status=404)
            
            if Entry_Masterobj:
                    Entry_Master_Log.objects.create(
                        Entry_Master = Entry_Masterobj,
                        LastApporvalStatus = Entry_Masterobj.LastApporvalStatus,
                        hr_as = Entry_Masterobj.hr_as,
                        ep_as = Entry_Masterobj.ep_as,
                        ar_as = Entry_Masterobj.ar_as,
                        rd_as = Entry_Masterobj.rd_as,
                        hr_ar = Entry_Masterobj.hr_ar,
                        ceo_as = Entry_Masterobj.ceo_as,
                        ceo_as_remarks = Entry_Masterobj.ceo_as_remarks,
                        hr_actionOnDatetime = Entry_Masterobj.hr_actionOnDatetime,
                        ep_actionOnDatetime = Entry_Masterobj.ep_actionOnDatetime,
                        ar_actionOnDatetime = Entry_Masterobj.ar_actionOnDatetime,
                        rd_actionOnDatetime = Entry_Masterobj.rd_actionOnDatetime,
                        hr_ar_actionOnDatetime = Entry_Masterobj.hr_ar_actionOnDatetime,
                        ceo_actionOnDatetime = Entry_Masterobj.ceo_actionOnDatetime,
                        OrganizationID = Entry_Masterobj.OrganizationID,
                        CreatedByUsername = Entry_Masterobj.CreatedByUsername,
                        CreatedBy = Entry_Masterobj.CreatedBy,
                    )
            Entry_Masterobj.LastApporvalStatus = Status
            Entry_Masterobj.ceo_as = Status
            Entry_Masterobj.ceo_as_remarks = Remarks
            Entry_Masterobj.ceo_actionOnDatetime =  datetime.now()

            Entry_Masterobj.save()

        # print('we are reached here', OID,Emp_Code)
        Send_Leave_Approval_Notification(
            organization_id=OID,
            EmpCode=Emp_Code,
            title="PADP Approved",
            message=f"{EmpName}, your PADP has been {Status}",
            module_name="PADP",
            action="Approved",
            hopsId=hops_id,
            user_type="admin",
            priority="high"
        )

        response_data = {
            'message': f'{Status} successfully'
        }
        return JsonResponse(response_data, status=200)







from HumanResources.views import EmployeeDetailsData
from django.http import JsonResponse
def Userinfo(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])

    EmpCode = request.GET.get('EmpCode')
    EmpID = request.GET.get('EmpID')
    SessionEmployeeCode = str(request.session["EmployeeCode"])


    final_results = []
    EmpCodedetails = EmployeeDetailsData(EmpID, OrganizationID)
    if EmpCodedetails:
        Level = EmpCodedetails.Level
    A = ''
    
    if Level in ['A', 'T', 'E']:
        A = 'Yes'
    if Level in ['M', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'R', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7']:
        A = 'No'

    if A == 'Yes':
        apdpdetas = APADP.objects.filter(OrganizationID=OrganizationID, EmployeeCode=EmpCode, IsDelete=False)
        final_performance_ratings = FinalPerformancerating.objects.filter(
            APADP__in=apdpdetas, OrganizationID=OrganizationID, IsDelete=False
        )

        for rating in final_performance_ratings:
            final_results.append({
                'EmployeeCode': rating.APADP.EmployeeCode,
                'Appraisee_Name': rating.APADP.EmpName,
                # 'ReviewPeriod': f"From Date: {rating.APADP.review_from_date} <br> To Date: {rating.APADP.review_to_date}",
                'ReviewPeriod_From': f"From Date: {rating.APADP.review_from_date}",
                'ReviewPeriod_To': f"To Date: {rating.APADP.review_to_date}",
                'FinalPerformanceRating': rating.rating,
                'SalaryIncrementOption': rating.SalaryIncrementOption,
                'Approval_stage': rating.APADP.Approval_stage() ,
                # 'pending_status': rating.APADP.pending_status(),
                'CreatedOn': rating.CreatedDateTime.strftime('%d %b %Y'),
                'CreatedBy': rating.CreatedByUsername,
                  'LastApporvalStatus':rating.APADP.LastApporvalStatus,
                'id': rating.APADP.id,
                'URl':'A'
            })

    else:
        entry_records = Entry_Master.objects.filter(
            OrganizationID=OrganizationID,
            EmployeeCode=EmpCode,
            IsDelete=False
        )

        for entry in entry_records:
            final_perf_record = FINAL_PERFORMANCE_RATING.objects.filter(
                Entry_Master=entry,
                OrganizationID=OrganizationID,
                IsDelete=False
            ).first()

            if final_perf_record:
                performance_rating = "Outstanding" if final_perf_record.OUTSTANDING else \
                                    "Above Standard" if final_perf_record.ABOVE_STANDARD else \
                                    "Meets Expectation" if final_perf_record.MEETS_EXPECTATION else \
                                    "Below Standard" if final_perf_record.BELOW_STANDARD else \
                                    "Deficient" if final_perf_record.DEFICIENT else "Not Rated"

                salary_increment =  "No Correction" if final_perf_record.NO_CORRECTION   else \
                                "3 %" if final_perf_record.per_3 else  \
                                "5 %" if final_perf_record.per_5 else \
                                "8 %" if final_perf_record.per_8 else \
                                   "10 %" if final_perf_record.per_10 else \
                                f"Correction \n{final_perf_record.FromSalary}  To {final_perf_record.ToSalary}"  if final_perf_record.SALARY_CORRECTION else \
                                f"Promotion From  \n{final_perf_record.FromPosition}  To {final_perf_record.ToPosition}" if final_perf_record.PROMOTION else \
                                f"Promotion With Increament \n  {final_perf_record.FromSalary} To {final_perf_record.ToSalary} \n {final_perf_record.FromPosition} To \n{final_perf_record.ToPosition}" if final_perf_record.PROMOTION_WITH_INCREASE else  "Action Pending"   
                
            else:
                performance_rating = "Not Rated"
                salary_increment = "Not Specified"

            final_results.append({
                'EmployeeCode': entry.EmployeeCode,
                'Appraisee_Name': entry.Appraisee_Name,
            #    'ReviewPeriod': f"From Date: {entry.FromReviewDate.strftime('%d %b %Y')}  To Date: {entry.ToReviewDate.strftime('%d %b %Y')}",
               'ReviewPeriod_From': f"From Date: {entry.FromReviewDate.strftime('%d %b %Y')}",
               'ReviewPeriod_To': f"To Date: {entry.ToReviewDate.strftime('%d %b %Y')}",
                'FinalPerformanceRating': performance_rating,
                'SalaryIncrementOption': salary_increment,
                'Approval_stage': entry.Approval_stage() ,
                # 'pending_status': entry.pending_status(),
             'LastApporvalStatus':entry.LastApporvalStatus,
                'CreatedOn': entry.CreatedDateTime.strftime('%d %b %Y'),
                'CreatedBy': entry.CreatedByUsername,
                'id': entry.id,
                'URl':'M'
            })
    # print("your employee organization id is here::",EmpCodedetails.OrganizationID)
    context = {
        'EmpCode': EmpCode,
        'EmpCodedetails': EmpCodedetails,
        'final_results': final_results,
        'A': A,
        'SessionEmployeeCode':SessionEmployeeCode
    }

    return render(request, "PADPAPP/PADPNEW/Userinfo.html", context)



from django.shortcuts import render, redirect
from .models import Master_APADP_Item, Master_APADP_SubItem,APADP,Master_APADP_SubItemDetail,DevelopmentGoalsApdpa,FinalPerformancerating

from HumanResources.views import EmployeeDetailsData,MultipleDepartmentofEmployee

def convert_date_format(date_str):
   
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d") 
        return date_obj  
    except ValueError:
        return "Invalid date format"


from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
def Refresh_View(request, apadp_id):
    
    try:
        empdata = APADP.objects.get(id=apadp_id)
        OrganizationID = empdata.OrganizationID
        EmployeeCode = empdata.EmployeeCode

        if EmployeeCode and OrganizationID:
            EmployeePersonalDetailsIDFromCode = EmployeePersonalDetails.objects.filter(
                EmployeeCode=EmployeeCode,
                OrganizationID=OrganizationID,
                IsDelete=0
            ).first()

            if EmployeePersonalDetailsIDFromCode is None:
                return HttpResponse("Error: Employee personal details not found.", status=404)
            
            EmpID = EmployeePersonalDetailsIDFromCode.EmpID

            NewCTC = 0
            if EmpID is not None:
                # print("empid  found")
                ctc_salary_details = Salary_Detail_Master.objects.filter(
                    Salary_title__Title='CTC (A+C)', IsDelete=False,
                    OrganizationID=OrganizationID, EmpID=EmpID
                ).order_by('-id').first()

                if ctc_salary_details:
                    # print("the function is here")
                    NewCTC = ctc_salary_details.Permonth
                else:
                    NewCTC=0
                    # print("the function is not found")
            else:
                print("empid not found at Refresh_View")

            EmployeeWorkDetails2 = EmployeeWorkDetails.objects.filter(
                EmpID=EmpID,
                IsDelete=0,
                IsSecondary=0
            ).first()

            if EmployeeWorkDetails2 is None:
                return HttpResponse("Error: Employee work details not found.", status=404)

            EmpCodedetails = EmployeeDetailsData(EmpID, OrganizationID)


            empdata.ReportingtoDesigantion = EmployeeWorkDetails2.ReportingtoDesignation
            empdata.EmpName = EmpCodedetails.full_name if EmpCodedetails else ''
            empdata.Designation = EmployeeWorkDetails2.Designation
            empdata.Department = EmployeeWorkDetails2.Department
            empdata.Level = EmployeeWorkDetails2.Level
            empdata.ReportingtoLevel = EmployeeWorkDetails2.ReportingtoLevel
            empdata.DateofJoining = EmployeeWorkDetails2.DateofJoining
            empdata.Current_Salary = NewCTC

            try:
                empdata.save()
            except Exception as e:
                return HttpResponse("Data is not saved properly.", status=500)

        else:
            return HttpResponse("Error: Employee Code and Organization details not found.", status=500)

        # Success redirect
            # Prepare query parameters
        query_params = {
            "Page": "Userinfo",
            "EmpCode": EmployeeCode,   # or use actual EmpCode if different
            "EmpID": EmpID,
            "ID": apadp_id
        }
        
        # Build URL
        base_url = reverse('NewAPADP')  # replace with your view name for /PADP/NewAPADP/
        url = f"{base_url}?{urlencode(query_params)}"
        return redirect(url)

        # return redirect(f'/PADP/NewAPADP/?ID={apadp_id}&Page=PADPApprove')

    except ObjectDoesNotExist as e:
        return HttpResponse("Error: Required employee data not found.", status=404)

    except MultipleObjectsReturned as e:
        return HttpResponse("Error: Multiple employee records found. Please contact admin.", status=500)

    except Exception as e:
        return HttpResponse("An unexpected error occurred. Please contact support.", status=500)   



# def Get_HR_Manager_list(OrganizationID):
#     try:
#         matching_work = EmployeeWorkDetails.objects.filter(
#             EmpStatus__in=('Confirmed', 'On Probation', 'Not Confirmed'),
#             Department__in=('HR', 'Human Resources'),
#             OrganizationID=OrganizationID,
#             IsDelete=False,
#             IsSecondary=False
#         ).values_list('EmpID', flat=True)

#         if matching_work:
#             personal = EmployeePersonalDetails.objects.filter(EmpID=matching_work, IsDelete=False)
#             if personal:
#                 return [f"{p.FirstName} {p.LastName}" for p in personal]
#     except Exception as e:
#         print(f"Error in RD role name fetch: {e}")
#     return None

def Get_HR_Manager_list(OrganizationID):
    try:
        matching_work = EmployeeWorkDetails.objects.filter(
            EmpStatus__in=('Confirmed', 'On Probation', 'Not Confirmed'),
            Department__in=('HR', 'Human Resources'),
            OrganizationID=OrganizationID,
            IsDelete=False,
            IsSecondary=False
        ).values_list('EmpID', flat=True)

        if matching_work.exists():
            personal = EmployeePersonalDetails.objects.filter(EmpID__in=matching_work, IsDelete=False)
            if personal.exists():
                return [f"{p.FirstName} {p.LastName}" for p in personal]
    except Exception as e:
        print(f"Error in HR Manager role name fetch: {e}")
    return None

# def Get_DottedLine_Name_ByDesignation(DottedLineValue,OrganizationID):
#     try:
#         matching_work = EmployeeWorkDetails.objects.filter(
#             EmpStatus__in=('Confirmed', 'On Probation', 'Not Confirmed'),
#             Designation__iexact=DottedLineValue,
#             OrganizationID=OrganizationID,
#             IsDelete=False,
#             IsSecondary=False
#         ).values_list('EmpID', flat=True).first()

#         if matching_work:
#             personal = EmployeePersonalDetails.objects.filter(EmpID=matching_work).first()
#             if personal:
#                 return f"{personal.FirstName} {personal.LastName}"
#     except Exception as e:
#         print(f"Error in Dotted role name fetch: {e}")
#     return ''


def Get_DottedLine_Name_ByDesignation(dotted_line_value):
    try:
        # Get first matching work detail record
        work_detail = EmployeeWorkDetails.objects.filter(
            Designation__iexact=dotted_line_value,
            EmpStatus__in=('Confirmed', 'On Probation', 'Not Confirmed'),
            IsDelete=False,
            IsSecondary=False
        ).first()

        if not work_detail:
            return ''

        # Get personal details for the found employee
        personal = EmployeePersonalDetails.objects.filter(
            EmpID=work_detail.EmpID,
            # OrganizationID=work_detail.OrganizationID,
            IsDelete=False
        ).first()

        if personal:
            return f"{personal.FirstName} {personal.LastName}"
    except Exception as e:
        print(f"Error in Dotted role name fetch for Designation '{dotted_line_value}': {e}")

    return ''

from app.send_notification import *

from datetime import datetime
def NewAPADP(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
 
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    EmpCode = request.GET.get('EmpCode')
    EmpID = request.GET.get('EmpID') or None
    UserOID = request.GET.get('OID') or None
    
    if EmpID is None:
        if UserOID and EmpCode:
            Personalobj = EmployeePersonalDetails.objects.filter(
                IsDelete=False, IsEmployeeCreated=True, EmployeeCode = EmpCode, OrganizationID=UserOID
            ).first()

            if Personalobj:
                EmpID = Personalobj.EmpID

    UserType = request.session.get("UserType")
    UserType = str(UserType).lower()
    username = request.session.get("FullName")
    EmpCodedetails = EmployeeDetailsData(EmpID,OrganizationID)
    SessionEmployeeCode = str(request.session["EmployeeCode"])
    SessionDesignation = ''
    SessionDesignation  = get_employee_designation_by_EmployeeCode(OrganizationID,SessionEmployeeCode)

    Departmentsession = 'No'
    GetDepartmentsession = MultipleDepartmentofEmployee(OrganizationID, SessionEmployeeCode)

    department = request.session.get("Department_Name")
    department = str(department).lower()

    not_allowed = not (department == 'hr' or UserType == 'gm' or str(OrganizationID) == '3')

    if GetDepartmentsession:
        if 'Human Resources' in GetDepartmentsession :
            Departmentsession = 'hr'

    Page  = request.GET.get('Page')
    apadp_items = Master_APADP_Item.objects.filter(OrganizationID=0, IsDelete=False)
    apadp_subitems = Master_APADP_SubItem.objects.filter(Master_APADP_Item__OrganizationID=0, IsDelete=False)
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).values('designations').distinct().order_by('designations')
 
    apadp_id = request.GET.get('ID')
    existing_apadp = None
    existing_goals = []
    existing_performance_rating = None
    existing_details = []

    NewCTC = 0

    if EmpID is not None:
        ctc_salary_details = Salary_Detail_Master.objects.filter(
            Salary_title__Title='CTC (A+C)', IsDelete=False,
            OrganizationID=UserOID, EmpID=EmpID
        ).order_by('-id').first()

        if ctc_salary_details:
            NewCTC = ctc_salary_details.Permonth
        else:
            NewCTC=0
    else:
        NewCTC=0

 
    if apadp_id:
            DataFrom = "APADP"
            existing_apadp = APADP.objects.get(id=apadp_id)
            Existing_Entry_Log = None
            if existing_apadp:
                from_date =  convert_date_format(existing_apadp.review_from_date)
                to_date = convert_date_format(existing_apadp.review_to_date)
                existing_apadp.review_from_date = from_date
                existing_apadp.review_to_date = to_date

            existing_goals = DevelopmentGoalsApdpa.objects.filter(APADP=existing_apadp).values(
                'id', 'Goal', 'Timeline', 'Status', 'Remarks', 'GoalStartDate', 'GoalCompletionDate'
            )
            existing_performance_rating = FinalPerformancerating.objects.filter(APADP=existing_apadp).first()
            if OrganizationID == "3":
                existing_details = Master_APADP_SubItemDetail.objects.filter(APADP=existing_apadp,)
            else:    
                existing_details = Master_APADP_SubItemDetail.objects.filter(APADP=existing_apadp,)
    else: 
        DataFrom = "HR"       
        existing_apadp = {
            'EmployeeCode': EmpCodedetails.EmployeeCode,
            'EmpName': EmpCodedetails.full_name,
            'Designation': EmpCodedetails.Designation,
            'Department': EmpCodedetails.Department,
            'Level': EmpCodedetails.Level,
            'ReportingtoDesigantion': EmpCodedetails.ReportingtoDesignation,
            'ReportingtoDesigantionName': EmpCodedetails.ReportingtoDesignationName,
            'ReportingtoLevel': EmpCodedetails.ReportingtoLevel,
            'DateofJoining': EmpCodedetails.DateofJoining,
            'Tenure': EmpCodedetails.tenure_till_today,
            'review_from_date': EmpCodedetails.review_from_date,
            'review_to_date': EmpCodedetails.review_to_date,
            'Current_Salary':EmpCodedetails.CTC
        }

    existing_details_dict = {
        detail.Master_APADP_SubItem.id: detail.Performance
        for detail in existing_details
    }

    if request.method == "POST":
        EmployeeCode = request.POST.get('EmployeeCode') or ''
        EmpName = request.POST.get('EmpName') or ''
        Designation = request.POST.get('Designation') or ''
        Department = request.POST.get('Department') or ''
        Level = request.POST.get('Level') or ''
        ReportingtoDesigantion = request.POST.get('ReportingtoDesigantion') or ''
        ReportingtoLevel = request.POST.get('ReportingtoLevel') or ''
        DateofJoining = request.POST.get('DateofJoining') or ''
        Tenure = request.POST.get('Tenure') or ''
        review_from_date = request.POST.get('review_from_date')
        review_to_date = request.POST.get('review_to_date')
        Development = request.POST.get('Development') or ''
        Finalcomments = request.POST.get('Finalcomments') or ''
        ApporveBtn = request.POST.get('ApporveBtn') or ''
        HRManager = request.POST.get('HRManager') or ''
        ReportingToName = request.POST.get('ReportingToName') or ''
        CurrentSalary = request.POST.get('CurrentSalary') or 0
        
        if DataFrom == "APADP":
            padp = APADP_Master_Log.objects.create(
                APADP=existing_apadp,
                LastApporvalStatus = existing_apadp.LastApporvalStatus,
                hr_as = existing_apadp.hr_as,
                ar_as = existing_apadp.ar_as,
                hr_ar = existing_apadp.hr_ar,
                ceo_as = existing_apadp.ceo_as,
                ceo_as_remarks = existing_apadp.ceo_as_remarks,
                hr_actionOnDatetime = existing_apadp.hr_actionOnDatetime,
                ar_actionOnDatetime = existing_apadp.ar_actionOnDatetime,
                hr_ar_actionOnDatetime = existing_apadp.hr_ar_actionOnDatetime,
                ceo_actionOnDatetime = existing_apadp.ceo_actionOnDatetime,
                OrganizationID = existing_apadp.OrganizationID,
                CreatedBy = existing_apadp.CreatedBy,
            )

            existing_apadp.EmployeeCode = EmployeeCode
            existing_apadp.EmpName = EmpName
            existing_apadp.Designation = Designation
            existing_apadp.Department = Department
            existing_apadp.Level = Level
            existing_apadp.ReportingtoDesigantion = ReportingtoDesigantion
            existing_apadp.ReportingtoLevel = ReportingtoLevel
            existing_apadp.DateofJoining = DateofJoining
            existing_apadp.Tenure = Tenure
            existing_apadp.review_from_date = review_from_date
            existing_apadp.review_to_date = review_to_date
            existing_apadp.Development = Development
            existing_apadp.Finalcomments = Finalcomments
            existing_apadp.ModifyBy = UserID
            existing_apadp.Current_Salary = CurrentSalary
            padp=existing_apadp
            hops_id = str(padp.id) or 0

            if  padp.LastApporvalStatus == "Pending":
                if str(Departmentsession) == 'hr' and  padp.ar_as == "Submitted"  and ApporveBtn == '1':
                    padp.hr_ar = "Audited"  
                    padp.AuditedBy = SessionEmployeeCode
                    padp.AuditedBy_Name = username
                    padp.LastApporvalStatus = "Pending"  # new change
                    padp.hr_ar_actionOnDatetime = datetime.now()  
                    padp.ModifyDateTime = timezone.now()  

                    if hops_id != '0':
                        # CEO_Emp_Code = 001
                        Send_APDP_Audit_CEO_Notification(
                            organization_id='3',
                            EmpCode=['001'],
                            title="PADP Audit Completed by HR",
                            message=f"The PADP for {EmpName} has been successfully audited by HR and is now available for your review.",
                            module_name="PADP",
                            action="Audited",
                            hopsId=hops_id,
                            user_type="admin",
                            priority="high"
                        )
                    else:
                        print("Hops id is not found")
                        
 
                if SessionDesignation == padp.ReportingtoDesigantion and  ApporveBtn != '1':
                    padp.ar_as = "Submitted"  
                    padp.ar_actionOnDatetime = datetime.now()  
                    padp.ModifyDateTime = timezone.now()  

                if UserType == "ceo" and padp.ar_as == "Submitted" :
                    padp.ceo_as = "Approved"
                    padp.LastApporvalStatus = "Approved"  
                    padp.ceo_actionOnDatetime = datetime.now()
                    padp.ModifyDateTime = timezone.now()

            elif padp.LastApporvalStatus == "Returned":
                if str(Departmentsession) == 'hr':
                    padp.LastApporvalStatus = "Pending"  
                if str(Departmentsession) == 'hr' and  padp.ar_as == "Submitted"  and ApporveBtn == '1':
                    padp.hr_ar = "Audited"
                    padp.LastApporvalStatus = "Pending"  
                    padp.hr_ar_actionOnDatetime = datetime.now() # new change 
                    padp.ModifyDateTime = timezone.now()

                    if existing_apadp.ceo_as == "Returned":
                        existing_apadp.Last_CEO_Action = existing_apadp.ceo_as
                        existing_apadp.Last_CEO_action_On = existing_apadp.ceo_actionOnDatetime
                        existing_apadp.Last_CEO_action_Remarks = existing_apadp.ceo_as_remarks
                        existing_apadp.ceo_as = ""
                        existing_apadp.ceo_as_remarks = ""
                        existing_apadp.ceo_actionOnDatetime = None
                        padp.LastApporvalStatus = "Pending"  
                    else:
                        print("The CEO status is Not updated ::: ERROR::")
                
            existing_apadp.save()                        
        else:
            padp = APADP.objects.create(
                EmployeeCode=EmployeeCode,
                EmpName=EmpName,
                Designation=Designation,
                Department=Department,
                Level=Level,
                ReportingtoDesigantion=ReportingtoDesigantion,
                ReportingtoLevel=ReportingtoLevel,
                DateofJoining=DateofJoining,
                Tenure=Tenure,
                review_from_date=review_from_date,
                review_to_date=review_to_date,
                Finalcomments=Finalcomments,
                Development=Development,
                OrganizationID=OrganizationID,
                CreatedBy=UserID,
                CreatedByUsername=username,
                AuditedBy=UserID,
                AuditedBy_Name=username,
                hr_as = "Submitted",
                hr_actionOnDatetime = timezone.now(),
                HR_Manager=HRManager,
                Reporting_To_Name = ReportingToName,
                Current_Salary = CurrentSalary
            )
            hops_id = str(padp.id) or 0

            Send_Live_Notification(
                organization_id=OrganizationID,
                EmpCode=EmployeeCode,
                title=f"New PADP is created",
                message=f"The PADP for {EmpName} has been successfully audited by HR and is now available for your review.",
                module_name="PADP",
                action="Created",
                hopsId=hops_id,
                user_type="admin",
                priority="high"
            )

            # Immediately log this action
            APADP_Master_Log.objects.create(
                APADP=padp,
                LastApporvalStatus=padp.LastApporvalStatus,
                hr_as=padp.hr_as,
                ar_as=padp.ar_as,
                ceo_as=padp.ceo_as,
                OrganizationID=padp.OrganizationID,
                CreatedBy=padp.CreatedBy,
                hr_actionOnDatetime=padp.hr_actionOnDatetime,
            )
 
        Goal = request.POST.getlist('Goal[]')
        Timeline = request.POST.getlist('Timeline[]')
        Status = request.POST.getlist('Status[]')
        Remarks = request.POST.getlist('Remarks[]')
        GoalStartDate = request.POST.getlist('GoalStartDate[]')
        GoalCompletionDate = request.POST.getlist('GoalCompletionDate[]')
 
        for goal, timeline, status, remarks, goal_start_date, goal_completion_date in zip(Goal, Timeline, Status, Remarks, GoalStartDate, GoalCompletionDate):
            DevelopmentGoalsApdpa.objects.update_or_create(
                APADP=padp,
                Goal=goal,
                defaults={
                    'Timeline': timeline,
                    'Status': status,
                    'Remarks': remarks,
                    'GoalStartDate': goal_start_date,
                    'GoalCompletionDate': goal_completion_date,
                    'OrganizationID': OrganizationID,
                    'CreatedBy': UserID
                }
            )
        

        from django.core.exceptions import ObjectDoesNotExist

        Perf_rating = request.POST.get('rating') or ''
        SalaryIncrementOption = request.POST.get('SalaryIncrementOption') or ''
        SalaryCorrectionFrom = request.POST.get('SalaryCorrectionFrom') or 0
        SalaryCorrectionTo = request.POST.get('SalaryCorrectionTo') or 0
        JustificationSalaryCorrection = request.POST.get('JustificationSalaryCorrection') or ''
        PromotionFrom = request.POST.get('PromotionFrom') or ''
        PromotionTo = request.POST.get('PromotionTo') or ''
        JustificationPromotion = request.POST.get('JustificationPromotion') or ''

        try:
            performance_rating = FinalPerformancerating.objects.get(APADP=padp)
            
            performance_rating.rating = Perf_rating
            performance_rating.SalaryIncrementOption = SalaryIncrementOption
            performance_rating.SalaryCorrectionFrom =SalaryCorrectionFrom
            performance_rating.SalaryCorrectionTo = SalaryCorrectionTo
            performance_rating.JustificationSalaryCorrection = JustificationSalaryCorrection
            performance_rating.PromotionFrom = PromotionFrom
            performance_rating.PromotionTo = PromotionTo
            performance_rating.JustificationPromotion = JustificationPromotion
            performance_rating.OrganizationID = OrganizationID
            performance_rating.CreatedBy = UserID

            performance_rating.save()

        except ObjectDoesNotExist:
            FinalPerformancerating.objects.create(
                APADP=padp,
                rating=Perf_rating,
                SalaryIncrementOption=SalaryIncrementOption,
                SalaryCorrectionFrom=SalaryCorrectionFrom,
                SalaryCorrectionTo=SalaryCorrectionTo,
                JustificationSalaryCorrection=JustificationSalaryCorrection,
                PromotionFrom=PromotionFrom,
                PromotionTo=PromotionTo,
                JustificationPromotion=JustificationPromotion,
                OrganizationID=OrganizationID,
                CreatedBy=UserID,
                CreatedByUsername=username,
            )

       
        for subitem in apadp_subitems:
            Performance = request.POST.get(f'Performance_{subitem.id}', '')
            Master_APADP_SubItemDetail.objects.update_or_create(
                Master_APADP_SubItem=subitem,
                APADP=padp,
                defaults={
                    'Performance': Performance,
                    'OrganizationID': OrganizationID,
                    'CreatedBy': UserID
                }
            )

        if Page == "PADPERDC":
            return redirect('PADPERDC')
        
        if Page == "PADPApprove":
            return redirect('PADPApprove')
        
        if Page == "Userinfo":    
           return redirect(f'/PADP/Userinfo?EmpCode={EmpCode}&EmpID={EmpID}')

    Get_HR_ManagerList = Get_HR_Manager_list(OrganizationID) or ''

    context = {
        'EmpCode': EmpCode,
        'SessionEmployeeCode':SessionEmployeeCode,
        'EmpCodedetails': EmpCodedetails,
        'apadp_items': apadp_items,
        'apadp_subitems': apadp_subitems,
        'Designations': Designations,
        'existing_apadp': existing_apadp,
        'existing_performance_rating': existing_performance_rating,
        'existing_goals': existing_goals,
        'existing_details': existing_details,
        'existing_details_dict': existing_details_dict,
        'Departmentsession':   Departmentsession,
        'apadp_id':apadp_id,
        'not_allowed':not_allowed,
        'Get_HR_ManagerList':Get_HR_ManagerList,
        'CTC': NewCTC if NewCTC else 0,
        'NewCTC': NewCTC,
        'EmpOrgID': UserOID,
        'EmpID': EmpID,
        'EmpCode': EmpCode,
        'Page':Page
    }
    return render(request, "PADPAPP/PADPNEW/NewAPADP.html", context)
 






#  -------------- Refresh data
from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode

from datetime import timedelta
from django.http import JsonResponse

def Refresh_Salary_Data_PADP(request, apadp_id):
    if not apadp_id:
        return JsonResponse({"error": "The PADP Is not found for this employee"}, status=404)
    
    print("We are here and the id is also there", apadp_id)

    APADP_obj = APADP.objects.get(id=apadp_id)
    EmpCode = APADP_obj.EmployeeCode
    OID = APADP_obj.OrganizationID

    EmpID = None
    if OID and EmpCode:
        Personalobj = EmployeePersonalDetails.objects.filter(
            IsDelete=False, IsEmployeeCreated=True,
            EmployeeCode=EmpCode, OrganizationID=OID
        ).first()
        if Personalobj:
            EmpID = Personalobj.EmpID

    Workobj = EmployeeWorkDetails.objects.filter(
        OrganizationID=OID, IsDelete=False, IsSecondary=False, EmpID=EmpID
    ).first()

    NewDesignation = ''
    NewCTC = 0
    if Workobj:
        NewDesignation = Workobj.Designation
        ctc_salary_details = Salary_Detail_Master.objects.filter(
            Salary_title__Title='CTC (A+C)', IsDelete=False,
            OrganizationID=OID, EmpID=EmpID
        ).order_by('-id').first()
        if ctc_salary_details:
            NewCTC = ctc_salary_details.Permonth

    # Save updates
    performance_rating = FinalPerformancerating.objects.get(APADP=apadp_id)
    performance_rating.SalaryCorrectionFrom = NewCTC
    performance_rating.PromotionFrom = NewDesignation
    performance_rating.save()

    return JsonResponse({
        "salary": NewCTC,
        "designation": NewDesignation,
    })



def Refresh_Salary_Data_Master(request, Padpid):
    if not Padpid:
        return JsonResponse({"error": "The PADP Is not found for this employee"}, status=404)
    
    print("We are here and the id is also there", Padpid)

    APADP_obj = Entry_Master.objects.get(id=Padpid)
    EmpCode = APADP_obj.EmployeeCode
    OID = APADP_obj.OrganizationID

    EmpID = None
    if OID and EmpCode:
        Personalobj = EmployeePersonalDetails.objects.filter(
            IsDelete=False, IsEmployeeCreated=True,
            EmployeeCode=EmpCode, OrganizationID=OID
        ).first()
        if Personalobj:
            EmpID = Personalobj.EmpID

    Workobj = EmployeeWorkDetails.objects.filter(
        OrganizationID=OID, IsDelete=False, IsSecondary=False, EmpID=EmpID
    ).first()

    NewDesignation = ''
    NewCTC = 0
    if Workobj:
        NewDesignation = Workobj.Designation
        ctc_salary_details = Salary_Detail_Master.objects.filter(
            Salary_title__Title='CTC (A+C)', IsDelete=False,
            OrganizationID=OID, EmpID=EmpID
        ).order_by('-id').first()
        if ctc_salary_details:
            NewCTC = ctc_salary_details.Permonth

    # Save updates
    # Sal_data = FINAL_PERFORMANCE_RATING.objects.filter(Entry_Master=Padpid,IsDelete =False).first()
    # print(f"performance_rating is here :: {Sal_data.FromSalary}")
    # performance_rating.SalaryCorrectionFrom = NewCTC
    # performance_rating.PromotionFrom = NewDesignation
    # performance_rating.save()

    return JsonResponse({
        "salary": NewCTC,
        "designation": NewDesignation,
    })


# from datetime import timedelta
# def Refresh_Salary_Data_Master(request, Padpid):
#     # print(f"the EmpCode is here:: {EmpCode}")
#     # print(f"the padp is here:: {Padpid}")
#     # print(f"the EmpID is here:: {EmpID}")
#     # print(f"the OrgID is here:: {OID}")

#     APADP_obj = Entry_Master.objects.get(id=Padpid)
#     # print(f"APADP is here::",APADP_obj.EmployeeCode)
#     # print(f"APADP is here::",APADP_obj.OrganizationID)
#     # print(f"EmployeeOrganizationID is here::",APADP_obj.EmployeeOrganizationID)
#     EmpCode = APADP_obj.EmployeeCode
#     OID = APADP_obj.EmployeeOrganizationID

#     # return HttpResponse("you reached here in master padp")

#     EmpID = None
#     if OID and EmpCode:
#         Personalobj = EmployeePersonalDetails.objects.filter(
#             IsDelete=False, IsEmployeeCreated=True, EmployeeCode = EmpCode, OrganizationID=OID
#         ).first()

#         if Personalobj:
#             EmpID = Personalobj.EmpID

#     Workobj = EmployeeWorkDetails.objects.filter(
#         OrganizationID=OID, IsDelete=False, IsSecondary=False, EmpID=EmpID
#     ).first()

#     NewDesignation = ''
#     NewCTC = 0

#     if Workobj:
#         ctc_salary_details = Salary_Detail_Master.objects.filter(
#             Salary_title__Title='CTC (A+C)',
#             IsDelete=False,
#             OrganizationID=OID,
#             EmpID=EmpID
#         ).order_by('-id').first()

#         NewDesignation = Workobj.Designation
#         print("your designation is here::=", NewDesignation)

#         if ctc_salary_details:
#             NewCTC = ctc_salary_details.Permonth
#             print("My Employee Salary details::", NewCTC)

#     if Padpid:
#         Sal_data = FINAL_PERFORMANCE_RATING.objects.filter(Entry_Master=Padpid,IsDelete =False).first()
#         print(f"performance_rating is here :: {Sal_data.FromSalary}")
#         Sal_data.FromSalary = NewCTC
#         Sal_data.FromPosition = NewDesignation
#         Sal_data.save()

    

#     # Prepare query parameters
#     query_params = {
#         "Page": "PADPERDC",
#         "EmpCode": EmpCode,   # or use actual EmpCode if different
#         "EmpID": EmpID,
#         "ID": Padpid,
#         "OID":OID
#     }
    
#     # Build URL
#     base_url = reverse('PADP_Add')  # replace with your view name for /PADP/NewAPADP/
#     url = f"{base_url}?{urlencode(query_params)}"
    
#     return redirect(url)


        



def apdpaDelete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    EmpCode = request.GET.get('EmpCode')
    EmpID = request.GET.get('EmpID')

    id = request.GET.get('ID')
    pda = APADP.objects.get(id=id)
    pda.IsDelete = True
    pda.ModifyBy = UserID
    pda.save()
    return redirect(f'/PADP/Userinfo?EmpCode={EmpCode}&EmpID={EmpID}')
 
   


    

    


from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from django.template.loader import get_template
from xhtml2pdf import pisa  

def generate_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


from datetime import datetime
from django.utils import timezone  
from app.models import OrganizationMaster


def ApadpPdf(request):
    # if 'OrganizationID' not in request.session:
    #     return redirect(MasterAttribute.Host)
    # else:
    #     print("Show Page Session")

    # # OrganizationID = request.session["OrganizationID"]
    # UserID = str(request.session["UserID"])
    emp_id = request.GET.get('ID')
    emp_data = get_object_or_404(APADP, id=emp_id)
    
    OrganizationID = emp_data.OrganizationID
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

    apadp_items = Master_APADP_Item.objects.filter(OrganizationID=0, IsDelete=False)
    apadp_subitems = Master_APADP_SubItem.objects.filter(
        Master_APADP_Item__OrganizationID=0, IsDelete=False
    )
    
   
    existing_details = Master_APADP_SubItemDetail.objects.filter(OrganizationID=OrganizationID)
    existing_goals = DevelopmentGoalsApdpa.objects.filter(APADP=emp_data).values(
                'id', 'Goal', 'Timeline', 'Status', 'Remarks', 'GoalStartDate', 'GoalCompletionDate'
            )
    existing_performance_rating = FinalPerformancerating.objects.filter(APADP=emp_data).first()
    status_mapping = {}
     
    if OrganizationID == "3":
                existing_details = Master_APADP_SubItemDetail.objects.filter(APADP=emp_data)
               
    else:    
                existing_details = Master_APADP_SubItemDetail.objects.filter(APADP=emp_data)
 
           
    for detail in existing_details:
        status_mapping[detail.Master_APADP_SubItem.id] = detail.Performance or None


    context = {
        'emp_data': emp_data,
        'organization_logos':organization_logos,
        'organization_logo':organization_logo,
        'current_datetime':current_datetime,
        'apadp_items':apadp_items,
        'apadp_subitems':apadp_subitems,
        'existing_details':existing_details,
        'status_mapping':status_mapping,
        'existing_goals':existing_goals,
        'existing_performance_rating':existing_performance_rating

    }
    return generate_pdf( 'PADPAPP/PADPNEW/ApadpPdf.html',context)
   
   



def PublicApadpPdf(request):
   
    # OrganizationID = request.session["OrganizationID"]
    
    emp_id = request.GET.get('ID')
    emp_data = get_object_or_404(APADP, id=emp_id)
    
    OrganizationID = emp_data.OrganizationID
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

    apadp_items = Master_APADP_Item.objects.filter(OrganizationID=0, IsDelete=False)
    apadp_subitems = Master_APADP_SubItem.objects.filter(
        Master_APADP_Item__OrganizationID=0, IsDelete=False
    )
    
   
    existing_details = Master_APADP_SubItemDetail.objects.filter(OrganizationID=OrganizationID)
    existing_goals = DevelopmentGoalsApdpa.objects.filter(APADP=emp_data).values(
                'id', 'Goal', 'Timeline', 'Status', 'Remarks', 'GoalStartDate', 'GoalCompletionDate'
            )
    existing_performance_rating = FinalPerformancerating.objects.filter(APADP=emp_data).first()
    status_mapping = {}
     
    if OrganizationID == "3":
                existing_details = Master_APADP_SubItemDetail.objects.filter(APADP=emp_data)
               
    else:    
                existing_details = Master_APADP_SubItemDetail.objects.filter(APADP=emp_data)
 
           
    for detail in existing_details:
        status_mapping[detail.Master_APADP_SubItem.id] = detail.Performance or None


    context = {
        'emp_data': emp_data,
        'organization_logos':organization_logos,
        'organization_logo':organization_logo,
        'current_datetime':current_datetime,
        'apadp_items':apadp_items,
        'apadp_subitems':apadp_subitems,
        'existing_details':existing_details,
        'status_mapping':status_mapping,
        'existing_goals':existing_goals,
        'existing_performance_rating':existing_performance_rating

    }
    return generate_pdf( 'PADPAPP/PADPNEW/ApadpPdf.html',context)
   

   
