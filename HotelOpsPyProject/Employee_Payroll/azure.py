from io import BytesIO
import uuid
from pathlib import Path

from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from .models  import AttendanceSalaryFile


# from azure.storage.blob import BlobServiceClient,ContentSettings
# storage_account_key = MasterAttribute.storage_account_key
# storage_account_name = MasterAttribute.storage_account_name
# connection_string = MasterAttribute.connection_string


from azure.storage.blob import BlobServiceClient,ContentSettings
storage_account_key = MasterAttribute.azure_storage_account_key
storage_account_name = MasterAttribute.azure_storage_account_name
connection_string = MasterAttribute.azure_connection_string


container_name = "attendancedata"

ALLOWED_EXTENSIONS = ['.pdf', '.xls', '.xlsx', '.csv']


from azure.storage.blob import BlobServiceClient, ContentSettings
from io import BytesIO
from pathlib import Path
import uuid

container_name = "attendancedata"
ALLOWED_EXTENSIONS = ['.pdf', '.xls', '.xlsx', '.csv']

# def get_content_settings(extension):
#     content_type_map = {
#         '.pdf': 'application/pdf',
#         '.xls': 'application/vnd.ms-excel',
#         '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#         '.csv': 'text/csv',
#     }
#     content_type = content_type_map.get(extension, 'application/octet-stream')
#     return ContentSettings(content_type=content_type)

# def create_blob_client(file_name):
#     Blob_Service_Client = BlobServiceClient.from_connection_string(connection_string)
#     Blob_Client = Blob_Service_Client.get_blob_client(container=container_name, blob=file_name)
#     return Blob_Client

# def check_file_ext(path):
#     ext = Path(path).suffix
#     return ext in ALLOWED_EXTENSIONS

# def save_file_id_to_db(id, file_name):
#     new_file = AttendanceSalaryFile.objects.get(id=id)
#     new_file.FileName = file_name
#     new_file.save()
#     return new_file
# def upload_file_to_blob(file, file_id):
#     if not check_file_ext(file.name):
#         return

#     file_prefix = uuid.uuid4().hex
#     ext = Path(file.name).suffix
#     file_name = f"{file_prefix}{ext}"
#     file_content = file.read()
#     file_io = BytesIO(file_content)

#     my_content_settings = get_content_settings(ext)

#     blob_client = create_blob_client(file_name=file_name)
  
#     blob_client.upload_blob(data=file_io, overwrite=True, content_settings=my_content_settings)

#     file_object = save_file_id_to_db(file_id, file_name)
#     return file_object
ALLOWED_EXTENSIONS = ['.pdf', '.xls', '.xlsx', '.csv']

def get_content_settings(extension):
    content_type_map = {
        '.pdf': 'application/pdf',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.csv': 'text/csv',
    }
    content_type = content_type_map.get(extension, 'application/octet-stream')
    return ContentSettings(content_type=content_type)

def create_blob_client(file_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    return blob_client

def check_file_ext(path):
    ext = Path(path).suffix
    return ext in ALLOWED_EXTENSIONS

def save_file_id_to_db(id, file_name, is_pdf=False):
    new_file = AttendanceSalaryFile.objects.get(id=id)
    if is_pdf:
        new_file.PdfFileName = file_name  
        new_file.PdfFileTitle = f"PDF_{file_name}"  
    else:
        new_file.FileName = file_name 
    new_file.save()
    return new_file

def upload_file_to_blob(file, file_id, is_pdf=False):
    if not check_file_ext(file.name):
        return

    file_prefix = uuid.uuid4().hex
    ext = Path(file.name).suffix
    file_name = f"{file_prefix}{ext}"
    file_content = file.read()
    file_io = BytesIO(file_content)

    my_content_settings = get_content_settings(ext)

    blob_client = create_blob_client(file_name=file_name)

    blob_client.upload_blob(data=file_io, overwrite=True, content_settings=my_content_settings)

    if is_pdf:
        save_file_id_to_db(file_id, file_name, is_pdf=True)
    else:
        save_file_id_to_db(file_id, file_name)
def download_blob(file_name):
    blob_client = create_blob_client(file_name)
    if not blob_client.exists():
        return None  
    
    blob_data = blob_client.download_blob()
    return blob_data.readall()  



# def  replace_file_from_blob(file):
#     blob_client = create_blob_client(file)
#     if not blob_client.exists():
#         return
#     blob_content = blob_client.delete_blob()
#     return blob_content