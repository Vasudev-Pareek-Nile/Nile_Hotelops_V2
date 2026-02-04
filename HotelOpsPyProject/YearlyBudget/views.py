from django.shortcuts import render
from django.shortcuts import render,redirect
from .models import Entry_Master_Year
from datetime import date
import datetime
from decimal import Decimal
import requests
from  django.db.models import Sum
from hotelopsmgmtpy.GlobalConfig import MasterAttribute

from .models import Finance_Category,Finance_Category_Entry_Details,Market_Segment_Category,Market_Segment_Entry_Details,Business_Source_Category,Business_Source_Entry_Details,ExpensesIncludingPayroll,CostPerCover,CostPerOccupiedRoomNight,ExpensesIncludingPayrollEntryDetails,CostPerCoverEntryDetails,CostPerOccupiedRoomNightEntryDetails, Engineering_Category_Entry_Details, Engineering_Category

from django.contrib import messages
def YearlyBudget_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
        'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = f"https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID="+str(OrganizationID)

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    # if I is not None:
    #     OrganizationID=I
    I = request.GET.get('I')
    if I is None:
         I =OrganizationID  
    data = Entry_Master_Year.objects.filter(OrganizationID=I, IsDelete=False)
    
    
    context =  {'memOrg':memOrg ,'OrganizationID':OrganizationID,'data':data,'I':I} 
    return render(request, "YearlyBudget/YearlyBudget_list.html",context)

def YearlyBudget_Entry_Details(request):
    # if 'OrganizationID' not in request.session:
    #     return redirect(MasterAttribute.Host)
    # else:
    #     print("Show Page Session")

    if 'OrganizationID' not in request.session:
        if request.method == 'POST':
            OrganizationID = request.POST["OrganizationID"]
            
        else:
            if 'OrganizationID' not in request.session:
                return redirect(MasterAttribute.Host)
            else:
                OrganizationID = request.session["OrganizationID"]
           
    else:
        OrganizationID = request.session["OrganizationID"]
        UserID = str(request.session["UserID"])
   
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
        'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = f"https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID="+str(OrganizationID)

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    
    
    EntryYear = request.GET.get('EntryYear')
    I = request.GET.get('I')
    if I is None:
         I =OrganizationID
    if EntryYear is None:
         today = datetime.date.today()
         EntryYear =today.year
    try:
        enmaster = Entry_Master_Year.objects.get(EntryYear=EntryYear, OrganizationID=I, IsDelete=False)
    except Entry_Master_Year.DoesNotExist:
        enmaster = Entry_Master_Year.objects.create(EntryYear=EntryYear, OrganizationID=I, CreatedBy= UserID,IsDelete=False)


    
    
    engineering_category = Engineering_Category.objects.filter(IsDelete=False)
    finance_category = Finance_Category.objects.filter(IsDelete=False)
    business_source_category  = Business_Source_Category.objects.filter(IsDelete=False)
    market_segment_category  = Market_Segment_Category.objects.filter(IsDelete=False)
    Expenses = ExpensesIncludingPayroll.objects.filter(IsDelete=False)
    CostCover = CostPerCover.objects.filter(IsDelete=False)
    CostOccupied = CostPerOccupiedRoomNight.objects.filter(IsDelete=False)

    
    for i in  finance_category:
         i.Month_1 =0
         i.Month_2 =0
         i.Month_3 =0
         i.Month_4 =0
         i.Month_5 =0
         i.Month_6 =0
         i.Month_7 =0
         i.Month_8 =0
         i.Month_9 =0
         i.Month_10 =0
         i.Month_11 =0
         i.Month_12 =0
            
         FC = Finance_Category_Entry_Details.objects.filter(IsDelete=False,EntryMaster = enmaster.pk ,Finance_Category_Name =i.id  )
        
         if FC.exists():
              i.Month_1 =FC[0].Month_1
              i.Month_2 =FC[0].Month_2
              i.Month_3 =FC[0].Month_3
              i.Month_4 =FC[0].Month_4
              i.Month_5 =FC[0].Month_5
              i.Month_6 =FC[0].Month_6
              i.Month_7 =FC[0].Month_7
              i.Month_8 =FC[0].Month_8
              i.Month_9 =FC[0].Month_9
              i.Month_10 =FC[0].Month_10
              i.Month_11 =FC[0].Month_11
              i.Month_12 =FC[0].Month_12
      
    for i in  market_segment_category:

         i.Month_1 =0
         i.Month_2 =0
         i.Month_3 =0
         i.Month_4 =0
         i.Month_5 =0
         i.Month_6 =0
         i.Month_7 =0
         i.Month_8 =0
         i.Month_9 =0
         i.Month_10 =0
         i.Month_11 =0
         i.Month_12 =0
         MSC = Market_Segment_Entry_Details.objects.filter(IsDelete=False,EntryMaster = enmaster.pk ,Market_Segment_Category_Name =i.id  )
         if MSC.exists():
              i.Month_1 =MSC[0].Month_1
              i.Month_2 =MSC[0].Month_2
              i.Month_3 =MSC[0].Month_3
              i.Month_4 =MSC[0].Month_4
              i.Month_5 =MSC[0].Month_5
              i.Month_6 =MSC[0].Month_6
              i.Month_7 =MSC[0].Month_7
              i.Month_8 =MSC[0].Month_8
              i.Month_9 =MSC[0].Month_9
              i.Month_10 =MSC[0].Month_10
              i.Month_11 =MSC[0].Month_11
              i.Month_12 =MSC[0].Month_12
    for i in  business_source_category:

         i.Month_1 =0
         i.Month_2 =0
         i.Month_3 =0
         i.Month_4 =0
         i.Month_5 =0
         i.Month_6 =0
         i.Month_7 =0
         i.Month_8 =0
         i.Month_9 =0
         i.Month_10 =0
         i.Month_11 =0
         i.Month_12 =0
         BSE = Business_Source_Entry_Details.objects.filter(IsDelete=False,EntryMaster = enmaster.pk ,Business_Source_Category_Name =i.id  )
         if BSE.exists():
              i.Month_1 =BSE[0].Month_1
              i.Month_2 =BSE[0].Month_2
              i.Month_3 =BSE[0].Month_3
              i.Month_4 =BSE[0].Month_4
              i.Month_5 =BSE[0].Month_5
              i.Month_6 =BSE[0].Month_6
              i.Month_7 =BSE[0].Month_7
              i.Month_8 =BSE[0].Month_8
              i.Month_9 =BSE[0].Month_9
              i.Month_10 =BSE[0].Month_10
              i.Month_11 =BSE[0].Month_11
              i.Month_12 =BSE[0].Month_12
    
    for i  in Expenses:
         i.Month_1 =0
         i.Month_2 =0
         i.Month_3 =0
         i.Month_4 =0
         i.Month_5 =0
         i.Month_6 =0
         i.Month_7 =0
         i.Month_8 =0
         i.Month_9 =0
         i.Month_10 =0
         i.Month_11 =0
         i.Month_12 =0
         EXP = ExpensesIncludingPayrollEntryDetails.objects.filter(IsDelete=False,EntryMaster = enmaster.pk ,ExpensesIncludingPayroll =i.id  )
         if EXP.exists():
              i.Month_1 =EXP[0].Month_1
              i.Month_2 =EXP[0].Month_2
              i.Month_3 =EXP[0].Month_3
              i.Month_4 =EXP[0].Month_4
              i.Month_5 =EXP[0].Month_5
              i.Month_6 =EXP[0].Month_6
              i.Month_7 =EXP[0].Month_7
              i.Month_8 =EXP[0].Month_8
              i.Month_9 =EXP[0].Month_9
              i.Month_10 =EXP[0].Month_10
              i.Month_11 =EXP[0].Month_11
              i.Month_12 =EXP[0].Month_12
    
    for i  in CostCover:
         i.Month_1 =0
         i.Month_2 =0
         i.Month_3 =0
         i.Month_4 =0
         i.Month_5 =0
         i.Month_6 =0
         i.Month_7 =0
         i.Month_8 =0
         i.Month_9 =0
         i.Month_10 =0
         i.Month_11 =0
         i.Month_12 =0
         CPC = CostPerCoverEntryDetails.objects.filter(IsDelete=False,EntryMaster = enmaster.pk ,CostPerCover =i.id  )
         if CPC.exists():
              i.Month_1 =CPC[0].Month_1
              i.Month_2 =CPC[0].Month_2
              i.Month_3 =CPC[0].Month_3
              i.Month_4 =CPC[0].Month_4
              i.Month_5 =CPC[0].Month_5
              i.Month_6 =CPC[0].Month_6
              i.Month_7 =CPC[0].Month_7
              i.Month_8 =CPC[0].Month_8
              i.Month_9 =CPC[0].Month_9
              i.Month_10 =CPC[0].Month_10
              i.Month_11 =CPC[0].Month_11
              i.Month_12 =CPC[0].Month_12

    for i  in CostOccupied:
         i.Month_1 =0
         i.Month_2 =0
         i.Month_3 =0
         i.Month_4 =0
         i.Month_5 =0
         i.Month_6 =0
         i.Month_7 =0
         i.Month_8 =0
         i.Month_9 =0
         i.Month_10 =0
         i.Month_11 =0
         i.Month_12 =0
         CPOCRN = CostPerOccupiedRoomNightEntryDetails.objects.filter(IsDelete=False,EntryMaster = enmaster.pk ,CostPerOccupiedRoomNight =i.id  )
         if CPOCRN.exists():
              i.Month_1 =CPOCRN[0].Month_1
              i.Month_2 =CPOCRN[0].Month_2
              i.Month_3 =CPOCRN[0].Month_3
              i.Month_4 =CPOCRN[0].Month_4
              i.Month_5 =CPOCRN[0].Month_5
              i.Month_6 =CPOCRN[0].Month_6
              i.Month_7 =CPOCRN[0].Month_7
              i.Month_8 =CPOCRN[0].Month_8
              i.Month_9 =CPOCRN[0].Month_9
              i.Month_10 =CPOCRN[0].Month_10
              i.Month_11 =CPOCRN[0].Month_11
              i.Month_12 =CPOCRN[0].Month_12
    

        
    for i in engineering_category:
         i.Month_1 =0
         i.Month_2 =0
         i.Month_3 =0
         i.Month_4 =0
         i.Month_5 =0
         i.Month_6 =0
         i.Month_7 =0
         i.Month_8 =0
         i.Month_9 =0
         i.Month_10 =0
         i.Month_11 =0
         i.Month_12 =0
            
         EC = Engineering_Category_Entry_Details.objects.filter(
              IsDelete=False,
              EntryMaster = enmaster.pk,
              Engineering_Category_Name =i.id  
            )
        
         if EC.exists():
              i.Month_1 =EC[0].Month_1
              i.Month_2 =EC[0].Month_2
              i.Month_3 =EC[0].Month_3
              i.Month_4 =EC[0].Month_4
              i.Month_5 =EC[0].Month_5
              i.Month_6 =EC[0].Month_6
              i.Month_7 =EC[0].Month_7
              i.Month_8 =EC[0].Month_8
              i.Month_9 =EC[0].Month_9
              i.Month_10 =EC[0].Month_10
              i.Month_11 =EC[0].Month_11
              i.Month_12 =EC[0].Month_12
      
    if request.method == 'POST':
            Fc = Finance_Category_Entry_Details.objects.filter(IsDelete=False, EntryMaster=enmaster)
            for finance_category_detail in Fc:
                finance_category_detail.IsDelete = True
                finance_category_detail.ModifyBy = UserID
                finance_category_detail.save()

            MSE = Market_Segment_Entry_Details.objects.filter(IsDelete=False, EntryMaster=enmaster)
            for market_segment_category_details in MSE:
                market_segment_category_details.IsDelete = True
                market_segment_category_details.ModifyBy = UserID
                market_segment_category_details.save()    

            BSE = Business_Source_Entry_Details.objects.filter(IsDelete=False, EntryMaster=enmaster)
            for business_source_category_details in BSE:
                business_source_category_details.IsDelete = True
                business_source_category_details.ModifyBy = UserID
                business_source_category_details.save()
            
            EXP = ExpensesIncludingPayrollEntryDetails.objects.filter(IsDelete=False,EntryMaster =enmaster)
            for ExpDetails in EXP:
                 ExpDetails.IsDelete = True
                 ExpDetails.ModifyBy = UserID
                 ExpDetails.save()

            CPC = CostPerCoverEntryDetails.objects.filter(IsDelete=False,EntryMaster =enmaster)
            for CostCoverDetails in CPC:
                 CostCoverDetails.IsDelete = True
                 CostCoverDetails.ModifyBy = UserID
                 CostCoverDetails.save()  

            CPOCRN = CostPerOccupiedRoomNightEntryDetails.objects.filter(IsDelete=False,EntryMaster =enmaster)
            for CostOccupiedDetails in CPOCRN:
                 CostOccupiedDetails.IsDelete = True
                 CostOccupiedDetails.ModifyBy = UserID
                 CostOccupiedDetails.save()          

            EC = Engineering_Category_Entry_Details.objects.filter(IsDelete=False,EntryMaster=enmaster)
            for EC_Detials in EC:
                EC_Detials.IsDelete = True
                EC_Detials.ModifyBy = UserID
                EC_Detials.save()          


            

            Total_finance_category_item = int(request.POST["Total_finance_category_item"])            
            months = ["Month_1", "Month_2", "Month_3", "Month_4", "Month_5", "Month_6", "Month_7", "Month_8", "Month_9", "Month_10", "Month_11", "Month_12"]
            
            for x in range(Total_finance_category_item + 1):
                    month_data = []
                    for month in months:
                        month_key = f"finance_category_{month}_{x}"
                        month_value = request.POST.get(month_key)
                    
                        try:
                            month_data.append(float(month_value))
                            
                        except (ValueError, TypeError):
                        
                        
                            month_data.append(float('0.00'))  
                       
                    Finance_categoryID_ = request.POST.get(f"Finance_categoryID_{x}")
                    
                    if Finance_categoryID_ is not None:
                        Finance_categoryObj = Finance_Category.objects.get(id=Finance_categoryID_,IsDelete=False)
                        EntObj = Entry_Master_Year.objects.get(id=enmaster.pk,IsDelete=False)

                        
                        var = Finance_Category_Entry_Details.objects.create(
                             EntryMaster= EntObj,
                             Finance_Category_Name=Finance_categoryObj,
                           
                            Month_1=Decimal(month_data[0]),
                            Month_2=Decimal(month_data[1]),
                            Month_3=Decimal(month_data[2]),
                            Month_4=Decimal(month_data[3]),
                            Month_5=Decimal(month_data[4]),
                            Month_6=Decimal(month_data[5]),
                            Month_7=Decimal(month_data[6]),
                            Month_8=Decimal(month_data[7]),
                            Month_9=Decimal(month_data[8]),
                            Month_10=Decimal(month_data[9]),
                            Month_11=Decimal(month_data[10]),
                            Month_12=Decimal(month_data[11]),
                            OrganizationID = OrganizationID,
                            CreatedBy = UserID
                        )

            Total_market_segment_category_item = int(request.POST["Total_market_segment_category_item"])

            for x in range(Total_market_segment_category_item + 1):
                    month_data = []
                    for month in months:
                        month_key = f"market_segment_category_{month}_{x}"
                        month_value = request.POST.get(month_key)
                        try:
                            month_data.append(float(month_value))
                        except (ValueError, TypeError):
                            month_data.append(float('0.00'))  
                    
                    market_segment_categoryID_ = request.POST.get(f"market_segment_categoryID_{x}")
                    
                    if market_segment_categoryID_ is not None:
                        Market_Segment_CategoryObj = Market_Segment_Category.objects.get(id=market_segment_categoryID_,IsDelete=False)
                        EntObj = Entry_Master_Year.objects.get(id=enmaster.pk,IsDelete=False)

                        
                        var = Market_Segment_Entry_Details.objects.create(
                            EntryMaster= EntObj,
                            Market_Segment_Category_Name=Market_Segment_CategoryObj,
                           
                            Month_1=Decimal(month_data[0]),
                            Month_2=Decimal(month_data[1]),
                            Month_3=Decimal(month_data[2]),
                            Month_4=Decimal(month_data[3]),
                            Month_5=Decimal(month_data[4]),
                            Month_6=Decimal(month_data[5]),
                            Month_7=Decimal(month_data[6]),
                            Month_8=Decimal(month_data[7]),
                            Month_9=Decimal(month_data[8]),
                            Month_10=Decimal(month_data[9]),
                            Month_11=Decimal(month_data[10]),
                            Month_12=Decimal(month_data[11]),
                            OrganizationID = OrganizationID,
                            CreatedBy = UserID
                        )

            Total_business_source_category_item  =  int(request.POST["Total_business_source_category_item"])

            for x in range(Total_business_source_category_item + 1):
                    month_data = []
                    for month in months:
                        month_key = f"business_source_category_{month}_{x}"
                        month_value = request.POST.get(month_key)
                        try:
                            month_data.append(float(month_value))
                        except (ValueError, TypeError):
                            month_data.append(float('0.00'))  
                    
                    business_source_categoryID_ = request.POST.get(f"business_source_categoryID_{x}")
                    
                    if business_source_categoryID_ is not None:
                        Business_Source_CategoryObj = Business_Source_Category.objects.get(id=business_source_categoryID_,IsDelete=False)
                        EntObj = Entry_Master_Year.objects.get(id=enmaster.pk,IsDelete=False)

                        
                        var = Business_Source_Entry_Details.objects.create(
                            EntryMaster= EntObj,
                            Business_Source_Category_Name=Business_Source_CategoryObj,
                           
                            Month_1=Decimal(month_data[0]),
                            Month_2=Decimal(month_data[1]),
                            Month_3=Decimal(month_data[2]),
                            Month_4=Decimal(month_data[3]),
                            Month_5=Decimal(month_data[4]),
                            Month_6=Decimal(month_data[5]),
                            Month_7=Decimal(month_data[6]),
                            Month_8=Decimal(month_data[7]),
                            Month_9=Decimal(month_data[8]),
                            Month_10=Decimal(month_data[9]),
                            Month_11=Decimal(month_data[10]),
                            Month_12=Decimal(month_data[11]),
                            OrganizationID = OrganizationID,
                            CreatedBy = UserID
                        ) 
            
            
            Total_Expense_item  =  int(request.POST["Total_Expense_item"])
            for x in range(Total_Expense_item + 1):
                                month_data = []
                                for month in months:
                                    month_key = f"Expense_{month}_{x}"
                                    month_value = request.POST.get(month_key)
                                    try:
                                        month_data.append(float(month_value))
                                    except (ValueError, TypeError):
                                        month_data.append(float('0.00'))  
                                
                                ExpenseID_ = request.POST.get(f"ExpenseID_{x}")
                                
                                if ExpenseID_ is not None:
                                    ExpenseObj = ExpensesIncludingPayroll.objects.get(id=ExpenseID_,IsDelete=False)
                                    EntObj = Entry_Master_Year.objects.get(id=enmaster.pk,IsDelete=False)

                                    
                                    var = ExpensesIncludingPayrollEntryDetails.objects.create(
                                        EntryMaster= EntObj,
                                        ExpensesIncludingPayroll=ExpenseObj,
                                    
                                        Month_1=Decimal(month_data[0]),
                                        Month_2=Decimal(month_data[1]),
                                        Month_3=Decimal(month_data[2]),
                                        Month_4=Decimal(month_data[3]),
                                        Month_5=Decimal(month_data[4]),
                                        Month_6=Decimal(month_data[5]),
                                        Month_7=Decimal(month_data[6]),
                                        Month_8=Decimal(month_data[7]),
                                        Month_9=Decimal(month_data[8]),
                                        Month_10=Decimal(month_data[9]),
                                        Month_11=Decimal(month_data[10]),
                                        Month_12=Decimal(month_data[11]),
                                        OrganizationID = OrganizationID,
                                        CreatedBy = UserID
                                    ) 

            Total_CostCover_item  =  int(request.POST["Total_CostCover_item"])
            for x in range(Total_CostCover_item + 1):
                                month_data = []
                                for month in months:
                                    month_key = f"CostCover_{month}_{x}"
                                    month_value = request.POST.get(month_key)
                                    try:
                                        month_data.append(float(month_value))
                                    except (ValueError, TypeError):
                                        month_data.append(float('0.00'))  
                                
                                CostCoverID_ = request.POST.get(f"CostCoverID_{x}")
                                
                                if CostCoverID_ is not None:
                                    CostCoverObj = CostPerCover.objects.get(id=CostCoverID_,IsDelete=False)
                                    EntObj = Entry_Master_Year.objects.get(id=enmaster.pk,IsDelete=False)

                                    
                                    var = CostPerCoverEntryDetails.objects.create(
                                        EntryMaster= EntObj,
                                        CostPerCover=CostCoverObj,
                                    
                                        Month_1=Decimal(month_data[0]),
                                        Month_2=Decimal(month_data[1]),
                                        Month_3=Decimal(month_data[2]),
                                        Month_4=Decimal(month_data[3]),
                                        Month_5=Decimal(month_data[4]),
                                        Month_6=Decimal(month_data[5]),
                                        Month_7=Decimal(month_data[6]),
                                        Month_8=Decimal(month_data[7]),
                                        Month_9=Decimal(month_data[8]),
                                        Month_10=Decimal(month_data[9]),
                                        Month_11=Decimal(month_data[10]),
                                        Month_12=Decimal(month_data[11]),
                                        OrganizationID = OrganizationID,
                                        CreatedBy = UserID
                                    )   

            Total_CostOccupied_item  =  int(request.POST["Total_CostOccupied_item"])

            for x in range(Total_CostOccupied_item + 1):
                                month_data = []
                                for month in months:
                                    month_key = f"CostOccupied_{month}_{x}"
                                    month_value = request.POST.get(month_key)
                                    try:
                                        month_data.append(float(month_value))
                                    except (ValueError, TypeError):
                                        month_data.append(float('0.00'))  
                                
                                CostOccupiedID_ = request.POST.get(f"CostOccupiedID_{x}")
                                
                                if CostOccupiedID_ is not None:
                                    CostPerOccupiedObj = CostPerOccupiedRoomNight.objects.get(id=CostOccupiedID_,IsDelete=False)
                                    EntObj = Entry_Master_Year.objects.get(id=enmaster.pk,IsDelete=False)

                                    
                                    var = CostPerOccupiedRoomNightEntryDetails.objects.create(
                                        EntryMaster= EntObj,
                                        CostPerOccupiedRoomNight=CostPerOccupiedObj,
                                    
                                        Month_1=Decimal(month_data[0]),
                                        Month_2=Decimal(month_data[1]),
                                        Month_3=Decimal(month_data[2]),
                                        Month_4=Decimal(month_data[3]),
                                        Month_5=Decimal(month_data[4]),
                                        Month_6=Decimal(month_data[5]),
                                        Month_7=Decimal(month_data[6]),
                                        Month_8=Decimal(month_data[7]),
                                        Month_9=Decimal(month_data[8]),
                                        Month_10=Decimal(month_data[9]),
                                        Month_11=Decimal(month_data[10]),
                                        Month_12=Decimal(month_data[11]),
                                        OrganizationID = OrganizationID,
                                        CreatedBy = UserID
                                    )                                                 


            # Total_Engineering_item --------------->
            Total_Engineering_item = int(request.POST["Total_Engineering_item"])

            for x in range(Total_Engineering_item + 1):
                    month_data = []
                    for month in months:
                        month_key = f"Engineering_Category_{month}_{x}"
                        month_value = request.POST.get(month_key)
                        try:
                            month_data.append(float(month_value))
                        except (ValueError, TypeError):
                            month_data.append(float('0.00'))  
                    
                    Engineering_categoryID_ = request.POST.get(f"Engineering_categoryID_{x}")
                    
                    if Engineering_categoryID_ is not None:
                        Engineering_CategoryObj = Engineering_Category.objects.get(id=Engineering_categoryID_,IsDelete=False)
                        EntObj = Entry_Master_Year.objects.get(id=enmaster.pk,IsDelete=False)

                        
                        var = Engineering_Category_Entry_Details.objects.create(
                            EntryMaster= EntObj,
                            Engineering_Category_Name=Engineering_CategoryObj,
                           
                            Month_1=Decimal(month_data[0]),
                            Month_2=Decimal(month_data[1]),
                            Month_3=Decimal(month_data[2]),
                            Month_4=Decimal(month_data[3]),
                            Month_5=Decimal(month_data[4]),
                            Month_6=Decimal(month_data[5]),
                            Month_7=Decimal(month_data[6]),
                            Month_8=Decimal(month_data[7]),
                            Month_9=Decimal(month_data[8]),
                            Month_10=Decimal(month_data[9]),
                            Month_11=Decimal(month_data[10]),
                            Month_12=Decimal(month_data[11]),
                            OrganizationID = OrganizationID,
                            CreatedBy = UserID
                        )

            
            messages.success(request,"Your information has been successfully submitted.")
            return redirect('/YearlyBudget/YearlyBudget_list?I='+str(I))

        
    today = datetime.date.today()
    CYear = today.year+1 
   
    

    context =  {'memOrg':memOrg ,
                'OrganizationID':OrganizationID,
                'CYear':range(CYear,2020,-1),
                'finance_category':finance_category,
                'engineering_category':engineering_category,
                'business_source_category':business_source_category,
                'market_segment_category':market_segment_category,
                'Expenses':Expenses,
                'CostCover':CostCover,
                'CostOccupied':CostOccupied,
                'EntryYear':EntryYear,'I':I
                } 
   
    return render(request, "YearlyBudget/YearlyBudget_Entry.html",context)
    

def  YearlyBudget_View(request,id):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])

    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
        'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = f"https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID="+str(OrganizationID)

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")


    entry_master_year_instance = Entry_Master_Year.objects.get(id=id)
    organization_id = entry_master_year_instance.OrganizationID
    entry_year =  entry_master_year_instance.EntryYear
  

    
    finance_details = Finance_Category_Entry_Details.objects.filter(EntryMaster = id ,IsDelete=False).values('Finance_Category_Name__Finance_category').annotate(
        Sum_Month_1=Sum('Month_1'),
        Sum_Month_2=Sum('Month_2'),
        Sum_Month_3=Sum('Month_3'),
        Sum_Month_4=Sum('Month_4'),
        Sum_Month_5=Sum('Month_5'),
        Sum_Month_6=Sum('Month_6'),
        Sum_Month_7=Sum('Month_7'),
        Sum_Month_8=Sum('Month_8'),
        Sum_Month_9=Sum('Month_9'),
        Sum_Month_10=Sum('Month_10'),
        Sum_Month_11=Sum('Month_11'),
        Sum_Month_12=Sum('Month_12'),
        YTD=Sum('Month_12'),
    ).order_by('Finance_Category_Name__id') 
    
    for m in finance_details:
        if m['Finance_Category_Name__Finance_category'] == "Occupancy" or m['Finance_Category_Name__Finance_category'] == "Rooms Profitability" or m['Finance_Category_Name__Finance_category'] == "F&B Profitability" or m['Finance_Category_Name__Finance_category'] == "GOP":
            count = 0
            for i in range(1, 13):
                if m[f'Sum_Month_{i}'] > 0:
                    count += 1
            
            if count > 0:
                val = m['Sum_Month_1'] + m['Sum_Month_2'] + m['Sum_Month_3'] + m['Sum_Month_4'] + m['Sum_Month_5'] + m['Sum_Month_6'] + m['Sum_Month_7'] + m['Sum_Month_8'] + m['Sum_Month_9'] + m['Sum_Month_10'] + m['Sum_Month_11'] + m['Sum_Month_12']
                val = val / count
                m['YTD'] = val
            else:
                m['YTD'] = 0
        else:
            m['YTD'] = m['Sum_Month_1'] + m['Sum_Month_2'] + m['Sum_Month_3'] + m['Sum_Month_4'] + m['Sum_Month_5'] + m['Sum_Month_6'] + m['Sum_Month_7'] + m['Sum_Month_8'] + m['Sum_Month_9'] + m['Sum_Month_10'] + m['Sum_Month_11'] + m['Sum_Month_12']

        
        
             
        
    
    market_segment_category_details = Market_Segment_Entry_Details.objects.filter(EntryMaster = id ,IsDelete=False).values('Market_Segment_Category_Name__market_segment_category').annotate(
        Sum_Month_1=Sum('Month_1'),
        Sum_Month_2=Sum('Month_2'),
        Sum_Month_3=Sum('Month_3'),
        Sum_Month_4=Sum('Month_4'),
        Sum_Month_5=Sum('Month_5'),
        Sum_Month_6=Sum('Month_6'),
        Sum_Month_7=Sum('Month_7'),
        Sum_Month_8=Sum('Month_8'),
        Sum_Month_9=Sum('Month_9'),
        Sum_Month_10=Sum('Month_10'),
        Sum_Month_11=Sum('Month_11'),
        Sum_Month_12=Sum('Month_12')
    ).order_by('Market_Segment_Category_Name__id')    
    
    business_source_category_details = Business_Source_Entry_Details.objects.filter(EntryMaster = id ,IsDelete=False).values('Business_Source_Category_Name__business_source_category').annotate(
        Sum_Month_1=Sum('Month_1'),
        Sum_Month_2=Sum('Month_2'),
        Sum_Month_3=Sum('Month_3'),
        Sum_Month_4=Sum('Month_4'),
        Sum_Month_5=Sum('Month_5'),
        Sum_Month_6=Sum('Month_6'),
        Sum_Month_7=Sum('Month_7'),
        Sum_Month_8=Sum('Month_8'),
        Sum_Month_9=Sum('Month_9'),
        Sum_Month_10=Sum('Month_10'),
        Sum_Month_11=Sum('Month_11'),
        Sum_Month_12=Sum('Month_12')
    ).order_by('Business_Source_Category_Name__id')
    Expenes = ExpensesIncludingPayrollEntryDetails.objects.filter(EntryMaster = id ,IsDelete=False).values('ExpensesIncludingPayroll__Title').annotate(
        Sum_Month_1=Sum('Month_1'),
        Sum_Month_2=Sum('Month_2'),
        Sum_Month_3=Sum('Month_3'),
        Sum_Month_4=Sum('Month_4'),
        Sum_Month_5=Sum('Month_5'),
        Sum_Month_6=Sum('Month_6'),
        Sum_Month_7=Sum('Month_7'),
        Sum_Month_8=Sum('Month_8'),
        Sum_Month_9=Sum('Month_9'),
        Sum_Month_10=Sum('Month_10'),
        Sum_Month_11=Sum('Month_11'),
        Sum_Month_12=Sum('Month_12')
    ).order_by('ExpensesIncludingPayroll__id')
    CostPer = CostPerCoverEntryDetails.objects.filter(EntryMaster = id ,IsDelete=False).values('CostPerCover__Title').annotate(
        Sum_Month_1=Sum('Month_1'),
        Sum_Month_2=Sum('Month_2'),
        Sum_Month_3=Sum('Month_3'),
        Sum_Month_4=Sum('Month_4'),
        Sum_Month_5=Sum('Month_5'),
        Sum_Month_6=Sum('Month_6'),
        Sum_Month_7=Sum('Month_7'),
        Sum_Month_8=Sum('Month_8'),
        Sum_Month_9=Sum('Month_9'),
        Sum_Month_10=Sum('Month_10'),
        Sum_Month_11=Sum('Month_11'),
        Sum_Month_12=Sum('Month_12')
    ).order_by('CostPerCover__id')
    CostOccupied = CostPerOccupiedRoomNightEntryDetails.objects.filter(EntryMaster = id ,IsDelete=False).values('CostPerOccupiedRoomNight__Title').annotate(
        Sum_Month_1=Sum('Month_1'),
        Sum_Month_2=Sum('Month_2'),
        Sum_Month_3=Sum('Month_3'),
        Sum_Month_4=Sum('Month_4'),
        Sum_Month_5=Sum('Month_5'),
        Sum_Month_6=Sum('Month_6'),
        Sum_Month_7=Sum('Month_7'),
        Sum_Month_8=Sum('Month_8'),
        Sum_Month_9=Sum('Month_9'),
        Sum_Month_10=Sum('Month_10'),
        Sum_Month_11=Sum('Month_11'),
        Sum_Month_12=Sum('Month_12')
    ).order_by('CostPerOccupiedRoomNight__id')

    context= {'finance_details':finance_details,'market_segment_category_details':market_segment_category_details,'business_source_category_details':business_source_category_details,'organization_id':organization_id,'entry_year':entry_year,'memOrg':memOrg,'Expenes':Expenes,'CostPer':CostPer,'CostOccupied':CostOccupied}    
    return render(request,"YearlyBudget/YearlyBudget_View.html",context)