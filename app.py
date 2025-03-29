import streamlit as st
import requests
import log_manager
import os
from PIL import Image

# Telegram Bot Settings
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"

# Function to send alerts to Telegram
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

# Load and display sample image
image_path = "sample_img.jpeg"
if os.path.exists(image_path):
    image = Image.open(image_path)
    st.sidebar.image(image, use_column_width=True)
else:
    st.sidebar.write("Image not found.")

# App Title
st.title("🕵️ Digital Footprint Analyzer")
st.write("Monitor user activity, detect unsafe emails & links, and log everything!")

# User Choice
option = st.radio("🔍 What do you want to check?", ["Email Breach", "Website Safety", "Live Logs"])

if option == "Email Breach":
    email = st.text_input("📧 Enter email:")
    
    if st.button("🔍 Check Email Breach"):
        log_manager.log_activity(f"Email check: {email}")
        send_telegram_alert(f"🚨 ALERT: Email {email} was checked. Marked as unsafe!")
        st.error(f"⚠️ {email} is NOT SAFE (Potential breach detected).")

elif option == "Website Safety":
    url = st.text_input("🌍 Enter URL:")
    
    if st.button("🔍 Check Website Safety"):
        log_manager.log_activity(f"Website check: {url}")
        
        if url.startswith("http://"):
            send_telegram_alert(f"🚨 ALERT: {url} is UNSAFE (HTTP detected)!")
            st.error(f"❌ {url} is UNSAFE (HTTP detected).")
        else:
            send_telegram_alert(f"🚨 ALERT: {url} was checked. Marked as unsafe!")
            st.error(f"⚠️ {url} is NOT SAFE (Potential threat detected).")

elif option == "Live Logs":
    st.write("📜 **Live Log Activity (Only Visible to Admin)**")
    logs = log_manager.get_logs()
    for log in logs:
        st.write(log)
