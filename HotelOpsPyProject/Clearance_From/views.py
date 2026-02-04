from django.shortcuts import render,get_object_or_404


from hotelopsmgmtpy.GlobalConfig import MasterAttribute

from django.shortcuts import render, redirect
from .models import MasterClearanceItem,MasterReturnItem,ClearenceEmp,ClearanceItemDetail,ReturnItemDetail
from django.utils import timezone
from django.contrib import messages

def add_item(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    if request.method == "POST":
        approved_item = request.POST.get('ApprovedItem')
        
        
        
        if approved_item:  
            item = MasterClearanceItem(
                ApprovedItem=approved_item,
                OrganizationID=OrganizationID,
                CreatedBy=UserID,
              
            )
            item.save()
            messages.success(request, 'Item added successfully!')
            return redirect('MasterClearanceApproved')  
        else:
            messages.error(request, 'Please provide an item name.')
    
    return redirect('MasterClearanceApproved')  

from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def edit_clearance(request):
    if request.method == 'POST':
        clearance_id = request.POST.get('clearance_id')
        item_title = request.POST.get('item_title')

        
        clearance = get_object_or_404(MasterClearanceItem, id=clearance_id)
        
        # Update the fields with new data
        clearance.ApprovedItem = item_title
        clearance.save()

        return JsonResponse({'message': 'Item updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def MasterClearanceApproved(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    clearances = MasterClearanceItem.objects.filter(IsDelete=False)  
    context={'clearances':clearances}
    return render(request,'Clearance/MasterClearanceApproved.html',context)



def MasterClearanceItemDelete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    cle=MasterClearanceItem.objects.get(id=id)
    cle.IsDelete=True
    cle.ModifyBy=UserID
    cle.save()

    
    return redirect('MasterClearanceApproved')



def ReturnAdd(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    if request.method == "POST":
        ItemTitle = request.POST.get('ItemTitle')
        Department = request.POST.get('Department')
        MasterReturnItem.objects.create(
            ItemTitle=ItemTitle,
            Department=Department,
            OrganizationID=OrganizationID,
            CreatedBy=UserID,

            )
        messages.success(request, 'ReturnAdd Item successfully!')


    return redirect('MasterReturnlist')  
     






def MasterReturnlist(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    returns = MasterReturnItem.objects.filter(IsDelete=False)  
    context={'returns':returns}
    return render(request,'Clearance/MasterReturnlist.html',context)
     
def ReturnEdit(request):
    if 'OrganizationID' not in request.session:
            return redirect(MasterAttribute.Host)
    else:
            print("Show Page Session")
    
    
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    if request.method == 'POST':
        item_id = request.POST.get('id')
        item_title = request.POST.get('ItemTitle')
        department = request.POST.get('Department')
        
        item = get_object_or_404(MasterReturnItem, id=item_id)
        item.ItemTitle = item_title
        item.Department = department
        item.ModifyBy=UserID
        item.save()
        messages.success(request, 'Return Edit  Item successfully!')
        return redirect('MasterReturnlist')
    return redirect('MasterReturnlist')


def ClearanceDelete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    ret=MasterReturnItem.objects.get(id=id)
    ret.IsDelete=True
    ret.ModifyBy=UserID
    ret.save()

    
    return redirect('MasterReturnlist')

from HumanResources.views import EmployeeNameandDesignation




from django.shortcuts import render, redirect, get_object_or_404
from .models import ClearenceEmp, MasterClearanceItem, ClearanceItemDetail, MasterReturnItem, ReturnItemDetail
from django.utils import timezone
from django.contrib import messages
from app.models import OrganizationMaster
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import ClearenceEmp, ClearanceItemDetail, ReturnItemDetail, MasterClearanceItem, MasterReturnItem

from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from HumanResources.views import EmployeeDetailsData,HrManagerNameandDesignation,ManagerNameandDesignation
from django.urls import reverse

def ClearanceFrom(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')  

    OrganizationID = request.session.get("OrganizationID")
    OID  = request.GET.get('OID')
    Page  = request.GET.get('Page')

    if OID:
            OrganizationID= OID
    UserID = str(request.session.get("UserID"))

    empNames = EmployeeNameandDesignation(request, OrganizationID) 
    clearancesdata = MasterClearanceItem.objects.filter(IsDelete=False)  
    returndata = MasterReturnItem.objects.filter(IsDelete=False)  
    clearance_items  = None
    return_items  = None
    clearance_emp = None
    clearance_emp_id = request.GET.get('ID')
    EmpID  = request.GET.get('EmpID')
    EmpCode  = request.GET.get('EC')
    
    
    EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
    clearance_emp = {
        'EmpCode': EmpDetails.EmployeeCode,
        'Name': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
       
        'Position': EmpDetails.Designation,
        'DateofJoining' : EmpDetails.DateofJoining,
      
    }
    
   
    if EmpCode is not None:
        if clearance_emp_id:
            try:
                clearance_emp = ClearenceEmp.objects.get(id=clearance_emp_id)
                

                for cl in clearancesdata:
                    cl.ItemStatus = 0
                    clearance_items = ClearanceItemDetail.objects.filter(ClearenceEmp=clearance_emp,MasterClearanceItem=cl)
                    if clearance_items.exists():
                        cl.ItemStatus =  clearance_items[0].ItemStatus

                for rd in returndata:
                    rd.ReturndataStatus = 0
                    rd.ReceivedName = 0

                    return_items = ReturnItemDetail.objects.filter(ClearenceEmp=clearance_emp,MasterReturnItem=rd)

                    if return_items.exists():
                        rd.ReturndataStatus =  return_items[0].ReturndataStatus
                        rd.ReceivedName =  return_items[0].ReceivedName


                
            except ClearenceEmp.DoesNotExist:
                clearance_emp = None
                

    if request.method == "POST":
        
        EmpCode = request.POST.get('EmpCode')
        Name = request.POST.get('Name')
        Position = request.POST.get('Position')
        SeparationDate = request.POST.get('SeparationDate')
        FinishingTime = request.POST.get('FinishingTime')

       
        if clearance_emp and clearance_emp_id :
            clearance_emp.EmpCode = EmpCode
            clearance_emp.Position = Position
            clearance_emp.Name = Name
            clearance_emp.SeparationDate = SeparationDate
            clearance_emp.FinishingTime = FinishingTime
            clearance_emp.ModifyBy = UserID
            clearance_emp.ModifyDateTime = datetime.now()

            clearance_emp.save()
        else:
            clearance_emp = ClearenceEmp.objects.create(
                EmpCode=EmpCode,
                Position=Position,
                Name=Name,
                SeparationDate=SeparationDate,
                FinishingTime=FinishingTime,
                OrganizationID=OrganizationID,
                CreatedBy=UserID
            )

       # Process clearance data items
        Totalclearancesdata = int(request.POST.get("Totalclearancesdata", 0))
        for i in range(Totalclearancesdata + 1):
            clearancesdata_key = f"clearancesdata_ID_{i}"
            clearancesdata_value = request.POST.get(clearancesdata_key)

            if clearancesdata_value:
                try:
                    mexit = MasterClearanceItem.objects.get(id=clearancesdata_value)
                except MasterClearanceItem.DoesNotExist:
                    continue

                ItemStatus_key = f"ItemStatus_{i}"
                ItemStatus_value = int(request.POST.get(ItemStatus_key, 0))

                # Debugging output
           
                ClearanceItemDetail.objects.update_or_create(
                    MasterClearanceItem=mexit,
                    ClearenceEmp=clearance_emp,
                    defaults={
                        'ItemStatus': ItemStatus_value,
                        'OrganizationID': OrganizationID,
                        'CreatedBy': UserID,
                    }
                )

        
        Totalreturndata = int(request.POST.get("Totalreturndata", 0))
        for i in range(Totalreturndata + 1):
            returndata_key = f"returndata_ID_{i}"
            returndata_value = request.POST.get(returndata_key)

            if returndata_value:
                try:
                    returndat = MasterReturnItem.objects.get(id=returndata_value)
                except MasterReturnItem.DoesNotExist:
                    continue

                ReturndataStatus_key = f"ReturndataStatus_{i}"
                ReturndataStatus_value = int(request.POST.get(ReturndataStatus_key, 0))
                ReceivedName_key = f"ReceivedName_{i}"
                ReceivedName_value = request.POST.get(ReceivedName_key, 0)

              
                ReturnItemDetail.objects.update_or_create(
                    MasterReturnItem=returndat,
                    ClearenceEmp=clearance_emp,
                    defaults={
                        'ReturndataStatus': ReturndataStatus_value,
                        'ReceivedName': ReceivedName_value,
                        'OrganizationID': OrganizationID,
                        'CreatedBy': UserID,
                    }
                )


        # messages.success(request, "Clearance data saved successfully.")
        # return redirect('ClearanceFromlist')

        if  Page == "ClearanceFromlist":
             return redirect('ClearanceFromlist')
        Success = True        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('Clearance_From')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
        return redirect(redirect_url)
    
    context = {
        'clearancesdata': clearancesdata,
        'returndata': returndata,
        'empNames': empNames,
        'today': timezone.now().date(),
        'clearance_emp': clearance_emp,
        'clearance_items': clearance_items if clearance_emp else None,
        'return_items': return_items if return_items else None,
    }
                                  
    
    return render(request, 'Clearance/ClearanceFrom.html', context)









def ClearancefromDelete(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
  
   
    OrganizationID =request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID =str(request.session["UserID"])
    id=request.GET.get('ID')
    EmpID=request.GET.get('EmpID')

    cle=ClearenceEmp.objects.get(id=id)
    cle.IsDelete=True
    cle.ModifyBy=UserID
    cle.save()

    Success = 'Deleted'        
    encrypted_id = encrypt_id(EmpID)
    url = reverse('Clearance_From')  
    redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
    return redirect(redirect_url)    
   
from django.db.models import Subquery, OuterRef
from HumanResources.models import EmployeePersonalDetails
def ClearanceFromlist(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    if UserID=="20201212180048":
        OrganizationID=501
        
    emp_id_subquery = Subquery(
        EmployeePersonalDetails.objects.filter(
            EmployeeCode=OuterRef('EmpCode'),
            IsDelete=False
        ).values('EmpID')[:1]
    )

    ClearanceFromdatas = ClearenceEmp.objects.filter(OrganizationID=OrganizationID,IsDelete=False).annotate(
        EmpID=emp_id_subquery)

    item_statuses = {}
    for item in ClearanceItemDetail.objects.filter(IsDelete=False):
        emp_id = item.ClearenceEmp.id
        if emp_id not in item_statuses:
            item_statuses[emp_id] = {}
        item_statuses[emp_id][item.MasterClearanceItem.id] = item.ItemStatus

    context = {'ClearanceFromdatas': ClearanceFromdatas, 'item_statuses': item_statuses}
    return render(request, 'Clearance/ClearanceFromlist.html', context)


from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from django.template.loader import get_template
from xhtml2pdf import pisa  

def generate_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

from datetime import datetime
from django.utils import timezone  


def ClearancePdf(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    
    
    emp_id = request.GET.get('ID')
    
    
    emp_data = get_object_or_404(ClearenceEmp, id=emp_id)
    
    
    masterempsdetalis = MasterClearanceItem.objects.filter(IsDelete=False)
    empsdetalis = ClearanceItemDetail.objects.filter(IsDelete=False,ClearenceEmp=emp_data)
     
    empmasterreturn=MasterReturnItem.objects.filter(IsDelete=False) 
    empdetailsdatas=ReturnItemDetail.objects.filter(IsDelete=False,ClearenceEmp=emp_data)
    context = {
        'emp_data': emp_data,
        'organization_logos':organization_logos,
        'current_datetime':current_datetime,
        'empsdetalis':empsdetalis,
        'masterempsdetalis':masterempsdetalis,
        'organization_logo':organization_logo,
        'empmasterreturn':empmasterreturn,
        'empdetailsdatas':empdetailsdatas,

    }
    return generate_pdf( 'Clearance/ClearancePdf.html',context)
     
