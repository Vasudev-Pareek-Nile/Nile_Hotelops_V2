# from io import BytesIO
# import uuid
# from pathlib import Path
# import mimetypes
# from azure.storage.blob import BlobServiceClient, ContentSettings
# import os

# connection_string = "DefaultEndpointsProtocol=https;AccountName=hotelopsdevstorage;AccountKey=gH5NXveEI5+AlwbwjBqGLj14u8Il9QLdsr8aarLlFp8gSPRDxdrW8CWTw34yhmpGdJXJlJFCELOY+AStEL/i4A==;BlobEndpoint=https://hotelopsdevstorage.blob.core.windows.net/;QueueEndpoint=https://hotelopsdevstorage.queue.core.windows.net/;TableEndpoint=https://hotelopsdevstorage.table.core.windows.net/;FileEndpoint=https://hotelopsdevstorage.file.core.windows.net/;"
# container_name = "data"

# ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.jpeg', '.jpg', '.png']

# def get_content_type(file_name):
#     return mimetypes.guess_type(file_name)[0] or 'application/octet-stream'

# def create_blob_client(file_name):
#     blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#     blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
#     return blob_client

# def upload_file_to_blob(file_stream, file_name):
#     if not file_name.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
#         raise ValueError("File extension not allowed.")

#     blob_client = create_blob_client(file_name)
#     blob_client.upload_blob(file_stream, overwrite=True, content_settings=ContentSettings(content_type=get_content_type(file_name)))
#     print(f"File '{file_name}' uploaded successfully to blob container '{container_name}'.")

#     return blob_client.url

# from django.http import HttpResponse
# from azure.storage.blob import BlobServiceClient

# def download_file_from_blob(file_name):
#     blob_client = create_blob_client(file_name)
    
#     try:
        
#         download_stream = blob_client.download_blob()
#         file_data = download_stream.readall()

        
#         response = HttpResponse(file_data, content_type=get_content_type(file_name))
#         response['Content-Disposition'] = f'attachment; filename={Path(file_name).name}'
#         return response
#     except Exception as e:
#         print(f"Error downloading file '{file_name}': {e}")
#         return None


from io import BytesIO
import uuid
from pathlib import Path
from datetime import datetime, timedelta
import mimetypes
from azure.storage.blob import BlobServiceClient, ContentSettings, generate_blob_sas, BlobSasPermissions
import os
from django.http import HttpResponse

# # Azure connection string and container name
# connection_string = "DefaultEndpointsProtocol=https;AccountName=hotelopsdevstorage;AccountKey=gH5NXveEI5+AlwbwjBqGLj14u8Il9QLdsr8aarLlFp8gSPRDxdrW8CWTw34yhmpGdJXJlJFCELOY+AStEL/i4A==;BlobEndpoint=https://hotelopsdevstorage.blob.core.windows.net/;QueueEndpoint=https://hotelopsdevstorage.queue.core.windows.net/;TableEndpoint=https://hotelopsdevstorage.table.core.windows.net/;FileEndpoint=https://hotelopsdevstorage.file.core.windows.net/;"
# container_name = "data"

import mimetypes
from io import BytesIO
from azure.storage.blob import BlobServiceClient, ContentSettings
from hotelopsmgmtpy.GlobalConfig import MasterAttribute


storage_account_key = MasterAttribute.azure_storage_account_key
storage_account_name = MasterAttribute.azure_storage_account_name
connection_string = MasterAttribute.azure_connection_string
container_name = "nilecareer"


ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.jpeg', '.jpg', '.png']


def get_content_type(file_name):
    mime_type, _ = mimetypes.guess_type(file_name)
    return mime_type or 'application/octet-stream'


def create_blob_client(file_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    Nfile_name= "0/"+file_name
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=Nfile_name)
    return blob_client


def Bannerupload_file_to_blob(file_stream, file_name):
    
    if not file_name.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
        raise ValueError("File extension not allowed.")

    
    content_type = get_content_type(file_name)

    
    file_content = file_stream
    file_io = BytesIO(file_content)

    
    blob_client = create_blob_client(file_name)
    blob_client.upload_blob(data=file_io, overwrite=True, content_settings=ContentSettings(content_type=content_type))

    return file_name


# # Upload file to blob storage
# def upload_file_to_blob(file_stream, file_name):
#     if not file_name.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
#         raise ValueError("File extension not allowed.")
    
#     # Upload the file to the blob
#     blob_client = create_blob_client(file_name)
#     blob_client.upload_blob(file_stream, overwrite=True, content_settings=ContentSettings(content_type=get_content_type(file_name)))
    
#     # Generate SAS URL for the uploaded file
#     sas_url = generate_sas_url(file_name)
#     print(f"File '{file_name}' uploaded successfully to blob container '{container_name}'.")
#     return sas_url

# # Function to generate SAS token and URL
# def generate_sas_url(blob_name):
#     blob_service_client = BlobServiceClient.from_connection_string(connection_string)
#     blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

#     sas_token = generate_blob_sas(
#         account_name=blob_service_client.account_name,
#         container_name=container_name,
#         blob_name=blob_name,
#         account_key=blob_service_client.credential.account_key,
#         permission=BlobSasPermissions(read=True),
#         expiry=datetime.utcnow() + timedelta(hours=30)  
#     )

#     sas_url = f"{blob_client.url}?{sas_token}"
#     return sas_url


def Bannerdownload_blob(file):
    blob_client = create_blob_client(file)
    if not blob_client.exists():
        return
    blob_content = blob_client.download_blob()
    return blob_content
