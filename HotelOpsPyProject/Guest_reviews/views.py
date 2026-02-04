from django.shortcuts import render,redirect
from .models import  HotelStay
import requests
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from django.contrib import messages
from app.models import OrganizationMaster
# Create your views here.
def reviews_add(request):
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
    UserID =str(request.session["UserID"])
    if request.method=="POST":
      
             hotel= request.POST['hotel']

             hm = OrganizationMaster.objects.get(OrganizationID=hotel)
             sources= request.POST['sources']
             date= request.POST['date']
             image=request.FILES.get('image')
        
        # room_no= request.POST['room_no']
        # guest_name= request.POST['guest_name']
        # stay_days= request.POST['stay_days']
        # complaint= request.POST['complaint']
        # process_lapse= request.POST['process_lapse']
        # gm_comment= request.POST['gm_comment']
    #    room_no=room_no,
    #                                    guest_name=guest_name,
    #                                     stay_days=stay_days,complaint=complaint,process_lapse=process_lapse,
    #                                     gm_comment=gm_comment
             guest =HotelStay.objects.create(hotel=hm,sources=sources,date=date, image=image,OrganizationID=OrganizationID,CreatedBy=UserID)
             messages.success(request," Social Media Guest Feedback Register Successfully" )
    context= {'memOrg':memOrg }



    
    return render(request,'guest/reviews_add.html',context)


def reviews_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    if OrganizationID=="3":
        guest = HotelStay.objects.filter(IsDelete=False,OrganizationID=OrganizationID).select_related("hotel").order_by('-id')
    else:
        hm = OrganizationMaster.objects.get(OrganizationID=OrganizationID)
        guest = HotelStay.objects.filter(IsDelete=False,hotel=hm).select_related("hotel").order_by('-id');
    context={'guest':guest}
    return render(request,'guest/reviews_list.html',context)


def reviews_edit(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    guest=HotelStay.objects.get(id=id)
    if request.method=="POST":
      
        gm_date= request.POST['gm_date']
        guest_name= request.POST['guest_name']
        room_no= request.POST['room_no']
        stay_days= request.POST['stay_days']
        complaint= request.POST['complaint']
        process_lapse= request.POST['process_lapse']
        Action_Plan= request.POST['Action_Plan']
        gm_comment= request.POST['gm_comment']

        guest.gm_date=gm_date
        guest.guest_name=guest_name
        guest.room_no=room_no
        guest.stay_days=stay_days
        guest.complaint=complaint
        guest.process_lapse=process_lapse
        guest.Action_Plan=Action_Plan
        guest.gm_comment=gm_comment
        guest.ModifyBy=UserID
        guest.status = 1 
        guest.save()
        messages.success(request," GM/HM Feedback Register Successfully" )
        return redirect('Gm_list') 
    context={'guest':guest}

   
    return render(request,'guest/reviews_edit.html',context)


def Gm_list(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID = request.session["OrganizationID"]

    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {'hotel-api-token': hotelapitoken}  # Replace with your actual header key and value
    api_url = f"https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

    if OrganizationID=="3":
        queryset = HotelStay.objects.filter(IsDelete=False,OrganizationID=OrganizationID).select_related("hotel").order_by('-id');
    else:
        hm = OrganizationMaster.objects.get(OrganizationID=OrganizationID)
        queryset = HotelStay.objects.filter(IsDelete=False,hotel=hm).select_related("hotel").order_by('-id');

    # Process the filter form
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        hotel = request.GET.get('hotel')
        status = request.GET.get('status')
        process_lapse = request.GET.get('process_lapse')
        Action_Plan = request.GET.get('Action_Plan')
        gm_comment = request.GET.get('gm_comment')
        if status == 'Pending':
           status_value = 0
        elif status == 'Closed':
           status_value = 1

        filter_args = {}

        if start_date and end_date:
            filter_args['gm_date__range'] = [start_date, end_date]

        if hotel:
            filter_args['hotel'] = hotel
        if status:
             filter_args['status'] = status_value
        if process_lapse:
            filter_args['process_lapse__icontains'] = process_lapse

        if Action_Plan:
            filter_args['Action_Plan__icontains'] = Action_Plan

        if gm_comment:
             filter_args['gm_comment__icontains'] = gm_comment     

        queryset = queryset.filter(**filter_args)
        

    context = {'start_date': start_date,
        'end_date': end_date,
        'hotel': hotel,
        'status': status,
        'process_lapse': process_lapse,
        'Action_Plan': Action_Plan,
        'gm_comment': gm_comment,
        'memOrg': memOrg,
        'guests': queryset,}
    return render(request, 'guest/Gm_list.html', context)