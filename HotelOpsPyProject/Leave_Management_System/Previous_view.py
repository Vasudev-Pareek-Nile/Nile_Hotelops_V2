from django.shortcuts import render,redirect
import requests
from .models import CompOffApplication, Leave_Type_Master,Leave_Config_Details,Leave_Application,Leave_Process_Master,Leave_Process_Details,Emp_Leave_Balance_Master,EmpMonthLevelCreditMaster,EmpMonthLevelDebitMaster,National_Holidays,Optional_Holidays
from hotelopsmgmtpy.GlobalConfig import MasterAttribute, OrganizationDetail
from datetime import date,timedelta
from datetime import datetime
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db  import connection, transaction
import datetime
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from app.models import EmployeeMaster

def EmployeeDataSelect(OrganizationID=None, EmployeeCode=None,Designation =None,ReportingtoDesignation =None):
    with connection.cursor() as cursor:
        cursor.execute("EXEC SP_EmployeeMaster_For_Leave @OrganizationID=%s, @EmployeeCode=%s, @Designation=%s, @ReportingtoDesignation=%s", [OrganizationID, EmployeeCode,Designation,ReportingtoDesignation])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
    rowslist = [dict(zip(columns, row)) for row in rows]
    return rowslist




# def EmployeeDetails(request): 
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")
    
#     OrganizationID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])
#     EmployeeCode = '451000004' 
#     # request.session["EmployeeCode"] 
#     EmployeeDetails =  get_object_or_404(EmployeeMaster,EmployeeCode = EmployeeCode ,OrganizationID = OrganizationID ,IsDelete = False)
#     Desigantion  = EmployeeDetails.Designation or ''
#     Department = EmployeeDetails.Department or ''

#     EmployeeList  = EmployeeMaster.objects.filter(OrganizationID = OrganizationID,IsDelete = False,
#                                                     #  EmployeeCode = EmployeeCode
#                                                     # Department =  "Human Resources"
#                                                     ReportingtoDesigantion = Desigantion
#                                                       ) 
#     EmployeeList = list(EmployeeList.values())

#     return JsonResponse({"EmployeeList":EmployeeList},safe=False)

def  Employee_Dashboard(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    Emp_code=request.session["EmployeeCode"]
    leave_balance  =  Emp_Leave_Balance_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Emp_code=Emp_code)
    total = 0
    for leave in leave_balance:
        total = total + leave.Balance
    leave_requset_Pending = Leave_Application.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Emp_code=Emp_code,Status=0)
    leave_requset_Pending_count = len(leave_requset_Pending)
    leave_requset_rejected = Leave_Application.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Emp_code=Emp_code,Status=-1)
    leave_requset_rejected_count = len(leave_requset_rejected)
    leave_requset_appr = Leave_Application.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Emp_code=Emp_code,Status=1)
    leave_requset_appr_count = len(leave_requset_appr)
    # leave_type = leave_balance.Leave_Type_Master.Type
    

    context = {
        'total':total,
        'leave_requset_Pending_count':leave_requset_Pending_count,
        'leave_requset_rejected_count':leave_requset_rejected_count,
        'leave_requset_appr_count':leave_requset_appr_count,
        'leave_balance':leave_balance,
    }
    return render(request,"LMS/DASHBOARD/Employee_Dashboard.html",context)
    

from django.http import JsonResponse
from django.http import JsonResponse
from django.core.serializers import serialize

from datetime import datetime



def all_leaves(request):
    if 'OrganizationID' not in request.session:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    OrganizationID = request.session["OrganizationID"]
    Emp_code = request.session["EmployeeCode"]
    response_data = []

        # Fetch attendance
    attendance_data = Attendance_Data.objects.filter(
        IsDelete=False, OrganizationID=OrganizationID, EmployeeCode=Emp_code
    ).distinct()


    if attendance_data:
        print("attendance data ")
        for attendance in attendance_data:
            response_data.append({
                'title': attendance.Status,
                'in_time': attendance.In_Time,
                'out_time': attendance.Out_Time,
                's_in_time': attendance.S_In_Time,
                's_out_time': attendance.S_Out_Time,
                'duty_hours': attendance.Duty_Hour,
                'status': attendance.Status if attendance.Status else "",
                'type':'attend',
                'start': attendance.Date.strftime('%Y-%m-%d'),  
                'end': attendance.Date.strftime('%Y-%m-%d'),     
        })
                

        all_leaves = Leave_Application.objects.filter(IsDelete=False,OrganizationID=OrganizationID, Emp_code=Emp_code).distinct()
        if all_leaves.exists():
            for leave in all_leaves:
                leave_dict = {
                    'title': leave.Leave_Type_Master.Type,
                    'classes':'myclass',
                    'id': leave.id,
                    'status':leave.Status,
                    'start': leave.Start_Date.strftime('%Y-%m-%d'),  
                    'end': leave.End_Date.strftime('%Y-%m-%d'),      
                    'type':'leave',
                }
                response_data.append(leave_dict)

    return JsonResponse(response_data, safe=False)



def all_leavesDate(request):
    if 'OrganizationID' not in request.session:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    OrganizationID = request.session["OrganizationID"]
    Emp_code = request.session["EmployeeCode"]
    selected_date = request.GET.get('date', None)

    print("Selected data is here")
    print(selected_date)
    response_data = []

    if selected_date:
        try:
            selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        # Fetch attendance
        attendance_data = Attendance_Data.objects.filter(
            IsDelete=False, OrganizationID=OrganizationID, EmployeeCode=Emp_code, Date=selected_date_obj
        )


        if attendance_data:
            for attendance in attendance_data:
                response_data.append({
                    'title': attendance.Status,
                    'in_time': attendance.In_Time,
                    'out_time': attendance.Out_Time,
                    's_in_time': attendance.S_In_Time,
                    's_out_time': attendance.S_Out_Time,
                    'duty_hours': attendance.Duty_Hour,
                    'status': attendance.Status if attendance.Status else "",
                    'type':'attendance',
                    'start': attendance.Date.strftime('%Y-%m-%d'),  
                    'end': attendance.Date.strftime('%Y-%m-%d'),    
            })
                

        all_leaves = Leave_Application.objects.filter(IsDelete=False,OrganizationID=OrganizationID, Emp_code=Emp_code, Start_Date__lte =selected_date_obj, End_Date__gte =selected_date_obj)
        if all_leaves.exists():
        
        
            for leave in all_leaves:
                leave_dict = {
                    'title': leave.Leave_Type_Master.Type,
                    'classes':'myclass',
                    'id': leave.id,
                    'status':leave.Status,
                    'start': leave.Start_Date.strftime('%Y-%m-%d'),  
                    'end': leave.End_Date.strftime('%Y-%m-%d'),      
                    'type':'leave',
                    'Reason': leave.Reason,
                    'Total_credit': leave.Total_credit,
                    'ReportingtoDesigantion':leave.ReportingtoDesigantion,
                    'Remark':leave.Remark,
                    'ReportingtoDesigantion':leave.ReportingtoDesigantion,
                }
                response_data.append(leave_dict)

    return JsonResponse(response_data, safe=False)



def  CEO_Dashboard(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    Emp_code=request.session["EmployeeCode"]
    
    return render(request,"LMS/DASHBOARD/CEO_Dashboard.html")



def  CEO_Dashboard_Iframe(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    Emp_code=request.session["EmployeeCode"]
    
    return render(request,"LMS/DASHBOARD/CEO_Dashboard_Iframe.html")




def all_leaves_ceo(request):
    if 'OrganizationID' not in request.session:
      return redirect(MasterAttribute.Host)
    else:
      OrganizationID = request.session["OrganizationID"]
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
    UserType = request.session["UserType"]
    EmployeeCode=request.session["EmployeeCode"]
    
    # obj = get_object_or_404(EmployeeMaster,EmployeeCode=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False)

    # Desigantion = obj.Designation
    # obj = EmployeeDataSelect(OrganizationID,EmployeeCode)
    # Desigantion = obj[0]['Designation']       
    

    emp_list = EmployeeDataSelect(ReportingtoDesignation=UserType)
    
    all_leaves = Leave_Application.objects.filter(IsDelete=False,Status=1, ReportingtoDesigantion=UserType)
    leave_list = []

    for leave in all_leaves:
      for emp in emp_list:    
        if emp['EmployeeCode'] == leave.Emp_code:
            name= emp['EmpName']
            fullname = emp['EmpName']
            leave_dict = {
                'title': leave.Leave_Type_Master.Type + ' '+ name,
               
                 'classes':'myclass',

               'type':leave.Leave_Type_Master.Type,
                'fullname': fullname,
                'id': leave.id,
                  'status':leave.Status,
                
                'start': leave.Start_Date.strftime('%Y-%m-%d'),  
                'end':  leave.End_Date.strftime('%Y-%m-%d 23:00'),      
            }
            leave_list.append(leave_dict)
   

   
    return JsonResponse(leave_list, safe=False)




def all_leaves_hr(request):
    if 'OrganizationID' not in request.session:
      return redirect(MasterAttribute.Host)
    else:
      OrganizationID = request.session["OrganizationID"]
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    UserType = request.session["UserType"]
    Department_Name=request.session['Department_Name']
    Emp_code=request.session["EmployeeCode"]



    emp_list = EmployeeDataSelect(OrganizationID)
    
    all_leaves = Leave_Application.objects.filter(IsDelete=False,OrganizationID=OrganizationID)
    leave_list = []

    for leave in all_leaves:
      for emp in emp_list:    
        if emp['EmployeeCode'] == leave.Emp_code:
            name= emp['EmpName']
            fullname = emp['EmpName']
            leave_dict = {
                'title': leave.Leave_Type_Master.Type + ' ' +name,
                 'classes':'myclass',

               'type':leave.Leave_Type_Master.Type,
                'fullname': fullname,
                'id': leave.id,
                  'status':leave.Status,
                'start': leave.Start_Date.strftime('%Y-%m-%d'),  
                'end': leave.End_Date.strftime('%Y-%m-%d 23:00'),      
            }
            leave_list.append(leave_dict)
   
    return JsonResponse(leave_list, safe=False)






#  Hr Dashboard View
def  Hr_Dashboard(request):

    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
   
    Emp_code=request.session["EmployeeCode"]
    leave_requset_Pending = Leave_Application.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Status=0)
    leave_requset_Pending_count = len(leave_requset_Pending)
    
    leave_requset_appr = Leave_Application.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Status=1)
    leave_requset_appr_count = len(leave_requset_appr)
    context = {
        'leave_requset_Pending_count':leave_requset_Pending_count,
        'leave_requset_appr_count':leave_requset_appr_count,
    }

    return render(request,"LMS/DASHBOARD/Hr_Dashboard.html",context)



# start Check
 
# Leave Type Master List

def  Leave_Type_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    leave_type = Leave_Type_Master.objects.filter(IsDelete = False,Is_Active=True).order_by('id')
    context = {'leave_type':leave_type}

    return render(request,"LMS/LEAVE/Leave_Type_List.html",context)



# Leave Type Master
@transaction.atomic
def  Leave_Type_Add(request): 
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    type_id =  request.GET.get('ID')
    type = None 
    if type_id is not None:
        type  = get_object_or_404(Leave_Type_Master, id=type_id, IsDelete=False,Is_Active=True)
    with transaction.atomic():
        if request.method == "POST":
            if type_id is not None:
                Type = request.POST['Type']
                FullName = request.POST['FullName']
                Description  = request.POST['Description']
                
                Is_active = request.POST.get('status', '')
                Is_active = True if Is_active == 'on' else False
                type.Is_Active = Is_active
                
                type.Type= Type
                type.FullName = FullName
                type.Description =Description 
                type.ModifyBy = UserID
                
                type.save()
                messages.success(request,"Leave Type Updated Succesfully")
            else:    
                Type = request.POST['Type']
                FullName = request.POST['FullName']
                Description  = request.POST['Description']
                Is_active = request.POST.get('status', '')
                Is_active = True if Is_active == 'on' else False
             

                type = Leave_Type_Master.objects.create(OrganizationID=OrganizationID,CreatedBy = UserID,Type = Type,FullName= FullName,Description = Description,Is_Active = Is_active)
                messages.success(request,"Leave Type Added Succesfully")
            return redirect('Leave_Type_List')
    context = {'type':type}
    return render(request,"LMS/LEAVE/Leave_Type_Add.html",context)

# Leave Type  Delete
@transaction.atomic
def Leave_Type_Delete(request,id):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")

     OrganizationID = request.session["OrganizationID"]
     UserID = str(request.session["UserID"])
     with transaction.atomic():
        type = Leave_Type_Master.objects.get(id = id)
        type.IsDelete =True
        type.ModifyBy =  UserID
        type.save()
        messages.warning(request,"Leave Type Deleted Succesfully")
        return redirect('Leave_Type_List') 
    
    
# Leave Config List
def Leave_Config_List(request,id):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    configs = Leave_Config_Details.objects.filter(Leave_Type_Master=id, IsDelete=False)
    context = {'configs': configs,'type_id':id}

    return render(request,"LMS/LEAVE/Leave_Config_List.html",context)
from decimal import Decimal

# Leave Config Details
@transaction.atomic
def  Leave_Config_Add(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
   
    type_id = request.GET.get('T_ID')
   
    try:
        type = Leave_Type_Master.objects.get(id=type_id,IsDelete=False,Is_Active=True)
    except:
        type = None
    config_id = request.GET.get('ID')
    config =  None
    if config_id is not None:
        config =get_object_or_404(Leave_Config_Details,id=config_id,IsDelete=False)
    with transaction.atomic():
        if request.method == "POST":
            if config_id is not None:
                Leave_type = request.POST['Leave_type']
            
                Monitor_Balance = request.POST.get('MBalance', '')
                Monitor_Balance = True if Monitor_Balance == 'on' else False
                Carry_FWD = request.POST.get('CFWD', '')
                Carry_FWD = True if Carry_FWD == 'on' else False
                
                Encash = request.POST.get('Ecash', '')
                Encash = True if Encash == 'on' else False

                IsMonthly = request.POST.get('Monthly', '')
                IsMonthly = True if IsMonthly == 'on' else False

                IsDate = request.POST.get('IsDate', '')
                IsDate = True if IsDate == 'on' else False 

                IsConfirmed = request.POST.get('Confirmed', '')
                IsConfirmed = True if IsConfirmed == 'on' else False


                IsAutoCredit = request.POST.get('IsAutoCredit', '')
                IsAutoCredit = True if IsAutoCredit == 'on' else False

                Financial_Year_Start_Date =  request.POST['FSD']
                Financial_Year_End_Date =  request.POST['FED']
                YLeave =  request.POST['YLeave']
              
                Appn_Times =  request.POST['ATimes']
                Apply_Max =  request.POST['AMax']
                Apply_Min =  request.POST['AMin']
                # Overdaft =  request.POST['Odaft']
                Maximum_Accumulation=  request.POST['Max_Accum']
                Leave_id = Leave_Type_Master.objects.get(id=Leave_type,IsDelete=False,Is_Active=True)
                
                config.Leave_Type_Master = Leave_id
                config.Monitor_Balance =  Monitor_Balance
                config.Carry_FWD =   Carry_FWD
                config.Encash = Encash
                config.IsMonthly = IsMonthly
                config.IsDate = IsDate
                config.IsAutoCredit = IsAutoCredit

                config.Financial_Year_Start_Date = Financial_Year_Start_Date
                config.Financial_Year_End_Date =Financial_Year_End_Date 
                config.Appn_Times = Decimal(Appn_Times)
                config.Apply_Max = Decimal(Apply_Max)
                config.Apply_Min = Decimal(Apply_Min)
                # config.Overdaft = Decimal(Overdaft)
                config.Maximum_Accumulation = Decimal(Maximum_Accumulation)
                config.YearlyLeave = Decimal(YLeave)
              
                config.IsConfirmed = IsConfirmed
                config.OrganizationID =OrganizationID
                config.ModifyBy = UserID
                config.save()
                messages.success(request,"Leave Config Updated Succesfully")
                

            else:
            
                Leave_type = request.POST['Leave_type']
                
            
                Monitor_Balance = request.POST.get('MBalance', '')
                Monitor_Balance = True if Monitor_Balance == 'on' else False
                Carry_FWD = request.POST.get('CFWD', '')
                
                Carry_FWD = True if Carry_FWD == 'on' else False
                
                Encash = request.POST.get('Ecash', '')
                Encash = True if Encash == 'on' else False
                
                IsMonthly = request.POST.get('Monthly', '')
                IsMonthly = True if IsMonthly == 'on' else False
                
                IsConfirmed = request.POST.get('Confirmed', '')
                IsConfirmed = True if IsConfirmed == 'on' else False

                IsDate = request.POST.get('IsDate', '')
                IsDate = True if IsDate == 'on' else False
                
                
                
                IsAutoCredit = request.POST.get('IsAutoCredit', '')
                IsAutoCredit = True if IsAutoCredit == 'on' else False
                

                


                Financial_Year_Start_Date =  request.POST['FSD']
                Financial_Year_End_Date =  request.POST['FED']
                YLeave =  request.POST['YLeave']
               
                Appn_Times =  request.POST['ATimes']
                Apply_Max =  request.POST['AMax']
                Apply_Min =  request.POST['AMin']
                # Overdaft =  request.POST['Odaft']
                Maximum_Accumulation=  request.POST['Max_Accum']

                Leave_id = Leave_Type_Master.objects.get(id=Leave_type,IsDelete=False,Is_Active=True)
                config = Leave_Config_Details.objects.create(
                Leave_Type_Master = Leave_id ,
    
                Monitor_Balance =  Monitor_Balance,
                Carry_FWD = Carry_FWD,
                Encash = Encash,
                
                Financial_Year_Start_Date = Financial_Year_Start_Date,
                Financial_Year_End_Date = Financial_Year_End_Date,
                
                YearlyLeave = YLeave,
               

                Appn_Times =Appn_Times,
                Apply_Max = Apply_Max,
                Apply_Min = Apply_Min,
                
                # Overdaft =Overdaft,
                Maximum_Accumulation =Maximum_Accumulation,
                IsMonthly = IsMonthly,
                IsDate = IsDate, 
                IsConfirmed =  IsConfirmed,
                IsAutoCredit = IsAutoCredit,

                OrganizationID = OrganizationID,
                CreatedBy = UserID,
              
                )
                messages.success(request,"Leave Config Added Succesfully")


            return redirect("/Leave_Management_System/Leave_Config_List/ID="+Leave_type)    

    current_year = datetime.now().year
    DefaultFinancial_Year_Start_Date = datetime(current_year, 1, 1)
    DefaultFinancial_Year_End_Date = datetime(current_year, 12, 31)
    context = {'config':config,
                'type':type ,
                'DefaultFinancial_Year_Start_Date' :DefaultFinancial_Year_Start_Date, 
                'DefaultFinancial_Year_End_Date' : DefaultFinancial_Year_End_Date 
               }
    return render(request,"LMS/LEAVE/Leave_Config_Add.html",context)


# Leave Config Delete
@transaction.atomic
def  Leave_Config_Delete(request,id):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")

     OrganizationID = request.session["OrganizationID"]
     UserID = str(request.session["UserID"])
     with transaction.atomic():
        config = Leave_Config_Details.objects.get(id = id)
        Leave_type=config.Leave_Type_Master.id
        config.IsDelete =True
        config.ModifyBy =  UserID
        config.save()
        messages.warning(request,"Leave Config Deleted Succesfully")
        return redirect("/Leave_Management_System/Leave_Config_List/ID="+str(Leave_type))    
    

# Leave Proccess Master 
@transaction.atomic     
def Leave_Process(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    emp_list = EmployeeDataSelect(OrganizationID)
    
    with transaction.atomic():
        if request.method == "POST":
            leave_type_id = request.POST['type']
            credit = request.POST['credit']
                

            leave_type = Leave_Type_Master.objects.get(id=leave_type_id,IsDelete=False,Is_Active = True)
            process = Leave_Process_Master.objects.create(OrganizationID=OrganizationID,Leave_Type_Master=leave_type, Credit=credit, Status=False)
            all_emp_codes = request.POST.getlist('all_emp_codes[]')
        

            for empcode in all_emp_codes:
            
            
                if empcode is not None and empcode != '':
                    Emp_code =   empcode 
                    data = Leave_Process_Details.objects.create(OrganizationID=OrganizationID,Leave_Process_Master=process, Emp_code=Emp_code)
            messages.success(request,"Leave Assigned Succesfully")
            return redirect('LeaveProcessDetails')
        
    
    leave_type_list = Leave_Type_Master.objects.filter(IsDelete=False, Is_Active=True)
    leave_type_list = Leave_Type_Master.objects.filter(IsDelete=False, Is_Active=True)

    context = {'Leave_Type': leave_type_list, 'Emp_list': emp_list}
    return render(request, "LMS/LEAVEPROCESS/Leave_Process_Master.html", context)
    
from django.db.models import Prefetch
# Leave Process Details
@transaction.atomic     
def LeaveProcessDetails(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    ID = request.GET.get('ID')
    with transaction.atomic():
        if ID is not None:
            Leave_Process = Leave_Process_Master.objects.get(id=ID, OrganizationID=OrganizationID, IsDelete=False)
            Leave_Details = Leave_Process_Details.objects.filter(OrganizationID=OrganizationID, IsDelete=False,
                                                                Leave_Process_Master=Leave_Process.id)
            for detail in Leave_Details:
                L_id = detail.Leave_Process_Master
                balance = detail.Leave_Process_Master.Credit
                Emp_code = detail.Emp_code
                try:
                    previous_balance=0
                    
                    Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=L_id.Leave_Type_Master,
                                                                    Emp_code=Emp_code,OrganizationID=OrganizationID,IsDelete=False)
                    if Leave_Balance.exists():
                        Leave_Balance=Leave_Balance.first()
                        previous_balance = Leave_Balance.Balance
                        total = previous_balance + balance
                        Leave_Balance.Balance = total
                        Leave_Balance.save()
                        
                    else:
                        if Emp_code is not None and Emp_code != '':  
                            Leave_Balance = Emp_Leave_Balance_Master.objects.create(OrganizationID=OrganizationID,
                                Leave_Type_Master=L_id.Leave_Type_Master, Emp_code=Emp_code, Balance=balance)
                            Leave_Credit = EmpMonthLevelCreditMaster.objects.create(Leave_Type_Master=L_id.Leave_Type_Master,OrganizationID=OrganizationID,
                                                                    Emp_code=Emp_code, credit=balance)
                    # except:
                    #          if Emp_code is not None and Emp_code != '':  
                    #             Leave_Balance = Emp_Leave_Balance_Master.objects.create(OrganizationID=OrganizationID,
                    #                 Leave_Type_Master=L_id.Leave_Type_Master, Emp_code=Emp_code, Balance=balance)
                    #             Leave_Credit = EmpMonthLevelCreditMaster.objects.create(Leave_Type_Master=L_id.Leave_Type_Master,OrganizationID=OrganizationID,
                    #                                                     Emp_code=Emp_code, credit=balance)
                except: #Emp_Leave_Balance_Master.DoesNotExist:
                        if Emp_code is not None and Emp_code != '':  
                            Leave_Balance = Emp_Leave_Balance_Master.objects.create(OrganizationID=OrganizationID,
                                Leave_Type_Master=L_id.Leave_Type_Master, Emp_code=Emp_code, Balance=balance)
                Leave_Credit = EmpMonthLevelCreditMaster.objects.create(Leave_Type_Master=L_id.Leave_Type_Master,OrganizationID=OrganizationID,
                                                                    Emp_code=Emp_code, credit=balance)


            Leave_Process.Status = True
            Leave_Process.save()

    details = Leave_Process_Master.objects.filter(OrganizationID=OrganizationID, IsDelete=False, Status=False)
    for m in details:
        m.leave_process_details= Leave_Process_Details.objects.filter(Leave_Process_Master=m)
    # Prefetch related Leave_Process_Details for each Leave_Process_Master to avoid additional queries in the template
    
    # details = details.prefetch_related(Prefetch('leave_process_details', queryset=leave_process_details_prefetch))

    context = {'details': details}
    return render(request, "LMS/LEAVEPROCESS/LeaveProcessDetails.html", context)



import json

@transaction.atomic 
def  Leave_Application_view(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    UserType = str(request.session["UserType"])
    EmployeeCode=request.session["EmployeeCode"]
    if 'Page' in request.GET:
            Page = request.GET.get('Page')
            if Page == 'EmployeeApply':
                EmployeeCode  = request.GET.get('EmployeeCode')
   
    if UserType !="CEO":
        if EmployeeCode is not None and EmployeeCode != '':
           

            Leave_Balance = Emp_Leave_Balance_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Emp_code=EmployeeCode).order_by('Leave_Type_Master_id') 
            Leave_Types = Leave_Type_Master.objects.filter(IsDelete=False,Is_Active=True).order_by('id')
            # obj = EmployeeMaster.objects.get(EmployeeCode=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False)
            obj = EmployeeDataSelect(OrganizationID,EmployeeCode)

            if obj:
                pass
            else:
               
               
                    messages.warning(request,"Contact to hr department no  Employee Details found")
                    return render(request,"LMS/LEAVEAPPLICATION/Error.html")

            ReportingtoDesigantion = obj[0]['ReportingtoDesigantion']
            EmployeeName  = obj[0]['EmpName']
            
            leave_id =  request.GET.get('ID')
            leave =  None   
            if leave_id is not None:
                
                leave = get_object_or_404(Leave_Application, id=leave_id,OrganizationID=OrganizationID, IsDelete=False)   
            with transaction.atomic():
                if request.method =="POST":
                    if leave_id is not None:
                            
                                leave_type_id = request.POST['leave_type']
                                
                                    
                                        
                                leave_type = Leave_Type_Master.objects.get(id=leave_type_id,IsDelete=False,Is_Active=True)
                                Start_Date = request.POST['FromDate']
                                
                                End_Date = request.POST['ToDate']
                                Reason =  request.POST['Reason']
                                LeaveCredit =  Decimal(request.POST['LeaveCredit'])  
                                FromHalf = int(request.POST.get('FromHalf', 0))
                                ToHalf = int(request.POST.get('ToHalf', 0))
                            
                                From_1st_Half = False
                                From_2nd_Half = False

                                To_1st_Half = False 
                                To_2nd_Half = False
                                if FromHalf == 0:
                                    From_1st_Half =  True
                                else:
                                    From_2nd_Half = True

                                if ToHalf == 0:
                                    To_1st_Half =  True
                                else:
                                    To_2nd_Half = True
                                

                               
                                
                                
                                    
                                    
                                PreviousLeaveType = leave.Leave_Type_Master
                                PreviousLeaveDebit = leave.Total_credit
                                Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=PreviousLeaveType,
                                                                                Emp_code=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False).first()
                
                
                                Leave_debit = EmpMonthLevelDebitMaster.objects.filter(Leave_Type_Master=PreviousLeaveType,OrganizationID=OrganizationID,
                                                                            Emp_code=EmployeeCode,debit=PreviousLeaveDebit).order_by('-CreatedDateTime').first()
                
                
                                if Leave_debit :
                                    Balance = Leave_Balance.Balance 
                                    Leave_Balance.Balance  = Balance + Leave_debit.debit
                                    Leave_Balance.save()

                                
                                Info =  CombinedLeaveInfo(UserID=UserID, OrganizationID=OrganizationID, LeaveID=leave_type_id, EmployeeCode=EmployeeCode, SelectedLeaveType=leave_type.Type, LeaveCredit=LeaveCredit, Start_Date=Start_Date,End_Date = End_Date)

                            
                                if isinstance(Info, list):
                                
                                
                                   
                                    context = {'messages': Info, 'Leave_Types': Leave_Types}
                                    return render(request, "LMS/LEAVEAPPLICATION/Leave_Application.html", context)
                                
                                leave.Leave_Type_Master= leave_type
                                leave.Start_Date =Start_Date 
                                leave.From_1st_Half = From_1st_Half
                                leave.From_2nd_Half=From_2nd_Half
                                leave.End_Date=End_Date
                                leave.To_1st_Half = To_1st_Half
                                leave.To_2nd_Half=To_2nd_Half
                                leave.Reason=Reason
                                leave.Total_credit = LeaveCredit
                                leave.Emp_code=EmployeeCode
                                leave.ReportingtoDesigantion=ReportingtoDesigantion
                                leave.ModifyBy = UserID
                                leave.save()

                                Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=leave_type,
                                                Emp_code=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False).first()
                
                                Balance=Leave_Balance.Balance 
                                Leave_Balance.Balance  = Balance - Decimal(LeaveCredit)
                                Leave_Balance.save()

                                


                                Leave_debit = EmpMonthLevelDebitMaster.objects.create(Leave_Type_Master=leave_type,OrganizationID=OrganizationID,
                                                                            Emp_code=EmployeeCode, debit=LeaveCredit)
                                messages.success(request,"Updated Successfully")  


                        
                    else:
                                


                        
                                leave_type_id = request.POST['leave_type']
                            
                                    

                                leave_type = Leave_Type_Master.objects.get(id=leave_type_id,IsDelete=False,Is_Active=True)
                                Start_Date = request.POST['FromDate']
                                
                                End_Date = request.POST['ToDate']
                                Reason =  request.POST['Reason']
                                LeaveCredit = Decimal(request.POST['LeaveCredit'])  

                                FromHalf = int(request.POST.get('FromHalf', 0))
                                ToHalf = int(request.POST.get('ToHalf', 0))
                            
                                From_1st_Half = False
                                From_2nd_Half = False

                                To_1st_Half = False 
                                To_2nd_Half = False
                                if FromHalf == 0:
                                    From_1st_Half =  True
                                else:
                                    From_2nd_Half = True

                                if ToHalf == 0:
                                    To_1st_Half =  True
                                else:
                                    To_2nd_Half = True
                                
                             




                                Info =  CombinedLeaveInfo(UserID=UserID, OrganizationID=OrganizationID, LeaveID=leave_type_id, EmployeeCode=EmployeeCode, SelectedLeaveType=leave_type.Type, LeaveCredit=LeaveCredit, Start_Date=Start_Date,End_Date = End_Date)
                              
                                if isinstance(Info, list):
                                
                                
                                    context = {'messages': Info, 'Leave_Types': Leave_Types}
                                
                                
                                    
                                    return render(request, "LMS/LEAVEAPPLICATION/Leave_Application.html", context)

                            

                                application = Leave_Application.objects.create(OrganizationID=OrganizationID,Status=0,CreatedBy=UserID,
                                                                        
                                                                            Leave_Type_Master= leave_type,
                                                                            Start_Date =Start_Date ,From_1st_Half = From_1st_Half,
                                                                            From_2nd_Half=From_2nd_Half,
                                                                            End_Date=End_Date,
                                                                            To_1st_Half = To_1st_Half,
                                                                            To_2nd_Half=To_2nd_Half,
                                                                            Reason=Reason,
                                                                            Total_credit = LeaveCredit,
                                                                            Emp_code=EmployeeCode,
                                                                            ReportingtoDesigantion=ReportingtoDesigantion,

                                                                            )
                                Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=leave_type,
                                                Emp_code=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False).first()
                
                                Balance=Leave_Balance.Balance 
                                Leave_Balance.Balance  = Balance - Decimal(LeaveCredit)
                                Leave_Balance.save()

                                


                                Leave_debit = EmpMonthLevelDebitMaster.objects.create(Leave_Type_Master=leave_type,OrganizationID=OrganizationID,
                                                                            Emp_code=EmployeeCode, debit=LeaveCredit)
                                



                                messages.success(request,"Applied Successfully")
                    if 'Page' in request.GET:
                        Page = request.GET.get('Page')
                        if Page == 'EmployeeApply':
                            return redirect('Employee_Leave_Status')

                    else:            
                        return redirect('Leave_Status')



                    
                    

            prv_app = Leave_Application.objects.filter(OrganizationID=OrganizationID, IsDelete=False, Emp_code=EmployeeCode).first()





            context={'Leave_Balance':Leave_Balance,'Leave_Types':Leave_Types,'prv_app':prv_app,'leave':leave,'UserID':UserID,'EmployeeCode':EmployeeCode,'EmployeeName':EmployeeName}
            return render(request,"LMS/LEAVEAPPLICATION/Leave_Application.html",context)
    
    
    
        else:
           

            messages.warning(request,"Contact to hr department no  Employee Details found")
            return render(request,"LMS/LEAVEAPPLICATION/Error.html")

    else:
         

            messages.warning(request,"Contact to hr department no  Employee Details found")
            return render(request,"LMS/LEAVEAPPLICATION/Error.html")






@transaction.atomic 
def  Employee_Leave_Application_view(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    UserType = str(request.session["UserType"])

    EmployeeCode=request.session["EmployeeCode"]
   
    if UserType !="CEO":
        if EmployeeCode is not None and EmployeeCode != '':
           

            Leave_Balance = Emp_Leave_Balance_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Emp_code=EmployeeCode).order_by('Leave_Type_Master_id') 
            Leave_Types = Leave_Type_Master.objects.filter(IsDelete=False,Is_Active=True).order_by('id')
            # obj = EmployeeMaster.objects.get(EmployeeCode=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False)
            obj = EmployeeDataSelect(OrganizationID,EmployeeCode)

            if obj:
                pass
            else:
               
               
                    messages.warning(request,"Contact to hr department no  Employee Details found")
                    return render(request,"LMS/LEAVEAPPLICATION/Error.html")

            ReportingtoDesigantion = obj[0]['ReportingtoDesigantion']
            
            leave_id =  request.GET.get('ID')
            leave =  None   
            if leave_id is not None:
                
                leave = get_object_or_404(Leave_Application, id=leave_id,OrganizationID=OrganizationID, IsDelete=False)   
            with transaction.atomic():
                if request.method =="POST":
                    if leave_id is not None:
                            
                                leave_type_id = request.POST['leave_type']
                                
                                    
                                        
                                leave_type = Leave_Type_Master.objects.get(id=leave_type_id,IsDelete=False,Is_Active=True)
                                Start_Date = request.POST['FromDate']
                                
                                End_Date = request.POST['ToDate']
                                Reason =  request.POST['Reason']
                                LeaveCredit =  Decimal(request.POST['LeaveCredit'])  
                                FromHalf = int(request.POST.get('FromHalf', 0))
                                ToHalf = int(request.POST.get('ToHalf', 0))
                            
                                From_1st_Half = False
                                From_2nd_Half = False

                                To_1st_Half = False 
                                To_2nd_Half = False
                                if FromHalf == 0:
                                    From_1st_Half =  True
                                else:
                                    From_2nd_Half = True

                                if ToHalf == 0:
                                    To_1st_Half =  True
                                else:
                                    To_2nd_Half = True
                                

                               
                                
                                
                                    
                                    
                                PreviousLeaveType = leave.Leave_Type_Master
                                PreviousLeaveDebit = leave.Total_credit
                                Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=PreviousLeaveType,
                                                                                Emp_code=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False).first()
                
                
                                Leave_debit = EmpMonthLevelDebitMaster.objects.filter(Leave_Type_Master=PreviousLeaveType,OrganizationID=OrganizationID,
                                                                            Emp_code=EmployeeCode,debit=PreviousLeaveDebit).order_by('-CreatedDateTime').first()
                
                
                                if Leave_debit :
                                    Balance = Leave_Balance.Balance 
                                    Leave_Balance.Balance  = Balance + Leave_debit.debit
                                    Leave_Balance.save()

                                
                                Info =  CombinedLeaveInfo(UserID=UserID, OrganizationID=OrganizationID, LeaveID=leave_type_id, EmployeeCode=EmployeeCode, SelectedLeaveType=leave_type.Type, LeaveCredit=LeaveCredit, Start_Date=Start_Date,End_Date = End_Date)

                            
                                if isinstance(Info, list):
                                
                                
                                   
                                    context = {'messages': Info, 'Leave_Types': Leave_Types}
                                    return render(request, "LMS/LEAVEAPPLICATION/Employee_Leave_Application_view.html", context)
                                
                                leave.Leave_Type_Master= leave_type
                                leave.Start_Date =Start_Date 
                                leave.From_1st_Half = From_1st_Half
                                leave.From_2nd_Half=From_2nd_Half
                                leave.End_Date=End_Date
                                leave.To_1st_Half = To_1st_Half
                                leave.To_2nd_Half=To_2nd_Half
                                leave.Reason=Reason
                                leave.Total_credit = LeaveCredit
                                leave.Emp_code=EmployeeCode
                                leave.ReportingtoDesigantion=ReportingtoDesigantion
                                leave.ModifyBy = UserID
                                leave.save()

                                Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=leave_type,
                                                Emp_code=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False).first()
                
                                Balance=Leave_Balance.Balance 
                                Leave_Balance.Balance  = Balance - Decimal(LeaveCredit)
                                Leave_Balance.save()

                                


                                Leave_debit = EmpMonthLevelDebitMaster.objects.create(Leave_Type_Master=leave_type,OrganizationID=OrganizationID,
                                                                            Emp_code=EmployeeCode, debit=LeaveCredit)
                                messages.success(request,"Updated Successfully")  


                        
                    else:
                                


                        
                                leave_type_id = request.POST['leave_type']
                            
                                    

                                leave_type = Leave_Type_Master.objects.get(id=leave_type_id,IsDelete=False,Is_Active=True)
                                Start_Date = request.POST['FromDate']
                                
                                End_Date = request.POST['ToDate']
                                Reason =  request.POST['Reason']
                                LeaveCredit = Decimal(request.POST['LeaveCredit'])  

                                FromHalf = int(request.POST.get('FromHalf', 0))
                                ToHalf = int(request.POST.get('ToHalf', 0))
                            
                                From_1st_Half = False
                                From_2nd_Half = False

                                To_1st_Half = False 
                                To_2nd_Half = False
                                if FromHalf == 0:
                                    From_1st_Half =  True
                                else:
                                    From_2nd_Half = True

                                if ToHalf == 0:
                                    To_1st_Half =  True
                                else:
                                    To_2nd_Half = True
                                
                             




                                Info =  CombinedLeaveInfo(UserID=UserID, OrganizationID=OrganizationID, LeaveID=leave_type_id, EmployeeCode=EmployeeCode, SelectedLeaveType=leave_type.Type, LeaveCredit=LeaveCredit, Start_Date=Start_Date,End_Date = End_Date)
                              
                                if isinstance(Info, list):
                                
                                
                                    context = {'messages': Info, 'Leave_Types': Leave_Types}
                                
                                
                                    
                                    return render(request, "LMS/LEAVEAPPLICATION/Employee_Leave_Application_view.html", context)

                            

                                application = Leave_Application.objects.create(OrganizationID=OrganizationID,Status=0,CreatedBy=UserID,
                                                                        
                                                                            Leave_Type_Master= leave_type,
                                                                            Start_Date =Start_Date ,From_1st_Half = From_1st_Half,
                                                                            From_2nd_Half=From_2nd_Half,
                                                                            End_Date=End_Date,
                                                                            To_1st_Half = To_1st_Half,
                                                                            To_2nd_Half=To_2nd_Half,
                                                                            Reason=Reason,
                                                                            Total_credit = LeaveCredit,
                                                                            Emp_code=EmployeeCode,
                                                                            ReportingtoDesigantion=ReportingtoDesigantion,

                                                                            )
                                Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=leave_type,
                                                Emp_code=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False).first()
                
                                Balance=Leave_Balance.Balance 
                                Leave_Balance.Balance  = Balance - Decimal(LeaveCredit)
                                Leave_Balance.save()

                                


                                Leave_debit = EmpMonthLevelDebitMaster.objects.create(Leave_Type_Master=leave_type,OrganizationID=OrganizationID,
                                                                            Emp_code=EmployeeCode, debit=LeaveCredit)
                                



                                messages.success(request,"Applied Successfully")
                    return redirect('Leave_Status')



                    
                    

            prv_app = Leave_Application.objects.filter(OrganizationID=OrganizationID, IsDelete=False, Emp_code=EmployeeCode).first()





            context={'Leave_Balance':Leave_Balance,'Leave_Types':Leave_Types,'prv_app':prv_app,'leave':leave,'UserID':UserID}
            return render(request,"LMS/LEAVEAPPLICATION/Employee_Leave_Application_view.html",context)
    
    
    
        else:
           

            messages.warning(request,"Contact to hr department no  Employee Details found")
            return render(request,"LMS/LEAVEAPPLICATION/Error.html")

    else:
         

            messages.warning(request,"Contact to hr department no  Employee Details found")
            return render(request,"LMS/LEAVEAPPLICATION/Error.html")




def  CompOffRequest_view(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    UserType = str(request.session["UserType"])
    EmployeeCode=request.session["EmployeeCode"]
    if 'Page' in request.GET:
            Page = request.GET.get('Page')
            if Page == 'EmployeeApply':
                EmployeeCode  = request.GET.get('EmployeeCode')
   
    if UserType !="CEO":
        if EmployeeCode is not None and EmployeeCode != '':
           
            obj = EmployeeDataSelect(OrganizationID,EmployeeCode)

            if obj:
                pass
            else:
               
               
                    messages.warning(request,"Contact to hr department no  Employee Details found")
                    return render(request,"LMS/LEAVEAPPLICATION/Error.html")

            ReportingtoDesigantion = obj[0]['ReportingtoDesigantion']
            EmployeeName  = obj[0]['EmpName']
            
            leave_id =  request.GET.get('ID')
            leave =  None   
            if leave_id is not None:
                
                leave = get_object_or_404(CompOffApplication, id=leave_id,OrganizationID=OrganizationID, IsDelete=False)   
            with transaction.atomic():
                if request.method =="POST":
                    if leave_id is not None:
                                messages.success(request,"Updated Successfully")  
                        
                    else:
                        
                                CompOff_Date = request.POST['CompOff_Date']
                                Reason = request.POST['Reason']
                                application = CompOffApplication.objects.create(OrganizationID=OrganizationID,Status="Pending",CreatedBy=UserID,
                                                                        
                                                                            CompOff_Date= CompOff_Date,
                                                                            
                                                                            Reason=Reason,
                                                                            Emp_Code=EmployeeCode,
                                                                            ReportingtoDesigantion=ReportingtoDesigantion,

                                                                            )


                                messages.success(request,"Applied Successfully")
                    if 'Page' in request.GET:
                        Page = request.GET.get('Page')
                        if Page == 'EmployeeApply':
                            return redirect('Employee_Leave_Status')

                    else:            
                        return redirect('Leave_Status')



                    
                    


            context={'leave':leave,'UserID':UserID,'EmployeeCode':EmployeeCode,'EmployeeName':EmployeeName}
            return render(request,"LMS/LEAVEAPPLICATION/CompOffRequest.html",context)
    
    
    
        else:
           

            messages.warning(request,"Contact to hr department no  Employee Details found")
            return render(request,"LMS/LEAVEAPPLICATION/Error.html")

    else:
         

            messages.warning(request,"Contact to hr department no  Employee Details found")
            return render(request,"LMS/LEAVEAPPLICATION/Error.html")




def CombinedLeaveInfo(UserID,OrganizationID,LeaveID,EmployeeCode ,SelectedLeaveType, LeaveCredit, Start_Date,End_Date):
    error_messages = []

    
    
    current_year = datetime.now().year
   
    LeaveID = LeaveID
    SelectedLeaveType = SelectedLeaveType
    LeaveCredit = LeaveCredit
    Date = Start_Date
    # print(LeaveID)
    OP = False

    try:
        objconfig = get_object_or_404(Leave_Config_Details, Leave_Type_Master_id=LeaveID, IsDelete=False, Financial_Year_Start_Date__year=current_year)
        
        LeaveCountObj = Leave_Application.objects.filter(
            Leave_Type_Master_id=LeaveID,
            Emp_code=EmployeeCode,
            Start_Date__year=current_year,
            IsDelete=False,
            Status = 1,
            OrganizationID=OrganizationID,
           
        )

        
        
        
        Apply_Max = objconfig.Apply_Max
        Apply_Min =  objconfig.Apply_Min
        IsConfirmed = objconfig.IsConfirmed 
        if IsConfirmed:
            # CofirmedStatusObj = get_object_or_404(EmployeeMaster, EmployeeCode=EmployeeCode, OrganizationID=OrganizationID, IsDelete=False)
            CofirmedStatusObj = EmployeeDataSelect(OrganizationID,EmployeeCode)
            CofirmedStatusObj = CofirmedStatusObj[0]['EmpStatus']
            # print(CofirmedStatusObj)
            if CofirmedStatusObj != 'Confirmed':
                            error_messages.append(f'Cannot apply for {SelectedLeaveType} you are not Confirmed')   
        
        Appn_Times =  objconfig.Appn_Times
        LeaveCount = LeaveCountObj.count() or 0
        
        if LeaveCount == Appn_Times:
            error_messages.append(f'You cannot apply for {SelectedLeaveType} more than {Appn_Times} times in a year')   


        
        if  LeaveCredit < Apply_Min:
            error_messages.append(f'You cannot apply  {SelectedLeaveType} less than {Apply_Min}')

        if  LeaveCredit > Apply_Max:
            error_messages.append(f'You cannot apply  {SelectedLeaveType} more than {Apply_Max}')    

            
        ContinueLeaveTypes = ['PL', 'CL']

        if SelectedLeaveType in ContinueLeaveTypes:
            ContinueLeaveTypes.remove(SelectedLeaveType)

            previous_application = Leave_Application.objects.filter(
                OrganizationID=OrganizationID,
                IsDelete=False,
                Emp_code=EmployeeCode,

            
            ).order_by('-End_Date').first()

            if previous_application:
                PreviousLeaveType = previous_application.Leave_Type_Master.Type
                PreviousEndDate = previous_application.End_Date

                if PreviousLeaveType in ContinueLeaveTypes:
                    Start_Date_date = datetime.strptime(Start_Date, '%Y-%m-%d').date()
                    difference_days = abs((PreviousEndDate - Start_Date_date).days)
                    if difference_days >= 1:
                        pass
                    else:
                        error_messages.append(f'You cannot apply for {SelectedLeaveType} if you previously applied for {PreviousLeaveType}')



        CheckBalance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master_id=LeaveID,
            Emp_code=EmployeeCode,
            IsDelete=False,
            OrganizationID=OrganizationID).first()
        Balance = CheckBalance.Balance
        
        RemainingBalance = Balance - LeaveCredit 
       
        if RemainingBalance < Decimal('0.00'):
            error_messages.append(f"Your {CheckBalance.Leave_Type_Master.Type} balance is {Balance}  you are applying for {LeaveCredit}")

        
        
        IsDate = objconfig.IsDate
      
        if IsDate and Date:
            objs = Optional_Holidays.objects.filter(Date=Date, Is_Active=True, IsDelete=False)
            if objs.exists():
                OP = True
            else:
                date_object = datetime.strptime(Date, "%Y-%m-%d")

                formatted_date = date_object.strftime("%d-%m-%y")
                error_messages.append(f"No {SelectedLeaveType} is present for {formatted_date}  ")    
                
        if error_messages:
            return error_messages

        return {
            'IsDate': objconfig.IsDate,
            
        }

    except Optional_Holidays.DoesNotExist:
        error_messages.append("No Optional Holiday is present for selected date")
        return error_messages
    except Leave_Config_Details.DoesNotExist:
        error_messages.append("No leave config found")
        return error_messages
    
    except Exception as e:
        error_messages.append(f"An unexpected error occurred: {str(e)}")
        return error_messages



# Leave Appication  Cancel
@transaction.atomic
def Leave__Appication_Cancel(request,id):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")

     OrganizationID = request.session["OrganizationID"]
     UserID = str(request.session["UserID"])
     with transaction.atomic():
        leave_app = Leave_Application.objects.get(id = id)
        leave_app.IsDelete =True
        leave_app.ModifyBy =  UserID
        leave_app.save()

        Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=leave_app.Leave_Type_Master,
                                                                                Emp_code=leave_app.Emp_code,OrganizationID=OrganizationID,IsDelete=False).first()
                
                
        Leave_debit = EmpMonthLevelDebitMaster.objects.filter(Leave_Type_Master=leave_app.Leave_Type_Master,OrganizationID=OrganizationID,
                                                                            Emp_code=leave_app.Emp_code, debit=leave_app.Total_credit).order_by('-CreatedDateTime').first()
                
                
                
        Balance = Leave_Balance.Balance 
        Leave_Balance.Balance  = Balance + Leave_debit.debit
        Leave_Balance.save()

        messages.warning(request,"Leave Application Canceled Succesfully")
        return redirect('Leave_Status') 



# @transaction.atomic
# def Approval_list(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")

#     OrganizationID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])
#     print(UserID)
#     UserType = request.session["UserType"]
#     Department_Name=request.session['Department_Name']
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     headers = {
#     'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
#     }
#     api_url = "http://hotelops.in/API/PyAPI/HREmployeeListForApproval?UserID="+str(UserID)
   
    
#     # response = requests.get(api_url, headers=headers)
#     # # response_content = response.content.decode('utf-8')
#     # mem = response.json()

#     try:
#         response = requests.get(api_url, headers=headers)
#         response.raise_for_status()  # Optional: Check for any HTTP errors
#         emp_list = response.json()
#       #  return JsonResponse(mem)
#     except requests.exceptions.RequestException as e:
#         print(f"Error occurred: {e}")
    
#     today = datetime.now()
#     default_start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
#     default_end_date = (today + timedelta(days=30)).strftime('%Y-%m-%d')

#     Status = request.GET.get('Status', '0')
#     Start_Date = request.GET.get('Start_Date', default_start_date)
#     To_Date = request.GET.get('To_Date', default_end_date)   

#     # Status  = request.GET.get('Status')
#     # Start_Date  = request.GET.get('Start_Date')
#     # To_Date  = request.GET.get('To_Date')
    
#     if Status is None:
#         Status = 0
 
#     if UserType.lower() == "ceo" :
#         approval_list = Leave_Application.objects.filter(IsDelete=False, Status=0)
#     else:
#         approval_list = Leave_Application.objects.filter(OrganizationID=OrganizationID, IsDelete=False, Status=Status,
#                                                          Start_Date__range = (Start_Date,To_Date)
#                                                          )
   
#     employee_data = [] 

#     for emp in emp_list:
    
#             emp_code = emp.get('EmployeeCode')
#             leave_application_entry = approval_list.filter(Emp_code=emp_code)

#             if leave_application_entry:
#                 od =OrganizationDetail(emp.get('OrganizationID'))
#                 employee_details = {
#                     'Hotel':  od.OrganizationDomainCode,
#                     'EmpID': emp.get('EmpID'),
#                     'EmployeeCode': emp_code,
#                     'FirstName': emp.get('FirstName'),
#                     'MiddleName': emp.get('MiddleName'),
#                     'LastName': emp.get('LastName'),
#                     'Department': emp.get('Department'),
#                     'Designation': emp.get('Designation'),
#                     'Reportingto': emp.get('Reportingto'),
#                 }

#                 employee_data.append(employee_details)
#             else:
#                 employee_details = {
#                     'Hotel':  '',
#                     'EmpID': '',
#                     'EmployeeCode': emp_code,
#                     'FirstName': emp.get('FirstName'),
#                     'MiddleName': emp.get('MiddleName'),
#                     'LastName': emp.get('LastName'),
#                     'Department': emp.get('Department'),
#                     'Designation': emp.get('Designation'),
#                     'Reportingto': emp.get('Reportingto'),
#                 }
#                 employee_data.append(employee_details)
        

#     context ={'approval_list':approval_list,'employee_data': employee_data,'Status':Status,'To_Date':To_Date,'Start_Date':Start_Date}
#     return render(request,"LMS/APOOVAL/Approval_list.html",context)





@transaction.atomic
def Approval_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
    UserType = request.session["UserType"]
    EmployeeCode=request.session["EmployeeCode"]
    
    today = datetime.now()
    default_start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
    default_end_date = (today + timedelta(days=30)).strftime('%Y-%m-%d')

    Status = request.GET.get('Status')
    Start_Date = request.GET.get('Start_Date', default_start_date)
    To_Date = request.GET.get('To_Date', default_end_date)   
    approval_list = []
    

    if Status is None:
        Status = 0


    if UserType == "CEO":
        approval_list = Leave_Application.objects.filter(
            IsDelete=False, 
            Status=Status, 
            ReportingtoDesigantion=UserType
        )
        # employee_mapping = {emp.EmployeeCode: emp for emp in EmployeeMaster.objects.filter(IsDelete=False,  ReportingtoDesigantion=UserType)}
        Empobjs = EmployeeDataSelect(ReportingtoDesignation=UserType)
        employee_mapping = {emp['EmployeeCode']: emp for emp in Empobjs}
        
    
    if UserType != "CEO":
        if EmployeeCode is not None and EmployeeCode != '':
           
            
            # obj = EmployeeMaster.objects.get(EmployeeCode=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False)
            # Desigantion = obj.Designation

            obj = EmployeeDataSelect(OrganizationID,EmployeeCode)
            
            if obj:
                Desigantion = obj[0]['Designation']        
                if obj[0]['Department'] == 'Human Resources':
                        approval_list = Leave_Application.objects.filter(
                            OrganizationID=OrganizationID,
                            IsDelete=False,
                            Status=Status,
                            Start_Date__range=(Start_Date, To_Date),    
                        
                        
                        ).exclude(ReportingtoDesigantion="CEO")
                
                else:
                    approval_list = Leave_Application.objects.filter(
                        OrganizationID=OrganizationID,
                        IsDelete=False,
                        Status=Status,
                        Start_Date__range=(Start_Date, To_Date),
                        ReportingtoDesigantion=Desigantion
                    )
            # employee_mapping = {emp.EmployeeCode: emp for emp in EmployeeMaster.objects.filter(IsDelete=False,  OrganizationID=OrganizationID)}
            Empobjs = EmployeeDataSelect(OrganizationID)
            employee_mapping = {emp['EmployeeCode']: emp for emp in Empobjs}
        else:    
            print("Employee Not Code Found")

            messages.warning(request,"Contact to hr department no  Employee Details found")
            return render(request,"LMS/LEAVEAPPLICATION/Error.html")    

    

    employee_data = []
    
    for application in approval_list:
        emp_details = employee_mapping.get(application.Emp_code)
        if emp_details:
            employee_data.append({
                "EmpName": emp_details['EmpName'],
                "EmployeeCode": emp_details['EmployeeCode'],
                "LeaveApplicationDetails": application
            })

   
        
    context = {'employee_data': employee_data,'Status':Status,'To_Date':To_Date,'Start_Date':Start_Date}
    return render(request,"LMS/APOOVAL/Approval_list.html",context)





@transaction.atomic
def CompOfffApproval_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
    UserType = request.session["UserType"]
    EmployeeCode=request.session["EmployeeCode"]
    
    today = datetime.now()
    default_start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
    default_end_date = (today + timedelta(days=30)).strftime('%Y-%m-%d')

    Status = request.GET.get('Status')
    Start_Date = request.GET.get('Start_Date', default_start_date)
    To_Date = request.GET.get('To_Date', default_end_date)   
    approval_list = []
    

    if Status is None:
        Status = "Pending"


    if UserType == "CEO":
        approval_list = Leave_Application.objects.filter(
            IsDelete=False, 
            Status=Status, 
            ReportingtoDesigantion=UserType
        )
        # employee_mapping = {emp.EmployeeCode: emp for emp in EmployeeMaster.objects.filter(IsDelete=False,  ReportingtoDesigantion=UserType)}
        Empobjs = EmployeeDataSelect(ReportingtoDesignation=UserType)
        employee_mapping = {emp['EmployeeCode']: emp for emp in Empobjs}
        
    
    if UserType != "CEO":
        if EmployeeCode is not None and EmployeeCode != '':
           
            
            # obj = EmployeeMaster.objects.get(EmployeeCode=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False)
            # Desigantion = obj.Designation

            obj = EmployeeDataSelect(OrganizationID,EmployeeCode)
            
            if obj:
                Desigantion = obj[0]['Designation']        
                if obj[0]['Department'] == 'Human Resources':
                        approval_list = CompOffApplication.objects.filter(
                            OrganizationID=OrganizationID,
                            IsDelete=False,
                            Status=Status,
                            CompOff_Date__range=(Start_Date, To_Date),    
                        
                        
                        ).exclude(ReportingtoDesigantion="CEO")
                
                else:
                    approval_list = CompOffApplication.objects.filter(
                        OrganizationID=OrganizationID,
                        IsDelete=False,
                        Status=Status,
                        CompOff_Date__range=(Start_Date, To_Date),
                        ReportingtoDesigantion=Desigantion
                    )
            # employee_mapping = {emp.EmployeeCode: emp for emp in EmployeeMaster.objects.filter(IsDelete=False,  OrganizationID=OrganizationID)}
            Empobjs = EmployeeDataSelect(OrganizationID)
            employee_mapping = {emp['EmployeeCode']: emp for emp in Empobjs}
        else:    
            print("Employee Not Code Found")

            messages.warning(request,"Contact to hr department no  Employee Details found")
            return render(request,"LMS/LEAVEAPPLICATION/Error.html")    

    

    employee_data = []
    
    for application in approval_list:
        emp_details = employee_mapping.get(application.Emp_Code)
        if emp_details:
            employee_data.append({
                "EmpName": emp_details['EmpName'],
                "EmployeeCode": emp_details['EmployeeCode'],
                "LeaveApplicationDetails": application
            })

   
        
    context = {'employee_data': employee_data,'Status':Status,'To_Date':To_Date,'Start_Date':Start_Date}
    return render(request,"LMS/APOOVAL/CompOfffApproval_list.html",context)





# def HR_Manager_List(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")

#     OrganizationID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])
#     UserType = request.session["UserType"]
#     Department_Name=request.session['Department_Name']
#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     headers = {
#     'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
#     }
#     api_url = "http://hotelops.in/API/PyAPI/HREmployeeListForApproval?UserID="+str(UserID)
#     # response = requests.get(api_url, headers=headers)
#     # # response_content = response.content.decode('utf-8')
#     # mem = response.json()

#     try:
#         response = requests.get(api_url, headers=headers)
#         response.raise_for_status()  # Optional: Check for any HTTP errors
#         emp_list = response.json()
#       #  return JsonResponse(mem)
#     except requests.exceptions.RequestException as e:
#         print(f"Error occurred: {e}")

#     hotelapitoken = MasterAttribute.HotelAPIkeyToken
#     headers = {
#         'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
#     }
#     api_url = "http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID=" + str(OrganizationID)

#     try:
#         response = requests.get(api_url, headers=headers)
#         response.raise_for_status()  # Optional: Check for any HTTP errors
#         memOrg = response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error occurred: {e}")

#     I = request.GET.get('I')
    
#     Status  = request.GET.get('Status')
#     Start_Date  = request.GET.get('Start_Date')
#     To_Date  = request.GET.get('To_Date')
#     if Status is None:
#         Status = 0
 
#     if I:
#         approval_list = Leave_Application.objects.filter(OrganizationID=I, IsDelete=False, Status=Status,
#                                                          Start_Date__range = (Start_Date,To_Date)
#                                                          )
#     else:
#         approval_list = Leave_Application.objects.filter( IsDelete=False, Status=Status,
#                                                          Start_Date__range = (Start_Date,To_Date)
#                                                          )
#         I = ''

#     employee_data = [] 

#     for emp in emp_list:
        
#         emp_code = emp.get('EmployeeCode')
#         leave_application_entry = approval_list.filter(Emp_code=emp_code)

#         if leave_application_entry:
#             od =OrganizationDetail(emp.get('OrganizationID'))
#             employee_details = {
#                 'Hotel':  od.OrganizationDomainCode,
#                 'EmpID': emp.get('EmpID'),
#                 'EmployeeCode': emp_code,
#                 'FirstName': emp.get('FirstName'),
#                 'MiddleName': emp.get('MiddleName'),
#                 'LastName': emp.get('LastName'),
#                 'Department': emp.get('Department'),
#                 'Designation': emp.get('Designation'),
#                 'Reportingto': emp.get('Reportingto'),
#             }

#             employee_data.append(employee_details)
    
#     context ={'approval_list':approval_list,'employee_data': employee_data,'Status':Status,'memOrg':memOrg,'I':I,'To_Date':To_Date,'Start_Date':Start_Date}
#     return render(request,"LMS/APOOVAL/HR_Manager_List.html",context)





# @transaction.atomic
# def Leave_Status(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         print("Show Page Session")

#     OrganizationID = request.session["OrganizationID"]
#     UserID = str(request.session["UserID"])
#     Emp_code=request.session["EmployeeCode"]
    
#     status = Leave_Application.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Emp_code=Emp_code)
#     currentdate = date.today()
#     context ={'status':status,'currentdate':currentdate}
#     return render(request,"LMS/APOOVAL/Leave_Status.html",context)





from HumanResources.models import EmployeePersonalDetails

@transaction.atomic
def Leave_Status(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserDepartment = request.session["Department_Name"]
    UserType = request.session["UserType"]
    EmpCode = request.session["EmployeeCode"]
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if not start_date:  # If None or empty string
        start_date = (datetime.now() - timedelta(days=30)).date()
    else:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        except ValueError:
            start_date = (datetime.now() - timedelta(days=30)).date()  # Fallback if invalid format

    if not end_date:  # If None or empty string
        end_date = (datetime.now() + timedelta(days=60)).date()
    else:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            end_date = (datetime.now() + timedelta(days=60)).date()  # Fallback if invalid format
    

    # Base QuerySet - Fetch all employees' leave records
    status = Leave_Application.objects.filter(
        OrganizationID=OrganizationID,
        IsDelete=False,
        Start_Date__gte=start_date, 
        End_Date__lte=end_date,
    )

    if UserDepartment.lower() =="hr" or UserType.lower() == "gm":
            employee_ids = EmployeeDataSelect(OrganizationID=OrganizationID)
    else:
        # Fetch Employee Details based on Emp_code in leave records
        employee_ids = EmployeeDataSelect(OrganizationID=OrganizationID,EmployeeCode=EmpCode)

    # Filtering based on user inputs
    
    leave_type = request.GET.get('leave_type')
    leave_status = request.GET.get('status')
    total_credit = request.GET.get('total_credit')

    # Apply filters only if values are provided
    
    if leave_type:
        status = status.filter(Leave_Type_Master_id=leave_type)
    if leave_status:
        status = status.filter(Status=leave_status)
    if total_credit:
        status = status.filter(Total_credit__gte=total_credit)

    # Fetch leave types for dropdown
    leave_types = Leave_Type_Master.objects.all()

    context = {
        'status': status,  # Contains all employees' leave records
        'currentdate': date.today(),
        'leave_types': leave_types,
        "employees": employee_ids,  # Employee details
        "OrganizationID": OrganizationID,  # Organization ID
    }
    return render(request, "LMS/APOOVAL/Leave_Status.html", context)



def build_employee_dict(employee_data):
    return {emp['EmployeeCode']: emp['EmpName'] for emp in employee_data}

@transaction.atomic
def Employee_Leave_Status(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    employeeobj = EmployeeDataSelect(OrganizationID)
    
    employee_dict = build_employee_dict(employeeobj)

    status = Leave_Application.objects.filter(OrganizationID=OrganizationID, IsDelete=False)
    for i in status:
        EmployeeCode = i.Emp_code
        if EmployeeCode in employee_dict:
            i.EmpName = employee_dict[EmployeeCode]
        else:
            i.EmpName = ""  

        i.save()

    currentdate = date.today()
    context = {'status': status, 'currentdate': currentdate}
    return render(request, "LMS/APOOVAL/Employee_Leave_Status.html", context)




@transaction.atomic
def Employee_Leave_Status(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    employeeobj = EmployeeDataSelect(OrganizationID)
    
    employee_dict = build_employee_dict(employeeobj)

    status = Leave_Application.objects.filter(OrganizationID=OrganizationID, IsDelete=False)
    for i in status:
        EmployeeCode = i.Emp_code
        if EmployeeCode in employee_dict:
            i.EmpName = employee_dict[EmployeeCode]
        else:
            i.EmpName = ""  

        i.save()

    currentdate = date.today()
    context = {'status': status, 'currentdate': currentdate}
    return render(request, "LMS/APOOVAL/Employee_Leave_Status.html", context)



@transaction.atomic
def CompOffClaim_Status(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    Emp_code=request.session["EmployeeCode"]
    
    status = CompOffApplication.objects.filter(OrganizationID=OrganizationID,Emp_Code=Emp_code, IsDelete=False)
    currentdate = date.today()
    context = {'status': status, 'currentdate': currentdate}
    return render(request, "LMS/APOOVAL/CompOffClaim_Status.html", context)

from Employee_Payroll.models import Attendance_Data, WeekOffDetails
@transaction.atomic
def Approve_Leave(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    # OrganizationID = request.session["OrganizationID"]
    
    UserID = str(request.session["UserID"])
    UserType = request.session["UserType"]
   
    ApplicationID = request.GET.get('ID')
    OrganizationID = request.GET.get('OID')
    if ApplicationID is not None:
        with transaction.atomic():
            approve =Leave_Application.objects.get(id=ApplicationID,OrganizationID=OrganizationID,IsDelete=False)

            L_id = approve.Leave_Type_Master
            debit = approve.Total_credit
            Emp_code = approve.Emp_code
            
            action = request.GET.get('action') 
            if action == 'approve':
                # Leave_Balance = Emp_Leave_Balance_Master.objects.get(Leave_Type_Master=L_id,
                #                                                                 Emp_code=Emp_code,OrganizationID=OrganizationID,IsDelete=False)
                # Balance=Leave_Balance.Balance 
                # Leave_Balance.Balance  = Balance - debit
                # Leave_Balance.save()
                LeaveStartDate  = approve.Start_Date
                LeaveEndDate =    approve.End_Date
                current_date = LeaveStartDate
                while current_date <= LeaveEndDate:
                    objAtt, created = Attendance_Data.objects.update_or_create(
                        Date=current_date,
                        IsDelete=False,
                        EmployeeCode=Emp_code,
                        OrganizationID=OrganizationID,
                        defaults={
                            'IsDelete': False,  # Fields to update or set
                            # Add other fields you want to update or set here
                            'Status': approve.Leave_Type_Master.Type,
                            'ModifyBy' : UserID
                        }
                    )
                    current_date += timedelta(days=1)
                
                # attendacne = Attendance_Data.objects.filter(
                #                                               Date__range = (LeaveStartDate,LeaveEndDate),OrganizationID = OrganizationID,IsDelete = False,
                #                                               EmployeeCode = Emp_code
                #                                             )
                         
                # for att in attendacne:
                  
                #     att.Status = approve.Leave_Type_Master.Type
                #     att.ModifyBy = UserID
                #     att.save()


                # Leave_debit = EmpMonthLevelDebitMaster.objects.create(Leave_Type_Master=L_id,OrganizationID=OrganizationID,
                #                                                             Emp_code=Emp_code, debit=debit)
                
                
                
                
                
                approve.Status = 1
                approve.ModifyBy = UserID
                messages.success(request, "Leave Approved Successfully")
           
            
                approve.save()
            
                return redirect('Approval_list')
    







def RejectLeave(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    UserID = str(request.session["UserID"])
    UserType = request.session["UserType"]

    if request.method == 'POST':
        ApplicationID = request.POST.get('ID')
        OrganizationID = request.POST.get('OID')
        Remark = request.POST.get('Remark')
        
        if ApplicationID is not None:
            with transaction.atomic():
                approve = get_object_or_404(Leave_Application, id=ApplicationID, OrganizationID=OrganizationID, IsDelete=False)
                approve.Status = -1
                approve.ModifyBy = UserID
                approve.Remark = Remark
                approve.save()
                

                Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=approve.Leave_Type_Master,
                                                                                Emp_code=approve.Emp_code,OrganizationID=OrganizationID,IsDelete=False).first()
                
                
                Leave_debit = EmpMonthLevelDebitMaster.objects.filter(Leave_Type_Master=approve.Leave_Type_Master,OrganizationID=OrganizationID,
                                                                            Emp_code=approve.Emp_code, debit=approve.Total_credit).order_by('-CreatedDateTime').first()
                
                
                
                Balance = Leave_Balance.Balance 
                Leave_Balance.Balance  = Balance + Leave_debit.debit
                Leave_Balance.save()


                messages.warning(request, "Leave Rejected Successfully")
        
        return redirect('Approval_list')
    else:
        return redirect('Approval_list')



def RevokeLeave(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    # OrganizationID = request.session["OrganizationID"]
    
    UserID = str(request.session["UserID"])
    UserType = request.session["UserType"]
   
    ApplicationID = request.GET.get('ID')
    OrganizationID = request.GET.get('OID')
    if ApplicationID is not None:
        with transaction.atomic():
            approve =Leave_Application.objects.get(id=ApplicationID,OrganizationID=OrganizationID,IsDelete=False)

            L_id = approve.Leave_Type_Master
            debit = approve.Total_credit
            Emp_code = approve.Emp_code
            action = request.GET.get('action') 
            if action == 'revoke':
                Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=L_id,
                                                                                Emp_code=Emp_code,OrganizationID=OrganizationID,IsDelete=False).first()
                
                
                Leave_debit = EmpMonthLevelDebitMaster.objects.filter(Leave_Type_Master=L_id,OrganizationID=OrganizationID,
                                                                            Emp_code=Emp_code, debit=debit).order_by('-CreatedDateTime').first()
                
                
                
                Balance = Leave_Balance.Balance 
                Leave_Balance.Balance  = Balance + Leave_debit.debit
                Leave_Balance.save()
                
                LeaveStartDate  = approve.Start_Date
                LeaveEndDate =    approve.End_Date
               
                try:
                    attendacne = Attendance_Data.objects.filter(
                                                                Date__range = (LeaveStartDate,LeaveEndDate),OrganizationID = OrganizationID,IsDelete = False,
                                                                EmployeeCode = Emp_code
                                                                )
                    if attendacne:         
                        for att in attendacne:
                            if att.In_Time and att.Out_Time:
                                Status = "Present"    
                            if att.In_Time or att.Out_Time:
                                Status = "Absent"
                        

                            att.Status = Status
                            att.ModifyBy = UserID
                            att.save()
                except:
                        print("Error")


                
          
                approve.Status = 2
                approve.ModifyBy = UserID
                messages.success(request, "Leave Revoked Successfully")
           
            
                approve.save()
          
                return redirect('Approval_list')
    


def CompOffApprove_Leave(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    # OrganizationID = request.session["OrganizationID"]
    
    UserID = str(request.session["UserID"])
    UserType = request.session["UserType"]
   
    ApplicationID = request.GET.get('ID')
    OrganizationID = request.GET.get('OID')
    if ApplicationID is not None:
        with transaction.atomic():
            approve =CompOffApplication.objects.get(id=ApplicationID,OrganizationID=OrganizationID,IsDelete=False)

            Emp_code = approve.Emp_Code
            
            action = request.GET.get('action') 
            if action == 'approve':
                
                approve.Status = "Approved"
                approve.ModifyBy = UserID
                messages.success(request, "Approved Successfully")
           
            
                approve.save()
                
                balance = 1
                try:
                    previous_balance=0
                    try:
                        LTM_OBJ= Leave_Type_Master.objects.filter(IsDelete=False,OrganizationID=3,Type="Comp-off").first()
                        Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=LTM_OBJ,
                                                                        Emp_code=Emp_code,OrganizationID=OrganizationID,IsDelete=False)
                        if Leave_Balance.exists():
                            Leave_Balance=Leave_Balance.first()
                            previous_balance = Leave_Balance.Balance
                            total = previous_balance + balance
                            Leave_Balance.Balance = total
                            Leave_Balance.ModifyBy=UserID
                            Leave_Balance.save()
                        else:
                            Leave_Balance = Emp_Leave_Balance_Master.objects.create(OrganizationID=OrganizationID,
                                Leave_Type_Master=LTM_OBJ, Emp_code=Emp_code, Balance=balance,CreatedBy=UserID)
                    except:
                        previous_balance=0
                    
                except Emp_Leave_Balance_Master.DoesNotExist:
                        if Emp_code is not None and Emp_code != '':  
                            Leave_Balance = Emp_Leave_Balance_Master.objects.create(OrganizationID=OrganizationID,
                                Leave_Type_Master=LTM_OBJ, Emp_code=Emp_code, Balance=balance)
                Leave_Credit = EmpMonthLevelCreditMaster.objects.create(Leave_Type_Master=LTM_OBJ,OrganizationID=OrganizationID,
                                                                    Emp_code=Emp_code, credit=balance,CreatedBy=UserID)

            
                return redirect('CompOfffApproval_list')
    


def Employee_Leave_Balance(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    EmployeeCode=request.session["EmployeeCode"]
    
    UserID = str(request.session["UserID"])
    UserType = request.session["UserType"]
    
    
    
    
    if UserType == "CEO":
        #  employeeobj = EmployeeMaster.objects.filter(
            
        #      ReportingtoDesigantion=UserType,
        #         IsDelete=False,
                
        #     )
        employeeobj = EmployeeDataSelect(ReportingtoDesignation=UserType)
        
    else:    
        if EmployeeCode is not None and EmployeeCode != '':
            # obj = EmployeeMaster.objects.get(EmployeeCode=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False)
            obj = EmployeeDataSelect(OrganizationID,EmployeeCode)
            Desigantion = obj[0]['Designation']
            # if obj.Department == 'Human Resources':
            #     employeeobj = EmployeeMaster.objects.filter(
                
            #         OrganizationID=OrganizationID,
            #         IsDelete=False
            #     )
            # else:
            #     employeeobj = EmployeeMaster.objects.filter(
            #         ReportingtoDesigantion=Desigantion,
            #         OrganizationID=OrganizationID,
            #         IsDelete=False
            #     )
            if obj[0]['Department'] == 'Human Resources':
                employeeobj = EmployeeDataSelect(OrganizationID)
               
            else:
                 employeeobj = EmployeeDataSelect(OrganizationID,ReportingtoDesignation=Desigantion)
               
        else:

            messages.warning(request,"Contact to hr department no  Employee Details found")
            return render(request,"LMS/LEAVEAPPLICATION/Error.html")        
   
    context = {'emps':employeeobj}
    return render(request,"LMS/BALANCE/Employee_Leave_Balance.html",context)






def Employee_Leave_Apply(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    EmployeeCode=request.session["EmployeeCode"]
    
    UserID = str(request.session["UserID"])
    UserType = request.session["UserType"]
    
    
    
    
    if UserType == "CEO":
       
        employeeobj = EmployeeDataSelect(ReportingtoDesignation=UserType)
        
    else:    
        if EmployeeCode is not None and EmployeeCode != '':
            obj = EmployeeDataSelect(OrganizationID,EmployeeCode)
            Desigantion = obj[0]['Designation']
          
            if obj[0]['Department'] == 'Human Resources':
                employeeobj = EmployeeDataSelect(OrganizationID)
               
            else:
                 employeeobj = EmployeeDataSelect(OrganizationID,ReportingtoDesignation=Desigantion)
               
        else:

            messages.warning(request,"Contact to hr department no  Employee Details found")
            return render(request,"LMS/LEAVEAPPLICATION/Error.html")        
   
    context = {'emps':employeeobj}
    return render(request,"LMS/LEAVEPROCESS/Employee_Leave_Apply.html",context)


@transaction.atomic
def Employee_Leave_Balance_view(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    
    UserID = str(request.session["UserID"])
    UserType = request.session["UserType"]

    
    Emp_code = request.GET.get('ID')
    if UserType == "CEO":
        Leave_balance = Emp_Leave_Balance_Master.objects.filter(IsDelete=False,Emp_code=Emp_code).order_by('Leave_Type_Master_id')
    else:
        Leave_balance = Emp_Leave_Balance_Master.objects.filter(OrganizationID=OrganizationID,IsDelete=False,Emp_code=Emp_code).order_by('Leave_Type_Master_id')
    context = {'Leave_balance':Leave_balance}
    return render(request,"LMS/BALANCE/Employee_Leave_Balance_view.html",context)




# National Holidays  Add


@transaction.atomic
def National_Holidays_ADD(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    N_id = request.GET.get("ID")
    n_data = None
    if N_id is not None:
        n_data = get_object_or_404(National_Holidays,id=N_id,OrganizationID=OrganizationID,IsDelete=False)

    with transaction.atomic():
        if request.method =="POST": 
            if N_id is not None:
                name = request.POST['name']
                Description  = request.POST['Description']
                Date =  request.POST['Date']
                Is_active = request.POST.get('status', '')
                Is_active = True if Is_active == 'on' else False
            

                
                n_data.CreatedBy = UserID
                n_data.Name = name
                n_data.Description = Description
                n_data.Is_Active = Is_active
                n_data.Date=Date
                n_data.ModifyBy = UserID
                n_data.save()

                messages.success(request,"National Holiday Updated Succesfully")
                return redirect('National_Holidays_List') 
            else:
                name = request.POST['name']
                Description  = request.POST['Description']
                Date =  request.POST['Date']
                Is_active = request.POST.get('status', '')
                Is_active = True if Is_active == 'on' else False
            

                National_Holiday = National_Holidays.objects.create(OrganizationID=OrganizationID,CreatedBy = UserID,Name = name,Description = Description,Is_Active = Is_active,Date=Date)
                messages.success(request,"National Holiday Added Succesfully")
                return redirect('National_Holidays_List')    

    
    context ={'n_data':n_data}
    return render(request,"LMS/LEAVE/National_Holidays_ADD.html",context)

# National Holidays  List
@transaction.atomic
def  National_Holidays_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    Nationals = National_Holidays.objects.filter(IsDelete = False).order_by('Date')
    context = {'Nationals':Nationals}

    return render(request,"LMS/LEAVE/National_Holidays_List.html",context)


@transaction.atomic
def National_Holidays_Delete(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")

     OrganizationID = request.session["OrganizationID"]
     UserID = str(request.session["UserID"])
     id = request.GET.get("ID")
     with transaction.atomic():
        National_Holiday = National_Holidays.objects.get(id = id)
        National_Holiday.IsDelete =True
        National_Holiday.ModifyBy =  UserID
        National_Holiday.save()
        messages.warning(request,"National Holiday Deleted Succesfully")
        return redirect('National_Holidays_List')


# Optional Holidays  Add


@transaction.atomic
def Optional_Holidays_ADD(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    o_id = request.GET.get("ID")
    o_data = None
    if o_id is not None:
        o_data = get_object_or_404(Optional_Holidays,id=o_id,OrganizationID=OrganizationID,IsDelete=False)

    with transaction.atomic():
        if request.method =="POST": 
            if o_id is not None:
                name = request.POST['name']
                Description  = request.POST['Description']
                Date =  request.POST['Date']
                Is_active = request.POST.get('status', '')
                Is_active = True if Is_active == 'on' else False
            

                
                o_data.CreatedBy = UserID
                o_data.Name = name
                o_data.Description = Description
                o_data.Is_Active = Is_active
                o_data.Date=Date
                o_data.ModifyBy = UserID
                o_data.save()

                messages.success(request,"Optional Holiday Updated Succesfully")
                return redirect('Optional_Holidays_List') 
            else:
                name = request.POST['name']
                Description  = request.POST['Description']
                Date =  request.POST['Date']
                Is_active = request.POST.get('status', '')
                Is_active = True if Is_active == 'on' else False
            

                Optional_Holiday = Optional_Holidays.objects.create(OrganizationID=OrganizationID,CreatedBy = UserID,Name = name,Description = Description,Is_Active = Is_active,Date=Date)
                messages.success(request,"Optional Holiday Added Succesfully")
                return redirect('Optional_Holidays_List')    

    
    context ={'o_data':o_data}
    return render(request,"LMS/LEAVE/Optional_Holidays_ADD.html",context)

# Optional Holidays  List
@transaction.atomic
def  Optional_Holidays_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    Optionals = Optional_Holidays.objects.filter(IsDelete = False).order_by('Date')
    context = {'Optionals':Optionals}
    
    return render(request,"LMS/LEAVE/Optional_Holidays_List.html",context)



def HolidayList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    Optionals = Optional_Holidays.objects.filter(IsDelete = False).order_by('Date')
    Nationals = National_Holidays.objects.filter(IsDelete = False).order_by('Date')
   
    
    context = {'Optionals':Optionals, 'Nationals':Nationals}
    return render(request,"LMS/LEAVE/HolidayList.html",context)

def employee_leave_report(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    # Get filter parameters from request
    emp_code = request.GET.get("emp_code", None)
    start_date = request.GET.get("start_date", None)
    end_date = request.GET.get("end_date", None)
    leave_type = request.GET.get("leave_type", None)

    # Base Query (Fetching non-deleted leave records)
    leave_query = Leave_Application.objects.filter(IsDelete=False,OrganizationID=OrganizationID)

    # Apply Filters
    if emp_code:
        leave_query = leave_query.filter(Emp_code=emp_code)

    if start_date and end_date:
        leave_query = leave_query.filter(
            Q(Start_Date__lte=end_date) & Q(End_Date__gte=start_date)
        )

    if leave_type:
        leave_query = leave_query.filter(Leave_Type_Master__Type=leave_type)

    # Fetch results
    leave_records = leave_query.order_by("-Start_Date")

    return render(request, "LMS/LEAVE/leave_report.html", {"leaves": leave_records})



@transaction.atomic
def Optional_Holidays_Delete(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")

     OrganizationID = request.session["OrganizationID"]
     UserID = str(request.session["UserID"])
     id = request.GET.get("ID")
     with transaction.atomic():
        Optional_Holiday = Optional_Holidays.objects.get(id = id)
        Optional_Holiday.IsDelete =True
        Optional_Holiday.ModifyBy =  UserID
        Optional_Holiday.save()
        messages.warning(request,"Optional_Holiday Deleted Succesfully")
        return redirect('Optional_Holidays_List')





# End check






# API         

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Leave_Type_Master
from .serializers import LeaveTypeMasterSerializer,EmpLeaveBalanceSerializer,LeaveApplicationSerializer
from datetime import datetime
from decimal import Decimal
from django.http import JsonResponse

class LeaveType(APIView):
    def get(self, request, format=None):
        try:
            hotelapitoken = MasterAttribute.HotelAPIkeyToken
            token =  request.headers.get('hotel-api-token')
           
                    
            if token != hotelapitoken:
                return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)
          
            leaves = Leave_Type_Master.objects.filter(IsDelete=False,Is_Active =True)
            serializer = LeaveTypeMasterSerializer(leaves, many=True)

            return JsonResponse(serializer.data,safe=False)

        except Leave_Type_Master.DoesNotExist:
            return JsonResponse({"error": "Leave type does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LeaveBalance(APIView):
    def get(self,request,format = None):
        try:
            hotelapitoken = MasterAttribute.HotelAPIkeyToken
            token = request.headers.get('hotel-api-token')
            if token != hotelapitoken:
                return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)
            
            organization_id = self.request.query_params.get('OID')
            EmpCode = self.request.query_params.get('EmpCode')
            
            Balance  = Emp_Leave_Balance_Master.objects.filter(Emp_code= EmpCode,OrganizationID = organization_id)
            serializer = EmpLeaveBalanceSerializer(Balance,many = True) 
            return JsonResponse(serializer.data,safe=False)    

        
        except Emp_Leave_Balance_Master.DoesNotExist:
            return JsonResponse({"error": "Leave Balance  not exist"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





class LeaveApply(APIView):
    def get(self, request, format=None):
        try:
            hotelapitoken = MasterAttribute.HotelAPIkeyToken
            token = request.headers.get('hotel-api-token')
            
            if token != hotelapitoken:
                return Response({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)

            
            organization_id = self.request.query_params.get('OID')
            EmpCode = self.request.query_params.get('EmpCode')
            AppID =self.request.query_params.get('AppID')
            if AppID:
                 Application  = Leave_Application.objects.get(id=AppID,IsDelete=False)
                 serializer = LeaveApplicationSerializer(Application)
            else:
                 Application  = Leave_Application.objects.filter(Emp_code = EmpCode,OrganizationID  =organization_id, IsDelete = False)
                 serializer = LeaveApplicationSerializer(Application,many=True)    
            

            return JsonResponse(serializer.data,safe=False)

        except Leave_Application.DoesNotExist:
            return JsonResponse({"error": "Leave Application does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    



       
      
    def post(self,request,format = None):
        try:
            hotelapitoken = MasterAttribute.HotelAPIkeyToken
            token = request.headers.get('hotel-api-token')
            if token != hotelapitoken:
                return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)
            OrganizationID = request.POST.get('OID')
            EmployeeCode = request.POST.get('EmpCode')
            


            # EmployeeDetails = EmployeeMaster.objects.get(EmployeeCode = EmployeeCode ,OrganizationID = OrganizationID ,IsDelete = False)
            EmployeeDetails = EmployeeDataSelect(OrganizationID,EmployeeCode)

            ReportingtoDesigantion  = EmployeeDetails.Designation

       
            LeaveID = request.POST.get('LeaveID')
            UserID = request.POST.get('UserID')
            
            leave_type = Leave_Type_Master.objects.get(id=LeaveID, IsDelete=False, Is_Active = True)         
            
            
            FromHalf = int(request.POST.get('FromHalf', 0))
            ToHalf = int(request.POST.get('ToHalf', 0))
            FromDate = datetime.strptime(request.POST.get('FromDate'), '%Y-%m-%d')
            ToDate = datetime.strptime(request.POST.get('ToDate'), '%Y-%m-%d')
            
            Reason =   request.POST.get('Reason')
            Total_credit = Decimal(request.POST.get('Total_credit'))
            
            
            From_1st_Half = False
            From_2nd_Half = False

            To_1st_Half = False 
            To_2nd_Half = False
            if FromHalf == 0:
                From_1st_Half =  True
            else:
                From_2nd_Half = True

            if ToHalf == 0:
                To_1st_Half =  True
            else:
                To_2nd_Half = True    

            FromDateStr = FromDate.date().strftime('%Y-%m-%d')
            ToDateStr = ToDate.date().strftime('%Y-%m-%d')    
              
           

            Info =  CombinedLeaveInfo(UserID=UserID, OrganizationID=OrganizationID, LeaveID=LeaveID, EmployeeCode=EmployeeCode, SelectedLeaveType=leave_type.Type, LeaveCredit=Total_credit, Start_Date=FromDateStr,End_Date = ToDateStr)
            
            if isinstance(Info, list):
                    context = {'messages': Info}
                    return JsonResponse(context)
            
            
                

            application = Leave_Application.objects.create(OrganizationID=OrganizationID,Status=0,CreatedBy=UserID,
                                                        
                                                        Leave_Type_Master= leave_type,
                                                        Start_Date = FromDate ,From_1st_Half = From_1st_Half,
                                                        From_2nd_Half=From_2nd_Half,
                                                        End_Date=ToDate,
                                                        To_1st_Half = To_1st_Half,
                                                        To_2nd_Half=To_2nd_Half,
                                                        Reason=Reason,
                                                        Total_credit = Total_credit,
                                                        Emp_code=EmployeeCode,
                                                        ReportingtoDesigantion=ReportingtoDesigantion,

                                                        )
            
            return JsonResponse({"success": "Applied"}, status=status.HTTP_200_OK)
        except Exception as e:
                return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



    def put(self,request,format = None):
        try:
            hotelapitoken = MasterAttribute.HotelAPIkeyToken
            token = request.headers.get('hotel-api-token')
            if token != hotelapitoken:
                return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)
            OrganizationID = request.POST.get('OID')
            EmployeeCode = request.POST.get('EmpCode')
            
            AppID =request.POST.get('AppID')
            try:
                Application  = Leave_Application.objects.get(id=AppID,IsDelete=False)
                
                LeaveID = request.POST.get('LeaveID')
                UserID = request.POST.get('UserID')
                leave_type = Leave_Type_Master.objects.get(id=LeaveID,  IsDelete=False,Is_Active = True)         
              
                FromHalf = int(request.POST.get('FromHalf', 0))
                ToHalf = int(request.POST.get('ToHalf', 0))
                FromDate = datetime.strptime(request.POST.get('FromDate'), '%Y-%m-%d')
                ToDate = datetime.strptime(request.POST.get('ToDate'), '%Y-%m-%d')
                
                Reason =   request.POST.get('Reason')
                Total_credit = Decimal(request.POST.get('Total_credit'))
                
                
                From_1st_Half = False
                From_2nd_Half = False

                To_1st_Half = False 
                To_2nd_Half = False
                if FromHalf == 0:
                    From_1st_Half =  True
                else:
                    From_2nd_Half = True

                if ToHalf == 0:
                    To_1st_Half =  True
                else:
                    To_2nd_Half = True

                FromDateStr = FromDate.date().strftime('%Y-%m-%d')
                ToDateStr = ToDate.date().strftime('%Y-%m-%d')    
                
                PreviousLeaveType = Application.Leave_Type_Master
                PreviousLeaveDebit = Application.Total_credit
                Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=PreviousLeaveType,
                                                                                Emp_code=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False).first()
                
                
                Leave_debit = EmpMonthLevelDebitMaster.objects.filter(Leave_Type_Master=PreviousLeaveType,OrganizationID=OrganizationID,
                                                                            Emp_code=EmployeeCode,debit=PreviousLeaveDebit).order_by('-CreatedDateTime').first()
                
                
                if Leave_debit :
                            Balance = Leave_Balance.Balance 
                            Leave_Balance.Balance  = Balance + Leave_debit.debit
                            Leave_Balance.save()


                Info =  CombinedLeaveInfo(UserID=UserID, OrganizationID=OrganizationID, LeaveID=LeaveID, EmployeeCode=EmployeeCode, SelectedLeaveType=leave_type.Type, LeaveCredit=Total_credit, Start_Date=FromDateStr,End_Date = ToDateStr)
                
                if isinstance(Info, list):
                        context = {'messages': Info}
                        return JsonResponse(context)    

                
                Application.Leave_Type_Master= leave_type
                Application.Start_Date =FromDate 
                Application.From_1st_Half = From_1st_Half
                Application.From_2nd_Half=From_2nd_Half
                Application.End_Date=ToDate
                Application.To_1st_Half = To_1st_Half
                Application.To_2nd_Half=To_2nd_Half
                Application.Reason=Reason
                Application.Total_credit = Total_credit
                Application.Emp_code=EmployeeCode
                Application.ModifyBy = UserID
                Application.save()



                Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=leave_type,
                                                Emp_code=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False).first()
                
                Balance=Leave_Balance.Balance 
                Leave_Balance.Balance  = Balance - Decimal(Total_credit)
                Leave_Balance.save()

                                


                Leave_debit = EmpMonthLevelDebitMaster.objects.create(Leave_Type_Master=leave_type,OrganizationID=OrganizationID,
                                                                            Emp_code=EmployeeCode, debit=Total_credit)
            
                
                return JsonResponse({"success": "Updated"}, status=status.HTTP_200_OK)
            except Leave_Application.DoesNotExist:
                return JsonResponse({"error": "Leave Application does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
       
    def delete(self, request, format=None):
            try:
                hotelapitoken = MasterAttribute.HotelAPIkeyToken
                token = request.headers.get('hotel-api-token')
                
                if token != hotelapitoken:
                    return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)
                
                AppID =self.request.query_params.get('AppID')
                try:
                    UserID = self.request.query_params.get('UserID')
                    Application  = Leave_Application.objects.get(id=AppID,IsDelete=False)
                    Application.IsDelete = True
                    Application.ModifyBy = UserID
                    Application.save()
                    return JsonResponse({"success": "Deleted"}, status=status.HTTP_200_OK)
                except Leave_Application.DoesNotExist:
                  return JsonResponse({"error": "Leave Application does not exist"}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
              return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        




class Apporval(APIView):
    def get(self, request, format=None):
        try:
            hotelapitoken = MasterAttribute.HotelAPIkeyToken
            token = request.headers.get('hotel-api-token')
            if token != hotelapitoken:
                return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)
            
            OrganizationID = request.query_params.get('OID')
            
            UserType = request.query_params.get('UserType')
            
            Status = request.query_params.get('Status')
            Start_Date = request.query_params.get('Start_Date')
            To_Date = request.query_params.get('To_Date')
            EmployeeCode  =   request.query_params.get('EmployeeCode','')

            if Status is None:
                Status = 0


            if UserType == "CEO":
                approval_list = Leave_Application.objects.filter(
                    IsDelete=False, 
                    Status=Status, 
                    ReportingtoDesigantion=UserType
                )
                # employee_mapping = {emp.EmployeeCode: emp for emp in EmployeeMaster.objects.filter(IsDelete=False,  ReportingtoDesigantion=UserType)}
                
                
                Empobjs = EmployeeDataSelect(ReportingtoDesignation=UserType)
                employee_mapping = {emp['EmployeeCode']: emp for emp in Empobjs}         
            
            if UserType != "CEO":
                if EmployeeCode is not None and EmployeeCode != '':
                
                    
                    # obj = EmployeeMaster.objects.get(EmployeeCode=EmployeeCode,OrganizationID=OrganizationID,IsDelete=False)
                    # obj = EmployeeDataSelect(OrganizationID,EmployeeCode)
                    # Desigantion = obj.Designation
                    obj = EmployeeDataSelect(OrganizationID,EmployeeCode)
                    Desigantion = obj[0]['Designation']        
                    if obj[0]['Department'] == 'Human Resources':
                            
                            approval_list = Leave_Application.objects.filter(
                                OrganizationID=OrganizationID,
                                IsDelete=False,
                                Status=Status,
                                Start_Date__range=(Start_Date, To_Date),
                            
                            ).exclude(ReportingtoDesigantion="CEO")
                    
                    else:
                       
                        approval_list = Leave_Application.objects.filter(
                            OrganizationID=OrganizationID,
                            IsDelete=False,
                            Status=Status,
                            Start_Date__range=(Start_Date, To_Date),
                            ReportingtoDesigantion=Desigantion
                        )

                
                    # employee_mapping = {emp.EmployeeCode: emp for emp in EmployeeMaster.objects.filter(IsDelete=False,  OrganizationID=OrganizationID)}
                    Empobjs = EmployeeDataSelect(OrganizationID)
                    employee_mapping = {emp['EmployeeCode']: emp for emp in Empobjs}    

            employee_data = []

            for application in approval_list:
                emp_details = employee_mapping.get(application.Emp_code)
                if emp_details:
                    employee_data.append({
                        "EmpName": emp_details['EmpName'],
                        "EmployeeCode": emp_details['EmployeeCode'],
                        "LeaveApplicationDetails": {
                            'Leave_Type': application.Leave_Type_Master.Type,
                            'Start_Date': application.Start_Date,
                            'End_Date': application.End_Date,
                            'Reason': application.Reason,
                            'Status': application.Status,
                            'Total_credit': application.Total_credit,
                            'ID': application.id
                        }
                    })

            if employee_data:
                return JsonResponse(employee_data, safe=False)
            else:
                return JsonResponse({"error": "No Records exist"}, status=status.HTTP_404_NOT_FOUND)

             

       
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



    
    
    
    def post(self,request,format = None):
    
        try:
            hotelapitoken = MasterAttribute.HotelAPIkeyToken
            token = request.headers.get('hotel-api-token')
            if token != hotelapitoken:
                return JsonResponse({"error": "Invalid API token"}, status=status.HTTP_403_FORBIDDEN)        
        
        
            OrganizationID = request.POST.get('OID')
            UserID = request.POST.get('UserID')
            ApplicationID = request.POST.get('AppID')
            
            if ApplicationID is not None:
                with transaction.atomic():
                    approve =Leave_Application.objects.get(id=ApplicationID,OrganizationID=OrganizationID,IsDelete=False)
                    L_id = approve.Leave_Type_Master
                    debit = approve.Total_credit
                    Emp_code = approve.Emp_code
                    action = request.POST.get('Action')
                                
                    if action == 'approve':
                        Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=L_id,
                                                                                        Emp_code=Emp_code,OrganizationID=OrganizationID,IsDelete=False).first()
                        Balance=Leave_Balance.Balance 
                        Leave_Balance.Balance  = Balance - debit
                        Leave_Balance.save()
                        LeaveStartDate  = approve.Start_Date
                        LeaveEndDate =    approve.End_Date
                        current_date = LeaveStartDate
                        while current_date <= LeaveEndDate:
                            objAtt, created = Attendance_Data.objects.update_or_create(
                                Date=current_date,
                                EmployeeCode=Emp_code,
                                IsDelete=False,
                                OrganizationID=OrganizationID,
                                defaults={
                                    'IsDelete': False,  # Fields to update or set
                                    # Add other fields you want to update or set here
                                    'Status': approve.Leave_Type_Master.Type,
                                    'ModifyBy' : UserID
                                }
                            )
                            current_date += timedelta(days=1)
                    
                        # attendacne = Attendance_Data.objects.filter(
                        #                                             Date__range = (LeaveStartDate,LeaveEndDate),OrganizationID = OrganizationID,IsDelete = False,
                        #                                             EmployeeCode = Emp_code
                        #                                             )
                                
                        # for att in attendacne:
                        
                        #     att.Status = approve.Leave_Type_Master.Type
                        #     att.ModifyBy = UserID
                        #     att.save()


                        Leave_debit = EmpMonthLevelDebitMaster.objects.create(Leave_Type_Master=L_id,OrganizationID=OrganizationID,
                                                                                    Emp_code=Emp_code, debit=debit)
                        
                        approve.Status = 1
                        approve.ModifyBy = UserID
                       
                    
                        approve.save()
                        return JsonResponse({"success": "Approved Successfully"}, status=status.HTTP_200_OK)
                    
                    if action == 'revoke':
                        Leave_Balance = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=L_id,
                                                                                        Emp_code=Emp_code,OrganizationID=OrganizationID,IsDelete=False).first()
                        
                        
                        Leave_debit = EmpMonthLevelDebitMaster.objects.filter(Leave_Type_Master=L_id,OrganizationID=OrganizationID,
                                                                                    Emp_code=Emp_code, debit=debit).order_by('-CreatedDateTime').first()
                        
                        
                        
                        Balance = Leave_Balance.Balance 
                        Leave_Balance.Balance  = Balance + Leave_debit.debit
                        Leave_Balance.save()
                        
                        LeaveStartDate  = approve.Start_Date
                        LeaveEndDate =    approve.End_Date
                    
                        attendacne = Attendance_Data.objects.filter(
                                                                    Date__range = (LeaveStartDate,LeaveEndDate),OrganizationID = OrganizationID,IsDelete = False,
                                                                    EmployeeCode = Emp_code
                                                                    )
                        if attendacne:         
                            for att in attendacne:
                                if att.In_Time and att.Out_Time:
                                    Status = "Present"    
                                if att.In_Time or att.Out_Time:
                                    Status = "Absent"
                            

                                att.Status = Status
                                att.ModifyBy = UserID
                                att.save()


                        
                       
                        approve.Status = 2
                        approve.ModifyBy = UserID
                        approve.save()
                      
                        return JsonResponse({"success": "Revoked Successfully"}, status=status.HTTP_200_OK)
                    

                    if action == "reject":
                        Remark = request.POST.get('Remark')
                     
                        approve =Leave_Application.objects.get(id=ApplicationID,OrganizationID=OrganizationID,IsDelete=False)
                        approve.Status = -1
                        approve.ModifyBy = UserID
                        approve.Remark = Remark
                        approve.save()
                        
                        
                        return JsonResponse({"success": "Rejected Successfully"}, status=status.HTTP_200_OK)



                    else:
                        return JsonResponse({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
                    
        except Exception as e:
              return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  







