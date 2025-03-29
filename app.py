import streamlit as st
import requests
import os

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
            st.success("✅ Alert Sent to Telegram!")
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

# Upload the image file if missing
if not os.path.exists(image_path):
    with open(image_path, "wb") as f:
        f.write(requests.get("https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg").content)  # Generic placeholder

st.sidebar.image(image_path, use_column_width=True)

st.sidebar.markdown("### Stay Safe from Scams!")
st.sidebar.info("This system detects fake calls, emails, and websites in real time.")

# 🔹 Checkboxes for Different Types
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
        fake_websites = ["scam-site.com", "free-money.xyz", "clickhere.win"]
        temp_mail_domains = ["tempmail.com", "10minutemail.com", "fakeinbox.com"]
        malicious_links = ["hacker-site.com", "phishingscam.net", "malware-load.xyz"]

        # 🔹 Detection Logic
        alert_message = None

        if check_call:
            if len(user_input) != 10 or not user_input.isdigit():
                st.error("❌ Invalid Phone Number! Must be 10 digits.")
                alert_message = f"🚨 Invalid Phone Number Attempt: {user_input}"
            elif user_input in fake_calls:
                st.error("❌ This is a Fake Call Number!")
                alert_message = f"🚨 Fake Call Alert! Number: {user_input}"

        if check_email:
            domain = user_input.split("@")[-1]
            if "@" not in user_input or "." not in domain:
                st.error("❌ Invalid Email Format!")
                alert_message = f"🚨 Invalid Email Format: {user_input}"
            elif domain in temp_mail_domains:
                st.error("❌ This is a Temporary Email!")
                alert_message = f"🚨 Temporary Email Alert! Email: {user_input}"
            else:
                st.warning("⚠️ Email Not Verified as Safe!")
                alert_message = f"⚠️ Email Alert! Email: {user_input}"

        if check_website:
            if user_input.startswith("http://"):
                st.error("❌ Blocked! HTTP Websites Are Unsafe. Use HTTPS.")
                alert_message = f"🚨 Unsafe Website Alert! URL: {user_input}"
            elif any(link in user_input for link in fake_websites + malicious_links):
                st.error("❌ Malicious or Fake Website Detected!")
                alert_message = f"🚨 Malicious Website Alert! URL: {user_input}"
            else:
                st.warning("⚠️ Website Not Verified as Safe!")
                alert_message = f"⚠️ Website Alert! URL: {user_input}"

        # 🔹 Send Telegram Alert (No Logs for Users)
        if alert_message:
            send_telegram_alert(alert_message)
        else:
            st.success("✅ This seems safe!")
