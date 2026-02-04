from django.contrib import admin
from .models import LavelAdd,OnRollDivisionMaster,OnRollDepartmentMaster,OnRollDesignationMaster,ContractDivisionMaster,ContractDepartmentMaster,ContractDesignationMaster,ServicesDivisionMaster,ServicesDepartmentMaster,ServicesDesignationMaster,CorporateDivisionMaster,CorporateDepartmentMaster,CorporateDesignationMaster,ModuleMapping,ManageBudgetOnRoll,BudgetMealCost,BudgetInsuranceCost,ManageBudgetContract,ManageBudgetSharedServices,EntryActualMealCost,EntryActualInsuranceCost,EntryActualContract,EntryActualSharedServices
# Register your models here.
admin.site.register(LavelAdd)
admin.site.register(OnRollDivisionMaster)
admin.site.register(OnRollDepartmentMaster)
admin.site.register(OnRollDesignationMaster)

admin.site.register(ContractDivisionMaster)
admin.site.register(ContractDepartmentMaster)
admin.site.register(ContractDesignationMaster)


admin.site.register(ServicesDivisionMaster)
admin.site.register(ServicesDepartmentMaster)
admin.site.register(ServicesDesignationMaster)

admin.site.register(CorporateDivisionMaster)
admin.site.register(CorporateDepartmentMaster)
admin.site.register(CorporateDesignationMaster)


admin.site.register(ModuleMapping)
admin.site.register(ManageBudgetOnRoll)
admin.site.register(BudgetMealCost)

admin.site.register(BudgetInsuranceCost)

admin.site.register(ManageBudgetContract)
admin.site.register(ManageBudgetSharedServices)

admin.site.register(EntryActualMealCost)

admin.site.register(EntryActualInsuranceCost)

admin.site.register(EntryActualContract)
admin.site.register(EntryActualSharedServices)
