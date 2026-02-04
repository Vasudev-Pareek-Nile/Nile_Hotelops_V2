from argparse import REMAINDER
from copyreg import remove_extension
from datetime import date
import datetime
import copy
from decimal import Decimal
from io import BytesIO
#from django.db.models import Sum
import json
from django.db import router
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
import requests
from FixedExpense.models import FixedExpenseEntryDetails, FixedExpenseEntryMaster, FixedExpenseMaster ,FixedExpenseDepartmentMaster
from app.models import MonthListMaster
from django.db.models import Subquery,Sum
from django.db.models import OuterRef
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.db import connection
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import JsonResponse
from datetime import datetime
from django.utils.safestring import mark_safe
from django.db.models import Case, When, Value, OuterRef, Subquery
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


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



 
def  FixedExpenseHotelYearlyReport(request):
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


    Expapi_url = "https://hotelops.in/API/PyFixedExpenseAPI/FixedExpense_Hotel_Yearly_Report?OrganizationID="+str(I)+"&EntryYear="+str(EntryYear)
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

    return render(request, 'FixedExpense/FixedExpenseHotelYearlyReport.html' ,context) 


def  FixedExpenseHotelCombineMontlyReport(request):
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
    
        


    Expapi_url = "https://hotelops.in/API/PyFixedExpenseAPI/FixedExpense_HotelCombine_Monthly_Report?EntryMonth="+str(EntryMonth)+"&EntryYear="+str(EntryYear)
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

    return render(request, 'FixedExpense/FixedExpenseHotelCombineMontlyReport.html' ,context) 

 
def  FixedExpenseList(request):
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
    api_url = "https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID="+str(OrganizationID)
    # response = requests.get(api_url, headers=headers)
    # # response_content = response.content.decode('utf-8')
    # mem = response.json()

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        memOrg = response.json()
      #  return JsonResponse(mem)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    I=""
    if 'I' in request.GET:
        I=request.GET["I"]
    else:
        I = OrganizationID
    mem = FixedExpenseEntryMaster.objects.filter(IsDelete=False,OrganizationID=I).annotate(
    Monthtitle=Subquery(MonthListMaster.objects.filter(id=OuterRef('EntryMonth')).values('MonthName')[:1])
        ).order_by('-EntryYear','-EntryMonth').values()       
    
    return render(request, 'FixedExpense/FixedExpenseList.html' ,{'mem' :mem,'memOrg':memOrg }) 

   
   
def FixedExpenseEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session['OrganizationID']
    UserID = str(request.session["UserID"])
    d = {"OrganizationID":OrganizationID,"UserID":UserID}
    
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"] 
        EntryYear = request.POST["EntryYear"] 
        
        enmaster= FixedExpenseEntryMaster.objects.create(EntryMonth=EntryMonth,EntryYear=EntryYear,Total=0,OrganizationID=OrganizationID,CreatedBy=UserID)
        enmaster.save()
             
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            Amount = request.POST["Amount_" + str(x)]
            if(Amount == ''):
                Amount = 0
                      
            TitleID_ = request.POST["TitleID_" + str(x)]
            Isapplicable = request.POST["Isapplicable_" + str(x)]
            Remakrs = request.POST["Remakrs_" + str(x)]
            
            TitleObje=FixedExpenseMaster.objects.get(id=TitleID_)
            EntOBj=FixedExpenseEntryMaster.objects.get(id=enmaster.pk)
              
            v = FixedExpenseEntryDetails.objects.create(Amount = Amount,
                                                       FixedExpenseMaster=TitleObje,
                                                       FixedExpenseEntryMaster= EntOBj,
                                                       Remakrs=Remakrs,Isapplicable=Isapplicable
                                                      )                        
        return(redirect('/FixedExpense/FixedExpenseList'))
    mem = FixedExpenseMaster.objects.filter(IsDelete = False).order_by("sort_order")   
    today = datetime.today()
    CYear = today.year
    CMonth = today.month
    return render(request, 'FixedExpense/FixedExpenseEntry.html' ,{'mem':mem,'CYear':range(CYear,2020,-1),'CMonth':CMonth})



def delete_FixedExpense (request,id):
    mem = FixedExpenseEntryMaster.objects.get(id = id)
    mem.IsDelete = True
    mem.ModifyBy = 1
    mem.save()
    return(redirect('/FixedExpense/FixedExpenseList'))


def FixedExpenseEdit(request , id):
    if request.method == "POST":
        EntryMonth = request.POST["EntryMonth"]
        EntryYear = request.POST["EntryYear"]
        Total = request.POST["Total"]
        
        mem = FixedExpenseEntryMaster.objects.get(id = id)            
        mem.EntryMonth = EntryMonth
        mem.EntryYear =EntryYear
        mem.Total = Total
        mem.save()  
        
        TotalItem = request.POST["TotalItem"]
        for x in range(int(TotalItem)+1):
            
            Amount = request.POST["Amount_" + str(x)]
            if(Amount == ''):
                Amount = 0

                
            TitleID_ = request.POST["TitleID_" + str(x)]
            Isapplicable = request.POST["Isapplicable_" + str(x)]
            Remakrs_ = request.POST["Remakrs_" + str(x)]
            mem1 = FixedExpenseEntryMaster.objects.get(id = id)
              
            try:
                sv = FixedExpenseEntryDetails.objects.get( FixedExpenseEntryMaster = id , FixedExpenseMaster = TitleID_)
                sv.Amount = Amount
                sv.Isapplicable=Isapplicable;
                sv.Remakrs=Remakrs_;
                sv.save()
            except ObjectDoesNotExist:
                TitleObje=FixedExpenseMaster.objects.get(id=TitleID_)
                EntOBj=FixedExpenseEntryMaster.objects.get(id=id)
                FixedExpenseEntryDetails.objects.create(Amount = Amount,
                                    FixedExpenseMaster=TitleObje,
                                    FixedExpenseEntryMaster= EntOBj,
                                    Remakrs=Remakrs_,Isapplicable=Isapplicable
                                    )                        
        return(redirect('/FixedExpense/FixedExpenseList'))   
    #mem1 = FixedExpenseEntryDetails.objects.filter(FixedExpenseEntryMaster=id,IsDelete = False).select_related("FixedExpenseMaster")
    mem1 = FixedExpenseEntryDetails.objects.filter(FixedExpenseEntryMaster=id,IsDelete = False).select_related("FixedExpenseMaster").filter(FixedExpenseMaster__IsDelete = False)
    
    Res= FixedExpenseMaster.objects.filter(IsDelete=False).order_by('sort_order')
    for i in Res:
         i.Amount=0
         o =FixedExpenseEntryDetails.objects.filter(FixedExpenseEntryMaster=id,IsDelete = False,FixedExpenseMaster=i.id)
         print(o)
         if o.exists():
             print(o[0].Amount)
             i.Amount =o[0].Amount
             i.Isapplicable=o[0].Isapplicable
             i.Remakrs=o[0].Remakrs
        #  if o is not None:
            #  i.Amount = o.Amount

    # # Get a subquery for the FixedExpenseMaster IDs present in FixedExpenseEntryDetails
    # subquery = FixedExpenseEntryDetails.objects.filter(
    # FixedExpenseMaster_id=OuterRef('id')
    # ).values('FixedExpenseMaster_id')

    # # Annotate each FixedExpenseMaster object with a flag indicating presence in FixedExpenseEntryDetails
    # mem1 = FixedExpenseMaster.objects.annotate(
    # is_present_in_entry=Case(
    #     When(id__in=Subquery(subquery), then=Value(True)),
    #     default=Value(False),
    #     output_field=models.BooleanField(),
    # )
    # )
    # print
    # subquery = FixedExpenseEntryDetails.objects.filter(FixedExpenseEntryMaster=id)
    # # Main query to perform right outer join-like operation
    # query = FixedExpenseMaster.objects.annotate(
    #     matching_details_id=Subquery(subquery.values('FixedExpenseMaster')),
    #     entry_amount=Subquery(subquery.values('Amount')),
    #     entry_type=Subquery(subquery.values('Isapplicable')),
    #     entry_remarks=Subquery(subquery.values('Remakrs'))
    # ).filter(matching_details_id=F('id'))
    # results = query.values()
    mem = FixedExpenseEntryMaster.objects.get(id = id)
    today = datetime.today()
    CYear = today.year
    CYear = int(CYear)+1   
    return render(request,'FixedExpense/FixedExpenseEdit.html',{'mem':mem , 'mem1':mem1,'Res':Res ,'CYear':range(2022,CYear) })

def indian_number_format(value):
    if value is None:
        return ""

    value_str = str(value)
    parts = value_str.split(".")

    integer_part = parts[0]
    decimal_part = parts[1] if len(parts) > 1 else "00"

    integer_part_length = len(integer_part)
    result = []
    firstt=0
    group_count = 0  # To keep track of groups of digits
    for i in range(integer_part_length - 1, -1, -1):
        result.insert(0, integer_part[i])
        group_count += 1

        if group_count == 3 and i != 0 and firstt==0:
            result.insert(0, ",")
            group_count = 0
            firstt =1


        if group_count == 2 and i != 0 and firstt==1:
            result.insert(0, ",")
            group_count = 0
            firstt =1


    formatted_integer_part = "".join(result)
    formatted_decimal_part = decimal_part.ljust(2, "0")

    return f"{formatted_integer_part}.{formatted_decimal_part}"
def FixedExpenseviewdata(request,id):
  
    template_path = "FixedExpense/FixedExpenseviewdata.html"
    mem1 = FixedExpenseEntryDetails.objects.filter(FixedExpenseEntryMaster=id,IsDelete = False, FixedExpenseEntryMaster__IsDelete=False).select_related("FixedExpenseMaster").order_by( 'FixedExpenseMaster__FixedExpenseDepartmentMaster__sort_order',
    'FixedExpenseMaster__sort_order').filter(FixedExpenseMaster__IsDelete = False)
    Resob=[]
    currentDep=''
    STotal =0
    v = copy.copy(mem1[0]) 
    #v=item
    #v.FixedExpenseMaster.title=""
    v.FixedExpenseMaster.FixedExpenseDepartmentMaster.title
    v.IsFirst=True
    v.is_ST_true=False
    v.is_Last=True
    v.is_HT_true=True
    v.is_AI_true=False
    v.Amount=0
    #v.FixedExpenseMaster.title=item.FixedExpenseMaster.FixedExpenseDepartmentMaster.title
    Resob.append(v)
    for item in mem1:
       
        if currentDep=='':
            item.IsFirst=False
        else:   
            item.IsFirst=True
        item.is_AI_true=True
        item.is_HT_true=False
        
        item.is_ST_true=False
        item.is_Last=True
        print(STotal)
       
        if  item.FixedExpenseMaster.title!="Total" and currentDep!='' and currentDep!=item.FixedExpenseMaster.FixedExpenseDepartmentMaster.title:
             
             v = copy.copy(item) 
             
             #v=item
            #  v.FixedExpenseMaster.title="Total"
             v.is_ST_true=True
             v.is_HT_true=False
             v.is_AI_true=False
             
             
             v.Amount=STotal
             #v.FixedExpenseMaster.title=item.FixedExpenseMaster.FixedExpenseDepartmentMaster.title
             Resob.append(v)

             
             item.FixedExpenseMaster.title = item.FixedExpenseMaster.title
             Resob.append(item)
            
            
             
            #  item.is_HT_true=True
            #  item.is_ST_true=False
            #  Resob.append(item)
        else:
            if currentDep=='' or currentDep!=item.FixedExpenseMaster.FixedExpenseDepartmentMaster.title:
                # x ={"Title":item.FixedExpenseMaster.FixedExpenseDepartmentMaster.title,"HT":1}
                
                item.is_HT_true=True
                
              
            else:
                item.is_HT_true = False
                item.is_AI_true=True
               
            
            
            
            Resob.append(item)
        if currentDep!='' and currentDep!=item.FixedExpenseMaster.FixedExpenseDepartmentMaster.title:
            STotal=0
        STotal = STotal+item.Amount
        currentDep=item.FixedExpenseMaster.FixedExpenseDepartmentMaster.title

    v = copy.copy(mem1[0]) 
    #v=item
    #v.FixedExpenseMaster.title=""
    v.FixedExpenseMaster.FixedExpenseDepartmentMaster.title=""
    v.IsFirst=True
    v.is_ST_true=True
    v.is_Last=False
    v.is_HT_true=False
    v.is_AI_true=False
    v.Amount=STotal
    #v.FixedExpenseMaster.title=item.FixedExpenseMaster.FixedExpenseDepartmentMaster.title
    Resob.append(v)
    mem = FixedExpenseEntryMaster.objects.get(id = id)
    for i in Resob:
        i.Amount = indian_number_format(i.Amount)
    CMonth =MasterAttribute.MonthList[mem.EntryMonth]
    
    grand_total = mem1.aggregate(total_amount=Sum('Amount'))['total_amount'] or 0
    grand_total = indian_number_format(grand_total)
    # context = {
    #     'mem1': mem1,
    #     'grand_total': grand_total,
    # }
    
    mydict={'mem':mem,'mem1':mem1,'Resob':Resob,'grand_total':grand_total ,'CMonth':CMonth }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report gcc club.pdf"'
   
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
  
    pdf  = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
    return None 



