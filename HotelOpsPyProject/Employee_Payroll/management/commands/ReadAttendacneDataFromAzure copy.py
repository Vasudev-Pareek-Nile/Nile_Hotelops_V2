
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from azure.storage.blob import BlobServiceClient
from django.db import connection
import json

from Employee_Payroll.models import Raw_Attendance_Data_File, Raw_Attendance_Data, Attendance_Data, Organization_Details, Raw_Attendance_Data_log
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
import csv
import requests

class Command(BaseCommand):
    help = 'Fetch data from an API and log the response for each organization'
    
    def handle(self, *args, **kwargs):
        # orgs = OrganizationMaster.objects.filter(IsDelete=False,IsNileHotel=1,Activation_status=1)

        validOrgs = Organization_Details.objects.filter(IsDelete=False)

        # self.stdout.write(self.style.SUCCESS(f"Fetching attendance for date:, OrgID: 1001"))

        if validOrgs:
            # for org in orgs:
            for org in validOrgs:
                if org.Biometric_Machine_Name == 'WYSE':
                    try:
                        now = timezone.now()
                        today_date_obj = now.date()
                        # today_date_obj = date(2025, 8, 31)
                        OrganizationID =   org.OID
                        UserID = 0

                        
                        file_name_obj = self.get_latest_file(today_date_obj,OrganizationID)
                        # print(file_name_obj)
                        if file_name_obj:
                            blob_name = file_name_obj.File_Name
                            blob_content = self.download_blob(blob_name,OrganizationID)
                            if blob_content:
                                full_data = self.parse_json(blob_content,OrganizationID)
                                if full_data and 'data' in full_data:
                                    data = full_data['data']
                                    first_date, last_date = self.get_file_date_range(data)
                                    try:
                                        self.process_attendance_file(data, today_date_obj, OrganizationID, UserID, first_date, last_date)
                                    except:
                                        print("Error Occured at Handle class while processing attendance file")

                                    # with transaction.atomic():
                                    #     with connection.cursor() as cursor:
                                    #         cursor.execute("Employee_Payroll_UpdateAttendance_Org ?",OrganizationID)
                                        
                                    self.stdout.write(self.style.SUCCESS(f'Blob content for {today_date_obj} is downloaded and processed.'))
                            else:
                                self.stdout.write(self.style.ERROR('Blob content is None or error occurred while downloading blob.'))
                        else:
                            self.stdout.write(self.style.ERROR(f'No file present for  ({today_date_obj}) for {OrganizationID ,OrganizationID}.'))
                    
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {str(e)}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Skipping organization {OrganizationID} with unsupported Biometric Machine Name: {org.Biometric_Machine_Name}'))
        else:
            print("Invalid Configuration Found")

        with transaction.atomic():
            with connection.cursor() as cursor:
                # cursor.execute("Employee_Payroll_UpdateAttendance_Org ?",0)
                cursor.execute("EXEC Employee_Payroll_UpdateAttendance_All_Org")


    def get_file_date_range(self, data):
        dates = []
        for row in data:
            try:
                fields = row.split(',')
                if len(fields) < 2:
                    continue
                date_str = fields[1].strip()   # "01/08/2025"
                date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
                dates.append(date_obj)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error parsing date from row: {row} | {e}"))
                continue

        if not dates:
            return None, None

        return min(dates), max(dates)
        
    #  ----------- / example code ------------------- 

    def get_latest_file(self, attendance_date,OrganizationID):
        return Raw_Attendance_Data_File.objects.filter(
            IsDelete=False,
            Attendance_Date=attendance_date,
            OrganizationID=OrganizationID
        ).order_by('-CreatedDateTime').first()
    
    def create_blob_client(self, blob_name,OrganizationID):
        container_name = "attendancedata"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        return container_client.get_blob_client(blob_name)

    def download_blob(self, blob_name,OrganizationID):
        blob_client = self.create_blob_client(blob_name,OrganizationID)

        if not blob_client.exists():
            self.stdout.write(
                f"No file present for {OrganizationID})."
            )
            return None  

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


    def process_attendance_file(self, data, attendance_date_obj, OrganizationID, UserID, first_date=None, last_date=None):
        org_obj = Organization_Details.objects.get(OID=OrganizationID, IsDelete=False)
        OID_Code = org_obj.OID_Code
        match_found = False

        bulk_update_list = []
        bulk_create_list = []
        employee_codes = set()

        # Parse and format data
        for row in data:
        # for i, row in enumerate(data, start=1):
            try:
                fields = row.split(',')
                if len(fields) <3:
                    continue  

                RawEmployeeCode, Date, Time, Status = fields
                # RawEmployeeCode, Date, Time, Status = fields[:4]
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
                    CreatedDateTime=timezone.now(),
                    ModifyBy=UserID,
                    ModifyDateTime=timezone.now(),
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
                existing_rec.ModifyDateTime = timezone.now()
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
        
        self.stdout.write(self.style.SUCCESS("Step 3: Backing up and replacing attendance..."))
        self.backup_and_replace_attendance(bulk_create_list, first_date, last_date)
        self.stdout.write(self.style.SUCCESS("Step 3 completed."))

        if not match_found:
            self.stdout.write(self.style.WARNING(f"No new attendance records matched the date {attendance_date_obj}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Processed {len(new_records)} new records, updated {len(bulk_update_list)} records."))

        return f"Processed {len(new_records)} new records, updated {len(bulk_update_list)} records."



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


    ############ Backup and Replace Attendance ############

    def backup_and_replace_attendance(self, bulk_create_list, first_date=None, last_date=None):
        with transaction.atomic():
            if not bulk_create_list:
                self.stdout.write(self.style.WARNING("No records to insert."))
                return

            org_id = bulk_create_list[0].OrganizationID

            # Filter by date range if provided
            existing_records = Raw_Attendance_Data.objects.filter(
                IsDelete=False,
                OrganizationID=org_id
            )
            if first_date and last_date:
                existing_records = existing_records.filter(Date__range=(first_date, last_date))

            # Backup
            if existing_records.exists():
                log_records = [
                    Raw_Attendance_Data_log(
                        EmployeeCode=rec.EmployeeCode,
                        Date=rec.Date,
                        Time=rec.Time,
                        Status=rec.Status,
                        OrganizationID=rec.OrganizationID,
                        CreatedBy=rec.CreatedBy,
                        CreatedDateTime=rec.CreatedDateTime,
                        ModifyBy=rec.ModifyBy,
                        ModifyDateTime=rec.ModifyDateTime,
                        IsDelete=rec.IsDelete
                    ) for rec in existing_records
                ]
                Raw_Attendance_Data_log.objects.bulk_create(log_records)
                self.stdout.write(self.style.SUCCESS(
                    f"Backed up {len(log_records)} records for Org {org_id}, "
                    f"Dates: {first_date} → {last_date}"
                ))

            # Delete existing records only in that date range
            deleted_count, _ = existing_records.delete()
            self.stdout.write(self.style.SUCCESS(
                f"Deleted {deleted_count} records for Org {org_id} in range {first_date} → {last_date}."
            ))

            # Insert new records
            Raw_Attendance_Data.objects.bulk_create(bulk_create_list)
            self.stdout.write(self.style.SUCCESS(
                f"Inserted {len(bulk_create_list)} new records for Org {org_id} "
                f"({first_date} → {last_date})."
            ))






