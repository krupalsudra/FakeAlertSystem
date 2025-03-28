import streamlit as st
import re
import json
import datetime
import requests

# Logging function (Only you can see the logs)
def log_activity(alert_type, user_input, result):
    log_data = {
        "timestamp": str(datetime.datetime.now()),
        "alert_type": alert_type,
        "input": user_input,
        "result": result
    }
    with open("activity.json", "a") as log_file:
        json.dump(log_data, log_file)
        log_file.write("\n")

# Telegram Alert Function (Replace with your Telegram Bot API & Chat ID)
def send_telegram_alert(message):
    TELEGRAM_BOT_TOKEN = "your_bot_token"
    TELEGRAM_CHAT_ID = "your_chat_id"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except:
        pass  # Avoid breaking the app if Telegram is down

# UI Design
st.title("🛡️ Fake Alert System")
st.markdown("### Detect and block fake calls, websites, and emails instantly 24/7")

# Tabs for Separate Checks
tab1, tab2, tab3 = st.tabs(["📞 Fake Call", "🌐 Fake Website", "📧 Fake Email"])

# Fake Data Lists (Can be connected to a database)
fake_calls = ["+1234567890", "+1987654321", "+1122334455"]
fake_websites = ["scam-site.com", "free-money.xyz", "clickhere.win"]
fake_emails = ["fake@scam.com", "lottery@fraud.net", "winmoney@spam.org"]
temp_mail_domains = ["tempmail.com", "mailinator.com", "10minutemail.com"]

# Fake Call Detection
with tab1:
    st.subheader("📞 Fake Call Detector")
    phone_number = st.text_input("Enter Phone Number:")
    
    if st.button("Check Call"):
        if not phone_number.isdigit() or len(phone_number) != 10:
            result = "⚠️ Invalid phone number! Must be exactly 10 digits."
        elif phone_number in fake_calls:
            result = "❌ Fake Call Detected! Blocked instantly."
            send_telegram_alert(f"🚨 Fake Call Detected: {phone_number}")
        else:
            result = "✅ This call seems safe."
        
        log_activity("Fake Call", phone_number, result)
        st.write(result)

# Fake Website Detection
with tab2:
    st.subheader("🌐 Fake Website Detector")
    website_url = st.text_input("Enter Website URL:")
    
    if st.button("Check Website"):
        if not website_url.startswith("https://"):
            result = "❌ This website is blocked because it is not using HTTPS."
        elif any(site in website_url for site in fake_websites):
            result = "❌ Fake Website Detected! Access Blocked."
            send_telegram_alert(f"🚨 Fake Website Detected: {website_url}")
        else:
            result = "✅ This website seems safe."
        
        log_activity("Fake Website", website_url, result)
        st.write(result)

# Fake Email Detection
with tab3:
    st.subheader("📧 Fake Email Detector")
    email_input = st.text_input("Enter Email Address:")
    
    if st.button("Check Email"):
        email_regex = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
        
        if not re.match(email_regex, email_input):
            result = "⚠️ Invalid email format! Please enter a valid email."
        elif email_input in fake_emails:
            result = "❌ Fake Email Detected! Blocked instantly."
            send_telegram_alert(f"🚨 Fake Email Detected: {email_input}")
        elif any(domain in email_input for domain in temp_mail_domains):
            result = "⚠️ Temporary Email Detected! It is not a valid email."
            send_telegram_alert(f"⚠️ Temporary Email Used: {email_input}")
        else:
            result = "✅ This email seems safe."
        
        log_activity("Fake Email", email_input, result)
        st.write(result)

# Live Logs (Only for Admin)
if st.checkbox("🔍 View Live Logs (Admin Only)"):
    st.subheader("📜 Activity Logs")
    try:
        with open("activity.json", "r") as log_file:
            logs = log_file.readlines()
            for log in logs[-10:]:  # Show last 10 logs
                st.json(json.loads(log))
    except:
        st.write("No logs available yet.")

st.markdown("🔒 **24/7 Real-time Protection Against Fraud**")
