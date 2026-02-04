
import requests
import json

def send_notification():
    url = "https://hopsnoteapi-hcgte9grewc3cmav.centralindia-01.azurewebsites.net/api/Notifications"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "userId": ["20250421158544"],
        "title": "Hello",
        "message": "Sir Hello",
        "type": "info",
        "organizationId": "3",
        "moduleName": "GuestGlith",
        "action": "CREATE",
        "hopsId": "20251015168427",
        "userType": "admin",
        "priority": "high"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("✅ Notification sent successfully!")
        else:
            print(f"❌ Failed to send notification. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print("⚠️ Error while sending notification:", e)


if __name__ == "__main__":
    send_notification()


    