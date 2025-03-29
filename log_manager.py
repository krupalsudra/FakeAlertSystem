import datetime

LOG_FILE = "activity.log"

def log_activity(activity):
    """Logs all activities into a file."""
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {activity}\n")

def get_logs():
    """Reads and returns the log file content for admin view."""
    try:
        with open(LOG_FILE, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return []
