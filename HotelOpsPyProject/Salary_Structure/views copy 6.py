from django.shortcuts import render, redirect
# from HumanResources.views import SalaryTitle_Master, PT_Config
from HumanResources.models import SalaryTitle_Master, PT_Config, Salary_Detail_Master

# Create your views here.
def salary_structure(request):
    Session_Org_ID = request.session["OrganizationID"]
    org_id = request.GET.get("OID")

    if not org_id:
        org_id = Session_Org_ID

    print("OrganizationID in Salary Structure:", org_id, Session_Org_ID)

    context = {
        'org_id':org_id
    }
    return render(request, 'Salary_Structure/Salary_Structure.html', context)





def Handle_SalaryStructure(request):
    if request.method == 'POST':
        display_names = request.POST.getlist('DisplayName[]')
        salary_types = request.POST.getlist('SalaryType[]')
        basis_types = request.POST.getlist('Calculation_Basis_Type[]')
        # categories = request.POST.getlist('Category[]')
        formulas = request.POST.getlist('Formula_Expression[]')
        row_ids = request.POST.getlist('RowID[]')  # may be shorter
        SalaryCode = request.POST.getlist('Salary_Code[]')  # may be shorter
        Org_id = request.POST.getlist('Orgid[]')  # may be shorter
        selected_Orgid = request.POST.getlist('selected_Orgid')  # may be shorter

        # typeorder = 1
        # titleorder = 1

        while len(row_ids) < len(display_names):
            row_ids.append("")

        typeorder_cache = {}
        titleorder_cache = {}

        for i in range(len(display_names)):
            row_id = row_ids[i]

            # Map category
            category_map = {
                'A': 'Earnings',
                'B': 'Deductions',
                'C': 'Contribution',
                'D': 'Total',
            }
            category = category_map.get(salary_types[i], 'Other')


            if row_id:  
                obj = SalaryTitle_Master.objects.get(id=row_id)
                obj.Display_Names = display_names[i]
                obj.Type = salary_types[i]
                obj.Calculation_Basis_Type = basis_types[i]
                obj.Category = category 
                obj.Formula_Expression = formulas[i]
                obj.Salary_Code = SalaryCode[i]
                obj.save()
            else: 
                stype = salary_types[i]

                if stype not in typeorder_cache:
                    last_obj = SalaryTitle_Master.objects.filter(Type=stype, IsDelete=0).order_by('-TypeOrder').first()
                    last_title = SalaryTitle_Master.objects.filter(Type=stype, IsDelete=0).order_by('-TitleOrder').first()
                    
                    typeorder_cache[stype] = last_obj.TypeOrder if last_obj else 0
                    titleorder_cache[stype] = last_title.TitleOrder if last_title else 0

                # Increment for this new row
                # typeorder_cache[stype]
                titleorder_cache[stype] += 1

                print("Inserting new row with TypeOrder:", typeorder_cache[stype], "TitleOrder:", titleorder_cache[stype])

                SalaryTitle_Master.objects.create(
                    # TypeOrder=typeorder,
                    # TitleOrder=titleorder,
                    TypeOrder=typeorder_cache[stype],
                    TitleOrder=titleorder_cache[stype],
                    Salary_Code = SalaryCode[i],
                    Display_Names=display_names[i],
                    Type=salary_types[i],
                    Calculation_Basis_Type=basis_types[i],
                    Category=category,
                    Formula_Expression=formulas[i],
                    IsDelete=False,
                    HotelID=Org_id[i]
                )
        
        if selected_Orgid:
            url = f"{reverse('salary_structure')}?OID={selected_Orgid[0]}"
            return redirect(url)
        else:
            return redirect("salary_structure")

    return redirect('salary_structure')




from django.utils import timezone

# def Handle_PT_Configration(request):
#     if request.method == 'POST':
#         Type = request.POST.get('PT_Type')
#         Last_Month = request.POST.get('PT_Last_Month')  
#         Last_Month_Value = request.POST.get('PT_Last_Month_Value')

#         gender = request.POST.getlist('PT_Gender[]')  
#         Salary_From = request.POST.getlist('PT_Salary_From[]') 
#         Salary_To = request.POST.getlist('PT_Salary_To[]') 
#         PT_Amount = request.POST.getlist('PT_Amount[]')  

#         # PT_objs = PT_Config.objects.filter(IsDelete=False)

#         PT_Config.objects.create(
#             Type = Type,
#             Hotel_ID = 0,
#             Gender = '',
#             Salary_From = 0,
#             Salary_To = 0,
#             PT_Amount = 0,
#             Last_Month = 1,    
#             Last_Month_Value = 1,
#             IsActive = True,
#             OrganizationID = 0,
#             CreatedBy = 123,
#             ModifyBy = 123,
#             CreatedDateTime = timezone.now(),
#             ModifyDateTime = timezone.now(),
#             IsDelete = False
#         )
#     else:
#         print("form is not reached here")

#         return redirect('salary_structure')

#     return redirect('salary_structure')

# from django.utils import timezone
# from .models import PT_Config

# def Handle_PT_Configration(request):
#     Orgid = '3'
#     if request.method == 'POST':
#         Type = request.POST.get('PT_Type')
#         Last_Month = request.POST.get('PT_Last_Month')  
#         Last_Month_Value = request.POST.get('PT_Last_Month_Value')

#         genders = request.POST.getlist('PT_Gender[]')  
#         salaries_from = request.POST.getlist('PT_Salary_From[]') 
#         salaries_to = request.POST.getlist('PT_Salary_To[]') 
#         pt_amounts = request.POST.getlist('PT_Amount[]')  

#         # loop over each row
#         for i in range(len(genders)):
#             PT_Config.objects.create(
#                 Type=Type,
#                 Hotel_ID=0,   # you can set dynamically
#                 Gender=genders[i],
#                 Salary_From=salaries_from[i] if salaries_from[i] else 0,
#                 Salary_To=salaries_to[i] if salaries_to[i] else 0,
#                 PT_Amount=pt_amounts[i] if pt_amounts[i] else 0,
#                 Last_Month=Last_Month,
#                 Last_Month_Value=Last_Month_Value,
#                 IsActive=True,
#                 OrganizationID=0,   # set if available
#                 CreatedBy=123,
#                 ModifyBy=123,
#                 CreatedDateTime=timezone.now(),
#                 ModifyDateTime=timezone.now(),
#                 IsDelete=False
#             )

#         # url = reverse('salary_structure', args=[Orgid])
#         # return redirect('salary_structure', args=[Orgid])
#         return redirect('salary_structure')
#     else:
#         print("form is not reached here")
#         return redirect('salary_structure')

from django.utils import timezone
# from .models import PT_Config

def Handle_PT_Configration(request):
    Session_Org_ID = request.session["OrganizationID"]
    UserID = request.session["UserID"]
    org_id = request.GET.get("OID")

    if request.method == 'POST':
        Type = request.POST.get('PT_Type')
        Last_Month = request.POST.get('PT_Last_Month')  
        Last_Month_Value = request.POST.get('PT_Last_Month_Value')
        OrganizationID = request.POST.get('SelectedOrg')  # comes from hidden field

        # Lists from form
        genders = request.POST.getlist('PT_Gender[]')  
        salaries_from = request.POST.getlist('PT_Salary_From[]') 
        salaries_to = request.POST.getlist('PT_Salary_To[]') 
        pt_amounts = request.POST.getlist('PT_Amount[]')  

        # Loop row by row (zip keeps them aligned)
        for s_from, s_to, amount, g in zip(salaries_from, salaries_to, pt_amounts, genders):
            # Skip completely empty rows
            if not (s_from or s_to or amount):
                continue

            PT_Config.objects.create(
                Type=Type,
                Hotel_ID=OrganizationID,
                Gender=g,
                Salary_From=s_from if s_from else 0,
                Salary_To=s_to if s_to else 0,
                PT_Amount=amount if amount else 0,
                Last_Month=Last_Month if Last_Month else 0,
                Last_Month_Value=Last_Month_Value if Last_Month_Value else 0,
                IsActive=True,
                OrganizationID=Session_Org_ID if Session_Org_ID else 0,
                CreatedBy= UserID if UserID else 0,
                ModifyBy= UserID if UserID else 0,
                CreatedDateTime=timezone.now(),
                ModifyDateTime=timezone.now(),
                IsDelete=False
            )

        return redirect('salary_structure')
    else:
        return redirect('salary_structure')


# def Handle_PT_Configration(request):
#     if request.method == 'POST':
#         Type = request.POST.get('PT_Type')
#         Last_Month = request.POST.get('PT_Last_Month')  
#         Last_Month_Value = request.POST.get('PT_Last_Month_Value')

#         gender = request.POST.getlist('PT_Gender[]')  
#         Salary_From = request.POST.getlist('PT_Salary_From[]') 
#         Salary_To = request.POST.getlist('PT_Salary_To[]') 
#         PT_Amount = request.POST.getlist('PT_Amount[]')  

#         # PT_objs = PT_Config.objects.filter(IsDelete=False)

#         PT_Config.objects.create(
#             Type = Type,
#             hotelID = 0,
#             gender = '',
#             Salary_From = 0,
#             Salary_To = 0,
#             PT_Amount = 0,
#             Last_Month = Last_Month,    
#             Last_Month_Value = Last_Month_Value,
#             isActive = True,
#             OrganizationID = 0,
#             CreatedBy = request.user.id if request.user.is_authenticated else None,
#             ModifyBy = request.user.id if request.user.is_authenticated else None,
#             CreatedDateTime = timezone.now(),
#             ModifyDateTime = timezone.now(),
#             IsDelete = False
#         )

#         # print("form data:", request.POST)   
#         print("form Type:", Type)
#         print("Form Gender:", gender)
#         print("Form Last_Month:", Last_Month)
#         print("Form Last_Month_Value:", Last_Month_Value)   
#         print("Form Salary_From:", Salary_From)
#         print("Form Salary_To:", Salary_To)
#         print("Form PT_Amount:", PT_Amount)
#         print("form is reached here")
#     else:
#         print("form is not reached here")

#         return redirect('salary_structure')

#     return redirect('salary_structure')



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

# def calculate_salary_from_inputs(input_values, organization_id, hotel_id):
#     """
#     Calculate salary using SalaryTitle_Master formulas + user inputs.
#     input_values = dict of manually entered values (Basic, Conveyance, etc.)
#     """

#     # 1. Load salary structure for org/hotel
#     salary_titles = SalaryTitle_Master.objects.filter(
#         # OrganizationID=organization_id,
#         # HotelID=hotel_id,
#         IsDelete=False
#     ).order_by("TypeOrder", "TitleOrder")

#     # 2. Start with provided inputs
#     values = input_values.copy()
#     aeval = Interpreter()
#     results = {}

#     # 3. Loop through salary titles in order
#     for st in salary_titles:
#         code = st.Salary_Code
#         formula = st.Formula_Expression

#         if not code:
#             continue

#         if formula:
#             # Put current known values into evaluator
#             for k, v in values.items():
#                 aeval.symtable[k] = v

#             try:
#                 results[code] = aeval(formula)
#             except Exception:
#                 results[code] = 0
#         else:
#             # If no formula, pick from input values (default 0)
#             results[code] = values.get(code, 0)

#         # Update dictionary for later formulas
#         aeval.symtable[code] = results[code]
#         values[code] = results[code]

#     # 4. Calculate per annum as well
#     per_annum = {k: round(v * 12, 2) for k, v in results.items()}

#     return {
#         "per_month": results,
#         "per_annum": per_annum
#     }





from asteval import Interpreter

def salary_Calc(request):
    SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=False).order_by('TypeOrder', 'TitleOrder')
    # SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=TitleOrder).order_by(TitleOrderTypeOrder', 'TitleOrder')

    context = {
        'SalaryTitles': SalaryTitles
    }
    return render(request, 'Salary_Structure/Salary_Calc.html', context)


# def Salary_Calc_Ready(request):
#     SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=False).order_by('TypeOrder', 'TitleOrder')
#     # SalaryTitles = SalaryTitle_Master.objects.filter(IsDelete=TitleOrder).order_by(TitleOrderTypeOrder', 'TitleOrder')

#     context = {
#         'SalaryTitles': SalaryTitles
#     }
#     return render(request, 'Salary_Structure/Salary_Calc_Ready.html', context)


from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.urls import reverse

def Salary_Calc_Ready(request, Orgid):
    Session_Org_ID = request.session["OrganizationID"]
    # org_id = request.GET.get("OID")


    EmpID = 6321
    if not Orgid:
        Orgid = Session_Org_ID

    if not Orgid and not EmpID:
        print("please first provide neccessory details like Empid and orgid")

    # salary_titles = SalaryTitle_Master.objects.filter(OrganizationID=Orgid, IsDelete=False).order_by('TypeOrder', 'TitleOrder')   
    SalaryTitles  = SalaryTitle_Master.objects.filter(IsDelete=False, HotelID=OID).order_by('TypeOrder','TitleOrder')

    salary_details = Salary_Detail_Master.objects.filter(
        IsDelete=False,
        EmpID=EmpID,
        OrganizationID=OID
    ).values('Salary_title_id', 'Permonth', 'Perannum')


    salary_map = {s['Salary_title_id']: s for s in salary_details}

    for salary in SalaryTitles:
        detail = salary_map.get(salary.id)
        if detail:
            salary.Permonth = detail['Permonth']
            salary.Perannum = detail['Perannum']
        else:
            salary.Permonth = 0
            salary.Perannum = 0

    employee_input = {}
    results_dict = {}

    if request.method == "POST":
        per_month = request.POST.getlist("PerMonth")
        per_annum = request.POST.getlist("PerAnnum")
        row_ids   = request.POST.getlist("RowID[]")

        for i in range(0, len(row_ids), 2):
            salary_code = row_ids[i+1]
            index = i // 2
            per_annum_val = per_annum[index].strip() if index < len(per_annum) else ""
            per_month_val = per_month[index].strip() if index < len(per_month) else ""

            try:
                value = float(per_month_val) if per_month_val else 0
                # value = float(per_annum_val) if per_annum_val else float(per_month_val or 0)
            except ValueError:
                value = 0
            employee_input[salary_code] = value

        results_dict.update(calculate_salary(employee_input, Orgid=Orgid))

        # 👇 store values temporarily in session if needed
        request.session["employee_input"] = employee_input
        request.session["results_dict"] = results_dict

        # 👇 redirect instead of render
        # return redirect(reverse("Salary_Calc_Ready"))
        # if selected_Orgid:
        url = reverse('Salary_Calc_Ready', args=[Orgid])
        return redirect(url)
        # else:
        #     return redirect("Salary_Calc_Ready")

    # 👇 retrieve from session if available
    employee_input = request.session.pop("employee_input", {})
    results_dict = request.session.pop("results_dict", {})

    merged_data = []
    for item in salary_titles:
        code = item.Salary_Code
        merged_data.append({
            "id": item.id,
            "Display_Names": item.Display_Names,
            "TypeOrder": item.TypeOrder,
            "TitleOrder": item.TitleOrder,
            "Type": item.Type,
            "Salary_Code": code,
            "Calculation_Basis_Type": item.Calculation_Basis_Type,
            "Category": item.Category,
            "Formula_Expression": item.Formula_Expression,
            "Entered_Value": employee_input.get(code, 0),
            "Calculated_Value": results_dict.get(code, 0),  # from calc engine
            "PerAnnum_Value": results_dict.get(code, 0) * 12 if code in results_dict else 0
        })

    # return JsonResponse({"data": list(merged_data)})
    # return JsonResponse(list(merged_data), safe=False)
    return render(request, "Salary_Structure/Salary_Calc_Ready.html", {
        "SalaryTitles": merged_data
    })



def calculate_salary(employee_input, Orgid):
    # from asteval import Interpreter

    aeval = Interpreter()

    for code, value in employee_input.items():
        aeval.symtable[code] = value
        print("User Inputs:", code, value)

    results = {}

    salary_components = (
        SalaryTitle_Master.objects
        .filter(IsDelete=0, HotelID=Orgid)
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
def SalaryStructureAPI(request, Orgid):
    print("Orgid in API:", Orgid)
    try:
        salary_titles = SalaryTitle_Master.objects.filter(IsDelete=False, HotelID=Orgid).order_by('TypeOrder', 'TitleOrder')

        # SalaryCodes = salary_titles.values_list('Salary_Code', flat=True).distinct()
        SalaryCodes = list(salary_titles.values_list('Salary_Code', flat=True).distinct())
        # print("SalaryCode:", SalaryCodes)
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
                "orgid":Orgid if Orgid else 0
                # "Salary_Code": item.Salary_Code,
            }
            for item in salary_titles
        ]

        return Response({
            "salary_codes": SalaryCodes, 
            "salary_structure": data       
        }, status=rest_status.HTTP_200_OK)

        # return Response(data, status=rest_status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=rest_status.HTTP_500_INTERNAL_SERVER_ERROR)
