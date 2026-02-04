import asyncio
from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient, BlobClient, ContainerClient

async def main():
    account_url = "your_account_url"
    credential = DefaultAzureCredential()

    async with BlobServiceClient(account_url=account_url, credential=credential) as blob_service_client:
        container_client = blob_service_client.get_container_client(container="sample-container")
        

if __name__ == "__main__":
    asyncio.run(main())