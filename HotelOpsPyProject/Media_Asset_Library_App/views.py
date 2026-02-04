from django.shortcuts import render,redirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
import requests
from .models import Media_Asset_Library,Categories
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from PIL import Image
from moviepy.editor import VideoFileClip
from io import BytesIO
from pathlib import Path
from datetime import datetime
from pathlib import Path
from moviepy.editor import VideoFileClip
from datetime import date,timedelta
from django.core.files.storage import default_storage
from django.db.models import Q
import mimetypes
import os
from django.db import transaction


# Gallert View
def homeMedia(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
        'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = "https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID=" + str(OrganizationID)

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

    I = request.GET.get('I', OrganizationID)
    category = request.GET.get('category')
    print(category)
    query = request.GET.get('q', '')

    Media_List = Media_Asset_Library.objects.filter(For_Hotels=I, IsDelete=False).order_by("-id")

    if query:
        Media_List = Media_List.filter(
            Q(Title__icontains=query) |
           
            Q(Descriptions__icontains=query)
        )

    if category:
        Media_List = Media_List.filter(category__id=category,For_Hotels=I, IsDelete=False).order_by("-id")
    
    categories = Categories.objects.filter(IsDelete=False)
    selectedCategory = category if category else ""
    searchQuery = query if query else ""
    context = {
        'Media_List': Media_List,
        'memOrg': memOrg,
        'categories': categories,
        'I': I,
        'OrganizationID': OrganizationID,
        'selectedCategory': selectedCategory,
        'searchQuery': searchQuery, 
    }

    return render(request, "Media_Asset_Library/mediahome.html", context)

# View for view page
def view_download_Media(request,id):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    media = Media_Asset_Library.objects.get(id=id)
    hotel_name_id  = media.For_Hotels
   
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
        'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = f"https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={hotel_name_id}"


    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        memOrg = response.json()
       
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        # Handle the error as needed
    
    


    media = Media_Asset_Library.objects.get(id=id)
    
    context =  {'media':media,
                'memOrg':memOrg , 
                
                'OrganizationID':OrganizationID
                } 
    
    return render(request,"Media_Asset_Library/mediaview.html",context)
 
# Download Media View
def download_media(request, id, resolution):
    media = Media_Asset_Library.objects.get(id=id)

    if media.Media_Type == 'Image':
        image_path = media.Media.path

        original_width = media.Original_Width
        original_height = media.Original_Height

        if resolution == 'actual':
          
            image = Image.open(image_path)
        else:
          
            if resolution == 'high':
                target_width = 3840
                target_height = int((target_width / original_width) * original_height)
            elif resolution == 'medium':
                target_width = 1920
                target_height = int((target_width / original_width) * original_height)
            elif resolution == 'low':
                target_width = 1080
                target_height = int((target_width / original_width) * original_height)
            else:
                return HttpResponse("Invalid resolution")

            image = Image.open(image_path)
            image = image.resize((target_width, target_height), Image.LANCZOS)

        if image.mode == 'RGBA':
            image = image.convert('RGB')

        response = HttpResponse(content_type='image/jpeg')
        if resolution == 'actual':
            response['Content-Disposition'] = f'attachment; filename="{media.Title}_original.jpg"'
        else:
            response['Content-Disposition'] = f'attachment; filename="{media.Title}_{resolution}.jpg"'
        image.save(response, 'JPEG')
        return response
    elif media.Media_Type == 'Video' and resolution == 'actual':
        
        video_path = media.Media.path
        video_file = default_storage.open(video_path)
        mime_type, _ = mimetypes.guess_type(video_file.name)
        response = HttpResponse(content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename="{media.Title}_original.{mime_type.split("/")[1]}"'
        response.write(video_file.read())
        video_file.close()
        return response

     
    return HttpResponse("Invalid resolution or media type")




from django.http import JsonResponse
from django.shortcuts import render

@transaction.atomic()
def upload_media(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session.get("OrganizationID")
    UserID = str(request.session.get("UserID"))
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
        'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = f"https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        # Handle the error as needed

    default_expiration_date = (date.today() + timedelta(days=365)).isoformat()
    default_upload_date = date.today().isoformat()
    categories = Categories.objects.filter(IsDelete=False)
    with transaction.atomic():
       if request.method == 'POST':
        title = request.POST.get('title')
        media_files = request.FILES.getlist('media_files')
        descriptions = request.POST.get('descriptions')
        expiration_date = request.POST.get('expiration_date')
        upload_date = request.POST.get('upload_date')
        upload_by = request.POST.get('upload_by')
        for_hotels = request.POST.get('for_hotel')
        category = request.POST.get('category')

        category_id = Categories.objects.get(id=category)

        version = request.POST.get('version')
        for media in media_files:
            file_extension = Path(media.name).suffix.lower()[1:]

            if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                media_type = 'Image'
            elif file_extension in ['mp4', 'avi', 'mov']:
                media_type = 'Video'
            else:
                return JsonResponse({'success': False, 'error': f"Unsupported file type: {file_extension}"})

            media_asset = Media_Asset_Library(
                Title=title,
                Media=media,
                Descriptions=descriptions,
                Media_Type=media_type,
                Expiration_Date=datetime.strptime(expiration_date, '%Y-%m-%d').date(),
                Upload_Date=datetime.strptime(upload_date, '%Y-%m-%d').date(),
                Upload_By=upload_by,
                For_Hotels=for_hotels,
                category=category_id,
                version=version,
                OrganizationID=OrganizationID,
                CreatedBy=UserID,
            )

            media_asset.save()

            if media_type == 'Image':
                image_path = media_asset.Media.path
                image = Image.open(image_path)
                original_width, original_height = image.size
                media_asset.Original_Width = original_width
                media_asset.Original_Height = original_height
                media_asset.save()
            elif media_type == 'Video':
                video_path = media_asset.Media.path
                video_clip = VideoFileClip(video_path)
                original_width = video_clip.size[0]
                original_height = video_clip.size[1]
                media_asset.Original_Width = original_width
                media_asset.Original_Height = original_height
                media_asset.save()
        messages.success(request,"Uploaded Successfully")     
        return redirect('homeMedia')

    context = {'memOrg': memOrg,'default_expiration_date': default_expiration_date,'default_upload_date': default_upload_date,'categories':categories,'OrganizationID':OrganizationID}
    return render(request, "Media_Asset_Library/mediaupload.html", context)

# media_delete
def media_delete(request,id):
    
    media = Media_Asset_Library.objects.get(id=id)
  
    media.IsDelete=True
    media.save()
    messages.warning(request, 'Media Deleted successfully.')
    return redirect('homeMedia')


from django.urls import reverse
# edit_media
@transaction.atomic
def edit_media(request, id):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    media = Media_Asset_Library.objects.get(id=id)
    version = int(media.version) + 1
     
    
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
        'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = f"https://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        # Handle the error as needed
    categories = Categories.objects.filter(IsDelete=False) 
    with transaction.atomic():  
      if request.method == 'POST':
        media.Title = request.POST.get('title')
        media_file = request.FILES.get('media_file')
        media.Descriptions = request.POST.get('descriptions')
        media.Expiration_Date = request.POST.get('expiration_date')
        media.Upload_Date = request.POST.get('upload_date')
        media.Upload_By = request.POST.get('upload_by')
        media.For_Hotels = request.POST.get('for_hotel')
    
        media.version = version 
        category = request.POST.get('category')
        
        category_id = Categories.objects.get(id = category)
        media.category =  category_id
        if media_file:
            
            media.Media = media_file
            media.save()

            file_extension = Path(media_file.name).suffix.lower()[1:] 
            media_type = 'Image' if file_extension in ['jpg', 'jpeg', 'png', 'gif'] else 'Video' if file_extension in ['mp4', 'avi', 'mov'] else None

            if media_type is None:
                messages.error(request, 'Unsupported file type.')
                return redirect('homeMedia')

            media.Media_Type = media_type

            if media_type == 'Image':
                image_path = default_storage.path(media.Media.name)
                image = Image.open(image_path)
                original_width, original_height = image.size
                media.Original_Width = original_width
                media.Original_Height = original_height
            elif media_type == 'Video':
                video_path = default_storage.path(media.Media.name)
                video_clip = VideoFileClip(video_path)
                original_width = video_clip.size[0]
                original_height = video_clip.size[1]
                media.Original_Width = original_width
                media.Original_Height = original_height

            media.save() 
        else:
          
            media.save()

        messages.success(request, 'Media asset updated successfully.')
        I= request.POST.get('for_hotel')
        return redirect(reverse('homeMedia') + f'?I={I}')
    
    context = {'media': media, 'memOrg': memOrg,'categories':categories}
    return render(request, "Media_Asset_Library/edit_media.html", context)

