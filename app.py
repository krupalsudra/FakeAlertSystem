import streamlit as st
import requests
import log_manager
import re

# Telegram Bot Settings
TELEGRAM_BOT_TOKEN = "7778478472:AAG3vqv-CSmiarFBgDDQjdJtgGQlqrZ8oFo"
TELEGRAM_CHAT_ID = "6728315195"

# Malicious URLs & Temporary Email Domains
MALICIOUS_URLS = ["phishing.com", "malware-site.net", "scam-website.org"]
TEMP_EMAIL_DOMAINS = ["tempmail.com", "mailinator.com", "10minutemail.com", "yopmail.com", "guerrillamail.com"]

# Function to send alerts to Telegram
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    return response.status_code

# Page Configuration
st.set_page_config(page_title="Cyber Threat Analyzer", page_icon="🚨", layout="wide")

# Header
st.markdown("<h1 style='text-align: center; color: red;'>🚨 Cyber Threat Analyzer 🚨</h1>", unsafe_allow_html=True)
st.write("A professional security tool to analyze emails, websites, and phone numbers for threats.")

# Create Three Columns
col1, col2, col3 = st.columns(3)

# **EMAIL CHECK**  
with col1:
    st.markdown("### 📧 **Email Verification**")
    email = st.text_input("Enter Email:", placeholder="example@domain.com").strip()

    if st.button("🔍 Check Email"):
        if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.com$", email):
            log_manager.log_activity(f"Blocked Invalid Email: {email}")
            send_telegram_alert(f"🚨 ALERT: {email} is INVALID! Only `.com` emails are allowed.")
            st.error("❌ Invalid email! Must be lowercase and end with `.com`")
        else:
            domain = email.split("@")[-1]
            if domain in TEMP_EMAIL_DOMAINS:
                log_manager.log_activity(f"Blocked Temp Email: {email}")
                send_telegram_alert(f"🚨 ALERT: {email} is a temporary email! Marked as unsafe.")
                st.error(f"⚠️ {email} is UNSAFE (Temporary Email Detected).")
            else:
                log_manager.log_activity(f"Safe Email Checked: {email}")
                st.success(f"✅ {email} is SAFE.")

# **WEBSITE CHECK**  
with col2:
    st.markdown("### 🌍 **Website Safety Check**")
    url = st.text_input("Enter Website URL:", placeholder="https://example.com").strip()

    if st.button("🔍 Check Website Safety"):
        domain = url.replace("http://", "").replace("https://", "").split("/")[0]

        if url.startswith("http://"):
            log_manager.log_activity(f"Blocked HTTP site: {url}")
            send_telegram_alert(f"🚨 ALERT: Blocked HTTP site: {url}")
            st.error("❌ Blocked! HTTP websites are not secure.")
        elif domain in MALICIOUS_URLS:
            log_manager.log_activity(f"Blocked Malicious Site: {url}")
            send_telegram_alert(f"🚨 ALERT: {url} is a known malicious website! Marked as unsafe.")
            st.error(f"❌ {url} is UNSAFE (Malicious Website Detected).")
        else:
            log_manager.log_activity(f"Safe Website Checked: {url}")
            st.success(f"✅ {url} is SAFE.")

# **PHONE NUMBER CHECK**  
with col3:
    st.markdown("### 📱 **Phone Number Validation**")
    phone = st.text_input("Enter 10-digit Phone Number:", placeholder="9876543210").strip()

    if st.button("🔍 Validate Phone Number"):
        if re.fullmatch(r"\d{10}", phone):
            log_manager.log_activity(f"Valid Phone Checked: {phone}")
            st.success(f"✅ {phone} is a VALID phone number.")
        else:
            log_manager.log_activity(f"Blocked Invalid Phone: {phone}")
            send_telegram_alert(f"🚨 ALERT: Invalid phone number entered: {phone}")
            st.error("❌ Invalid Phone Number! Must be exactly 10 digits.")

# **Live Log Activity**
st.markdown("---")
st.markdown("### 📜 **Live Log Activity (Admin Only)**")
logs = log_manager.get_logs()
if logs:
    for log in logs:
        st.code(log)
else:
    st.info("No logs available.")
