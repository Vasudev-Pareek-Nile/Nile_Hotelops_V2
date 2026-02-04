from io import BytesIO
import uuid
from pathlib import Path
from .models  import Resume
from io import BytesIO
import uuid
from pathlib import Path
from .models import Resume
import mimetypes  # Import the mimetypes module


from azure.storage.blob import BlobServiceClient,ContentSettings
# storage_account_key = "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="
# storage_account_name = "devstoreaccount1"
# connection_string = "AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;DefaultEndpointsProtocol=http;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
# container_name = "resumes"
storage_account_key = "PV6pykN3d/a4jjH64vEd4qsQUGQuohDthY2JUGN9z5+9EmoGBJpabNShKP0rJOAxWj5kvwAXD1BPUUUSUZgSfg=="
storage_account_name = "hotelopsblob"
connection_string = "DefaultEndpointsProtocol=https;AccountName=hotelopsblob;AccountKey=PV6pykN3d/a4jjH64vEd4qsQUGQuohDthY2JUGN9z5+9EmoGBJpabNShKP0rJOAxWj5kvwAXD1BPUUUSUZgSfg==;BlobEndpoint=https://hotelopsblob.blob.core.windows.net/;QueueEndpoint=https://hotelopsblob.queue.core.windows.net/;TableEndpoint=https://hotelopsblob.table.core.windows.net/;FileEndpoint=https://hotelopsblob.file.core.windows.net/;"
container_name = "employeedatabank"

ALLOWED_EXTENTIONS = ['.pdf', '.docx', '.doc']

def get_content_type(file_name):
  
    return mimetypes.guess_type(file_name)[0] or 'application/octet-stream'



def create_blob_client(file_name):
     
     Blob_Service_Client = BlobServiceClient.from_connection_string(connection_string)
     Blo_Client = Blob_Service_Client.get_blob_client(container=container_name,blob=file_name)

     return Blo_Client


def check_file_ext(path):
    ext = Path(path).suffix
    return ext in ALLOWED_EXTENTIONS


def save_file_id_to_db(id,file_name):
    new_file = Resume.objects.get(id=id)
    new_file.file_id = file_name
   
    new_file.save()
    return new_file

def upload_file_to_blob(file, file_id):
    if not check_file_ext(file.name):
        return

    file_prefix = uuid.uuid4().hex
    ext = Path(file.name).suffix
    folder_name = "0/"
    file_nameU = f"{folder_name}{file_prefix}{ext}"
    file_name = f"{file_prefix}{ext}"
    file_content = file.read()
    file_io = BytesIO(file_content)
    
    # Get the content type based on the file extension
    content_type = get_content_type(file.name)

    # Create the blob client and upload the file with the determined content type
    blob_client = create_blob_client(file_name=file_nameU)
    blob_client.upload_blob(data=file_io, overwrite=True, content_settings=ContentSettings(content_type=content_type))
    
    file_object = save_file_id_to_db(file_id, file_name)
    return file_object

def download_blob(file):
    blob_client = create_blob_client(file)
    if not blob_client.exists():
        return
    blob_content = blob_client.download_blob()
    return blob_content


