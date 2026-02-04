


def calculate_profile_completion(employee, modelname):
    filled_fields = 0
    missing_fields = []

    # Field mapping with friendly display names
    field_mapping = {
    "Personal Details": { 
        'EmployeeCode': 'Employee Code',
        'Prefix': 'Prefix',
        'FirstName': 'First Name',
        'LastName': 'Last Name',
        'Gender': 'Gender',
        'MobileNumber': 'Mobile Number',
        'ProfileImageFileName': 'Profile Image',
        'CovidVaccination': 'Covid Vaccination Status',
        'MaritalStatus': 'Marital Status',
        'DateofBirth': 'Date of Birth',
        'age': 'Age',
        'EmailAddress': 'Email Address',
       
    },
    "Work Details": {
        'Designation': 'Designation',
        'Department': 'Department',
        'EmpStatus': 'Employee Status',
        'Level': 'Level',
        'DateofJoining': 'Date of Joining',
        'CompanyAccommodation': 'Company Accommodation',
        'Salary': 'Salary',
        'EmploymentType': 'Employment Type',
        'ReportingtoDesignation': 'Reporting to Designation',
        'ReportingtoDepartment': 'Reporting to Department',
        'ReportingtoLevel': 'Reporting to Level',
        'DottedLine': 'Dotted Line',
        'Locker': 'Locker',
       
        
    },
    "Emergency Information": {
        'FirstName': 'Emergency First Name',
        'LastName': 'Emergency Last Name',
        'Relation': 'Emergency Relation',
        'EmergencyContactNumber_1': 'Emergency Contact Number 1',
        'EmergencyContactNumber_2': 'Emergency Contact Number 2',
        'ProvidentFundNumber': 'Provident Fund Number',
       
        'BloodGroup': 'Blood Group',
    },
    "Family Details": {
        'MotherName': 'Mother Name',
        'FatherName': 'Father Name',
    },
    "Address Information": {
        'Permanent_Address': 'Permanent Address',
        'Permanent_City': 'Permanent City',
        'Permanent_State': 'Permanent State',
        'Permanent_Pincode': 'Permanent Pincode',
        'Permanent_HousePhoneNumber': 'Permanent House Phone Number',
        'Temporary_Address': 'Temporary Address',
        'Temporary_City': 'Temporary City',
        'Temporary_State': 'Temporary State',
        'Temporary_Pincode': 'Temporary Pincode',
        'Temporary_HousePhoneNumber': 'Temporary House Phone Number',
    },
    "Identity Information": {
        'AadhaarNumber': 'Aadhaar Number',
        'AadhaarFileName': 'Aadhaar File',
    },
    "Bank Information": {
        'BankAccountNumber': 'Bank Account Number',
        'NameofBank': 'Name of Bank',
        'BankBranch': 'Bank Branch',
        'IFSCCode': 'IFSC Code',
    },
}


    model_fields = field_mapping.get(modelname, {})
    for field, display_name in model_fields.items():
        if getattr(employee, field, None):  
            filled_fields += 1
        else:
            missing_fields.append(display_name)  

    total_fields = len(model_fields)
    profile_completion_percentage = (filled_fields / total_fields) * 100 if total_fields > 0 else 0

    return profile_completion_percentage, missing_fields





from HumanResources.models import (
    EmployeePersonalDetails,
    EmployeeWorkDetails,
    EmployeeEmergencyInformationDetails,
    EmployeeFamilyDetails,
    EmployeeAddressInformationDetails,
    EmployeeIdentityInformationDetails,
    EmployeeBankInformationDetails
)

def update_employee_profile(emp_id, organization_id):
    try:
        # Fetch the employee's personal details
        employee = EmployeePersonalDetails.objects.filter(EmpID=emp_id, OrganizationID=organization_id, IsDelete=False).first()

        if not employee:
            return f"Employee with EmpID {emp_id} and OrganizationID {organization_id} not found."

        total_filled_percentage = 0
        combined_missing_fields = []

        # Personal Details
        personal_completion, personal_missing_fields = calculate_profile_completion(employee, "Personal Details")
        total_filled_percentage += personal_completion
        combined_missing_fields.extend(personal_missing_fields)

        # Work Details
        work_details = EmployeeWorkDetails.objects.filter(EmpID=emp_id, IsDelete=False,IsSecondary=False).first()
        if work_details:
            work_completion, work_missing_fields = calculate_profile_completion(work_details, "Work Details")
            total_filled_percentage += work_completion
            combined_missing_fields.extend(work_missing_fields)

        # Emergency Information
        emergency_info = EmployeeEmergencyInformationDetails.objects.filter(EmpID=emp_id, IsDelete=False).first()
        if emergency_info:
            emergency_completion, emergency_missing_fields = calculate_profile_completion(emergency_info, "Emergency Information")
            total_filled_percentage += emergency_completion
            combined_missing_fields.extend(emergency_missing_fields)

        # Family Details
        family_info = EmployeeFamilyDetails.objects.filter(EmpID=emp_id, IsDelete=False).first()
        if family_info:
            family_completion, family_missing_fields = calculate_profile_completion(family_info, "Family Details")
            total_filled_percentage += family_completion
            combined_missing_fields.extend(family_missing_fields)

        # Address Information
        address_info = EmployeeAddressInformationDetails.objects.filter(EmpID=emp_id, IsDelete=False).first()
        if address_info:
            address_completion, address_missing_fields = calculate_profile_completion(address_info, "Address Information")
            total_filled_percentage += address_completion
            combined_missing_fields.extend(address_missing_fields)

        # Identity Information
        identity_info = EmployeeIdentityInformationDetails.objects.filter(EmpID=emp_id, IsDelete=False).first()
        if identity_info:
            identity_completion, identity_missing_fields = calculate_profile_completion(identity_info, "Identity Information")
            total_filled_percentage += identity_completion
            combined_missing_fields.extend(identity_missing_fields)

        # Bank Information
        bank_info = EmployeeBankInformationDetails.objects.filter(EmpID=emp_id, IsDelete=False).first()
        if bank_info:
            bank_completion, bank_missing_fields = calculate_profile_completion(bank_info, "Bank Information")
            total_filled_percentage += bank_completion
            combined_missing_fields.extend(bank_missing_fields)

        # Calculate overall average profile completion percentage
        total_sections = 7  # Total sections
        overall_profile_completion = total_filled_percentage / total_sections

        # Update EmployeePersonalDetails with aggregated data
        employee.ProfileCompletion = round(overall_profile_completion, 2)
        employee.MissingFields = ','.join(set(combined_missing_fields)) if combined_missing_fields else None
        employee.save()

        return f"Employee {employee.EmployeeCode} updated with ProfileCompletion: {round(overall_profile_completion, 2)}%"
    except Exception as e:
        return f"An error occurred: {str(e)}"
