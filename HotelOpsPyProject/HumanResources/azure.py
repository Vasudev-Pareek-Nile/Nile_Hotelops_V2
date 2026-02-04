from io import BytesIO
import uuid
from pathlib import Path

from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from .models import EmployeePersonalDetails,EmployeeQualificationDetails,EmployeePreviousWorkInformationDetails,EmployeeDocumentsInformationDetails,EmployeeIdentityInformationDetails
import mimetypes


from azure.storage.blob import BlobServiceClient,ContentSettings
storage_account_key = MasterAttribute.azure_storage_account_key
storage_account_name = MasterAttribute.azure_storage_account_name
connection_string = MasterAttribute.azure_connection_string

container_name = "humanresources"

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    ext = Path(filename).suffix.lower()[1:]  # Get extension without dot
    return ext in ALLOWED_EXTENSIONS

def create_blob_client(file_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    return blob_client

def save_file_id_to_db(id, file_name,ModelName):
    if ModelName == "EmployeePersonalDetails":
        new_file = EmployeePersonalDetails.objects.get(EmpID=id)
        new_file.ProfileImageFileName = file_name
        new_file.save()
    elif ModelName == "EmployeeQualificationDetails":
        new_file = EmployeeQualificationDetails.objects.get(id=id)
        new_file.FileName = file_name
        new_file.save()
    elif ModelName  == "EmployeePreviousWorkInformationDetails":     
        new_file = EmployeePreviousWorkInformationDetails.objects.get(id=id)
        new_file.FileName = file_name
        new_file.save()
    elif ModelName  == "EmployeeDocumentsInformationDetails":     
        new_file = EmployeeDocumentsInformationDetails.objects.get(id=id)
        new_file.FileName = file_name
        new_file.save()
    elif ModelName  == "EmployeeIdentityInformationDetails_Pan":
        new_file = EmployeeIdentityInformationDetails.objects.get(id=id)
        new_file.PanFileName = file_name
        new_file.save()
    elif ModelName  == "EmployeeIdentityInformationDetails_Aadhaar":
        new_file = EmployeeIdentityInformationDetails.objects.get(id=id)
        new_file.AadhaarFileName = file_name
        new_file.save()   
    elif ModelName  == "EmployeeIdentityInformationDetails_License":
        new_file = EmployeeIdentityInformationDetails.objects.get(id=id)
        new_file.DrivingFileName = file_name
        new_file.save()        

                
    else:
        new_file = None
    return new_file

def upload_file_to_blob(file, file_id, folder_name,ModelName):
    if not allowed_file(file.name):
        raise ValueError("File type not allowed.")
    
    file_prefix = uuid.uuid4().hex
    ext = Path(file.name).suffix
    file_name = f"{folder_name}/{file_prefix}{ext}"
    file_content = file.read()
    file_io = BytesIO(file_content)
    
    # Determine the MIME type based on the file extension
    content_type, _ = mimetypes.guess_type(file.name)
    content_type = content_type or 'application/octet-stream'  
    
    blob_client = create_blob_client(file_name=file_name)
    blob_client.upload_blob(data=file_io, overwrite=True, content_settings=ContentSettings(content_type=content_type))
    
    file_object = save_file_id_to_db(file_id, file_name,ModelName)
    return file_object

def download_blob(file):
    blob_client = create_blob_client(file)
    if not blob_client.exists():
        return
    blob_content = blob_client.download_blob()
    return blob_content