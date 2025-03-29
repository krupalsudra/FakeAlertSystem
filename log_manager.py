import datetime

LOG_FILE = "security_logs.txt"

def log_activity(activity):
    """Logs security-related activity to a file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {activity}\n"
    with open(LOG_FILE, "a") as file:
        file.write(log_entry)

def get_logs():
    """Retrieves all logged activities."""
    try:
        with open(LOG_FILE, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []
