from django.shortcuts import render,redirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from .models import hiring_data_NEW
from django.shortcuts import get_object_or_404
# Create your views here.
# def home(request):
    # pass
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def HiringAdd(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
  
   
     OrganizationID =request.session["OrganizationID"]
     UserID =str(request.session["UserID"])
     hiring_id=request.GET.get('ID')
     hiring = None

     if hiring_id is not None:
       hiring = get_object_or_404(hiring_data_NEW,id=hiring_id,OrganizationID=OrganizationID)
     if request.method=="POST":
         if hiring_id is not None:
            hiring.department_division= request.POST['department_division']
            hiring.positions1= request.POST['positions1']
            hiring.positions2= request.POST['positions2']
            hiring.positions3= request.POST['positions3']
            hiring.positions4= request.POST['positions4']
            hiring.reporting= request.POST['reporting']
            hiring.Feedback_percent1= request.POST['Feedback_percent1']
            hiring.Feedback_percent2= request.POST['Feedback_percent2']
            hiring.Feedback_percent3= request.POST['Feedback_percent3']
            hiring.Feedback_percent4= request.POST['Feedback_percent4']
            hiring.Feedback_position1= request.POST['Feedback_position1']
            hiring.Feedback_position2= request.POST['Feedback_position2']
            hiring.Feedback_position3= request.POST['Feedback_position3']
            hiring.Feedback_position4= request.POST['Feedback_position4']
            hiring.hiring= request.POST['hiring']
            hiring.fairing=request.POST['fairing']
            hiring.property_transfer= request.POST['property_transfer']
            hiring.ModifyBy =UserID
            hiring.save()
         else: 
            
            department_division= request.POST['department_division']
            positions1= request.POST['positions1']
            positions2= request.POST['positions2']
            positions3= request.POST['positions3']
            positions4= request.POST['positions4']
            reporting= request.POST['reporting']
            Feedback_percent1= request.POST['Feedback_percent1']
            Feedback_percent2= request.POST['Feedback_percent2']
            Feedback_percent3= request.POST['Feedback_percent3']
            Feedback_percent4= request.POST['Feedback_percent4']
            Feedback_position1= request.POST['Feedback_position1']
            Feedback_position2= request.POST['Feedback_position2']
            Feedback_position3= request.POST['Feedback_position3']
            Feedback_position4= request.POST['Feedback_position4']
            hiring= request.POST['hiring']
            fairing=request.POST['fairing']
            property_transfer= request.POST['property_transfer']
            Hiring =hiring_data_NEW.objects.create(department_division=department_division,
                                                positions1=positions1,
                                                positions2=positions2,
                                                positions3=positions3,
                                                positions4=positions4,
                                                reporting=reporting,
                                                Feedback_percent1=Feedback_percent1,
                                                Feedback_percent2=Feedback_percent2,
                                                         Feedback_percent3=Feedback_percent3,
                                                         Feedback_percent4=Feedback_percent4,
                                                         Feedback_position1=Feedback_position1,
                                                         Feedback_position2=Feedback_position2,
                                                         Feedback_position3=Feedback_position3,
                                                         Feedback_position4=Feedback_position4,
                                                         hiring=hiring,
                                                         fairing=fairing,
                                                         property_transfer=property_transfer,
                                                         OrganizationID=OrganizationID,CreatedBy=UserID)
         return redirect('Reporting_list')
     
     context ={'hiring':hiring}
     return render(request,"Reporting/HiringAdd.html",context)


def Reporting_list(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")
  
   
     OrganizationID =request.session["OrganizationID"]
     UserID =str(request.session["UserID"])
     hiring = hiring_data_NEW.objects.filter(IsDelete=False,OrganizationID=OrganizationID)  
     context={'hiring':hiring}
     return render(request,"Reporting/Reporting_list.html",context)

def Reporting_delet(request):
    
    id=request.GET.get('ID')
    hiring=hiring_data_NEW.objects.get(id=id)
    hiring.IsDelete=True
    hiring.save()

    
    return redirect('Reporting_list')

def hiring_report(request):
   if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
   else:
        print("Show Page Session")
  
   
   OrganizationID =request.session["OrganizationID"]
   UserID =str(request.session["UserID"])
   hiring = hiring_data_NEW.objects.filter(IsDelete=False,OrganizationID=OrganizationID)  
   context={'hiring':hiring}
   return render(request,"Reporting/hiring_report.html",context)

def report_pdf(request):
   if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
   else:
        print("Show Page Session")
  
   
   OrganizationID =request.session["OrganizationID"]
   UserID =str(request.session["UserID"])
   hiring = hiring_data_NEW.objects.filter(IsDelete=False,OrganizationID=OrganizationID)  
   template_path = 'Reporting/report_pdf.html'
   context = {'hiring': hiring}
    # Create a Django response object, and specify content_type as pdf
   response = HttpResponse(content_type='application/pdf')
   response['Content-Disposition'] = 'inline; filename="report.pdf"'
    # find the template and render it.
   template = get_template(template_path)
   html = template.render(context)

    # create a pdf
   pisa_status = pisa.CreatePDF(
   html, dest=response, hiring_report=hiring_report)
    # if error then show some funny view
   if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
   return response
    