


from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from app.models import EmployeeMaster,OrganizationMaster
from Leave_Management_System.models import Emp_Leave_Balance_Master, Leave_Config_Details, EmpMonthLevelCreditMaster
from datetime import datetime

from app.views import EmployeeDataSelectLeaveCredit_Data




class Command(BaseCommand):
    help = 'Employee Leave Balance Credit'

    def handle(self, *args, **options):
                    
                # orgs = OrganizationMaster.objects.filter(IsDelete=False)
                
            
                
                # for org in orgs:
                #     OrganizationID = org.OrganizationID        
                    # previous_year = datetime.now().year - 1
                    previous_year = 2025
                    
                    OrganizationID = 1

                    
                    leave_configs = Leave_Config_Details.objects.filter(
                        IsDelete=False,
                        IsAutoCredit=True,
                        Financial_Year_Start_Date__year=previous_year
                    )

                
                    employees = EmployeeDataSelectLeaveCredit_Data(OrganizationID=OrganizationID)
                    for employee in employees:
                        try:
                            EmployeeCode = employee['EmployeeCode']
                            EmployeeBalance = Emp_Leave_Balance_Master.objects.filter(
                                OrganizationID=OrganizationID,
                                Emp_code=EmployeeCode,
                                IsDelete=False
                            )
                          
                            if EmployeeBalance.exists():
                               
                                for leaveConfig in leave_configs:
                                   

                                    update_employee_balance =  Emp_Leave_Balance_Master.objects.filter(
                                        OrganizationID=OrganizationID,
                                        IsDelete=False,
                                        Leave_Type_Master=leaveConfig.Leave_Type_Master,
                                        Emp_code=EmployeeCode
                                        ).first()
                                    
                                    if update_employee_balance:     
                                        Balance = 0
                                        if leaveConfig.Carry_FWD:
                                        
                                             
                                            previous_year_balance = update_employee_balance.Balance
                                            if previous_year_balance > leaveConfig.Maximum_Accumulation:
                                                
                                                previous_year_balance = leaveConfig.Maximum_Accumulation
                                            Balance += previous_year_balance

                                        update_employee_balance.Balance = Balance
                                        update_employee_balance.save()

                                   

                        except Exception as e:
                            print(f"Error processing employee {employee['EmpName']}: {e}")

                    print(f"Leave credit cycle completed for {OrganizationID}.")
