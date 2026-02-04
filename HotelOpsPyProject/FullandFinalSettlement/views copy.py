from HumanResources.models import EmployeeWorkDetails,EmployeePersonalDetails, SalaryTitle_Master, Salary_Detail_Master, EmployeeBankInformationDetails
from Leave_Management_System.models import Leave_Type_Master, Emp_Leave_Balance_Master, EmpMonthLevelCreditMaster, EmpMonthLevelDebitMaster, Leave_Application
# from django.db.models import Sum, F, Value, DecimalField, Coalesce, Subquery, OuterRef, Sum
from django.db.models import Sum, Sum
from UniformInventory.models import UniformDetails, UniformInformation, UniformItemMaster 
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from AdvanceSalaryForm.models import AdvanceSalaryForm
from EmpResignation.models import EmpResigantionModel
from HumanResources.views import EmployeeDetailsData
from django.template.loader import get_template
from datetime import datetime, date, timedelta
from Employee_Payroll.models import SalarySlip
from django.shortcuts import render, redirect
from decimal import Decimal, InvalidOperation
from .models import Full_and_Final_Settltment
from hotelopsmgmtpy.utils import encrypt_id
from app.models import OrganizationMaster   
from app.models import DepartmentMaster
from app.views import OrganizationList
from django.http import HttpResponse
from django.db import   transaction
from urllib.parse import urlencode
from requests import Session, post
from django.contrib import messages
from django.db import connection
from django.urls import reverse
from xhtml2pdf import pisa
from io import BytesIO
from .models import *
from . import forms
import json
import re
# from django.shortcuts import render,
# from django.shortcuts import render,redirect
# from django.shortcuts import render, redirect


def FullandFinalDelete(request):
       if 'OrganizationID' not in request.session:
                return redirect(MasterAttribute.Host)
       EmpID = request.GET.get('EmpID')
       OrganizationID = request.session["OrganizationID"]
       OID  = request.GET.get('OID')
       if OID:
            OrganizationID= OID
       UserID = request.session["UserID"]
       EmpCode = request.GET.get('EC')
       ID = request.GET.get('FID')
       if ID is not None:
           
       
            Final = Full_and_Final_Settltment.objects.filter(id=ID,IsDelete=False,OrganizationID=OrganizationID).first()
            Final.IsDelete=True
            Final.ModifyBy  = UserID
            Final.save()
            Success = 'Deleted'        
            encrypted_id = encrypt_id(EmpID)
            url = reverse('FullandFinal')  
            redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
            return redirect(redirect_url)  
            

def FullandFinalPdfView(request):
     if 'OrganizationID' not in request.session:
                return redirect(MasterAttribute.Host)
     EmpID = request.GET.get('EmpID')
     OrganizationID = request.session["OrganizationID"]
     OID  = request.GET.get('OID')
     if OID:
            OrganizationID= OID
    
     id = request.GET["FID"]
     base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
     organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
     organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
   
     organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
     organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    
     template_path = "final/FullandFinalView.html"
     get_data =Full_and_Final_Settltment.objects.get(id=id)
    
     today = date.today() 
     print("today:", today)
     mydict={
        'Ed':get_data,
        'organization_logos':organization_logos,
        'organization_logo':organization_logo,
        'today':today,
        }

    
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'filename="report gcc club.pdf"'
     template = get_template(template_path)
     html = template.render(mydict)

     result = BytesIO()
     pdf  = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
     if not pdf.err:
        return HttpResponse(result.getvalue(), content_type = 'application/pdf')
     return None 



# from django.db.models import Subquery, OuterRef
# from HumanResources.models import EmployeePersonalDetails

@transaction.atomic()
def FullandFinalList(request): 
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
     
    OrganizationID = request.session["OrganizationID"]
    
    UserID = str(request.session["UserID"])
    if UserID == '20201212180048':
        OrganizationID = 501

    memorg = OrganizationList(OrganizationID=OrganizationID)
    I = request.GET.get('I', OrganizationID)
    D = request.GET.get('D', '')

    depts = DepartmentMaster.objects.filter(IsDelete=False)

    # Fetch Full and Final records
    fanfs = Full_and_Final_Settltment.objects.filter(
        OrganizationID=I, IsDelete=False
    ).order_by('-CreatedDateTime')
    
    if D != '':
        fanfs = fanfs.filter(Dept=D)

    # Build a mapping from EmployeeCode -> EmpID
    emp_map = {
        emp.EmployeeCode: emp.EmpID
        for emp in EmployeePersonalDetails.objects.filter(
            IsDelete=False, OrganizationID=OrganizationID
        )
    }

    # Attach EmpID manually
    for obj in fanfs:
        obj.EmpID_Resolved = emp_map.get(obj.Emp_Code, None)

    context = {
        'fanfs': fanfs,
        'memorg': memorg,
        'I': I,
        'depts': depts,
        'D': D
    }

    return render(request, 'final/FullandFinalList.html', context)




def extract_notice_days(notice_period_str):
    if not notice_period_str:
        return 0  # Default if string is empty or None

    notice_period_str = notice_period_str.strip().lower()

    # Match patterns like "15 days", "1 month", "2 months", "negotiated notice period 1 month"
    days_match = re.search(r'(\d+)\s*day', notice_period_str)
    months_match = re.search(r'(\d+)\s*month', notice_period_str)

    if days_match:
        return int(days_match.group(1))
    elif months_match:
        return int(months_match.group(1)) * 30  # Assuming 1 month = 30 days
    else:
        return 0  # If nothing matched


def safe_decimal(value):
    try:
        return Decimal(value) if value.strip() else Decimal(0)
    except (InvalidOperation, AttributeError):
        return Decimal(0)


from datetime import date

PL_RATE = 1.75

def count_months_opening_balance(start_date, end_date):
    """
    Count months for Opening Balance
    Rule: count joining month only if day <= 15
    """
    if start_date > end_date:
        return 0

    months = 0
    current = date(start_date.year, start_date.month, 1)

    while current <= end_date:
        # First month check (joining month)
        if current.year == start_date.year and current.month == start_date.month:
            if start_date.day <= 15:
                months += 1
        else:
            months += 1

        # move to next month
        if current.month == 12:
            current = date(current.year + 1, 1, 1)
        else:
            current = date(current.year, current.month + 1, 1)

    return months


def count_months_leave_earned(start_date, end_date):
    """
    Count months for Leave Earned (Current Year)
    Rule: count last month only if last working day >= 16
    """
    if start_date > end_date:
        return 0

    months = 0
    current = date(start_date.year, start_date.month, 1)

    while current <= end_date:
        # Last month check
        if current.year == end_date.year and current.month == end_date.month:
            if end_date.day >= 16:
                months += 1
        else:
            months += 1

        # move to next month
        if current.month == 12:
            current = date(current.year + 1, 1, 1)
        else:
            current = date(current.year, current.month + 1, 1)

    return months


def FullandFinalEntry(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
   
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID
    UserID = request.session["UserID"]
   
    EmpID = request.GET.get('EmpID')
    EmpCode = request.GET.get('EC')
    ID = request.GET.get('FID')

    if ID:
        FieldShow = 'Show' 
        # print("FieldShow Is Here::", FieldShow)
    else:
        FieldShow = 'Hide' 
        # print("FieldShow Is Here::", FieldShow)

   
    # EmpID = request.GET.get('EmpID')
    # EmpCode = '049'
    # ID = request.GET.get('FID')
    # Page = request.GET.get('page')
    Page = request.GET.get("Page")

    # print("page value::", Page)
    # print("PageType value::", PageType)
    # print("page value::", request.GET.get("Page"))
    if not EmpID:
        EmpIDobj  =EmployeePersonalDetails.objects.filter(IsDelete=False,OrganizationID=OrganizationID,EmployeeCode=EmpCode).first() 
        if EmpIDobj:
            EmpID = EmpIDobj.EmpID
   
    Fobj = None
    DataFromFobj = None

    # print("Checking EmpDetails for EmpID:", EmpID, "OrgID:", OrganizationID,  "EmpCode:", EmpCode)

    if EmpCode is not None:
        # EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
        try:
            EmpDetails = EmployeeDetailsData(EmpID, OrganizationID)
        except Exception as e:
            return HttpResponse(f"Error retrieving employee details: {e}", status=500)

        if not EmpDetails:
            # You can show a friendly error or redirect or handle default values
            return HttpResponse(
                f"Employee master data not found for EmpID={EmpID}, OrgID={OrganizationID}.", status=404
            )

        EmpDetailsObj = {
            'Emp_Code': EmpDetails.EmployeeCode,
            'Name': f"{EmpDetails.FirstName} {EmpDetails.MiddleName} {EmpDetails.LastName}",
            'Dept': EmpDetails.Department,
            'Designation': EmpDetails.Designation,
            'DOJ': EmpDetails.DateofJoining,
            'Tenure':EmpDetails.tenure_till_today,
            # 'EmpStatus':EmpDetails.EmpStatus
            'EmpStatus': EmpDetails.EmpStatus,
        }

        if ID is not None:
            Fobj = Full_and_Final_Settltment.objects.filter(OrganizationID=OrganizationID,IsDelete=False,id=ID).first()
           
        if Fobj is not None:
            DataFromFobj = 'DataFromFobj'
        else:
            DataFromFobj = 'DataFromFobjHR'

    if request.method == "POST":
        if DataFromFobj == "DataFromFobj" and ID:    

            # print("Submitted Auditor value:", request.POST.get("Auditor"))
            # Employee Details
            Fobj.Name = request.POST.get('employeeName') or None
            Fobj.Emp_Code = request.POST.get('employeeCode') or None
            Fobj.DOJ = request.POST.get('joiningDate') or None
            Fobj.Date_Of_Leaving = request.POST.get('LeavingDate') or None
            Fobj.Dept = request.POST.get('Department') or None
            Fobj.Designation = request.POST.get('Designation') or None
            Fobj.Emp_Resignation_Date = request.POST.get('Emp_Resignation_Date') or None
            Fobj.EmpStatus = request.POST.get('EmpStatus') or None

            # print("Submitted EmpStatus value:", request.POST.get("EmpStatus"))
            # print("Submitted Emp_Resignation_Date value:", request.POST.get("Emp_Resignation_Date"))

            Fobj.Leave_PL_From_Date=request.POST.get('From_Date') or None
            Fobj.Leave_PL_To_Date=request.POST.get('To_Date') or None

            # Exit Reason Flags
            Fobj.Absconding = request.POST.get('Absconding') or None
            Fobj.Resignation = request.POST.get('Resignation') or None
            Fobj.Notice_Days_Served = request.POST.get('Notice_Days_Served') or None
            Fobj.Confirmed = request.POST.get('Confirmed') or None
            Fobj.Terminated = request.POST.get('Terminated') or None
            Fobj.Laid_Off = request.POST.get('Laid_Off') or None
            Fobj.Deduction_from_salary_PL_Boolean = request.POST.get('Deduction_from_salary_PL') or None # new 

            # Salary & Leave
            # Fobj.Deduction_from_salary_PL = request.POST.get('Deduction_from_salary_PL')
            # Salary & Leave
            Fobj.Current_Salary = safe_decimal(request.POST.get('Current_Salary')) or None
            Fobj.PL_Basic_Salary = safe_decimal(request.POST.get('PL_Basic_Salary')) or None
            Fobj.NPP_Gross = safe_decimal(request.POST.get('NPP_Gross')) or None

            # Leave Summary
            Fobj.LS_Opening_Balance = safe_decimal(request.POST.get('LS_Opening_Balance')) or None
            Fobj.LS_Leaved_Earned = safe_decimal(request.POST.get('LS_Leaved_Earned')) or None
            Fobj.LS_Leaved_Availed = safe_decimal(request.POST.get('LS_Leaved_Availed')) or None
            Fobj.LS_PL_Bal = safe_decimal(request.POST.get('LS_PL_Bal')) or None

            # Other Earnings & Deductions
            Fobj.LTA_Amount = safe_decimal(request.POST.get('LTAAmount')) or None
            Fobj.Other_Earnings = safe_decimal(request.POST.get('OtherEarnings')) or None
            Fobj.Total_Earning = safe_decimal(request.POST.get('TOTALEARNING')) or None

            Fobj.OtherDeductions = safe_decimal(request.POST.get('OtherDeductions')) or None
            Fobj.Notice_Period_Deductions = safe_decimal(request.POST.get('NOTICEPERIODDeductions')) or None
            Fobj.Advance_Salary = safe_decimal(request.POST.get('AdvanceSalary')) or None

            Fobj.Total_Advance_Taken = safe_decimal(request.POST.get('TotalAdvanceTaken')) or None
            Fobj.Total_Advance_Paid = safe_decimal(request.POST.get('TotalAdvancePaid')) or None
            Fobj.Remaining_Amount = safe_decimal(request.POST.get('RemainingAmount')) or None

            # Leave Travel Entitlement
            Fobj.Total_Months_Worked = safe_decimal(request.POST.get('TOTALMONTHSWORKED')) or None
            Fobj.LTA_Rate = safe_decimal(request.POST.get('LTARATE')) or None
            Fobj.Total_Days_Worked = safe_decimal(request.POST.get('TOTALDAYSWORKED')) or None
            Fobj.Pro_Rata_Basis_Payment = safe_decimal(request.POST.get('PRORATABASISPAYMENT')) or None

            # PL Payment
            Fobj.PL_Total_PL = safe_decimal(request.POST.get('PL_Total_PL')) or None
            Fobj.PL_Rate = safe_decimal(request.POST.get('PL_Rate')) or None
            Fobj.PL_Amount = safe_decimal(request.POST.get('PL_Amount')) or None
            Fobj.Total_PL_Balance = safe_decimal(request.POST.get('TotalPLBalance')) or None


            # Notice Period Pay
            Fobj.NPP_Total_Notice_Pay_Days = safe_decimal(request.POST.get('NPP_Total_Notice_Pay_Days')) or None
            Fobj.NPP_Rate = safe_decimal(request.POST.get('NPP_Rate')) or None
            Fobj.NPP_Net_Amount_Paid = safe_decimal(request.POST.get('NPP_Net_Amount_Paid')) or None

            # Gratuity Payment
            Fobj.GP_No_Of_Years = safe_decimal(request.POST.get('GP_No_Of_Years')) or None
            Fobj.GP_Last_Basics = safe_decimal(request.POST.get('GP_Last_Basics')) or None
            Fobj.GP_Graturity_Days = safe_decimal(request.POST.get('GraturityDaysPeryear')) or None
            Fobj.GP_Graturity_Payments = safe_decimal(request.POST.get('GP_Graturity_Payments')) or None

            # Final Payment Summary
            Fobj.FFPS_Pending_Salary = safe_decimal(request.POST.get('PendingSalary')) or None
            Fobj.FFPS_PL = safe_decimal(request.POST.get('FinalPLPaymentAmount')) or None
            Fobj.FFPS_Gratuity = safe_decimal(request.POST.get('FinalGraturityPayments')) or None
            Fobj.FFPS_Grand_Total = safe_decimal(request.POST.get('FFPS_Payable_Amount')) or None
            Fobj.Employee_PF_Amount = safe_decimal(request.POST.get('EmployeePFAmount')) or None
            Fobj.PT_Amount = safe_decimal(request.POST.get('PTAmount')) or None
            

            Fobj.FFPS_Deductions = safe_decimal(request.POST.get('TotalDeductions')) or None
            Fobj.FFPS_Uniform_Deductions = safe_decimal(request.POST.get('FinalUniformDeductions')) or None

            # Status
            Fobj.AuditedByHR = request.POST.get('AuditedByHR') or None # new Done 
            Fobj.AuditedByFinance = request.POST.get('AuditedByFinance') or None # new Done 
            Fobj.AuditedByGM = request.POST.get('AuditedByGM') or None # new Done 
            Fobj.PaymentStatus = request.POST.get('PaymentStatus') or None # new Done 
            Fobj.FinalStatus = request.POST.get('FinalStatus') or None # new Done 
            Fobj.AuditedBy_Auditor = request.POST.get('Auditor') or None # new Done 


            # Remarks
            Fobj.LTA_Remarks= request.POST.get('LTARemarks') or None
            Fobj.Final_PL_Payment_Remarks= request.POST.get('PLPaymentRemarks') or None
            Fobj.Graturity_Payments_Earning_Remarks=request.POST.get('GraturityPaymentsEarningRemarks') or None
            Fobj.Other_Earnings_Remarks=request.POST.get('OtherEarningsRemarks') or None
            Fobj.Pending_Salary_Remarks=request.POST.get('PendingSalaryRemarks') or None
            Fobj.Total_Earning_Remarks=request.POST.get('TOTALEARNINGRemarks') or None
            Fobj.Uniform_Deductions_Remarks=request.POST.get('UniformDeductionsRemarks') or None
            Fobj.Other_Deductions_Remarks=request.POST.get('OtherDeductionsRemarks') or None
            Fobj.Notice_Period_Deductions_Remarks=request.POST.get('NOTICEPERIODDeductionsRemarks') or None
            Fobj.Advance_Salary_Remarks=request.POST.get('AdvanceSalaryRemarks') or None
            Fobj.Total_Deductions_Remarks=request.POST.get('TotalDeductionsRemarks') or None
            Fobj.PT_Amount_Remarks=request.POST.get('PTAmountRemarks') or None
            Fobj.Employee_PF_Amount_Remarks=request.POST.get('EmployeePFAmountRemarks') or None
           
            # Fobj.PaymentRemarks=request.POST.get('PaymentRemarks'),
            Fobj.OrganizationID = OrganizationID
            Fobj.ModifyBy = UserID
            Fobj.ModifyDateTime = date.today()
            try:
                employee_work_details = EmployeeWorkDetails.objects.get(
                    EmpID=EmpID, OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False)
                employee_work_details.EmpStatus = "F&F In Completed"
                employee_work_details.ModifyBy = UserID
                employee_work_details.save()
            except EmployeeWorkDetails.DoesNotExist:
                print("EmployeeWorkDetails record not found.")

            # Fobj.save()

            try:
                Fobj.save()
            except Exception as e:
                print(f"Error Updating Full_and_Final_Settltment: {e}")
                return HttpResponse("An error occurred while saving the updating.", status=500)
           
            # after successful edit
            if Page == "FullandFinalList":
                params = {
                    'Success': 'True',
                    'action': 'edit',
                    'message': 'Full and Final Settlement updated successfully!'
                }
                url = f"{reverse('FullandFinalList')}?{urlencode(params)}"
                return redirect(url)
            
            EditSuccess = True
            encrypted_id = encrypt_id(EmpID)
            params = {
                'EmpID': encrypted_id,
                'OID': OrganizationID,
                'Success': 'True',
                'action': 'edit',
                'message': 'Full and Final Settlement updated successfully!'
            }
            url = f"{reverse('FullandFinal')}?{urlencode(params)}"
            return redirect(url)
        else:
            Fobj = Full_and_Final_Settltment(
                # Employee Details
                Name=request.POST.get('employeeName'),
                Emp_Code=request.POST.get('employeeCode'),
                DOJ=request.POST.get('joiningDate'),
                Date_Of_Leaving=request.POST.get('LeavingDate'),
                Dept=request.POST.get('Department'),
                Designation=request.POST.get('Designation'),

                EmpStatus=request.POST.get('EmpStatus'),
                Emp_Resignation_Date=request.POST.get('Emp_Resignation_Date'),


                # Exit Reason Flags
                Absconding=request.POST.get('Absconding'),
                Resignation=request.POST.get('Resignation'),
                Notice_Days_Served=request.POST.get('Notice_Days_Served'),
                Confirmed=request.POST.get('Confirmed'),
                Terminated=request.POST.get('Terminated'),
                Laid_Off=request.POST.get('Laid_Off'),
                Deduction_from_salary_PL_Boolean=request.POST.get('Deduction_from_salary_PL'),

                # Salary & Leave
                Current_Salary=safe_decimal(request.POST.get('Current_Salary')),
                PL_Basic_Salary=safe_decimal(request.POST.get('PL_Basic_Salary')),
                NPP_Gross=safe_decimal(request.POST.get('NPP_Gross')),

                # Leave Summary
                Leave_PL_From_Date=request.POST.get('From_Date'),
                Leave_PL_To_Date=request.POST.get('To_Date'),
                LS_Opening_Balance=safe_decimal(request.POST.get('LS_Opening_Balance')),
                LS_Leaved_Earned=safe_decimal(request.POST.get('LS_Leaved_Earned')),
                LS_Leaved_Availed=safe_decimal(request.POST.get('LS_Leaved_Availed')),
                LS_PL_Bal=safe_decimal(request.POST.get('LS_PL_Bal')),

                # Other Earnings & Deductions
                LTA_Amount=safe_decimal(request.POST.get('LTAAmount')),
                Other_Earnings=safe_decimal(request.POST.get('OtherEarnings')),
                Total_Earning=safe_decimal(request.POST.get('TOTALEARNING')),
                OtherDeductions=safe_decimal(request.POST.get('OtherDeductions')),
                Notice_Period_Deductions=safe_decimal(request.POST.get('NOTICEPERIODDeductions')),
                Advance_Salary=safe_decimal(request.POST.get('AdvanceSalary')),
                Total_Advance_Taken=safe_decimal(request.POST.get('TotalAdvanceTaken')),
                Total_Advance_Paid=safe_decimal(request.POST.get('TotalAdvancePaid')),
                Remaining_Amount=safe_decimal(request.POST.get('RemainingAmount')),
                Employee_PF_Amount = safe_decimal(request.POST.get('EmployeePFAmount')),
                PT_Amount = safe_decimal(request.POST.get('PTAmount')),

                # Bank Details
                Bank_Name=request.POST.get('BankName'),
                Branch_Name=request.POST.get('BranchName'),
                Accounts_Number=request.POST.get('AccountsNumber'),
                IFSCCode=request.POST.get('IFSCCode'),

                # Leave Travel Entitlement
                Total_Months_Worked=safe_decimal(request.POST.get('TOTALMONTHSWORKED')),
                LTA_Rate=safe_decimal(request.POST.get('LTARATE')),
                Total_Days_Worked=safe_decimal(request.POST.get('TOTALDAYSWORKED')),
                Pro_Rata_Basis_Payment=safe_decimal(request.POST.get('PRORATABASISPAYMENT')),

                # Remarks
                LTA_Remarks=request.POST.get('LTARemarks'),
                Final_PL_Payment_Remarks=request.POST.get('PLPaymentRemarks'),
                Graturity_Payments_Earning_Remarks=request.POST.get('GraturityPaymentsEarningRemarks'),
                Other_Earnings_Remarks=request.POST.get('OtherEarningsRemarks'),
                Pending_Salary_Remarks=request.POST.get('PendingSalaryRemarks'),
                Total_Earning_Remarks=request.POST.get('TOTALEARNINGRemarks'),
                Uniform_Deductions_Remarks=request.POST.get('UniformDeductionsRemarks'),
                Other_Deductions_Remarks=request.POST.get('OtherDeductionsRemarks'),
                Notice_Period_Deductions_Remarks=request.POST.get('NOTICEPERIODDeductionsRemarks'),
                Advance_Salary_Remarks=request.POST.get('AdvanceSalaryRemarks'),
                Total_Deductions_Remarks=request.POST.get('TotalDeductionsRemarks'),
                PT_Amount_Remarks=request.POST.get('PTAmountRemarks'),
                Employee_PF_Amount_Remarks=request.POST.get('EmployeePFAmountRemarks'),

                # PL Payment
                PL_Total_PL=safe_decimal(request.POST.get('PL_Total_PL')),
                PL_Rate=safe_decimal(request.POST.get('PL_Rate')),
                PL_Amount=safe_decimal(request.POST.get('PL_Amount')),
                Total_PL_Balance = safe_decimal(request.POST.get('TotalPLBalance')),


                # Notice Period Pay
                NPP_Total_Notice_Pay_Days=safe_decimal(request.POST.get('NPP_Total_Notice_Pay_Days')),
                NPP_Rate=safe_decimal(request.POST.get('NPP_Rate')),
                NPP_Net_Amount_Paid=safe_decimal(request.POST.get('NPP_Net_Amount_Paid')),
                Total_Notice_Days_Served=request.POST.get('TotalNoticeServed'),

                # Gratuity Payment
                GP_No_Of_Years=safe_decimal(request.POST.get('GP_No_Of_Years')),
                GP_Last_Basics=safe_decimal(request.POST.get('GP_Last_Basics')),
                GP_Graturity_Days=safe_decimal(request.POST.get('GraturityDaysPeryear')),
                GP_Graturity_Payments=safe_decimal(request.POST.get('GP_Graturity_Payments')),

                # Final Full & Final Pay
                FFPS_Pending_Salary=safe_decimal(request.POST.get('PendingSalary')),
                FFPS_PL=safe_decimal(request.POST.get('FinalPLPaymentAmount')),
                FFPS_Gratuity=safe_decimal(request.POST.get('FinalGraturityPayments')),
                FFPS_Grand_Total=safe_decimal(request.POST.get('FFPS_Payable_Amount')),
                FFPS_Deductions=safe_decimal(request.POST.get('TotalDeductions')),
                FFPS_Uniform_Deductions=safe_decimal(request.POST.get('FinalUniformDeductions')),

                
                # Status
                AuditedByHR = request.POST.get('AuditedByHR'), 
                AuditedByFinance = request.POST.get('AuditedByFinance'), 
                AuditedByGM = request.POST.get('AuditedByGM'),
                PaymentStatus = request.POST.get('PaymentStatus'), 
                FinalStatus = request.POST.get('FinalStatus'),
                AuditedBy_Auditor = request.POST.get('Auditor'),

                OrganizationID=OrganizationID,
                CreatedBy=UserID,
                CreatedDateTime=date.today()
            )
            try:
                Fobj.save()
                message = 'Full and Final Settlement Submited successfully!'
            except Exception as e:
                print(f"Error saving Full_and_Final_Settltment: {e}")
                Errormessage = "An error occurred while saving the data."
                return HttpResponse("An error occurred while saving the data.", status=500)

            encrypted_id = encrypt_id(EmpID)
            params = {
                'EmpID': encrypted_id,
                'OID': OrganizationID,
                'Success': 'True',
                'action': 'submit',
                'message': 'Full and Final Settlement Submited successfully!'
            }
            url = f"{reverse('FullandFinal')}?{urlencode(params)}"
            return redirect(url)


    # Other Data Sending to Template --->
        # Calculating PL balance and return type.
    Leave_Type_Masterdata_ID = Leave_Type_Master.objects.filter(Type="PL").values_list('id', flat=True).first()
    Leave_Balance_Master = Emp_Leave_Balance_Master.objects.filter(Leave_Type_Master=Leave_Type_Masterdata_ID, Emp_code=EmpCode, IsDelete=False, OrganizationID=OrganizationID).first()

    if Leave_Balance_Master:
        LeaveBalance = Leave_Balance_Master.Balance
    else:
        LeaveBalance = 0
    
    EmpMonthLevelCreditMaster_Data = EmpMonthLevelCreditMaster.objects.filter(Leave_Type_Master=Leave_Type_Masterdata_ID, Emp_code=EmpCode, IsDelete=False).first()

    if EmpMonthLevelCreditMaster_Data:
        PL_Every_Month_Credit = EmpMonthLevelCreditMaster_Data.credit
    else:
        PL_Every_Month_Credit = 0
    
    EmpMonthLevelDebitMaster_Data = EmpMonthLevelDebitMaster.objects.filter(Leave_Type_Master=Leave_Type_Masterdata_ID, Emp_code=EmpCode, IsDelete=False).first()
    if EmpMonthLevelDebitMaster_Data:
        PL_Every_Month_debit = EmpMonthLevelDebitMaster_Data.debit
    else:
        PL_Every_Month_debit = 0



    # Basic Salary
    basic_title_id = SalaryTitle_Master.objects.filter(Title="Basic", IsDelete=False, OrganizationID=OrganizationID).values_list('id', flat=True).first()

    if basic_title_id:
        basic_salary_data = Salary_Detail_Master.objects.filter(Salary_title=basic_title_id, IsDelete=False, EmpID=EmpID, OrganizationID=OrganizationID).first()
    else:
        basic_title_id=None
        print("No Basic Salary Id Found")

    BasicSalary = basic_salary_data.Permonth if basic_salary_data else 0

    # Gross (A) Salary
    gross_title_id = SalaryTitle_Master.objects.filter(Title="Gross (A)", IsDelete=False, OrganizationID=OrganizationID).values_list('id', flat=True).first()

    if gross_title_id:
        gross_salary_data = Salary_Detail_Master.objects.filter(Salary_title=gross_title_id, IsDelete=False, EmpID=EmpID, OrganizationID=OrganizationID).first()
    else:
        gross_title_id = None
        print("NO gross_title_id is Found")

    GrossSalary = gross_salary_data.Permonth if gross_salary_data else 0
    

    # PT Salary
    # PF_title_id = None
    PT_title_id = SalaryTitle_Master.objects.filter(Title="PT", IsDelete=False, OrganizationID=OrganizationID).values_list('id', flat=True).first()

    # PF_title_id
    PT_tax_data = None

    if PT_title_id:
        PT_tax_data = Salary_Detail_Master.objects.filter(Salary_title=PT_title_id, IsDelete=False, EmpID=EmpID, OrganizationID=OrganizationID).first()

        if not PT_tax_data:
            print(f"No Employer PF salary data found for EmpID {EmpID}")
    else:
        PT_title_id = None
        print("No PT_title_id found")

    PT_Tax = PT_tax_data.Permonth if PT_tax_data else 0

    # PF Salary
    # PF_title_id = None
    PF_title_id = SalaryTitle_Master.objects.filter(Title="Employee PF @12% (Basic)", IsDelete=False, OrganizationID=OrganizationID).values_list('id', flat=True).first()

    # PF_title_id = None
    PF_tax_data = None

    if PF_title_id:
        PF_tax_data = Salary_Detail_Master.objects.filter(Salary_title=PF_title_id, IsDelete=False, EmpID=EmpID, OrganizationID=OrganizationID).first()

        if not PF_tax_data:
            print(f"No Employer PF salary data found for EmpID {EmpID}")
    else:
        PF_title_id = None
        print("No PF_title_id Found")

    Employee_PF = PF_tax_data.Permonth if PF_tax_data else 0
    

    # NOTICE PERIOD PAY and Leave Summary To - LastWorkingDay Date
    EmpResignation_Data = EmpResigantionModel.objects.filter(
        IsDelete=False,
        Emp_Code=EmpCode,
        OrganizationID=OrganizationID
    ).first()

    if EmpResignation_Data:
        LastWorkingDaysDate = EmpResignation_Data.LastWorkingDays
        RawNoticePeriodDays = EmpResignation_Data.NoticePeriod
        NoticePeriodDays = extract_notice_days(RawNoticePeriodDays)
        # DateOfJoining = EmpResignation_Data.DOJ
    else:
        print("EmpResignation_Data Not Found")
        LastWorkingDaysDate = date.today()
        NoticePeriodDays = 0


    Workobj = EmployeeWorkDetails.objects.filter(OrganizationID=OrganizationID, IsDelete=False,IsSecondary=False, EmpID=EmpID).first()


    # Getting DateOfJoining and TenureTIllToday
    if Workobj:
        DateOfJoining = Workobj.DateofJoining
        TenureTillToday = Workobj.tenure_till_today()  

        # Extract number of years
        match = re.search(r'(\d+)\s+year', TenureTillToday)
        if match:
            TenureYears = int(match.group(1))
        else:
            TenureYears = 0  # If "year" is not mentioned (e.g., less than 1 year)

        # print("Extracted Years:", TenureYears)
    else:
        print("Workobj is not Found")
        DateOfJoining = None
        TenureTillToday = None
        TenureYears = 0
    
    GraturityPaymentMonthDays = 15
    GraturityDivideDays = 26

    if TenureYears == 5 or TenureYears > 5:
        GraturityPayments = (GraturityPaymentMonthDays * BasicSalary * TenureYears) / GraturityDivideDays
        GraturityPayments = round(GraturityPayments, 2)
    else:
        GraturityPayments = 0



    # Getting Bank Details
    BankDetailObj = EmployeeBankInformationDetails.objects.filter(OrganizationID=OrganizationID, IsDelete=False, EmpID=EmpID).first()

    if BankDetailObj:
        BankName = BankDetailObj.NameofBank or ''
        BankBranch = BankDetailObj.BankBranch or ''
        BankAccountNumber = BankDetailObj.BankAccountNumber or ''
        BankIFSCCode = BankDetailObj.IFSCCode or ''
    else:
        BankName = BankBranch = BankAccountNumber = BankIFSCCode = ''

    
    # Total Credit or Leave Availed between GIven Period
    total_credit = Leave_Application.objects.filter(
        Leave_Type_Master_id = Leave_Type_Masterdata_ID,
        OrganizationID=OrganizationID,
        Emp_code=EmpCode,
        # Emp_code=EmpCode,
        Start_Date__range=[DateOfJoining, LastWorkingDaysDate],
        Status=1,
        IsDelete=False
    ).aggregate(
        total_credit=Sum('Total_credit')
    )['total_credit'] or 0


    # Step 1: Get the UniformInformation object for the given employee
    UniformDeductions = 0
    Uniform_ID = 0

    UniformInformationdata = UniformInformation.objects.filter(
        OrganizationID=OrganizationID,
        IsDelete=False,
        EmployeeCode=EmpCode
    ).values('id', 'ReturnAmount').first()

    if UniformInformationdata:
        UniformDeductions = UniformInformationdata['ReturnAmount']
        Uniform_ID = UniformInformationdata['id']
    else:
        UniformDeductions = int(0)
        Uniform_ID = 0

    # Advance Salary Form Values: ----------->
    AdvanceSalaryFormData =  AdvanceSalaryForm.objects.filter(OrganizationID=OrganizationID, is_delete=False, emp_code=EmpCode)

    TotalAdvancePayment = 0
    if AdvanceSalaryFormData:
        for amount in AdvanceSalaryFormData:
            TotalAdvancePayment += amount.LoanAmount
    else:
        # print("AdvanceSalaryFormData not found")
        TotalAdvancePayment = 0


    # Salary Slip data:
    Salary_Slip_Data =  SalarySlip.objects.filter(OrganizationID=OrganizationID, IsDelete=False, EmployeeCode=EmpCode)
    
    TotalAmountPaid = 0
    if Salary_Slip_Data:
        for amount in Salary_Slip_Data:
            TotalAmountPaid += float(amount.AdvanceLoan)
    else:
        print("Salary_Slip_Data is not found")
        TotalAmountPaid = 0
        
        
    # ---------------------------------------- Pratice Leave Calculate
    current_year = LastWorkingDaysDate.year
    year_start = date(current_year, 1, 1)
    
    opening_months = 0
    opening_balance = 0

    if DateOfJoining and DateOfJoining < year_start:
        opening_end_date = year_start - timedelta(days=1)  # 31-12-previous year

        opening_months = count_months_opening_balance(
            DateOfJoining,
            opening_end_date
        )
        opening_balance = round(opening_months * PL_RATE, 2)

    earned_months = count_months_leave_earned(
        year_start,
        LastWorkingDaysDate
    )

    leave_earned = round(earned_months * PL_RATE, 2)

    total_pl_balance = round(opening_balance + leave_earned, 2)
    
    print('OpeningBalanceMonths:', opening_months)
    print('OpeningBalancePL:', opening_balance)
    print('LeaveEarnedMonths:', earned_months)
    print('LeaveEarnedPL:', leave_earned)
    print('TotalPLBalance:', total_pl_balance)
    
    # ---------------------------------------- Pratice End
    context = {
        'OrganizationID': OrganizationID, 
        'Fobj': Fobj, 
        'EmpDetailsObj':EmpDetailsObj,
        'BasicSalary':BasicSalary, 
        'GrossSalary':GrossSalary, 
        'PT_Tax':PT_Tax,
        'Employee_PF':Employee_PF,
        'LeaveBalance':LeaveBalance,
        'PL_Every_Month_Credit':PL_Every_Month_Credit,
        'PL_Every_Month_debit':PL_Every_Month_debit,
        'DateOfJoining':DateOfJoining,
        'LastWorkingDaysDate':LastWorkingDaysDate,
        'OpeningBalancePL': opening_balance,   # new
        'LeaveEarnedPL': leave_earned,         # new
        'TotalPLBalance': total_pl_balance,    # new
        'total_credit':total_credit,
        'NoticePeriodDays':NoticePeriodDays,
        # 'EmpResignation_Date':EmpResignation_Data.Date_Of_res if EmpResignation_Data.Date_Of_res else '',
        'EmpResignation_Date': getattr(EmpResignation_Data, 'Date_Of_res', ''),
        'EmpStatus':Workobj.EmpStatus if Workobj.EmpStatus else 'Not Resigned',
        'TenureYears':TenureYears,
        'GraturityPayments':GraturityPayments,
        'BankName':BankName,
        'BankBranch':BankBranch,
        'BankAccountNumber':BankAccountNumber,
        'BankIFSCCode':BankIFSCCode,
        'UniformDeductions':UniformDeductions,
        'Uniform_ID':Uniform_ID,
        'FieldShow':FieldShow,

        # Advance Salary:
        'TotalAdvancePayment':TotalAdvancePayment,
        'TotalAmountPaid':TotalAmountPaid,
    }
    return render(request, "final/FullandFinalEntry.html", context)
 

from datetime import datetime, timezone
from django.db import transaction
from django.shortcuts import render, redirect
from datetime import date

@transaction.atomic()
def FullAndFinal_Approval_List(request): 
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
     
    OrganizationID = request.session["OrganizationID"]
    
    UserID = str(request.session["UserID"])
    if UserID == '20201212180048':
        OrganizationID = 501

    memorg = OrganizationList(OrganizationID=OrganizationID)
    I = request.GET.get('I', OrganizationID)
    D = request.GET.get('D', '')

    depts = DepartmentMaster.objects.filter(IsDelete=False)

    # Fetch Full and Final records
    fanfs = Full_and_Final_Settltment.objects.filter(
        OrganizationID=I, IsDelete=False
    ).order_by('-CreatedDateTime')
    
    if D != '':
        fanfs = fanfs.filter(Dept=D)

    # Build a mapping from EmployeeCode -> EmpID
    emp_map = {
        emp.EmployeeCode: emp.EmpID
        for emp in EmployeePersonalDetails.objects.filter(
            IsDelete=False, OrganizationID=OrganizationID
        )
    }

    today = date.today()

    # Attach EmpID manually
    for obj in fanfs:
        obj.EmpID_Resolved = emp_map.get(obj.Emp_Code, None)

        # print("date of leaving", obj.Date_Of_Leaving)

        # Default values
        obj.Pending_From_HR = ''
        obj.Pending_From_Finance = ''
        obj.Pending_From_GM = ''
        obj.Pending_From_Auditor = ''

        # HR Pending
        if obj.AuditedByHR == 'Pending':
            start_date = obj.AuditedByHR_Date_Time or (obj.CreatedDateTime.date() if obj.CreatedDateTime else today)
            Pending_From_HR = (today - start_date).days
            obj.Pending_From_HR = f'Since {Pending_From_HR} Days'

        # Finance Pending
        elif obj.AuditedByFinance == 'Pending':
            start_date = obj.AuditedByFinance_Date_Time or obj.AuditedByHR_Date_Time or today
            Pending_From_Finance = (today - start_date).days
            obj.Pending_From_Finance = f'Since {Pending_From_Finance} Days'

        # GM Pending
        elif obj.AuditedByGM == 'Pending':
            start_date = obj.AuditedByGM_Date_Time or obj.AuditedByFinance_Date_Time or today
            # print("Gm Start Date::", start_date)
            Pending_From_GM = (today - start_date).days
            obj.Pending_From_GM = f'Since {Pending_From_GM} Days'

        # Auditor Pending
        elif obj.AuditedBy_Auditor == 'Pending':
            start_date = obj.AuditedBy_Auditor_Date_Time or obj.AuditedByGM_Date_Time or today
            # print("Auditor Start Date::", start_date)
            Pending_From_Auditor = (today - start_date).days
            obj.Pending_From_Auditor = f'Since {Pending_From_Auditor} Days'

    context = {
        'fanfs': fanfs,
        'memorg': memorg,
        'I': I,
        'depts': depts,
        'D': D
    }

    return render(request, 'final/Approval_Pages/FullAndFinalApprovalList.html', context)





from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Full_and_Final_Settltment
from .serializers import FullAndFinalSettlementSerializer

@api_view(['GET'])
def get_all_fandf(request):
    data = Full_and_Final_Settltment.objects.filter(IsDelete=False).order_by('-id')
    serializer = FullAndFinalSettlementSerializer(data, many=True)
    return Response({
        "status": True,
        "message": "Success",
        "data": serializer.data
    })




@api_view(['GET'])
def get_fandf_by_emp(request):
    # Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    # AccessToken = request.headers.get('Authorization', '')

    # Token checks
    # if not AccessToken:
    #     return Response({'error': 'Token not found'}, status=400)
    # if AccessToken != Fixed_Token:
    #     return Response({'error': 'Invalid token'}, status=400)

    Emp_Code = request.GET.get("Emp_Code")
    OID = request.GET.get("OID")

    # OID checks
    if not OID:
        return Response({'error': 'OID is required'}, status=400)
    if OID != '333333' and not OrganizationMaster.objects.filter(OrganizationID=OID).exists():
        return Response({'error': 'Invalid OrganizationID'}, status=400)

    # Special OID → Return all data
    if OID in ['3333333', '333333']:
        qs = Full_and_Final_Settltment.objects.filter(IsDelete=False)
        serializer = FullAndFinalSettlementSerializer(qs, many=True)

        data = list(serializer.data)

        for item in data:
            org = OrganizationMaster.objects.filter(
                OrganizationID=item.get("OrganizationID"),
                IsDelete=False,
                IsNileHotel=1,
                Activation_status=1
            ).values("ShortDisplayLabel").first()

            item["OrganizationName"] = org["ShortDisplayLabel"] if org else None

        return Response({
            "status": True,
            "message": "Success",
            "data": data
        })

    # Normal flow (single employee)
    qs = Full_and_Final_Settltment.objects.filter(
        # Emp_Code=Emp_Code,
        OrganizationID=OID,
        IsDelete=False
    ).first()

    if not qs:
        return Response({
            "status": False,
            "message": "Record not found"
        })

    serializer = FullAndFinalSettlementSerializer(qs)
    data = dict(serializer.data)

    org = OrganizationMaster.objects.filter(
        OrganizationID=OID,
        IsDelete=False,
        IsNileHotel=1,
        Activation_status=1
    ).values("ShortDisplayLabel").first()

    data["htl"] = org["ShortDisplayLabel"] if org else None

    return Response({
        "status": True,
        "message": "Success",
        "data": data
    })
    
from django.db.models import DateField
from django.db.models.functions import Cast

@api_view(['GET'])
def get_fandf_by_OID(request):
    Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
    AccessToken = request.headers.get('Authorization', '')

    # Token checks
    if not AccessToken:
        return Response({'error': 'Token not found'}, status=400)
    if AccessToken != Fixed_Token:
        return Response({'error': 'Invalid token'}, status=400)
    
    # -------------------------------
    # NEW ACCESS CHECK
    UserID = request.GET.get("UserID")
    ALLOWED_USER_IDS = ['20201212180048', '20251209112591']

    if not UserID:
        return Response({'error': 'UserID is required'}, status=400)

    if UserID not in ALLOWED_USER_IDS:
        return Response({'error': 'Not found'}, status=404)
    # -------------------------------

    Emp_Code = request.GET.get("Emp_Code")
    OID = request.GET.get("OID")
    FinalStatus = request.GET.get("FinalStatus")
    # UserID = request.GET.get("UserID")

    # OID checks
    if not OID:
        return Response({'error': 'OID is required'}, status=400)
    if OID != '333333' and not OrganizationMaster.objects.filter(OrganizationID=OID).exists():
        return Response({'error': 'Invalid OrganizationID'}, status=400)

    # Special OID → Return all data
    if OID in ['3333333', '333333']:
        # qs = Full_and_Final_Settltment.objects.filter(IsDelete=False).order_by("-Date_Of_Leaving")
        qs = Full_and_Final_Settltment.objects.filter(
            IsDelete=False
        ).annotate(
            leaving_date=Cast("Date_Of_Leaving", DateField())
        ).order_by("-leaving_date")
        serializer = FullAndFinalSettlementSerializer(qs, many=True)

        data = list(serializer.data)

        for item in data:
            org = OrganizationMaster.objects.filter(
                OrganizationID=item.get("OrganizationID"),
                IsDelete=False,
                IsNileHotel=1,
                Activation_status=1
            ).values("ShortDisplayLabel").first()

            item["HTL"] = org["ShortDisplayLabel"] if org else None

        return Response({
            "status": True,
            "message": "Success",
            "data": data
        })
        
    # Normal flow (all employees for OID)
    # qs = Full_and_Final_Settltment.objects.filter(
    #     OrganizationID=OID,
    #     IsDelete=False
    # ).order_by("-Date_Of_Leaving")
    qs = Full_and_Final_Settltment.objects.filter(
        OrganizationID=OID,
        IsDelete=False
    ).annotate(
        leaving_date=Cast("Date_Of_Leaving", DateField())
    ).order_by("-leaving_date")
        
    if FinalStatus and FinalStatus.lower() != "all":
        qs = qs.filter(FinalStatus=FinalStatus)
        
    if not qs.exists():
        return Response({
            "status": False,
            "message": "No employees found"
        })

    serializer = FullAndFinalSettlementSerializer(qs, many=True)
    data = list(serializer.data)

    # Add hotel label for each item
    org = OrganizationMaster.objects.filter(
        OrganizationID=OID,
        IsDelete=False,
        IsNileHotel=1,
        Activation_status=1
    ).values("ShortDisplayLabel").first()

    for item in data:
        item["HTL"] = org["ShortDisplayLabel"] if org else None

    return Response({
        "status": True,
        "message": "Success",
        "data": data
    })

# @api_view(['GET'])
# def get_fandf_by_OID(request):
#     Fixed_Token = 'ujhj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea11f'
#     AccessToken = request.headers.get('Authorization', '')

#     # Token checks
#     if not AccessToken:
#         return Response({'error': 'Token not found'}, status=400)
#     if AccessToken != Fixed_Token:
#         return Response({'error': 'Invalid token'}, status=400)

#     Emp_Code = request.GET.get("Emp_Code")
#     OID = request.GET.get("OID")
#     FinalStatus = request.GET.get("FinalStatus")
#     UserID = request.GET.get("UserID")

#     # OID checks
#     if not OID:
#         return Response({'error': 'OID is required'}, status=400)
#     if OID != '333333' and not OrganizationMaster.objects.filter(OrganizationID=OID).exists():
#         return Response({'error': 'Invalid OrganizationID'}, status=400)

#     # # Special OID → Return all data
#     # if OID in ['3333333', '333333']:
#     #     # qs = Full_and_Final_Settltment.objects.filter(IsDelete=False).order_by("-Date_Of_Leaving")
#     #     qs = Full_and_Final_Settltment.objects.filter(
#     #         IsDelete=False
#     #     ).annotate(
#     #         leaving_date=Cast("Date_Of_Leaving", DateField())
#     #     ).order_by("-leaving_date")
#     #     serializer = FullAndFinalSettlementSerializer(qs, many=True)

#     #     data = list(serializer.data)

#     #     for item in data:
#     #         org = OrganizationMaster.objects.filter(
#     #             OrganizationID=item.get("OrganizationID"),
#     #             IsDelete=False,
#     #             IsNileHotel=1,
#     #             Activation_status=1
#     #         ).values("ShortDisplayLabel").first()

#     #         item["HTL"] = org["ShortDisplayLabel"] if org else None

#     #     return Response({
#     #         "status": True,
#     #         "message": "Success",
#     #         "data": data
#     #     })
        
#     # # Normal flow (all employees for OID)
#     # # qs = Full_and_Final_Settltment.objects.filter(
#     # #     OrganizationID=OID,
#     # #     IsDelete=False
#     # # ).order_by("-Date_Of_Leaving")
#     # qs = Full_and_Final_Settltment.objects.filter(
#     #     IsDelete=False
#     # ).annotate(
#     #     leaving_date=Cast("Date_Of_Leaving", DateField())
#     # ).order_by("-leaving_date")
        
#     # if FinalStatus and FinalStatus.lower() != "all":
#     #     qs = qs.filter(FinalStatus=FinalStatus)
        
#     # if not qs.exists():
#     #     return Response({
#     #         "status": False,
#     #         "message": "No employees found"
#     #     })

#     # serializer = FullAndFinalSettlementSerializer(qs, many=True)
#     # data = list(serializer.data)

#     # # Add hotel label for each item
#     # org = OrganizationMaster.objects.filter(
#     #     OrganizationID=OID,
#     #     IsDelete=False,
#     #     IsNileHotel=1,
#     #     Activation_status=1
#     # ).values("ShortDisplayLabel").first()

#     # for item in data:
#     #     item["HTL"] = org["ShortDisplayLabel"] if org else None

#     return Response({
#         "status": False,
#         "message": "No Data Found"
#     })
    
    
from pathlib import Path
import mimetypes
from django.contrib import messages
from .azure import upload_file_to_blob,ALLOWED_EXTENTIONS,download_blob

def Upload_Auditor_Approval_Upload_File(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID =request.session["OrganizationID"]
        OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID   
    EmpID = request.GET.get('EmpID')
    Page  = request.GET.get('Page')
    id = request.GET.get('LOE_ID')    
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix

        new_file = upload_file_to_blob(file,id)
        if not new_file:
            messages.warning(request, f"{ext} not allowed only accept {', '.join(ext.lower()for ext in ALLOWED_EXTENTIONS)} ")
            return render(request, "letterofexp/upload_file.html", {}) 
        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()
        if Page == 'Trainees_Emp_List':
            return redirect('Trainees_Emp_List')
      
        Success = 'Uploaded'        
        encrypted_id = encrypt_id(EmpID)
        url = reverse('EmployeeLetters')  
        redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
        return redirect(redirect_url)
    
    
    return render(request, "Trainees_Exp/Upload_File.html")



# def Upload_Auditor_Approval_Upload_File(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)
#     else:
#         OrganizationID =request.session["OrganizationID"]
#         OID  = request.GET.get('OID')
#     if OID:
#             OrganizationID= OID   
#     EmpID = request.GET.get('EmpID')
#     Page  = request.GET.get('Page')
#     id = request.GET.get('LOE_ID')    
#     if request.method == 'POST' and request.FILES['file']:
#         file = request.FILES['file']
#         ext = Path(file.name).suffix

#         new_file = upload_file_to_blob(file,id)
#         if not new_file:
#             messages.warning(request, f"{ext} not allowed only accept {', '.join(ext.lower()for ext in ALLOWED_EXTENTIONS)} ")
#             return render(request, "letterofexp/upload_file.html", {}) 
#         new_file.file_name = file.name
#         new_file.file_extention = ext
#         new_file.save()

#         Success = 'Uploaded'        
#         return Success
    

# from django.http import HttpResponse

# def Upload_Auditor_Approval_Upload_File(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)

#     OrganizationID = request.GET.get('OID', request.session["OrganizationID"])
#     Emp_Code = request.GET.get('EmpCode', 0)
#     print("EmpCode::", Emp_Code)
#     print("OrganizationID::", OrganizationID)
    
#     qs = Full_and_Final_Settltment.objects.filter(IsDelete=False, Emp_Code=Emp_Code, OrganizationID=OrganizationID).only('id').first()


#     if request.method == 'POST' and request.FILES.get('file'):
#         file = request.FILES['file']
#         ext = Path(file.name).suffix.lower()
#         print("file:", file)
#         print("ext:", ext)

#         new_file = upload_file_to_blob(file, qs.id)
        
#         if not new_file:
#             return HttpResponse("Invalid file", status=400)

#         new_file.file_name = file.name
#         new_file.file_extention = ext
#         new_file.save()

#         return HttpResponse("Uploaded")  

#     return HttpResponse("Invalid request", status=400)

from django.http import HttpResponse

def Upload_Auditor_Approval_Upload_File(request):

    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.GET.get('OID', request.session["OrganizationID"])
    Emp_Code = request.GET.get('EmpCode', 0)

    print("EmpCode::", Emp_Code)
    print("OrganizationID::", OrganizationID)

    qs = Full_and_Final_Settltment.objects.filter(
        IsDelete=False, Emp_Code=Emp_Code, OrganizationID=OrganizationID
    ).only('id').first()

    # ❗ Handle missing record
    if not qs:
        return HttpResponse("Record not found for given EmpCode & OrganizationID", status=404)

    # ❗ File upload
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        ext = Path(file.name).suffix.lower()

        new_file = upload_file_to_blob(file, qs.id)
        
        if not new_file:
            return HttpResponse("Invalid file format", status=400)

        new_file.file_name = file.name
        new_file.file_extention = ext
        new_file.save()

        return HttpResponse("Uploaded")

    return HttpResponse("Invalid request", status=400)
 
 
 

from django.http import HttpResponse,Http404

def Auditor_Approval_Download_File(request):
    id = request.GET.get('FNF_ID')
    # OID  = request.GET.get('OID')
    # if OID:
    #         OrganizationID= OID   
    file = Full_and_Final_Settltment.objects.get(id=id)
    file_id = file.file_id
    file_name = file.file_name
    
    file_type, _ = mimetypes.guess_type(file_id)
    
    
    blob_name = file_id
    blob_content = download_blob(blob_name)
    
    if blob_content:
        response = HttpResponse(blob_content.readall(), content_type=file_type)
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        messages.success(request, f"{file_name} was successfully downloaded")
        return response
    return Http404


# def Auditor_Approval_Repalce_File(request):
#     if 'OrganizationID' not in request.session:
#         return redirect(MasterAttribute.Host)

#     OrganizationID = request.session["OrganizationID"]
#     OID = request.GET.get('OID')
#     Page = request.GET.get('Page')
#     if OID:
#         OrganizationID = OID

#     UserID = str(request.session["UserID"])
#     EmpID = request.GET.get('EmpID')
#     id = request.GET.get('FNF_ID')

#     # Fetch existing record
#     obj = Full_and_Final_Settltment.objects.get(id=id)

#     # ---------- DELETE FILE PROPERLY ----------
#     obj.file_id = None
#     obj.file_name = None
#     obj.ModifyBy = UserID
#     obj.save()
#     # -----------------------------------------

#     # Success = "Deleted"
#     # encrypted_id = encrypt_id(EmpID)
#     # url = reverse('EmployeeLetters')

#     # redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}"
#     # return redirect(redirect_url)
#     return HttpResponse("Deleted")
    

from django.http import JsonResponse

def Auditor_Approval_Repalce_File(request):
    if 'OrganizationID' not in request.session:
        return JsonResponse({"status": "error", "message": "Unauthorized"}, status=401)

    OrganizationID = request.session["OrganizationID"]
    OID = request.GET.get('OID')
    if OID:
        OrganizationID = OID

    UserID = str(request.session["UserID"])
    emp_id = request.GET.get('EmpID')
    fnf_id = request.GET.get('FNF_ID')

    try:
        obj = Full_and_Final_Settltment.objects.get(id=fnf_id)
    except Full_and_Final_Settltment.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Record not found"}, status=404)

    # ---------- DELETE FILE PROPERLY ----------
    obj.file_id = None
    obj.file_name = None
    obj.ModifyBy = UserID
    obj.save()
    # -----------------------------------------

    return JsonResponse({
        "status": "success",
        "message": "File deleted successfully",
        "FNF_ID": fnf_id,
        "EmpID": emp_id
    })
