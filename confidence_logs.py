import json
from datetime import datetime

CONFIDENCE_LOGS_FILE = "confidence_logs.json"

try:
    with open(CONFIDENCE_LOGS_FILE, "r") as f:
        pass
except FileNotFoundError:
    with open(CONFIDENCE_LOGS_FILE, "w") as f:
        json.dump([], f, indent=4)

def add_confidence_log(intent_tag, confidence_score):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "intent_tag": intent_tag,
        "confidence_score": confidence_score
    }
    with open(CONFIDENCE_LOGS_FILE, "r+") as f:
        logs = json.load(f)
        logs.append(log_entry)
        f.seek(0)
        json.dump(logs, f, indent=4)
