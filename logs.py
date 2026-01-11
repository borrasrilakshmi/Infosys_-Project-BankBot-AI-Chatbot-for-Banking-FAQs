import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_FILE = os.path.join(BASE_DIR, "data", "logs.json")

def add_user_log(event, response):
    logs = []
    if os.path.exists(LOGS_FILE):
        with open(LOGS_FILE, "r") as f:
            logs = json.load(f)
    logs.append({"event": event, "response": response})
    with open(LOGS_FILE, "w") as f:
        json.dump(logs, f, indent=4)
