from django.shortcuts import render,redirect
from .models import *
# Create your views here.
# from .forms import Eventform 
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
import io ,os
# from .forms import EventForm
from django.http import JsonResponse 
from io import BytesIO
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse, HttpResponseRedirect
from requests import Session, post
from hotelopsmgmtpy.GlobalConfig import MasterAttribute

from django.contrib.auth.models import Group
from .models import *
from django.shortcuts import render,redirect
from xhtml2pdf import pisa
from django.template.loader import get_template
from scantybaggage import link_callback
from django.db.models import Count
from azure.storage.blob import BlobServiceClient
from django.urls import reverse_lazy, reverse
from datetime import datetime
import requests
def index(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        OrganizationID =request.session["OrganizationID"]
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
 
    
    context= {'memOrg':memOrg }
    return render(request,'salesevent/index.html',context)





def all_events(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID = request.session["OrganizationID"]
    I=""
    # if 'I' in request.GET:
    #         I= request.GET.get('I')  # Access the 'I' value from the request parameters
    #         print(I)
       
       
    # else:
    #     I = OrganizationID      

    I= request.GET.get('I')
    

    all_events = SalesEventCalendar.objects.filter(IsDelete=False, OrganizationID=I)
    event_list = []

    for event in all_events:
        event_dict = {
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime('%Y-%m-%d'),
            'end': event.end.strftime('%Y-%m-%d'),
            'OrganizationID': event.OrganizationID
        }
        event_list.append(event_dict)
   
    return JsonResponse(event_list, safe=False)



def add_event(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")


   
    UserID =str(request.session["UserID"])
   
    title = request.GET.get("title", None)
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    orgid = request.GET.get("orgid", None)
  
   
    
    start = datetime.strptime(start,"%d-%m-%Y")
    start = start.strftime("%Y-%m-%d")

    end = datetime.strptime(end,"%d-%m-%Y")
    end = end.strftime("%Y-%m-%d")

    

   
    
    id = request.GET.get("id", None)
    if id=='0':
        event = SalesEventCalendar(name=str(title), start=start,end = end,OrganizationID=orgid,CreatedBy=UserID)
        event.save()
    else:
        event = SalesEventCalendar.objects.get(id=id)
        event.start = start
        event.end = end
      
        event.name = title
        event.save()
        
    data = {}
    return JsonResponse(data)
    

def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
   
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    orgid = request.GET.get("orgid", None)

    

    event = SalesEventCalendar.objects.get(id=id)
    event.start = start
    event.end = end

   
    event.name = title
    event.OrganizationID = orgid
    event.save()
    data = {}
    return JsonResponse(data)


def remove(request):
    id = request.GET.get("id", None)
    event = SalesEventCalendar.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)