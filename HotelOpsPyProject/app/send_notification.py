import threading
import requests
# from HumanResources.models import EmployeeWorkDetails, EmployeePersonalDetails

class NotificationSender:
    def __init__(self):
        # self.url = "https://hopsnoteapi-hcgte9grewc3cmav.centralindia-01.azurewebsites.net/api/Notifications"
        self.url = "https://hopsna.hopr.in/api/Notifications"
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def send(self, EmpCode, title, message, organization_id, module_name, action, hopsId,
             user_type="admin", priority="high", type="info"):
        payload = {
            "EmpCode": EmpCode,
            # "EmpCode": user_ids if isinstance(EmpCode, list) else [user_ids],
            "title": title,
            "message": message,
            "type": type,
            "organizationId": str(organization_id),
            "moduleName": module_name,
            "action": action,
            "hopsId": hopsId,
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


def Send_Live_Notification(EmpCode,title, message, organization_id, module_name,hopsId, action, user_type, priority):
    """Send notification asynchronously using a thread"""
    # user_id=["20250421158544"],
    def background_task():
        # EmpWorkDetails = EmployeeWorkDetails.objects.filter(Designation__in=ReportingtoDesigantion, OrganizationID=OrgID, IsSecondary=False, IsDelete=False).values('EmpID')
        # EmpPersonalDetails = EmployeeWorkDetails.objects.filter(EmpID=EmpWorkDetails.EmpID, IsDelete=False).values('EmployeeCode')

        EmpCodeData = Get_EmployeeCode_by_Designation_OrgID(EmpCode,organization_id)
        print("Employee Code data is here::", EmpCodeData)
        notifier.send(
            EmpCode=EmpCodeData,
            title=title,
            message=message,
            organization_id=organization_id,
            module_name=module_name,
            action=action,
            hopsId=hopsId,
            user_type=user_type,
            priority=priority
        )

    # Start background thread (non-blocking)
    threading.Thread(target=background_task, daemon=True).start()

    # print(f"i execute successfully userids={user_id}")
    return "Notification triggered asynchronously"




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




# Example usage:
# if __name__ == "__main__":
#     # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

#     notifier = NotificationSender()

#     notifier.send(
#         EmpCode=["001"],
#         title="Hello",
#         message="Sir Hello my namge is vasudev",
#         organization_id=3,
#         module_name="GuestGlith",
#         action="CREATE",
#         hops_id="3265",
#         user_type="admin",
#         priority="high"
#     )

def Get_Employee_Name_By_EmpCode(EmpCode, OrgID):
        EmpName=''
        if EmpCode and OrgID:
            EmpName = EmployeeMaster.objects.filter(
                EmployeeCode=EmpCode,
                OrganizationID=OrgID,
                IsSecondary=False,
                IsDelete=False
            ).values_list('EmpName', flat=True).first()
        else:
            EmpName=''

        return EmpName


def Send_Leave_Approval_Notification(EmpCode,title, message, organization_id, module_name,hopsId, action, user_type, priority):
    """Send notification asynchronously using a thread"""
    # user_id=["20250421158544"],
    def background_task():
        # EmpWorkDetails = EmployeeWorkDetails.objects.filter(Designation__in=ReportingtoDesigantion, OrganizationID=OrgID, IsSecondary=False, IsDelete=False).values('EmpID')
        # EmpPersonalDetails = EmployeeWorkDetails.objects.filter(EmpID=EmpWorkDetails.EmpID, IsDelete=False).values('EmployeeCode')

        # EmpCodeData = Get_EmployeeCode_by_Designation_OrgID(EmpCode,organization_id)
        EmpCodeData = list(EmpCode)
        # print("Employee Code data is here::", EmpCodeData)
        # print("organization_id data is here::", organization_id)
        # print
        notifier.send(
            EmpCode=EmpCodeData,
            title=title,
            message=message,
            organization_id=organization_id,
            module_name=module_name,
            action=action,
            hopsId=hopsId,
            user_type=user_type,
            priority=priority
        )

    # Start background thread (non-blocking)
    threading.Thread(target=background_task, daemon=True).start()

    # print(f"i execute successfully userids={user_id}")
    return "Notification triggered asynchronously"




def Send_APDP_Audit_CEO_Notification(EmpCode,title, message, organization_id, module_name,hopsId, action, user_type, priority):
    """Send notification asynchronously using a thread"""
    # user_id=["20250421158544"],
    def background_task():
        # EmpWorkDetails = EmployeeWorkDetails.objects.filter(Designation__in=ReportingtoDesigantion, OrganizationID=OrgID, IsSecondary=False, IsDelete=False).values('EmpID')
        # EmpPersonalDetails = EmployeeWorkDetails.objects.filter(EmpID=EmpWorkDetails.EmpID, IsDelete=False).values('EmployeeCode')

        # EmpCodeData = Get_EmployeeCode_by_Designation_OrgID(EmpCode,organization_id)
        # EmpCodeData = EmpCode
        print("Employee Code data is here::", EmpCode)
        print("organization_id data is here::", organization_id)
        # print
        notifier.send(
            EmpCode=EmpCode,
            title=title,
            message=message,
            organization_id=organization_id,
            module_name=module_name,
            action=action,
            hopsId=hopsId,
            user_type=user_type,
            priority=priority
        )

    # Start background thread (non-blocking)
    threading.Thread(target=background_task, daemon=True).start()

    # print(f"i execute successfully userids={user_id}")
    return "Notification triggered asynchronously"

