

       
from django.core.management.base import BaseCommand
from app.models import EmployeeMaster, OrganizationMaster
from django.shortcuts import get_object_or_404

from Leave_Management_System.models import Emp_Leave_Balance_Master, Leave_Config_Details, EmpMonthLevelCreditMaster
from datetime import datetime

from app.views import EmployeeDataSelectLeaveCredit_Data

class Command(BaseCommand):
    help = 'Employee Leave Balance Credit'

    def handle(self, *args, **options):
        # orgs = OrganizationMaster.objects.filter(IsDelete=False)
        
      
        
        # for org in orgs:
        #     OrganizationID = org.OrganizationID
 
        
            OrganizationID = 1
            
            
            # current_year = 2025
            current_year = datetime.now().year

            current_month = datetime.now().month
            leave_configs = Leave_Config_Details.objects.filter(IsDelete=False,Financial_Year_Start_Date__year = current_year)
        
            # employees = EmployeeMaster.objects.filter(IsDelete=False, OrganizationID=OrganizationID)
            
            employees = EmployeeDataSelectLeaveCredit_Data(OrganizationID=OrganizationID)
            for employee in employees:
                DateofJoining = employee['DateofJoining']
                #Leave Credit when employee join before date of 15
                comparison_date = datetime(current_year, current_month, 15).date() 
             
                
                if DateofJoining <= comparison_date:

                    try:
                        EmployeeCode = employee['EmployeeCode']
                        EmployeeBalance = Emp_Leave_Balance_Master.objects.filter(OrganizationID=OrganizationID, Emp_code=EmployeeCode, IsDelete=False)
                       
                        if EmployeeBalance.exists():
                          
                            for leaveConfig in leave_configs:
                                  

                                    
                                    if leaveConfig.IsMonthly and leaveConfig.IsAutoCredit:
                                        
                                        UpdateBalance = round((leaveConfig.YearlyLeave / 12), 2)
                                        
                                        UpdateEmployeeBalance = Emp_Leave_Balance_Master.objects.filter(
                                        OrganizationID=OrganizationID,
                                        IsDelete=False,
                                        Leave_Type_Master=leaveConfig.Leave_Type_Master,
                                        Emp_code=EmployeeCode
                                        ).first()
                                        
                                        if UpdateEmployeeBalance:
                                            Balance = UpdateEmployeeBalance.Balance + UpdateBalance
                                            UpdateEmployeeBalance.Balance = Balance
                                            UpdateEmployeeBalance.save()
                                        else:
                                            Emp_Leave_Balance_Master.objects.create(
                                            OrganizationID=OrganizationID,
                                            Leave_Type_Master=leaveConfig.Leave_Type_Master,
                                            Emp_code=EmployeeCode,
                                            Balance=UpdateBalance
                                            )

                                      
                                            

                                        EmpMonthLevelCreditMaster.objects.create(
                                            OrganizationID=OrganizationID,
                                            Leave_Type_Master=leaveConfig.Leave_Type_Master,
                                            Emp_code=EmployeeCode,
                                            credit=UpdateBalance
                                        )

                                
                                

                                
                                                
                                            
                                    

                        else:
                           
                            for leaveConfig in leave_configs:
                                try:
                                        
                                    
                                
                                        if leaveConfig.IsMonthly:
                                            CreditBalance = round((leaveConfig.YearlyLeave / 12), 2)
                                        else:
                                            CreditBalance = leaveConfig.YearlyLeave
                                    
                                        Emp_Leave_Balance_Master.objects.create(
                                            OrganizationID=OrganizationID,
                                            Leave_Type_Master=leaveConfig.Leave_Type_Master,
                                            Emp_code=EmployeeCode,
                                            Balance=CreditBalance
                                        )

                                        EmpMonthLevelCreditMaster.objects.create(
                                            OrganizationID=OrganizationID,
                                            Leave_Type_Master=leaveConfig.Leave_Type_Master,
                                            Emp_code=EmployeeCode,
                                            credit=CreditBalance
                                        )
                                except Exception as e:
                                    print(f"Error processing leave config for {employee['EmpName']}: {e}")

                    except Exception as e:
                        print(f"Error processing employee {employee['EmpName']}: {e}")

            print(f"Leave credit cycle completed for {OrganizationID}")


