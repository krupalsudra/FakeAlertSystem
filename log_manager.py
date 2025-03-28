import os
import json
import logging
from datetime import datetime

# ✅ Log directory and file paths
LOG_DIR = "logs"
LOG_FILE_JSON = os.path.join(LOG_DIR, "activity.json")
LOG_FILE_TEXT = os.path.join(LOG_DIR, "activity.log")

# ✅ Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# ✅ Configure Logging
logging.basicConfig(
    filename=LOG_FILE_TEXT, 
    level=logging.INFO, 
    format="%(asctime)s - %(message)s"
)

# 📌 **Function to Add a Log Entry**
def add_log(event_type, entity, status, action, details=""):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,   # Email Scan, Phone Scan, Website Scan
        "entity": entity,           # Email, Phone Number, or URL
        "status": status,           # Fake or Safe
        "action": action,           # Blocked, Alerted, or Allowed
        "details": details          # Additional info if needed
    }

    # ✅ Append log to JSON file
    with open(LOG_FILE_JSON, "a") as log_file:
        json.dump(log_entry, log_file)
        log_file.write("\n")

    # ✅ Log to text file
    logging.info(json.dumps(log_entry))

# 📌 **Function to Retrieve Logs**
def get_logs():
    logs = []
    if os.path.exists(LOG_FILE_JSON):
        with open(LOG_FILE_JSON, "r") as log_file:
            logs = [json.loads(line.strip()) for line in log_file if line.strip()]
    return logs

# 📌 **Function to Clear Logs**
def clear_logs():
    """Clears all logs from the system."""
    open(LOG_FILE_JSON, "w").close()
    open(LOG_FILE_TEXT, "w").close()
    logging.info("✅ Logs cleared successfully!")

# 📌 **Function to Print Logs (For Debugging)**
def print_logs():
    logs = get_logs()
    if not logs:
        print("🔹 No logs found.")
    else:
        print("📜 Logged Entries:")
        for log in logs:
            print(json.dumps(log, indent=4))

# ✅ **Test the Log Manager (Standalone Execution)**
if __name__ == "__main__":
    # 📌 Sample Log Entries (Test Cases)
    add_log("Email Scan", "fake@scam.com", "Fake", "Blocked", "Detected as phishing email")
    add_log("Phone Scan", "1234567890", "Fake", "Blocked", "Detected as scam call")
    add_log("Website Scan", "https://scam-site.com", "Fake", "Blocked", "Detected as fake website")

    # 📌 Print Logs
    print_logs()
    
    # 📌 Clear Logs (Uncomment to Test)
    # clear_logs()
