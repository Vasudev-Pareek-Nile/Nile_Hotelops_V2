from .models import EmployeePersonalDetails,EmployeeEmergencyInformationDetails,EmployeeWorkDetails

from django.db.models import Subquery, OuterRef


def  NewJoineeRerports(OrganizationID):
 
    work_details = EmployeeWorkDetails.objects.filter(EmpID=OuterRef('EmpID'),IsDelete=False,OrganizationID=OrganizationID,IsSecondary=False)

    employees = EmployeePersonalDetails.objects.annotate(
        work_designation=Subquery(work_details.values('Designation')[:1]),
        work_department=Subquery(work_details.values('Department')[:1]),
        work_email=Subquery(work_details.values('OfficialEmailAddress')[:1])
    ).filter(IsDelete=False,OrganizationID=OrganizationID)

   
    for emp in employees:
        print(f"Emp Code:{emp.EmployeeCode}",f"Name: {emp.FirstName} {emp.LastName}",f"Designation: {emp.work_designation}",f"Department: {emp.work_department}",f"Official Email: {emp.work_email}")

   

from prettytable import PrettyTable

def EmergencyInformation(OrganizationID):
    work_details = EmployeeWorkDetails.objects.filter(EmpID=OuterRef('EmpID'), IsDelete=False,IsSecondary=False, OrganizationID=OrganizationID)
    Emerg_details = EmployeeEmergencyInformationDetails.objects.filter(EmpID=OuterRef('EmpID'), IsDelete=False, OrganizationID=OrganizationID)

    employees = EmployeePersonalDetails.objects.annotate(
        work_designation=Subquery(work_details.values('Designation')[:1]),
        work_department=Subquery(work_details.values('Department')[:1]),
        work_email=Subquery(work_details.values('OfficialEmailAddress')[:1]),
        emergency_first_name=Subquery(Emerg_details.values('FirstName')[:1]),
        emergency_middle_name=Subquery(Emerg_details.values('MiddleName')[:1]),
        emergency_last_name=Subquery(Emerg_details.values('LastName')[:1]),
        emergency_relation=Subquery(Emerg_details.values('Relation')[:1]),
        emergency_contact_1=Subquery(Emerg_details.values('EmergencyContactNumber_1')[:1]),
        emergency_contact_2=Subquery(Emerg_details.values('EmergencyContactNumber_2')[:1]),
        provident_fund_number=Subquery(Emerg_details.values('ProvidentFundNumber')[:1]),
        esi_number=Subquery(Emerg_details.values('ESINumber')[:1]),
        blood_group=Subquery(Emerg_details.values('BloodGroup')[:1]),
    ).filter(IsDelete=False, OrganizationID=OrganizationID)

    table = PrettyTable()
    table.field_names = [
        "Emp Code", "Name", "Designation", "Department", "Official Email",
        "Emergency Contact Name", "Relation", "Contact 1", "Contact 2",
        "PF Number", "ESI Number", "Blood Group"
    ]

    # Add rows to the table
    for emp in employees:
        emergency_name = f"{emp.emergency_first_name} {emp.emergency_middle_name or ''} {emp.emergency_last_name}".strip()
        table.add_row([
            emp.EmployeeCode,
            f"{emp.FirstName} {emp.LastName}",
            emp.work_designation,
            emp.work_department,
            emp.work_email,
            emergency_name,
            emp.emergency_relation,
            emp.emergency_contact_1,
            emp.emergency_contact_2,
            emp.provident_fund_number,
            emp.esi_number,
            emp.blood_group
        ])

    # Print the table
    print(table)
