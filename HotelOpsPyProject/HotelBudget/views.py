from argparse import REMAINDER
import asyncio
from copyreg import remove_extension
from datetime import date
import datetime
from decimal import Decimal
from django.db import router
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
import requests
from HotelBudget.models import AG_Analysis_Master, AG_AnalysisEntryDetail, AG_AnalysisEntryMaster, AG_HREntryDetails, AG_HREntryMaster, AG_HRMaster, AG_SecurityEntryDetails, AG_SecurityEntryMaster, AG_SecurityMaster, BeverageRevenueBanquet_EntryDetail, BeverageRevenueBanquet_Master, BeverageRevenueEntryDetail, BeverageRevenueMaster, FB_IRD_EnrtyMaster, FB_IRD_EntryDetail, FB_IRD_FoodRevenue_EntryDetail, FB_MiniBar_EnrtyMaster, FB_MiniBar_EntryDetail, FB_MiniBar_FoodRevenue_EntryDetail, FB_MiniBar_FoodRevenue_Master, FB_MiniBar_Master, FB_MiniBar_TotalOtherIncome_EntryDetail, FB_MiniBar_TotalOtherIncome_Master, FB_ODCEntryDetail, FB_ODCEntryMaster, FB_ODCMaster, FB_Worksheet_EnrtyMaster, FB_Worksheet_Master, FBBanquet_EnrtyMaster, FBBanquet_EntryDetail, FBBanquet_Master, FBIRD_BeverageRevenue_Maste_EntryDetail, FBIRD_BeverageRevenue_Master, FBIRD_FoodRevenue_Master, FBIRD_Master, FBIRD_TotalOtherIncome_Master, FBIRD_TotalOtherIncome_MasterIncome_EntryDetail, FBW_Beverage_Food_Average_Check_1_Details, FBW_Beverage_Food_Average_Check_Details, FBW_Break_Beverage_Average_Check_1_Details, FBW_Break_Beverage_Average_Check_Details, FBW_Break_Beverage_External_Covers_Details, FBW_Break_Beverage_Internal_Covers_Details, FBW_Break_Beverage_Revenue_1_Details, FBW_Break_Beverage_Revenue_Details, FBW_Break_Food_Average_Check_1_Details, FBW_Break_Food_Average_Check_Details, FBW_Break_Food_Revenue_1_Details, FBW_Break_Food_Revenue_Details, FBW_Break_food_External_Covers_Details, FBW_Break_food_Internal_Covers_Details, FBW_Capture_Rates_AllMealTypes_Details, FBW_Capture_Rates_Breakfast_Details, FBW_Capture_Rates_Dinner_Details, FBW_Capture_Rates_Launch_Details, FBW_Capture_Rates_Others_Details, FBW_Capture_Rates_Supper_Details, FBW_Dinner_Bevarage_Average_Check_1_Details, FBW_Dinner_Bevarage_Average_Check_Details, FBW_Dinner_Beverage_External_Covers_Details, FBW_Dinner_Beverage_Internal_Covers_Details, FBW_Dinner_Beverage_Revenue_1_Details, FBW_Dinner_Beverage_Revenue_Details, FBW_Dinner_Food_Average_Check_1_Details, FBW_Dinner_Food_Average_Check_Details, FBW_Dinner_Food_External_Covers_Details, FBW_Dinner_Food_Internal_Covers_Details, FBW_Dinner_Food_Revenue_1_Details, FBW_Dinner_Food_Revenue_Details, FBW_Launch_Beverage_External_Details, FBW_Launch_Beverage_Internal_Details, FBW_Launch_Beverage_Revenue_1_Details, FBW_Launch_Beverage_Revenue_Details, FBW_Launch_Food_Average_Check_1_Details, FBW_Launch_Food_Average_Check_Details, FBW_Launch_Food_External_Details, FBW_Launch_Food_Internal_Details, FBW_Launch_Food_Revenue_1_Details, FBW_Launch_Food_Revenue_Details, FBW_Other_Beverage_Average_Check_1_Details, FBW_Other_Beverage_Average_Check_Details, FBW_Other_Beverage_External_Covers_Details, FBW_Other_Beverage_Internal_Covers_Details, FBW_Other_Beverage_Revenue_1_Details, FBW_Other_Beverage_Revenue_Details, FBW_Other_Food_Average_Check_1_Details, FBW_Other_Food_Average_Check_Details, FBW_Other_Food_External_Covers_Details, FBW_Other_Food_Internal_Covers_Details, FBW_Other_Food_Revenue_1_Details, FBW_Other_Food_Revenue_Details, FBW_Super_Beverage_Average_Check_1_Details, FBW_Super_Beverage_Average_Check_Details, FBW_Super_Beverage_External_Covers_Details, FBW_Super_Beverage_Internal_Covers_Details, FBW_Super_Beverage_Revenue_1_Details, FBW_Super_Beverage_Revenue_Details, FBW_Super_Food_Average_Check_1_Details, FBW_Super_Food_Average_Check_Details, FBW_Super_Food_External_Covers_Details, FBW_Super_Food_Internal_Covers_Details, FBW_Super_Food_Revenue_1_Details, FBW_Super_Food_Revenue_Details, FoodRevenueBanquet_EntryDetail, FoodRevenueBanquet_Master, FoodRevenueEntryDetail, FoodRevenueMaster, IT_EntryMaster, It_OtherExpenseEntryDetails, It_ServiceEntryDetails, It_SystemExpenseEntryDetails, ItOtherExpenseMaster, ItServiceMaster, ItSystemExpenseMaster, MinorGuestEntryDetail, MinorGuestEntryMaster, MinorGuestMaster, OOD_HealthEntryDetail, OOD_HealthEntryMaster, OOD_HealthMaster, OOD_LaundryEntryDetail, OOD_LaundryEntryMaster, OOD_LaundryMaster, OOD_TransportEntryDetail, OOD_TransportEntryMaster, OOD_TransportMaster, OODBusinessEntryDetail, OODBusinessEntryMaster, OODBusinessMaster, Outlet1_BeverageRevenue_Maste_EntryDetail, Outlet1_BeverageRevenue_Master, Outlet1_EnrtyMaster, Outlet1_EntryDetail, Outlet1_FoodRevenue_EntryDetail, Outlet1_FoodRevenue_Master, Outlet1_Master, Outlet1_TotalOtherIncome_Master, Outlet1_TotalOtherIncome_MasterIncome_EntryDetail, Outlet2_BeverageRevenue_Maste_EntryDetail, Outlet2_BeverageRevenue_Master, Outlet2_EnrtyMaster, Outlet2_EntryDetail, Outlet2_FoodRevenue_EntryDetail, Outlet2_FoodRevenue_Master, Outlet2_Master, Outlet2_TotalOtherIncome_Master, Outlet2_TotalOtherIncome_MasterIncome_EntryDetail, Outlet3_BeverageRevenue_Maste_EntryDetail, Outlet3_BeverageRevenue_Master, Outlet3_EnrtyMaster, Outlet3_EntryDetail, Outlet3_FoodRevenue_EntryDetail, Outlet3_FoodRevenue_Master, Outlet3_Master, Outlet3_TotalOtherIncome_Master, Outlet3_TotalOtherIncome_MasterIncome_EntryDetail, Outlet4_BeverageRevenue_Maste_EntryDetail, Outlet4_BeverageRevenue_Master, Outlet4_EnrtyMaster, Outlet4_EntryDetail, Outlet4_FoodRevenue_EntryDetail, Outlet4_FoodRevenue_Master, Outlet4_Master, Outlet4_TotalOtherIncome_Master, Outlet4_TotalOtherIncome_MasterIncome_EntryDetail, Outlet5_BeverageRevenue_Maste_EntryDetail, Outlet5_BeverageRevenue_Master, Outlet5_EnrtyMaster, Outlet5_EntryDetail, Outlet5_FoodRevenue_EntryDetail, Outlet5_FoodRevenue_Master, Outlet5_Master, Outlet5_TotalOtherIncome_Master, Outlet5_TotalOtherIncome_MasterIncome_EntryDetail, PL_Engineering_Entry_Master, PL_Engineering_EntryDetails, PL_Engineering_Master, PL_FB_BeverageRevenue_Maste_EntryDetail, PL_FB_BeverageRevenue_Master, PL_FB_EnrtyMaster, PL_FB_EntryDetail, PL_FB_FoodRevenue_EntryDetail, PL_FB_FoodRevenue_Master, PL_FB_Master, PL_FB_TotalOtherIncome_Master, PL_FB_TotalOtherIncome_MasterIncome_EntryDetail, PLUtilitiesEntryDetails, PLUtilitiesEntryMaster, PLUtilitiesMaster, Rental_Other_IncomeEntryDetail, Rental_Other_IncomeEntryMaster, Rental_Other_IncomeMaster, RoomWorksheet_CategoryDetails, RoomWorksheet_CategoryMaster, RoomWorksheet_EnrtyMaster, RoomWorksheet_ItemDetails, RoomWorksheet_ItemMaster, SM_MarketingEntryDetails, SM_MarketingExpenseMaster, SM_SaleMarketingEntryMaster, SM_SalesEntryDetails, SM_SalesExpenseMaster, Total_AG_Master, Total_AGEntryDetails, Total_AGEntryMaster, Total_FB_BeverageRevenue_Maste_EntryDetail, Total_FB_BeverageRevenue_Master, Total_FB_EnrtyMaster, Total_FB_EntryDetail, Total_FB_FoodRevenue_EntryDetail, Total_FB_FoodRevenue_Master, Total_FB_Master, Total_FB_TotalOtherIncome_Master, Total_FB_TotalOtherIncome_MasterIncome_EntryDetail, TotalOtherIncomeEntryDetail, TotalOtherIncomeMaster
from app.models import MonthListMaster
from django.db.models import Subquery
from django.db.models import OuterRef
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.db import connection
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO


def homepage(request):
    return render(request, 'HB/homepage.html' )


def  HPLUtilitiesList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = PLUtilitiesEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'HBBPLUtilities/PLUtilitiesList.html' ,{'mem' :mem }) 


def delete_HPLUtilities (request,id):
    mem = PLUtilitiesEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/HotelBudget/HPLUtilitiesList'))
  
 
def HPLUtilitiesEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"] 
        EntryYear = request.POST["EntryYear"] 
        
        enmaster= PLUtilitiesEntryMaster.objects.create(EntryMonth=EntryMonth,EntryYear=EntryYear,TotalAmount=0,OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()
             
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            PLUtilities_Amount = request.POST["Amount_" + str(x)]
            if(PLUtilities_Amount == ''):
                PLUtilities_Amount = 0
                      
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObje=PLUtilitiesMaster.objects.get(id=TitleID_)
            EntOBj=PLUtilitiesEntryMaster.objects.get(id=enmaster.pk)
              
            v = PLUtilitiesEntryDetails.objects.create(PLUtilities_Amount = PLUtilities_Amount,
                                                       PLUtilitiesMaster=TitleObje,
                                                       PLUtilitiesEntryMaster= EntOBj
                                                      )                        
        return(redirect('/HotelBudget/HPLUtilitiesList'))   
    mem = PLUtilitiesMaster.objects.filter(IsDelete = False)    
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'HBBPLUtilities/PLUtilitiesEntry.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def HPLUtilitiesEdit(request , id):
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        TotalAmount = request.POST["TotalAmount"]
        
        mem = PLUtilitiesEntryMaster.objects.get(id = id)            
        mem.EntryMonth = EntryMonth
        mem.EntryYear =EntryYear
        mem.TotalAmount = TotalAmount
        mem.save()  
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            PLUtilities_Amount = request.POST["Amount_" + str(x)]
            TitleID_ = request.POST["TitleID_" + str(x)]
            mem1 = PLUtilitiesEntryMaster.objects.get(id = id)
              
            sv = PLUtilitiesEntryDetails.objects.get( PLUtilitiesEntryMaster = id , PLUtilitiesMaster = TitleID_)
            sv.PLUtilities_Amount = PLUtilities_Amount
            sv.save()
                                                        
        return(redirect('/HotelBudget/HPLUtilitiesList'))   
    mem1 = PLUtilitiesEntryDetails.objects.filter(PLUtilitiesEntryMaster=id,IsDelete = False).select_related("PLUtilitiesMaster")
    mem = PLUtilitiesEntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1   
    return render(request,'HBBPLUtilities/PLUtilitiesEdit.html',{'mem':mem , 'mem1':mem1 ,'CYear':range(2022,CYear) })


def HPLUtilitiesView(request , id):
  
    template_path = "HBBPLUtilities/PLUtilitiesviewdata.html"
    mem1 = PLUtilitiesEntryDetails.objects.filter(PLUtilitiesEntryMaster=id,IsDelete = False).select_related("PLUtilitiesMaster")
    mem = PLUtilitiesEntryMaster.objects.get(id = id)
 
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)
  
    result = BytesIO()
 
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 



def  HEngList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = PL_Engineering_Entry_Master.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'HBBENG/EngineeringList.html' ,{'mem' :mem }) 

         
def HEngEntry(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses ==''):
            PayrollAndRelatedExpenses =0
        TotalExpenses = request.POST['TotalExpenses']
        if(TotalExpenses==''):
            TotalExpenses=0
        
        enmaster =  PL_Engineering_Entry_Master.objects.create(EntryMonth =  EntryMonth , EntryYear = EntryYear,
                                    SalaryAndWages=SalaryAndWages , Bonuses_and_Incentives=Bonuses_and_Incentives , Salary_Wages_and_Bonuses=Salary_Wages_and_Bonuses,
                                    EmployeeBenefits=EmployeeBenefits,Total_Other_Expenses=Total_Other_Expenses,PayrollRelatedExpenses=PayrollRelatedExpenses,
                                    PayrollAndRelatedExpenses=PayrollAndRelatedExpenses , TotalExpenses=TotalExpenses,OrganizationID=OrganizationID,CreatedBy=UserID )
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            PL_Engineering_Amount = request.POST["Amount_" + str(x)]
            if(PL_Engineering_Amount==''):
             PL_Engineering_Amount=0
                      
            
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = PL_Engineering_Master.objects.get(id = TitleID_)
            EntObj = PL_Engineering_Entry_Master.objects.get(id=enmaster.pk)
            
            v =  PL_Engineering_EntryDetails.objects.create( PL_Engineering_Amount = PL_Engineering_Amount, 
                            PL_Engineering_Master =TitleObj , PL_Engineering_Entry_Master = EntObj  )            
        
        return(redirect('/HotelBudget/HEngList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = PL_Engineering_Master.objects.filter(IsDelete=False)
    return render(request, 'HBBENG/Engineering_Entry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def HEngListDelete(request,id):
    mem = PL_Engineering_Entry_Master.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HEngList'))

 
def HEngListEdit(request , id):
    if request.method == "POST":
        
        EntryMonth = request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        SalaryAndWages = request.POST["SalaryAndWages"]
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST["Salary_Wages_and_Bonuses"]
        EmployeeBenefits = request.POST["EmployeeBenefits"]
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        TotalExpenses = request.POST['TotalExpenses']
        
        mem = PL_Engineering_Entry_Master.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives = Bonuses_and_Incentives
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits = EmployeeBenefits
        mem.PayrollRelatedExpenses = PayrollRelatedExpenses
        mem.Total_Other_Expenses = Total_Other_Expenses
        mem.PayrollAndRelatedExpenses = PayrollAndRelatedExpenses
        mem.TotalExpenses = TotalExpenses
        
        mem.save()
        
        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
                            
            TitleID_ = request.POST["TitleID_" + str(x)]
            PL_Engineering_Amount = request.POST["Amount_" + str(x)]
            mem1 = PL_Engineering_Entry_Master.objects.get(id = id)
            ED = PL_Engineering_EntryDetails.objects.get(PL_Engineering_Master = TitleID_,PL_Engineering_Entry_Master=id)
            ED.PL_Engineering_Amount=PL_Engineering_Amount
            ED.save()                            
       
        return(redirect('/HotelBudget/HEngList'))
    mem1 = PL_Engineering_EntryDetails.objects.filter(PL_Engineering_Entry_Master=id ,IsDelete = False).select_related("PL_Engineering_Master")
    mem = PL_Engineering_Entry_Master.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear) +1
    return render(request,'HBBENG/EngEdit.html',{'mem':mem,'mem1':mem1 , 'CYear':range(2022,CYear)})


def HEngviewdata(request, id):
    template_path = "HBBENG/Engviewdata.html"
    mem1 = PL_Engineering_EntryDetails.objects.filter(PL_Engineering_Entry_Master=id , IsDelete = False).select_related("PL_Engineering_Master")
    mem = PL_Engineering_Entry_Master.objects.get(id = id)
    
      
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 
  
  
def HSMList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = SM_SaleMarketingEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()
     
    return render(request, 'HBBSM/SMList.html' ,{'mem' :mem }) 
       

           
def HSMEntry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")       
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages=0
        Bonuses = request.POST['Bonuses']
        if(Bonuses==''):
            Bonuses=0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Sales_Expenses = request.POST['Total_Sales_Expenses']
        if(Total_Sales_Expenses==''):
            Total_Sales_Expenses=0
        Total_Marketing_Expenses = request.POST['Total_Marketing_Expenses']
        if(Total_Marketing_Expenses==''):
            Total_Marketing_Expenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        TotalExpenses = request.POST['TotalExpenses']
        if(TotalExpenses==''):
            TotalExpenses=0

        enmaster = SM_SaleMarketingEntryMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,SalaryAndWages = SalaryAndWages ,
                                                Bonuses=Bonuses,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               TotalExpenses = TotalExpenses ,  Total_Marketing_Expenses=  Total_Marketing_Expenses,
                             Total_Sales_Expenses= Total_Sales_Expenses, OrganizationID=OrganizationID,CreatedBy=UserID    )
        enmaster.save()
        
        TotalItem = request.POST["TotalItem"]
        EntObj =  SM_SaleMarketingEntryMaster.objects.get(id=enmaster.pk)
        for x in range(int(TotalItem)+1):
            AmountSales = request.POST["Amount_" + str(x)]
            if(AmountSales ==''):
                AmountSales = 0
                
            TitleID_ = request.POST["TitleID_" + str(x)]
        
            TitleObj =  SM_SalesExpenseMaster.objects.get(id = TitleID_)
           
           
        
            v = SM_SalesEntryDetails.objects.create(AmountSales = AmountSales, 
                             SM_SalesExpenseMaster = TitleObj , SM_SaleMarketingEntryMaster = EntObj  )   
          
            
        TotalItemMarketing = request.POST["TotalItemMarketing"]
        for x in range(int(TotalItemMarketing)+1):
            AmountMarketing = request.POST["MAmount_" + str(x)]
            if( AmountMarketing ==''):
                 AmountMarketing = 0
                
            MTitleID_ = request.POST["MTitleID_" + str(x)]
        
            MTitleObj =  SM_MarketingExpenseMaster.objects.get(id = MTitleID_)
       
            
             
            v1 = SM_MarketingEntryDetails.objects.create( AmountMarketing =  AmountMarketing, 
                     SM_MarketingExpenseMaster = MTitleObj ,SM_SaleMarketingEntryMaster = EntObj )         
              
        
        return(redirect('/HotelBudget/HSMList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  SM_SalesExpenseMaster.objects.filter(IsDelete = False)  
    mem1 = SM_MarketingExpenseMaster.objects.filter(IsDelete = False)
    return render(request , 'HBBSM/SMEntry.html' ,{'mem':mem ,'mem1':mem1, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def HSMDelete(request,id):
    mem =  SM_SaleMarketingEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HSMList'))

def HSMEdit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses = request.POST['Bonuses']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Sales_Expenses = request.POST['Total_Sales_Expenses']
        Total_Marketing_Expenses = request.POST['Total_Marketing_Expenses']
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        TotalExpenses = request.POST['TotalExpenses']

        mem =  SM_SaleMarketingEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses =  Bonuses
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Sales_Expenses = Total_Sales_Expenses
        mem.Total_Marketing_Expenses =  Total_Marketing_Expenses
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.TotalExpenses =  TotalExpenses 
        
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            AmountSales = request.POST["Amount_" + str(x)]
            mem1 =  SM_SaleMarketingEntryMaster.objects.get(id = id)
            sv =  SM_SalesEntryDetails.objects.get(SM_SalesExpenseMaster = TitleID_ , SM_SaleMarketingEntryMaster = id)
            sv.AmountSales =  AmountSales
            sv.save()
            
        TotalItemMarketing = request.POST["TotalItemMarketing"]
        for x in range(int(TotalItemMarketing) +1):
           
            MTitleID_ = request.POST["MTitleID_" + str(x)]
            AmountMarketing = request.POST["MAmount_" + str(x)]
            
            sv = SM_MarketingEntryDetails.objects.get(SM_MarketingExpenseMaster = MTitleID_ , SM_SaleMarketingEntryMaster = id)
            sv.AmountMarketing  =  AmountMarketing 
            sv.save()
            
        return(redirect('/HotelBudget/HSMList'))
             
    mem1 = SM_SalesEntryDetails.objects.filter( SM_SaleMarketingEntryMaster=id ,IsDelete = False).select_related("SM_SalesExpenseMaster")
    mem2 = SM_MarketingEntryDetails.objects.filter(SM_SaleMarketingEntryMaster =id ,IsDelete=False ).select_related("SM_MarketingExpenseMaster")
    mem = SM_SaleMarketingEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'HBBSM/SMEdit.html' , {'mem1' :mem1 ,'mem2':mem2, 'mem':mem ,'CYear':range(2022,CYear)})
 
def HSMviewdata(request, id):
    template_path = "HBBSM/SMviewdata.html"
    mem1 = SM_SalesEntryDetails.objects.filter(SM_SaleMarketingEntryMaster=id , IsDelete = False).select_related("SM_SalesExpenseMaster")
    mem = SM_SaleMarketingEntryMaster.objects.get(id = id)
    mem2 = SM_MarketingEntryDetails.objects.filter(SM_SaleMarketingEntryMaster=id , IsDelete = False).select_related("SM_MarketingExpenseMaster")
  
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'mem2':mem2, 'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 


  
def HITList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = IT_EntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()
     
    return render(request, 'HBBIT/ITList.html' ,{'mem' :mem }) 


def HITEntry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")       
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages ==''):
            SalaryAndWages=0
        Bonuses = request.POST['Bonuses']
        if(Bonuses==''):
            Bonuses=0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        TotalExpenses = request.POST['TotalExpenses']
        if(TotalExpenses==''):
            TotalExpenses=0
        Total_Cost_Of_Services = request.POST['Total_Cost_Of_Services']
        if(Total_Cost_Of_Services==''):
            Total_Cost_Of_Services=0

        enmaster = IT_EntryMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,SalaryAndWages = SalaryAndWages ,
                                                Bonuses=Bonuses,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               TotalExpenses = TotalExpenses,Total_Cost_Of_Services=Total_Cost_Of_Services,OrganizationID=OrganizationID,CreatedBy=UserID  )
        enmaster.save() 
              
        EntObj = IT_EntryMaster.objects.get(id=enmaster.pk)   
        
        TotalItem = request.POST["TotalItem"]      
        for x in range(int(TotalItem)+1):
            
            AmountServices = request.POST["Amount_" + str(x)]
            if( AmountServices ==''):
                AmountServices = 0              
            TitleID_ = request.POST["TitleID_" + str(x)]
        
            TitleObj =   ItServiceMaster.objects.get(id = TitleID_)  
                
        
            v = It_ServiceEntryDetails.objects.create( AmountServices =  AmountServices, 
                              ItServiceMaster = TitleObj , IT_EntryMaster = EntObj  )   
          
            
        TotalItemSystem = request.POST["TotalItemSystem"]
        for x in range(int(TotalItemSystem)+1):
            AmountSystemExpense  = request.POST["MAmount_" + str(x)]
            if(  AmountSystemExpense  ==''):
                AmountSystemExpense  = 0
                
            MTitleID_ = request.POST["MTitleID_" + str(x)]
        
            MTitleObj =   ItSystemExpenseMaster.objects.get(id = MTitleID_)
       
            v1 = It_SystemExpenseEntryDetails.objects.create( AmountSystemExpense =  AmountSystemExpense, 
                     ItSystemExpenseMaster = MTitleObj ,IT_EntryMaster = EntObj )         
        
        
        TotalOtherExpenses = request.POST["TotalOtherExpenses"]    
        for x in range(int(TotalOtherExpenses)+1):
            AmountOtherExpense = request.POST["OAmount_" + str(x)]
            if(AmountOtherExpense == ''):
                AmountOtherExpense = 0
                
            OTitleID_ = request.POST["OTitleID_" + str(x)]
            OTitleObj = ItOtherExpenseMaster.objects.get(id = OTitleID_)
            
            v2 = It_OtherExpenseEntryDetails.objects.create(AmountOtherExpense = AmountOtherExpense,
                                           ItOtherExpenseMaster=OTitleObj ,IT_EntryMaster = EntObj )
            
                     
        return(redirect('/HotelBudget/HITList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month     
    mem =  ItServiceMaster.objects.filter(IsDelete = False)  
    mem1 = ItSystemExpenseMaster.objects.filter(IsDelete = False)
    mem2 = ItOtherExpenseMaster.objects.filter(IsDelete = False)
    return render(request , 'HBBIT/ITEntry.html' ,{'mem':mem ,'mem1':mem1,'mem2':mem2, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def HITDelete(request,id):
    mem =  IT_EntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HITList'))


def HITEdit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        Total_Cost_Of_Services = request.POST['Total_Cost_Of_Services'] 
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        TotalExpenses = request.POST['TotalExpenses']

        mem =  IT_EntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.Total_Cost_Of_Services = Total_Cost_Of_Services
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives =  Bonuses_and_Incentives
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.TotalExpenses =  TotalExpenses 
        
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            AmountServices = request.POST["Amount_" + str(x)]
            mem1 =  IT_EntryMaster.objects.get(id = id)
            sv =  It_ServiceEntryDetails.objects.get(ItServiceMaster = TitleID_ , IT_EntryMaster = id)
            sv.AmountServices =  AmountServices
            sv.save()
            
        TotalItemSystem = request.POST["TotalItemSystem"]
        for x in range(int(TotalItemSystem) +1):
           
            MTitleID_ = request.POST["MTitleID_" + str(x)]
            AmountSystemExpense = request.POST["MAmount_" + str(x)]
            
            sv = It_SystemExpenseEntryDetails.objects.get(ItSystemExpenseMaster = MTitleID_ , IT_EntryMaster = id)
            sv.AmountSystemExpense  =    AmountSystemExpense 
            sv.save()
            
        return(redirect('/HotelBudget/HITList'))
             
    mem1 = It_ServiceEntryDetails.objects.filter(IT_EntryMaster=id ,IsDelete = False).select_related("ItServiceMaster")
    mem2 =  It_SystemExpenseEntryDetails.objects.filter(IT_EntryMaster =id ,IsDelete=False ).select_related("ItSystemExpenseMaster")
    mem = IT_EntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'HBBIT/ITEdit.html' , {'mem1' :mem1 ,'mem2':mem2, 'mem':mem ,'CYear':range(2022,CYear)})


def HITView(request , id):
  
    template_path = "HBBIT/ITView.html"
    mem1 = It_ServiceEntryDetails.objects.filter( IT_EntryMaster =id,IsDelete = False).select_related("ItServiceMaster")
    mem2 = It_SystemExpenseEntryDetails.objects.filter(IT_EntryMaster=id,IsDelete = False).select_related("ItSystemExpenseMaster")
    mem3 = It_OtherExpenseEntryDetails.objects.filter(IT_EntryMaster=id,IsDelete = False).select_related("ItOtherExpenseMaster")
    mem = IT_EntryMaster.objects.get(id = id)
 
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict= {'mem':mem,'mem1':mem1,'mem2':mem2, 'mem3':mem3, 'CMonth':CMonth }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)
  
    result = BytesIO()
 
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 


def HAG_SecurityList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = AG_SecurityEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )       
    return render(request, 'HBBAG_Security/AG_SecurityList.html' ,{'mem' :mem }) 


def HAG_SecurityEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages ==''):
            SalaryAndWages =0
        Bonuses = request.POST['Bonuses']
        if(Bonuses == ''):
            Bonuses =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses ==''):
            Salary_Wages_and_Bonuses =0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits ==''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses ==''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses ==''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses =0
        TotalExpenses = request.POST['TotalExpenses']
        if(TotalExpenses == ''):
            TotalExpenses =0
        
        enmaster = AG_SecurityEntryMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear, SalaryAndWages = SalaryAndWages ,
                                                Bonuses=Bonuses,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               TotalExpenses = TotalExpenses,OrganizationID=OrganizationID,CreatedBy=UserID  )
        enmaster.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount ==''):
                Amount = 0
                
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = AG_SecurityMaster.objects.get(id = TitleID_)
            EntObj = AG_SecurityEntryMaster.objects.get(id=enmaster.pk)
            
            v = AG_SecurityEntryDetails.objects.create(Amount = Amount, 
                             AG_SecurityMaster = TitleObj , AG_SecurityEntryMaster = EntObj  )         
        
        return(redirect('/HotelBudget/HAG_SecurityList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  AG_SecurityMaster.objects.filter(IsDelete = False)  
    return render(request , 'HBBAG_Security/AG_SecurityEntry.html' ,{'mem':mem ,'CYear':range(CYear,2020,-1),'CMonth':CMonth})
   

def HAG_SecurityEdit(request,id):
    if request.method =="POST":
        
        EntryMonth =  request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses = request.POST['Bonuses']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses  = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        TotalExpenses = request.POST['TotalExpenses']
        
        mem = AG_SecurityEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses =  Bonuses
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses  =   PayrollRelatedExpenses  
        mem.PayrollAndRelatedExpenses  =   PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.TotalExpenses =  TotalExpenses 
        
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
            Amount = request.POST["Amount_" + str(x)]
            TitleID_ = request.POST["TitleID_" + str(x)]   
            
            mem1 = AG_SecurityEntryMaster.objects.get(id=id)
            sv = AG_SecurityEntryDetails.objects.get(AG_SecurityMaster = TitleID_ , AG_SecurityEntryMaster=id)
            sv.Amount = Amount
            sv.save()  
            
        return(redirect('/HotelBudget/HAG_SecurityList'))
    mem1 = AG_SecurityEntryDetails.objects.filter(AG_SecurityEntryMaster=id , IsDelete=False).select_related("AG_SecurityMaster")
    mem = AG_SecurityEntryMaster.objects.get(id = id)  
    
    today = datetime.date.today()
    CYear = today.year        
    CYear = int(CYear)+1
    mem = AG_SecurityEntryMaster.objects.get(id = id)
    return render(request , 'HBBAG_Security/AG_SecurityEdit.html' , {'mem' :mem , 'mem1':mem1 ,'CYear':range(2022,CYear)})    
        
def HAG_SecurityDelete(request,id):
    mem = AG_SecurityEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HAG_SecurityList'))

def HAG_Securityviewdata(request, id):
    template_path = "HBBAG_Security/AG_Securityviewdata.html"
    mem1 = AG_SecurityEntryDetails.objects.filter(AG_SecurityEntryMaster=id , IsDelete = False).select_related("AG_SecurityMaster")
    mem = AG_SecurityEntryMaster.objects.get(id = id)
    
      
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 



def HAG_HRList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = AG_HREntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'HBBAG_HR/AG_HRList.html' ,{'mem' :mem }) 


def HAG_HREntry(request):
       
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages ==''):
            SalaryAndWages =0
        Bonuses = request.POST['Bonuses']
        if(Bonuses ==''):
            Bonuses =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses ==''):
            Salary_Wages_and_Bonuses =0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits ==''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses == ''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses  ==''):
            Total_Other_Expenses=0
        TotalExpenses = request.POST['TotalExpenses']
        if(TotalExpenses == ''):
            TotalExpenses =0
        
        enmaster = AG_HREntryMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,SalaryAndWages = SalaryAndWages ,
                                                Bonuses=Bonuses,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               TotalExpenses = TotalExpenses,OrganizationID=OrganizationID,CreatedBy=UserID )
        enmaster.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount ==''):
                Amount = 0
                
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = AG_HRMaster.objects.get(id = TitleID_)
            EntObj = AG_HREntryMaster.objects.get(id=enmaster.pk)
            
            v = AG_HREntryDetails.objects.create(Amount = Amount, 
                             AG_HRMaster = TitleObj , AG_HREntryMaster = EntObj  )         
        
        return(redirect('/HotelBudget/HAG_HRList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  AG_HRMaster.objects.filter(IsDelete = False)  
    return render(request , 'HBBAG_HR/AG_HREntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})
    

def HAG_HREdit(request,id):
    
    if request.method =="POST":
        EntryMonth =  request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses = request.POST['Bonuses']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        TotalExpenses = request.POST['TotalExpenses']
        
        mem = AG_HREntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses =  Bonuses
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses =    PayrollAndRelatedExpenses
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.TotalExpenses =  TotalExpenses
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) + 1):
            Amount = request.POST["Amount_" + str(x) ]
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            mem1 = AG_HREntryMaster.objects.get(id=id)
            sv = AG_HREntryDetails.objects.get(AG_HRMaster=TitleID_ ,AG_HREntryMaster =id)
            sv.Amount = Amount
            sv.save() 
        return(redirect('/HotelBudget/HAG_HRList'))       
    mem1 = AG_HREntryDetails.objects.filter(AG_HREntryMaster=id , IsDelete =False).select_related("AG_HRMaster")
    mem = AG_HREntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear) +1
    return render(request , 'HBBAG_HR/AG_HREdit.html' , {'mem' :mem ,'mem1':mem1 , 'CYear':range(2022,CYear)})
     
def HAG_HRDelete(request,id):
    mem = AG_HREntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/HotelBudget/HAG_HRList'))

def HAG_HRviewdata(request, id):
    template_path = "HBBAG_HR/AG_HRviewdata.html"
    mem1 = AG_HREntryDetails.objects.filter(AG_HREntryMaster=id , IsDelete = False).select_related("AG_HRMaster")
    mem = AG_HREntryMaster.objects.get(id = id)
    
      
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 
 

 
 
def HAG_AnalysisList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = AG_AnalysisEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'HBBAG_Analysis/AG_AnalysisList.html' ,{'mem' :mem }) 
       
        
def HAG_AnalysisEntry(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        SalaryAndWages = request.POST['SalaryAndWages']
        if (SalaryAndWages==''):
            SalaryAndWages = 0
        Bonuses = request.POST['Bonuses']
        if(Bonuses == ''):
            Bonuses = 0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses ==''):
            Salary_Wages_and_Bonuses = 0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits ==''):
            EmployeeBenefits = 0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses ==''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses =0
        TotalExpenses = request.POST['TotalExpenses']
        if(TotalExpenses ==''):
            TotalExpenses =0
        
        enmaster =  AG_AnalysisEntryMaster.objects.create(EntryMonth =  EntryMonth , EntryYear = EntryYear,
                                    SalaryAndWages=SalaryAndWages, Bonuses= Bonuses, Salary_Wages_and_Bonuses=Salary_Wages_and_Bonuses,
                                    EmployeeBenefits=EmployeeBenefits,  PayrollRelatedExpenses=  PayrollRelatedExpenses,Total_Other_Expenses=Total_Other_Expenses,
                                    PayrollAndRelatedExpenses=PayrollAndRelatedExpenses , TotalExpenses= TotalExpenses,OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = AG_Analysis_Master.objects.get(id = TitleID_)
            EntObj = AG_AnalysisEntryMaster.objects.get(id=enmaster.pk)
            
            v =  AG_AnalysisEntryDetail.objects.create(Amount = Amount, 
                            AG_Analysis_Master =TitleObj , AG_AnalysisEntryMaster = EntObj  )        
        
        return(redirect('/HotelBudget/HAG_AnalysisList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = AG_Analysis_Master.objects.filter(IsDelete=False)
    return render(request, 'HBBAG_Analysis/AG_AnalysisEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def HAG_AnalysisDelete(request,id):
    mem =  AG_AnalysisEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HAG_AnalysisList'))

def HAG_AnalysisEdit(request,id):
    if request.method =="POST":
        
        EntryMonth =  request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses = request.POST['Bonuses']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        TotalExpenses = request.POST['TotalExpenses']
        
        mem = AG_AnalysisEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses =  Bonuses
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.TotalExpenses =  TotalExpenses 
        
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 = AG_AnalysisEntryMaster.objects.get(id = id)
            sv = AG_AnalysisEntryDetail.objects.get(AG_Analysis_Master = TitleID_ , AG_AnalysisEntryMaster = id)
            sv.Amount = Amount
            sv.save()
            
        return(redirect('/HotelBudget/HAG_AnalysisList'))
             
    mem1 = AG_AnalysisEntryDetail.objects.filter( AG_AnalysisEntryMaster=id ,IsDelete = False).select_related("AG_Analysis_Master")
    mem = AG_AnalysisEntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    
    mem = AG_AnalysisEntryMaster.objects.get(id = id)
    return render(request ,'HBBAG_Analysis/AG_AnalysisEdit.html' , {'mem' :mem , 'mem1':mem1 ,'CYear':range(2022,CYear)})

def HAG_Analysisviewdata(request, id):
    template_path = "HBBAG_Analysis/AG_Ratioviewdata.html"
    mem1 = AG_AnalysisEntryDetail.objects.filter(AG_AnalysisEntryMaster=id , IsDelete = False).select_related("AG_Analysis_Master")
    mem = AG_AnalysisEntryMaster.objects.get(id = id)
         
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 


def HTotal_AGList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Total_AGEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'HBBTotal_AG/Total_AGList.html' ,{'mem' :mem }) 
              

def HTotal_AGEntry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses = request.POST['Bonuses']
        if(Bonuses ==''):
            Bonuses =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses ==''):
            Salary_Wages_and_Bonuses =0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits ==''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses == ''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses ==''):
            Total_Other_Expenses =0
        TotalExpenses = request.POST['TotalExpenses']
        if(TotalExpenses == ''):
            TotalExpenses =0
        
        enmaster = Total_AGEntryMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,SalaryAndWages = SalaryAndWages ,
                                                Bonuses=Bonuses,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               TotalExpenses = TotalExpenses,OrganizationID=OrganizationID,CreatedBy=UserID   )
        enmaster.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount ==''):
                Amount = 0
                
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = Total_AG_Master.objects.get(id = TitleID_)
            EntObj =  Total_AGEntryMaster.objects.get(id=enmaster.pk)
            
            v = Total_AGEntryDetails.objects.create(Amount = Amount, 
                             Total_AG_Master = TitleObj , Total_AGEntryMaster = EntObj  )         
        
        return(redirect('/HotelBudget/HTotal_AGList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  Total_AG_Master.objects.filter(IsDelete = False)  
    return render(request , 'HBBTotal_AG/Total_AGEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})


def HTotal_AGDelete(request,id):
    mem = Total_AGEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HTotal_AGList'))


def HTotal_AGEdit(request,id):
    if request.method =="POST":
        
        EntryMonth =  request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses = request.POST['Bonuses']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        TotalExpenses = request.POST['TotalExpenses']
        
        mem = Total_AGEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses =  Bonuses
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.TotalExpenses =  TotalExpenses 
        
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 = Total_AGEntryMaster.objects.get(id = id)
            sv = Total_AGEntryDetails.objects.get(Total_AG_Master = TitleID_ , Total_AGEntryMaster = id)
            sv.Amount = Amount
            sv.save()
            
        return(redirect('/HotelBudget/HTotal_AGList'))
             
    mem1 = Total_AGEntryDetails.objects.filter( Total_AGEntryMaster=id ,IsDelete = False).select_related("Total_AG_Master")
    mem = Total_AGEntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    
    mem = Total_AGEntryMaster.objects.get(id = id)
    return render(request , 'HBBTotal_AG/Total_AGEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})


def HTotal_AGviewdata(request, id):
    template_path = "HBBTotal_AG/Total_AGviewdata.html"
    mem1 = Total_AGEntryDetails.objects.filter(Total_AGEntryMaster=id , IsDelete = False).select_related("Total_AG_Master")
    mem = Total_AGEntryMaster.objects.get(id = id)
         
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 



def HRental_IncomeList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Rental_Other_IncomeEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'ROIncome/Rental_IncomeList.html' ,{'mem' :mem }) 
       
              
def HRental_IncomeEntry(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        Rental_And_OtherIncome = request.POST['Rental_And_OtherIncome']
        if(Rental_And_OtherIncome == ''):
            Rental_And_OtherIncome =0
       
        enmaster =  Rental_Other_IncomeEntryMaster.objects.create(EntryMonth =  EntryMonth , EntryYear = EntryYear,
                                                           Rental_And_OtherIncome = Rental_And_OtherIncome,OrganizationID=OrganizationID,CreatedBy=UserID )
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = Rental_Other_IncomeMaster.objects.get(id = TitleID_)
            EntObj = Rental_Other_IncomeEntryMaster.objects.get(id=enmaster.pk)
            
            v =  Rental_Other_IncomeEntryDetail.objects.create(Amount = Amount, 
                            Rental_Other_IncomeMaster =TitleObj , Rental_Other_IncomeEntryMaster = EntObj  )        
        
        return(redirect('/HotelBudget/HRental_IncomeList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = Rental_Other_IncomeMaster.objects.filter(IsDelete=False)
    return render(request, 'ROIncome/Rental_IncomeEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def HRental_IncomeDelete(request,id):
    mem =  Rental_Other_IncomeEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HRental_IncomeList'))


def HRental_IncomeEdit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        Rental_And_OtherIncome = request.POST['Rental_And_OtherIncome']    
        mem =  Rental_Other_IncomeEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.Rental_And_OtherIncome = Rental_And_OtherIncome     
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 =  Rental_Other_IncomeEntryMaster.objects.get(id = id)
            sv =  Rental_Other_IncomeEntryDetail.objects.get(Rental_Other_IncomeMaster = TitleID_ ,Rental_Other_IncomeEntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
        return(redirect('/HotelBudget/HRental_IncomeList'))
             
    mem1 = Rental_Other_IncomeEntryDetail.objects.filter(Rental_Other_IncomeEntryMaster=id ,IsDelete = False).select_related("Rental_Other_IncomeMaster")
    mem = Rental_Other_IncomeEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'ROIncome/Rental_IncomeEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})

 
def HRental_Incomeviewdata(request, id):
    template_path = "ROIncome/Rental_Incomeviewdata.html"
    mem1 = Rental_Other_IncomeEntryDetail.objects.filter(Rental_Other_IncomeEntryMaster=id , IsDelete = False).select_related("Rental_Other_IncomeMaster")
    mem = Rental_Other_IncomeEntryMaster.objects.get(id = id)
         
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None   





def  MinorGuestList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = MinorGuestEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'MinorGuest/MGList.html' ,{'mem' :mem }) 


def MinorGuestEntry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        LocalCallRevenue = request.POST['LocalCallRevenue']
        if(LocalCallRevenue == ''):
            LocalCallRevenue =0
        LongDistanceCallRevenue = request.POST['LongDistanceCallRevenue']
        if(LongDistanceCallRevenue == ''):
            LongDistanceCallRevenue = 0
        InternetRevenue = request.POST['InternetRevenue']
        if(InternetRevenue == ''):
            InternetRevenue =0
        OtherMisRevenue = request.POST['OtherMisRevenue']
        if(OtherMisRevenue == ''):
            OtherMisRevenue =0
        TelecommunicationRevenueOthers = request.POST['TelecommunicationRevenueOthers']
        if(TelecommunicationRevenueOthers == ''):
            TelecommunicationRevenueOthers =0
        TelecommunicationRevenue = request.POST['TelecommunicationRevenue']
        if(TelecommunicationRevenue == ''):
            TelecommunicationRevenue =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses = request.POST['Bonuses']
        if(Bonuses ==''):
            Bonuses =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses ==''):
            Salary_Wages_and_Bonuses =0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits ==''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses == ''):
            PayrollAndRelatedExpenses =0
        Total_Cost_Sales = request.POST['Total_Cost_Sales']
        if(Total_Cost_Sales ==''):
            Total_Cost_Sales =0
        DepartmentIncomeLoss = request.POST['DepartmentIncomeLoss']
        if(DepartmentIncomeLoss == ''):
            DepartmentIncomeLoss =0
        
        enmaster = MinorGuestEntryMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,LocalCallRevenue = LocalCallRevenue ,
                                LongDistanceCallRevenue=LongDistanceCallRevenue,InternetRevenue=InternetRevenue,OtherMisRevenue=OtherMisRevenue,
                                TelecommunicationRevenueOthers=TelecommunicationRevenueOthers,TelecommunicationRevenue=TelecommunicationRevenue,
                        SalaryAndWages=SalaryAndWages,  Bonuses=Bonuses,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Cost_Sales= Total_Cost_Sales,
                               DepartmentIncomeLoss = DepartmentIncomeLoss,OrganizationID=OrganizationID,CreatedBy=UserID   )
        enmaster.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount ==''):
                Amount = 0
                
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = MinorGuestMaster.objects.get(id = TitleID_)
            EntObj =  MinorGuestEntryMaster.objects.get(id=enmaster.pk)
            
            v = MinorGuestEntryDetail.objects.create(Amount = Amount, 
                             MinorGuestMaster = TitleObj , MinorGuestEntryMaster = EntObj  )         
        
        return(redirect('/HotelBudget/MinorGuestList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  MinorGuestMaster.objects.filter(IsDelete = False)  
    return render(request , 'MinorGuest/MGEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})



def Minor_GuestEdit(request,id):
    if request.method =="POST":
        
        EntryMonth =  request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        LocalCallRevenue = request.POST["LocalCallRevenue"]
        LongDistanceCallRevenue = request.POST["LongDistanceCallRevenue"]
        InternetRevenue = request.POST["InternetRevenue"]
        OtherMisRevenue = request.POST["OtherMisRevenue"]
        TelecommunicationRevenueOthers = request.POST["TelecommunicationRevenueOthers"]
        TelecommunicationRevenue = request.POST["TelecommunicationRevenue"]
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses = request.POST['Bonuses']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Cost_Sales = request.POST['Total_Cost_Sales']
        DepartmentIncomeLoss = request.POST['DepartmentIncomeLoss']
        
        mem = MinorGuestEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.LocalCallRevenue = LocalCallRevenue
        mem.LongDistanceCallRevenue = LongDistanceCallRevenue
        mem.InternetRevenue = InternetRevenue
        mem.OtherMisRevenue = OtherMisRevenue
        mem.TelecommunicationRevenueOthers = TelecommunicationRevenueOthers
        mem.TelecommunicationRevenue = TelecommunicationRevenue
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses =  Bonuses
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Cost_Sales =   Total_Cost_Sales
        mem.DepartmentIncomeLoss =  DepartmentIncomeLoss 
        
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 = MinorGuestEntryMaster.objects.get(id = id)
            sv = MinorGuestEntryDetail.objects.get(MinorGuestMaster = TitleID_ , MinorGuestEntryMaster = id)
            sv.Amount = Amount
            sv.save()
            
        return(redirect('/HotelBudget/MinorGuestList'))
             
    mem1 = MinorGuestEntryDetail.objects.filter( MinorGuestEntryMaster=id ,IsDelete = False).select_related("MinorGuestMaster")
    mem = MinorGuestEntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    
    mem = MinorGuestEntryMaster.objects.get(id = id)
    return render(request , 'MinorGuest/MNEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})


def Minor_GuestDelete(request,id):
    mem = MinorGuestEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/MinorGuestList'))

def Minor_Guestviewdata(request, id):
    template_path = "MinorGuest/MNView.html"
    mem1 = MinorGuestEntryDetail.objects.filter(MinorGuestEntryMaster=id , IsDelete = False).select_related("MinorGuestMaster")
    mem = MinorGuestEntryMaster.objects.get(id = id)
         
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None   


def  OODBusinessList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = OODBusinessEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'OODBusiness/OODBusinessList.html' ,{'mem' :mem }) 


def OODBusinessEntry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        TelephoneAndFax = request.POST['TelephoneAndFax']
        if(TelephoneAndFax == ''):
            TelephoneAndFax =0
        InternetCharge = request.POST['InternetCharge']
        if(InternetCharge == ''):
            InternetCharge = 0
        Photocopy = request.POST['Photocopy']
        if(Photocopy == ''):
            Photocopy =0
        EuipmentRental = request.POST['EuipmentRental']
        if(EuipmentRental == ''):
            EuipmentRental =0
        MeetingRoomRental = request.POST['MeetingRoomRental']
        if(MeetingRoomRental == ''):
            MeetingRoomRental =0
        BusinessCentreSales = request.POST['BusinessCentreSales']
        if(BusinessCentreSales == ''):
            BusinessCentreSales =0
        BusinessCentreRevenueOther = request.POST["BusinessCentreRevenueOther"]
        if(BusinessCentreRevenueOther == ''):
            BusinessCentreRevenueOther = 0
        BusinessCentreRevenue = request.POST["BusinessCentreRevenue"]
        if(BusinessCentreRevenue == ''):
            BusinessCentreRevenue =0
        CostOfBusinessCentre = request.POST["CostOfBusinessCentre"]
        if(CostOfBusinessCentre == ''):
            CostOfBusinessCentre =0
        Total_Cost_Sales = request.POST["Total_Cost_Sales"]
        if(Total_Cost_Sales == ''):
            Total_Cost_Sales =0
        GrossProfit = request.POST["GrossProfit"]
        if(GrossProfit == ''):
            GrossProfit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses = request.POST['Bonuses']
        if(Bonuses ==''):
            Bonuses =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses ==''):
            Salary_Wages_and_Bonuses =0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits ==''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses == ''):
            PayrollAndRelatedExpenses =0
        TotalOtherExpenses = request.POST['TotalOtherExpenses']
        if(TotalOtherExpenses ==''):
            TotalOtherExpenses =0
        TotalExpenses = request.POST["TotalExpenses"]
        if(TotalExpenses == ''):
            TotalExpenses = 0
        DepartmentIncomeLoss = request.POST['DepartmentIncomeLoss']
        if(DepartmentIncomeLoss == ''):
            DepartmentIncomeLoss =0
        
        enmaster = OODBusinessEntryMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,TelephoneAndFax = TelephoneAndFax ,
                                InternetCharge=InternetCharge , Photocopy=Photocopy,EuipmentRental=EuipmentRental,
                                MeetingRoomRental=MeetingRoomRental,BusinessCentreSales=BusinessCentreSales,BusinessCentreRevenueOther=BusinessCentreRevenueOther,
                                BusinessCentreRevenue=BusinessCentreRevenue,CostOfBusinessCentre=CostOfBusinessCentre,
                                Total_Cost_Sales=Total_Cost_Sales,GrossProfit=GrossProfit,
                        SalaryAndWages=SalaryAndWages,  Bonuses=Bonuses,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, TotalOtherExpenses= TotalOtherExpenses,
                               TotalExpenses=TotalExpenses , 
                               DepartmentIncomeLoss = DepartmentIncomeLoss,OrganizationID=OrganizationID,CreatedBy=UserID   )
        enmaster.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount ==''):
                Amount = 0
                
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = OODBusinessMaster.objects.get(id = TitleID_)
            EntObj =  OODBusinessEntryMaster.objects.get(id=enmaster.pk)
            
            v = OODBusinessEntryDetail.objects.create(Amount = Amount, 
                             OODBusinessMaster = TitleObj , OODBusinessEntryMaster = EntObj  )         
        
        return(redirect('/HotelBudget/OODBusinessList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  OODBusinessMaster.objects.filter(IsDelete = False)  
    return render(request , 'OODBusiness/OODBusinessEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})


def OODBusinessEdit(request,id):
    if request.method =="POST":
        
        EntryMonth =  request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        TelephoneAndFax = request.POST["TelephoneAndFax"]
        InternetCharge = request.POST["InternetCharge"]
        Photocopy = request.POST["Photocopy"]
        MeetingRoomRental = request.POST["MeetingRoomRental"]
        BusinessCentreSales = request.POST["BusinessCentreSales"]
        BusinessCentreRevenueOther = request.POST["BusinessCentreRevenueOther"]
        BusinessCentreRevenue  = request.POST["BusinessCentreRevenue"]
        CostOfBusinessCentre = request.POST["CostOfBusinessCentre"]
        Total_Cost_Sales = request.POST["Total_Cost_Sales"]
        GrossProfit = request.POST["GrossProfit"]
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses = request.POST['Bonuses']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        TotalOtherExpenses = request.POST['TotalOtherExpenses']
        TotalExpenses = request.POST['TotalExpenses']
        DepartmentIncomeLoss = request.POST['DepartmentIncomeLoss']
        
        mem = OODBusinessEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.TelephoneAndFax = TelephoneAndFax
        mem.InternetCharge = InternetCharge
        mem.Photocopy = Photocopy
        mem.MeetingRoomRental = MeetingRoomRental
        mem.BusinessCentreSales = BusinessCentreSales
        mem.BusinessCentreRevenueOther = BusinessCentreRevenueOther
        mem.BusinessCentreRevenue  = BusinessCentreRevenue 
        mem.CostOfBusinessCentre = CostOfBusinessCentre
        mem.Total_Cost_Sales = Total_Cost_Sales
        mem.GrossProfit = GrossProfit
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses =  Bonuses
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.TotalOtherExpenses =   TotalOtherExpenses
        mem.TotalExpenses = TotalExpenses
        mem.DepartmentIncomeLoss =  DepartmentIncomeLoss 
        
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 = OODBusinessEntryMaster.objects.get(id = id)
            sv = OODBusinessEntryDetail.objects.get(OODBusinessMaster = TitleID_ , OODBusinessEntryMaster = id)
            sv.Amount = Amount
            sv.save()
            
        return(redirect('/HotelBudget/OODBusinessList'))
             
    mem1 = OODBusinessEntryDetail.objects.filter( OODBusinessEntryMaster=id ,IsDelete = False).select_related("OODBusinessMaster")
    mem = OODBusinessEntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    
    mem = OODBusinessEntryMaster.objects.get(id = id)
    return render(request , 'OODBusiness/OODBusinessEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})

def OODBusiness_Delete (request,id):
    mem = OODBusinessEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/HotelBudget/OODBusinessList'))
  

def OODBusinessView(request , id):
  
    template_path = "OODBusiness/OODBusinessView.html"
    mem1 = OODBusinessEntryDetail.objects.filter(OODBusinessEntryMaster=id,IsDelete = False).select_related("OODBusinessMaster")
    mem = OODBusinessEntryMaster.objects.get(id = id)
 
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)
  
    result = BytesIO()
 
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 


 
def  HOOD_LaundryList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = OOD_LaundryEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'OODLaundryHB/OOD_LaundryList.html' ,{'mem' :mem }) 


def HOOD_LaundryEntry(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        Dry_CleaningServices = request.POST['Dry_CleaningServices']
        if(Dry_CleaningServices == ''):
            Dry_CleaningServices =0
        LaundryServices  = request.POST['LaundryServices']
        if(LaundryServices ==''):
            LaundryServices =0
        PressingServices = request.POST["PressingServices"]
        if(PressingServices == ''):
            PressingServices =0
        GuestLaundryRevenue  = request.POST['GuestLaundryRevenue']
        if(GuestLaundryRevenue ==''):
            GuestLaundryRevenue =0
        Cost_OfLaundryServices = request.POST['Cost_OfLaundryServices']
        if(Cost_OfLaundryServices ==''):
            Cost_OfLaundryServices =0
        Total_CostOfSales = request.POST['Total_CostOfSales']
        if(Total_CostOfSales ==''):
            Total_CostOfSales =0
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit ==''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages ==''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives=0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses ==''):
            Salary_Wages_and_Bonuses =0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits ==''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses == ''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses ==''):
            Total_Other_Expenses =0
        TotalExpenses = request.POST['TotalExpenses']
        if(TotalExpenses == ''):
            TotalExpenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0
      
        enmaster =  OOD_LaundryEntryMaster.objects.create(EntryMonth = EntryMonth, EntryYear = EntryYear,
                        Dry_CleaningServices=  Dry_CleaningServices, LaundryServices = LaundryServices,
                        PressingServices=PressingServices, 
                        GuestLaundryRevenue=GuestLaundryRevenue ,   Cost_OfLaundryServices= Cost_OfLaundryServices,
                       Total_CostOfSales= Total_CostOfSales,  Gross_Profit= Gross_Profit,
                  SalaryAndWages= SalaryAndWages ,  Bonuses_and_Incentives =  Bonuses_and_Incentives ,
               Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,  EmployeeBenefits= EmployeeBenefits,
              PayrollRelatedExpenses= PayrollRelatedExpenses, PayrollAndRelatedExpenses= PayrollAndRelatedExpenses,
               Total_Other_Expenses= Total_Other_Expenses , TotalExpenses= TotalExpenses,  DepartmentIncome =  DepartmentIncome,OrganizationID=OrganizationID,CreatedBy=UserID )
        
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = OOD_LaundryMaster.objects.get(id = TitleID_)
            EntObj = OOD_LaundryEntryMaster.objects.get(id=enmaster.pk)
            
            v =  OOD_LaundryEntryDetail.objects.create(Amount = Amount, 
                            OOD_LaundryMaster =TitleObj , OOD_LaundryEntryMaster = EntObj  )        
        
        return(redirect('/HotelBudget/HOOD_LaundryList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = OOD_LaundryMaster.objects.filter(IsDelete=False)
    return render(request, 'OODLaundryHB/OOD_LaundryEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})


def HOOD_LaundryEdit(request,id):   
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        Dry_CleaningServices = request.POST['Dry_CleaningServices']
        LaundryServices = request.POST['LaundryServices']
        PressingServices = request.POST['PressingServices']
        GuestLaundryRevenue = request.POST['GuestLaundryRevenue']
        Cost_OfLaundryServices = request.POST['Cost_OfLaundryServices']
        Total_CostOfSales = request.POST['Total_CostOfSales']
        Gross_Profit  = request.POST['Gross_Profit']
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits  = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses  = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        TotalExpenses = request.POST['TotalExpenses']
        DepartmentIncome  = request.POST['DepartmentIncome']
          
        mem =   OOD_LaundryEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.Dry_CleaningServices  =  Dry_CleaningServices 
        mem.LaundryServices =  LaundryServices
        mem.PressingServices = PressingServices
        mem.GuestLaundryRevenue =   GuestLaundryRevenue
        mem.Cost_OfLaundryServices =   Cost_OfLaundryServices
        mem.Total_CostOfSales =   Total_CostOfSales
        mem.Gross_Profit  =  Gross_Profit 
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives  =  Bonuses_and_Incentives 
        mem.Salary_Wages_and_Bonuses =  Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =   EmployeeBenefits 
        mem.PayrollRelatedExpenses  =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses =   PayrollAndRelatedExpenses
        mem.Total_Other_Expenses =  Total_Other_Expenses
        mem.TotalExpenses =   TotalExpenses
        mem.DepartmentIncome  =   DepartmentIncome 
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 =  OOD_LaundryEntryMaster.objects.get(id = id)
            sv =  OOD_LaundryEntryDetail.objects.get(OOD_LaundryMaster = TitleID_ , OOD_LaundryEntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
        return(redirect('/HotelBudget/HOOD_LaundryList'))
             
    mem1 = OOD_LaundryEntryDetail.objects.filter(OOD_LaundryEntryMaster=id ,IsDelete = False).select_related("OOD_LaundryMaster")
    mem = OOD_LaundryEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'OODLaundryHB/OOD_LaundryEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})

def HOOD_LaundryDelete(request,id):
    mem = OOD_LaundryEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HOOD_LaundryList'))

def HOOD_Laundryviewdata(request, id):
    template_path = "OODLaundryHB/OOD_Laundryviewdata.html"
    mem1 = OOD_LaundryEntryDetail.objects.filter(OOD_LaundryEntryMaster=id , IsDelete = False).select_related("OOD_LaundryMaster")
    mem = OOD_LaundryEntryMaster.objects.get(id = id)
         
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None    


def HOOD_TransportList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = OOD_TransportEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'OODTransportHB/OOD_TransportList.html' ,{'mem' :mem }) 
      
      
     
def HOOD_TransportEntry(request):   
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
            Salary_Wages_and_Bonuses =0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits == ''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses == ''):
            PayrollAndRelatedExpenses ==0
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses ==''):
            Total_Other_Expenses=0
        TotalExpenses = request.POST['TotalExpenses']
        if(TotalExpenses ==''):
            TotalExpenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0
      
        enmaster =  OOD_TransportEntryMaster.objects.create(EntryMonth = EntryMonth, EntryYear = EntryYear,                      
                  SalaryAndWages= SalaryAndWages ,  Bonuses_and_Incentives =  Bonuses_and_Incentives ,
               Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,  EmployeeBenefits= EmployeeBenefits,
              PayrollRelatedExpenses= PayrollRelatedExpenses, PayrollAndRelatedExpenses= PayrollAndRelatedExpenses,
               Total_Other_Expenses= Total_Other_Expenses , TotalExpenses= TotalExpenses,  DepartmentIncome =  DepartmentIncome,OrganizationID=OrganizationID,CreatedBy=UserID)
        
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj =  OOD_TransportMaster.objects.get(id = TitleID_)
            EntObj =  OOD_TransportEntryMaster.objects.get(id=enmaster.pk)
            
            v =   OOD_TransportEntryDetail.objects.create(Amount = Amount, 
                            OOD_TransportMaster =TitleObj ,  OOD_TransportEntryMaster = EntObj  )        
                
        return(redirect('/HotelBudget/HOOD_TransportList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem =  OOD_TransportMaster.objects.filter(IsDelete=False)
    return render(request, 'OODTransportHB/OOD_TransportEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})


def HOOD_TransportEdit(request,id):   
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        InHouseLimousineRevenue  = request.POST['InHouseLimousineRevenue']
        if(InHouseLimousineRevenue == ''):
            InHouseLimousineRevenue =0
        ExternalLimousineRevenue = request.POST["ExternalLimousineRevenue"]
        if(ExternalLimousineRevenue == ''):
            ExternalLimousineRevenue =0
        GuestTransportationRevenue = request.POST["GuestTransportationRevenue"]
        if(GuestTransportationRevenue == ''):
            GuestTransportationRevenue =0
        GuestTransportRevenue = request.POST['GuestTransportRevenue']
        if(GuestTransportRevenue == ''):
            GuestTransportRevenue =0
        Cost_OfGuestTransportation = request.POST['Cost_OfGuestTransportation']
        if(Cost_OfGuestTransportation == ''):
            Cost_OfGuestTransportation =0
        Total_CostOfSales = request.POST['Total_CostOfSales']
        if(Total_CostOfSales == ''):
            Total_CostOfSales =0
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages ==''):
            SalaryAndWages = 0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses ==''):
            Salary_Wages_and_Bonuses =0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits == ''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses == ''):
            PayrollAndRelatedExpenses = 0
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses =0
        TotalExpenses = request.POST['TotalExpenses']
        if(TotalExpenses == ''):
            TotalExpenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0
      
        mem =  OOD_TransportEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.InHouseLimousineRevenue  =   InHouseLimousineRevenue 
        mem.ExternalLimousineRevenue = ExternalLimousineRevenue
        mem.GuestTransportationRevenue = GuestTransportationRevenue
        mem.GuestTransportRevenue =   GuestTransportRevenue
        mem.Cost_OfGuestTransportation =    Cost_OfGuestTransportation
        mem.Total_CostOfSales =   Total_CostOfSales
        mem.Gross_Profit  =  Gross_Profit 
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives  =  Bonuses_and_Incentives 
        mem.Salary_Wages_and_Bonuses =  Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =   EmployeeBenefits 
        mem.PayrollRelatedExpenses  =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses =   PayrollAndRelatedExpenses
        mem.Total_Other_Expenses =  Total_Other_Expenses
        mem.TotalExpenses =   TotalExpenses
        mem.DepartmentIncome  =   DepartmentIncome 
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 =   OOD_TransportEntryMaster.objects.get(id = id)
            sv =  OOD_TransportEntryDetail.objects.get(OOD_TransportMaster = TitleID_ , OOD_TransportEntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
        return(redirect('/HotelBudget/HOOD_TransportList'))
             
    mem1 = OOD_TransportEntryDetail.objects.filter( OOD_TransportEntryMaster=id ,IsDelete = False).select_related("OOD_TransportMaster")
    mem =  OOD_TransportEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'OODTransportHB/OOD_TransportEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})


def HOOD_TransportDelete(request,id):
    mem =  OOD_TransportEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HOOD_TransportList'))



def HOOD_Transportviewdata(request, id):
    template_path = "OODTransportHB/OOD_Transportviewdata.html"
    mem1 = OOD_TransportEntryDetail.objects.filter(OOD_TransportEntryMaster=id , IsDelete = False).select_related("OOD_TransportMaster")
    mem = OOD_TransportEntryMaster.objects.get(id = id)
         
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None    



def HOOD_HealthList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = OOD_HealthEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'OODHealthHB/OOD_HealthList.html' ,{'mem' :mem }) 


      
def HOOD_HealthEntry(request):  
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FitnessLessonRevenue = request.POST['FitnessLessonRevenue']
        if(FitnessLessonRevenue == ''):
            FitnessLessonRevenue =0
        MassageRevenue = request.POST['MassageRevenue']
        if(MassageRevenue == ''):
            MassageRevenue = 0
        SpaTreatmentRevenue = request.POST['SpaTreatmentRevenue']
        if(SpaTreatmentRevenue == ''):
            SpaTreatmentRevenue =0
        SalonTreatmentRevenue = request.POST['SalonTreatmentRevenue']
        if(SalonTreatmentRevenue == ''):
            SalonTreatmentRevenue =0
        MerchandiseRevenue = request.POST['MerchandiseRevenue']
        if(MerchandiseRevenue == ''):
            MerchandiseRevenue =0
        HealthWellnessRevenue = request.POST['HealthWellnessRevenue']
        if(HealthWellnessRevenue == ''):
            HealthWellnessRevenue =0
        HealthClubSpaRevenueOther = request.POST['HealthClubSpaRevenueOther']
        if(HealthClubSpaRevenueOther == ''):
            HealthClubSpaRevenueOther =0
        HealthClubSpaRevenue   = request.POST['HealthClubSpaRevenue']
        if(HealthClubSpaRevenue == ''):
            HealthClubSpaRevenue =0
        Cost_OfMerchandise  = request.POST['Cost_OfMerchandise']
        if(Cost_OfMerchandise == ''):
            Cost_OfMerchandise =0
        Total_CostOfSales = request.POST['Total_CostOfSales']
        if(Total_CostOfSales ==''):
            Total_CostOfSales =0
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit ==''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
            Salary_Wages_and_Bonuses =0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits == ''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses == ''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses ==''):
            Total_Other_Expenses =0
        TotalExpenses = request.POST['TotalExpenses']
        if(TotalExpenses == ''):
            TotalExpenses = 0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0
      
        enmaster =   OOD_HealthEntryMaster.objects.create(EntryMonth = EntryMonth, EntryYear = EntryYear,
                                MassageRevenue =MassageRevenue,SpaTreatmentRevenue=SpaTreatmentRevenue,
                          SalonTreatmentRevenue=SalonTreatmentRevenue,MerchandiseRevenue=MerchandiseRevenue,
                          HealthWellnessRevenue =HealthWellnessRevenue,HealthClubSpaRevenueOther=HealthClubSpaRevenueOther,     
                         FitnessLessonRevenue = FitnessLessonRevenue ,   HealthClubSpaRevenue =  HealthClubSpaRevenue , 
                         Cost_OfMerchandise= Cost_OfMerchandise ,  Total_CostOfSales= Total_CostOfSales,  Gross_Profit= Gross_Profit,
                  SalaryAndWages= SalaryAndWages ,  Bonuses_and_Incentives =  Bonuses_and_Incentives ,
               Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,  EmployeeBenefits= EmployeeBenefits,
              PayrollRelatedExpenses= PayrollRelatedExpenses, PayrollAndRelatedExpenses= PayrollAndRelatedExpenses,
               Total_Other_Expenses= Total_Other_Expenses , TotalExpenses= TotalExpenses,  DepartmentIncome =  DepartmentIncome,OrganizationID=OrganizationID,CreatedBy=UserID )
        
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = OOD_HealthMaster.objects.get(id = TitleID_)
            EntObj = OOD_HealthEntryMaster.objects.get(id=enmaster.pk)
            
            v =  OOD_HealthEntryDetail.objects.create(Amount = Amount, 
                            OOD_HealthMaster =TitleObj , OOD_HealthEntryMaster = EntObj  )        
        
        return(redirect('/HotelBudget/HOOD_HealthList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = OOD_HealthMaster.objects.filter(IsDelete=False)
    return render(request, 'OODHealthHB/OOD_HealthEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def HOOD_HealthDelete(request,id):
    mem = OOD_HealthEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HOOD_HealthList'))



def HOOD_HealthEdit(request,id):   
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FitnessLessonRevenue = request.POST['FitnessLessonRevenue']
        if(FitnessLessonRevenue == ''):
            FitnessLessonRevenue =0
        MassageRevenue = request.POST['MassageRevenue']
        if(MassageRevenue == ''):
            MassageRevenue =0
        SpaTreatmentRevenue = request.POST['SpaTreatmentRevenue']
        if(SpaTreatmentRevenue == ''):
            SpaTreatmentRevenue =0
        SalonTreatmentRevenue = request.POST['SalonTreatmentRevenue']
        if(SalonTreatmentRevenue == ''):
            SalonTreatmentRevenue =0
        MerchandiseRevenue = request.POST['MerchandiseRevenue']
        if(MerchandiseRevenue == ''):
            MerchandiseRevenue =0
        HealthWellnessRevenue = request.POST['HealthWellnessRevenue']
        if(HealthWellnessRevenue == ''):
            HealthWellnessRevenue =0
        HealthClubSpaRevenueOther = request.POST['HealthClubSpaRevenueOther']
        if(HealthClubSpaRevenueOther == ''):
            HealthClubSpaRevenueOther =0
        HealthClubSpaRevenue   = request.POST['HealthClubSpaRevenue']
        if(HealthClubSpaRevenue == ''):
            HealthClubSpaRevenue =0
        Cost_OfMerchandise  = request.POST['Cost_OfMerchandise']
        if(Cost_OfMerchandise ==''):
            Cost_OfMerchandise =0
        Total_CostOfSales = request.POST['Total_CostOfSales']
        if(Total_CostOfSales == ''):
            Total_CostOfSales =0
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
            Salary_Wages_and_Bonuses =0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits == ''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses == ''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses =0
        TotalExpenses = request.POST['TotalExpenses']
        if(TotalExpenses == ''):
            TotalExpenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0
      
        mem =  OOD_HealthEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FitnessLessonRevenue  =  FitnessLessonRevenue 
        mem.MassageRevenue = MassageRevenue
        mem.SpaTreatmentRevenue = SpaTreatmentRevenue
        mem.SalonTreatmentRevenue = SalonTreatmentRevenue
        mem.MerchandiseRevenue = MerchandiseRevenue
        mem.HealthWellnessRevenue = HealthWellnessRevenue
        mem.HealthClubSpaRevenueOther = HealthClubSpaRevenueOther
        mem.HealthClubSpaRevenue =   HealthClubSpaRevenue
        mem.Cost_OfMerchandise =    Cost_OfMerchandise
        mem.Total_CostOfSales =   Total_CostOfSales
        mem.Gross_Profit  =  Gross_Profit 
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives  =  Bonuses_and_Incentives 
        mem.Salary_Wages_and_Bonuses =  Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =   EmployeeBenefits 
        mem.PayrollRelatedExpenses  =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses =   PayrollAndRelatedExpenses
        mem.Total_Other_Expenses =  Total_Other_Expenses
        mem.TotalExpenses =   TotalExpenses
        mem.DepartmentIncome  =   DepartmentIncome 
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 =   OOD_HealthEntryMaster.objects.get(id = id)
            sv =  OOD_HealthEntryDetail.objects.get(OOD_HealthMaster = TitleID_ , OOD_HealthEntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
        return(redirect('/HotelBudget/HOOD_HealthList'))
             
    mem1 = OOD_HealthEntryDetail.objects.filter( OOD_HealthEntryMaster=id ,IsDelete = False).select_related("OOD_HealthMaster")
    mem =  OOD_HealthEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'OODHealthHB/OOD_HealthEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})



def HOOD_Healthviewdata(request, id):
    template_path = "OODHealthHB/OOD_Healthviewdata.html"
    mem1 = OOD_HealthEntryDetail.objects.filter(OOD_HealthEntryMaster=id , IsDelete = False).select_related("OOD_HealthMaster")
    mem = OOD_HealthEntryMaster.objects.get(id = id)
         
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None      




  
def FB_ODCList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = FB_ODCEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'FBODC/FBODCList.html' ,{'mem' :mem }) 
                            
       
def FB_ODCEntry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")       
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST["BeverageRevenue"]
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST["TotalOtherIncome"]
        if(TotalOtherIncome == ''):
            TotalOtherIncome = 0
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue == ''):
            FBRevenue =0           
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages=0
        Bonuses = request.POST['Bonuses']
        if(Bonuses==''):
            Bonuses=0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0
        Gross_Profit = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome==''):
            DepartmentIncome=0

        enmaster = FB_ODCEntryMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,
                                    FoodRevenue=FoodRevenue ,SalaryAndWages = SalaryAndWages ,
                                   BeverageRevenue=BeverageRevenue,TotalOtherIncome=TotalOtherIncome,
                                    FBRevenue=FBRevenue, FoodCostOfSales=FoodCostOfSales,
                                    BeverageCostOfSales=BeverageCostOfSales,                                    
                                    TotalCostOfFbSales=TotalCostOfFbSales,AudioVisualEquipmentCostOfSales=AudioVisualEquipmentCostOfSales,
                                    FBOtherCostOfSales=FBOtherCostOfSales,TotalCostOfOtherRev=TotalCostOfOtherRev,
                                    TotalCostOfSales=TotalCostOfSales,Gross_Profit=Gross_Profit,
                                 Bonuses=Bonuses,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               DepartmentIncome = DepartmentIncome , 
                             OrganizationID=OrganizationID,CreatedBy=UserID    )
        enmaster.save()
 
        
        TotalItem = request.POST["TotalItem"]
        EntObj =  FB_ODCEntryMaster.objects.get(id=enmaster.pk)
        
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount ==''):
                Amount = 0
                
            TitleID_ = request.POST["TitleID_" + str(x)]        
            TitleObj =  FB_ODCMaster.objects.get(id = TitleID_)           
        
            v = FB_ODCEntryDetail.objects.create(Amount = Amount, 
                             FB_ODCMaster = TitleObj , FB_ODCEntryMaster = EntObj  )   
          
            
        TotalItemFood = request.POST["TotalItemFood"]
        for x in range(int(TotalItemFood)+1):
            Amount1 = request.POST["FAmount_" + str(x)]
            if( Amount1 ==''):
                 Amount1 = 0
                
            FTitleID_ = request.POST["FTitleID_"+ str(x)]        
            FTitleObj =  FoodRevenueMaster.objects.get(id = FTitleID_)
                   
            v1 = FoodRevenueEntryDetail.objects.create( Amount1 =  Amount1, 
                     FoodRevenueMaster = FTitleObj ,FB_ODCEntryMaster = EntObj )         
              
              
        TotalItemBeverage = request.POST["TotalItemBeverage"]
        for x in range(int(TotalItemBeverage)+1):
            Amount2 = request.POST["BAmount_" + str(x)]
            if( Amount2 ==''):
                 Amount2 = 0
                
            BTitleID_ = request.POST["BTitleID_" + str(x)]        
            BTitleObj =  BeverageRevenueMaster.objects.get(id = BTitleID_)
                   
            v2 = BeverageRevenueEntryDetail.objects.create( Amount2 =  Amount2, 
                     BeverageRevenueMaster = BTitleObj ,FB_ODCEntryMaster = EntObj )         
              
                
        TotalItemOther= request.POST["TotalItemOther"]
        for x in range(int(TotalItemOther)+1):
            Amount3 = request.POST["OAmount_" + str(x)]
            if( Amount3 ==''):
                 Amount3 = 0
                
            OTitleID_ = request.POST["OTitleID_" + str(x)]        
            OTitleObj =  TotalOtherIncomeMaster.objects.get(id = OTitleID_)
                   
            v3 = TotalOtherIncomeEntryDetail.objects.create( Amount3 =  Amount3, 
                     TotalOtherIncomeMaster = OTitleObj ,FB_ODCEntryMaster = EntObj )         
              
        
        return(redirect('/HotelBudget/FB_ODCList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  FB_ODCMaster.objects.filter(IsDelete = False)  
    mem1 = FoodRevenueMaster.objects.filter(IsDelete = False)
    mem2 = BeverageRevenueMaster.objects.filter(IsDelete = False)
    mem3 = TotalOtherIncomeMaster.objects.filter(IsDelete = False)
    return render(request , 'FBODC/FBODCEntry.html' ,{'mem':mem ,'mem1':mem1,'mem2':mem2,'mem3':mem3, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def FB_ODCDelete(request,id):
    mem =  FB_ODCEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/FB_ODCList'))



def FB_ODCEdit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue ==''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales == ''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0
        Gross_Profit = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses = request.POST['Bonuses']
        if(Bonuses == ''):
            Bonuses =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
            Salary_Wages_and_Bonuses = 0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits == ''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses ==''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0

        mem =  FB_ODCEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue = FoodRevenue
        mem.BeverageRevenue = BeverageRevenue
        mem.TotalOtherIncome = TotalOtherIncome
        mem.FBRevenue = FBRevenue
        mem.FoodCostOfSales = FoodCostOfSales
        mem.BeverageCostOfSales = BeverageCostOfSales
        mem.TotalCostOfFbSales = TotalCostOfFbSales
        mem.AudioVisualEquipmentCostOfSales = AudioVisualEquipmentCostOfSales
        mem.FBOtherCostOfSales = FBOtherCostOfSales
        mem.TotalCostOfOtherRev = TotalCostOfOtherRev
        mem.TotalCostOfSales = TotalCostOfSales
        mem.Gross_Profit = Gross_Profit        
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses =  Bonuses
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.DepartmentIncome =  DepartmentIncome 
        
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem =  FB_ODCEntryMaster.objects.get(id = id)
            sv =  FB_ODCEntryDetail.objects.get(FB_ODCMaster = TitleID_ , FB_ODCEntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
            
        TotalItemFood  = request.POST["TotalItemFood"]
        for x in range(int( TotalItemFood ) +1):
           
            FTitleID_ = request.POST["FTitleID_" + str(x)]
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 == ''):
                Amount1 =0
            
            sv = FoodRevenueEntryDetail.objects.get(FoodRevenueMaster = FTitleID_ , FB_ODCEntryMaster = id)
            sv.Amount1  =  Amount1 
            sv.save()
            
               
        TotalItemBeverage   = request.POST["TotalItemBeverage"]
        for x in range(int( TotalItemBeverage  ) +1):
           
            BTitleID_ = request.POST["BTitleID_" + str(x)]
            Amount2 = request.POST["BAmount_" + str(x)]
            if(Amount2 == ''):
                Amount2 =0
            
            sv = BeverageRevenueEntryDetail.objects.get(BeverageRevenueMaster = BTitleID_ , FB_ODCEntryMaster = id)
            sv.Amount2  =  Amount2 
            sv.save()
            
        TotalItemOther   = request.POST["TotalItemOther"]
        for x in range(int( TotalItemOther ) +1):
           
            OTitleID_ = request.POST["OTitleID_" + str(x)]
            Amount3 = request.POST["OAmount_" + str(x)]
            if(Amount3 == ''):
                Amount3 =0
            
            sv = TotalOtherIncomeEntryDetail.objects.get(TotalOtherIncomeMaster = OTitleID_ , FB_ODCEntryMaster = id)
            sv.Amount3  =  Amount3 
            sv.save()
            
        return(redirect('/HotelBudget/FB_ODCList'))
    
    mem4 = FB_ODCEntryDetail.objects.filter( FB_ODCEntryMaster=id ,IsDelete = False).select_related("FB_ODCMaster")  
    mem3 = TotalOtherIncomeEntryDetail.objects.filter( FB_ODCEntryMaster=id ,IsDelete = False).select_related("TotalOtherIncomeMaster")       
    mem2 = BeverageRevenueEntryDetail.objects.filter( FB_ODCEntryMaster=id ,IsDelete = False).select_related("BeverageRevenueMaster")
    mem1 = FoodRevenueEntryDetail.objects.filter(FB_ODCEntryMaster =id ,IsDelete=False ).select_related("FoodRevenueMaster")
    mem = FB_ODCEntryMaster.objects.get(id = id)
     
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'FBODC/FBODCEdit.html' , {'mem1' :mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'mem':mem ,'CYear':range(2022,CYear)})

def FB_ODCView(request, id):
    template_path = "FBODC/FBODCView.html"
    mem4 = FB_ODCEntryDetail.objects.filter( FB_ODCEntryMaster=id ,IsDelete = False).select_related("FB_ODCMaster")  
    mem3 = TotalOtherIncomeEntryDetail.objects.filter( FB_ODCEntryMaster=id ,IsDelete = False).select_related("TotalOtherIncomeMaster")       
    mem2 = BeverageRevenueEntryDetail.objects.filter( FB_ODCEntryMaster=id ,IsDelete = False).select_related("BeverageRevenueMaster")
    mem1 = FoodRevenueEntryDetail.objects.filter(FB_ODCEntryMaster =id ,IsDelete=False ).select_related("FoodRevenueMaster")
    mem = FB_ODCEntryMaster.objects.get(id = id)
  
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'mem2':mem2,'mem3':mem3, 'mem4':mem4, 'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 



  
def HFB_BanquetList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = FBBanquet_EnrtyMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'FB_BanquetHB/FBBanquetList.html' ,{'mem' :mem }) 
                            
                            
def HFB_BanquetEntry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")       
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST["BeverageRevenue"]
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        RoomHireRevenue = request.POST["RoomHireRevenue"]
        if(RoomHireRevenue == ''):
            RoomHireRevenue = 0
        AudioVisualRevenue = request.POST['AudioVisualRevenue']
        if(AudioVisualRevenue == ''):
            AudioVisualRevenue = 0
        ServiceChargeRevenue = request.POST['ServiceChargeRevenue']
        if(ServiceChargeRevenue == ''):
            ServiceChargeRevenue =0
        FBRevenueOthers = request.POST['FBRevenueOthers']
        if(FBRevenueOthers == ''):
            FBRevenueOthers =0  
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0        
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0 
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0 
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev = 0 
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0 
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages=0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives==''):
            Bonuses_and_Incentives=0   
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome==''):
            DepartmentIncome=0

        enmaster = FBBanquet_EnrtyMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,
                                    FoodRevenue=FoodRevenue ,SalaryAndWages = SalaryAndWages ,
                                   BeverageRevenue=BeverageRevenue,RoomHireRevenue=RoomHireRevenue,
                                    FBRevenueOthers=FBRevenueOthers, FoodCostOfSales=FoodCostOfSales,
                                    TotalOtherIncome=TotalOtherIncome,
                                    BeverageCostOfSales=BeverageCostOfSales,AudioVisualRevenue=AudioVisualRevenue,                                   
                                    TotalCostOfFbSales=TotalCostOfFbSales,AudioVisualEquipmentCostOfSales=AudioVisualEquipmentCostOfSales,
                                    FBOtherCostOfSales=FBOtherCostOfSales,TotalCostOfOtherRev=TotalCostOfOtherRev,
                                    TotalCostOfSales=TotalCostOfSales,Gross_Profit=Gross_Profit,FBRevenue=FBRevenue,
                                 Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               DepartmentIncome = DepartmentIncome , 
                             OrganizationID=OrganizationID,CreatedBy=UserID    )
        enmaster.save()
 
        
        TotalItemFood = request.POST["TotalItemFood"]
        EntObj =  FBBanquet_EnrtyMaster.objects.get(id=enmaster.pk)
        
        for x in range(int(TotalItemFood)+1):
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 ==''):
                Amount1 = 0
                
            FTitleID_ = request.POST["FTitleID_" + str(x)]        
            FTitleObj =  FoodRevenueBanquet_Master.objects.get(id = FTitleID_)           
        
            v = FoodRevenueBanquet_EntryDetail.objects.create(Amount1 = Amount1, 
                             FoodRevenueBanquet_Master = FTitleObj , FBBanquet_EnrtyMaster = EntObj  )   
          
            
        TotalItemBeverage = request.POST["TotalItemBeverage"]
        for x in range(int(TotalItemBeverage)+1):
            Amount2 = request.POST["BAmount_" + str(x)]
            if( Amount2 ==''):
                 Amount2 = 0
                
            BTitleID_ = request.POST["BTitleID_"+ str(x)]        
            BTitleObj =  BeverageRevenueBanquet_Master.objects.get(id = BTitleID_)
                   
            v1 = BeverageRevenueBanquet_EntryDetail.objects.create( Amount2 =  Amount2, 
                     BeverageRevenueBanquet_Master = BTitleObj ,FBBanquet_EnrtyMaster = EntObj )         
              
              
        TotalItemBanquet = request.POST["TotalItemBanquet"]
        for x in range(int(TotalItemBanquet)+1):
            Amount3 = request.POST["FBAmount_" + str(x)]
            if( Amount3 ==''):
                 Amount3 = 0
                
            FBTitleID_ = request.POST["FBTitleID_" + str(x)]        
            FBTitleObj =  FBBanquet_Master.objects.get(id = FBTitleID_)
                   
            v2 = FBBanquet_EntryDetail.objects.create( Amount3 =  Amount3, 
                     FBBanquet_Master = FBTitleObj ,FBBanquet_EnrtyMaster = EntObj )         
              
                
        return(redirect('/HotelBudget/HFB_BanquetList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  FoodRevenueBanquet_Master.objects.filter(IsDelete = False)  
    mem1 = BeverageRevenueBanquet_Master.objects.filter(IsDelete = False)
    mem2 = FBBanquet_Master.objects.filter(IsDelete = False)
    return render(request , 'FB_BanquetHB/FBBanquetEntry.html' ,{'mem':mem ,'mem1':mem1,'mem2':mem2, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def FB_BanquetDelete(request,id):
    mem =  FBBanquet_EnrtyMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HFB_BanquetList'))


def HFB_BanquetEdit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST["BeverageRevenue"]
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        RoomHireRevenue = request.POST["RoomHireRevenue"]
        if(RoomHireRevenue == ''):
            RoomHireRevenue = 0
        AudioVisualRevenue = request.POST['AudioVisualRevenue']
        if(AudioVisualRevenue == ''):
            AudioVisualRevenue = 0
        ServiceChargeRevenue = request.POST['ServiceChargeRevenue']
        if(ServiceChargeRevenue == ''):
            ServiceChargeRevenue =0
        FBRevenueOthers = request.POST['FBRevenueOthers']
        if(FBRevenueOthers == ''):
            FBRevenueOthers =0  
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0        
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0 
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0 
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev = 0 
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0 
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages=0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives==''):
            Bonuses_and_Incentives=0   
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome==''):
            DepartmentIncome=0

        mem =  FBBanquet_EnrtyMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue = FoodRevenue
        mem.BeverageRevenue = BeverageRevenue
        mem.RoomHireRevenue = RoomHireRevenue 
        mem.AudioVisualRevenue = AudioVisualRevenue
        mem.ServiceChargeRevenue = ServiceChargeRevenue
        mem.FBRevenueOthers = FBRevenueOthers
        mem.TotalOtherIncome = TotalOtherIncome        
        mem.FBRevenue = FBRevenue
        mem.FoodCostOfSales = FoodCostOfSales
        mem.BeverageCostOfSales = BeverageCostOfSales
        mem.TotalCostOfFbSales = TotalCostOfFbSales
        mem.AudioVisualEquipmentCostOfSales = AudioVisualEquipmentCostOfSales
        mem.FBOtherCostOfSales = FBOtherCostOfSales
        mem.TotalCostOfOtherRev = TotalCostOfOtherRev
        mem.TotalCostOfSales = TotalCostOfSales
        mem.Gross_Profit = Gross_Profit        
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives =  Bonuses_and_Incentives
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.DepartmentIncome =  DepartmentIncome 
        
        mem.save()
            
        TotalItemFood  = request.POST["TotalItemFood"]
        for x in range(int( TotalItemFood ) +1):
           
            FTitleID_ = request.POST["FTitleID_" + str(x)]
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 == ''):
                Amount1 =0
            
            sv = FoodRevenueBanquet_EntryDetail.objects.get(FoodRevenueBanquet_Master = FTitleID_ , FBBanquet_EnrtyMaster = id)
            sv.Amount1  =  Amount1 
            sv.save()
            
               
        TotalItemBeverage   = request.POST["TotalItemBeverage"]
        for x in range(int( TotalItemBeverage  ) +1):
           
            BTitleID_ = request.POST["BTitleID_" + str(x)]
            Amount2 = request.POST["BAmount_" + str(x)]
            if(Amount2 == ''):
                Amount2 =0
            
            sv = BeverageRevenueBanquet_EntryDetail.objects.get(BeverageRevenueBanquet_Master = BTitleID_ , FBBanquet_EnrtyMaster = id)
            sv.Amount2  =  Amount2 
            sv.save()
            
        TotalItemBanquet   = request.POST["TotalItemBanquet"]
        for x in range(int( TotalItemBanquet ) +1):
           
            FBTitleID_ = request.POST["FBTitleID_" + str(x)]
            Amount3 = request.POST["FBAmount_" + str(x)]
            if(Amount3 == ''):
                Amount3 =0
            
            sv = FBBanquet_EntryDetail.objects.get(FBBanquet_Master = FBTitleID_ , FBBanquet_EnrtyMaster = id)
            sv.Amount3  =  Amount3 
            sv.save()
            
        return(redirect('/HotelBudget/HFB_BanquetList'))
    
    mem3 = FBBanquet_EntryDetail.objects.filter( FBBanquet_EnrtyMaster=id ,IsDelete = False).select_related("FBBanquet_Master")       
    mem2 = BeverageRevenueBanquet_EntryDetail.objects.filter( FBBanquet_EnrtyMaster=id ,IsDelete = False).select_related("BeverageRevenueBanquet_Master")
    mem1 = FoodRevenueBanquet_EntryDetail.objects.filter(FBBanquet_EnrtyMaster =id ,IsDelete=False ).select_related("FoodRevenueBanquet_Master")
    mem = FBBanquet_EnrtyMaster.objects.get(id = id)
     
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'FB_BanquetHB/FBBanquetEdit.html' , {'mem1' :mem1 ,'mem2':mem2,'mem3':mem3, 'mem':mem ,'CYear':range(2022,CYear)})

def HFB_BanquetView(request, id):
    template_path = "FB_BanquetHB/FB_BanquetView.html"
    mem3 = FBBanquet_EntryDetail.objects.filter( FBBanquet_EnrtyMaster=id ,IsDelete = False).select_related("FBBanquet_Master")       
    mem2 = BeverageRevenueBanquet_EntryDetail.objects.filter( FBBanquet_EnrtyMaster=id ,IsDelete = False).select_related("BeverageRevenueBanquet_Master")
    mem1 = FoodRevenueBanquet_EntryDetail.objects.filter(FBBanquet_EnrtyMaster =id ,IsDelete=False ).select_related("FoodRevenueBanquet_Master")
    mem = FBBanquet_EnrtyMaster.objects.get(id = id)
  
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'mem2':mem2,'mem3':mem3, 'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 




def FB_MiniBarList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = FB_MiniBar_EnrtyMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'FB_MiniBar/FB_MiniBarList.html' ,{'mem' :mem }) 
                            
                            
                            
def FB_MiniBarEntry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")       
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        MiniBarRevenue = request.POST['MiniBarRevenue']
        if(MiniBarRevenue == ''):
            MiniBarRevenue =0
        BeverageRevenue = request.POST["BeverageRevenue"]
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0        
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0 
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0 
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev = 0 
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0 
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages=0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives==''):
            Bonuses_and_Incentives=0   
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome==''):
            DepartmentIncome=0

        enmaster = FB_MiniBar_EnrtyMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,
                                    FoodRevenue=FoodRevenue ,SalaryAndWages = SalaryAndWages ,
                                   BeverageRevenue=BeverageRevenue,
                                     FoodCostOfSales=FoodCostOfSales,
                                    TotalOtherIncome=TotalOtherIncome,MiniBarRevenue=MiniBarRevenue,
                                    BeverageCostOfSales=BeverageCostOfSales,                                   
                                    TotalCostOfFbSales=TotalCostOfFbSales,AudioVisualEquipmentCostOfSales=AudioVisualEquipmentCostOfSales,
                                    FBOtherCostOfSales=FBOtherCostOfSales,TotalCostOfOtherRev=TotalCostOfOtherRev,
                                    TotalCostOfSales=TotalCostOfSales,Gross_Profit=Gross_Profit,FBRevenue=FBRevenue,
                                 Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               DepartmentIncome = DepartmentIncome , 
                             OrganizationID=OrganizationID,CreatedBy=UserID    )
        enmaster.save()
 
        
        TotalItemFood = request.POST["TotalItemFood"]
        EntObj =  FB_MiniBar_EnrtyMaster.objects.get(id=enmaster.pk)
        
        for x in range(int(TotalItemFood)+1):
            Amount2 = request.POST["FAmount_" + str(x)]
            if(Amount2 ==''):
                Amount2 = 0
                
            FTitleID_ = request.POST["FTitleID_" + str(x)]        
            FTitleObj =  FB_MiniBar_FoodRevenue_Master.objects.get(id = FTitleID_)           
        
            v = FB_MiniBar_FoodRevenue_EntryDetail.objects.create(Amount2 = Amount2, 
                             FB_MiniBar_FoodRevenue_Master = FTitleObj , FB_MiniBar_EnrtyMaster = EntObj  )   
          
            
        TotalOtherItem = request.POST["TotalOtherItem"]
        for x in range(int(TotalOtherItem)+1):
            Amount3 = request.POST["OAmount_" + str(x)]
            if( Amount3 ==''):
                 Amount3 = 0
                
            OTitleID_ = request.POST["OTitleID_"+ str(x)]        
            OTitleObj =  FB_MiniBar_TotalOtherIncome_Master.objects.get(id = OTitleID_)
                   
            v1 = FB_MiniBar_TotalOtherIncome_EntryDetail.objects.create( Amount3 =  Amount3, 
                     FB_MiniBar_TotalOtherIncome_Master = OTitleObj ,FB_MiniBar_EnrtyMaster = EntObj )         
              
              
        TotalItemFBMiniBar = request.POST["TotalItemFBMiniBar"]
        for x in range(int(TotalItemFBMiniBar)+1):
            Amount1 = request.POST["FBAmount_" + str(x)]
            if( Amount1 ==''):
                 Amount1 = 0
                
            FBTitleID_ = request.POST["FBTitleID_" + str(x)]        
            FBTitleObj =  FB_MiniBar_Master.objects.get(id = FBTitleID_)
                   
            v2 = FB_MiniBar_EntryDetail.objects.create( Amount1 =  Amount1, 
                     FB_MiniBar_Master = FBTitleObj ,FB_MiniBar_EnrtyMaster = EntObj )         
              
                
        return(redirect('/HotelBudget/FB_MiniBarList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  FB_MiniBar_FoodRevenue_Master.objects.filter(IsDelete = False)  
    mem1 = FB_MiniBar_TotalOtherIncome_Master.objects.filter(IsDelete = False)
    mem2 = FB_MiniBar_Master.objects.filter(IsDelete = False)
    return render(request , 'FB_MiniBar/FB_MiniBarEntry.html' ,{'mem':mem ,'mem1':mem1,'mem2':mem2, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def FB_MiniBarDelete(request,id):
    mem =  FB_MiniBar_EnrtyMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/FB_MiniBarList'))



def FB_MiniBarEdit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        MiniBarRevenue = request.POST['MiniBarRevenue']
        if(MiniBarRevenue == ''):
            MiniBarRevenue =0
        BeverageRevenue = request.POST["BeverageRevenue"]
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0        
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0 
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0 
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev = 0 
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0 
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages=0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives==''):
            Bonuses_and_Incentives=0   
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome==''):
            DepartmentIncome=0


        mem =  FB_MiniBar_EnrtyMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue = FoodRevenue
        mem.BeverageRevenue = BeverageRevenue
        mem.MiniBarRevenue = MiniBarRevenue 
        mem.TotalOtherIncome = TotalOtherIncome        
        mem.FBRevenue = FBRevenue
        mem.FoodCostOfSales = FoodCostOfSales
        mem.BeverageCostOfSales = BeverageCostOfSales
        mem.TotalCostOfFbSales = TotalCostOfFbSales
        mem.AudioVisualEquipmentCostOfSales = AudioVisualEquipmentCostOfSales
        mem.FBOtherCostOfSales = FBOtherCostOfSales
        mem.TotalCostOfOtherRev = TotalCostOfOtherRev
        mem.TotalCostOfSales = TotalCostOfSales
        mem.Gross_Profit = Gross_Profit        
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives =  Bonuses_and_Incentives
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.DepartmentIncome =  DepartmentIncome 
        
        mem.save()
            
        TotalItemFood  = request.POST["TotalItemFood"]
        for x in range(int( TotalItemFood ) +1):
           
            FTitleID_ = request.POST["FTitleID_" + str(x)]
            Amount2 = request.POST["FAmount_" + str(x)]
            if(Amount2 == ''):
                Amount2 =0
            
            sv = FB_MiniBar_FoodRevenue_EntryDetail.objects.get(FB_MiniBar_FoodRevenue_Master = FTitleID_ , FB_MiniBar_EnrtyMaster = id)
            sv.Amount2  =  Amount2 
            sv.save()
            
               
        TotalOtherItem   = request.POST["TotalOtherItem"]
        for x in range(int( TotalOtherItem  ) +1):
           
            OTitleID_ = request.POST["OTitleID_" + str(x)]
            Amount3 = request.POST["OAmount_" + str(x)]
            if(Amount3 == ''):
                Amount3 =0
            
            sv = FB_MiniBar_TotalOtherIncome_EntryDetail.objects.get(FB_MiniBar_TotalOtherIncome_Master = OTitleID_ , FB_MiniBar_EnrtyMaster = id)
            sv.Amount3  =  Amount3 
            sv.save()
            
        TotalItemFBMiniBar   = request.POST["TotalItemFBMiniBar"]
        for x in range(int( TotalItemFBMiniBar ) +1):
           
            FBTitleID_ = request.POST["FBTitleID_" + str(x)]
            Amount1 = request.POST["FBAmount_" + str(x)]
            if(Amount1 == ''):
                Amount1 =0
            
            sv = FB_MiniBar_EntryDetail.objects.get(FB_MiniBar_Master = FBTitleID_ , FB_MiniBar_EnrtyMaster = id)
            sv.Amount1  =  Amount1 
            sv.save()
            
        return(redirect('/HotelBudget/FB_MiniBarList'))
    
    mem3 = FB_MiniBar_EntryDetail.objects.filter( FB_MiniBar_EnrtyMaster=id ,IsDelete = False).select_related("FB_MiniBar_Master")       
    mem2 = FB_MiniBar_TotalOtherIncome_EntryDetail.objects.filter( FB_MiniBar_EnrtyMaster=id ,IsDelete = False).select_related("FB_MiniBar_TotalOtherIncome_Master")
    mem1 = FB_MiniBar_FoodRevenue_EntryDetail.objects.filter(FB_MiniBar_EnrtyMaster =id ,IsDelete=False ).select_related("FB_MiniBar_FoodRevenue_Master")
    mem = FB_MiniBar_EnrtyMaster.objects.get(id = id)
     
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'FB_MiniBar/FB_MiniBarEdit.html' , {'mem1' :mem1 ,'mem2':mem2,'mem3':mem3, 'mem':mem ,'CYear':range(2022,CYear)})


def FB_MiniBarView(request, id):
    template_path = "FB_MiniBar/FB_MiniBarView.html"
    mem3 = FB_MiniBar_EntryDetail.objects.filter( FB_MiniBar_EnrtyMaster=id ,IsDelete = False).select_related("FB_MiniBar_Master")       
    mem2 = FB_MiniBar_TotalOtherIncome_EntryDetail.objects.filter( FB_MiniBar_EnrtyMaster=id ,IsDelete = False).select_related("FB_MiniBar_TotalOtherIncome_Master")
    mem1 = FB_MiniBar_FoodRevenue_EntryDetail.objects.filter(FB_MiniBar_EnrtyMaster =id ,IsDelete=False ).select_related("FB_MiniBar_FoodRevenue_Master")
    mem = FB_MiniBar_EnrtyMaster.objects.get(id = id)
  
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'mem2':mem2,'mem3':mem3, 'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 


  
def HFB_IRDList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = FB_IRD_EnrtyMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'FB_IRDHB/FB_IRDList.html' ,{'mem' :mem }) 
                            
                            
                            
def HFB_IRDEntry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")       
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST["BeverageRevenue"]
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0        
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0 
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0 
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev = 0 
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0 
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages=0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives==''):
            Bonuses_and_Incentives=0   
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome==''):
            DepartmentIncome=0

        enmaster = FB_IRD_EnrtyMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,
                                    FoodRevenue=FoodRevenue ,SalaryAndWages = SalaryAndWages ,
                                   BeverageRevenue=BeverageRevenue,
                                     FoodCostOfSales=FoodCostOfSales,
                                    TotalOtherIncome=TotalOtherIncome,
                                    BeverageCostOfSales=BeverageCostOfSales,                                  
                                    TotalCostOfFbSales=TotalCostOfFbSales,AudioVisualEquipmentCostOfSales=AudioVisualEquipmentCostOfSales,
                                    FBOtherCostOfSales=FBOtherCostOfSales,TotalCostOfOtherRev=TotalCostOfOtherRev,
                                    TotalCostOfSales=TotalCostOfSales,Gross_Profit=Gross_Profit,FBRevenue=FBRevenue,
                                 Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               DepartmentIncome = DepartmentIncome , 
                             OrganizationID=OrganizationID,CreatedBy=UserID    )
        enmaster.save()
 
        
           
        TotalItemFood = request.POST["TotalItemFood"]
        EntObj =  FB_IRD_EnrtyMaster.objects.get(id=enmaster.pk)
       
        for x in range(int(TotalItemFood)+1):
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 ==''):
                Amount1 = 0
                
            FTitleID_ = request.POST["FTitleID_" + str(x)]        
            FTitleObj =   FBIRD_FoodRevenue_Master.objects.get(id = FTitleID_)           
        
            v = FB_IRD_FoodRevenue_EntryDetail.objects.create(Amount1 = Amount1, 
                             FBIRD_FoodRevenue_Master = FTitleObj , FB_IRD_EnrtyMaster = EntObj  )   
          
            
        TotalItemBeverage = request.POST["TotalItemBeverage"]
        for x in range(int(TotalItemBeverage)+1):
            Amount2 = request.POST["BAmount_" + str(x)]
            if( Amount2 ==''):
                 Amount2 = 0
                
            BTitleID_ = request.POST["BTitleID_"+ str(x)]        
            BTitleObj =  FBIRD_BeverageRevenue_Master.objects.get(id = BTitleID_)
                   
            v1 = FBIRD_BeverageRevenue_Maste_EntryDetail.objects.create( Amount2 =  Amount2, 
                     FBIRD_BeverageRevenue_Master = BTitleObj ,FB_IRD_EnrtyMaster = EntObj )         
                           
             
        TotalOtherItem = request.POST["TotalOtherItem"]
        for x in range(int(TotalOtherItem)+1):
            Amount3 = request.POST["OAmount_" + str(x)]
            if( Amount3 ==''):
                 Amount3 = 0
                
            OTitleID_ = request.POST["OTitleID_"+ str(x)]        
            OTitleObj =   FBIRD_TotalOtherIncome_Master.objects.get(id = OTitleID_)
                   
            v1 = FBIRD_TotalOtherIncome_MasterIncome_EntryDetail.objects.create( Amount3 =  Amount3, 
                      FBIRD_TotalOtherIncome_Master = OTitleObj ,FB_IRD_EnrtyMaster = EntObj )         
                      
              
              
        TotalFBIRDItem = request.POST["TotalFBIRDItem"]
        for x in range(int(TotalFBIRDItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if( Amount ==''):
                 Amount = 0
                
            TitleID_ = request.POST["TitleID_"+ str(x)]        
            TitleObj =  FBIRD_Master.objects.get(id = TitleID_)
                   
            v1 = FB_IRD_EntryDetail.objects.create( Amount =  Amount, 
                     FBIRD_Master = TitleObj ,FB_IRD_EnrtyMaster = EntObj )         
              
                
        return(redirect('/HotelBudget/HFB_IRDList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  FBIRD_FoodRevenue_Master.objects.filter(IsDelete = False)  
    mem1 = FBIRD_BeverageRevenue_Master.objects.filter(IsDelete = False)
    mem2 = FBIRD_TotalOtherIncome_Master.objects.filter(IsDelete = False)
    mem3 =  FBIRD_Master.objects.filter(IsDelete = False)
    return render(request , 'FB_IRDHB/FB_IRDEntry.html' ,{'mem':mem ,'mem1':mem1,'mem2':mem2,'mem3':mem3, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def HFB_IRDDelete(request,id):
    mem =  FB_IRD_EnrtyMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HFB_IRDList'))



def HFB_IRDEdit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue ==''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales == ''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0
        Gross_Profit = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
            Salary_Wages_and_Bonuses = 0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits == ''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses ==''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0

        mem =  FB_ODCEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue = FoodRevenue
        mem.BeverageRevenue = BeverageRevenue
        mem.TotalOtherIncome = TotalOtherIncome
        mem.FBRevenue = FBRevenue
        mem.FoodCostOfSales = FoodCostOfSales
        mem.BeverageCostOfSales = BeverageCostOfSales
        mem.TotalCostOfFbSales = TotalCostOfFbSales
        mem.AudioVisualEquipmentCostOfSales = AudioVisualEquipmentCostOfSales
        mem.FBOtherCostOfSales = FBOtherCostOfSales
        mem.TotalCostOfOtherRev = TotalCostOfOtherRev
        mem.TotalCostOfSales = TotalCostOfSales
        mem.Gross_Profit = Gross_Profit        
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives =  Bonuses_and_Incentives
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.DepartmentIncome =  DepartmentIncome 
        
        mem.save()
        
        TotalFBIRDItem = request.POST["TotalFBIRDItem"]
        for x in range(int(    TotalFBIRDItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem =  FB_IRD_EnrtyMaster.objects.get(id = id)
            sv =  FB_IRD_EntryDetail.objects.get(FBIRD_Master = TitleID_ , FB_IRD_EnrtyMaster = id)
            sv.Amount =  Amount
            sv.save()
            
            
        TotalItemFood  = request.POST["TotalItemFood"]
        for x in range(int( TotalItemFood ) +1):
           
            FTitleID_ = request.POST["FTitleID_" + str(x)]
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 == ''):
                Amount1 =0
            
            sv = FB_IRD_FoodRevenue_EntryDetail.objects.get(FBIRD_FoodRevenue_Master = FTitleID_ , FB_IRD_EnrtyMaster = id)
            sv.Amount1  =  Amount1 
            sv.save()
            
               
        TotalItemBeverage   = request.POST["TotalItemBeverage"]
        for x in range(int( TotalItemBeverage  ) +1):
           
            BTitleID_ = request.POST["BTitleID_" + str(x)]
            Amount2 = request.POST["BAmount_" + str(x)]
            if(Amount2 == ''):
                Amount2 =0
            
            sv = FBIRD_BeverageRevenue_Maste_EntryDetail.objects.get(FBIRD_BeverageRevenue_Master = BTitleID_ , FB_IRD_EnrtyMaster = id)
            sv.Amount2  =  Amount2 
            sv.save()
            
        TotalOtherItem   = request.POST["TotalOtherItem"]
        for x in range(int( TotalOtherItem ) +1):
           
            OTitleID_ = request.POST["OTitleID_" + str(x)]
            Amount3 = request.POST["OAmount_" + str(x)]
            if(Amount3 == ''):
                Amount3 =0
            
            sv = FBIRD_TotalOtherIncome_MasterIncome_EntryDetail.objects.get(FBIRD_TotalOtherIncome_Master = OTitleID_ , FB_IRD_EnrtyMaster = id)
            sv.Amount3  =  Amount3 
            sv.save()
            
        return(redirect('/HotelBudget/HFB_IRDList'))
    
    mem4 = FB_IRD_EntryDetail.objects.filter( FB_IRD_EnrtyMaster=id ,IsDelete = False).select_related("FBIRD_Master")  
    mem3 = FBIRD_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( FB_IRD_EnrtyMaster=id ,IsDelete = False).select_related("FBIRD_TotalOtherIncome_Master")       
    mem2 = FBIRD_BeverageRevenue_Maste_EntryDetail.objects.filter( FB_IRD_EnrtyMaster=id ,IsDelete = False).select_related("FBIRD_BeverageRevenue_Master")
    mem1 = FB_IRD_FoodRevenue_EntryDetail.objects.filter(FB_IRD_EnrtyMaster =id ,IsDelete=False ).select_related("FBIRD_FoodRevenue_Master")
    mem = FB_IRD_EnrtyMaster.objects.get(id = id)
     
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'FB_IRDHB/FB_IRDEdit.html' , {'mem1' :mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'mem':mem ,'CYear':range(2022,CYear)})



def HFB_IRDView(request, id):
    template_path = "FB_IRDHB/FB_IRDView.html"
    mem4 = FB_IRD_EntryDetail.objects.filter( FB_IRD_EnrtyMaster=id ,IsDelete = False).select_related("FBIRD_Master")       
    mem3 = FBIRD_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( FB_IRD_EnrtyMaster=id ,IsDelete = False).select_related("FBIRD_TotalOtherIncome_Master")
    mem2 = FBIRD_BeverageRevenue_Maste_EntryDetail.objects.filter(FB_IRD_EnrtyMaster =id ,IsDelete=False ).select_related("FBIRD_BeverageRevenue_Master")
    mem1 = FB_IRD_FoodRevenue_EntryDetail.objects.filter(FB_IRD_EnrtyMaster =id ,IsDelete=False ).select_related("FBIRD_FoodRevenue_Master")
    mem = FB_IRD_EnrtyMaster.objects.get(id = id)
  
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 


  
def HOutlet1_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Outlet1_EnrtyMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'Outlet1_HB/Outlet1List.html' ,{'mem' :mem }) 
                            
                            
                          
def HOutlet1_Entry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")       
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST["BeverageRevenue"]
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0        
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0 
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0 
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev = 0 
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0 
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages=0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives==''):
            Bonuses_and_Incentives=0   
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome==''):
            DepartmentIncome=0

        enmaster = Outlet1_EnrtyMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,
                                    FoodRevenue=FoodRevenue ,SalaryAndWages = SalaryAndWages ,
                                   BeverageRevenue=BeverageRevenue,
                                     FoodCostOfSales=FoodCostOfSales,
                                    TotalOtherIncome=TotalOtherIncome,
                                    BeverageCostOfSales=BeverageCostOfSales,                                  
                                    TotalCostOfFbSales=TotalCostOfFbSales,AudioVisualEquipmentCostOfSales=AudioVisualEquipmentCostOfSales,
                                    FBOtherCostOfSales=FBOtherCostOfSales,TotalCostOfOtherRev=TotalCostOfOtherRev,
                                    TotalCostOfSales=TotalCostOfSales,Gross_Profit=Gross_Profit,FBRevenue=FBRevenue,
                                 Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               DepartmentIncome = DepartmentIncome , 
                             OrganizationID=OrganizationID,CreatedBy=UserID    )
        enmaster.save()
 
        
           
        TotalItemFood = request.POST["TotalItemFood"]
        EntObj =  Outlet1_EnrtyMaster.objects.get(id=enmaster.pk)
       
        for x in range(int(TotalItemFood)+1):
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 ==''):
                Amount1 = 0
                
            FTitleID_ = request.POST["FTitleID_" + str(x)]        
            FTitleObj =   Outlet1_FoodRevenue_Master.objects.get(id = FTitleID_)           
        
            v = Outlet1_FoodRevenue_EntryDetail.objects.create(Amount1 = Amount1, 
                             Outlet1_FoodRevenue_Master = FTitleObj , Outlet1_EnrtyMaster = EntObj  )   
          
            
        TotalItemBeverage = request.POST["TotalItemBeverage"]
        for x in range(int(TotalItemBeverage)+1):
            Amount2 = request.POST["BAmount_" + str(x)]
            if( Amount2 ==''):
                 Amount2 = 0
                
            BTitleID_ = request.POST["BTitleID_"+ str(x)]        
            BTitleObj =  Outlet1_BeverageRevenue_Master.objects.get(id = BTitleID_)
                   
            v1 = Outlet1_BeverageRevenue_Maste_EntryDetail.objects.create( Amount2 =  Amount2, 
                     Outlet1_BeverageRevenue_Master = BTitleObj ,Outlet1_EnrtyMaster = EntObj )         
                           
             
        TotalOtherItem = request.POST["TotalOtherItem"]
        for x in range(int(TotalOtherItem)+1):
            Amount3 = request.POST["OAmount_" + str(x)]
            if( Amount3 ==''):
                 Amount3 = 0
                
            OTitleID_ = request.POST["OTitleID_"+ str(x)]        
            OTitleObj =   Outlet1_TotalOtherIncome_Master.objects.get(id = OTitleID_)
                   
            v1 = Outlet1_TotalOtherIncome_MasterIncome_EntryDetail.objects.create( Amount3 =  Amount3, 
                      Outlet1_TotalOtherIncome_Master = OTitleObj ,Outlet1_EnrtyMaster = EntObj )         
                      
              
              
        TotalOutlet1Item = request.POST["TotalOutlet1Item"]
        for x in range(int(TotalOutlet1Item)+1):
            Amount = request.POST["Amount_" + str(x)]
            if( Amount ==''):
                 Amount = 0
                
            TitleID_ = request.POST["TitleID_"+ str(x)]        
            TitleObj =  Outlet1_Master.objects.get(id = TitleID_)
                   
            v1 = Outlet1_EntryDetail.objects.create( Amount =  Amount, 
                     Outlet1_Master = TitleObj ,Outlet1_EnrtyMaster = EntObj )         
              
                
        return(redirect('/HotelBudget/HOutlet1_List'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  Outlet1_FoodRevenue_Master.objects.filter(IsDelete = False)  
    mem1 = Outlet1_BeverageRevenue_Master.objects.filter(IsDelete = False)
    mem2 = Outlet1_TotalOtherIncome_Master.objects.filter(IsDelete = False)
    mem3 =  Outlet1_Master.objects.filter(IsDelete = False)
    return render(request , 'Outlet1_HB/Outlet1Entry.html' ,{'mem':mem ,'mem1':mem1,'mem2':mem2,'mem3':mem3, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def HOutlet1_Delete(request,id):
    mem =  Outlet1_EnrtyMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HOutlet1_List'))




def HOutlet1_Edit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue ==''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales == ''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0
        Gross_Profit = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
            Salary_Wages_and_Bonuses = 0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits == ''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses ==''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0

        mem =  Outlet1_EnrtyMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue = FoodRevenue
        mem.BeverageRevenue = BeverageRevenue
        mem.TotalOtherIncome = TotalOtherIncome
        mem.FBRevenue = FBRevenue
        mem.FoodCostOfSales = FoodCostOfSales
        mem.BeverageCostOfSales = BeverageCostOfSales
        mem.TotalCostOfFbSales = TotalCostOfFbSales
        mem.AudioVisualEquipmentCostOfSales = AudioVisualEquipmentCostOfSales
        mem.FBOtherCostOfSales = FBOtherCostOfSales
        mem.TotalCostOfOtherRev = TotalCostOfOtherRev
        mem.TotalCostOfSales = TotalCostOfSales
        mem.Gross_Profit = Gross_Profit        
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives =  Bonuses_and_Incentives
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.DepartmentIncome =  DepartmentIncome 
        
        mem.save()
        
        TotalOutlet1 = request.POST["TotalOutlet1"]
        for x in range(int( TotalOutlet1) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem =  Outlet1_EnrtyMaster.objects.get(id = id)
            sv =  Outlet1_EntryDetail.objects.get(Outlet1_Master = TitleID_ , Outlet1_EnrtyMaster = id)
            sv.Amount =  Amount
            sv.save()
            
            
        TotalItemFood  = request.POST["TotalItemFood"]
        for x in range(int( TotalItemFood ) +1):
           
            FTitleID_ = request.POST["FTitleID_" + str(x)]
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 == ''):
                Amount1 =0
            
            sv = Outlet1_FoodRevenue_EntryDetail.objects.get(Outlet1_FoodRevenue_Master = FTitleID_ , Outlet1_EnrtyMaster = id)
            sv.Amount1  =  Amount1 
            sv.save()
            
               
        TotalItemBeverage   = request.POST["TotalItemBeverage"]
        for x in range(int( TotalItemBeverage  ) +1):
           
            BTitleID_ = request.POST["BTitleID_" + str(x)]
            Amount2 = request.POST["BAmount_" + str(x)]
            if(Amount2 == ''):
                Amount2 =0
            
            sv = Outlet1_BeverageRevenue_Maste_EntryDetail.objects.get(Outlet1_BeverageRevenue_Master = BTitleID_ , Outlet1_EnrtyMaster = id)
            sv.Amount2  =  Amount2 
            sv.save()
            
        TotalOtherItem   = request.POST["TotalOtherItem"]
        for x in range(int( TotalOtherItem ) +1):
           
            OTitleID_ = request.POST["OTitleID_" + str(x)]
            Amount3 = request.POST["OAmount_" + str(x)]
            if(Amount3 == ''):
                Amount3 =0
            
            sv = Outlet1_TotalOtherIncome_MasterIncome_EntryDetail.objects.get(Outlet1_TotalOtherIncome_Master = OTitleID_ , Outlet1_EnrtyMaster = id)
            sv.Amount3  =  Amount3 
            sv.save()
            
        return(redirect('/HotelBudget/HOutlet1_List'))
    
    mem4 = Outlet1_EntryDetail.objects.filter( Outlet1_EnrtyMaster=id ,IsDelete = False).select_related("Outlet1_Master")  
    mem3 = Outlet1_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( Outlet1_EnrtyMaster=id ,IsDelete = False).select_related("Outlet1_TotalOtherIncome_Master")       
    mem2 = Outlet1_BeverageRevenue_Maste_EntryDetail.objects.filter( Outlet1_EnrtyMaster=id ,IsDelete = False).select_related("Outlet1_BeverageRevenue_Master")
    mem1 = Outlet1_FoodRevenue_EntryDetail.objects.filter(Outlet1_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet1_FoodRevenue_Master")
    mem = Outlet1_EnrtyMaster.objects.get(id = id)
     
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'Outlet1_HB/Outlet1Edit.html' , {'mem1' :mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'mem':mem ,'CYear':range(2022,CYear)})


def HOutlet1_View(request, id):
    template_path = "Outlet1_HB/Outlet1View.html"
    mem4 = Outlet1_EntryDetail.objects.filter( Outlet1_EnrtyMaster=id ,IsDelete = False).select_related("Outlet1_Master")       
    mem3 = Outlet1_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( Outlet1_EnrtyMaster=id ,IsDelete = False).select_related("Outlet1_TotalOtherIncome_Master")
    mem2 = Outlet1_BeverageRevenue_Maste_EntryDetail.objects.filter(Outlet1_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet1_BeverageRevenue_Master")
    mem1 = Outlet1_FoodRevenue_EntryDetail.objects.filter(Outlet1_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet1_FoodRevenue_Master")
    mem = Outlet1_EnrtyMaster.objects.get(id = id)
  
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 

  
  
  
def HOutlet2_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Outlet2_EnrtyMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'Outlet2_HB/Outlet2List.html' ,{'mem' :mem }) 
                            

                          
def HOutlet2_Entry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")       
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST["BeverageRevenue"]
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0        
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0 
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0 
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev = 0 
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0 
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages=0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives==''):
            Bonuses_and_Incentives=0   
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome==''):
            DepartmentIncome=0

        enmaster = Outlet2_EnrtyMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,
                                    FoodRevenue=FoodRevenue ,SalaryAndWages = SalaryAndWages ,
                                   BeverageRevenue=BeverageRevenue,
                                     FoodCostOfSales=FoodCostOfSales,
                                    TotalOtherIncome=TotalOtherIncome,
                                    BeverageCostOfSales=BeverageCostOfSales,                                  
                                    TotalCostOfFbSales=TotalCostOfFbSales,AudioVisualEquipmentCostOfSales=AudioVisualEquipmentCostOfSales,
                                    FBOtherCostOfSales=FBOtherCostOfSales,TotalCostOfOtherRev=TotalCostOfOtherRev,
                                    TotalCostOfSales=TotalCostOfSales,Gross_Profit=Gross_Profit,FBRevenue=FBRevenue,
                                 Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               DepartmentIncome = DepartmentIncome , 
                             OrganizationID=OrganizationID,CreatedBy=UserID    )
        enmaster.save()
 
        
           
        TotalItemFood = request.POST["TotalItemFood"]
        EntObj =  Outlet2_EnrtyMaster.objects.get(id=enmaster.pk)
       
        for x in range(int(TotalItemFood)+1):
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 ==''):
                Amount1 = 0
                
            FTitleID_ = request.POST["FTitleID_" + str(x)]        
            FTitleObj =   Outlet2_FoodRevenue_Master.objects.get(id = FTitleID_)           
        
            v = Outlet2_FoodRevenue_EntryDetail.objects.create(Amount1 = Amount1, 
                             Outlet2_FoodRevenue_Master = FTitleObj , Outlet2_EnrtyMaster = EntObj  )   
          
            
        TotalItemBeverage = request.POST["TotalItemBeverage"]
        for x in range(int(TotalItemBeverage)+1):
            Amount2 = request.POST["BAmount_" + str(x)]
            if( Amount2 ==''):
                 Amount2 = 0
                
            BTitleID_ = request.POST["BTitleID_"+ str(x)]        
            BTitleObj =  Outlet2_BeverageRevenue_Master.objects.get(id = BTitleID_)
                   
            v1 = Outlet2_BeverageRevenue_Maste_EntryDetail.objects.create( Amount2 =  Amount2, 
                     Outlet2_BeverageRevenue_Master = BTitleObj ,Outlet2_EnrtyMaster = EntObj )         
                           
             
        TotalOtherItem = request.POST["TotalOtherItem"]
        for x in range(int(TotalOtherItem)+1):
            Amount3 = request.POST["OAmount_" + str(x)]
            if( Amount3 ==''):
                 Amount3 = 0
                
            OTitleID_ = request.POST["OTitleID_"+ str(x)]        
            OTitleObj =   Outlet2_TotalOtherIncome_Master.objects.get(id = OTitleID_)
                   
            v1 = Outlet2_TotalOtherIncome_MasterIncome_EntryDetail.objects.create( Amount3 =  Amount3, 
                      Outlet2_TotalOtherIncome_Master = OTitleObj ,Outlet2_EnrtyMaster = EntObj )         
                      
              
              
        TotalOutlet1Item = request.POST["TotalOutlet1Item"]
        for x in range(int(TotalOutlet1Item)+1):
            Amount = request.POST["Amount_" + str(x)]
            if( Amount ==''):
                 Amount = 0
                
            TitleID_ = request.POST["TitleID_"+ str(x)]        
            TitleObj =  Outlet2_Master.objects.get(id = TitleID_)
                   
            v1 = Outlet2_EntryDetail.objects.create( Amount =  Amount, 
                     Outlet2_Master = TitleObj ,Outlet2_EnrtyMaster = EntObj )         
              
                
        return(redirect('/HotelBudget/HOutlet2_List'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  Outlet2_FoodRevenue_Master.objects.filter(IsDelete = False)  
    mem1 = Outlet2_BeverageRevenue_Master.objects.filter(IsDelete = False)
    mem2 = Outlet2_TotalOtherIncome_Master.objects.filter(IsDelete = False)
    mem3 =  Outlet2_Master.objects.filter(IsDelete = False)
    return render(request , 'Outlet2_HB/Outlet2Entry.html' ,{'mem':mem ,'mem1':mem1,'mem2':mem2,'mem3':mem3, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def HOutlet2_Delete(request,id):
    mem =  Outlet2_EnrtyMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HOutlet2_List'))



def HOutlet2_Edit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue ==''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales == ''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0
        Gross_Profit = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
            Salary_Wages_and_Bonuses = 0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits == ''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses ==''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0

        mem =  Outlet2_EnrtyMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue = FoodRevenue
        mem.BeverageRevenue = BeverageRevenue
        mem.TotalOtherIncome = TotalOtherIncome
        mem.FBRevenue = FBRevenue
        mem.FoodCostOfSales = FoodCostOfSales
        mem.BeverageCostOfSales = BeverageCostOfSales
        mem.TotalCostOfFbSales = TotalCostOfFbSales
        mem.AudioVisualEquipmentCostOfSales = AudioVisualEquipmentCostOfSales
        mem.FBOtherCostOfSales = FBOtherCostOfSales
        mem.TotalCostOfOtherRev = TotalCostOfOtherRev
        mem.TotalCostOfSales = TotalCostOfSales
        mem.Gross_Profit = Gross_Profit        
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives =  Bonuses_and_Incentives
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.DepartmentIncome =  DepartmentIncome 
        
        mem.save()
        
        TotalOutlet1 = request.POST["TotalOutlet1"]
        for x in range(int( TotalOutlet1) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem =  Outlet2_EnrtyMaster.objects.get(id = id)
            sv =  Outlet2_EntryDetail.objects.get(Outlet2_Master = TitleID_ , Outlet2_EnrtyMaster = id)
            sv.Amount =  Amount
            sv.save()
            
            
        TotalItemFood  = request.POST["TotalItemFood"]
        for x in range(int( TotalItemFood ) +1):
           
            FTitleID_ = request.POST["FTitleID_" + str(x)]
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 == ''):
                Amount1 =0
            
            sv = Outlet2_FoodRevenue_EntryDetail.objects.get(Outlet2_FoodRevenue_Master = FTitleID_ , Outlet2_EnrtyMaster = id)
            sv.Amount1  =  Amount1 
            sv.save()
            
               
        TotalItemBeverage   = request.POST["TotalItemBeverage"]
        for x in range(int( TotalItemBeverage  ) +1):
           
            BTitleID_ = request.POST["BTitleID_" + str(x)]
            Amount2 = request.POST["BAmount_" + str(x)]
            if(Amount2 == ''):
                Amount2 =0
            
            sv = Outlet2_BeverageRevenue_Maste_EntryDetail.objects.get(Outlet2_BeverageRevenue_Master = BTitleID_ , Outlet2_EnrtyMaster = id)
            sv.Amount2  =  Amount2 
            sv.save()
            
        TotalOtherItem   = request.POST["TotalOtherItem"]
        for x in range(int( TotalOtherItem ) +1):
           
            OTitleID_ = request.POST["OTitleID_" + str(x)]
            Amount3 = request.POST["OAmount_" + str(x)]
            if(Amount3 == ''):
                Amount3 =0
            
            sv = Outlet2_TotalOtherIncome_MasterIncome_EntryDetail.objects.get(Outlet2_TotalOtherIncome_Master = OTitleID_ , Outlet2_EnrtyMaster = id)
            sv.Amount3  =  Amount3 
            sv.save()
            
        return(redirect('/HotelBudget/HOutlet2_List'))
    
    mem4 = Outlet2_EntryDetail.objects.filter( Outlet2_EnrtyMaster=id ,IsDelete = False).select_related("Outlet2_Master")  
    mem3 = Outlet2_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( Outlet2_EnrtyMaster=id ,IsDelete = False).select_related("Outlet2_TotalOtherIncome_Master")       
    mem2 = Outlet2_BeverageRevenue_Maste_EntryDetail.objects.filter( Outlet2_EnrtyMaster=id ,IsDelete = False).select_related("Outlet2_BeverageRevenue_Master")
    mem1 = Outlet2_FoodRevenue_EntryDetail.objects.filter(Outlet2_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet2_FoodRevenue_Master")
    mem = Outlet2_EnrtyMaster.objects.get(id = id)
     
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'Outlet2_HB/Outlet2Edit.html' , {'mem1' :mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'mem':mem ,'CYear':range(2022,CYear)})


def HOutlet2_View(request, id):
    template_path = "Outlet2_HB/Outlet2View.html"
    mem4 = Outlet2_EntryDetail.objects.filter( Outlet2_EnrtyMaster=id ,IsDelete = False).select_related("Outlet2_Master")       
    mem3 = Outlet2_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( Outlet2_EnrtyMaster=id ,IsDelete = False).select_related("Outlet2_TotalOtherIncome_Master")
    mem2 = Outlet2_BeverageRevenue_Maste_EntryDetail.objects.filter(Outlet2_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet2_BeverageRevenue_Master")
    mem1 = Outlet2_FoodRevenue_EntryDetail.objects.filter(Outlet2_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet2_FoodRevenue_Master")
    mem = Outlet2_EnrtyMaster.objects.get(id = id)
  
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 


  
def HOutlet3_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Outlet3_EnrtyMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'Outlet3_HB/Outlet3List.html' ,{'mem' :mem }) 
                            
                            
                          
def HOutlet3_Entry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")       
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST["BeverageRevenue"]
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0        
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0 
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0 
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev = 0 
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0 
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages=0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives==''):
            Bonuses_and_Incentives=0   
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome==''):
            DepartmentIncome=0

        enmaster = Outlet3_EnrtyMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,
                                    FoodRevenue=FoodRevenue ,SalaryAndWages = SalaryAndWages ,
                                   BeverageRevenue=BeverageRevenue,
                                     FoodCostOfSales=FoodCostOfSales,
                                    TotalOtherIncome=TotalOtherIncome,
                                    BeverageCostOfSales=BeverageCostOfSales,                                  
                                    TotalCostOfFbSales=TotalCostOfFbSales,AudioVisualEquipmentCostOfSales=AudioVisualEquipmentCostOfSales,
                                    FBOtherCostOfSales=FBOtherCostOfSales,TotalCostOfOtherRev=TotalCostOfOtherRev,
                                    TotalCostOfSales=TotalCostOfSales,Gross_Profit=Gross_Profit,FBRevenue=FBRevenue,
                                 Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               DepartmentIncome = DepartmentIncome , 
                             OrganizationID=OrganizationID,CreatedBy=UserID    )
        enmaster.save()
 
        
           
        TotalItemFood = request.POST["TotalItemFood"]
        EntObj =  Outlet3_EnrtyMaster.objects.get(id=enmaster.pk)
       
        for x in range(int(TotalItemFood)+1):
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 ==''):
                Amount1 = 0
                
            FTitleID_ = request.POST["FTitleID_" + str(x)]        
            FTitleObj =   Outlet3_FoodRevenue_Master.objects.get(id = FTitleID_)           
        
            v = Outlet3_FoodRevenue_EntryDetail.objects.create(Amount1 = Amount1, 
                             Outlet3_FoodRevenue_Master = FTitleObj , Outlet3_EnrtyMaster = EntObj  )   
          
            
        TotalItemBeverage = request.POST["TotalItemBeverage"]
        for x in range(int(TotalItemBeverage)+1):
            Amount2 = request.POST["BAmount_" + str(x)]
            if( Amount2 ==''):
                 Amount2 = 0
                
            BTitleID_ = request.POST["BTitleID_"+ str(x)]        
            BTitleObj =  Outlet3_BeverageRevenue_Master.objects.get(id = BTitleID_)
                   
            v1 = Outlet3_BeverageRevenue_Maste_EntryDetail.objects.create( Amount2 =  Amount2, 
                     Outlet3_BeverageRevenue_Master = BTitleObj ,Outlet3_EnrtyMaster = EntObj )         
                           
             
        TotalOtherItem = request.POST["TotalOtherItem"]
        for x in range(int(TotalOtherItem)+1):
            Amount3 = request.POST["OAmount_" + str(x)]
            if( Amount3 ==''):
                 Amount3 = 0
                
            OTitleID_ = request.POST["OTitleID_"+ str(x)]        
            OTitleObj =   Outlet3_TotalOtherIncome_Master.objects.get(id = OTitleID_)
                   
            v1 = Outlet3_TotalOtherIncome_MasterIncome_EntryDetail.objects.create( Amount3 =  Amount3, 
                      Outlet3_TotalOtherIncome_Master = OTitleObj ,Outlet3_EnrtyMaster = EntObj )         
                      
              
              
        TotalOutlet1Item = request.POST["TotalOutlet1Item"]
        for x in range(int(TotalOutlet1Item)+1):
            Amount = request.POST["Amount_" + str(x)]
            if( Amount ==''):
                 Amount = 0
                
            TitleID_ = request.POST["TitleID_"+ str(x)]        
            TitleObj =  Outlet3_Master.objects.get(id = TitleID_)
                   
            v1 = Outlet3_EntryDetail.objects.create( Amount =  Amount, 
                     Outlet3_Master = TitleObj ,Outlet3_EnrtyMaster = EntObj )         
              
                
        return(redirect('/HotelBudget/HOutlet3_List'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  Outlet3_FoodRevenue_Master.objects.filter(IsDelete = False)  
    mem1 = Outlet3_BeverageRevenue_Master.objects.filter(IsDelete = False)
    mem2 = Outlet3_TotalOtherIncome_Master.objects.filter(IsDelete = False)
    mem3 =  Outlet3_Master.objects.filter(IsDelete = False)
    return render(request , 'Outlet3_HB/Outlet3Entry.html' ,{'mem':mem ,'mem1':mem1,'mem2':mem2,'mem3':mem3, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def HOutlet3_Delete(request,id):
    mem =  Outlet3_EnrtyMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HOutlet3_List'))


def HOutlet3_Edit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue ==''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales == ''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0
        Gross_Profit = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
            Salary_Wages_and_Bonuses = 0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits == ''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses ==''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0

        mem =  Outlet3_EnrtyMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue = FoodRevenue
        mem.BeverageRevenue = BeverageRevenue
        mem.TotalOtherIncome = TotalOtherIncome
        mem.FBRevenue = FBRevenue
        mem.FoodCostOfSales = FoodCostOfSales
        mem.BeverageCostOfSales = BeverageCostOfSales
        mem.TotalCostOfFbSales = TotalCostOfFbSales
        mem.AudioVisualEquipmentCostOfSales = AudioVisualEquipmentCostOfSales
        mem.FBOtherCostOfSales = FBOtherCostOfSales
        mem.TotalCostOfOtherRev = TotalCostOfOtherRev
        mem.TotalCostOfSales = TotalCostOfSales
        mem.Gross_Profit = Gross_Profit        
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives =  Bonuses_and_Incentives
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.DepartmentIncome =  DepartmentIncome 
        
        mem.save()
        
        TotalOutlet1 = request.POST["TotalOutlet1"]
        for x in range(int( TotalOutlet1) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem =  Outlet3_EnrtyMaster.objects.get(id = id)
            sv =  Outlet3_EntryDetail.objects.get(Outlet3_Master = TitleID_ , Outlet3_EnrtyMaster = id)
            sv.Amount =  Amount
            sv.save()
            
            
        TotalItemFood  = request.POST["TotalItemFood"]
        for x in range(int( TotalItemFood ) +1):
           
            FTitleID_ = request.POST["FTitleID_" + str(x)]
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 == ''):
                Amount1 =0
            
            sv = Outlet3_FoodRevenue_EntryDetail.objects.get(Outlet3_FoodRevenue_Master = FTitleID_ , Outlet3_EnrtyMaster = id)
            sv.Amount1  =  Amount1 
            sv.save()
            
               
        TotalItemBeverage   = request.POST["TotalItemBeverage"]
        for x in range(int( TotalItemBeverage  ) +1):
           
            BTitleID_ = request.POST["BTitleID_" + str(x)]
            Amount2 = request.POST["BAmount_" + str(x)]
            if(Amount2 == ''):
                Amount2 =0
            
            sv = Outlet3_BeverageRevenue_Maste_EntryDetail.objects.get(Outlet3_BeverageRevenue_Master = BTitleID_ , Outlet3_EnrtyMaster = id)
            sv.Amount2  =  Amount2 
            sv.save()
            
        TotalOtherItem   = request.POST["TotalOtherItem"]
        for x in range(int( TotalOtherItem ) +1):
           
            OTitleID_ = request.POST["OTitleID_" + str(x)]
            Amount3 = request.POST["OAmount_" + str(x)]
            if(Amount3 == ''):
                Amount3 =0
            
            sv = Outlet3_TotalOtherIncome_MasterIncome_EntryDetail.objects.get(Outlet3_TotalOtherIncome_Master = OTitleID_ , Outlet3_EnrtyMaster = id)
            sv.Amount3  =  Amount3 
            sv.save()
            
        return(redirect('/HotelBudget/HOutlet3_List'))
    
    mem4 = Outlet3_EntryDetail.objects.filter( Outlet3_EnrtyMaster=id ,IsDelete = False).select_related("Outlet3_Master")  
    mem3 = Outlet3_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( Outlet3_EnrtyMaster=id ,IsDelete = False).select_related("Outlet3_TotalOtherIncome_Master")       
    mem2 = Outlet3_BeverageRevenue_Maste_EntryDetail.objects.filter( Outlet3_EnrtyMaster=id ,IsDelete = False).select_related("Outlet3_BeverageRevenue_Master")
    mem1 = Outlet3_FoodRevenue_EntryDetail.objects.filter(Outlet3_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet3_FoodRevenue_Master")
    mem = Outlet3_EnrtyMaster.objects.get(id = id)
     
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'Outlet3_HB/Outlet3Edit.html' , {'mem1' :mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'mem':mem ,'CYear':range(2022,CYear)})


def HOutlet3_View(request, id):
    template_path = "Outlet3_HB/Outlet3View.html"
    mem4 = Outlet3_EntryDetail.objects.filter( Outlet3_EnrtyMaster=id ,IsDelete = False).select_related("Outlet3_Master")       
    mem3 = Outlet3_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( Outlet3_EnrtyMaster=id ,IsDelete = False).select_related("Outlet3_TotalOtherIncome_Master")
    mem2 = Outlet3_BeverageRevenue_Maste_EntryDetail.objects.filter(Outlet3_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet3_BeverageRevenue_Master")
    mem1 = Outlet3_FoodRevenue_EntryDetail.objects.filter(Outlet3_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet3_FoodRevenue_Master")
    mem = Outlet3_EnrtyMaster.objects.get(id = id)
  
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 



def HOutlet4_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Outlet4_EnrtyMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'Outlet4_HB/Outlet4List.html' ,{'mem' :mem }) 
                            
                            
                         
def HOutlet4_Entry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")       
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST["BeverageRevenue"]
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0        
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0 
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0 
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev = 0 
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0 
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages=0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives==''):
            Bonuses_and_Incentives=0   
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome==''):
            DepartmentIncome=0

        enmaster = Outlet4_EnrtyMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,
                                    FoodRevenue=FoodRevenue ,SalaryAndWages = SalaryAndWages ,
                                   BeverageRevenue=BeverageRevenue,
                                     FoodCostOfSales=FoodCostOfSales,
                                    TotalOtherIncome=TotalOtherIncome,
                                    BeverageCostOfSales=BeverageCostOfSales,                                  
                                    TotalCostOfFbSales=TotalCostOfFbSales,AudioVisualEquipmentCostOfSales=AudioVisualEquipmentCostOfSales,
                                    FBOtherCostOfSales=FBOtherCostOfSales,TotalCostOfOtherRev=TotalCostOfOtherRev,
                                    TotalCostOfSales=TotalCostOfSales,Gross_Profit=Gross_Profit,FBRevenue=FBRevenue,
                                 Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               DepartmentIncome = DepartmentIncome , 
                             OrganizationID=OrganizationID,CreatedBy=UserID    )
        enmaster.save()
 
        
           
        TotalItemFood = request.POST["TotalItemFood"]
        EntObj =  Outlet4_EnrtyMaster.objects.get(id=enmaster.pk)
       
        for x in range(int(TotalItemFood)+1):
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 ==''):
                Amount1 = 0
                
            FTitleID_ = request.POST["FTitleID_" + str(x)]        
            FTitleObj =   Outlet4_FoodRevenue_Master.objects.get(id = FTitleID_)           
        
            v = Outlet4_FoodRevenue_EntryDetail.objects.create(Amount1 = Amount1, 
                             Outlet4_FoodRevenue_Master = FTitleObj , Outlet4_EnrtyMaster = EntObj  )   
          
            
        TotalItemBeverage = request.POST["TotalItemBeverage"]
        for x in range(int(TotalItemBeverage)+1):
            Amount2 = request.POST["BAmount_" + str(x)]
            if( Amount2 ==''):
                 Amount2 = 0
                
            BTitleID_ = request.POST["BTitleID_"+ str(x)]        
            BTitleObj =  Outlet4_BeverageRevenue_Master.objects.get(id = BTitleID_)
                   
            v1 = Outlet4_BeverageRevenue_Maste_EntryDetail.objects.create( Amount2 =  Amount2, 
                     Outlet4_BeverageRevenue_Master = BTitleObj ,Outlet4_EnrtyMaster = EntObj )         
                           
             
        TotalOtherItem = request.POST["TotalOtherItem"]
        for x in range(int(TotalOtherItem)+1):
            Amount3 = request.POST["OAmount_" + str(x)]
            if( Amount3 ==''):
                 Amount3 = 0
                
            OTitleID_ = request.POST["OTitleID_"+ str(x)]        
            OTitleObj =   Outlet4_TotalOtherIncome_Master.objects.get(id = OTitleID_)
                   
            v1 = Outlet4_TotalOtherIncome_MasterIncome_EntryDetail.objects.create( Amount3 =  Amount3, 
                      Outlet4_TotalOtherIncome_Master = OTitleObj ,Outlet4_EnrtyMaster = EntObj )         
                      
              
              
        TotalOutlet1Item = request.POST["TotalOutlet1Item"]
        for x in range(int(TotalOutlet1Item)+1):
            Amount = request.POST["Amount_" + str(x)]
            if( Amount ==''):
                 Amount = 0
                
            TitleID_ = request.POST["TitleID_"+ str(x)]        
            TitleObj =  Outlet4_Master.objects.get(id = TitleID_)
                   
            v1 = Outlet4_EntryDetail.objects.create( Amount =  Amount, 
                     Outlet4_Master = TitleObj ,Outlet4_EnrtyMaster = EntObj )         
              
                
        return(redirect('/HotelBudget/HOutlet4_List'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  Outlet4_FoodRevenue_Master.objects.filter(IsDelete = False)  
    mem1 = Outlet4_BeverageRevenue_Master.objects.filter(IsDelete = False)
    mem2 = Outlet4_TotalOtherIncome_Master.objects.filter(IsDelete = False)
    mem3 =  Outlet4_Master.objects.filter(IsDelete = False)
    return render(request , 'Outlet4_HB/Outlet4Entry.html' ,{'mem':mem ,'mem1':mem1,'mem2':mem2,'mem3':mem3, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def HOutlet4_Delete(request,id):
    mem =  Outlet4_EnrtyMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HOutlet4_List'))


def HOutlet4_Edit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue ==''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales == ''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0
        Gross_Profit = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
            Salary_Wages_and_Bonuses = 0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits == ''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses ==''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0

        mem =  Outlet4_EnrtyMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue = FoodRevenue
        mem.BeverageRevenue = BeverageRevenue
        mem.TotalOtherIncome = TotalOtherIncome
        mem.FBRevenue = FBRevenue
        mem.FoodCostOfSales = FoodCostOfSales
        mem.BeverageCostOfSales = BeverageCostOfSales
        mem.TotalCostOfFbSales = TotalCostOfFbSales
        mem.AudioVisualEquipmentCostOfSales = AudioVisualEquipmentCostOfSales
        mem.FBOtherCostOfSales = FBOtherCostOfSales
        mem.TotalCostOfOtherRev = TotalCostOfOtherRev
        mem.TotalCostOfSales = TotalCostOfSales
        mem.Gross_Profit = Gross_Profit        
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives =  Bonuses_and_Incentives
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.DepartmentIncome =  DepartmentIncome 
        
        mem.save()
        
        TotalOutlet1 = request.POST["TotalOutlet1"]
        for x in range(int( TotalOutlet1) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem =  Outlet4_EnrtyMaster.objects.get(id = id)
            sv =  Outlet4_EntryDetail.objects.get(Outlet4_Master = TitleID_ , Outlet4_EnrtyMaster = id)
            sv.Amount =  Amount
            sv.save()
            
            
        TotalItemFood  = request.POST["TotalItemFood"]
        for x in range(int( TotalItemFood ) +1):
           
            FTitleID_ = request.POST["FTitleID_" + str(x)]
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 == ''):
                Amount1 =0
            
            sv = Outlet4_FoodRevenue_EntryDetail.objects.get(Outlet4_FoodRevenue_Master = FTitleID_ , Outlet4_EnrtyMaster = id)
            sv.Amount1  =  Amount1 
            sv.save()
            
               
        TotalItemBeverage   = request.POST["TotalItemBeverage"]
        for x in range(int( TotalItemBeverage  ) +1):
           
            BTitleID_ = request.POST["BTitleID_" + str(x)]
            Amount2 = request.POST["BAmount_" + str(x)]
            if(Amount2 == ''):
                Amount2 =0
            
            sv = Outlet4_BeverageRevenue_Maste_EntryDetail.objects.get(Outlet4_BeverageRevenue_Master = BTitleID_ , Outlet4_EnrtyMaster = id)
            sv.Amount2  =  Amount2 
            sv.save()
            
        TotalOtherItem   = request.POST["TotalOtherItem"]
        for x in range(int( TotalOtherItem ) +1):
           
            OTitleID_ = request.POST["OTitleID_" + str(x)]
            Amount3 = request.POST["OAmount_" + str(x)]
            if(Amount3 == ''):
                Amount3 =0
            
            sv = Outlet4_TotalOtherIncome_MasterIncome_EntryDetail.objects.get(Outlet4_TotalOtherIncome_Master = OTitleID_ , Outlet4_EnrtyMaster = id)
            sv.Amount3  =  Amount3 
            sv.save()
            
        return(redirect('/HotelBudget/HOutlet4_List'))
    
    mem4 = Outlet4_EntryDetail.objects.filter( Outlet4_EnrtyMaster=id ,IsDelete = False).select_related("Outlet4_Master")  
    mem3 = Outlet4_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( Outlet4_EnrtyMaster=id ,IsDelete = False).select_related("Outlet4_TotalOtherIncome_Master")       
    mem2 = Outlet4_BeverageRevenue_Maste_EntryDetail.objects.filter( Outlet4_EnrtyMaster=id ,IsDelete = False).select_related("Outlet4_BeverageRevenue_Master")
    mem1 = Outlet4_FoodRevenue_EntryDetail.objects.filter(Outlet4_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet4_FoodRevenue_Master")
    mem = Outlet4_EnrtyMaster.objects.get(id = id)
     
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'Outlet4_HB/Outlet4Edit.html' , {'mem1' :mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'mem':mem ,'CYear':range(2022,CYear)})

def HOutlet4_View(request, id):
    template_path = "Outlet4_HB/Outlet4View.html"
    mem4 = Outlet4_EntryDetail.objects.filter( Outlet4_EnrtyMaster=id ,IsDelete = False).select_related("Outlet4_Master")       
    mem3 = Outlet4_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( Outlet4_EnrtyMaster=id ,IsDelete = False).select_related("Outlet4_TotalOtherIncome_Master")
    mem2 = Outlet4_BeverageRevenue_Maste_EntryDetail.objects.filter(Outlet4_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet4_BeverageRevenue_Master")
    mem1 = Outlet4_FoodRevenue_EntryDetail.objects.filter(Outlet4_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet4_FoodRevenue_Master")
    mem = Outlet4_EnrtyMaster.objects.get(id = id)
  
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 



def HOutlet5_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Outlet5_EnrtyMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'Outlet5_HB/Outlet5List.html' ,{'mem' :mem }) 
                            

                         
def HOutlet5_Entry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")       
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST["BeverageRevenue"]
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0        
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0 
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0 
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev = 0 
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0 
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages=0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives==''):
            Bonuses_and_Incentives=0   
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome==''):
            DepartmentIncome=0

        enmaster = Outlet5_EnrtyMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,
                                    FoodRevenue=FoodRevenue ,SalaryAndWages = SalaryAndWages ,
                                   BeverageRevenue=BeverageRevenue,
                                     FoodCostOfSales=FoodCostOfSales,
                                    TotalOtherIncome=TotalOtherIncome,
                                    BeverageCostOfSales=BeverageCostOfSales,                                  
                                    TotalCostOfFbSales=TotalCostOfFbSales,AudioVisualEquipmentCostOfSales=AudioVisualEquipmentCostOfSales,
                                    FBOtherCostOfSales=FBOtherCostOfSales,TotalCostOfOtherRev=TotalCostOfOtherRev,
                                    TotalCostOfSales=TotalCostOfSales,Gross_Profit=Gross_Profit,FBRevenue=FBRevenue,
                                 Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               DepartmentIncome = DepartmentIncome , 
                             OrganizationID=OrganizationID,CreatedBy=UserID    )
        enmaster.save()
 
        
           
        TotalItemFood = request.POST["TotalItemFood"]
        EntObj =  Outlet5_EnrtyMaster.objects.get(id=enmaster.pk)
       
        for x in range(int(TotalItemFood)+1):
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 ==''):
                Amount1 = 0
                
            FTitleID_ = request.POST["FTitleID_" + str(x)]        
            FTitleObj =   Outlet5_FoodRevenue_Master.objects.get(id = FTitleID_)           
        
            v = Outlet5_FoodRevenue_EntryDetail.objects.create(Amount1 = Amount1, 
                             Outlet5_FoodRevenue_Master = FTitleObj , Outlet5_EnrtyMaster = EntObj  )   
          
            
        TotalItemBeverage = request.POST["TotalItemBeverage"]
        for x in range(int(TotalItemBeverage)+1):
            Amount2 = request.POST["BAmount_" + str(x)]
            if( Amount2 ==''):
                 Amount2 = 0
                
            BTitleID_ = request.POST["BTitleID_"+ str(x)]        
            BTitleObj =  Outlet5_BeverageRevenue_Master.objects.get(id = BTitleID_)
                   
            v1 = Outlet5_BeverageRevenue_Maste_EntryDetail.objects.create( Amount2 =  Amount2, 
                     Outlet5_BeverageRevenue_Master = BTitleObj ,Outlet5_EnrtyMaster = EntObj )         
                           
             
        TotalOtherItem = request.POST["TotalOtherItem"]
        for x in range(int(TotalOtherItem)+1):
            Amount3 = request.POST["OAmount_" + str(x)]
            if( Amount3 ==''):
                 Amount3 = 0
                
            OTitleID_ = request.POST["OTitleID_"+ str(x)]        
            OTitleObj =   Outlet5_TotalOtherIncome_Master.objects.get(id = OTitleID_)
                   
            v1 = Outlet5_TotalOtherIncome_MasterIncome_EntryDetail.objects.create( Amount3 =  Amount3, 
                      Outlet5_TotalOtherIncome_Master = OTitleObj ,Outlet5_EnrtyMaster = EntObj )         
                      
              
              
        TotalOutlet1Item = request.POST["TotalOutlet1Item"]
        for x in range(int(TotalOutlet1Item)+1):
            Amount = request.POST["Amount_" + str(x)]
            if( Amount ==''):
                 Amount = 0
                
            TitleID_ = request.POST["TitleID_"+ str(x)]        
            TitleObj =  Outlet5_Master.objects.get(id = TitleID_)
                   
            v1 = Outlet5_EntryDetail.objects.create( Amount =  Amount, 
                     Outlet5_Master = TitleObj ,Outlet5_EnrtyMaster = EntObj )         
              
                
        return(redirect('/HotelBudget/HOutlet5_List'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  Outlet5_FoodRevenue_Master.objects.filter(IsDelete = False)  
    mem1 = Outlet5_BeverageRevenue_Master.objects.filter(IsDelete = False)
    mem2 = Outlet5_TotalOtherIncome_Master.objects.filter(IsDelete = False)
    mem3 =  Outlet5_Master.objects.filter(IsDelete = False)
    return render(request , 'Outlet5_HB/Outlet5Entry.html' ,{'mem':mem ,'mem1':mem1,'mem2':mem2,'mem3':mem3, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def HOutlet5_Delete(request,id):
    mem =  Outlet5_EnrtyMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HOutlet5_List'))


def HOutlet5_Edit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue ==''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales == ''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0
        Gross_Profit = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
            Salary_Wages_and_Bonuses = 0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits == ''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses ==''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0

        mem =  Outlet5_EnrtyMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue = FoodRevenue
        mem.BeverageRevenue = BeverageRevenue
        mem.TotalOtherIncome = TotalOtherIncome
        mem.FBRevenue = FBRevenue
        mem.FoodCostOfSales = FoodCostOfSales
        mem.BeverageCostOfSales = BeverageCostOfSales
        mem.TotalCostOfFbSales = TotalCostOfFbSales
        mem.AudioVisualEquipmentCostOfSales = AudioVisualEquipmentCostOfSales
        mem.FBOtherCostOfSales = FBOtherCostOfSales
        mem.TotalCostOfOtherRev = TotalCostOfOtherRev
        mem.TotalCostOfSales = TotalCostOfSales
        mem.Gross_Profit = Gross_Profit        
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives =  Bonuses_and_Incentives
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.DepartmentIncome =  DepartmentIncome 
        
        mem.save()
        
        TotalOutlet1 = request.POST["TotalOutlet1"]
        for x in range(int( TotalOutlet1) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem =  Outlet5_EnrtyMaster.objects.get(id = id)
            sv =  Outlet5_EntryDetail.objects.get(Outlet5_Master = TitleID_ , Outlet5_EnrtyMaster = id)
            sv.Amount =  Amount
            sv.save()
            
            
        TotalItemFood  = request.POST["TotalItemFood"]
        for x in range(int( TotalItemFood ) +1):
           
            FTitleID_ = request.POST["FTitleID_" + str(x)]
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 == ''):
                Amount1 =0
            
            sv = Outlet5_FoodRevenue_EntryDetail.objects.get(Outlet5_FoodRevenue_Master = FTitleID_ , Outlet5_EnrtyMaster = id)
            sv.Amount1  =  Amount1 
            sv.save()
            
               
        TotalItemBeverage   = request.POST["TotalItemBeverage"]
        for x in range(int( TotalItemBeverage  ) +1):
           
            BTitleID_ = request.POST["BTitleID_" + str(x)]
            Amount2 = request.POST["BAmount_" + str(x)]
            if(Amount2 == ''):
                Amount2 =0
            
            sv = Outlet5_BeverageRevenue_Maste_EntryDetail.objects.get(Outlet5_BeverageRevenue_Master = BTitleID_ , Outlet5_EnrtyMaster = id)
            sv.Amount2  =  Amount2 
            sv.save()
            
        TotalOtherItem   = request.POST["TotalOtherItem"]
        for x in range(int( TotalOtherItem ) +1):
           
            OTitleID_ = request.POST["OTitleID_" + str(x)]
            Amount3 = request.POST["OAmount_" + str(x)]
            if(Amount3 == ''):
                Amount3 =0
            
            sv = Outlet5_TotalOtherIncome_MasterIncome_EntryDetail.objects.get(Outlet5_TotalOtherIncome_Master = OTitleID_ , Outlet5_EnrtyMaster = id)
            sv.Amount3  =  Amount3 
            sv.save()
            
        return(redirect('/HotelBudget/HOutlet5_List'))
    
    mem4 = Outlet5_EntryDetail.objects.filter( Outlet5_EnrtyMaster=id ,IsDelete = False).select_related("Outlet5_Master")  
    mem3 = Outlet5_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( Outlet5_EnrtyMaster=id ,IsDelete = False).select_related("Outlet5_TotalOtherIncome_Master")       
    mem2 = Outlet5_BeverageRevenue_Maste_EntryDetail.objects.filter( Outlet5_EnrtyMaster=id ,IsDelete = False).select_related("Outlet5_BeverageRevenue_Master")
    mem1 = Outlet5_FoodRevenue_EntryDetail.objects.filter(Outlet5_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet5_FoodRevenue_Master")
    mem = Outlet5_EnrtyMaster.objects.get(id = id)
     
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'Outlet5_HB/Outlet5Edit.html' , {'mem1' :mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'mem':mem ,'CYear':range(2022,CYear)})


def HOutlet5_View(request, id):
    template_path = "Outlet5_HB/Outlet5View.html"
    mem4 = Outlet5_EntryDetail.objects.filter( Outlet5_EnrtyMaster=id ,IsDelete = False).select_related("Outlet5_Master")       
    mem3 = Outlet5_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( Outlet5_EnrtyMaster=id ,IsDelete = False).select_related("Outlet5_TotalOtherIncome_Master")
    mem2 = Outlet5_BeverageRevenue_Maste_EntryDetail.objects.filter(Outlet5_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet5_BeverageRevenue_Master")
    mem1 = Outlet5_FoodRevenue_EntryDetail.objects.filter(Outlet5_EnrtyMaster =id ,IsDelete=False ).select_related("Outlet5_FoodRevenue_Master")
    mem = Outlet5_EnrtyMaster.objects.get(id = id)
  
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 



  
def PL_FB_Outlet_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = PL_FB_EnrtyMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'PL_FB_Outlet/PL_FBList.html' ,{'mem' :mem }) 
                            
                         
def PL_FB_Outlet_Entry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")       
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST["BeverageRevenue"]
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0        
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0 
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0 
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev = 0 
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0 
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages=0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives==''):
            Bonuses_and_Incentives=0   
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome==''):
            DepartmentIncome=0

        enmaster = PL_FB_EnrtyMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,
                                    FoodRevenue=FoodRevenue ,SalaryAndWages = SalaryAndWages ,
                                   BeverageRevenue=BeverageRevenue,
                                     FoodCostOfSales=FoodCostOfSales,
                                    TotalOtherIncome=TotalOtherIncome,
                                    BeverageCostOfSales=BeverageCostOfSales,                                  
                                    TotalCostOfFbSales=TotalCostOfFbSales,AudioVisualEquipmentCostOfSales=AudioVisualEquipmentCostOfSales,
                                    FBOtherCostOfSales=FBOtherCostOfSales,TotalCostOfOtherRev=TotalCostOfOtherRev,
                                    TotalCostOfSales=TotalCostOfSales,Gross_Profit=Gross_Profit,FBRevenue=FBRevenue,
                                 Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               DepartmentIncome = DepartmentIncome , 
                             OrganizationID=OrganizationID,CreatedBy=UserID    )
        enmaster.save()
 
        
           
        TotalItemFood = request.POST["TotalItemFood"]
        EntObj =  PL_FB_EnrtyMaster.objects.get(id=enmaster.pk)
       
        for x in range(int(TotalItemFood)+1):
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 ==''):
                Amount1 = 0
                
            FTitleID_ = request.POST["FTitleID_" + str(x)]        
            FTitleObj =   PL_FB_FoodRevenue_Master.objects.get(id = FTitleID_)           
        
            v = PL_FB_FoodRevenue_EntryDetail.objects.create(Amount1 = Amount1, 
                             PL_FB_FoodRevenue_Master = FTitleObj , PL_FB_EnrtyMaster = EntObj  )   
          
            
        TotalItemBeverage = request.POST["TotalItemBeverage"]
        for x in range(int(TotalItemBeverage)+1):
            Amount2 = request.POST["BAmount_" + str(x)]
            if( Amount2 ==''):
                 Amount2 = 0
                
            BTitleID_ = request.POST["BTitleID_"+ str(x)]        
            BTitleObj =  PL_FB_BeverageRevenue_Master.objects.get(id = BTitleID_)
                   
            v1 = PL_FB_BeverageRevenue_Maste_EntryDetail.objects.create( Amount2 =  Amount2, 
                     PL_FB_BeverageRevenue_Master = BTitleObj ,PL_FB_EnrtyMaster = EntObj )         
                           
             
        TotalOtherItem = request.POST["TotalOtherItem"]
        for x in range(int(TotalOtherItem)+1):
            Amount3 = request.POST["OAmount_" + str(x)]
            if( Amount3 ==''):
                 Amount3 = 0
                
            OTitleID_ = request.POST["OTitleID_"+ str(x)]        
            OTitleObj =   PL_FB_TotalOtherIncome_Master.objects.get(id = OTitleID_)
                   
            v1 = PL_FB_TotalOtherIncome_MasterIncome_EntryDetail.objects.create( Amount3 =  Amount3, 
                      PL_FB_TotalOtherIncome_Master = OTitleObj ,PL_FB_EnrtyMaster = EntObj )         
                      
              
              
        TotalOutlet1Item = request.POST["TotalOutlet1Item"]
        for x in range(int(TotalOutlet1Item)+1):
            Amount = request.POST["Amount_" + str(x)]
            if( Amount ==''):
                 Amount = 0
                
            TitleID_ = request.POST["TitleID_"+ str(x)]        
            TitleObj =  PL_FB_Master.objects.get(id = TitleID_)
                   
            v1 = PL_FB_EntryDetail.objects.create( Amount =  Amount, 
                     PL_FB_Master = TitleObj ,PL_FB_EnrtyMaster = EntObj )         
              
                
        return(redirect('/HotelBudget/PL_FB_Outlet_List'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  PL_FB_FoodRevenue_Master.objects.filter(IsDelete = False)  
    mem1 = PL_FB_BeverageRevenue_Master.objects.filter(IsDelete = False)
    mem2 = PL_FB_TotalOtherIncome_Master.objects.filter(IsDelete = False)
    mem3 =  PL_FB_Master.objects.filter(IsDelete = False)
    return render(request , 'PL_FB_Outlet/PL_FBEntry.html' ,{'mem':mem ,'mem1':mem1,'mem2':mem2,'mem3':mem3, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})
                           
def PL_FB_Outlet_Delete(request,id):
    mem =  PL_FB_EnrtyMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/PL_FB_Outlet_List'))


def PL_FB_Outlet_Edit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue ==''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales == ''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0
        Gross_Profit = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
            Salary_Wages_and_Bonuses = 0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits == ''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses ==''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0

        mem =  PL_FB_EnrtyMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue = FoodRevenue
        mem.BeverageRevenue = BeverageRevenue
        mem.TotalOtherIncome = TotalOtherIncome
        mem.FBRevenue = FBRevenue
        mem.FoodCostOfSales = FoodCostOfSales
        mem.BeverageCostOfSales = BeverageCostOfSales
        mem.TotalCostOfFbSales = TotalCostOfFbSales
        mem.AudioVisualEquipmentCostOfSales = AudioVisualEquipmentCostOfSales
        mem.FBOtherCostOfSales = FBOtherCostOfSales
        mem.TotalCostOfOtherRev = TotalCostOfOtherRev
        mem.TotalCostOfSales = TotalCostOfSales
        mem.Gross_Profit = Gross_Profit        
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives =  Bonuses_and_Incentives
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.DepartmentIncome =  DepartmentIncome 
        
        mem.save()
        
        TotalOutlet1 = request.POST["TotalOutlet1"]
        for x in range(int( TotalOutlet1) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem =  PL_FB_EnrtyMaster.objects.get(id = id)
            sv =  PL_FB_EntryDetail.objects.get(PL_FB_Master = TitleID_ , PL_FB_EnrtyMaster = id)
            sv.Amount =  Amount
            sv.save()
            
            
        TotalItemFood  = request.POST["TotalItemFood"]
        for x in range(int( TotalItemFood ) +1):
           
            FTitleID_ = request.POST["FTitleID_" + str(x)]
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 == ''):
                Amount1 =0
            
            sv = PL_FB_FoodRevenue_EntryDetail.objects.get(PL_FB_FoodRevenue_Master = FTitleID_ , PL_FB_EnrtyMaster = id)
            sv.Amount1  =  Amount1 
            sv.save()
            
               
        TotalItemBeverage   = request.POST["TotalItemBeverage"]
        for x in range(int( TotalItemBeverage  ) +1):
           
            BTitleID_ = request.POST["BTitleID_" + str(x)]
            Amount2 = request.POST["BAmount_" + str(x)]
            if(Amount2 == ''):
                Amount2 =0
            
            sv = PL_FB_BeverageRevenue_Maste_EntryDetail.objects.get(PL_FB_BeverageRevenue_Master = BTitleID_ , PL_FB_EnrtyMaster = id)
            sv.Amount2  =  Amount2 
            sv.save()
            
        TotalOtherItem   = request.POST["TotalOtherItem"]
        for x in range(int( TotalOtherItem ) +1):
           
            OTitleID_ = request.POST["OTitleID_" + str(x)]
            Amount3 = request.POST["OAmount_" + str(x)]
            if(Amount3 == ''):
                Amount3 =0
            
            sv = PL_FB_TotalOtherIncome_MasterIncome_EntryDetail.objects.get(PL_FB_TotalOtherIncome_Master = OTitleID_ , PL_FB_EnrtyMaster = id)
            sv.Amount3  =  Amount3 
            sv.save()
            
        return(redirect('/HotelBudget/PL_FB_Outlet_List'))
    
    mem4 = PL_FB_EntryDetail.objects.filter( PL_FB_EnrtyMaster=id ,IsDelete = False).select_related("PL_FB_Master")  
    mem3 = PL_FB_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( PL_FB_EnrtyMaster=id ,IsDelete = False).select_related("PL_FB_TotalOtherIncome_Master")       
    mem2 = PL_FB_BeverageRevenue_Maste_EntryDetail.objects.filter( PL_FB_EnrtyMaster=id ,IsDelete = False).select_related("PL_FB_BeverageRevenue_Master")
    mem1 = PL_FB_FoodRevenue_EntryDetail.objects.filter(PL_FB_EnrtyMaster =id ,IsDelete=False ).select_related("PL_FB_FoodRevenue_Master")
    mem = PL_FB_EnrtyMaster.objects.get(id = id)
     
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'PL_FB_Outlet/PL_FBEdit.html' , {'mem1' :mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'mem':mem ,'CYear':range(2022,CYear)})


def PL_FB_Outlet_View(request, id):
    template_path = "PL_FB_Outlet/PL_FBView.html"
    mem4 = PL_FB_EntryDetail.objects.filter( PL_FB_EnrtyMaster=id ,IsDelete = False).select_related("PL_FB_Master")       
    mem3 = PL_FB_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( PL_FB_EnrtyMaster=id ,IsDelete = False).select_related("PL_FB_TotalOtherIncome_Master")
    mem2 = PL_FB_BeverageRevenue_Maste_EntryDetail.objects.filter(PL_FB_EnrtyMaster =id ,IsDelete=False ).select_related("PL_FB_BeverageRevenue_Master")
    mem1 = PL_FB_FoodRevenue_EntryDetail.objects.filter(PL_FB_EnrtyMaster =id ,IsDelete=False ).select_related("PL_FB_FoodRevenue_Master")
    mem = PL_FB_EnrtyMaster.objects.get(id = id)
  
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 



def RoomWorksheet_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = RoomWorksheet_EnrtyMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'RoomWorksheet/RoomWorksheetList.html' ,{'mem' :mem }) 
                            
                            

def RoomWorkSheetEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"] 
        EntryYear = request.POST["EntryYear"] 
        
        enmaster= RoomWorksheet_EnrtyMaster.objects.create(EntryMonth=EntryMonth,EntryYear=EntryYear,OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()
        
        EntOBj=RoomWorksheet_EnrtyMaster.objects.get(id=enmaster.pk)   
          
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount == ''):
                Amount = 0
                      
            ItemID_ = request.POST["ItemID_" + str(x)]
            
            TitleObje=RoomWorksheet_ItemMaster.objects.get(id=ItemID_)
              
            v = RoomWorksheet_ItemDetails.objects.create(Amount = Amount,
                                                       RoomWorksheet_ItemMaster=TitleObje,
                                                       RoomWorksheet_EnrtyMaster= EntOBj
                                                      )  
                      
        TotalCategoryItem = request.POST["TotalCategoryItem"]
        for x in range(int(TotalCategoryItem)):
            Amount = request.POST["CategoryAmout_" + str(x) ]
            if(Amount == ''):
                Amount = 0
                
            CategoryID_ = request.POST["CategoryID_" + str(x)]           
            CTitleObje=RoomWorksheet_CategoryMaster.objects.get(id=CategoryID_)                        
              
            v1 = RoomWorksheet_CategoryDetails.objects.create(Amount = Amount,
                                                       RoomWorksheet_CategoryMaster=CTitleObje,
                                                       RoomWorksheet_EnrtyMaster= EntOBj
                                                      )  
              
                                
        return(redirect('/HotelBudget/RoomWorksheet_List'))   
    mem = RoomWorksheet_ItemMaster.objects.filter(IsDelete = False).select_related('RoomWorksheet_CategoryMaster').all()    
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'RoomWorkSheet/RoomWorkSheetEntry.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})


def RoomWorksheet_Delete(request,id):
    mem =  RoomWorksheet_EnrtyMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/RoomWorksheet_List'))


def RoomWorksheet_Edit(request , id):
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        mem = RoomWorksheet_EnrtyMaster.objects.get(id = id)            
        mem.EntryMonth = EntryMonth
        mem.EntryYear =EntryYear
        mem.save()  
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            Amount = request.POST["Amount_" + str(x)]
            if(Amount == ''):
                Amount = 0
            ItemID_ = request.POST["ItemID_" + str(x)]
            mem1 = RoomWorksheet_EnrtyMaster.objects.get(id = id)
              
            sv = RoomWorksheet_ItemDetails.objects.get(RoomWorksheet_EnrtyMaster = id , RoomWorksheet_ItemMaster = ItemID_)
            sv.Amount = Amount
            sv.save()        
        
        TotalCategoryItem = request.POST["TotalCategoryItem"]
        for x in range(int(TotalCategoryItem)):
            
            Amount = request.POST["CategoryAmout_" + str(x)]
            if(Amount == ''):
                Amount =0
            CategoryID_ = request.POST["CategoryID_" + str(x)]
            mem1 = RoomWorksheet_EnrtyMaster.objects.get(id = id)
              
            sv = RoomWorksheet_CategoryDetails.objects.get(RoomWorksheet_EnrtyMaster = id , RoomWorksheet_CategoryMaster = CategoryID_)
            sv.Amount = Amount
            sv.save()
                                                                                
        return(redirect('/HotelBudget/RoomWorksheet_List'))   
    mem1 = RoomWorksheet_ItemMaster.objects.filter(IsDelete = False).select_related('RoomWorksheet_CategoryMaster').all()    
    mem = RoomWorksheet_EnrtyMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1   
    return render(request,'RoomWorksheet/RoomWorksheetEdit.html',{'mem':mem , 'mem1':mem1 ,'CYear':range(2022,CYear) })


def RoomWorksheet_View(request , id):
  
    template_path = "RoomWorksheet/RoomWorksheetView.html"
    mem1 = RoomWorksheet_ItemDetails.objects.filter(RoomWorksheet_EnrtyMaster=id,IsDelete = False).select_related("RoomWorksheet_ItemMaster")
    mem2 = RoomWorksheet_CategoryDetails.objects.filter(RoomWorksheet_EnrtyMaster=id,IsDelete = False).select_related("RoomWorksheet_CategoryMaster")
    mem = RoomWorksheet_EnrtyMaster.objects.get(id = id)
 
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1,'mem2':mem2, 'CMonth':CMonth }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)
  
    result = BytesIO()
 
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 



  
def HTotalFB_List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Total_FB_EnrtyMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'HBTotal_FB/Total_FBList.html' ,{'mem' :mem }) 
                            

                        
def HTotalFB_Entry(request):    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")       
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
       
    if request.method == 'POST':
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST["BeverageRevenue"]
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0        
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0 
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0 
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev = 0 
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0 
        Gross_Profit  = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages==''):
            SalaryAndWages=0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives==''):
            Bonuses_and_Incentives=0   
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses=0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome==''):
            DepartmentIncome=0

        enmaster = Total_FB_EnrtyMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,
                                    FoodRevenue=FoodRevenue ,SalaryAndWages = SalaryAndWages ,
                                   BeverageRevenue=BeverageRevenue,
                                     FoodCostOfSales=FoodCostOfSales,
                                    TotalOtherIncome=TotalOtherIncome,
                                    BeverageCostOfSales=BeverageCostOfSales,                                  
                                    TotalCostOfFbSales=TotalCostOfFbSales,AudioVisualEquipmentCostOfSales=AudioVisualEquipmentCostOfSales,
                                    FBOtherCostOfSales=FBOtherCostOfSales,TotalCostOfOtherRev=TotalCostOfOtherRev,
                                    TotalCostOfSales=TotalCostOfSales,Gross_Profit=Gross_Profit,FBRevenue=FBRevenue,
                                 Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               DepartmentIncome = DepartmentIncome , 
                             OrganizationID=OrganizationID,CreatedBy=UserID    )
        enmaster.save()
 
        
           
        TotalItemFood = request.POST["TotalItemFood"]
        EntObj =  Total_FB_EnrtyMaster.objects.get(id=enmaster.pk)
       
        for x in range(int(TotalItemFood)+1):
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 ==''):
                Amount1 = 0
                
            FTitleID_ = request.POST["FTitleID_" + str(x)]        
            FTitleObj =   Total_FB_FoodRevenue_Master.objects.get(id = FTitleID_)           
        
            v = Total_FB_FoodRevenue_EntryDetail.objects.create(Amount1 = Amount1, 
                             Total_FB_FoodRevenue_Master = FTitleObj , Total_FB_EnrtyMaster = EntObj  )   
          
            
        TotalItemBeverage = request.POST["TotalItemBeverage"]
        for x in range(int(TotalItemBeverage)+1):
            Amount2 = request.POST["BAmount_" + str(x)]
            if( Amount2 ==''):
                 Amount2 = 0
                
            BTitleID_ = request.POST["BTitleID_"+ str(x)]        
            BTitleObj =  Total_FB_BeverageRevenue_Master.objects.get(id = BTitleID_)
                   
            v1 = Total_FB_BeverageRevenue_Maste_EntryDetail.objects.create( Amount2 =  Amount2, 
                     Total_FB_BeverageRevenue_Master = BTitleObj ,Total_FB_EnrtyMaster = EntObj )         
                           
             
        TotalOtherItem = request.POST["TotalOtherItem"]
        for x in range(int(TotalOtherItem)+1):
            Amount3 = request.POST["OAmount_" + str(x)]
            if( Amount3 ==''):
                 Amount3 = 0
                
            OTitleID_ = request.POST["OTitleID_"+ str(x)]        
            OTitleObj =   Total_FB_TotalOtherIncome_Master.objects.get(id = OTitleID_)
                   
            v1 = Total_FB_TotalOtherIncome_MasterIncome_EntryDetail.objects.create( Amount3 =  Amount3, 
                      Total_FB_TotalOtherIncome_Master = OTitleObj ,Total_FB_EnrtyMaster = EntObj )         
                      
              
              
        TotalOutlet1Item = request.POST["TotalOutlet1Item"]
        for x in range(int(TotalOutlet1Item)+1):
            Amount = request.POST["Amount_" + str(x)]
            if( Amount ==''):
                 Amount = 0
                
            TitleID_ = request.POST["TitleID_"+ str(x)]        
            TitleObj =  Total_FB_Master.objects.get(id = TitleID_)
                   
            v1 = Total_FB_EntryDetail.objects.create( Amount =  Amount, 
                     Total_FB_Master = TitleObj ,Total_FB_EnrtyMaster = EntObj )         
              
                
        return(redirect('/HotelBudget/HTotalFB_List'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  Total_FB_FoodRevenue_Master.objects.filter(IsDelete = False)  
    mem1 = Total_FB_BeverageRevenue_Master.objects.filter(IsDelete = False)
    mem2 = Total_FB_TotalOtherIncome_Master.objects.filter(IsDelete = False)
    mem3 =  Total_FB_Master.objects.filter(IsDelete = False)
    return render(request , 'HBTotal_FB/Total_FBEntry.html' ,{'mem':mem ,'mem1':mem1,'mem2':mem2,'mem3':mem3, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def HTotalFB_Delete(request,id):
    mem =  Total_FB_EnrtyMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HotelBudget/HTotalFB_List'))


def HTotalFB_Edit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        if(FoodRevenue == ''):
            FoodRevenue =0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue ==''):
            BeverageRevenue =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0
        FBRevenue = request.POST['FBRevenue']
        if(FBRevenue ==''):
            FBRevenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales == ''):
            BeverageCostOfSales =0
        TotalCostOfFbSales = request.POST['TotalCostOfFbSales']
        if(TotalCostOfFbSales == ''):
            TotalCostOfFbSales =0
        AudioVisualEquipmentCostOfSales = request.POST['AudioVisualEquipmentCostOfSales']
        if(AudioVisualEquipmentCostOfSales == ''):
            AudioVisualEquipmentCostOfSales =0
        FBOtherCostOfSales = request.POST['FBOtherCostOfSales']
        if(FBOtherCostOfSales == ''):
            FBOtherCostOfSales =0
        TotalCostOfOtherRev = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev == ''):
            TotalCostOfOtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0
        Gross_Profit = request.POST['Gross_Profit']
        if(Gross_Profit == ''):
            Gross_Profit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
            Salary_Wages_and_Bonuses = 0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits == ''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses == ''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses ==''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0

        mem =  Total_FB_EnrtyMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue = FoodRevenue
        mem.BeverageRevenue = BeverageRevenue
        mem.TotalOtherIncome = TotalOtherIncome
        mem.FBRevenue = FBRevenue
        mem.FoodCostOfSales = FoodCostOfSales
        mem.BeverageCostOfSales = BeverageCostOfSales
        mem.TotalCostOfFbSales = TotalCostOfFbSales
        mem.AudioVisualEquipmentCostOfSales = AudioVisualEquipmentCostOfSales
        mem.FBOtherCostOfSales = FBOtherCostOfSales
        mem.TotalCostOfOtherRev = TotalCostOfOtherRev
        mem.TotalCostOfSales = TotalCostOfSales
        mem.Gross_Profit = Gross_Profit        
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives =  Bonuses_and_Incentives
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses  =  PayrollAndRelatedExpenses 
        mem.Total_Other_Expenses =   Total_Other_Expenses
        mem.DepartmentIncome =  DepartmentIncome 
        
        mem.save()
        
        TotalOutlet1 = request.POST["TotalOutlet1"]
        for x in range(int( TotalOutlet1) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem =  Total_FB_EnrtyMaster.objects.get(id = id)
            sv =  Total_FB_EntryDetail.objects.get(Total_FB_Master = TitleID_ , Total_FB_EnrtyMaster = id)
            sv.Amount =  Amount
            sv.save()
            
            
        TotalItemFood  = request.POST["TotalItemFood"]
        for x in range(int( TotalItemFood ) +1):
           
            FTitleID_ = request.POST["FTitleID_" + str(x)]
            Amount1 = request.POST["FAmount_" + str(x)]
            if(Amount1 == ''):
                Amount1 =0
            
            sv = Total_FB_FoodRevenue_EntryDetail.objects.get(Total_FB_FoodRevenue_Master = FTitleID_ , Total_FB_EnrtyMaster = id)
            sv.Amount1  =  Amount1 
            sv.save()
            
               
        TotalItemBeverage   = request.POST["TotalItemBeverage"]
        for x in range(int( TotalItemBeverage  ) +1):
           
            BTitleID_ = request.POST["BTitleID_" + str(x)]
            Amount2 = request.POST["BAmount_" + str(x)]
            if(Amount2 == ''):
                Amount2 =0
            
            sv = Total_FB_BeverageRevenue_Maste_EntryDetail.objects.get(Total_FB_BeverageRevenue_Master = BTitleID_ , Total_FB_EnrtyMaster = id)
            sv.Amount2  =  Amount2 
            sv.save()
            
        TotalOtherItem   = request.POST["TotalOtherItem"]
        for x in range(int( TotalOtherItem ) +1):
           
            OTitleID_ = request.POST["OTitleID_" + str(x)]
            Amount3 = request.POST["OAmount_" + str(x)]
            if(Amount3 == ''):
                Amount3 =0
            
            sv = Total_FB_TotalOtherIncome_MasterIncome_EntryDetail.objects.get(Total_FB_TotalOtherIncome_Master = OTitleID_ , Total_FB_EnrtyMaster = id)
            sv.Amount3  =  Amount3 
            sv.save()
            
        return(redirect('/HotelBudget/HTotalFB_List'))
    
    mem4 = Total_FB_EntryDetail.objects.filter( Total_FB_EnrtyMaster=id ,IsDelete = False).select_related("Total_FB_Master")  
    mem3 = Total_FB_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( Total_FB_EnrtyMaster=id ,IsDelete = False).select_related("Total_FB_TotalOtherIncome_Master")       
    mem2 = Total_FB_BeverageRevenue_Maste_EntryDetail.objects.filter( Total_FB_EnrtyMaster=id ,IsDelete = False).select_related("Total_FB_BeverageRevenue_Master")
    mem1 = Total_FB_FoodRevenue_EntryDetail.objects.filter(Total_FB_EnrtyMaster =id ,IsDelete=False ).select_related("Total_FB_FoodRevenue_Master")
    mem = Total_FB_EnrtyMaster.objects.get(id = id)
     
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'HBTotal_FB/Total_FBEdit.html' , {'mem1' :mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'mem':mem ,'CYear':range(2022,CYear)})


def HTotalFB_View(request, id):
    template_path = "HBTotal_FB/Total_FBView.html"
    mem4 = Total_FB_EntryDetail.objects.filter( Total_FB_EnrtyMaster=id ,IsDelete = False).select_related("Total_FB_Master")       
    mem3 = Total_FB_TotalOtherIncome_MasterIncome_EntryDetail.objects.filter( Total_FB_EnrtyMaster=id ,IsDelete = False).select_related("Total_FB_TotalOtherIncome_Master")
    mem2 = Total_FB_BeverageRevenue_Maste_EntryDetail.objects.filter(Total_FB_EnrtyMaster =id ,IsDelete=False ).select_related("Total_FB_BeverageRevenue_Master")
    mem1 = Total_FB_FoodRevenue_EntryDetail.objects.filter(Total_FB_EnrtyMaster =id ,IsDelete=False ).select_related("Total_FB_FoodRevenue_Master")
    mem = Total_FB_EnrtyMaster.objects.get(id = id)
  
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'mem2':mem2,'mem3':mem3,'mem4':mem4, 'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 


def FB_WorksheetList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = FB_Worksheet_EnrtyMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'FB_Worksheet/FB_WorksheetList.html' ,{'mem' :mem }) 


def FB_WorksheetDelete (request,id):
    mem = FB_Worksheet_EnrtyMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/HotelBudget/FB_WorksheetList'))
  

def FB_WorksheetEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"] 
        EntryYear = request.POST["EntryYear"] 
        
        enmaster= FB_Worksheet_EnrtyMaster.objects.create(EntryMonth=EntryMonth,EntryYear=EntryYear,OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()
        EntOBj=FB_Worksheet_EnrtyMaster.objects.get(id=enmaster.pk)    
        TotalItem = request.POST["TotalItem"]
        
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount == ''):
                Amount = 0                      
            TitleID_ = request.POST["TitleID_" + str(x)]            
            TitleObje=FB_Worksheet_Master.objects.get(id=TitleID_)              
            v = FBW_Break_food_Internal_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj
                                                      )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount1_" + str(x)]
            if(Amount == ''):
                Amount = 0    
            BTitleID_ = request.POST["BTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BTitleID_)
            v1 = FBW_Break_food_External_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )
            
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount2_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BBTitleID_ = request.POST["BBTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BBTitleID_)
            v1 = FBW_Break_Beverage_Internal_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )
            
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount3_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BExTitleID_ = request.POST["BExTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BExTitleID_)
            v1 = FBW_Break_Beverage_External_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )
                   
    # For second table
    
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BVCAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BVCTitleID_ = request.POST["BVCTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BVCTitleID_)
            v = FBW_Break_Food_Average_Check_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )   
            
            
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BVCAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BVC1TitleID_ = request.POST["BVC1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BVC1TitleID_)
            v1 = FBW_Break_Food_Average_Check_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj ) 
              
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BBAAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BBATitleID_ = request.POST["BBATitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BBATitleID_)
            v2 = FBW_Break_Beverage_Average_Check_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )
             
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BBAAmount2_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BBA2TitleID_ = request.POST["BBA2TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BBA2TitleID_)
            v3 = FBW_Break_Beverage_Average_Check_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj ) 
   # For Third table
   
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BFRAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BFRTitleID_ = request.POST["BFRTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BFRTitleID_)
            v = FBW_Break_Food_Revenue_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj ) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BFRAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BFR1TitleID_ = request.POST["BFRTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BFR1TitleID_)
            v1 = FBW_Break_Food_Revenue_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj ) 
            
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BBRAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BBRTitleID_ = request.POST["BFRTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BBRTitleID_)
            v2 = FBW_Break_Beverage_Revenue_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj ) 
        
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BBR1Amount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BBR1TitleID_ = request.POST["BFRTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BBRTitleID_)
            v3 = FBW_Break_Beverage_Revenue_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj ) 
            
       # For Fourth table
       
        for x in range(int(TotalItem)+1):
            Amount = request.POST["FIAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            FITitleID_ = request.POST["FITitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=FITitleID_)
            v = FBW_Launch_Food_Internal_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj ) 
           
        for x in range(int(TotalItem)+1):
            Amount = request.POST["FEAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            FETitleID_ = request.POST["FETitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=FETitleID_)
            v1 = FBW_Launch_Food_External_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj ) 
        
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BIAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BITitleID_ = request.POST["BITitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BITitleID_)
            v2 = FBW_Launch_Beverage_Internal_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj ) 
            
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BEAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BETitleID_ = request.POST["BETitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BETitleID_)
            v3 = FBW_Launch_Beverage_External_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj ) 
            
 # For Five table
        for x in range(int(TotalItem)+1):
            Amount = request.POST["LFAAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            LFATitleID_ = request.POST["LFATitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=LFATitleID_)
            v = FBW_Launch_Food_Average_Check_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj ) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["LFAAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            LFA1TitleID_ = request.POST["LFA1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=LFA1TitleID_)
            v1 = FBW_Launch_Food_Average_Check_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj ) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["LFBAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            LFBTitleID_ = request.POST["LFBTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=LFBTitleID_)
            v2 = FBW_Beverage_Food_Average_Check_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj ) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["LFBAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            LFB1TitleID_ = request.POST["LFB1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=LFB1TitleID_)
            v3 = FBW_Beverage_Food_Average_Check_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )  
   
 # For Six table
        for x in range(int(TotalItem)+1):
            Amount = request.POST["FRAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            FRTitleID_ = request.POST["FRTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=FRTitleID_)
            v = FBW_Launch_Food_Revenue_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["FRAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            FR1TitleID_ = request.POST["FR1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=FR1TitleID_)
            v1 = FBW_Launch_Food_Revenue_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BRAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BRTitleID_ = request.POST["BRTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BRTitleID_)
            v2 = FBW_Launch_Beverage_Revenue_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BRAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BR1TitleID_ = request.POST["BR1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BR1TitleID_)
            v3 = FBW_Launch_Beverage_Revenue_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )  
     # For Seven table
        for x in range(int(TotalItem)+1):
            Amount = request.POST["DIAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            DITitleID_ = request.POST["DITitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=DITitleID_)
            v3 = FBW_Dinner_Food_Internal_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["DEAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            DETitleID_ = request.POST["DETitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=DETitleID_)
            v3 = FBW_Dinner_Food_External_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BIAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BITitleID_ = request.POST["BITitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BITitleID_)
            v3 = FBW_Dinner_Beverage_Internal_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BEAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BETitleID_ = request.POST["BETitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BETitleID_)
            v3 = FBW_Dinner_Beverage_External_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )  
    # For Eight table 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["DFAAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            DFTitleID_ = request.POST["DFTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=DFTitleID_)
            v3 = FBW_Dinner_Food_Average_Check_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["DFAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            DF1TitleID_ = request.POST["DF1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=DF1TitleID_)
            v3 = FBW_Dinner_Food_Average_Check_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BFAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BFTitleID_ = request.POST["BFTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BFTitleID_)
            v3 = FBW_Dinner_Bevarage_Average_Check_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj ) 
                                                        
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BFAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BF1TitleID_ = request.POST["BF1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BF1TitleID_)
            v3 = FBW_Dinner_Bevarage_Average_Check_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )  
 # For Nine table   
        for x in range(int(TotalItem)+1):
            Amount = request.POST["FRAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            FRTitleID_ = request.POST["FRTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=FRTitleID_)
            v3 = FBW_Dinner_Food_Revenue_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )   
        for x in range(int(TotalItem)+1):
            Amount = request.POST["FRAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            FR1TitleID_ = request.POST["FR1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=FR1TitleID_)
            v3 = FBW_Dinner_Food_Revenue_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )   
        for x in range(int(TotalItem)+1):
            Amount = request.POST["DRAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            DRTitleID_ = request.POST["DRTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=DRTitleID_)
            v3 = FBW_Dinner_Beverage_Revenue_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                       FB_Worksheet_EnrtyMaster= EntOBj )    
        for x in range(int(TotalItem)+1):
            Amount = request.POST["DRAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            DR1TitleID_ = request.POST["DR1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=DR1TitleID_)
            v3 = FBW_Dinner_Beverage_Revenue_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )    
 # For Ten table     (Super Food View)       
         
        for x in range(int(TotalItem)+1):
            Amount = request.POST["SIAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            SITitleID_ = request.POST["SITitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=SITitleID_)
            v3 = FBW_Super_Food_Internal_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj ) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["SEAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            SETitleID_ = request.POST["SETitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=SETitleID_)
            v3 = FBW_Super_Food_External_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj ) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["SBIAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            SBITitleID_ = request.POST["SBITitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=SBITitleID_)
            v3 = FBW_Super_Beverage_Internal_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )    
        for x in range(int(TotalItem)+1):
            Amount = request.POST["SBEAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            SBETitleID_ = request.POST["SBETitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=SBETitleID_)
            v3 = FBW_Super_Beverage_External_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
 # For Ten table     (Super Food Average View)   
        for x in range(int(TotalItem)+1):
            Amount = request.POST["ACAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            ACTitleID_ = request.POST["ACTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=ACTitleID_)
            v3 = FBW_Super_Food_Average_Check_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
        
        for x in range(int(TotalItem)+1):
            Amount = request.POST["ACAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            AC1TitleID_ = request.POST["AC1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=AC1TitleID_)
            v3 = FBW_Super_Food_Average_Check_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BCAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BCTitleID_ = request.POST["BCTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BCTitleID_)
            v3 = FBW_Super_Beverage_Average_Check_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BCAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BC1TitleID_ = request.POST["BC1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BC1TitleID_)
            v3 = FBW_Super_Beverage_Average_Check_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
            
# For Eleven table (Super Food Revenue View)       
        for x in range(int(TotalItem)+1):
            Amount = request.POST["SRAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            SRTitleID_ = request.POST["SRTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=SRTitleID_)
            v3 = FBW_Super_Food_Revenue_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj ) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["SRAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            SR1TitleID_ = request.POST["SR1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=SR1TitleID_)
            v3 = FBW_Super_Food_Revenue_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj ) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BRAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BRTitleID_ = request.POST["BRTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BRTitleID_)
            v3 = FBW_Super_Beverage_Revenue_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj ) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["BRAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            BR1TitleID_ = request.POST["BR1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=BR1TitleID_)
            v3 = FBW_Super_Beverage_Revenue_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
# For Twelve table (Other Food Internal View) 

        for x in range(int(TotalItem)+1):
            Amount = request.POST["OIAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            OITitleID_ = request.POST["OITitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=OITitleID_)
            v = FBW_Other_Food_Internal_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )   
            
        for x in range(int(TotalItem)+1):
            Amount = request.POST["OETitleID_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            OETitleID_ = request.POST["OETitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=OETitleID_)
            v1 = FBW_Other_Food_External_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj ) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["OBIAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            OBITitleID_ = request.POST["OBITitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=OBITitleID_)
            v2 = FBW_Other_Beverage_Internal_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj ) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["OBEAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            OBETitleID_ = request.POST["OBETitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=OBETitleID_)
            v3 = FBW_Other_Beverage_External_Covers_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )   
# For Thirteen table (Other Food Internal View) 
      
        for x in range(int(TotalItem)+1):
            Amount = request.POST["OAAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            OATitleID_ = request.POST["OATitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=OATitleID_)
            v3 = FBW_Other_Food_Average_Check_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj ) 
        
        for x in range(int(TotalItem)+1):
            Amount = request.POST["OAAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            OA1TitleID_ = request.POST["OA1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=OA1TitleID_)
            v3 = FBW_Other_Food_Average_Check_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )   
        for x in range(int(TotalItem)+1):
            Amount = request.POST["OBAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            OBTitleID_ = request.POST["OA1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=OA1TitleID_)
            v3 = FBW_Other_Beverage_Average_Check_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["OBAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            OB1TitleID_ = request.POST["OB1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=OB1TitleID_)
            v3 = FBW_Other_Beverage_Average_Check_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
             
    # For Fourteen table (Other Food Internal View) 
        
        for x in range(int(TotalItem)+1):
            Amount = request.POST["OFRAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            OFRTitleID_ = request.POST["OFRTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=OFRTitleID_)
            v3 = FBW_Other_Food_Revenue_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["OFR1Amount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            OFR1TitleID_ = request.POST["OFR1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=OFR1TitleID_)
            v3 = FBW_Other_Food_Revenue_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["OBRAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            OBRTitleID_ = request.POST["OBRTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=OBRTitleID_)
            v3 = FBW_Other_Beverage_Revenue_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["OBR1Amount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            OBR1TitleID_ = request.POST["OBR1TitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=OBR1TitleID_)
            v3 = FBW_Other_Beverage_Revenue_1_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
    
# For Fifteen table (Other Food Internal View)  
        for x in range(int(TotalItem)+1):
            Amount = request.POST["CRBAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            CRBTitleID_ = request.POST["CRBTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=CRBTitleID_)
            v3 = FBW_Capture_Rates_Breakfast_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
            
# For Sixteen table (Other Food Internal View) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["CRLAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            CRLTitleID_ = request.POST["CRLTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=CRLTitleID_)
            v3 = FBW_Capture_Rates_Launch_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
# For Seventeen table (Other Food Internal View) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["CRDAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            CRDTitleID_ = request.POST["CRDTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=CRDTitleID_)
            v3 = FBW_Capture_Rates_Dinner_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )  
            

# For Eighteen table (Other Food Internal View) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["CRSAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            CRSTitleID_ = request.POST["CRSTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=CRSTitleID_)
            v3 = FBW_Capture_Rates_Supper_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )
     
# For Nighteen table (Other Food Internal View) 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["CROAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            CROTitleID_ = request.POST["CROTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=CROTitleID_)
            v3 = FBW_Capture_Rates_Others_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )
# For Twenteen table (Other Food Internal View)      
        for x in range(int(TotalItem)+1):
            Amount = request.POST["CRAMTAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0                 
            CRAMTTitleID_ = request.POST["CRAMTTitleID_" + str(x)]                
            TitleObje=FB_Worksheet_Master.objects.get(id=CRAMTTitleID_)
            v3 = FBW_Capture_Rates_AllMealTypes_Details.objects.create(Amount = Amount,
                                                       FB_Worksheet_Master=TitleObje,
                                                   FB_Worksheet_EnrtyMaster= EntOBj )

        return(redirect('/HotelBudget/FB_WorksheetList'))   
    mem = FB_Worksheet_Master.objects.filter(IsDelete = False)    
  
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'FB_Worksheet/FB_WorksheetEntry.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})



def FB_WorksheetEdit(request , id):
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
       
        mem = FB_Worksheet_EnrtyMaster.objects.get(id = id) 
                   
        mem.EntryMonth = EntryMonth
        mem.EntryYear =EntryYear
        mem.save()  
        
    # Breakfast food internal covers    
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            Amount = request.POST["Amount_" + str(x)]
            if(Amount == ''):
                Amount = 0
            TitleID_ = request.POST["TitleID_" + str(x)]
            mem1 = FB_Worksheet_EnrtyMaster.objects.get(id = id)
              
            sv = FBW_Break_food_Internal_Covers_Details.objects.get(FB_Worksheet_EnrtyMaster = id , FB_Worksheet_Master = TitleID_)
            sv.Amount = Amount
            sv.save()
 # Breakfast food external covers 
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            Amount = request.POST["Amount1_" + str(x)]
            if(Amount == ''):
                Amount = 0
            BTitleID_  = request.POST["BTitleID_" + str(x)]
            mem1 = FB_Worksheet_EnrtyMaster.objects.get(id = id)
              
            sv = FBW_Break_food_External_Covers_Details.objects.get(FB_Worksheet_EnrtyMaster = id , FB_Worksheet_Master = BTitleID_)
            sv.Amount = Amount
            sv.save()       
 # Breakfast food Beverage Internal covers 
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            Amount = request.POST["Amount2_" + str(x)]
            if(Amount == ''):
                Amount = 0
            BBTitleID_   = request.POST["BBTitleID_" + str(x)]
            mem1 = FB_Worksheet_EnrtyMaster.objects.get(id = id)
              
            sv = FBW_Break_Beverage_Internal_Covers_Details.objects.get(FB_Worksheet_EnrtyMaster = id , FB_Worksheet_Master = BBTitleID_)
            sv.Amount = Amount
            sv.save()                 
 # Breakfast food Beverage External covers 
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            Amount = request.POST["Amount3_" + str(x)]
            if(Amount == ''):
                Amount = 0
            BExTitleID_    = request.POST["BExTitleID_" + str(x)]
            mem1 = FB_Worksheet_EnrtyMaster.objects.get(id = id)
              
            sv = FBW_Break_Beverage_External_Covers_Details.objects.get(FB_Worksheet_EnrtyMaster = id , FB_Worksheet_Master = BExTitleID_)
            sv.Amount = Amount
            sv.save()    
 # Breakfast food Average Check    
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            Amount = request.POST["BVCAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0
            BVCTitleID_     = request.POST["BVCTitleID_" + str(x)]
            mem1 = FB_Worksheet_EnrtyMaster.objects.get(id = id)
              
            sv = FBW_Break_Food_Average_Check_Details.objects.get(FB_Worksheet_EnrtyMaster = id , FB_Worksheet_Master = BVCTitleID_)
            sv.Amount = Amount
            sv.save()    
 # Breakfast food Average Check 
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            Amount = request.POST["BVCAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0
            BVC1TitleID_      = request.POST["BVC1TitleID_" + str(x)]
            mem1 = FB_Worksheet_EnrtyMaster.objects.get(id = id)
              
            sv = FBW_Break_Food_Average_Check_1_Details.objects.get(FB_Worksheet_EnrtyMaster = id , FB_Worksheet_Master = BVC1TitleID_)
            sv.Amount = Amount
            sv.save()     
 # Breakfast Beverage Average Check 
 
        # TotalItem = request.POST["TotalItem"]
        # for x in range(int(TotalItem)+1):
            
        #     Amount = request.POST["BBAAmount1_" + str(x)]
        #     if(Amount == ''):
        #         Amount = 0
        #     BBATitleID_       = request.POST["BBATitleID_" + str(x)]
        #     mem1 = FB_Worksheet_EnrtyMaster.objects.get(id = id)
              
        #     sv = FBW_Break_Beverage_Average_Check_Details.objects.get(FB_Worksheet_EnrtyMaster = id , FB_Worksheet_Master = BBATitleID_)
        #     sv.Amount = Amount
        #     sv.save()  
        
 # Breakfast Beverage Average Check 
 
        # TotalItem = request.POST["TotalItem"]
        # for x in range(int(TotalItem)+1):
            
        #     Amount = request.POST["BBAAmount2_" + str(x)]
        #     if(Amount == ''):
        #         Amount = 0
        #     BBA2TitleID_ = request.POST["BBA2TitleID_ " + str(x)] 
        #     mem1 = FB_Worksheet_EnrtyMaster.objects.get(id = id)
              
        #     sv = FBW_Break_Beverage_Average_Check_1_Details.objects.get(FB_Worksheet_EnrtyMaster = id , FB_Worksheet_Master = TitleID_)
        #     sv.Amount = Amount
        #     sv.save()  
 
    # For Third table
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            Amount = request.POST["BFRAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0
            BFRTitleID_ = request.POST["BFRTitleID_" + str(x)]
            mem1 = FB_Worksheet_EnrtyMaster.objects.get(id = id)
              
            sv = FBW_Break_Food_Revenue_Details.objects.get(FB_Worksheet_EnrtyMaster = id , FB_Worksheet_Master = BFRTitleID_ )
            sv.Amount = Amount
            sv.save()    
            
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            Amount = request.POST["BFRAmount1_" + str(x)]
            if(Amount == ''):
                Amount = 0
            BFR1TitleID_ = request.POST["BFR1TitleID_" + str(x)]
            mem1 = FB_Worksheet_EnrtyMaster.objects.get(id = id)
              
            sv = FBW_Break_Food_Revenue_1_Details.objects.get(FB_Worksheet_EnrtyMaster = id , FB_Worksheet_Master = BFR1TitleID_  )
            sv.Amount = Amount
            sv.save()   
             
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            Amount = request.POST["BBRAmount_" + str(x)]
            if(Amount == ''):
                Amount = 0
            BBRTitleID_ = request.POST["BBRTitleID_" + str(x)]
            mem1 = FB_Worksheet_EnrtyMaster.objects.get(id = id)
              
            sv = FBW_Break_Beverage_Revenue_Details.objects.get(FB_Worksheet_EnrtyMaster = id , FB_Worksheet_Master = BBRTitleID_   )
            sv.Amount = Amount
            sv.save()   
        
        # TotalItem = request.POST["TotalItem"]
        # for x in range(int(TotalItem)+1):
            
        #     Amount = request.POST["BBR1Amount_" + str(x)]
        #     if(Amount == ''):
        #         Amount = 0
        #     BBR1TitleID_  = request.POST["BBR1TitleID_" + str(x)]
        #     mem1 = FB_Worksheet_EnrtyMaster.objects.get(id = id)
              
        #     sv = FBW_Break_Beverage_Revenue_1_Details.objects.get(FB_Worksheet_EnrtyMaster = id , FB_Worksheet_Master = BBR1TitleID_ )
        #     sv.Amount = Amount
        #     sv.save()    
    
                                     
        return(redirect('/HotelBudget/FB_WorksheetList'))   
    mem1 = FBW_Break_food_Internal_Covers_Details.objects.filter(FB_Worksheet_EnrtyMaster=id,IsDelete = False).select_related("FB_Worksheet_Master")
    mem = FB_Worksheet_EnrtyMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1   
    return render(request,'FB_Worksheet/FB_WorksheetEdit.html',{'mem':mem , 'mem1':mem1 ,'CYear':range(2022,CYear) })




def FB_WorksheetView(request, id):
    template_path = "FB_Worksheet/FB_WorksheetView.html"
    mem1 = FBW_Break_food_Internal_Covers_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem2 = FBW_Break_food_External_Covers_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem3 = FBW_Break_Beverage_Internal_Covers_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem4 = FBW_Break_Beverage_External_Covers_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem5 = FBW_Break_Food_Average_Check_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem6 = FBW_Break_Food_Average_Check_1_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem7 = FBW_Break_Beverage_Average_Check_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem8 = FBW_Break_Beverage_Average_Check_1_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem9 = FBW_Break_Food_Revenue_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem10 = FBW_Break_Food_Revenue_1_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem11 = FBW_Break_Beverage_Revenue_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem12 = FBW_Break_Beverage_Revenue_1_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem13 = FBW_Launch_Food_Internal_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem14 = FBW_Launch_Food_External_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem15 = FBW_Launch_Beverage_Internal_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem16 = FBW_Launch_Beverage_External_Details.objects.filter(FB_Worksheet_EnrtyMaster =id ,IsDelete=False ).select_related("FB_Worksheet_Master")
    mem = FB_Worksheet_EnrtyMaster.objects.get(id = id)
  
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1,'mem2':mem2,'mem3':mem3,'mem4':mem4, 
            'mem5':mem5,'mem6':mem6,'mem7':mem7,'mem8':mem8,'mem9':mem9,'mem10':mem10,
            'mem11':mem11,'mem12':mem12,'mem13':mem13,'mem14':mem14,'mem15':mem15,'mem16':mem16,  'CMonth':CMonth }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
  
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
   
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
   
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 





def  YearlyReport(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    current_year = datetime.datetime.now().year
    years = range(2022, current_year + 1)


    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
    'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = "https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID="+str(OrganizationID)
    # response = requests.get(api_url, headers=headers)
    # # response_content = response.content.decode('utf-8')
    # mem = response.json()

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        mem = response.json()
      #  return JsonResponse(mem)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    I=""
    if 'I' in request.GET:
        I=request.GET["I"]
    else:
        I = OrganizationID
    rt=""
    if 'rt' in request.GET:
        rt=request.GET["rt"]
    else:
        rt = "plu"
    results=[];
    print(rt)
    if rt=="plu":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_PLUtility_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="pleng":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_PLengineering_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="plsm":
            with connection.cursor() as cursor:
                cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_SM_salemarketingentry_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
                results = cursor.fetchall()
    elif rt=="plit":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_IT_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="plsecurity":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_Security_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="plhr":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_HR_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="plag":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_AGAG_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="pltotalag":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_TotalAg_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="RentalOtherIncome":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_RentalOtherIncome_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="MinorGuestCommunication":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_MinorGuestCommunication_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="OODBusinessCentre":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_OODBusinessCentre_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="OODGuestLaundry":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_OODGuestLaundry_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="OODTransport":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_OODTransport_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="OODSPA":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_OODSPA_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="TotalOOD":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_TotalOOD_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="FBOOD":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_FBOOD_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="FBBanquet":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_FBBanquet_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()

    elif rt=="FBMiniBar":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_FBMiniBar_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="FB_IRD":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_FB_IRD_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="Outlet1":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_Outlet1_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="Outlet2":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_Outlet2_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="Outlet3":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_Outlet3_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="Outlet4":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_Outlet4_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="Outlet5":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_Outlet5_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="PLFBOutlets":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_PLFBOutlets_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="TotalFB":
        with connection.cursor() as cursor:
            cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_TotalFB_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
            results = cursor.fetchall()
    elif rt=="RoomsWorksheet":
        print("A")
        

        hotelapitoken = MasterAttribute.HotelAPIkeyToken
        headers = {
        'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
        }

        I=""
        if 'I' in request.GET:
            I=request.GET["I"]
        else:
            I = OrganizationID

        EntryYear=""
        if 'EntryYear' in request.GET:
            EntryYear=request.GET["EntryYear"]
        else:
            EntryYear=current_year


        Expapi_url = "https://hotelops.in/API/HotelBudgetAPI/YearlyReport_RoomsWorksheet_entryDetails_Select?OrganizationID="+str(3)+"&EntryYear="+str(EntryYear)
        # response = requests.get(api_url, headers=headers)
        # # response_content = response.content.decode('utf-8')
        # mem = response.json()

        try:
            response = requests.get(Expapi_url, headers=headers)
            response.raise_for_status()  # Optional: Check for any HTTP errors
            DataRes = response.json()
        #  return JsonResponse(mem)
            
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
        table=""
        if DataRes!=[]:
            headers = list(DataRes[0].keys())

            # Create the table headers
            table_header = '<thead><tr>'
            for header in headers:
                table_header += f'<th>{header}</th>'
            table_header += '</tr></thead>'

            # Create the table body
            table_body = '<tbody>'
            for item in DataRes:
                table_body += '<tr>'
                for key, value in item.items():
                    table_body += f'<td>{value}</td>'
                table_body += '</tr>'
            table_body += '</tbody>'

            # Combine the table header and body
        table = f'<table id="tableData" class="table table-bordered">{table_header}{table_body}</table>'
        context = {'years': years,'mem':mem,'DataRes':DataRes,'results':results}
        return render(request, 'HotelBudgetReport/YearlyReport.html' ,context) 
        #execute_stored_procedure_and_wait()
        # with connection.cursor() as cursor:
        #     print("1")
        #     cursor.execute("EXEC PyHotelBudget_SP_Report_YearlyReport_RoomsWorksheetTest_entryDetails_Select @OrganizationID=%s, @EntryYear=%s", [3,2023])
        #     print("2")
        #     results = cursor.fetchone()
        #     print(results)
    elif rt=="FBWorksheet":
        print("A")
        DataResFBW=[]

        hotelapitoken = MasterAttribute.HotelAPIkeyToken
        headers = {
        'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
        }

        I=""
        if 'I' in request.GET:
            I=request.GET["I"]
        else:
            I = OrganizationID

        EntryYear=""
        if 'EntryYear' in request.GET:
            EntryYear=request.GET["EntryYear"]
        else:
            EntryYear=current_year


        Expapi_url = "https://hotelops.in/API/HotelBudgetAPI/YearlyReport_FBWorksheet_entryDetails_Select?OrganizationID="+str(3)+"&EntryYear="+str(EntryYear)
        # response = requests.get(api_url, headers=headers)
        # # response_content = response.content.decode('utf-8')
        # mem = response.json()

        try:
            response = requests.get(Expapi_url, headers=headers)
            response.raise_for_status()  # Optional: Check for any HTTP errors
            DataResFBW = response.json()
        #  return JsonResponse(mem)
            
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
        table=""
        table_header=""
        table_body=""
        

            # Combine the table header and body
        table = f'<table id="tableData" class="table table-bordered">{table_header}{table_body}</table>'
        print(DataResFBW)
        context = {'years': years,'mem':mem,'DataResFBW':DataResFBW,'results':results}
        return render(request, 'HotelBudgetReport/YearlyReport.html' ,context) 

    # Run the asyncio event loop with the main coroutine
    context = {'years': years,'mem':mem,'results':results}
    
    return render(request, 'HotelBudgetReport/YearlyReport.html' ,context) 



