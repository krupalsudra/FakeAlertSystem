import json
import datetime

LOG_FILE_JSON = "logs/activity.json"
LOG_FILE_TXT = "logs/activity.log"

def log_activity(alert_type, value):
    """Logs detected fake alerts in JSON and text format."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {"timestamp": timestamp, "alert_type": alert_type, "value": value}

    # Save log in JSON file
    try:
        with open(LOG_FILE_JSON, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(log_entry)
    with open(LOG_FILE_JSON, "w") as file:
        json.dump(logs, file, indent=4)

    # Save log in text file
    with open(LOG_FILE_TXT, "a") as file:
        file.write(f"{timestamp} - {alert_type}: {value}\n")
