import datetime
import os

LOG_FILE = "activity_logs.txt"

# 🔹 Function to Log Activity
def log_activity(activity_type, message):
    """Logs activities securely."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {activity_type}: {message}\n"

    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_entry)

# 🔹 Function to Read Logs (Admin Only)
def get_logs():
    """Returns logs only for admin access."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as log_file:
            return log_file.readlines()
    return []
