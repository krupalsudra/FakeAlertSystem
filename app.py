import streamlit as st
import re
import requests
import logging
import os
import json
from datetime import datetime

# ✅ Telegram Bot Configuration (Replace with your own credentials)
TELEGRAM_BOT_TOKEN = "7778478472:AAG3vqv-CSmiarFBgDDQjdJtgGQlqrZ8oFo"
TELEGRAM_CHAT_ID = "6728315195"

# ✅ Ensure logs directory exists
LOG_DIR = "logs"
LOG_FILE_JSON = os.path.join(LOG_DIR, "activity.json")
os.makedirs(LOG_DIR, exist_ok=True)

# ✅ Setup Logging
logging.basicConfig(filename=os.path.join(LOG_DIR, "activity.log"), level=logging.INFO, format="%(asctime)s - %(message)s")

# ✅ Fake Data Lists (Simulating a database)
fake_calls = ["1234567890", "9876543210", "1122334455"]
fake_websites = ["scam-site.com", "free-money.xyz", "clickhere.win"]
fake_emails = ["fake@scam.com", "lottery@fraud.net", "winmoney@spam.org"]

# 📌 **Validation Functions**
def is_valid_email(email):
    """Check if email is in valid format and lowercase."""
    email_regex = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
    return bool(re.match(email_regex, email))

def is_valid_phone(phone):
    """Check if phone number contains exactly 10 digits."""
    return phone.isdigit() and len(phone) == 10

def is_valid_website(url):
    """Check if the website starts with HTTPS (block HTTP)."""
    return url.startswith("https://")

# 📌 **Logging Function**
def log_activity(event_type, entity, status, action, details=""):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,
        "entity": entity,
        "status": status,
        "action": action,
        "details": details
    }
    with open(LOG_FILE_JSON, "a") as log_file:
        json.dump(log_entry, log_file)
        log_file.write("\n")
    logging.info(log_entry)

# 📌 **Telegram Alert Function**
def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(url, data=data)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Failed to send Telegram alert: {e}")

# 📌 **Detection Functions**
def detect_fake_phone(phone):
    if not is_valid_phone(phone):
        return "⚠️ Invalid phone number! It must be exactly 10 digits."
    
    if phone in fake_calls:
        alert_msg = f"❌ Fake Call Detected: {phone} - Blocked!"
        send_telegram_alert(alert_msg)
        log_activity("Phone Scan", phone, "Fake", "Blocked", "Detected as Fake Call")
        return alert_msg
    
    return "✅ This call seems safe."

def detect_fake_website(url):
    if not is_valid_website(url):
        return "❌ This website is blocked because it is not using HTTPS."
    
    if any(site in url for site in fake_websites):
        alert_msg = f"❌ Fake Website Detected: {url} - Access Blocked!"
        send_telegram_alert(alert_msg)
        log_activity("Website Scan", url, "Fake", "Blocked", "Detected as Fake Website")
        return alert_msg

    return "✅ This website seems safe."

def detect_fake_email(email):
    if not is_valid_email(email):
        return "⚠️ Invalid email format! Please enter a valid email in lowercase."

    if email in fake_emails:
        alert_msg = f"❌ Fake Email Detected: {email} - Blocked!"
        send_telegram_alert(alert_msg)
        log_activity("Email Scan", email, "Fake", "Blocked", "Detected as Fake Email")
        return alert_msg

    return "✅ This email seems safe."

# 🎯 **Streamlit UI**
st.title("🚨 Fake Alert Detection & Blocking System")
st.markdown("### Detect and block fake calls, websites, and emails instantly 24/7")

# 📌 Select alert type
alert_type = st.selectbox("Select alert type:", ["Fake Call", "Fake Website", "Fake Email"])
user_input = st.text_area("Enter details (Phone Number / URL / Email Address):", "").strip()

# 🔍 **Check Alert**
if st.button("Check Alert"):
    if alert_type == "Fake Call":
        result = detect_fake_phone(user_input)
    elif alert_type == "Fake Website":
        result = detect_fake_website(user_input)
    elif alert_type == "Fake Email":
        result = detect_fake_email(user_input)
    else:
        result = "⚠️ Unknown alert type."

    st.subheader(result)

# 🔒 **Footer**
st.markdown("🔒 **24/7 Real-time Protection Against Fraud**")
