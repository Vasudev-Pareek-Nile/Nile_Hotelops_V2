from django.shortcuts import render

# Create your views here.






from django.shortcuts import render, redirect
from .models import EmpCodeofConductDocMaster,Docmaster

from django.http import HttpResponseRedirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute

from django.shortcuts import redirect

from .models import EmpCodeofConductDocMaster  

def CodeDelete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    cle=EmpCodeofConductDocMaster.objects.get(id=id)
    cle.IsDelete=True
    cle.ModifyBy=UserID
    cle.save()

    
    return redirect('Checklistshow')
    

from django.http import JsonResponse
from django.shortcuts import redirect
from .models import EmpCodeofConductDocMaster
from HumanResources.views import EmployeeDetailsData  
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from django.urls import reverse
from django.shortcuts import redirect, reverse
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

from django.shortcuts import redirect
from django.http import JsonResponse

from django.shortcuts import redirect

from django.urls import reverse
from django.utils.http import urlencode  
from Checklist_Issued.views import run_background_checklist_tasks

def submit_emp_code_of_conduct(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID = str(request.session["UserID"])
    EmpID = request.GET.get('EmpID')

    # Fetch employee details
    EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
    check_instance = {
        'EmployeeCode': EmpDetails.EmployeeCode,
        'EmpName': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
        'Department': EmpDetails.Department,
        'Designation': EmpDetails.Designation,
        'DateofJoining': EmpDetails.DateofJoining,
        'OrganizationID': EmpDetails.OrganizationID,
    }

    if request.method == 'POST':
        try:
            Empcode = request.POST.get('Empcode')
            name = request.FILES.get('FileName')  # Handle file input
            conductdate = request.POST.get('Conductdate')
            document_id = request.POST.get('id')

            if document_id:
                # Update existing document
                emp_doc = EmpCodeofConductDocMaster.objects.filter(id=document_id).first()
                if emp_doc:
                    emp_doc.Empcode = check_instance['EmployeeCode']
                    if name:  # Only update the file if a new file is uploaded
                        emp_doc.FileName = name
                    emp_doc.Conductdate = conductdate
                    emp_doc.OrganizationID = OrganizationID
                    emp_doc.CreatedBy = UserID
                    emp_doc.save()
                else:
                    return JsonResponse({'success': False, 'message': 'Document not found.'})
            else:
                # Create new document
                EmpCodeofConductDocMaster.objects.create(
                    Empcode=check_instance['EmployeeCode'],
                    FileName=name,
                    Conductdate=conductdate,
                    OrganizationID=OrganizationID,
                    CreatedBy=UserID
                )
                
            Object_ID=6
            run_background_checklist_tasks(Empcode, OID, Object_ID, UserID)

            # Redirect with success parameters
            Success = True
            encrypted_id = encrypt_id(EmpID)
            url = reverse('CodeConduct')  # Replace 'Resignation' with the actual redirect view name
            query_params = urlencode({'EmpID': encrypted_id, 'Success': Success})
            redirect_url = f"{url}?{query_params}&OID={OrganizationID}"
            return redirect(redirect_url)

        except Exception as e:
            # Log the error for debugging
            Success = True
            encrypted_id = encrypt_id(EmpID)
            url = reverse('CodeConduct')  # Replace 'Resignation' with the actual redirect view name
            query_params = urlencode({'EmpID': encrypted_id, 'Success': Success})
            redirect_url = f"{url}?{query_params}"
            return redirect(redirect_url)

    elif request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            emp_id = request.GET.get('id')
            emp_doc = EmpCodeofConductDocMaster.objects.get(id=emp_id)

            data = {
                'id': emp_doc.id,
                'Empcode': emp_doc.Empcode,
                'FileName': emp_doc.FileName if emp_doc.FileName else '',
                'Conductdate': emp_doc.Conductdate.strftime('%Y-%m-%d'),
            }
            return JsonResponse(data)
        except Exception as e:
            print(f"Error occurred while fetching data: {str(e)}")
            return JsonResponse({'success': False, 'message': 'An error occurred while fetching data.'})

    return redirect('codeconductlist')  # Fallback redirect


           

from django.shortcuts import redirect

from django.shortcuts import get_object_or_404
from .azuree import upload_file_to_azurees
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import requests

import requests

from azure.storage.blob import BlobServiceClient
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

from azure.storage.blob import BlobServiceClient
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404

def download_sample_file(request, doc_id):
    # Retrieve document from database
    doc = get_object_or_404(Docmaster, id=doc_id)
    file_url = doc.samplefile

    # Azure Blob Storage credentials
    account_name = "hotelopsdevstorage"
    connection_string = "DefaultEndpointsProtocol=https;AccountName=hotelopsdevstorage;AccountKey=gH5NXveEI5+AlwbwjBqGLj14u8Il9QLdsr8aarLlFp8gSPRDxdrW8CWTw34yhmpGdJXJlJFCELOY+AStEL/i4A==;BlobEndpoint=https://hotelopsdevstorage.blob.core.windows.net/;QueueEndpoint=https://hotelopsdevstorage.queue.core.windows.net/;TableEndpoint=https://hotelopsdevstorage.table.core.windows.net/;FileEndpoint=https://hotelopsdevstorage.file.core.windows.net/;"
    container_name = "codeconduct"
    folder_name = "Simplefile"

    try:
        # Extract file name from file_url
        file_name = file_url.split('/')[-1]
        blob_name = f"{folder_name}/{file_name}"

        # Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # Download blob content
        stream = blob_client.download_blob()

        # Generate HTTP response
        response = HttpResponse(
            stream.readall(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response

    except Exception as e:
        # Log the error or handle it accordingly
        raise Http404(f"File could not be downloaded: {str(e)}")



from django.http import HttpResponse, Http404
from docx2pdf import convert
from azure.storage.blob import BlobServiceClient
import tempfile
import os

def download_sample_pdf_file(request, doc_id):
    doc = get_object_or_404(Docmaster, id=doc_id)
    file_url = doc.samplefile

    # Azure storage details
    account_name = "hotelopsdevstorage"
    connection_string = "DefaultEndpointsProtocol=https;AccountName=hotelopsdevstorage;AccountKey=gH5NXveEI5+AlwbwjBqGLj14u8Il9QLdsr8aarLlFp8gSPRDxdrW8CWTw34yhmpGdJXJlJFCELOY+AStEL/i4A==;BlobEndpoint=https://hotelopsdevstorage.blob.core.windows.net/;"
    container_name = "codeconduct"
    folder_name = "Simplefile"

    try:
        file_name = file_url.split('/')[-1]
        blob_name = f"{folder_name}/{file_name}"

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        # Temporary folder for processing
        with tempfile.TemporaryDirectory() as tmpdir:
            docx_path = os.path.join(tmpdir, file_name)

            # Save DOCX locally
            with open(docx_path, "wb") as f:
                f.write(blob_client.download_blob().readall())

            # Convert DOCX → PDF
            pdf_path = os.path.splitext(docx_path)[0] + ".pdf"
            convert(docx_path, pdf_path)

            # Read PDF file
            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()

        # Return PDF for download
        response = HttpResponse(pdf_data, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{file_name.replace(".docx", ".pdf")}"'
        return response

    except Exception as e:
        raise Http404(f"Error converting file: {str(e)}")



from django.shortcuts import render, redirect
from .models import Docmaster


def upload_sample_file(request):
    if request.method == "POST" and request.FILES['samplefile']:
        file = request.FILES['samplefile']
        
       
        url = upload_file_to_azurees(file)
        
       
        doc = Docmaster(samplefile=url)
        doc.save()
        
        return redirect('success_url')  

    return render(request, 'Conduct/upload_file.html')  




def codeconductlist(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])

    codeconducts = EmpCodeofConductDocMaster.objects.filter(OrganizationID=OrganizationID,IsDelete=False)
    docs = Docmaster.objects.all()
    
    context={
        'codeconducts':codeconducts,
        'docs':docs
    }
    return render(request, 'Conduct/codeconductlist.html',context)



def download_codeconduct_file(request, conduct_id):
    # Fetch the document
    conduct_doc = get_object_or_404(EmpCodeofConductDocMaster, id=conduct_id)

    # Azure Blob Storage credentials
    account_name = "hotelopsdevstorage"
    connection_string = "DefaultEndpointsProtocol=https;AccountName=hotelopsdevstorage;AccountKey=gH5NXveEI5+AlwbwjBqGLj14u8Il9QLdsr8aarLlFp8gSPRDxdrW8CWTw34yhmpGdJXJlJFCELOY+AStEL/i4A==;BlobEndpoint=https://hotelopsdevstorage.blob.core.windows.net/"
    container_name = "codeconduct"

    try:
        # Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=conduct_doc.FileName)

        # Download the blob content
        stream = blob_client.download_blob()
        response = HttpResponse(stream.readall(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{conduct_doc.FileName}"'
        return response
    except Exception as e:
        print(f"Error occurred while downloading the file: {str(e)}")
        raise Http404("File could not be downloaded.")
    

from app.Global_Api import Get_Employee_Master_Data_with_EmpID
from datetime import datetime    
from app.models import OrganizationMaster
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
import json
    
def Employee_Details_Cover_Page_View(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
        OrganizationID= OID 
        
    EmpID = request.GET.get('EmpID')

    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')

    
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    

    organization = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logo = f"{base_url}{organization.OrganizationLogo}" if organization and organization.OrganizationLogo else None

    EmployeeData = Get_Employee_Master_Data_with_EmpID(EmpID,OrganizationID)
    
    print("data is here::", EmployeeData)
    context = {
        'EmpData':EmployeeData,
        'organization_logo': organization_logo,
        'current_datetime': current_datetime,
    }
    # return render(request, 'Conduct/Employee_Details_CoverPage.html', context)

   
    # context = {
    #     'selectedOrganizationID': selectedOrganizationID,
    #     'current_datetime': current_datetime,
    #     'UserID': UserID,
    #     'organization_logo': organization_logo,
    #     'organization_logos':organization_logos,
    #     'selectedOrganizationName': selectedOrganizationName,
    #     'projects': projects,
    # }

    template_path = "Conduct/Employee_Details_CoverPage.html"
    html_string = render_to_string(template_path, context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ActualMasterReport.pdf"'

    result = BytesIO()
    pisa_status = pisa.CreatePDF(BytesIO(html_string.encode("UTF-8")), dest=result)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')

    response.write(result.getvalue())
    return response



