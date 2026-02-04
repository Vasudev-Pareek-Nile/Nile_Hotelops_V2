from django.core.management.base import BaseCommand
from HumanResources.models import (
    EmployeePersonalDetails,
    EmployeeWorkDetails,
    EmployeeEmergencyInformationDetails,
    EmployeeFamilyDetails,
    EmployeeAddressInformationDetails,
    EmployeeIdentityInformationDetails,
    EmployeeBankInformationDetails
)
from HumanResources.Profile import calculate_profile_completion
from app.models import OrganizationMaster

class Command(BaseCommand):
    help = 'Updates profile completion for all employees'

    def handle(self, *args, **kwargs):
        # Optionally, you can filter by organization
        orgs = OrganizationMaster.objects.filter(IsDelete=False)
        for org in orgs:
              
             

                OrganizationID = org.OrganizationID
       
                employees = EmployeePersonalDetails.objects.filter(IsDelete=False, OrganizationID=OrganizationID)
                
                if employees:
                    for employee in employees:
                        total_filled_percentage = 0
                        combined_missing_fields = []

                        # Personal Details
                        personal_completion, personal_missing_fields = calculate_profile_completion(employee, "Personal Details")
                        total_filled_percentage += personal_completion
                        combined_missing_fields.extend(personal_missing_fields)

                        # Work Details
                        work_details = EmployeeWorkDetails.objects.filter(EmpID=employee.EmpID, IsDelete=False,IsSecondary=False).first()
                        if work_details:
                            work_completion, work_missing_fields = calculate_profile_completion(work_details, "Work Details")
                            total_filled_percentage += work_completion
                            combined_missing_fields.extend(work_missing_fields)

                        # Emergency Information
                        emergency_info = EmployeeEmergencyInformationDetails.objects.filter(EmpID=employee.EmpID, IsDelete=False).first()
                        if emergency_info:
                            emergency_completion, emergency_missing_fields = calculate_profile_completion(emergency_info, "Emergency Information")
                            total_filled_percentage += emergency_completion
                            combined_missing_fields.extend(emergency_missing_fields)

                        # Family Details
                        family_info = EmployeeFamilyDetails.objects.filter(EmpID=employee.EmpID, IsDelete=False).first()
                        if family_info:
                            family_completion, family_missing_fields = calculate_profile_completion(family_info, "Family Details")
                            total_filled_percentage += family_completion
                            combined_missing_fields.extend(family_missing_fields)

                        # Address Information
                        address_info = EmployeeAddressInformationDetails.objects.filter(EmpID=employee.EmpID, IsDelete=False).first()
                        if address_info:
                            address_completion, address_missing_fields = calculate_profile_completion(address_info, "Address Information")
                            total_filled_percentage += address_completion
                            combined_missing_fields.extend(address_missing_fields)

                        # Identity Information
                        identity_info = EmployeeIdentityInformationDetails.objects.filter(EmpID=employee.EmpID, IsDelete=False).first()
                        if identity_info:
                            identity_completion, identity_missing_fields = calculate_profile_completion(identity_info, "Identity Information")
                            total_filled_percentage += identity_completion
                            combined_missing_fields.extend(identity_missing_fields)

                        # Bank Information
                        bank_info = EmployeeBankInformationDetails.objects.filter(EmpID=employee.EmpID, IsDelete=False).first()
                        if bank_info:
                            bank_completion, bank_missing_fields = calculate_profile_completion(bank_info, "Bank Information")
                            total_filled_percentage += bank_completion
                            combined_missing_fields.extend(bank_missing_fields)

                        # Calculate overall average profile completion percentage
                        total_sections = 7  # Now there are 7 sections: Personal, Work, Emergency, Family, Address, Identity, Bank
                        overall_profile_completion = total_filled_percentage / total_sections

                        # Update EmployeePersonalDetails with aggregated data
                        employee.ProfileCompletion = round(overall_profile_completion, 2)
                        employee.MissingFields = ','.join(set(combined_missing_fields)) if combined_missing_fields else None
                        employee.save()

                        self.stdout.write(self.style.SUCCESS(
                            f'Updated {employee.EmployeeCode} with ProfileCompletion: {overall_profile_completion}%'
                        ))

        self.stdout.write(self.style.SUCCESS(f'All employee profiles processed successfully for OrganizationID: {OrganizationID}'))
