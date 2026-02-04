from django.shortcuts import render, redirect
from hotelopsmgmtpy.GlobalConfig import MasterAttribute
from HumanResources.models import SalaryTitle_Master,Salary_Detail_Master,EmployeePersonalDetails,EmployeeWorkDetails,EmployeeFamilyDetails,EmployeeChildDetails,EmployeeEmergencyInformationDetails,EmployeeAddressInformationDetails,EmployeeBankInformationDetails,EmployeeQualificationDetails,EmployeePreviousWorkInformationDetails,EmployeeDocumentsInformationDetails,EmployeeIdentityInformationDetails,DesignationHistory
# from HumanResources.models import EmployeePersonalDetails,EmployeeWorkDetails
# from HumanResources.views import EmployeeCardDetails
from Leave_Management_System.models import Emp_Leave_Balance_Master, Leave_Application
from datetime import date, timedelta
from Employee_Payroll.models import Attendance_Data, WeekOffDetails
from django.http import JsonResponse
from datetime import date, timedelta
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.timezone import localtime


# Create your views here.


# Employee_Personal_Dashboard_View views here.
def Employee_Personal_Dashboard_View(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        print("Show Page Session")
     
    return render(request, "Employee_Personal_Dashboard/Employee_Dashboard.html")



def format_time(time_str):
    """Convert '13:21:03.0000000' to '01:21 PM'."""
    if time_str:
        try:
            return datetime.strptime(time_str[:8], "%H:%M:%S").strftime("%I:%M %p")
        except ValueError:
            return time_str  # Return original if parsing fails
    return ""


# def Employee_Personal_Dashboard_API(request):
#     if 'OrganizationID' not in request.session:
#         return JsonResponse({'error': 'Session expired or invalid'}, status=401)

#     OrganizationID = request.session["OrganizationID"]
#     # EmployeeCode = request.session["EmployeeCode"]
#     EmployeeCode = str(request.session["EmployeeCode"]).strip()

#     Emp_Id = None
#     if EmployeeCode:
#         Emp_Id = EmployeePersonalDetails.objects.filter(
#             EmployeeCode=EmployeeCode, OrganizationID=OrganizationID, IsDelete=False
#         ).values_list('EmpID', flat=True).first()

#         leave_balance = list(Emp_Leave_Balance_Master.objects.filter(
#             OrganizationID=OrganizationID, IsDelete=False, Emp_code=EmployeeCode
#         ).select_related('Leave_Type_Master').values(
#             'Emp_code',
#             'Balance',
#             'Leave_Type_Master__id',
#             'Leave_Type_Master__Type'
#         ))

#         leave_balance_data = []
#         for leave in leave_balance:
#             leave_balance_data.append({
#                 "Emp_code": leave["Emp_code"],
#                 "Balance": leave["Balance"],
#                 "Leave_Type_Master": {
#                     "id": leave["Leave_Type_Master__id"],
#                     "Type": leave["Leave_Type_Master__Type"],
#                 }
#             })

#         # leave_balance = list(Emp_Leave_Balance_Master.objects.filter(
#         #     OrganizationID=OrganizationID, IsDelete=False, Emp_code=EmployeeCode
#         # ).values())

#         leave_requset_appr_count = Leave_Application.objects.filter(
#             OrganizationID=OrganizationID, IsDelete=False, Emp_code=EmployeeCode, Status=1
#         ).count()

#         leave_requset_Pending_count = Leave_Application.objects.filter(
#             OrganizationID=OrganizationID, IsDelete=False, Emp_code=EmployeeCode, Status=0
#         ).count()

#         leave_requset_rejected_count = Leave_Application.objects.filter(
#             OrganizationID=OrganizationID, IsDelete=False, Emp_code=EmployeeCode, Status=-1
#         ).count()
#     else:
#         return JsonResponse({'error': 'Invalid employee code'}, status=400)

#     if Emp_Id:
#         Emobj = EmployeeCardDetails_EmployeeDashboard(Emp_Id, OrganizationID)
#     if Emobj:
#         Emobj_data = {
#             'EmpID': Emobj.EmpID,
#             'EmployeeCode': Emobj.EmployeeCode,
#             'FullName': f'{Emobj.FirstName} {Emobj.MiddleName} {Emobj.LastName}',
#             'Department': Emobj.Department,
#             'EmpStatus': Emobj.EmpStatus,
#             'Designation': Emobj.Designation,
#             'Level': Emobj.Level,
#             'DateofJoining': Emobj.DateofJoining.strftime('%Y-%m-%d') if Emobj.DateofJoining else None,
#             'ReportingtoDesignation': Emobj.ReportingtoDesignation,
#             'ReportingtoDepartment': Emobj.ReportingtoDepartment,
#             'ReportingtoLevel': Emobj.ReportingtoLevel,
#             'TenureTillToday': Emobj.TenureTillToday,

#             'MobileNumber': Emobj.MobileNumber,
#             'EmailAddress': Emobj.EmailAddress,
#             'ProfileImageFileName': Emobj.ProfileImageFileName,
#             'DateofBirth': Emobj.DateofBirth,
#             'Gender': Emobj.Gender,
#         }

#     today = date.today()
#     next_90_days = today + timedelta(days=90)

#     leave_applications = list(Leave_Application.objects.filter(
#         IsDelete=0,
#         Emp_code=EmployeeCode,
#         OrganizationID=OrganizationID,
#         Start_Date__range=(today, next_90_days)
#     ).select_related('Leave_Type_Master').values(
#         'Emp_code',
#         'Start_Date',
#         'End_Date',
#         'Status',
#         'Leave_Type_Master__id',
#         'Leave_Type_Master__Type'
#     ))

#     Selected_Leave_Application = []
#     for leave in leave_applications:
#         Selected_Leave_Application.append({
#             "Emp_code": leave["Emp_code"],
#             "Start_Date": leave["Start_Date"].strftime("%Y-%m-%d"),
#             "End_Date": leave["End_Date"].strftime("%Y-%m-%d"),
#             "Status": leave["Status"],
#             "Leave_Type_Master": {
#                 "id": leave["Leave_Type_Master__id"],
#                 "Type": leave["Leave_Type_Master__Type"],
#             }
#         })

#     # qs = Emp_Leave_Balance_Master.objects.filter(
#     #     OrganizationID=OrganizationID,
#     #     IsDelete=False,
#     #     Emp_code=EmployeeCode
#     # )

#     # print(qs.query)  # Shows the raw SQL
#     # print(qs.count())  # Executes the query and shows the count


        
        
#     # Fetch Employee Personal Details
#     Empobjs = EmployeePersonalDetails.objects.filter(
#         IsDelete=False, OrganizationID=OrganizationID, IsEmployeeCreated=True, EmployeeCode=EmployeeCode,
#     ).values('EmployeeCode', 'Prefix', 'FirstName', 'MiddleName', 'LastName')

#     # Create a dictionary mapping EmployeeCode to full name
#     employee_data = {}
#     for emp in Empobjs:
#         emp_code = emp["EmployeeCode"]
#         full_name = f"{emp['FirstName']} {emp['MiddleName']} {emp['LastName']}".strip()
        
#         employee_data[emp_code] = {
#             "EmployeeCode": emp_code,
#             "EmployeeName": full_name,
#             "Attendance": [],  # Initialize an empty list for attendance
#         }

#     attendance_data = Attendance_Data.objects.filter(
#         OrganizationID=OrganizationID,
#         IsDelete=False,
#         # Date__year=Selected_Year, 
#         # Date__month=Selected_Month,
#         EmployeeCode=EmployeeCode  # Restrict normal users to their own data
#     ).distinct()


#     if attendance_data.exists():  # Check if data exists
#         for attendance in attendance_data:
#             emp_code = attendance.EmployeeCode

#             if emp_code not in employee_data:
#                 employee_data[emp_code] = {
#                     "EmployeeCode": emp_code,
#                     "EmployeeName": "Unknown",  # Default name if not found
#                     "Attendance": [],
#                 }

#             # Add attendance data
#             employee_data[emp_code]["Attendance"].append({
#                 'title': attendance.Status,
#                 'in_time': format_time(attendance.In_Time),
#                 'out_time': format_time(attendance.Out_Time),
#                 's_in_time': format_time(attendance.S_In_Time),
#                 's_out_time': format_time(attendance.S_Out_Time),
#                 'duty_hours': attendance.Duty_Hour,
#                 'status': attendance.Status if attendance.Status else "",
#                 'type': 'attendance',
#                 'Date': attendance.Date,  # Store as datetime for sorting
#                 'DateFormatted': attendance.Date.strftime('%d-%m-%Y'),
#             })

#             for emp_code in employee_data:
#                 employee_data[emp_code]["Attendance"].sort(key=lambda x: x["Date"])  # Oldest date first
#     else:
#         attendance = None


#     leave_data = Leave_Application.objects.filter(
#         OrganizationID=OrganizationID,
#         IsDelete=False,
#         # Start_Date__year=Selected_Year,
#         # Start_Date__month=Selected_Month,
#         Emp_code=EmployeeCode  # Restrict normal users to their own data
#     ).distinct()


#     for leave in leave_data:
#         emp_code = leave.Emp_code
#         leave_days = (leave.End_Date - leave.Start_Date).days + 1 if leave.Start_Date and leave.End_Date else 0
#         # print('leave days are here ------ ',leave_days)

#         # Ensure the employee exists in employee_data
#         if emp_code not in employee_data:
#             employee_data[emp_code] = {
#                 "EmployeeCode": emp_code,
#                 "EmployeeName": "Unknown",
#                 "Attendance": [],
#             }

#         leave_dict = {
#             'title': leave.Leave_Type_Master.Type,
#             'Leavestatus': leave.Status,
#             'start': leave.Start_Date.strftime('%d-%m-%Y'),
#             'end': leave.End_Date.strftime('%d-%m-%Y'),
#             'leave_Days': leave_days,
#             'type': 'leave',
#             'Reason': leave.Reason,
#             'Total_credit': leave.Total_credit,
#             'ReportingtoDesigantion': leave.ReportingtoDesigantion,
#             'Remark': leave.Remark,
#         }

#         employee_data[emp_code]["Attendance"].append(leave_dict)



#     return JsonResponse({
#         'Emobj': Emobj_data,
#         'Selected_Leave_Application': Selected_Leave_Application,
#         'leave_requset_Pending_count': leave_requset_Pending_count,
#         'leave_requset_rejected_count': leave_requset_rejected_count,
#         'leave_requset_appr_count': leave_requset_appr_count,
#         # 'Selected_Leave_Application': Selected_Leave_Application,
#         'leave_balance': leave_balance_data,
#         'employee_data': employee_data,
#     }, safe=False)




def Employee_Personal_Profile(request):
    return render(request, "Employee_Personal_Dashboard/Personal_Profile.html")



def Employee_Personal_Profile_Api(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)

    OrganizationID = request.session["OrganizationID"]
    EmployeeCode = request.session["EmployeeCode"]

    Personal_Details_Object = {}
    Emobj_data = {}
    Work_Details_Object = {}
    Bank_Details_Object = {}

    if EmployeeCode:
        Personal_Obj = EmployeePersonalDetails.objects.filter(
            EmployeeCode=EmployeeCode,
            IsDelete=False,
            OrganizationID=OrganizationID,
            IsEmployeeCreated=True
        ).first()

        if Personal_Obj:
            # Personal Info
            Personal_Details_Object = {
                'EmpID': Personal_Obj.EmpID,
                'EmployeeCode': Personal_Obj.EmployeeCode,
                'Prefix': Personal_Obj.Prefix or '',
                'FirstName': Personal_Obj.FirstName or '',
                'MiddleName': Personal_Obj.MiddleName or '',
                'LastName': Personal_Obj.LastName or '',
                'Gender': Personal_Obj.Gender or '',
                'MaritalStatus': Personal_Obj.MaritalStatus or '',
                'DateofBirth': Personal_Obj.DateofBirth,
                'age': Personal_Obj.age,
                'MobileNumber': Personal_Obj.MobileNumber or '',
                'EmailAddress': Personal_Obj.EmailAddress or '',
                'ProfileImageFileName': Personal_Obj.ProfileImageFileName or '',
                'ProfileImageFileTitle': Personal_Obj.ProfileImageFileTitle or '',
                'ProfileCompletion': Personal_Obj.ProfileCompletion,
            }


            if Personal_Obj:
                Emobj = EmployeeCardDetails(Personal_Obj.EmpID, OrganizationID)
                if Emobj:
                    Emobj_data = {
                        'EmpID': Emobj.EmpID,
                        'EmployeeCode': Emobj.EmployeeCode,
                        'FullName': f'{Emobj.FirstName} {Emobj.MiddleName} {Emobj.LastName}',
                        'Department': Emobj.Department,
                        'EmpStatus': Emobj.EmpStatus,
                        'Designation': Emobj.Designation,
                        'Level': Emobj.Level,
                        'DateofJoining': Emobj.DateofJoining.strftime('%Y-%m-%d') if Emobj.DateofJoining else None,
                        'ReportingtoDesignation': Emobj.ReportingtoDesignation,
                        'ReportingtoDepartment': Emobj.ReportingtoDepartment,
                        'ReportingtoLevel': Emobj.ReportingtoLevel,
                        'TenureTillToday': Emobj.TenureTillToday,

                        'MobileNumber': Emobj.MobileNumber,
                        'EmailAddress': Emobj.EmailAddress,
                        'ProfileImageFileName': Emobj.ProfileImageFileName,
                        'DateofBirth': Emobj.DateofBirth,
                        'Gender': Emobj.Gender,
                    }

            # Work Info
            work_obj = EmployeeWorkDetails.objects.filter(
                EmpID=Personal_Obj.EmpID,
                IsDelete=False,
                OrganizationID=OrganizationID,
                IsSecondary=False
            ).first()

            if work_obj:
                Work_Details_Object = {
                    'EmpStatus': work_obj.EmpStatus,
                    'Designation': work_obj.Designation,
                    'Department': work_obj.Department,
                    'Level': work_obj.Level,
                    'ReportingtoDesignation': work_obj.ReportingtoDesignation,
                    'ReportingtoDepartment': work_obj.ReportingtoDepartment,
                    'ReportingtoLevel': work_obj.ReportingtoLevel,
                    'DottedLine': work_obj.DottedLine,
                    'OfficialEmailAddress': work_obj.OfficialEmailAddress,
                    'OfficialMobileNo': work_obj.OfficialMobileNo,
                    'DateofJoining': work_obj.DateofJoining,
                    'CompanyAccommodation': work_obj.CompanyAccommodation,
                    'Locker': work_obj.Locker,
                    'LockerType': work_obj.LockerType,
                    'LockerNumber': work_obj.LockerNumber,
                }

            # Bank Info
            bank_obj = EmployeeBankInformationDetails.objects.filter(
                EmpID=Personal_Obj.EmpID,
                IsDelete=False,
                OrganizationID=OrganizationID
            ).first()

            if bank_obj:
                Bank_Details_Object = {
                    'BankAccountNumber': bank_obj.BankAccountNumber,
                    'NameofBank': bank_obj.NameofBank,
                    'BankBranch': bank_obj.BankBranch,
                    'IFSCCode': bank_obj.IFSCCode,
                }

            # Employee Emergency Information Details Info
            Emergency_Info = EmployeeEmergencyInformationDetails.objects.filter(
                EmpID=Personal_Obj.EmpID,
                IsDelete=False,
                OrganizationID=OrganizationID
            ).first()

            if Emergency_Info:
                Emergency_info_object = {
                    'FirstName': Emergency_Info.FirstName if Emergency_Info.FirstName else '',
                    'MiddleName': Emergency_Info.MiddleName if Emergency_Info.MiddleName else '',
                    'LastName': Emergency_Info.LastName if Emergency_Info.LastName else '',
                    'Relation': Emergency_Info.Relation if Emergency_Info.Relation else '',
                    'EmergencyContactNumber_1': Emergency_Info.EmergencyContactNumber_1 if Emergency_Info.EmergencyContactNumber_1 else '',
                    'EmergencyContactNumber_2': Emergency_Info.EmergencyContactNumber_2 if Emergency_Info.EmergencyContactNumber_2 else '',
                }

            # Family Informations Info
            family_obj  = EmployeeFamilyDetails.objects.filter(
                EmpID=Personal_Obj.EmpID,
                IsDelete=False,
                OrganizationID=OrganizationID
            ).first()

            if family_obj :
                family_info_object = {
                    'SpouseName': family_obj.SpouseName or '',
                    'SpouseDateofBirth': family_obj.SpouseDateofBirth,
                    'SpouseAge': family_obj.SpouseAge or '',
                    'SpouseContactNo': family_obj.SpouseContactNo or '',

                    'MotherName': family_obj.MotherName or '',
                    'MotherDateofBirth': family_obj.MotherDateofBirth,
                    'MotherAge': family_obj.MotherAge or '',
                    'MotherContactNo': family_obj.MotherContactNo or '',

                    'FatherName': family_obj.FatherName or '',
                    'FatherDateofBirth': family_obj.FatherDateofBirth,
                    'FatherAge': family_obj.FatherAge or '',
                    'FatherContactNo': family_obj.FatherContactNo or '',

                    'LandlineNo': family_obj.LandlineNo or '',
                }

    return JsonResponse({
        'Personal_Details': Personal_Details_Object,
        'Work_Details': Work_Details_Object,
        'Bank_Details': Bank_Details_Object,
        'Emobj': Emobj_data,
        'Emergency_informations': Emergency_info_object,
        'family_obj':family_info_object,
    }, safe=False)






def Employee_Personal_Dashboard_API(request):
    if 'OrganizationID' not in request.session:
        return JsonResponse({'error': 'Session expired or invalid'}, status=401)

    OrganizationID = request.session["OrganizationID"]
    # EmployeeCode = request.session["EmployeeCode"]
    EmployeeCode = str(request.session["EmployeeCode"]).strip()

    Emp_Id = None
    if EmployeeCode:
        Emp_Id = EmployeePersonalDetails.objects.filter(
            EmployeeCode=EmployeeCode, OrganizationID=OrganizationID, IsDelete=False
        ).values_list('EmpID', flat=True).first()

        leave_balance = list(Emp_Leave_Balance_Master.objects.filter(
            OrganizationID=OrganizationID, IsDelete=False, Emp_code=EmployeeCode
        ).select_related('Leave_Type_Master').values(
            'Emp_code',
            'Balance',
            'Leave_Type_Master__id',
            'Leave_Type_Master__Type'
        ))

        leave_balance_data = []
        for leave in leave_balance:
            leave_balance_data.append({
                "Emp_code": leave["Emp_code"],
                "Balance": leave["Balance"],
                "Leave_Type_Master": {
                    "id": leave["Leave_Type_Master__id"],
                    "Type": leave["Leave_Type_Master__Type"],
                }
            })

        # leave_balance = list(Emp_Leave_Balance_Master.objects.filter(
        #     OrganizationID=OrganizationID, IsDelete=False, Emp_code=EmployeeCode
        # ).values())

        leave_requset_appr_count = Leave_Application.objects.filter(
            OrganizationID=OrganizationID, IsDelete=False, Emp_code=EmployeeCode, Status=1
        ).count()

        leave_requset_Pending_count = Leave_Application.objects.filter(
            OrganizationID=OrganizationID, IsDelete=False, Emp_code=EmployeeCode, Status=0
        ).count()

        leave_requset_rejected_count = Leave_Application.objects.filter(
            OrganizationID=OrganizationID, IsDelete=False, Emp_code=EmployeeCode, Status=-1
        ).count()
    else:
        return JsonResponse({'error': 'Invalid employee code'}, status=400)

    if Emp_Id:
        Emobj = EmployeeCardDetails_EmployeeDashboard(Emp_Id, OrganizationID)
    if Emobj:
        Emobj_data = {
            'EmpID': Emobj.EmpID,
            'EmployeeCode': Emobj.EmployeeCode,
            'FullName': f'{Emobj.FirstName} {Emobj.MiddleName} {Emobj.LastName}',
            'Department': Emobj.Department,
            'EmpStatus': Emobj.EmpStatus,
            'Designation': Emobj.Designation,
            'Level': Emobj.Level,
            'DateofJoining': Emobj.DateofJoining.strftime('%Y-%m-%d') if Emobj.DateofJoining else None,
            'ReportingtoDesignation': Emobj.ReportingtoDesignation,
            'ReportingtoDepartment': Emobj.ReportingtoDepartment,
            'ReportingtoLevel': Emobj.ReportingtoLevel,
            'TenureTillToday': Emobj.TenureTillToday,

            'MobileNumber': Emobj.MobileNumber,
            'EmailAddress': Emobj.EmailAddress,
            'ProfileImageFileName': Emobj.ProfileImageFileName,
            'DateofBirth': Emobj.DateofBirth,
            'Gender': Emobj.Gender,
        }

    today = date.today()
    next_90_days = today + timedelta(days=90)

    leave_applications = list(Leave_Application.objects.filter(
        IsDelete=0,
        Emp_code=EmployeeCode,
        OrganizationID=OrganizationID,
        Start_Date__range=(today, next_90_days)
    ).select_related('Leave_Type_Master').values(
        'Emp_code',
        'Start_Date',
        'End_Date',
        'Status',
        'Leave_Type_Master__id',
        'Leave_Type_Master__Type'
    ))

    Selected_Leave_Application = []
    for leave in leave_applications:
        Selected_Leave_Application.append({
            "Emp_code": leave["Emp_code"],
            "Start_Date": leave["Start_Date"].strftime("%Y-%m-%d"),
            "End_Date": leave["End_Date"].strftime("%Y-%m-%d"),
            "Status": leave["Status"],
            "Leave_Type_Master": {
                "id": leave["Leave_Type_Master__id"],
                "Type": leave["Leave_Type_Master__Type"],
            }
        })

    # qs = Emp_Leave_Balance_Master.objects.filter(
    #     OrganizationID=OrganizationID,
    #     IsDelete=False,
    #     Emp_code=EmployeeCode
    # )

    # print(qs.query)  # Shows the raw SQL
    # print(qs.count())  # Executes the query and shows the count


        
        
    # Fetch Employee Personal Details
    Empobjs = EmployeePersonalDetails.objects.filter(
        IsDelete=False, OrganizationID=OrganizationID, IsEmployeeCreated=True, EmployeeCode=EmployeeCode,
    ).values('EmployeeCode', 'Prefix', 'FirstName', 'MiddleName', 'LastName')

    # Create a dictionary mapping EmployeeCode to full name
    employee_data = {}
    for emp in Empobjs:
        emp_code = emp["EmployeeCode"]
        full_name = f"{emp['FirstName']} {emp['MiddleName']} {emp['LastName']}".strip()
        
        employee_data[emp_code] = {
            "EmployeeCode": emp_code,
            "EmployeeName": full_name,
            "Attendance": [],  # Initialize an empty list for attendance
        }

    attendance_data = Attendance_Data.objects.filter(
        OrganizationID=OrganizationID,
        IsDelete=False,
        # Date__year=Selected_Year, 
        # Date__month=Selected_Month,
        EmployeeCode=EmployeeCode  # Restrict normal users to their own data
    ).distinct()


    if attendance_data.exists():  # Check if data exists
        for attendance in attendance_data:
            emp_code = attendance.EmployeeCode

            if emp_code not in employee_data:
                employee_data[emp_code] = {
                    "EmployeeCode": emp_code,
                    "EmployeeName": "Unknown",  # Default name if not found
                    "Attendance": [],
                }

            # Add attendance data
            employee_data[emp_code]["Attendance"].append({
                'title': attendance.Status,
                'in_time': format_time(attendance.In_Time),
                'out_time': format_time(attendance.Out_Time),
                's_in_time': format_time(attendance.S_In_Time),
                's_out_time': format_time(attendance.S_Out_Time),
                'duty_hours': attendance.Duty_Hour,
                'status': attendance.Status if attendance.Status else "",
                'type': 'attendance',
                'Date': attendance.Date,  # Store as datetime for sorting
                'DateFormatted': attendance.Date.strftime('%d-%m-%Y'),
            })

            for emp_code in employee_data:
                employee_data[emp_code]["Attendance"].sort(key=lambda x: x["Date"])  # Oldest date first
    else:
        attendance = None


    leave_data = Leave_Application.objects.filter(
        OrganizationID=OrganizationID,
        IsDelete=False,
        # Start_Date__year=Selected_Year,
        # Start_Date__month=Selected_Month,
        Emp_code=EmployeeCode  # Restrict normal users to their own data
    ).distinct()


    for leave in leave_data:
        emp_code = leave.Emp_code
        leave_days = (leave.End_Date - leave.Start_Date).days + 1 if leave.Start_Date and leave.End_Date else 0
        # print('leave days are here ------ ',leave_days)

        # Ensure the employee exists in employee_data
        if emp_code not in employee_data:
            employee_data[emp_code] = {
                "EmployeeCode": emp_code,
                "EmployeeName": "Unknown",
                "Attendance": [],
            }

        leave_dict = {
            'title': leave.Leave_Type_Master.Type,
            'Leavestatus': leave.Status,
            'start': leave.Start_Date.strftime('%d-%m-%Y'),
            'end': leave.End_Date.strftime('%d-%m-%Y'),
            'leave_Days': leave_days,
            'type': 'leave',
            'Reason': leave.Reason,
            'Total_credit': leave.Total_credit,
            'ReportingtoDesigantion': leave.ReportingtoDesigantion,
            'Remark': leave.Remark,
        }

        employee_data[emp_code]["Attendance"].append(leave_dict)



    return JsonResponse({
        'Emobj': Emobj_data,
        'Selected_Leave_Application': Selected_Leave_Application,
        'leave_requset_Pending_count': leave_requset_Pending_count,
        'leave_requset_rejected_count': leave_requset_rejected_count,
        'leave_requset_appr_count': leave_requset_appr_count,
        # 'Selected_Leave_Application': Selected_Leave_Application,
        'leave_balance': leave_balance_data,
        'employee_data': employee_data,
    }, safe=False)




def EmployeeCardDetails_EmployeeDashboard(EmpID, OrganizationID):
    Emobj = EmployeePersonalDetails.objects.only(
        'EmpID', 'EmployeeCode', 'FirstName', 'MiddleName', 'LastName',
        'MobileNumber', 'EmailAddress', 'ProfileImageFileName',
        'DateofBirth', 'Gender'
    ).filter(
        IsDelete=False,
        EmpID=EmpID,
        OrganizationID=OrganizationID
    ).first()

    Workobj = EmployeeWorkDetails.objects.only(
        'Department', 'EmpStatus', 'Designation', 'Level',
        'DateofJoining', 'ReportingtoDesignation',
        'ReportingtoDepartment', 'ReportingtoLevel'
    ).filter(
        OrganizationID=OrganizationID,
        IsDelete=False,
        IsSecondary=False,
        EmpID=EmpID
    ).first()

    if Emobj and Workobj:
        tenure = Workobj.tenure_till_today()

        Emobj.Department = Workobj.Department
        Emobj.EmpStatus = Workobj.EmpStatus
        Emobj.Designation = Workobj.Designation
        Emobj.Level = Workobj.Level
        Emobj.DateofJoining = Workobj.DateofJoining
        Emobj.ReportingtoDesignation = Workobj.ReportingtoDesignation
        Emobj.ReportingtoDepartment = Workobj.ReportingtoDepartment
        Emobj.ReportingtoLevel = Workobj.ReportingtoLevel
        Emobj.TenureTillToday = tenure

    return Emobj





# from datetime import date, timedelta
# from django.db.models import Count, Case, When, IntegerField
# from django.http import JsonResponse

# def Employee_Personal_Dashboard_API(request):
#     if 'OrganizationID' not in request.session:
#         return JsonResponse({'error': 'Session expired or invalid'}, status=401)

#     OrganizationID = request.session["OrganizationID"]
#     EmployeeCode = str(request.session["EmployeeCode"]).strip()

#     # Step 1: Get EmpID
#     Emp_Id = EmployeePersonalDetails.objects.filter(
#         EmployeeCode=EmployeeCode, OrganizationID=OrganizationID, IsDelete=False
#     ).values_list('EmpID', flat=True).first()

#     if not Emp_Id:
#         return JsonResponse({'error': 'Invalid employee code'}, status=400)

#     # Step 2: Get Employee Card Details (optimized)
#     Emobj = EmployeeCardDetails_EmployeeDashboard(Emp_Id, OrganizationID)

#     Emobj_data = {
#         'EmpID': Emobj.EmpID,
#         'EmployeeCode': Emobj.EmployeeCode,
#         'FullName': f'{Emobj.FirstName} {Emobj.MiddleName} {Emobj.LastName}'.strip(),
#         'Department': Emobj.Department,
#         'EmpStatus': Emobj.EmpStatus,
#         'Designation': Emobj.Designation,
#         'Level': Emobj.Level,
#         'DateofJoining': Emobj.DateofJoining.strftime('%Y-%m-%d') if Emobj.DateofJoining else None,
#         'ReportingtoDesignation': Emobj.ReportingtoDesignation,
#         'ReportingtoDepartment': Emobj.ReportingtoDepartment,
#         'ReportingtoLevel': Emobj.ReportingtoLevel,
#         'TenureTillToday': Emobj.TenureTillToday,
#         'MobileNumber': Emobj.MobileNumber,
#         'EmailAddress': Emobj.EmailAddress,
#         'ProfileImageFileName': Emobj.ProfileImageFileName,
#         'DateofBirth': Emobj.DateofBirth,
#         'Gender': Emobj.Gender,
#     }

#     # Step 3: Leave Balance (optimized)
#     leave_balance = list(
#         Emp_Leave_Balance_Master.objects.filter(
#             OrganizationID=OrganizationID, IsDelete=False, Emp_code=EmployeeCode
#         )
#         .select_related('Leave_Type_Master')
#         .values(
#             'Emp_code',
#             'Balance',
#             'Leave_Type_Master__id',
#             'Leave_Type_Master__Type'
#         )
#     )

#     # Step 4: Leave counts (single DB hit)
#     leave_status_counts = Leave_Application.objects.filter(
#         OrganizationID=OrganizationID,
#         IsDelete=False,
#         Emp_code=EmployeeCode
#     ).aggregate(
#         leave_requset_appr_count=Count(Case(When(Status=1, then=1), output_field=IntegerField())),
#         leave_requset_Pending_count=Count(Case(When(Status=0, then=1), output_field=IntegerField())),
#         leave_requset_rejected_count=Count(Case(When(Status=-1, then=1), output_field=IntegerField())),
#     )

#     # Step 5: Upcoming Leaves (next 90 days)
#     today = date.today()
#     next_90_days = today + timedelta(days=90)

#     upcoming_leaves = list(
#         Leave_Application.objects.filter(
#             IsDelete=False,
#             Emp_code=EmployeeCode,
#             OrganizationID=OrganizationID,
#             Start_Date__range=(today, next_90_days)
#         )
#         .select_related('Leave_Type_Master')
#         .values(
#             'Emp_code',
#             'Start_Date',
#             'End_Date',
#             'Status',
#             'Leave_Type_Master__id',
#             'Leave_Type_Master__Type'
#         )
#     )

#     Selected_Leave_Application = [{
#         "Emp_code": leave["Emp_code"],
#         "Start_Date": leave["Start_Date"].strftime("%Y-%m-%d"),
#         "End_Date": leave["End_Date"].strftime("%Y-%m-%d"),
#         "Status": leave["Status"],
#         "Leave_Type_Master": {
#             "id": leave["Leave_Type_Master__id"],
#             "Type": leave["Leave_Type_Master__Type"],
#         }
#     } for leave in upcoming_leaves]

#     # Step 6: Attendance
#     attendance_data = Attendance_Data.objects.filter(
#         OrganizationID=OrganizationID,
#         IsDelete=False,
#         EmployeeCode=EmployeeCode
#     ).order_by('Date')

#     attendance_list = [{
#         'title': att.Status,
#         'in_time': format_time(att.In_Time),
#         'out_time': format_time(att.Out_Time),
#         's_in_time': format_time(att.S_In_Time),
#         's_out_time': format_time(att.S_Out_Time),
#         'duty_hours': att.Duty_Hour,
#         'status': att.Status or "",
#         'type': 'attendance',
#         'Date': att.Date,
#         'DateFormatted': att.Date.strftime('%d-%m-%Y'),
#     } for att in attendance_data]

#     # Step 7: Past Leave Applications
#     leave_data = Leave_Application.objects.filter(
#         OrganizationID=OrganizationID,
#         IsDelete=False,
#         Emp_code=EmployeeCode
#     ).select_related('Leave_Type_Master')

#     past_leave_list = []
#     for leave in leave_data:
#         leave_days = (leave.End_Date - leave.Start_Date).days + 1 if leave.Start_Date and leave.End_Date else 0
#         past_leave_list.append({
#             'title': leave.Leave_Type_Master.Type,
#             'Leavestatus': leave.Status,
#             'start': leave.Start_Date.strftime('%d-%m-%Y'),
#             'end': leave.End_Date.strftime('%d-%m-%Y'),
#             'leave_Days': leave_days,
#             'type': 'leave',
#             'Reason': leave.Reason,
#             'Total_credit': leave.Total_credit,
#             'ReportingtoDesigantion': leave.ReportingtoDesigantion,
#             'Remark': leave.Remark,
#         })

#     return JsonResponse({
#         'Emobj': Emobj_data,
#         'Selected_Leave_Application': Selected_Leave_Application,
#         **leave_status_counts,
#         'leave_balance': leave_balance,
#         'attendance': attendance_list,
#         'past_leaves': past_leave_list,
#     }, safe=False)



# def EmployeeCardDetails_EmployeeDashboard(EmpID, OrganizationID):
#     # Use select_related to join Work Details if FK exists (assuming relation exists)
#     Emobj = EmployeePersonalDetails.objects.filter(
#         IsDelete=False,
#         EmpID=EmpID,
#         OrganizationID=OrganizationID
#     ).first()

#     Workobj = EmployeeWorkDetails.objects.filter(
#         OrganizationID=OrganizationID,
#         IsDelete=False,
#         IsSecondary=False,
#         EmpID=EmpID
#     ).first()

#     if Emobj and Workobj:
#         tenure = Workobj.tenure_till_today()

#         # Do not save — just attach values temporarily
#         Emobj.Department = Workobj.Department
#         Emobj.EmpStatus = Workobj.EmpStatus
#         Emobj.Designation = Workobj.Designation
#         Emobj.Level = Workobj.Level
#         Emobj.DateofJoining = Workobj.DateofJoining
#         Emobj.ReportingtoDesignation = Workobj.ReportingtoDesignation
#         Emobj.ReportingtoDepartment = Workobj.ReportingtoDepartment
#         Emobj.ReportingtoLevel = Workobj.ReportingtoLevel
#         Emobj.TenureTillToday = tenure

#     return Emobj


