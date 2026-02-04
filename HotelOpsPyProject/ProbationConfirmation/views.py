from django.shortcuts import render,redirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute,OrganizationDetail
from django.db import   transaction
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Emp_Confirmation_Master,Emp_Confirmation_Details,Category_Master,Item_Master,Confirm_Date,Emp_Confirmation_Objective_Details, Emp_Confirmation_Objective_Goals
from HumanResources.views import EmployeeDetailsData
from django.db.models import Subquery, OuterRef
  
import requests
from hotelopsmgmtpy.utils import encrypt_id,decrypt_id
from django.urls import reverse
from LetterOfConfirmation.models import LETTEROFCONFIRMATIONEmployeeDetail
def ListPC(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    UserType = request.session.get("UserType") 
     
    OrganizationID = request.session["OrganizationID"]
    UserID = str(request.session["UserID"])
    
    hotelapitoken = MasterAttribute.HotelAPIkeyToken
    headers = {
        'hotel-api-token': hotelapitoken  # Replace with your actual header key and value
    }
    api_url = "http://hotelops.in/API/PyAPI/OrganizationListSelect?OrganizationID=" + str(OrganizationID)
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Optional: Check for any HTTP errors
        memOrg = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")   
    I = request.GET.get('I',OrganizationID)
    if UserType == 'CEO' and request.GET.get('I') is None:
        I = 401
    emp_id_subquery = Subquery(
        EmployeePersonalDetails.objects.filter(
            EmployeeCode=OuterRef('EmpCode'),
            IsDelete=False
        ).values('EmpID')[:1]
    )

   
    Emp_objs = Emp_Confirmation_Master.objects.filter(OrganizationID = OrganizationID,IsDelete=False).annotate(
        EmpID=emp_id_subquery)
    for emp in Emp_objs:
          Cnf_Filename = None
          if emp.LOC_ID:
               Cnf_Filenameobj =  LETTEROFCONFIRMATIONEmployeeDetail.objects.filter(OrganizationID=OrganizationID, IsDelete=False,id=emp.LOC_ID).first()
               if Cnf_Filenameobj:
                    Cnf_Filename = Cnf_Filenameobj.file_name
          emp.Cnf_Filename = Cnf_Filename
          emp.save()
    
    context = {'Emp_objs':Emp_objs,'UserID':UserID,'I':I,'memOrg':memOrg}
    return render(request, 'ProbationConfirmation/List.html',context)

   
from app.views import Error   
from HumanResources.models import EmployeeWorkDetails,EmployeePersonalDetails
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
@transaction.atomic()
def NewPC(request): 
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
     
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID


    UserID = str(request.session["UserID"])
    hotelapitoken = MasterAttribute.HotelAPIkeyToken 
    
    
    EmpCode  = request.GET.get('EC')
    EmpID  = request.GET.get('EmpID')

    if EmpID == '':
        EmpIDobj =  EmployeePersonalDetails.objects.filter(OrganizationID=OrganizationID,IsDelete=False,EmployeeCode=EmpCode).first()
        EmpID = EmpIDobj.EmpID
    if EmpID == 'None' or EmpID == '':
            return Error(request, "Employee is not Found in Human Resources Data.")
        
    Page  = request.GET.get('Page')

    ID  = request.GET.get('ID')

    Month  = 6
    confirm_period = Confirm_Date.objects.filter(OrganizationID=OrganizationID, IsDelete=False).order_by('-CreatedDateTime').first()
    
    
    Categories  = Category_Master.objects.filter(IsDelete=False)
    for m in Categories:
        item= Item_Master.objects.filter(IsDelete=False,Category=m)
        m.items = item
    
    Emp_obj = None
    objectives_data = []
    if EmpCode is not None:
        if ID is not None:
            Emp_obj = Emp_Confirmation_Master.objects.filter(id=ID,IsDelete=False).first()
            for m in Categories:
                item= Item_Master.objects.filter(IsDelete=False,Category=m)
                m.items = item
                for it in item:
                    dt = Emp_Confirmation_Details.objects.filter(IsDelete=False,Emp_Confirmation_Master=Emp_obj,Item_Master__Category = m,Item_Master=it)
                    it.emp_detail = dt

            objectives = Emp_Confirmation_Objective_Details.objects.filter(Emp_Confirmation_Master_id=ID,IsDelete=False,OrganizationID = OrganizationID)
            objectives_data = []

            for objective in objectives:
                goals = Emp_Confirmation_Objective_Goals.objects.filter(Emp_Confirmation_Objective_Details=objective,IsDelete=False,OrganizationID = OrganizationID)
                goals_data = [{'id': goal.id, 'name': goal.GoalName} for goal in goals]
                objectives_data.append({
                    'id': objective.id,
                    'name': objective.ObjectiveName,
                    'goals': goals_data
                })
        if Emp_obj is not None:
            DataFromEmp_obj  = 'Emp_obj'
           

        else:
            

            DataFromEmp_obj  = 'Emp_objHR'
            EmpDetails  = EmployeeDetailsData(EmpID,OrganizationID)
          
          
         

            Emp_obj  =   {
                                'EmpCode' : EmpDetails.EmployeeCode,
                               'EmpName': " ".join(filter(None, [EmpDetails.FirstName, EmpDetails.MiddleName, EmpDetails.LastName])),
                               
                                'Department' : EmpDetails.Department,
                                'Position' : EmpDetails.Designation,
                                'JoiningDate':EmpDetails.DateofJoining
                                
                               }

   
            if confirm_period:
                confirmation_date = EmpDetails.DateofJoining + relativedelta(months=int(confirm_period.Month))
                
                Emp_obj['ConfDate'] = confirmation_date
            else:
                confirmation_date = EmpDetails.DateofJoining + relativedelta(months=int(Month))
                
                Emp_obj['ConfDate'] = confirmation_date




    with transaction.atomic():
        if request.method == "POST":
                                           
            if DataFromEmp_obj == "Emp_obj" and ID:
                Emp_obj.EmpCode = request.POST['EmpCode'] or ''
                Emp_obj.EmpName = request.POST['EmpName'] or ''
                Emp_obj.Position = request.POST['Position'] or ''
                Emp_obj.Department = request.POST['Department'] or ''
                Emp_obj.JoiningDate =  request.POST['JoiningDate']
                Emp_obj.ConfDate =  request.POST['ConfDate'] or ''
                Emp_obj.Strengths =  request.POST['Strengths'] or ''
                Emp_obj.Improvement = request.POST['Improvement'] or ''
                Emp_obj.Trainingattended  = request.POST['Trainingattended'] or ''

                EmpCon = request.POST.get('EmpCon') 
                Exten = request.POST.get('Exten') 
                Guide = request.POST.get('Guide') 
                ConfDate = request.POST['ConfDate']
                
                EmpConfirm = False
                if EmpCon == "Yes":
                    EmpConfirm = True




                Extended = ''
               
                if EmpCon == "Extended":
                    Extended = Exten
                    if ConfDate:
                       
                        ExtendedMonth = int(Exten.split()[0]) 
                        ConfDate = datetime.strptime(ConfDate, '%Y-%m-%d') 
                        
                        ConfDate += timedelta(days=30 * ExtendedMonth)
                                                
                        

               



                Emp_obj.ConfDate =  ConfDate
                Guidelines = False
                if Guide == "Yes":
                    Guidelines = True

                Emp_obj.EmpConfirm = EmpConfirm
                Emp_obj.Guidelines = Guidelines
                Emp_obj.Extended = Extended
                Emp_obj.ModifyBy = UserID
                Emp_obj.save()


                try:
                    Total_Category  =  int(request.POST["Total_Category"])
                except (TypeError, ValueError):
                    Total_Category = 0

                for cat in range(Total_Category + 1):
                    Cat_ID =  request.POST.get(f'Cat_ID_{cat}')
                    

                    try:
                        Total_Item_Count = int(request.POST.get(f'cat_{ cat }_Total_Item'))
                    except (TypeError, ValueError):
                        Total_Item_Count = 0
                
                     
                    for x in range(Total_Item_Count + 1):
                            Item_ID = request.POST.get(f'cat_{ cat }_Item_Id_{ x }')

                            if not Item_ID:  # skip if missing
                                continue

                            # print("the item id is here::", Item_ID)
                            # print("POST keys:", request.POST.keys())
                            # print("cat_0_Item_Id_0:", request.POST.get("cat_0_Item_Id_0"))
                            Item_ID_revised = request.POST.get("cat_0_Item_Id_0")
                                                        
                            Is =  request.POST.get(f'cat_{ cat }_IsYes_{ x }')
                            IsYes = False
                            if Is == "Yes":
                                IsYes = True
                            Remarks = request.POST.get(f'cat_{cat }_Remarks_{x}')


                            # Emp_Details = get_object_or_404(Emp_Confirmation_Details,Emp_Confirmation_Master = Emp_obj,IsDelete=False,Item_Master_id = Item_ID)
                            Emp_Details = Emp_Confirmation_Details.objects.filter(
                                Emp_Confirmation_Master_id=Emp_obj,
                                # id = int(ID),
                                IsDelete=False,
                                Item_Master_id = Item_ID
                            ).first()

                            # print("the value of Emp_Details object::", Emp_Details)
                            # print("the value of isyes::", IsYes)
                            if Emp_Details:
                                Emp_Details.IsYes = IsYes
                                Emp_Details.Remarks = Remarks
                                Emp_Details.ModifyBy = UserID
                                Emp_Details.save()
                            else:
                                Emp_Details = Emp_Confirmation_Details.objects.create(
                                    OrganizationID = OrganizationID,
                                    CreatedBy = UserID,
                                    Emp_Confirmation_Master = Emp_obj,
                                    Item_Master_id = Item_ID,
                                    IsYes = IsYes,                                     
                                    Remarks = Remarks                                         
                                )
                                print("Skipping creation of Emp_Confirmation_Details for Item_ID:", Item_ID)

                objectives_to_save = []
                goals_to_save = []

                for key, value in request.POST.items():
                    if key.startswith('objective') and not 'goal' in key:
                        objective_number = key.replace('objective-', '')
                        objective_name = value
                        
                        # Check if it's an existing objective or a new one
                        if 'objective-' in key:
                            objective_id = int(objective_number)
                            objective = Emp_Confirmation_Objective_Details.objects.filter(id=objective_id,IsDelete=False,OrganizationID = OrganizationID).first()
                            if  objective:
                                objective.ObjectiveName = objective_name
                                objective.save()
                            else:    
                                obj= Emp_Confirmation_Objective_Details.objects.create(
                                    Emp_Confirmation_Master_id=ID,
                                    ObjectiveName=objective_name,
                                    OrganizationID=OrganizationID,
                                    CreatedBy=UserID,
                                )
                            
                        
                        objectives_to_save.append(objective)

                    if 'goal' in key:
                        goal_key_parts = key.split('-')
                        
                        objective_id = int(goal_key_parts[1])
                       
                        goal_id = int(goal_key_parts[3])
                        goal_name = value

                        if goal_id != 0:
                            goal = Emp_Confirmation_Objective_Goals.objects.filter(id=goal_id,IsDelete=False,OrganizationID = OrganizationID).first()
                            if goal:
                                goal.GoalName = goal_name
                                goal.save()
                            else:
                                
                                objective = Emp_Confirmation_Objective_Details.objects.filter(id=objective_id,IsDelete=False,OrganizationID = OrganizationID).first()
                                if objective:
                                    goal = Emp_Confirmation_Objective_Goals.objects.create(
                                        Emp_Confirmation_Objective_Details_id=objective_id,
                                        GoalName=goal_name,
                                        OrganizationID=OrganizationID,
                                        CreatedBy=UserID,
                                    )
                                else:
                                    goal = Emp_Confirmation_Objective_Goals.objects.create(
                                        Emp_Confirmation_Objective_Details_id=obj.id,
                                        GoalName=goal_name,
                                        OrganizationID=OrganizationID,
                                        CreatedBy=UserID,
                                    )

                                
                        
                        goals_to_save.append(goal)  
                # e = request.GET.get('E', "")
                # if e!='':
                #     EC = request.GET.get('EC', "")
                #     O = request.GET.get('O', "")
                #     od = OrganizationDetail(OrganizationID)
                #     DomainCode=od.get_OrganizationDomainCode()
                #     newd = MasterAttribute.CurrentHost.replace("http://hotelops.in","http://"+DomainCode+".hotelops.in")
                #     return redirect(newd+"/HR/Home/EmpProfile?E="+e+"&Q=empprobationconfirmation&EC="+EC+"&O="+O+"")
                # messages.success(request,"Updated Successfully !")        
            else:
                EmpCode = request.POST['EmpCode'] or ''
                EmpName = request.POST['EmpName'] or ''
                Position = request.POST['Position'] or ''
                Department = request.POST['Department'] or ''
                JoiningDate =  request.POST['JoiningDate']
                ConfDate =  request.POST['ConfDate'] or ''
                EmpCon = request.POST.get('EmpCon')
                print("EmpCon = ",EmpCon) 
                Exten = request.POST.get('Exten') 
                Strengths =  request.POST['Strengths'] or ''
                Improvement = request.POST['Improvement'] or ''
                Guide = request.POST.get('Guide') 
                Trainingattended  = request.POST['Trainingattended'] or ''

                EmpConfirm = False
                if EmpCon == "Yes":
                    EmpConfirm = True
                Extended = ''
                if EmpCon == "Extended":
                    Extended = Exten
                    if ConfDate:
                        ExtendedMonth = int(Exten.split()[0]) 
                        ConfDate = datetime.strptime(ConfDate, '%Y-%m-%d') 
                        ConfDate += timedelta(days=30 * ExtendedMonth)

                Guidelines = False
                if Guide == "Yes":
                    Guidelines = True

                    
                Emp_Confirmation = Emp_Confirmation_Master.objects.create(
                    OrganizationID=OrganizationID,CreatedBy = UserID ,
                    EmpCode = EmpCode,
                    EmpName = EmpName,
                    Position = Position,
                    Department = Department,
                    JoiningDate = JoiningDate,
                    ConfDate =  ConfDate,
                    EmpConfirm =   EmpConfirm,
                    Extended = Extended,
                    Strengths =  Strengths,
                    Improvement = Improvement,
                    Guidelines = Guidelines,
                    Trainingattended  =  Trainingattended,
                ) 
                
                
                
                Total_Category  =  int(request.POST["Total_Category"])
                for cat in range(Total_Category + 1):
                    Cat_ID =  request.POST.get(f'Cat_ID_{cat}')
                    
                    Total_Item_Count = int(request.POST.get(f'cat_{ cat }_Total_Item'))
                  
                
                     
                    for x in range(Total_Item_Count + 1):
                            Item_ID = request.POST.get(f'cat_{ cat }_Item_Id_{ x }')
                            
                            Is =  request.POST.get(f'cat_{ cat }_IsYes_{ x }')
                            IsYes = False
                            if Is == "Yes":
                                IsYes = True
                            Remarks = request.POST.get(f'cat_{cat }_Remarks_{x}')
                            Emp_Details = Emp_Confirmation_Details.objects.create(
                                OrganizationID = OrganizationID,
                                CreatedBy = UserID,
                                Emp_Confirmation_Master = Emp_Confirmation,
                                Item_Master_id = Item_ID,
                                IsYes = IsYes ,
                                Remarks = Remarks
                            )
                            print(f'ID={Item_ID} Isyes= {IsYes}  Remarks = {Remarks}' )
                

                for key, value in request.POST.items():
                    if key.startswith('objective') and not 'goal' in key:
                        objective_name = value
                        
                        # Check if it's an existing objective or a new one
                        if 'objective-' in key:
                            obj= Emp_Confirmation_Objective_Details.objects.create(
                                    Emp_Confirmation_Master_id=Emp_Confirmation.id,
                                    ObjectiveName=objective_name,
                                    OrganizationID=OrganizationID,
                                    CreatedBy=UserID,
                                )


                    if 'goal' in key:
                        goal_name = value

                        goal = Emp_Confirmation_Objective_Goals.objects.create(
                            Emp_Confirmation_Objective_Details_id=obj.id,
                            GoalName=goal_name,
                            OrganizationID=OrganizationID,
                            CreatedBy=UserID,
                        )

                
                
                # e = request.GET.get('E', "")
                # if e!='':
                #     EC = request.GET.get('EC', "")
                #     O = request.GET.get('O', "")
                #     od = OrganizationDetail(OrganizationID)
                #     DomainCode=od.get_OrganizationDomainCode()
                #     newd = MasterAttribute.CurrentHost.replace("http://hotelops.in","http://"+DomainCode+".hotelops.in")
                #     return redirect(newd+"/HR/Home/EmpProfile?E="+e+"&Q=empprobationconfirmation&EC="+EC+"&O="+O+"")
                # messages.success(request,"Added Successfully !")        
            
            # return redirect('ListPC')
            try:
                employee_work_details = EmployeeWorkDetails.objects.get(
                    EmpID=EmpID, OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False)
                employee_work_details.EmpStatus = "Not Confirmed"
                employee_work_details.ModifyBy = UserID
                employee_work_details.save()
            except EmployeeWorkDetails.DoesNotExist:
                print("EmployeeWorkDetails record not found.")
            
            if Page:
                return redirect('ListPC')
            Success = True        
            encrypted_id = encrypt_id(EmpID)
            url = reverse('ProbationConfirmation')  
            redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
            return redirect(redirect_url)

    context = {
        'Emp_obj':Emp_obj,
        'OrganizationID':OrganizationID,
        'hotelapitoken':hotelapitoken,
        'Categories':Categories,
        'Month':Month,
        'objectives': objectives_data
    }
    return render(request, 'ProbationConfirmation/New.html',context)


@transaction.atomic
def DeletePC(request):
     if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
     else:
        print("Show Page Session")

     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID
     UserID = str(request.session["UserID"])
     id = request.GET.get("ID")
     EmpID  = request.GET.get('EmpID')
    
     with transaction.atomic():
        Emp_obj = Emp_Confirmation_Master.objects.get(id = id)
        Emp_obj.IsDelete =True
        Emp_obj.ModifyBy =  UserID
        Emp_obj.save()
        Success = True        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('ProbationConfirmation')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
        return redirect(redirect_url)
     





from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
import codecs
from django.db.models import Subquery
from django.core.exceptions import FieldError
from django.db import DatabaseError, OperationalError

from django.db.models import Subquery, OuterRef

def ViewPC(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    EmpCode = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID = str(request.session["UserID"])

    EmpCode  = request.GET.get('EC')

    try:
        # Subquery to get ReportingtoDesignation
        # Step 1: Get ReportingtoDesignation(s) for the given EmployeeCode
        emp_ids = EmployeePersonalDetails.objects.filter(
            EmployeeCode=EmpCode,
            OrganizationID=OrganizationID,
            IsDelete=False
        ).values_list('EmpID', flat=True)

        if not emp_ids:
            raise ValueError("No employee found with the given EmployeeCode.")

        reporting_designations = EmployeeWorkDetails.objects.filter(
            EmpID__in=emp_ids,
            IsDelete=False,
            IsSecondary=False
        ).values('ReportingtoDesignation')


        if not reporting_designations:
            raise ValueError("No reporting designations found for given employee.")

        # Step 2: Filter EmployeeWorkDetails with matching designation
        work_details = EmployeeWorkDetails.objects.filter(
            Designation__in=Subquery(reporting_designations),
            EmpStatus__in=['Confirmed', 'On Probation'],
            OrganizationID=OrganizationID,
            IsDelete=False,
            IsSecondary = False
        ).values('EmpID', 'Designation')

        if not work_details:
            raise ValueError("No active employees found matching the reporting designations.")
        
        # Step 3: Get personal details for those EmpIDs
        emp_ids_matched = [wd['EmpID'] for wd in work_details]

        Reporting_To_Personal_Details = EmployeePersonalDetails.objects.filter(
            EmpID__in=emp_ids_matched,
            OrganizationID=OrganizationID,
            IsDelete=False
        ).values('Prefix', 'FirstName', 'MiddleName', 'LastName', 'EmpID')

        if not Reporting_To_Personal_Details:
            raise ValueError("No personal details found for the matched employee.")
        
    except ValueError as ve:
        # Custom logical errors like no data found
        Reporting_To_Personal_Details = None
        designation = None
        print(f"[ValueError] {ve}")

    except FieldError as fe:
        # Django-specific field lookup issues
        Reporting_To_Personal_Details = None
        designation = None
        print(f"[FieldError] {fe}")

    except (DatabaseError, OperationalError) as db_err:
        # Database connection or query-level problems
        Reporting_To_Personal_Details = None
        designation = None
        print(f"[DatabaseError] {db_err}")

    except Exception as e:
        # Fallback for anything unexpected
        Reporting_To_Personal_Details = None
        designation = None
        print(f"[Unhandled Exception] {e}")


    # print("Reporting to designation is here:", Reporting_To_Personal_Details)
    # print("work_details with designation:", work_details)
    # print("reporting_designations with ReportingtoDesignation:", reporting_designations)
    # print("emp_ids with emp_ids:", emp_ids)


    Categories = Category_Master.objects.filter(IsDelete=False)
    for m in Categories:
        item = Item_Master.objects.filter(IsDelete=False, Category=m)
        m.items = item

    ID = request.GET.get('ID')
    Emp_obj = None
    if ID is not None:
        Emp_obj = get_object_or_404(Emp_Confirmation_Master, id=ID, IsDelete=False)
        for m in Categories:
            item = Item_Master.objects.filter(IsDelete=False, Category=m)
            m.items = item
            for it in item:
                dt = Emp_Confirmation_Details.objects.filter(IsDelete=False, Emp_Confirmation_Master=Emp_obj, Item_Master__Category=m, Item_Master=it)
                it.emp_detail = dt 



    if EmpCode is not None:
        if ID is not None:
            Emp_obj = Emp_Confirmation_Master.objects.filter(id=ID,IsDelete=False).first()
            for m in Categories:
                item= Item_Master.objects.filter(IsDelete=False,Category=m)
                m.items = item
                for it in item:
                    dt = Emp_Confirmation_Details.objects.filter(IsDelete=False,Emp_Confirmation_Master=Emp_obj,Item_Master__Category = m,Item_Master=it)
                    it.emp_detail = dt

            objectives = Emp_Confirmation_Objective_Details.objects.filter(Emp_Confirmation_Master_id=ID,IsDelete=False,OrganizationID = OrganizationID)
            objectives_data = []

            for objective in objectives:
                goals = Emp_Confirmation_Objective_Goals.objects.filter(Emp_Confirmation_Objective_Details=objective,IsDelete=False,OrganizationID = OrganizationID)
                goals_data = [{'id': goal.id, 'name': goal.GoalName} for goal in goals]
                objectives_data.append({
                    'id': objective.id,
                    'name': objective.ObjectiveName,
                    'goals': goals_data
                })

    print("Emp_obj.Department:::", Emp_obj.Department)
    template_path = "ProbationConfirmation/View.html"
    extended_value = Emp_obj.Extended.strip()    
    mydict = {'Categories': Categories, 'Emp_obj': Emp_obj,'extended_value':extended_value ,'data':objectives_data, 'Reporting_To_Personal_Details':Reporting_To_Personal_Details,'work_details':work_details}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Confirmation.pdf"'

    template = get_template(template_path)
    html = template.render(mydict)

    # Encode HTML content as UTF-8
    html_utf8 = html.encode("UTF-8")

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_utf8), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None







# def submit_objectives(request):
#     Emp_Confirmation_id = request.GET.get('ID')
#     OrganizationID = 1001
#     UserID = 0

#     if request.method == "POST":
#         objectives_to_save = []
#         goals_to_save = []

#         for key, value in request.POST.items():
#             if key.startswith('objective') and not 'goal' in key:
#                 objective_number = key.replace('objective-', '')
#                 objective_name = value
                
#                 # Check if it's an existing objective or a new one
#                 if 'objective-' in key:
#                     objective_id = int(objective_number)
#                     objective = Emp_Confirmation_Objective_Details.objects.filter(id=objective_id,IsDelete=False,OrganizationID = OrganizationID).first()
#                     if  objective:
#                         objective.ObjectiveName = objective_name
#                         objective.save()
#                     else:    
#                         obj= Emp_Confirmation_Objective_Details.objects.create(
#                             Emp_Confirmation_Master_id=Emp_Confirmation_id,
#                             ObjectiveName=objective_name,
#                             OrganizationID=OrganizationID,
#                             CreatedBy=UserID,
#                         )
                       
                
#                 objectives_to_save.append(objective)

#             if 'goal' in key:
#                 goal_key_parts = key.split('-')
                
#                 objective_id = int(goal_key_parts[1])
#                 print(objective_id)
#                 goal_id = int(goal_key_parts[3])
#                 goal_name = value

#                 if goal_id != 0:
#                     goal = Emp_Confirmation_Objective_Goals.objects.filter(id=goal_id,IsDelete=False,OrganizationID = OrganizationID).first()
#                     if goal:
#                         goal.GoalName = goal_name
#                         goal.save()
#                     else:
                        
#                         objective = Emp_Confirmation_Objective_Details.objects.filter(id=objective_id,IsDelete=False,OrganizationID = OrganizationID).first()
#                         if objective:
#                             goal = Emp_Confirmation_Objective_Goals.objects.create(
#                                 Emp_Confirmation_Objective_Details_id=objective_id,
#                                 GoalName=goal_name,
#                                 OrganizationID=OrganizationID,
#                                 CreatedBy=UserID,
#                             )
#                         else:
#                             goal = Emp_Confirmation_Objective_Goals.objects.create(
#                                 Emp_Confirmation_Objective_Details_id=obj.id,
#                                 GoalName=goal_name,
#                                 OrganizationID=OrganizationID,
#                                 CreatedBy=UserID,
#                             )

                        
                
#                 goals_to_save.append(goal)


#         return redirect('ListPC')

#     # Fetch existing objectives and goals for rendering the form
#     objectives = Emp_Confirmation_Objective_Details.objects.filter(Emp_Confirmation_Master_id=Emp_Confirmation_id,IsDelete=False,OrganizationID = OrganizationID)
#     objectives_data = []

#     for objective in objectives:
#         goals = Emp_Confirmation_Objective_Goals.objects.filter(Emp_Confirmation_Objective_Details=objective,IsDelete=False,OrganizationID = OrganizationID)
#         goals_data = [{'id': goal.id, 'name': goal.GoalName} for goal in goals]
#         objectives_data.append({
#             'id': objective.id,
#             'name': objective.ObjectiveName,
#             'goals': goals_data
#         })

#     context = {'objectives': objectives_data}
#     return render(request, 'ProbationConfirmation/submit_objectives.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

def delete_objective(request, objective_id):
    if request.method == 'DELETE':
        objective = get_object_or_404(Emp_Confirmation_Objective_Details, id=objective_id)
        objective.IsDelete = True
        objective.save()
        return JsonResponse({'message': 'Objective deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def delete_goal(request, goal_id):
    if request.method == 'DELETE':
        goal = get_object_or_404(Emp_Confirmation_Objective_Goals, id=goal_id)
        goal.IsDelete = True
        goal.save()
        return JsonResponse({'message': 'Goal deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)







                
                
