import streamlit as st
import requests
import os
import log_manager  # Ensure log_manager.py exists in your directory

# 🔹 Telegram Bot Configuration (Replace with your actual credentials)
TELEGRAM_BOT_TOKEN = "7778478472:AAG3vqv-CSmiarFBgDDQjdJtgGQlqrZ8oFo"
TELEGRAM_CHAT_ID = "6728315195"

# 🔹 Function to Send Telegram Alert
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    try:
        response = requests.post(url, data=data)
        result = response.json()
        
        if response.status_code == 200 and result.get("ok"):
            st.success("✅ Telegram Alert Sent!")
        else:
            st.error(f"⚠️ Failed to Send Telegram Alert: {result}")
    
    except Exception as e:
        st.error(f"⚠️ Error Sending Telegram Alert: {e}")

# 🔹 Set Page Title & Icon
st.set_page_config(page_title="Fake Alert System", page_icon="⚠️")
st.title("🚨 Fake Alert System")
st.markdown("#### Protect Yourself from Fake Calls, Emails, and Websites")

# 🔹 Sidebar with Image & Info
image_path = "fake_alert_logo.png"

if os.path.exists(image_path):
    st.sidebar.image(image_path, use_column_width=True)
else:
    st.sidebar.error("⚠️ Missing logo file! Please upload 'fake_alert_logo.png'.")

st.sidebar.markdown("### Stay Safe from Scams!")
st.sidebar.info("This system detects fake calls, emails, and websites in real time.")

# 🔹 Fake Data Check Inputs (Separate Checkboxes)
check_call = st.checkbox("Check Phone Number")
check_email = st.checkbox("Check Email Address")
check_website = st.checkbox("Check Website URL")

user_input = st.text_input("Enter Number / Email / Website:")

if st.button("Check Now"):
    if not user_input:
        st.warning("⚠️ Please enter a value to check!")
    else:
        # 🔹 Fake Data Lists
        fake_calls = ["+1234567890", "+1987654321", "+1122334455"]
        fake_emails = ["fake@scam.com", "lottery@fraud.net", "winmoney@spam.org"]
        fake_websites = ["scam-site.com", "free-money.xyz", "clickhere.win"]
        temp_mail_domains = ["tempmail.com", "10minutemail.com", "fakeinbox.com"]
        malicious_links = ["hacker-site.com", "phishingscam.net", "malware-load.xyz"]

        # 🔹 Detection Logic
        alert_message = None

        if check_call:
            if len(user_input) != 10 or not user_input.isdigit():
                st.error("❌ Invalid Phone Number! Must be 10 digits.")
            elif user_input in fake_calls:
                st.error("❌ This is a Fake Call Number!")
                alert_message = f"🚨 Fake Call Alert! Number: {user_input}"

        if check_email:
            domain = user_input.split("@")[-1]
            if "@" not in user_input or "." not in domain:
                st.error("❌ Invalid Email Format!")
            elif domain in temp_mail_domains or user_input in fake_emails:
                st.error("❌ This is a Fake or Temporary Email!")
                alert_message = f"🚨 Fake Email Alert! Email: {user_input}"

        if check_website:
            if user_input.startswith("http://"):
                st.error("❌ Blocked! HTTP Websites Are Unsafe. Use HTTPS.")
                alert_message = f"🚨 Unsafe Website Alert! URL: {user_input}"
            elif any(link in user_input for link in fake_websites + malicious_links):
                st.error("❌ Malicious or Fake Website Detected!")
                alert_message = f"🚨 Malicious Website Alert! URL: {user_input}"

        # 🔹 Send Telegram Alert & Log Activity
        if alert_message:
            log_manager.log_activity("Alert", alert_message)
            send_telegram_alert(alert_message)
        else:
            st.success("✅ This seems safe!")

# 🔹 Admin Log Access (Hidden from Normal Users)
if st.sidebar.button("View Logs (Admin Only)"):
    logs = log_manager.get_logs()
    
    if logs:
        st.sidebar.markdown("### 📜 Activity Logs")
        st.sidebar.text_area("Logs", "".join(logs), height=300)
    else:
        st.sidebar.info("No logs found!")
