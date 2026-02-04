
from Leave_Management_System.models import Emp_Leave_Balance_Master,EmpMonthLevelCreditMaster,Leave_Type_Master,CompoffLogMaster
from django.core.management.base import BaseCommand
from Employee_Payroll.models import Attendance_Data,WeekOffDetails
from datetime import date, timedelta
from app.models import OrganizationMaster
from hotelopsmgmtpy.GlobalConfig import MasterAttribute

import requests

from datetime import datetime,date
from calendar import monthrange


class Command(BaseCommand):
    
        
    def handle(self, *args, **kwargs):
           orgs  = OrganizationMaster.objects.filter(IsDelete= False)
           for org in orgs: 
        
                OrganizationID = org.OrganizationID
                print(OrganizationID)
                
                hotelapitoken = MasterAttribute.HotelAPIkeyToken
                headers = {
                    'hotel-api-token': hotelapitoken  
                }

                
                api_url = "http://hotelops.in/API/PyAPI/HREmployeeList?OrganizationID="+str(OrganizationID)


                try:
                    response = requests.get(api_url, headers=headers)
                    response.raise_for_status() 
                    emp_list = response.json()
                
                except requests.exceptions.RequestException as e:
                    print(f"Error occurred: {e}")

                
                for emp in emp_list:
                        
                            try:    
                                EmployeeCode =  emp['EmployeeCode']                                
                        
                                
                              
                                today = date.today()
                               

                                print(today)
                               


                                
                                last_7_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7, 0, -1)]
                                
                                next_day = today

                            

                            
                                dates = last_7_days 
                              
                                NextDate = next_day
                              

                                
                                Status_list = ['Present']
                                leave_type = Leave_Type_Master.objects.filter(OrganizationID = 1001, IsDelete=False)
                              
                                leave_list = []
                                for leave in leave_type:
                                    leave_list.append(leave.Type)
                                Status_list.extend(leave_list)
                            
                                attendance_data_working_days = Attendance_Data.objects.filter(EmployeeCode=EmployeeCode, OrganizationID=OrganizationID, IsDelete=False, Status__in=Status_list,Date__in = dates )

                                PresentDays = len(attendance_data_working_days)
                            
                                

                                attendance_data_absent_days = Attendance_Data.objects.filter(EmployeeCode=EmployeeCode, OrganizationID=OrganizationID, IsDelete=False, Status='Absent', Date__in = dates)
                            
                                absent_dates = [data.Date for data in attendance_data_absent_days ]
                                AbsentDays = len(absent_dates)
                                
                                
                                NextDayobj = Attendance_Data.objects.filter(EmployeeCode=EmployeeCode, OrganizationID=OrganizationID, IsDelete=False, Date = NextDate, Status__in=leave_list).first()
                                if NextDayobj is not None:
                                    NextDayStatus= NextDayobj.Status
                                else:
                                    NextDayStatus = None    

                                        


                                
                                            
                                if PresentDays >= 6 and AbsentDays == 0  and NextDayStatus == None:
                                    try:
                                        leave_type = Leave_Type_Master.objects.get(Type__icontains='comp', IsDelete=False, OrganizationID=OrganizationID)

                                        for data in attendance_data_working_days:
                                            try:
                                                CompoffLogMaster.objects.get(EmployeeCode=EmployeeCode, CompoffDate__in=dates, OrganizationID=OrganizationID, IsDelete=False)
                                            except CompoffLogMaster.DoesNotExist:
                                                try:
                                                    weekoff = WeekOffDetails.objects.get(Emp_Code=EmployeeCode, WeekoffDate=data.Date, OrganizationID=OrganizationID, IsDelete=False)
                                                    if weekoff and data.Status == "Present":
                                                        leave_balance = Emp_Leave_Balance_Master.objects.filter(
                                                            Leave_Type_Master_id=leave_type.id, 
                                                            Emp_code=EmployeeCode, 
                                                            OrganizationID=OrganizationID, 
                                                            IsDelete=False
                                                        ).first()

                                                        if leave_balance:
                                                            leave_balance.Balance += 1
                                                            leave_balance.save()
                                                        else:
                                                            leave_balance = Emp_Leave_Balance_Master.objects.create(
                                                                Leave_Type_Master_id=leave_type.id,
                                                                Emp_code=EmployeeCode,
                                                                Balance=1,
                                                                OrganizationID=OrganizationID,
                                                                IsDelete=False
                                                            )

                                                        EmpMonthLevelCreditMaster.objects.create(
                                                            Leave_Type_Master_id=leave_type.id,
                                                            Emp_code=EmployeeCode,
                                                            credit=1,
                                                            OrganizationID=OrganizationID
                                                        )

                                                        CompoffLogMaster.objects.create(
                                                            EmployeeCode=EmployeeCode, 
                                                            CompoffDate=data.Date,
                                                            OrganizationID=OrganizationID,
                                                            Remarks=f'Created on behalf of present on week off ({data.Date})'
                                                        )
                                                except WeekOffDetails.DoesNotExist:
                                                    print(f"Week off detail does not exist for employee {EmployeeCode} on date {data.Date}")
                                    except Leave_Type_Master.DoesNotExist:
                                        print(f"Leave type 'comp' does not exist for organization ID {OrganizationID}")
                                    except Exception as e:
                                        print(f"An unexpected error occurred: {e}")
                            
                            



                                
                            except Exception as e:
                                    print(f"An unexpected error occurred for employee {EmployeeCode}: {e}")                        

                self.stdout.write(self.style.SUCCESS(f'Records created successfully'))








