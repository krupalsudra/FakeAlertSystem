from fastapi import FastAPI, Query, HTTPException, Depends
import firebase_admin
from firebase_admin import messaging, credentials
import os

app = FastAPI()

# Set the correct path to the Firebase credentials file
firebase_json_path = r"C:\FakeAlertSystem\Backend\firebase-adminsdk.json"

if os.path.exists(firebase_json_path):
    # Initialize Firebase for Notifications
    cred = credentials.Certificate(firebase_json_path)
    firebase_admin.initialize_app(cred)
    firebase_initialized = True
else:
    import logging
    logging.warning(f"⚠️ Firebase credentials file not found: {firebase_json_path}")
    firebase_initialized = False  # Prevent Firebase errors later

# Dependency to validate inputs but allow optional fields
def validate_inputs(
    email: str = Query(None, description="User email (Example: test@example.com)"),
    phone: str = Query(None, description="User phone (Example: +1234567890)"),
    url: str = Query(None, description="Website URL (Example: https://example.com)")
):
    if not any([email, phone, url]):
        raise HTTPException(status_code=400, detail="At least one of email, phone, or URL is required")
    return {"email": email, "phone": phone, "url": url}

@app.get("/")
async def check_fake_alert(inputs: dict = Depends(validate_inputs)):
    email = inputs.get("email")
    phone = inputs.get("phone")
    url = inputs.get("url")

    # Fake detection logic
    if email and any(c.isupper() for c in email):
        return {"status": "error", "message": "Uppercase emails are not allowed!"}
    if url and not url.startswith("https://"):
        return {"status": "error", "message": "Only HTTPS websites are allowed!"}

    if firebase_initialized:
        message = messaging.Message(
            notification=messaging.Notification(
                title="⚠️ Fake Alert Detected!",
                body=f"Suspicious activity detected for {email or phone or url}",
            ),
            topic="fake_alerts",
        )
        try:
            response = messaging.send(message)
        except Exception as e:
            return {"status": "error", "message": f"FCM Error: {str(e)}"}

        return {"status": "success", "message": "Checked successfully!", "fcm_response": response}
    
    return {"status": "warning", "message": "Firebase not initialized, but API is running"}

