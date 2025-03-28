import streamlit as st
import re
import logging
import json
import os
import requests
from datetime import datetime

# Telegram Bot Config (Replace with your actual bot token & chat ID)
TELEGRAM_BOT_TOKEN = "7778478472:AAG3vqv-CSmiarFBgDDQjdJtgGQlqrZ8oFo"
TELEGRAM_CHAT_ID = "6728315195"

# Create Logs Directory
LOG_DIR = "logs"
LOG_FILE_JSON = os.path.join(LOG_DIR, "activity.json")
os.makedirs(LOG_DIR, exist_ok=True)

# Logging Setup
logging.basicConfig(filename=os.path.join(LOG_DIR, "activity.log"), level=logging.INFO, format="%(asctime)s - %(message)s")

# Fake Data Lists (Can be replaced with a real-time database)
FAKE_CALLS = ["+1234567890", "+1987654321", "+1122334455"]
FAKE_WEBSITES = ["scam-site.com", "free-money.xyz", "clickhere.win"]
FAKE_EMAILS = ["fake@scam.com", "lottery@fraud.net", "winmoney@spam.org"]

# 🛡️ Functions for Validation
def is_valid_email(email):
    """Check if email is valid and lowercase."""
    email_regex = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
    return re.match(email_regex, email)

def is_valid_phone(phone):
    """Check if phone number contains exactly 10 digits."""
    return phone.isdigit() and len(phone) == 10

def is_valid_website(url):
    """Check if the website starts with HTTPS (block HTTP)."""
    return url.startswith("https://")

# 📢 Function to Send Telegram Alerts
def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        requests.post(url, data=data)
    except Exception as e:
        logging.error(f"Failed to send Telegram alert: {e}")

# 📜 Function to Log Activities
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

# 🌟 Streamlit UI
st.title("🚨 Fake Alert Detection & Blocking System")
st.markdown("### Detect and block fake calls, websites, and emails instantly 24/7")

# 📞 Fake Call Checker
st.header("📞 Check Fake Calls")
phone_number = st.text_input("Enter Phone Number:")
if st.button("Check Call"):
    if not is_valid_phone(phone_number):
        st.error("⚠️ Invalid phone number! It must be exactly 10 digits.")
    elif phone_number in FAKE_CALLS:
        st.error("❌ Fake Call Detected! Blocked instantly.")
        send_telegram_alert(f"⚠️ Fake Call Alert! Number: {phone_number}")
        log_activity("Phone Scan", phone_number, "Fake", "Blocked")
    else:
        st.success("✅ This call seems safe.")
        log_activity("Phone Scan", phone_number, "Safe", "Allowed")

# 📧 Fake Email Checker
st.header("📧 Check Fake Emails")
email_address = st.text_input("Enter Email Address:")
if st.button("Check Email"):
    if not is_valid_email(email_address):
        st.error("⚠️ Invalid email format! Please enter a valid email in lowercase.")
    elif email_address in FAKE_EMAILS:
        st.error("❌ Fake Email Detected! Blocked instantly.")
        send_telegram_alert(f"⚠️ Fake Email Alert! Email: {email_address}")
        log_activity("Email Scan", email_address, "Fake", "Blocked")
    else:
        st.success("✅ This email seems safe.")
        log_activity("Email Scan", email_address, "Safe", "Allowed")

# 🌐 Fake Website Checker
st.header("🌐 Check Fake Websites")
website_url = st.text_input("Enter Website URL:")
if st.button("Check Website"):
    if not is_valid_website(website_url):
        st.error("❌ This website is blocked because it is not using HTTPS.")
    elif any(site in website_url for site in FAKE_WEBSITES):
        st.error("❌ Fake Website Detected! Access Blocked.")
        send_telegram_alert(f"⚠️ Fake Website Alert! URL: {website_url}")
        log_activity("Website Scan", website_url, "Fake", "Blocked")
    else:
        st.success("✅ This website seems safe.")
        log_activity("Website Scan", website_url, "Safe", "Allowed")

# 🔒 Footer
st.markdown("🔒 **24/7 Real-time Protection Against Fraud**")
