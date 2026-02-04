
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from azure.storage.blob import BlobServiceClient
from django.db import connection
import json

from Employee_Payroll.models import Raw_Attendance_Data_File, Raw_Attendance_Data, Attendance_Data, Organization_Details
# from Leave_Management_System.views import EmployeeDataSelect
from Employee_Payroll.objParse import parse_dateF
from Leave_Management_System.models import Leave_Application
from app.models import OrganizationMaster
from hotelopsmgmtpy.GlobalConfig import MasterAttribute

storage_account_key = MasterAttribute.azure_storage_account_key
storage_account_name = MasterAttribute.azure_storage_account_name
connection_string = MasterAttribute.azure_connection_string
from django.db import transaction
from datetime import date, timedelta
class Command(BaseCommand):
    help = 'Fetch data from an API and log the response for each organization'
    
    def handle(self, *args, **kwargs):
        orgs = OrganizationMaster.objects.filter(IsDelete=False,IsNileHotel=1,Activation_status=1)

        for org in orgs:

            try:
                now = timezone.now()
                # today_date_obj = now.date()
                today_date_obj = date(2025, 7, 31) 
                OrganizationID =   org.OrganizationID
                UserID = 0
                
              
                file_name_obj = self.get_latest_file(today_date_obj,OrganizationID)
                print(file_name_obj)
                if file_name_obj:
                    blob_name = file_name_obj.File_Name
                    blob_content = self.download_blob(blob_name,OrganizationID)
                    if blob_content:
                        full_data = self.parse_json(blob_content,OrganizationID)
                        if full_data and 'data' in full_data:
                            data = full_data['data']
                            print(data)
                            # employee_data = EmployeeDataSelect(OrganizationID)
                            try:
                                self.process_attendance_file(data, today_date_obj, OrganizationID, UserID)
                            except:
                                print()
                            # with transaction.atomic():
                            #     with connection.cursor() as cursor:
                            #         cursor.execute("Employee_Payroll_UpdateAttendance_Org ?",OrganizationID)
                               
                            # self.process_employee_attendance(employee_data, today_date_obj, OrganizationID, UserID)
                                
                            self.stdout.write(self.style.SUCCESS(f'Blob content for {today_date_obj} is downloaded and processed.'))
                    else:
                        self.stdout.write(self.style.ERROR('Blob content is None or error occurred while downloading blob.'))
                else:
                    self.stdout.write(self.style.ERROR(f'No file present for  ({today_date_obj}) for {org.OrganizationName ,org.OrganizationID}.'))
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {str(e)}'))
        
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("Employee_Payroll_UpdateAttendance_Org ?",0)


    
    def get_latest_file(self, attendance_date,OrganizationID):
        return Raw_Attendance_Data_File.objects.filter(
            IsDelete=False,
            Attendance_Date=attendance_date,OrganizationID=OrganizationID
        ).order_by('-CreatedDateTime').first()
    
    def create_blob_client(self, blob_name,OrganizationID):
        container_name = "attendancedata"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        return container_client.get_blob_client(blob_name)

    def download_blob(self, blob_name,OrganizationID):
        blob_client = self.create_blob_client(blob_name,OrganizationID)
        try:
            blob_content = blob_client.download_blob().readall()
            return blob_content
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error downloading blob: {e}"))
            return None
    
    def parse_json(self, blob_content,OrganizationID):
        try:
            return json.loads(blob_content)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'JSON decode error: {str(e)}'))
            return None


    def process_attendance_file(self, data, attendance_date_obj, OrganizationID, UserID):
        org_obj = Organization_Details.objects.get(OID=OrganizationID, IsDelete=False)
        OID_Code = org_obj.OID_Code
        match_found = False

        bulk_update_list = []
        bulk_create_list = []
        employee_codes = set()

        # Parse and format data
        for row in data:
            try:
                fields = row.split(',')
                if len(fields) <3:
                    continue  # Skip invalid rows

                RawEmployeeCode, Date, Time, Status = fields
                date_obj = parse_dateF(Date)

                # Format Employee Code
                if OID_Code:
                    RawEmployeeCode = RawEmployeeCode.zfill(3)
                    DumpEmployeeCode = str(OID_Code) + RawEmployeeCode
                    DumpEmployeeCode = DumpEmployeeCode.zfill(9)
                else:
                    DumpEmployeeCode = RawEmployeeCode

                employee_codes.add(DumpEmployeeCode)

                # Create new attendance record instance
                attendance_record = Raw_Attendance_Data(
                    EmployeeCode=DumpEmployeeCode,
                    Date=date_obj,
                    Time=Time,
                    Status=Status,
                    OrganizationID=OrganizationID,
                    CreatedBy=UserID,
                    CreatedDateTime=datetime.now(),
                    ModifyBy=UserID,
                    ModifyDateTime=datetime.now(),
                    IsDelete=False
                )
                bulk_create_list.append(attendance_record)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing row '{row}': {str(e)}"))
                continue

        # Fetch existing records to update
        existing_records = Raw_Attendance_Data.objects.filter(
            EmployeeCode__in=employee_codes,
            Date=attendance_date_obj,
            OrganizationID=OrganizationID,
            IsDelete=False
        )

        existing_dict = {(rec.EmployeeCode, rec.Date): rec for rec in existing_records}

        # Separate updates from inserts
        new_records = []
        for record in bulk_create_list:
            key = (record.EmployeeCode, record.Date)
            if key in existing_dict:
                # Update existing records
                existing_rec = existing_dict[key]
                existing_rec.Time = record.Time
                existing_rec.Status = record.Status
                existing_rec.ModifyBy = UserID
                existing_rec.ModifyDateTime = datetime.now()
                bulk_update_list.append(existing_rec)
            else:
                # New records
                new_records.append(record)
                match_found = True

        # Bulk update and insert inside a transaction
        with transaction.atomic():
            if bulk_update_list:
                Raw_Attendance_Data.objects.bulk_update(
                    bulk_update_list,
                    ["Time", "Status", "ModifyBy", "ModifyDateTime"]
                )
            if new_records:  # Only insert new records
                Raw_Attendance_Data.objects.bulk_create(new_records)

        if not match_found:
            self.stdout.write(self.style.WARNING(f"No new attendance records matched the date {attendance_date_obj}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Processed {len(new_records)} new records, updated {len(bulk_update_list)} records."))

        return f"Processed {len(new_records)} new records, updated {len(bulk_update_list)} records."
    def process_attendance_file_RunningOld(self, data, attendance_date_obj, OrganizationID, UserID):
        org_obj = Organization_Details.objects.get(OID=OrganizationID, IsDelete=False)
        OID_Code = org_obj.OID_Code
        match_found = False
        for row in data:
            fields = row.split(',')
            
            if len(fields)>3: #or 0==1:
                try:
                    RawEmployeeCode, Date, Time, Status = fields
                    
                    DumpEmployeeCode=""
                    if OID_Code != '':
                        if len(RawEmployeeCode) == 1:
                            RawEmployeeCode = '00' + RawEmployeeCode
                        elif len(RawEmployeeCode) == 2:
                            RawEmployeeCode = '0' + RawEmployeeCode
                        
                        DumpEmployeeCode = str(OID_Code) + RawEmployeeCode
                        DumpEmployeeCode = DumpEmployeeCode.zfill(9)
                    else:
                        DumpEmployeeCode=RawEmployeeCode
                    records = Raw_Attendance_Data.objects.filter(
                        EmployeeCode=DumpEmployeeCode,
                        Date=Date,
                        OrganizationID=OrganizationID,
                        IsDelete=True
                    )
                    
                    if records.exists():
                        records.update(isDelete=True)
                    
                except:
                        print() 
        for row in data:
            fields = row.split(',')
            if len(fields)>3: #or 0==1:
                try:
                    RawEmployeeCode, Date, Time, Status = fields
                    date_str=Date
                    date_obj=parse_dateF(date_str)
                    #date_obj = datetime.strptime(Date, '%d/%m/%Y').date()
                    DumpEmployeeCode = RawEmployeeCode
                    if OID_Code != '':
                        if len(RawEmployeeCode) == 1:
                            RawEmployeeCode = '00' + RawEmployeeCode
                        elif len(RawEmployeeCode) == 2:
                            RawEmployeeCode = '0' + RawEmployeeCode
                        
                        DumpEmployeeCode = str(OID_Code) + RawEmployeeCode
                        DumpEmployeeCode = DumpEmployeeCode.zfill(9)

                    Raw_Attendance_Data.objects.create(
                        EmployeeCode=DumpEmployeeCode,
                        Date=date_obj,
                        Time=Time,
                        Status=Status,
                        OrganizationID=OrganizationID,
                        CreatedBy=UserID
                    )
                    match_found = True
                except Exception as e:
                    print(f"An error occurred: {str(e)}")

        if not match_found:
            self.stdout.write(self.style.WARNING(f"Attendance record of file does not match with selected date {attendance_date_obj}"))

    def process_employee_attendance(self, employee_data, attendance_date_obj, OrganizationID, UserID):
        for emp in employee_data:
            Level = emp 
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
