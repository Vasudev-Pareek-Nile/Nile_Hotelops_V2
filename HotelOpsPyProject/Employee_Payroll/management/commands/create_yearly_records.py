from django.core.management.base import BaseCommand
from Employee_Payroll.models import Attendance_Data
from datetime import date, timedelta
from hotelopsmgmtpy.GlobalConfig import MasterAttribute,OrganizationDetail

import requests

class Command(BaseCommand):
    
    
    help = 'Creates yearly records for the next year'
    
    
        
    def handle(self, *args, **kwargs):
        
        
        
        hotelapitoken = MasterAttribute.HotelAPIkeyToken
        headers = {
            'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
        }
        
        
        api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID=3"

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status() 
            memOrg = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
           
        print(memOrg)
        
        
        
        api_url = "http://hotelops.in/API/PyAPI/HREmployeeList?OrganizationID=" + str(1001)
        

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  # Optional: Check for any HTTP errors
            emp_list = response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")

        current_year = date.today().year

        start_date = date(current_year + 1, 1, 1)
        end_date = date(current_year + 1, 12, 31)

        delta = timedelta(days=1)
        current_date = start_date

        for emp in emp_list:
            EmployeeCode = emp['EmployeeCode']
            current_date = start_date  
            while current_date <= end_date:
                Attendance_Data.objects.create(
                    EmployeeCode=EmployeeCode,
                    Date=current_date,
                )
                current_date += delta

        self.stdout.write(self.style.SUCCESS(f'Yearly records created successfully for the next year '))
