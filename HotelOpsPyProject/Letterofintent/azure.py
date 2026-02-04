from io import BytesIO
import uuid
from pathlib import Path

from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from .models  import LETTEROFINTENTEmployeeDetail


# from azure.storage.blob import BlobServiceClient,ContentSettings
# storage_account_key = MasterAttribute.storage_account_key
# storage_account_name = MasterAttribute.storage_account_name
# connection_string = MasterAttribute.connection_string

from azure.storage.blob import BlobServiceClient,ContentSettings
storage_account_key = MasterAttribute.azure_storage_account_key
storage_account_name = MasterAttribute.azure_storage_account_name
connection_string = MasterAttribute.azure_connection_string



container_name = "employeeletters"
ALLOWED_EXTENTIONS = ['.pdf', '.doc', '.docx', '.PDF', '.DOC', '.DOCX']


my_content_settings = ContentSettings(content_type='application/pdf')



def create_blob_client(file_name):
     
     Blob_Service_Client = BlobServiceClient.from_connection_string(connection_string)
     Blo_Client = Blob_Service_Client.get_blob_client(container=container_name,blob=file_name)

     return Blo_Client


def check_file_ext(path):
    ext = Path(path).suffix
    return ext in ALLOWED_EXTENTIONS


def save_file_id_to_db(id,file_name):
    new_file = LETTEROFINTENTEmployeeDetail.objects.get(id=id)
    new_file.file_id = file_name
   
    new_file.save()
    return new_file

def upload_file_to_blob(file,file_id):

    if not check_file_ext(file.name):
        return

    file_prefix = uuid.uuid4().hex
    ext = Path(file.name).suffix
    # file_name = f"{file_prefix}{ext}"
    file_name = f"Letterofintent/{file_prefix}{ext}"
    file_content = file.read()
    file_io = BytesIO(file_content)
    blob_client = create_blob_client(file_name=file_name)
    blob_client.upload_blob(data=file_io,overwrite=True, content_settings=my_content_settings)
    file_object = save_file_id_to_db(file_id,file_name)

    return file_object


def download_blob(file):
    blob_client = create_blob_client(file)
    if not blob_client.exists():
        return
    blob_content = blob_client.download_blob()
    return blob_content


# def  replace_file_from_blob(file):
#     blob_client = create_blob_client(file)
#     if not blob_client.exists():
#         return
#     blob_content = blob_client.delete_blob()
#     return blob_content