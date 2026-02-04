from argparse import REMAINDER
from copyreg import remove_extension
import datetime

from decimal import Decimal
from django.db import router
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
import requests
from HotelBudget.models import AG_Analysis_Master, AG_AnalysisEntryDetail, AG_AnalysisEntryMaster, AG_HREntryDetails, AG_HREntryMaster, AG_HRMaster, AG_SecurityEntryDetails, AG_SecurityEntryMaster, AG_SecurityMaster, IT_EntryMaster, It_OtherExpenseEntryDetails, It_ServiceEntryDetails, It_SystemExpenseEntryDetails, ItOtherExpenseMaster, ItServiceMaster, ItSystemExpenseMaster, MinorGuestEntryDetail, MinorGuestEntryMaster, MinorGuestMaster, OOD_LaundryEntryDetail, OOD_LaundryEntryMaster, OOD_LaundryMaster, OOD_TransportEntryDetail, OOD_TransportEntryMaster, OOD_TransportMaster, OODBusinessEntryDetail, OODBusinessEntryMaster, OODBusinessMaster, PL_Engineering_Entry_Master, PL_Engineering_EntryDetails, PL_Engineering_Master, PLUtilitiesEntryDetails, PLUtilitiesEntryMaster, PLUtilitiesMaster, Rental_Other_IncomeEntryDetail, Rental_Other_IncomeEntryMaster, Rental_Other_IncomeMaster, SM_MarketingEntryDetails, SM_MarketingExpenseMaster, SM_SaleMarketingEntryMaster, SM_SalesEntryDetails, SM_SalesExpenseMaster, Total_AG_Master, Total_AGEntryDetails, Total_AGEntryMaster
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
        InHouseLimousineRevenue = request.POST["InHouseLimousineRevenue"]
        if(InHouseLimousineRevenue == ''):
            InHouseLimousineRevenue =0
        ExternalLimousineRevenue = request.POST["ExternalLimousineRevenue"]
        if(ExternalLimousineRevenue == ''):
            ExternalLimousineRevenue =0
        ExternalGuestTransportation  = request.POST['ExternalGuestTransportation']
        if(ExternalGuestTransportation == ''):
            ExternalGuestTransportation =0
        GuestTransportationRevenue = request.POST["GuestTransportationRevenue"]
        if(GuestTransportationRevenue == ''):
            GuestTransportationRevenue = 0
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
                            InHouseLimousineRevenue=InHouseLimousineRevenue,ExternalLimousineRevenue=ExternalLimousineRevenue,
                       ExternalGuestTransportation = ExternalGuestTransportation,GuestTransportationRevenue=GuestTransportationRevenue,  
                          GuestTransportRevenue = GuestTransportRevenue  ,  Cost_OfGuestTransportation= Cost_OfGuestTransportation,
                       Total_CostOfSales= Total_CostOfSales,  Gross_Profit= Gross_Profit,
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




            

            

    context = {'years': years,'mem':mem,'results':results}

    return render(request, 'HotelBudgetReport/YearlyReport.html' ,context) 
