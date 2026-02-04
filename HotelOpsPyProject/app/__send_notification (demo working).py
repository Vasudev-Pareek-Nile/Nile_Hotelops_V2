import threading
import requests

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


def Send_Live_Notification(user_id, Title, Message, OrgID, ModuleName, action, user_type, priority):
    """Send notification asynchronously using a thread"""
    def background_task():
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

    # ✅ Start background thread (non-blocking)
    threading.Thread(target=background_task, daemon=True).start()

    print(f"i execute successfully userids={user_id}")
    return "Notification triggered asynchronously"
