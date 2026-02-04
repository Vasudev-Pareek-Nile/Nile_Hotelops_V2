from azure.storage.blob import BlobServiceClient
from django.http import HttpResponse, JsonResponse
import mimetypes
import uuid
import re 
import os
from azure.storage.blob import BlobServiceClient
connection_string = "DefaultEndpointsProtocol=https;AccountName=hotelopsdevstorage;AccountKey=gH5NXveEI5+AlwbwjBqGLj14u8Il9QLdsr8aarLlFp8gSPRDxdrW8CWTw34yhmpGdJXJlJFCELOY+AStEL/i4A==;BlobEndpoint=https://hotelopsdevstorage.blob.core.windows.net/;QueueEndpoint=https://hotelopsdevstorage.queue.core.windows.net/;TableEndpoint=https://hotelopsdevstorage.table.core.windows.net/;FileEndpoint=https://hotelopsdevstorage.file.core.windows.net/;"
container_name = "codeconduct"
folder_name = "Simplefile"

def create_blob_client(file_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    return blob_client


def sanitize_file_name(file_name):
    
    sanitized_name = re.sub(r'[^a-zA-Z0-9-_./]', '_', file_name)
    return sanitized_name



def upload_file_to_azurees(file):
    
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    
    blob_name = f"{folder_name}/{os.path.basename(file.name)}"  
    
    
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    
    blob_client.upload_blob(file.read(), overwrite=True)

    
    url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}"
    return url



def upload_file_to_azure(file):
    sanitized_file_name = sanitize_file_name(file.name)
    
    file_name = f"{uuid.uuid4()}-{sanitized_file_name}"
    
    blob_client = create_blob_client(file_name)
    try:
        blob_client.upload_blob(file, overwrite=True)
        return file_name 
    except Exception as e:
        print(f"Failed to upload to Azure: {e}")
        return None