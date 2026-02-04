from argparse import REMAINDER
from copyreg import remove_extension
from datetime import date
import datetime
from decimal import Decimal
from django.db import router
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from app.models import MonthListMaster
from django.db.models import Subquery
from django.db.models import OuterRef
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from .models import AG_Analysis_Master, AG_AnalysisEntryDetail, AG_AnalysisEntryMaster, AG_HREntryDetails, AG_HREntryMaster, AG_HRMaster, AG_SecurityEntryDetails, AG_SecurityEntryMaster, AG_SecurityMaster, FB_BanquetEntryDetail, FB_BanquetEntryMaster, FB_BanquetMaster, FB_IRDEntryDetail, FB_IRDEntryMaster, FB_IRDMaster, IT_EntryMaster, It_ServiceEntryDetails, It_SystemExpenseEntryDetails, ItServiceMaster, ItSystemExpenseMaster, OOD_HealthEntryDetail, OOD_HealthEntryMaster, OOD_HealthMaster, OOD_LaundryEntryDetail, OOD_LaundryEntryMaster, OOD_LaundryMaster, OOD_TransportEntryDetail, OOD_TransportEntryMaster, OOD_TransportMaster, Outlet,Expenses, Outlet_1EntryDetail, Outlet_1EntryMaster, Outlet_1Master, Outlet_2EntryDetail, Outlet_2EntryMaster, Outlet_2Master, Outlet_3EntryDetail, Outlet_3EntryMaster, Outlet_3Master, Outlet_4EntryDetail, Outlet_4EntryMaster, Outlet_4Master, Outlet_5EntryDetail, Outlet_5EntryMaster, Outlet_5Master, PL_Engineering_EntryDetails, PL_Engineering_Master,  PL_Engineering_Entry_Master, PL_RoomsEntryDetail, PL_RoomsEntryMaster, PL_RoomsMaster, PL_SummaryEntryDetail, PL_SummaryEntryMaster, PL_SummaryMaster, PLUtilitiesEntryDetails, PLUtilitiesEntryMaster,PayrollExpenses, PayrollExpensesEntry,PLUtilitiesMaster, Rental_Other_IncomeEntryDetail, Rental_Other_IncomeEntryMaster, Rental_Other_IncomeMaster, SM_MarketingEntryDetails, SM_MarketingExpenseMaster, SM_SaleMarketingEntryMaster, SM_SalesEntryDetails, SM_SalesExpenseMaster,  Total_AG_Master, Total_AGEntryDetails, Total_AGEntryMaster, Total_FBEntryDetail, Total_FBEntryMaster, Total_FBMaster, Total_OODEntryDetail, Total_OODEntryMaster, Total_OODMaster
from django.db import connection
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO

def homepage(request):
    # cursor = connection.cursor()
    # try:
    #    cursor.execute('[dbo].[HBudgetReport_SP_Expense_Caluclation_Update]',[])
       
    # finally:
    #    cursor.close()
    return render(request, 'homepage.html' )
 
def index(request):
    if 'OrgaizationID' not in request.session:
        return redirect(MasterAttribute)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    mem = Outlet.objects.filter(IsDelete=False)
    return render(request, 'index.html' ,{'mem' :mem})

def add(request):
    if request.method == "POST":
        title = request.POST['title']
        obj = Outlet.objects.create(title = title)
        obj.save()
        return (redirect('/'))
    
    return render(request,'add.html')

    
def delete(request,id):
    mem = Outlet.objects.get(id = id)
    mem.IsDelete=True
    mem.ModifyBy=1
    mem.save()
    #mem.delete()
    return redirect('/')


def update(request , id):
    mem = Outlet.objects.get(id = id)
    return render(request,'update.html',{'mem':mem})

def updata (request , id):
    title = request.POST["title"]
    mem = Outlet.objects.get(id = id)
    mem.title = title
    mem.save()
    
    return redirect("/")
 

def expenses(request):
    
    if 'OrgaizationID' not in request.session:
        return redirect(MasterAttribute)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    rem = Expenses.objects.all()
    return render(request, 'expenses.html' ,{'rem' :rem})


def add_expenses(request):
    if request.method == "POST":
        title = request.POST['title']
        obj = Expenses.objects.create(title = title)
        obj.save()
        return (redirect('/expenses'))
    return render(request,'add_expenses.html')
    
def delete_expenses(request,id):
    rem = Expenses.objects.get(id = id)
    rem.delete()
    return redirect('/expenses')



def update_expenses(request , id):
    if request.method == "POST":
        title = request.POST["title"]
        rem = Expenses.objects.get(id = id)
        rem.title = title
        rem.save()    
        return redirect("/expenses")
    rem = Expenses.objects.get(id = id)
    return render(request,'update_expenses.html',{'rem':rem})

# def updata_expenses(request , id):
#     title = request.POST["title"]
#     rem = Expenses.objects.get(id = id)
#     rem.title = title
#     rem.save()    
#     return redirect("/expenses")


def payrollExpenses(request):
    
    if 'OrgaizationID' not in request.session:
        return redirect(MasterAttribute)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    mem = PayrollExpenses.objects.filter(IsDelete=False)
    return render(request, 'Payroll/payrollExpenses.html' ,{'mem' :mem})

def add_payrollExpenses(request):
    if request.method == "POST":
        title = request.POST['title']
        obj = PayrollExpenses.objects.create(title = title)
        obj.save()
        return (redirect('/PayrollExpenses'))
    return render(request,'Payroll/add_payrollExpenses.html')

def delete_payrollExpenses(request,id):
    mem = PayrollExpenses.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/PayrollExpenses'))

def update_payrollExpenses(request , id):
    if request.method == "POST":
        title = request.POST["title"]
        rem = PayrollExpenses.objects.get(id = id)
        rem.title = title
        rem.save()    
        return (redirect('/PayrollExpenses'))
    rem = PayrollExpenses.objects.get(id = id)
    return render(request,'Payroll/update_PayrollExpenses.html',{'rem':rem})
    
    

def PayrollExpenseEntry(request):
    
    if 'OrgaizationID' not in request.session:
        return redirect(MasterAttribute)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == "POST":
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)):
            Amount=request.POST["Amount_"+str(x)]
            ExpenseID=request.POST["ExpenseID_"+str(x)]
            v=PayrollExpenses.objects.get(id=ExpenseID)
            obj = PayrollExpensesEntry.objects.create(ExpenseID =v ,Amount=Amount)
            obj.save()
        
        # title = request.POST['title']
        # obj = Outlet.objects.create(title = title)
        # obj.save()
        #return (redirect('/'))
    mem = PayrollExpenses.objects.filter(IsDelete=False)
    return render(request,'Payroll/PayrollExpenseEntry.html',{'mem' :mem})


 
def  PLUtilitiesList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = PLUtilitiesEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'PLUtilities/PLUtilitiesList.html' ,{'mem' :mem }) 



def delete_PLUtilities (request,id):
    mem = PLUtilitiesEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/HBudgetReport/PLUtilitiesList'))


def PLUtilitiesEdit(request , id):
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
                                                        
        return(redirect('/HBudgetReport/PLUtilitiesList'))   
    mem1 = PLUtilitiesEntryDetails.objects.filter(PLUtilitiesEntryMaster=id,IsDelete = False).select_related("PLUtilitiesMaster")
    mem = PLUtilitiesEntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1   
    return render(request,'PLUtilities/PLUtilitiesEdit.html',{'mem':mem , 'mem1':mem1 ,'CYear':range(2022,CYear) })



def PLUtilitiesView(request , id):
  
    template_path = "PLUtilities/PLUtilitiesviewdata.html"
    # NileLogo=MasterAttribute.NileLogo
    mem1 = PLUtilitiesEntryDetails.objects.filter(PLUtilitiesEntryMaster=id,IsDelete = False).select_related("PLUtilitiesMaster")
    mem = PLUtilitiesEntryMaster.objects.get(id = id)
    #  ScantyBaggageForm=forms.ScantyBaggageForm()
    
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }

    # context = {'myvar': 'this is your template context','p':varM}
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(mydict)

    # create a pdf
    result = BytesIO()
    #  pisa_status = pisa.CreatePDF(
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        # html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 
  
   
def PutilitiesEntry(request):
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
        return(redirect('/HBudgetReport/PLUtilitiesList'))
    mem = PLUtilitiesMaster.objects.filter(IsDelete = False)    
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'PLUtilities/PLUtilitiesEntry.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})


def Engviewdata(request, id):
    template_path = "Eng/Engviewdata.html"
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
  
          
def PL_EngineeringEntry(request):
    
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
        TraineeStaff = request.POST['TraineeStaff']
        if(TraineeStaff==''):
            TraineeStaff=0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses=0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
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
                                    SalaryAndWages=SalaryAndWages , TraineeStaff=TraineeStaff , Salary_Wages_and_Bonuses=Salary_Wages_and_Bonuses,
                                    EmployeeBenefits=EmployeeBenefits,Total_Other_Expenses=Total_Other_Expenses,
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
        
        return(redirect('/HBudgetReport/EngineeringList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = PL_Engineering_Master.objects.filter(IsDelete=False)
    return render(request, 'Eng/PL_Engineering_Entry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})


def  EngList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = PL_Engineering_Entry_Master.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    return render(request, 'Eng/EngineeringList.html' ,{'mem' :mem }) 


def EngListEdit(request , id):
    if request.method == "POST":
        
        EntryMonth = request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        SalaryAndWages = request.POST["SalaryAndWages"]
        TraineeStaff = request.POST['TraineeStaff']
        Salary_Wages_and_Bonuses = request.POST["Salary_Wages_and_Bonuses"]
        EmployeeBenefits = request.POST["EmployeeBenefits"]
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        TotalExpenses = request.POST['TotalExpenses']
        
        mem = PL_Engineering_Entry_Master.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.SalaryAndWages = SalaryAndWages
        mem.TraineeStaff = TraineeStaff
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits = EmployeeBenefits
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
                             
       
        return(redirect('/HBudgetReport/EngineeringList'))
    mem1 = PL_Engineering_EntryDetails.objects.filter(PL_Engineering_Entry_Master=id ,IsDelete = False).select_related("PL_Engineering_Master")
    mem = PL_Engineering_Entry_Master.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear) +1
    return render(request,'Eng/EngEdit.html',{'mem':mem,'mem1':mem1 , 'CYear':range(2022,CYear)})


def EngListDelete(request,id):
    mem = PL_Engineering_Entry_Master.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/EngineeringList'))

 
 
def AG_Securityviewdata(request, id):
    template_path = "AG_Security/AG_Securityviewdata.html"
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
 
 
def AG_SecurityEntry(request):
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
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
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
                                                Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
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
        
        return(redirect('/HBudgetReport/AG_SecurityList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  AG_SecurityMaster.objects.filter(IsDelete = False)  
    return render(request , 'AG_Security/AG_SecurityEntry.html' ,{'mem':mem ,'CYear':range(CYear,2020,-1),'CMonth':CMonth})
   

def AG_SecurityList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = AG_SecurityEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )       
    return render(request, 'AG_Security/AG_SecurityList.html' ,{'mem' :mem }) 


def AG_SecurityEdit(request,id):
    if request.method =="POST":
        
        EntryMonth =  request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses  = request.POST['PayrollRelatedExpenses']
        ExpensesPayrollAndRelated = request.POST['ExpensesPayrollAndRelated']
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        TotalExpenses = request.POST['TotalExpenses']
        
        mem = AG_SecurityEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives =  Bonuses_and_Incentives
        mem.Salary_Wages_and_Bonuses = Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =  EmployeeBenefits
        mem.PayrollRelatedExpenses  =   PayrollRelatedExpenses  
        mem.ExpensesPayrollAndRelated  =   ExpensesPayrollAndRelated 
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
            
        return(redirect('/HBudgetReport/AG_SecurityList'))
    mem1 = AG_SecurityEntryDetails.objects.filter(AG_SecurityEntryMaster=id , IsDelete=False).select_related("AG_SecurityMaster")
    mem = AG_SecurityEntryMaster.objects.get(id = id)  
    
    today = datetime.date.today()
    CYear = today.year        
    CYear = int(CYear)+1
    mem = AG_SecurityEntryMaster.objects.get(id = id)
    return render(request , 'AG_Security/AG_SecurityEdit.html' , {'mem' :mem , 'mem1':mem1 ,'CYear':range(2022,CYear)})
          
        
def AG_SecurityDelete(request,id):
    mem = AG_SecurityEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/AG_SecurityList'))



def AG_HRviewdata(request, id):
    template_path = "AG_HR/AG_HRviewdata.html"
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
 

def AG_HRList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = AG_HREntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'AG_HR/AG_HRList.html' ,{'mem' :mem }) 

def AG_HREntry(request):
       
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
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives ==''):
            Bonuses_and_Incentives =0
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
                                                Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
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
        
        return(redirect('/HBudgetReport/AG_HRList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  AG_HRMaster.objects.filter(IsDelete = False)  
    return render(request , 'AG_HR/AG_HREntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})
    

def AG_HREdit(request,id):
    
    if request.method =="POST":
        EntryMonth =  request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
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
        mem.Bonuses_and_Incentives =  Bonuses_and_Incentives
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
        return(redirect('/HBudgetReport/AG_HRList'))       
    mem1 = AG_HREntryDetails.objects.filter(AG_HREntryMaster=id , IsDelete =False).select_related("AG_HRMaster")
    mem = AG_HREntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear) +1
    return render(request , 'AG_HR/AG_HREdit.html' , {'mem' :mem ,'mem1':mem1 , 'CYear':range(2022,CYear)})

     
def AG_HRDelete(request,id):
    mem = AG_HREntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/HBudgetReport/AG_HRList'))





def Total_AGviewdata(request, id):
    template_path = "Total_AG/Total_AGviewdata.html"
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
      
  
def Total_AGList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Total_AGEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )   
     
    return render(request, 'Total_AG/Total_AGList.html' ,{'mem' :mem }) 
              

def Total_AGEntry(request):    
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
        if(Bonuses_and_Incentives ==''):
            Bonuses_and_Incentives =0
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
                                                Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
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
        
        return(redirect('/HBudgetReport/Total_AGList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  Total_AG_Master.objects.filter(IsDelete = False)  
    return render(request , 'Total_AG/Total_AGEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})



def Total_AGDelete(request,id):
    mem = Total_AGEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/Total_AGList'))



def Total_AGEdit(request,id):
    if request.method =="POST":
        
        EntryMonth =  request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
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
            Amount = request.POST["Amount_" + str(x)]
            mem1 = Total_AGEntryMaster.objects.get(id = id)
            sv = Total_AGEntryDetails.objects.get(Total_AG_Master = TitleID_ , Total_AGEntryMaster = id)
            sv.Amount = Amount
            sv.save()
            
        return(redirect('/HBudgetReport/Total_AGList'))
             
    mem1 = Total_AGEntryDetails.objects.filter( Total_AGEntryMaster=id ,IsDelete = False).select_related("Total_AG_Master")
    mem = Total_AGEntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    
    mem = Total_AGEntryMaster.objects.get(id = id)
    return render(request , 'Total_AG/Total_AGEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})



  
 
def SMviewdata(request, id):
    template_path = "SalesMarketing/SMviewdata.html"
    mem1 = SM_SalesEntryDetails.objects.filter(SM_SaleMarketingEntryMaster=id , IsDelete = False).select_related("SM_SalesExpenseMaster")
    mem = SM_SaleMarketingEntryMaster.objects.get(id = id)
    mem2 = SM_SalesEntryDetails.objects.filter(SM_SaleMarketingEntryMaster=id , IsDelete = False).select_related("SM_MarketingExpenseMaster")
  
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
       
  
def SMList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = SM_SaleMarketingEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()
     
    return render(request, 'SalesMarketing/SMList.html' ,{'mem' :mem }) 
       
       
def SMEntry(request):    
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
                                                Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
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
              
        
        return(redirect('/HBudgetReport/SMList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month       
    mem =  SM_SalesExpenseMaster.objects.filter(IsDelete = False)  
    mem1 = SM_MarketingExpenseMaster.objects.filter(IsDelete = False)
    return render(request , 'SalesMarketing/SMEntry.html' ,{'mem':mem ,'mem1':mem1, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def SMDelete(request,id):
    mem =  SM_SaleMarketingEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/SMList'))




def SMEdit(request,id):
    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
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
        mem.Bonuses_and_Incentives =  Bonuses_and_Incentives
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
            
        return(redirect('/HBudgetReport/SMList'))
             
    mem1 = SM_SalesEntryDetails.objects.filter( SM_SaleMarketingEntryMaster=id ,IsDelete = False).select_related("SM_SalesExpenseMaster")
    mem2 = SM_MarketingEntryDetails.objects.filter(SM_SaleMarketingEntryMaster =id ,IsDelete=False ).select_related("SM_MarketingExpenseMaster")
    mem = SM_SaleMarketingEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'SalesMarketing/SMEdit.html' , {'mem1' :mem1 ,'mem2':mem2, 'mem':mem ,'CYear':range(2022,CYear)})





  
def ITList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = IT_EntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()
     
    return render(request, 'IT/ITList.html' ,{'mem' :mem }) 
       

def ITEntry(request):    
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
        TotalExpenses = request.POST['TotalExpenses']
        if(TotalExpenses==''):
            TotalExpenses=0
        Total_Cost_Of_Services = request.POST['Total_Cost_Of_Services']
        if(Total_Cost_Of_Services==''):
            Total_Cost_Of_Services=0

        enmaster = IT_EntryMaster.objects.create(EntryMonth = EntryMonth , EntryYear = EntryYear ,SalaryAndWages = SalaryAndWages ,
                                                Bonuses_and_Incentives=Bonuses_and_Incentives,  Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,
                                EmployeeBenefits = EmployeeBenefits ,  PayrollRelatedExpenses= PayrollRelatedExpenses,
                               PayrollAndRelatedExpenses= PayrollAndRelatedExpenses, Total_Other_Expenses= Total_Other_Expenses,
                               TotalExpenses = TotalExpenses,Total_Cost_Of_Services=Total_Cost_Of_Services,OrganizationID=OrganizationID,CreatedBy=UserID  )
        enmaster.save() 
              
        EntObj = IT_EntryMaster.objects.get(id=enmaster.pk)   
        TotalItem = request.POST["TotalItem"]      
        for x in range(int(TotalItem)+1):
            
            AmountServices = request.POST["MAmount_" + str(x)]
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
                     
        return(redirect('/HBudgetReport/ITList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month     
    mem =  ItServiceMaster.objects.filter(IsDelete = False)  
    mem1 = ItSystemExpenseMaster.objects.filter(IsDelete = False)
    return render(request , 'IT/ITEntry.html' ,{'mem':mem ,'mem1':mem1, 'CYear':range(CYear,2020,-1),'CMonth':CMonth})


def ITDelete(request,id):
    mem =  IT_EntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/ITList'))


def ITEdit(request,id):
    
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
            
        return(redirect('/HBudgetReport/ITList'))
             
    mem1 = It_ServiceEntryDetails.objects.filter(IT_EntryMaster=id ,IsDelete = False).select_related("ItServiceMaster")
    mem2 =  It_SystemExpenseEntryDetails.objects.filter(IT_EntryMaster =id ,IsDelete=False ).select_related("ItSystemExpenseMaster")
    mem = IT_EntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request , 'IT/ITEdit.html' , {'mem1' :mem1 ,'mem2':mem2, 'mem':mem ,'CYear':range(2022,CYear)})





 
def AG_Analysisviewdata(request, id):
    template_path = "AG_RatioAnalysis/AG_Ratioviewdata.html"
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
      
  
def AG_AnalysisList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = AG_AnalysisEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'AG_RatioAnalysis/AG_AnalysisList.html' ,{'mem' :mem }) 
       

        
def AG_AnalysisEntry(request):
    
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
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives = 0
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
                                    SalaryAndWages=SalaryAndWages, Bonuses_and_Incentives= Bonuses_and_Incentives, Salary_Wages_and_Bonuses=Salary_Wages_and_Bonuses,
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
        
        return(redirect('/HBudgetReport/AG_AnalysisList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = AG_Analysis_Master.objects.filter(IsDelete=False)
    return render(request, 'AG_RatioAnalysis/AG_AnalysisEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})


def AG_AnalysisDelete(request,id):
    mem =  AG_AnalysisEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/AG_AnalysisList'))


def AG_AnalysisEdit(request,id):
    if request.method =="POST":
        
        EntryMonth =  request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
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
            Amount = request.POST["Amount_" + str(x)]
            mem1 = AG_AnalysisEntryMaster.objects.get(id = id)
            sv = AG_AnalysisEntryDetail.objects.get(AG_Analysis_Master = TitleID_ , AG_AnalysisEntryMaster = id)
            sv.Amount = Amount
            sv.save()
            
        return(redirect('/HBudgetReport/AG_AnalysisList'))
             
    mem1 = AG_AnalysisEntryDetail.objects.filter( AG_AnalysisEntryMaster=id ,IsDelete = False).select_related("AG_Analysis_Master")
    mem = AG_AnalysisEntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    
    mem = AG_AnalysisEntryMaster.objects.get(id = id)
    return render(request ,'AG_RatioAnalysis/AG_AnalysisEdit.html' , {'mem' :mem , 'mem1':mem1 ,'CYear':range(2022,CYear)})







 
def Rental_Incomeviewdata(request, id):
    template_path = "Rental_Other_Income/Rental_Incomeviewdata.html"
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
  
def Rental_IncomeList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Rental_Other_IncomeEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'Rental_Other_Income/Rental_IncomeList.html' ,{'mem' :mem }) 
       
def Rental_IncomeEntry(request):
    
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
        
        return(redirect('/HBudgetReport/Rental_IncomeList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = Rental_Other_IncomeMaster.objects.filter(IsDelete=False)
    return render(request, 'Rental_Other_Income/Rental_IncomeEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def Rental_IncomeDelete(request,id):
    mem =  Rental_Other_IncomeEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/Rental_IncomeList'))

def Rental_IncomeEdit(request,id):
    
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
            
        return(redirect('/HBudgetReport/Rental_IncomeList'))
             
    mem1 = Rental_Other_IncomeEntryDetail.objects.filter(Rental_Other_IncomeEntryMaster=id ,IsDelete = False).select_related("Rental_Other_IncomeMaster")
    mem = Rental_Other_IncomeEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'Rental_Other_Income/Rental_IncomeEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})



  

def OOD_Laundryviewdata(request, id):
    template_path = "OOD_Laundry/OOD_Laundryviewdata.html"
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
  
def OOD_LaundryList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = OOD_LaundryEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'OOD_Laundry/OOD_LaundryList.html' ,{'mem' :mem }) 
       
def OOD_LaundryEntry(request):
    
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
        
        return(redirect('/HBudgetReport/OOD_LaundryList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = OOD_LaundryMaster.objects.filter(IsDelete=False)
    return render(request, 'OOD_Laundry/OOD_LaundryEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def OOD_LaundryDelete(request,id):
    mem = OOD_LaundryEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/OOD_LaundryList'))


def OOD_LaundryEdit(request,id):   
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        Dry_CleaningServices = request.POST['Dry_CleaningServices']
        LaundryServices = request.POST['LaundryServices']
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
            
        return(redirect('/HBudgetReport/OOD_LaundryList'))
             
    mem1 = OOD_LaundryEntryDetail.objects.filter(OOD_LaundryEntryMaster=id ,IsDelete = False).select_related("OOD_LaundryMaster")
    mem = OOD_LaundryEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'OOD_Laundry/OOD_LaundryEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})






def OOD_Transportviewdata(request, id):
    template_path = "OOD_Transport/OOD_Transportviewdata.html"
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
 
def OOD_TransportList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = OOD_TransportEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'OOD_Transport/OOD_TransportList.html' ,{'mem' :mem }) 
      
     
def OOD_TransportEntry(request):   
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
        ExternalGuestTransportation  = request.POST['ExternalGuestTransportation']
        if(ExternalGuestTransportation == ''):
            ExternalGuestTransportation =0
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
                       ExternalGuestTransportation = ExternalGuestTransportation,  
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
                
        cursor = connection.cursor()
        try:
            print("test data")
            # cursor.execute('[dbo].[HBudgetReport_SP_Expense_Caluclation_Update]',[int(OrganizationID),int(EntryMonth),int(EntryYear)])
            sql = 'EXEC [dbo].[HBudgetReport_SP_Expense_Caluclation_Update] @OrganizationID=%s, @EntryMonth=%s, @EntryYear=%s'
            params = (OrganizationID, EntryMonth, EntryYear)
            cursor.execute(sql, params)
            
            print("test data1")
        finally:
            cursor.close()
        return(redirect('/HBudgetReport/OOD_TransportList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem =  OOD_TransportMaster.objects.filter(IsDelete=False)
    return render(request, 'OOD_Transport/OOD_TransportEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def OOD_TransportDelete(request,id):
    mem =  OOD_TransportEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/OOD_TransportList'))


def OOD_TransportEdit(request,id):   
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        ExternalGuestTransportation  = request.POST['ExternalGuestTransportation']
        GuestTransportRevenue = request.POST['GuestTransportRevenue']
        Cost_OfGuestTransportation = request.POST['Cost_OfGuestTransportation']
        Total_CostOfSales = request.POST['Total_CostOfSales']
        Gross_Profit  = request.POST['Gross_Profit']
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        TotalExpenses = request.POST['TotalExpenses']
        DepartmentIncome = request.POST['DepartmentIncome']
      
        mem =  OOD_TransportEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.ExternalGuestTransportation  =   ExternalGuestTransportation 
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
            
        return(redirect('/HBudgetReport/OOD_TransportList'))
             
    mem1 = OOD_TransportEntryDetail.objects.filter( OOD_TransportEntryMaster=id ,IsDelete = False).select_related("OOD_TransportMaster")
    mem =  OOD_TransportEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'OOD_Transport/OOD_TransportEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})








def OOD_Healthviewdata(request, id):
    template_path = "OOD_Health/OOD_Healthviewdata.html"
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

def OOD_HealthList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = OOD_HealthEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'OOD_Health/OOD_HealthList.html' ,{'mem' :mem }) 
      
def OOD_HealthEntry(request):  
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
        SpaTreatmentRevenue = request.POST['SpaTreatmentRevenue']
        if(SpaTreatmentRevenue == ''):
            SpaTreatmentRevenue =0
        HealthClubAndSpaRevenue   = request.POST['HealthClubAndSpaRevenue']
        if(HealthClubAndSpaRevenue == ''):
            HealthClubAndSpaRevenue =0
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
                         SpaTreatmentRevenue = SpaTreatmentRevenue ,   HealthClubAndSpaRevenue =  HealthClubAndSpaRevenue , 
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
        
        return(redirect('/HBudgetReport/OOD_HealthList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = OOD_HealthMaster.objects.filter(IsDelete=False)
    return render(request, 'OOD_Health/OOD_HealthEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def OOD_HealthDelete(request,id):
    mem = OOD_HealthEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/OOD_HealthList'))


def OOD_HealthEdit(request,id):   
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        SpaTreatmentRevenue = request.POST['SpaTreatmentRevenue']
        HealthClubAndSpaRevenue   = request.POST['HealthClubAndSpaRevenue']
        Cost_OfMerchandise  = request.POST['Cost_OfMerchandise']
        Total_CostOfSales = request.POST['Total_CostOfSales']
        Gross_Profit  = request.POST['Gross_Profit']
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        TotalExpenses = request.POST['TotalExpenses']
        DepartmentIncome = request.POST['DepartmentIncome']
      
        mem =  OOD_HealthEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.SpaTreatmentRevenue  =  SpaTreatmentRevenue 
        mem.HealthClubAndSpaRevenue =   HealthClubAndSpaRevenue
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
            
        return(redirect('/HBudgetReport/OOD_HealthList'))
             
    mem1 = OOD_HealthEntryDetail.objects.filter( OOD_HealthEntryMaster=id ,IsDelete = False).select_related("OOD_HealthMaster")
    mem =  OOD_HealthEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'OOD_Health/OOD_HealthEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})




def FB_Banquetviewdata(request, id):
    template_path = "FB_Banquet/FB_Banquetviewdata.html"
    mem1 = FB_BanquetEntryDetail.objects.filter(FB_BanquetEntryMaster=id , IsDelete = False).select_related("FB_BanquetMaster")
    mem = FB_BanquetEntryMaster.objects.get(id = id)
         
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

def FB_BanquetList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = FB_BanquetEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'FB_Banquet/FB_BanquetList.html' ,{'mem' :mem })
                 
def FB_BanquetEntry(request):  
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
        TotalFoodRevenue  = request.POST['TotalFoodRevenue']
        if(TotalFoodRevenue ==''):
            TotalFoodRevenue =0
        TotalBEVERAGEREVENUE = request.POST['TotalBEVERAGEREVENUE']
        if(TotalBEVERAGEREVENUE ==''):
            TotalBEVERAGEREVENUE =0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue ==''):
            BeverageRevenue =0
        HallRental = request.POST['HallRental']
        if(HallRental == ''):
            HallRental =0
        FB_RevenueMisc = request.POST['FB_RevenueMisc']
        if(FB_RevenueMisc ==''):
            FB_RevenueMisc =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome ==''):
            TotalOtherIncome =0
        FB_Revenue = request.POST['FB_Revenue']
        if(FB_Revenue ==''):
            FB_Revenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales ==''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales == ''):
            BeverageCostOfSales =0
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        if(TotalCostOfFBSales ==''):
            TotalCostOfFBSales =0
        AudioVisualEquipmentCostOfSale = request.POST['AudioVisualEquipmentCostOfSale']
        if(AudioVisualEquipmentCostOfSale ==''):
            AudioVisualEquipmentCostOfSale =0
        FB_OtherCostOfSales  = request.POST['FB_OtherCostOfSales']
        if(FB_OtherCostOfSales == ''):
            FB_OtherCostOfSales =0
        TotalCostOf_OtherRev = request.POST['TotalCostOf_OtherRev']       
        if(TotalCostOf_OtherRev ==''):
            TotalCostOf_OtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales ==''):
            TotalCostOfSales =0
        GrossProfit  = request.POST['GrossProfit']
        if(GrossProfit ==''):
            GrossProfit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages ==''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives ==''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
            Salary_Wages_and_Bonuses =0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits == ''):
            EmployeeBenefits =0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses ==''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses == ''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses ==''):
            Total_Other_Expenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome ==''):
            DepartmentIncome =0
      
        enmaster =   FB_BanquetEntryMaster.objects.create(EntryMonth = EntryMonth, EntryYear = EntryYear,
                     FoodRevenue= FoodRevenue, TotalFoodRevenue = TotalFoodRevenue ,  TotalBEVERAGEREVENUE=  TotalBEVERAGEREVENUE,
                      BeverageRevenue=  BeverageRevenue,  HallRental=  HallRental, FB_RevenueMisc= FB_RevenueMisc,
                        TotalOtherIncome= TotalOtherIncome,  FB_Revenue=  FB_Revenue,  FoodCostOfSales=  FoodCostOfSales,
                        BeverageCostOfSales=  BeverageCostOfSales,  TotalCostOfFBSales=  TotalCostOfFBSales,
                         FB_OtherCostOfSales = FB_OtherCostOfSales ,  TotalCostOf_OtherRev=  TotalCostOf_OtherRev,                         
                         AudioVisualEquipmentCostOfSale= AudioVisualEquipmentCostOfSale,  
                        TotalCostOfSales=TotalCostOfSales, GrossProfit=GrossProfit,
                  SalaryAndWages= SalaryAndWages ,  Bonuses_and_Incentives =  Bonuses_and_Incentives ,
               Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,  EmployeeBenefits= EmployeeBenefits,
              PayrollRelatedExpenses= PayrollRelatedExpenses, PayrollAndRelatedExpenses= PayrollAndRelatedExpenses,
              Total_Other_Expenses= Total_Other_Expenses ,  DepartmentIncome =  DepartmentIncome,OrganizationID=OrganizationID,CreatedBy=UserID )        
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = FB_BanquetMaster.objects.get(id = TitleID_)
            EntObj = FB_BanquetEntryMaster.objects.get(id=enmaster.pk)
            
            v =  FB_BanquetEntryDetail.objects.create(Amount = Amount, 
                            FB_BanquetMaster =TitleObj , FB_BanquetEntryMaster = EntObj  )        
        
        return(redirect('/HBudgetReport/FB_BanquetList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = FB_BanquetMaster.objects.filter(IsDelete=False)
    return render(request, 'FB_Banquet/FB_BanquetEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def FB_BanquetDelete(request,id):
    mem =  FB_BanquetEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/FB_BanquetList'))

def FB_BanquetEdit(request,id):   
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        TotalFoodRevenue  = request.POST['TotalFoodRevenue']
        TotalBEVERAGEREVENUE = request.POST['TotalBEVERAGEREVENUE']
        BeverageRevenue = request.POST['BeverageRevenue']
        HallRental = request.POST['HallRental']
        FB_RevenueMisc = request.POST['FB_RevenueMisc']
        TotalOtherIncome = request.POST['TotalOtherIncome']
        FB_Revenue = request.POST['FB_Revenue']
        FoodCostOfSales = request.POST['FoodCostOfSales']
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        AudioVisualEquipmentCostOfSale = request.POST['AudioVisualEquipmentCostOfSale']
        FB_OtherCostOfSales  = request.POST['FB_OtherCostOfSales']
        TotalCostOf_OtherRev = request.POST['TotalCostOf_OtherRev']       
        TotalCostOfSales = request.POST['TotalCostOfSales']
        GrossProfit  = request.POST['GrossProfit']
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        DepartmentIncome = request.POST['DepartmentIncome']
      
        mem =  FB_BanquetEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue  =   FoodRevenue 
        mem.TotalFoodRevenue  =   TotalFoodRevenue 
        mem.TotalBEVERAGEREVENUE =     TotalBEVERAGEREVENUE
        mem.BeverageRevenue =   BeverageRevenue
        mem.HallRental =  HallRental
        mem.FB_RevenueMisc =  FB_RevenueMisc
        mem.TotalOtherIncome =  TotalOtherIncome
        mem.FB_Revenue  =  FB_Revenue
        mem.FoodCostOfSales  =  FoodCostOfSales
        mem.BeverageCostOfSales =   BeverageCostOfSales 
        mem.TotalCostOfFBSales =  TotalCostOfFBSales
        mem.AudioVisualEquipmentCostOfSale =   AudioVisualEquipmentCostOfSale
        mem.FB_OtherCostOfSales =    FB_OtherCostOfSales 
        mem.TotalCostOf_OtherRev  = TotalCostOf_OtherRev 
        mem.TotalCostOfSales =   TotalCostOfSales       
        mem.GrossProfit  =   GrossProfit 
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives  =  Bonuses_and_Incentives 
        mem.Salary_Wages_and_Bonuses =  Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =   EmployeeBenefits 
        mem.PayrollRelatedExpenses  =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses =   PayrollAndRelatedExpenses
        mem.Total_Other_Expenses =  Total_Other_Expenses
        mem.DepartmentIncome  =   DepartmentIncome 
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 =   FB_BanquetEntryMaster.objects.get(id = id)
            sv =  FB_BanquetEntryDetail.objects.get(FB_BanquetMaster = TitleID_ , FB_BanquetEntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
        return(redirect('/HBudgetReport/FB_BanquetList'))
             
    mem1 = FB_BanquetEntryDetail.objects.filter( FB_BanquetEntryMaster=id ,IsDelete = False).select_related("FB_BanquetMaster")
    mem =  FB_BanquetEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'FB_Banquet/FB_BanquetEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})







def FB_IRDviewdata(request, id):
    template_path = "FB_IRD/FB_IRDviewdata.html"
    mem1 = FB_IRDEntryDetail.objects.filter(FB_IRDEntryMaster=id , IsDelete = False).select_related("FB_IRDMaster")
    mem = FB_IRDEntryMaster.objects.get(id = id)
         
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

def FB_IRDList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = FB_IRDEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'FB_IRD/FB_IRDList.html' ,{'mem' :mem })
                                  
def FB_IRDEntry(request):  
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
        if (FoodRevenue == ''):
            FoodRevenue =0
        TotalFoodRevenue  = request.POST['TotalFoodRevenue']
        if(TotalFoodRevenue ==''):
            TotalFoodRevenue =0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalBEVERAGEREVENUE = request.POST['TotalBEVERAGEREVENUE']
        if(TotalBEVERAGEREVENUE == ''):
            TotalBEVERAGEREVENUE =0
        RoomHireRevenue = request.POST['RoomHireRevenue']
        if(RoomHireRevenue ==''):
            RoomHireRevenue =0
        AudioVisualRevenue = request.POST['AudioVisualRevenue']
        if(AudioVisualRevenue == ''):
            AudioVisualRevenue =0
        ServiceChargeRevenue = request.POST['ServiceChargeRevenue']
        if(ServiceChargeRevenue == ''):
            ServiceChargeRevenue =0
        FB_Revenue_Others = request.POST['FB_Revenue_Others']       
        if(FB_Revenue_Others == ''):
            FB_Revenue_Others =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome == ''):
            TotalOtherIncome =0
        FB_Revenue = request.POST['FB_Revenue']
        if(FB_Revenue == ''):
            FB_Revenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales == ''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales == ''):
            BeverageCostOfSales =0
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        if(TotalCostOfFBSales == ''):
            TotalCostOfFBSales =0
        AudioVisualEquipmentCostOfSale = request.POST['AudioVisualEquipmentCostOfSale']
        if(AudioVisualEquipmentCostOfSale == ''):
            AudioVisualEquipmentCostOfSale =0
        FB_OtherCostOfSales  = request.POST['FB_OtherCostOfSales']
        if(FB_OtherCostOfSales == ''):
            FB_OtherCostOfSales =0
        TotalCostOf_OtherRev = request.POST['TotalCostOf_OtherRev']  
        if(TotalCostOf_OtherRev ==''):
            TotalCostOf_OtherRev =0     
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales == ''):
            TotalCostOfSales =0
        GrossProfit  = request.POST['GrossProfit']
        if(GrossProfit == ''):
            GrossProfit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if (SalaryAndWages == ''):
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
        if(PayrollRelatedExpenses ==''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses == ''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses ==''):
            Total_Other_Expenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome == ''):
            DepartmentIncome =0
      
        enmaster =   FB_IRDEntryMaster.objects.create(EntryMonth = EntryMonth, EntryYear = EntryYear,
                     FoodRevenue= FoodRevenue, TotalFoodRevenue = TotalFoodRevenue ,  TotalBEVERAGEREVENUE=  TotalBEVERAGEREVENUE,
                      BeverageRevenue=  BeverageRevenue, RoomHireRevenue=  RoomHireRevenue, 
                        TotalOtherIncome= TotalOtherIncome,  FB_Revenue=  FB_Revenue,  FoodCostOfSales=  FoodCostOfSales,
                        BeverageCostOfSales=  BeverageCostOfSales,  TotalCostOfFBSales=  TotalCostOfFBSales,
                         FB_OtherCostOfSales = FB_OtherCostOfSales ,  TotalCostOf_OtherRev=  TotalCostOf_OtherRev,                         
                         AudioVisualEquipmentCostOfSale= AudioVisualEquipmentCostOfSale,  
                        TotalCostOfSales=TotalCostOfSales, GrossProfit=GrossProfit, AudioVisualRevenue= AudioVisualRevenue,
                  ServiceChargeRevenue=  ServiceChargeRevenue,  FB_Revenue_Others=  FB_Revenue_Others,                         
                  SalaryAndWages= SalaryAndWages ,  Bonuses_and_Incentives =  Bonuses_and_Incentives ,
               Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,  EmployeeBenefits= EmployeeBenefits,
              PayrollRelatedExpenses= PayrollRelatedExpenses, PayrollAndRelatedExpenses= PayrollAndRelatedExpenses,
              Total_Other_Expenses= Total_Other_Expenses ,  DepartmentIncome =  DepartmentIncome,OrganizationID=OrganizationID,CreatedBy=UserID   )        
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = FB_IRDMaster.objects.get(id = TitleID_)
            EntObj = FB_IRDEntryMaster.objects.get(id=enmaster.pk)
            
            v =  FB_IRDEntryDetail.objects.create(Amount = Amount, 
                            FB_IRDMaster =TitleObj , FB_IRDEntryMaster = EntObj  )        
        
        return(redirect('/HBudgetReport/FB_IRDList'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = FB_IRDMaster.objects.filter(IsDelete=False)
    return render(request, 'FB_IRD/FB_IRDEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1) ,'CMonth':CMonth})

def FB_IRDDelete(request,id):
    mem =  FB_IRDEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/FB_IRDList'))

def FB_IRDEdit(request,id):   
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        TotalFoodRevenue  = request.POST['TotalFoodRevenue']
        BeverageRevenue = request.POST['BeverageRevenue']
        TotalBEVERAGEREVENUE = request.POST['TotalBEVERAGEREVENUE']
        RoomHireRevenue = request.POST['RoomHireRevenue']
        AudioVisualRevenue = request.POST['AudioVisualRevenue']
        ServiceChargeRevenue = request.POST['ServiceChargeRevenue']
        FB_Revenue_Others = request.POST['FB_Revenue_Others']        
        TotalOtherIncome = request.POST['TotalOtherIncome']
        FB_Revenue = request.POST['FB_Revenue']
        FoodCostOfSales = request.POST['FoodCostOfSales']
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        AudioVisualEquipmentCostOfSale = request.POST['AudioVisualEquipmentCostOfSale']
        FB_OtherCostOfSales  = request.POST['FB_OtherCostOfSales']
        TotalCostOf_OtherRev = request.POST['TotalCostOf_OtherRev']       
        TotalCostOfSales = request.POST['TotalCostOfSales']
        GrossProfit  = request.POST['GrossProfit']
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        DepartmentIncome = request.POST['DepartmentIncome']
      
        mem =  FB_IRDEntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue  =   FoodRevenue 
        mem.TotalFoodRevenue  =   TotalFoodRevenue 
        mem.TotalBEVERAGEREVENUE =     TotalBEVERAGEREVENUE
        mem.BeverageRevenue =   BeverageRevenue
        mem.RoomHireRevenue =   RoomHireRevenue
        mem.AudioVisualRevenue =    AudioVisualRevenue
        mem.ServiceChargeRevenue =  ServiceChargeRevenue
        mem.FB_Revenue_Others  =  FB_Revenue_Others        
        mem.TotalOtherIncome =  TotalOtherIncome
        mem.FB_Revenue  =  FB_Revenue
        mem.FoodCostOfSales  =  FoodCostOfSales
        mem.BeverageCostOfSales =   BeverageCostOfSales 
        mem.TotalCostOfFBSales =  TotalCostOfFBSales
        mem.AudioVisualEquipmentCostOfSale =   AudioVisualEquipmentCostOfSale
        mem.FB_OtherCostOfSales =    FB_OtherCostOfSales 
        mem.TotalCostOf_OtherRev  = TotalCostOf_OtherRev 
        mem.TotalCostOfSales =   TotalCostOfSales       
        mem.GrossProfit  =   GrossProfit 
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives  =  Bonuses_and_Incentives 
        mem.Salary_Wages_and_Bonuses =  Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =   EmployeeBenefits 
        mem.PayrollRelatedExpenses  =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses =   PayrollAndRelatedExpenses
        mem.Total_Other_Expenses =  Total_Other_Expenses
        mem.DepartmentIncome  =   DepartmentIncome 
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 =   FB_IRDEntryMaster.objects.get(id = id)
            sv =  FB_IRDEntryDetail.objects.get(FB_IRDMaster = TitleID_ , FB_IRDEntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
        return(redirect('/HBudgetReport/FB_IRDList'))
             
    mem1 = FB_IRDEntryDetail.objects.filter( FB_IRDEntryMaster=id ,IsDelete = False).select_related("FB_IRDMaster")
    mem =  FB_IRDEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'FB_IRD/FB_IRDEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})






def Outlet_1viewdata(request, id):
    template_path = "Outlet_1/Outlet_1viewdata.html"
    mem1 = Outlet_1EntryDetail.objects.filter(Outlet_1EntryMaster=id , IsDelete = False).select_related("Outlet_1Master")
    mem = Outlet_1EntryMaster.objects.get(id = id)
         
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

def Outlet_1List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Outlet_1EntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'Outlet_1/Outlet_1List.html' ,{'mem' :mem }) 
                                                                                                   
def Outlet_1Entry(request):  
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
        if (FoodRevenue == ''):
            FoodRevenue =0
        MealPlan = request.POST['FB_Revenue_Others']
        if(MealPlan ==''):
            MealPlan =0
        TotalFoodRevenue  = request.POST['TotalFoodRevenue']
        if(TotalFoodRevenue ==''):
            TotalFoodRevenue =0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalBEVERAGEREVENUE = request.POST['TotalBEVERAGEREVENUE']
        if(TotalBEVERAGEREVENUE == ''):
            TotalBEVERAGEREVENUE =0
        AudioVisualRevenue = request.POST['AudioVisualRevenue']
        if(AudioVisualRevenue == ''):
            AudioVisualRevenue =0
        FB_Revenue_Others = request.POST['FB_Revenue_Others']        
        if(FB_Revenue_Others == ''):
            FB_Revenue_Others =0
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome ==''):
            TotalOtherIncome =0
        FB_Revenue = request.POST['FB_Revenue']
        if(FB_Revenue ==''):
            FB_Revenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales ==''):
            FoodCostOfSales = 0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        if(TotalCostOfFBSales == ''):
            TotalCostOfFBSales =0
        AudioVisualEquipmentCostOfSale = request.POST['AudioVisualEquipmentCostOfSale']
        if(AudioVisualEquipmentCostOfSale ==''):
            AudioVisualEquipmentCostOfSale =0
        FB_OtherCostOfSales  = request.POST['FB_OtherCostOfSales']
        if(FB_OtherCostOfSales == ''):
            FB_OtherCostOfSales =0
        TotalCostOf_OtherRev = request.POST['TotalCostOf_OtherRev']      
        if(TotalCostOf_OtherRev ==''):
            TotalCostOf_OtherRev =0 
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales ==''):
            TotalCostOfSales =0
        GrossProfit  = request.POST['GrossProfit']
        if(GrossProfit == ''):
            GrossProfit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages == ''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives ==''):
            Bonuses_and_Incentives =0
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
        if(PayrollAndRelatedExpenses ==''):
            PayrollAndRelatedExpenses =0
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome ==''):
            DepartmentIncome =0
        
            
        enmaster =   Outlet_1EntryMaster.objects.create(EntryMonth = EntryMonth, EntryYear = EntryYear,
                     FoodRevenue= FoodRevenue, TotalFoodRevenue = TotalFoodRevenue ,  TotalBEVERAGEREVENUE=  TotalBEVERAGEREVENUE,
                      BeverageRevenue=  BeverageRevenue,  MealPlan= MealPlan,  TotalOtherIncome= TotalOtherIncome,
                          FB_Revenue=  FB_Revenue,  FoodCostOfSales=  FoodCostOfSales, FB_Revenue_Others= FB_Revenue_Others,
                        BeverageCostOfSales=  BeverageCostOfSales,  TotalCostOfFBSales=  TotalCostOfFBSales,
                         FB_OtherCostOfSales = FB_OtherCostOfSales ,  TotalCostOf_OtherRev=  TotalCostOf_OtherRev,                         
                         AudioVisualEquipmentCostOfSale= AudioVisualEquipmentCostOfSale,  
                        TotalCostOfSales=TotalCostOfSales, GrossProfit=GrossProfit, AudioVisualRevenue= AudioVisualRevenue,                       
                  SalaryAndWages= SalaryAndWages ,  Bonuses_and_Incentives =  Bonuses_and_Incentives ,
               Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,  EmployeeBenefits= EmployeeBenefits,
              PayrollRelatedExpenses= PayrollRelatedExpenses, PayrollAndRelatedExpenses= PayrollAndRelatedExpenses,
              Total_Other_Expenses= Total_Other_Expenses ,  DepartmentIncome =  DepartmentIncome,OrganizationID=OrganizationID,CreatedBy=UserID  )        
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = Outlet_1Master.objects.get(id = TitleID_)
            EntObj = Outlet_1EntryMaster.objects.get(id=enmaster.pk)
            
            v =  Outlet_1EntryDetail.objects.create(Amount = Amount, 
                            Outlet_1Master =TitleObj , Outlet_1EntryMaster = EntObj  )        
        
        return(redirect('/HBudgetReport/Outlet_1List'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = Outlet_1Master.objects.filter(IsDelete=False)
    return render(request, 'Outlet_1/Outlet_1Entry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})

def Outlet_1Delete(request,id):
    mem =  Outlet_1EntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/Outlet_1List'))


def Outlet_1Edit(request,id):   
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        MealPlan = request.POST['FB_Revenue_Others']
        TotalFoodRevenue  = request.POST['TotalFoodRevenue']
        BeverageRevenue = request.POST['BeverageRevenue']
        TotalBEVERAGEREVENUE = request.POST['TotalBEVERAGEREVENUE']
        AudioVisualRevenue = request.POST['AudioVisualRevenue']
        FB_Revenue_Others = request.POST['FB_Revenue_Others']        
        TotalOtherIncome = request.POST['TotalOtherIncome']
        FB_Revenue = request.POST['FB_Revenue']
        FoodCostOfSales = request.POST['FoodCostOfSales']
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        AudioVisualEquipmentCostOfSale = request.POST['AudioVisualEquipmentCostOfSale']
        FB_OtherCostOfSales  = request.POST['FB_OtherCostOfSales']
        TotalCostOf_OtherRev = request.POST['TotalCostOf_OtherRev']       
        TotalCostOfSales = request.POST['TotalCostOfSales']
        GrossProfit  = request.POST['GrossProfit']
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        DepartmentIncome = request.POST['DepartmentIncome']
      
      
        mem =  Outlet_1EntryMaster.objects.get(id = id)
       
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue  =   FoodRevenue 
        mem.MealPlan =   MealPlan
        mem.TotalFoodRevenue  =   TotalFoodRevenue 
        mem.TotalBEVERAGEREVENUE =     TotalBEVERAGEREVENUE
        mem.BeverageRevenue =   BeverageRevenue       
        mem.AudioVisualRevenue =    AudioVisualRevenue        
        mem.FB_Revenue_Others  =  FB_Revenue_Others        
        mem.TotalOtherIncome =  TotalOtherIncome
        mem.FB_Revenue  =  FB_Revenue
        mem.FoodCostOfSales  =  FoodCostOfSales
        mem.BeverageCostOfSales =   BeverageCostOfSales 
        mem.TotalCostOfFBSales =  TotalCostOfFBSales
        mem.AudioVisualEquipmentCostOfSale =   AudioVisualEquipmentCostOfSale
        mem.FB_OtherCostOfSales =    FB_OtherCostOfSales 
        mem.TotalCostOf_OtherRev  = TotalCostOf_OtherRev 
        mem.TotalCostOfSales =   TotalCostOfSales       
        mem.GrossProfit  =   GrossProfit 
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives  =  Bonuses_and_Incentives 
        mem.Salary_Wages_and_Bonuses =  Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =   EmployeeBenefits 
        mem.PayrollRelatedExpenses  =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses =   PayrollAndRelatedExpenses
        mem.Total_Other_Expenses =  Total_Other_Expenses
        mem.DepartmentIncome  =   DepartmentIncome 
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 =   Outlet_1EntryMaster.objects.get(id = id)
            sv =  Outlet_1EntryDetail.objects.get(Outlet_1Master = TitleID_ , Outlet_1EntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
        return(redirect('/HBudgetReport/Outlet_1List'))
             
    mem1 = Outlet_1EntryDetail.objects.filter( Outlet_1EntryMaster=id ,IsDelete = False).select_related("Outlet_1Master")
    mem =  Outlet_1EntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'Outlet_1/Outlet_1Edit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})







def Outlet_2viewdata(request, id):
    template_path = "Outlet_2/Outlet_2viewdata.html"
    mem1 = Outlet_2EntryDetail.objects.filter(Outlet_2EntryMaster=id , IsDelete = False).select_related("Outlet_2Master")
    mem = Outlet_2EntryMaster.objects.get(id = id)
         
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

def Outlet_2List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Outlet_2EntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'Outlet_2/Outlet_2List.html' ,{'mem' :mem }) 
                                                                                             
def Outlet_2Entry(request):  
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
        if (FoodRevenue == ''):
            FoodRevenue =0
        TotalFoodRevenue  = request.POST['TotalFoodRevenue']
        if(TotalFoodRevenue == ''):
            TotalFoodRevenue = 0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalBEVERAGEREVENUE = request.POST['TotalBEVERAGEREVENUE']
        if(TotalBEVERAGEREVENUE == ''):
            TotalBEVERAGEREVENUE =0
        RoomHireRevenue = request.POST['RoomHireRevenue']
        if (RoomHireRevenue ==''):
            RoomHireRevenue =0
        AudioVisualRevenue = request.POST['AudioVisualRevenue']
        if(AudioVisualRevenue == ''):
            AudioVisualRevenue =0
        ServiceChargeRevenue = request.POST['ServiceChargeRevenue']
        if(ServiceChargeRevenue ==''):
            ServiceChargeRevenue =0
        FB_Revenue_Others = request.POST['FB_Revenue_Others']      
        if(FB_Revenue_Others == ''):
            FB_Revenue_Others =0  
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome ==''):
            TotalOtherIncome =0
        FB_Revenue = request.POST['FB_Revenue']
        if(FB_Revenue ==''):
            FB_Revenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales ==''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        if(TotalCostOfFBSales == ''):TotalCostOfFBSales =0
        AudioVisualEquipmentCostOfSale = request.POST['AudioVisualEquipmentCostOfSale']
        if(AudioVisualEquipmentCostOfSale ==''):
            AudioVisualEquipmentCostOfSale =0
        FB_OtherCostOfSales  = request.POST['FB_OtherCostOfSales']
        if(FB_OtherCostOfSales == ''):
            FB_OtherCostOfSales =0
        TotalCostOf_OtherRev = request.POST['TotalCostOf_OtherRev']       
        if(TotalCostOf_OtherRev ==''):
            TotalCostOf_OtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales ==''):
            TotalCostOfSales =0
        GrossProfit  = request.POST['GrossProfit']
        if(GrossProfit ==''):
            GrossProfit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages ==''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
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
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses = 0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome ==''):
            DepartmentIncome = 0
      
        enmaster =   Outlet_2EntryMaster.objects.create(EntryMonth = EntryMonth, EntryYear = EntryYear,
                     FoodRevenue= FoodRevenue, TotalFoodRevenue = TotalFoodRevenue ,  TotalBEVERAGEREVENUE=  TotalBEVERAGEREVENUE,
                      BeverageRevenue=  BeverageRevenue, RoomHireRevenue=  RoomHireRevenue, 
                        TotalOtherIncome= TotalOtherIncome,  FB_Revenue=  FB_Revenue,  FoodCostOfSales=  FoodCostOfSales,
                        BeverageCostOfSales=  BeverageCostOfSales,  TotalCostOfFBSales=  TotalCostOfFBSales,
                         FB_OtherCostOfSales = FB_OtherCostOfSales ,  TotalCostOf_OtherRev=  TotalCostOf_OtherRev,                         
                         AudioVisualEquipmentCostOfSale= AudioVisualEquipmentCostOfSale,  
                        TotalCostOfSales=TotalCostOfSales, GrossProfit=GrossProfit, AudioVisualRevenue= AudioVisualRevenue,
                  ServiceChargeRevenue=  ServiceChargeRevenue,  FB_Revenue_Others=  FB_Revenue_Others,                         
                  SalaryAndWages= SalaryAndWages ,  Bonuses_and_Incentives =  Bonuses_and_Incentives ,
               Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,  EmployeeBenefits= EmployeeBenefits,
              PayrollRelatedExpenses= PayrollRelatedExpenses, PayrollAndRelatedExpenses= PayrollAndRelatedExpenses,
              Total_Other_Expenses= Total_Other_Expenses ,  DepartmentIncome =  DepartmentIncome,OrganizationID=OrganizationID,CreatedBy=UserID )        
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = Outlet_2Master.objects.get(id = TitleID_)
            EntObj = Outlet_2EntryMaster.objects.get(id=enmaster.pk)
            
            v =  Outlet_2EntryDetail.objects.create(Amount = Amount, 
                            Outlet_2Master =TitleObj , Outlet_2EntryMaster = EntObj  )        
        
        return(redirect('/HBudgetReport/Outlet_2List'))
    today = datetime.date.today()
    CYear = today.year
    CMonth= today.month
    mem = Outlet_2Master.objects.filter(IsDelete=False)
    return render(request, 'Outlet_2/Outlet_2Entry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})                                                                  
                                                                   

def Outlet_2Delete(request,id):
    mem =  Outlet_2EntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/Outlet_2List'))

def Outlet_2Edit(request,id):   
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        TotalFoodRevenue  = request.POST['TotalFoodRevenue']
        BeverageRevenue = request.POST['BeverageRevenue']
        TotalBEVERAGEREVENUE = request.POST['TotalBEVERAGEREVENUE']
        RoomHireRevenue = request.POST['RoomHireRevenue']
        AudioVisualRevenue = request.POST['AudioVisualRevenue']
        ServiceChargeRevenue = request.POST['ServiceChargeRevenue']
        FB_Revenue_Others = request.POST['FB_Revenue_Others']        
        TotalOtherIncome = request.POST['TotalOtherIncome']
        FB_Revenue = request.POST['FB_Revenue']
        FoodCostOfSales = request.POST['FoodCostOfSales']
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        AudioVisualEquipmentCostOfSale = request.POST['AudioVisualEquipmentCostOfSale']
        FB_OtherCostOfSales  = request.POST['FB_OtherCostOfSales']
        TotalCostOf_OtherRev = request.POST['TotalCostOf_OtherRev']       
        TotalCostOfSales = request.POST['TotalCostOfSales']
        GrossProfit  = request.POST['GrossProfit']
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        DepartmentIncome = request.POST['DepartmentIncome']
      
        mem =  Outlet_2EntryMaster.objects.get(id = id)
        
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue  =   FoodRevenue 
        mem.TotalFoodRevenue  =   TotalFoodRevenue 
        mem.TotalBEVERAGEREVENUE =     TotalBEVERAGEREVENUE
        mem.BeverageRevenue =   BeverageRevenue
        mem.RoomHireRevenue =   RoomHireRevenue
        mem.AudioVisualRevenue =    AudioVisualRevenue
        mem.ServiceChargeRevenue =  ServiceChargeRevenue
        mem.FB_Revenue_Others  =  FB_Revenue_Others        
        mem.TotalOtherIncome =  TotalOtherIncome
        mem.FB_Revenue  =  FB_Revenue
        mem.FoodCostOfSales  =  FoodCostOfSales
        mem.BeverageCostOfSales =   BeverageCostOfSales 
        mem.TotalCostOfFBSales =  TotalCostOfFBSales
        mem.AudioVisualEquipmentCostOfSale =   AudioVisualEquipmentCostOfSale
        mem.FB_OtherCostOfSales =    FB_OtherCostOfSales 
        mem.TotalCostOf_OtherRev  = TotalCostOf_OtherRev 
        mem.TotalCostOfSales =   TotalCostOfSales       
        mem.GrossProfit  =   GrossProfit 
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives  =  Bonuses_and_Incentives 
        mem.Salary_Wages_and_Bonuses =  Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =   EmployeeBenefits 
        mem.PayrollRelatedExpenses  =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses =   PayrollAndRelatedExpenses
        mem.Total_Other_Expenses =  Total_Other_Expenses
        mem.DepartmentIncome  =   DepartmentIncome 
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 =   Outlet_2EntryMaster.objects.get(id = id)
            sv =  Outlet_2EntryDetail.objects.get(Outlet_2Master = TitleID_ , Outlet_2EntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
        return(redirect('/HBudgetReport/Outlet_2List'))
             
    mem1 = Outlet_2EntryDetail.objects.filter( Outlet_2EntryMaster=id ,IsDelete = False).select_related("Outlet_2Master")
    mem = Outlet_2EntryMaster.objects.get(id = id)
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'Outlet_2/Outlet_2Edit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})

                                                                
                                                                   
                                                                   
                                                                                                                      


def Outlet_3viewdata(request, id):
    template_path = "Outlet_3/Outlet_3viewdata.html"
    mem1 = Outlet_3EntryDetail.objects.filter(Outlet_3EntryMaster=id , IsDelete = False).select_related("Outlet_3Master")
    mem = Outlet_3EntryMaster.objects.get(id = id)
         
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

def Outlet_3List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Outlet_3EntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'Outlet_3/Outlet_3List.html' ,{'mem' :mem }) 
                                                                                             
def Outlet_3Entry(request):  
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
        if (FoodRevenue == ''):
            FoodRevenue =0
        TotalFoodRevenue  = request.POST['TotalFoodRevenue']
        if(TotalFoodRevenue == ''):
            TotalFoodRevenue = 0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalBEVERAGEREVENUE = request.POST['TotalBEVERAGEREVENUE']
        if(TotalBEVERAGEREVENUE == ''):
            TotalBEVERAGEREVENUE =0
        RoomHireRevenue = request.POST['RoomHireRevenue']
        if (RoomHireRevenue ==''):
            RoomHireRevenue =0
        AudioVisualRevenue = request.POST['AudioVisualRevenue']
        if(AudioVisualRevenue == ''):
            AudioVisualRevenue =0
        ServiceChargeRevenue = request.POST['ServiceChargeRevenue']
        if(ServiceChargeRevenue ==''):
            ServiceChargeRevenue =0
        FB_Revenue_Others = request.POST['FB_Revenue_Others']      
        if(FB_Revenue_Others == ''):
            FB_Revenue_Others =0  
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome ==''):
            TotalOtherIncome =0
        FB_Revenue = request.POST['FB_Revenue']
        if(FB_Revenue ==''):
            FB_Revenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales ==''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        if(TotalCostOfFBSales == ''):TotalCostOfFBSales =0
        AudioVisualEquipmentCostOfSale = request.POST['AudioVisualEquipmentCostOfSale']
        if(AudioVisualEquipmentCostOfSale ==''):
            AudioVisualEquipmentCostOfSale =0
        FB_OtherCostOfSales  = request.POST['FB_OtherCostOfSales']
        if(FB_OtherCostOfSales == ''):
            FB_OtherCostOfSales =0
        TotalCostOf_OtherRev = request.POST['TotalCostOf_OtherRev']       
        if(TotalCostOf_OtherRev ==''):
            TotalCostOf_OtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales ==''):
            TotalCostOfSales =0
        GrossProfit  = request.POST['GrossProfit']
        if(GrossProfit ==''):
            GrossProfit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages ==''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
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
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses = 0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome ==''):
            DepartmentIncome = 0
      
        enmaster =   Outlet_3EntryMaster.objects.create(EntryMonth = EntryMonth, EntryYear = EntryYear,
                     FoodRevenue= FoodRevenue, TotalFoodRevenue = TotalFoodRevenue ,  TotalBEVERAGEREVENUE=  TotalBEVERAGEREVENUE,
                      BeverageRevenue=  BeverageRevenue, RoomHireRevenue=  RoomHireRevenue, 
                        TotalOtherIncome= TotalOtherIncome,  FB_Revenue=  FB_Revenue,  FoodCostOfSales=  FoodCostOfSales,
                        BeverageCostOfSales=  BeverageCostOfSales,  TotalCostOfFBSales=  TotalCostOfFBSales,
                         FB_OtherCostOfSales = FB_OtherCostOfSales ,  TotalCostOf_OtherRev=  TotalCostOf_OtherRev,                         
                         AudioVisualEquipmentCostOfSale= AudioVisualEquipmentCostOfSale,  
                        TotalCostOfSales=TotalCostOfSales, GrossProfit=GrossProfit, AudioVisualRevenue= AudioVisualRevenue,
                  ServiceChargeRevenue=  ServiceChargeRevenue,  FB_Revenue_Others=  FB_Revenue_Others,                         
                  SalaryAndWages= SalaryAndWages ,  Bonuses_and_Incentives =  Bonuses_and_Incentives ,
               Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,  EmployeeBenefits= EmployeeBenefits,
              PayrollRelatedExpenses= PayrollRelatedExpenses, PayrollAndRelatedExpenses= PayrollAndRelatedExpenses,
              Total_Other_Expenses= Total_Other_Expenses ,  DepartmentIncome =  DepartmentIncome,OrganizationID=OrganizationID,CreatedBy=UserID )        
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = Outlet_3Master.objects.get(id = TitleID_)
            EntObj = Outlet_3EntryMaster.objects.get(id=enmaster.pk)
            
            v =  Outlet_3EntryDetail.objects.create(Amount = Amount, 
                            Outlet_3Master =TitleObj , Outlet_3EntryMaster = EntObj  )        
        
        return(redirect('/HBudgetReport/Outlet_3List'))
    today = datetime.date.today()
    CYear = today.year
    CMonth= today.month
    mem = Outlet_3Master.objects.filter(IsDelete=False)
    return render(request, 'Outlet_3/Outlet_3Entry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})                                                                  
                                                                                                            
def Outlet_3Delete(request,id):
    mem =  Outlet_3EntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/Outlet_3List'))


def Outlet_3Edit(request,id):   
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        MealPlan = request.POST['FB_Revenue_Others']
        TotalFoodRevenue  = request.POST['TotalFoodRevenue']
        BeverageRevenue = request.POST['BeverageRevenue']
        TotalBEVERAGEREVENUE = request.POST['TotalBEVERAGEREVENUE']
        AudioVisualRevenue = request.POST['AudioVisualRevenue']
        FB_Revenue_Others = request.POST['FB_Revenue_Others']        
        TotalOtherIncome = request.POST['TotalOtherIncome']
        FB_Revenue = request.POST['FB_Revenue']
        FoodCostOfSales = request.POST['FoodCostOfSales']
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        AudioVisualEquipmentCostOfSale = request.POST['AudioVisualEquipmentCostOfSale']
        FB_OtherCostOfSales  = request.POST['FB_OtherCostOfSales']
        TotalCostOf_OtherRev = request.POST['TotalCostOf_OtherRev']       
        TotalCostOfSales = request.POST['TotalCostOfSales']
        GrossProfit  = request.POST['GrossProfit']
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        DepartmentIncome = request.POST['DepartmentIncome']
      
      
        mem =  Outlet_3EntryMaster.objects.get(id = id)
       
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue  =   FoodRevenue 
        mem.MealPlan =   MealPlan
        mem.TotalFoodRevenue  =   TotalFoodRevenue 
        mem.TotalBEVERAGEREVENUE =     TotalBEVERAGEREVENUE
        mem.BeverageRevenue =   BeverageRevenue       
        mem.AudioVisualRevenue =    AudioVisualRevenue        
        mem.FB_Revenue_Others  =  FB_Revenue_Others        
        mem.TotalOtherIncome =  TotalOtherIncome
        mem.FB_Revenue  =  FB_Revenue
        mem.FoodCostOfSales  =  FoodCostOfSales
        mem.BeverageCostOfSales =   BeverageCostOfSales 
        mem.TotalCostOfFBSales =  TotalCostOfFBSales
        mem.AudioVisualEquipmentCostOfSale =   AudioVisualEquipmentCostOfSale
        mem.FB_OtherCostOfSales =    FB_OtherCostOfSales 
        mem.TotalCostOf_OtherRev  = TotalCostOf_OtherRev 
        mem.TotalCostOfSales =   TotalCostOfSales       
        mem.GrossProfit  =   GrossProfit 
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives  =  Bonuses_and_Incentives 
        mem.Salary_Wages_and_Bonuses =  Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =   EmployeeBenefits 
        mem.PayrollRelatedExpenses  =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses =   PayrollAndRelatedExpenses
        mem.Total_Other_Expenses =  Total_Other_Expenses
        mem.DepartmentIncome  =   DepartmentIncome 
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 =   Outlet_3EntryMaster.objects.get(id = id)
            sv =  Outlet_3EntryDetail.objects.get(Outlet_3Master = TitleID_ , Outlet_3EntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
        return(redirect('/HBudgetReport/Outlet_3List'))
             
    mem1 = Outlet_3EntryDetail.objects.filter( Outlet_3EntryMaster=id ,IsDelete = False).select_related("Outlet_3Master")
    mem =  Outlet_3EntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'Outlet_3/Outlet_3Edit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})






def Outlet_4viewdata(request, id):
    template_path = "Outlet_4/Outlet_4viewdata.html"
    mem1 = Outlet_4EntryDetail.objects.filter(Outlet_4EntryMaster=id , IsDelete = False).select_related("Outlet_4Master")
    mem = Outlet_4EntryMaster.objects.get(id = id)
         
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
                                                                                                                    

def Outlet_4List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Outlet_4EntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )    
    return render(request, 'Outlet_4/Outlet_4List.html' ,{'mem' :mem }) 
   
                                                                                          
def Outlet_4Entry(request):  
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
        if (FoodRevenue == ''):
            FoodRevenue =0
        TotalFoodRevenue  = request.POST['TotalFoodRevenue']
        if(TotalFoodRevenue == ''):
            TotalFoodRevenue = 0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalBEVERAGEREVENUE = request.POST['TotalBEVERAGEREVENUE']
        if(TotalBEVERAGEREVENUE == ''):
            TotalBEVERAGEREVENUE =0
        RoomHireRevenue = request.POST['RoomHireRevenue']
        if (RoomHireRevenue ==''):
            RoomHireRevenue =0
        AudioVisualRevenue = request.POST['AudioVisualRevenue']
        if(AudioVisualRevenue == ''):
            AudioVisualRevenue =0
        ServiceChargeRevenue = request.POST['ServiceChargeRevenue']
        if(ServiceChargeRevenue ==''):
            ServiceChargeRevenue =0
        FB_Revenue_Others = request.POST['FB_Revenue_Others']      
        if(FB_Revenue_Others == ''):
            FB_Revenue_Others =0  
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome ==''):
            TotalOtherIncome =0
        FB_Revenue = request.POST['FB_Revenue']
        if(FB_Revenue ==''):
            FB_Revenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales ==''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        if(TotalCostOfFBSales == ''):TotalCostOfFBSales =0
        AudioVisualEquipmentCostOfSale = request.POST['AudioVisualEquipmentCostOfSale']
        if(AudioVisualEquipmentCostOfSale ==''):
            AudioVisualEquipmentCostOfSale =0
        FB_OtherCostOfSales  = request.POST['FB_OtherCostOfSales']
        if(FB_OtherCostOfSales == ''):
            FB_OtherCostOfSales =0
        TotalCostOf_OtherRev = request.POST['TotalCostOf_OtherRev']       
        if(TotalCostOf_OtherRev ==''):
            TotalCostOf_OtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales ==''):
            TotalCostOfSales =0
        GrossProfit  = request.POST['GrossProfit']
        if(GrossProfit ==''):
            GrossProfit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages ==''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
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
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses = 0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome ==''):
            DepartmentIncome = 0
      
        enmaster =   Outlet_4EntryMaster.objects.create(EntryMonth = EntryMonth, EntryYear = EntryYear,
                     FoodRevenue= FoodRevenue, TotalFoodRevenue = TotalFoodRevenue ,  TotalBEVERAGEREVENUE=  TotalBEVERAGEREVENUE,
                      BeverageRevenue=  BeverageRevenue, RoomHireRevenue=  RoomHireRevenue, 
                        TotalOtherIncome= TotalOtherIncome,  FB_Revenue=  FB_Revenue,  FoodCostOfSales=  FoodCostOfSales,
                        BeverageCostOfSales=  BeverageCostOfSales,  TotalCostOfFBSales=  TotalCostOfFBSales,
                         FB_OtherCostOfSales = FB_OtherCostOfSales ,  TotalCostOf_OtherRev=  TotalCostOf_OtherRev,                         
                         AudioVisualEquipmentCostOfSale= AudioVisualEquipmentCostOfSale,  
                        TotalCostOfSales=TotalCostOfSales, GrossProfit=GrossProfit, AudioVisualRevenue= AudioVisualRevenue,
                  ServiceChargeRevenue=  ServiceChargeRevenue,  FB_Revenue_Others=  FB_Revenue_Others,                         
                  SalaryAndWages= SalaryAndWages ,  Bonuses_and_Incentives =  Bonuses_and_Incentives ,
               Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,  EmployeeBenefits= EmployeeBenefits,
              PayrollRelatedExpenses= PayrollRelatedExpenses, PayrollAndRelatedExpenses= PayrollAndRelatedExpenses,
              Total_Other_Expenses= Total_Other_Expenses ,  DepartmentIncome =  DepartmentIncome,OrganizationID=OrganizationID,CreatedBy=UserID )        
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = Outlet_4Master.objects.get(id = TitleID_)
            EntObj = Outlet_4EntryMaster.objects.get(id=enmaster.pk)
            
            v = Outlet_4EntryDetail.objects.create(Amount = Amount ,
                                    Outlet_4Master = TitleObj , Outlet_4EntryMaster = EntObj)
                                    
        return(redirect('/HBudgetReport/Outlet_4List'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = Outlet_4Master.objects.filter(IsDelete=False)
    return render(request, 'Outlet_4/Outlet_4Entry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMonth':CMonth})                                                                  
                                                                                                                                                                                                              
def Outlet_4Delete(request,id):
    mem =  Outlet_4EntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/Outlet_4List'))

def Outlet_4Edit(request,id):   
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        MealPlan = request.POST['FB_Revenue_Others']
        TotalFoodRevenue  = request.POST['TotalFoodRevenue']
        BeverageRevenue = request.POST['BeverageRevenue']
        TotalBEVERAGEREVENUE = request.POST['TotalBEVERAGEREVENUE']
        AudioVisualRevenue = request.POST['AudioVisualRevenue']
        FB_Revenue_Others = request.POST['FB_Revenue_Others']        
        TotalOtherIncome = request.POST['TotalOtherIncome']
        FB_Revenue = request.POST['FB_Revenue']
        FoodCostOfSales = request.POST['FoodCostOfSales']
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        AudioVisualEquipmentCostOfSale = request.POST['AudioVisualEquipmentCostOfSale']
        FB_OtherCostOfSales  = request.POST['FB_OtherCostOfSales']
        TotalCostOf_OtherRev = request.POST['TotalCostOf_OtherRev']       
        TotalCostOfSales = request.POST['TotalCostOfSales']
        GrossProfit  = request.POST['GrossProfit']
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        DepartmentIncome = request.POST['DepartmentIncome']
      
      
        mem =  Outlet_4EntryMaster.objects.get(id = id)
       
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue  =   FoodRevenue 
        mem.MealPlan =   MealPlan
        mem.TotalFoodRevenue  =   TotalFoodRevenue 
        mem.TotalBEVERAGEREVENUE =     TotalBEVERAGEREVENUE
        mem.BeverageRevenue =   BeverageRevenue       
        mem.AudioVisualRevenue =    AudioVisualRevenue        
        mem.FB_Revenue_Others  =  FB_Revenue_Others        
        mem.TotalOtherIncome =  TotalOtherIncome
        mem.FB_Revenue  =  FB_Revenue
        mem.FoodCostOfSales  =  FoodCostOfSales
        mem.BeverageCostOfSales =   BeverageCostOfSales 
        mem.TotalCostOfFBSales =  TotalCostOfFBSales
        mem.AudioVisualEquipmentCostOfSale =   AudioVisualEquipmentCostOfSale
        mem.FB_OtherCostOfSales =    FB_OtherCostOfSales 
        mem.TotalCostOf_OtherRev  = TotalCostOf_OtherRev 
        mem.TotalCostOfSales =   TotalCostOfSales       
        mem.GrossProfit  =   GrossProfit 
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives  =  Bonuses_and_Incentives 
        mem.Salary_Wages_and_Bonuses =  Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =   EmployeeBenefits 
        mem.PayrollRelatedExpenses  =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses =   PayrollAndRelatedExpenses
        mem.Total_Other_Expenses =  Total_Other_Expenses
        mem.DepartmentIncome  =   DepartmentIncome 
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 =   Outlet_4EntryMaster.objects.get(id = id)
            sv =  Outlet_4EntryDetail.objects.get(Outlet_4Master = TitleID_ , Outlet_4EntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
        return(redirect('/HBudgetReport/Outlet_4List'))
             
    mem1 = Outlet_4EntryDetail.objects.filter( Outlet_4EntryMaster=id ,IsDelete = False).select_related("Outlet_4Master")
    mem =  Outlet_4EntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'Outlet_4/Outlet_4Edit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})






def Outlet_5viewdata(request, id):
    template_path = "Outlet_5/Outlet_5viewdata.html"
    mem1 = Outlet_5EntryDetail.objects.filter(Outlet_5EntryMaster=id , IsDelete = False).select_related("Outlet_5Master")
    mem = Outlet_5EntryMaster.objects.get(id = id)
         
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
                                                                                                                                                                                       

def Outlet_5List(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Outlet_5EntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )
    return render(request, 'Outlet_5/Outlet_5List.html' ,{'mem' :mem }) 
                                                                                                                                                               
def Outlet_5Entry(request):  
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
        if (FoodRevenue == ''):
            FoodRevenue =0
        TotalFoodRevenue  = request.POST['TotalFoodRevenue']
        if(TotalFoodRevenue == ''):
            TotalFoodRevenue = 0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue == ''):
            BeverageRevenue =0
        TotalBEVERAGEREVENUE = request.POST['TotalBEVERAGEREVENUE']
        if(TotalBEVERAGEREVENUE == ''):
            TotalBEVERAGEREVENUE =0
        RoomHireRevenue = request.POST['RoomHireRevenue']
        if (RoomHireRevenue ==''):
            RoomHireRevenue =0
        AudioVisualRevenue = request.POST['AudioVisualRevenue']
        if(AudioVisualRevenue == ''):
            AudioVisualRevenue =0
        ServiceChargeRevenue = request.POST['ServiceChargeRevenue']
        if(ServiceChargeRevenue ==''):
            ServiceChargeRevenue =0
        FB_Revenue_Others = request.POST['FB_Revenue_Others']      
        if(FB_Revenue_Others == ''):
            FB_Revenue_Others =0  
        TotalOtherIncome = request.POST['TotalOtherIncome']
        if(TotalOtherIncome ==''):
            TotalOtherIncome =0
        FB_Revenue = request.POST['FB_Revenue']
        if(FB_Revenue ==''):
            FB_Revenue =0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales ==''):
            FoodCostOfSales =0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales ==''):
            BeverageCostOfSales =0
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        if(TotalCostOfFBSales == ''):TotalCostOfFBSales =0
        AudioVisualEquipmentCostOfSale = request.POST['AudioVisualEquipmentCostOfSale']
        if(AudioVisualEquipmentCostOfSale ==''):
            AudioVisualEquipmentCostOfSale =0
        FB_OtherCostOfSales  = request.POST['FB_OtherCostOfSales']
        if(FB_OtherCostOfSales == ''):
            FB_OtherCostOfSales =0
        TotalCostOf_OtherRev = request.POST['TotalCostOf_OtherRev']       
        if(TotalCostOf_OtherRev ==''):
            TotalCostOf_OtherRev =0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales ==''):
            TotalCostOfSales =0
        GrossProfit  = request.POST['GrossProfit']
        if(GrossProfit ==''):
            GrossProfit =0
        SalaryAndWages = request.POST['SalaryAndWages']
        if(SalaryAndWages ==''):
            SalaryAndWages =0
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        if(Bonuses_and_Incentives == ''):
            Bonuses_and_Incentives =0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses == ''):
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
        if(Total_Other_Expenses == ''):
            Total_Other_Expenses = 0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome ==''):
            DepartmentIncome = 0
      
        enmaster =   Outlet_5EntryMaster.objects.create(EntryMonth = EntryMonth, EntryYear = EntryYear,
                     FoodRevenue= FoodRevenue, TotalFoodRevenue = TotalFoodRevenue ,  TotalBEVERAGEREVENUE=  TotalBEVERAGEREVENUE,
                      BeverageRevenue=  BeverageRevenue, RoomHireRevenue=  RoomHireRevenue, 
                        TotalOtherIncome= TotalOtherIncome,  FB_Revenue=  FB_Revenue,  FoodCostOfSales=  FoodCostOfSales,
                        BeverageCostOfSales=  BeverageCostOfSales,  TotalCostOfFBSales=  TotalCostOfFBSales,
                         FB_OtherCostOfSales = FB_OtherCostOfSales ,  TotalCostOf_OtherRev=  TotalCostOf_OtherRev,                         
                         AudioVisualEquipmentCostOfSale= AudioVisualEquipmentCostOfSale,  
                        TotalCostOfSales=TotalCostOfSales, GrossProfit=GrossProfit, AudioVisualRevenue= AudioVisualRevenue,
                  ServiceChargeRevenue=  ServiceChargeRevenue,  FB_Revenue_Others=  FB_Revenue_Others,                         
                  SalaryAndWages= SalaryAndWages ,  Bonuses_and_Incentives =  Bonuses_and_Incentives ,
               Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,  EmployeeBenefits= EmployeeBenefits,
              PayrollRelatedExpenses= PayrollRelatedExpenses, PayrollAndRelatedExpenses= PayrollAndRelatedExpenses,
              Total_Other_Expenses= Total_Other_Expenses ,  DepartmentIncome = DepartmentIncome   ,OrganizationID=OrganizationID,CreatedBy=UserID )        
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = Outlet_5Master.objects.get(id = TitleID_)
            EntObj = Outlet_5EntryMaster.objects.get(id=enmaster.pk)
            
            v = Outlet_5EntryDetail.objects.create(Amount = Amount ,
                                    Outlet_5Master = TitleObj, Outlet_5EntryMaster = EntObj)
                                    
        return(redirect('/HBudgetReport/Outlet_5List'))
    today = datetime.date.today()
    CYear = today.year
    CMonth = today.month
    mem = Outlet_5Master.objects.filter(IsDelete=False)
    return render(request, 'Outlet_5/Outlet_5Entry.html' ,{'mem':mem , 'CYear':range(CYear, 2020,-1),'CMonth':CMonth})                                                                  
                                                                                                                                                                                                                                                                                                              
def Outlet_5Delete(request,id):
    mem =  Outlet_5EntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/Outlet_5List'))

def Outlet_5Edit(request,id):   
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        FoodRevenue = request.POST['FoodRevenue']
        MealPlan = request.POST['FB_Revenue_Others']
        TotalFoodRevenue  = request.POST['TotalFoodRevenue']
        BeverageRevenue = request.POST['BeverageRevenue']
        TotalBEVERAGEREVENUE = request.POST['TotalBEVERAGEREVENUE']
        AudioVisualRevenue = request.POST['AudioVisualRevenue']
        FB_Revenue_Others = request.POST['FB_Revenue_Others']        
        TotalOtherIncome = request.POST['TotalOtherIncome']
        FB_Revenue = request.POST['FB_Revenue']
        FoodCostOfSales = request.POST['FoodCostOfSales']
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        AudioVisualEquipmentCostOfSale = request.POST['AudioVisualEquipmentCostOfSale']
        FB_OtherCostOfSales  = request.POST['FB_OtherCostOfSales']
        TotalCostOf_OtherRev = request.POST['TotalCostOf_OtherRev']       
        TotalCostOfSales = request.POST['TotalCostOfSales']
        GrossProfit  = request.POST['GrossProfit']
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        DepartmentIncome = request.POST['DepartmentIncome']     
      
        mem =  Outlet_5EntryMaster.objects.get(id = id)
       
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.FoodRevenue  =   FoodRevenue 
        mem.MealPlan =   MealPlan
        mem.TotalFoodRevenue  =   TotalFoodRevenue 
        mem.TotalBEVERAGEREVENUE =     TotalBEVERAGEREVENUE
        mem.BeverageRevenue =   BeverageRevenue       
        mem.AudioVisualRevenue =    AudioVisualRevenue        
        mem.FB_Revenue_Others  =  FB_Revenue_Others        
        mem.TotalOtherIncome =  TotalOtherIncome
        mem.FB_Revenue  =  FB_Revenue
        mem.FoodCostOfSales  =  FoodCostOfSales
        mem.BeverageCostOfSales =   BeverageCostOfSales 
        mem.TotalCostOfFBSales =  TotalCostOfFBSales
        mem.AudioVisualEquipmentCostOfSale =   AudioVisualEquipmentCostOfSale
        mem.FB_OtherCostOfSales =    FB_OtherCostOfSales 
        mem.TotalCostOf_OtherRev  = TotalCostOf_OtherRev 
        mem.TotalCostOfSales =   TotalCostOfSales       
        mem.GrossProfit  =   GrossProfit 
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives  =  Bonuses_and_Incentives 
        mem.Salary_Wages_and_Bonuses =  Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =   EmployeeBenefits 
        mem.PayrollRelatedExpenses  =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses =   PayrollAndRelatedExpenses
        mem.Total_Other_Expenses =  Total_Other_Expenses
        mem.DepartmentIncome  =   DepartmentIncome 
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 =   Outlet_5EntryMaster.objects.get(id = id)
            sv =  Outlet_5EntryDetail.objects.get(Outlet_5Master = TitleID_ , Outlet_5EntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
        return(redirect('/HBudgetReport/Outlet_5List'))
             
    mem1 = Outlet_5EntryDetail.objects.filter( Outlet_5EntryMaster=id ,IsDelete = False).select_related("Outlet_5Master")
    mem =  Outlet_5EntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'Outlet_5/Outlet_5Edit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})





def PL_Roomsviewdata(request, id):
    template_path = "PL_Rooms/PL_Roomsviewdata.html"
    mem1 = PL_RoomsEntryDetail.objects.filter(PL_RoomsEntryMaster=id , IsDelete = False).select_related("PL_RoomsMaster")
    mem = PL_RoomsEntryMaster.objects.get(id = id)
         
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
                                                                                                                    

def PL_RoomsList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = PL_RoomsEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )
    
    return render(request, 'PL_Rooms/PL_RoomsList.html' ,{'mem' :mem }) 
                                                                                                                                                                                                                        
def PL_RoomsEntry(request):  
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
        TransientRoomRevenue  = request.POST['TransientRoomRevenue']
        if(TransientRoomRevenue == ''):
            TransientRoomRevenue =0
        TransientRoomRevenueSez   = request.POST['TransientRoomRevenueSez']
        if(TransientRoomRevenueSez ==''):
            TransientRoomRevenueSez =0
        ClubMisc_O = request.POST['ClubMisc_O']
        if(ClubMisc_O == ''):
            ClubMisc_O =0
        RoomRevenueExtraBedCharge = request.POST['RoomRevenueExtraBedCharge']
        if(RoomRevenueExtraBedCharge == ''):
            RoomRevenueExtraBedCharge =0
        TotalRoomRevenue = request.POST['TotalRoomRevenue']
        if(TotalRoomRevenue == ''):
            TotalRoomRevenue =0
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
        if(DepartmentIncome ==''):
            DepartmentIncome =0
      
        enmaster =   PL_RoomsEntryMaster.objects.create(EntryMonth = EntryMonth, EntryYear = EntryYear,
                        TransientRoomRevenue = TransientRoomRevenue ,    TransientRoomRevenueSez =   TransientRoomRevenueSez , 
                         ClubMisc_O= ClubMisc_O,    RoomRevenueExtraBedCharge= RoomRevenueExtraBedCharge, 
                         TotalRoomRevenue=  TotalRoomRevenue,TotalExpenses=TotalExpenses,                                                                          
                  SalaryAndWages= SalaryAndWages ,  Bonuses_and_Incentives =  Bonuses_and_Incentives ,
               Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,  EmployeeBenefits= EmployeeBenefits,
              PayrollRelatedExpenses= PayrollRelatedExpenses, PayrollAndRelatedExpenses= PayrollAndRelatedExpenses,
              Total_Other_Expenses= Total_Other_Expenses ,  DepartmentIncome =  DepartmentIncome ,OrganizationID=OrganizationID,CreatedBy=UserID)        
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = PL_RoomsMaster.objects.get(id = TitleID_)
            EntObj = PL_RoomsEntryMaster.objects.get(id=enmaster.pk)
            
            v = PL_RoomsEntryDetail.objects.create(Amount = Amount ,
                                    PL_RoomsMaster = TitleObj, PL_RoomsEntryMaster = EntObj)
                                    
        return(redirect('/HBudgetReport/PL_RoomsList'))
    today = datetime.date.today()
    CYear = today.year
    CMmonth = today.month
    mem = PL_RoomsMaster.objects.filter(IsDelete=False)
    return render(request, 'PL_Rooms/PL_RoomsEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMmonth':CMmonth})                                                                  
                                                                                                                                                                                                                                                                                                                                                                                                     
def PL_RoomsDelete(request,id):
    mem =  PL_RoomsEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/PL_RoomsList'))
                                                                 

def PL_RoomsEdit(request,id):    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        TransientRoomRevenue  = request.POST['TransientRoomRevenue']
        TransientRoomRevenueSez   = request.POST['TransientRoomRevenueSez']
        ClubMisc_O = request.POST['ClubMisc_O']
        RoomRevenueExtraBedCharge = request.POST['RoomRevenueExtraBedCharge']
        TotalRoomRevenue = request.POST['TotalRoomRevenue']
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        TotalExpenses = request.POST['TotalExpenses']
        DepartmentIncome = request.POST['DepartmentIncome']
      
        mem =   PL_RoomsEntryMaster.objects.get(id = id)
       
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.TransientRoomRevenue  =  TransientRoomRevenue 
        mem.TransientRoomRevenueSez =    TransientRoomRevenueSez
        mem.ClubMisc_O  =    ClubMisc_O 
        mem.RoomRevenueExtraBedCharge =    RoomRevenueExtraBedCharge
        mem.TotalRoomRevenue  =    TotalRoomRevenue        
        mem.TotalExpenses = TotalExpenses
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives  =  Bonuses_and_Incentives 
        mem.Salary_Wages_and_Bonuses =  Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =   EmployeeBenefits 
        mem.PayrollRelatedExpenses  =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses =   PayrollAndRelatedExpenses
        mem.Total_Other_Expenses =  Total_Other_Expenses
        mem.DepartmentIncome  =   DepartmentIncome 
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 =   PL_RoomsEntryMaster.objects.get(id = id)
            sv =  PL_RoomsEntryDetail.objects.get(PL_RoomsMaster = TitleID_ , PL_RoomsEntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
        return(redirect('/HBudgetReport/PL_RoomsList'))
             
    mem1 = PL_RoomsEntryDetail.objects.filter( PL_RoomsEntryMaster=id ,IsDelete = False).select_related("PL_RoomsMaster")
    mem =  PL_RoomsEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'PL_Rooms/PL_RoomsEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})




def Total_OODviewdata(request, id):
    template_path = "Total_OOD/Total_OODviewdata.html"
    mem1 = Total_OODEntryDetail.objects.filter(Total_OODEntryMaster=id , IsDelete = False).select_related("Total_OODMaster")
    mem = Total_OODEntryMaster.objects.get(id = id)
         
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
                  
                                                                                                            
def Total_OODList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Total_OODEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        )
    
    return render(request, 'Total_OOD/Total_OODList.html' ,{'mem' :mem }) 
                                                                                                                                                                                                                     
def Total_OODEntry(request):  
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
        SpaTreatmentRevenue  = request.POST['SpaTreatmentRevenue']
        if(SpaTreatmentRevenue ==''):
            SpaTreatmentRevenue =0
        Mod_ExtGuestTransportation    = request.POST['Mod_ExtGuestTransportation']
        if(Mod_ExtGuestTransportation ==''):
            Mod_ExtGuestTransportation =0
        GuestLaundryRevenue = request.POST['GuestLaundryRevenue']
        if(GuestLaundryRevenue == ''):
            GuestLaundryRevenue= 0
        Revenue = request.POST['Revenue']
        if(Revenue ==''):
            Revenue =0
        Cost_OfMerchandise = request.POST['Cost_OfMerchandise']
        if(Cost_OfMerchandise == ''):
            Cost_OfMerchandise =0
        Cost_OfGuestTransportation = request.POST['Cost_OfGuestTransportation']
        if(Cost_OfGuestTransportation == ''):
            Cost_OfGuestTransportation =0
        Cost_OfLaundryServices = request.POST['Cost_OfLaundryServices']
        if(Cost_OfLaundryServices == ''):
            Cost_OfLaundryServices
        Total_CostOfSales = request.POST['Total_CostOfSales']
        if(Total_CostOfSales == ''):
            Total_CostOfSales =0
        GrossProfit = request.POST['GrossProfit']      
        if(GrossProfit == ''):
            GrossProfit =0
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
        if(TotalExpenses ==''):
            TotalExpenses =0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome ==''):
            DepartmentIncome ==0
      
        enmaster =   Total_OODEntryMaster.objects.create(EntryMonth = EntryMonth, EntryYear = EntryYear,
                     SpaTreatmentRevenue = SpaTreatmentRevenue  , Mod_ExtGuestTransportation = Mod_ExtGuestTransportation  , 
                     GuestLaundryRevenue= GuestLaundryRevenue,  Revenue= Revenue, Cost_OfMerchandise = Cost_OfMerchandise , 
                        TotalExpenses=TotalExpenses,   Cost_OfGuestTransportation=  Cost_OfGuestTransportation,                                                                         
                  SalaryAndWages= SalaryAndWages ,  Bonuses_and_Incentives =  Bonuses_and_Incentives ,  Cost_OfLaundryServices=  Cost_OfLaundryServices,
               Salary_Wages_and_Bonuses= Salary_Wages_and_Bonuses,  EmployeeBenefits= EmployeeBenefits,Total_CostOfSales=Total_CostOfSales,
              PayrollRelatedExpenses= PayrollRelatedExpenses, PayrollAndRelatedExpenses= PayrollAndRelatedExpenses,GrossProfit=GrossProfit,
              Total_Other_Expenses= Total_Other_Expenses ,  DepartmentIncome =  DepartmentIncome ,OrganizationID=OrganizationID,CreatedBy=UserID)        
        enmaster.save()

        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = Total_OODMaster.objects.get(id = TitleID_)
            EntObj = Total_OODEntryMaster.objects.get(id=enmaster.pk)
            
            v = Total_OODEntryDetail.objects.create(Amount = Amount ,
                                    Total_OODMaster = TitleObj, Total_OODEntryMaster = EntObj)
                                    
        return(redirect('/HBudgetReport/Total_OODList'))
    today = datetime.date.today()
    CYear = today.year
    CMmonth = today.month
    mem = Total_OODMaster.objects.filter(IsDelete=False)
    return render(request, 'Total_OOD/Total_OODEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMmonth':CMmonth})                                                                  
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
def Total_OODDelete(request,id):
    mem =  Total_OODEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/Total_OODList'))
                                                         

def Total_OODEdit(request,id):    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        SpaTreatmentRevenue  = request.POST['SpaTreatmentRevenue']
        Mod_ExtGuestTransportation    = request.POST['Mod_ExtGuestTransportation']
        GuestLaundryRevenue = request.POST['GuestLaundryRevenue']
        Revenue = request.POST['Revenue']
        Cost_OfMerchandise = request.POST['Cost_OfMerchandise']
        Cost_OfGuestTransportation = request.POST['Cost_OfGuestTransportation']
        Cost_OfLaundryServices = request.POST['Cost_OfLaundryServices']
        Total_CostOfSales = request.POST['Total_CostOfSales']
        GrossProfit = request.POST['GrossProfit']      
        SalaryAndWages = request.POST['SalaryAndWages']
        Bonuses_and_Incentives = request.POST['Bonuses_and_Incentives']
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        EmployeeBenefits = request.POST['EmployeeBenefits']
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        Total_Other_Expenses  = request.POST['Total_Other_Expenses']
        TotalExpenses = request.POST['TotalExpenses']
        DepartmentIncome = request.POST['DepartmentIncome']
      
      
        mem =   Total_OODEntryMaster.objects.get(id = id)
       
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.SpaTreatmentRevenue   =   SpaTreatmentRevenue  
        mem.Mod_ExtGuestTransportation =   Mod_ExtGuestTransportation
        mem.GuestLaundryRevenue   =     GuestLaundryRevenue  
        mem.Revenue  =   Revenue  
        mem.Cost_OfMerchandise = Cost_OfMerchandise
        mem.Cost_OfGuestTransportation = Cost_OfGuestTransportation
        mem.Cost_OfLaundryServices = Cost_OfLaundryServices
        mem.Total_CostOfSales = Total_CostOfSales
        mem.GrossProfit = GrossProfit       
        mem.SalaryAndWages = SalaryAndWages
        mem.Bonuses_and_Incentives  =  Bonuses_and_Incentives 
        mem.Salary_Wages_and_Bonuses =  Salary_Wages_and_Bonuses
        mem.EmployeeBenefits  =   EmployeeBenefits 
        mem.PayrollRelatedExpenses  =  PayrollRelatedExpenses 
        mem.PayrollAndRelatedExpenses =   PayrollAndRelatedExpenses
        mem.Total_Other_Expenses =  Total_Other_Expenses
        mem.TotalExpenses = TotalExpenses
        mem.DepartmentIncome  =   DepartmentIncome 
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 =   Total_OODEntryMaster.objects.get(id = id)
            sv =  Total_OODEntryDetail.objects.get(Total_OODMaster = TitleID_ , Total_OODEntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
        return(redirect('/HBudgetReport/Total_OODList'))
             
    mem1 = Total_OODEntryDetail.objects.filter( Total_OODEntryMaster=id ,IsDelete = False).select_related("Total_OODMaster")
    mem =  Total_OODEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'Total_OOD/Total_OODEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})






def PL_Summaryviewdata(request, id):
    template_path = "PL_Summary/PL_Summaryviewdata.html"
    mem1 = PL_SummaryEntryDetail.objects.filter(PL_SummaryEntryMaster=id , IsDelete = False).select_related("PL_SummaryMaster")
    mem = PL_SummaryEntryMaster.objects.get(id = id)
         
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
                  
                                                                                                           
def PL_SummaryList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = PL_SummaryEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()
    
    return render(request, 'PL_Summary/PL_SummaryList.html' ,{'mem' :mem }) 

                                                                                                                                                                                                                    
def PL_SummaryEntry(request):  
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
        RoomsRevenue  = request.POST['RoomsRevenue']
        if(RoomsRevenue==''):
                RoomsRevenue=0
        FoodAndBeverageRevenue    = request.POST['FoodAndBeverageRevenue']
        if(FoodAndBeverageRevenue==''):
                FoodAndBeverageRevenue=0
        OtherOperatedDepartmentRevenue = request.POST['OtherOperatedDepartmentRevenue']
        if(OtherOperatedDepartmentRevenue ==''):
            OtherOperatedDepartmentRevenue = 0
        RentalsAndOtherIncome = request.POST['RentalsAndOtherIncome']
        if(RentalsAndOtherIncome ==''):
            RentalsAndOtherIncome =0
        TotalRevenue = request.POST['TotalRevenue']
        if(TotalRevenue ==''):
            TotalRevenue =0
        RoomExpenses = request.POST['RoomExpenses']
        if(RoomExpenses==''):
            RoomExpenses=0
        FoodAndBeverageExpenses = request.POST['FoodAndBeverageExpenses']
        if(FoodAndBeverageExpenses==''):
            FoodAndBeverageExpenses=0
        OtherOperatedDepartmentExpenses = request.POST['OtherOperatedDepartmentExpenses']
        if(OtherOperatedDepartmentExpenses==''):
            OtherOperatedDepartmentExpenses=0
        Total_DepartmentalExpenses = request.POST['Total_DepartmentalExpenses']   
        if(Total_DepartmentalExpenses==''):
            Total_DepartmentalExpenses = 0   
        Total_DepartmentalIncome = request.POST['Total_DepartmentalIncome']
        if(Total_DepartmentalIncome==''):
            Total_DepartmentalIncome = 0
        AdministrationAndGeneral = request.POST['AdministrationAndGeneral']
        if(AdministrationAndGeneral ==''):
            AdministrationAndGeneral = 0
        InformationAndTelecommunicationsSystem = request.POST['InformationAndTelecommunicationsSystem']
        if(InformationAndTelecommunicationsSystem==''):
            InformationAndTelecommunicationsSystem=0
        SalesAndMarketing = request.POST['SalesAndMarketing']
        if(SalesAndMarketing==''):
            SalesAndMarketing=0
        PropertyOperartionAndMaintenance = request.POST['PropertyOperartionAndMaintenance']
        if(PropertyOperartionAndMaintenance==''):
            PropertyOperartionAndMaintenance=0
        Utilities = request.POST['Utilities']
        if(Utilities==''):
            Utilities=0
        TotalUndistributedExpenses  = request.POST['TotalUndistributedExpenses']
        if(TotalUndistributedExpenses==''):
            TotalUndistributedExpenses=0
        GrossOperatingProfit = request.POST['GrossOperatingProfit']
        if(GrossOperatingProfit==''):
            GrossOperatingProfit
        GOP = request.POST['GOP']
        if(GOP==''):
            GOP =0
      
        enmaster =   PL_SummaryEntryMaster.objects.create(EntryMonth = EntryMonth, EntryYear = EntryYear, RoomsRevenue=RoomsRevenue,
                       FoodAndBeverageRevenue=FoodAndBeverageRevenue, OtherOperatedDepartmentRevenue=OtherOperatedDepartmentRevenue,
                     RentalsAndOtherIncome=RentalsAndOtherIncome, TotalRevenue=TotalRevenue,RoomExpenses=RoomExpenses,
                   FoodAndBeverageExpenses=FoodAndBeverageExpenses, OtherOperatedDepartmentExpenses=OtherOperatedDepartmentExpenses,
                Total_DepartmentalExpenses=Total_DepartmentalExpenses, Total_DepartmentalIncome=Total_DepartmentalIncome,
                AdministrationAndGeneral=AdministrationAndGeneral, InformationAndTelecommunicationsSystem=InformationAndTelecommunicationsSystem,
               SalesAndMarketing=SalesAndMarketing, PropertyOperartionAndMaintenance=PropertyOperartionAndMaintenance,
                Utilities=Utilities, TotalUndistributedExpenses=TotalUndistributedExpenses,  GrossOperatingProfit=GrossOperatingProfit,
                   GOP=GOP ,   OrganizationID=OrganizationID,CreatedBy=UserID)  
        enmaster.save()
       
        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = PL_SummaryMaster.objects.get(id = TitleID_)
            EntObj = PL_SummaryEntryMaster.objects.get(id=enmaster.pk)
            
            v = PL_SummaryEntryDetail.objects.create(Amount = Amount ,
                                    PL_SummaryMaster = TitleObj, PL_SummaryEntryMaster = EntObj)
                                    
        return(redirect('/HBudgetReport/PL_SummaryList'))
    today = datetime.date.today()
    CYear = today.year
    CMmonth = today.month
    mem = PL_SummaryMaster.objects.filter(IsDelete=False)
    return render(request, 'PL_Summary/PL_SummaryEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMmonth':CMmonth})                                                                  
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
def PL_SummaryDelete(request,id):
    mem =  PL_SummaryEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/PL_SummaryList'))
                                                         

def PL_SummaryEdit(request,id):    
    if request.method =="POST":
        
        EntryMonth = request.POST['EntryMonth']
        EntryYear = request.POST['EntryYear']
        RoomsRevenue  = request.POST['RoomsRevenue']
        FoodAndBeverageRevenue    = request.POST['FoodAndBeverageRevenue']
        OtherOperatedDepartmentRevenue = request.POST['OtherOperatedDepartmentRevenue']
        RentalsAndOtherIncome = request.POST['RentalsAndOtherIncome']
        TotalRevenue = request.POST['TotalRevenue']
        RoomExpenses = request.POST['RoomExpenses']
        FoodAndBeverageExpenses = request.POST['FoodAndBeverageExpenses']
        OtherOperatedDepartmentExpenses = request.POST['OtherOperatedDepartmentExpenses']
        Total_DepartmentalExpenses = request.POST['Total_DepartmentalExpenses']      
        Total_DepartmentalIncome = request.POST['Total_DepartmentalIncome']
        AdministrationAndGeneral = request.POST['AdministrationAndGeneral']
        InformationAndTelecommunicationsSystem = request.POST['InformationAndTelecommunicationsSystem']
        SalesAndMarketing = request.POST['SalesAndMarketing']
        PropertyOperartionAndMaintenance = request.POST['PropertyOperartionAndMaintenance']
        Utilities = request.POST['Utilities']
        TotalUndistributedExpenses  = request.POST['TotalUndistributedExpenses']
        GrossOperatingProfit = request.POST['GrossOperatingProfit']
        GOP = request.POST['GOP']
           
        mem =   PL_SummaryEntryMaster.objects.get(id = id)
       
        mem.EntryMonth = EntryMonth
        mem.EntryYear = EntryYear
        mem.RoomsRevenue   =   RoomsRevenue  
        mem.FoodAndBeverageRevenue =   FoodAndBeverageRevenue
        mem.OtherOperatedDepartmentRevenue   =     OtherOperatedDepartmentRevenue  
        mem.RentalsAndOtherIncome  =   RentalsAndOtherIncome  
        mem.TotalRevenue = TotalRevenue
        mem.RoomExpenses = RoomExpenses
        mem.FoodAndBeverageExpenses = FoodAndBeverageExpenses
        mem.OtherOperatedDepartmentExpenses = OtherOperatedDepartmentExpenses
        mem.Total_DepartmentalExpenses = Total_DepartmentalExpenses       
        mem.Total_DepartmentalIncome = Total_DepartmentalIncome
        mem.AdministrationAndGeneral  =  AdministrationAndGeneral 
        mem.InformationAndTelecommunicationsSystem =  InformationAndTelecommunicationsSystem
        mem.SalesAndMarketing  =   SalesAndMarketing 
        mem.PropertyOperartionAndMaintenance  =  PropertyOperartionAndMaintenance 
        mem.Utilities =   Utilities
        mem.TotalUndistributedExpenses =  TotalUndistributedExpenses
        mem.GrossOperatingProfit = GrossOperatingProfit
        mem.GOP  =   GOP 
        mem.save()
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem) +1):
           
            TitleID_ = request.POST["TitleID_" + str(x)]
            Amount = request.POST["Amount_" + str(x)]
            mem1 =   PL_SummaryEntryMaster.objects.get(id = id)
            sv =  PL_SummaryEntryDetail.objects.get(PL_SummaryMaster = TitleID_ , PL_SummaryEntryMaster = id)
            sv.Amount =  Amount
            sv.save()
            
        return(redirect('/HBudgetReport/PL_SummaryList'))
             
    mem1 = PL_SummaryEntryDetail.objects.filter( PL_SummaryEntryMaster=id ,IsDelete = False).select_related("PL_SummaryMaster")
    mem =  PL_SummaryEntryMaster.objects.get(id = id)
    
    today = datetime.date.today()
    CYear = today.year
    CYear = int(CYear)+1
    return render(request ,'PL_Summary/PL_SummaryEdit.html' , {'mem1' :mem1 , 'mem':mem ,'CYear':range(2022,CYear)})




                                                                                                           
def Total_FBList(request):
    
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = Total_FBEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()
    
    return render(request, 'Total_FB/Total_FBList.html' ,{'mem' :mem }) 

                                                                                                                                                                                                                   
def Total_FBEntry(request):  
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
        FoodRevenue  = request.POST['FoodRevenue']
        if(FoodRevenue==''):
                FoodRevenue=0
        TotalFoodRevenue    = request.POST['TotalFoodRevenue']
        if(TotalFoodRevenue==''):
                TotalFoodRevenue=0
        BeverageRevenue = request.POST['BeverageRevenue']
        if(BeverageRevenue ==''):
            BeverageRevenue = 0
        TotalBeverageRevenue = request.POST['TotalBeverageRevenue']
        if(TotalBeverageRevenue ==''):
            TotalBeverageRevenue =0
        AudioVisualEquipmentCostOfSales1 = request.POST['AudioVisualEquipmentCostOfSales1']
        if(AudioVisualEquipmentCostOfSales1 ==''):
            AudioVisualEquipmentCostOfSales1 =0
        FB_OtherCostOfSales1 = request.POST['FB_OtherCostOfSales1']
        if(FB_OtherCostOfSales1==''):
            FB_OtherCostOfSales1=0
        HallRental = request.POST['HallRental']
        if(HallRental==''):
            HallRental=0
        FB_Revenue_MISC = request.POST['FB_Revenue_MISC']
        if(FB_Revenue_MISC==''):
            FB_Revenue_MISC=0
        TotalOtherIncome = request.POST['TotalOtherIncome']   
        if(TotalOtherIncome==''):
            TotalOtherIncome = 0   
        FB_Revenue = request.POST['FB_Revenue']
        if(FB_Revenue==''):
            FB_Revenue = 0
        FoodCostOfSales = request.POST['FoodCostOfSales']
        if(FoodCostOfSales ==''):
            FoodCostOfSales = 0
        BeverageCostOfSales = request.POST['BeverageCostOfSales']
        if(BeverageCostOfSales==''):
            BeverageCostOfSales=0
        TotalCostOfFBSales = request.POST['TotalCostOfFBSales']
        if(TotalCostOfFBSales==''):
            TotalCostOfFBSales=0
        AudioVisualEquipmentCostOfSales2 = request.POST['AudioVisualEquipmentCostOfSales2']
        if(AudioVisualEquipmentCostOfSales2==''):
            AudioVisualEquipmentCostOfSales2=0
        FB_OtherCostOfSales2 = request.POST['FB_OtherCostOfSales2']
        if(FB_OtherCostOfSales2==''):
            FB_OtherCostOfSales2=0
        TotalCostOfOtherRev  = request.POST['TotalCostOfOtherRev']
        if(TotalCostOfOtherRev==''):
            TotalCostOfOtherRev=0
        TotalCostOfSales = request.POST['TotalCostOfSales']
        if(TotalCostOfSales==''):
            TotalCostOfSales =0
        GrossProfit = request.POST['GrossProfit']
        if(GrossProfit ==''):
            GrossProfit=0
        Salary_Wages_and_Bonuses = request.POST['Salary_Wages_and_Bonuses']
        if(Salary_Wages_and_Bonuses==''):
            Salary_Wages_and_Bonuses = 0
        EmployeeBenefits = request.POST['EmployeeBenefits']
        if(EmployeeBenefits==''):
            EmployeeBenefits=0
        PayrollRelatedExpenses = request.POST['PayrollRelatedExpenses']
        if(PayrollRelatedExpenses==''):
            PayrollRelatedExpenses =0
        PayrollAndRelatedExpenses = request.POST['PayrollAndRelatedExpenses']
        if(PayrollAndRelatedExpenses==''):
            PayrollAndRelatedExpenses=0
        Total_Other_Expenses = request.POST['Total_Other_Expenses']
        if(Total_Other_Expenses==''):
            Total_Other_Expenses=0
        DepartmentIncome = request.POST['DepartmentIncome']
        if(DepartmentIncome==''):
            DepartmentIncome=0
        RoomsAvailable = request.POST['RoomsAvailable']
        if(RoomsAvailable==''):
            RoomsAvailable=0
        RoomsOccupied = request.POST['RoomsOccupied']
        if(RoomsOccupied==''):
            RoomsOccupied=0
        Occupany = request.POST['Occupany']
        if(Occupany==''):
            Occupany =0
        NumberOfGuests = request.POST['NumberOfGuests']     
        if(NumberOfGuests==''):
            NumberOfGuests=0
        NoOfFoodCovers = request.POST['NoOfFoodCovers']
        if(NoOfFoodCovers ==''):
            NoOfFoodCovers =0
        NoOfBeverageCovers = request.POST['NoOfBeverageCovers']
        if(NoOfBeverageCovers==''):
            NoOfBeverageCovers=0
        AveFoodPerCoverage = request.POST['AveFoodPerCoverage']
        if(AveFoodPerCoverage ==''):
            AveFoodPerCoverage = 0
        AveBeveragePerCoverage = request.POST['AveBeveragePerCoverage']
        if(AveBeveragePerCoverage==''):
            AveBeveragePerCoverage=0
        AveFoodAndBeveragePerCoverage = request.POST['AveFoodAndBeveragePerCoverage']
        if(AveFoodAndBeveragePerCoverage==''):
            AveFoodAndBeveragePerCoverage=0
      
        enmaster =   Total_FBEntryMaster.objects.create(EntryMonth = EntryMonth, EntryYear = EntryYear,FoodRevenue=FoodRevenue,
                       TotalFoodRevenue=TotalFoodRevenue, BeverageRevenue=BeverageRevenue,
                     TotalBeverageRevenue=TotalBeverageRevenue,AudioVisualEquipmentCostOfSales1=AudioVisualEquipmentCostOfSales1,FB_OtherCostOfSales1=FB_OtherCostOfSales1,
                   HallRental=HallRental, FB_Revenue_MISC=FB_Revenue_MISC,TotalOtherIncome=TotalOtherIncome,FB_Revenue=FB_Revenue,
                FoodCostOfSales=FoodCostOfSales, BeverageCostOfSales=BeverageCostOfSales,TotalCostOfFBSales=TotalCostOfFBSales,AudioVisualEquipmentCostOfSales2=AudioVisualEquipmentCostOfSales2,
                FB_OtherCostOfSales2=FB_OtherCostOfSales2,TotalCostOfOtherRev=TotalCostOfOtherRev, 
                   TotalCostOfSales=TotalCostOfSales ,GrossProfit=GrossProfit,Salary_Wages_and_Bonuses=Salary_Wages_and_Bonuses,EmployeeBenefits=EmployeeBenefits,
            PayrollRelatedExpenses=PayrollRelatedExpenses,PayrollAndRelatedExpenses=PayrollAndRelatedExpenses, Total_Other_Expenses=Total_Other_Expenses,
           DepartmentIncome=DepartmentIncome, RoomsAvailable=RoomsAvailable,RoomsOccupied=RoomsOccupied,
          Occupany=Occupany,NumberOfGuests=NumberOfGuests,NoOfFoodCovers=NoOfFoodCovers,NoOfBeverageCovers=NoOfBeverageCovers,
          AveFoodPerCoverage=AveFoodPerCoverage,AveBeveragePerCoverage=AveBeveragePerCoverage,AveFoodAndBeveragePerCoverage=AveFoodAndBeveragePerCoverage,
               OrganizationID=OrganizationID,CreatedBy=UserID)  
        enmaster.save()
       
        TotalItem = request.POST["TotalItem"] 
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount==''):
                Amount=0
                              
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObj = Total_FBMaster.objects.get(id = TitleID_)
            EntObj = Total_FBEntryMaster.objects.get(id=enmaster.pk)
            
            v = Total_FBEntryDetail.objects.create(Amount = Amount ,
                                    Total_FBMaster = TitleObj, Total_FBEntryMaster = EntObj)
                                    
        return(redirect('/HBudgetReport/Total_FBList'))
    today = datetime.date.today()
    CYear = today.year
    CMmonth = today.month
    mem = Total_FBMaster.objects.filter(IsDelete=False)
    return render(request, 'Total_FB/Total_FBEntry.html' ,{'mem':mem , 'CYear':range(CYear,2020,-1),'CMmonth':CMmonth})                                                                  
                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
def Total_FBDelete(request,id):
    mem =  Total_FBEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return (redirect('/HBudgetReport/Total_FBList'))
                                                        