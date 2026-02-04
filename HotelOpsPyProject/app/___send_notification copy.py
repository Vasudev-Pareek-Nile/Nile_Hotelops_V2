import requests
import json

class NotificationSender:
    def __init__(self):
        self.url = "https://hopsnoteapi-hcgte9grewc3cmav.centralindia-01.azurewebsites.net/api/Notifications"
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def send(self, user_ids, title, message, organization_id, module_name, action, hops_id, user_type="admin", priority="high", type="info"):
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
                print("✅ Notification sent successfully!")
            else:
                print(f"❌ Failed to send notification. Status: {response.status_code}, Response: {response.text}")
            return response
        except Exception as e:
            print("⚠️ Error while sending notification:", e)
            return None


# Shared instance
notifier = NotificationSender()


def Send_Live_Notification(user_ids, Title, Message, OrgID, ModuleName, Action="CREATE", HopsID=0, UserType="admin", priority="high"):
    return notifier.send(
        user_ids=user_ids,
        title=Title,
        message=Message,
        organization_id=OrgID,
        module_name=ModuleName,
        action=Action,
        hops_id=HopsID,
        user_type=UserType,
        priority=priority
    )

# Create a single shared instance
# notifier = NotificationSender()


# # Utility function for easier use
# def Send_Live_Notification(user_ids, Title, Message, OrgID, ModuleName, Action="CREATE", HopsID=0, UserType="admin", priority="high"):
#     return notifier.send(
#         user_ids=user_ids,
#         title=Title,
#         message=Message,
#         organization_id=OrgID,
#         module_name=ModuleName,
#         action=Action,
#         hops_id=HopsID,
#         user_type=UserType,
#         priority=priority
#     )


notifier = NotificationSender()

# # Example usage:
def Notifer_demo(user_id, Title, Message, OrgID,ModuleName,action,user_type,priority):
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"


    notifier.send(
        user_ids=user_id,
        title=Title,
        message=Message,
        organization_id=OrgID,
        module_name=ModuleName,
        action=action,
        hops_id="3265",
        user_type=user_type,
        priority=priority
    )

    print(f"i execute successfully userids={user_id}")
    return 'i execute successfully'




# # Example usage:
# if __name__ == "__main__":
#     # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

#     notifier = NotificationSender()

#     notifier.send(
#         user_ids=["20250421158544"],
#         title="Hello",
#         message="Sir Hello my namge is vasudev",
#         organization_id=3,
#         module_name="GuestGlith",
#         action="CREATE",
#         hops_id="3265",
#         user_type="admin",
#         priority="high"
#     )
