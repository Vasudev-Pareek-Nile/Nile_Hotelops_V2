from django.core.management.base import BaseCommand
from Leave_Management_System.models import Emp_Leave_Balance_Master, Leave_Config_Details

class Command(BaseCommand):
    help = 'Employee Leave Balance Credit'

    def handle(self, *args, **options):
        
        leave_types = Leave_Config_Details.objects.all()
        for leave_type in leave_types:
            
            if leave_type.IsMonthly:
            
                employees = Emp_Leave_Balance_Master.objects.filter(
                    Leave_Type_Master=leave_type.Leave_Type_Master
                )

                for employee in employees:
                    employee.Balance += (leave_type.YearlyLeave/12)

                    employee.OrganizationID = leave_type.OrganizationID
                    

                    employee.save()
