
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from azure.storage.blob import BlobServiceClient
from django.db import connection
import json

from Employee_Payroll.models import Raw_Attendance_Data_File, Raw_Attendance_Data, Attendance_Data, Organization_Details
from Leave_Management_System.views import EmployeeDataSelect
from Leave_Management_System.models import Leave_Application
from app.models import OrganizationMaster
from hotelopsmgmtpy.GlobalConfig import MasterAttribute

storage_account_key = MasterAttribute.azure_storage_account_key
storage_account_name = MasterAttribute.azure_storage_account_name
connection_string = MasterAttribute.azure_connection_string

from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Process attendance files for a date range.'

    def add_arguments(self, parser):
        parser.add_argument('--start_date', type=str, help='Start date in YYYY-MM-DD format')
        parser.add_argument('--end_date', type=str, help='End date in YYYY-MM-DD format')

    def handle(self, *args, **kwargs):
        start_date_str = kwargs['start_date']
        end_date_str = kwargs['end_date']

        start_date = date.fromisoformat(start_date_str) if start_date_str else date.today()
        end_date = date.fromisoformat(end_date_str) if end_date_str else date.today()

        if start_date > end_date:
            self.stdout.write(self.style.ERROR('Start date must be before or equal to end date.'))
            return

        orgs = OrganizationMaster.objects.filter(IsDelete=False)

        for org in orgs:
            try:
                OrganizationID = org.OrganizationID

                current_date = start_date
                while current_date <= end_date:
                    UserID = 0

                    file_name_obj = self.get_latest_file(current_date, OrganizationID)
                    if file_name_obj:
                        
                                employee_data = EmployeeDataSelect(OrganizationID)
                                
                                self.process_employee_attendance(employee_data, current_date, OrganizationID, UserID)
                                self.stdout.write(self.style.SUCCESS(f'Attendance processed for  {current_date} OID = {OrganizationID}'))
                        
                    
                    # Move to the next date
                    current_date += timedelta(days=1)

            except Exception as e:
                    self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {str(e)}'))
    def get_latest_file(self, attendance_date,OrganizationID):
        return Raw_Attendance_Data_File.objects.filter(
            IsDelete=False,
            Attendance_Date=attendance_date,OrganizationID=OrganizationID
        ).order_by('-CreatedDateTime').first()

    def process_employee_attendance(self, employee_data, attendance_date_obj, OrganizationID, UserID):
        for emp in employee_data:
            Level = emp['Level']
            EmployeeCode = emp['EmployeeCode']
            Level_List = ["M", "M1", "M2", "M3", "M4", "M5", "M6"]

            latest_out_time = self.get_latest_out_time(EmployeeCode, OrganizationID, attendance_date_obj)
            earliest_in_time = self.get_earliest_in_time(EmployeeCode, OrganizationID, attendance_date_obj)

            if (latest_out_time and earliest_in_time) or (Level in Level_List and (latest_out_time or earliest_in_time)):
                attendance_records = self.calculate_duty_hours(earliest_in_time, latest_out_time)
                
                attendance_data_fields = {
                    'EmployeeCode': EmployeeCode,
                    'Date': attendance_date_obj,
                    'OrganizationID': OrganizationID,
                    'CreatedBy': UserID,
                    'In_Time': earliest_in_time,
                    'Out_Time': latest_out_time,
                    'Duty_Hour': attendance_records['DutyHours'],
                    'Status': self.determine_status(Level, attendance_records['DutyHours']),
                }
                objEx =Attendance_Data.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmployeeCode=EmployeeCode,Date=attendance_date_obj).first()
                if objEx:
                    objEx.IsDelete=True
                    objEx.save()
                        
                Attendance_Data.objects.create(**attendance_data_fields)
            else:
                self.process_leave_status(EmployeeCode, attendance_date_obj,OrganizationID , UserID)

    def get_latest_out_time(self, employee_code, OrganizationID, attendance_date_obj):
        latest_out_time_query = """
            SELECT MAX(Time) AS MaxOutTime
            FROM Employee_Payroll_raw_attendance_data
            WHERE EmployeeCode = %s
                AND OrganizationID = %s
                AND IsDelete = 0
                AND Status = 'OUT'
                AND Date = %s;
        """
        with connection.cursor() as cursor:
            cursor.execute(latest_out_time_query, [employee_code, OrganizationID, attendance_date_obj])
            result = cursor.fetchone()
        return result[0] if result else None

    def get_earliest_in_time(self, employee_code, OrganizationID, attendance_date_obj):
        earliest_in_time_query = """
            SELECT MIN(Time) AS MinInTime
            FROM Employee_Payroll_raw_attendance_data
            WHERE EmployeeCode = %s
                AND Date = %s
                AND OrganizationID = %s
                AND IsDelete = 0
                AND Status = 'IN';
        """
        with connection.cursor() as cursor:
            cursor.execute(earliest_in_time_query, [employee_code, attendance_date_obj, OrganizationID])
            result = cursor.fetchone()
        return result[0] if result else None

    def calculate_duty_hours(self, in_time_str, out_time_str):
        attendance_records = {'DutyHours': None}

        if in_time_str and out_time_str:
            in_time = datetime.strptime(in_time_str, '%H:%M:%S')
            out_time = datetime.strptime(out_time_str, '%H:%M:%S')
            duty_hours = out_time - in_time
            duty_hours_time = str(duty_hours).split()[-1]
            attendance_records['DutyHours'] = duty_hours_time

        return attendance_records

    def determine_status(self, level, duty_hours):
        if level in ["M", "M1", "M2", "M3", "M4", "M5", "M6"]:
            if duty_hours:
                duty_hours_timedelta = datetime.strptime(duty_hours, '%H:%M:%S') - datetime(1900, 1, 1)
                if duty_hours_timedelta >= timedelta(hours=8, minutes=30):
                    return "Present"
                elif duty_hours_timedelta >= timedelta(hours=5):
                    return "Half Day Present"
            return "Absent"
        else:
            return "Present" if duty_hours else "Absent"

    def process_leave_status(self, employee_code, attendance_date_obj, OrganizationID, UserID):
        query = """
            SELECT *
            FROM Leave_Management_System_leave_application
            WHERE Start_Date <= %s
                AND End_Date >= %s
                AND IsDelete = 0
                AND Emp_code = %s
                AND OrganizationID = %s
                AND Status = 1;
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [attendance_date_obj, attendance_date_obj, employee_code, OrganizationID])
            rows = cursor.fetchall()

        leave_status = 'Absent'
        if rows:
            leave_status = 'Leave'

        Attendance_Data.objects.create(
            EmployeeCode=employee_code,
            Date=attendance_date_obj,
            OrganizationID=OrganizationID,
            CreatedBy=UserID,
            Status=leave_status
        )
