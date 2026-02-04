from Employee_Payroll.models import Raw_Attendance_Data_File,Organization_Details
from azure.storage.blob import BlobServiceClient, ContentSettings
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.core.management.base import BaseCommand
from Employee_Payroll.models import APILog
from app.models import OrganizationMaster
from datetime import datetime  
from pathlib import Path
from io import BytesIO
import requests
import time
import json
import uuid
import os


storage_account_key = MasterAttribute.azure_storage_account_key
storage_account_name = MasterAttribute.azure_storage_account_name
connection_string = MasterAttribute.azure_connection_string




class Command(BaseCommand):
    help = 'Fetch data from an API and log the response for each organization'

    def handle(self, *args, **kwargs):
       
        # orgs = OrganizationMaster.objects.filter(IsDelete=False  , OrganizationID__in = [1001,1101,1301])
        orgs = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1,  Activation_status=1)
        for org in orgs:
                OrganizationID = org.OrganizationID
                
                
                hotelapitoken = MasterAttribute.HotelAPIkeyToken
                headers = {
                    'hotel-api-token': hotelapitoken  
                }
                org_details = Organization_Details.objects.filter(OID=OrganizationID,IsDelete=False).first()
                if org_details:
                        if org_details.OrgUrl:
                            org_url = org_details.OrgUrl
                            
                            month =datetime.now().month
                            year = datetime.now().year
                            
                            api_url = f'{org_url}&month={month}&year={year}'

                            try:
                                start_time = time.time()
                                response = requests.get(api_url)
                                response_time = time.time() - start_time
                                
                                if response.status_code == 200:
                                    data = response.json()
                                    # print("Data")
                                    # print(OrganizationID)
                                    # print(api_url)
                                    # print(data)
                                    upload_to_azure(data, OrganizationID)
                                    message = f"Data has been uploaded to Azure Blob Storage for Organization ID {OrganizationID}"
                                else:
                                    message = f"Failed to retrieve data. HTTP Status code: {response.status_code}"
                                
                                APILog.objects.create(
                                    Url=api_url,
                                    Status_Code=response.status_code,
                                    Response_Time=response_time,
                                    Message=message,
                                    OrganizationID=OrganizationID,
                                )
                                
                                self.stdout.write(self.style.SUCCESS(message))
                                
                            except requests.RequestException as e:
                                error_message = f"An error occurred: {str(e)}"
                                self.stdout.write(self.style.ERROR(error_message))
                                APILog.objects.create(
                                    Url=api_url,
                                    Status_Code=response.status_code,
                                    Response_Time=response_time,
                                    Message=error_message,
                                    OrganizationID=OrganizationID,
                                )



def create_blob_client():
    connection_string = MasterAttribute.azure_connection_string
    container_name = "attendancedata"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    return blob_service_client.get_container_client(container_name)

def upload_to_azure(data, organization_id):
    blob_client = create_blob_client()
    
   
    file_prefix = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
 
    filename = f"{file_prefix}_{organization_id}.json"
    Attendance_Date = datetime.now().date()
     
    obj = Raw_Attendance_Data_File.objects.create(
                File_Name=filename,
                Attendance_Date=Attendance_Date,
                OrganizationID=organization_id
            )
    file_content = json.dumps(data)
    blob_client.upload_blob(name=filename, data=file_content, overwrite=True,content_settings=ContentSettings(content_type='application/json'))




