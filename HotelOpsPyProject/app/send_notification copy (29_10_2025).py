import threading
import requests
from HumanResources.models import EmployeeWorkDetails, EmployeePersonalDetails

class NotificationSender:
    def __init__(self):
        self.url = "https://hopsnoteapi-hcgte9grewc3cmav.centralindia-01.azurewebsites.net/api/Notifications"
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def send(self, user_ids, title, message, organization_id, module_name, action, hops_id,
             user_type="admin", priority="high", type="info"):
        payload = {
            "userId": user_ids if isinstance(user_ids, list) else [user_ids],
            "title": title,
            "message": message,
            "type": type,
            "organizationId": str(organization_id),
            "moduleName": module_name,
            "action": action,
            "hopsId": hops_id,
            "userType": user_type,
            "priority": priority
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            if response.status_code in [200, 201]:
                print(f"✅ Notification sent successfully! ({response.status_code})")
            else:
                print(f"❌ Failed to send notification. Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print("⚠️ Error while sending notification:", e)


# Shared instance
notifier = NotificationSender()


def Send_Live_Notification(EmpCode,Title, Message, OrgID, ModuleName,hops_id, action, user_type, priority):
    """Send notification asynchronously using a thread"""
    user_id=["20250421158544"],
    def background_task():
        # EmpWorkDetails = EmployeeWorkDetails.objects.filter(Designation__in=ReportingtoDesigantion, OrganizationID=OrgID, IsSecondary=False, IsDelete=False).values('EmpID')
        # EmpPersonalDetails = EmployeeWorkDetails.objects.filter(EmpID=EmpWorkDetails.EmpID, IsDelete=False).values('EmployeeCode')

        EmpCodeData = Get_EmployeeCode_by_Designation_OrgID(EmpCode,OrgID)
        print("Employee Code data is here::", EmpCodeData)
        notifier.send(
            user_ids=EmpCodeData,
            title=Title,
            message=Message,
            organization_id=OrgID,
            module_name=ModuleName,
            action=action,
            hops_id=hops_id,
            user_type=user_type,
            priority=priority
        )

    # Start background thread (non-blocking)
    threading.Thread(target=background_task, daemon=True).start()

    # print(f"i execute successfully userids={user_id}")
    return "Notification triggered asynchronously"



# def Get_EmployeeCode_by_Designation_OrgID(EmpCode,ReportingtoDesigantion,OrgID):
#     EmpWorkDetails = EmployeeWorkDetails.objects.filter(Designation__in=ReportingtoDesigantion, OrganizationID=OrgID, IsSecondary=False, IsDelete=False).values('EmpID')
#     EmpPersonalDetails = EmployeeWorkDetails.objects.filter(EmpID=EmpWorkDetails.EmpID, IsDelete=False).values('EmployeeCode')
#     return EmpPersonalDetails

    


# def Get_EmployeeCode_by_Designation_OrgID(EmpCode, ReportingtoDesigantion, OrgID):
#     # print("Reporting to designation is here", ReportingtoDesigantion)
#     # print("OrgID is here", OrgID)
#     # Get EmpIDs for given designation and organization
#     emp_ids = EmployeeWorkDetails.objects.filter(
#         Designation__iexact=ReportingtoDesigantion,
#         OrganizationID=OrgID,
#         IsSecondary=False,
#         IsDelete=False
#     ).values_list('EmpID', flat=True)
#     # print("Employee Id is here::", emp_ids)

#     # Fetch EmployeeCodes for those EmpIDs
#     EmpPersonalDetails = EmployeePersonalDetails.objects.filter(
#         EmpID__in=emp_ids,
#         IsDelete=False
#     ).values_list('EmployeeCode', flat=True)
#     # print("EmpPersonalDetails Id is here::", EmpPersonalDetails)

#     return list(EmpPersonalDetails)


from app.models import EmployeeMaster
def Get_EmployeeCode_by_Designation_OrgID(EmpCode, OrgID):
    # Get the designation that this employee reports to
    reporting_to_designation = EmployeeMaster.objects.filter(
        EmployeeCode=EmpCode,
        OrganizationID=OrgID,
        IsSecondary=False,
        IsDelete=False
    ).values_list('ReportingtoDesigantion', flat=True).first()

    # No reporting designation found
    if not reporting_to_designation:
        return []  

    # Get all employee codes with that designation
    emp_codes = EmployeeMaster.objects.filter(
        Designation__iexact=reporting_to_designation,
        OrganizationID=OrgID,
        IsSecondary=False,
        IsDelete=False
    ).values_list('EmployeeCode', flat=True)

    return list(emp_codes)
