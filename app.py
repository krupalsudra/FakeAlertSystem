import streamlit as st
import requests
import log_manager
import re

# Telegram Bot Settings
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"

# Malicious URLs & Temp Emails for validation
MALICIOUS_URLS = ["phishing.com", "malware-site.net", "scam-website.org"]
TEMP_EMAIL_DOMAINS = ["tempmail.com", "mailinator.com", "10minutemail.com"]

# Function to send alerts to Telegram
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

# App Title
st.title("🚨 Fake Alert System")
st.write("A professional tool to check for email breaches, website safety, and log activities.")

# Sidebar Menu
st.sidebar.title("🔍 Navigation")
option = st.sidebar.radio("Select an Option", ["Email Breach", "Website Safety", "Phone Number Check", "Live Logs"])

# Email Breach Check
if option == "Email Breach":
    email = st.text_input("📧 Enter Email:")
    
    if st.button("🔍 Check Email"):
        domain = email.split("@")[-1]
        if domain in TEMP_EMAIL_DOMAINS:
            log_manager.log_activity(f"Unsafe email checked: {email}")
            send_telegram_alert(f"🚨 ALERT: {email} is a temporary email! Marked as unsafe.")
            st.error(f"⚠️ {email} is UNSAFE (Temporary Email Detected).")
        else:
            log_manager.log_activity(f"Safe email checked: {email}")
            st.success(f"✅ {email} is SAFE.")

# Website Safety Check
elif option == "Website Safety":
    url = st.text_input("🌍 Enter Website URL:")

    if st.button("🔍 Check Website Safety"):
        domain = url.replace("http://", "").replace("https://", "").split("/")[0]
        
        if domain in MALICIOUS_URLS:
            log_manager.log_activity(f"Unsafe website checked: {url}")
            send_telegram_alert(f"🚨 ALERT: {url} is a known malicious website! Marked as unsafe.")
            st.error(f"❌ {url} is UNSAFE (Malicious Website Detected).")
        else:
            log_manager.log_activity(f"Safe website checked: {url}")
            st.success(f"✅ {url} is SAFE.")

# Phone Number Validation
elif option == "Phone Number Check":
    phone = st.text_input("📱 Enter 10-digit Phone Number:")
    
    if st.button("🔍 Validate Phone Number"):
        if re.fullmatch(r"\d{10}", phone):
            log_manager.log_activity(f"Valid phone number checked: {phone}")
            st.success(f"✅ {phone} is a VALID phone number.")
        else:
            log_manager.log_activity(f"Invalid phone number checked: {phone}")
            send_telegram_alert(f"🚨 ALERT: Invalid phone number entered: {phone}")
            st.error("❌ Invalid Phone Number! Must be exactly 10 digits.")

# Live Logs
elif option == "Live Logs":
    st.write("📜 **Live Log Activity (Only Visible to Admin)**")
    logs = log_manager.get_logs()
    for log in logs:
        st.write(log)
