from argparse import REMAINDER
from copyreg import remove_extension
from datetime import date
import datetime
from decimal import Decimal
from io import BytesIO
import json
from django.db import router
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
import requests
from TrainingAssessment.models import TrainingAssessmentEntryDetails, TrainingAssessmentEntryMaster, TrainingAssessmentMaster 
from app.models import MonthListMaster
from django.db.models import Subquery
from django.db.models import OuterRef
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.db import connection
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import JsonResponse
from datetime import datetime
from django.utils.safestring import mark_safe

def  HotelYearlyReportAPI(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
    'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = "https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID=3"
    # response = requests.get(api_url, headers=headers)
    # # response_content = response.content.decode('utf-8')
    # mem = response.json()

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        mem = response.json()
      #  return JsonResponse(mem)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

    # api_url = "https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID=3"


    # response = requests.get(api_url, headers=headers)
    # response.raise_for_status()  # Optional: Check for any HTTP errors
    # try:
    #     mem = response.json()
    # except json.JSONDecodeError:
    #     mem = json.loads(response.text)
    #     #mem=response.json()
    json_response = json.dumps(mem)  # Serialize the object to JSON
    return JsonResponse(json_response, safe=False)



 
def  TrainingAssessmentHotelYearlyReport(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    current_year = datetime.now().year
    years = range(2022, current_year + 1)


    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
    'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = "https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID="+str(OrganizationID)
    # response = requests.get(api_url, headers=headers)
    # # response_content = response.content.decode('utf-8')
    # mem = response.json()

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        mem = response.json()
      #  return JsonResponse(mem)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    I=""
    if 'I' in request.GET:
        I=request.GET["I"]
    else:
        I = OrganizationID

    EntryYear=""
    if 'EntryYear' in request.GET:
        EntryYear=request.GET["EntryYear"]
    else:
        EntryYear=current_year


    Expapi_url = "https://hotelops.in/API/PyTrainingAssessmentAPI/TrainingAssessment_Hotel_Yearly_Report?OrganizationID="+str(I)+"&EntryYear="+str(EntryYear)
    # response = requests.get(api_url, headers=headers)
    # # response_content = response.content.decode('utf-8')
    # mem = response.json()

    try:
        response = requests.get(Expapi_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        DataRes = response.json()
      #  return JsonResponse(mem)
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    context = {'years': years,'mem':mem,'DataRes':DataRes}

    return render(request, 'TrainingAssessment/TrainingAssessmentHotelYearlyReport.html' ,context) 


def  TrainingAssessmentHotelCombineMontlyReport(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    current_year = datetime.now().year
    current_month = datetime.now().month
    years = range(2022, current_year + 1)


    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
    'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = "https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID="+str(OrganizationID)
    # response = requests.get(api_url, headers=headers)
    # # response_content = response.content.decode('utf-8')
    # mem = response.json()

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        mem = response.json()
      #  return JsonResponse(mem)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    I=""
    if 'I' in request.GET:
        I=request.GET["I"]
    else:
        I = OrganizationID

    EntryYear=""
    if 'EntryYear' in request.GET:
        EntryYear=request.GET["EntryYear"]
    else:
        EntryYear=current_year

    EntryMonth=""
    if 'EntryMonth' in request.GET:
        EntryMonth=request.GET["EntryMonth"]
    else:
        EntryMonth=current_month    
    
        


    Expapi_url = "https://hotelops.in/API/PyTrainingAssessmentAPI/TrainingAssessment_HotelCombine_Monthly_Report?EntryMonth="+str(EntryMonth)+"&EntryYear="+str(EntryYear)
    # response = requests.get(api_url, headers=headers)
    # # response_content = response.content.decode('utf-8')
    # mem = response.json()

    try:
        response = requests.get(Expapi_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        DataRes = response.json()
      #  return JsonResponse(mem)
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    table=""
    if DataRes!=[]:
        headers = list(DataRes[0].keys())

        # Create the table headers
        table_header = '<thead><tr>'
        for header in headers:
            table_header += f'<th>{header}</th>'
        table_header += '</tr></thead>'

        # Create the table body
        table_body = '<tbody>'
        for item in DataRes:
            table_body += '<tr>'
            for key, value in item.items():
                table_body += f'<td>{value}</td>'
            table_body += '</tr>'
        table_body += '</tbody>'

        # Combine the table header and body
        table = f'<table id="tableData" class="table table-bordered">{table_header}{table_body}</table>'

    
    context = {'years': years,'mem':mem,'DataRes':mark_safe(table),'EntryMonth':EntryMonth,'EntryYear':EntryYear}

    return render(request, 'TrainingAssessment/TrainingAssessmentHotelCombineMontlyReport.html' ,context) 

 
def  TrainingAssessmentList(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    
    mem = TrainingAssessmentEntryMaster.objects.filter(IsDelete=False,OrganizationID=OrganizationID).values()       
    
    return render(request, 'TrainingAssessment/TrainingAssessmentList.html' ,{'mem' :mem }) 
def convert_date_format(date_string):
    try:
        # Parse the input date string into a datetime object
        date_obj = datetime.strptime(date_string, '%d/%B/%Y')
        # Convert the datetime object to the desired format
        formatted_date = date_obj.strftime('%Y-%m-%d')
        return formatted_date
    except ValueError:
        return None  # Handle invalid date format here
   
   
def TrainingAssessmentEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == "POST":
        TrainingDate = request.POST["TrainingDate"] 
        EmployeeCode = request.POST["EmployeeCode"] 
        EmployeeName = request.POST["EmployeeName"] 
        EmployeeDesignation = request.POST["EmployeeDesignation"] 
        try:
            print(TrainingDate)
            TrainingDateObj = convert_date_format(TrainingDate)
            print(TrainingDateObj)
        except ValueError:
            error_message = 'Invalid date format. Please use YYYY-MM-DD.'
            TrainingDateObj = datetime.today()
            # Handle the error and render the form again with the error message.
        
        
        enmaster= TrainingAssessmentEntryMaster.objects.create(TrainingDate=TrainingDateObj,EmpCode=EmployeeCode,EmpName=EmployeeName,EmpDesignation=EmployeeDesignation,OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()
             
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            Status = request.POST["Status_" + str(x)]
            if(Status == ''):
                Status = ''
                      
            TitleID_ = request.POST["TitleID_" + str(x)]
            
            TitleObje=TrainingAssessmentMaster.objects.get(id=TitleID_)
            EntOBj=TrainingAssessmentEntryMaster.objects.get(id=enmaster.pk)
              
            v = TrainingAssessmentEntryDetails.objects.create(Status = Status,
                                                       TrainingAssessmentMaster=TitleObje,
                                                       TrainingAssessmentEntryMaster= EntOBj,
                                                      
                                                      )                        
        return(redirect('/TrainingAssessment/TrainingAssessmentList'))
    mem = TrainingAssessmentMaster.objects.filter(IsDelete = False)    
    today = datetime.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'TrainingAssessment/TrainingAssessmentEntry.html' ,{'mem':mem,'d':d})



def delete_TrainingAssessment (request,id):
    mem = TrainingAssessmentEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/TrainingAssessment/TrainingAssessmentList'))


def TrainingAssessmentEdit(request , id):
    if request.method == "POST":
        TrainingDate = request.POST["TrainingDate"] 
        EmployeeCode = request.POST["EmployeeCode"] 
        EmployeeName = request.POST["EmployeeName"] 
        EmployeeDesignation = request.POST["EmployeeDesignation"] 
        try:
            print(TrainingDate)
            TrainingDateObj = convert_date_format(TrainingDate)
            print(TrainingDateObj)
        except ValueError:
            error_message = 'Invalid date format. Please use YYYY-MM-DD.'
            TrainingDateObj = datetime.today()
            # Handle the error and render the form again with the error message.
        mem = TrainingAssessmentEntryMaster.objects.get(id = id)            
        mem.TrainingDate = TrainingDateObj
        mem.EmpCode =EmployeeCode
        mem.EmpName = EmployeeName
        mem.EmpDesignation = EmployeeDesignation
        mem.save()  
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            Status = request.POST["Status_" + str(x)]
            if(Status == ''):
                Status = ''
            TitleID_ = request.POST["TitleID_" + str(x)]
            mem1 = TrainingAssessmentEntryMaster.objects.get(id = id)
            print(id)  
            print(TitleID_)  
            sv = TrainingAssessmentEntryDetails.objects.get( TrainingAssessmentEntryMaster = id , TrainingAssessmentMaster = TitleID_)
            sv.Status = Status
            sv.save()
                                                        
        return(redirect('/TrainingAssessment/TrainingAssessmentList'))   
    #mem1 = TrainingAssessmentEntryDetails.objects.filter(TrainingAssessmentEntryMaster=id,IsDelete = False).select_related("TrainingAssessmentMaster")
    mem1 = TrainingAssessmentEntryDetails.objects.filter(TrainingAssessmentEntryMaster=id,IsDelete = False).select_related("TrainingAssessmentMaster")
    # subquery = TrainingAssessmentEntryDetails.objects.filter(TrainingAssessmentEntryMaster=id)
    # # Main query to perform right outer join-like operation
    # query = TrainingAssessmentMaster.objects.annotate(
    #     matching_details_id=Subquery(subquery.values('TrainingAssessmentMaster')),
    #     entry_amount=Subquery(subquery.values('Amount')),
    #     entry_type=Subquery(subquery.values('Isapplicable')),
    #     entry_remarks=Subquery(subquery.values('Remakrs'))
    # ).filter(matching_details_id=F('id'))
    # results = query.values()
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    mem = TrainingAssessmentEntryMaster.objects.get(id = id)
    return render(request,'TrainingAssessment/TrainingAssessmentEdit.html',{'mem':mem , 'mem1':mem1 ,'d':d})



def TrainingAssessmentviewdata(request,id):
  
    template_path = "TrainingAssessment/TrainingAssessmentviewdata.html"
    mem1 = TrainingAssessmentEntryDetails.objects.filter(TrainingAssessmentEntryMaster=id,IsDelete = False).select_related("TrainingAssessmentMaster")
    mem = TrainingAssessmentEntryMaster.objects.get(id = id)
    
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    mydict={'mem':mem,'mem1':mem1 ,'CMonth':CMonth }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
   
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
  
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 