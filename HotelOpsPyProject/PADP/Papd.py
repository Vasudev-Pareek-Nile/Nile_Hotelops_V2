from django.shortcuts import render,redirect
from .models import Objective_Master,Attribute_Master,Ineffective_Indicators_Master,Effective_Indicators_Master,Entry_Master,Leadership_Details,Leadership_AttributeDetails,Effective_Indicators_Details_Appraisee,Effective_Indicators_Details_Appraisor,Ineffective_Indicators_Details_Appraisee,Ineffective_Indicators_Details_Appraisor,SPECIFIC_MEASURABLE_ACHIEVABLE,SPECIFIC_MEASURABLE_ACHIEVABLE_Details,SUMMARY_AND_ACKNOWLEDGEMENT,FINAL_PERFORMANCE_RATING,calculate_appraisal_date,calculate_next_date,Get_next_approval_level, APADP, APADP_Master_Log, Entry_Master_Log
from Manning_Guide.models import OnRollDesignationMaster,CorporateDesignationMaster
import datetime
from itertools import zip_longest

from hotelopsmgmtpy.GlobalConfig  import MasterAttribute
from django.shortcuts import get_object_or_404
from django.db  import connection, transaction
from HumanResources.views import get_employee_designation_by_EmployeeCode,EmployeeDetailsData,get_employee_names_by_designation,get_Appraisers_ReportingtoDesignation,EmployeeDetailsDataFromDesignation
from HumanResources.models import EmployeePersonalDetails, SalaryTitle_Master, Salary_Detail_Master
from KRA.views import TargetAssignNamesWithReportingtoDesignationEmployeeNameCode
from app.views import OrganizationList 
# PADP 

from itertools import chain
import calendar
import datetime
from django.utils import timezone


from itertools import chain
import calendar
import datetime
from datetime import timedelta


def ReviewDatePeriod(DateofJoining):
    if not DateofJoining:
        return {"error": "Date of Joining is required."}

    try:
        if isinstance(DateofJoining, str):
            DateofJoining = datetime.strptime(DateofJoining, "%Y-%m-%d").date()
        
        from_date = DateofJoining
        to_date = from_date + timedelta(days=365)   

        return {
            "from_date": from_date,
            "to_date": to_date        }

    except ValueError as e:
        return {"error": "Invalid Date of Joining format. Use YYYY-MM-DD."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}


from HumanResources.views import get_employee_department_by_EmployeeCode,MultipleDepartmentofEmployee
from .views import Get_HR_Manager_list, Get_DottedLine_Name_ByDesignation
from app.send_notification import *

@transaction.atomic
def PADP_Add(request):
    if 'OrganizationID' not in request.session: 
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    OrganizationID = request.session["OrganizationID"]
    
    UserID = str(request.session["UserID"])

    orgs = OrganizationList(OrganizationID)
    selectedOrganizationID  = int(OrganizationID)

    # Empty variable updated when no details found
    Nokra_message = None



    PadpDottedLine = ''
    # Login User Details 
    SessionEmployeeCode = str(request.session["EmployeeCode"])
    SessionEmployeeName = request.session.get("FullName")

    SessionDesignation = ''
    SessionDesignation  = get_employee_designation_by_EmployeeCode(OrganizationID,SessionEmployeeCode)
    Department = request.session.get("Department_Name")
    UserName = request.session.get("FullName")
    Departmentsession = 'No'
    # Departmentsession = str(Department).lower()
    # GetDepartmentsession = get_employee_department_by_EmployeeCode(OrganizationID, SessionEmployeeCode)
    GetDepartmentsession = MultipleDepartmentofEmployee(OrganizationID, SessionEmployeeCode)


    if GetDepartmentsession:
        if 'Human Resources' in GetDepartmentsession :
            Departmentsession = 'hr'


    UserType = request.session.get("UserType")
    UserType = str(UserType).lower()
    Page  = request.GET.get('Page')
    UserOID  = request.GET.get('OID')

    # print("userorganiztion id is here::", UserID)
    
    rowslist = None
    columns = None 
    OverallRating   = None

    
    # Login User Role Details
    SessionDottedLine  = 'No'

    Appraiser  = 'No' 
    # Default  Appraiser is No if ReportingtoDesigantion == Login User Designation becomes yes
    Hide = 'No'
    if str(Departmentsession) == 'hr':
        Hide = 'Yes'

    Designations = OnRollDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    DottedLineDesignations = CorporateDesignationMaster.objects.filter(IsDelete=False).order_by('designations')
    
    MergedDesignationsFrom = chain(Designations, DottedLineDesignations)
    MergedDesignationsTo = chain(Designations, DottedLineDesignations)
    

    SPE_MEA_ACH_Detail  = None
        
    HR_ManagerName = get_employee_names_by_designation(OrganizationID, 'Human Resources Manager')
    if HR_ManagerName is None:
        HR_ManagerName = ''

    #  For Edit PADP Data
    padp_id = request.GET.get('ID')
    padp =None
    sum_data = None
    Sal_data  = None
    EmpCode = request.GET.get('EmpCode')
    EmpID = request.GET.get('EmpID')

    if EmpID is None:
        if UserOID and EmpCode:
            Personalobj = EmployeePersonalDetails.objects.filter(
                IsDelete=False, IsEmployeeCreated=True, EmployeeCode = EmpCode, OrganizationID=UserOID
            ).first()

            if Personalobj:
                EmpID = Personalobj.EmpID

    # Empobj_new = EmployeeDetailsData(EmpID,OrganizationID)
    NewCTC = 0

    if EmpID is not None:
        ctc_salary_details = Salary_Detail_Master.objects.filter(
            Salary_title__Title='CTC (A+C)', IsDelete=False,
            OrganizationID=UserOID, EmpID=EmpID
        ).order_by('-id').first()
        if ctc_salary_details:
            print("the function is here")
            NewCTC = ctc_salary_details.Permonth
        else:
            NewCTC=0
            print("the function is not found")
    else:
        NewCTC=0
    

    # PADP Data Details 
    if padp_id is not None:
        if OrganizationID == "3":
            # For ceo and RD OrganizationID will not work
            padp =  Entry_Master.objects.filter(IsDelete =False,id = padp_id).first()
           
        else:
            # Organization Specific Data 
            padp =  Entry_Master.objects.filter(OrganizationID = OrganizationID,IsDelete =False,id = padp_id).first()
        
        EmployeeLevel = padp.Aprraise_Level
        EmpCode = padp.EmployeeCode
        
        if EmpCode:
            Em =  EmployeePersonalDetails.objects.filter(
                EmployeeCode=EmpCode,
                OrganizationID = OrganizationID,
                IsDelete=False
            ).first()

        if padp:
            selectedOrganizationID = padp.EmployeeOrganizationID

    
            PadpEmployeeCode  = padp.EmployeeCode
            if SessionEmployeeCode  == PadpEmployeeCode:
                     Hide = 'No'
            PadpDottedLine = ''
            if SessionDesignation == padp.DottedLine:
                     PadpDottedLine =  padp.DottedLine
                     SessionDottedLine = 'Yes'
                     Hide = 'No'
            ceoapproved = 'No'
            if padp.ReportingtoDesigantion == padp.DottedLine:
                     PadpDottedLine =  padp.DottedLine
                     if UserType ==  "ceo":
                        SessionDottedLine = 'Yes'
                        ceoapproved = 'Yes'

    else:
        if EmpID:

            Empobj = EmployeeDetailsData(EmpID,OrganizationID)
            # Empobj = Empobj_new
            EmployeeLevel = Empobj.Level

   
    # Objective and Attribute Acc to Employee Details Data 
    objs =  Objective_Master.objects.filter(IsDelete=False,Level= EmployeeLevel)
    for m in objs:
        attr1= Attribute_Master.objects.filter(IsDelete=False,Objective_Master=m)
        m.Attibutes = attr1
        Effect1 = Effective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
        m.Effectives = Effect1
        Infect1 = Ineffective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
        m.Ineffectives = Infect1

    if padp_id is not None:
        Datafrom = 'PADP'
 
        if OrganizationID == "3":
            # For ceo and RD OrganizationID will not work
            padp =  Entry_Master.objects.filter(IsDelete =False,id = padp_id).first()
            if padp.ReportingtoDesigantion == SessionDesignation:
                    Appraiser = 'Yes'  

        else:
            # Organization Specific Data 
            padp =  Entry_Master.objects.filter(IsDelete =False,id = padp_id,OrganizationID = OrganizationID).first()
            if padp:

                # if ReportingtoDesigantion == Login User Designation
                if padp.ReportingtoDesigantion == SessionDesignation:
                    Appraiser = 'Yes'    

        if padp:
            # KRA 
            selected_from_year =  padp.FromReviewDate.year
            selected_from_month = padp.FromReviewDate.month  
            selected_to_year =  padp.ToReviewDate.year 
            selected_to_month =  padp.ToReviewDate.month 

            try:
                with connection.cursor() as cursor:
                    # Update the SQL query to use the correct stored procedure and parameters
                    cursor.execute("""
                        EXEC sp_GetKraYearlyReportForPadp 
                            @OrganizationID=%s, 
                            @EmployeeCode=%s, 
                            @FromYear=%s, 
                            @FromMonth=%s, 
                            @ToYear=%s, 
                            @ToMonth=%s
                        """, [
                            padp.OrganizationID, 
                            padp.EmployeeCode, 
                            selected_from_year, 
                            selected_from_month, 
                            selected_to_year, 
                            selected_to_month
                        ])
                    rows = cursor.fetchall()
                    columns = [col[0] for col in cursor.description]
                    rowslist = [dict(zip(columns, row)) for row in rows]
                    columns = list(rowslist[0].keys()) if rowslist else []
                    
                    if not rowslist:
                        Nokra_message = "No KRA details found for the selected period."
                       

            except Exception as e:
                # print("No Kra Details is not Found")
                Nokra_message = "No KRA details found for the selected period."

            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        EXEC sp_GetKraOverallRatingForPadp 
                            @OrganizationID=%s, 
                            @EmployeeCode=%s, 
                            @FromYear=%s, 
                            @FromMonth=%s, 
                            @ToYear=%s, 
                            @ToMonth=%s
                    """, [
                        padp.OrganizationID, 
                        padp.EmployeeCode, 
                        selected_from_year, 
                        selected_from_month, 
                        selected_to_year, 
                        selected_to_month
                    ])
                    result = cursor.fetchone()
                    
                    if result:
                        OverallRating = result[0]  
                    else:
                        OverallRating = None  
            except Exception as e:
                print("No Overall Rating Details is not Found")

   
        
        Leadership_Detail = Leadership_Details.objects.filter(
            Entry_Master=padp,
            IsDelete =False
        ).first()
        
        sum_data = SUMMARY_AND_ACKNOWLEDGEMENT.objects.filter(
            Entry_Master=padp,
            IsDelete =False
        ).first()
        
        Sal_data = FINAL_PERFORMANCE_RATING.objects.filter(
            Entry_Master=padp,
            IsDelete =False
        ).first()
          
          
        SPE_MEA_ACH_Detail = SPECIFIC_MEASURABLE_ACHIEVABLE_Details.objects.filter(
            SPECIFIC_MEASURABLE_ACHIEVABLE__Entry_Master = padp,
            IsDelete =False
        )
       
        for m in objs:
            m.LD = Leadership_Details.objects.filter(
                Entry_Master=padp,
                Objective_Master=m,
                IsDelete =False
            )
            
            attr1= Attribute_Master.objects.filter(
                IsDelete=False,
                Objective_Master=m
            )
            m.Attibutes = attr1
            for a in attr1:
                    k = Leadership_AttributeDetails.objects.filter(
                            IsDelete =False,
                            Leadership_Details__Objective_Master=m,
                            Attribute_Master=a,
                            Leadership_Details__Entry_Master = padp
                        )
                    a.detailatt = k

            Effect1 = Effective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
            m.Effectives = Effect1
            for eff in  Effect1:
                c = Effective_Indicators_Details_Appraisee.objects.filter(
                    IsDelete =False,
                    Entry_Master=padp,
                    Objective_Master=m,
                    Effective_Indicators_Master=eff
                )
               
                eff.effdetail_Appee = c
              
                d = Effective_Indicators_Details_Appraisor.objects.filter(
                    IsDelete =False,
                    Entry_Master=padp,
                    Objective_Master=m,
                    Effective_Indicators_Master=eff
                )
                eff.effdetail_Appor = d
               
            Infect1 = Ineffective_Indicators_Master.objects.filter(IsDelete=False,Objective_Master=m)
            m.Ineffectives = Infect1
            for inff in Infect1:
                kl = Ineffective_Indicators_Details_Appraisee.objects.filter(
                    IsDelete =False,
                    Entry_Master=padp,
                    Objective_Master=m,
                    Ineffective_Indicators_Master=inff
                )    
                inff.inffdetailAppee =  kl
                ml = Ineffective_Indicators_Details_Appraisor.objects.filter(
                    IsDelete =False,
                    Entry_Master=padp,
                    Objective_Master=m,
                    Ineffective_Indicators_Master=inff
                )    
                inff.inffdetailAppor =  ml  
    else:
        Datafrom = 'HR' 
        ReviewPeriod = ReviewDatePeriod(Empobj.DateofJoining)

        if "error" in ReviewPeriod:
            # Handle the error gracefully
            FromReviewDate = "N/A"
            ToReviewDate = "N/A"
            error_message = ReviewPeriod["error"]
            print(f"Error: {error_message}")
        else:
            FromReviewDate = ReviewPeriod["from_date"]
            print("FromReviewDate = ",FromReviewDate)
            ToReviewDate = ReviewPeriod["to_date"]

        if Empobj:
            if Empobj.DottedLine:
                DottedLine_Name = Get_DottedLine_Name_ByDesignation(Empobj.DottedLine)
            else:
                DottedLine_Name = ''


        # print("The Dotted line name == ", DottedLine_Name)

        padp = {
            'EmployeeCode': Empobj.EmployeeCode,
            'Appraisee_Name': Empobj.full_name,
            'Department': Empobj.Department if Empobj else 'N/A',
            'Aprraisee_position': Empobj.Designation if Empobj else 'N/A',
            'Aprraise_Level': Empobj.Level if Empobj else 'N/A',
            'Date_Joined_Company': Empobj.DateofJoining if Empobj else 'N/A',
            'FromReviewDate': FromReviewDate,
            'ToReviewDate': ToReviewDate,
            'Appraisor_Name': Empobj.ReportingtoDesignationName if Empobj else 'N/A',
            'Appraisor_Title': Empobj.ReportingtoDesignation if Empobj else 'N/A',
            'ReportingToLevel': Empobj.ReportingtoLevel if Empobj else 'N/A',
            'Tenure_Till_Today': Empobj.tenure_till_today if Empobj else 'N/A',
            'Appraisor_Mgr': get_Appraisers_ReportingtoDesignation(OrganizationID, Empobj.ReportingtoDesignation),
            'BasicSalary': Empobj.BasicSalary,
            'Current_Salary': Empobj.CTC,
            'DottedLine': Empobj.DottedLine if Empobj else 'N/A',
            'DottedLine_Name':DottedLine_Name
        }
        # print("Employee total ctc salary is here", Empobj.CTC)

    if isinstance(padp, dict):  
        padp['CTC'] = Empobj.CTC 
   
    HrAudit = 'No'
    ep_submitted = 'No'
    if padp_id is not None:
        if padp.DottedLine !=  padp.ReportingtoDesigantion and padp.rd_as == "Submitted" or padp.Aprraise_Level in ('M'):
            HrAudit = "Yes"
        if padp.DottedLine ==  padp.ReportingtoDesigantion  and padp.ar_as=="Submitted":
            HrAudit = "Yes"

        # new code
        if padp.ep_as:
            ep_submitted = 'Yes'
            
    with transaction.atomic():    
        if request.method == "POST":
                if padp_id is not None and Datafrom == 'PADP':
                    btn_value =   request.POST['btn_value']
                    if UserType == "ceo":
                        # For ceo and RD OrganizationID will not work
                        padp =  Entry_Master.objects.filter(IsDelete =False,id = padp_id).first()
                    
                    else:
                        # Organization Specific Data 
                        padp =  Entry_Master.objects.filter(IsDelete =False,id = padp_id).first()


                    Entry_Master_Log.objects.create(
                        Entry_Master = padp,
                        LastApporvalStatus = padp.LastApporvalStatus,
                        hr_as = padp.hr_as,
                        ep_as = padp.ep_as,
                        ar_as = padp.ar_as,
                        rd_as = padp.rd_as,
                        hr_ar = padp.hr_ar,
                        ceo_as = padp.ceo_as,
                        ceo_as_remarks = padp.ceo_as_remarks,
                        hr_actionOnDatetime = padp.hr_actionOnDatetime,
                        ep_actionOnDatetime = padp.ep_actionOnDatetime,
                        ar_actionOnDatetime = padp.ar_actionOnDatetime,
                        rd_actionOnDatetime = padp.rd_actionOnDatetime,
                        hr_ar_actionOnDatetime = padp.hr_ar_actionOnDatetime,
                        ceo_actionOnDatetime = padp.ceo_actionOnDatetime,
                        OrganizationID = padp.OrganizationID,
                        CreatedByUsername = padp.CreatedByUsername,
                        CreatedBy = padp.CreatedBy
                    )

                    # padp.Review_Date = request.POST['Review_Date']
                    padp.Appraisee_Name =request.POST['Appraisee_Name']
                    padp.Aprraisee_position = request.POST['Aprraisee_position']
                    padp.Department = request.POST['Aprraisee_Department']
                    padp.Date_Joined_Company = request.POST['Date_Joined_Company']
                    padp.Appraisor_Name =request.POST['Appraisor_Name']
                    padp.Appraisor_Title  = request.POST['Appraisor_Title']
                    padp.ReportingtoDesigantion  = request.POST['Appraisor_Title']
                    padp.Current_Salary  = request.POST['CurrentSalary']
                    
                    padp.DottedLine  = request.POST['DottedLine']

                    padp.FromReviewDate =request.POST['FromReviewDate']
                    padp.ToReviewDate = request.POST['ToReviewDate']
                    padp.EmployeeCode =  request.POST['padp_Emp_Code'] 
                    padp.Aprraise_Level = request.POST['Aprraise_Level']
                    padp.ModifyBy = UserID
            
                    
                    if SessionEmployeeCode == PadpEmployeeCode:
                        if btn_value == "1":
                            padp.ep_as = "Submitted"
                        else:
                            print("The Employee status is marked as Draft")
                            if padp.ep_as != 'Submitted':
                                # print(f"The Employee status is {padp.ep_as} and not skiped to Draft")
                                padp.ep_as = "Draft"
                                padp.LastApporvalStatus =  "Draft"   
                                padp.DraftBy = UserID
                                padp.DraftByName = SessionEmployeeName
                                padp.DraftByDateTime = datetime.datetime.now()  
                                padp.ModifyDateTime = timezone.now()  
                                # print(f"The Employee status is changed to {padp.ep_as}")
                            else:
                                print(f"The Employee status is {padp.ep_as} and skiped to Draft")

                        padp.ep_actionOnDatetime =  datetime.datetime.now()  
                        padp.ModifyDateTime =  timezone.now()  
                    
                    if SessionDesignation ==  padp.Appraisor_Title:
                        if btn_value == "1":
                             padp.ar_as = "Submitted"
                        else:
                            padp.ar_as = "Draft"
                            padp.LastApporvalStatus =  "Draft"   
                            padp.DraftBy = UserID
                            padp.DraftByName = SessionEmployeeName
                            padp.DraftByDateTime = datetime.datetime.now() 
                             
                        padp.ar_actionOnDatetime =  datetime.datetime.now()
                        padp.ModifyDateTime =  timezone.now()
                        
                   
                    if SessionDesignation ==  padp.DottedLine:
                        if btn_value == "1":
                             padp.rd_as = "Submitted"
                        else:
                            padp.rd_as = "Draft"
                            padp.LastApporvalStatus =  "Draft"   
                            padp.DraftBy = UserID
                            padp.DraftByName = SessionEmployeeName
                            padp.DraftByDateTime = datetime.datetime.now()  
                            
                        padp.rd_actionOnDatetime =  datetime.datetime.now() 
                        padp.ModifyDateTime =  timezone.now() 

                    hops_id = str(padp.id) or 0
                    Empname = padp.Appraisee_Name or ''
                    if HrAudit == "Yes":
                        if btn_value == "2":
                            padp.hr_ar = "Audited"
                            padp.LastApporvalStatus =  "Pending"  # new change
                            padp.AuditedBy = SessionEmployeeCode
                            padp.AuditedBy_Name = SessionEmployeeName
                            padp.hr_ar_actionOnDatetime = datetime.datetime.now()
                            padp.ModifyDateTime = timezone.now()

                            if hops_id != '0':
                                # CEO_Emp_Code = 001
                                Send_APDP_Audit_CEO_Notification(
                                    organization_id='3',
                                    EmpCode=['001'],
                                    title="PADP Audit Completed by HR",
                                    message=f"The PADP for {Empname} has been successfully audited by HR and is now available for your review.",
                                    module_name="PADP",
                                    action="Audited",
                                    hopsId=hops_id,
                                    user_type="admin",
                                    priority="high"
                                )
                            else:
                                print("Hops id is not found")

                            # Logic: If CEO had returned, reset CEO fields and set LastApporvalStatus to Pending
                            if padp.ceo_as == "Returned":
                                padp.Last_CEO_Action = padp.ceo_as
                                padp.Last_CEO_action_On = padp.ceo_actionOnDatetime
                                padp.Last_CEO_action_Remarks = padp.ceo_as_remarks

                                padp.ceo_as = None
                                padp.ceo_as_remarks = ""
                                padp.ceo_actionOnDatetime = None
                                padp.LastApporvalStatus = "Pending"

                        elif btn_value == "-1":
                            padp.ep_as = None
                            padp.ar_as = None
                            padp.rd_as = None
                            padp.hr_ar = None
                            padp.ep_actionOnDatetime = None
                            padp.ar_actionOnDatetime = None
                            padp.rd_actionOnDatetime = None
                            padp.hr_ar_actionOnDatetime = None
                            padp.hr_as = "Return"
                            padp.LastApporvalStatus =  "Pending" 
                            padp.hr_actionOnDatetime = datetime.datetime.now()    
                            padp.ModifyDateTime = timezone.now()    

                        else:
                            padp.hr_ar = "Draft"
                            padp.LastApporvalStatus =  "Draft"   
                            padp.DraftBy = UserID
                            padp.DraftByName = SessionEmployeeName
                            padp.DraftByDateTime = datetime.datetime.now() 
                            padp.hr_ar_actionOnDatetime = datetime.datetime.now()
                            padp.ModifyDateTime = timezone.now()


                    if str(Departmentsession) == 'hr' and HrAudit != 'Yes':
                        if btn_value == "1":
                            padp.hr_as = "Submitted"
                            padp.LastApporvalStatus = "Submitted"
                        else:
                            padp.DraftBy = UserID
                            padp.DraftByName = SessionEmployeeName
                            padp.DraftByDateTime = datetime.datetime.now() 
                            padp.hr_as = "Draft"
                            padp.LastApporvalStatus =  "Draft"   

                        padp.hr_actionOnDatetime = datetime.datetime.now()    
                        padp.ModifyDateTime = timezone.now()    

                    if UserType ==  "ceo" :
                            if btn_value == "1":
                                padp.ceo_as = "Approved"
                                padp.LastApporvalStatus ==  "Approved"
                            else:
                                padp.DraftBy = UserID
                                padp.DraftByName = SessionEmployeeName
                                padp.DraftByDateTime = datetime.datetime.now() 
                                padp.ceo_as = "Draft"
                                padp.LastApporvalStatus =  "Draft"   

                            padp.ceo_actionOnDatetime =  datetime.datetime.now()       
                            padp.ModifyDateTime =  timezone.now()
                                   
                    if ceoapproved == 'Yes':
                        if btn_value == "1":
                            padp.ceo_as = "Approved"
                            padp.LastApporvalStatus =  "Approved"   
                        else:
                            padp.DraftBy = UserID
                            padp.DraftByName = SessionEmployeeName
                            padp.DraftByDateTime = datetime.datetime.now() 
                            padp.ceo_as = "Draft"
                            padp.LastApporvalStatus =  "Draft"   
 
                        padp.ceo_actionOnDatetime =  datetime.datetime.now()       
                        padp.ModifyDateTime =  timezone.now()       

                    padp.save()
                    
                    if  Appraiser == "Yes":
                            SP_GM_Rating_Excellent = False
                            # SP_GM_Rating_Good = False
                            SP_GM_Rating_Average = False
                            SP_GM_Rating_Poor = False
                            SP_GM_Rating_Needs_Improvement = False
                            spgm  =request.POST.get('spgm')
                            if spgm == "E":
                                SP_GM_Rating_Excellent=True
                            # if spgm == "G":
                            #     SP_GM_Rating_Good= True
                            if spgm == "A":
                                SP_GM_Rating_Average= True
                            if spgm == "P":
                                SP_GM_Rating_Poor= True
                            if spgm == "N":
                                SP_GM_Rating_Needs_Improvement= True
                            sum_data.SP_GM_Rating_Excellent = SP_GM_Rating_Excellent
                            # sum_data.SP_GM_Rating_Good =  SP_GM_Rating_Good
                            
                            sum_data.SP_GM_Rating_Average = SP_GM_Rating_Average
                            sum_data.SP_GM_Rating_Poor =  SP_GM_Rating_Poor
                            sum_data.SP_GM_Rating_Needs_Improvement =  SP_GM_Rating_Needs_Improvement
                            sum_data.SP_GM_Comment  =request.POST.get('SP_GM_Comment') or '' 

                    if  SessionDottedLine == "Yes":
                            RD_Rating_Excellent = False
                            # RD_Rating_Good = False
                            RD_Rating_Average = False
                            RD_Rating_Poor = False
                            RD_Rating_Needs_Improvement = False
                            rdr  = request.POST.get('RDR')
                            if rdr == "E":
                                RD_Rating_Excellent=True
                            # if rdr == "G":
                            #     RD_Rating_Good= True
                            if rdr == "A":
                                RD_Rating_Average= True
                            if rdr == "P":
                                RD_Rating_Poor= True
                            if rdr == "N":
                                RD_Rating_Needs_Improvement= True
                                
                            sum_data.RD_Rating_Excellent = RD_Rating_Excellent
                            # sum_data.RD_Rating_Good =  RD_Rating_Good
                            sum_data.RD_Rating_Average = RD_Rating_Average
                            sum_data.RD_Rating_Poor =  RD_Rating_Poor
                            sum_data.RD_Rating_Needs_Improvement =  RD_Rating_Needs_Improvement 
                            sum_data.RD_Comment  =request.POST.get('RD_Comment')    or ''   
                    
                    sum_data.SUMMARY_APPRAISEE = request.POST.get('SUMMARY_APPRAISEE') or ''
                    
                    sum_data.SUMMARY_APPRAISOR = request.POST.get('SUMMARY_APPRAISOR') or ''

                    sum_data.Appraisee = request.POST.get('Appraisee_ACK') or ''
                    sum_data.Appraisor = request.POST.get('Appraisor_ACK') or ''
                    sum_data.HR_Manager = request.POST.get('HR_Manager_ACK') or ''
                    sum_data.Appraisor_Mgr= request.POST.get('Appraisor_Mgr_ACK') or ''
                    sum_data.Anticipated_promotionffransfer_Date = request.POST.get('Anticipated_Date') or None
                    sum_data.Position = request.POST.get('Position_ACK') or ''
                    sum_data.Alternative_Position = request.POST.get('Alternative_Position') or ''
                    sum_data.ModifyBy = UserID
                    sum_data.save()
                 
                    # if Appraisee  and Appraiser Common for both 
                    if  Hide == 'No' :     
                        if Leadership_Detail:
                            # LEADERSHIP COMPETENCIES

                            tr = request.POST.get('Total_objective') or ''
                            if tr !='':
                                Total_objective = int(request.POST["Total_objective"])   
                                # print("Total_objective Value: ", Total_objective)     
                                for obj in range(Total_objective + 1):
                                    
                                    obj_id_key = f'obj_ID_{obj}'
                                    obj_id_value = request.POST.get(obj_id_key)
                                    obj_data = get_object_or_404(Objective_Master, id=obj_id_value, IsDelete=False)
                                    Appraise_Comments_key  = f'Appraise_Comments_{obj}'  
                                    Appraise_Comments =request.POST[Appraise_Comments_key]
                                    Appraisor_Comments_key = f'Appraisor_Comments_{obj}'
                                    Appraisor_Comments = request.POST[Appraisor_Comments_key]
                                    Leader_Detail =  Leadership_Details.objects.get(Entry_Master=padp,Objective_Master_id=obj_data.id)
                                    Leader_Detail.Appraise_Comments =  Appraise_Comments
                                    Leader_Detail.Appraisor_Comments = Appraisor_Comments
                                    Leader_Detail.ModifyBy = UserID
                                    Leader_Detail.save()

                                    total_attribute_key = f'obj_{obj}_Total_attribute'
                                    total_attribute_Count = int(request.POST.get(total_attribute_key))
                                    
                                    for att in range(total_attribute_Count+1):
                                        att_id_key = f'obj_{obj}_Att_ID_{att}'
                                        att_id_value = request.POST.get(att_id_key)
                                        att_data = get_object_or_404(Attribute_Master, id=att_id_value, IsDelete=False)
                                        Leader_Attribute = Leadership_AttributeDetails.objects.get(
                                            Leadership_Details = Leader_Detail,
                                            Attribute_Master_id=att_data.id
                                        )

                                        if Appraiser == "No":

                                            Does_NOT_Appee = False
                                            Rarely_Appee = False
                                            Sometiems_Appee = False
                                            Often_Appee = False
                                            Always_Appee = False
                                            
                                            does_key_Appee = f'obj_{obj}_attr_{att}_Appee'
                                            does_Appee_value = request.POST.get(does_key_Appee)
                                            if does_Appee_value == "D" :
                                                Does_NOT_Appee =True
                                            
                                            rarely_key_Appee = f'obj_{obj}_attr_{att}_Appee'
                                            rarely_Appee_value = request.POST.get(rarely_key_Appee)
                                            if rarely_Appee_value == "R" :
                                                Rarely_Appee =True

                                            Sometimes_key_Appee = f'obj_{obj}_attr_{att}_Appee'
                                            Sometimes_Appee_value = request.POST.get(Sometimes_key_Appee)
                                            if Sometimes_Appee_value == "S" :
                                                Sometiems_Appee =True


                                            Often_key_Appee = f'obj_{obj}_attr_{att}_Appee'
                                            Often_Appee_value = request.POST.get(Often_key_Appee)
                                            if Often_Appee_value == "O" :
                                                Often_Appee =True
                                            
                                            Always_key_Appee = f'obj_{obj}_attr_{att}_Appee'
                                            Always_Appee_value = request.POST.get(Always_key_Appee)
                                            if Always_Appee_value == "A" :
                                                Always_Appee =True
                                        
                                            if  Does_NOT_Appee:    
                                                Leader_Attribute.Does_NOT_Appee = Does_NOT_Appee
                                            if  Rarely_Appee:    
                                                Leader_Attribute.Rarely_Appee = Rarely_Appee
                                            if  Sometiems_Appee:    
                                                Leader_Attribute.Sometiems_Appee = Sometiems_Appee
                                            if  Often_Appee:    
                                                Leader_Attribute.Often_Appee = Often_Appee
                                            if  Always_Appee:    
                                                Leader_Attribute.Always_Appee = Always_Appee    
                                    
                                    
                                        if  Appraiser == "Yes":
                                            Does_NOT_Appor = False
                                            Rarely_Appor = False
                                            Sometiems_Appor = False
                                            Often_Appor = False
                                            Always_Appor = False

                                            does_key_Appor = f'obj_{obj}_attr_{att}_Appor'
                                            does_Appor_value = request.POST.get(does_key_Appor)
                                            if does_Appor_value == "D" :
                                                Does_NOT_Appor =True

                                            rarely_key_Appor = f'obj_{obj}_attr_{att}_Appor'
                                            rarely_Appor_value = request.POST.get(rarely_key_Appor)
                                            if rarely_Appor_value == "R" :
                                                Rarely_Appor =True    
                                            
                                            Sometimes_key_Appor = f'obj_{obj}_attr_{att}_Appor'
                                            Sometimes_Appor_value = request.POST.get(Sometimes_key_Appor)
                                            if Sometimes_Appor_value == "S" :
                                                Sometiems_Appor =True

                                            Often_key_Appee = f'obj_{obj}_attr_{att}_Appee'
                                            Often_Appee_value = request.POST.get(Often_key_Appee)
                                            if Often_Appee_value == "O" :
                                                Often_Appee =True
                                            
                                            Often_key_Appor = f'obj_{obj}_attr_{att}_Appor'
                                            Often_Appor_value = request.POST.get(Often_key_Appor)
                                            if Often_Appor_value == "O":
                                                Often_Appor =True

                                            Always_key_Appor = f'obj_{obj}_attr_{att}_Appor'
                                            Always_Appor_value = request.POST.get(Always_key_Appor)
                                            if Always_Appor_value == "A" :
                                                Always_Appor =True

                                    
                                    
                                            if  Does_NOT_Appor:   

                                                Leader_Attribute.Does_NOT_Appor = Does_NOT_Appor
                                            if  Rarely_Appor:   

                                                Leader_Attribute.Rarely_Appor =Rarely_Appor 
                                            if  Sometiems_Appor:   

                                                Leader_Attribute.Sometiems_Appor = Sometiems_Appor
                                            if  Often_Appor:   

                                                Leader_Attribute.Often_Appor = Often_Appor
                                            
                                            if  Always_Appor:   

                                                Leader_Attribute.Always_Appor = Always_Appor



                                        Leader_Attribute.ModifyBy = UserID
                                        Leader_Attribute.save()
                                    # APPRAISEE  EFFECTIVE
                                    total_Effective_key_Appee=f'obj_{obj}_Total_Effective_Appee'
                                    total_Effective_key_Count_Appee = int(request.POST.get(total_Effective_key_Appee))
                            
                                    
                                    for  Effective_key_Appee in range(total_Effective_key_Count_Appee+1):
                                        EFF_Appee_ID = f'EFF_{Effective_key_Appee}_obj_{obj}_Appee_ID'
                                        EFF_Appee_ID_Value = request.POST.get(EFF_Appee_ID)

                                        Effective_key_Appee = f'EFF_{Effective_key_Appee}_obj_{obj}_Appee'
                                        Effective_key_Appee_value = request.POST.get(Effective_key_Appee)

                                        Eff_Appee = get_object_or_404(Effective_Indicators_Master,id=EFF_Appee_ID_Value, IsDelete=False)
                                        
                                        Eff_data_Appee  = Effective_Indicators_Details_Appraisee.objects.filter(IsDelete=False,Entry_Master=padp,Objective_Master_id=obj_data.id,Effective_Indicators_Master = Eff_Appee).first()
                                        if  Eff_data_Appee:
                                            Eff_Appee_Status =False
                                            if Effective_key_Appee_value == "1":
                                                Eff_Appee_Status = True
                                            Eff_data_Appee.Status = Eff_Appee_Status
                                            Eff_data_Appee.ModifyBy = UserID
                                            Eff_data_Appee.save()
                                            
                                    # APPRAISEE Ineffective
                                    total_Ineffective_key_Appee=f'obj_{obj}_Total_Ineffective_Appee'
                                    total_Ineffective_key_Count_Appee = int(request.POST.get(total_Ineffective_key_Appee))
                                    for  Ineffective_key_Appee in range(total_Ineffective_key_Count_Appee+1):
                                        Ineff_Appee_ID = f'Ine_{Ineffective_key_Appee}_obj_{obj}_Appee_ID'
                                        Ineff_Appee_ID_Value =   request.POST.get(Ineff_Appee_ID)   

                                        
                                        Ineffective_key_Appee = f'Ine_{Ineffective_key_Appee}_obj_{obj}_Appee'
                                        Ineffective_key_Appee_value = request.POST.get(Ineffective_key_Appee)
                                        
                                        
                                        Inf_Appee = get_object_or_404(Ineffective_Indicators_Master,id=Ineff_Appee_ID_Value, IsDelete=False)
                                        Inf_data_Appee  = Ineffective_Indicators_Details_Appraisee.objects.filter(IsDelete=False,Entry_Master=padp,Objective_Master_id=obj_data.id,Ineffective_Indicators_Master = Inf_Appee).first()
                                        if Inf_data_Appee:
                                            Inf_Appee_Status = False
                                            if Ineffective_key_Appee_value == "1":
                                                Inf_Appee_Status = True
                                            Inf_data_Appee.Status = Inf_Appee_Status
                                            Inf_data_Appee.ModifyBy = UserID
                                            Inf_data_Appee.save()    

                                    # APPRAISOR Effective
                                    total_Effective_key_Appor=f'obj_{obj}_Total_Effective_Appor'
                                    total_Effective_key_Count_Appor = int(request.POST.get(total_Effective_key_Appor))
                                    

                                    
                                    for  Effective_key_Appor in range(total_Effective_key_Count_Appor+1):
                                        Eff_Appor_ID = f'EFF_{Effective_key_Appor}_obj_{obj}_Appor_ID'   
                                        Eff_Appor_ID_Value = request.POST.get(Eff_Appor_ID)

                                        Effective_key_Appor = f'EFF_{Effective_key_Appor}_obj_{obj}_Appor'
                                        Effective_key_Appor_value = request.POST.get(Effective_key_Appor)

                                    
                                        Eff_Appor = get_object_or_404(Effective_Indicators_Master,id=Eff_Appor_ID_Value, IsDelete=False)
                                        Eff_data_Appor  = Effective_Indicators_Details_Appraisor.objects.filter(IsDelete=False,Entry_Master=padp ,Objective_Master_id=obj_data.id,Effective_Indicators_Master = Eff_Appor).first()
                                        if Eff_data_Appor:
                                        
                                            Eff_Appor_Status = False
                                            if Effective_key_Appor_value == "1":
                                                Eff_Appor_Status = True
                                            Eff_data_Appor.Status = Eff_Appor_Status
                                            Eff_data_Appor.ModifyBy = UserID
                                            Eff_data_Appor.save()    
                                    #  APPRAISOR Ineffective    
                                
                                
                                    total_Ineffective_key_Appor=f'obj_{obj}_Total_Ineffective_Appor'
                                    total_Ineffective_key_Count_Appor = int(request.POST.get(total_Ineffective_key_Appor))
                                    for  Ineffective_key_Appor in range(total_Ineffective_key_Count_Appor+1):
                                        Ineff_Appor_ID=f'Ine_{Ineffective_key_Appor}_obj_{obj}_Appor_ID'
                                        Ineff_Appor_ID_Value = request.POST.get(Ineff_Appor_ID)
                                        
                                        Ineffective_key_Appor = f'Ine_{Ineffective_key_Appor}_obj_{obj}_Appor'
                                        Ineffective_key_Appor_value = request.POST.get(Ineffective_key_Appor)
                                    
                                        
                                        
                                        Inff_Appor = get_object_or_404(Ineffective_Indicators_Master,id=Ineff_Appor_ID_Value, IsDelete=False)
                                        Inff_data_Appor  = Ineffective_Indicators_Details_Appraisor.objects.filter(IsDelete=False,Entry_Master=padp,Objective_Master_id=obj_data.id,Ineffective_Indicators_Master = Inff_Appor).first()
                                        if Inff_data_Appor:
                                            Inf_Appor_Status = False
                                            if str(Ineffective_key_Appor_value) == "1":
                                                Inf_Appor_Status = True
                                                Inff_data_Appor.Status = Inf_Appor_Status
                                                Inff_data_Appor.ModifyBy = UserID
                                                Inff_data_Appor.save()
                        else:    
                            # LEADERSHIP COMPETENCIES
                            tr = request.POST.get('Total_objective') or ''
                            if tr !='':
                                Total_objective = int(request.POST["Total_objective"])
                                
                                
                                for obj in range(Total_objective + 1):
                                    
                                    obj_id_key = f'obj_ID_{obj}'
                                        
                                    obj_id_value = request.POST.get(obj_id_key)
                                    
                                    obj_data = get_object_or_404(Objective_Master, id=obj_id_value, IsDelete=False)
                                    Appraise_Comments_key  = f'Appraise_Comments_{obj}'  
                                    Appraise_Comments =request.POST[Appraise_Comments_key]
                                
                                    
                                    
                                    Appraisor_Comments_key = f'Appraisor_Comments_{obj}'
                                    
                                    Appraisor_Comments = request.POST[Appraisor_Comments_key]

                                    
                                    Leadership_Detail =  Leadership_Details.objects.create(CreatedBy=UserID,Appraise_Comments=Appraise_Comments,Appraisor_Comments=Appraisor_Comments,Entry_Master=padp,Objective_Master_id=obj_data.id)
                                    

                                    total_attribute_key = f'obj_{obj}_Total_attribute'
                                    total_attribute_Count = int(request.POST.get(total_attribute_key))
                                    for att in range(total_attribute_Count+1):
                                        att_id_key = f'obj_{obj}_Att_ID_{att}'
                                        att_id_value = request.POST.get(att_id_key)
                                        att_data = get_object_or_404(Attribute_Master, id=att_id_value, IsDelete=False)

                                        Does_NOT_Appee = False
                                        Rarely_Appee = False
                                        Sometiems_Appee = False
                                        Often_Appee = False
                                        Always_Appee = False
                                        
                                        does_key_Appee = f'obj_{obj}_attr_{att}_Appee'
                                        does_Appee_value = request.POST.get(does_key_Appee)
                                        if does_Appee_value == "D" :
                                            Does_NOT_Appee =True
                                        
                                        rarely_key_Appee = f'obj_{obj}_attr_{att}_Appee'
                                        rarely_Appee_value = request.POST.get(rarely_key_Appee)
                                        if rarely_Appee_value == "R" :
                                            Rarely_Appee =True

                                        Sometimes_key_Appee = f'obj_{obj}_attr_{att}_Appee'
                                        Sometimes_Appee_value = request.POST.get(Sometimes_key_Appee)
                                        if Sometimes_Appee_value == "S" :
                                            Sometiems_Appee =True


                                        Often_key_Appee = f'obj_{obj}_attr_{att}_Appee'
                                        Often_Appee_value = request.POST.get(Often_key_Appee)
                                        if Often_Appee_value == "O" :
                                            Often_Appee =True
                                        
                                        Always_key_Appee = f'obj_{obj}_attr_{att}_Appee'
                                        Always_Appee_value = request.POST.get(Always_key_Appee)

                                        if Always_Appee_value == "A" :
                                            Always_Appee =True
                                
                                        Does_NOT_Appor = False
                                        Rarely_Appor = False
                                        Sometiems_Appor = False
                                        Often_Appor = False
                                        Always_Appor = False

                                        does_key_Appor = f'obj_{obj}_attr_{att}_Appor'
                                        does_Appor_value = request.POST.get(does_key_Appor)
                                        if does_Appor_value == "D" :
                                            Does_NOT_Appor =True

                                        rarely_key_Appor = f'obj_{obj}_attr_{att}_Appor'
                                        rarely_Appor_value = request.POST.get(rarely_key_Appor)
                                        if rarely_Appor_value == "R" :
                                            Rarely_Appor =True    
                                        
                                        Sometimes_key_Appor = f'obj_{obj}_attr_{att}_Appor'
                                        Sometimes_Appor_value = request.POST.get(Sometimes_key_Appor)
                                        if Sometimes_Appor_value == "S" :
                                            Sometiems_Appor =True

                                        Often_key_Appee = f'obj_{obj}_attr_{att}_Appee'
                                        Often_Appee_value = request.POST.get(Often_key_Appee)
                                        if Often_Appee_value == "O" :
                                            Often_Appee =True
                                        
                                        Often_key_Appor = f'obj_{obj}_attr_{att}_Appor'
                                        Often_Appor_value = request.POST.get(Often_key_Appor)
                                        if Often_Appor_value == "O":
                                            Often_Appor =True

                                        Always_key_Appor = f'obj_{obj}_attr_{att}_Appor'
                                        Always_Appor_value = request.POST.get(Always_key_Appor)
                                        if Always_Appor_value == "A" :
                                            Always_Appor =True

                                        Leadership_AttributeDetails.objects.create(
                                            Leadership_Details= Leadership_Detail,
                                            Attribute_Master=att_data,
                                            Does_NOT_Appee = Does_NOT_Appee,
                                            Does_NOT_Appor = Does_NOT_Appor,
                                            Rarely_Appee = Rarely_Appee,
                                            Rarely_Appor =Rarely_Appor ,
                                            Sometiems_Appee = Sometiems_Appee,
                                            Sometiems_Appor = Sometiems_Appor,

                                            Often_Appee =Often_Appee,
                                            Often_Appor = Often_Appor,
                                            Always_Appee = Always_Appee,
                                            Always_Appor = Always_Appor,
                                            CreatedBy = UserID
                                        )    
                                        
                                    # APPRAISEE  Effective
                                    total_Effective_key_Appee=f'obj_{obj}_Total_Effective_Appee'
                                    total_Effective_key_Count_Appee = int(request.POST.get(total_Effective_key_Appee))
                                    
                                    for  Effective_key_Appee in range(total_Effective_key_Count_Appee+1):
                                        EFF_Appee_ID = f'EFF_{Effective_key_Appee}_obj_{obj}_Appee_ID'
                                        EFF_Appee_ID_Value = request.POST.get(EFF_Appee_ID)


                                        Effective_key_Appee = f'EFF_{Effective_key_Appee}_obj_{obj}_Appee'
                                        Effective_key_Appee_value = request.POST.get(Effective_key_Appee)

                                        
                                        Eff_Appee = get_object_or_404(Effective_Indicators_Master,id=EFF_Appee_ID_Value, IsDelete=False)
                                        Eff_Appee_Status =False
                                        if Effective_key_Appee_value == "1":
                                            Eff_Appee_Status = True
                                        Eff_data_Appee  = Effective_Indicators_Details_Appraisee.objects.create(CreatedBy = UserID,Entry_Master=padp,Objective_Master_id=obj_data.id,Effective_Indicators_Master = Eff_Appee,Status=Eff_Appee_Status )
                                            
                                    #  APPRAISEE  Ineffective    
                                    total_Ineffective_key_Appee=f'obj_{obj}_Total_Ineffective_Appee'
                                    total_Ineffective_key_Count_Appee = int(request.POST.get(total_Ineffective_key_Appee))
                                    for  Ineffective_key_Appee in range(total_Ineffective_key_Count_Appee+1):
                                        Ineff_Appee_ID = f'Ine_{Ineffective_key_Appee}_obj_{obj}_Appee_ID'
                                        Ineff_Appee_ID_Value =   request.POST.get(Ineff_Appee_ID)   

                                        
                                        Ineffective_key_Appee = f'Ine_{Ineffective_key_Appee}_obj_{obj}_Appee'
                                        Ineffective_key_Appee_value = request.POST.get(Ineffective_key_Appee)
                                        
                                        
                                        Inf_Appee = get_object_or_404(Ineffective_Indicators_Master,id=Ineff_Appee_ID_Value, IsDelete=False)
                                        Inf_Appee_Status = False
                                        if Ineffective_key_Appee_value == "1":
                                            Inf_Appee_Status = True
                                        Inf_data_Appee  = Ineffective_Indicators_Details_Appraisee.objects.create(CreatedBy = UserID,Entry_Master=padp,Objective_Master_id=obj_data.id,Ineffective_Indicators_Master = Inf_Appee,Status = Inf_Appee_Status )
                                    # APPRAISOR Effective
                                    total_Effective_key_Appor=f'obj_{obj}_Total_Effective_Appor'
                                    total_Effective_key_Count_Appor = int(request.POST.get(total_Effective_key_Appor))
                                    
                                    for  Effective_key_Appor in range(total_Effective_key_Count_Appor+1):
                                        Eff_Appor_ID = f'EFF_{Effective_key_Appor}_obj_{obj}_Appor_ID'   
                                        Eff_Appor_ID_Value = request.POST.get(Eff_Appor_ID)

                                        Effective_key_Appor = f'EFF_{Effective_key_Appor}_obj_{obj}_Appor'
                                        Effective_key_Appor_value = request.POST.get(Effective_key_Appor)

                                        Eff_Appor = get_object_or_404(Effective_Indicators_Master,id=Eff_Appor_ID_Value, IsDelete=False)
                                        Eff_Appor_Status = False
                                        if Effective_key_Appor_value == "1":
                                            Eff_Appor_Status = True
                                        Eff_data_Appor  = Effective_Indicators_Details_Appraisor.objects.create(CreatedBy = UserID,Entry_Master=padp,Objective_Master_id=obj_data.id,Effective_Indicators_Master = Eff_Appor,Status = Eff_Appor_Status)


                                    #  APPRAISOR Ineffective    
                                    total_Ineffective_key_Appor=f'obj_{obj}_Total_Ineffective_Appor'
                                    total_Ineffective_key_Count_Appor = int(request.POST.get(total_Ineffective_key_Appor))
                                    for  Ineffective_key_Appor in range(total_Ineffective_key_Count_Appor+1):
                                        Ineff_Appor_ID=f'Ine_{Ineffective_key_Appor}_obj_{obj}_Appor_ID'
                                        Ineff_Appor_ID_Value = request.POST.get(Ineff_Appor_ID)
                                        
                                        Ineffective_key_Appor = f'Ine_{Ineffective_key_Appor}_obj_{obj}_Appor'
                                        Ineffective_key_Appor_value = request.POST.get(Ineffective_key_Appor)
                                        
                                        
                                        Inff_Appor = get_object_or_404(Ineffective_Indicators_Master,id=Ineff_Appor_ID_Value, IsDelete=False)
                                        Inf_Appor_Status = False
                                        if Ineffective_key_Appor_value == "1":
                                            Inf_Appor_Status = True
                                        Inff_data_Appor  = Ineffective_Indicators_Details_Appraisor.objects.create(CreatedBy = UserID,Entry_Master=padp,Objective_Master_id=obj_data.id,Ineffective_Indicators_Master = Inff_Appor,Status = Inf_Appor_Status )

                        # specific measureable
                        if Appraiser == 'Yes':
                                    SMAobj = SPECIFIC_MEASURABLE_ACHIEVABLE.objects.filter(Entry_Master=padp, IsDelete=False)
                                    
                                    if SMAobj:
                                        # If SMAobj exists, update as before
                                        objective_types = request.POST.getlist('objective_type[]')
                                        spec_ids = request.POST.getlist('spec_ids[]')
                                        spec_is_delete = request.POST.getlist('spec_is_delete[]')
                                        smart_goals = request.POST.getlist('smart_goal[]')
                                        action_steps = request.POST.getlist('action_steps[]')
                                        statuses = request.POST.getlist('status[]')

                                        processed_ids = set()

                                        try:
                                            with transaction.atomic():  # Ensure all database changes are committed or rolled back
                                                for i, obj_id in enumerate(objective_types):
                                                    goal = smart_goals[i] or ''
                                                    action = action_steps[i] or ''
                                                    status = statuses[i] or ''

                                                    # Fetch or create SPECIFIC_MEASURABLE_ACHIEVABLE
                                                    SPEC_MEA, created = SPECIFIC_MEASURABLE_ACHIEVABLE.objects.get_or_create(
                                                        Entry_Master=padp,
                                                        Objective_Master_id=obj_id,
                                                        defaults={'CreatedBy': UserID, 'ModifyBy': UserID}
                                                    )

                                                    # Process SPECIFIC_MEASURABLE_ACHIEVABLE_Details
                                                    if i < len(spec_ids):
                                                        detail_id = spec_ids[i]
                                                        is_delete = spec_is_delete[i]

                                                        if detail_id:  # Update existing record
                                                            ACHIEVABLE = SPECIFIC_MEASURABLE_ACHIEVABLE_Details.objects.filter(
                                                                id=detail_id,
                                                               
                                                            ).first()

                                                            if ACHIEVABLE:
                                                                if is_delete == "1":
                                                                    ACHIEVABLE.IsDelete = True
                                                                else:
                                                                    ACHIEVABLE.SPECIFIC_MEASURABLE_ACHIEVABLE = SPEC_MEA
                                                                    ACHIEVABLE.SMART_GOAL = goal or ''
                                                                    ACHIEVABLE.ACTION_STEPS = action or ''
                                                                    ACHIEVABLE.COMPLETION_DATE = status or ''
                                                                ACHIEVABLE.ModifyBy = UserID
                                                                ACHIEVABLE.save()
                                                                processed_ids.add(detail_id)
                                                        elif is_delete != "1":  # Create new record if not marked for deletion
                                                            SPECIFIC_MEASURABLE_ACHIEVABLE_Details.objects.create(
                                                                SPECIFIC_MEASURABLE_ACHIEVABLE=SPEC_MEA,
                                                                SMART_GOAL=goal or '',
                                                                ACTION_STEPS=action or '',
                                                                COMPLETION_DATE=status or '',
                                                                CreatedBy=UserID
                                                            )
                                        except Exception as e:
                                            # Log error for debugging
                                            print(f"Error occurred: {e}")

                                    else:
                                        # Else block: When SMAobj does not exist, create new entries
                                        objective_types = request.POST.getlist('objective_type[]')
                                        spec_ids = request.POST.getlist('spec_ID[]')
                                        spec_is_delete = request.POST.getlist('spec_is_delete[]')
                                        smart_goals = request.POST.getlist('smart_goal[]')
                                        action_steps = request.POST.getlist('action_steps[]')
                                        statuses = request.POST.getlist('status[]')

                                        processed_ids = set()

                                        try:
                                            with transaction.atomic():  # Ensure all database changes are committed or rolled back
                                                for i, obj_id in enumerate(objective_types):
                                                    goal = smart_goals[i] or ''
                                                    action = action_steps[i] or  '' 
                                                    status = statuses[i] or ''

                                                    # Create a new SPECIFIC_MEASURABLE_ACHIEVABLE entry
                                                    SPEC_MEA = SPECIFIC_MEASURABLE_ACHIEVABLE.objects.create(
                                                        Entry_Master=padp,
                                                        Objective_Master_id=obj_id,
                                                        CreatedBy=UserID,
                                                        ModifyBy=UserID
                                                    )

                                                    # Process SPECIFIC_MEASURABLE_ACHIEVABLE_Details based on conditions
                                                    if spec_ids:  # Check if spec_ids is not empty
                                                        detail_id = spec_ids[i] if i < len(spec_ids) else None
                                                        is_delete = spec_is_delete[i] if i < len(spec_is_delete) else None

                                                        if is_delete != "1" and detail_id:  # Only create new record if not marked for deletion and id exists
                                                            SPECIFIC_MEASURABLE_ACHIEVABLE_Details.objects.create(
                                                                SPECIFIC_MEASURABLE_ACHIEVABLE=SPEC_MEA,
                                                                SMART_GOAL=goal or '',
                                                                ACTION_STEPS=action or '',
                                                                COMPLETION_DATE=status or '',
                                                                CreatedBy=UserID
                                                            )
                                                        elif is_delete == "1" and detail_id:  # If marked for deletion, we skip creation
                                                            print(f"Skipping creation for spec_id {detail_id} as it is marked for deletion.")
                                                    
                                                    # Optionally, you can handle other edge cases or log as needed

                                        except Exception as e:
                                            # Log error for debugging
                                            print(f"Error occurred: {e}")

                    if UserType == "ceo" or HrAudit == "Yes":
                        
                        if Sal_data :        
                                DEFICIENT = False
                                BELOW_STANDARD = False
                                MEETS_EXPECTATION = False
                                # ABOVE_STANDARD = False
                                OUTSTANDING = False
                                E_KEY  =request.POST.get('E_KEY')
                                if E_KEY == "D":
                                    DEFICIENT = True
                                if E_KEY == "B":
                                    BELOW_STANDARD = True
                                if E_KEY == "M":
                                    MEETS_EXPECTATION = True
                                # if E_KEY == "A":
                                #     ABOVE_STANDARD = True
                                if E_KEY == "O":
                                    OUTSTANDING = True

                                NO_CORRECTION = False
                                SALARY_CORRECTION = False
                                PROMOTION = False
                                PROMOTION_WITH_INCREASE = False
                                S_KEY  =request.POST.get('S_KEY')
                                if S_KEY == "N":
                                    NO_CORRECTION = True
                                if S_KEY == "S":
                                    SALARY_CORRECTION = True
                                if S_KEY == "P":
                                    PROMOTION = True
                                if S_KEY == "PWI":
                                    PROMOTION_WITH_INCREASE = True

                                per_3 = False
                                per_5 = False
                                per_8 = False
                                per_10 = False

                            
                                if S_KEY == "3":
                                    per_3 = True
                                if S_KEY == "5":
                                    per_5 = True
                                if S_KEY == "8":
                                    per_8 = True
                                if S_KEY == "10":
                                    per_10 = True    

                                
                                FromPosition = ''
                                ToPosition = ''
                                FromSalary = 0
                                ToSalary = 0

                                if S_KEY == "S":
                                    FromSalary =  request.POST['FromSalary'] or 0
                                    ToSalary = request.POST['ToSalary'] or 0
                                if S_KEY == "P":    
                                    FromPosition = request.POST['FromPosition']
                                    ToPosition = request.POST['ToPosition']
                                if S_KEY == "PWI" :
                                    FromSalary =  request.POST['FromSalary'] or 0 
                                    ToSalary = request.POST['ToSalary'] or 0
                                
                                    FromPosition = request.POST['FromPosition']
                                    ToPosition = request.POST['ToPosition']   
                                
                                Sal_data.DEFICIENT = DEFICIENT 
                                Sal_data.BELOW_STANDARD = BELOW_STANDARD 
                                Sal_data.MEETS_EXPECTATION = MEETS_EXPECTATION
                                # Sal_data.ABOVE_STANDARD = ABOVE_STANDARD 
                                Sal_data.OUTSTANDING = OUTSTANDING 

                                Sal_data.NO_CORRECTION = NO_CORRECTION
                                Sal_data.per_3 = per_3
                                Sal_data.per_5 = per_5
                                Sal_data.per_8 = per_8
                                Sal_data.per_10 = per_10

                                Sal_data.SALARY_CORRECTION =  SALARY_CORRECTION
                                Sal_data.PROMOTION = PROMOTION
                                Sal_data.PROMOTION_WITH_INCREASE = PROMOTION_WITH_INCREASE
                                Sal_data.FromSalary =  FromSalary
                                Sal_data.ToSalary = ToSalary
                                Sal_data.FromPosition = FromPosition 
                                Sal_data.JustificationComments  =request.POST.get('JustificationComments') or '' 
                                Sal_data.ToPosition = ToPosition 
                                Sal_data.ModifyBy = UserID
                                Sal_data.save()
                        else:
                                DEFICIENT = False
                                BELOW_STANDARD = False
                                MEETS_EXPECTATION = False
                                # ABOVE_STANDARD = False
                                OUTSTANDING = False
                                E_KEY  =request.POST.get('E_KEY')
                                JustificationComments  =request.POST.get('JustificationComments') or '' 

                                
                                if E_KEY == "D":
                                    DEFICIENT = True
                                if E_KEY == "B":
                                    BELOW_STANDARD = True
                                if E_KEY == "M":
                                    MEETS_EXPECTATION = True
                                # if E_KEY == "A":
                                #     ABOVE_STANDARD = True
                                if E_KEY == "O":
                                    OUTSTANDING = True

                                NO_CORRECTION = False
                                SALARY_CORRECTION = False
                                PROMOTION = False
                                PROMOTION_WITH_INCREASE = False
                                S_KEY  =request.POST.get('S_KEY')
                                if S_KEY == "N":
                                    NO_CORRECTION = True
                                if S_KEY == "S":
                                    SALARY_CORRECTION = True
                                if S_KEY == "P":
                                    PROMOTION = True
                                if S_KEY == "PWI":
                                    PROMOTION_WITH_INCREASE = True

                                per_3 = False
                                per_5 = False
                                per_8 = False
                                per_10 = False

                            
                                if S_KEY == "3":
                                    per_3 = True
                                if S_KEY == "5":
                                    per_5 = True
                                if S_KEY == "8":
                                    per_8 = True
                                if S_KEY == "10":
                                    per_10 = True    
                                
                                FromPosition = ''
                                ToPosition = ''
                                FromSalary = 0
                                ToSalary = 0

                                if S_KEY == "S":
                                    FromSalary =  request.POST['FromSalary'] or 0
                                    ToSalary = request.POST['ToSalary'] or 0
                                if S_KEY == "P":    
                                    FromPosition = request.POST['FromPosition']
                                    ToPosition = request.POST['ToPosition']
                                if S_KEY == "PWI" :
                                    FromSalary =  request.POST['FromSalary'] or 9
                                    ToSalary = request.POST['ToSalary'] or 0
                                
                                    FromPosition = request.POST['FromPosition']
                                    ToPosition = request.POST['ToPosition']    
            

                                FI_PER_RAT  =  FINAL_PERFORMANCE_RATING.objects.create(
                                    CreatedBy=UserID,Entry_Master=padp,
                                    DEFICIENT = DEFICIENT ,
                                    BELOW_STANDARD = BELOW_STANDARD ,
                                    MEETS_EXPECTATION = MEETS_EXPECTATION,
                                    # ABOVE_STANDARD = ABOVE_STANDARD ,
                                    OUTSTANDING = OUTSTANDING ,
                                    
                                    NO_CORRECTION = NO_CORRECTION,
                                    per_3 = per_3,
                                    per_5 = per_5,
                                    per_8 = per_8,
                                    per_10 = per_10,
                                    JustificationComments = JustificationComments,

                                    SALARY_CORRECTION =  SALARY_CORRECTION,
                                    PROMOTION = PROMOTION,
                                    PROMOTION_WITH_INCREASE = PROMOTION_WITH_INCREASE,
                                    FromSalary =  FromSalary,
                                    ToSalary = ToSalary,
                                    FromPosition = FromPosition ,
                                    ToPosition = ToPosition,
                                )
                else:
                    btn_value =   request.POST['btn_value']
                    padp_Emp_Code = request.POST['padp_Emp_Code'] 
                    # EmployeeOrganizationID = 1
                    EmployeeOrganizationID = request.POST['EmployeeOrganizationID'] 
                  
                    HRManager_name =request.POST['HRManager']

                    Appraisee_Name =request.POST['Appraisee_Name']
                    CurrentSalary =request.POST['CurrentSalary']
                    Aprraisee_position = request.POST['Aprraisee_position']
                    Aprraisee_Department = request.POST['Aprraisee_Department']
                    Date_Joined_Company = request.POST['Date_Joined_Company']
                    Appraisor_Name =request.POST['Appraisor_Name']
                    Appraisor_Title  = request.POST['Appraisor_Title']
                    FromReviewDate =request.POST['FromReviewDate']
                    ToReviewDate = request.POST['ToReviewDate']
                    Aprraise_Level = request.POST['Aprraise_Level']
                    SUMMARY_APPRAISEE = request.POST.get('SUMMARY_APPRAISEE') or ''
                    SUMMARY_APPRAISOR = request.POST.get('SUMMARY_APPRAISOR') or ''
                    DottedLine  = request.POST.get('DottedLine') or ''
                    Appraisee_ACK = request.POST.get('Appraisee_ACK') or ''
                    Appraisor_ACK = request.POST.get('Appraisor_ACK') or ''
                    HR_Manager_ACK = request.POST.get('HR_Manager_ACK') or ''
                    Appraisor_Mgr_ACK= request.POST.get('Appraisor_Mgr_ACK') or ''
                    Anticipated_Date = request.POST.get('Anticipated_Date')  or  None
                    Position_ACK = request.POST.get('Position_ACK') or ''
                    Alternative_Position = request.POST.get('Alternative_Position') or ''
                
                    EN_Master = Entry_Master.objects.create(OrganizationID=OrganizationID,CreatedBy=UserID,ToReviewDate=ToReviewDate,Appraisee_Name=Appraisee_Name,EmployeeOrganizationID=EmployeeOrganizationID,Aprraisee_position=Aprraisee_position,Date_Joined_Company=Date_Joined_Company,Appraisor_Name=Appraisor_Name,Appraisor_Title=Appraisor_Title,FromReviewDate=FromReviewDate,ReportingtoDesigantion = Appraisor_Title,EmployeeCode =  padp_Emp_Code,Aprraise_Level = Aprraise_Level, CreatedByUsername=UserName,DottedLine=DottedLine,
                    AuditedBy=UserID, AuditedBy_Name=UserName, HR_Manager_Name=HRManager_name, Current_Salary=CurrentSalary, Department=Aprraisee_Department)

                    hops_id = str(EN_Master.id) or 0

                    Send_Live_Notification(
                        organization_id=OrganizationID,
                        EmpCode=padp_Emp_Code,
                        title=f"New PADP is created",
                        message=f"The PADP for {Appraisee_Name} has been successfully audited by HR and is now available for your review.",
                        module_name="PADP",
                        action="Created",
                        hopsId=hops_id,
                        user_type="admin",
                        priority="high"
                    )

                    Entry_Master_Log.objects.create(
                        Entry_Master = EN_Master,
                        LastApporvalStatus = EN_Master.LastApporvalStatus,
                        hr_as = EN_Master.hr_as,
                        ep_as = EN_Master.ep_as,
                        ar_as = EN_Master.ar_as,
                        rd_as = EN_Master.rd_as,
                        hr_ar = EN_Master.hr_ar,
                        ceo_as = EN_Master.ceo_as,
                        ceo_as_remarks = EN_Master.ceo_as_remarks,
                        hr_actionOnDatetime = EN_Master.hr_actionOnDatetime,
                        ep_actionOnDatetime = EN_Master.ep_actionOnDatetime,
                        ar_actionOnDatetime = EN_Master.ar_actionOnDatetime,
                        rd_actionOnDatetime = EN_Master.rd_actionOnDatetime,
                        hr_ar_actionOnDatetime = EN_Master.hr_ar_actionOnDatetime,
                        ceo_actionOnDatetime = EN_Master.ceo_actionOnDatetime,
                        OrganizationID = EN_Master.OrganizationID,
                        CreatedByUsername = EN_Master.CreatedByUsername,
                        CreatedBy = EN_Master.CreatedBy,
                    )
        
                    if btn_value == "1":
                        EN_Master.hr_as = "Submitted"
                    else:
                        EN_Master.hr_as = "Draft"
                        EN_Master.DraftBy = "Draft"
                        EN_Master.DraftByName = "Draft"
                        EN_Master.LastApporvalStatus = "Draft"
                        EN_Master.DraftByDateTime = datetime.datetime.now()   
                        
                    EN_Master.hr_actionOnDatetime = datetime.datetime.now()   

                    if str(Departmentsession) =='hr':
                        EN_Master.Hr_Status =  btn_value

                    EN_Master.save()
                    
                    SP_GM_Rating_Excellent = False
                    # SP_GM_Rating_Good = False
                    SP_GM_Rating_Average = False
                    SP_GM_Rating_Poor = False
                    SP_GM_Rating_Needs_Improvement = False
                    spgm = request.POST.get('spgm')
                

                    if spgm == "E":
                        SP_GM_Rating_Excellent=True
                    # if spgm == "G":
                    #     SP_GM_Rating_Good= True
                    if spgm == "A":
                        SP_GM_Rating_Average= True
                    if spgm == "P":
                        SP_GM_Rating_Poor= True
                    if spgm == "N":
                        SP_GM_Rating_Needs_Improvement= True
                    SP_GM_Comment  = request.POST.get('SP_GM_Comment') or '' 
                    RD_Rating_Excellent = False
                    # RD_Rating_Good = False
                    RD_Rating_Average = False
                    RD_Rating_Poor = False
                    RD_Rating_Needs_Improvement = False
                    rdr  = request.POST.get('rdr')
                    if rdr == "E":
                        RD_Rating_Excellent=True
                    # if rdr == "G":
                    #     RD_Rating_Good= True
                    if rdr == "A":
                        RD_Rating_Average= True
                    if rdr == "P":
                        RD_Rating_Poor= True
                    if rdr == "N":
                        RD_Rating_Needs_Improvement= True    
                    RD_Comment  = request.POST.get('RD_Comment')     or ''      

                    sum_and_ack = SUMMARY_AND_ACKNOWLEDGEMENT.objects.create(
                        CreatedBy=UserID,
                        Entry_Master=EN_Master,
                        SUMMARY_APPRAISEE = SUMMARY_APPRAISEE,
                        SUMMARY_APPRAISOR = SUMMARY_APPRAISOR,
                        Appraisee = Appraisee_ACK ,
                        Appraisor = Appraisor_ACK,
                        HR_Manager = HR_Manager_ACK, 
                        Appraisor_Mgr =  Appraisor_Mgr_ACK,
                        Anticipated_promotionffransfer_Date = Anticipated_Date,
                        Position = Position_ACK,
                        Alternative_Position = Alternative_Position,
                        SP_GM_Rating_Excellent = SP_GM_Rating_Excellent,
                        # SP_GM_Rating_Good = SP_GM_Rating_Good,
                        SP_GM_Rating_Average = SP_GM_Rating_Average,
                        SP_GM_Rating_Poor = SP_GM_Rating_Poor,
                        SP_GM_Rating_Needs_Improvement = SP_GM_Rating_Needs_Improvement,
                        SP_GM_Comment =SP_GM_Comment,
                        RD_Rating_Excellent = RD_Rating_Excellent,
                        # RD_Rating_Good = RD_Rating_Good,
                        RD_Rating_Average = RD_Rating_Average,
                        RD_Rating_Poor = RD_Rating_Poor,
                        RD_Rating_Needs_Improvement = RD_Rating_Needs_Improvement,
                        RD_Comment = RD_Comment
                    )

                if Page == "PADPERDC":
                    return redirect('PADPERDC')
                 
                if Page == "PADPApprove":
                    return redirect('PADPApprove')
                
                if Page == "Userinfo":
                    return redirect(f'/PADP/Userinfo?EmpCode={EmpCode}&EmpID={EmpID}')
    
    # print("Nokra_message", Nokra_message)  
    Get_HR_ManagerList = Get_HR_Manager_list(OrganizationID) or ''
    # Get_DottedLine_Name = Get_DottedLine_Name_ByDesignation()

    # print("the new ctc is here:", NewCTC)
    context ={
        'padp_id':padp_id,
        'objs':objs,
        'padp':padp,
        'sum_data':sum_data,
        'Sal_data':Sal_data,
        'Hide':Hide,
        'Datafrom':Datafrom,
        'Appraiser':Appraiser,
        'SessionDesignation':SessionDesignation,
        'HR_ManagerName':HR_ManagerName,
        'SessionDottedLine':SessionDottedLine,
        'PadpDottedLine':PadpDottedLine   ,
        'UserType':UserType    ,
        'MergedDesignationsFrom':MergedDesignationsFrom , 
        'MergedDesignationsTo':MergedDesignationsTo,
        'rowslist':rowslist,
        'columns': columns, 
        'Departmentsession':Departmentsession,
        'OverallRating':OverallRating , 
        'SPE_MEA_ACH_Detail':SPE_MEA_ACH_Detail, 
        'orgs':orgs,
        'selectedOrganizationID' :selectedOrganizationID ,
        'HrAudit':HrAudit,
        'Nokra_message':Nokra_message,   
        'ep_submitted':ep_submitted,
        'SessionEmployeeCode':SessionEmployeeCode,
        'Get_HR_ManagerList':Get_HR_ManagerList,
        'EmpID': EmpID if EmpID else None,
        'EmpCode': EmpCode if EmpCode else Empobj.EmployeeCode,
        'UserOID':UserOID,
        'NewCTC':NewCTC,
        'Page':Page
    }
    return render(request,"PADPAPP/PADP/PADP_Add.html",context)       

from HumanResources.models import EmployeePersonalDetails, EmployeeWorkDetails
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse

def Refresh_MangerLevel_View(request, apadp_id):
    try:
        # print("the padp id is here::", apadp_id)
        PADPData = Entry_Master.objects.get(id=apadp_id)

        OrganizationID = PADPData.OrganizationID
        EmployeeCode = PADPData.EmployeeCode
        # print("the padp OrganizationID is here::", OrganizationID)
        # print("the padp EmployeeCode is here::", EmployeeCode)

        EmployeePersonalDetailsIDFromCode = EmployeePersonalDetails.objects.filter(
            EmployeeCode=EmployeeCode,
            OrganizationID=OrganizationID,
            IsDelete=0
        ).first()

        if EmployeePersonalDetailsIDFromCode is None:
        # Handle the case where employee personal details were not found
            return HttpResponse("Error: Employee personal details not found.", status=404)
        
        EmpID = EmployeePersonalDetailsIDFromCode.EmpID

        
        NewCTC = 0
        if EmpID is not None:
            # print("empid  found")
            ctc_salary_details = Salary_Detail_Master.objects.filter(
                Salary_title__Title='CTC (A+C)', IsDelete=False,
                OrganizationID=OrganizationID, EmpID=EmpID
            ).order_by('-id').first()

            if ctc_salary_details:
                # print("the function is here")
                NewCTC = ctc_salary_details.Permonth
            else:
                NewCTC=0
                # print("the function is not found")
        else:
            print("empid not found at Refresh_MangerLevel_View")
            # NewCTC=0

        EmployeeWorkDetails2 = EmployeeWorkDetails.objects.filter(
            EmpID=EmpID,
            IsDelete=0,
            IsSecondary=0
        ).first()

        if EmployeeWorkDetails2 is None:
            return HttpResponse("Error: Employee work details not found.", status=404)
        

        EmpCodedetails = EmployeeDetailsData(EmpID, OrganizationID)
        Appraisor_Name =PADPData.Appraisor_Name
        Refresh_Appraisor_Name =''
        
        empa = EmployeeDetailsDataFromDesignation(EmployeeWorkDetails2.ReportingtoDesignation,OrganizationID)

        if empa is not None:
            Refresh_Appraisor_Name= empa.FirstName + ' ' +empa.MiddleName + ' '+empa.LastName 
    
        # print("empa:",empa)
        # print("ReportingtoDesignation:",EmployeeWorkDetails2.ReportingtoDesignation)
        # print("Appraisor_Name:",Appraisor_Name)
        
        PADPData.Appraisee_Name = EmpCodedetails.full_name
        PADPData.Current_Salary = EmployeeWorkDetails2.Salary if EmployeeWorkDetails2.Salary else NewCTC
        
        if EmployeeWorkDetails2.Designation:
            PADPData.Aprraisee_position = EmployeeWorkDetails2.Designation

        if EmployeeWorkDetails2.Level:
            PADPData.Aprraise_Level = EmployeeWorkDetails2.Level

        if EmployeeWorkDetails2.ReportingtoDesignation:
            PADPData.Appraisor_Title = EmployeeWorkDetails2.ReportingtoDesignation

        PADPData.Appraisor_Name = Refresh_Appraisor_Name

        # DottedLine =EmployeeWorkDetails2.DottedLine
        if EmployeeWorkDetails2.DottedLine:
            PADPData.DottedLine=EmployeeWorkDetails2.DottedLine

        PADPData.save()

        return redirect(f'/PADP/PADP_Add/?Page=PADPApprove&ID={apadp_id}')

    except ObjectDoesNotExist as e:
        print("Data not found:", e)
        return HttpResponse("Error: Required employee data not found.", status=404)

    except MultipleObjectsReturned as e:
        print("Multiple records found when only one expected:", e)
        return HttpResponse("Error: Multiple employee records found. Please contact admin.", status=500)

    except Exception as e:
        print("An unexpected error occurred:", e)
        return HttpResponse("An unexpected error occurred. Please contact support.", status=500)  