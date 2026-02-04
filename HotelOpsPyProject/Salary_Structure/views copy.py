from django.shortcuts import render, redirect
from HumanResources.views import SalaryTitle_Master

# Create your views here.
def salary_structure(request):
    SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=False).order_by('TypeOrder', 'TitleOrder')
    # SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=TitleOrder).order_by(TitleOrderTypeOrder', 'TitleOrder')

    context = {
        'SalaryTitles': SalaryTitles
    }

    return render(request, 'Salary_Structure/Salary_Structure.html', context)

def salary_Calc(request):
    SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=False).order_by('TypeOrder', 'TitleOrder')
    # SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=TitleOrder).order_by(TitleOrderTypeOrder', 'TitleOrder')

    context = {
        'SalaryTitles': SalaryTitles
    }

    return render(request, 'Salary_Structure/Salary_Calc.html', context)





# def Handle_SalaryStructure(request):
#     if request.method == 'POST':
#         display_names = request.POST.getlist('DisplayName[]')
#         salary_types = request.POST.getlist('SalaryType[]')
#         basis_types = request.POST.getlist('Calculation_Basis_Type[]')
#         categories = request.POST.getlist('Category[]')
#         formulas = request.POST.getlist('Formula_Expression[]')
#         row_ids = request.POST.getlist('RowID[]') if 'RowID[]' in request.POST else []  # optional hidden field

#         for i in range(len(display_names)):
#             if row_ids and row_ids[i]:
#                 obj = SalaryTitle_Master.objects.get(id=row_ids[i])
#                 obj.Display_Names = display_names[i]
#                 obj.Type = salary_types[i]
#                 obj.Calculation_Basis_Type = basis_types[i]
#                 obj.Category = categories[i]
#                 obj.Formula_Expression = formulas[i]
#                 obj.save()
#             else:
#                 SalaryTitle_Master.objects.create(
#                     Display_Names=display_names[i],
#                     Type=salary_types[i],
#                     Calculation_Basis_Type=basis_types[i],
#                     Category=categories[i],
#                     Formula_Expression=formulas[i],
#                     IsDelete=False  
#                 )

#         return redirect('salary_structure')

#     return redirect('salary_structure')


def Handle_SalaryStructure(request):
    if request.method == 'POST':
        display_names = request.POST.getlist('DisplayName[]')
        salary_types = request.POST.getlist('SalaryType[]')
        basis_types = request.POST.getlist('Calculation_Basis_Type[]')
        categories = request.POST.getlist('Category[]')
        formulas = request.POST.getlist('Formula_Expression[]')
        row_ids = request.POST.getlist('RowID[]')  # may be shorter
        SalaryCode = request.POST.getlist('Salary_Code[]')  # may be shorter

        typeorder = 1
        titleorder = 1

        while len(row_ids) < len(display_names):
            row_ids.append("")

        for i in range(len(display_names)):
            row_id = row_ids[i]

            if row_id:  
                obj = SalaryTitle_Master.objects.get(id=row_id)
                obj.Display_Names = display_names[i]
                obj.Type = salary_types[i]
                obj.Calculation_Basis_Type = basis_types[i]
                obj.Category = categories[i]
                obj.Formula_Expression = formulas[i]
                obj.Salary_Code = SalaryCode[i]
                obj.save()
            else: 
                SalaryTitle_Master.objects.create(
                    TypeOrder=typeorder,
                    TitleOrder=titleorder,
                    Salary_Code = SalaryCode[i],
                    Display_Names=display_names[i],
                    Type=salary_types[i],
                    Calculation_Basis_Type=basis_types[i],
                    Category=categories[i],
                    Formula_Expression=formulas[i],
                    IsDelete=False
                )

        return redirect('salary_structure')

    return redirect('salary_structure')





def Handle_PT_Configration(request):
    if request.method == 'POST':
        Type = request.POST.get('PT_Type')
        State = request.POST.get('PT_State')
        gender = request.POST.get('PT_Gender')
        Last_Month = request.POST.get('PT_Last_Month')  
        Last_Month_Value = request.POST.get('PT_Last_Month_Value')
        Salary_From = request.POST.get('PT_Salary_From')
        Salary_To = request.POST.get('PT_Salary_To')
        PT_Amount = request.POST.get('PT_Amount')   
        print("form data:", request.POST)   
        print("form data:", Type, State)
        print("form is reached here")
    else:
        print("form is not reached here")

        return redirect('salary_structure')

    return redirect('salary_structure')



def Delete_Salary_Structure(request, id):
    # SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=False).order_by('TypeOrder', 'TitleOrder')
    print("ElementID:", id)
    print("Delete_Salary_Structure is reached here")
    try:
        salary_title = SalaryTitle_Master.objects.get(id=id)
        salary_title.IsDelete = True
        salary_title.save() 
    except SalaryTitle_Master.DoesNotExist:
        print(f"SalaryTitle with id {id} does not exist.")
    
    return redirect('salary_structure')









from asteval import Interpreter
# from .models import SalaryTitle_Master

def calculate_salary_from_inputs(input_values, organization_id, hotel_id):
    """
    Calculate salary using SalaryTitle_Master formulas + user inputs.
    input_values = dict of manually entered values (Basic, Conveyance, etc.)
    """

    # 1. Load salary structure for org/hotel
    salary_titles = SalaryTitle_Master.objects.filter(
        # OrganizationID=organization_id,
        # HotelID=hotel_id,
        IsDelete=False
    ).order_by("TypeOrder", "TitleOrder")

    # 2. Start with provided inputs
    values = input_values.copy()
    aeval = Interpreter()
    results = {}

    # 3. Loop through salary titles in order
    for st in salary_titles:
        code = st.Salary_Code
        formula = st.Formula_Expression

        if not code:
            continue

        if formula:
            # Put current known values into evaluator
            for k, v in values.items():
                aeval.symtable[k] = v

            try:
                results[code] = aeval(formula)
            except Exception:
                results[code] = 0
        else:
            # If no formula, pick from input values (default 0)
            results[code] = values.get(code, 0)

        # Update dictionary for later formulas
        aeval.symtable[code] = results[code]
        values[code] = results[code]

    # 4. Calculate per annum as well
    per_annum = {k: round(v * 12, 2) for k, v in results.items()}

    return {
        "per_month": results,
        "per_annum": per_annum
    }

















#  ----------------------------- API's ----------------------

from app.models import OrganizationMaster
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status as rest_status

@api_view(['GET'])
# def OrganizationList(request, user_orgid, session_Orgid):
def OrganizationList(request, user_orgid, session_Orgid):
    # OrganizationID = request.session["OrganizationID"]
    # user_orgid = '3'
    # session_Orgid = '3'

    if session_Orgid == '3':
        orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1)
    else:
        orgs = OrganizationMaster.objects.filter(IsDelete=False, Activation_status=1, OrganizationID=user_orgid)
    
    if orgs.exists():
        orgs = orgs.values('id', 'OrganizationName', 'OrganizationID')
    else:
        orgs = []   

    return Response(orgs, status=rest_status.HTTP_200_OK)

    # return render(request, 'Salary_Structure/OrganizationList.html', {})



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status as rest_status
# from .models import SalaryTitle_Master

@api_view(['GET'])
def SalaryStructureAPI(request):
    try:
        salary_titles = SalaryTitle_Master.objects.filter(IsDelete=False).order_by('TypeOrder', 'TitleOrder')
        data = [
            {
                "id": item.id,
                "Display_Names": item.Display_Names,
                "TypeOrder": item.TypeOrder,
                "TitleOrder": item.TitleOrder,
                "Type": item.Type,
                "Salary_Code": item.Salary_Code,
                "Calculation_Basis_Type": item.Calculation_Basis_Type,
                "Category": item.Category,
                "Formula_Expression": item.Formula_Expression,
            }
            for item in salary_titles
        ]
        return Response(data, status=rest_status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
