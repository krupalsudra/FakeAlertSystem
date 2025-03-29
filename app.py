import streamlit as st
import requests
import log_manager
import re

# Telegram Bot Settings
TELEGRAM_BOT_TOKEN = "7778478472:AAG3vqv-CSmiarFBgDDQjdJtgGQlqrZ8oFo"
TELEGRAM_CHAT_ID = "6728315195"

# Malicious URLs & Temp Emails for validation
MALICIOUS_URLS = ["phishing.com", "malware-site.net", "scam-website.org"]
TEMP_EMAIL_DOMAINS = ["tempmail.com", "mailinator.com", "10minutemail.com"]

# Function to send alerts to Telegram
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

# Page Config
st.set_page_config(page_title="Fake Alert System", page_icon="🚨", layout="centered")

# Header
st.markdown(
    "<h1 style='text-align: center; color: red;'>🚨 Fake Alert System 🚨</h1>", 
    unsafe_allow_html=True
)
st.write("A professional tool to analyze emails, websites, and phone numbers for security threats.")

# Section Selection
st.markdown("---")
st.markdown("### 🔍 **Select a Security Check**")
choice = st.selectbox("", ["Email Breach Check", "Website Safety Check", "Phone Number Validation", "View Live Logs"])

# Email Breach Check
if choice == "Email Breach Check":
    st.markdown("### 📧 **Email Breach Check**")
    email = st.text_input("Enter Email (must be lowercase):", placeholder="example@domain.com").strip()

    if st.button("🔍 Check Email"):
        if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", email):
            st.error("❌ Invalid email format! Use only lowercase letters and correct format.")
        else:
            domain = email.split("@")[-1]
            if domain in TEMP_EMAIL_DOMAINS:
                log_manager.log_activity(f"Unsafe email checked: {email}")
                send_telegram_alert(f"🚨 ALERT: {email} is a temporary email! Marked as unsafe.")
                st.error(f"⚠️ {email} is UNSAFE (Temporary Email Detected).")
            else:
                log_manager.log_activity(f"Safe email checked: {email}")
                st.success(f"✅ {email} is SAFE.")

# Website Safety Check
elif choice == "Website Safety Check":
    st.markdown("### 🌍 **Website Safety Check**")
    url = st.text_input("Enter Website URL:", placeholder="https://example.com").strip()

    if st.button("🔍 Check Website Safety"):
        domain = url.replace("http://", "").replace("https://", "").split("/")[0]

        if url.startswith("http://"):
            log_manager.log_activity(f"Blocked unsafe HTTP site: {url}")
            send_telegram_alert(f"🚨 ALERT: Blocked HTTP site: {url}")
            st.error("❌ Blocked! HTTP websites are not secure.")
        elif domain in MALICIOUS_URLS:
            log_manager.log_activity(f"Unsafe website checked: {url}")
            send_telegram_alert(f"🚨 ALERT: {url} is a known malicious website! Marked as unsafe.")
            st.error(f"❌ {url} is UNSAFE (Malicious Website Detected).")
        else:
            log_manager.log_activity(f"Safe website checked: {url}")
            st.success(f"✅ {url} is SAFE.")

# Phone Number Validation
elif choice == "Phone Number Validation":
    st.markdown("### 📱 **Phone Number Validation**")
    phone = st.text_input("Enter 10-digit Phone Number:", placeholder="9876543210").strip()

    if st.button("🔍 Validate Phone Number"):
        if re.fullmatch(r"\d{10}", phone):
            log_manager.log_activity(f"Valid phone number checked: {phone}")
            st.success(f"✅ {phone} is a VALID phone number.")
        else:
            log_manager.log_activity(f"Invalid phone number checked: {phone}")
            send_telegram_alert(f"🚨 ALERT: Invalid phone number entered: {phone}")
            st.error("❌ Invalid Phone Number! Must be exactly 10 digits.")

# Live Logs
elif choice == "View Live Logs":
    st.markdown("### 📜 **Live Log Activity (Admin Only)**")
    logs = log_manager.get_logs()
    if logs:
        for log in logs:
            st.code(log)
    else:
        st.info("No logs available.")
