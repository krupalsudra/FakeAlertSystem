import streamlit as st
import requests
import log_manager

# Telegram Bot Configuration (Replace with your actual credentials)
TELEGRAM_BOT_TOKEN = "7778478472:AAG3vqv-CSmiarFBgDDQjdJtgGQlqrZ8oFo"
TELEGRAM_CHAT_ID = "6728315195"

# Function to Send Telegram Alert
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    return response.json()

# Title & Description
st.set_page_config(page_title="Fake Alert System", page_icon="⚠️")
st.title("🚨 Fake Alert System")
st.markdown("#### Protect Yourself from Fake Calls, Emails, and Websites")

# Sidebar Image & Info
st.sidebar.image("fake_alert_logo.png", use_column_width=True)
st.sidebar.markdown("### Stay Safe from Scams!")
st.sidebar.info("This system detects fake calls, emails, and websites in real time.")

# Fake Data Check Input
option = st.selectbox("Select Type to Check:", ["Fake Call", "Fake Email", "Fake Website"])
user_input = st.text_input("Enter Number / Email / Website:")

if st.button("Check Now"):
    if not user_input:
        st.warning("⚠️ Please enter a value to check!")
    else:
        # Fake Data Lists
        fake_calls = ["+1234567890", "+1987654321", "+1122334455"]
        fake_emails = ["fake@scam.com", "lottery@fraud.net", "winmoney@spam.org"]
        fake_websites = ["scam-site.com", "free-money.xyz", "clickhere.win"]

        # Detection Logic
        if option == "Fake Call" and user_input in fake_calls:
            st.error("❌ This is a Fake Call Number!")
            log_manager.log_activity("Fake Call Detected", user_input)
            send_telegram_alert(f"🚨 Fake Call Alert! Number: {user_input}")

        elif option == "Fake Email" and user_input in fake_emails:
            st.error("❌ This is a Fake Email Address!")
            log_manager.log_activity("Fake Email Detected", user_input)
            send_telegram_alert(f"🚨 Fake Email Alert! Email: {user_input}")

        elif option == "Fake Website" and user_input in fake_websites:
            st.error("❌ This is a Fake Website!")
            log_manager.log_activity("Fake Website Detected", user_input)
            send_telegram_alert(f"🚨 Fake Website Alert! URL: {user_input}")

        else:
            st.success("✅ This seems safe!")

# Footer
st.markdown("---")
st.markdown("📌 **Developed by Krupal Sudra** | 🎓 MSc IT | Roll No: 13")
