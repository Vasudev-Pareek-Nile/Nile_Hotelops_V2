from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.

# Manage Master -  On Roll models



class LavelAdd(models.Model):
    lavelname=models.CharField(max_length=255)
    
    

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.lavelname
    

class OnRollDivisionMaster(models.Model):
    DivisionName=models.CharField(max_length=255)
    
    Order = models.IntegerField(default=999)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.DivisionName}   {self.Order}'

class OnRollDepartmentMaster(models.Model):
    OnRollDivisionMaster = models.ForeignKey(OnRollDivisionMaster, on_delete=models.CASCADE)
    DepartmentName = models.CharField(max_length=255)
    Order = models.IntegerField(default=999)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.DepartmentName}   {self.Order}'
    

class OnRollDesignationMaster(models.Model):
    OnRollDivisionMaster = models.ForeignKey(OnRollDivisionMaster, on_delete=models.CASCADE)
    OnRollDepartmentMaster = models.ForeignKey(OnRollDepartmentMaster, on_delete=models.CASCADE)
    Div = models.CharField(max_length=255)
    Dept = models.CharField(max_length=255)
    designations = models.CharField(max_length=255)
    Lavel = models.CharField(max_length=255)
    Report_Designations = models.CharField(max_length=255,blank=True,null=True)
    Dotted_Line_Reporting_Designation = models.CharField(max_length=255, blank=True,null=True)
    Direct_Reporting_Division = models.CharField(max_length=255, blank=True,null=True)
    Direct_Reporting_Department = models.CharField(max_length=255, blank=True,null=True)
    Direct_Reporting_Designation = models.CharField(max_length=255, blank=True,null=True)
    Direct_Reporting_Level = models.CharField(max_length=255, blank=True,null=True)
    Order = models.IntegerField(default=999)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.designations}   {self.Order}' 





# Manage Master -  Contract


class ContractDivisionMaster(models.Model):
    DivisionName=models.CharField(max_length=255)
    Order = models.IntegerField(default=999)

    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.DivisionName}   {self.Order}' 
    



class ContractDepartmentMaster(models.Model):
    ContractDivisionMaster = models.ForeignKey(ContractDivisionMaster, on_delete=models.CASCADE)
    DepartmentName = models.CharField(max_length=255)
    Order = models.IntegerField(default=999)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.DepartmentName}   {self.Order}' 
    

class ContractDesignationMaster(models.Model):
    ContractDivisionMaster = models.ForeignKey(ContractDivisionMaster, on_delete=models.CASCADE)
    ContractDepartmentMaster = models.ForeignKey(ContractDepartmentMaster, on_delete=models.CASCADE)
    Div = models.CharField(max_length=255)
    Dept = models.CharField(max_length=255)
    designations = models.CharField(max_length=255)
    Lavel = models.CharField(max_length=255)
    Report_Designations = models.CharField(max_length=255)
    Order = models.IntegerField(default=999)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.Lavel}   {self.Order}'    


# Manage Master -  Shared Services


class ServicesDivisionMaster(models.Model):
    DivisionName=models.CharField(max_length=255)
    
    Order = models.IntegerField(default=999)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.DivisionName}   {self.Order}'

class ServicesDepartmentMaster(models.Model):
    ServicesDivisionMaster = models.ForeignKey(ServicesDivisionMaster, on_delete=models.CASCADE)
    DepartmentName = models.CharField(max_length=255)
    Order = models.IntegerField(default=999)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    
    
    def __str__(self):
        return f'{self.DepartmentName}   {self.Order}'
    

class ServicesDesignationMaster(models.Model):
    ServicesDivisionMaster = models.ForeignKey(ServicesDivisionMaster, on_delete=models.CASCADE)
    ServicesDepartmentMaster = models.ForeignKey(ServicesDepartmentMaster, on_delete=models.CASCADE)
    Div = models.CharField(max_length=255)
    Dept = models.CharField(max_length=255)
    designations = models.CharField(max_length=255)
    Lavel = models.CharField(max_length=255)
    Report_Designations = models.CharField(max_length=255)
    Order = models.IntegerField(default=999)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.Lavel        


#      Master Manage Corporate 

class CorporateDivisionMaster(models.Model):
    DivisionName=models.CharField(max_length=255)
    
    Order = models.IntegerField(default=999)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.DivisionName}   {self.Order}'

class CorporateDepartmentMaster(models.Model):
    CorporateDivisionMaster = models.ForeignKey(CorporateDivisionMaster, on_delete=models.CASCADE)
    DepartmentName = models.CharField(max_length=255)
    Order = models.IntegerField(default=999)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    
    
    def __str__(self):
        return f'{self.DepartmentName}   {self.Order}'
    

class CorporateDesignationMaster(models.Model):
    CorporateDivisionMaster = models.ForeignKey(CorporateDivisionMaster, on_delete=models.CASCADE)
    CorporateDepartmentMaster = models.ForeignKey(CorporateDepartmentMaster, on_delete=models.CASCADE)
    Div = models.CharField(max_length=255)
    Dept = models.CharField(max_length=255)
    designations = models.CharField(max_length=255)
    Lavel = models.CharField(max_length=255)
   
    Order = models.IntegerField(default=999)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.Lavel        




class ModuleMapping(models.Model):
    Department = models.CharField(max_length=255,blank=True,null=True)
    Level = models.CharField(max_length=255,blank=True,null=True)
    reporting_to = models.CharField(max_length=255,blank=True,null=True)
    Weightage1 = models.CharField(max_length=255,blank=True,null=True)
    Dotted_Line = models.CharField(max_length=255,blank=True,null=True)
    Weightage2 = models.CharField(max_length=255,blank=True,null=True)
    module_name= models.CharField(max_length=255,blank=True,null=True)
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)
        



#      Master Budget 

# class ManageBudgetOnRoll(models.Model):
#     on_roll_division_master = models.ForeignKey(OnRollDivisionMaster, on_delete=models.CASCADE)
#     on_roll_department_master = models.ForeignKey(OnRollDepartmentMaster, on_delete=models.CASCADE)
#     on_roll_designation_master = models.ForeignKey(OnRollDesignationMaster, on_delete=models.CASCADE)
    
#     hotel_name = models.CharField(max_length=255, blank=True, null=True)
#     avg_salary_data = models.BigIntegerField(default=0,blank=True, null=True)
#     head_count_deta = models.BigIntegerField(default=0,blank=True, null=True)
#     morning_data = models.BigIntegerField(default=0,blank=True, null=True)
#     general_data = models.BigIntegerField(default=0,blank=True, null=True)
#     afternoon_data = models.BigIntegerField(default=0,blank=True, null=True)
#     night_data = models.BigIntegerField(default=0,blank=True, null=True)
#     m_break_data = models.BigIntegerField(default=0,blank=True, null=True)
#     relievers_data = models.BigIntegerField(default=0,blank=True, null=True)
#     total_ctc_data = models.BigIntegerField(default=0,blank=True, null=True)

    
#     organization_id = models.BigIntegerField(default=0)
#     created_by = models.BigIntegerField(default=0)
#     created_date_time = models.DateTimeField(default=timezone.now)
#     modify_by = models.BigIntegerField(default=0)
#     modify_date_time = models.DateTimeField(default=timezone.now)
#     is_delete = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.hotel_name} - Average Salary: {self.avg_salary_data}"


class ManageBudgetOnRoll(models.Model):
    on_roll_division_master = models.ForeignKey(OnRollDivisionMaster, on_delete=models.CASCADE)
    on_roll_department_master = models.ForeignKey(OnRollDepartmentMaster, on_delete=models.CASCADE)
    on_roll_designation_master = models.ForeignKey(OnRollDesignationMaster, on_delete=models.CASCADE)
    
    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    avg_salary = models.BigIntegerField(default=0,blank=True, null=True)
    head_count = models.BigIntegerField(default=0,blank=True, null=True)
    morning = models.BigIntegerField(default=0,blank=True, null=True)
    general_deta = models.BigIntegerField(default=0,blank=True, null=True)
    afternoon = models.BigIntegerField(default=0,blank=True, null=True)
    night = models.BigIntegerField(default=0,blank=True, null=True)
    m_break = models.BigIntegerField(default=0,blank=True, null=True)
    relievers = models.BigIntegerField(default=0,blank=True, null=True)
    total_ctc = models.BigIntegerField(default=0,blank=True, null=True)

    Budget_Year = models.CharField(max_length=255, blank=True, null=True)

    
    OrganizationID = models.BigIntegerField(default=0)
    created_by = models.BigIntegerField(default=0)
    created_date_time = models.DateTimeField(default=timezone.now)
    modify_by = models.BigIntegerField(default=0)
    modify_date_time = models.DateTimeField(default=timezone.now)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hotel_name} - Average Salary: {self.avg_salary}"


class ManageBudgetContract(models.Model):
    contract_division_master = models.ForeignKey(ContractDivisionMaster, on_delete=models.CASCADE)
    contract_department_master = models.ForeignKey(ContractDepartmentMaster, on_delete=models.CASCADE)
    contract_designation_master = models.ForeignKey(ContractDesignationMaster, on_delete=models.CASCADE)

    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    avg_salary = models.BigIntegerField(default=0,blank=True, null=True)
    head_count = models.BigIntegerField(default=0,blank=True, null=True)
    morning = models.BigIntegerField(default=0,blank=True, null=True)
    general_deta = models.BigIntegerField(default=0,blank=True, null=True)
    afternoon = models.BigIntegerField(default=0,blank=True, null=True)
    night = models.BigIntegerField(default=0,blank=True, null=True)
    m_break = models.BigIntegerField(default=0,blank=True, null=True)
    relievers = models.BigIntegerField(default=0,blank=True, null=True)
    total_ctc = models.BigIntegerField(default=0,blank=True, null=True)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.hotel_name} - Average Salary: {self.avg_salary}"



class ManageBudgetSharedServices(models.Model):
    services_division_master = models.ForeignKey(ServicesDivisionMaster, on_delete=models.CASCADE)
    services_department_master = models.ForeignKey(ServicesDepartmentMaster, on_delete=models.CASCADE)
    services_designation_master = models.ForeignKey(ServicesDesignationMaster, on_delete=models.CASCADE)

    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    avg_salary = models.BigIntegerField(default=0,blank=True, null=True)
    head_count = models.BigIntegerField(default=0,blank=True, null=True)
    morning = models.BigIntegerField(default=0,blank=True, null=True)
    general_deta = models.BigIntegerField(default=0,blank=True, null=True)
    afternoon = models.BigIntegerField(default=0,blank=True, null=True)
    night = models.BigIntegerField(default=0,blank=True, null=True)
    m_break = models.BigIntegerField(default=0,blank=True, null=True)
    relievers = models.BigIntegerField(default=0,blank=True, null=True)
    total_ctc = models.BigIntegerField(default=0,blank=True, null=True)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.hotel_name} - Average Salary: {self.avg_salary}"





class BudgetMealCost(models.Model):
    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    cafeteriamealcost= models.BigIntegerField(default=0,blank=True, null=True)

    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cafeteriamealcost} "     



class BudgetInsuranceCost(models.Model):
    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    EmployeeInsurancecost= models.BigIntegerField(default=0,blank=True, null=True)

    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.EmployeeInsurancecost} "     

class EntryActualMealCost(models.Model):
    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    cafeteriamealcost= models.BigIntegerField(default=0,blank=True, null=True)

    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cafeteriamealcost} "     



class EntryActualInsuranceCost(models.Model):
    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    EmployeeInsurancecost= models.BigIntegerField(default=0,blank=True, null=True)

    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.EmployeeInsurancecost} "  



class EntryActualContract(models.Model):
    contract_division_master = models.ForeignKey(ContractDivisionMaster, on_delete=models.CASCADE)
    contract_department_master = models.ForeignKey(ContractDepartmentMaster, on_delete=models.CASCADE)
    contract_designation_master = models.ForeignKey(ContractDesignationMaster, on_delete=models.CASCADE)

    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    avg_salary = models.BigIntegerField(default=0,blank=True, null=True)
    head_count = models.BigIntegerField(default=0,blank=True, null=True)
    morning = models.BigIntegerField(default=0,blank=True, null=True)
    general_deta = models.BigIntegerField(default=0,blank=True, null=True)
    afternoon = models.BigIntegerField(default=0,blank=True, null=True)
    night = models.BigIntegerField(default=0,blank=True, null=True)
    m_break = models.BigIntegerField(default=0,blank=True, null=True)
    relievers = models.BigIntegerField(default=0,blank=True, null=True)
    total_ctc = models.BigIntegerField(default=0,blank=True, null=True)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.hotel_name} - Average Salary: {self.avg_salary}"



class EntryActualSharedServices(models.Model):
    services_division_master = models.ForeignKey(ServicesDivisionMaster, on_delete=models.CASCADE)
    services_department_master = models.ForeignKey(ServicesDepartmentMaster, on_delete=models.CASCADE)
    services_designation_master = models.ForeignKey(ServicesDesignationMaster, on_delete=models.CASCADE)

    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    avg_salary = models.BigIntegerField(default=0,blank=True, null=True)
    head_count = models.BigIntegerField(default=0,blank=True, null=True)
    morning = models.BigIntegerField(default=0,blank=True, null=True)
    general_deta = models.BigIntegerField(default=0,blank=True, null=True)
    afternoon = models.BigIntegerField(default=0,blank=True, null=True)
    night = models.BigIntegerField(default=0,blank=True, null=True)
    m_break = models.BigIntegerField(default=0,blank=True, null=True)
    relievers = models.BigIntegerField(default=0,blank=True, null=True)
    total_ctc = models.BigIntegerField(default=0,blank=True, null=True)
    
    OrganizationID = models.BigIntegerField(default=0)
    CreatedBy = models.BigIntegerField(default=0)
    CreatedDateTime = models.DateTimeField(default=timezone.now)
    ModifyBy = models.BigIntegerField(default=0)
    ModifyDateTime = models.DateTimeField(default=timezone.now)
    IsDelete = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.hotel_name} - Average Salary: {self.avg_salary}"
