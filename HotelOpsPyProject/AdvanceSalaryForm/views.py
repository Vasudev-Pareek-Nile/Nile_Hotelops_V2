from django.shortcuts import render
from django.shortcuts import render,redirect

# Create your views here.
from HumanResources.views import EmployeeDetailsData
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from datetime import datetime, date
from django.urls import reverse
from hotelopsmgmtpy.utils import encrypt_id, decrypt_id
from .models import AdvanceSalaryForm
from django.contrib import messages
from HumanResources.models import EmployeeBankInformationDetails


def AdvanceSalaryHome(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
    
    OrganizationID = request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
            OrganizationID= OID   
    UserID = str(request.session["UserID"])

    
    EmpCode  = request.GET.get('EC')
    EmpID  = request.GET.get('EmpID')
    Application_Form_id_str = request.GET.get("R_ID")
    Application_Form_id = int(Application_Form_id_str) if Application_Form_id_str else None

    DepartmentName = request.GET.get('DepartmentName')
    # print("Employee ID is here: ", EmpID)
    # print("Employee Code is here: ", EmpCode)
    # print("Employee OID is here: ", OID)


    EmpDetails  = EmployeeDetailsData(EmpID,OrganizationID)

    AdvanceSalaryFormData = AdvanceSalaryForm.objects.filter(emp_code=EmpCode, OrganizationID=OrganizationID, Application_Form_No=Application_Form_id, is_delete=False).first()
    BankAccoundNo = EmployeeBankInformationDetails.objects.filter(EmpID=EmpID, OrganizationID=OrganizationID, IsDelete=False).first()

    # print("BankAccoundNo::", BankAccoundNo)
    # print("BankAccoundNo::-----------------------------")
    # print("BankAccoundNo::", BankAccoundNo.BankAccountNumber)

    if request.method == "POST":
        EmployeeCode = request.POST['EmployeeCode']
        EmployeeID = request.POST['EmployeeID']
        EmployeeName = request.POST['EmployeeName']
        Designation = request.POST['Designation']
        Department = request.POST['Department']
        DateOfLoan_str = request.POST.get('DateOfLoan')
        # LoanAmountRequired = request.POST['LoanAmountRequired']
        LoanAmountRequired = float(request.POST.get('LoanAmountRequired') or 0)
        NoofInstallments = request.POST['NoofInstallments']
        ReasonsforRequest = request.POST['ReasonsforRequest']
        # BankACNo = request.POST['BankACNo']

        BankACNo = float(request.POST.get('BankACNo') or 0)

        # ACCOUNTS DEPARTMENT
        PreviousLoanTaken = float(request.POST.get('PreviousLoanTaken') or 0)
        DuesInRepayment = float(request.POST.get('DuesInRepayment') or 0)
        PrevNoofInstallments = int(float(request.POST.get('PrevNoofInstallments') or 0))
        ReasonforPreviousLoan = request.POST['ReasonforPreviousLoan']


        # HUMAN RESOURCES DEPARTMENT 
        CurrentSalary = float(request.POST.get('CurrentSalary') or 0)
        Recommendation = request.POST['Recommendation']
        DateOfJoining_str = request.POST['DateOfJoining']

        # DateOfLoan_str = request.POST.get('DateOfLoan')
        try:
            DateOfLoan = datetime.strptime(DateOfLoan_str, '%Y-%m-%d').date() if DateOfLoan_str else None
        except ValueError:
            DateOfLoan = None

        try:
            DateOfJoining = datetime.strptime(DateOfJoining_str, '%d/%m/%y').date()
        except ValueError:
            DateOfJoining = None  # handle error or default

        try:
            if AdvanceSalaryFormData and Application_Form_id:
                AdvanceSalaryFormData.emp_code = EmployeeCode
                AdvanceSalaryFormData.EmpID = EmployeeID
                AdvanceSalaryFormData.EmployeeName = EmployeeName
                AdvanceSalaryFormData.Designation = Designation
                AdvanceSalaryFormData.Department = Department
                AdvanceSalaryFormData.DateofLoan = DateOfLoan
                AdvanceSalaryFormData.LoanAmount = LoanAmountRequired
                AdvanceSalaryFormData.No_Of_Installments = NoofInstallments
                AdvanceSalaryFormData.BankACNo = BankACNo
                AdvanceSalaryFormData.Reasons_For_Request = ReasonsforRequest
                AdvanceSalaryFormData.Prev_Loan_Taken = PreviousLoanTaken
                AdvanceSalaryFormData.Dues_Repayment = DuesInRepayment
                AdvanceSalaryFormData.Prev_No_Of_Installments = PrevNoofInstallments
                AdvanceSalaryFormData.Reason_For_PreviousLoan = ReasonforPreviousLoan
                AdvanceSalaryFormData.Current_Salary = CurrentSalary
                AdvanceSalaryFormData.Recommendation = Recommendation
                AdvanceSalaryFormData.DateofJoining = DateOfJoining
                AdvanceSalaryFormData.modify_by = UserID

                AdvanceSalaryFormData.save()

            else:
                AdvanceSalaryObj = AdvanceSalaryForm.objects.create(
                    emp_code = EmployeeCode,
                    EmpID = EmployeeID,
                    EmployeeName = EmployeeName,
                    Designation = Designation,
                    Department = Department,
                    DateofLoan = DateOfLoan,
                    LoanAmount = LoanAmountRequired,
                    No_Of_Installments = NoofInstallments,
                    BankACNo = BankACNo,
                    Reasons_For_Request = ReasonsforRequest,

                    Prev_Loan_Taken = PreviousLoanTaken,
                    Dues_Repayment = DuesInRepayment,
                    Prev_No_Of_Installments = PrevNoofInstallments,
                    Reason_For_PreviousLoan = ReasonforPreviousLoan,

                    Current_Salary = CurrentSalary,
                    Recommendation = Recommendation,
                    DateofJoining = DateOfJoining,
                    
                    OrganizationID = OrganizationID,
                    created_by = UserID
                )
            messages.success(request, "SALARY ADVANCE / LOAN APPLICATION Application submitted successfully.")
            Success = True 
            encrypted_id = encrypt_id(EmpID)
            url = reverse('EmployeeLetters')  
            redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
            return redirect(redirect_url)
        except Exception as e:
            # Error redirect
            # print("Error while submitting form:", e)  # Log it for debugging
            messages.error(request, "Something went wrong while submitting the form.")
            Success = True 
            encrypted_id = encrypt_id(EmpID)
            url = reverse('EmployeeLetters')  
            redirect_url = f"{url}?EmpID={encrypted_id}&OID={OrganizationID}&Success={Success}" 
            return redirect(redirect_url)


    raw_date = EmpDetails.DateofJoining  # For testing
    formatted_date = raw_date.strftime('%y/%m/%d')  # '21/02/25'

    # print("Complete details", EmpDetails)
    Context  =  {
        'EmpID' : EmpDetails.EmpID,
        "BankAccoundNo":BankAccoundNo.BankAccountNumber,
        'emp_code' : EmpDetails.EmployeeCode,
        'FullName': f"{EmpDetails.Prefix} {EmpDetails.FirstName}{EmpDetails.MiddleName or ''} {EmpDetails.LastName}",
        'mobile_number' : EmpDetails.MobileNumber,
        'email' : EmpDetails.EmailAddress,
        'date_of_joining' : formatted_date,
        'department' : EmpDetails.Department,
        'designation' : EmpDetails.Designation,
        'Reporting_to_designation' : EmpDetails.ReportingtoDesignation,
        'level' : EmpDetails.Level,
        'basic_salary' : EmpDetails.BasicSalary,
        'address' : EmpDetails.Address,
        'AdvanceSalaryFormData':AdvanceSalaryFormData,
        "today": date.today()
    }
    return render(request, 'AdvanceSalaryForm/AdvanceSalaryForm.html', Context)





# Download pdf --------------->
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from app.models import OrganizationMaster 

def download_Advance_Salary_pdf(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")

    OrganizationID =request.session["OrganizationID"]
    OID  = request.GET.get('OID')
    if OID:
        OrganizationID= OID   
    
    Application_Form_id = request.GET["R_ID"]
    Application_Form_id = int(Application_Form_id)
    # print("Application_Form_id::", Application_Form_id)
    # print("Application_Form_id", type(Application_Form_id))
    EmpID =  request.GET["EmpID"]
    EmpCode = request.GET["EC"]


    # Base filter query

    base_url = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    organizations = OrganizationMaster.objects.filter(OrganizationID=3).first()
    organization_logos = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None

    organizations = OrganizationMaster.objects.filter(OrganizationID=OrganizationID).first()
    organization_logo = f"{base_url}{organizations.OrganizationLogo}" if organizations and organizations.OrganizationLogo else None
    organization_logo = organizations.OrganizationName

    AdvanceSalaryFormData = AdvanceSalaryForm.objects.filter(emp_code=EmpCode, OrganizationID=OrganizationID, Application_Form_No=Application_Form_id, is_delete=False)

    # print("AdvanceSalaryFormData::", AdvanceSalaryFormData)
    current_datetime = datetime.now().strftime('%d %B %Y %H:%M:%S')

    # Prepare context for the PDF template
    context = {
        'organization_logo': organization_logo,
        'organization_logos':organization_logos,
        'current_datetime':current_datetime,
        'AdvanceSalaryFormData':AdvanceSalaryFormData,
    }

    template_path = 'AdvanceSalaryForm/Advance_Salary_Form_PDF.html'
    template = get_template(template_path)
    html = template.render(context).encode("UTF-8")
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{organization_logo}_Advance_Salary_Report.pdf"'


    pisa_status = pisa.CreatePDF(html, dest=response, encoding="UTF-8")

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response

