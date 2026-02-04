from datetime import date
from django.db import models


   
class  PLUtilitiesMaster(models.Model):
    title = models.CharField(max_length = 200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
            
class PLUtilitiesEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    TotalAmount  = models.DecimalField(decimal_places=2,max_digits=12 )
    IsDelete = models.BooleanField(default=False)
         
class PLUtilitiesEntryDetails(models.Model):
    PLUtilitiesMaster =models.ForeignKey(PLUtilitiesMaster, on_delete=models.CASCADE)
    PLUtilitiesEntryMaster =models.ForeignKey(PLUtilitiesEntryMaster, on_delete=models.CASCADE)
    PLUtilities_Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
      
   
class PL_Engineering_Master(models.Model):
    title = models.CharField(max_length =  200 , blank=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
   
class PL_Engineering_Entry_Master(models.Model):
    EntryMonth =models.BigIntegerField(default=0, blank=True )
    EntryYear =models.BigIntegerField(default=0, blank=True)
    SalaryAndWages = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses_and_Incentives = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    PayrollRelatedExpenses =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    PayrollAndRelatedExpenses = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Total_Other_Expenses = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    TotalExpenses = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)  
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class PL_Engineering_EntryDetails(models.Model):
    PL_Engineering_Master =models.ForeignKey(PL_Engineering_Master, on_delete=models.CASCADE,blank=True)
    PL_Engineering_Entry_Master =models.ForeignKey(PL_Engineering_Entry_Master, on_delete=models.CASCADE,blank=True)
    PL_Engineering_Amount = models.DecimalField(decimal_places=2,max_digits=12,default=0,null=True,blank=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
    
class SM_SalesExpenseMaster(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class SM_MarketingExpenseMaster(models.Model):
    Mtitle = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
    
  
class SM_SaleMarketingEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    SalaryAndWages = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True)
    Total_Sales_Expenses =  models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True)
    Total_Marketing_Expenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True)
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    TotalExpenses = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
  
     
class SM_SalesEntryDetails(models.Model):
    SM_SalesExpenseMaster =models.ForeignKey(SM_SalesExpenseMaster, on_delete=models.CASCADE)
    SM_SaleMarketingEntryMaster =models.ForeignKey(SM_SaleMarketingEntryMaster, on_delete=models.CASCADE)
    AmountSales = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
        
class SM_MarketingEntryDetails(models.Model):
    SM_MarketingExpenseMaster =models.ForeignKey(SM_MarketingExpenseMaster, on_delete=models.CASCADE)
    SM_SaleMarketingEntryMaster =models.ForeignKey(SM_SaleMarketingEntryMaster, on_delete=models.CASCADE)
    AmountMarketing = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    

  
class ItServiceMaster(models.Model):
    title_1 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class ItSystemExpenseMaster(models.Model):
    title_2 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
        
class ItOtherExpenseMaster(models.Model):
    title_3 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class IT_EntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    Total_Cost_Of_Services =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    SalaryAndWages = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True)
    Total_System_Expenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True)
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    TotalExpenses = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
 
class It_ServiceEntryDetails(models.Model):
    ItServiceMaster =models.ForeignKey(ItServiceMaster, on_delete=models.CASCADE)
    IT_EntryMaster =models.ForeignKey( IT_EntryMaster, on_delete=models.CASCADE)
    AmountServices = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)    
        
class It_SystemExpenseEntryDetails(models.Model):
    ItSystemExpenseMaster =models.ForeignKey(ItSystemExpenseMaster, on_delete=models.CASCADE)
    IT_EntryMaster =models.ForeignKey( IT_EntryMaster, on_delete=models.CASCADE)
    AmountSystemExpense = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
            
class It_OtherExpenseEntryDetails(models.Model):
    ItOtherExpenseMaster =models.ForeignKey(ItOtherExpenseMaster, on_delete=models.CASCADE)
    IT_EntryMaster =models.ForeignKey( IT_EntryMaster, on_delete=models.CASCADE)
    AmountOtherExpense = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
    
class AG_SecurityMaster(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
      
class AG_SecurityEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    SalaryAndWages = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0 ,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places = 2 , max_digits = 12)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places = 2 , max_digits = 12)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places = 2, max_digits = 12)
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places = 2, max_digits = 12)
    TotalExpenses = models.DecimalField(default = 0 ,  decimal_places = 2, max_digits = 12)   
    OrganizationID = models.BigIntegerField(default=0 )
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class AG_SecurityEntryDetails(models.Model):
    AG_SecurityMaster =models.ForeignKey(AG_SecurityMaster, on_delete=models.CASCADE)
    AG_SecurityEntryMaster =models.ForeignKey(AG_SecurityEntryMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
    
class AG_HRMaster(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)  
        
class AG_HREntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    SalaryAndWages = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True)
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    TotalExpenses = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
      
class AG_HREntryDetails(models.Model):
    AG_HRMaster =models.ForeignKey(AG_HRMaster, on_delete=models.CASCADE)
    AG_HREntryMaster =models.ForeignKey(AG_HREntryMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
    
class AG_Analysis_Master(models.Model):
    title_1 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
        
class AG_AnalysisEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    SalaryAndWages = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True)
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    TotalExpenses = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
              
class AG_AnalysisEntryDetail(models.Model):
    AG_Analysis_Master =models.ForeignKey(AG_Analysis_Master, on_delete=models.CASCADE)
    AG_AnalysisEntryMaster =models.ForeignKey( AG_AnalysisEntryMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
class Total_AG_Master(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)  
    
class Total_AGEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    SalaryAndWages = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True)
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    TotalExpenses = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class Total_AGEntryDetails(models.Model):
    Total_AG_Master =models.ForeignKey(Total_AG_Master, on_delete=models.CASCADE)
    Total_AGEntryMaster =models.ForeignKey(Total_AGEntryMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
 
class Rental_Other_IncomeMaster(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
             
class Rental_Other_IncomeEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    Rental_And_OtherIncome = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)     
  
class Rental_Other_IncomeEntryDetail(models.Model):
    Rental_Other_IncomeMaster =models.ForeignKey(Rental_Other_IncomeMaster, on_delete=models.CASCADE)
    Rental_Other_IncomeEntryMaster =models.ForeignKey(Rental_Other_IncomeEntryMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    


 
class MinorGuestMaster(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
                        
class MinorGuestEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    LocalCallRevenue = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    LongDistanceCallRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    InternetRevenue = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    OtherMisRevenue = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TelecommunicationRevenueOthers = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)
    TelecommunicationRevenue = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    SalaryAndWages = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True)
    Total_Cost_Sales = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    DepartmentIncomeLoss = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)     
   
class MinorGuestEntryDetail(models.Model):
    MinorGuestMaster =models.ForeignKey(MinorGuestMaster, on_delete=models.CASCADE)
    MinorGuestEntryMaster =models.ForeignKey(MinorGuestEntryMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    

class OODBusinessMaster(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
                            
class OODBusinessEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    TelephoneAndFax = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    InternetCharge =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    Photocopy = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    EuipmentRental = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    MeetingRoomRental = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)
    BusinessCentreSales = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    BusinessCentreRevenueOther =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    BusinessCentreRevenue  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    CostOfBusinessCentre =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    Total_Cost_Sales = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    GrossProfit = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    SalaryAndWages = models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True)
    TotalOtherExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True)
    TotalExpenses =  models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True)
    DepartmentIncomeLoss = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)     
    
class OODBusinessEntryDetail(models.Model):
    OODBusinessMaster =models.ForeignKey(OODBusinessMaster, on_delete=models.CASCADE)
    OODBusinessEntryMaster =models.ForeignKey(OODBusinessEntryMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
 
class OOD_LaundryMaster(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
                     
class OOD_LaundryEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    Dry_CleaningServices = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    LaundryServices =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    PressingServices =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    GuestLaundryRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    Cost_OfLaundryServices =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    Total_CostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    Gross_Profit =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalaryAndWages =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses_and_Incentives= models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True) 
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    TotalExpenses = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    DepartmentIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)     
 
class OOD_LaundryEntryDetail(models.Model):
    OOD_LaundryMaster =models.ForeignKey(OOD_LaundryMaster, on_delete=models.CASCADE)
    OOD_LaundryEntryMaster =models.ForeignKey(OOD_LaundryEntryMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    

class OOD_TransportMaster(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class OOD_TransportEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    InHouseLimousineRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    ExternalLimousineRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    GuestTransportationRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    GuestTransportRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    Cost_OfGuestTransportation =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    Total_CostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    Gross_Profit =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalaryAndWages =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses_and_Incentives= models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True) 
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    TotalExpenses = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    DepartmentIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)     
    
class OOD_TransportEntryDetail(models.Model):
    OOD_TransportMaster =models.ForeignKey(OOD_TransportMaster, on_delete=models.CASCADE)
    OOD_TransportEntryMaster =models.ForeignKey(OOD_TransportEntryMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    

class OOD_HealthMaster(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)    
  
class OOD_HealthEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    FitnessLessonRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    MassageRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SpaTreatmentRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalonTreatmentRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    MerchandiseRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    HealthWellnessRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    HealthClubSpaRevenueOther =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    HealthClubSpaRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    HealthClubAndSpaRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    Cost_OfMerchandise =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    Total_CostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    Gross_Profit =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalaryAndWages =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses_and_Incentives= models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True) 
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    TotalExpenses = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    DepartmentIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)     
    
class OOD_HealthEntryDetail(models.Model):
    OOD_HealthMaster =models.ForeignKey(OOD_HealthMaster, on_delete=models.CASCADE)
    OOD_HealthEntryMaster =models.ForeignKey(OOD_HealthEntryMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    


    

class FB_ODCMaster(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FoodRevenueMaster(models.Model):
    title1 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class BeverageRevenueMaster(models.Model):
    title2 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   

class TotalOtherIncomeMaster(models.Model):
    title3 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FB_ODCEntryMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    FoodRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    BeverageRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalOtherIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FoodCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    BeverageCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfFbSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    AudioVisualEquipmentCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBOtherCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfOtherRev =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)     
    Gross_Profit =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalaryAndWages =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True) 
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    DepartmentIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
    
class FB_ODCEntryDetail(models.Model):
    FB_ODCMaster =models.ForeignKey(FB_ODCMaster, on_delete=models.CASCADE)
    FB_ODCEntryMaster =models.ForeignKey(FB_ODCEntryMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class FoodRevenueEntryDetail(models.Model):
    FoodRevenueMaster =models.ForeignKey(FoodRevenueMaster, on_delete=models.CASCADE)
    FB_ODCEntryMaster =models.ForeignKey(FB_ODCEntryMaster, on_delete=models.CASCADE)
    Amount1 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
 
class BeverageRevenueEntryDetail(models.Model):
    BeverageRevenueMaster =models.ForeignKey(BeverageRevenueMaster, on_delete=models.CASCADE)
    FB_ODCEntryMaster =models.ForeignKey(FB_ODCEntryMaster, on_delete=models.CASCADE)
    Amount2 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)    

class TotalOtherIncomeEntryDetail(models.Model):
    TotalOtherIncomeMaster =models.ForeignKey(TotalOtherIncomeMaster, on_delete=models.CASCADE)
    FB_ODCEntryMaster =models.ForeignKey(FB_ODCEntryMaster, on_delete=models.CASCADE)
    Amount3 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
 
    
    
    
class FoodRevenueBanquet_Master(models.Model):
    title1 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class BeverageRevenueBanquet_Master(models.Model):
    title2 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   

class FBBanquet_Master(models.Model):
    title3 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FBBanquet_EnrtyMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    FoodRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    BeverageRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    RoomHireRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    AudioVisualRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    ServiceChargeRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBRevenueOthers  = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalOtherIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FoodCostOfSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    BeverageCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfFbSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    AudioVisualEquipmentCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBOtherCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfOtherRev =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    TotalCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    Gross_Profit =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalaryAndWages =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses_and_Incentives  = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True) 
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    DepartmentIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
        
class FoodRevenueBanquet_EntryDetail(models.Model):
    FoodRevenueBanquet_Master =models.ForeignKey(FoodRevenueBanquet_Master, on_delete=models.CASCADE)
    FBBanquet_EnrtyMaster =models.ForeignKey(FBBanquet_EnrtyMaster, on_delete=models.CASCADE)
    Amount1 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
     
class BeverageRevenueBanquet_EntryDetail(models.Model):
    BeverageRevenueBanquet_Master =models.ForeignKey(BeverageRevenueBanquet_Master, on_delete=models.CASCADE)
    FBBanquet_EnrtyMaster =models.ForeignKey(FBBanquet_EnrtyMaster, on_delete=models.CASCADE)
    Amount2 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)    
    
class FBBanquet_EntryDetail(models.Model):
    FBBanquet_Master =models.ForeignKey(FBBanquet_Master, on_delete=models.CASCADE)
    FBBanquet_EnrtyMaster =models.ForeignKey(FBBanquet_EnrtyMaster, on_delete=models.CASCADE)
    Amount3 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    

    
class FB_MiniBar_Master(models.Model):
    title1 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
     
class FB_MiniBar_FoodRevenue_Master(models.Model):
    title2 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FB_MiniBar_TotalOtherIncome_Master(models.Model):
    title3 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FB_MiniBar_EnrtyMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    FoodRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    MiniBarRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    BeverageRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    RoomHireRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    AudioVisualRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    ServiceChargeRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBRevenueOthers  = models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalOtherIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FoodCostOfSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    BeverageCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfFbSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    AudioVisualEquipmentCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBOtherCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfOtherRev =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    TotalCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    Gross_Profit =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalaryAndWages =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses_and_Incentives  = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True) 
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    DepartmentIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
        
class FB_MiniBar_EntryDetail(models.Model):
    FB_MiniBar_Master =models.ForeignKey(FB_MiniBar_Master, on_delete=models.CASCADE)
    FB_MiniBar_EnrtyMaster =models.ForeignKey(FB_MiniBar_EnrtyMaster, on_delete=models.CASCADE)
    Amount1 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
           
class FB_MiniBar_FoodRevenue_EntryDetail(models.Model):
    FB_MiniBar_FoodRevenue_Master =models.ForeignKey(FB_MiniBar_FoodRevenue_Master, on_delete=models.CASCADE)
    FB_MiniBar_EnrtyMaster =models.ForeignKey(FB_MiniBar_EnrtyMaster, on_delete=models.CASCADE)
    Amount2 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
         
class FB_MiniBar_TotalOtherIncome_EntryDetail(models.Model):
    FB_MiniBar_TotalOtherIncome_Master =models.ForeignKey(FB_MiniBar_TotalOtherIncome_Master, on_delete=models.CASCADE)
    FB_MiniBar_EnrtyMaster =models.ForeignKey(FB_MiniBar_EnrtyMaster, on_delete=models.CASCADE)
    Amount3 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
    
    
class FBIRD_Master(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FBIRD_FoodRevenue_Master(models.Model):
    title1 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FBIRD_BeverageRevenue_Master(models.Model):
    title2 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
    
class FBIRD_TotalOtherIncome_Master(models.Model):
    title3 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class FB_IRD_EnrtyMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    FoodRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    BeverageRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalOtherIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FoodCostOfSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    BeverageCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfFbSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    AudioVisualEquipmentCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBOtherCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfOtherRev =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    TotalCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    Gross_Profit =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalaryAndWages =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses_and_Incentives  = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True) 
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    DepartmentIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
        
        
class FB_IRD_EntryDetail(models.Model):
    FBIRD_Master =models.ForeignKey(FBIRD_Master, on_delete=models.CASCADE)
    FB_IRD_EnrtyMaster =models.ForeignKey(FB_IRD_EnrtyMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
           
class FB_IRD_FoodRevenue_EntryDetail(models.Model):
    FBIRD_FoodRevenue_Master =models.ForeignKey(FBIRD_FoodRevenue_Master, on_delete=models.CASCADE)
    FB_IRD_EnrtyMaster =models.ForeignKey(FB_IRD_EnrtyMaster, on_delete=models.CASCADE)
    Amount1 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
         
class FBIRD_BeverageRevenue_Maste_EntryDetail(models.Model):
    FBIRD_BeverageRevenue_Master =models.ForeignKey(FBIRD_BeverageRevenue_Master, on_delete=models.CASCADE)
    FB_IRD_EnrtyMaster =models.ForeignKey(FB_IRD_EnrtyMaster, on_delete=models.CASCADE)
    Amount2 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
        
class FBIRD_TotalOtherIncome_MasterIncome_EntryDetail(models.Model):
    FBIRD_TotalOtherIncome_Master =models.ForeignKey( FBIRD_TotalOtherIncome_Master, on_delete=models.CASCADE)
    FB_IRD_EnrtyMaster =models.ForeignKey(FB_IRD_EnrtyMaster, on_delete=models.CASCADE)
    Amount3 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
    
   
   
class Outlet1_Master(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class Outlet1_FoodRevenue_Master(models.Model):
    title1 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class  Outlet1_BeverageRevenue_Master(models.Model):
    title2 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
    
class  Outlet1_TotalOtherIncome_Master(models.Model):
    title3 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class Outlet1_EnrtyMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    FoodRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    BeverageRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalOtherIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FoodCostOfSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    BeverageCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfFbSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    AudioVisualEquipmentCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBOtherCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfOtherRev =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    TotalCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    Gross_Profit =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalaryAndWages =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses_and_Incentives  = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True) 
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    DepartmentIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
        
        
class Outlet1_EntryDetail(models.Model):
    Outlet1_Master =models.ForeignKey(Outlet1_Master, on_delete=models.CASCADE)
    Outlet1_EnrtyMaster =models.ForeignKey(Outlet1_EnrtyMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
           
class Outlet1_FoodRevenue_EntryDetail(models.Model):
    Outlet1_FoodRevenue_Master =models.ForeignKey(Outlet1_FoodRevenue_Master, on_delete=models.CASCADE)
    Outlet1_EnrtyMaster =models.ForeignKey(Outlet1_EnrtyMaster, on_delete=models.CASCADE)
    Amount1 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
         
class Outlet1_BeverageRevenue_Maste_EntryDetail(models.Model):
    Outlet1_BeverageRevenue_Master =models.ForeignKey(Outlet1_BeverageRevenue_Master, on_delete=models.CASCADE)
    Outlet1_EnrtyMaster =models.ForeignKey(Outlet1_EnrtyMaster, on_delete=models.CASCADE)
    Amount2 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
        
class Outlet1_TotalOtherIncome_MasterIncome_EntryDetail(models.Model):
    Outlet1_TotalOtherIncome_Master =models.ForeignKey( Outlet1_TotalOtherIncome_Master, on_delete=models.CASCADE)
    Outlet1_EnrtyMaster =models.ForeignKey(Outlet1_EnrtyMaster, on_delete=models.CASCADE)
    Amount3 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
    


   
   
class Outlet2_Master(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class Outlet2_FoodRevenue_Master(models.Model):
    title1 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class  Outlet2_BeverageRevenue_Master(models.Model):
    title2 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
    
class  Outlet2_TotalOtherIncome_Master(models.Model):
    title3 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class Outlet2_EnrtyMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    FoodRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    BeverageRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalOtherIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FoodCostOfSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    BeverageCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfFbSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    AudioVisualEquipmentCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBOtherCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfOtherRev =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    TotalCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    Gross_Profit =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalaryAndWages =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses_and_Incentives  = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True) 
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    DepartmentIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
        
        
class Outlet2_EntryDetail(models.Model):
    Outlet2_Master =models.ForeignKey(Outlet2_Master, on_delete=models.CASCADE)
    Outlet2_EnrtyMaster =models.ForeignKey(Outlet2_EnrtyMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
           
class Outlet2_FoodRevenue_EntryDetail(models.Model):
    Outlet2_FoodRevenue_Master =models.ForeignKey(Outlet2_FoodRevenue_Master, on_delete=models.CASCADE)
    Outlet2_EnrtyMaster =models.ForeignKey(Outlet2_EnrtyMaster, on_delete=models.CASCADE)
    Amount1 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
         
class Outlet2_BeverageRevenue_Maste_EntryDetail(models.Model):
    Outlet2_BeverageRevenue_Master =models.ForeignKey(Outlet2_BeverageRevenue_Master, on_delete=models.CASCADE)
    Outlet2_EnrtyMaster =models.ForeignKey(Outlet2_EnrtyMaster, on_delete=models.CASCADE)
    Amount2 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
        
class Outlet2_TotalOtherIncome_MasterIncome_EntryDetail(models.Model):
    Outlet2_TotalOtherIncome_Master =models.ForeignKey( Outlet2_TotalOtherIncome_Master, on_delete=models.CASCADE)
    Outlet2_EnrtyMaster =models.ForeignKey(Outlet2_EnrtyMaster, on_delete=models.CASCADE)
    Amount3 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
   



   
class Outlet3_Master(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class Outlet3_FoodRevenue_Master(models.Model):
    title1 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class  Outlet3_BeverageRevenue_Master(models.Model):
    title2 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
    
class  Outlet3_TotalOtherIncome_Master(models.Model):
    title3 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class Outlet3_EnrtyMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    FoodRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    BeverageRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalOtherIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FoodCostOfSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    BeverageCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfFbSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    AudioVisualEquipmentCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBOtherCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfOtherRev =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    TotalCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    Gross_Profit =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalaryAndWages =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses_and_Incentives  = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True) 
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    DepartmentIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
        
        
class Outlet3_EntryDetail(models.Model):
    Outlet3_Master =models.ForeignKey(Outlet3_Master, on_delete=models.CASCADE)
    Outlet3_EnrtyMaster =models.ForeignKey(Outlet3_EnrtyMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
           
class Outlet3_FoodRevenue_EntryDetail(models.Model):
    Outlet3_FoodRevenue_Master =models.ForeignKey(Outlet3_FoodRevenue_Master, on_delete=models.CASCADE)
    Outlet3_EnrtyMaster =models.ForeignKey(Outlet3_EnrtyMaster, on_delete=models.CASCADE)
    Amount1 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
         
class Outlet3_BeverageRevenue_Maste_EntryDetail(models.Model):
    Outlet3_BeverageRevenue_Master =models.ForeignKey(Outlet3_BeverageRevenue_Master, on_delete=models.CASCADE)
    Outlet3_EnrtyMaster =models.ForeignKey(Outlet3_EnrtyMaster, on_delete=models.CASCADE)
    Amount2 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
        
class Outlet3_TotalOtherIncome_MasterIncome_EntryDetail(models.Model):
    Outlet3_TotalOtherIncome_Master =models.ForeignKey( Outlet3_TotalOtherIncome_Master, on_delete=models.CASCADE)
    Outlet3_EnrtyMaster =models.ForeignKey(Outlet3_EnrtyMaster, on_delete=models.CASCADE)
    Amount3 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)    
   
   
   
   
   
class Outlet4_Master(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class Outlet4_FoodRevenue_Master(models.Model):
    title1 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class  Outlet4_BeverageRevenue_Master(models.Model):
    title2 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
    
class  Outlet4_TotalOtherIncome_Master(models.Model):
    title3 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class Outlet4_EnrtyMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    FoodRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    BeverageRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalOtherIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FoodCostOfSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    BeverageCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfFbSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    AudioVisualEquipmentCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBOtherCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfOtherRev =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    TotalCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    Gross_Profit =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalaryAndWages =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses_and_Incentives  = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True) 
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    DepartmentIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
        
        
class Outlet4_EntryDetail(models.Model):
    Outlet4_Master =models.ForeignKey(Outlet4_Master, on_delete=models.CASCADE)
    Outlet4_EnrtyMaster =models.ForeignKey(Outlet4_EnrtyMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
           
class Outlet4_FoodRevenue_EntryDetail(models.Model):
    Outlet4_FoodRevenue_Master =models.ForeignKey(Outlet4_FoodRevenue_Master, on_delete=models.CASCADE)
    Outlet4_EnrtyMaster =models.ForeignKey(Outlet4_EnrtyMaster, on_delete=models.CASCADE)
    Amount1 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
         
class Outlet4_BeverageRevenue_Maste_EntryDetail(models.Model):
    Outlet4_BeverageRevenue_Master =models.ForeignKey(Outlet4_BeverageRevenue_Master, on_delete=models.CASCADE)
    Outlet4_EnrtyMaster =models.ForeignKey(Outlet4_EnrtyMaster, on_delete=models.CASCADE)
    Amount2 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
        
class Outlet4_TotalOtherIncome_MasterIncome_EntryDetail(models.Model):
    Outlet4_TotalOtherIncome_Master =models.ForeignKey( Outlet4_TotalOtherIncome_Master, on_delete=models.CASCADE)
    Outlet4_EnrtyMaster =models.ForeignKey(Outlet4_EnrtyMaster, on_delete=models.CASCADE)
    Amount3 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
   
   
   


  
   
class Outlet5_Master(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class Outlet5_FoodRevenue_Master(models.Model):
    title1 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class  Outlet5_BeverageRevenue_Master(models.Model):
    title2 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
    
class  Outlet5_TotalOtherIncome_Master(models.Model):
    title3 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class Outlet5_EnrtyMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    FoodRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    BeverageRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalOtherIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FoodCostOfSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    BeverageCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfFbSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    AudioVisualEquipmentCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBOtherCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfOtherRev =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    TotalCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    Gross_Profit =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalaryAndWages =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses_and_Incentives  = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True) 
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    DepartmentIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
        
        
class Outlet5_EntryDetail(models.Model):
    Outlet5_Master =models.ForeignKey(Outlet5_Master, on_delete=models.CASCADE)
    Outlet5_EnrtyMaster =models.ForeignKey(Outlet5_EnrtyMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
           
class Outlet5_FoodRevenue_EntryDetail(models.Model):
    Outlet5_FoodRevenue_Master =models.ForeignKey(Outlet5_FoodRevenue_Master, on_delete=models.CASCADE)
    Outlet5_EnrtyMaster =models.ForeignKey(Outlet5_EnrtyMaster, on_delete=models.CASCADE)
    Amount1 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
         
class Outlet5_BeverageRevenue_Maste_EntryDetail(models.Model):
    Outlet5_BeverageRevenue_Master =models.ForeignKey(Outlet5_BeverageRevenue_Master, on_delete=models.CASCADE)
    Outlet5_EnrtyMaster =models.ForeignKey(Outlet5_EnrtyMaster, on_delete=models.CASCADE)
    Amount2 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
        
class Outlet5_TotalOtherIncome_MasterIncome_EntryDetail(models.Model):
    Outlet5_TotalOtherIncome_Master =models.ForeignKey( Outlet5_TotalOtherIncome_Master, on_delete=models.CASCADE)
    Outlet5_EnrtyMaster =models.ForeignKey(Outlet5_EnrtyMaster, on_delete=models.CASCADE)
    Amount3 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
   
   

  
   
class PL_FB_Master(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class PL_FB_FoodRevenue_Master(models.Model):
    title1 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class  PL_FB_BeverageRevenue_Master(models.Model):
    title2 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
    
class  PL_FB_TotalOtherIncome_Master(models.Model):
    title3 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class PL_FB_EnrtyMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    FoodRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    BeverageRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalOtherIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FoodCostOfSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    BeverageCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfFbSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    AudioVisualEquipmentCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBOtherCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfOtherRev =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    TotalCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    Gross_Profit =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalaryAndWages =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses_and_Incentives  = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True) 
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    DepartmentIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
        
        
class PL_FB_EntryDetail(models.Model):
    PL_FB_Master =models.ForeignKey(PL_FB_Master, on_delete=models.CASCADE)
    PL_FB_EnrtyMaster =models.ForeignKey(PL_FB_EnrtyMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
           
class PL_FB_FoodRevenue_EntryDetail(models.Model):
    PL_FB_FoodRevenue_Master =models.ForeignKey(PL_FB_FoodRevenue_Master, on_delete=models.CASCADE)
    PL_FB_EnrtyMaster =models.ForeignKey(PL_FB_EnrtyMaster, on_delete=models.CASCADE)
    Amount1 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
         
class PL_FB_BeverageRevenue_Maste_EntryDetail(models.Model):
    PL_FB_BeverageRevenue_Master =models.ForeignKey(PL_FB_BeverageRevenue_Master, on_delete=models.CASCADE)
    PL_FB_EnrtyMaster =models.ForeignKey(PL_FB_EnrtyMaster, on_delete=models.CASCADE)
    Amount2 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
        
class PL_FB_TotalOtherIncome_MasterIncome_EntryDetail(models.Model):
    PL_FB_TotalOtherIncome_Master =models.ForeignKey( PL_FB_TotalOtherIncome_Master, on_delete=models.CASCADE)
    PL_FB_EnrtyMaster =models.ForeignKey(PL_FB_EnrtyMaster, on_delete=models.CASCADE)
    Amount3 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
     
   
class Total_FB_Master(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class Total_FB_FoodRevenue_Master(models.Model):
    title1 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class  Total_FB_BeverageRevenue_Master(models.Model):
    title2 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
    
class  Total_FB_TotalOtherIncome_Master(models.Model):
    title3 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class Total_FB_EnrtyMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    FoodRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    BeverageRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalOtherIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBRevenue =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FoodCostOfSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    BeverageCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfFbSales  =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)   
    AudioVisualEquipmentCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    FBOtherCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)  
    TotalCostOfOtherRev =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    TotalCostOfSales =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True)    
    Gross_Profit =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    SalaryAndWages =  models.DecimalField(default = 0, blank=True,decimal_places = 2 , max_digits = 12)
    Bonuses_and_Incentives  = models.DecimalField(default = 0 ,decimal_places = 2 , max_digits = 12)
    Salary_Wages_and_Bonuses = models.DecimalField(default = 0,blank=True,decimal_places = 2, max_digits = 12)
    EmployeeBenefits = models.DecimalField(default = 0 , decimal_places=2, max_digits = 12, blank=True)
    PayrollRelatedExpenses = models.DecimalField(default=0 , decimal_places =2 , max_digits=12 ,blank=True)
    PayrollAndRelatedExpenses = models.DecimalField(default=0 , decimal_places =2, max_digits = 12,blank=True) 
    Total_Other_Expenses = models.DecimalField(default = 0 , decimal_places= 2, max_digits =12 ,blank=True)
    DepartmentIncome =  models.DecimalField(default = 0 ,decimal_places = 2, max_digits =12,blank=True) 
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
        
        
class Total_FB_EntryDetail(models.Model):
    Total_FB_Master =models.ForeignKey(Total_FB_Master, on_delete=models.CASCADE)
    Total_FB_EnrtyMaster =models.ForeignKey(Total_FB_EnrtyMaster, on_delete=models.CASCADE)
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
           
class Total_FB_FoodRevenue_EntryDetail(models.Model):
    Total_FB_FoodRevenue_Master =models.ForeignKey(Total_FB_FoodRevenue_Master, on_delete=models.CASCADE)
    Total_FB_EnrtyMaster =models.ForeignKey(Total_FB_EnrtyMaster, on_delete=models.CASCADE)
    Amount1 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
         
class Total_FB_BeverageRevenue_Maste_EntryDetail(models.Model):
    Total_FB_BeverageRevenue_Master =models.ForeignKey(Total_FB_BeverageRevenue_Master, on_delete=models.CASCADE)
    Total_FB_EnrtyMaster =models.ForeignKey(Total_FB_EnrtyMaster, on_delete=models.CASCADE)
    Amount2 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
        
class Total_FB_TotalOtherIncome_MasterIncome_EntryDetail(models.Model):
    Total_FB_TotalOtherIncome_Master =models.ForeignKey( Total_FB_TotalOtherIncome_Master, on_delete=models.CASCADE)
    Total_FB_EnrtyMaster =models.ForeignKey(Total_FB_EnrtyMaster, on_delete=models.CASCADE)
    Amount3 = models.DecimalField(decimal_places=2,max_digits=12)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
     
   
class  RoomWorksheet_SectionMaster(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   


class  RoomWorksheet_CategoryMaster(models.Model):
    CategoryTitle = models.CharField(max_length =  200)
    RoomWorksheet_SectionMaster =models.ForeignKey( RoomWorksheet_SectionMaster, on_delete=models.CASCADE)
    EntryType=models.CharField(default='',max_length=20)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
    

class  RoomWorksheet_ItemMaster(models.Model):
    ItemTitle = models.CharField(max_length =  200)
    RoomWorksheet_CategoryMaster =models.ForeignKey( RoomWorksheet_CategoryMaster, on_delete=models.CASCADE)
    EntryType=models.CharField(default='',max_length=20)
    IsTotal=models.IntegerField(default=0)
    TitleLevel=models.IntegerField(default=0)
    IsPer=models.IntegerField(default=0)
    IsFormula=models.IntegerField(default=0)
    IsReadOnly=models.IntegerField(default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
    
 
class RoomWorksheet_EnrtyMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
      
class RoomWorksheet_ItemDetails(models.Model):
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    RoomWorksheet_EnrtyMaster =models.ForeignKey( RoomWorksheet_EnrtyMaster, on_delete=models.CASCADE)
    RoomWorksheet_ItemMaster =models.ForeignKey( RoomWorksheet_ItemMaster, on_delete=models.CASCADE)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
    
class RoomWorksheet_CategoryDetails(models.Model):
    Amount = models.DecimalField(decimal_places=2,max_digits=12)
    RoomWorksheet_EnrtyMaster =models.ForeignKey( RoomWorksheet_EnrtyMaster, on_delete=models.CASCADE)
    RoomWorksheet_CategoryMaster =models.ForeignKey( RoomWorksheet_CategoryMaster, on_delete=models.CASCADE)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
      
      
   
class FB_Worksheet_Master(models.Model):
    title = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FB_Worksheet_EnrtyMaster(models.Model):
    EntryMonth =models.BigIntegerField(default=0)
    EntryYear =models.BigIntegerField(default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 
 
class FBW_Break_food_Internal_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
class FBW_Break_food_External_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
       
class FBW_Break_Beverage_Internal_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
      
class FBW_Break_Beverage_External_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
# SECONE TABLE MODEL
      
class FBW_Break_Food_Average_Check_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
     
class FBW_Break_Food_Average_Check_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
class FBW_Break_Beverage_Average_Check_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
  
class FBW_Break_Beverage_Average_Check_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
# THIRD TABLE MODEL

 
class FBW_Break_Food_Revenue_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FBW_Break_Food_Revenue_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FBW_Break_Beverage_Revenue_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FBW_Break_Beverage_Revenue_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
# FOURTH TABLE MODEL

    
class FBW_Launch_Food_Internal_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
     
class FBW_Launch_Food_External_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
     
class FBW_Launch_Beverage_Internal_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
     
class FBW_Launch_Beverage_External_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
        
# FIVE TABLE MODEL
   
class FBW_Launch_Food_Average_Check_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FBW_Launch_Food_Average_Check_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FBW_Beverage_Food_Average_Check_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)    

class FBW_Beverage_Food_Average_Check_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
# Six TABLE MODEL


class FBW_Launch_Food_Revenue_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FBW_Launch_Food_Revenue_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FBW_Launch_Beverage_Revenue_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
 
class FBW_Launch_Beverage_Revenue_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

  # For Seven table
  

class FBW_Dinner_Food_Internal_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   

class FBW_Dinner_Food_External_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Dinner_Beverage_Internal_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Dinner_Beverage_External_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    

  # For Eight table

class FBW_Dinner_Food_Average_Check_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   

class FBW_Dinner_Food_Average_Check_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   

class FBW_Dinner_Bevarage_Average_Check_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False) 

class FBW_Dinner_Bevarage_Average_Check_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   

  # For Nine table
  
class FBW_Dinner_Food_Revenue_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   

class FBW_Dinner_Food_Revenue_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
 
class FBW_Dinner_Beverage_Revenue_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   

class FBW_Dinner_Beverage_Revenue_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)   
    

  # For Nine table (Super Food Model)
  
class FBW_Super_Food_Internal_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Super_Food_External_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
 
class FBW_Super_Beverage_Internal_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Super_Beverage_External_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
  # For Ten table (Super Food Average)

class FBW_Super_Food_Average_Check_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Super_Food_Average_Check_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Super_Beverage_Average_Check_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Super_Beverage_Average_Check_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
# For Eleven table (Super Food Revenue View)   

class FBW_Super_Food_Revenue_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Super_Food_Revenue_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Super_Beverage_Revenue_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Super_Beverage_Revenue_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    
# SECOND MASTER FOR FB WORKSHEET

   
class FB_Worksheet_Second_Master(models.Model):
    title1 = models.CharField(max_length =  200)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
# For Twelvw table (Other Food Internal View)   

class FBW_Other_Food_Internal_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Other_Food_External_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE )
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
class FBW_Other_Beverage_Internal_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE )
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Other_Beverage_External_Covers_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
# For Thirteen table (Other Food Internal View) 


class FBW_Other_Food_Average_Check_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Other_Food_Average_Check_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Other_Beverage_Average_Check_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Other_Beverage_Average_Check_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
# For Fourteen table (Other Food Internal View) 


class FBW_Other_Food_Revenue_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Other_Food_Revenue_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Other_Beverage_Revenue_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

class FBW_Other_Beverage_Revenue_1_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
# For Fifteen table (Other Food Internal View) 

class FBW_Capture_Rates_Breakfast_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
# For Sixteen table (Other Food Internal View) 

class FBW_Capture_Rates_Launch_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
# For Seventeen table (Other Food Internal View) 

class FBW_Capture_Rates_Dinner_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)

# For Eighteen table (Other Food Internal View) 

class FBW_Capture_Rates_Supper_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    

# For Nighteen table (Other Food Internal View) 

class FBW_Capture_Rates_Others_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    

# For Twenteen table (Other Food Internal View) 

class FBW_Capture_Rates_AllMealTypes_Details(models.Model):
    FB_Worksheet_Master =models.ForeignKey(FB_Worksheet_Master, on_delete=models.CASCADE , default=0)
    FB_Worksheet_EnrtyMaster =models.ForeignKey(FB_Worksheet_EnrtyMaster, on_delete=models.CASCADE)
    Amount =  models.DecimalField(decimal_places=2,max_digits=12 , default=0)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateField(default = date.today)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateField(default = date.today)
    IsDelete = models.BooleanField(default=False)
    
    