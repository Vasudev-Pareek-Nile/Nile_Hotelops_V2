from pyexpat.errors import messages
from wsgiref import headers
from django.shortcuts import render,HttpResponse,redirect
from Leave_Management_System.models import Emp_Leave_Balance_Master, EmpMonthLevelDebitMaster, Leave_Application
from app.models import OrganizationMaster
import json
from rest_framework.decorators import api_view
from hotelopsmgmtpy.GlobalConfig import MasterAttribute 
import requests
from django.http import JsonResponse
from .config import Config
from django.db  import connection, transaction

from Employee_Payroll.models import Attendance_Data, WeekOffDetails

@transaction.atomic
def CEOApprove_Leave(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    # OrganizationID = request.session["OrganizationID"]
    
    UserID = str(request.session["UserID"])
    UserType = request.session["UserType"]
    
    ApplicationID = request.POST.get('AppID',0)
    OrganizationID = request.POST.get('OID',0)
    Remark = request.POST.get('Remark','')
    action = request.POST.get('BtnAction','')
    if ApplicationID is not None:
        approve =Leave_Application.objects.get(id=ApplicationID,OrganizationID=OrganizationID,IsDelete=False)
        with transaction.atomic():
            

            L_id = approve.Leave_Type_Master
            debit = approve.Total_credit
            Emp_code = approve.Emp_code
            
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
                
                approve.Status = 1
                approve.ModifyBy = UserID
                approve.save()
            else:
                
                #approve = get_object_or_404(Leave_Application, id=ApplicationID, OrganizationID=OrganizationID, IsDelete=False)
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
        
    return redirect("/dashboard/CEoDashboard")            
    


from django.shortcuts import get_object_or_404




def CEORejectLeave(request):
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


                
        
        return redirect("/dashboard")        
    else:
         return redirect("/dashboard")        







def dashboard_view(request,id):
    ApiToken=request.session["ApiToken"]#="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6InZpa3JhbUBOaWxlIiwidG9rZW4iOiJNVU52TW5Kc1JFSlZka3RrWmpsVmMwbGxZVXg2WVhWSU0zVjZNVlYyUkd4emJFRnlXbnBWTVhCQlVGRkRiVEJHYzFocE1XRjFObGhTT0V4UWJHRk1jV1ZsVlc4eGN6ZHlZMGQyT1ZRMVJrZFhUMlJqWVUxQ1pUVnJlVEpEWnpoRVkxUk1NRVZ3VDFoVVQwbEtkamRYUlZsSk0yaGpka1ZxVWtKbk5uQXlVakV4ZVRKMGREUmtWVk5EVTFCWGNIWlJUV2xFZG1oUlozSldiWEpDYVRoc1MxZHFTV3BWYTNSalkyaEJiMVo1TjAxb1UxSTBaRlV6ZWtkRVducEhNR0p5V2tSUFNWUlRVbWwzVlhSUFNXOHpXV0ZoVEdwUmNXTmpXSGRJTldwalNuVmtTa3hrWmpONlNsZ3hUVGc0YW5sRFVHZEhVM0ZZZWpSbFdGY3ljR1ZTV1E9PSIsIlVzZXJJRCI6IjIwMjAxMjEyMTgwMDQ4IiwiT3JnYW5pemF0aW9uSUQiOiIzIiwiVXNlclR5cGUiOiJDRU8iLCJuYmYiOjE3MzA3MDk4NzksImV4cCI6MTc2MjI0NTg3OSwiaWF0IjoxNzMwNzA5ODc5fQ.u1qKojYzFFMFU40OiSNcnxSOViBn0p4ui5fn1NHTxGw"
    
    if 'CEoDashboard' ==id:
        ApiToken=request.session["ApiToken"]
        bdayData=DashboardBday(ApiToken)
        return render(request, 'ceodashboard/CEoDashboard.html',{'bdayData':bdayData})
    elif 'GMDashboard' == id:
        ApiToken=request.session["ApiToken"]
        bdayData=GMDashboardBday(ApiToken)
        return render(request, 'ceodashboard/GMDashboard.html',{'bdayData':bdayData})
    elif 'RoomDivisionDashboard' == id:
        ApiToken=request.session["ApiToken"]
        bdayData=DashboardBday(ApiToken)
        return render(request, 'ceodashboard/RoomDivision.html',{'bdayData':bdayData})
    elif 'FBServiceDashboard'  == id:
        ApiToken=request.session["ApiToken"]
        bdayData=DashboardBday(ApiToken)
        return render(request, 'ceodashboard/FBServiceDashboard.html',{'bdayData':bdayData})
    elif 'FBProductionDashboard'  == id:
        ApiToken=request.session["ApiToken"]
        bdayData=DashboardBday(ApiToken)
        return render(request, 'ceodashboard/FBServiceDashboard.html',{'bdayData':bdayData})
    elif 'revenueDashboard' == id:
        ApiToken=request.session["ApiToken"]
        bdayData=DashboardBday(ApiToken)
        return render(request, 'ceodashboard/revenue.html',{'bdayData':bdayData})
    elif 'marketingDashboard' == id:
        ApiToken=request.session["ApiToken"]
        bdayData=DashboardBday(ApiToken)
        return render(request, 'ceodashboard/marketingDashboard.html',{'bdayData':bdayData})
    elif 'saleDashboard' == id:
        ApiToken=request.session["ApiToken"]
        bdayData=DashboardBday(ApiToken)
        return render(request, 'ceodashboard/SaleDashboard.html',{'bdayData':bdayData})
    elif 'financeDashboard' == id:
        ApiToken=request.session["ApiToken"]
        bdayData=DashboardBday(ApiToken)
        return render(request, 'ceodashboard/finance.html',{'bdayData':bdayData})
    elif 'D_OpsDashboard' == id:
        ApiToken=request.session["ApiToken"]
        bdayData=DashboardBday(ApiToken)
        return render(request, 'ceodashboard/d_opsDashboard.html',{'bdayData':bdayData})
    elif 'EngineeringDashboard' == id:
        ApiToken=request.session["ApiToken"]
        bdayData=DashboardBday(ApiToken)
        return render(request, 'ceodashboard/EngineeringDashboard.html',{'bdayData':bdayData})
    elif 'HRDashboard' == id:
        ApiToken=request.session["ApiToken"]
        bdayData=DashboardBday(ApiToken)
        return render(request, 'ceodashboard/HRDashboard.html',{'bdayData':bdayData})
    elif 'TrainingDashboard' == id:
        ApiToken=request.session["ApiToken"]
        bdayData=DashboardBday(ApiToken)
        return render(request, 'ceodashboard/trainingDashboard.html',{'bdayData':bdayData})

def HotelRevenueChartData(request):
    RT = request.GET.get('RT','4')
    Edate= request.GET.get('Edate','')
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}HotelRevenueChartData?RT={RT}"
    if Edate!="":
        url=f"{main_url}HotelRevenueChartData?RT={RT}&Edate={Edate}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            HotelRevenueData = []

            for item in data.get("Table", []):
                hotel_name = item.get("Hotel")
                ARR = item.get("ARR")
                RevPar = round(item.get("RevPar", 0)) if item.get("RevPar") is not None else 0
                OCC = round(item.get("OCC", 0)) if item.get("OCC") is not None else 0
                TotalRevenue = round(item.get("TotalRevenue", 0)) if item.get("TotalRevenue") is not None else 0
                RoomRevenue = round(item.get("RoomRevenue", 0)) if item.get("RoomRevenue") is not None else 0
                FTD_Budget = round(item.get("FTD_Budget", 0)) if item.get("FTD_Budget") is not None else 0
                FBRevenue = round(item.get("FBRevenue", 0)) if item.get("FBRevenue") is not None else 0
                FTD_Variance = round(item.get("FTD_Variance", 0)) if item.get("FTD_Variance") is not None else 0
                MTD_Budget = round(item.get("MTD_Budget", 0)) if item.get("MTD_Budget") is not None else 0
                MTD_TotalBudget = round(item.get("MTD_TotalBudget", 0)) if item.get("MTD_TotalBudget") is not None else 0
                MTD_Actual = round(item.get("MTD_Actual", 0)) if item.get("MTD_Actual") is not None else 0
                MTD_Variance = round(item.get("MTD_Variance", 0)) if item.get("MTD_Variance") is not None else 0                   
                MTD_TotalVariance = round(item.get("MTD_TotalVariance", 0)) if item.get("MTD_TotalVariance") is not None else 0
                YTD_Budget = round(item.get("YTD_Budget", 0)) if item.get("YTD_Budget") is not None else 0
                YTD_TotalBudget = round(item.get("YTD_TotalBudget", 0)) if item.get("YTD_TotalBudget") is not None else 0
                YTD_Actual = round(item.get("YTD_Actual", 0)) if item.get("YTD_Actual") is not None else 0
                YTD_Variance = round(item.get("YTD_Variance", 0)) if item.get("YTD_Variance") is not None else 0
                YTD_TotalVariance = round(item.get("YTD_TotalVariance", 0)) if item.get("YTD_TotalVariance") is not None else 0

                HotelRevenueData.append({
                    "Hotel": hotel_name,
                    "ARR" :ARR,
                    "RevPar": RevPar,
                    "OCC":OCC,
                    "TotalRevenue":TotalRevenue,
                    "FBRevenue":FBRevenue,
                    "RoomRevenue":RoomRevenue,
                    "FTD_Variance":FTD_Variance,
                    "FTD_Budget":FTD_Budget,
                    "MTD_Budget":MTD_Budget,
                    "MTD_TotalBudget":MTD_TotalBudget,
                    "MTD_Actual":MTD_Actual,
                    "MTD_Variance":MTD_Variance,
                    "MTD_TotalVariance":MTD_TotalVariance,
                    "YTD_Budget":YTD_Budget,
                    "YTD_TotalBudget":YTD_TotalBudget,
                    "YTD_Actual":YTD_Actual,
                    "YTD_Variance":YTD_Variance,
                    "YTD_TotalVariance":YTD_TotalVariance,


                })
            
            return JsonResponse({"Table": HotelRevenueData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)
        

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMRevenueChartData(request):
    RT = request.GET.get('RT')
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMHotelRevenueChartData?RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            HotelRevenueData = []

            for item in data.get("Table", []):
                hotel_name = item.get("Hotel")
                ARR = item.get("ARR")
                RevPar = round(item.get("RevPar", 0)) if item.get("RevPar") is not None else 0
                OCC = round(item.get("OCC", 0)) if item.get("OCC") is not None else 0
                TotalRevenue = round(item.get("TotalRevenue", 0)) if item.get("TotalRevenue") is not None else 0
                RoomRevenue = round(item.get("RoomRevenue", 0)) if item.get("RoomRevenue") is not None else 0
                FTD_Budget = round(item.get("FTD_Budget", 0)) if item.get("FTD_Budget") is not None else 0
                FBRevenue = round(item.get("FBRevenue", 0)) if item.get("FBRevenue") is not None else 0
                FTD_Variance = round(item.get("FTD_Variance", 0)) if item.get("FTD_Variance") is not None else 0
                MTD_Budget = round(item.get("MTD_Budget", 0)) if item.get("MTD_Budget") is not None else 0
                MTD_TotalBudget = round(item.get("MTD_TotalBudget", 0)) if item.get("MTD_TotalBudget") is not None else 0
                MTD_Actual = round(item.get("MTD_Actual", 0)) if item.get("MTD_Actual") is not None else 0
                MTD_Variance = round(item.get("MTD_Variance", 0)) if item.get("MTD_Variance") is not None else 0                   
                MTD_TotalVariance = round(item.get("MTD_TotalVariance", 0)) if item.get("MTD_TotalVariance") is not None else 0
                YTD_Budget = round(item.get("YTD_Budget", 0)) if item.get("YTD_Budget") is not None else 0
                YTD_TotalBudget = round(item.get("YTD_TotalBudget", 0)) if item.get("YTD_TotalBudget") is not None else 0
                YTD_Actual = round(item.get("YTD_Actual", 0)) if item.get("YTD_Actual") is not None else 0
                YTD_Variance = round(item.get("YTD_Variance", 0)) if item.get("YTD_Variance") is not None else 0
                YTD_TotalVariance = round(item.get("YTD_TotalVariance", 0)) if item.get("YTD_TotalVariance") is not None else 0

                HotelRevenueData.append({
                    "Hotel": hotel_name,
                    "ARR" :ARR,
                    "RevPar": RevPar,
                    "OCC":OCC,
                    "TotalRevenue":TotalRevenue,
                    "FBRevenue":FBRevenue,
                    "RoomRevenue":RoomRevenue,
                    "FTD_Variance":FTD_Variance,
                    "FTD_Budget":FTD_Budget,
                    "MTD_Budget":MTD_Budget,
                    "MTD_TotalBudget":MTD_TotalBudget,
                    "MTD_Actual":MTD_Actual,
                    "MTD_Variance":MTD_Variance,
                    "MTD_TotalVariance":MTD_TotalVariance,
                    "YTD_Budget":YTD_Budget,
                    "YTD_TotalBudget":YTD_TotalBudget,
                    "YTD_Actual":YTD_Actual,
                    "YTD_Variance":YTD_Variance,
                    "YTD_TotalVariance":YTD_TotalVariance,


                })
            
            return JsonResponse({"Table": HotelRevenueData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)
        

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

       

def DashboardBday(ApiToken):
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':"Bearer "+ApiToken,
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}CEODashboardUpComingBirthday"
    


    
    try:
        response = requests.request('get',url, headers=TOKEN_HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            bdayData = []

            for item in data:
                hotel_name = item.get("HTL")
                EmpName = item.get("EmpName")
                Date = item.get("Date")
                
                bdayData.append({
                    "hotel_name": hotel_name,
                    "EmpName": EmpName,
                    "Date": Date,
                })    
             
            return bdayData
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMDashboardBday(ApiToken):
    main_url = Config.API_URL
   
    TOKEN_HEADERS ={
        'Authorization':"Bearer "+ApiToken,
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMDashboardUpComingBirthday"
    


    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            bdayData = []

            for item in data:
                hotel_name = item.get("HTL")
                EmpName = item.get("EmpName")
                Date = item.get("Date")
                
                bdayData.append({
                    "hotel_name": hotel_name,
                    "EmpName": EmpName,
                    "Date": Date,
                })    
             
            return bdayData
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def revenue_data_view(request):
    RT = request.GET.get('time_range')
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEORevenueTotal?RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            item = data.get("Table", [])[0]

            if item:  
                TotalREVENUE = item.get("TotalREVENUE")
                RoomRevenue = item.get("RoomRevenue")
                FBRevenue = item.get("FBRevenue")
                RestRevenue = item.get("RestRevenue")
                BanquetRevenue = item.get("BanquetRevenue")
                RevPar = item.get("RevPar")
                ADR = item.get("ADR")
            
           
            data ={
                    "TotalREVENUE": TotalREVENUE,
                    "RoomRevenue" :RoomRevenue,
                    "FBRevenue": FBRevenue,
                    "RestRevenue":RestRevenue,
                    "BanquetRevenue":BanquetRevenue,
                    "RevPar":RevPar,
                    "ADR" : ADR

                }
            
            
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMRevenueData(request):
    RT = request.GET.get('time_range')
    main_url = Config.API_URL

     
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMHotelRevenueData?RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            item = data.get("Table", [])[0]

            if item:  
                TotalREVENUE = item.get("TotalREVENUE")
                RoomRevenue = item.get("RoomRevenue")
                FBRevenue = item.get("FBRevenue")
                RestRevenue = item.get("RestRevenue")
                BanquetRevenue = item.get("BanquetRevenue")
                RevPar = item.get("RevPar")
                ADR = item.get("ADR")
                
                AvgTotalREVENUE = item.get("AvgTotalREVENUE")
                AvgRoomRevenue = item.get("AvgRoomRevenue")
                AvgFBRevenue = item.get("AvgFBRevenue")
                AvgRestRevenue = item.get("AvgRestRevenue")
                AvgBanquetRevenue = item.get("AvgBanquetRevenue")
                AvgRevPar = item.get("AvgRevPar")
                AvgADR = item.get("AvgADR")
           
            data ={
                    "TotalREVENUE": TotalREVENUE,
                    "RoomRevenue" :RoomRevenue,
                    "FBRevenue": FBRevenue,
                    "RestRevenue":RestRevenue,
                    "BanquetRevenue":BanquetRevenue,
                    "RevPar":RevPar,
                    "ADR" : ADR,

                    "AvgTotalREVENUE": AvgTotalREVENUE,
                    "AvgRoomRevenue" :AvgRoomRevenue,
                    "AvgFBRevenue": AvgFBRevenue,
                    "AvgRestRevenue":AvgRestRevenue,
                    "AvgBanquetRevenue":AvgBanquetRevenue,
                    "AvgRevPar":AvgRevPar,
                    "AvgADR" : AvgADR

                }
            
            
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

    

def RDSalesContractChartData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}RDSalesContractChartData?RT={RT}"

    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            saleChart_data = []
            for item in data.get("Table", []):
                hotel_name = item.get("Hotel")
                OrganizationID= item.get("OrganizationID")
                Total = round(item.get("Total", 0)) if item.get("Total") is not None else 0
                TotalActive = round(item.get("TotalActive", 0)) if item.get("TotalActive") is not None else 0
                TotalExpired = round(item.get("TotalExpired", 0)) if item.get("TotalExpired") is not None else 0
                DetailsJson =item.get("DetailsJson")
                  
                saleChart_data.append({
                    "Hotel": hotel_name,
                    "OrganizationID" :OrganizationID,
                    "Total": Total,
                    "DetailsJson":DetailsJson,
                    "TotalActive":TotalActive,
                    "TotalExpired":TotalExpired
                })
            
            return JsonResponse({"Table": saleChart_data})
        
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def RDSalesContractChartDataDetails(request):
    RT = request.GET.get('RT', None)
    OID= request.GET.get('OrganizationID',None)
    status= request.GET.get('status')
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}RDSalesContractChartDataDetails?OID={OID}&status={status}&RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            saleChartDetailsData = []
            for item in data:
                CompanyName = item.get("CompanyName")
                VendorName = item.get("VendorName")
                FromDate = item.get("FromDate")
                ToDate = item.get("ToDate")
                UploadStatus = item.get("UploadStatus")
                AccountManager =item.get("AccountManager")
                CreditApproved =item.get("CreditApproved")
                
                saleChartDetailsData.append({
                    "CompanyName": CompanyName,
                    "VendorName" :VendorName,
                    "FromDate": FromDate,
                    "ToDate":ToDate,
                    "UploadStatus":UploadStatus,
                    "AccountManager":AccountManager,
                    "CreditApproved":CreditApproved,
                })
            
            
            return JsonResponse({"saleChartDetailsData": saleChartDetailsData})
        
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMSalesContractChartData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMSalesContractChartData?RT={RT}"

    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            saleChart_data = []
            for item in data.get("Table", []):
                hotel_name = item.get("Hotel")
                OrganizationID= item.get("OrganizationID")
                Total = round(item.get("Total", 0)) if item.get("Total") is not None else 0
                TotalActive = round(item.get("TotalActive", 0)) if item.get("TotalActive") is not None else 0
                TotalExpired = round(item.get("TotalExpired", 0)) if item.get("TotalExpired") is not None else 0
                DetailsJson =item.get("DetailsJson")
                  
                saleChart_data.append({
                    "Hotel": hotel_name,
                    "OrganizationID" :OrganizationID,
                    "Total": Total,
                    "DetailsJson":DetailsJson,
                    "TotalActive":TotalActive,
                    "TotalExpired":TotalExpired
                })
            
            return JsonResponse({"Table": saleChart_data})
        
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)





def hotel_chart_data(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}HotelRevenueChartData?RT={RT}"
    url1=f"{main_url}CEORevenueTotal?RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        HotelChartData = []
        RoomData = []
        if response.status_code == 200:
            data = response.json()

            for item in data.get("Table", []):
                hotel_name = item.get("Hotel")
                ARR = item.get("ARR")
                RevPar = round(item.get("RevPar", 0)) if item.get("RevPar") is not None else 0
                OCC = round(item.get("OCC", 0)) if item.get("OCC") is not None else 0  
                
                HotelChartData.append({
                    "hotel_name": hotel_name,
                    "ARR" :ARR,
                    "RevPar": RevPar,
                    "OCC":OCC
                })
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)
        
        response2 = requests.get(url1, headers=TOKEN_HEADERS)
        if response2.status_code == 200:
            data2 = response2.json()
            item = data2.get("Table", [])[0]
           
            
            if item:
                CompRoom = item.get("CompRoom")
                H_CompRoom = item.get("H_CompRoom")
                V_CompRoom = item.get("V_CompRoom")
                CompRoomPer = item.get("CompRoomPer")
                TotalGlitch = item.get("TotalGlitch")
                TotalGlitchPer = item.get("TotalGlitchPer")
                TotalIncident = item.get("TotalIncident")
                TotalIncidentPer = item.get("TotalIncidentPer") 
                 
            RoomData.append({
                    "CompRoom": CompRoom,
                    "H_CompRoom" :H_CompRoom,
                    "V_CompRoom": V_CompRoom,
                    "CompRoomPer":CompRoomPer,
                    "TotalGlitch": TotalGlitch,
                    "TotalGlitchPer" :TotalGlitchPer,
                    "TotalIncident": TotalIncident,
                    "TotalIncidentPer":TotalIncidentPer,
                })
        else:
            return JsonResponse({"error": "Failed to fetch data from second API"}, status=response2.status_code)
        
        return JsonResponse({
            "HotelChartData": HotelChartData,
            "RoomData": RoomData
        })
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
def GMhotel_chart_data(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMHotelRevenueChartData?RT={RT}"
    url1=f"{main_url}GMHotelRevenueData?RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        HotelChartData = []
        RoomData = []
        if response.status_code == 200:
            data = response.json()

            for item in data.get("Table", []):
                hotel_name = item.get("Hotel")
                ARR = item.get("ARR")
                RevPar = round(item.get("RevPar", 0)) if item.get("RevPar") is not None else 0
                OCC = round(item.get("OCC", 0)) if item.get("OCC") is not None else 0  
                
                HotelChartData.append({
                    "hotel_name": hotel_name,
                    "ARR" :ARR,
                    "RevPar": RevPar,
                    "OCC":OCC
                })
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)
        
        response2 = requests.get(url1, headers=TOKEN_HEADERS)
        if response2.status_code == 200:
            data2 = response2.json()
            item = data2.get("Table", [])[0]
           
            
            if item:
                CompRoom = item.get("CompRoom")
                H_CompRoom = item.get("H_CompRoom")
                V_CompRoom = item.get("V_CompRoom")
                CompRoomPer = item.get("CompRoomPer")
                TotalGlitch = item.get("TotalGlitch")
                TotalGlitchPer = item.get("TotalGlitchPer")
                TotalIncident = item.get("TotalIncident")
                TotalIncidentPer = item.get("TotalIncidentPer") 
                 
            RoomData.append({
                    "CompRoom": CompRoom,
                    "H_CompRoom" :H_CompRoom,
                    "V_CompRoom": V_CompRoom,
                    "CompRoomPer":CompRoomPer,
                    "TotalGlitch": TotalGlitch,
                    "TotalGlitchPer" :TotalGlitchPer,
                    "TotalIncident": TotalIncident,
                    "TotalIncidentPer":TotalIncidentPer,
                })
        else:
            return JsonResponse({"error": "Failed to fetch data from second API"}, status=response2.status_code)
        
        return JsonResponse({
            "HotelChartData": HotelChartData,
            "RoomData": RoomData
        })
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def CompRoomDetails(request):
    
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 100))  # default: 100 records

    offset = (page - 1) * page_size
    url = f"{main_url}CompRoomDetails?RT={RT}&offset={offset}&limit={page_size}"
    # url=f"{main_url}CompRoomDetails?RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            # CompRoomData = []
            # for item in data:
            #     ID = item.get("ID", 0)
            #     hotel_name = item.get("Hotel")
            #     GuestName = item.get("GuestName")
            #     CompanyName = item.get("CompanyName")
            #     NoRoom =item.get("NoRoom")
            #     ArrivalDate = item.get("ArrivalDate")
            #     DepartureDate =item.get("DepartureDate")
            #     CompRoomStatus =item.get("CompRoomStatus")
                
            #     CompRoomData.append({
            #         "ID": ID,
            #         "Hotel": hotel_name,
            #         "GuestName":GuestName,
            #         "CompanyName": CompanyName,
            #         "NoRoom": NoRoom,
            #         "ArrivalDate":ArrivalDate,
            #         "DepartureDate": DepartureDate,
            #         "CompRoomStatus": CompRoomStatus,
                    
            #     })
            
            return JsonResponse({"CompRoomData": data})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMCompRoomDetails(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMCompRoomDetails?RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            CompRoomData = []
            for item in data:
                ID = item.get("ID", 0)
                hotel_name = item.get("Hotel")
                GuestName = item.get("GuestName")
                CompanyName = item.get("CompanyName")
                NoRoom =item.get("NoRoom")
                ArrivalDate = item.get("ArrivalDate")
                DepartureDate =item.get("DepartureDate")
                CompRoomStatus =item.get("CompRoomStatus")
                
                CompRoomData.append({
                    "ID": ID,
                    "Hotel": hotel_name,
                    "GuestName":GuestName,
                    "CompanyName": CompanyName,
                    "NoRoom": NoRoom,
                    "ArrivalDate":ArrivalDate,
                    "DepartureDate": DepartureDate,
                    "CompRoomStatus": CompRoomStatus,
                    
                })
            
            return JsonResponse({"CompRoomData": CompRoomData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def maintanceBreakdown(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOEngineeringChartData?RT={RT}"
   
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            totalMaintaceBreakdownData = []
            for item in data.get("Table", []):
                TotalEq = round(item.get("TotalEq", 0)) if item.get("TotalEq") is not None else 0
                TotalUW = round(item.get("TotalUW", 0)) if item.get("TotalUW") is not None else 0
                TotalUA = round(item.get("TotalUA", 0)) if item.get("TotalUA") is not None else 0
                TotalBreakdown = round(item.get("TotalBreakdown", 0)) if item.get("TotalBreakdown") is not None else 0
                TotalBreakdownAmount =round(item.get("TotalBreakdownAmount", 0)) if item.get("TotalBreakdownAmount") is not None else 0
                TotalMaint = round(item.get("TotalMaint", 0)) if item.get("TotalMaint") is not None else 0
                TotalMaintPending =round(item.get("TotalMaintPending", 0)) if item.get("TotalMaintPending") is not None else 0
         
                totalMaintaceBreakdownData.append({
                    "TotalEq": TotalEq,
                    "TotalUW": TotalUW,
                    "TotalUA":TotalUA,
                    "TotalBreakdown": TotalBreakdown,
                    "TotalBreakdownAmount": TotalBreakdownAmount,
                    "TotalMaint":TotalMaint,
                    "TotalMaintPending": TotalMaintPending,   
                })
           
            maintancData = []

            maintenanceBreakdownData = {}
            if "Table1" in data:
                for item in data.get("Table1", []):
                    hotel_name = item.get("HTL")
                    OrganizationID = item.get("OrganizationID")
                    Total_maintance = round(item.get("Total", 0)) if item.get("Total") is not None else 0

                    
                    maintenanceBreakdownData[hotel_name] = {
                        "Hotel": hotel_name,
                        "OrganizationID": OrganizationID,
                        "Total_maintance": Total_maintance,
                        "Total_maintance_complete": 0,  
                        "breakdown_count": 0,           
                        "breakdown_repaired": 0         
                    }

            if "Table2" in data:
                for item in data.get("Table2", []):
                    hotel_name = item.get("HTL")
                    Total_maintance_complete = round(item.get("Total", 0)) if item.get("Total") is not None else 0

                    if hotel_name in maintenanceBreakdownData:
                        maintenanceBreakdownData[hotel_name]["Total_maintance_complete"] = Total_maintance_complete

            
            if "Table3" in data:
                for item in data.get("Table3", []):
                    hotel_name = item.get("HTL")
                    breakdown_count = round(item.get("Total", 0)) if item.get("Total") is not None else 0

                    if hotel_name in maintenanceBreakdownData:
                        maintenanceBreakdownData[hotel_name]["breakdown_count"] = breakdown_count

            
            if "Table4" in data:
                for item in data.get("Table4", []):
                    hotel_name = item.get("HTL")
                    breakdown_repaired = round(item.get("Total", 0)) if item.get("Total") is not None else 0

                    if hotel_name in maintenanceBreakdownData:
                        maintenanceBreakdownData[hotel_name]["breakdown_repaired"] = breakdown_repaired

        
            maintancData = list(maintenanceBreakdownData.values())
            response_data = {
                'totalMaintaceBreakdownData': totalMaintaceBreakdownData,
                'maintenanceBreakdownData': maintancData,
        
             }
            return JsonResponse(response_data)   
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMMaintanceBreakdown(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMEngineeringChartData?RT={RT}"
   
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            totalMaintaceBreakdownData = []
            for item in data.get("Table", []):
                TotalEq = round(item.get("TotalEq", 0)) if item.get("TotalEq") is not None else 0
                TotalUW = round(item.get("TotalUW", 0)) if item.get("TotalUW") is not None else 0
                TotalUA = round(item.get("TotalUA", 0)) if item.get("TotalUA") is not None else 0
                TotalBreakdown = round(item.get("TotalBreakdown", 0)) if item.get("TotalBreakdown") is not None else 0
                TotalBreakdownAmount =round(item.get("TotalBreakdownAmount", 0)) if item.get("TotalBreakdownAmount") is not None else 0
                TotalMaint = round(item.get("TotalMaint", 0)) if item.get("TotalMaint") is not None else 0
                TotalMaintPending =round(item.get("TotalMaintPending", 0)) if item.get("TotalMaintPending") is not None else 0
         
                totalMaintaceBreakdownData.append({
                    "TotalEq": TotalEq,
                    "TotalUW": TotalUW,
                    "TotalUA":TotalUA,
                    "TotalBreakdown": TotalBreakdown,
                    "TotalBreakdownAmount": TotalBreakdownAmount,
                    "TotalMaint":TotalMaint,
                    "TotalMaintPending": TotalMaintPending,   
                })
           
            maintancData = []

            maintenanceBreakdownData = {}
            if "Table1" in data:
                for item in data.get("Table1", []):
                    Day = item.get("Day")
                    Total_maintance = round(item.get("Total", 0)) if item.get("Total") is not None else 0

                    
                    maintenanceBreakdownData[Day] = {
                        "Day": Day,
                        "Total_maintance": Total_maintance,
                        "Total_maintance_complete": 0,  
                        "breakdown_count": 0,           
                        "breakdown_repaired": 0         
                    }

            if "Table2" in data:
                for item in data.get("Table2", []):
                    Day = item.get("Day")
                    Total_maintance_complete = round(item.get("Total", 0)) if item.get("Total") is not None else 0

                    if Day in maintenanceBreakdownData:
                        maintenanceBreakdownData[Day]["Total_maintance_complete"] = Total_maintance_complete

            
            if "Table3" in data:
                for item in data.get("Table3", []):
                    Day = item.get("Day")
                    breakdown_count = round(item.get("Total", 0)) if item.get("Total") is not None else 0

                    if Day in maintenanceBreakdownData:
                        maintenanceBreakdownData[Day]["breakdown_count"] = breakdown_count

            
            if "Table4" in data:
                for item in data.get("Table4", []):
                    Day = item.get("Day")
                    breakdown_repaired = round(item.get("Total", 0)) if item.get("Total") is not None else 0

                    if Day in maintenanceBreakdownData:
                        maintenanceBreakdownData[Day]["breakdown_repaired"] = breakdown_repaired

        
            maintancData = list(maintenanceBreakdownData.values())
            response_data = {
                'totalMaintaceBreakdownData': totalMaintaceBreakdownData,
                'maintenanceBreakdownData': maintancData,
        
             }
            return JsonResponse(response_data)   
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)




def CEOEngineeringTotalEquipmentDetailsData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOEngineeringTotalEquipmentDetailsData?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TotalEquipmentDetailsData = []
            for item in data:
                hotel_name = item.get("HTL", 0)
                Descriptions = item.get("Descriptions")
                Area = item.get("Area")
                Department = item.get("Department")
                WarrantyEndDate =item.get("WarrantyEndDate")
                Status = item.get("Status")
                AMCEndDate =item.get("AMCEndDate")
                AStatus =item.get("AStatus")

                TotalEquipmentDetailsData.append({
                    "Hotel": hotel_name,
                    "Descriptions":Descriptions,
                    "Area": Area,
                    "Department": Department,
                    "WarrantyEndDate":WarrantyEndDate,
                    "Status": Status,
                    "AMCEndDate": AMCEndDate,
                    "AStatus": AStatus,    
                })
            return JsonResponse({"Table": TotalEquipmentDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def GMEngineeringTotalEquipmentDetailsData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMEngineeringTotalEquipmentDetailsData?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TotalEquipmentDetailsData = []
            for item in data:
                
                Descriptions = item.get("Descriptions")
                Area = item.get("Area")
                Department = item.get("Department")
                WarrantyEndDate =item.get("WarrantyEndDate")
                Status = item.get("Status")
                AMCEndDate =item.get("AMCEndDate")
                AStatus =item.get("AStatus")

                TotalEquipmentDetailsData.append({
                    "Descriptions":Descriptions,
                    "Area": Area,
                    "Department": Department,
                    "WarrantyEndDate":WarrantyEndDate,
                    "Status": Status,
                    "AMCEndDate": AMCEndDate,
                    "AStatus": AStatus,    
                })
            return JsonResponse({"Table": TotalEquipmentDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def CEOEngineeringTotalUWEquipmentDetailsData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOEngineeringTotalUWEquipmentDetailsData?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TotalEquipmentDetailsData = []
            for item in data:
                hotel_name = item.get("HTL", 0)
                Descriptions = item.get("Descriptions")
                Area = item.get("Area")
                Department = item.get("Department")
                WarrantyEndDate =item.get("WarrantyEndDate")
                Status = item.get("Status")
                AMCEndDate =item.get("AMCEndDate")
                AStatus =item.get("AStatus")
                
                
                TotalEquipmentDetailsData.append({
                    "Hotel": hotel_name,
                    "Descriptions":Descriptions,
                    "Area": Area,
                    "Department": Department,
                    "WarrantyEndDate":WarrantyEndDate,
                    "Status": Status,
                     "AMCEndDate": AMCEndDate,
                      "AStatus": AStatus,
                    
                })
            
            return JsonResponse({"Table": TotalEquipmentDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def GMEngineeringTotalUWEquipmentDetailsData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMEngineeringTotalUWEquipmentDetailsData?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TotalEquipmentDetailsData = []
            for item in data:
                Descriptions = item.get("Descriptions")
                Area = item.get("Area")
                Department = item.get("Department")
                WarrantyEndDate =item.get("WarrantyEndDate")
                Status = item.get("Status")
                AMCEndDate =item.get("AMCEndDate")
                AStatus =item.get("AStatus")
                
                
                TotalEquipmentDetailsData.append({
                    "Descriptions":Descriptions,
                    "Area": Area,
                    "Department": Department,
                    "WarrantyEndDate":WarrantyEndDate,
                    "Status": Status,
                     "AMCEndDate": AMCEndDate,
                      "AStatus": AStatus,
                    
                })
            
            return JsonResponse({"Table": TotalEquipmentDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def CEOEngineeringTotalUAEquipmentDetailsData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOEngineeringTotalUAEquipmentDetailsData?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TotalEquipmentDetailsData = []
            for item in data:
                hotel_name = item.get("HTL", 0)
                Descriptions = item.get("Descriptions")
                Area = item.get("Area")
                Department = item.get("Department")
                WarrantyEndDate =item.get("WarrantyEndDate")
                Status = item.get("Status")
                AMCEndDate =item.get("AMCEndDate")
                AStatus =item.get("AStatus")
                
                
                TotalEquipmentDetailsData.append({
                    "Hotel": hotel_name,
                    "Descriptions":Descriptions,
                    "Area": Area,
                    "Department": Department,
                    "WarrantyEndDate":WarrantyEndDate,
                    "Status": Status,
                     "AMCEndDate": AMCEndDate,
                      "AStatus": AStatus,  
                })
            
            return JsonResponse({"Table": TotalEquipmentDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMEngineeringTotalUAEquipmentDetailsData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMEngineeringTotalUAEquipmentDetailsData?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TotalEquipmentDetailsData = []
            for item in data:
                Descriptions = item.get("Descriptions")
                Area = item.get("Area")
                Department = item.get("Department")
                WarrantyEndDate =item.get("WarrantyEndDate")
                Status = item.get("Status")
                AMCEndDate =item.get("AMCEndDate")
                AStatus =item.get("AStatus")
                
                
                TotalEquipmentDetailsData.append({
                    "Descriptions":Descriptions,
                    "Area": Area,
                    "Department": Department,
                    "WarrantyEndDate":WarrantyEndDate,
                    "Status": Status,
                     "AMCEndDate": AMCEndDate,
                      "AStatus": AStatus,  
                })
            
            return JsonResponse({"Table": TotalEquipmentDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)




def CEOEngineeringTotalBreakdownDetailsData(request):
    RT = request.GET.get('RT', None)
    OrganizationID=request.GET.get('OrganizationID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    if OrganizationID:
        url=f"{main_url}CEOEngineeringTotalBreakdownDetailsData?RT={RT}&O={OrganizationID}"

    else:
        url=f"{main_url}CEOEngineeringTotalBreakdownDetailsData?RT={RT}"
    
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TotalEquipmentDetailsData = []
            for item in data:
                hotel_name = item.get("HTL", 0)
                Descriptions = item.get("Descriptions")
                Area = item.get("Area")
                Department = item.get("Department")
                WarrantyEndDate =item.get("WarrantyEndDate")
                Status = item.get("Status")
                AMCEndDate =item.get("AMCEndDate")
                AStatus =item.get("AStatus")
                BreakdownDate =item.get("BreakdownDate")
                MStatus = item.get("MStatus")
                BreakdownReason =item.get("BreakdownReason")
                Amount =item.get("Amount")
                
                
                TotalEquipmentDetailsData.append({
                    "Hotel": hotel_name,
                    "Descriptions":Descriptions,
                    "Area": Area,
                    "Department": Department,
                    "WarrantyEndDate":WarrantyEndDate,
                    "Status": Status,
                    "AMCEndDate": AMCEndDate,
                    "AStatus": AStatus,
                    "BreakdownDate":BreakdownDate,
                    "MStatus": MStatus,
                    "BreakdownReason": BreakdownReason,
                    "Amount": Amount,  
                })
            
            return JsonResponse({"Table": TotalEquipmentDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMEngineeringTotalBreakdownDetailsData(request):
    RT = request.GET.get('RT', None)
    Day=request.GET.get('Day', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    if Day:
        
        url=f"{main_url}GMEngineeringTotalBreakdownDetailsData?RT={RT}&Day={Day}"
        
    else:
       
        url=f"{main_url}GMEngineeringTotalBreakdownDetailsData?RT={RT}"
    
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
           
            
            TotalEquipmentDetailsData = []
            for item in data:
                Descriptions = item.get("Descriptions")
                Area = item.get("Area")
                Department = item.get("Department")
                WarrantyEndDate =item.get("WarrantyEndDate")
                Status = item.get("Status")
                AMCEndDate =item.get("AMCEndDate")
                AStatus =item.get("AStatus")
                BreakdownDate =item.get("BreakdownDate")
                MStatus = item.get("MStatus")
                BreakdownReason =item.get("BreakdownReason")
                Amount =item.get("Amount")
                
                
                TotalEquipmentDetailsData.append({
                    "Descriptions":Descriptions,
                    "Area": Area,
                    "Department": Department,
                    "WarrantyEndDate":WarrantyEndDate,
                    "Status": Status,
                    "AMCEndDate": AMCEndDate,
                    "AStatus": AStatus,
                    "BreakdownDate":BreakdownDate,
                    "MStatus": MStatus,
                    "BreakdownReason": BreakdownReason,
                    "Amount": Amount,  
                })
           
            
            return JsonResponse({"Table": TotalEquipmentDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def CEOEngineeringTotalMaintenanceDetailsData(request):
    RT = request.GET.get('RT', None)
    OrganizationID=request.GET.get('OrganizationID', None)

    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOEngineeringTotalMaintenanceDetailsData?RT={RT}&O={OrganizationID}"
    
    if OrganizationID:
        url=f"{main_url}CEOEngineeringTotalMaintenanceDetailsData?RT={RT}&O={OrganizationID}"  
    else:
        url=f"{main_url}CEOEngineeringTotalMaintenanceDetailsData?RT={RT}"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TotalEquipmentDetailsData = []
            for item in data:
                
                hotel_name = item.get("HTL", 0)
                Descriptions = item.get("Descriptions")
                Area = item.get("Area")
                Department = item.get("Department")
                WarrantyEndDate =item.get("WarrantyEndDate")
                Status = item.get("Status")
                AMCEndDate =item.get("AMCEndDate")
                AStatus =item.get("AStatus")
                MaintenanceDate =item.get("MaintenanceDate")
                MStatus = item.get("MStatus")
               
                
                TotalEquipmentDetailsData.append({
                    "Hotel": hotel_name,
                    "Descriptions":Descriptions,
                    "Area": Area,
                    "Department": Department,
                    "WarrantyEndDate":WarrantyEndDate,
                    "Status": Status,
                    "AMCEndDate": AMCEndDate,
                    "AStatus": AStatus,
                    "MaintenanceDate":MaintenanceDate,
                    "MStatus": MStatus,
                    
                })
            
            return JsonResponse({"Table": TotalEquipmentDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMEngineeringTotalMaintenanceDetailsData(request):
    RT = request.GET.get('RT', None)
    Day=request.GET.get('Day', None)

    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    
    
    if Day:
        url=f"{main_url}GMEngineeringTotalMaintenanceDetailsData?RT={RT}&Day={Day}"  
    else:
        url=f"{main_url}GMEngineeringTotalMaintenanceDetailsData?RT={RT}"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TotalEquipmentDetailsData = []
            for item in data:
                Descriptions = item.get("Descriptions")
                Area = item.get("Area")
                Department = item.get("Department")
                WarrantyEndDate =item.get("WarrantyEndDate")
                Status = item.get("Status")
                AMCEndDate =item.get("AMCEndDate")
                AStatus =item.get("AStatus")
                MaintenanceDate =item.get("MaintenanceDate")
                MStatus = item.get("MStatus")
               
                
                TotalEquipmentDetailsData.append({
                    "Descriptions":Descriptions,
                    "Area": Area,
                    "Department": Department,
                    "WarrantyEndDate":WarrantyEndDate,
                    "Status": Status,
                    "AMCEndDate": AMCEndDate,
                    "AStatus": AStatus,
                    "MaintenanceDate":MaintenanceDate,
                    "MStatus": MStatus,
                    
                })
            
            return JsonResponse({"Table": TotalEquipmentDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)




def CEOEngineeringTotalPendingMaintenanceDetailsData(request):
    RT = request.GET.get('RT', None)
    OrganizationID=request.GET.get('OrganizationID', None)

    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOEngineeringTotalPendingMaintenanceDetailsData?RT={RT}&O={OrganizationID}&DAY=1"
    
    if OrganizationID:
        url=f"{main_url}CEOEngineeringTotalPendingMaintenanceDetailsData?RT={RT}&O={OrganizationID}&DAY=1"   
    else:
        url=f"{main_url}CEOEngineeringTotalPendingMaintenanceDetailsData?RT={RT}&DAY=1"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TotalEquipmentDetailsData = []
            for item in data:
                hotel_name = item.get("HTL", 0)
                Descriptions = item.get("Descriptions")
                Area = item.get("Area")
                Department = item.get("Department")
                WarrantyEndDate =item.get("WarrantyEndDate")
                Status = item.get("Status")
                AMCEndDate =item.get("AMCEndDate")
                AStatus =item.get("AStatus")
                MaintenanceDate =item.get("MaintenanceDate")
                MStatus = item.get("MStatus")
               
                TotalEquipmentDetailsData.append({
                    "Hotel": hotel_name,
                    "Descriptions":Descriptions,
                    "Area": Area,
                    "Department": Department,
                    "WarrantyEndDate":WarrantyEndDate,
                    "Status": Status,
                    "AMCEndDate": AMCEndDate,
                    "AStatus": AStatus,
                    "MaintenanceDate":MaintenanceDate,
                    "MStatus": MStatus,
                    
                })
            
            return JsonResponse({"Table": TotalEquipmentDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMEngineeringTotalPendingMaintenanceDetailsData(request):
    RT = request.GET.get('RT', None)
    Day=request.GET.get('Day', None)

    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    
    if Day:
        url=f"{main_url}GMEngineeringTotalPendingMaintenanceDetailsData?RT={RT}&Day={Day}"   
    else:
        url=f"{main_url}GMEngineeringTotalPendingMaintenanceDetailsData?RT={RT}&DAY=1"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TotalEquipmentDetailsData = []
            for item in data:
                Descriptions = item.get("Descriptions")
                Area = item.get("Area")
                Department = item.get("Department")
                WarrantyEndDate =item.get("WarrantyEndDate")
                Status = item.get("Status")
                AMCEndDate =item.get("AMCEndDate")
                AStatus =item.get("AStatus")
                MaintenanceDate =item.get("MaintenanceDate")
                MStatus = item.get("MStatus")
               
                TotalEquipmentDetailsData.append({
                    "Descriptions":Descriptions,
                    "Area": Area,
                    "Department": Department,
                    "WarrantyEndDate":WarrantyEndDate,
                    "Status": Status,
                    "AMCEndDate": AMCEndDate,
                    "AStatus": AStatus,
                    "MaintenanceDate":MaintenanceDate,
                    "MStatus": MStatus,
                    
                })
            
            return JsonResponse({"Table": TotalEquipmentDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def GlitchDetails(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}GlitchDetails?RT={RT}"
    if RT:
        url=f"{main_url}GlitchDetails?RT={RT}"
    else:
        url=f"{main_url}GlitchDetails"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            GlitchData = []
            for item in data:
                ID = item.get("ID", 0)
                OID = item.get("OrganizationID", 0)
                hotel_name = item.get("Hotel")
                GuestName = item.get("GuestName")
                CompanyName = item.get("CompanyName")
                Complaint =item.get("Complaint")
                ServiceRecovery = item.get("ServiceRecovery")
                ProcessLapse =item.get("ProcessLapse")
                ProcessLapseCategory =item.get("ProcessLapseCategory")
                GMComment =item.get("GMComment")
                CreatedOn =item.get("CreatedOn")
                Status =item.get("Status")
                
                GlitchData.append({
                    "ID": ID,
                    'OID':OID,
                    "Hotel": hotel_name,
                    "GuestName":GuestName,
                    "CompanyName": CompanyName,
                    "Complaint": Complaint,
                    "ServiceRecovery":ServiceRecovery,
                    "ProcessLapse": ProcessLapse,
                    "ProcessLapseCategory": ProcessLapseCategory,
                    "GMComment": GMComment,
                    "CreatedOn": CreatedOn,
                    "Status": Status,
                    
                })
            
            return JsonResponse({"GlitchData": GlitchData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMGlitchDetails(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMGlitchDetails?RT={RT}"
    if RT:
        url=f"{main_url}GMGlitchDetails?RT={RT}"
    else:
        url=f"{main_url}GMGlitchDetails"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            GlitchData = []
            for item in data:
                ID = item.get("ID", 0)
                OID = item.get("OrganizationID", 0)
                hotel_name = item.get("Hotel")
                GuestName = item.get("GuestName")
                CompanyName = item.get("CompanyName")
                Complaint =item.get("Complaint")
                ServiceRecovery = item.get("ServiceRecovery")
                ProcessLapse =item.get("ProcessLapse")
                ProcessLapseCategory =item.get("ProcessLapseCategory")
                GMComment =item.get("GMComment")
                CreatedOn =item.get("createdDate")
                Status =item.get("Status")
                
                GlitchData.append({
                    "ID": ID,
                    "OID": OID,
                    "Hotel": hotel_name,
                    "GuestName":GuestName,
                    "CompanyName": CompanyName,
                    "Complaint": Complaint,
                    "ServiceRecovery":ServiceRecovery,
                    "ProcessLapse": ProcessLapse,
                    "ProcessLapseCategory": ProcessLapseCategory,
                    "GMComment": GMComment,
                    "CreatedOn": CreatedOn,
                    "Status": Status,
                    
                })
            
            return JsonResponse({"GlitchData": GlitchData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def IncidentDetails(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    
    if RT:
        url=f"{main_url}IncidentDetails?RT={RT}"
    else:
        url=f"{main_url}IncidentDetails"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            IncidentData = []
            for item in data:
                ID = item.get("ID")
                hotel_name = item.get("Hotel")
                Location =item.get("Location")
                IncidentDate = item.get("IncidentDate")
                Description = item.get("Description")
                AccidentCause = item.get("AccidentCause")
                Anycasualty =item.get("Anycasualty")
                Damagedcaused =item.get("Damagedcaused")
                Investigation =item.get("Investigation")
                
                IncidentData.append({
                    "ID": ID,
                    "Hotel": hotel_name,
                    "Location":Location,
                    "IncidentDate": IncidentDate,
                    "Description": Description,
                    "AccidentCause":AccidentCause,
                    "Anycasualty": Anycasualty,
                    "Damagedcaused": Damagedcaused,
                    "Investigation": Investigation,
                   
                })
            
            return JsonResponse({"IncidentData": IncidentData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMIncidentDetails(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    
    if RT:
        url=f"{main_url}GMIncidentDetails?RT={RT}"
    else:
        url=f"{main_url}GMIncidentDetails"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            IncidentData = []
            for item in data:
                ID = item.get("ID")
                hotel_name = item.get("Hotel")
                Location =item.get("Location")
                IncidentDate = item.get("IncidentDate")
                Description = item.get("Description")
                AccidentCause = item.get("AccidentCause")
                Anycasualty =item.get("Anycasualty")
                Damagedcaused =item.get("Damagedcaused")
                Investigation =item.get("Investigation")
                
                IncidentData.append({
                    "ID": ID,
                    "Hotel": hotel_name,
                    "Location":Location,
                    "IncidentDate": IncidentDate,
                    "Description": Description,
                    "AccidentCause":AccidentCause,
                    "Anycasualty": Anycasualty,
                    "Damagedcaused": Damagedcaused,
                    "Investigation": Investigation,
                   
                })
            
            return JsonResponse({"IncidentData": IncidentData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)




def occupancy_chart_data(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
        OrganizationID = request.session["OrganizationID"]
    if OrganizationID == "3":
        organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1)
    else:
        organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1, OrganizationID=OrganizationID)

    organization_choices = [(org.OrganizationID, org.ShortDisplayLabel) for org in organizations]

    axis_data = [org[1] for org in organization_choices]  
    occupancy = []
    
    for org in organization_choices:
        OrganizationID = org[0] 
        try:
            
            org_data = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first() 
            
            if org_data:
                occupancy.append(int(round(org_data.occupancy, 1)))
            else:
                occupancy.append(0)
        
        except Exception as e:
            occupancy.append(0)
    

    return JsonResponse({
        'axis_data': axis_data,
        'occupancy': occupancy,
    })

def CEOOutOfOrderData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    
    if RT:
        url=f"{main_url}CEOOutOfOrderData?RT={RT}"
    else:
        url=f"{main_url}CEOOutOfOrderData"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            OutOfOrderData = []
            for item in data:
                hotel_name = item.get("HTL")
                Total = round(item.get("Total", 0)) if item.get("Total") is not None else 0
                OrganizationID =item.get("OrganizationID")

                OutOfOrderData.append({
                    "Hotel": hotel_name,
                    "Total": Total,
                    "OrganizationID":OrganizationID,
                })
            
            return JsonResponse({"Table": OutOfOrderData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def CEOOutOfOrderDetails(request):
    RT = request.GET.get('RT', None)
    OID= request.GET.get('OrganizationID',None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOOutOfOrderDetails?OID={OID}&RT={RT}"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
           
            
            OutOfOrderDetailsData = []
            for item in data:
                ROMNUB = item.get("ROMNUB")
                FRMDAT = item.get("FRMDAT")
                TOODAT =item.get("TOODAT")
                DESCRP = item.get("DESCRP")
                
                OutOfOrderDetailsData.append({
                    "ROMNUB": ROMNUB,
                    "FRMDAT": FRMDAT,
                    "TOODAT":TOODAT,
                    "DESCRP":DESCRP,
                })
            
            return JsonResponse({"OutOfOrderDetailsData": OutOfOrderDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def GMOutOfOrderData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    headers = Config.TOKEN_HEADERS
    
    if RT:
        url=f"{main_url}CEOOutOfOrderData?RT={RT}"
    else:
        url=f"{main_url}CEOOutOfOrderData"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            
            OutOfOrderData = []
            for item in data:
                hotel_name = item.get("HTL")
                Total = round(item.get("Total", 0)) if item.get("Total") is not None else 0
                OrganizationID =item.get("OrganizationID")

                OutOfOrderData.append({
                    "Hotel": hotel_name,
                    "Total": Total,
                    "OrganizationID":OrganizationID,
                })
            
            return JsonResponse({"Table": OutOfOrderData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def RDRoomsSRMSChart(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}RDRoomsSRMSChart?RT={RT}"    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            srmsChart_data = []
            for item in data.get("Table", []):
                hotel_name = item.get("Hotel")
                Total = round(item.get("Total", 0)) if item.get("Total") is not None else 0
                DetailsJson =item.get("DetailsJson")
                
                srmsChart_data.append({
                    "Hotel": hotel_name,
                    "Total": Total,
                    "DetailsJson":DetailsJson,
                })
            
            return JsonResponse({"Table": srmsChart_data})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMRoomsSRMSChart(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMRoomsSRMSChart?RT={RT}"    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            srmsChart_data = []
            for item in data.get("Table", []):
                Department = item.get("Department")
                Total = round(item.get("Total", 0)) if item.get("Total") is not None else 0
                DetailsJson =item.get("DetailsJson")
                
                srmsChart_data.append({
                    "Department": Department,
                    "Total": Total,
                    "DetailsJson":DetailsJson,
                })
            
            return JsonResponse({"Table": srmsChart_data})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def RDGuestMetChartData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}RDGuestMetChartData?RT={RT}"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            guest_data = []
            for item in data.get("Table", []):
                hotel_name = item.get("Hotel")
                OrganizationID= item.get("OrganizationID")

                Total = round(item.get("Total", 0)) if item.get("Total") is not None else 0
                TotalArrival = round(item.get("TotalArrival", 0)) if item.get("TotalArrival") is not None else 0
                TotalDeparture = round(item.get("TotalDeparture", 0)) if item.get("TotalDeparture") is not None else 0
                TotalInHouse = round(item.get("TotalInHouse", 0)) if item.get("TotalInHouse") is not None else 0
                
                guest_data.append({
                    "Hotel": hotel_name,
                    "OrganizationID" :OrganizationID,
                    "Total": Total,
                    "TotalArrival":TotalArrival,
                    "TotalDeparture":TotalDeparture,
                    "TotalInHouse":TotalInHouse


                })
            
            return JsonResponse({"Table": guest_data})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def RDGuestMetChartDataDetails(request):
    RT = request.GET.get('RT', None)
    MetOn=request.GET.get('MetOn', None)
    OID=request.GET.get('OrganizationID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}RDGuestMetChartDataDetails?OID={OID}&MetOn={MetOn}&RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            guestChartDetailsData = []
            for item in data:
                GuestName = item.get("GuestName")
                Arrival= item.get("Arrival")
                RoomNo = item.get("RoomNo")
                Departure= item.get("Departure")
                Feedback = item.get("Feedback")
                Actiontaken= item.get("Actiontaken")
                FeedbackType = item.get("FeedbackType")
                MetBy= item.get("MetBy")
                MetOn = item.get("MetOn")
                UpdateOn= item.get("UpdateOn")
                Updatedby = item.get("Updatedby")
                    
                guestChartDetailsData.append({
                    "GuestName": GuestName,
                    "Arrival" :Arrival,
                    "RoomNo": RoomNo,
                    "Departure":Departure,
                    "Feedback":Feedback,
                    "Actiontaken":Actiontaken,
                    "FeedbackType":FeedbackType,
                    "MetBy":MetBy,
                    "MetOn":MetOn,
                    "Updatedby":Updatedby,
                    "UpdateOn":UpdateOn,
                 
             })
            
            return JsonResponse({"Table": guestChartDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMGuestMetChartDataDetails(request):
    RT = request.GET.get('RT', None)
    MetOn=request.GET.get('MetOn', None)
    OID=request.GET.get('OrganizationID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMGuestMetChartDataDetails?OID={OID}&MetOn={MetOn}&RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            guestChartDetailsData = []
            for item in data:
                GuestName = item.get("GuestName")
                Arrival= item.get("Arrival")
                RoomNo = item.get("RoomNo")
                Departure= item.get("Departure")
                Feedback = item.get("Feedback")
                Actiontaken= item.get("Actiontaken")
                FeedbackType = item.get("FeedbackType")
                MetBy= item.get("MetBy")
                MetOn = item.get("MetOn")
                UpdateOn= item.get("UpdateOn")
                Updatedby = item.get("Updatedby")
                    
                guestChartDetailsData.append({
                    "GuestName": GuestName,
                    "Arrival" :Arrival,
                    "RoomNo": RoomNo,
                    "Departure":Departure,
                    "Feedback":Feedback,
                    "Actiontaken":Actiontaken,
                    "FeedbackType":FeedbackType,
                    "MetBy":MetBy,
                    "MetOn":MetOn,
                    "Updatedby":Updatedby,
                    "UpdateOn":UpdateOn,
                 
             })
            
            return JsonResponse({"Table": guestChartDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def GMGuestMetChartData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMGuestMetChartData?RT={RT}"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            guest_data = []
            for item in data.get("Table", []):
                hotel_name = item.get("Hotel")
                OrganizationID= item.get("OrganizationID")

                Total = round(item.get("Total", 0)) if item.get("Total") is not None else 0
                TotalArrival = round(item.get("TotalArrival", 0)) if item.get("TotalArrival") is not None else 0
                TotalDeparture = round(item.get("TotalDeparture", 0)) if item.get("TotalDeparture") is not None else 0
                TotalInHouse = round(item.get("TotalInHouse", 0)) if item.get("TotalInHouse") is not None else 0
                
                guest_data.append({
                    "Hotel": hotel_name,
                    "OrganizationID" :OrganizationID,
                    "Total": Total,
                    "TotalArrival":TotalArrival,
                    "TotalDeparture":TotalDeparture,
                    "TotalInHouse":TotalInHouse


                })
            
            return JsonResponse({"Table": guest_data})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)




def GMArCollection(request):
    RT = request.GET.get('RT', None)
    OID=request.GET.get('OrganizationID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}GMArCollection?OID={OID}&RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            GMArCollectionData = []
            for item in data:
                Account = item.get("Account")
                Day91= item.get("Day91")
                TotalPending = item.get("TotalPending")
                LastupdateDate= item.get("LastupdateDate")
                
                    
                GMArCollectionData.append({
                    "Account": Account,
                    "Day91" :Day91,
                    "TotalPending":TotalPending,
                    "LastupdateDate":LastupdateDate,
                 
             })
            
            return JsonResponse({"Table": GMArCollectionData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMArCollectiondata(request):

    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMArCollection"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            GMArCollectionData = []
            for item in data:
                Account = item.get("Account")
                Day91= item.get("Day91")
                TotalPending = item.get("TotalPending")
                LastupdateDate= item.get("LastupdateDate")
                
                    
                GMArCollectionData.append({
                    "Account": Account,
                    "Day91" :Day91,
                    "TotalPending":TotalPending,
                    "LastupdateDate":LastupdateDate,
                 
             })
            
            return JsonResponse({"Table": GMArCollectionData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def CEOHLPReportChartData(request):
    RD = request.GET.get('RD', None)
   
    OID=request.GET.get('OID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOHLPReportChartData?RD={RD}&OID={OID}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            HlpReportData = []
            for item in data.get("Table", []):
                Title = item.get("Title")
                YOD= item.get("YOD")
                LYOD = item.get("LYOD")
   
                HlpReportData.append({
                    "Title": Title,
                    "YOD" :YOD,
                    "LYOD":LYOD,
                 
             })

            return JsonResponse({"Table": HlpReportData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def GMHLPReportChartData(request):
    RD = request.GET.get('RD', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMHLPReportChartData?RD={RD}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            HlpReportData = []
            for item in data.get("Table", []):
                Title = item.get("Title")
                YOD= item.get("YOD")
                LYOD = item.get("LYOD")
   
                HlpReportData.append({
                    "Title": Title,
                    "YOD" :YOD,
                    "LYOD":LYOD,
                 
             })

            return JsonResponse({"Table": HlpReportData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def GMPayMaster(request):
    RT = request.GET.get('RT', None)
    OID=request.GET.get('OrganizationID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}GMPayMaster?OID={OID}&RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            GMPayMasterData = []
            for item in data:
                ROOM = item.get("ROOM")
                FULL_NAME= item.get("FULL_NAME")
                COMPANY_NAME = item.get("COMPANY_NAME")
                BALANCE = item.get("BALANCE")
                ARRIVAL= item.get("ARRIVAL")
                DEPARTURE = item.get("DEPARTURE")
                LastupdateDate= item.get("LastupdateDate")
                 
                GMPayMasterData.append({
                    "ROOM": ROOM,
                    "FULL_NAME" :FULL_NAME,
                    "COMPANY_NAME":COMPANY_NAME,
                    "BALANCE":BALANCE,
                    "ARRIVAL" :ARRIVAL,
                    "DEPARTURE":DEPARTURE,
                    "LastupdateDate":LastupdateDate,   
             })
            
            return JsonResponse({"Table": GMPayMasterData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMPayMasterData(request):

    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMPayMaster"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            GMPayMasterData = []
            for item in data:
                ROOM = item.get("ROOM")
                FULL_NAME= item.get("FULL_NAME")
                COMPANY_NAME = item.get("COMPANY_NAME")
                BALANCE = item.get("BALANCE")
                ARRIVAL= item.get("ARRIVAL")
                DEPARTURE = item.get("DEPARTURE")
                LastupdateDate= item.get("LastupdateDate")
                 
                GMPayMasterData.append({
                    "ROOM": ROOM,
                    "FULL_NAME" :FULL_NAME,
                    "COMPANY_NAME":COMPANY_NAME,
                    "BALANCE":BALANCE,
                    "ARRIVAL" :ARRIVAL,
                    "DEPARTURE":DEPARTURE,
                    "LastupdateDate":LastupdateDate,   
             })
            
            return JsonResponse({"Table": GMPayMasterData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def CEODashboardMasterData(request):

    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}CEODashboardMasterData"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()

            return JsonResponse(data)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def MOMList(request):

    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}MOMList"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
                    
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def RDGatepass(request):
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}RDGatepass"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
                    
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def RDCompRoom(request):
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}CEODashboardMasterData"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
                    
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def RDChecklistChartData(request):
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}RDChecklistChartData"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
                    
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def RDCapex(request):
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}RDCapex"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
                    
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def RDLeaveApplication(request):
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}RDLeaveApplication"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
                    
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def RDOpenPosition(request):
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}RDOpenPosition"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
                    
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def RDInterviewAssessment(request):
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}RDInterviewAssessment"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
                    
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def RDEmpResignation(request):
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}RDEmpResignation"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
                    
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def RDExitInterview(request):
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}RDExitInterview"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
                    
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def RDPADPList(request):
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}RDPADPList"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
                    
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def CEO_ManningGuide(request):
    Level = request.GET.get('level', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}CEO_ManningGuide?OID=3&Level={Level}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
                    
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def CEO_ManningGuideDetails(request):
    Level = request.GET.get('level', None)
    OrganizationID = request.GET.get('OrganizationID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}CEO_ManningGuideDetails?OID={OrganizationID}&Level={Level}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
                    
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def RDCheckListDetailsChart(request):
    RT = request.GET.get('RT', None)
    OID=request.GET.get('OrganizationID')
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}RDCheckListDetailsChart?OID={OID}&RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()     
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def UserList(request):
    RT = request.GET.get('RT', None)
    OID=request.GET.get('O')
    
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"https://hotelops.in/API/UserAPI/UserList?OrganizationID={OID}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()     
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def discardsChartData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}CEODashboardDiscardsChartData?RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()     
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def LostAndFoundChart(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}CEODashboardLostAndFoundChartData?RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()     
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
def LostAndFoundChartDataDetails(request):
    RT = request.GET.get('RT', None)
    OID=request.GET.get('OrganizationID')
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}CEODashboardLostAndFoundChartDataDetails?RT={RT}&OID={OID}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()     
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def DiscardsDetailsChartData(request):
    RT = request.GET.get('RT', None)
    OID=request.GET.get('OrganizationID')

    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}CEODashboardDiscardsDetailsChartData?RT={RT}&OID={OID}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()     
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)




def FollowUps(request):
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}FollowUps"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
                    
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)




def GMPayGMGatepass_OverdueData(request):

    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMGatepass_OverdueChartDataSelect"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            gatepass_OverdueData = []
            for item in data:
                RGPNO = item.get("RGPNO")
                ItemName= item.get("ItemName")
                Quantity = item.get("Quantity")
                VendorName = item.get("VendorName")
                Company= item.get("Company")
                Out_Date = item.get("Out_Date")
                ExpReturnDate= item.get("ExpReturnDate")
                Department = item.get("Department")
                TakenBy= item.get("TakenBy")
                 
                gatepass_OverdueData.append({
                    "RGPNO": RGPNO,
                    "ItemName" :ItemName,
                    "Quantity":Quantity,
                    "VendorName":VendorName,
                    "Company" :Company,
                    "Out_Date":Out_Date,
                    "ExpReturnDate":ExpReturnDate,   
                    "Department":Department,
                    "TakenBy":TakenBy,   
             })
            
            return JsonResponse({"Table": gatepass_OverdueData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)




def TrainingHoursDetails(request):
    RT = request.GET.get('RT', None)
    OID=request.GET.get('OrganizationID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOTrainingHoursDetails?OID={OID}&RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            trainingHourData = []
            for item in data:
                Topic = item.get("Topic")
                Department= item.get("Department")
                NoOfMember = item.get("NoOfMember")
                TrainingDate = item.get("TrainingDate")
                StartTime= item.get("StartTime")
                EndTime = item.get("EndTime")
                
                 
                trainingHourData.append({
                    "Topic": Topic,
                    "Department" :Department,
                    "NoOfMember":NoOfMember,
                    "TrainingDate":TrainingDate,
                    "StartTime" :StartTime,
                    "EndTime":EndTime,
             })
            
            return JsonResponse({"Table": trainingHourData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMTrainingScheduleDetails(request):
    RT = request.GET.get('RT', None)
    Day = request.GET.get('Day', None)

    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMTrainingScheduleDetails?Day={Day}&RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            trainingHourData = []
            for item in data:
                Topic = item.get("Topic")
                Department= item.get("Department")
                NoOfMember = item.get("ConductedByNoofTeammembers")
                TrainingDate = item.get("Date")
                StartTime= item.get("StartTime")
                EndTime = item.get("EndTime")
                
                 
                trainingHourData.append({
                    "Topic": Topic,
                    "Department" :Department,
                    "NoOfMember":NoOfMember,
                    "TrainingDate":TrainingDate,
                    "StartTime" :StartTime,
                    "EndTime":EndTime,
             })
            
            return JsonResponse({"Table": trainingHourData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def WarningLettersDetails(request):
    RT = request.GET.get('RT', None)
    OID=request.GET.get('OrganizationID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEO_WarningLettersDetails?OID={OID}&RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            WarningLettersDetailsData = []
            for item in data:
                Name = item.get("Name")
                Designation= item.get("Designation")
                Department = item.get("Department")
                EmployeeProblems = item.get("EmployeeProblems")
                WarningType= item.get("WarningType")
                WarnOn = item.get("WarnOn")
                
                 
                WarningLettersDetailsData.append({
                    "Name": Name,
                    "Designation" :Designation,
                    "Department":Department,
                    "EmployeeProblems":EmployeeProblems,
                    "WarningType" :WarningType,
                    "WarnOn":WarnOn,
             })
            
            return JsonResponse({"Table": WarningLettersDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def DailyBreakageDetails(request):
    RT = request.GET.get('RT', None)
    OID=request.GET.get('OrganizationID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEO_DailyBreakageDetails?OID={OID}&RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            WarningLettersDetailsData = []
            for item in data:
                Item = item.get("Item")
                Nos= item.get("Nos")
                TotalCost = item.get("TotalCost")
                PersonResponsible = item.get("PersonResponsible")
                
                
                 
                WarningLettersDetailsData.append({
                    "Item": Item,
                    "Nos" :Nos,
                    "TotalCost":TotalCost,
                    "PersonResponsible":PersonResponsible,

             })
            
            return JsonResponse({"Table": WarningLettersDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def CEO_ConsumptionDetailsChartDataSelect(request):
    RT = request.GET.get('RT', None)
    OID=request.GET.get('OrganizationID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 100))  # default: 100 records

    offset = (page - 1) * page_size
    url = f"{main_url}CEO_ConsumptionDetailsChartDataSelect?OID={OID}&RT={RT}&offset={offset}&limit={page_size}"
    
    # url=f"{main_url}CEO_ConsumptionDetailsChartDataSelect?OID={OID}&RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def CEO_RestaurantFeedbackDetails(request):
    RT = request.GET.get('RT', None)
    OID=request.GET.get('OrganizationID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEO_RestaurantFeedbackDetails?OID={OID}&RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data,safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def RD_ConsumptionDetailsChartDataSelect(request):
    RT = request.GET.get('RT', None)
    OID=request.GET.get('OrganizationID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}RD_ConsumptionDetailsChartDataSelect?OID={OID}&RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def CateringSalesEventDetails(request):
    RT = request.GET.get('RT', None)
    OID=request.GET.get('OrganizationID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEO_CateringSalesEventDetails?OID={OID}&RT={RT}"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            cateringSalesEventData = []
            for item in data:
                FunctionName = item.get("FunctionName")
                CompanyName= item.get("CompanyName")
                ContactName = item.get("ContactName")
                Attending = item.get("Attending")
                ArrivalDate= item.get("ArrivalDate")
                DepartureDate = item.get("DepartureDate")
                
                 
                cateringSalesEventData.append({
                    "FunctionName": FunctionName,
                    "CompanyName" :CompanyName,
                    "ContactName":ContactName,
                    "Attending":Attending,
                    "ArrivalDate" :ArrivalDate,
                    "DepartureDate":DepartureDate,
             })
            
            return JsonResponse({"Table": cateringSalesEventData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def CEOPPMCheckListDetailsChartDataSelect(request):
    RT = request.GET.get('RT', None)
    OID=request.GET.get('OrganizationID', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOPPMCheckListDetailsChartDataSelect?OID={OID}&RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            PPMCheckListDetailsData = []
            for item in data:
                EntryID = item.get("EntryID")
                RoomNumber= item.get("RoomNumber")
                EntryDate = item.get("EntryDate")
                IsDoneEng = item.get("IsDoneEng")
                IsDoneHK= item.get("IsDoneHK")
                OrganizationID = item.get("OrganizationID")

                PPMCheckListDetailsData.append({
                    "EntryID": EntryID,
                    "RoomNumber" :RoomNumber,
                    "EntryDate":EntryDate,
                    "IsDoneEng":IsDoneEng,
                    "IsDoneHK" :IsDoneHK,
                    "OrganizationID":OrganizationID,  
                 
             })
            
            return JsonResponse({"Table": PPMCheckListDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMPPMCheckListDetailsChartDataSelect(request):
    RT = request.GET.get('RT', None)
    Day=request.GET.get('Day', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMPPMCheckListDetailsChartDataSelect?Day={Day}&RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            PPMCheckListDetailsData = []
            for item in data:
                EntryID = item.get("EntryID")
                RoomNumber= item.get("RoomNumber")
                EntryDate = item.get("EntryDate")
                IsDoneEng = item.get("IsDoneEng")
                IsDoneHK= item.get("IsDoneHK")
                OrganizationID = item.get("OrganizationID")

                PPMCheckListDetailsData.append({
                    "EntryID": EntryID,
                    "RoomNumber" :RoomNumber,
                    "EntryDate":EntryDate,
                    "IsDoneEng":IsDoneEng,
                    "IsDoneHK" :IsDoneHK,
                    "OrganizationID":OrganizationID,  
                 
             })
            
            return JsonResponse({"Table": PPMCheckListDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)




def HotelForecastOccupancyChartData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}HotelForecastOccupancyChartData?RT={RT}"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            occupancy_data = []
            for item in data.get("Table", []):
                if item.get("Hotel"):
                    hotel_name = item.get("Hotel")
                    Occupancy = item.get("Occupancy", 0)  
                    if Occupancy is not None:
                        Occupancy = round(Occupancy) 
                    
                else:
                    continue 
                
                occupancy_data.append({
                    "Hotel": hotel_name,
                    "Occupancy": Occupancy
                })
            
            return JsonResponse({"Table": occupancy_data})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def HotelForecastADRChartData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}HotelForecastADRChartData?RT={RT}"

    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            adr_data = []
            for item in data.get("Table", []):
                
                hotel_name = item.get("Hotel")
                ADR = item.get("ADR", 0)
                if ADR is not None:
                    ADR = round(ADR)      
                
                adr_data.append({
                    "Hotel": hotel_name,
                    "ADR": ADR
                })
            
            return JsonResponse({"Table": adr_data})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    

def CEOPayMasterChartData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOPayMasterChartData?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            payMasterData = []
            for item in data.get("Table", []):
                hotel_name = item.get("HTL")
                OrganizationID= item.get("OrganizationID")
                balance = item.get("BALANCE",0)
                if balance is not None:
                    balance = round(balance)

                payMasterData.append({
                    "Hotel": hotel_name,
                    "OrganizationID" :OrganizationID,
                    "balance": balance,
                    

                })
            
            return JsonResponse({"Table": payMasterData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
def CEOARCollectionChartData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOARCollectionChartData?RT={RT}"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            ArCollectionData = []
            for item in data.get("Table", []):
                hotel_name = item.get("HTL")
                OrganizationID= item.get("OrganizationID")
                balance = round(item.get("BALANCE", 0)) if item.get("BALANCE") is not None else 0

                ArCollectionData.append({
                    "Hotel": hotel_name,
                    "OrganizationID" :OrganizationID,
                    "balance": balance,   

                })
            
            return JsonResponse({"Table": ArCollectionData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def CEOORGList(request):
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOORGList"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            Organizations = []
            for item in data:
                OrganizationID= item.get("OrganizationID")
                Organization_name = item.get("Organization_name")
                  
                Organizations.append({
                    "OrganizationID" :OrganizationID,
                    "Organization_name": Organization_name
                })
            
            return JsonResponse({"Table": Organizations})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def RDRoomsPPMChart(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}RDRoomsPPMChart?RT={RT}"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            ArCollectionData = []
            for item in data.get("Table", []):
                hotel_name = item.get("Hotel")
                OrganizationID= item.get("OrganizationID")
                Total = item.get("Total")

                ArCollectionData.append({
                    "Hotel": hotel_name,
                    "OrganizationID" :OrganizationID,
                    "Total": Total
                    

                })
            
            return JsonResponse({"Table": ArCollectionData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMPPMCheckListChartDataSelect(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMPPMCheckListChartDataSelect?RT={RT}"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            ppmData = []
            for item in data:
                Day = item.get("Day")
                Total = item.get("Total")

                ppmData.append({
                    "Day": Day,
                    "Total": Total
                    

                })
            
            return JsonResponse({"Table": ppmData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMTrainingSchedule(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMTrainingSchedule?RT={RT}"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            trainingHoursData = []
            for item in data:
                Day= item.get("Day")
                Total = item.get("Total")

                trainingHoursData.append({
                    "Day": Day,
                    "Total": Total
                    

                })
            
            return JsonResponse({"Table": trainingHoursData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def CEOTrainingHours(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOTrainingHours?RT={RT}"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            trainingHoursData = []
            for item in data:
                hotel_name = item.get("Hotel")
                OrganizationID= item.get("OrganizationID")
                Total = item.get("Total")

                trainingHoursData.append({
                    "Hotel": hotel_name,
                    "OrganizationID" :OrganizationID,
                    "Total": Total
                    

                })
            
            return JsonResponse({"Table": trainingHoursData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def CEOWarningLetters(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOWarningLetters?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            warningLetterData = []
            for item in data:
                hotel_name = item.get("Hotel")
                OrganizationID= item.get("OrganizationID")
                Total = item.get("Column1")

                warningLetterData.append({
                    "Hotel": hotel_name,
                    "OrganizationID" :OrganizationID,
                    "Total": Total
                })
            
            return JsonResponse({"Table": warningLetterData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def CEOCateringSalesEvent(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEOCateringSalesEvent?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            cateringSaleData = []
            for item in data:
                hotel_name = item.get("Hotel")
                OrganizationID= item.get("OrganizationID")
                Total = item.get("Total")

                cateringSaleData.append({
                    "Hotel": hotel_name,
                    "OrganizationID" :OrganizationID,
                    "Total": Total
                    

                })
            
            return JsonResponse({"Table": cateringSaleData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def DailyBreakageData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEODailyBreakage?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            breakageData = []
            for item in data:
                hotel_name = item.get("Hotel")
                OrganizationID= item.get("OrganizationID")
                Total = item.get("TotalCost")

                breakageData.append({
                    "Hotel": hotel_name,
                    "OrganizationID" :OrganizationID,
                    "Total": Total
                    

                })
            
            return JsonResponse({"Table": breakageData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def restaurantFeedbackChartData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEORestaurantFeedback?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            breakageData = []
            for item in data:
                hotel_name = item.get("Hotel")
                OrganizationID= item.get("OrganizationID")
                Total = item.get("Total")

                breakageData.append({
                    "Hotel": hotel_name,
                    "OrganizationID" :OrganizationID,
                    "Total": Total
                    

                })
            
            return JsonResponse({"Table": breakageData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def CEODashboardConsumptionChartData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEODashboardConsumptionChartData?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            breakageData = []
            for item in data:
                hotel_name = item.get("Hotel")
                OrganizationID= item.get("OrganizationID")
                Total = item.get("Total")

                breakageData.append({
                    "Hotel": hotel_name,
                    "OrganizationID" :OrganizationID,
                    "Total": Total
                    

                })
            
            return JsonResponse({"Table": breakageData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def RDDashboardConsumptionChartData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}RDDashboardConsumptionChartData?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            breakageData = []
            for item in data:
                hotel_name = item.get("Hotel")
                OrganizationID= item.get("OrganizationID")
                Total = item.get("Total")

                breakageData.append({
                    "Hotel": hotel_name,
                    "OrganizationID" :OrganizationID,
                    "Total": Total
                    

                })
            
            return JsonResponse({"Table": breakageData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def RDRoomsSRMSTopRequestChart(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}RDRoomsSRMSTopRequestChart?RT={RT}"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TopSRMSData = []
            for item in data.get("Table", []):
                CallDescription = item.get("CallDescription")
                TotalRequest = round(item.get("TotalRequest", 0)) if item.get("TotalRequest") is not None else 0
               
                TopSRMSData.append({
                    "CallDescription": CallDescription,
                    "TotalRequest" :TotalRequest 
                })
            
            return JsonResponse({"Table": TopSRMSData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
def GMRoomsSRMSTopRequestChart(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMRoomsSRMSTopRequestChart?RT={RT}"
    
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TopSRMSData = []
            for item in data.get("Table", []):
                CallDescription = item.get("CallDescription")
                TotalRequest = round(item.get("TotalRequest", 0)) if item.get("TotalRequest") is not None else 0
               
                TopSRMSData.append({
                    "CallDescription": CallDescription,
                    "TotalRequest" :TotalRequest 
                })
            
            return JsonResponse({"Table": TopSRMSData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def RDRoomsSRMSTopRequestDetailsChart(request):
    RT = request.GET.get('RT', None)
    srmsRequest= request.GET.get('srmsRequest')
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}RDRoomsSRMSTopRequestDetailsChart?Request={srmsRequest}&RT={RT}"

    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TopSRMSRequestDetailsData = []
            for item in data.get("Table", []):
                Hotel = item.get("Hotel")
                TotalRequest = item.get("TotalRequest", 0)


                TopSRMSRequestDetailsData.append({
                    "Hotel": Hotel,
                    "TotalRequest" :TotalRequest 
                })
            
            return JsonResponse({"Table": TopSRMSRequestDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def GMRoomsSRMSTopRequestDetailsChart(request):
    RT = request.GET.get('RT', None)
    srmsRequest= request.GET.get('srmsRequest')
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMRoomsSRMSTopRequestDetailsChart?Request={srmsRequest}&RT={RT}"

    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            
            TopSRMSRequestDetailsData = []
            for item in data.get("Table", []):
                Hotel = item.get("Hotel")
                TotalRequest = item.get("TotalRequest", 0)


                TopSRMSRequestDetailsData.append({
                    "Hotel": Hotel,
                    "TotalRequest" :TotalRequest 
                })
            
            return JsonResponse({"Table": TopSRMSRequestDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def RDRoomsSRMSCompletedDurationDetailsChart(request):
    RT = request.GET.get('RT', None)
    srmsRequest= request.GET.get('srmsRequest')
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}RDRoomsSRMSCompletedDurationDetailsChart?CD={srmsRequest}&RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TopSRMSRequestDetailsData = []
            for item in data.get("Table", []):
                Hotel = item.get("Hotel")
                CallDescription = item.get("CallDescription")
                Location = item.get("Location")
                Remark = item.get("Remark", 0)
                RequestDateTime = item.get("RequestDateTime")
                RequestMode = item.get("RequestMode", 0)
                AssignedUserName = item.get("AssignedUserName", 0)
                CompleteBy = item.get("CompleteBy")
                CompleteDateTime = item.get("CompleteDateTime", 0)

                TopSRMSRequestDetailsData.append({
                    "Hotel": Hotel,
                    "CallDescription" :CallDescription ,
                    "Location": Location,
                    "Remark" :Remark, 
                    "Hotel": Hotel,
                    "RequestDateTime" :RequestDateTime ,
                    "RequestMode": RequestMode,
                    "AssignedUserName" :AssignedUserName,
                    "CompleteBy": CompleteBy,
                    "CompleteDateTime" :CompleteDateTime
                })
            
            return JsonResponse({"Table": TopSRMSRequestDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def GMRoomsSRMSCompletedDurationDetailsChart(request):
    RT = request.GET.get('RT', None)
    srmsRequest= request.GET.get('srmsRequest')
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMRoomsSRMSCompletedDurationDetailsChart?CD={srmsRequest}&RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            TopSRMSRequestDetailsData = []
            for item in data.get("Table", []):
                Hotel = item.get("Hotel")
                CallDescription = item.get("CallDescription")
                Location = item.get("Location")
                Remark = item.get("Remark", 0)
                RequestDateTime = item.get("RequestDateTime")
                RequestMode = item.get("RequestMode", 0)
                AssignedUserName = item.get("AssignedUserName", 0)
                CompleteBy = item.get("CompleteBy")
                CompleteDateTime = item.get("CompleteDateTime", 0)

                TopSRMSRequestDetailsData.append({
                    "Hotel": Hotel,
                    "CallDescription" :CallDescription ,
                    "Location": Location,
                    "Remark" :Remark, 
                    "Hotel": Hotel,
                    "RequestDateTime" :RequestDateTime ,
                    "RequestMode": RequestMode,
                    "AssignedUserName" :AssignedUserName,
                    "CompleteBy": CompleteBy,
                    "CompleteDateTime" :CompleteDateTime
                })
            
            return JsonResponse({"Table": TopSRMSRequestDetailsData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)




def totalMainataceData(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
        OrganizationID = request.session["OrganizationID"]
    if OrganizationID == "3":
        organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1)
    else:
        organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1, OrganizationID=OrganizationID)

    organization_choices = [(org.OrganizationID, org.ShortDisplayLabel) for org in organizations]

    axis_data = [org[1] for org in organization_choices]  
    total_maintanceCompleted_data = []
    total_maintance_data = []

    for org in organization_choices:
        OrganizationID = org[0] 
        try:
            
            org_data = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first() 
            
            if org_data:
                total_maintance_data.append(int(round(org_data.total_maintance, 1)))
                total_maintanceCompleted_data.append(int(round(org_data.total_maintanceCompleted, 1)))
            else:
                total_maintance_data.append(0)
                total_maintanceCompleted_data.append(0)
        
        except Exception as e:
            total_maintance_data.append(0)
            total_maintanceCompleted_data.append(0)
    
    return JsonResponse({
        'axis_data': axis_data,
        'arr_data': total_maintance_data,
        'revpar_data': total_maintanceCompleted_data,
       
    })


def RDRoomsSRMSCompletedDurationChart(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}RDRoomsSRMSCompletedDurationChart?RT={RT}"

    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            SRMSCompletionDurationData = []
            for item in data.get("Table", []):
                CompleteDuration = item.get("CompleteDurestion")
                TotalRequest = round(item.get("TotalRequest", 0)) if item.get("TotalRequest") is not None else 0
              
                SRMSCompletionDurationData.append({
                    "CompleteDuration": CompleteDuration,
                    "TotalRequest" :TotalRequest 
                })
            
            return JsonResponse({"Table": SRMSCompletionDurationData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def GMRoomsSRMSCompletedDurationChart(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMRoomsSRMSCompletedDurationChart?RT={RT}"

    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            SRMSCompletionDurationData = []
            for item in data.get("Table", []):
                CompleteDuration = item.get("CompleteDurestion")
                TotalRequest = round(item.get("TotalRequest", 0)) if item.get("TotalRequest") is not None else 0
              
                SRMSCompletionDurationData.append({
                    "CompleteDuration": CompleteDuration,
                    "TotalRequest" :TotalRequest 
                })
            
            return JsonResponse({"Table": SRMSCompletionDurationData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def CEORevenueGridDetailsModalData(request):
    RT = request.GET.get('RT', None)
    Type = request.GET.get('Type', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}CEORevenueGridDetailsModalData?RT={RT}&Type={Type}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            RevenueData = []
            for item in data:
                hotel_name = item.get("HTL")
                if Type=='Total Revenue':
                    Revenue = round(item.get("Revenue", 0)) if item.get("Revenue") is not None else 0
                elif Type=='Room Revenue':
                    Revenue = round(item.get("FTD_Room_Revenue", 0)) if item.get("FTD_Room_Revenue") is not None else 0
                elif Type=='FB Revenue':
                    Revenue = round(item.get("FTD_FB_Revenue", 0)) if item.get("FTD_FB_Revenue") is not None else 0   
                
                RevenueData.append({
                    "Hotel": hotel_name,
                    "Total": Revenue,
                   
                })
            
            
            return JsonResponse({"Table": RevenueData})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



from datetime import datetime, timedelta
def all_leaves_ceo(request):
    
    
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}all_leaves_ceo"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        
        if response.status_code == 200:
            data = response.json()

            all_leaves_data = []
           
            for item in data:
                title = item.get("title")
                type = item.get("type", None)
                fullname = item.get("fullname", None)
                id = item.get("id")
                status = item.get("status", None)
                start = item.get("start", None)
                end = item.get("end", None) 

                start = datetime.strptime(start, '%d %b %Y')
                end = datetime.strptime(end, '%d %b %Y %H:%M')

                if isinstance(start, datetime):
                    start = start.isoformat()  
                if isinstance(end, datetime):
                    end = end.isoformat() 
                
                all_leaves_data.append({
                    "title": title,
                    "start": start,
                    "end": end,
                })
            return JsonResponse({"Table": all_leaves_data})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def all_leaves_GM(request):

    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}all_leaves_GM"
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()

            all_leaves_data = []
           
            for item in data:
                title = item.get("title")
                type = item.get("type", None)
                fullname = item.get("fullname", None)
                id = item.get("id")
                status = item.get("status", None)
                start = item.get("start", None)
                end = item.get("end", None)

                def parse_date(date_str):
                    try:
                        return datetime.strptime(date_str, '%d %b %Y %H:%M')
                    except ValueError:
                       
                        return datetime.strptime(date_str, '%d %b %Y')

                
                start = parse_date(start)
                end = parse_date(end)

                if isinstance(start, datetime):
                    start = start.isoformat()  
                if isinstance(end, datetime):
                    end = end.isoformat() 
                
                all_leaves_data.append({
                    "title": title,
                    "start": start,
                    "end": end,
                })
            return JsonResponse({"Table": all_leaves_data})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)



def RDDSRChartData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }
    url=f"{main_url}RDDSRChartData?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            total_visit_data = []
            for item in data.get("Table", []):
                hotel_name = item.get("Hotel", "Unknown Hotel")
                total_visit = round(item.get("TotalVisit", 0)) if item.get("TotalVisit") is not None else 0
                details_json = item.get("DetailsJson", None)  
                
                total_visit_data.append({
                    "Hotel": hotel_name,
                    "TotalVisit": total_visit,
                    "DetailsJson": details_json
                })
            
            return JsonResponse({"Table": total_visit_data})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def GMDSRChartData(request):
    RT = request.GET.get('RT', None)
    main_url = Config.API_URL
    TOKEN_HEADERS ={
        'Authorization':'Bearer '+request.session["ApiToken"],
        'mobile-app-api-token':Config.MobileAppToken
    }

    url=f"{main_url}GMDSRChartData?RT={RT}"
    
    try:
        response = requests.get(url, headers=TOKEN_HEADERS)
        if response.status_code == 200:
            data = response.json()
            
            total_visit_data = []
            for item in data.get("Table", []):
                EmpName = item.get("EmpName")
                total_visit = round(item.get("TotalVisit", 0)) if item.get("TotalVisit") is not None else 0
                details_json = item.get("DetailsJson", None)  
                
                total_visit_data.append({
                    "EmpName": EmpName,
                    "TotalVisit": total_visit,
                    "DetailsJson": details_json
                })
            
            return JsonResponse({"Table": total_visit_data})
        else:
            return JsonResponse({"error": "Failed to fetch data"}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


