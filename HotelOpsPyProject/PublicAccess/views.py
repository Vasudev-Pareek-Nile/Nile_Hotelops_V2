
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.apps import apps
from django.http import HttpResponse
from .models import PublicAccessUrl
from Letterofintent.views import GenerateDataLink
from hotelopsmgmtpy.utils import decrypt_id
from django.shortcuts import render
from django.http import HttpResponse
import datetime
def Accept(request, token):
    public_url = PublicAccessUrl.objects.filter(UniqueToken=token).first()
    
    if public_url is None:
        return render(request, 'Public/message.html', {
            'title': 'Not Found',
            'message': 'This link is not valid.'
        }, status=404)
    
    if public_url.is_expired():
        return render(request, 'Public/message.html', {
            'title': 'Link Expired',
            'message': 'This link has expired.'
        }, status=410)

    if public_url.IsClicked:
        return render(request, 'Public/message.html', {
            'title': 'Already Submitted',
            'message': 'You have already submitted your response.'
        }, status=410)

    public_url.IsClicked = True
    public_url.LastClicked = timezone.now()
    public_url.save()

    model_class = apps.get_model(public_url.AppName, public_url.ModelName)
    
    ID = decrypt_id(public_url.InstanceId)
    
    instance = get_object_or_404(model_class, id=ID)

    if hasattr(instance, 'LOIStatus'):
        instance.LOIStatus = 'Accepted'
        instance.LastLoistatusModifyDate = datetime.datetime.now()
              
        
        GenerateDataLink(request, instance.OrganizationID, instance.id)
        instance.save()

    message = "Your acceptance of the offer has been recorded. For more details, check your mail."
    context = {
        'message': message
    }

    return render(request, 'Public/message.html', context)