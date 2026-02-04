from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import OnRollDivisionMaster, OnRollDepartmentMaster,LavelAdd,OnRollDesignationMaster,ContractDivisionMaster,ContractDepartmentMaster,ContractDesignationMaster,ModuleMapping,BudgetMealCost,BudgetInsuranceCost,EntryActualMealCost,EntryActualInsuranceCost,EntryActualContract,EntryActualSharedServices
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from app.views import Error
from django.db.models import OuterRef,Subquery
# manage Master - Level
def laveldeta(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    OrganizationID = request.session.get("OrganizationID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
        pass
    else:
        return Error(request, "No Access")       

    lavels = LavelAdd.objects.filter(IsDelete=False)
    context = {
        'lavels': lavels,
    }
    return render(request, "manningguide/Master/laveldeta.html",context)

def Masterlavel(request):
    if request.method == "POST":
        try:
            lavelname = request.POST.get('lavelname')
            lavel_id = request.POST.get('lavel_id')

            if lavel_id:
                lavel = get_object_or_404(LavelAdd, pk=lavel_id)
                lavel.lavelname = lavelname
                lavel.save()
                messages.success(request, 'Level updated successfully!')
            else:
                LavelAdd.objects.create(lavelname=lavelname)
                messages.success(request, 'Level added successfully!')

            return redirect('laveldeta')

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('laveldeta')  

    

def level_Edit(request):
    lavel_id = request.GET.get('id')
    try:
        level = LavelAdd.objects.get(id=lavel_id)
        data = {
            'id': level.id,
            'lavelname': level.lavelname,
        }
        return JsonResponse(data)
    except LavelAdd.DoesNotExist:
        return JsonResponse({'error': 'Level not found'}, status=404)
        
        

def level_delete(request):
    id = request.GET.get('ID')
    if id:
        try:
            delete = LavelAdd.objects.get(id=id)
            delete.IsDelete = True
            delete.save()
            messages.success(request, 'Data has been deleted successfully.')
        except ContractDepartmentMaster.DoesNotExist:
            messages.error(request, 'The record you are trying to delete does not exist.')
    
    return redirect('laveldeta')  #    




# Manage Master - <br> On Roll

def homedeta(request):

    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    OrganizationID = request.session.get("OrganizationID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")       
    
    laveladds = LavelAdd.objects.filter(IsDelete=False)

    Divisionsfilter = OnRollDivisionMaster.objects.filter(IsDelete=False)
    Departmentsfilter = OnRollDepartmentMaster.objects.filter(IsDelete=False)

    departments = OnRollDepartmentMaster.objects.all().order_by('Order')
    reportings = OnRollDesignationMaster.objects.all().order_by('Order')
    divisions = OnRollDivisionMaster.objects.all().order_by('Order')

    context = {
        'Divisionsfilter': Divisionsfilter,
        'laveladds': laveladds,
        'departments': departments,
        'reportings': reportings,
        'divisions': divisions,
        'Departmentsfilter':Departmentsfilter,
    }
    return render(request, "manningguide/Master/homedeta.html", context)




def OnRollDivisionAdd(request):
    if request.method == "POST":
        DivisionName = request.POST.get('DivisionName')
        division_id = request.POST.get('division_id')
        
        if division_id:  
            try:
                division = OnRollDivisionMaster.objects.get(id=division_id)
                division.DivisionName = DivisionName
                division.save()
                messages.success(request, 'Division updated successfully!')
            except OnRollDivisionMaster.DoesNotExist:
                messages.error(request, 'Division not found!')
        else:
            
            preOrder = OnRollDivisionMaster.objects.order_by('-Order').first()
            if preOrder:
                order = preOrder.Order + 1   
            else:
                order = 999
                
            OnRollDivisionMaster.objects.create(DivisionName=DivisionName, Order=order)
            messages.success(request, 'Division added successfully!')
        
        return redirect('homedeta')



from django.http import JsonResponse

def divisions_list(request):
    division_id = request.GET.get('id')

    try:
        division = OnRollDivisionMaster.objects.get(id=division_id)
        data = {
            'id': division.id,
            'DivisionName': division.DivisionName, 
           
        }
        return JsonResponse(data)
    except OnRollDivisionMaster.DoesNotExist:
        return JsonResponse({'error': 'Division not found'}, status=404)

from django.shortcuts import get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Max
from .models import OnRollDivisionMaster


@require_POST
def move_up_viewdivisiononroll(request, id):
    division = get_object_or_404(OnRollDivisionMaster, id=id)
    if division.Order >=0:  
        try:
            swap_division = OnRollDivisionMaster.objects.get(Order=division.Order - 1)
            division.Order, swap_division.Order = swap_division.Order, division.Order
            division.save()
            swap_division.save()
            print(f"Moved up: {division.DivisionName}")
        except OnRollDivisionMaster.DoesNotExist:
            pass
        return HttpResponse('Moved Up')
    else:
        return HttpResponse('Already at the top')

@require_POST
def move_down_viewdivisiononroll(request, id):
    division = get_object_or_404(OnRollDivisionMaster, id=id)
    
    max_order = OnRollDivisionMaster.objects.aggregate(Max('Order'))['Order__max']
    
    if division.Order < max_order:
        try:
            swap_division = OnRollDivisionMaster.objects.get(Order=division.Order + 1)
            division.Order, swap_division.Order = swap_division.Order, division.Order
            division.save()
            swap_division.save()
            
            print(f"Moved down: {division.DivisionName}")
        except OnRollDivisionMaster.DoesNotExist:
            pass
        return HttpResponse('Moved Down')
    else:
        return HttpResponse('Already at the bottom')
    





   


def division_delete(request):
    id = request.GET.get('ID')
    if id:
        try:
            delete = OnRollDivisionMaster.objects.get(id=id)
            delete.IsDelete = True
            delete.save()
            messages.success(request, 'Data has been deleted successfully.')
        except OnRollDivisionMaster.DoesNotExist:
            messages.error(request, 'The record you are trying to delete does not exist.')
    
    return redirect('homedeta')  #






def OnRollDepartmentAdd(request):
    if request.method == "POST":
        department_id = request.POST.get('department_id')
        division_id = request.POST.get('DivisionID')
        department_name = request.POST.get('DepartmentName')
        
        if department_id:  
            try:
                department = OnRollDepartmentMaster.objects.get(id=department_id)
                department.OnRollDivisionMaster_id = division_id
                department.DepartmentName = department_name
                department.save()
                messages.success(request, 'Department updated successfully!')
            except OnRollDepartmentMaster.DoesNotExist:
                messages.error(request, 'Department not found!')
        else:  
            preOrder = OnRollDepartmentMaster.objects.order_by('-Order').first()
            if preOrder:
                order = preOrder.Order + 1   
            else:
                order = 999
            OnRollDepartmentMaster.objects.create(OnRollDivisionMaster_id=division_id, DepartmentName=department_name,Order=order )
            messages.success(request, 'Department added successfully!')
        
        return redirect('homedeta')

from django.http import JsonResponse

def departments_list(request):
    department_id = request.GET.get('id')

    try:
        department = OnRollDepartmentMaster.objects.get(id=department_id)
        data = {
            'id': department.id,
            'DivisionID': department.OnRollDivisionMaster_id,
            'DepartmentName': department.DepartmentName,
        }
        return JsonResponse(data)
    except OnRollDepartmentMaster.DoesNotExist:
        return JsonResponse({'error': 'Department not found'}, status=404)




@require_POST
def move_up_departmentonroll(request, id):
    department = get_object_or_404(OnRollDepartmentMaster, id=id)
    if department.Order >=0:
        try:
            swap_department = OnRollDepartmentMaster.objects.get(
                OnRollDivisionMaster=department.OnRollDivisionMaster,
                Order=department.Order - 1
            )
            department.Order, swap_department.Order = swap_department.Order, department.Order
            department.save()
            swap_department.save()
            print(f"Moved up: {department.DepartmentName}")
        except OnRollDepartmentMaster.DoesNotExist:
            pass
        return HttpResponse('Moved Up')
    else:
        return HttpResponse('Already at the top')

@require_POST
def move_down_departmentonroll(request, id):
    department = get_object_or_404(OnRollDepartmentMaster, id=id)
    max_order = OnRollDepartmentMaster.objects.filter(
        OnRollDivisionMaster=department.OnRollDivisionMaster
    ).aggregate(Max('Order'))['Order__max']
    
    if department.Order < max_order:
        try:
            swap_department = OnRollDepartmentMaster.objects.get(
                OnRollDivisionMaster=department.OnRollDivisionMaster,
                Order=department.Order + 1
            )
            department.Order, swap_department.Order = swap_department.Order, department.Order
            department.save()
            swap_department.save()
            print(f"Moved down: {department.DepartmentName}")
        except OnRollDepartmentMaster.DoesNotExist:
            pass
        return HttpResponse('Moved Down')
    else:
        return HttpResponse('Already at the bottom')


def department_delete(request):
    id = request.GET.get('ID')
    if id:
        try:
            delete = OnRollDepartmentMaster.objects.get(id=id)
            delete.IsDelete = True
            delete.save()
            messages.success(request, 'Data has been deleted successfully.')
        except OnRollDivisionMaster.DoesNotExist:
            messages.error(request, 'The record you are trying to delete does not exist.')
    
    return redirect('homedeta')  #






def OnRollDesignationAdd(request):
    if request.method == "POST":
        DivisionID = request.POST.get('DivisionID')
        DepartmentID = request.POST.get('DepartmentID')
        Div = request.POST.get('Div')
        Dept = request.POST.get('Dept')
        designations = request.POST.get('designations')
        Lavel = request.POST.get('Lavel')
        Report_Designations = request.POST.get('Report_Designations')
        designation_id = request.POST.get('designation_id')
        
        if designation_id:  
            try:
                designation = OnRollDesignationMaster.objects.get(id=designation_id)
                designation.OnRollDivisionMaster_id = DivisionID
                designation.OnRollDepartmentMaster_id = DepartmentID
                designation.Div = Div
                designation.Dept = Dept
                designation.designations = designations
                designation.Lavel = Lavel
                designation.Report_Designations = Report_Designations
                designation.save()
                messages.success(request, 'Designation updated successfully!')
            except OnRollDesignationMaster.DoesNotExist:
                messages.error(request, 'Designation not found!')
        else:  
            preOrder = OnRollDesignationMaster.objects.order_by('-Order').first()
            if preOrder:
                order = preOrder.Order + 1   
            else:
                order = 999
            OnRollDesignationMaster.objects.create(
                OnRollDivisionMaster_id=DivisionID,
                OnRollDepartmentMaster_id=DepartmentID,
                Div=Div,
                Dept=Dept,
                designations=designations,
                Lavel=Lavel,
                Report_Designations=Report_Designations,
                Order=order

            )
            messages.success(request, 'Designation added successfully!')
        
        return redirect('homedeta')

def designation_details(request):
    designation_id = request.GET.get('id')

    try:
        designation = OnRollDesignationMaster.objects.get(id=designation_id)
        data = {
            'id': designation.id,
            'DivisionID': designation.OnRollDivisionMaster_id,
            'DepartmentID': designation.OnRollDepartmentMaster_id,
            'Div': designation.Div,
            'Dept': designation.Dept,
            'designations': designation.designations,
            'Lavel': designation.Lavel,  
            'Report_Designations': designation.Report_Designations,  
        }
        return JsonResponse(data)
    except OnRollDesignationMaster.DoesNotExist:
        return JsonResponse({'error': 'Designation not found'}, status=404)

def designationadd_delete(request):
    id = request.GET.get('ID')
    if id:
        try:
            delete = OnRollDesignationMaster.objects.get(id=id)
            delete.IsDelete = True
            delete.save()
            messages.success(request, 'Data has been deleted successfully.')
        except OnRollDivisionMaster.DoesNotExist:
            messages.error(request, 'The record you are trying to delete does not exist.')
    
    return redirect('homedeta')  #





@require_POST
def move_up_designation_onroll(request, id):
    designation = get_object_or_404(OnRollDesignationMaster, id=id)
    if designation.Order >= 0:
        try:
            swap_designation = OnRollDesignationMaster.objects.get(
                OnRollDepartmentMaster=designation.OnRollDepartmentMaster,
                Order=designation.Order - 1
            )
            designation.Order, swap_designation.Order = swap_designation.Order, designation.Order
            designation.save()
            swap_designation.save()
            print(f"Moved up: {designation.designations}")
        except OnRollDesignationMaster.DoesNotExist:
            pass
        return HttpResponse('Moved Up')
    else:
        return HttpResponse('Already at the top')

@require_POST
def move_down_designation_onroll(request, id):
    designation = get_object_or_404(OnRollDesignationMaster, id=id)
    max_order = OnRollDesignationMaster.objects.filter(
        OnRollDepartmentMaster=designation.OnRollDepartmentMaster
    ).aggregate(Max('Order'))['Order__max']
    
    if designation.Order < max_order:
        try:
            swap_designation = OnRollDesignationMaster.objects.get(
                OnRollDepartmentMaster=designation.OnRollDepartmentMaster,
                Order=designation.Order + 1
            )
            designation.Order, swap_designation.Order = swap_designation.Order, designation.Order
            designation.save()
            swap_designation.save()
            print(f"Moved down: {designation.designations}")
        except OnRollDesignationMaster.DoesNotExist:
            pass
        return HttpResponse('Moved Down')
    else:
        return HttpResponse('Already at the bottom')

# Manage Master - <br> Contract




def Managecontract(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    OrganizationID = request.session.get("OrganizationID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")       
    laveladds = LavelAdd.objects.all()
    Divisionsfilter = ContractDivisionMaster.objects.filter(IsDelete=False)
    Departmentsfilter = ContractDepartmentMaster.objects.filter(IsDelete=False)
    departments = ContractDepartmentMaster.objects.all().order_by('Order')
    reportings = ContractDesignationMaster.objects.all().order_by('Order')
    divisions = ContractDivisionMaster.objects.all().order_by('Order')
    
    context = {
        'laveladds': laveladds,
        'departments': departments,
        'reportings': reportings,
        'divisions': divisions,
        'Divisionsfilter':Divisionsfilter,
        'Departmentsfilter':Departmentsfilter
    }
    return render(request, "manningguide/Master/managecontract.html", context)











def ContractDivisionAdd(request):
    if request.method == "POST":
        division_name = request.POST.get('DivisionName')
        division_id = request.POST.get('division_id')
        
        if division_id:
            try:
                division = ContractDivisionMaster.objects.get(id=division_id)
                division.DivisionName = division_name
                division.save()
                messages.success(request, 'Division updated successfully!')
            except ContractDivisionMaster.DoesNotExist:
                messages.error(request, 'Division not found!')
        else:
            preOrder = ContractDivisionMaster.objects.order_by('-Order').first()
            if preOrder:
                order = preOrder.Order + 1   
            else:
                order = 999
            ContractDivisionMaster.objects.create(DivisionName=division_name,Order=order)
            messages.success(request, 'Division added successfully!')
        
        return redirect('Managecontract')
    else:
        # Handle GET requests if needed
        pass

def Contractdivisions_list(request):
    division_id = request.GET.get('id')

    try:
        division = ContractDivisionMaster.objects.get(id=division_id)
        data = {
            'id': division.id,
            'DivisionName': division.DivisionName,
        }
        return JsonResponse(data)
    except ContractDivisionMaster.DoesNotExist:
        return JsonResponse({'error': 'Division not found'}, status=404)


@require_POST
def move_up_divisioncontract(request, id):
    division = get_object_or_404(ContractDivisionMaster, id=id)
    if division.Order >= 0:  
        try:
            swap_division = ContractDivisionMaster.objects.get(Order=division.Order - 1)
            division.Order, swap_division.Order = swap_division.Order, division.Order
            
            division.save()
            swap_division.save()
            print(f"Moved up: {division.DivisionName}")
        except ContractDivisionMaster.DoesNotExist:
            pass
        return HttpResponse('Moved Up')
    else:
        return HttpResponse('Already at the top')

@require_POST
def move_down_divisioncontract(request, id):
    division = get_object_or_404(ContractDivisionMaster, id=id)
    max_order = ContractDivisionMaster.objects.aggregate(Max('Order'))['Order__max']
    
    if division.Order < max_order:
        try:
            swap_division = ContractDivisionMaster.objects.get(Order=division.Order + 1)
            division.Order, swap_division.Order = swap_division.Order, division.Order
            
            division.save()
            swap_division.save()
            print(f"Moved down: {division.DivisionName}")
        except ContractDivisionMaster.DoesNotExist:
            pass
        return HttpResponse('Moved Down')
    else:
        return HttpResponse('Already at the bottom')




















def ContractDivision_delete(request):
    id = request.GET.get('ID')
    if id:
        try:
            delete = ContractDivisionMaster.objects.get(id=id)
            delete.IsDelete = True
            delete.save()
            messages.success(request, 'Data has been deleted successfully.')
        except ContractDivisionMaster.DoesNotExist:
            messages.error(request, 'The record you are trying to delete does not exist.')
    
    return redirect('Managecontract')  #





def ContractDepartmentAdd(request):
    if request.method == "POST":
        division_id = request.POST.get('DivisionID')
        department_name = request.POST.get('DepartmentName')
        department_id = request.POST.get('department_id')
        
        if division_id and department_name:
            if department_id:  
                try:
                    department = ContractDepartmentMaster.objects.get(id=department_id)
                    department.ContractDivisionMaster_id = division_id
                    department.DepartmentName = department_name
                    department.save()
                    messages.success(request, 'Department updated successfully!')
                except ContractDepartmentMaster.DoesNotExist:
                    messages.error(request, 'Department not found!')
            else:
                preOrder = ContractDepartmentMaster.objects.order_by('-Order').first()
                if preOrder:
                  order = preOrder.Order + 1   
                else:
                  order = 999 
                ContractDepartmentMaster.objects.create(ContractDivisionMaster_id=division_id, DepartmentName=department_name,Order=order)
                messages.success(request, 'Department added successfully!')
        
        return redirect('Managecontract')

def Contractdepartments_list(request):
    department_id = request.GET.get('id')

    try:
        department = ContractDepartmentMaster.objects.get(id=department_id)
        data = {
            'id': department.id,
            'DivisionID': department.ContractDivisionMaster_id,
            'DepartmentName': department.DepartmentName,
        }
        return JsonResponse(data)
    except OnRollDepartmentMaster.DoesNotExist:
        return JsonResponse({'error': 'Department not found'}, status=404)








def ContractDepartment_delete(request):
    id = request.GET.get('ID')
    if id:
        try:
            delete = ContractDepartmentMaster.objects.get(id=id)
            delete.IsDelete = True
            delete.save()
            messages.success(request, 'Data has been deleted successfully.')
        except ContractDepartmentMaster.DoesNotExist:
            messages.error(request, 'The record you are trying to delete does not exist.')
    
    return redirect('Managecontract')  #

@require_POST
def move_up_departmentContract(request, id):
    department = get_object_or_404(ContractDepartmentMaster, id=id)
    if department.Order >= 0:
        try:
            swap_department = ContractDepartmentMaster.objects.get(Order=department.Order - 1, ContractDivisionMaster=department.ContractDivisionMaster)
            department.Order, swap_department.Order = swap_department.Order, department.Order
            
            department.save()
            swap_department.save()
            print(f"Moved up: {department.DepartmentName}")
        except ContractDepartmentMaster.DoesNotExist:
            pass
        return HttpResponse('Moved Up')
    else:
        return HttpResponse('Already at the top')



@require_POST
def move_down_departmentContract(request, id):
    department = get_object_or_404(ContractDepartmentMaster, id=id)
    max_order = ContractDepartmentMaster.objects.filter(ContractDivisionMaster=department.ContractDivisionMaster).aggregate(Max('Order'))['Order__max']
    
    if department.Order < max_order:
        try:
            swap_department = ContractDepartmentMaster.objects.get(Order=department.Order + 1, ContractDivisionMaster=department.ContractDivisionMaster)
            department.Order, swap_department.Order = swap_department.Order, department.Order
            
            department.save()
            swap_department.save()
            print(f"Moved down: {department.DepartmentName}")
        except ContractDepartmentMaster.DoesNotExist:
            pass
        return HttpResponse('Moved Down')
    else:
        return HttpResponse('Already at the bottom')



def ContractDesignationAdd(request):
    if request.method == 'POST':
        designation_id = request.POST.get('designation_id')
        DivisionID = request.POST.get('DivisionID')
        DepartmentID = request.POST.get('DepartmentID')
        Div = request.POST.get('Div')
        Dept = request.POST.get('Dept')
        designations = request.POST.get('designations')
        Lavel = request.POST.get('Lavel')
        Report_Designations = request.POST.get('Report_Designations')
        
        if designation_id:
           
            designation = get_object_or_404(ContractDesignationMaster, id=designation_id)
            designation.ContractDivisionMaster_id = DivisionID
            designation.ContractDepartmentMaster_id = DepartmentID
            designation.Div = Div
            designation.Dept = Dept
            designation.designations = designations
            designation.Lavel = Lavel
            designation.Report_Designations = Report_Designations
            designation.save()
            messages.success(request, 'Designation updated successfully!')
        else:
            preOrder = ContractDesignationMaster.objects.order_by('-Order').first()
            if preOrder:
                  order = preOrder.Order + 1   
            else:
                  order = 999 
            designation = ContractDesignationMaster.objects.create(
                ContractDivisionMaster_id=DivisionID,
                ContractDepartmentMaster_id=DepartmentID,
                Div=Div,
                Dept=Dept,
                designations=designations,
                Lavel=Lavel,
                Report_Designations=Report_Designations,
                Order=order
            )
            messages.success(request, 'Designation added successfully!')
        
        return redirect('Managecontract')  
    
def Contractdesignation_details(request):
    designation_id = request.GET.get('id')

    try:
        designation = get_object_or_404(ContractDesignationMaster, id=designation_id)
        data = {
            'id': designation.id,
            'DivisionID': designation.ContractDivisionMaster_id,
            'DepartmentID': designation.ContractDepartmentMaster_id,
            'Div': designation.Div,
            'Dept': designation.Dept,
            'designations': designation.designations,
            'Lavel': designation.Lavel,
            'Report_Designations': designation.Report_Designations,
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)


def ContractDesignation_delete(request):
    id = request.GET.get('ID')
    if id:
        try:
            delete = ContractDesignationMaster.objects.get(id=id)
            delete.IsDelete = True
            delete.save()
            messages.success(request, 'Data has been deleted successfully.')
        except ContractDesignationMaster.DoesNotExist:
            messages.error(request, 'The record you are trying to delete does not exist.')
    
    return redirect('Managecontract') 

@require_POST
def move_up_designationContract(request, id):
    designation = get_object_or_404(ContractDesignationMaster, id=id)
    if designation.Order >= 0:
        try:
            swap_designation = ContractDesignationMaster.objects.get(
                ContractDepartmentMaster=designation.ContractDepartmentMaster,
                Order=designation.Order - 1
            )
            designation.Order, swap_designation.Order = swap_designation.Order, designation.Order
            designation.save()
            swap_designation.save()
            print(f"Moved up: {designation.designations}")
            return HttpResponse('Moved Up')
        except ContractDesignationMaster.DoesNotExist:
            pass
    return HttpResponse('Already at the top')

@require_POST
def move_down_designationContract(request, id):
    designation = get_object_or_404(ContractDesignationMaster, id=id)
    max_order = ContractDesignationMaster.objects.filter(
        ContractDepartmentMaster=designation.ContractDepartmentMaster
    ).aggregate(Max('Order'))['Order__max']
    
    if designation.Order < max_order:
        try:
            swap_designation = ContractDesignationMaster.objects.get(
                ContractDepartmentMaster=designation.ContractDepartmentMaster,
                Order=designation.Order + 1
            )
            designation.Order, swap_designation.Order = swap_designation.Order, designation.Order
            designation.save()
            swap_designation.save()
            print(f"Moved down: {designation.designations}")
            return HttpResponse('Moved Down')
        except ContractDesignationMaster.DoesNotExist:
            pass
    return HttpResponse('Already at the bottom')






# Manage Master - <br> Shared Services

from .models import ServicesDepartmentMaster,ServicesDivisionMaster,ServicesDesignationMaster

def SharedServices(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    OrganizationID = request.session.get("OrganizationID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")       
    laveladds = LavelAdd.objects.filter(IsDelete=False)
    Divisionsfilter = ServicesDivisionMaster.objects.filter(IsDelete=False)
    Departmentsfilter = ServicesDepartmentMaster.objects.filter(IsDelete=False)
    






    departments = ServicesDepartmentMaster.objects.all().order_by('Order')
    
    reportings = ServicesDesignationMaster.objects.all().order_by('Order')
    
   
    divisions = ServicesDivisionMaster.objects.all().order_by('Order')
    
    context = {
        
        'laveladds': laveladds,
        'departments': departments,
        'reportings': reportings,
        'divisions': divisions,
        'Divisionsfilter':Divisionsfilter,
        'Departmentsfilter':Departmentsfilter
        

    }
    
    return render(request, "manningguide/Master/SharedServices.html",context)



    

def Servicesdivisions_list(request):
    division_id = request.GET.get('id')
    try:
        division = ServicesDivisionMaster.objects.get(id=division_id)
        data = {
            'id': division.id,
            'DivisionName': division.DivisionName,
        }
        return JsonResponse(data)
    except ServicesDivisionMaster.DoesNotExist:
        return JsonResponse({'error': 'Division not found'}, status=404)

def ServicesDivisionAdd(request):
    if request.method == "POST":
        division_name = request.POST.get('DivisionName')
        division_id = request.POST.get('division_id')
        
        if division_id:
            try:
                division = ServicesDivisionMaster.objects.get(id=division_id)
                division.DivisionName = division_name
                division.save()
                messages.success(request, 'Division updated successfully!')
            except ServicesDivisionMaster.DoesNotExist:
                messages.error(request, 'Division not found!')
        else:
            preOrder = ServicesDivisionMaster.objects.order_by('-Order').first()
            order = preOrder.Order + 1 if preOrder else 999
            ServicesDivisionMaster.objects.create(DivisionName=division_name, Order=order)
            messages.success(request, 'Division added successfully!')
        
        return redirect('SharedServices')


@require_POST
def move_up_divisionservices(request, id):
    division = get_object_or_404(ServicesDivisionMaster, id=id)
    if division.Order > 0:
        try:
            swap_division = ServicesDivisionMaster.objects.get(Order=division.Order - 1)
            division.Order, swap_division.Order = swap_division.Order, division.Order
            division.save()
            swap_division.save()
            return HttpResponse('Moved Up')
        except ServicesDivisionMaster.DoesNotExist:
            pass
    return HttpResponse('Already at the top or error occurred')

@require_POST
def move_down_divisionservices(request, id):
    division = get_object_or_404(ServicesDivisionMaster, id=id)
    max_order = ServicesDivisionMaster.objects.aggregate(Max('Order'))['Order__max']
    if division.Order < max_order:
        try:
            swap_division = ServicesDivisionMaster.objects.get(Order=division.Order + 1)
            division.Order, swap_division.Order = swap_division.Order, division.Order
            division.save()
            swap_division.save()
            return HttpResponse('Moved Down')
        except ServicesDivisionMaster.DoesNotExist:
            pass
    return HttpResponse('Already at the bottom or error occurred')








def ServicesDepartmentAdd(request):
    if request.method == "POST":
        division_id = request.POST.get('DivisionID')
        department_name = request.POST.get('DepartmentName')
        department_id = request.POST.get('department_id')
        
        if division_id and department_name:
            if department_id:
                try:
                    department = ServicesDepartmentMaster.objects.get(id=department_id)
                    department.ServicesDivisionMaster_id = division_id
                    department.DepartmentName = department_name
                    department.save()
                    messages.success(request, 'Department updated successfully!')
                except ServicesDepartmentMaster.DoesNotExist:
                    messages.error(request, 'Department not found!')
            else:
                preOrder = ServicesDepartmentMaster.objects.order_by('-Order').first()
                order = preOrder.Order + 1 if preOrder else 999
                ServicesDepartmentMaster.objects.create(ServicesDivisionMaster_id=division_id, DepartmentName=department_name, Order=order)
                messages.success(request, 'Department added successfully!')
        
        return redirect('SharedServices')

def Servicesdepartments_list(request):
    department_id = request.GET.get('id')

    try:
        department = ServicesDepartmentMaster.objects.get(id=department_id)
        data = {
            'id': department.id,
            'DivisionID': department.ServicesDivisionMaster_id,
            'DepartmentName': department.DepartmentName,
        }
        return JsonResponse(data)
    except ServicesDepartmentMaster.DoesNotExist:
        return JsonResponse({'error': 'Department not found'}, status=404)


@require_POST
def move_up_departmentservices(request, id):
    department = get_object_or_404(ServicesDepartmentMaster, id=id)
    if department.Order > 0:
        try:
            swap_department = ServicesDepartmentMaster.objects.get(Order=department.Order - 1)
            department.Order, swap_department.Order = swap_department.Order, department.Order
            department.save()
            swap_department.save()
            return HttpResponse('Moved Up')
        except ServicesDepartmentMaster.DoesNotExist:
            pass
    return HttpResponse('Already at the top or error occurred')

@require_POST
def move_down_departmentservices(request, id):
    department = get_object_or_404(ServicesDepartmentMaster, id=id)
    max_order = ServicesDepartmentMaster.objects.filter(ServicesDivisionMaster=department.ServicesDivisionMaster).aggregate(Max('Order'))['Order__max']
    if department.Order < max_order:
        try:
            swap_department = ServicesDepartmentMaster.objects.get(Order=department.Order + 1)
            department.Order, swap_department.Order = swap_department.Order, department.Order
            department.save()
            swap_department.save()
            return HttpResponse('Moved Down')
        except ServicesDepartmentMaster.DoesNotExist:
            pass
    return HttpResponse('Already at the bottom or error occurred')










def Servicesdesignation_details(request):
    designation_id = request.GET.get('id')

    try:
        designation = ServicesDesignationMaster.objects.get(id=designation_id)
        data = {
            'id': designation.id,
            'DivisionID': designation.ServicesDivisionMaster_id,
            'DepartmentID': designation.ServicesDepartmentMaster_id,
            'Div': designation.Div,
            'Dept': designation.Dept,
            'designations': designation.designations,
            'Lavel': designation.Lavel,  
            'Report_Designations': designation.Report_Designations,  
        }
        return JsonResponse(data)
    except ServicesDesignationMaster.DoesNotExist:
        return JsonResponse({'error': 'Designation not found'}, status=404)

def ServicesDesignationAdd(request):
    if request.method == 'POST':
        designation_id = request.POST.get('designation_id')
        DivisionID = request.POST.get('DivisionID')
        DepartmentID = request.POST.get('DepartmentID')
        Div = request.POST.get('Div')
        Dept = request.POST.get('Dept')
        designations = request.POST.get('designations')
        Lavel = request.POST.get('Lavel')
        Report_Designations = request.POST.get('Report_Designations')
        
        if designation_id:
            designation = get_object_or_404(ServicesDesignationMaster, id=designation_id)
            designation.ServicesDivisionMaster_id = DivisionID
            designation.ServicesDepartmentMaster_id = DepartmentID
            designation.Div = Div
            designation.Dept = Dept
            designation.designations = designations
            designation.Lavel = Lavel
            designation.Report_Designations = Report_Designations
            designation.save()
            messages.success(request, 'Designation updated successfully!')
        else:
            preOrder = ServicesDesignationMaster.objects.order_by('-Order').first()
            order = preOrder.Order + 1 if preOrder else 999
            ServicesDesignationMaster.objects.create(
                ServicesDivisionMaster_id=DivisionID,
                ServicesDepartmentMaster_id=DepartmentID,
                Div=Div,
                Dept=Dept,
                designations=designations,
                Lavel=Lavel,
                Report_Designations=Report_Designations,
                Order=order
            )
            messages.success(request, 'Designation added successfully!')
        
        return redirect('SharedServices')


@require_POST
def move_up_designationservices(request, id):
    designation = get_object_or_404(ServicesDesignationMaster, id=id)
    if designation.Order > 0:
        try:
            swap_designation = ServicesDesignationMaster.objects.get(Order=designation.Order - 1)
            designation.Order, swap_designation.Order = swap_designation.Order, designation.Order
            designation.save()
            swap_designation.save()
            return HttpResponse('Moved Up')
        except ServicesDesignationMaster.DoesNotExist:
            pass
    return HttpResponse('Already at the top or error occurred')

@require_POST
def move_down_designationservices(request, id):
    designation = get_object_or_404(ServicesDesignationMaster, id=id)
    max_order = ServicesDesignationMaster.objects.filter(ServicesDivisionMaster=designation.ServicesDivisionMaster, ServicesDepartmentMaster=designation.ServicesDepartmentMaster).aggregate(Max('Order'))['Order__max']
    if designation.Order < max_order:
        try:
            swap_designation = ServicesDesignationMaster.objects.get(Order=designation.Order + 1)
            designation.Order, swap_designation.Order = swap_designation.Order, designation.Order
            designation.save()
            swap_designation.save()
            return HttpResponse('Moved Down')
        except ServicesDesignationMaster.DoesNotExist:
            pass
    return HttpResponse('Already at the bottom or error occurred')






def ServicesDivision_delete(request):
    id = request.GET.get('ID')
    if id:
        try:
            delete = ServicesDivisionMaster.objects.get(id=id)
            delete.IsDelete = True
            delete.save()
            messages.success(request, 'Data has been deleted successfully.')
        except ServicesDivisionMaster.DoesNotExist:
            messages.error(request, 'The record you are trying to delete does not exist.')
    
    return redirect('SharedServices')  #    

def ServicesDepartment_delete(request):
    id = request.GET.get('ID')
    if id:
        try:
            delete = ServicesDepartmentMaster.objects.get(id=id)
            delete.IsDelete = True
            delete.save()
            messages.success(request, 'Data has been deleted successfully.')
        except ServicesDepartmentMaster.DoesNotExist:
            messages.error(request, 'The record you are trying to delete does not exist.')
    
    return redirect('SharedServices')  #  


def ServicesDesignation_delete(request):
    id = request.GET.get('ID')
    if id:
        try:
            delete = ServicesDesignationMaster.objects.get(id=id)
            delete.IsDelete = True
            delete.save()
            messages.success(request, 'Data has been deleted successfully.')
        except ServicesDesignationMaster.DoesNotExist:
            messages.error(request, 'The record you are trying to delete does not exist.')
    
    return redirect('SharedServices') 



# Manage Master - <br> Corporate
from .models import CorporateDivisionMaster,CorporateDepartmentMaster,CorporateDesignationMaster

def Corporate(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    OrganizationID = request.session.get("OrganizationID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")       
    laveladds = LavelAdd.objects.filter(IsDelete=False)
    Divisionsfilter = CorporateDivisionMaster.objects.filter(IsDelete=False)
    Departmentsfilter = CorporateDepartmentMaster.objects.filter(IsDelete=False)
    






    departments = CorporateDepartmentMaster.objects.filter(IsDelete=False).order_by('Order')
    
    reportings = CorporateDesignationMaster.objects.filter(IsDelete=False).order_by('Order')
    
   
    divisions = CorporateDivisionMaster.objects.filter(IsDelete=False).order_by('Order')
    
    context = {
        
        'laveladds': laveladds,
        'departments': departments,
        'reportings': reportings,
        'divisions': divisions,
        'Divisionsfilter':Divisionsfilter,
        'Departmentsfilter':Departmentsfilter
        

    }
    return render(request, "manningguide/Master/Corporate.html",context)


  
def CorporateDivisionAdd(request):
    if request.method == "POST":
        division_name = request.POST.get('DivisionName')
        division_id = request.POST.get('division_id')
        
        if division_id:
            try:
                division = CorporateDivisionMaster.objects.get(id=division_id)
                division.DivisionName = division_name
                division.save()
                messages.success(request, 'Division updated successfully!')
            except CorporateDivisionMaster.DoesNotExist:
                messages.error(request, 'Division not found!')
        else:
            preOrder = CorporateDivisionMaster.objects.order_by('-Order').first()
            order = preOrder.Order + 1 if preOrder else 999
            CorporateDivisionMaster.objects.create(DivisionName=division_name, Order=order)
            messages.success(request, 'Division added successfully!')
        
        return redirect('Corporate')


@require_POST
def move_up_divisionCorporate(request, id):
    division = get_object_or_404(CorporateDivisionMaster, id=id)
    if division.Order > 0:
        try:
            swap_division = CorporateDivisionMaster.objects.get(Order=division.Order - 1)
            division.Order, swap_division.Order = swap_division.Order, division.Order
            division.save()
            swap_division.save()
            return HttpResponse('Moved Up')
        except CorporateDivisionMaster.DoesNotExist:
            pass
    return HttpResponse('Already at the top or error occurred')

@require_POST
def move_down_divisionCorporate(request, id):
    division = get_object_or_404(CorporateDivisionMaster, id=id)
    max_order = CorporateDivisionMaster.objects.aggregate(Max('Order'))['Order__max']
    if division.Order < max_order:
        try:
            swap_division = CorporateDivisionMaster.objects.get(Order=division.Order + 1)
            division.Order, swap_division.Order = swap_division.Order, division.Order
            division.save()
            swap_division.save()
            return HttpResponse('Moved Down')
        except CorporateDivisionMaster.DoesNotExist:
            pass
    return HttpResponse('Already at the bottom or error occurred')


def CorporateDepartmentAdd(request):
    if request.method == "POST":
        division_id = request.POST.get('DivisionID')
        department_name = request.POST.get('DepartmentName')
        department_id = request.POST.get('department_id')
        
        if division_id and department_name:
            if department_id:
                try:
                    department = CorporateDepartmentMaster.objects.get(id=department_id)
                    department.CorporateDivisionMaster_id = division_id
                    department.DepartmentName = department_name
                    department.save()
                    messages.success(request, 'Department updated successfully!')
                except CorporateDepartmentMaster.DoesNotExist:
                    messages.error(request, 'Department not found!')
            else:
                preOrder = CorporateDepartmentMaster.objects.order_by('-Order').first()
                order = preOrder.Order + 1 if preOrder else 999
                CorporateDepartmentMaster.objects.create(CorporateDivisionMaster_id=division_id, DepartmentName=department_name, Order=order)
                messages.success(request, 'Department added successfully!')
        
        return redirect('Corporate')




@require_POST
def move_up_departmentCorporate(request, id):
    department = get_object_or_404(CorporateDepartmentMaster, id=id)
    if department.Order > 0:
        try:
            swap_department = CorporateDepartmentMaster.objects.get(Order=department.Order - 1)
            department.Order, swap_department.Order = swap_department.Order, department.Order
            department.save()
            swap_department.save()
            return HttpResponse('Moved Up')
        except CorporateDepartmentMaster.DoesNotExist:
            pass
    return HttpResponse('Already at the top or error occurred')

@require_POST
def move_down_departmentCorporate(request, id):
    department = get_object_or_404(CorporateDepartmentMaster, id=id)
    max_order = CorporateDepartmentMaster.objects.filter(CorporateDivisionMaster=department.CorporateDivisionMaster).aggregate(Max('Order'))['Order__max']
    if department.Order < max_order:
        try:
            swap_department = CorporateDepartmentMaster.objects.get(Order=department.Order + 1)
            department.Order, swap_department.Order = swap_department.Order, department.Order
            department.save()
            swap_department.save()
            return HttpResponse('Moved Down')
        except CorporateDepartmentMaster.DoesNotExist:
            pass
    return HttpResponse('Already at the bottom or error occurred')



def CorporateDesignationAdd(request):
    if request.method == 'POST':
        designation_id = request.POST.get('designation_id')
        DivisionID = request.POST.get('DivisionID')
        DepartmentID = request.POST.get('DepartmentID')
        Div = request.POST.get('Div')
        Dept = request.POST.get('Dept')
        designations = request.POST.get('designations')
        Lavel = request.POST.get('Lavel')
       
        
        if designation_id:
            designation = get_object_or_404(CorporateDesignationMaster, id=designation_id)
            designation.CorporateDivisionMaster_id = DivisionID
            designation.CorporateDepartmentMaster_id = DepartmentID
            designation.Div = Div
            designation.Dept = Dept
            designation.designations = designations
            designation.Lavel = Lavel
           
            designation.save()
            messages.success(request, 'Designation updated successfully!')
        else:
            preOrder = CorporateDesignationMaster.objects.order_by('-Order').first()
            order = preOrder.Order + 1 if preOrder else 999
            CorporateDesignationMaster.objects.create(
                CorporateDivisionMaster_id=DivisionID,
                CorporateDepartmentMaster_id=DepartmentID,
                Div=Div,
                Dept=Dept,
                designations=designations,
                Lavel=Lavel,
                
                Order=order
            )
            messages.success(request, 'Designation added successfully!')
        
        return redirect('Corporate')

@require_POST
def move_up_designationCorporate(request, id):
    designation = get_object_or_404(CorporateDesignationMaster, id=id)
    if designation.Order > 0:
        try:
            swap_designation = CorporateDesignationMaster.objects.get(Order=designation.Order - 1)
            designation.Order, swap_designation.Order = swap_designation.Order, designation.Order
            designation.save()
            swap_designation.save()
            return HttpResponse('Moved Up')
        except CorporateDesignationMaster.DoesNotExist:
            pass
    return HttpResponse('Already at the top or error occurred')

@require_POST
def move_down_designationCorporate(request, id):
    designation = get_object_or_404(CorporateDesignationMaster, id=id)
    max_order = CorporateDesignationMaster.objects.filter(CorporateDivisionMaster=designation.CorporateDivisionMaster, CorporateDepartmentMaster=designation.CorporateDepartmentMaster).aggregate(Max('Order'))['Order__max']
    if designation.Order < max_order:
        try:
            swap_designation = CorporateDesignationMaster.objects.get(Order=designation.Order + 1)
            designation.Order, swap_designation.Order = swap_designation.Order, designation.Order
            designation.save()
            swap_designation.save()
            return HttpResponse('Moved Down')
        except CorporateDesignationMaster.DoesNotExist:
            pass
    return HttpResponse('Already at the bottom or error occurred')





def CorporateDivision_delete(request):
    id = request.GET.get('ID')
    if id:
        try:
            delete = CorporateDivisionMaster.objects.get(id=id)
            delete.IsDelete = True
            delete.save()
            messages.success(request, 'Data has been deleted successfully.')
        except CorporateDivisionMaster.DoesNotExist:
            messages.error(request, 'The record you are trying to delete does not exist.')
    
    return redirect('Corporate') 


def CorporateDepartment_delete(request):
    id = request.GET.get('ID')
    if id:
        try:
            delete = CorporateDepartmentMaster.objects.get(id=id)
            delete.IsDelete = True
            delete.save()
            messages.success(request, 'Data has been deleted successfully.')
        except CorporateDepartmentMaster.DoesNotExist:
            messages.error(request, 'The record you are trying to delete does not exist.')
    
    return redirect('Corporate')



def CorporateDesignation_delete(request):
    id = request.GET.get('ID')
    if id:
        try:
            delete = CorporateDesignationMaster.objects.get(id=id)
            delete.IsDelete = True
            delete.save()
            messages.success(request, 'Data has been deleted successfully.')
        except CorporateDesignationMaster.DoesNotExist:
            messages.error(request, 'The record you are trying to delete does not exist.')
    
    return redirect('Corporate') 



def Corporatedivisions_list(request):
    division_id = request.GET.get('id')
    try:
        division = CorporateDivisionMaster.objects.get(id=division_id)
        data = {
            'id': division.id,
            'DivisionName': division.DivisionName,
        }
        return JsonResponse(data)
    except CorporateDivisionMaster.DoesNotExist:
        return JsonResponse({'error': 'Division not found'}, status=404)
          


def Corporatedepartments_list(request):
    department_id = request.GET.get('id')

    try:
        department = CorporateDepartmentMaster.objects.get(id=department_id)
        data = {
            'id': department.id,
            'DivisionID': department.CorporateDivisionMaster_id,
            'DepartmentName': department.DepartmentName,
        }
        return JsonResponse(data)
    except CorporateDepartmentMaster.DoesNotExist:
        return JsonResponse({'error': 'Department not found'}, status=404)


def Corporatedesignation_details(request):
    designation_id = request.GET.get('id')

    try:
        designation = CorporateDesignationMaster.objects.get(id=designation_id)
        data = {
            'id': designation.id,
            'DivisionID': designation.CorporateDivisionMaster_id,
            'DepartmentID': designation.CorporateDepartmentMaster_id,
            'Div': designation.Div,
            'Dept': designation.Dept,
            'designations': designation.designations,
            'Lavel': designation.Lavel,  
            'Report_Designations': designation.designations,  
        }
        return JsonResponse(data)
    except CorporateDesignationMaster.DoesNotExist:
        return JsonResponse({'error': 'Designation not found'}, status=404)




# Module Mapping

def Module_Mapping(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    OrganizationID = request.session.get("OrganizationID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")       
    Designationfilters = OnRollDesignationMaster.objects.filter(IsDelete=False)
    Departmentsfilter = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    lavels = LavelAdd.objects.filter(IsDelete=False)
    moduls = ModuleMapping.objects.filter(IsDelete=False)
    context = {
        'Departmentsfilter': Departmentsfilter,
        'moduls':moduls,
        'lavels':lavels,
        'Designationfilters': Designationfilters
       
        
    }
    return render(request, "manningguide/Master/Module_Mapping.html",context)


def ModuleMappingAdd(request):
    if request.method == 'POST':
        division_id = request.POST.get('id')
        
        sorted_items = request.POST.get('sorted_items')
        sorted_items_list = sorted_items.split(',') if sorted_items else []

        departments = request.POST.getlist('Department')
        departments_str = ', '.join(departments)

        reporting_to = request.POST.get('reporting_to')
        weightage1 = request.POST.get('Weightage1')
        dotted_line = request.POST.get('Dotted_Line')
        weightage2 = request.POST.get('Weightage2')
        module_name = request.POST.get('module_name')
        
        if division_id:
            try:
                module_mapping = ModuleMapping.objects.get(id=division_id)
                module_mapping.Department = departments_str
                module_mapping.Level = sorted_items  # Store sorted items as needed
                module_mapping.reporting_to = reporting_to
                module_mapping.Weightage1 = weightage1
                module_mapping.Dotted_Line = dotted_line
                module_mapping.Weightage2 = weightage2
                module_mapping.module_name = module_name
                module_mapping.save()
            except ModuleMapping.DoesNotExist:
                messages.error(request, 'The record you are trying to update does not exist.')
                return redirect('Module_Mapping')
        else:
            
            module_mapping = ModuleMapping(
                Department=departments_str,
                Level=sorted_items,  # Store sorted items as needed
                reporting_to=reporting_to,
                Weightage1=weightage1,
                Dotted_Line=dotted_line,
                Weightage2=weightage2,
                module_name=module_name
            )
            module_mapping.save()

        return redirect('Module_Mapping')

    

def ModuleMapping_delete(request):
    id = request.GET.get('ID')
    if id:
        try:
            delete = ModuleMapping.objects.get(id=id)
            delete.IsDelete = True
            delete.save()
            messages.success(request, 'Data has been deleted successfully.')
        except ModuleMapping.DoesNotExist:
            messages.error(request, 'The record you are trying to delete does not exist.')
    
    return redirect('Module_Mapping') 


def Module_Edit(request):
    Module_id = request.GET.get('id')
    try:
        Module = ModuleMapping.objects.get(id=Module_id)
        data = {
            'id': Module.id,
            'Department': Module.Department,
            'Level': Module.Level,
            'reporting_to': Module.reporting_to,
            'Weightage1': Module.Weightage1,
            'Dotted_Line': Module.Dotted_Line,
            'Weightage2': Module.Weightage2,
            'module_name':Module.module_name
            
        }
        return JsonResponse(data)
    except ModuleMapping.DoesNotExist:
        return JsonResponse({'error': 'Module not found'}, status=404)
    







# Manage Budget On Roll

from .models import ManageBudgetOnRoll



from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ManageBudgetOnRoll, OnRollDivisionMaster, OnRollDepartmentMaster, OnRollDesignationMaster
from datetime import datetime
import requests








from django.http import HttpResponseRedirect
from django.urls import reverse


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ManageBudgetOnRoll, OnRollDivisionMaster, OnRollDepartmentMaster, OnRollDesignationMaster,ManageBudgetContract,ManageBudgetSharedServices
import requests
import logging
from django.db.models import Prefetch
from django.db.models import Case, When, IntegerField

logger = logging.getLogger(__name__)

# logger = logging.getLogger(__name__)

def BudgetOndeta(request):

    if 'OrganizationID' not in request.session or 'UserID' not in request.session:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')
    
    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")       

    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while fetching organization data: {e}")
        memOrg = []

    if request.method == 'POST':
        hotel_name = request.POST.get('hotel_name')
        # from datetime import datetime

        current_year = datetime.now().year

        ManageBudgetOnRoll.objects.filter(
            hotel_name=hotel_name,
            is_delete=False,
        ).update(is_delete=True)
        
        for key, value in request.POST.items():
            if key.startswith('avg_salary_data_'):
                designation_id = key.split('_')[3]
                designation = get_object_or_404(OnRollDesignationMaster, id=designation_id)
                department = designation.OnRollDepartmentMaster
                division = department.OnRollDivisionMaster

                
                def parse_post_data(post_key):
                    value = request.POST.get(post_key, '').strip()
                    return float(value) if value else 0.0

                defaults = {
                    'avg_salary': parse_post_data(f'avg_salary_data_{designation_id}'),
                    'head_count': int(parse_post_data(f'head_count_data_{designation_id}')),
                    'morning': int(parse_post_data(f'morning_data_{designation_id}')),
                    'general_deta': int(parse_post_data(f'general_data_{designation_id}')),
                    'afternoon': int(parse_post_data(f'afternoon_data_{designation_id}')),
                    'night': int(parse_post_data(f'night_data_{designation_id}')),
                    'm_break': int(parse_post_data(f'm_break_data_{designation_id}')),
                    'relievers': int(parse_post_data(f'relievers_data_{designation_id}')),
                    'total_ctc': parse_post_data(f'total_ctc_data_{designation_id}'),
                }
                
                    

                ManageBudgetOnRoll.objects.update_or_create(
                    on_roll_division_master=division,
                    on_roll_department_master=department,
                    on_roll_designation_master=designation,
                    is_delete=False,
                    hotel_name=hotel_name,
                    Budget_Year = current_year,
                    defaults={
                        **defaults,
                        'OrganizationID': OrganizationID,
                        'created_by': UserID,
                        # 'is_delete':False
                    }
                )

        
        return HttpResponseRedirect(f'{reverse("BudgetOndeta")}?hotel_name={hotel_name}')

    elif request.method == 'GET':
        hotel_name = request.GET.get('hotel_name', OrganizationID)

        if UserType == 'CEO' and request.GET.get('hotel_name') is None:
            hotel_name = 401


        existing_data = ManageBudgetOnRoll.objects.filter(hotel_name=hotel_name,is_delete =False)

        default_values = {}
        for data in existing_data:
            default_values[data.on_roll_designation_master.id] = {
                'avg_salary': data.avg_salary,
                'head_count': data.head_count or 0,
                'morning': data.morning,
                'general_deta': data.general_deta,
                'afternoon': data.afternoon,
                'night': data.night,
                'm_break': data.m_break,
                'relievers': data.relievers,
                'total_ctc': data.total_ctc,
            }

        # filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
        # filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

        # divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        #     Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
        #     Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
        # )
        
        filtered_departments = OnRollDepartmentMaster.objects.filter(
            IsDelete=False
        ).order_by('Order')

        # filtered_designations = OnRollDesignationMaster.objects.filter(
        #     IsDelete=False
        # ).order_by('Lavel', 'Order')   
        
        filtered_designations = OnRollDesignationMaster.objects.filter(
            IsDelete=False
        ).annotate(
            level_order=Case(
                When(Lavel='M6', then=1),
                When(Lavel='M5', then=2),
                When(Lavel='M4', then=3),
                When(Lavel='M3', then=4),
                When(Lavel='M2', then=5),
                When(Lavel='M1', then=6),
                When(Lavel='M', then=7),
                When(Lavel='E', then=8),
                When(Lavel='T', then=9),
                When(Lavel='A', then=10),
                default=99,
                output_field=IntegerField()
            )
        ).order_by('level_order', 'Order')

        divisions = OnRollDivisionMaster.objects.filter(
            IsDelete=False
        ).order_by('Order').prefetch_related(
            Prefetch(
                'onrolldepartmentmaster_set',
                queryset=filtered_departments
            ),
            Prefetch(
                'onrolldepartmentmaster_set__onrolldesignationmaster_set',
                queryset=filtered_designations
            )
        )

        context = {
            'divisions': divisions,
            'hotel_name': hotel_name,
            'existing_data': existing_data,
            'default_values': default_values,
            'memOrg': memOrg,
        }

        return render(request, "manningguide/ManageBudget/BudgetOnRoll.html", context)



from django.shortcuts import render, redirect, get_object_or_404
from .models import ManageBudgetContract, ContractDivisionMaster

from collections import defaultdict


logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from collections import defaultdict
import requests
import logging

# Assuming `logger` and `MasterAttribute` are defined elsewhere
logger = logging.getLogger(__name__)


def BudgetContract(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")

   
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    if not OrganizationID or not UserID:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')

    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    if request.method == 'POST':
        hotel_name = request.POST.get('hotel_name', '')

        

        for key, value in request.POST.items():
            if key.startswith('avg_salary_data_'):
                designation_id = key.split('_')[3]
                designation = get_object_or_404(ContractDesignationMaster, id=designation_id)
                department = designation.ContractDepartmentMaster
                division = department.ContractDivisionMaster

                def parse_post_data(post_key):
                    value = request.POST.get(post_key, '').strip()
                    return float(value) if value else 0.0

                defaults = {
                    'avg_salary': parse_post_data(f'avg_salary_data_{designation_id}'),
                    'head_count': int(parse_post_data(f'head_count_data_{designation_id}')),
                    'morning': int(parse_post_data(f'morning_data_{designation_id}')),
                    'general_deta': int(parse_post_data(f'general_data_{designation_id}')),
                    'afternoon': int(parse_post_data(f'afternoon_data_{designation_id}')),
                    'night': int(parse_post_data(f'night_data_{designation_id}')),
                    'm_break': int(parse_post_data(f'm_break_data_{designation_id}')),
                    'relievers': int(parse_post_data(f'relievers_data_{designation_id}')),
                    'total_ctc': parse_post_data(f'total_ctc_data_{designation_id}'),
                }

                ManageBudgetContract.objects.update_or_create(
                    contract_division_master=division,
                    contract_department_master=department,
                    contract_designation_master=designation,
                    hotel_name=hotel_name,
                    defaults={
                        **defaults,
                        'OrganizationID': OrganizationID,
                        'CreatedBy': UserID,
                    }
                )

       
        return HttpResponseRedirect(f'{reverse("BudgetContract")}?hotel_name={hotel_name}')

    elif request.method == 'GET':
        hotel_name = request.GET.get('hotel_name', OrganizationID)

        if UserType == 'CEO' and request.GET.get('hotel_name') is None:
            hotel_name = 401

    existing_data = ManageBudgetContract.objects.filter(hotel_name=hotel_name)

    default_values = {}
    for data in existing_data:
        default_values[data.contract_designation_master.id] = {
            'avg_salary': data.avg_salary,
            'head_count': data.head_count or 0,
            'morning': data.morning,
            'general_deta': data.general_deta,
            'afternoon': data.afternoon,
            'night': data.night,
            'm_break': data.m_break,
            'relievers': data.relievers,
            'total_ctc': data.total_ctc,
        }

    filtered_departments = ContractDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = ContractDesignationMaster.objects.filter(IsDelete=False)

    
    divisions = ContractDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('contractdepartmentmaster_set', queryset=filtered_departments),
        Prefetch('contractdepartmentmaster_set__contractdesignationmaster_set', queryset=filtered_designations)
    )

    context = {
        'divisions': divisions,
        'hotel_name': hotel_name,
        'default_values': default_values,
        'memOrg': memOrg,
    }
    return render(request, "manningguide/ManageBudget/BudgetContract.html", context)





def MealCost(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")

  
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    if not OrganizationID or not UserID:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')

    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    selected_hotel = request.GET.get('hotel_name', OrganizationID)
    if UserType == 'CEO' and request.GET.get('hotel_name') is None:
        selected_hotel = 401
    cafeteriamealcost = 0
    


    if request.method == 'POST':
        hotel_name = request.POST.get('hotel_name')
        

        cafeteriamealcost = request.POST.get('cafeteriamealcost', 0)

        
        budget_meal_cost, created = BudgetMealCost.objects.update_or_create(
            hotel_name=hotel_name,
            defaults={
                'cafeteriamealcost': cafeteriamealcost,
                'OrganizationID': OrganizationID,
                'CreatedBy': UserID,
                'ModifyBy': UserID,
                'ModifyDateTime': datetime.now()
            }
        )
        if not created:
            budget_meal_cost.ModifyDateTime = datetime.now()
            budget_meal_cost.save()

    
    if selected_hotel != 'Select':
        try:
            budget_meal_cost = BudgetMealCost.objects.get(hotel_name=selected_hotel)
            cafeteriamealcost = budget_meal_cost.cafeteriamealcost
        except BudgetMealCost.DoesNotExist:
            cafeteriamealcost = 0

    # print("selected hotel is here:", selected_hotel)
    context = {
        'memOrg': memOrg,
        'SelHotelName': selected_hotel,
        'cafeteriamealcost': cafeteriamealcost,
    }
    return render(request, "manningguide/ManageBudget/MealCost.html", context)




from datetime import datetime

def InsuranceCost(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    if not OrganizationID or not UserID:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')

    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    selected_hotel = request.GET.get('hotel_name', OrganizationID)

    if UserType == 'CEO' and request.GET.get('hotel_name') is None:
        selected_hotel = 401

    EmployeeInsurancecost = 0

    if request.method == 'POST':
        hotel_name = request.POST.get('hotel_name')

        

        EmployeeInsurancecost = request.POST.get('EmployeeInsurancecost', 0)

        insurance_cost, created = BudgetInsuranceCost.objects.update_or_create(
            hotel_name=hotel_name,
            defaults={
                'EmployeeInsurancecost': EmployeeInsurancecost,
                'OrganizationID': OrganizationID,
                'CreatedBy': UserID,
                'ModifyBy': UserID,
                'ModifyDateTime': datetime.now()
            }
        )
        if not created:
            insurance_cost.ModifyDateTime = datetime.now()
            insurance_cost.save()

    if selected_hotel != 'Select':
        try:
            insurance_cost = BudgetInsuranceCost.objects.get(hotel_name=selected_hotel)
            EmployeeInsurancecost = insurance_cost.EmployeeInsurancecost
        except BudgetInsuranceCost.DoesNotExist:
            EmployeeInsurancecost = 0

    context = {
        'memOrg': memOrg,
        'SelHotelName': selected_hotel,
        'EmployeeInsurancecost': EmployeeInsurancecost,
    }
    return render(request, "manningguide/ManageBudget/InsuranceCost.html", context)




from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
import requests
import logging

logger = logging.getLogger(__name__)

from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
import requests
import logging

logger = logging.getLogger(__name__)

def SharedServicesbudget(request):
    if 'OrganizationID' not in request.session or 'UserID' not in request.session:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')
    
    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")


    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  
    
    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while fetching organization data: {e}")
        memOrg = []
    
    if request.method == 'POST':
        hotel_name = request.POST.get('hotel_name')

               
        for key, value in request.POST.items():
            if key.startswith('avg_salary_data_'):
                designation_id = key.split('_')[3]
                designation = get_object_or_404(ServicesDesignationMaster, id=designation_id)
                department = designation.ServicesDepartmentMaster
                division = department.ServicesDivisionMaster
                
                def parse_post_data(post_key):
                    return request.POST.get(post_key, '').strip() or '0'
                
                defaults = {
                    'avg_salary': float(parse_post_data(f'avg_salary_data_{designation_id}')),
                    'head_count': int(parse_post_data(f'head_count_data_{designation_id}')),
                    'morning': int(parse_post_data(f'morning_data_{designation_id}')),
                    'general_deta': int(parse_post_data(f'general_data_{designation_id}')),
                    'afternoon': int(parse_post_data(f'afternoon_data_{designation_id}')),
                    'night': int(parse_post_data(f'night_data_{designation_id}')),
                    'm_break': int(parse_post_data(f'm_break_data_{designation_id}')),
                    'relievers': int(parse_post_data(f'relievers_data_{designation_id}')),
                    'total_ctc': float(parse_post_data(f'total_ctc_data_{designation_id}')),
                }

                ManageBudgetSharedServices.objects.update_or_create(
                    services_division_master=division,
                    services_department_master=department,
                    services_designation_master=designation,
                    hotel_name=hotel_name,
                    defaults={
                        **defaults,
                        'OrganizationID': OrganizationID,
                        'CreatedBy': UserID,
                    }
                )

        return redirect('SharedServicesbudget')
    elif request.method == 'GET':
        hotel_name = request.GET.get('hotel_name', OrganizationID)

        if UserType == 'CEO' and request.GET.get('hotel_name') is None:
            hotel_name = 401

    existing_data = ManageBudgetSharedServices.objects.filter(hotel_name=hotel_name)

    default_values = {}
    for data in existing_data:
        default_values[data.services_designation_master.id] = {
            'avg_salary': data.avg_salary,
            'head_count': data.head_count or 0,
            'morning': data.morning,
            'general_deta': data.general_deta,
            'afternoon': data.afternoon,
            'night': data.night,
            'm_break': data.m_break,
            'relievers': data.relievers,
            'total_ctc': data.total_ctc,
        }

    # divisions = ServicesDivisionMaster.objects.all().order_by('Order').prefetch_related(
    #         'servicesdepartmentmaster_set__servicesdesignationmaster_set'
    #     )
    filtered_departments = ServicesDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = ServicesDesignationMaster.objects.filter(IsDelete=False)

    
    divisions = ServicesDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('servicesdepartmentmaster_set', queryset=filtered_departments),
        Prefetch('servicesdepartmentmaster_set__servicesdesignationmaster_set', queryset=filtered_designations)
    )
    context = {
        'divisions': divisions,
        'hotel_name': hotel_name,
        'existing_data': existing_data,
        'default_values': default_values,
        'memOrg': memOrg,
        'avg_salarycount': ""
    }    
    return render(request, "manningguide/ManageBudget/BudgetSharedServices.html", context)










def Entrymealcost(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")

    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    if not OrganizationID or not UserID:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')

    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    
    selected_hotel = request.GET.get('hotel_name', OrganizationID)
    cafeteriamealcost = 0

    if UserType == 'CEO' and request.GET.get('hotel_name') is None:
        selected_hotel = 401


    if request.method == 'POST':
        hotel_name = request.POST.get('hotel_name')
        cafeteriamealcost = request.POST.get('cafeteriamealcost', 0)

        budget_meal_cost, created = EntryActualMealCost.objects.update_or_create(
            hotel_name=hotel_name,
            defaults={
                'cafeteriamealcost': cafeteriamealcost,
                'OrganizationID': OrganizationID,
                'CreatedBy': UserID,
                'ModifyBy': UserID,
                'ModifyDateTime': datetime.now()
            }
        )
        if not created:
            budget_meal_cost.ModifyDateTime = datetime.now()
            budget_meal_cost.save()

    if selected_hotel != 'Select':
        try:
            budget_meal_cost = EntryActualMealCost.objects.get(hotel_name=selected_hotel)
            cafeteriamealcost = budget_meal_cost.cafeteriamealcost
        except EntryActualMealCost.DoesNotExist:
            cafeteriamealcost = 0

    context = {
        'memOrg': memOrg,
        'SelHotelName': selected_hotel,
        'cafeteriamealcost': cafeteriamealcost,
    }
    return render(request, "manningguide/EntryActual/Entrymealcost.html", context)




    


def EntryInsurancesCost(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    if not OrganizationID or not UserID:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')

    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    selected_hotel = request.GET.get('hotel_name', OrganizationID)
    EmployeeInsurancecost = 0


    if UserType == 'CEO' and request.GET.get('hotel_name') is None:
        selected_hotel = 401

    if request.method == 'POST':
        hotel_name = request.POST.get('hotel_name')
        EmployeeInsurancecost = request.POST.get('EmployeeInsurancecost', 0)

        insurance_cost, created = EntryActualInsuranceCost.objects.update_or_create(
            hotel_name=hotel_name,
            defaults={
                'EmployeeInsurancecost': EmployeeInsurancecost,
                'OrganizationID': OrganizationID,
                'CreatedBy': UserID,
                'ModifyBy': UserID,
                'ModifyDateTime': datetime.now()
            }
        )
        if not created:
            insurance_cost.ModifyDateTime = datetime.now()
            insurance_cost.save()

    if selected_hotel != 'Select':
        try:
            insurance_cost = EntryActualInsuranceCost.objects.get(hotel_name=selected_hotel)
            EmployeeInsurancecost = insurance_cost.EmployeeInsurancecost
        except EntryActualInsuranceCost.DoesNotExist:
            EmployeeInsurancecost = 0

    context = {
        'memOrg': memOrg,
        'SelHotelName': selected_hotel,
        'EmployeeInsurancecost': EmployeeInsurancecost,
    }
    return render(request, "manningguide/EntryActual/Entryinsurancescost.html",context)
   


def safe_float(value):
    try:
        return float(value)
    except ValueError:
        return 0.0

def EntryActualContractCost(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')
    
    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  
    
    if not OrganizationID or not UserID:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')

    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    hotel_name = request.POST.get('hotel_name', '') if request.method == 'POST' else request.GET.get('hotel_name', OrganizationID)

    if UserType == 'CEO' and request.GET.get('hotel_name') is None:
        hotel_name = 401
    
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('avg_salary_data_'):
                designation_id = key.split('_')[3]
                designation = get_object_or_404(ContractDesignationMaster, id=designation_id)
                department = designation.ContractDepartmentMaster
                division = department.ContractDivisionMaster

                defaults = {
                    'avg_salary': safe_float(request.POST.get(f'avg_salary_data_{designation_id}', '')),
                    'head_count': safe_float(request.POST.get(f'head_count_data_{designation_id}', '')),
                    'morning': safe_float(request.POST.get(f'morning_data_{designation_id}', '')),
                    'general_deta': safe_float(request.POST.get(f'general_data_{designation_id}', '')),
                    'afternoon': safe_float(request.POST.get(f'afternoon_data_{designation_id}', '')),
                    'night': safe_float(request.POST.get(f'night_data_{designation_id}', '')),
                    'm_break': safe_float(request.POST.get(f'm_break_data_{designation_id}', '')),
                    'relievers': safe_float(request.POST.get(f'relievers_data_{designation_id}', '')),
                    'total_ctc': safe_float(request.POST.get(f'total_ctc_data_{designation_id}', '')),
                }

                EntryActualContract.objects.update_or_create(
                    contract_division_master=division,
                    contract_department_master=department,
                    contract_designation_master=designation,
                    hotel_name=hotel_name,
                    defaults={
                        **defaults,
                        'OrganizationID': OrganizationID,
                        'CreatedBy': UserID,
                    }
                )

    
    existing_data = EntryActualContract.objects.filter(hotel_name=hotel_name)

   

    default_values = {}
    for data in existing_data:
        default_values[data.contract_designation_master.id] = {
            'avg_salary': data.avg_salary,
            'head_count': data.head_count or 0,
            'morning': data.morning,
            'general_deta': data.general_deta,
            'afternoon': data.afternoon,
            'night': data.night,
            'm_break': data.m_break,
            'relievers': data.relievers,
            'total_ctc': data.total_ctc,
        }

    
    # divisions = ContractDivisionMaster.objects.all().order_by('Order').prefetch_related(
    #     'contractdepartmentmaster_set__contractdesignationmaster_set'
    # )
    filtered_departments = ContractDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = ContractDesignationMaster.objects.filter(IsDelete=False)

   
    divisions = ContractDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('contractdepartmentmaster_set', queryset=filtered_departments),
        Prefetch('contractdepartmentmaster_set__contractdesignationmaster_set', queryset=filtered_designations)
    )
   
    context = {
        'divisions': divisions,
        'hotel_name': hotel_name,
        'existing_data': existing_data,
        'default_values': default_values,
        'memOrg': memOrg,
    }

    return render(request, "manningguide/EntryActual/EntryActualContractCost.html", context)



def EntrySharedServices(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')
    
    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
        pass
    else:
        return Error(request, "No Access")  

    if not OrganizationID or not UserID:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')

    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    if request.method == 'POST':
        hotel_name = request.POST.get('hotel_name', '')  
        
       
        for key, value in request.POST.items():
            if key.startswith('avg_salary_data_'):
                designation_id = key.split('_')[3]
                designation = get_object_or_404(ServicesDesignationMaster, id=designation_id)
                department = designation.ServicesDepartmentMaster
                division = department.ServicesDivisionMaster

                
                defaults = {
                    'avg_salary': float(request.POST.get(f'avg_salary_data_{designation_id}', 0) or 0),
                    'head_count': float(request.POST.get(f'head_count_data_{designation_id}', 0) or 0),
                    'morning': float(request.POST.get(f'morning_data_{designation_id}', 0) or 0),
                    'general_deta': float(request.POST.get(f'general_data_{designation_id}', 0) or 0),
                    'afternoon': float(request.POST.get(f'afternoon_data_{designation_id}', 0) or 0),
                    'night': float(request.POST.get(f'night_data_{designation_id}', 0) or 0),
                    'm_break': float(request.POST.get(f'm_break_data_{designation_id}', 0) or 0),
                    'relievers': float(request.POST.get(f'relievers_data_{designation_id}', 0) or 0),
                    'total_ctc': float(request.POST.get(f'total_ctc_data_{designation_id}', 0) or 0),
                }

                EntryActualSharedServices.objects.update_or_create(
                    services_division_master=division,
                    services_department_master=department,
                    services_designation_master=designation,
                    hotel_name=hotel_name,
                    defaults={
                        **defaults,
                        'OrganizationID': OrganizationID,
                        'CreatedBy': UserID,
                    }
                )

        existing_data_list = EntryActualSharedServices.objects.filter(hotel_name=hotel_name)

    elif request.method == 'GET':
        hotel_name = request.GET.get('hotel_name', OrganizationID)

        if UserType == 'CEO' and request.GET.get('hotel_name') is None:
            hotel_name = 401

        existing_data_list = EntryActualSharedServices.objects.filter(hotel_name=hotel_name)

    # if UserType == 'CEO':
    #     hotel_name = 401

    default_values = {}
    for data in existing_data_list:
        default_values[data.services_designation_master.id] = {
            'avg_salary': data.avg_salary,
            'head_count': data.head_count or 0,
            'morning': data.morning,
            'general_deta': data.general_deta,
            'afternoon': data.afternoon,
            'night': data.night,
            'm_break': data.m_break,
            'relievers': data.relievers,
            'total_ctc': data.total_ctc,
        }

    # divisions = ServicesDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
    # 'servicesdepartmentmaster_set__servicesdesignationmaster_set'
    #  )
    filtered_departments = ServicesDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = ServicesDesignationMaster.objects.filter(IsDelete=False)

    
    divisions = ServicesDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('servicesdepartmentmaster_set', queryset=filtered_departments),
        Prefetch('servicesdepartmentmaster_set__servicesdesignationmaster_set', queryset=filtered_designations)
    )

    context = {
        'divisions': divisions,
        'hotel_name': hotel_name,
        'existing_data': existing_data_list,
        'default_values': default_values,
        'memOrg': memOrg,
    }

    return render(request, "manningguide/EntryActual/EntrySharedServices.html", context)



from app.models import EmployeeMaster,OrganizationMaster




import logging
import requests
from django.shortcuts import render, redirect
from django.db.models import Count, Sum, Q, F, FloatField, ExpressionWrapper

from HumanResources.models import EmployeeWorkDetails

logger = logging.getLogger(__name__)



logger = logging.getLogger(__name__)

def ViewActual(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')
    
    OrganizationID = request.session.get("OrganizationID")
    
    UserID = request.session.get("UserID")

    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
        pass
    else:
        return Error(request, "No Access")  
    
    logger.debug(f"Retrieved OrganizationID: {OrganizationID}")
    logger.debug(f"Retrieved UserID: {UserID}")

    if not OrganizationID or not UserID:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')

    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
        logger.debug(f"API response: {memOrg}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []
    

    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False)
    Departmentsdatas = OnRollDepartmentMaster.objects.filter(IsDelete=False)

    selectedOrganizationID = request.GET.get('hotel_name', OrganizationID)
    exclude_zero_headcount = request.GET.get('exclude_zero_headcount', '1')  
    selected_division = request.GET.get('divisionname')
    selected_department = request.GET.get('departmentname')

    if UserType == 'CEO' and request.GET.get('hotel_name') is None:
        selectedOrganizationID = 401
    
    # Filtering departments based on selection
    if selected_department and selected_department != 'All Department':
        filtered_departments = OnRollDepartmentMaster.objects.filter(
            IsDelete=False, DepartmentName=selected_department
        )
    elif selected_division and selected_division != 'All Division':
        filtered_departments = OnRollDepartmentMaster.objects.filter(
            OnRollDivisionMaster__DivisionName=selected_division, IsDelete=False
        )
    else:
        filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)

    # Filter designations
    # filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)
    filtered_designations = OnRollDesignationMaster.objects.filter(
        IsDelete=False
    ).annotate(
        level_order=Case(
            When(Lavel='M6', then=1),
            When(Lavel='M5', then=2),
            When(Lavel='M4', then=3),
            When(Lavel='M3', then=4),
            When(Lavel='M2', then=5),
            When(Lavel='M1', then=6),
            When(Lavel='M', then=7),
            When(Lavel='E', then=8),
            When(Lavel='T', then=9),
            When(Lavel='A', then=10),
            default=99,
            output_field=IntegerField()
        )
    ).order_by('level_order', 'Order')


    # Prefetch filtered departments and designations into divisions
    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
        Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
    )

    # Servicedivisions = ServicesDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
    #     'servicesdepartmentmaster_set__servicesdesignationmaster_set'
    # )
    filtered_contract_departments = ContractDepartmentMaster.objects.filter(IsDelete=False)
    filtered_contract_designations = ContractDesignationMaster.objects.filter(IsDelete=False)

    if selected_department and selected_department != 'All Department':
        filtered_departments = OnRollDepartmentMaster.objects.filter(
            IsDelete=False, DepartmentName=selected_department
        )
    else:
        filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)

    # Filtered querysets for related models (ServicesDivisionMaster)
    filtered_service_departments = ServicesDepartmentMaster.objects.filter(IsDelete=False)
    filtered_service_designations = ServicesDesignationMaster.objects.filter(IsDelete=False)

    # Query for ContractDivisionMaster
    contractdivisions = ContractDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('contractdepartmentmaster_set', queryset=filtered_contract_departments),
        Prefetch('contractdepartmentmaster_set__contractdesignationmaster_set', queryset=filtered_contract_designations)
    )

    # Query for ServicesDivisionMaster
    Servicedivisions = ServicesDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('servicesdepartmentmaster_set', queryset=filtered_service_departments),
        Prefetch('servicesdepartmentmaster_set__servicesdesignationmaster_set', queryset=filtered_service_designations)
    )
    
    
    employees_per_department_designation = EmployeeWorkDetails.objects.filter(
    OrganizationID=selectedOrganizationID,
    IsDelete=False,IsSecondary=False,
    EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"]
    )
    
    if exclude_zero_headcount == '1':  
        employees_per_department_designation = employees_per_department_designation.exclude(id=0)
    
     
    Contractbudget_department_designation = EntryActualContract.objects.filter(OrganizationID=selectedOrganizationID)
    if exclude_zero_headcount == '1':  
        Contractbudget_department_designation = Contractbudget_department_designation.exclude(head_count=0)
   
    Servicesbudget_department_designation = EntryActualSharedServices.objects.filter(OrganizationID=selectedOrganizationID)
    if exclude_zero_headcount == '1':  
        Servicesbudget_department_designation = Servicesbudget_department_designation.exclude(head_count=0)


    # employees_per_department_designation = EmployeeWorkDetails.objects.filter(IsDelete=False)

    if selectedOrganizationID:
        employees_per_department_designation = employees_per_department_designation.filter(OrganizationID=selectedOrganizationID,IsDelete=False)

    logger.debug(f"Filtered employees_per_department_designation queryset: {employees_per_department_designation}")

    employees_per_department_designation = employees_per_department_designation.exclude(
        Department__isnull=True
    ).exclude(
        Department=''
    )

    # logger.debug(f"Excluded employees_per_department_designation queryset: {employees_per_department_designation}")

    employees_per_department_designation = (
        employees_per_department_designation
        .values('Department', 'Designation')
        .annotate(
            num_employees=Count('id'),
            total_salary=Sum('Salary', filter=Q(Salary__isnull=False, Salary__gt=0)),
            avg_salary=ExpressionWrapper(
                Sum('Salary', filter=Q(Salary__isnull=False, Salary__gt=0)) / Count('id'),
                output_field=FloatField()
            )
        )
        .order_by('Department', 'Designation')
    )

    # logger.debug(f"Annotated employees_per_department_designation queryset: {employees_per_department_designation}")

    department_totals = {}
    employees_dict = {}
    division_totals = {}

    for emp in employees_per_department_designation:
        dept = emp['Department']
        department_name = dept
        designation = emp['Designation'] or 0
        avg_salary = emp['avg_salary'] or 0
        num_employees = emp['num_employees'] or 0
        multiplication_result = avg_salary * num_employees  

        divisions_qs = OnRollDivisionMaster.objects.filter(
           IsDelete=False, onrolldepartmentmaster__DepartmentName=department_name
        ).annotate(
            department_name=F('onrolldepartmentmaster__DepartmentName')
        ).values(
            'DivisionName',  
        )

        # logger.debug(f"Divisions queryset for department '{department_name}': {divisions_qs}")

        division_name = divisions_qs[0]['DivisionName'] if divisions_qs else None

        if dept not in department_totals:
            department_totals[dept] = {
                'total_salarymulti': 0,
                'total_headcount': 0,
                'salary_headcount_product': 0,
            }

        if division_name and division_name not in division_totals:
            division_totals[division_name] = {
                'divisiontotal_salarymulti': 0,
                'divisiontotal_headcount': 0,
                'divisionsalary_headcount_product': 0,
            }

        if dept not in employees_dict:
            employees_dict[dept] = {}

        employees_dict[dept][designation] = {
            'num_employees': num_employees,
            'avg_salary': avg_salary,
            'multiplication_result': multiplication_result  
        }

        # department_totals[dept]['total_salarymulti'] += avg_salary
        department_totals[dept]['total_salarymulti'] += multiplication_result
        department_totals[dept]['total_headcount'] += num_employees
        department_totals[dept]['salary_headcount_product'] = (
            department_totals[dept]['total_salarymulti'] / department_totals[dept]['total_headcount']
        )

        if division_name:
            # division_totals[division_name]['divisiontotal_salarymulti'] += avg_salary
            division_totals[division_name]['divisiontotal_salarymulti'] += multiplication_result
            division_totals[division_name]['divisiontotal_headcount'] += num_employees
            division_totals[division_name]['divisionsalary_headcount_product'] = (
                division_totals[division_name]['divisiontotal_salarymulti'] / division_totals[division_name]['divisiontotal_headcount']
            )

    if exclude_zero_headcount == '1':
        employees_per_department_designation = employees_per_department_designation.exclude(num_employees=0)

    grand_total_salary = sum(department['divisiontotal_salarymulti'] for department in division_totals.values() if 'divisiontotal_salarymulti' in department)
    grand_total_headcount = sum(department['divisiontotal_headcount'] for department in division_totals.values() if 'divisiontotal_headcount' in department)
   


    if grand_total_headcount > 0:
        grandsalarydivion = grand_total_salary / grand_total_headcount
    else:
        grandsalarydivion = 0
        
    # <!-- contract budget  -->

    Contractbudget_department_designation = EntryActualContract.objects.filter(
            hotel_name=selectedOrganizationID,IsDelete=False,
        ).values(
            'contract_department_master__DepartmentName',  
            'contract_designation_master__designations'      
        ).annotate(
            Contracthead_count=Sum('head_count'),
            Contracttotal_salary=Sum('avg_salary'),
            Contractavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
            Contractmultiplication_result=ExpressionWrapper(F('Contractavg_salary') * F('Contracthead_count'), output_field=FloatField())
        ).order_by(
            'contract_department_master__DepartmentName',    
            'contract_designation_master__designations'       
        )
    
        
    Contractbudgets_dict = {}
    Contractdepartment_totals = {}
    Contractdivision_totals = {}

        
    for Contractbudget in Contractbudget_department_designation:
            dept_id = Contractbudget['contract_department_master__DepartmentName']
            desig_id = Contractbudget['contract_designation_master__designations']

            if dept_id not in Contractbudgets_dict:
                Contractbudgets_dict[dept_id] = {}

            Contractbudgets_dict[dept_id][desig_id] = {
                'Contracthead_count': Contractbudget['Contracthead_count'],
                'Contractavg_salary': Contractbudget['Contractavg_salary'],
                'Contractmultiplication_result': Contractbudget['Contractmultiplication_result'],
            }

            if dept_id not in Contractdepartment_totals:
                Contractdepartment_totals[dept_id] = {
                    'Contractmultiplication_result': 0,
                    'Contracthead_count': 0,
                    'salary_headcount_contract': 0,
                }

            Contractdepartment_totals[dept_id]['Contractmultiplication_result'] += Contractbudget['Contractmultiplication_result']
            Contractdepartment_totals[dept_id]['Contracthead_count'] += Contractbudget['Contracthead_count']

            if Contractdepartment_totals[dept_id]['Contracthead_count'] > 0:
                Contractdepartment_totals[dept_id]['salary_headcount_contract'] = (
                    Contractdepartment_totals[dept_id]['Contractmultiplication_result'] / Contractdepartment_totals[dept_id]['Contracthead_count']
                )

            
            divisions_qs = ContractDivisionMaster.objects.filter(
                contractdepartmentmaster__DepartmentName=dept_id,IsDelete=False
            ).annotate(
                division_name=F('DivisionName')
            ).values('division_name')

            division_name = divisions_qs[0]['division_name'] if divisions_qs else None

            if division_name and division_name not in Contractdivision_totals:
                Contractdivision_totals[division_name] = {
                    'Contractdivisionmultiplication_result': 0,
                    'Contractdivisiontotal_headcount': 0,
                    'Contractdivisionsalary_headcount_product': 0,
                }

            if division_name:
                Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] += Contractbudget['Contractmultiplication_result']
                Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] += Contractbudget['Contracthead_count']

                if Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] > 0:
                    Contractdivision_totals[division_name]['Contractdivisionsalary_headcount_product'] = (
                        Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] / Contractdivision_totals[division_name]['Contractdivisiontotal_headcount']
                    )
    grandContractdivisionmultiplication_result = sum(
        dept['Contractdivisionmultiplication_result'] for dept in Contractdivision_totals.values() if 'Contractdivisionmultiplication_result' in dept
    )
    Contractgrand_total_headcount = sum(
        dept['Contractdivisiontotal_headcount'] for dept in Contractdivision_totals.values() if 'Contractdivisiontotal_headcount' in dept
    )
    
    if Contractgrand_total_headcount > 0:
        contractgrandsalarydivion = grandContractdivisionmultiplication_result / Contractgrand_total_headcount
    else:
        contractgrandsalarydivion = 0  
    

    # <!-- Shared Services Budget  -->
    Servicesbudget_department_designation = EntryActualSharedServices.objects.filter(
        hotel_name=selectedOrganizationID, IsDelete=False
    ).values(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    ).annotate(
        Serviceshead_count=Sum('head_count'),
        Servicestotal_salary=Sum('avg_salary'),
        Servicesavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        Servicesmultiplication_result=F('Servicesavg_salary') * F('Serviceshead_count')
    ).order_by(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    )

    Servicesbudgets_dict = {}
    departmentservices_dict = {}
    divisionservices_dict = {}

    for Servicesbudget in Servicesbudget_department_designation:
        dept_id = Servicesbudget['services_department_master__DepartmentName']
        desig_id = Servicesbudget['services_designation_master__designations']

        if dept_id not in Servicesbudgets_dict:
            Servicesbudgets_dict[dept_id] = {}

        Servicesbudgets_dict[dept_id][desig_id] = {
            'Serviceshead_count': Servicesbudget['Serviceshead_count'],
            'Servicesavg_salary': Servicesbudget['Servicesavg_salary'],
            'Servicesmultiplication_result': Servicesbudget['Servicesmultiplication_result'],
        }


        if dept_id not in departmentservices_dict:
            departmentservices_dict[dept_id] = {
                'TotalServicesmultiplication_result': 0,
                'TotalServiceshead_count': 0,
                'TotalServicessalary_headcount_contract': 0,
            }

        departmentservices_dict[dept_id]['TotalServicesmultiplication_result'] += Servicesbudget.get('Servicesmultiplication_result', 0.0) or 0.0
        departmentservices_dict[dept_id]['TotalServiceshead_count'] += Servicesbudget.get('Serviceshead_count', 0) or 0


        if departmentservices_dict[dept_id]['TotalServiceshead_count'] > 0:
            departmentservices_dict[dept_id]['TotalServicessalary_headcount_contract'] = (
                departmentservices_dict[dept_id]['TotalServicesmultiplication_result'] / departmentservices_dict[dept_id]['TotalServiceshead_count']
            )

        divisions_qs = ServicesDivisionMaster.objects.filter(
            servicesdepartmentmaster__DepartmentName=dept_id,IsDelete=False,
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')

        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name and division_name not in divisionservices_dict:
            divisionservices_dict[division_name] = {
                'Servicedivisionmultiplication_result': 0,
                'Servicedivisiontotal_headcount': 0,
                'Servicedivisionsalary_headcount_product': 0,
            }

        if division_name:
            divisionservices_dict[division_name]['Servicedivisionmultiplication_result'] += departmentservices_dict[dept_id]['TotalServicesmultiplication_result']
            divisionservices_dict[division_name]['Servicedivisiontotal_headcount'] += departmentservices_dict[dept_id]['TotalServiceshead_count']

            if divisionservices_dict[division_name]['Servicedivisiontotal_headcount'] > 0:
                divisionservices_dict[division_name]['Servicedivisionsalary_headcount_product'] = (
                    divisionservices_dict[division_name]['Servicedivisionmultiplication_result'] / divisionservices_dict[division_name]['Servicedivisiontotal_headcount']
                )

    
    Servicesgranddivisionmultiplication_result = sum(
        dept['Servicedivisionmultiplication_result'] for dept in divisionservices_dict.values() if 'Servicedivisionmultiplication_result' in dept
    )

    ServicesContractgrand_total_headcount = sum(
        dept['Servicedivisiontotal_headcount'] for dept in divisionservices_dict.values() if 'Servicedivisiontotal_headcount' in dept
    )

    if ServicesContractgrand_total_headcount > 0:
        Servicesgrandsalarydivion = Servicesgranddivisionmultiplication_result / ServicesContractgrand_total_headcount
    else:
        Servicesgrandsalarydivion = 0
    
    
    meal_cost_record = EntryActualMealCost.objects.filter(hotel_name=selectedOrganizationID,IsDelete=False).first()

    if meal_cost_record:
        meal_cost = meal_cost_record.cafeteriamealcost
    else:
        meal_cost = 0


    Insurance_cost_record = EntryActualInsuranceCost.objects.filter(hotel_name=selectedOrganizationID,IsDelete=False).first()

    if Insurance_cost_record:
        insurance_cost = Insurance_cost_record.EmployeeInsurancecost
    else:
        insurance_cost = 0
       
    # benefites total 
    # Ensure all variables have valid numeric values
    grand_total_headcount = grand_total_headcount or 0
    Contractgrand_total_headcount = Contractgrand_total_headcount or 0
    ServicesContractgrand_total_headcount = ServicesContractgrand_total_headcount or 0
    grand_total_salary = grand_total_salary or 0
    grandContractdivisionmultiplication_result = grandContractdivisionmultiplication_result or 0
    Servicesgranddivisionmultiplication_result = Servicesgranddivisionmultiplication_result or 0
    meal_cost = meal_cost or 0
    insurance_cost = insurance_cost or 0

    # Calculate Benefitesheadtotal and Benefitetotalctc
    Benefitesheadtotal = (
        grand_total_headcount + 
        Contractgrand_total_headcount + 
        ServicesContractgrand_total_headcount
    )

    Benefitetotalctc = (
        grand_total_salary + 
        grandContractdivisionmultiplication_result + 
        Servicesgranddivisionmultiplication_result + 
        meal_cost + 
        insurance_cost
    )

    if Benefitesheadtotal > 0:
        Avgsalarytotalctc = Benefitetotalctc / Benefitesheadtotal
    else:
        Avgsalarytotalctc = 0
    

    if Benefitesheadtotal > 0:
        Avgsalarymealcoat = meal_cost / Benefitesheadtotal
    else:
        Avgsalarymealcoat = 0
    
    insuranceheadcount = grand_total_headcount  +  ServicesContractgrand_total_headcount 

    if insuranceheadcount > 0:
        Avgsalaryinsurancecoat = insurance_cost / insuranceheadcount
    else:
        Avgsalaryinsurancecoat = 0

    # print("exclude_zero_headcount:", exclude_zero_headcount)
    context = {
        'divisions': Divisiondatas,
        'memOrg': memOrg,
        'employees_per_department_designation': employees_dict,
        'selectedOrganizationID': selectedOrganizationID,  
        'OrganizationID': OrganizationID,
        'contractdivisions': contractdivisions,
        'Servicedivisions': Servicedivisions,
        'department_totals': department_totals,
        'division_totals':division_totals,
        'grand_total_headcount':grand_total_headcount,
        'grand_total_salary':grand_total_salary,
        # 'grandsalarydivion':grandsalarydivion,
        'Divisiondatas':Divisiondatas,
        'Departmentsdatas':Departmentsdatas,
        'selected_division':selected_division,
        'selected_department':selected_department,
        'Contractbudgets_dict' :Contractbudgets_dict,
        'Contractdepartment_totals':Contractdepartment_totals,
        'Contractdivision_totals':Contractdivision_totals,
        'grandContractdivisionmultiplication_result':grandContractdivisionmultiplication_result,
        'Contractgrand_total_headcount':Contractgrand_total_headcount,
        'contractgrandsalarydivion':contractgrandsalarydivion,
        'Servicesbudgets_dict' :Servicesbudgets_dict,
        'departmentservices_dict' : departmentservices_dict,
        'divisionservices_dict' : divisionservices_dict,
        'Servicesgranddivisionmultiplication_result': Servicesgranddivisionmultiplication_result,
        'ServicesContractgrand_total_headcount': ServicesContractgrand_total_headcount,
        'Servicesgrandsalarydivion': Servicesgrandsalarydivion,
        'insurance_cost':insurance_cost,
        'meal_cost':meal_cost,
        'grandsalarydivion':grandsalarydivion,
        'Benefitesheadtotal':Benefitesheadtotal,
        'Benefitetotalctc':Benefitetotalctc,
        'Avgsalarytotalctc':Avgsalarytotalctc,
        'Avgsalarymealcoat':Avgsalarymealcoat,
        'Avgsalaryinsurancecoat':Avgsalaryinsurancecoat,
        'exclude_zero_headcount':exclude_zero_headcount

    }

    return render(request, "manningguide/EntryActual/EntryViewActual.html", context)














from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Count, Sum, Q, FloatField
from django.db.models import F, ExpressionWrapper
from datetime import datetime
import requests
import logging
from xhtml2pdf import pisa



logger = logging.getLogger(__name__)

def EntryActualPdf(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")


    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  
    UserID = request.session.get("UserID")
    fullname = request.session["FullName"]
    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    selectedOrganizationID = str(request.GET.get('hotel_name', OrganizationID))
    exclude_zero_headcount = request.GET.get('exclude_zero_headcount')
    selected_division = request.GET.get('divisionname')
    selected_department = request.GET.get('departmentname')
    

    include_on_roll = request.GET.get('include_on_roll') == 'true'
    include_contract = request.GET.get('include_contract') == 'true'
    include_shared_services = request.GET.get('include_shared_services') == 'true'
    include_cafeteria = request.GET.get('include_cafeteria') == 'true'
    include_insurance = request.GET.get('include_insurance') == 'true'
    

    employees_per_department_designation = EmployeeWorkDetails.objects.filter(OrganizationID=selectedOrganizationID,IsDelete=False,IsSecondary=False,EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"])
    
    if exclude_zero_headcount:  
        employees_per_department_designation = employees_per_department_designation.exclude(id=0)
    
     
    Contractbudget_department_designation = EntryActualContract.objects.filter(OrganizationID=selectedOrganizationID)
    if exclude_zero_headcount:  
        Contractbudget_department_designation = Contractbudget_department_designation.exclude(head_count=0)
   
    Servicesbudget_department_designation = EntryActualSharedServices.objects.filter(OrganizationID=selectedOrganizationID)
    if exclude_zero_headcount:  
        Servicesbudget_department_designation = Servicesbudget_department_designation.exclude(head_count=0)






    template_path = 'manningguide/EntryActual/EntryActualPdf.html'
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')

    selected_organization = next((org for org in memOrg if str(org.get('OrganizationID')) == selectedOrganizationID), None)
    selectedOrganizationName = selected_organization['Organization_name'] if selected_organization else "Unknown Organization"

    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organization = OrganizationMaster.objects.filter(OrganizationID=selectedOrganizationID).first()
    organization_logo = f"{base_url}{organization.OrganizationLogo}" if organization and organization.OrganizationLogo else None

    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False)
    departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)

    if selected_division and selected_division != 'All Division':
        Divisiondatas = Divisiondatas.filter(DivisionName=selected_division)
        departments = OnRollDepartmentMaster.objects.filter(
            OnRollDivisionMaster__DivisionName=selected_division, IsDelete=False
        )
    if selected_department and selected_department != 'All Department':
        departments = departments.filter(DepartmentName=selected_department)

    filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

       
    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
            Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
            Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
        )
    
    filtered_contract_departments = ContractDepartmentMaster.objects.filter(IsDelete=False)
    filtered_contract_designations = ContractDesignationMaster.objects.filter(IsDelete=False)

    
    filtered_service_departments = ServicesDepartmentMaster.objects.filter(IsDelete=False)
    filtered_service_designations = ServicesDesignationMaster.objects.filter(IsDelete=False)

    
    contractdivisions = ContractDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('contractdepartmentmaster_set', queryset=filtered_contract_departments),
        Prefetch('contractdepartmentmaster_set__contractdesignationmaster_set', queryset=filtered_contract_designations)
    )

    
    Servicedivisions = ServicesDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('servicesdepartmentmaster_set', queryset=filtered_service_departments),
        Prefetch('servicesdepartmentmaster_set__servicesdesignationmaster_set', queryset=filtered_service_designations)
    )
    

    employees_per_department_designation = EmployeeWorkDetails.objects.filter(OrganizationID=selectedOrganizationID,IsDelete=False,IsSecondary=False,EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"]).exclude(
        Department__isnull=True
    ).exclude(
        Department=''
    )

    employees_per_department_designation = (
        employees_per_department_designation
        .values('Department', 'Designation')
        .annotate(
            num_employees=Count('id'),
            total_salary=Sum('Salary', filter=Q(Salary__isnull=False, Salary__gt=0)),
            avg_salary=ExpressionWrapper(
                Sum('Salary', filter=Q(Salary__isnull=False, Salary__gt=0)) / Count('id'),
                output_field=FloatField()
            )
        )
        .order_by('Department', 'Designation')
    )

    logger.debug(f"Annotated employees_per_department_designation queryset: {employees_per_department_designation}")

    department_totals = {}
    employees_dict = {}
    division_totals = {}

    for emp in employees_per_department_designation:
        dept = emp['Department']
        department_name = dept
        designation = emp['Designation']
        avg_salary = emp['avg_salary'] or 0  # Default to 0 if None
        num_employees = emp['num_employees'] or 0  # Default to 0 if None
        multiplication_result = avg_salary * num_employees

        divisions_qs = OnRollDivisionMaster.objects.filter(
            onrolldepartmentmaster__DepartmentName=department_name
        ).annotate(
            department_name=F('onrolldepartmentmaster__DepartmentName')
        ).values(
            'DivisionName',  
        )

        logger.debug(f"Divisions queryset for department '{department_name}': {divisions_qs}")

        division_name = divisions_qs[0]['DivisionName'] if divisions_qs else None

        if dept not in department_totals:
            department_totals[dept] = {
                'total_salarymulti': 0,
                'total_headcount': 0,
                'salary_headcount_product': 0,
            }

        if division_name and division_name not in division_totals:
            division_totals[division_name] = {
                'divisiontotal_salarymulti': 0,
                'divisiontotal_headcount': 0,
                'divisionsalary_headcount_product': 0,
            }

        if dept not in employees_dict:
            employees_dict[dept] = {}

        employees_dict[dept][designation] = {
            'num_employees': num_employees,
            'avg_salary': avg_salary,
            'multiplication_result': multiplication_result  
        }

        department_totals[dept]['total_salarymulti'] += avg_salary
        department_totals[dept]['total_headcount'] += num_employees
        department_totals[dept]['salary_headcount_product'] = (
            department_totals[dept]['total_salarymulti'] / department_totals[dept]['total_headcount']
        )

        if division_name:
            division_totals[division_name]['divisiontotal_salarymulti'] += avg_salary
            division_totals[division_name]['divisiontotal_headcount'] += num_employees
            division_totals[division_name]['divisionsalary_headcount_product'] = (
                division_totals[division_name]['divisiontotal_salarymulti'] / division_totals[division_name]['divisiontotal_headcount']
            )

    if exclude_zero_headcount:
        employees_per_department_designation = employees_per_department_designation.exclude(num_employees=0)

    grand_total_salary = sum(department['divisiontotal_salarymulti'] for department in division_totals.values() if 'divisiontotal_salarymulti' in department)
    grand_total_headcount = sum(department['divisiontotal_headcount'] for department in division_totals.values() if 'divisiontotal_headcount' in department)
   


    if grand_total_headcount > 0:
        grandsalarydivion = grand_total_salary / grand_total_headcount
    else:
        grandsalarydivion = 0
# <!-- contract budget  -->

    Contractbudget_department_designation = EntryActualContract.objects.filter(
            hotel_name=selectedOrganizationID,
        ).values(
            'contract_department_master__DepartmentName',  
            'contract_designation_master__designations'      
        ).annotate(
            Contracthead_count=Sum('head_count'),
            Contracttotal_salary=Sum('avg_salary'),
            Contractavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
            Contractmultiplication_result=ExpressionWrapper(F('Contractavg_salary') * F('Contracthead_count'), output_field=FloatField())
        ).order_by(
            'contract_department_master__DepartmentName',    
            'contract_designation_master__designations'       
        )
    
        
    Contractbudgets_dict = {}
    Contractdepartment_totals = {}
    Contractdivision_totals = {}

        
    for Contractbudget in Contractbudget_department_designation:
            dept_id = Contractbudget['contract_department_master__DepartmentName']
            desig_id = Contractbudget['contract_designation_master__designations']

            if dept_id not in Contractbudgets_dict:
                Contractbudgets_dict[dept_id] = {}

            Contractbudgets_dict[dept_id][desig_id] = {
                'Contracthead_count': Contractbudget['Contracthead_count'],
                'Contractavg_salary': Contractbudget['Contractavg_salary'],
                'Contractmultiplication_result': Contractbudget['Contractmultiplication_result'],
            }

            if dept_id not in Contractdepartment_totals:
                Contractdepartment_totals[dept_id] = {
                    'Contractmultiplication_result': 0,
                    'Contracthead_count': 0,
                    'salary_headcount_contract': 0,
                }

            Contractdepartment_totals[dept_id]['Contractmultiplication_result'] += Contractbudget['Contractmultiplication_result']
            Contractdepartment_totals[dept_id]['Contracthead_count'] += Contractbudget['Contracthead_count']

            if Contractdepartment_totals[dept_id]['Contracthead_count'] > 0:
                Contractdepartment_totals[dept_id]['salary_headcount_contract'] = (
                    Contractdepartment_totals[dept_id]['Contractmultiplication_result'] / Contractdepartment_totals[dept_id]['Contracthead_count']
                )

            
            divisions_qs = ContractDivisionMaster.objects.filter(
                contractdepartmentmaster__DepartmentName=dept_id
            ).annotate(
                division_name=F('DivisionName')
            ).values('division_name')

            division_name = divisions_qs[0]['division_name'] if divisions_qs else None

            if division_name and division_name not in Contractdivision_totals:
                Contractdivision_totals[division_name] = {
                    'Contractdivisionmultiplication_result': 0,
                    'Contractdivisiontotal_headcount': 0,
                    'Contractdivisionsalary_headcount_product': 0,
                }

            if division_name:
                Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] += Contractbudget['Contractmultiplication_result']
                Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] += Contractbudget['Contracthead_count']

                if Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] > 0:
                    Contractdivision_totals[division_name]['Contractdivisionsalary_headcount_product'] = (
                        Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] / Contractdivision_totals[division_name]['Contractdivisiontotal_headcount']
                    )
    grandContractdivisionmultiplication_result = sum(
        dept['Contractdivisionmultiplication_result'] for dept in Contractdivision_totals.values() if 'Contractdivisionmultiplication_result' in dept
    )
    Contractgrand_total_headcount = sum(
        dept['Contractdivisiontotal_headcount'] for dept in Contractdivision_totals.values() if 'Contractdivisiontotal_headcount' in dept
    )
    
    if Contractgrand_total_headcount > 0:
        contractgrandsalarydivion = grandContractdivisionmultiplication_result / Contractgrand_total_headcount
    else:
        contractgrandsalarydivion = 0  
    

    # <!-- Shared Services Budget  -->
    Servicesbudget_department_designation = EntryActualSharedServices.objects.filter(
        hotel_name=selectedOrganizationID,
    ).values(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    ).annotate(
        Serviceshead_count=Sum('head_count'),
        Servicestotal_salary=Sum('avg_salary'),
        Servicesavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        Servicesmultiplication_result=F('Servicesavg_salary') * F('Serviceshead_count')
    ).order_by(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    )

    Servicesbudgets_dict = {}
    departmentservices_dict = {}
    divisionservices_dict = {}

    for Servicesbudget in Servicesbudget_department_designation:
        dept_id = Servicesbudget['services_department_master__DepartmentName']
        desig_id = Servicesbudget['services_designation_master__designations']

        if dept_id not in Servicesbudgets_dict:
            Servicesbudgets_dict[dept_id] = {}

        Servicesbudgets_dict[dept_id][desig_id] = {
            'Serviceshead_count': Servicesbudget['Serviceshead_count'],
            'Servicesavg_salary': Servicesbudget['Servicesavg_salary'],
            'Servicesmultiplication_result': Servicesbudget['Servicesmultiplication_result'],
        }


        if dept_id not in departmentservices_dict:
            departmentservices_dict[dept_id] = {
                'TotalServicesmultiplication_result': 0,
                'TotalServiceshead_count': 0,
                'TotalServicessalary_headcount_contract': 0,
            }

        departmentservices_dict[dept_id]['TotalServicesmultiplication_result'] += (
            Servicesbudget['Servicesmultiplication_result'] or 0
        )

        # Safely add 'Serviceshead_count'
        departmentservices_dict[dept_id]['TotalServiceshead_count'] += (
            Servicesbudget['Serviceshead_count'] or 0
        )

        if departmentservices_dict[dept_id]['TotalServiceshead_count'] > 0:
            departmentservices_dict[dept_id]['TotalServicessalary_headcount_contract'] = (
                departmentservices_dict[dept_id]['TotalServicesmultiplication_result'] / departmentservices_dict[dept_id]['TotalServiceshead_count']
            )

        divisions_qs = ServicesDivisionMaster.objects.filter(
            servicesdepartmentmaster__DepartmentName=dept_id
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')

        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name and division_name not in divisionservices_dict:
            divisionservices_dict[division_name] = {
                'Servicedivisionmultiplication_result': 0,
                'Servicedivisiontotal_headcount': 0,
                'Servicedivisionsalary_headcount_product': 0,
            }

        if division_name:
            divisionservices_dict[division_name]['Servicedivisionmultiplication_result'] += departmentservices_dict[dept_id]['TotalServicesmultiplication_result']
            divisionservices_dict[division_name]['Servicedivisiontotal_headcount'] += departmentservices_dict[dept_id]['TotalServiceshead_count']

            if divisionservices_dict[division_name]['Servicedivisiontotal_headcount'] > 0:
                divisionservices_dict[division_name]['Servicedivisionsalary_headcount_product'] = (
                    divisionservices_dict[division_name]['Servicedivisionmultiplication_result'] / divisionservices_dict[division_name]['Servicedivisiontotal_headcount']
                )

    
    Servicesgranddivisionmultiplication_result = sum(
        dept['Servicedivisionmultiplication_result'] for dept in divisionservices_dict.values() if 'Servicedivisionmultiplication_result' in dept
    )

    ServicesContractgrand_total_headcount = sum(
        dept['Servicedivisiontotal_headcount'] for dept in divisionservices_dict.values() if 'Servicedivisiontotal_headcount' in dept
    )

    if ServicesContractgrand_total_headcount > 0:
        Servicesgrandsalarydivion = Servicesgranddivisionmultiplication_result / ServicesContractgrand_total_headcount
    else:
        Servicesgrandsalarydivion = 0
    
    
    meal_cost_record = EntryActualMealCost.objects.filter(hotel_name=selectedOrganizationID).first()

    if meal_cost_record:
        meal_cost = meal_cost_record.cafeteriamealcost
    else:
        meal_cost = 0


    Insurance_cost_record = EntryActualInsuranceCost.objects.filter(hotel_name=selectedOrganizationID).first()

    if Insurance_cost_record:
        insurance_cost = Insurance_cost_record.EmployeeInsurancecost
    else:
        insurance_cost = 0
       
    # benefites total 
    # Ensure no None values in the calculation
    Benefitesheadtotal = (grand_total_headcount or 0) + (Contractgrand_total_headcount or 0) + (ServicesContractgrand_total_headcount or 0)

    Benefitetotalctc = (grand_total_salary or 0) + (grandContractdivisionmultiplication_result or 0) + (Servicesgranddivisionmultiplication_result or 0) + (meal_cost or 0) + (insurance_cost or 0)

    if Benefitesheadtotal > 0:
        Avgsalarytotalctc = Benefitetotalctc / Benefitesheadtotal
    else:
        Avgsalarytotalctc = 0
    

    if Benefitesheadtotal > 0:
        Avgsalarymealcoat = meal_cost / Benefitesheadtotal
    else:
        Avgsalarymealcoat = 0
    
    insuranceheadcount = grand_total_headcount  +  ServicesContractgrand_total_headcount 

    if insuranceheadcount not in (None, 0) and insurance_cost is not None:
        Avgsalaryinsurancecoat = insurance_cost / insuranceheadcount
    else:
        Avgsalaryinsurancecoat = 0 
    context = {
        'divisions': Divisiondatas if include_on_roll else None,
        'Contractdivisions': contractdivisions if include_contract else None,
        'current_datetime': datetime.now().strftime('%d %B %Y %H:%M:%S'),
        'UserID': UserID,
        'employees_per_department_designation': employees_dict,
        'department_totals': department_totals,
        'division_totals': division_totals,
        'selectedOrganizationID': selectedOrganizationID,
        'selectedOrganizationName': selectedOrganizationName,
        'organization_logo': organization_logo,
        'organization_logos': organization_logos,
        'grand_total_headcount': grand_total_headcount,
        'grand_total_salary': grand_total_salary,
       
        'Servicedivisions': Servicedivisions if include_shared_services else None,
        'cafeteria_meal_cost': 'Data for Cafeteria Meal Cost' if include_cafeteria else None,
        'employees_insurance_cost': 'Data for Employees Insurance Cost' if include_insurance else None,

        'Contractbudgets_dict' :Contractbudgets_dict,
        'Contractdepartment_totals':Contractdepartment_totals,
        'Contractdivision_totals':Contractdivision_totals,
        'grandContractdivisionmultiplication_result':grandContractdivisionmultiplication_result,
        'Contractgrand_total_headcount':Contractgrand_total_headcount,
        'contractgrandsalarydivion':contractgrandsalarydivion,
         'Servicesbudgets_dict' :Servicesbudgets_dict,
         'departmentservices_dict' : departmentservices_dict,
         'divisionservices_dict' : divisionservices_dict,
         'Servicesgranddivisionmultiplication_result': Servicesgranddivisionmultiplication_result,
         'ServicesContractgrand_total_headcount': ServicesContractgrand_total_headcount,
         'Servicesgrandsalarydivion': Servicesgrandsalarydivion,
         'insurance_cost':insurance_cost,
         'meal_cost':meal_cost,
         'grandsalarydivion':grandsalarydivion,
         'Benefitesheadtotal':Benefitesheadtotal,
         'Benefitetotalctc':Benefitetotalctc,
         'Avgsalarytotalctc':Avgsalarytotalctc,
         'Avgsalarymealcoat':Avgsalarymealcoat,
         'Avgsalaryinsurancecoat':Avgsalaryinsurancecoat,
         'fullname':fullname,
         'exclude_zero_headcount':exclude_zero_headcount
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="EntryActual.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response






from django.db.models.functions import Trim
from django.db.models import Count, Sum, FloatField, F, ExpressionWrapper
from django.shortcuts import render, redirect
import requests

def ViewBudget(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = str(request.session.get("UserID"))
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    if not OrganizationID:
        logger.error("OrganizationID not found in session or is empty.")
        return redirect('MasterAttribute.Host')

    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = None

    selected_division = request.GET.get('divisionname')
    selected_department = request.GET.get('departmentname')
    selected_organization_id = request.GET.get('hotel_name', OrganizationID)
    exclude_zero_headcount = request.GET.get('exclude_zero_headcount','1')  

    if UserType == 'CEO' and request.GET.get('hotel_name') is None:
        selected_organization_id = 401

    
    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False)
    departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)

    if selected_division and selected_division != 'All Division':
        Divisiondatas = Divisiondatas.filter(DivisionName=selected_division)
        departments = OnRollDepartmentMaster.objects.filter(
            OnRollDivisionMaster__DivisionName=selected_division, IsDelete=False
        )
    if selected_department and selected_department != 'All Department':
        departments = departments.filter(DepartmentName=selected_department)

   
    # contractdivisions = ContractDivisionMaster.objects.all().order_by('Order').prefetch_related(
    #     'contractdepartmentmaster_set__contractdesignationmaster_set'
    # )
    # Servicedivisions = ServicesDivisionMaster.objects.all().order_by('Order').prefetch_related(
    #     'servicesdepartmentmaster_set__servicesdesignationmaster_set'
    # )
    
    filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

       
    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
            Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
            Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
        )
    
    filtered_contract_departments = ContractDepartmentMaster.objects.filter(IsDelete=False)
    filtered_contract_designations = ContractDesignationMaster.objects.filter(IsDelete=False)

    
    filtered_service_departments = ServicesDepartmentMaster.objects.filter(IsDelete=False)
    filtered_service_designations = ServicesDesignationMaster.objects.filter(IsDelete=False)

    
    contractdivisions = ContractDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('contractdepartmentmaster_set', queryset=filtered_contract_departments),
        Prefetch('contractdepartmentmaster_set__contractdesignationmaster_set', queryset=filtered_contract_designations)
    )

    
    Servicedivisions = ServicesDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('servicesdepartmentmaster_set', queryset=filtered_service_departments),
        Prefetch('servicesdepartmentmaster_set__servicesdesignationmaster_set', queryset=filtered_service_designations)
    )
    
    
    managebudget_department_designation = ManageBudgetOnRoll.objects.filter(OrganizationID=selected_organization_id)
    
    # if exclude_zero_headcount:  
    #     managebudget_department_designation = managebudget_department_designation.exclude(head_count=0)
    
    Contractbudget_department_designation = ManageBudgetContract.objects.filter(OrganizationID=selected_organization_id)
    if exclude_zero_headcount:  
        Contractbudget_department_designation = Contractbudget_department_designation.exclude(head_count=0)
   
    Servicesbudget_department_designation = ManageBudgetSharedServices.objects.filter(OrganizationID=selected_organization_id)
    if exclude_zero_headcount:  
        Servicesbudget_department_designation = Servicesbudget_department_designation.exclude(head_count=0)

 


    

    managebudget_department_designation = ManageBudgetOnRoll.objects.annotate(
        clean_hotel_name=Trim('hotel_name')  
    ).filter(
        clean_hotel_name=selected_organization_id,  
        is_delete=False
    ).values(
        
        'on_roll_division_master__DivisionName',
       
        'on_roll_department_master__DepartmentName',
        
        'on_roll_designation_master__designations'
    ).annotate(
        head_count=F('head_count'),
        total_salary=Sum('avg_salary'),
        aavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        budgetmultiplication_result=ExpressionWrapper(F('aavg_salary') * F('head_count'), output_field=FloatField())
    ).order_by(
        'on_roll_division_master__DivisionName',
        'on_roll_department_master__DepartmentName',
        'on_roll_designation_master__designations'
    )
    
    if exclude_zero_headcount == '1':  
        managebudget_department_designation = managebudget_department_designation.exclude(head_count=0)
    
    print("exclude_zero_headcount value::", exclude_zero_headcount)
    
        
    budgets_dict = {}
    department_totals = {}
    division_totals = {}

    for budget in managebudget_department_designation:
        dept_id = budget['on_roll_department_master__DepartmentName']
        desig_id = budget['on_roll_designation_master__designations']

        if dept_id not in budgets_dict:
            budgets_dict[dept_id] = {}

        budgets_dict[dept_id][desig_id] = {
            'head_count': budget['head_count'],
            'aavg_salary': budget['aavg_salary'],
            'budgetmultiplication_result': budget['budgetmultiplication_result'],
        }

        if dept_id not in department_totals:
            department_totals[dept_id] = {
                'budgetmultiplication_result': 0,
                'total_headcount': 0,
                'salary_headcount_product': 0,
            }

        department_totals[dept_id]['budgetmultiplication_result'] += budget.get('budgetmultiplication_result', 0) or 0
        department_totals[dept_id]['total_headcount'] += budget.get('head_count', 0) or 0

       
        if department_totals[dept_id]['total_headcount'] > 0:
            department_totals[dept_id]['salary_headcount_product'] = (
                department_totals[dept_id]['budgetmultiplication_result'] / department_totals[dept_id]['total_headcount']
            )

        divisions_qs = OnRollDivisionMaster.objects.filter(
            onrolldepartmentmaster__DepartmentName=dept_id
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')

        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name and division_name not in division_totals:
            division_totals[division_name] = {
                'divisionmultiplication_result': 0,
                'divisiontotal_headcount': 0,
                'divisionsalary_headcount_product': 0,
            }

        if division_name:
            division_totals[division_name]['divisionmultiplication_result'] += budget.get('budgetmultiplication_result', 0) or 0
            division_totals[division_name]['divisiontotal_headcount'] += budget.get('head_count', 0) or 0

            
            if division_totals[division_name]['divisiontotal_headcount'] > 0:
                division_totals[division_name]['divisionsalary_headcount_product'] = (
                    division_totals[division_name]['divisionmultiplication_result'] / division_totals[division_name]['divisiontotal_headcount']
                )

    
    divisionmultiplication_result = sum(
         dept['divisionmultiplication_result'] for dept in division_totals.values() if 'divisionmultiplication_result' in dept
     )
    grand_total_headcount = sum(
         dept['divisiontotal_headcount'] for dept in division_totals.values() if 'divisiontotal_headcount' in dept
     )
    # grandsalarydivion = divisionmultiplication_result / grand_total_headcount
    if grand_total_headcount > 0:
        grandsalarydivion = divisionmultiplication_result / grand_total_headcount
    else:
        grandsalarydivion = 0  

    
# <!-- contract budget  -->

    Contractbudget_department_designation = ManageBudgetContract.objects.filter(
            hotel_name=selected_organization_id,
        ).values(
            'contract_department_master__DepartmentName',  
            'contract_designation_master__designations'      
        ).annotate(
            Contracthead_count=Sum('head_count'),
            Contracttotal_salary=Sum('avg_salary'),
            Contractavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
            Contractmultiplication_result=ExpressionWrapper(F('Contractavg_salary') * F('Contracthead_count'), output_field=FloatField())
        ).order_by(
            'contract_department_master__DepartmentName',    
            'contract_designation_master__designations'       
        )
    
        
    Contractbudgets_dict = {}
    Contractdepartment_totals = {}
    Contractdivision_totals = {}

        
    for Contractbudget in Contractbudget_department_designation:
            dept_id = Contractbudget['contract_department_master__DepartmentName']
            desig_id = Contractbudget['contract_designation_master__designations']

            if dept_id not in Contractbudgets_dict:
                Contractbudgets_dict[dept_id] = {}

            Contractbudgets_dict[dept_id][desig_id] = {
                'Contracthead_count': Contractbudget['Contracthead_count'],
                'Contractavg_salary': Contractbudget['Contractavg_salary'],
                'Contractmultiplication_result': Contractbudget['Contractmultiplication_result'],
            }

            if dept_id not in Contractdepartment_totals:
                Contractdepartment_totals[dept_id] = {
                    'Contractmultiplication_result': 0,
                    'Contracthead_count': 0,
                    'salary_headcount_contract': 0,
                }

            Contractdepartment_totals[dept_id]['Contractmultiplication_result'] += Contractbudget.get('Contractmultiplication_result', 0) or 0
            Contractdepartment_totals[dept_id]['Contracthead_count'] += Contractbudget.get('Contracthead_count', 0) or 0


            if Contractdepartment_totals[dept_id]['Contracthead_count'] > 0:
                Contractdepartment_totals[dept_id]['salary_headcount_contract'] = (
                    Contractdepartment_totals[dept_id]['Contractmultiplication_result'] / Contractdepartment_totals[dept_id]['Contracthead_count']
                )

            
            divisions_qs = ContractDivisionMaster.objects.filter(
                contractdepartmentmaster__DepartmentName=dept_id
            ).annotate(
                division_name=F('DivisionName')
            ).values('division_name')

            division_name = divisions_qs[0]['division_name'] if divisions_qs else None

            if division_name and division_name not in Contractdivision_totals:
                Contractdivision_totals[division_name] = {
                    'Contractdivisionmultiplication_result': 0,
                    'Contractdivisiontotal_headcount': 0,
                    'Contractdivisionsalary_headcount_product': 0,
                }

            if division_name:
                Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] += Contractbudget.get('Contractmultiplication_result', 0) or 0
                Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] += Contractbudget.get('Contracthead_count', 0) or 0

                if Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] > 0:
                    Contractdivision_totals[division_name]['Contractdivisionsalary_headcount_product'] = (
                        Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] / Contractdivision_totals[division_name]['Contractdivisiontotal_headcount']
                    )
    grandContractdivisionmultiplication_result = sum(
        dept['Contractdivisionmultiplication_result'] for dept in Contractdivision_totals.values() if 'Contractdivisionmultiplication_result' in dept
    )
    Contractgrand_total_headcount = sum(
        dept['Contractdivisiontotal_headcount'] for dept in Contractdivision_totals.values() if 'Contractdivisiontotal_headcount' in dept
    )

    
    if Contractgrand_total_headcount > 0:
        contractgrandsalarydivion = grandContractdivisionmultiplication_result / Contractgrand_total_headcount
    else:
        contractgrandsalarydivion = 0  

    

    # <!-- Shared Services Budget  -->
    Servicesbudget_department_designation = ManageBudgetSharedServices.objects.filter(
        hotel_name=selected_organization_id,
    ).values(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    ).annotate(
        Serviceshead_count=Sum('head_count'),
        Servicestotal_salary=Sum('avg_salary'),
        Servicesavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        Servicesmultiplication_result=F('Servicesavg_salary') * F('Serviceshead_count')
    ).order_by(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    )

    Servicesbudgets_dict = {}
    departmentservices_dict = {}
    divisionservices_dict = {}

    for Servicesbudget in Servicesbudget_department_designation:
        dept_id = Servicesbudget['services_department_master__DepartmentName']
        desig_id = Servicesbudget['services_designation_master__designations']

        if dept_id not in Servicesbudgets_dict:
            Servicesbudgets_dict[dept_id] = {}

        Servicesbudgets_dict[dept_id][desig_id] = {
            'Serviceshead_count': Servicesbudget['Serviceshead_count'],
            'Servicesavg_salary': Servicesbudget['Servicesavg_salary'],
            'Servicesmultiplication_result': Servicesbudget['Servicesmultiplication_result'],
        }


        if dept_id not in departmentservices_dict:
            departmentservices_dict[dept_id] = {
                'TotalServicesmultiplication_result': 0,
                'TotalServiceshead_count': 0,
                'TotalServicessalary_headcount_contract': 0,
            }

        departmentservices_dict[dept_id]['TotalServicesmultiplication_result'] += Servicesbudget.get('Servicesmultiplication_result', 0) or 0
        departmentservices_dict[dept_id]['TotalServiceshead_count'] += Servicesbudget.get('Serviceshead_count', 0) or 0

        if departmentservices_dict[dept_id]['TotalServiceshead_count'] > 0:
            departmentservices_dict[dept_id]['TotalServicessalary_headcount_contract'] = (
                departmentservices_dict[dept_id]['TotalServicesmultiplication_result'] / departmentservices_dict[dept_id]['TotalServiceshead_count']
            )

        divisions_qs = ServicesDivisionMaster.objects.filter(
            servicesdepartmentmaster__DepartmentName=dept_id
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')

        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name and division_name not in divisionservices_dict:
            divisionservices_dict[division_name] = {
                'Servicedivisionmultiplication_result': 0,
                'Servicedivisiontotal_headcount': 0,
                'Servicedivisionsalary_headcount_product': 0,
            }

        if division_name:
            divisionservices_dict[division_name]['Servicedivisionmultiplication_result'] += departmentservices_dict[dept_id]['TotalServicesmultiplication_result']
            divisionservices_dict[division_name]['Servicedivisiontotal_headcount'] += departmentservices_dict[dept_id]['TotalServiceshead_count']

            if divisionservices_dict[division_name]['Servicedivisiontotal_headcount'] > 0:
                divisionservices_dict[division_name]['Servicedivisionsalary_headcount_product'] = (
                    divisionservices_dict[division_name]['Servicedivisionmultiplication_result'] / divisionservices_dict[division_name]['Servicedivisiontotal_headcount']
                )

    
    Servicesgranddivisionmultiplication_result = sum(
        dept['Servicedivisionmultiplication_result'] for dept in divisionservices_dict.values() if 'Servicedivisionmultiplication_result' in dept
    )

    ServicesContractgrand_total_headcount = sum(
        dept['Servicedivisiontotal_headcount'] for dept in divisionservices_dict.values() if 'Servicedivisiontotal_headcount' in dept
    )

    if ServicesContractgrand_total_headcount > 0:
        Servicesgrandsalarydivion = Servicesgranddivisionmultiplication_result / ServicesContractgrand_total_headcount
    else:
        Servicesgrandsalarydivion = 0

   

    meal_cost_record = BudgetMealCost.objects.filter(hotel_name=selected_organization_id).first()

    if meal_cost_record:
        meal_cost = meal_cost_record.cafeteriamealcost
    else:
        meal_cost = 0

    
# Employee Insurance Cost
    

    Insurance_cost_record = BudgetInsuranceCost.objects.filter(hotel_name=selected_organization_id).first()

    # Ensure Insurance_cost is a valid number
    if Insurance_cost_record and Insurance_cost_record.EmployeeInsurancecost is not None:
        Insurance_cost = Insurance_cost_record.EmployeeInsurancecost
    else:
        Insurance_cost = 0

    # Calculate insuranceheadcount
    insuranceheadcount = (grand_total_headcount or 0) + (ServicesContractgrand_total_headcount or 0)

    # Safely calculate Avgsalaryinsurancecoat
    if insuranceheadcount > 0:
        Avgsalaryinsurancecoat = Insurance_cost / insuranceheadcount
    else:
        Avgsalaryinsurancecoat = 0

    
        
        
# benefites total 
    Benefitesheadtotal = (
        (grand_total_headcount or 0) +
        (Contractgrand_total_headcount or 0) +
        (ServicesContractgrand_total_headcount or 0)
    )

    Benefitetotalctc = (
        (divisionmultiplication_result or 0) +
        (grandContractdivisionmultiplication_result or 0) +
        (Servicesgranddivisionmultiplication_result or 0) +
        (meal_cost or 0) +
        (Insurance_cost or 0)
    )

    Benefitetotalctc = Benefitetotalctc or 0  # If None, default to 0
    meal_cost = meal_cost or 0               # If None, default to 0
    Benefitesheadtotal = Benefitesheadtotal or 0  # If None, default to 0

    # Calculate average salary for total CTC
    if Benefitesheadtotal > 0:
        Avgsalarytotalctc = Benefitetotalctc / Benefitesheadtotal
    else:
        Avgsalarytotalctc = 0

    # Calculate average meal cost
    if Benefitesheadtotal > 0:
        Avgsalarymealcoat = meal_cost / Benefitesheadtotal
    else:
        Avgsalarymealcoat = 0
    



    context = {
        'contractdivisions': contractdivisions,
        'Servicedivisions': Servicedivisions,
        'divisions': Divisiondatas,
        'memOrg': memOrg,
        
        'selectedOrganizationID': selected_organization_id,
        'OrganizationID': OrganizationID,
      
        'Divisiondatas': Divisiondatas,
        'Departmentsdatas': departments,
        'selected_division':selected_division,
        'selected_department':selected_department,
       
        'Contractbudgets_dict':Contractbudgets_dict,
        'Servicesbudgets_dict':Servicesbudgets_dict,

        'budgets_dict': budgets_dict,
        'department_totals': department_totals,
        'division_totals': division_totals,
        'divisionmultiplication_result':divisionmultiplication_result,
        'grand_total_headcount': grand_total_headcount,
        'grandsalarydivion':grandsalarydivion,
        'Contractdepartment_totals':Contractdepartment_totals,
        'Contractdivision_totals':Contractdivision_totals,
        'grandContractdivisionmultiplication_result':grandContractdivisionmultiplication_result,
        'Contractgrand_total_headcount':Contractgrand_total_headcount,
        'contractgrandsalarydivion':contractgrandsalarydivion,
        'departmentservices_dict':departmentservices_dict,
        'divisionservices_dict':divisionservices_dict,
        'Servicesgranddivisionmultiplication_result':Servicesgranddivisionmultiplication_result,
        'ServicesContractgrand_total_headcount':ServicesContractgrand_total_headcount,
        'Servicesgrandsalarydivion':Servicesgrandsalarydivion,
        'meal_cost':meal_cost,
        'Insurance_cost':Insurance_cost,
        'Benefitesheadtotal':Benefitesheadtotal,
        'Benefitetotalctc':Benefitetotalctc,
        'Avgsalarytotalctc':Avgsalarytotalctc,
        'Avgsalarymealcoat':Avgsalarymealcoat,
        'Avgsalaryinsurancecoat':Avgsalaryinsurancecoat,
        'managebudget_department_designation': managebudget_department_designation,
        'exclude_zero_headcount': exclude_zero_headcount,
        'Contractbudget_department_designation':Contractbudget_department_designation
    }

    return render(request, "manningguide/ManageBudget/ViewBudget.html", context)



from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
from django.shortcuts import render
from datetime import datetime

def ViewBudgetPdf(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
   
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []
    
    selected_organization_id = str(request.GET.get('hotel_name', OrganizationID))
    selected_division = request.GET.get('divisionname')
    selected_department = request.GET.get('departmentname')
    exclude_zero_headcount = request.GET.get('exclude_zero_headcount')
    
    include_on_roll = request.GET.get('include_on_roll') == 'true'
    include_contract = request.GET.get('include_contract') == 'true'
    include_shared_services = request.GET.get('include_shared_services') == 'true'
    include_cafeteria = request.GET.get('include_cafeteria') == 'true'
    include_insurance = request.GET.get('include_insurance') == 'true'

    template_path = 'manningguide/ManageBudget/ViewBudgetPdf.html'
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')

    selected_organization = next((org for org in memOrg if str(org.get('OrganizationID')) == selected_organization_id), None)
    selectedOrganizationName = selected_organization['Organization_name'] if selected_organization else "Unknown Organization"

    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organization = OrganizationMaster.objects.filter(OrganizationID=selected_organization_id).first()
    organization_logo = f"{base_url}{organization.OrganizationLogo}" if organization and organization.OrganizationLogo else None

    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False)
    departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)

    if selected_division and selected_division != 'All Division':
        Divisiondatas = Divisiondatas.filter(DivisionName=selected_division)
        departments = OnRollDepartmentMaster.objects.filter(
            OnRollDivisionMaster__DivisionName=selected_division, IsDelete=False
        )
    if selected_department and selected_department != 'All Department':
        departments = departments.filter(DepartmentName=selected_department)

    # contractdivisions = ContractDivisionMaster.objects.all().order_by('Order').prefetch_related(
    #     'contractdepartmentmaster_set__contractdesignationmaster_set'
    # )
    # Servicedivisions = ServicesDivisionMaster.objects.all().order_by('Order').prefetch_related(
    #     'servicesdepartmentmaster_set__servicesdesignationmaster_set'
    # )
    
    filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

       
    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
            Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
            Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
        )
    
    filtered_contract_departments = ContractDepartmentMaster.objects.filter(IsDelete=False)
    filtered_contract_designations = ContractDesignationMaster.objects.filter(IsDelete=False)

    
    filtered_service_departments = ServicesDepartmentMaster.objects.filter(IsDelete=False)
    filtered_service_designations = ServicesDesignationMaster.objects.filter(IsDelete=False)

    
    contractdivisions = ContractDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('contractdepartmentmaster_set', queryset=filtered_contract_departments),
        Prefetch('contractdepartmentmaster_set__contractdesignationmaster_set', queryset=filtered_contract_designations)
    )

    
    Servicedivisions = ServicesDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('servicesdepartmentmaster_set', queryset=filtered_service_departments),
        Prefetch('servicesdepartmentmaster_set__servicesdesignationmaster_set', queryset=filtered_service_designations)
    )
    
    # managebudget_department_designation = ManageBudgetOnRoll.objects.filter(
    #     hotel_name=selected_organization_id,
    # ).values(
    #     'on_roll_department_master__DepartmentName',
    #     'on_roll_designation_master__designations'
    # ).annotate(
    #     head_count=Sum('head_count'),
    #     total_salary=Sum('avg_salary'),
    #     aavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
    #     budgetmultiplication_result=F('aavg_salary') * F('head_count')
    # ).order_by(
    #     'on_roll_department_master__DepartmentName',
    #     'on_roll_designation_master__designations'
    # )

    managebudget_department_designation = ManageBudgetOnRoll.objects.annotate(
        clean_hotel_name=Trim('hotel_name')  
    ).filter(
        clean_hotel_name=selected_organization_id,  
        is_delete=False
    ).values(
        
        'on_roll_division_master__DivisionName',
       
        'on_roll_department_master__DepartmentName',
        
        'on_roll_designation_master__designations'
    ).annotate(
        head_count=F('head_count'),
        total_salary=Sum('avg_salary'),
        aavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        budgetmultiplication_result=ExpressionWrapper(F('aavg_salary') * F('head_count'), output_field=FloatField())
    ).order_by(
        'on_roll_division_master__DivisionName',
        'on_roll_department_master__DepartmentName',
        'on_roll_designation_master__designations'
    )
    
    budgets_dict = {}
    department_totals = {}
    division_totals = {}

    for budget in managebudget_department_designation:
        dept_id = budget['on_roll_department_master__DepartmentName']
        desig_id = budget['on_roll_designation_master__designations']

        if dept_id not in budgets_dict:
            budgets_dict[dept_id] = {}

        budgets_dict[dept_id][desig_id] = {
            'head_count': budget['head_count'],
            'aavg_salary': budget['aavg_salary'],
            'budgetmultiplication_result': budget['budgetmultiplication_result'],
        }

        if dept_id not in department_totals:
            department_totals[dept_id] = {
                'budgetmultiplication_result': 0,
                'total_headcount': 0,
                'salary_headcount_product': 0,
            }

        
        department_totals[dept_id]['budgetmultiplication_result'] += (
                budget['budgetmultiplication_result'] or 0
            )

            # Safely add 'head_count'
        department_totals[dept_id]['total_headcount'] += (
                budget['head_count'] or 0
            )
       
        if department_totals[dept_id]['total_headcount'] > 0:
            department_totals[dept_id]['salary_headcount_product'] = (
                department_totals[dept_id]['budgetmultiplication_result'] / department_totals[dept_id]['total_headcount']
            )

        divisions_qs = OnRollDivisionMaster.objects.filter(
            onrolldepartmentmaster__DepartmentName=dept_id
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')

        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name and division_name not in division_totals:
            division_totals[division_name] = {
                'divisionmultiplication_result': 0,
                'divisiontotal_headcount': 0,
                'divisionsalary_headcount_product': 0,
            }

        if division_name:
            # division_totals[division_name]['divisionmultiplication_result'] += budget['budgetmultiplication_result']
            # division_totals[division_name]['divisiontotal_headcount'] += budget['head_count']
            division_totals[division_name]['divisionmultiplication_result'] += (
                budget['budgetmultiplication_result'] or 0
            )

            # Safely add 'head_count'
            division_totals[division_name]['divisiontotal_headcount'] += (
                budget['head_count'] or 0
            )
            
            if division_totals[division_name]['divisiontotal_headcount'] > 0:
                division_totals[division_name]['divisionsalary_headcount_product'] = (
                    division_totals[division_name]['divisionmultiplication_result'] / division_totals[division_name]['divisiontotal_headcount']
                )

    
    divisionmultiplication_result = sum(
         dept['divisionmultiplication_result'] for dept in division_totals.values() if 'divisionmultiplication_result' in dept
     )
    grand_total_headcount = sum(
         dept['divisiontotal_headcount'] for dept in division_totals.values() if 'divisiontotal_headcount' in dept
     )
    # grandsalarydivion = divisionmultiplication_result / grand_total_headcount
    if grand_total_headcount > 0:
        grandsalarydivion = divisionmultiplication_result / grand_total_headcount
    else:
        grandsalarydivion = 0  

    
# <!-- contract budget  -->

    Contractbudget_department_designation = ManageBudgetContract.objects.filter(
            hotel_name=selected_organization_id,
        ).values(
            'contract_department_master__DepartmentName',  
            'contract_designation_master__designations'      
        ).annotate(
            Contracthead_count=Sum('head_count'),
            Contracttotal_salary=Sum('avg_salary'),
            Contractavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
            Contractmultiplication_result=ExpressionWrapper(F('Contractavg_salary') * F('Contracthead_count'), output_field=FloatField())
        ).order_by(
            'contract_department_master__DepartmentName',    
            'contract_designation_master__designations'       
        )

        
    Contractbudgets_dict = {}
    Contractdepartment_totals = {}
    Contractdivision_totals = {}

        
    for Contractbudget in Contractbudget_department_designation:
            dept_id = Contractbudget['contract_department_master__DepartmentName']
            desig_id = Contractbudget['contract_designation_master__designations']

            if dept_id not in Contractbudgets_dict:
                Contractbudgets_dict[dept_id] = {}

            Contractbudgets_dict[dept_id][desig_id] = {
                'Contracthead_count': Contractbudget['Contracthead_count'],
                'Contractavg_salary': Contractbudget['Contractavg_salary'],
                'Contractmultiplication_result': Contractbudget['Contractmultiplication_result'],
            }

            if dept_id not in Contractdepartment_totals:
                Contractdepartment_totals[dept_id] = {
                    'Contractmultiplication_result': 0,
                    'Contracthead_count': 0,
                    'salary_headcount_contract': 0,
                }

            # Contractdepartment_totals[dept_id]['Contractmultiplication_result'] += Contractbudget['Contractmultiplication_result']
            # Contractdepartment_totals[dept_id]['Contracthead_count'] += Contractbudget['Contracthead_count']
            Contractdepartment_totals[dept_id]['Contractmultiplication_result'] += (
                Contractbudget['Contractmultiplication_result'] or 0
            )

           
            Contractdepartment_totals[dept_id]['Contracthead_count'] += (
                Contractbudget['Contracthead_count'] or 0
            )
            if Contractdepartment_totals[dept_id]['Contracthead_count'] > 0:
                Contractdepartment_totals[dept_id]['salary_headcount_contract'] = (
                    Contractdepartment_totals[dept_id]['Contractmultiplication_result'] / Contractdepartment_totals[dept_id]['Contracthead_count']
                )

            
            divisions_qs = ContractDivisionMaster.objects.filter(
                contractdepartmentmaster__DepartmentName=dept_id
            ).annotate(
                division_name=F('DivisionName')
            ).values('division_name')

            division_name = divisions_qs[0]['division_name'] if divisions_qs else None

            if division_name and division_name not in Contractdivision_totals:
                Contractdivision_totals[division_name] = {
                    'Contractdivisionmultiplication_result': 0,
                    'Contractdivisiontotal_headcount': 0,
                    'Contractdivisionsalary_headcount_product': 0,
                }

            if division_name:
                # Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] += Contractbudget['Contractmultiplication_result']
                # Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] += Contractbudget['Contracthead_count']
                Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] += (
                    Contractbudget['Contractmultiplication_result'] or 0
                )

                # Safely add 'Contracthead_count'
                Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] += (
                    Contractbudget['Contracthead_count'] or 0
                )
                if Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] > 0:
                    Contractdivision_totals[division_name]['Contractdivisionsalary_headcount_product'] = (
                        Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] / Contractdivision_totals[division_name]['Contractdivisiontotal_headcount']
                    )
    grandContractdivisionmultiplication_result = sum(
        dept['Contractdivisionmultiplication_result'] for dept in Contractdivision_totals.values() if 'Contractdivisionmultiplication_result' in dept
    )
    Contractgrand_total_headcount = sum(
        dept['Contractdivisiontotal_headcount'] for dept in Contractdivision_totals.values() if 'Contractdivisiontotal_headcount' in dept
    )

    
    if Contractgrand_total_headcount > 0:
        contractgrandsalarydivion = grandContractdivisionmultiplication_result / Contractgrand_total_headcount
    else:
        contractgrandsalarydivion = 0  

    

    # <!-- Shared Services Budget  -->
    Servicesbudget_department_designation = ManageBudgetSharedServices.objects.filter(
        hotel_name=selected_organization_id,
    ).values(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    ).annotate(
        Serviceshead_count=Sum('head_count'),
        Servicestotal_salary=Sum('avg_salary'),
        Servicesavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        Servicesmultiplication_result=F('Servicesavg_salary') * F('Serviceshead_count')
    ).order_by(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    )

    Servicesbudgets_dict = {}
    departmentservices_dict = {}
    divisionservices_dict = {}

    for Servicesbudget in Servicesbudget_department_designation:
        dept_id = Servicesbudget['services_department_master__DepartmentName']
        desig_id = Servicesbudget['services_designation_master__designations']

        if dept_id not in Servicesbudgets_dict:
            Servicesbudgets_dict[dept_id] = {}

        Servicesbudgets_dict[dept_id][desig_id] = {
            'Serviceshead_count': Servicesbudget['Serviceshead_count'],
            'Servicesavg_salary': Servicesbudget['Servicesavg_salary'],
            'Servicesmultiplication_result': Servicesbudget['Servicesmultiplication_result'],
        }


        if dept_id not in departmentservices_dict:
            departmentservices_dict[dept_id] = {
                'TotalServicesmultiplication_result': 0,
                'TotalServiceshead_count': 0,
                'TotalServicessalary_headcount_contract': 0,
            }

        # departmentservices_dict[dept_id]['TotalServicesmultiplication_result'] += Servicesbudget['Servicesmultiplication_result']
        # departmentservices_dict[dept_id]['TotalServiceshead_count'] += Servicesbudget['Serviceshead_count']
        departmentservices_dict[dept_id]['TotalServicesmultiplication_result'] += (
            Servicesbudget['Servicesmultiplication_result'] or 0
        )

        # Safely add 'Serviceshead_count'
        departmentservices_dict[dept_id]['TotalServiceshead_count'] += (
            Servicesbudget['Serviceshead_count'] or 0
        )
        if departmentservices_dict[dept_id]['TotalServiceshead_count'] > 0:
            departmentservices_dict[dept_id]['TotalServicessalary_headcount_contract'] = (
                departmentservices_dict[dept_id]['TotalServicesmultiplication_result'] / departmentservices_dict[dept_id]['TotalServiceshead_count']
            )

        divisions_qs = ServicesDivisionMaster.objects.filter(
            servicesdepartmentmaster__DepartmentName=dept_id
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')

        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name and division_name not in divisionservices_dict:
            divisionservices_dict[division_name] = {
                'Servicedivisionmultiplication_result': 0,
                'Servicedivisiontotal_headcount': 0,
                'Servicedivisionsalary_headcount_product': 0,
            }

        if division_name:
            divisionservices_dict[division_name]['Servicedivisionmultiplication_result'] += departmentservices_dict[dept_id]['TotalServicesmultiplication_result']
            divisionservices_dict[division_name]['Servicedivisiontotal_headcount'] += departmentservices_dict[dept_id]['TotalServiceshead_count']

            if divisionservices_dict[division_name]['Servicedivisiontotal_headcount'] > 0:
                divisionservices_dict[division_name]['Servicedivisionsalary_headcount_product'] = (
                    divisionservices_dict[division_name]['Servicedivisionmultiplication_result'] / divisionservices_dict[division_name]['Servicedivisiontotal_headcount']
                )

    
    Servicesgranddivisionmultiplication_result = sum(
        dept['Servicedivisionmultiplication_result'] for dept in divisionservices_dict.values() if 'Servicedivisionmultiplication_result' in dept
    )

    ServicesContractgrand_total_headcount = sum(
        dept['Servicedivisiontotal_headcount'] for dept in divisionservices_dict.values() if 'Servicedivisiontotal_headcount' in dept
    )

    if ServicesContractgrand_total_headcount > 0:
        Servicesgrandsalarydivion = Servicesgranddivisionmultiplication_result / ServicesContractgrand_total_headcount
    else:
        Servicesgrandsalarydivion = 0

   

    meal_cost_record = BudgetMealCost.objects.filter(hotel_name=selected_organization_id).first()

    if meal_cost_record:
        meal_cost = meal_cost_record.cafeteriamealcost
    else:
        meal_cost = 0

    
# Employee Insurance Cost
    

    Insurance_cost_record = BudgetInsuranceCost.objects.filter(hotel_name=selected_organization_id).first()

    if Insurance_cost_record:
        Insurance_cost = Insurance_cost_record.EmployeeInsurancecost
    else:
        Insurance_cost = 0

    insuranceheadcount = grand_total_headcount  +  ServicesContractgrand_total_headcount 

    if insuranceheadcount > 0:
        Avgsalaryinsurancecoat = Insurance_cost / insuranceheadcount
    else:
        Avgsalaryinsurancecoat = 0
    
        
        
# benefites total 
    Benefitesheadtotal= grand_total_headcount + Contractgrand_total_headcount +  ServicesContractgrand_total_headcount 
    Benefitetotalctc = divisionmultiplication_result + grandContractdivisionmultiplication_result + Servicesgranddivisionmultiplication_result + meal_cost + Insurance_cost
    
    if Benefitesheadtotal > 0:
        Avgsalarytotalctc = Benefitetotalctc / Benefitesheadtotal
    else:
        Avgsalarytotalctc = 0
    
# meal avrg salary 
    if Benefitesheadtotal > 0:
        Avgsalarymealcoat = meal_cost / Benefitesheadtotal
    else:
        Avgsalarymealcoat = 0
    
  

    

    
    
    context = {
        'divisions': Divisiondatas if include_on_roll else None,
        'Contractdivisions': contractdivisions if include_contract else None,
        'current_datetime': datetime.now().strftime('%d %B %Y %H:%M:%S'),
        'UserID': UserID,
        'selected_organization_id': selected_organization_id,
        'selectedOrganizationName': selectedOrganizationName,
        'organization_logo': organization_logo,
        'organization_logos': organization_logos,
        'Servicedivisions': Servicedivisions if include_shared_services else None,
        'cafeteria_meal_cost': 'Data for Cafeteria Meal Cost' if include_cafeteria else None,
        'employees_insurance_cost': 'Data for Employees Insurance Cost' if include_insurance else None,
        'Contractbudgets_dict':Contractbudgets_dict,
        'Servicesbudgets_dict':Servicesbudgets_dict,

        'budgets_dict': budgets_dict,
        'department_totals': department_totals,
        'division_totals': division_totals,
        'divisionmultiplication_result':divisionmultiplication_result,
        'grand_total_headcount': grand_total_headcount,
        'grandsalarydivion':grandsalarydivion,
        'Contractdepartment_totals':Contractdepartment_totals,
        'Contractdivision_totals':Contractdivision_totals,
        'grandContractdivisionmultiplication_result':grandContractdivisionmultiplication_result,
        'Contractgrand_total_headcount':Contractgrand_total_headcount,
        'contractgrandsalarydivion':contractgrandsalarydivion,
        'departmentservices_dict':departmentservices_dict,
        'divisionservices_dict':divisionservices_dict,
        'Servicesgranddivisionmultiplication_result':Servicesgranddivisionmultiplication_result,
        'ServicesContractgrand_total_headcount':ServicesContractgrand_total_headcount,
        'Servicesgrandsalarydivion':Servicesgrandsalarydivion,
        'meal_cost':meal_cost,
        'Insurance_cost':Insurance_cost,
        'Benefitesheadtotal':Benefitesheadtotal,
        'Benefitetotalctc':Benefitetotalctc,
        'Avgsalarytotalctc':Avgsalarytotalctc,
        'Avgsalarymealcoat':Avgsalarymealcoat,
        'Avgsalaryinsurancecoat':Avgsalaryinsurancecoat
       
      
       
    }

    template = get_template(template_path)
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
    if pdf.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Budget.pdf"'
    
    return response





def indian_format(num):
    num_str = str(num).replace(',', '')  
    parts = num_str.split('.')
    integer_part = parts[0]
    decimal_part = parts[1] if len(parts) > 1 else '00'
    
   
    if len(integer_part) > 3:
        last_three = integer_part[-3:]
        other_digits = integer_part[:-3]
        formatted_integer = ','.join([other_digits[i:i+2] for i in range(0, len(other_digits), 2)]) + ',' + last_three
    else:
        formatted_integer = integer_part
    
    
    return f"{formatted_integer}.{decimal_part[:2]}"


import requests
from django.shortcuts import render, redirect
from django.db.models import Count, Sum, FloatField, ExpressionWrapper, Q
import logging

logger = logging.getLogger(__name__)


def VarianceReportView(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")

    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    if not OrganizationID or not UserID:
        logger.error("OrganizationID or UserID not found in session.")
        return redirect('MasterAttribute.Host')

    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    selectedOrganizationID = request.GET.get('hotel_name', OrganizationID)
    selected_division = request.GET.get('divisionname')
    selected_department = request.GET.get('departmentname')
    exclude_zero_headcount = request.GET.get('exclude_zero_headcount')  

    if UserType == 'CEO' and request.GET.get('hotel_name') is None:
        selectedOrganizationID = 401

    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False)
    departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)

    if selected_division and selected_division != 'All Division':
        Divisiondatas = Divisiondatas.filter(DivisionName=selected_division)
        departments = OnRollDepartmentMaster.objects.filter(
            OnRollDivisionMaster__DivisionName=selected_division, IsDelete=False
        )
    if selected_department and selected_department != 'All Department':
        departments = departments.filter(DepartmentName=selected_department)

    # contractdivisions = ContractDivisionMaster.objects.all().order_by('Order').prefetch_related(
    #     'contractdepartmentmaster_set__contractdesignationmaster_set'
    # )
    # Servicedivisions = ServicesDivisionMaster.objects.all().order_by('Order').prefetch_related(
    #     'servicesdepartmentmaster_set__servicesdesignationmaster_set'
    # )
    
    filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

       
    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
            Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
            Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
        )
    
    filtered_contract_departments = ContractDepartmentMaster.objects.filter(IsDelete=False)
    filtered_contract_designations = ContractDesignationMaster.objects.filter(IsDelete=False)

    
    filtered_service_departments = ServicesDepartmentMaster.objects.filter(IsDelete=False)
    filtered_service_designations = ServicesDesignationMaster.objects.filter(IsDelete=False)

    
    contractdivisions = ContractDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('contractdepartmentmaster_set', queryset=filtered_contract_departments),
        Prefetch('contractdepartmentmaster_set__contractdesignationmaster_set', queryset=filtered_contract_designations)
    )

    
    Servicedivisions = ServicesDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('servicesdepartmentmaster_set', queryset=filtered_service_departments),
        Prefetch('servicesdepartmentmaster_set__servicesdesignationmaster_set', queryset=filtered_service_designations)
    )
    
    employees_per_department_designation = EmployeeWorkDetails.objects.filter(OrganizationID=selectedOrganizationID,IsDelete=False,IsSecondary=False,EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"])
    
    if exclude_zero_headcount:  
        employees_per_department_designation = employees_per_department_designation.exclude(id=0)
    
    
    employees_per_department_designation = EmployeeWorkDetails.objects.all()

    if selectedOrganizationID:
        employees_per_department_designation = employees_per_department_designation.filter(OrganizationID=selectedOrganizationID,IsDelete=False,IsSecondary=False,EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"])
    

    employees_per_department_designation = (
        employees_per_department_designation
        .values('Department', 'Designation')
        .annotate(
            num_employees=Count('id'),
            total_salary=Sum('Salary'),
            avg_salary=ExpressionWrapper(Sum('Salary') / Count('id'), output_field=FloatField()),
            multiplication_result=F('avg_salary') * F('num_employees')
        )
        .order_by('Department', 'Designation')
    )

    # managebudget_department_designation = ManageBudgetOnRoll.objects.filter(
    #     hotel_name=selectedOrganizationID,
    # ).values(
    #     'on_roll_department_master__DepartmentName',
    #     'on_roll_designation_master__designations'
    # ).annotate(
    #     head_count=Sum('head_count'),
    #     total_salary=Sum('avg_salary'),
    #     aavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
    #     budgetmultiplication_result=F('aavg_salary') * F('head_count')
    # ).order_by(
    #     'on_roll_department_master__DepartmentName',
    #     'on_roll_designation_master__designations'
    # )

    managebudget_department_designation = ManageBudgetOnRoll.objects.annotate(
        clean_hotel_name=Trim('hotel_name')  
    ).filter(
        clean_hotel_name=selectedOrganizationID,  
        is_delete=False
    ).values(
        
        'on_roll_division_master__DivisionName',
       
        'on_roll_department_master__DepartmentName',
        
        'on_roll_designation_master__designations'
    ).annotate(
        head_count=F('head_count'),
        total_salary=Sum('avg_salary'),
        aavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        budgetmultiplication_result=ExpressionWrapper(F('aavg_salary') * F('head_count'), output_field=FloatField())
    ).order_by(
        'on_roll_division_master__DivisionName',
        'on_roll_department_master__DepartmentName',
        'on_roll_designation_master__designations'
    )
    departmentemp_totals = {}
    employees_dict = {}
    division_totals = {}

    for emp in employees_per_department_designation:
        dept = emp['Department']
        department_name = dept
        designation = emp['Designation'] 
        avg_salary = emp['avg_salary'] or 0
        num_employees = emp['num_employees'] or 0
        multiplication_result = avg_salary * num_employees  

        divisions_qs = OnRollDivisionMaster.objects.filter(
            onrolldepartmentmaster__DepartmentName=department_name
        ).annotate(
            department_name=F('onrolldepartmentmaster__DepartmentName')
        ).values(
            'DivisionName',  
        )

        logger.debug(f"Divisions queryset for department '{department_name}': {divisions_qs}")

        division_name = divisions_qs[0]['DivisionName'] if divisions_qs else None

        if dept not in departmentemp_totals:
            departmentemp_totals[dept] = {
                'total_salarymulti': 0,
                'total_headcount': 0,
                'salary_headcount_product': 0,
            }

        if division_name and division_name not in division_totals:
            division_totals[division_name] = {
                'divisiontotal_salarymulti': 0,
                'divisiontotal_headcount': 0,
                'divisionsalary_headcount_product': 0,
            }

        if dept not in employees_dict:
            employees_dict[dept] = {}

        employees_dict[dept][designation] = {
            'num_employees': num_employees,
            'avg_salary': avg_salary,
            'multiplication_result': multiplication_result  
        }

        departmentemp_totals[dept]['total_salarymulti'] += avg_salary
        departmentemp_totals[dept]['total_headcount'] += num_employees
        departmentemp_totals[dept]['salary_headcount_product'] = (
            departmentemp_totals[dept]['total_salarymulti'] / departmentemp_totals[dept]['total_headcount']
        )

        if division_name:
            division_totals[division_name]['divisiontotal_salarymulti'] += avg_salary
            division_totals[division_name]['divisiontotal_headcount'] += num_employees
            division_totals[division_name]['divisionsalary_headcount_product'] = (
                division_totals[division_name]['divisiontotal_salarymulti'] / division_totals[division_name]['divisiontotal_headcount']
            )


    budgets_dict = {}
    department_totals = {}
    divisiononroll_dict = {}

    for budget in managebudget_department_designation:
        dept_id = budget['on_roll_department_master__DepartmentName']
        desig_id = budget['on_roll_designation_master__designations']
        
        if dept_id not in budgets_dict:
            budgets_dict[dept_id] = {}
            
        budgets_dict[dept_id][desig_id] = {
            'head_count': budget['head_count'],
            'aavg_salary': budget['aavg_salary'],
            'budgetmultiplication_result': budget['budgetmultiplication_result'],
        }

        if dept_id not in department_totals:
            department_totals[dept_id] = {
                'aavg_salary': 0,
                'total_headcount': 0,
                'salary_headcount_product': 0,
            }

        department_totals[dept_id]['aavg_salary'] += budget.get('aavg_salary', 0) or 0
        department_totals[dept_id]['total_headcount'] += budget.get('head_count', 0) or 0
        
        # dpt_total_one = department_totals[dept_id]['aavg_salary'] 
        # dpt_total_two = budget.get('aavg_salary', 0) or 0
        
        # print("printing the dept totals")
        # print(f"{dpt_total_one+dpt_total_two} {dpt_total_one} + {dpt_total_two}")
        # dpt_total_one = department_totals[dept_id]['aavg_salary'] 
        # dpt_total_two = budget.get('aavg_salary', 0) or 0
        # total_dept = dpt_total_one+dpt_total_two
        
        # print("printing the dept totals")
        # print(f"total_dept: {total_dept}")

        if department_totals[dept_id]['total_headcount'] > 0:
            department_totals[dept_id]['salary_headcount_product'] = (
                department_totals[dept_id]['aavg_salary'] / department_totals[dept_id]['total_headcount']
            )

        divisions_qs = OnRollDivisionMaster.objects.filter(
            onrolldepartmentmaster__DepartmentName=dept_id
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')

        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name and division_name not in divisiononroll_dict:
            divisiononroll_dict[division_name] = {
                'onrollonmultiplication_result': 0,
                'onrolldivisiontotal_headcount': 0,
                'onrolldivisionsalary_headcount_product': 0,
            }

        if division_name:
            # Use `budget` values instead of `department_totals`
            divisiononroll_dict[division_name]['onrollonmultiplication_result'] += budget.get('aavg_salary', 0) or 0
            divisiononroll_dict[division_name]['onrolldivisiontotal_headcount'] += budget.get('head_count', 0) or 0


            if divisiononroll_dict[division_name]['onrolldivisiontotal_headcount'] > 0:
                divisiononroll_dict[division_name]['onrolldivisionsalary_headcount_product'] = (
                    divisiononroll_dict[division_name]['onrollonmultiplication_result'] / divisiononroll_dict[division_name]['onrolldivisiontotal_headcount']
                )

    grandtotalondataemp = sum(
        dept['divisiontotal_salarymulti'] for dept in division_totals.values() if 'divisiontotal_salarymulti' in dept
    )
    grandtotalondataemp_headcount = sum(
        dept['divisiontotal_headcount'] for dept in division_totals.values() if 'divisiontotal_headcount' in dept
    )

    if grandtotalondataemp_headcount > 0:
        Servicesgrandsalarydivion = grandtotalondataemp * grandtotalondataemp_headcount
    else:
        Servicesgrandsalarydivion = 0

    # Calculate budget totals
    grandtotalondatabudget = sum(
        dept['onrollonmultiplication_result'] for dept in divisiononroll_dict.values() if 'onrollonmultiplication_result' in dept
    )
    headgrandtotalondatabudget = sum(
        dept['onrolldivisiontotal_headcount'] for dept in divisiononroll_dict.values() if 'onrolldivisiontotal_headcount' in dept
    )

    if headgrandtotalondatabudget > 0:
        orrollServicesgrandsalarydivion = grandtotalondatabudget * headgrandtotalondatabudget
    else:
        orrollServicesgrandsalarydivion = 0

    # Calculate variances
    variance_detaavg_salary = grandtotalondataemp - grandtotalondatabudget
    variance_detaheadcount = grandtotalondataemp_headcount - headgrandtotalondatabudget
    variance_detatotal_ctc = Servicesgrandsalarydivion - orrollServicesgrandsalarydivion
    
  

    variance_dict = {}
    for dept, designations in employees_dict.items():
        if dept not in variance_dict:
            variance_dict[dept] = {}
        for desig, emp_data in designations.items():
            head_count = budgets_dict.get(dept, {}).get(desig, {}).get('head_count', 0)
            aavg_salary = budgets_dict.get(dept, {}).get(desig, {}).get('aavg_salary', 0)
            budget_multiplication_result = budgets_dict.get(dept, {}).get(desig, {}).get('budgetmultiplication_result', 0)

            emp_num_employees = emp_data.get('num_employees', 0)
            emp_avg_salary = emp_data.get('avg_salary', 0)
            emp_multiplication_result = emp_data.get('multiplication_result', 0)

            variance_head_count = (emp_num_employees or 0) - (head_count or 0)
            variance_salary = (emp_avg_salary or 0) - (aavg_salary or 0)
            variance_total_result = (emp_multiplication_result or 0) - (budget_multiplication_result or 0)
            
            # print(f"desig : {desig}")
            # print(f"BUD AVG SAL : {aavg_salary}")
            # print(f"ACT AVG SAL : {emp_avg_salary}")
            # print(f"variance_salary : {variance_salary}")

            # variance_head_count = (head_count or 0) - (emp_num_employees or 0)
            # variance_salary = (aavg_salary or 0) - (emp_avg_salary or 0)
            # variance_total_result = (budget_multiplication_result or 0) - (emp_multiplication_result or 0)

            # variance_head_count = head_count - emp_num_employees
            # variance_salary = aavg_salary - emp_avg_salary
            # variance_total_result = budget_multiplication_result - emp_multiplication_result

            # Remarks --> 	BUD AVG SAL as aavg_salary
            # Remarks --> 	ACT AVG SAL as emp_avg_salary
            # Remarks --> 	VAR AVG SAL as variance_salary
            
            # budget_val = budgets_dict.get(dept, {}).get(desig, {})
            # bud_avg_salary_Val = budget_val.get('aavg_salary', 0) or 0
            # emp_avg_salary_Val = emp_data.get('avg_salary', 0) or 0
            
            # print("--------------------(variance_salary_new)------------------------------")
            # print(f"BUD AVG SAL: {bud_avg_salary_Val}")
            # print(f"emp_avg_salary_Val: {emp_avg_salary_Val}")
            # print(f"variance_salary: {variance_salary} = aavg_salary:{aavg_salary} <--> emp_avg_salary:{emp_avg_salary}")
            # print(f"{variance_salary} = {aavg_salary} - {emp_avg_salary}")
            # print("---------------------(End variance_salary)-----------------------------")


            variance_dict[dept][desig] = {
                'variance_head_count': variance_head_count,
                'variance_salary': variance_salary,
                'variance_total_result': variance_total_result,
                'num_employees': emp_num_employees,
                'avg_salary': emp_avg_salary,
                'head_count': head_count,
                'aavg_salary': aavg_salary,
                'multiplication_result': emp_multiplication_result,
                'budgetmultiplication_result': budget_multiplication_result
            }
    for dept, designations in budgets_dict.items():
        if dept not in variance_dict:
            variance_dict[dept] = {}
    
        for desig, bud_data in designations.items():
            if desig not in variance_dict[dept]:
                head_count = bud_data.get('head_count', 0)
                aavg_salary = bud_data.get('aavg_salary', 0)
                budget_multiplication_result = bud_data.get('budgetmultiplication_result', 0)
    
                # Employee values = 0
                variance_dict[dept][desig] = {
                    'variance_head_count': 0 - head_count,
                    'variance_salary': 0 - aavg_salary,
                    'variance_total_result': 0 - budget_multiplication_result,
                    'num_employees': 0,
                    'avg_salary': 0,
                    'head_count': head_count,
                    'aavg_salary': aavg_salary,
                    'multiplication_result': 0,
                    'budgetmultiplication_result': budget_multiplication_result
                }
    department_variance_dict = {}
    for dept, emp_data in departmentemp_totals.items():
        # Get budget data for comparison
        budget_data = department_totals.get(dept, {})
        budget_aavg_salary = budget_data.get('aavg_salary', 0)
        budget_total_headcount = budget_data.get('total_headcount', 0)
        budget_salary_headcount_product = budget_data.get('salary_headcount_product', 0)

        # Get actual data
        actual_salary_multi = emp_data['total_salarymulti']
        actual_headcount = emp_data['total_headcount']
        actual_salary_headcount_product = emp_data['salary_headcount_product']

        # Calculate variance
        variance_salary_multi = actual_salary_multi - budget_aavg_salary
        variance_headcount = actual_headcount - budget_total_headcount
        variance_salary_headcount_product = actual_salary_headcount_product - budget_salary_headcount_product

        department_variance_dict[dept] = {
            'actual_salary_multi': actual_salary_multi,
            'actual_headcount': actual_headcount,
            'actual_salary_headcount_product': actual_salary_headcount_product,
            'budget_aavg_salary': budget_aavg_salary,
            'budget_total_headcount': budget_total_headcount,
            'budget_salary_headcount_product': budget_salary_headcount_product,
            'variance_salary_multi': variance_salary_multi,
            'variance_headcount': variance_headcount,
            'variance_salary_headcount_product': variance_salary_headcount_product
        }

# Calculate variance for divisions
    division_variance_dict = {}
    for division, data in divisiononroll_dict.items():
        # Get budget data for comparison
        budget_data = division_totals.get(division, {})
        budget_division_total_salary_multi = budget_data.get('divisiontotal_salarymulti', 0)
        budget_division_total_headcount = budget_data.get('divisiontotal_headcount', 0)
        budget_division_salary_headcount_product = budget_data.get('divisionsalary_headcount_product', 0)

        # Get actual data
        actual_salary_multi = data['onrollonmultiplication_result']
        actual_headcount = data['onrolldivisiontotal_headcount']
        actual_salary_headcount_product = data['onrolldivisionsalary_headcount_product']

        # Calculate variance
        variance_salary_multi =  budget_division_total_salary_multi - actual_salary_multi
        variance_headcount =  budget_division_total_headcount-actual_headcount
        variance_salary_headcount_product =  budget_division_salary_headcount_product-actual_salary_headcount_product
      
        division_variance_dict[division] = {
            'actual_salary_multi': actual_salary_multi,
            'actual_headcount': actual_headcount,
            'actual_salary_headcount_product': actual_salary_headcount_product,
            
            'budget_division_total_salary_multi': budget_division_total_salary_multi,
            'budget_division_total_headcount': budget_division_total_headcount,
            'budget_division_salary_headcount_product': budget_division_salary_headcount_product,
            
            'variance_salary_multi': variance_salary_multi,
            'variance_headcount': variance_headcount,
            'variance_salary_headcount_product': variance_salary_headcount_product
        }        
        
        # print("actual_salary_headcount_product:", actual_salary_headcount_product)
        # print("budget_division_salary_headcount_product:", budget_division_salary_headcount_product)
        # print("variance_salary_headcount_product:", variance_salary_headcount_product)
    
    # Retrieve and aggregate data from EntryActualContract

    actual_contract_data = EntryActualContract.objects.filter(
        hotel_name=selectedOrganizationID
    ).values(
        'contract_department_master__DepartmentName',
        'contract_designation_master__designations'
    ).annotate(
        actual_head_count=Sum('head_count'),
        actual_avg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        actual_total_ctc=F('actual_avg_salary') * F('actual_head_count')
    ).order_by(
        'contract_department_master__DepartmentName',
        'contract_designation_master__designations'
    )

    # Fetch and process budget contract data
    budget_contract_data = ManageBudgetContract.objects.filter(
        hotel_name=selectedOrganizationID
    ).values(
        'contract_department_master__DepartmentName',
        'contract_designation_master__designations'
    ).annotate(
        budget_head_count=Sum('head_count'),
        budget_avg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        budget_total_ctc=F('budget_avg_salary') * F('budget_head_count')
    ).order_by(
        'contract_department_master__DepartmentName',
        'contract_designation_master__designations'
    )

    # Initialize dictionaries
    actual_dict = {}
    Contractdepartment_totals = {}
    Contractdivision_totals = {}

    # Process actual contract data
    for item in actual_contract_data:
        dept = item['contract_department_master__DepartmentName']
        designation = item['contract_designation_master__designations']
        
        if dept not in actual_dict:
            actual_dict[dept] = {}
        actual_dict[dept][designation] = {
            'actual_head_count': item['actual_head_count'],
            'actual_avg_salary': item['actual_avg_salary'],
            'actual_total_ctc': item['actual_total_ctc']
        }
        
        if dept not in Contractdepartment_totals:
            Contractdepartment_totals[dept] = {
                'Contractmultiplication_result': 0,
                'Contracthead_count': 0,
                'salary_headcount_contract': 0,
            }

        # Update totals
        Contractdepartment_totals[dept]['Contractmultiplication_result'] += item['actual_avg_salary']
        Contractdepartment_totals[dept]['Contracthead_count'] += item['actual_head_count']

        if Contractdepartment_totals[dept]['Contracthead_count'] > 0:
            Contractdepartment_totals[dept]['salary_headcount_contract'] = (
                Contractdepartment_totals[dept]['Contractmultiplication_result'] * Contractdepartment_totals[dept]['Contracthead_count']
            )

        # Fetch and process division data
        divisions_qs = ContractDivisionMaster.objects.filter(
            contractdepartmentmaster__DepartmentName=dept
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')

        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name and division_name not in Contractdivision_totals:
            Contractdivision_totals[division_name] = {
                'Contractdivisionmultiplication_result': 0,
                'Contractdivisiontotal_headcount': 0,
                'Contractdivisionsalary_headcount_product': 0,
            }

        if division_name:
            Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] += item['actual_avg_salary']
            Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] += item['actual_head_count']

            if Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] > 0:
                Contractdivision_totals[division_name]['Contractdivisionsalary_headcount_product'] = (
                    Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] * Contractdivision_totals[division_name]['Contractdivisiontotal_headcount']
                )

    # Initialize budget-related dictionaries
    budget_dict = {}
    onrollContractdepartment_totals = {}
    onrollContractdivision_totals = {}

    # Process budget contract data
    for itembudget in budget_contract_data:
        dept = itembudget['contract_department_master__DepartmentName']
        designation = itembudget['contract_designation_master__designations']
        
        if dept not in budget_dict:
            budget_dict[dept] = {}
        budget_dict[dept][designation] = {
            'budget_head_count': itembudget['budget_head_count'],
            'budget_avg_salary': itembudget['budget_avg_salary'],
            'budget_total_ctc': itembudget['budget_total_ctc']
        }
        
        if dept not in onrollContractdepartment_totals:
            onrollContractdepartment_totals[dept] = {
                'Contractmultiplication_result': 0,
                'Contracthead_count': 0,
                'salary_headcount_contract': 0,
            }

        # Update totals
        onrollContractdepartment_totals[dept]['Contractmultiplication_result'] += (itembudget.get('budget_avg_salary', 0) or 0)
        onrollContractdepartment_totals[dept]['Contracthead_count'] += (itembudget.get('budget_head_count', 0) or 0)

        
        if onrollContractdepartment_totals[dept]['Contracthead_count'] > 0:
            onrollContractdepartment_totals[dept]['salary_headcount_contract'] = (
                onrollContractdepartment_totals[dept]['Contractmultiplication_result'] * onrollContractdepartment_totals[dept]['Contracthead_count']
            )

        # Fetch and process division data
        divisions_qs = ContractDivisionMaster.objects.filter(
            contractdepartmentmaster__DepartmentName=dept
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')

        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name and division_name not in onrollContractdivision_totals:
            onrollContractdivision_totals[division_name] = {
                'Contractdivisionmultiplication_result': 0,
                'Contractdivisiontotal_headcount': 0,
                'Contractdivisionsalary_headcount_product': 0,
            }

        if division_name:
            onrollContractdivision_totals[division_name]['Contractdivisionmultiplication_result'] += (itembudget['budget_avg_salary'] or 0)
            onrollContractdivision_totals[division_name]['Contractdivisiontotal_headcount'] += (itembudget['budget_head_count'] or 0)


            if onrollContractdivision_totals[division_name]['Contractdivisiontotal_headcount'] > 0:
                onrollContractdivision_totals[division_name]['Contractdivisionsalary_headcount_product'] = (
                    onrollContractdivision_totals[division_name]['Contractdivisionmultiplication_result'] * onrollContractdivision_totals[division_name]['Contractdivisiontotal_headcount']
      
                )

 # Calculate contract   
    enterycontractdetasgrand = sum(
        dept['Contractdivisionmultiplication_result'] for dept in Contractdivision_totals.values() if 'Contractdivisionmultiplication_result' in dept
    )
    enterycontractdetasheadgrandtotalon = sum(
        dept['Contractdivisiontotal_headcount'] for dept in Contractdivision_totals.values() if 'Contractdivisiontotal_headcount' in dept
    )

    if enterycontractdetasheadgrandtotalon > 0:
        enterycontractempgrandsalarydivion = enterycontractdetasgrand * enterycontractdetasheadgrandtotalon
    else:
        enterycontractempgrandsalarydivion = 0

   

 # Calculate budget contract
    budgetcontractgrandtotalondataemp = sum(
        dept['Contractdivisionmultiplication_result'] for dept in onrollContractdivision_totals.values() if 'Contractdivisionmultiplication_result' in dept
    )
    budgetcontractgrandtotalondataemp_headcount = sum(
        dept['Contractdivisiontotal_headcount'] for dept in onrollContractdivision_totals.values() if 'Contractdivisiontotal_headcount' in dept
    )

    if grandtotalondataemp_headcount > 0:
        budgetcontractdatagrandsalarydivion = budgetcontractgrandtotalondataemp * budgetcontractgrandtotalondataemp_headcount
    else:
        budgetcontractdatagrandsalarydivion = 0
    
    
    datavariance_detaavg_salary = enterycontractdetasgrand- budgetcontractgrandtotalondataemp  
    datavariance_detaheadcount = enterycontractdetasheadgrandtotalon - budgetcontractgrandtotalondataemp_headcount 
    datavariance_detatotal_ctc = enterycontractempgrandsalarydivion - budgetcontractdatagrandsalarydivion
    
    
    # # Calculate variances for contracts
    variance_contract_dict = {}
    for dept, designations in actual_dict.items():
        if dept not in variance_contract_dict:
            variance_contract_dict[dept] = {}
        for desig, actual_data in designations.items():
            budget_data = budget_dict.get(dept, {}).get(desig, {})

            actual_head_count = actual_data.get('actual_head_count') or 0
            actual_avg_salary = actual_data.get('actual_avg_salary') or 0
            actual_total_ctc = actual_data.get('actual_total_ctc') or 0

            budget_head_count = budget_data.get('budget_head_count') or 0
            budget_avg_salary = budget_data.get('budget_avg_salary') or 0
            budget_total_ctc = budget_data.get('budget_total_ctc') or 0

            variance_head_count = actual_head_count - budget_head_count
            variance_avg_salary = actual_avg_salary - budget_avg_salary
            variance_total_ctc = actual_total_ctc - budget_total_ctc

            variance_contract_dict[dept][desig] = {
                'variance_head_count': variance_head_count,
                'variance_avg_salary': variance_avg_salary,
                'variance_total_ctc': variance_total_ctc,
                'actual_head_count': actual_head_count,
                'actual_avg_salary': actual_avg_salary,
                'actual_total_ctc': actual_total_ctc,
                'budget_head_count': budget_head_count,
                'budget_avg_salary': budget_avg_salary,
                'budget_total_ctc': budget_total_ctc
            }

    # Calculate variances for department totals
    onrolldepartment_variance_dict = {}
    for dept, totals in onrollContractdepartment_totals.items():
        actual_totals = Contractdepartment_totals.get(dept, {})
        
        actual_multiplication_result = actual_totals.get('Contractmultiplication_result', 0)
        actual_head_count = actual_totals.get('Contracthead_count', 0)
        actual_salary_headcount_contract = actual_totals.get('salary_headcount_contract', 0)
        
        budget_multiplication_result = totals.get('Contractmultiplication_result', 0)
        budget_head_count = totals.get('Contracthead_count', 0)
        budget_salary_headcount_contract = totals.get('salary_headcount_contract', 0)

        variance_multiplication_result = actual_multiplication_result - budget_multiplication_result
        variance_head_count = actual_head_count - budget_head_count
        variance_salary_headcount_contract = actual_salary_headcount_contract - budget_salary_headcount_contract

        onrolldepartment_variance_dict[dept] = {
            'variance_multiplication_result': variance_multiplication_result,
            'variance_head_count': variance_head_count,
            'variance_salary_headcount_contract': variance_salary_headcount_contract,
            'actual_head_count': actual_head_count,
            'actual_multiplication_result': actual_multiplication_result,
            'actual_salary_headcount_contract': actual_salary_headcount_contract,
            'budget_head_count': budget_head_count,
            'budget_multiplication_result': budget_multiplication_result,
            'budget_salary_headcount_contract': budget_salary_headcount_contract
        }

    # Calculate variances for division totals
    onrolldivision_variance_dict = {}
    for division, totals in onrollContractdivision_totals.items():
        actual_totals = Contractdivision_totals.get(division, {})
        
        actual_multiplication_result = actual_totals.get('Contractdivisionmultiplication_result', 0)
        actual_head_count = actual_totals.get('Contractdivisiontotal_headcount', 0)
        actual_salary_headcount_product = actual_totals.get('Contractdivisionsalary_headcount_product', 0)
        
        budget_multiplication_result = totals.get('Contractdivisionmultiplication_result', 0)
        budget_head_count = totals.get('Contractdivisiontotal_headcount', 0)
        budget_salary_headcount_product = totals.get('Contractdivisionsalary_headcount_product', 0)

        variance_multiplication_result = actual_multiplication_result - budget_multiplication_result
        variance_head_count = actual_head_count - budget_head_count
        variance_salary_headcount_product = actual_salary_headcount_product - budget_salary_headcount_product

        onrolldivision_variance_dict[division] = {
            'variance_multiplication_result': variance_multiplication_result,
            'variance_head_count': variance_head_count,
            'variance_salary_headcount_product': variance_salary_headcount_product,
            'actual_head_count': actual_head_count,
            'actual_multiplication_result': actual_multiplication_result,
            'actual_salary_headcount_product': actual_salary_headcount_product,
            'budget_head_count': budget_head_count,
            'budget_multiplication_result': budget_multiplication_result,
            'budget_salary_headcount_product': budget_salary_headcount_product
        }
    
    Insurance_cost_record = BudgetInsuranceCost.objects.filter(hotel_name=selectedOrganizationID).first()

    if Insurance_cost_record:
        Insurance_cost = Insurance_cost_record.EmployeeInsurancecost
    else:
        Insurance_cost = 0 

    entryInsurance_cost_record = EntryActualInsuranceCost.objects.filter(hotel_name=selectedOrganizationID).first()

    if entryInsurance_cost_record:
        EntryInsurance_cost = entryInsurance_cost_record.EmployeeInsurancecost
    else:
        EntryInsurance_cost = 0       
    
    EntryInsurance_cost = EntryInsurance_cost or 0
    Insurance_cost = Insurance_cost or 0
    varinceinsurancecoast = EntryInsurance_cost - Insurance_cost

    mealcost = BudgetMealCost.objects.filter(hotel_name=selectedOrganizationID).first()

    if mealcost:
        budgetmeal = mealcost.cafeteriamealcost
    else:
        budgetmeal = 0 

    entrymealcost_record = EntryActualMealCost.objects.filter(hotel_name=selectedOrganizationID).first()

    if entrymealcost_record:
        Entrymealcost = entrymealcost_record.cafeteriamealcost
    else:
        Entrymealcost = 0       

    varicanmealcoast = (Entrymealcost or 0) - (budgetmeal or 0)
    
   
    actual_shared_services_data = EntryActualSharedServices.objects.filter(
        hotel_name=selectedOrganizationID
    ).values(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    ).annotate(
        actualservice_head_count=Sum('head_count'),
        actualservice_avg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        actualservice_total_ctc=F('actualservice_avg_salary') * F('actualservice_head_count')
    ).order_by(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    )

    # Query budget shared services data
    budget_shared_services_data = ManageBudgetSharedServices.objects.filter(
        hotel_name=selectedOrganizationID
    ).values(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    ).annotate(
        budgetservice_head_count=Sum('head_count'),
        budgetservice_avg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        budgetservice_total_ctc=F('budgetservice_avg_salary') * F('budgetservice_head_count')
    ).order_by(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    )

       
    actualservice_dict = {}
    departmentservices_dict = {}
    divisionservices_dict = {}

    for item in actual_shared_services_data:
        dept = item['services_department_master__DepartmentName']
        designation = item['services_designation_master__designations']
        
        
        if dept not in actualservice_dict:
            actualservice_dict[dept] = {}
        actualservice_dict[dept][designation] = {
            'actualservice_head_count': item['actualservice_head_count'],
            'actualservice_avg_salary': item['actualservice_avg_salary'],
            'actualservice_total_ctc': item['actualservice_total_ctc']
        }
        
        
        if dept not in departmentservices_dict:
            departmentservices_dict[dept] = {
                'TotalServicesmultiplication_result': 0,
                'TotalServiceshead_count': 0,
                'TotalServicessalary_headcount_contract': 0,
            }

        departmentservices_dict[dept]['TotalServicesmultiplication_result'] += (item.get('actualservice_avg_salary', 0) or 0)
        departmentservices_dict[dept]['TotalServiceshead_count'] += (item.get('actualservice_head_count', 0) or 0)

        
        
        if departmentservices_dict[dept]['TotalServiceshead_count'] > 0:
            departmentservices_dict[dept]['TotalServicessalary_headcount_contract'] = (
                departmentservices_dict[dept]['TotalServicesmultiplication_result'] * departmentservices_dict[dept]['TotalServiceshead_count']
            )
        
       
        divisions_qs = ServicesDivisionMaster.objects.filter(
            servicesdepartmentmaster__DepartmentName=dept
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')
        
        division_name = divisions_qs[0]['division_name'] if divisions_qs.exists() else None

        
        if division_name:
            if division_name not in divisionservices_dict:
                divisionservices_dict[division_name] = {
                    'Servicedivisionmultiplication_result': 0,
                    'Servicedivisiontotal_headcount': 0,
                    'Servicedivisionsalary_headcount_product': 0,
                }

            divisionservices_dict[division_name]['Servicedivisionmultiplication_result'] += (
                departmentservices_dict[dept]['TotalServicesmultiplication_result']
            )
            divisionservices_dict[division_name]['Servicedivisiontotal_headcount'] += (
                departmentservices_dict[dept]['TotalServiceshead_count']
            )
            
           
            if divisionservices_dict[division_name]['Servicedivisiontotal_headcount'] > 0:
                divisionservices_dict[division_name]['Servicedivisionsalary_headcount_product'] = (
                    divisionservices_dict[division_name]['Servicedivisionmultiplication_result'] * divisionservices_dict[division_name]['Servicedivisiontotal_headcount']
                )

           
    budgetservice_dict = {}
    totaldepartmentservices_dict = {}
    totaldivisionservices_dict = {}

    
    for itembudget in budget_shared_services_data:
        dept = itembudget['services_department_master__DepartmentName']
        designation = itembudget['services_designation_master__designations']
        
       
        if dept not in budgetservice_dict:
            budgetservice_dict[dept] = {}
        budgetservice_dict[dept][designation] = {
            'budgetservice_head_count': itembudget['budgetservice_head_count'],
            'budgetservice_avg_salary': itembudget['budgetservice_avg_salary'],
            'budgetservice_total_ctc': itembudget['budgetservice_total_ctc']
        }
        
        
        if dept not in totaldepartmentservices_dict:
            totaldepartmentservices_dict[dept] = {
                'TotalServicesmultiplication_result': 0,
                'TotalServiceshead_count': 0,
                'TotalServicessalary_headcount_contract': 0,
            }

       
        totaldepartmentservices_dict[dept]['TotalServicesmultiplication_result'] += (itembudget.get('budgetservice_avg_salary', 0) or 0)
        totaldepartmentservices_dict[dept]['TotalServiceshead_count'] += (itembudget.get('budgetservice_head_count', 0) or 0)

        
        
        if totaldepartmentservices_dict[dept]['TotalServiceshead_count'] > 0:
            totaldepartmentservices_dict[dept]['TotalServicessalary_headcount_contract'] = (
                totaldepartmentservices_dict[dept]['TotalServicesmultiplication_result'] * totaldepartmentservices_dict[dept]['TotalServiceshead_count']
            )
        
       
        divisions_qs = ServicesDivisionMaster.objects.filter(
            servicesdepartmentmaster__DepartmentName=dept
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')
        
        division_name = divisions_qs[0]['division_name'] if divisions_qs.exists() else None

        
        if division_name and division_name not in totaldivisionservices_dict:
            totaldivisionservices_dict[division_name] = {
                'Servicedivisionmultiplication_result': 0,
                'Servicedivisiontotal_headcount': 0,
                'Servicedivisionsalary_headcount_product': 0,
            }

        if division_name:
            totaldivisionservices_dict[division_name]['Servicedivisionmultiplication_result'] += (
                totaldepartmentservices_dict[dept]['TotalServicesmultiplication_result']
            )
            totaldivisionservices_dict[division_name]['Servicedivisiontotal_headcount'] += (
                totaldepartmentservices_dict[dept]['TotalServiceshead_count']
            )
            
            
            if totaldivisionservices_dict[division_name]['Servicedivisiontotal_headcount'] > 0:
                totaldivisionservices_dict[division_name]['Servicedivisionsalary_headcount_product'] = (
                    totaldivisionservices_dict[division_name]['Servicedivisionmultiplication_result'] * totaldivisionservices_dict[division_name]['Servicedivisiontotal_headcount']
                )

    # Calculate contract   
    enteryservicedetasgrand = sum(
        dept['Servicedivisionmultiplication_result'] for dept in divisionservices_dict.values() if 'Servicedivisionmultiplication_result' in dept
    )
    enteryservicedetasheadgrandtotalon = sum(
        dept['Servicedivisiontotal_headcount'] for dept in divisionservices_dict.values() if 'Servicedivisiontotal_headcount' in dept
    )

    if enteryservicedetasheadgrandtotalon > 0:
        enteryserviceempgrandsalarydivion = enteryservicedetasgrand * enteryservicedetasheadgrandtotalon
    else:
        enteryserviceempgrandsalarydivion = 0
    
    

 # Calculate budget contract
    budgetservicegrandtotalondataemp = sum(
        dept['Servicedivisionmultiplication_result'] for dept in totaldivisionservices_dict.values() if 'Servicedivisionmultiplication_result' in dept
    )
    budgetservicegrandtotalondataemp_headcount = sum(
        dept['Servicedivisiontotal_headcount'] for dept in totaldivisionservices_dict.values() if 'Servicedivisiontotal_headcount' in dept
    )

    if grandtotalondataemp_headcount > 0:
        budgetservicedatagrandsalarydivion = budgetservicegrandtotalondataemp * budgetservicegrandtotalondataemp_headcount
    else:
        budgetservicedatagrandsalarydivion = 0
    
   

    servicedatavariance_detaavg_salary = enteryservicedetasgrand- budgetservicegrandtotalondataemp  
    servicedatavariance_detaheadcount = enteryservicedetasheadgrandtotalon - budgetservicegrandtotalondataemp_headcount 
    servicedatavariance_detatotal_ctc = enteryserviceempgrandsalarydivion - budgetservicedatagrandsalarydivion
    
   
    variance_shared_services_dict = {}
    for dept, designations in actualservice_dict.items():
        if dept not in variance_shared_services_dict:
            variance_shared_services_dict[dept] = {}
        for desig, actual_data in designations.items():
            budget_data = budgetservice_dict.get(dept, {}).get(desig, {})

            actualservice_head_count = actual_data.get('actualservice_head_count', 0)
            actualservice_avg_salary = actual_data.get('actualservice_avg_salary', 0)
            actualservice_total_ctc = actual_data.get('actualservice_total_ctc', 0)

            budgetservice_head_count = budget_data.get('budgetservice_head_count', 0)
            budgetservice_avg_salary = budget_data.get('budgetservice_avg_salary', 0)
            budgetservice_total_ctc = budget_data.get('budgetservice_total_ctc', 0)

            variance_head_count = (actualservice_head_count or 0) - (budgetservice_head_count or 0)
            variance_avg_salary = (actualservice_avg_salary or 0) - (budgetservice_avg_salary or 0)
            variance_total_ctc = (actualservice_total_ctc or 0) - (budgetservice_total_ctc or 0)


            variance_shared_services_dict[dept][desig] = {
                'variance_head_count': variance_head_count,
                'variance_avg_salary': variance_avg_salary,
                'variance_total_ctc': variance_total_ctc,
                'actual_head_count': actualservice_head_count,
                'actual_avg_salary': actualservice_avg_salary,
                'actual_total_ctc': actualservice_total_ctc,
                'budget_head_count': budgetservice_head_count,
                'budget_avg_salary': budgetservice_avg_salary,
                'budget_total_ctc': budgetservice_total_ctc,
            }

    
    onrolldepartment_variance_dictss = {}
    for dept, totals in totaldepartmentservices_dict.items():
        actual_totals = departmentservices_dict.get(dept, {})
        
        actual_multiplication_result = actual_totals.get('TotalServicesmultiplication_result', 0)
        actual_head_count = actual_totals.get('TotalServiceshead_count', 0)
        actual_salary_headcount_contract = actual_totals.get('TotalServicessalary_headcount_contract', 0)
        
        budget_multiplication_result = totals.get('TotalServicesmultiplication_result', 0)
        budget_head_count = totals.get('TotalServiceshead_count', 0)
        budget_salary_headcount_contract = totals.get('TotalServicessalary_headcount_contract', 0)

        variance_multiplication_result = actual_multiplication_result - budget_multiplication_result
        variance_head_count = actual_head_count - budget_head_count
        variance_salary_headcount_contract = actual_salary_headcount_contract - budget_salary_headcount_contract

        onrolldepartment_variance_dictss[dept] = {
            'variance_multiplication_result': variance_multiplication_result,
            'variance_head_count': variance_head_count,
            'variance_salary_headcount_contract': variance_salary_headcount_contract,
            'actual_head_count': actual_head_count,
            'actual_multiplication_result': actual_multiplication_result,
            'actual_salary_headcount_contract': actual_salary_headcount_contract,
            'budget_head_count': budget_head_count,
            'budget_multiplication_result': budget_multiplication_result,
            'budget_salary_headcount_contract': budget_salary_headcount_contract,
        }

    

   
    onrolldivision_variance_dictss = {}
    for div, totals in totaldivisionservices_dict.items():
        actual_totals = divisionservices_dict.get(div, {})
        
        actual_multiplication_result = actual_totals.get('Servicedivisionmultiplication_result', 0)
        actual_head_count = actual_totals.get('Servicedivisiontotal_headcount', 0)
        actual_salary_headcount_product = actual_totals.get('Servicedivisionsalary_headcount_product', 0)
        
        budget_multiplication_result = totals.get('Servicedivisionmultiplication_result', 0)
        budget_head_count = totals.get('Servicedivisiontotal_headcount', 0)
        budget_salary_headcount_product = totals.get('Servicedivisionsalary_headcount_product', 0)

        variance_multiplication_result = actual_multiplication_result - budget_multiplication_result
        variance_head_count = actual_head_count - budget_head_count
        variance_salary_headcount_product = actual_salary_headcount_product - budget_salary_headcount_product

        onrolldivision_variance_dictss[div] = {
            'variance_multiplication_result': variance_multiplication_result,
            'variance_head_count': variance_head_count,
            'variance_salary_headcount_product': variance_salary_headcount_product,
            'actual_head_count': actual_head_count,
            'actual_multiplication_result': actual_multiplication_result,
            'actual_salary_headcount_product': actual_salary_headcount_product,
            'budget_head_count': budget_head_count,
            'budget_multiplication_result': budget_multiplication_result,
            'budget_salary_headcount_product': budget_salary_headcount_product,
        }


    context = {
        'divisions': Divisiondatas,
        'memOrg': memOrg,
        'exclude_zero_headcount':exclude_zero_headcount,
        'selectedOrganizationID': selectedOrganizationID,
        'selected_division': selected_division,
        'selected_department': selected_department,
        'Departmentsdatas': departments,
        'contractdivisions': contractdivisions,
        'Servicedivisions': Servicedivisions,
        'variance_dict': variance_dict,
        'variance_contract_dict': variance_contract_dict,
        'employees_dict':employees_dict,
        'budgets_dict':budgets_dict,
        'actual_dict':actual_dict,
        'budget_dict':budget_dict,
        'variance_contract_dict':variance_contract_dict,
        'Insurance_cost':Insurance_cost,
        'EntryInsurance_cost':EntryInsurance_cost,
        'budgetmeal':budgetmeal,
        'Entrymealcost':Entrymealcost,
        'actualservice_dict':actualservice_dict,
        'budgetservice_dict':budgetservice_dict,
        'variance_shared_services_dict':variance_shared_services_dict,
        'Divisiondatas':Divisiondatas,
        'department_totals':department_totals,
        'divisiononroll_dict':divisiononroll_dict,
        'departmentemp_totals':departmentemp_totals,
        'division_totals':division_totals,
        'department_variance_dict':department_variance_dict,
        'division_variance_dict':division_variance_dict,
        'Contractdepartment_totals':Contractdepartment_totals,
        'Contractdivision_totals':Contractdivision_totals,
         'onrollContractdepartment_totals':onrollContractdepartment_totals,
         'onrollContractdivision_totals':onrollContractdivision_totals,
         'onrolldepartment_variance_dict':onrolldepartment_variance_dict,
         'onrolldivision_variance_dict':onrolldivision_variance_dict,
         
        'departmentservices_dict' : departmentservices_dict,
        'divisionservices_dict': divisionservices_dict,
        'totaldepartmentservices_dict': totaldepartmentservices_dict,
        'totaldivisionservices_dict' : totaldivisionservices_dict,
        'onrolldepartment_variance_dictss':onrolldepartment_variance_dictss,

        'onrolldivision_variance_dictss':onrolldivision_variance_dictss,

        'grandtotalondataemp':grandtotalondataemp,
        'grandtotalondataemp_headcount':grandtotalondataemp_headcount,
        'Servicesgrandsalarydivion':Servicesgrandsalarydivion,
        'grandtotalondatabudget':grandtotalondatabudget,
        'headgrandtotalondatabudget':headgrandtotalondatabudget,
        'orrollServicesgrandsalarydivion':   orrollServicesgrandsalarydivion,
        'variance_detaavg_salary':variance_detaavg_salary,
        'variance_detaheadcount': variance_detaheadcount,
        'variance_detatotal_ctc': variance_detatotal_ctc,

        
        'budgetcontractgrandtotalondataemp':budgetcontractgrandtotalondataemp,
        'budgetcontractgrandtotalondataemp_headcount':budgetcontractgrandtotalondataemp_headcount,
        'budgetcontractdatagrandsalarydivion':budgetcontractdatagrandsalarydivion,

        'enterycontractdetasgrand':enterycontractdetasgrand,
        'enterycontractdetasheadgrandtotalon':enterycontractdetasheadgrandtotalon,
        'enterycontractempgrandsalarydivion':enterycontractempgrandsalarydivion,

        'datavariance_detaavg_salary':datavariance_detaavg_salary,
        'datavariance_detaheadcount':datavariance_detaheadcount,
        'datavariance_detatotal_ctc':datavariance_detatotal_ctc,

        'enteryservicedetasgrand' : enteryservicedetasgrand,
        'enteryservicedetasheadgrandtotalon' : enteryservicedetasheadgrandtotalon,
        'enteryserviceempgrandsalarydivion' : enteryserviceempgrandsalarydivion,
        
        'budgetservicegrandtotalondataemp' : budgetservicegrandtotalondataemp,
        'budgetservicegrandtotalondataemp_headcount' : budgetservicegrandtotalondataemp_headcount,
        'budgetservicedatagrandsalarydivion' : budgetservicedatagrandsalarydivion,
         
        'servicedatavariance_detaavg_salary' : servicedatavariance_detaavg_salary,
        'servicedatavariance_detaheadcount' : servicedatavariance_detaheadcount,
        'servicedatavariance_detatotal_ctc' : servicedatavariance_detatotal_ctc,

        'varicanmealcoast':varicanmealcoast,
        'varinceinsurancecoast' :varinceinsurancecoast
        
    }

    return render(request, "manningguide/VarianceReport/variancereport.html", context)



# --------------------------------------------------- / Experimental Code ------------------------------

def Variance_Ceo_Report(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")

    UserType = request.session.get("UserType") 
    
    # print("UserType is here::", UserType)
    Department_Name = request.session.get("Department_Name")
    if  UserType == 'CEO' :
            pass
    else:
           return Error(request, "No Access")  
    
    selectedOrganizationID = request.GET.get('hotel_name', OrganizationID)
    exclude_zero_headcount = request.GET.get('exclude_zero_headcount', 0) 

    print("selectedOrganizationID is here::", selectedOrganizationID)
    print("exclude_zero_headcount is here::", exclude_zero_headcount)

    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []
    
    context = {
        'memOrg': memOrg,
        'selectedOrganizationID':int(selectedOrganizationID),
        'selectedOrganizationID_str':selectedOrganizationID,
        'exclude_zero_headcount':int(exclude_zero_headcount)
    }
    return render(request, "manningguide/VarianceReport/Variance_Ceo_Report.html", context)


from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.db import connection

def Variance_Ceo_Report_PDF(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    exclude_zero_headcount = 0  # or fetch from query params if needed
    
    selectedOrganizationID = request.GET.get('hotel_name')
    if not selectedOrganizationID:
        selectedOrganizationID = OrganizationID

    exclude_zero_headcount_str = request.GET.get('exclude_zero', '0')  # default as string

    try:
        exclude_zero_headcount = int(exclude_zero_headcount_str)
    except ValueError:
        exclude_zero_headcount = 0

    # print("organization_id::", organization_id)
    # print("exclude_zero_headcount::", exclude_zero_headcount)

    # All Organization Name
    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    # Call the stored procedure directly
    with connection.cursor() as cursor:
        try:
            cursor.execute("EXEC ManningGuide_SP_Variance_Master_Rerport %s, %s", [selectedOrganizationID, exclude_zero_headcount])
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            return HttpResponse("Database error: " + str(e))
        

    selected_organization = next((org for org in memOrg if str(org['OrganizationID']) == selectedOrganizationID), None)
    selectedOrganizationName = selected_organization['Organization_name'] if selected_organization else "Unknown Organization"

    current_datetime = datetime.now()
    # Prepare context for PDF template
    context = {
        "records": data,
        "organization_id": OrganizationID,
        'current_datetime':current_datetime,
        'selectedOrganizationName': selectedOrganizationName,
    }

    template_path = 'manningguide/VarianceReport/Variance_Ceo_Report_PDF.html'
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Variance_CEO_Report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('PDF generation error <pre>' + html + '</pre>')

    return response



# from django.db.models import Sum, Count, Q, F, FloatField, IntegerField
# from django.db.models.functions import Coalesce
# from django.http import JsonResponse
# from datetime import datetime
# from .models import (
#     ManningGuide_ManningMaster,
#     EmployeeWorkDetails,
#     EmployeeSalary,
#     Full_and_Final_Settltment
# )

from django.db.models import Sum, F, FloatField, Value as V, Case, When
from django.db.models.functions import Coalesce
from collections import defaultdict
from HumanResources import * 

# from django.shortcuts import render
# from django.db.models import Prefetch, F, ExpressionWrapper, FloatField, Sum, Count
# from .models import (
#     OnRollDivisionMaster, OnRollDepartmentMaster, OnRollDesignationMaster,
#     ManageBudgetOnRoll
# )

def DepartmentTotalsView_Demo_Api(request):
    selected_organization_id = request.GET.get('hotel_name')
    selected_division = request.GET.get('divisionname')
    selected_department = request.GET.get('departmentname')
    exclude_zero_headcount = request.GET.get('exclude_zero_headcount')

    selected_organization_id = 1601
    selected_division = 'Finance'
    selected_department = 'Purchase'
    exclude_zero_headcount = 0


    # Filter divisions and departments
    filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

    divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).order_by('Order')

    if selected_division and selected_division != 'All Division':
        divisions = divisions.filter(DivisionName=selected_division)
        filtered_departments = filtered_departments.filter(OnRollDivisionMaster__DivisionName=selected_division)

    if selected_department and selected_department != 'All Department':
        filtered_departments = filtered_departments.filter(DepartmentName=selected_department)

    # Prefetch related data
    divisions = divisions.prefetch_related(
        Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
        Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
    )

    # Prepare budget data
    managebudget_qs = ManageBudgetOnRoll.objects.annotate(
        clean_hotel_name=F('hotel_name')
    ).filter(
        clean_hotel_name=selected_organization_id,
        is_delete=False
    ).values(
        'on_roll_division_master__DivisionName',
        'on_roll_department_master__DepartmentName',
        'on_roll_designation_master__designations'
    ).annotate(
        head_count=F('head_count'),
        total_salary=Sum('avg_salary'),
        aavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        budgetmultiplication_result=ExpressionWrapper(F('aavg_salary') * F('head_count'), output_field=FloatField())
    )

    if exclude_zero_headcount:
        managebudget_qs = managebudget_qs.exclude(head_count=0)

    department_totals = {}

    # for budget in managebudget_qs:
    #     dept_name = budget['on_roll_department_master__DepartmentName']
    #     if dept_name not in department_totals:
    #         department_totals[dept_name] = {
    #             'budgetmultiplication_result': 0,
    #             'total_headcount': 0,
    #             'salary_headcount_product': 0,
    #         }

    #     department_totals[dept_name]['budgetmultiplication_result'] += budget.get('budgetmultiplication_result', 0) or 0
    #     department_totals[dept_name]['total_headcount'] += budget.get('head_count', 0) or 0

    #     # Calculate average salary
    #     if department_totals[dept_name]['total_headcount'] > 0:
    #         department_totals[dept_name]['salary_headcount_product'] = (
    #             department_totals[dept_name]['budgetmultiplication_result'] / department_totals[dept_name]['total_headcount']
    #         )

    for budget in managebudget_qs:
        division_name = budget['on_roll_division_master__DivisionName']
        dept_name = budget['on_roll_department_master__DepartmentName']
        key = f"{division_name}::{dept_name}"  # unique per division+department

        if key not in department_totals:
            department_totals[key] = {
                'division': division_name,
                'department': dept_name,
                'budgetmultiplication_result': 0,
                'total_headcount': 0,
                'salary_headcount_product': 0,
            }

        department_totals[key]['budgetmultiplication_result'] += budget.get('budgetmultiplication_result', 0) or 0
        department_totals[key]['total_headcount'] += budget.get('head_count', 0) or 0

        if department_totals[key]['total_headcount'] > 0:
            department_totals[key]['salary_headcount_product'] = (
                department_totals[key]['budgetmultiplication_result'] / department_totals[key]['total_headcount']
            )


    print('divisions', divisions)
    print('department_totals', department_totals)

    from django.http import JsonResponse

    # return JsonResponse({
    #     'divisions': divisions,
    #     'department_totals': department_totals
    # }, safe=False)

    return JsonResponse({
        'divisions': list(divisions.values()),  # or .values_list('fieldname', flat=True)
        'department_totals': department_totals
    })


from django.db.models import Count, Sum, FloatField, F, Q, ExpressionWrapper, Prefetch
from django.shortcuts import render, redirect
# from .models import OnRollDivisionMaster, OnRollDepartmentMaster, EmployeeWorkDetails

def DepartmentTotalsView_Demo_Api2(request):
    # OrganizationID = request.session.get("OrganizationID")
    # selectedOrganizationID = request.GET.get('hotel_name', OrganizationID)
    # exclude_zero_headcount = request.GET.get('exclude_zero_headcount')  

    OrganizationID = 3
    selectedOrganizationID = 1601
    exclude_zero_headcount = 0

    # Filter departments and prefetch into divisions
    filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    Divisiondatas = (
        OnRollDivisionMaster.objects.filter(IsDelete=False)
        .order_by('Order')
        .prefetch_related(
            Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments)
        )
    )

    # Aggregate employee data per department
    employees_per_department = (
        EmployeeWorkDetails.objects.filter(
            OrganizationID=selectedOrganizationID,
            IsDelete=False,
            IsSecondary=False,
            EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"]
        )
        .exclude(Department__isnull=True)
        .exclude(Department='')
        .values('Department')
        .annotate(
            total_headcount=Count('id'),
            total_salarymulti=Sum('Salary', filter=Q(Salary__isnull=False, Salary__gt=0)),
            salary_headcount_product=ExpressionWrapper(
                Sum('Salary', filter=Q(Salary__isnull=False, Salary__gt=0)) / Count('id'),
                output_field=FloatField()
            )
        )
        .order_by('Department')
    )

    if exclude_zero_headcount:
        employees_per_department = employees_per_department.exclude(total_headcount=0)

    # Convert queryset to dictionary for template
    # department_totals = {
    #     row['Department']: {
    #         'total_salarymulti': row['total_salarymulti'] or 0,
    #         'total_headcount': row['total_headcount'] or 0,
    #         'salary_headcount_product': row['salary_headcount_product'] or 0
    #     }
    #     for row in employees_per_department
    # }

    department_totals = [
        {
            'Department': row['Department'],
            'total_salarymulti': row['total_salarymulti'] or 0,
            'total_headcount': row['total_headcount'] or 0,
            'salary_headcount_product': row['salary_headcount_product'] or 0
        }
        for row in employees_per_department
    ]

    context = {
        'department_totals': department_totals,
        # 'exclude_zero_headcount': bool(exclude_zero_headcount)
    }

    return JsonResponse(context, safe=False)



# from django.db.models import Sum, Count, F, FloatField, ExpressionWrapper, Q
# from HumanResources import Master
# # --------- try
# def DepartmentTotalsView_Demo_Api(request):
#     # selected_organization_id = request.GET.get('hotel_name')
#     # selected_division = request.GET.get('divisionname')
#     # selected_department = request.GET.get('departmentname')
#     # exclude_zero_headcount = request.GET.get('exclude_zero_headcount')

#     # selected_organization_id = 1601
    
#     # from django.db.models import Sum, Count, F, FloatField, ExpressionWrapper, Q

#     selected_organization_id = 1601

#     # === Budget Data ===
#     budget_qs = ManageBudgetOnRoll.objects.filter(
#         hotel_name=selected_organization_id,
#         is_delete=False
#     ).values(
#         'on_roll_division_master__DivisionName',
#         'on_roll_department_master__DepartmentName'
#     ).annotate(
#         bud_total_ctc=Sum(F('avg_salary') * F('head_count'), output_field=FloatField()),
#         bud_hc=Sum('head_count')
#     ).annotate(
#         bud_avg_sal=ExpressionWrapper(
#             F('bud_total_ctc') / F('bud_hc'),
#             output_field=FloatField()
#         )
#     )

#     # === Actual Data ===
#     actual_qs = HumanResources_MasterData.objects.filter(
#         OrganizationID=selected_organization_id,
#         EmpStatus__in=['On Probation', 'Confirmed', 'Not Confirmed']
#     ).values(
#         'Division',
#         'Department'
#     ).annotate(
#         act_total_ctc=Sum('Salary'),
#         act_hc=Count('EmpID')
#     ).annotate(
#         act_avg_sal=ExpressionWrapper(
#             F('act_total_ctc') / F('act_hc'),
#             output_field=FloatField()
#         )
#     )

#     # === Merge Budget + Actual ===
#     department_totals = {}

#     # First put budget in dict
#     for b in budget_qs:
#         dept_key = (b['on_roll_division_master__DivisionName'], b['on_roll_department_master__DepartmentName'])
#         department_totals[dept_key] = {
#             'bud_total_ctc': b['bud_total_ctc'] or 0,
#             'bud_hc': b['bud_hc'] or 0,
#             'bud_avg_sal': b['bud_avg_sal'] or 0,
#             'act_total_ctc': 0,
#             'act_hc': 0,
#             'act_avg_sal': 0
#         }

#     # Add actuals
#     for a in actual_qs:
#         dept_key = (a['Division'], a['Department'])
#         if dept_key not in department_totals:
#             department_totals[dept_key] = {
#                 'bud_total_ctc': 0,
#                 'bud_hc': 0,
#                 'bud_avg_sal': 0
#             }
#         department_totals[dept_key].update({
#             'act_total_ctc': a['act_total_ctc'] or 0,
#             'act_hc': a['act_hc'] or 0,
#             'act_avg_sal': a['act_avg_sal'] or 0
#         })

#     # === Calculate Variance ===
#     for dept, vals in department_totals.items():
#         vals['var_total_ctc'] = (vals['act_total_ctc'] or 0) - (vals['bud_total_ctc'] or 0)
#         vals['var_hc'] = (vals['act_hc'] or 0) - (vals['bud_hc'] or 0)
#         vals['var_avg_sal'] = (vals['act_avg_sal'] or 0) - (vals['bud_avg_sal'] or 0)

#     print(department_totals)


#     return JsonResponse({
#         'divisions': list(divisions.values()),  # or .values_list('fieldname', flat=True)
#         'department_totals': department_totals
#     })




from django.http import JsonResponse
from django.db import connection

def variance_report_api(request):
    organization_id = request.GET.get('organization_id', 401)
    exclude_zero_headcount_str = request.GET.get('exclude_zero', '0')  # default as string

    try:
        exclude_zero_headcount = int(exclude_zero_headcount_str)
    except ValueError:
        exclude_zero_headcount = 0

    print("organization_id::", organization_id)
    print("exclude_zero_headcount::", exclude_zero_headcount)


    with connection.cursor() as cursor:
        try:
            cursor.execute("EXEC ManningGuide_SP_Variance_Master_Rerport %s, %s", [organization_id, exclude_zero_headcount])
            
            # Get column names
            columns = [col[0] for col in cursor.description]
            
            # Fetch all rows
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return JsonResponse({'status': True, 'data': data}, safe=False)
        except Exception as e:
            return JsonResponse({'status': False, 'error': str(e)}, status=500)


# --------------------------------------------------- / Experimental Code ------------------------------



def variancepdf(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')
    
    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  
    
    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []
    

    selectedOrganizationID = str(request.GET.get('hotel_name', OrganizationID))
    selected_division = request.GET.get('divisionname')
    selected_department = request.GET.get('departmentname')
    
    
    include_on_roll = request.GET.get('include_on_roll') == 'true'
    include_contract = request.GET.get('include_contract') == 'true'
    include_shared_services = request.GET.get('include_shared_services') == 'true'
    include_cafeteria = request.GET.get('include_cafeteria') == 'true'
    include_insurance = request.GET.get('include_insurance') == 'true'
    

    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False)
    departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)

    if selected_division and selected_division != 'All Division':
        Divisiondatas = Divisiondatas.filter(DivisionName=selected_division)
        departments = OnRollDepartmentMaster.objects.filter(
            OnRollDivisionMaster__DivisionName=selected_division, IsDelete=False
        )
    if selected_department and selected_department != 'All Department':
        departments = departments.filter(DepartmentName=selected_department)

    # contractdivisions = ContractDivisionMaster.objects.all().order_by('Order').prefetch_related(
    #     'contractdepartmentmaster_set__contractdesignationmaster_set'
    # )
    # Servicedivisions = ServicesDivisionMaster.objects.all().order_by('Order').prefetch_related(
    #     'servicesdepartmentmaster_set__servicesdesignationmaster_set'
    # )
    
    filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

       
    Divisiondatas = OnRollDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
            Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
            Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
        )
    
    filtered_contract_departments = ContractDepartmentMaster.objects.filter(IsDelete=False)
    filtered_contract_designations = ContractDesignationMaster.objects.filter(IsDelete=False)

    
    filtered_service_departments = ServicesDepartmentMaster.objects.filter(IsDelete=False)
    filtered_service_designations = ServicesDesignationMaster.objects.filter(IsDelete=False)

    
    contractdivisions = ContractDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('contractdepartmentmaster_set', queryset=filtered_contract_departments),
        Prefetch('contractdepartmentmaster_set__contractdesignationmaster_set', queryset=filtered_contract_designations)
    )

    
    Servicedivisions = ServicesDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('servicesdepartmentmaster_set', queryset=filtered_service_departments),
        Prefetch('servicesdepartmentmaster_set__servicesdesignationmaster_set', queryset=filtered_service_designations)
    )
    




    template_path = 'manningguide/VarianceReport/variancepdf.html'
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')

    selected_organization = next((org for org in memOrg if str(org['OrganizationID']) == selectedOrganizationID), None)
    selectedOrganizationName = selected_organization['Organization_name'] if selected_organization else "Unknown Organization"
    
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organization = OrganizationMaster.objects.filter(OrganizationID=selectedOrganizationID).first()
    organization_logo = f"{base_url}{organization.OrganizationLogo}" if organization and organization.OrganizationLogo else None

    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

   
    

    employees_per_department_designation = EmployeeWorkDetails.objects.all()

    if selectedOrganizationID:
        employees_per_department_designation = employees_per_department_designation.filter(OrganizationID=selectedOrganizationID,IsDelete=False,IsSecondary=False,EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"])

    employees_per_department_designation = (
        employees_per_department_designation
        .values('Department', 'Designation')
        .annotate(
            num_employees=Count('id'),
            total_salary=Sum('Salary'),
            avg_salary=ExpressionWrapper(Sum('Salary') / Count('id'), output_field=FloatField()),
            multiplication_result=F('avg_salary') * F('num_employees')
        )
        .order_by('Department', 'Designation')
    )

    managebudget_department_designation = ManageBudgetOnRoll.objects.filter(
        hotel_name=selectedOrganizationID,
    ).values(
        'on_roll_department_master__DepartmentName',
        'on_roll_designation_master__designations'
    ).annotate(
        head_count=Sum('head_count'),
        total_salary=Sum('avg_salary'),
        aavg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        budgetmultiplication_result=F('aavg_salary') * F('head_count')
    ).order_by(
        'on_roll_department_master__DepartmentName',
        'on_roll_designation_master__designations'
    )

    departmentemp_totals = {}
    employees_dict = {}
    division_totals = {}

    for emp in employees_per_department_designation:
        dept = emp['Department']
        department_name = dept
        designation = emp['Designation']
        avg_salary = emp['avg_salary']
        num_employees = emp['num_employees']
        multiplication_result = avg_salary * num_employees  

        divisions_qs = OnRollDivisionMaster.objects.filter(
            onrolldepartmentmaster__DepartmentName=department_name
        ).annotate(
            department_name=F('onrolldepartmentmaster__DepartmentName')
        ).values(
            'DivisionName',  
        )

        logger.debug(f"Divisions queryset for department '{department_name}': {divisions_qs}")

        division_name = divisions_qs[0]['DivisionName'] if divisions_qs else None

        if dept not in departmentemp_totals:
            departmentemp_totals[dept] = {
                'total_salarymulti': 0,
                'total_headcount': 0,
                'salary_headcount_product': 0,
            }

        if division_name and division_name not in division_totals:
            division_totals[division_name] = {
                'divisiontotal_salarymulti': 0,
                'divisiontotal_headcount': 0,
                'divisionsalary_headcount_product': 0,
            }

        if dept not in employees_dict:
            employees_dict[dept] = {}

        employees_dict[dept][designation] = {
            'num_employees': num_employees,
            'avg_salary': avg_salary,
            'multiplication_result': multiplication_result  
        }

        departmentemp_totals[dept]['total_salarymulti'] += avg_salary
        departmentemp_totals[dept]['total_headcount'] += num_employees
        departmentemp_totals[dept]['salary_headcount_product'] = (
            departmentemp_totals[dept]['total_salarymulti'] * departmentemp_totals[dept]['total_headcount']
        )

        if division_name:
            division_totals[division_name]['divisiontotal_salarymulti'] += avg_salary
            division_totals[division_name]['divisiontotal_headcount'] += num_employees
            division_totals[division_name]['divisionsalary_headcount_product'] = (
                division_totals[division_name]['divisiontotal_salarymulti'] * division_totals[division_name]['divisiontotal_headcount']
            )

    


   










    budgets_dict = {}
    department_totals = {}
    divisiononroll_dict = {}

    for budget in managebudget_department_designation:
        dept_id = budget['on_roll_department_master__DepartmentName']
        desig_id = budget['on_roll_designation_master__designations']
        
        if dept_id not in budgets_dict:
            budgets_dict[dept_id] = {}
            
        budgets_dict[dept_id][desig_id] = {
            'head_count': budget['head_count'],
            'aavg_salary': budget['aavg_salary'],
            'budgetmultiplication_result': budget['budgetmultiplication_result'],
        }

        if dept_id not in department_totals:
            department_totals[dept_id] = {
                'aavg_salary': 0,
                'total_headcount': 0,
                'salary_headcount_product': 0,
            }

        department_totals[dept_id]['aavg_salary'] += (
            budget['aavg_salary'] or 0
        )

        
        department_totals[dept_id]['total_headcount'] += (
            budget['head_count'] or 0
        )

        if department_totals[dept_id]['total_headcount'] > 0:
            department_totals[dept_id]['salary_headcount_product'] = (
                department_totals[dept_id]['aavg_salary'] * department_totals[dept_id]['total_headcount']
            )

        divisions_qs = OnRollDivisionMaster.objects.filter(
            onrolldepartmentmaster__DepartmentName=dept_id
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')

        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name and division_name not in divisiononroll_dict:
            divisiononroll_dict[division_name] = {
                'onrollonmultiplication_result': 0,
                'onrolldivisiontotal_headcount': 0,
                'onrolldivisionsalary_headcount_product': 0,
            }

        if division_name:
            # Use `budget` values instead of `department_totals`
            # divisiononroll_dict[division_name]['onrollonmultiplication_result'] += budget['aavg_salary']
            # divisiononroll_dict[division_name]['onrolldivisiontotal_headcount'] += budget['head_count']
            divisiononroll_dict[division_name]['onrollonmultiplication_result'] += (
                budget['aavg_salary'] or 0
            )

            
            divisiononroll_dict[division_name]['onrolldivisiontotal_headcount'] += (
                budget['head_count'] or 0
            )
            if divisiononroll_dict[division_name]['onrolldivisiontotal_headcount'] > 0:
                divisiononroll_dict[division_name]['onrolldivisionsalary_headcount_product'] = (
                    divisiononroll_dict[division_name]['onrollonmultiplication_result'] / divisiononroll_dict[division_name]['onrolldivisiontotal_headcount']
                    # divisiononroll_dict[division_name]['onrollonmultiplication_result'] * divisiononroll_dict[division_name]['onrolldivisiontotal_headcount']
                )

    grandtotalondataemp = sum(
        dept['divisiontotal_salarymulti'] for dept in division_totals.values() if 'divisiontotal_salarymulti' in dept
    )
    grandtotalondataemp_headcount = sum(
        dept['divisiontotal_headcount'] for dept in division_totals.values() if 'divisiontotal_headcount' in dept
    )

    if grandtotalondataemp_headcount > 0:
        Servicesgrandsalarydivion = grandtotalondataemp * grandtotalondataemp_headcount
    else:
        Servicesgrandsalarydivion = 0

    # Calculate budget totals
    grandtotalondatabudget = sum(
        dept['onrollonmultiplication_result'] for dept in divisiononroll_dict.values() if 'onrollonmultiplication_result' in dept
    )
    headgrandtotalondatabudget = sum(
        dept['onrolldivisiontotal_headcount'] for dept in divisiononroll_dict.values() if 'onrolldivisiontotal_headcount' in dept
    )

    if headgrandtotalondatabudget > 0:
        orrollServicesgrandsalarydivion = grandtotalondatabudget * headgrandtotalondatabudget
    else:
        orrollServicesgrandsalarydivion = 0

    # Calculate variances
    variance_detaavg_salary = grandtotalondataemp - grandtotalondatabudget
    variance_detaheadcount = grandtotalondataemp_headcount - headgrandtotalondatabudget
    variance_detatotal_ctc = Servicesgrandsalarydivion - orrollServicesgrandsalarydivion
    
  

    variance_dict = {}
    for dept, designations in employees_dict.items():
        if dept not in variance_dict:
            variance_dict[dept] = {}
        for desig, emp_data in designations.items():
            head_count = budgets_dict.get(dept, {}).get(desig, {}).get('head_count', 0)
            aavg_salary = budgets_dict.get(dept, {}).get(desig, {}).get('aavg_salary', 0)
            budget_multiplication_result = budgets_dict.get(dept, {}).get(desig, {}).get('budgetmultiplication_result', 0)

            emp_num_employees = emp_data.get('num_employees', 0)
            emp_avg_salary = emp_data.get('avg_salary', 0)
            emp_multiplication_result = emp_data.get('multiplication_result', 0)

            variance_head_count = (emp_num_employees or 0) - (head_count or 0)

            
            variance_salary = (emp_avg_salary or 0) - (aavg_salary or 0)

            
            variance_total_result = (emp_multiplication_result or 0) - (budget_multiplication_result or 0)
            variance_dict[dept][desig] = {
                'variance_head_count': variance_head_count,
                'variance_salary': variance_salary,
                'variance_total_result': variance_total_result,
                'num_employees': emp_num_employees,
                'avg_salary': emp_avg_salary,
                'head_count': head_count,
                'aavg_salary': aavg_salary,
                'multiplication_result': emp_multiplication_result,
                'budgetmultiplication_result': budget_multiplication_result
            }

    department_variance_dict = {}
    for dept, emp_data in departmentemp_totals.items():
        # Get budget data for comparison
        budget_data = department_totals.get(dept, {})
        budget_aavg_salary = budget_data.get('aavg_salary', 0)
        budget_total_headcount = budget_data.get('total_headcount', 0)
        budget_salary_headcount_product = budget_data.get('salary_headcount_product', 0)

        # Get actual data
        actual_salary_multi = emp_data['total_salarymulti']
        actual_headcount = emp_data['total_headcount']
        actual_salary_headcount_product = emp_data['salary_headcount_product']

        # Calculate variance
        variance_salary_multi = actual_salary_multi - budget_aavg_salary
        variance_headcount = actual_headcount - budget_total_headcount
        variance_salary_headcount_product = actual_salary_headcount_product - budget_salary_headcount_product

        department_variance_dict[dept] = {
            'actual_salary_multi': actual_salary_multi,
            'actual_headcount': actual_headcount,
            'actual_salary_headcount_product': actual_salary_headcount_product,
            'budget_aavg_salary': budget_aavg_salary,
            'budget_total_headcount': budget_total_headcount,
            'budget_salary_headcount_product': budget_salary_headcount_product,
            'variance_salary_multi': variance_salary_multi,
            'variance_headcount': variance_headcount,
            'variance_salary_headcount_product': variance_salary_headcount_product
        }

# Calculate variance for divisions
    division_variance_dict = {}
    for division, data in divisiononroll_dict.items():
        # Get budget data for comparison
        budget_data = division_totals.get(division, {})
        budget_division_total_salary_multi = budget_data.get('divisiontotal_salarymulti', 0)
        budget_division_total_headcount = budget_data.get('divisiontotal_headcount', 0)
        budget_division_salary_headcount_product = budget_data.get('divisionsalary_headcount_product', 0)

        # Get actual data
        actual_salary_multi = data['onrollonmultiplication_result']
        actual_headcount = data['onrolldivisiontotal_headcount']
        actual_salary_headcount_product = data['onrolldivisionsalary_headcount_product']

        # Calculate variance
        variance_salary_multi = actual_salary_multi - budget_division_total_salary_multi
        variance_headcount = actual_headcount - budget_division_total_headcount
        variance_salary_headcount_product = actual_salary_headcount_product - budget_division_salary_headcount_product
        
        division_variance_dict[division] = {
            'actual_salary_multi': actual_salary_multi,
            'actual_headcount': actual_headcount,
            'actual_salary_headcount_product': actual_salary_headcount_product,
            'budget_division_total_salary_multi': budget_division_total_salary_multi,
            'budget_division_total_headcount': budget_division_total_headcount,
            'budget_division_salary_headcount_product': budget_division_salary_headcount_product,
            'variance_salary_multi': variance_salary_multi,
            'variance_headcount': variance_headcount,
            'variance_salary_headcount_product': variance_salary_headcount_product
        }        
    






    # Retrieve and aggregate data from EntryActualContract

    actual_contract_data = EntryActualContract.objects.filter(
        hotel_name=selectedOrganizationID
    ).values(
        'contract_department_master__DepartmentName',
        'contract_designation_master__designations'
    ).annotate(
        actual_head_count=Sum('head_count'),
        actual_avg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        actual_total_ctc=F('actual_avg_salary') * F('actual_head_count')
    ).order_by(
        'contract_department_master__DepartmentName',
        'contract_designation_master__designations'
    )

    # Fetch and process budget contract data
    budget_contract_data = ManageBudgetContract.objects.filter(
        hotel_name=selectedOrganizationID
    ).values(
        'contract_department_master__DepartmentName',
        'contract_designation_master__designations'
    ).annotate(
        budget_head_count=Sum('head_count'),
        budget_avg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        budget_total_ctc=F('budget_avg_salary') * F('budget_head_count')
    ).order_by(
        'contract_department_master__DepartmentName',
        'contract_designation_master__designations'
    )

    # Initialize dictionaries
    actual_dict = {}
    Contractdepartment_totals = {}
    Contractdivision_totals = {}

    # Process actual contract data
    for item in actual_contract_data:
        dept = item['contract_department_master__DepartmentName']
        designation = item['contract_designation_master__designations']
        
        if dept not in actual_dict:
            actual_dict[dept] = {}
        actual_dict[dept][designation] = {
            'actual_head_count': item['actual_head_count'],
            'actual_avg_salary': item['actual_avg_salary'],
            'actual_total_ctc': item['actual_total_ctc']
        }
        
        if dept not in Contractdepartment_totals:
            Contractdepartment_totals[dept] = {
                'Contractmultiplication_result': 0,
                'Contracthead_count': 0,
                'salary_headcount_contract': 0,
            }

        # Update totals
        Contractdepartment_totals[dept]['Contractmultiplication_result'] += item['actual_avg_salary']
        Contractdepartment_totals[dept]['Contracthead_count'] += item['actual_head_count']

        if Contractdepartment_totals[dept]['Contracthead_count'] > 0:
            Contractdepartment_totals[dept]['salary_headcount_contract'] = (
                Contractdepartment_totals[dept]['Contractmultiplication_result'] * Contractdepartment_totals[dept]['Contracthead_count']
            )

        # Fetch and process division data
        divisions_qs = ContractDivisionMaster.objects.filter(
            contractdepartmentmaster__DepartmentName=dept
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')

        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name and division_name not in Contractdivision_totals:
            Contractdivision_totals[division_name] = {
                'Contractdivisionmultiplication_result': 0,
                'Contractdivisiontotal_headcount': 0,
                'Contractdivisionsalary_headcount_product': 0,
            }

        if division_name:
            Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] += item['actual_avg_salary']
            Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] += item['actual_head_count']

            if Contractdivision_totals[division_name]['Contractdivisiontotal_headcount'] > 0:
                Contractdivision_totals[division_name]['Contractdivisionsalary_headcount_product'] = (
                    Contractdivision_totals[division_name]['Contractdivisionmultiplication_result'] * Contractdivision_totals[division_name]['Contractdivisiontotal_headcount']
                )

    # Initialize budget-related dictionaries
    budget_dict = {}
    onrollContractdepartment_totals = {}
    onrollContractdivision_totals = {}

    # Process budget contract data
    for itembudget in budget_contract_data:
        dept = itembudget['contract_department_master__DepartmentName']
        designation = itembudget['contract_designation_master__designations']
        
        if dept not in budget_dict:
            budget_dict[dept] = {}
        budget_dict[dept][designation] = {
            'budget_head_count': itembudget['budget_head_count'],
            'budget_avg_salary': itembudget['budget_avg_salary'],
            'budget_total_ctc': itembudget['budget_total_ctc']
        }
        
        if dept not in onrollContractdepartment_totals:
            onrollContractdepartment_totals[dept] = {
                'Contractmultiplication_result': 0,
                'Contracthead_count': 0,
                'salary_headcount_contract': 0,
            }

        # Update totals
        # onrollContractdepartment_totals[dept]['Contractmultiplication_result'] += itembudget['budget_avg_salary']
        # onrollContractdepartment_totals[dept]['Contracthead_count'] += itembudget['budget_head_count']
        onrollContractdepartment_totals[dept]['Contractmultiplication_result'] += (
            itembudget['budget_avg_salary'] or 0
        )

        # Safely add 'budget_head_count' to Contracthead_count
        onrollContractdepartment_totals[dept]['Contracthead_count'] += (
            itembudget['budget_head_count'] or 0
        )
        if onrollContractdepartment_totals[dept]['Contracthead_count'] > 0:
            onrollContractdepartment_totals[dept]['salary_headcount_contract'] = (
                onrollContractdepartment_totals[dept]['Contractmultiplication_result'] * onrollContractdepartment_totals[dept]['Contracthead_count']
            )

        # Fetch and process division data
        divisions_qs = ContractDivisionMaster.objects.filter(
            contractdepartmentmaster__DepartmentName=dept
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')

        division_name = divisions_qs[0]['division_name'] if divisions_qs else None

        if division_name and division_name not in onrollContractdivision_totals:
            onrollContractdivision_totals[division_name] = {
                'Contractdivisionmultiplication_result': 0,
                'Contractdivisiontotal_headcount': 0,
                'Contractdivisionsalary_headcount_product': 0,
            }
        
        if division_name:
            # onrollContractdivision_totals[division_name]['Contractdivisionmultiplication_result'] += itembudget['budget_avg_salary']
            # onrollContractdivision_totals[division_name]['Contractdivisiontotal_headcount'] += itembudget['budget_head_count']
            onrollContractdivision_totals[division_name]['Contractdivisionmultiplication_result'] += (
                itembudget['budget_avg_salary'] or 0
            )

           
            onrollContractdivision_totals[division_name]['Contractdivisiontotal_headcount'] += (
                itembudget['budget_head_count'] or 0
            )
            if onrollContractdivision_totals[division_name]['Contractdivisiontotal_headcount'] > 0:
                onrollContractdivision_totals[division_name]['Contractdivisionsalary_headcount_product'] = (
                    onrollContractdivision_totals[division_name]['Contractdivisionmultiplication_result'] * onrollContractdivision_totals[division_name]['Contractdivisiontotal_headcount']
      
                )


 

# Calculate contract   
    enterycontractdetasgrand = sum(
        dept['Contractdivisionmultiplication_result'] for dept in Contractdivision_totals.values() if 'Contractdivisionmultiplication_result' in dept
    )
    enterycontractdetasheadgrandtotalon = sum(
        dept['Contractdivisiontotal_headcount'] for dept in Contractdivision_totals.values() if 'Contractdivisiontotal_headcount' in dept
    )

    if enterycontractdetasheadgrandtotalon > 0:
        enterycontractempgrandsalarydivion = enterycontractdetasgrand * enterycontractdetasheadgrandtotalon
    else:
        enterycontractempgrandsalarydivion = 0

   

 # Calculate budget contract
    budgetcontractgrandtotalondataemp = sum(
        dept['Contractdivisionmultiplication_result'] for dept in onrollContractdivision_totals.values() if 'Contractdivisionmultiplication_result' in dept
    )
    budgetcontractgrandtotalondataemp_headcount = sum(
        dept['Contractdivisiontotal_headcount'] for dept in onrollContractdivision_totals.values() if 'Contractdivisiontotal_headcount' in dept
    )

    if grandtotalondataemp_headcount > 0:
        budgetcontractdatagrandsalarydivion = budgetcontractgrandtotalondataemp * budgetcontractgrandtotalondataemp_headcount
    else:
        budgetcontractdatagrandsalarydivion = 0
    
    
    datavariance_detaavg_salary = enterycontractdetasgrand- budgetcontractgrandtotalondataemp  
    datavariance_detaheadcount = enterycontractdetasheadgrandtotalon - budgetcontractgrandtotalondataemp_headcount 
    datavariance_detatotal_ctc = enterycontractempgrandsalarydivion - budgetcontractdatagrandsalarydivion
    
    
    # # Calculate variances for contracts
    variance_contract_dict = {}
    for dept, designations in actual_dict.items():
        if dept not in variance_contract_dict:
            variance_contract_dict[dept] = {}
        for desig, actual_data in designations.items():
            budget_data = budget_dict.get(dept, {}).get(desig, {})

            actual_head_count = actual_data.get('actual_head_count', 0)
            actual_avg_salary = actual_data.get('actual_avg_salary', 0)
            actual_total_ctc = actual_data.get('actual_total_ctc', 0)

            budget_head_count = budget_data.get('budget_head_count', 0)
            budget_avg_salary = budget_data.get('budget_avg_salary', 0)
            budget_total_ctc = budget_data.get('budget_total_ctc', 0)

            variance_head_count = actual_head_count - budget_head_count
            variance_avg_salary = actual_avg_salary - budget_avg_salary
            variance_total_ctc = actual_total_ctc - budget_total_ctc

            variance_contract_dict[dept][desig] = {
                'variance_head_count': variance_head_count,
                'variance_avg_salary': variance_avg_salary,
                'variance_total_ctc': variance_total_ctc,
                'actual_head_count': actual_head_count,
                'actual_avg_salary': actual_avg_salary,
                'actual_total_ctc': actual_total_ctc,
                'budget_head_count': budget_head_count,
                'budget_avg_salary': budget_avg_salary,
                'budget_total_ctc': budget_total_ctc
            }

    # Calculate variances for department totals
    onrolldepartment_variance_dict = {}
    for dept, totals in onrollContractdepartment_totals.items():
        actual_totals = Contractdepartment_totals.get(dept, {})
        
        actual_multiplication_result = actual_totals.get('Contractmultiplication_result', 0)
        actual_head_count = actual_totals.get('Contracthead_count', 0)
        actual_salary_headcount_contract = actual_totals.get('salary_headcount_contract', 0)
        
        budget_multiplication_result = totals.get('Contractmultiplication_result', 0)
        budget_head_count = totals.get('Contracthead_count', 0)
        budget_salary_headcount_contract = totals.get('salary_headcount_contract', 0)

        variance_multiplication_result = actual_multiplication_result - budget_multiplication_result
        variance_head_count = actual_head_count - budget_head_count
        variance_salary_headcount_contract = actual_salary_headcount_contract - budget_salary_headcount_contract

        onrolldepartment_variance_dict[dept] = {
            'variance_multiplication_result': variance_multiplication_result,
            'variance_head_count': variance_head_count,
            'variance_salary_headcount_contract': variance_salary_headcount_contract,
            'actual_head_count': actual_head_count,
            'actual_multiplication_result': actual_multiplication_result,
            'actual_salary_headcount_contract': actual_salary_headcount_contract,
            'budget_head_count': budget_head_count,
            'budget_multiplication_result': budget_multiplication_result,
            'budget_salary_headcount_contract': budget_salary_headcount_contract
        }

    # Calculate variances for division totals
    onrolldivision_variance_dict = {}
    for division, totals in onrollContractdivision_totals.items():
        actual_totals = Contractdivision_totals.get(division, {})
        
        actual_multiplication_result = actual_totals.get('Contractdivisionmultiplication_result', 0)
        actual_head_count = actual_totals.get('Contractdivisiontotal_headcount', 0)
        actual_salary_headcount_product = actual_totals.get('Contractdivisionsalary_headcount_product', 0)
        
        budget_multiplication_result = totals.get('Contractdivisionmultiplication_result', 0)
        budget_head_count = totals.get('Contractdivisiontotal_headcount', 0)
        budget_salary_headcount_product = totals.get('Contractdivisionsalary_headcount_product', 0)

        variance_multiplication_result = actual_multiplication_result - budget_multiplication_result
        variance_head_count = actual_head_count - budget_head_count
        variance_salary_headcount_product = actual_salary_headcount_product - budget_salary_headcount_product

        onrolldivision_variance_dict[division] = {
            'variance_multiplication_result': variance_multiplication_result,
            'variance_head_count': variance_head_count,
            'variance_salary_headcount_product': variance_salary_headcount_product,
            'actual_head_count': actual_head_count,
            'actual_multiplication_result': actual_multiplication_result,
            'actual_salary_headcount_product': actual_salary_headcount_product,
            'budget_head_count': budget_head_count,
            'budget_multiplication_result': budget_multiplication_result,
            'budget_salary_headcount_product': budget_salary_headcount_product
        }
    



    Insurance_cost_record = BudgetInsuranceCost.objects.filter(hotel_name=selectedOrganizationID).first()

    if Insurance_cost_record:
        Insurance_cost = Insurance_cost_record.EmployeeInsurancecost
    else:
        Insurance_cost = 0 

    entryInsurance_cost_record = EntryActualInsuranceCost.objects.filter(hotel_name=selectedOrganizationID).first()

    if entryInsurance_cost_record:
        EntryInsurance_cost = entryInsurance_cost_record.EmployeeInsurancecost
    else:
        EntryInsurance_cost = 0       
    
    
    varinceinsurancecoast = (EntryInsurance_cost or 0) - (Insurance_cost or 0)

    mealcost = BudgetMealCost.objects.filter(hotel_name=selectedOrganizationID).first()

    if mealcost:
        budgetmeal = mealcost.cafeteriamealcost
    else:
        budgetmeal = 0 

    entrymealcost_record = EntryActualMealCost.objects.filter(hotel_name=selectedOrganizationID).first()

    if entrymealcost_record:
        Entrymealcost = entrymealcost_record.cafeteriamealcost
    else:
        Entrymealcost = 0       

    varicanmealcoast = Entrymealcost - budgetmeal
    
   
    actual_shared_services_data = EntryActualSharedServices.objects.filter(
        hotel_name=selectedOrganizationID
    ).values(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    ).annotate(
        actualservice_head_count=Sum('head_count'),
        actualservice_avg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        actualservice_total_ctc=F('actualservice_avg_salary') * F('actualservice_head_count')
    ).order_by(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    )

    # Query budget shared services data
    budget_shared_services_data = ManageBudgetSharedServices.objects.filter(
        hotel_name=selectedOrganizationID
    ).values(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    ).annotate(
        budgetservice_head_count=Sum('head_count'),
        budgetservice_avg_salary=ExpressionWrapper(Sum('avg_salary') / Count('id'), output_field=FloatField()),
        budgetservice_total_ctc=F('budgetservice_avg_salary') * F('budgetservice_head_count')
    ).order_by(
        'services_department_master__DepartmentName',
        'services_designation_master__designations'
    )

       
    actualservice_dict = {}
    departmentservices_dict = {}
    divisionservices_dict = {}

    for item in actual_shared_services_data:
        dept = item['services_department_master__DepartmentName']
        designation = item['services_designation_master__designations']
        
        
        if dept not in actualservice_dict:
            actualservice_dict[dept] = {}
        actualservice_dict[dept][designation] = {
            'actualservice_head_count': item['actualservice_head_count'],
            'actualservice_avg_salary': item['actualservice_avg_salary'],
            'actualservice_total_ctc': item['actualservice_total_ctc']
        }
        
        
        if dept not in departmentservices_dict:
            departmentservices_dict[dept] = {
                'TotalServicesmultiplication_result': 0,
                'TotalServiceshead_count': 0,
                'TotalServicessalary_headcount_contract': 0,
            }

        # departmentservices_dict[dept]['TotalServicesmultiplication_result'] += item['actualservice_avg_salary']
        # departmentservices_dict[dept]['TotalServiceshead_count'] += item['actualservice_head_count']
        departmentservices_dict[dept]['TotalServicesmultiplication_result'] += (
            item['actualservice_avg_salary'] or 0
        )

        # Safely add 'actualservice_head_count' to TotalServiceshead_count
        departmentservices_dict[dept]['TotalServiceshead_count'] += (
            item['actualservice_head_count'] or 0
        )
        
        if departmentservices_dict[dept]['TotalServiceshead_count'] > 0:
            departmentservices_dict[dept]['TotalServicessalary_headcount_contract'] = (
                departmentservices_dict[dept]['TotalServicesmultiplication_result'] * departmentservices_dict[dept]['TotalServiceshead_count']
            )
        
       
        divisions_qs = ServicesDivisionMaster.objects.filter(
            servicesdepartmentmaster__DepartmentName=dept
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')
        
        division_name = divisions_qs[0]['division_name'] if divisions_qs.exists() else None

        
        if division_name:
            if division_name not in divisionservices_dict:
                divisionservices_dict[division_name] = {
                    'Servicedivisionmultiplication_result': 0,
                    'Servicedivisiontotal_headcount': 0,
                    'Servicedivisionsalary_headcount_product': 0,
                }

            divisionservices_dict[division_name]['Servicedivisionmultiplication_result'] += (
                departmentservices_dict[dept]['TotalServicesmultiplication_result']
            )
            divisionservices_dict[division_name]['Servicedivisiontotal_headcount'] += (
                departmentservices_dict[dept]['TotalServiceshead_count']
            )
            
           
            if divisionservices_dict[division_name]['Servicedivisiontotal_headcount'] > 0:
                divisionservices_dict[division_name]['Servicedivisionsalary_headcount_product'] = (
                    divisionservices_dict[division_name]['Servicedivisionmultiplication_result'] * divisionservices_dict[division_name]['Servicedivisiontotal_headcount']
                )

    


        





    
           
    budgetservice_dict = {}
    totaldepartmentservices_dict = {}
    totaldivisionservices_dict = {}

    
    for itembudget in budget_shared_services_data:
        dept = itembudget['services_department_master__DepartmentName']
        designation = itembudget['services_designation_master__designations']
        
       
        if dept not in budgetservice_dict:
            budgetservice_dict[dept] = {}
        budgetservice_dict[dept][designation] = {
            'budgetservice_head_count': itembudget['budgetservice_head_count'],
            'budgetservice_avg_salary': itembudget['budgetservice_avg_salary'],
            'budgetservice_total_ctc': itembudget['budgetservice_total_ctc']
        }
        
        
        if dept not in totaldepartmentservices_dict:
            totaldepartmentservices_dict[dept] = {
                'TotalServicesmultiplication_result': 0,
                'TotalServiceshead_count': 0,
                'TotalServicessalary_headcount_contract': 0,
            }

       
        # totaldepartmentservices_dict[dept]['TotalServicesmultiplication_result'] += itembudget['budgetservice_avg_salary']
        # totaldepartmentservices_dict[dept]['TotalServiceshead_count'] += itembudget['budgetservice_head_count']
        totaldepartmentservices_dict[dept]['TotalServicesmultiplication_result'] += itembudget['budgetservice_avg_salary'] or 0
        totaldepartmentservices_dict[dept]['TotalServiceshead_count'] += itembudget['budgetservice_head_count'] or 0
        
        if totaldepartmentservices_dict[dept]['TotalServiceshead_count'] > 0:
            totaldepartmentservices_dict[dept]['TotalServicessalary_headcount_contract'] = (
                totaldepartmentservices_dict[dept]['TotalServicesmultiplication_result'] * totaldepartmentservices_dict[dept]['TotalServiceshead_count']
            )
        
       
        divisions_qs = ServicesDivisionMaster.objects.filter(
            servicesdepartmentmaster__DepartmentName=dept
        ).annotate(
            division_name=F('DivisionName')
        ).values('division_name')
        
        division_name = divisions_qs[0]['division_name'] if divisions_qs.exists() else None

        
        if division_name and division_name not in totaldivisionservices_dict:
            totaldivisionservices_dict[division_name] = {
                'Servicedivisionmultiplication_result': 0,
                'Servicedivisiontotal_headcount': 0,
                'Servicedivisionsalary_headcount_product': 0,
            }

        if division_name:
            totaldivisionservices_dict[division_name]['Servicedivisionmultiplication_result'] += (
                totaldepartmentservices_dict[dept]['TotalServicesmultiplication_result']
            )
            totaldivisionservices_dict[division_name]['Servicedivisiontotal_headcount'] += (
                totaldepartmentservices_dict[dept]['TotalServiceshead_count']
            )
            
            
            if totaldivisionservices_dict[division_name]['Servicedivisiontotal_headcount'] > 0:
                totaldivisionservices_dict[division_name]['Servicedivisionsalary_headcount_product'] = (
                    totaldivisionservices_dict[division_name]['Servicedivisionmultiplication_result'] * totaldivisionservices_dict[division_name]['Servicedivisiontotal_headcount']
                )

    # Calculate contract   
    enteryservicedetasgrand = sum(
        dept['Servicedivisionmultiplication_result'] for dept in divisionservices_dict.values() if 'Servicedivisionmultiplication_result' in dept
    )
    enteryservicedetasheadgrandtotalon = sum(
        dept['Servicedivisiontotal_headcount'] for dept in divisionservices_dict.values() if 'Servicedivisiontotal_headcount' in dept
    )

    if enteryservicedetasheadgrandtotalon > 0:
        enteryserviceempgrandsalarydivion = enteryservicedetasgrand * enteryservicedetasheadgrandtotalon
    else:
        enteryserviceempgrandsalarydivion = 0
    
    

 # Calculate budget contract
    budgetservicegrandtotalondataemp = sum(
        dept['Servicedivisionmultiplication_result'] for dept in totaldivisionservices_dict.values() if 'Servicedivisionmultiplication_result' in dept
    )
    budgetservicegrandtotalondataemp_headcount = sum(
        dept['Servicedivisiontotal_headcount'] for dept in totaldivisionservices_dict.values() if 'Servicedivisiontotal_headcount' in dept
    )

    if grandtotalondataemp_headcount > 0:
        budgetservicedatagrandsalarydivion = budgetservicegrandtotalondataemp * budgetservicegrandtotalondataemp_headcount
    else:
        budgetservicedatagrandsalarydivion = 0
    
   

    servicedatavariance_detaavg_salary = enteryservicedetasgrand- budgetservicegrandtotalondataemp  
    servicedatavariance_detaheadcount = enteryservicedetasheadgrandtotalon - budgetservicegrandtotalondataemp_headcount 
    servicedatavariance_detatotal_ctc = enteryserviceempgrandsalarydivion - budgetservicedatagrandsalarydivion
    
   
    variance_shared_services_dict = {}
    for dept, designations in actualservice_dict.items():
        if dept not in variance_shared_services_dict:
            variance_shared_services_dict[dept] = {}
        for desig, actual_data in designations.items():
            budget_data = budgetservice_dict.get(dept, {}).get(desig, {})

            actualservice_head_count = actual_data.get('actualservice_head_count', 0)
            actualservice_avg_salary = actual_data.get('actualservice_avg_salary', 0)
            actualservice_total_ctc = actual_data.get('actualservice_total_ctc', 0)

            budgetservice_head_count = budget_data.get('budgetservice_head_count', 0)
            budgetservice_avg_salary = budget_data.get('budgetservice_avg_salary', 0)
            budgetservice_total_ctc = budget_data.get('budgetservice_total_ctc', 0)

            variance_head_count = (actualservice_head_count or 0) - (budgetservice_head_count or 0)
            variance_avg_salary = (actualservice_avg_salary or 0) - (budgetservice_avg_salary or 0)
            variance_total_ctc = (actualservice_total_ctc or 0) - (budgetservice_total_ctc or 0)


            variance_shared_services_dict[dept][desig] = {
                'variance_head_count': variance_head_count,
                'variance_avg_salary': variance_avg_salary,
                'variance_total_ctc': variance_total_ctc,
                'actual_head_count': actualservice_head_count,
                'actual_avg_salary': actualservice_avg_salary,
                'actual_total_ctc': actualservice_total_ctc,
                'budget_head_count': budgetservice_head_count,
                'budget_avg_salary': budgetservice_avg_salary,
                'budget_total_ctc': budgetservice_total_ctc,
            }

    
    onrolldepartment_variance_dictss = {}
    for dept, totals in totaldepartmentservices_dict.items():
        actual_totals = departmentservices_dict.get(dept, {})
        
        actual_multiplication_result = actual_totals.get('TotalServicesmultiplication_result', 0)
        actual_head_count = actual_totals.get('TotalServiceshead_count', 0)
        actual_salary_headcount_contract = actual_totals.get('TotalServicessalary_headcount_contract', 0)
        
        budget_multiplication_result = totals.get('TotalServicesmultiplication_result', 0)
        budget_head_count = totals.get('TotalServiceshead_count', 0)
        budget_salary_headcount_contract = totals.get('TotalServicessalary_headcount_contract', 0)

        variance_multiplication_result = actual_multiplication_result - budget_multiplication_result
        variance_head_count = actual_head_count - budget_head_count
        variance_salary_headcount_contract = actual_salary_headcount_contract - budget_salary_headcount_contract

        onrolldepartment_variance_dictss[dept] = {
            'variance_multiplication_result': variance_multiplication_result,
            'variance_head_count': variance_head_count,
            'variance_salary_headcount_contract': variance_salary_headcount_contract,
            'actual_head_count': actual_head_count,
            'actual_multiplication_result': actual_multiplication_result,
            'actual_salary_headcount_contract': actual_salary_headcount_contract,
            'budget_head_count': budget_head_count,
            'budget_multiplication_result': budget_multiplication_result,
            'budget_salary_headcount_contract': budget_salary_headcount_contract,
        }

    

   
    onrolldivision_variance_dictss = {}
    for div, totals in totaldivisionservices_dict.items():
        actual_totals = divisionservices_dict.get(div, {})
        
        actual_multiplication_result = actual_totals.get('Servicedivisionmultiplication_result', 0)
        actual_head_count = actual_totals.get('Servicedivisiontotal_headcount', 0)
        actual_salary_headcount_product = actual_totals.get('Servicedivisionsalary_headcount_product', 0)
        
        budget_multiplication_result = totals.get('Servicedivisionmultiplication_result', 0)
        budget_head_count = totals.get('Servicedivisiontotal_headcount', 0)
        budget_salary_headcount_product = totals.get('Servicedivisionsalary_headcount_product', 0)

        variance_multiplication_result = actual_multiplication_result - budget_multiplication_result
        variance_head_count = actual_head_count - budget_head_count
        variance_salary_headcount_product = actual_salary_headcount_product - budget_salary_headcount_product

        onrolldivision_variance_dictss[div] = {
            'variance_multiplication_result': variance_multiplication_result,
            'variance_head_count': variance_head_count,
            'variance_salary_headcount_product': variance_salary_headcount_product,
            'actual_head_count': actual_head_count,
            'actual_multiplication_result': actual_multiplication_result,
            'actual_salary_headcount_product': actual_salary_headcount_product,
            'budget_head_count': budget_head_count,
            'budget_multiplication_result': budget_multiplication_result,
            'budget_salary_headcount_product': budget_salary_headcount_product,
        }


   

   
    

    context = {
        'divisions': Divisiondatas if include_on_roll else None,
        'Contractdivisions': contractdivisions if include_contract else None,
         'Servicedivisions': Servicedivisions if include_shared_services else None,
        'cafeteria_meal_cost': 'Data for Cafeteria Meal Cost' if include_cafeteria else None,
        'employees_insurance_cost': 'Data for Employees Insurance Cost' if include_insurance else None,
        'current_datetime': current_datetime,
        'UserID': UserID,
        'employees_per_department_designation': employees_per_department_designation,
        'managebudget_department_designation':managebudget_department_designation,
        'selectedOrganizationID': selectedOrganizationID,
        'selectedOrganizationName': selectedOrganizationName,
        'organization_logo': organization_logo,
        'organization_logos': organization_logos,

          'variance_dict': variance_dict,
        # 'variance_contract_dict': variance_contract_dict,
        'employees_dict':employees_dict,
        'budgets_dict':budgets_dict,
        'actual_dict':actual_dict,
        'budget_dict':budget_dict,
        'variance_contract_dict':variance_contract_dict,
        'Insurance_cost':Insurance_cost,
        'EntryInsurance_cost':EntryInsurance_cost,
        'budgetmeal':budgetmeal,
        'Entrymealcost':Entrymealcost,
        'actualservice_dict':actualservice_dict,
        'budgetservice_dict':budgetservice_dict,
        'variance_shared_services_dict':variance_shared_services_dict,
        'Divisiondatas':Divisiondatas,
        'department_totals':department_totals,
        'divisiononroll_dict':divisiononroll_dict,
        'departmentemp_totals':departmentemp_totals,
        'division_totals':division_totals,
        'department_variance_dict':department_variance_dict,
        'division_variance_dict':division_variance_dict,
        'Contractdepartment_totals':Contractdepartment_totals,
        'Contractdivision_totals':Contractdivision_totals,
         'onrollContractdepartment_totals':onrollContractdepartment_totals,
         'onrollContractdivision_totals':onrollContractdivision_totals,
         'onrolldepartment_variance_dict':onrolldepartment_variance_dict,
         'onrolldivision_variance_dict':onrolldivision_variance_dict,
         
        'departmentservices_dict' : departmentservices_dict,
        'divisionservices_dict': divisionservices_dict,
        'totaldepartmentservices_dict': totaldepartmentservices_dict,
        'totaldivisionservices_dict' : totaldivisionservices_dict,
        'onrolldepartment_variance_dictss':onrolldepartment_variance_dictss,

        'onrolldivision_variance_dictss':onrolldivision_variance_dictss,

        'grandtotalondataemp':grandtotalondataemp,
        'grandtotalondataemp_headcount':grandtotalondataemp_headcount,
        'Servicesgrandsalarydivion':Servicesgrandsalarydivion,
        'grandtotalondatabudget':grandtotalondatabudget,
        'headgrandtotalondatabudget':headgrandtotalondatabudget,
        'orrollServicesgrandsalarydivion':   orrollServicesgrandsalarydivion,
        'variance_detaavg_salary':variance_detaavg_salary,
        'variance_detaheadcount': variance_detaheadcount,
        'variance_detatotal_ctc': variance_detatotal_ctc,

        
        'budgetcontractgrandtotalondataemp':budgetcontractgrandtotalondataemp,
        'budgetcontractgrandtotalondataemp_headcount':budgetcontractgrandtotalondataemp_headcount,
        'budgetcontractdatagrandsalarydivion':budgetcontractdatagrandsalarydivion,

        'enterycontractdetasgrand':enterycontractdetasgrand,
        'enterycontractdetasheadgrandtotalon':enterycontractdetasheadgrandtotalon,
        'enterycontractempgrandsalarydivion':enterycontractempgrandsalarydivion,

        'datavariance_detaavg_salary':datavariance_detaavg_salary,
        'datavariance_detaheadcount':datavariance_detaheadcount,
        'datavariance_detatotal_ctc':datavariance_detatotal_ctc,

        'enteryservicedetasgrand' : enteryservicedetasgrand,
        'enteryservicedetasheadgrandtotalon' : enteryservicedetasheadgrandtotalon,
        'enteryserviceempgrandsalarydivion' : enteryserviceempgrandsalarydivion,
        
        'budgetservicegrandtotalondataemp' : budgetservicegrandtotalondataemp,
        'budgetservicegrandtotalondataemp_headcount' : budgetservicegrandtotalondataemp_headcount,
        'budgetservicedatagrandsalarydivion' : budgetservicedatagrandsalarydivion,
         
        'servicedatavariance_detaavg_salary' : servicedatavariance_detaavg_salary,
        'servicedatavariance_detaheadcount' : servicedatavariance_detaheadcount,
        'servicedatavariance_detatotal_ctc' : servicedatavariance_detatotal_ctc,

        'varicanmealcoast':varicanmealcoast,
        'varinceinsurancecoast' :varinceinsurancecoast
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response






# Report Master all type report

from django.shortcuts import render, redirect
from django.db.models import Count, Sum, FloatField

import requests
import logging

logger = logging.getLogger(__name__)

def LevelWiseReport(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")

    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    selectedOrganizationID = request.GET.get('hotel_name', OrganizationID)
    selected_departments = request.GET.getlist('Department')
    selected_levels = request.GET.getlist('Level')
    if UserType == 'CEO' and request.GET.get('hotel_name') is None:
            selectedOrganizationID = 401
    # Default selection handling
    if not selected_departments:
        selected_departments = ['All_Department']
    if not selected_levels:
        selected_levels = ['All_Level']

    Departmentsfilter = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    levelfilters = LavelAdd.objects.filter(IsDelete=False)

    # divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).prefetch_related(
    #     'onrolldepartmentmaster_set__onrolldesignationmaster_set'
    # ).order_by('Order')
    filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    # filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)
    filtered_designations = OnRollDesignationMaster.objects.filter(
        IsDelete=False
    ).annotate(
        level_order=Case(
            When(Lavel='M6', then=1),
            When(Lavel='M5', then=2),
            When(Lavel='M4', then=3),
            When(Lavel='M3', then=4),
            When(Lavel='M2', then=5),
            When(Lavel='M1', then=6),
            When(Lavel='M', then=7),
            When(Lavel='E', then=8),
            When(Lavel='T', then=9),
            When(Lavel='A', then=10),
            default=99,
            output_field=IntegerField()
        )
    ).order_by('level_order', 'Order')

    
    divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
        Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
    )


    employees_per_department_designation = EmployeeWorkDetails.objects.filter(
        OrganizationID=selectedOrganizationID,
        IsDelete=False,
        IsSecondary=False,
        EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"]
    ).annotate(
        level_order=Case(
            When(Level='M6', then=1),
            When(Level='M5', then=2),
            When(Level='M4', then=3),
            When(Level='M3', then=4),
            When(Level='M2', then=5),
            When(Level='M1', then=6),
            When(Level='M', then=7),
            When(Level='E', then=8),
            When(Level='T', then=9),
            When(Level='A', then=10),
            default=99,
            output_field=IntegerField()
        )
    )

    if selected_departments and "All_Department" not in selected_departments:
        employees_per_department_designation = employees_per_department_designation.filter(Department__in=selected_departments)

    if selected_levels and "All_Level" not in selected_levels:
        employees_per_department_designation = employees_per_department_designation.filter(Level__in=selected_levels)

    # employees_per_department_designation = employees_per_department_designation \
    #     .values('Level', 'level_order', 'Department', 'Designation') \
    #     .annotate(
    #         num_employees=Count('id'),
    #         total_salary=Sum('Salary'),
    #         avg_salary=Sum('Salary') / Count('id')
    #     ).order_by('level_order')
    #     # ).order_by('Department', 'level_order', 'Designation')
    
    employees_per_department_designation = (
        employees_per_department_designation
        .values('Level', 'level_order', 'Department', 'Designation')
        .annotate(
            num_employees=Count('id'),
            total_salary=Sum('Salary'),
            avg_salary=Sum('Salary') / Count('id')
        )
        .order_by(
            'level_order',          # MAIN order (THIS FIXES IT)
            'Department',
            'Designation'
        )
    )


    # emp_data = {}
    # for emp in employees_per_department_designation:
    #     dept = emp['Department']
    #     desig = emp['Designation']
    #     if dept not in emp_data:
    #         emp_data[dept] = {}
    #     emp_data[dept][desig] = emp

    context = {
        'memOrg': memOrg,
        'Departmentsfilter': Departmentsfilter,
        'levelfilters': levelfilters,
        'divisions': divisions,
        # 'emp_data': emp_data,
        'rows': employees_per_department_designation,
        'selectedOrganizationID': selectedOrganizationID,
        'OrganizationID': OrganizationID,
        'selected_departments': selected_departments,
        'selected_levels': selected_levels,
    }

    return render(request, "manningguide/ReportMaster/LavelWiseReport.html", context)




from django.shortcuts import redirect, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def LevelWisePdf(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')
    # print("level wise pdf is downnloading")
    
    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  
    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    
    selectedOrganizationID = request.GET.get('hotel_name', OrganizationID)
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={selectedOrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while fetching organization data: {e}")
        memOrg = []

    selectedOrganizationID = request.GET.get('hotel_name', OrganizationID)
    # Fetch selected organization details
    selected_organization = next((org for org in memOrg if str(org['OrganizationID']) == selectedOrganizationID), None)
    selectedOrganizationName = selected_organization['Organization_name'] if selected_organization else "Unknown Organization"
    
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    
    organization = OrganizationMaster.objects.filter(OrganizationID=selectedOrganizationID).first()
    organization_logo = f"{base_url}{organization.OrganizationLogo}" if organization and organization.OrganizationLogo else None

    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

   
    selected_departments = request.GET.getlist('Department')
    selected_levels = request.GET.getlist('Level')

   
    Departmentsfilter = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    levelfilters = LavelAdd.objects.filter(IsDelete=False)
    # divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).prefetch_related(
    #     'onrolldepartmentmaster_set__onrolldesignationmaster_set'
    # ).order_by('Order')
    filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    # filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

    filtered_designations = OnRollDesignationMaster.objects.filter(
        IsDelete=False
    ).annotate(
        level_order=Case(
            When(Lavel='M6', then=1),
            When(Lavel='M5', then=2),
            When(Lavel='M4', then=3),
            When(Lavel='M3', then=4),
            When(Lavel='M2', then=5),
            When(Lavel='M1', then=6),
            When(Lavel='M', then=7),
            When(Lavel='E', then=8),
            When(Lavel='T', then=9),
            When(Lavel='A', then=10),
            default=99,
            output_field=IntegerField()
        )
    ).order_by('level_order', 'Order')

    
    divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).order_by('Order').prefetch_related(
        Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
        Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
    )
    
    employees_per_department_designation = EmployeeWorkDetails.objects.filter(
        OrganizationID=selectedOrganizationID,
        IsDelete=False,
        IsSecondary=False,
        EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"]
    ).annotate(
        level_order=Case(
            When(Level='M6', then=1),
            When(Level='M5', then=2),
            When(Level='M4', then=3),
            When(Level='M3', then=4),
            When(Level='M2', then=5),
            When(Level='M1', then=6),
            When(Level='M', then=7),
            When(Level='E', then=8),
            When(Level='T', then=9),
            When(Level='A', then=10),
            default=99,
            output_field=IntegerField()
        )
    )

    if selected_departments and "All_Department" not in selected_departments:
        employees_per_department_designation = employees_per_department_designation.filter(Department__in=selected_departments)

    if selected_levels and "All_Level" not in selected_levels:
        employees_per_department_designation = employees_per_department_designation.filter(Level__in=selected_levels)

    employees_per_department_designation = employees_per_department_designation \
        .values('Department', 'Designation', 'Level') \
        .annotate(
            num_employees=Count('id'),
            total_salary=Sum('Salary'),
            avg_salary=Sum('Salary') / Count('id')
        ).order_by('Department','level_order', 'Designation')

    emp_data = {}
    for emp in employees_per_department_designation:
        dept = emp['Department']
        desig = emp['Designation']
        if dept not in emp_data:
            emp_data[dept] = {}
        emp_data[dept][desig] = emp

    context = {
        'current_datetime': datetime.now().strftime('%d %B %Y %H:%M:%S'),
        'UserID': UserID,
        'selectedOrganizationID': selectedOrganizationID,
        'selectedOrganizationName': selectedOrganizationName,
        'organization_logo': organization_logo,
        'organization_logos': organization_logos,
        'memOrg': memOrg,
        'Departmentsfilter': Departmentsfilter,
        'levelfilters': levelfilters,
        'divisions': divisions,
        'emp_data': emp_data,
        'selectedOrganizationID': selectedOrganizationID,
        'OrganizationID': OrganizationID,
        'selected_departments': selected_departments,
        'selected_levels': selected_levels,
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'

    template = get_template('manningguide/ReportMaster/LevelWisePdf.html')
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse(f'We had some errors <pre>{html}</pre>')

    return response







from django.shortcuts import render, redirect
from django.db.models import Count, Sum
import requests
import logging

# Configure logger
logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect
from django.db.models import Sum, Count, F, FloatField, ExpressionWrapper
import requests
import logging

# Set up logging
logger = logging.getLogger(__name__)

def DeparmentsWiseReport(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")

    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")


    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
        pass
    else:
        return Error(request, "No Access")  
    
    # Fetch organization data
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    memOrg = []
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while fetching hotel data: {e}")

    
    Departmentsfilter = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    
    # divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).prefetch_related(
    #     'onrolldepartmentmaster_set__onrolldesignationmaster_set'
    # ).order_by('Order')
    filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

    
    divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).prefetch_related(
        Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
        Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
    ).order_by('Order')
    
    selected_department = request.GET.get('Department')

    if not selected_department:
        first_department = Departmentsfilter.first()
        if first_department:
            selected_department = first_department.DepartmentName
    
    employees = EmployeeWorkDetails.objects.filter(IsDelete=False,IsSecondary=False,EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"])
    if selected_department:
        employees = employees.filter(Department=selected_department)

    
    designation_totals_by_hotel = {}
    for hotel in memOrg:
        hotel_name = hotel['Organization_name']
        designation_totals_by_hotel[hotel_name] = {
            'salary': 0,
            'headcount': 0,
            'totalsalarydeta': 0,
            'variance_avg_salary': 0,
            'variance_headcount': 0,
            'variance_totalctc': 0,
        }

    for hotel in memOrg:
        hotel_name = hotel['Organization_name']
        employees_in_hotel = employees.filter(OrganizationID=hotel['OrganizationID'])
        totals = employees_in_hotel.aggregate(
            salary=Sum('Salary'),
            headcount=Count('id'),
        )
        
        totalsalarydeta = (totals['salary'] or 0) * (totals['headcount'] or 0)

        designation_totals_by_hotel[hotel_name].update({
            'salary': totals['salary'] or 0,
            'headcount': totals['headcount'] or 0,
            'totalsalarydeta': totalsalarydeta,
        })
    
    # Collect budget data
    budget_totals_by_hotel = {}
    for hotel in memOrg:
        hotel_name = hotel['Organization_name']
        organization_id = hotel['OrganizationID']
        
        budget_data = ManageBudgetOnRoll.objects.filter(
            on_roll_department_master__DepartmentName=selected_department,
            hotel_name=organization_id
        )
        totals = budget_data.aggregate(
            avg_salary=Sum('avg_salary'),
            head_count=Sum('head_count'),
        )

        budget_totals = {
            'avg_salary': totals['avg_salary'] or 0,
            'head_count': totals['head_count'] or 0,
            'budgetmultiplication_result': (totals['avg_salary'] or 0) * (totals['head_count'] or 0),
        }

        budget_totals_by_hotel[hotel_name] = budget_totals

        # Calculate variances
        if hotel_name in designation_totals_by_hotel:
            designation_totals_by_hotel[hotel_name].update({
                'variance_avg_salary': designation_totals_by_hotel[hotel_name]['salary'] - budget_totals['avg_salary'],
                'variance_headcount': designation_totals_by_hotel[hotel_name]['headcount'] - budget_totals['head_count'],
                'variance_totalctc': designation_totals_by_hotel[hotel_name]['totalsalarydeta'] - budget_totals['budgetmultiplication_result'],
            })

    
   
    context = {
        'Departmentsfilter': Departmentsfilter,
        'divisions': divisions,
        'memOrg': memOrg,
        'selected_department': selected_department,
        'designation_totals_by_hotel': designation_totals_by_hotel,
        'budget_totals_by_hotel':budget_totals_by_hotel
        
    }

    return render(request, "manningguide/ReportMaster/DeparmentsWiseReport.html", context)





from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io
import requests
from django.shortcuts import redirect


import logging

logger = logging.getLogger(__name__)

def DeparmentsWisePdf(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')
    
    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")
    

    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  
    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

    Departmentsfilter = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    
    # divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).prefetch_related(
    #     'onrolldepartmentmaster_set__onrolldesignationmaster_set'
    # ).order_by('Order')

    filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

    
    divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).prefetch_related(
        Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
        Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
    ).order_by('Order')
    selected_department = request.GET.get('Department')
    
    employees = EmployeeWorkDetails.objects.filter(IsDelete=False,IsSecondary=False,EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"])
    if selected_department:
        employees = employees.filter(Department=selected_department)

    
    designation_totals_by_hotel = {}
    for hotel in memOrg:
        hotel_name = hotel['Organization_name']
        designation_totals_by_hotel[hotel_name] = {
            'salary': 0,
            'headcount': 0,
            'totalsalarydeta': 0,
            'variance_avg_salary': 0,
            'variance_headcount': 0,
            'variance_totalctc': 0,
        }

    for hotel in memOrg:
        hotel_name = hotel['Organization_name']
        employees_in_hotel = employees.filter(OrganizationID=hotel['OrganizationID'])
        totals = employees_in_hotel.aggregate(
            salary=Sum('Salary'),
            headcount=Count('id'),
        )
        
        totalsalarydeta = (totals['salary'] or 0) * (totals['headcount'] or 0)

        designation_totals_by_hotel[hotel_name].update({
            'salary': totals['salary'] or 0,
            'headcount': totals['headcount'] or 0,
            'totalsalarydeta': totalsalarydeta,
        })
    
    # Collect budget data
    budget_totals_by_hotel = {}
    for hotel in memOrg:
        hotel_name = hotel['Organization_name']
        organization_id = hotel['OrganizationID']
        
        budget_data = ManageBudgetOnRoll.objects.filter(
            on_roll_department_master__DepartmentName=selected_department,
            hotel_name=organization_id
        )
        totals = budget_data.aggregate(
            avg_salary=Sum('avg_salary'),
            head_count=Sum('head_count'),
        )

        budget_totals = {
            'avg_salary': totals['avg_salary'] or 0,
            'head_count': totals['head_count'] or 0,
            'budgetmultiplication_result': (totals['avg_salary'] or 0) * (totals['head_count'] or 0),
        }

        budget_totals_by_hotel[hotel_name] = budget_totals

        # Calculate variances
        if hotel_name in designation_totals_by_hotel:
            designation_totals_by_hotel[hotel_name].update({
                'variance_avg_salary': designation_totals_by_hotel[hotel_name]['salary'] - budget_totals['avg_salary'],
                'variance_headcount': designation_totals_by_hotel[hotel_name]['headcount'] - budget_totals['head_count'],
                'variance_totalctc': designation_totals_by_hotel[hotel_name]['totalsalarydeta'] - budget_totals['budgetmultiplication_result'],
            })
    
    context = {
        'Departmentsfilter': Departmentsfilter,
        'divisions': divisions,
        'current_datetime': current_datetime,
        'UserID': UserID,
        'memOrg': memOrg,
       
      
       
        'selected_department': selected_department,
        
        'organization_logos': organization_logos,
        'designation_totals_by_hotel': designation_totals_by_hotel,
        'budget_totals_by_hotel':budget_totals_by_hotel
    }

    
    template_path = "manningguide/ReportMaster/DeparmentsWisePdf.html"
    html_string = render_to_string(template_path, context)

    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="departments_wise_report.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')

    return response


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum, Count
import requests
import logging
from io import BytesIO 

logger = logging.getLogger(__name__)

def DesignationWiseReport(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')
    
    OrganizationID = request.session.get("OrganizationID")
    
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    Designationfilter = OnRollDesignationMaster.objects.filter(IsDelete=False)
    # divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).prefetch_related(
    #     'onrolldepartmentmaster_set__onrolldesignationmaster_set'
    # ).order_by('Order')
    filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

    
    divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).prefetch_related(
        Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
        Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
    ).order_by('Order')
    selected_designation = request.GET.get('Designation')
    employees = EmployeeWorkDetails.objects.filter(IsDelete=False,IsSecondary=False,EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"])
    
    
    if not selected_designation:
        first_department = filtered_designations.first()
        if first_department:
            selected_designation = first_department.designations
    if selected_designation:
        employees = employees.filter(Designation=selected_designation)

    # Initialize the dictionary to store totals by hotel
    designation_totals_by_hotel = {}
    for hotel in memOrg:
        hotel_name = hotel['Organization_name']
        designation_totals_by_hotel[hotel_name] = {
            'salary': 0,
            'headcount': 0,
            'totalsalarydeta': 0,
            'variance_avg_salary': 0,
            'variance_headcount': 0,
            'variance_totalctc': 0,
        }

    for hotel in memOrg:
        hotel_name = hotel['Organization_name']
        employees_in_hotel = employees.filter(OrganizationID=hotel['OrganizationID'])
        totals = employees_in_hotel.aggregate(
            salary=Sum('Salary'),
            headcount=Count('id'),
        )
        
        totalsalarydeta = (totals['salary'] or 0) * (totals['headcount'] or 0)

        designation_totals_by_hotel[hotel_name].update({
            'salary': totals['salary'] or 0,
            'headcount': totals['headcount'] or 0,
            'totalsalarydeta': totalsalarydeta,
        })

    # Collect budget data
    budget_totals_by_hotel = {}
    for hotel in memOrg:
        hotel_name = hotel['Organization_name']
        organization_id = hotel['OrganizationID']
        
        budget_data = ManageBudgetOnRoll.objects.filter(
            on_roll_designation_master__designations=selected_designation,
            hotel_name=organization_id
        )
        totals = budget_data.aggregate(
            avg_salary=Sum('avg_salary'),
            head_count=Sum('head_count'),
        )

        budget_totals = {
            'avg_salary': totals['avg_salary'] or 0,
            'head_count': totals['head_count'] or 0,
            'budgetmultiplication_result': (totals['avg_salary'] or 0) * (totals['head_count'] or 0),
        }

        budget_totals_by_hotel[hotel_name] = budget_totals

        # Calculate variances
        if hotel_name in designation_totals_by_hotel:
            designation_totals_by_hotel[hotel_name].update({
                'variance_avg_salary': designation_totals_by_hotel[hotel_name]['salary'] - budget_totals['avg_salary'],
                'variance_headcount': designation_totals_by_hotel[hotel_name]['headcount'] - budget_totals['head_count'],
                'variance_totalctc': designation_totals_by_hotel[hotel_name]['totalsalarydeta'] - budget_totals['budgetmultiplication_result'],
            })

    context = {
        'Designationfilter': Designationfilter,
        'divisions': divisions,
        'memOrg': memOrg,
        'selected_designation': selected_designation,
        'designation_totals_by_hotel': designation_totals_by_hotel,
        'budget_totals_by_hotel': budget_totals_by_hotel,
    }

    return render(request, "manningguide/ReportMaster/DignationsWiseReport.html", context)







def DesignationWiseReportPdf(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')
    
    print("the urls hits: DesignationWiseReportPdf")
    
    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")

    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  
    
    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []
    
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

    Designationfilter = OnRollDesignationMaster.objects.filter(IsDelete=False)
    # divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).prefetch_related(
    #     'onrolldepartmentmaster_set__onrolldesignationmaster_set'
    # ).order_by('Order')
    filtered_departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    filtered_designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

    
    divisions = OnRollDivisionMaster.objects.filter(IsDelete=False).prefetch_related(
        Prefetch('onrolldepartmentmaster_set', queryset=filtered_departments),
        Prefetch('onrolldepartmentmaster_set__onrolldesignationmaster_set', queryset=filtered_designations)
    ).order_by('Order')
    selected_designation = request.GET.get('Designation')
    employees = EmployeeWorkDetails.objects.filter(IsDelete=False,IsSecondary=False,EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"])

    if selected_designation:
        employees = employees.filter(Designation=selected_designation)

    # Initialize the dictionary to store totals by hotel
    designation_totals_by_hotel = {}
    for hotel in memOrg:
        hotel_name = hotel['Organization_name']
        designation_totals_by_hotel[hotel_name] = {
            'salary': 0,
            'headcount': 0,
            'totalsalarydeta': 0,
            'variance_avg_salary': 0,
            'variance_headcount': 0,
            'variance_totalctc': 0,
        }

    for hotel in memOrg:
        hotel_name = hotel['Organization_name']
        employees_in_hotel = employees.filter(OrganizationID=hotel['OrganizationID'])
        totals = employees_in_hotel.aggregate(
            salary=Sum('Salary'),
            headcount=Count('id'),
        )
        
        totalsalarydeta = (totals['salary'] or 0) * (totals['headcount'] or 0)

        designation_totals_by_hotel[hotel_name].update({
            'salary': totals['salary'] or 0,
            'headcount': totals['headcount'] or 0,
            'totalsalarydeta': totalsalarydeta,
        })

    # Collect budget data
    budget_totals_by_hotel = {}
    for hotel in memOrg:
        hotel_name = hotel['Organization_name']
        organization_id = hotel['OrganizationID']
        
        budget_data = ManageBudgetOnRoll.objects.filter(
            on_roll_designation_master__designations=selected_designation,
            hotel_name=organization_id
        )
        totals = budget_data.aggregate(
            avg_salary=Sum('avg_salary'),
            head_count=Sum('head_count'),
        )

        budget_totals = {
            'avg_salary': totals['avg_salary'] or 0,
            'head_count': totals['head_count'] or 0,
            'budgetmultiplication_result': (totals['avg_salary'] or 0) * (totals['head_count'] or 0),
        }

        budget_totals_by_hotel[hotel_name] = budget_totals

        # Calculate variances
        if hotel_name in designation_totals_by_hotel:
            designation_totals_by_hotel[hotel_name].update({
                'variance_avg_salary': designation_totals_by_hotel[hotel_name]['salary'] - budget_totals['avg_salary'],
                'variance_headcount': designation_totals_by_hotel[hotel_name]['headcount'] - budget_totals['head_count'],
                'variance_totalctc': designation_totals_by_hotel[hotel_name]['totalsalarydeta'] - budget_totals['budgetmultiplication_result'],
            })


    context = {
        'current_datetime': current_datetime,
        'UserID': UserID,
        'organization_logos': organization_logos,

        'Designationfilter': Designationfilter,
        'divisions': divisions,
        'memOrg': memOrg,
        'selected_designation': selected_designation,
        'designation_totals_by_hotel': designation_totals_by_hotel,
        'budget_totals_by_hotel': budget_totals_by_hotel,
    }

    template_path = "manningguide/ReportMaster/DignationsWisePdf.html"
    html_string = render_to_string(template_path, context)

    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="dignations_wise_report.pdf"'

    result = BytesIO()
    pisa_status = pisa.CreatePDF(BytesIO(html_string.encode("UTF-8")), dest=result)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')

    response.write(result.getvalue())
    return response




from django.http import JsonResponse
from django.shortcuts import redirect
import json
import requests
import logging


from .filters import apply_filters

logger = logging.getLogger(__name__)

def get_departments(request):
    
    departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    
    
    department_ids_with_data = ManageBudgetOnRoll.objects.filter(
        is_delete=False
    ).values_list('on_roll_department_master_id', flat=True).distinct()
    
   
    departments_with_data = departments.filter(id__in=department_ids_with_data)
    
    
    data = [{'id': department.id, 'label': department.DepartmentName} for department in departments_with_data]
    
    return JsonResponse({'departments': data})

def get_designations(request):
    
    designations = OnRollDesignationMaster.objects.filter(IsDelete=False)
    
    
    designation_ids_with_data = ManageBudgetOnRoll.objects.filter(
        is_delete=False
    ).values_list('on_roll_designation_master_id', flat=True).distinct()
    
    
    designations_with_data = designations.filter(id__in=designation_ids_with_data)
    
    
    data = [{'id': designation.id, 'label': designation.designations} for designation in designations_with_data]
    
    return JsonResponse({'designations': data})


def get_levels(request):
    if request.method == 'GET':
        try:
            
            designation_ids_with_data = ManageBudgetOnRoll.objects.filter(
                is_delete=False
            ).values_list('on_roll_designation_master_id', flat=True).distinct()

            
            levels = OnRollDesignationMaster.objects.filter(
                IsDelete=False, 
                id__in=designation_ids_with_data
            ).values_list('Lavel', flat=True).distinct()

            data = [{'id': level, 'label': level} for level in levels]
            return JsonResponse({'levels': data})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)




def MasterLevelwise(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')
    
    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")


    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  
    
    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    
    selectedOrganizationID = request.GET.get('hotel_name', OrganizationID)
    if UserType == 'CEO' and request.GET.get('hotel_name') is None:
        selectedOrganizationID = 401
    
    budgetonroll = ManageBudgetOnRoll.objects.filter(
        is_delete=False,
        hotel_name=selectedOrganizationID 
    )
    
    context = {
        'memOrg': memOrg,
        'selectedOrganizationID': int(selectedOrganizationID),
        'budgetonroll': budgetonroll  
    }
    return render(request, "manningguide/ReportMaster/MasterLevelwise.html", context)





from django.http import JsonResponse
import json



import json
from django.http import JsonResponse
from .models import ManageBudgetOnRoll

from django.http import JsonResponse
import json
from .models import ManageBudgetOnRoll  

def budget_filter(request):
    if request.method == 'POST' and request.content_type.startswith('application/json'):
        try:
            data = json.loads(request.body)
            hotel_name = data.get('hotel_name')
            filter_criteria = data.get('filters', [])
            
            
            
            if hotel_name is None:
                return JsonResponse({'error': 'hotel_name not provided'}, status=400)
            
            query = ManageBudgetOnRoll.objects.filter(is_delete=False, hotel_name=hotel_name)
            
            query = query.annotate(
                level_order=Case(
                    When(on_roll_designation_master__Lavel='M6', then=1),
                    When(on_roll_designation_master__Lavel='M5', then=2),
                    When(on_roll_designation_master__Lavel='M4', then=3),
                    When(on_roll_designation_master__Lavel='M3', then=4),
                    When(on_roll_designation_master__Lavel='M2', then=5),
                    When(on_roll_designation_master__Lavel='M1', then=6),
                    When(on_roll_designation_master__Lavel='M', then=7),
                    When(on_roll_designation_master__Lavel='E', then=8),
                    When(on_roll_designation_master__Lavel='T', then=9),
                    When(on_roll_designation_master__Lavel='A', then=10),
                    default=99,
                    output_field=IntegerField()
                )
            )

            query = apply_filters(query, filter_criteria)
            query = query.order_by(
                'on_roll_department_master__Order',
                'level_order',
                'on_roll_designation_master__Order'
            )

            project_data = list(query.values(
                'on_roll_department_master__DepartmentName',
                'on_roll_designation_master__designations',
                'on_roll_designation_master__Lavel',
                'avg_salary',
                'head_count',
                'total_ctc',
            ))

            return JsonResponse({'projects': project_data})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method or content type'}, status=400)



def get_departmentsActual(request):
    
    departments = OnRollDepartmentMaster.objects.filter(IsDelete=False)
    
    
    department_names_with_employees = EmployeeWorkDetails.objects.filter(
        IsDelete=False,IsSecondary=False,EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"]
    ).values_list('Department', flat=True).distinct()
    
    
    filtered_departments = departments.filter(DepartmentName__in=department_names_with_employees)

    
    data = [{'id': department.DepartmentName, 'label': department.DepartmentName} for department in filtered_departments]
    
    return JsonResponse({'departments': data})

def get_designationsActual(request):
    
    designations = OnRollDesignationMaster.objects.filter(IsDelete=False)
    
    
    designations_with_employees = EmployeeWorkDetails.objects.filter(
        IsDelete=False,IsSecondary=False,EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"]
    ).values_list('Designation', flat=True).distinct()
    
    
    filtered_designations = designations.filter(designations__in=designations_with_employees)

   
    data = [{'id': designation.designations, 'label': designation.designations} for designation in filtered_designations]
    
    return JsonResponse({'designations': data})


import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from datetime import datetime
import logging

logger = logging.getLogger(__name__)



logger = logging.getLogger(__name__)

def budget_master_pdf(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')
    
    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")

    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  
    
    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []
    
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')

    selectedOrganizationID = request.GET.get('hotel_name', OrganizationID)
    filters = request.GET.get('filters', '[]')

    try:
        filter_criteria = json.loads(filters)
    except json.JSONDecodeError:
        filter_criteria = []

    selected_organization = next((org for org in memOrg if str(org['OrganizationID']) == selectedOrganizationID), None)
    selectedOrganizationName = selected_organization['Organization_name'] if selected_organization else "Unknown Organization"
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    
    organization = OrganizationMaster.objects.filter(OrganizationID=selectedOrganizationID).first()
    organization_logo = f"{base_url}{organization.OrganizationLogo}" if organization and organization.OrganizationLogo else None

    
    query = ManageBudgetOnRoll.objects.filter(is_delete=False, hotel_name=selectedOrganizationID)
            
    query = query.annotate(
        level_order=Case(
            When(on_roll_designation_master__Lavel='M6', then=1),
            When(on_roll_designation_master__Lavel='M5', then=2),
            When(on_roll_designation_master__Lavel='M4', then=3),
            When(on_roll_designation_master__Lavel='M3', then=4),
            When(on_roll_designation_master__Lavel='M2', then=5),
            When(on_roll_designation_master__Lavel='M1', then=6),
            When(on_roll_designation_master__Lavel='M', then=7),
            When(on_roll_designation_master__Lavel='E', then=8),
            When(on_roll_designation_master__Lavel='T', then=9),
            When(on_roll_designation_master__Lavel='A', then=10),
            default=99,
            output_field=IntegerField()
        )
    )
            
    query = apply_filters(query, filter_criteria)
    query = query.order_by(
        'on_roll_department_master__Order',
        'level_order',
        'on_roll_designation_master__Order'
    )
    
    project_data = list(query.values(
        'on_roll_department_master__DepartmentName',
        'on_roll_designation_master__designations',
        'on_roll_designation_master__Lavel',
        'avg_salary',
        'head_count',
        'total_ctc',
    ))

    context = {
        'selectedOrganizationID': selectedOrganizationID,
        'current_datetime': current_datetime,
        'UserID': UserID,
        'organization_logos': organization_logos,
        'organization_logo': organization_logo,
        'selectedOrganizationName': selectedOrganizationName,
        'project_data': project_data,
    }

    template_path = "manningguide/ReportMaster/BudgetMasterPdf.html"
    html_string = render_to_string(template_path, context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="BudgetMasterReport.pdf"'

    result = BytesIO()
    pisa_status = pisa.CreatePDF(BytesIO(html_string.encode("UTF-8")), dest=result)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')

    response.write(result.getvalue())
    return response




from django.shortcuts import render, redirect
import requests
import logging

logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect
import requests
import logging


logger = logging.getLogger(__name__)


from django.http import JsonResponse















from django.shortcuts import render, redirect
import requests
import logging

logger = logging.getLogger(__name__)

def ActualMasterReport(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")

    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    selectedOrganizationID = request.GET.get('hotel_name', OrganizationID)
    if UserType == 'CEO' and request.GET.get('hotel_name') is None:
            selectedOrganizationID = 401

    actualdata = EmployeeWorkDetails.objects.filter(
        OrganizationID=selectedOrganizationID,IsDelete=False,IsSecondary=False,EmpStatus__in=["On Probation", "Confirmed", "Not Confirmed"]
    )
   

    context = {
        'memOrg': memOrg,
        'selectedOrganizationID': selectedOrganizationID,
        'actualdata': actualdata  
    }

    return render(request, "manningguide/ReportMaster/ActualMasterReport.html", context)






import json
from django.http import JsonResponse
  
from django.db.models import Count, Sum, Avg
import logging

logger = logging.getLogger(__name__)










@csrf_exempt
def Actualdata_filter(request):
    logger.info('Request received with method: %s', request.method)
    
    if request.method == 'POST' and request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
            logger.info('Data received: %s', data)
            organization_id = data.get('hotel_name')
            filters = data.get('filters', {})

            if not organization_id:
                return JsonResponse({'error': 'hotel_name not provided'}, status=400)
            
            statuses = ['On Probation', 'Not Confirmed', 'Confirmed']

            # query = EmployeeWorkDetails.objects.filter(
            # OrganizationID=organization_id,
            # EmpStatus__in=statuses,IsDelete=False,IsSecondary=False,
            # )
    
            
            # query = query.exclude(
            #     Q(Department__isnull=True) | Q(Department='') |
            #     Q(Designation__isnull=True) | Q(Designation='')
            # )
            
            query = EmployeeWorkDetails.objects.filter(
                OrganizationID=organization_id,
                EmpStatus__in=statuses,
                IsDelete=False,
                IsSecondary=False,
            ).exclude(
                Q(Department__isnull=True) | Q(Department='') |
                Q(Designation__isnull=True) | Q(Designation='')
            ).annotate(
                level_order=Case(
                    When(Level='M6', then=1),
                    When(Level='M5', then=2),
                    When(Level='M4', then=3),
                    When(Level='M3', then=4),
                    When(Level='M2', then=5),
                    When(Level='M1', then=6),
                    When(Level='M', then=7),
                    When(Level='E', then=8),
                    When(Level='T', then=9),
                    When(Level='A', then=10),
                    default=99,
                    output_field=IntegerField()
                )
            )

            aggregated_data = query.values(
                'Department',
                'Designation',
                'Level',
                'level_order'
            ).annotate(
                emp_count=Count('id'),
                total_salary=Sum('Salary'),
                avg_salary=Avg('Salary')
            ).order_by('Department', 'level_order', 'Designation')
            
            projects = apply_filters(aggregated_data, filters)

            projects = list(projects)
            logger.info('Projects fetched: %s', projects)
            return JsonResponse({'projects': projects})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            logger.error('Exception occurred: %s', str(e))
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method or content type'}, status=400)


from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
import json
from datetime import datetime

def Actualdatapdf(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserID = request.session.get("UserID")

    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  
    
    hotelapitoken = MasterAttribute.HotelAPIkeyToken  
    headers = {'hotel-api-token': hotelapitoken}
    api_url = f"http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID={OrganizationID}"

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred: {e}")
        memOrg = []

    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    selectedOrganizationID = request.GET.get('hotel_name', OrganizationID)
    filters = request.GET.get('filters', '[]')

    try:
        filter_criteria = json.loads(filters)
    except json.JSONDecodeError:
        filter_criteria = []

    selected_organization = next((org for org in memOrg if str(org['OrganizationID']) == selectedOrganizationID), None)
    selectedOrganizationName = selected_organization['Organization_name'] if selected_organization else "Unknown Organization"
    
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None


    organization = OrganizationMaster.objects.filter(OrganizationID=selectedOrganizationID).first()
    organization_logo = f"{base_url}{organization.OrganizationLogo}" if organization and organization.OrganizationLogo else None

    statuses = ['On Probation', 'Not Confirmed', 'Confirmed']

    # query = EmployeeWorkDetails.objects.filter(
    #     OrganizationID=selectedOrganizationID,
    #     EmpStatus__in=statuses,IsDelete=False,IsSecondary=False,
    # )

    # query = query.exclude(
    #     Q(Department__isnull=True) | Q(Department='') |
    #     Q(Designation__isnull=True) | Q(Designation='')
    # )

    # aggregated_data = query.values(
    #     'Department',
    #     'Designation',
    #     'Level'
    # ).annotate(
    #     emp_count=Count('id'),
    #     total_salary=Sum('Salary'),
    #     avg_salary=Avg('Salary')
    # ).order_by('Department', 'Designation')
    

    query = EmployeeWorkDetails.objects.filter(
        OrganizationID=selectedOrganizationID,
        EmpStatus__in=statuses,
        IsDelete=False,
        IsSecondary=False,
    ).exclude(
        Q(Department__isnull=True) | Q(Department='') |
        Q(Designation__isnull=True) | Q(Designation='')
    ).annotate(
        level_order=Case(
            When(Level='M6', then=1),
            When(Level='M5', then=2),
            When(Level='M4', then=3),
            When(Level='M3', then=4),
            When(Level='M2', then=5),
            When(Level='M1', then=6),
            When(Level='M', then=7),
            When(Level='E', then=8),
            When(Level='T', then=9),
            When(Level='A', then=10),
            default=99,
            output_field=IntegerField()
        )
    )

    aggregated_data = query.values(
        'Department',
        'Designation',
        'Level',
        'level_order'
    ).annotate(
        emp_count=Count('id'),
        total_salary=Sum('Salary'),
        avg_salary=Avg('Salary')
    ).order_by('Department', 'level_order', 'Designation')
    
    
    projects = apply_filters(aggregated_data, filter_criteria)
    projects = list(projects)

    context = {
        'selectedOrganizationID': selectedOrganizationID,
        'current_datetime': current_datetime,
        'UserID': UserID,
        'organization_logo': organization_logo,
        'organization_logos':organization_logos,
        'selectedOrganizationName': selectedOrganizationName,
        'projects': projects,
    }

    template_path = "manningguide/ReportMaster/Actualdatapdf.html"
    html_string = render_to_string(template_path, context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ActualMasterReport.pdf"'

    result = BytesIO()
    pisa_status = pisa.CreatePDF(BytesIO(html_string.encode("UTF-8")), dest=result)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')

    response.write(result.getvalue())
    return response




from django.db.models import Sum

from django.db.models import Sum



def degntioncount(request):
    
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

   
    hotel_label_mapping = OrganizationMaster.objects.filter(
        IsDelete=False, Activation_status=1
    ).exclude(
        OrganizationID__in=[3, 1,2050]  
    ).values('OrganizationID', 'ShortDisplayLabel')

    hotel_label_dict = {str(item['OrganizationID']): item['ShortDisplayLabel'] for item in hotel_label_mapping}

    # Get Divisions
    Divisions = OnRollDivisionMaster.objects.all()

    selected_division = request.GET.get('DivisionName')

    # Get Designations based on selected division
    if selected_division:
        division_instance = OnRollDivisionMaster.objects.filter(DivisionName=selected_division).first()
        if division_instance:
            Designations = OnRollDesignationMaster.objects.filter(
                managebudgetonroll__on_roll_division_master=division_instance,
                managebudgetonroll__is_delete=False
            ).distinct()
        else:
            Designations = OnRollDesignationMaster.objects.none()
    else:
        Designations = OnRollDesignationMaster.objects.all()

    # Get head count data
    if selected_division:
        head_count_data = ManageBudgetOnRoll.objects.filter(
            is_delete=False,
            on_roll_division_master=division_instance
        ).values(
            'on_roll_designation_master__designations', 'hotel_name'
        ).annotate(total_head_count=Sum('head_count'))
    else:
        head_count_data = ManageBudgetOnRoll.objects.filter(
            is_delete=False
        ).values(
            'on_roll_designation_master__designations', 'hotel_name'
        ).annotate(total_head_count=Sum('head_count'))

    # Initialize head count dictionary and total head count
    head_count_dict = {}
    total_head_count_all_designations = {}  # Store total headcount for each hotel

    for item in head_count_data:
        designation = item['on_roll_designation_master__designations']
        hotel_name = item['hotel_name']
        total_head_count = item['total_head_count']

        # Get hotel short label
        short_label = hotel_label_dict.get(hotel_name, "Unknown")

        # Initialize dictionary for each designation if it doesn't exist
        if designation not in head_count_dict:
            head_count_dict[designation] = {}

        # Store head count for each hotel and designation
        head_count_dict[designation][short_label] = total_head_count

        # Calculate total head count for all designations for each hotel
        if short_label not in total_head_count_all_designations:
            total_head_count_all_designations[short_label] = 0

       # Ensure total_head_count_all_designations[short_label] is initialized to 0 if it's None
        # Ensure total_head_count_all_designations[short_label] is initialized to 0 if it's None
        total_head_count_all_designations[short_label] = total_head_count_all_designations.get(short_label, 0)

        # Ensure total_head_count is not None, if it is, initialize it to 0
        if total_head_count is None:
            total_head_count = 0

        # Now safely perform the addition
        total_head_count_all_designations[short_label] += total_head_count


    context = {
        'Designations': Designations,
        'Divisions': Divisions,
        'ShortDisplayLabels': hotel_label_dict.values(),
        'head_count_dict': head_count_dict,
        'total_head_count_all_designations': total_head_count_all_designations,
        'selected_division': selected_division,  
    }

    return render(request, "manningguide/ReportMaster/Degantion.html", context)






from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.db.models import Sum
from urllib.parse import unquote

def degntioncountPdf(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    hotel_label_mapping = OrganizationMaster.objects.filter(
        IsDelete=False, Activation_status=1
    ).exclude(
        OrganizationID__in=[3, 1,2050]  
    ).values('OrganizationID', 'ShortDisplayLabel')

    hotel_label_dict = {str(item['OrganizationID']): item['ShortDisplayLabel'] for item in hotel_label_mapping}
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
    # Get Divisions
    Divisions = OnRollDivisionMaster.objects.all()

    
    selected_division = request.GET.get('DivisionName')
    print("DivisionName = ",selected_division)

    # Get Designations based on selected division
    if selected_division:
        division_instance = OnRollDivisionMaster.objects.filter(DivisionName=selected_division).first()
        if division_instance:
            Designations = OnRollDesignationMaster.objects.filter(
                managebudgetonroll__on_roll_division_master=division_instance,
                managebudgetonroll__is_delete=False
            ).distinct()
        else:
            Designations = OnRollDesignationMaster.objects.none()
    else:
        Designations = OnRollDesignationMaster.objects.all()

    # Get head count data
    if selected_division:
        head_count_data = ManageBudgetOnRoll.objects.filter(
            is_delete=False,
            on_roll_division_master=division_instance
        ).values(
            'on_roll_designation_master__designations', 'hotel_name'
        ).annotate(total_head_count=Sum('head_count'))
    else:
        head_count_data = ManageBudgetOnRoll.objects.filter(
            is_delete=False
        ).values(
            'on_roll_designation_master__designations', 'hotel_name'
        ).annotate(total_head_count=Sum('head_count'))

    # Initialize head count dictionary and total head count
    head_count_dict = {}
    total_head_count_all_designations = {}  # Store total headcount for each hotel

    for item in head_count_data:
        designation = item['on_roll_designation_master__designations']
        hotel_name = item['hotel_name']
        total_head_count = item['total_head_count']

        # Get hotel short label
        short_label = hotel_label_dict.get(hotel_name, "Unknown")

        # Initialize dictionary for each designation if it doesn't exist
        if designation not in head_count_dict:
            head_count_dict[designation] = {}

        # Store head count for each hotel and designation
        head_count_dict[designation][short_label] = total_head_count

        # Calculate total head count for all designations for each hotel
        if short_label not in total_head_count_all_designations:
            total_head_count_all_designations[short_label] = 0

        # Initialize the value if it's None
       

        total_head_count_all_designations[short_label] = total_head_count_all_designations.get(short_label, 0)

        # Ensure total_head_count is not None, if it is, initialize it to 0
        if total_head_count is None:
            total_head_count = 0

        # Now safely perform the addition
        total_head_count_all_designations[short_label] += total_head_count


    
    context = {
        'Designations': Designations,
        'Divisions': Divisions,
        'ShortDisplayLabels': hotel_label_dict.values(),
        'head_count_dict': head_count_dict,
        'total_head_count_all_designations': total_head_count_all_designations,
        'selected_division': selected_division,
        'organization_logos':organization_logos,
        'current_datetime':current_datetime
    }

    # Generate the HTML content from the template
    template_path = 'manningguide/ReportMaster/BudgetHeadCountpdf.html'  # Same HTML template
    html = render_to_string(template_path, context)

    # Prepare the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="DesignationHeadcountReport.pdf"'

    # Create the PDF from HTML
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Check if there was an error during PDF generation
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=400)

    return response











def BudgetsalaryDesignation(request):
    
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    # Map hotel labels, excluding OrganizationID 3 and 1
    hotel_label_mapping = OrganizationMaster.objects.filter(
        IsDelete=False, Activation_status=1
    ).exclude(
        OrganizationID__in=[3, 1, 2050]  
    ).values('OrganizationID', 'ShortDisplayLabel')

    hotel_label_dict = {str(item['OrganizationID']): item['ShortDisplayLabel'] for item in hotel_label_mapping}

    # Get Divisions
    Divisions = OnRollDivisionMaster.objects.all()

    selected_division = request.GET.get('DivisionName')

    # Get Designations based on selected division
    if selected_division:
        division_instance = OnRollDivisionMaster.objects.filter(DivisionName=selected_division).first()
        if division_instance:
            Designations = OnRollDesignationMaster.objects.filter(
                managebudgetonroll__on_roll_division_master=division_instance,
                managebudgetonroll__is_delete=False
            ).distinct()
        else:
            Designations = OnRollDesignationMaster.objects.none()
    else:
        Designations = OnRollDesignationMaster.objects.all()

    # Get total CTC data instead of head count
    if selected_division:
        ctc_data = ManageBudgetOnRoll.objects.filter(
            is_delete=False,
            on_roll_division_master=division_instance
        ).values(
            'on_roll_designation_master__designations', 'hotel_name'
        ).annotate(total_ctc=Sum('total_ctc'))
    else:
        ctc_data = ManageBudgetOnRoll.objects.filter(
            is_delete=False
        ).values(
            'on_roll_designation_master__designations', 'hotel_name'
        ).annotate(total_ctc=Sum('total_ctc'))

    # Initialize dictionaries for storing CTC data
    ctc_dict = {}
    total_ctc_all_designations = {}  # Store total CTC for each hotel

    for item in ctc_data:
        designation = item['on_roll_designation_master__designations']
        hotel_name = item['hotel_name']
        total_ctc = item['total_ctc']

        # Get hotel short label
        short_label = hotel_label_dict.get(hotel_name, "Unknown")

        # Initialize dictionary for each designation if it doesn't exist
        if designation not in ctc_dict:
            ctc_dict[designation] = {}

        # Store CTC for each hotel and designation
        ctc_dict[designation][short_label] = total_ctc

        # Calculate total CTC for all designations for each hotel
        if short_label not in total_ctc_all_designations:
            total_ctc_all_designations[short_label] = 0

        total_ctc_all_designations[short_label] += total_ctc

    context = {
        'Designations': Designations,
        'Divisions': Divisions,
        'ShortDisplayLabels': hotel_label_dict.values(),
        'ctc_dict': ctc_dict,  # Updated to include ctc_dict instead of head_count_dict
        'total_ctc_all_designations': total_ctc_all_designations,
        'selected_division': selected_division,  
    }

    return render(request, "manningguide/ReportMaster/BudgetsalaryDesignation.html", context)

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa  # For xhtml2pdf
# from weasyprint import HTML  # For WeasyPrint (optional)

def BudgetsalaryDesignationPDF(request):
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    # Fetch the same data as in BudgetsalaryDesignation
    hotel_label_mapping = OrganizationMaster.objects.filter(
        IsDelete=False, Activation_status=1
    ).exclude(
        OrganizationID__in=[3, 1, 2050]
    ).values('OrganizationID', 'ShortDisplayLabel')

    hotel_label_dict = {str(item['OrganizationID']): item['ShortDisplayLabel'] for item in hotel_label_mapping}
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
    Divisions = OnRollDivisionMaster.objects.all()
    selected_division = request.GET.get('DivisionName')

    if selected_division:
        division_instance = OnRollDivisionMaster.objects.filter(DivisionName=selected_division).first()
        if division_instance:
            Designations = OnRollDesignationMaster.objects.filter(
                managebudgetonroll__on_roll_division_master=division_instance,
                managebudgetonroll__is_delete=False
            ).distinct()
        else:
            Designations = OnRollDesignationMaster.objects.none()
    else:
        Designations = OnRollDesignationMaster.objects.all()

    if selected_division:
        ctc_data = ManageBudgetOnRoll.objects.filter(
            is_delete=False,
            on_roll_division_master=division_instance
        ).values(
            'on_roll_designation_master__designations', 'hotel_name'
        ).annotate(total_ctc=Sum('total_ctc'))
    else:
        ctc_data = ManageBudgetOnRoll.objects.filter(
            is_delete=False
        ).values(
            'on_roll_designation_master__designations', 'hotel_name'
        ).annotate(total_ctc=Sum('total_ctc'))

    ctc_dict = {}
    total_ctc_all_designations = {}

    for item in ctc_data:
        designation = item['on_roll_designation_master__designations']
        hotel_name = item['hotel_name']
        total_ctc = item['total_ctc']
        short_label = hotel_label_dict.get(hotel_name, "Unknown")

        if designation not in ctc_dict:
            ctc_dict[designation] = {}

        ctc_dict[designation][short_label] = total_ctc

        if short_label not in total_ctc_all_designations:
            total_ctc_all_designations[short_label] = 0

        total_ctc_all_designations[short_label] += total_ctc

    context = {
        'Designations': Designations,
        'Divisions': Divisions,
        'ShortDisplayLabels': hotel_label_dict.values(),
        'ctc_dict': ctc_dict,
        'total_ctc_all_designations': total_ctc_all_designations,
        'selected_division': selected_division,
        'organization_logos':organization_logos,
        'current_datetime':current_datetime
    }

    
    
    template_path = 'manningguide/ReportMaster/BudgetsalaryDesignationPDF.html'
    html = render_to_string(template_path, context)

   
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="BudgetsalaryDesignation.pdf"'

    
    pisa_status = pisa.CreatePDF(html, dest=response)

   

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response



from django.db.models import Count
from django.db.models import FloatField
from django.db.models.functions import Cast

from django.db.models import Count, Q, F, FloatField, Sum
from django.db.models.functions import Cast

def ActualHeadCountDesignation(request):
    
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    
    hotel_label_mapping = OrganizationMaster.objects.filter(
        IsDelete=False, Activation_status=1
    ).exclude(
        OrganizationID__in=[1,2050]
    ).values('OrganizationID', 'ShortDisplayLabel')

    hotel_label_dict = {str(item['OrganizationID']): item['ShortDisplayLabel'] for item in hotel_label_mapping}

    Divisions = OnRollDivisionMaster.objects.filter(IsDelete=False)
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

    selected_division = request.GET.get('DivisionName')
    selected_department = request.GET.get('DepartmentName')

    if selected_division:
        division_instance = OnRollDivisionMaster.objects.filter(DivisionName=selected_division).first()
        if division_instance:
            departments = OnRollDepartmentMaster.objects.filter(
                OnRollDivisionMaster=division_instance,
                IsDelete=False
            )
            Designations = OnRollDesignationMaster.objects.filter(
                OnRollDepartmentMaster__in=departments,
                IsDelete=False
            ).distinct()

   
    head_count_filter = {'IsDelete': False,'IsSecondary':False}
    if selected_division and Designations.exists():
        designation_names = Designations.values_list('designations', flat=True)
        head_count_filter['Designation__in'] = designation_names

    head_count_data = EmployeeWorkDetails.objects.filter(**head_count_filter).values(
        'Designation', 'OrganizationID'
    ).annotate(
        num_employees=Count('id'),
        total_salary=Sum(
            Cast('Salary', FloatField()), 
            filter=Q(Salary__isnull=False, Salary__gt=0)
        )
    )

    head_count_dict = {}
    total_head_count_all_designations = {}

    for item in head_count_data:
        designation = item['Designation']
        try:
            hotel_id = str(item['OrganizationID'])   
        except ValueError:
            hotel_id = None  
        
        num_employees = item['num_employees']

        if hotel_id is not None:
            short_label = hotel_label_dict.get(hotel_id, "Unknown")
            
            if designation not in head_count_dict:
                head_count_dict[designation] = {}
            head_count_dict[designation][short_label] = num_employees

            total_head_count_all_designations[short_label] = (
                total_head_count_all_designations.get(short_label, 0) + num_employees
            )

    context = {
        'Designations': Designations,
        'Divisions': Divisions,
        'ShortDisplayLabels': hotel_label_dict.values(),
        'head_count_dict': head_count_dict,
        'total_head_count_all_designations': total_head_count_all_designations,
        'selected_division': selected_division,
        'selected_department': selected_department,
    }

    return render(request, "manningguide/ReportMaster/ActualHeadCount.html", context)





from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa

def ActualHeadCountDesignationPDF(request):
    
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

   
    hotel_label_mapping = OrganizationMaster.objects.filter(
        IsDelete=False, Activation_status=1
    ).exclude(
        OrganizationID__in=[1,2050]
    ).values('OrganizationID', 'ShortDisplayLabel')

    hotel_label_dict = {str(item['OrganizationID']): item['ShortDisplayLabel'] for item in hotel_label_mapping}
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
    Divisions = OnRollDivisionMaster.objects.filter(IsDelete=False)
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

    selected_division = request.GET.get('DivisionName')
    selected_department = request.GET.get('DepartmentName')

    
    if selected_division:
        division_instance = OnRollDivisionMaster.objects.filter(DivisionName=selected_division).first()
        if division_instance:
            departments = OnRollDepartmentMaster.objects.filter(
                OnRollDivisionMaster=division_instance,
                IsDelete=False
            )
            Designations = OnRollDesignationMaster.objects.filter(
                OnRollDepartmentMaster__in=departments,
                IsDelete=False
            ).distinct()

    
    head_count_filter = {'IsDelete': False,'IsSecondary':False}
    if selected_division and Designations.exists():
        designation_names = Designations.values_list('designations', flat=True)
        head_count_filter['Designation__in'] = designation_names

    head_count_data = EmployeeWorkDetails.objects.filter(**head_count_filter).values(
        'Designation', 'OrganizationID'
    ).annotate(
        num_employees=Count('id'),
        total_salary=Sum(
            Cast('Salary', FloatField()), 
            filter=Q(Salary__isnull=False, Salary__gt=0)
        )
    )

    head_count_dict = {}
    total_head_count_all_designations = {}

    for item in head_count_data:
        designation = item['Designation']
        try:
            hotel_id = str(item['OrganizationID'])  
        except ValueError:
            hotel_id = None  
        
        num_employees = item['num_employees']

        if hotel_id is not None:
            short_label = hotel_label_dict.get(hotel_id, "Unknown")
            
            if designation not in head_count_dict:
                head_count_dict[designation] = {}
            head_count_dict[designation][short_label] = num_employees

            total_head_count_all_designations[short_label] = (
                total_head_count_all_designations.get(short_label, 0) + num_employees
            )

    context = {
        'Designations': Designations,
        'Divisions': Divisions,
        'ShortDisplayLabels': hotel_label_dict.values(),
        'head_count_dict': head_count_dict,
        'total_head_count_all_designations': total_head_count_all_designations,
        'selected_division': selected_division,
        'selected_department': selected_department,
        'organization_logos':organization_logos,
        'current_datetime':current_datetime
    }

    
    template_path = 'manningguide/ReportMaster/ActualHeadCountPDF.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ActualHeadCount.pdf"'

    html = render_to_string(template_path, context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=400)
    
    return response




from django.db.models import Count, Q, F, FloatField, Sum
from django.db.models.functions import Cast

def ActualsalaryDesignation(request):
    # Ensure session has OrganizationID
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    # Get mapping of hotels and short display labels
    hotel_label_mapping = OrganizationMaster.objects.filter(
        IsDelete=False, Activation_status=1
    ).exclude(
        OrganizationID__in=[1,2050]
    ).values('OrganizationID', 'ShortDisplayLabel')

    hotel_label_dict = {str(item['OrganizationID']): item['ShortDisplayLabel'] for item in hotel_label_mapping}

    Divisions = OnRollDivisionMaster.objects.filter(IsDelete=False)
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

    selected_division = request.GET.get('DivisionName')
    selected_department = request.GET.get('DepartmentName')

    # Filter designations based on selected division and department
    if selected_division:
        division_instance = OnRollDivisionMaster.objects.filter(DivisionName=selected_division).first()
        if division_instance:
            departments = OnRollDepartmentMaster.objects.filter(
                OnRollDivisionMaster=division_instance,
                IsDelete=False
            )
            Designations = OnRollDesignationMaster.objects.filter(
                OnRollDepartmentMaster__in=departments,
                IsDelete=False
            ).distinct()

    # Filter EmployeeWorkDetails based on the Designation
    salary_filter = {'IsDelete': False,'IsSecondary':False}
    if selected_division and Designations.exists():
        designation_names = Designations.values_list('designations', flat=True)
        salary_filter['Designation__in'] = designation_names

    salary_data = EmployeeWorkDetails.objects.filter(**salary_filter).values(
        'Designation', 'OrganizationID'
    ).annotate(
        total_salary=Sum(
            Cast('Salary', FloatField()), 
            filter=Q(Salary__isnull=False, Salary__gt=0)
        )
    )

    salary_dict = {}
    total_salary_all_designations = {}

    for item in salary_data:
        designation = item['Designation']
        try:
            hotel_id = str(item['OrganizationID'])  # Ensure hotel_id is string for dictionary keys
        except ValueError:
            hotel_id = None  # Handle non-numeric values appropriately

        total_salary = item['total_salary'] or 0

        if hotel_id is not None:
            short_label = hotel_label_dict.get(hotel_id, "Unknown")

            if designation not in salary_dict:
                salary_dict[designation] = {}
            salary_dict[designation][short_label] = total_salary

            total_salary_all_designations[short_label] = (
                total_salary_all_designations.get(short_label, 0) + total_salary
            )

    context = {
        'Designations': Designations,
        'Divisions': Divisions,
        'ShortDisplayLabels': hotel_label_dict.values(),
        'salary_dict': salary_dict,
        'total_salary_all_designations': total_salary_all_designations,
        'selected_division': selected_division,
        'selected_department': selected_department,
    }

    return render(request, "manningguide/ReportMaster/ActualsalaryDesignationdata.html", context)


from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.db.models import Sum, Q
from django.db.models.functions import Cast
from django.db.models import FloatField

def ActualsalaryDesignationPdf(request):
    
    if 'OrganizationID' not in request.session:
        return redirect('MasterAttribute.Host')

    OrganizationID = request.session.get("OrganizationID")
    UserType = request.session.get("UserType") 
    Department_Name = request.session.get("Department_Name")
    if OrganizationID == '3' or   UserType == 'GM' or Department_Name == 'HR'  :
            pass
    else:
           return Error(request, "No Access")  

    
    hotel_label_mapping = OrganizationMaster.objects.filter(
        IsDelete=False, Activation_status=1
    ).exclude(
        OrganizationID__in=[1,2050]
    ).values('OrganizationID', 'ShortDisplayLabel')
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')
    hotel_label_dict = {str(item['OrganizationID']): item['ShortDisplayLabel'] for item in hotel_label_mapping}
    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
    Divisions = OnRollDivisionMaster.objects.filter(IsDelete=False)
    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False)

    selected_division = request.GET.get('DivisionName')
    selected_department = request.GET.get('DepartmentName')

   
    if selected_division:
        division_instance = OnRollDivisionMaster.objects.filter(DivisionName=selected_division).first()
        if division_instance:
            departments = OnRollDepartmentMaster.objects.filter(
                OnRollDivisionMaster=division_instance,
                IsDelete=False
            )
            Designations = OnRollDesignationMaster.objects.filter(
                OnRollDepartmentMaster__in=departments,
                IsDelete=False
            ).distinct()

    
    salary_filter = {'IsDelete': False,'IsSecondary':False}
    if selected_division and Designations.exists():
        designation_names = Designations.values_list('designations', flat=True)
        salary_filter['Designation__in'] = designation_names

    salary_data = EmployeeWorkDetails.objects.filter(**salary_filter).values(
        'Designation', 'OrganizationID'
    ).annotate(
        total_salary=Sum(
            Cast('Salary', FloatField()), 
            filter=Q(Salary__isnull=False, Salary__gt=0)
        )
    )

    salary_dict = {}
    total_salary_all_designations = {}

   
    for item in salary_data:
        designation = item['Designation']
        try:
            hotel_id = str(item['OrganizationID'])  
        except ValueError:
            hotel_id = None 

        total_salary = item['total_salary'] or 0

        if hotel_id is not None:
            short_label = hotel_label_dict.get(hotel_id, "Unknown")

           
            if designation not in salary_dict:
                salary_dict[designation] = {}
            salary_dict[designation][short_label] = total_salary

            
            total_salary_all_designations[short_label] = (
                total_salary_all_designations.get(short_label, 0) + total_salary
            )

    
    context = {
        'Designations': Designations,
        'Divisions': Divisions,
        'ShortDisplayLabels': hotel_label_dict.values(),
        'salary_dict': salary_dict,
        'total_salary_all_designations': total_salary_all_designations,
        'selected_division': selected_division,
        'selected_department': selected_department,
        'organization_logos':organization_logos,
        'current_datetime':current_datetime
    }

   
    template_path = 'manningguide/ReportMaster/ActualsalaryDesignationpdf.html'
    html = render_to_string(template_path, context)
    
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="ActualSalaryDesignationReport.pdf"'

   
    pisa_status = pisa.CreatePDF(html, dest=response)

    
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=400)
    
    return response





def variance_details_report_experiment(request):
    context = {}
    # return render("variance_details_report_experiment.html", context)
    return render(request, "manningguide/VarianceReport/variance_details_report_experiment.html",context)
