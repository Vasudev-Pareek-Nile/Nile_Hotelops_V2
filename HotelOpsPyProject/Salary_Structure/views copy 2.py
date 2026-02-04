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







# -------------------------------- Trial Code ----------------------------

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





from asteval import Interpreter

# def calculate_salary(employee_input):
#     aeval = Interpreter()

#     # First, load user entered values
#     for code, value in employee_input.items():
#         print("-------------------------------------------------------------------------------")
#         print("User Inputs:", code, value)
#         print("-------------------------------------------------------------------------------")

#         aeval.symtable[code] = value

#     results = {}

#     # Now loop through components & evaluate formula if present
#     salary_components = SalaryTitle_Master.objects.filter(IsDelete=0).order_by("TitleOrder")

#     for comp in salary_components:
#         code = comp.Salary_Code
#         formula = comp.Formula_Expression

#         print("Formula Check:", code, " ----- ", formula)

#         if formula and formula.lower() != "none":
#             try:
#                 value = aeval(formula)
#                 aeval.symtable[code] = value  # store for future dependencies
#             except Exception as e:
#                 value = 0
#         else:
#             # take from user input if provided
#             value = employee_input.get(code, 0)

#         results[code] = value

#     return results
#     # return JsonResponse({"results": results})

def calculate_salary(employee_input):
    # from asteval import Interpreter

    aeval = Interpreter()

    for code, value in employee_input.items():
        aeval.symtable[code] = value
        print("User Inputs:", code, value)

    results = {}

    salary_components = (
        SalaryTitle_Master.objects
        .filter(IsDelete=0)
        .order_by("TypeOrder", "TitleOrder")
    )

    for comp in salary_components:
        code = (comp.Salary_Code or "").strip()
        formula_Rep = (comp.Formula_Expression or "")
        formula = formula_Rep.replace("x", "*").replace("÷", "/")
        print("Evaluating:", code, " with formula: ", formula)

        if not formula or formula.strip() == "" or formula.strip().lower() == "none":
            value = employee_input.get(code, 0)
        else:
            try:
                value = aeval(formula.strip())
                if value is None:
                    value = employee_input.get(code, 0)
            except Exception:
                value = employee_input.get(code, 0)

        results[code] = value
        aeval.symtable[code] = value  

    return results







#  Calculate Salary Structure from user inputs ------------


def salary_Calc(request):
    SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=False).order_by('TypeOrder', 'TitleOrder')
    # SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=TitleOrder).order_by(TitleOrderTypeOrder', 'TitleOrder')

    context = {
        'SalaryTitles': SalaryTitles
    }
    return render(request, 'Salary_Structure/Salary_Calc.html', context)


from django.http import JsonResponse
# def salary_Calc_post_value(request):
#     if request.method == "POST":
#         per_month_values = request.POST.getlist("PerMonth")
#         row_ids = request.POST.getlist("RowID[]")  # contains [id, Salary_Code, id, Salary_Code...]

#         employee_input = {}

#         # loop through RowID[] in pairs
#         for i in range(0, len(row_ids), 2):
#             salary_code = row_ids[i+1]  # second element is Salary_Code
#             per_month = per_month_values[i // 2]   # match same index
#             if per_month:  # only add if user entered something
#                 employee_input[salary_code] = float(per_month)

#         print("Final Employee Input:", employee_input)

#         # call your calculation engine
#         salary = calculate_salary(employee_input)
#         print("Calculated Salary:", salary)

#         return JsonResponse({"employee_input": employee_input, "salary": salary})




# def salary_Calc_post_value(request):
#     SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=False).order_by('TypeOrder', 'TitleOrder')
#     # SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=TitleOrder).order_by(TitleOrderTypeOrder', 'TitleOrder')
#     print("salary_Calc_post_value is reached here")
#     print("form data:", request.POST)

#     context = {
#         # 'SalaryTitles': SalaryTitles
#     }
#     return render(request, 'Salary_Structure/Salary_Calc.html', context)

def salary_Calc_post_value(request):
    if request.method == "POST":
        print("form data:", request.POST)

        per_annum = request.POST.getlist("PerAnnum")
        per_month = request.POST.getlist("PerMonth")
        row_ids   = request.POST.getlist("RowID[]")   # comes in [id, code, id, code...]

        employee_input = {}

        # iterate in steps of 2 (id, code)
        for i in range(0, len(row_ids), 2):
            salary_id = row_ids[i]          # DB id (not needed, but available)
            salary_code = row_ids[i+1]      # "Basic", "HRA", etc

            # match index for PerAnnum & PerMonth
            index = i // 2
            per_annum_val = per_annum[index].strip() if index < len(per_annum) else ""
            per_month_val = per_month[index].strip() if index < len(per_month) else ""

            # choose PerAnnum first, else fallback to PerMonth
            value = 0
            if per_annum_val.isdigit():
                value = int(per_annum_val)
            elif per_month_val.isdigit():
                value = int(per_month_val)

            employee_input[salary_code] = value

            print("employee_input:", employee_input)


            results = calculate_salary(employee_input)  # Call your calculation engine here

        # return render(request, "Salary_Structure/Salary_Calc.html", {"employee_input": employee_input})
        return JsonResponse({"results": results})
        # return employee_input
    

@api_view(['GET'])
def SalaryStructureAPI_Calculations(request):
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
