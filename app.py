import streamlit as st
import re

# Title
st.title("🚨 Fake Alert Detection & Blocking System")
st.markdown("### Detect and block fake calls, websites, and emails instantly 24/7")

# User Input
alert_type = st.selectbox("Select alert type:", ["Fake Call", "Fake Website", "Fake Email"])
user_input = st.text_area("Enter details (Phone Number / URL / Email Address):", "").strip()

# Fake Data Lists (Can be connected to a real-time database)
fake_calls = ["+1234567890", "+1987654321", "+1122334455"]
fake_websites = ["scam-site.com", "free-money.xyz", "clickhere.win"]
fake_emails = ["fake@scam.com", "lottery@fraud.net", "winmoney@spam.org"]

# Validation Functions
def is_valid_email(email):
    """Check if email is in valid format and lowercase."""
    email_regex = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
    return re.match(email_regex, email)

def is_valid_phone(phone):
    """Check if phone number contains exactly 10 digits."""
    return phone.isdigit() and len(phone) == 10

def is_valid_website(url):
    """Check if the website starts with HTTPS (block HTTP)."""
    return url.startswith("https://")

# Detection Function
def detect_fake_alert(alert_type, text):
    if not text:
        return "⚠️ Please enter details to check!"
    
    text = text.strip().lower()  # Convert to lowercase for comparison

    if alert_type == "Fake Call":
        if not is_valid_phone(text):
            return "⚠️ Invalid phone number! It must be exactly 10 digits."
        if text in fake_calls:
            return "❌ Fake Call Detected! Blocked instantly."
        return "✅ This call seems safe."

    elif alert_type == "Fake Website":
        if not is_valid_website(text):
            return "❌ This website is blocked because it is not using HTTPS."
        if any(site in text for site in fake_websites):
            return "❌ Fake Website Detected! Access Blocked."
        return "✅ This website seems safe."

    elif alert_type == "Fake Email":
        if not is_valid_email(text):
            return "⚠️ Invalid email format! Please enter a valid email in lowercase."
        if text in fake_emails:
            return "❌ Fake Email Detected! Blocked instantly."
        return "✅ This email seems safe."

    return "⚠️ Unknown alert type."

# Check Alert
if st.button("Check Alert"):
    result = detect_fake_alert(alert_type, user_input)
    st.subheader(result)

# Footer
st.markdown("🔒 **24/7 Real-time Protection Against Fraud**")
