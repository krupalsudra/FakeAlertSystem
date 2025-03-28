import json
import datetime

LOG_FILE = "activity.json"

# Function to log activity
def log_activity(alert_type, user_input, result):
    log_data = {
        "timestamp": str(datetime.datetime.now()),
        "alert_type": alert_type,
        "input": user_input,
        "result": result
    }
    with open(LOG_FILE, "a") as log_file:
        json.dump(log_data, log_file)
        log_file.write("\n")

# Function to read logs
def get_logs():
    logs = []
    try:
        with open(LOG_FILE, "r") as log_file:
            logs = log_file.readlines()
        logs = [json.loads(log) for log in logs]  # Convert JSON strings to dicts
    except FileNotFoundError:
        logs = []
    return logs[-10:]  # Return only the last 10 logs

# Function to clear logs (Admin Only)
def clear_logs():
    open(LOG_FILE, "w").close()  # Overwrite file with empty content
