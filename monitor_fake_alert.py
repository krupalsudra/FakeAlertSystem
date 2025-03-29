import time
import requests
import log_manager

# Telegram Bot Configuration (Replace with your actual credentials)
TELEGRAM_BOT_TOKEN = "your_correct_telegram_bot_token"
TELEGRAM_CHAT_ID = "your_telegram_chat_id"

# Fake Data Lists
fake_calls = ["+1234567890", "+1987654321", "+1122334455"]
fake_websites = ["scam-site.com", "free-money.xyz", "clickhere.win"]
fake_emails = ["fake@scam.com", "lottery@fraud.net", "winmoney@spam.org"]

# Function to Send Telegram Alert
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    return response.json()

# 24/7 Monitoring Function
def monitor_fake_alerts():
    while True:
        new_fake_data = [
            {"type": "Fake Call", "value": "+1234567890"},
            {"type": "Fake Website", "value": "scam-site.com"},
            {"type": "Fake Email", "value": "fake@scam.com"}
        ]

        for data in new_fake_data:
            alert_type = data["type"]
            text = data["value"]

            if alert_type == "Fake Call" and text in fake_calls:
                log_manager.log_activity("Fake Call Detected", text)
                send_telegram_alert(f"🚨 Fake Call Alert! Number: {text}")

            elif alert_type == "Fake Website" and text in fake_websites:
                log_manager.log_activity("Fake Website Detected", text)
                send_telegram_alert(f"🚨 Fake Website Alert! URL: {text}")

            elif alert_type == "Fake Email" and text in fake_emails:
                log_manager.log_activity("Fake Email Detected", text)
                send_telegram_alert(f"🚨 Fake Email Alert! Email: {text}")

        time.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    monitor_fake_alerts()
