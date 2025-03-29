import requests
import datetime
import os

# 🔹 Telegram Bot Configuration (Replace with your actual credentials)
TELEGRAM_BOT_TOKEN = "7778478472:AAG3vqv-CSmiarFBgDDQjdJtgGQlqrZ8oFo"
TELEGRAM_CHAT_ID = "6728315195"

# 🔹 Log File Path (Only You Can Access)
LOG_FILE = "logs.txt"

# 🔹 Function to Store Logs
def log_activity(activity_type, data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {activity_type}: {data}\n"
    
    # Append log entry to the file
    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_entry)
    
    # Also send log to Telegram
    send_telegram_alert(f"🔍 **New Alert Logged**\n📌 Type: {activity_type}\n📢 Data: {data}")

# 🔹 Function to Send Logs to Telegram
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"⚠️ Error Sending Telegram Alert: {e}")

# 🔹 Function to Show Logs (Only You Can See)
def get_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as log_file:
            return log_file.read()
    return "No logs available."
