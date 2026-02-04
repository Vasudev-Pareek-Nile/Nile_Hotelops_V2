from django.shortcuts import render,redirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
import requests
from django.contrib import messages

from django.db import   transaction
from .models import Salary_Correction
import locale
from django.shortcuts import get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO    
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.shortcuts import redirect
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa


def ListSC(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
     
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    locale.setlocale(locale.LC_NUMERIC, 'en_IN')
    Salaries  = Salary_Correction.objects.filter(OrganizationID=OrganizationID,IsDelete=False).order_by("-id")
    for salary_correction in Salaries:
        
        formatted_Current_Salary  = locale.format_string("%.2f",salary_correction.Current_Salary,grouping=True)
        salary_correction.Current_Salary = formatted_Current_Salary
        formatted_salary = locale.format_string("%.2f", salary_correction.Proposed_Salary, grouping=True)
        salary_correction.Proposed_Salary = formatted_salary



   
    context = {'Salaries':Salaries}
    return render(request, 'Salary_Correction/List.html',context)


@transaction.atomic()
def Correction(request): 
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
     
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
   
    hotelapitoken = MasterAttribute.HotelAPIkeyToken 
    ID  = request.GET.get('ID')
    cor_obj = None
    if ID is not None:
        cor_obj = get_object_or_404(Salary_Correction,id=ID,IsDelete=False)

    with transaction.atomic():
        if request.method == "POST":
            if ID is not None:
                    cor_obj.Name = request.POST['Name'] or ''
                    cor_obj.EmployeeCode = request.POST['EmployeeCode'] or ''
                    cor_obj.Date  = request.POST['Date'] 
                    cor_obj.Department = request.POST['Department'] or ''
                    cor_obj.Designation = request.POST['Designation'] or ''
                    cor_obj.Current_Salary = request.POST['Current_Salary'] or 0.00
                   
                    cor_obj.Date_of_Last_salary_review = request.POST['Date_of_Last_salary_review']
                    cor_obj.Last_Increment_Amount = request.POST['Last_Increment_Amount'] or ''
                    Slab = request.POST.get('Slab') 
                    cor_obj.Proposed_Salary = request.POST['Proposed_Salary'] or 0.00
                    cor_obj.Effective_Date = request.POST['Effective_Date']
                    cor_obj.Justification_Request = request.POST['Justification_Request'] or ''
        
                    Last_Increment_Slab_3 = False
                    Last_Increment_Slab_5 = False
                    Last_Increment_Slab_8 = False
                    Last_Increment_Slab_None = False

                    if Slab == "3":
                        Last_Increment_Slab_3 =True
                    if Slab == "5":
                        Last_Increment_Slab_5  = True
                    if Slab == "8":
                        Last_Increment_Slab_8  = True
                    if Slab == "None":
                        Last_Increment_Slab_None  = True       

                    cor_obj.Last_Increment_Slab_3 = Last_Increment_Slab_3
                    cor_obj.Last_Increment_Slab_5 = Last_Increment_Slab_5
                    cor_obj.Last_Increment_Slab_8 = Last_Increment_Slab_8
                    cor_obj.Last_Increment_Slab_None = Last_Increment_Slab_None
                    
                    cor_obj.ModifyBy = UserID
                    cor_obj.save()

                    messages.success(request,'Employee Salary Correction Record is Updated Successfully!')
            else:        
                    Name = request.POST['Name'] or ''
                    EmployeeCode = request.POST['EmployeeCode'] or ''
                    Date  = request.POST['Date'] 
                    Department = request.POST['Department'] or ''
                    Designation = request.POST['Designation'] or ''
                    Current_Salary = request.POST['Current_Salary'] or ''
                    Date_of_Last_salary_review = request.POST['Date_of_Last_salary_review']
                    Last_Increment_Amount = request.POST['Last_Increment_Amount'] or 0.00
                    Slab = request.POST.get('Slab') 
                    Proposed_Salary = request.POST['Proposed_Salary'] or 0.00
                    Effective_Date = request.POST['Effective_Date']
                    Justification_Request = request.POST['Justification_Request'] or ''
        
                    Last_Increment_Slab_3 = False
                    Last_Increment_Slab_5 = False
                    Last_Increment_Slab_8 = False
                    Last_Increment_Slab_None = False

                    if Slab == "3":
                        Last_Increment_Slab_3 =True
                    if Slab == "5":
                        Last_Increment_Slab_5  = True
                    if Slab == "8":
                        Last_Increment_Slab_8  = True
                    if Slab == "None":
                        Last_Increment_Slab_None  = True       



                    cor_obj = Salary_Correction.objects.create(
                        Name = Name,
                        OrganizationID = OrganizationID,
                        CreatedBy = UserID,
                        Date = Date ,
                        EmployeeCode = EmployeeCode,
                        Department = Department,
                        Designation = Designation,
                        Current_Salary =Current_Salary,
                        Date_of_Last_salary_review = Date_of_Last_salary_review,
                        Last_Increment_Amount = Last_Increment_Amount,
                        Last_Increment_Slab_3 = Last_Increment_Slab_3,
                        Last_Increment_Slab_5 = Last_Increment_Slab_5,
                        Last_Increment_Slab_8 = Last_Increment_Slab_8,
                        Last_Increment_Slab_None = Last_Increment_Slab_None, 
                    Proposed_Salary  = Proposed_Salary,
                        Effective_Date = Effective_Date,
                        Justification_Request =Justification_Request
                    )     
                    messages.success(request,'Employee Salary Correction Record is created Successfully!')




            return redirect('ListSC')
        

    context = {'cor_obj':cor_obj,'OrganizationID':OrganizationID,'hotelapitoken':hotelapitoken}
    return render(request, 'Salary_Correction/Correction.html',context)

@transaction.atomic()
def DeleteSC(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
     
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    ID  = request.GET.get('ID')
    with transaction.atomic():
        cor_obj = Salary_Correction.objects.get(id=ID,IsDelete=False)
        cor_obj.IsDelete  = True
        cor_obj.ModifyBy = UserID
        cor_obj.save()
        messages.warning(request,'Employee Salary Correction Record is Deleted Successfully!')
        return redirect('ListSC')

     
# from app.models import OrganizationMaster

def ViewSC(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
        
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"]) 
    # org_Details  =  OrganizationMaster.objects.get(OrganizationID= OrganizationID)
    ID  = request.GET.get('ID')
    cor_obj = Salary_Correction.objects.get(id=ID,IsDelete=False)
    locale.setlocale(locale.LC_NUMERIC, 'en_IN')
    # print(cor_obj.Proposed_Salary)
    # print(cor_obj.Current_Salary)

    formatted_Current_Salary  = locale.format_string("%.2f",cor_obj.Current_Salary,grouping=True)
    
    formatted_Proposed_Salary = locale.format_string("%.2f", cor_obj.Proposed_Salary, grouping=True)
    formatted_Last_Increment_Amount = locale.format_string("%.2f", cor_obj.Last_Increment_Amount, grouping=True)

   
    template_path = "Salary_Correction/View.html"
    mydict = {'cor_obj':cor_obj,'org_Details':'','formatted_Proposed_Salary':formatted_Proposed_Salary,'formatted_Current_Salary':formatted_Current_Salary
,  'formatted_Last_Increment_Amount':formatted_Last_Increment_Amount             }  

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="padp.pdf"'
    
    template = get_template(template_path)
    html = template.render(mydict)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
    
    

    

