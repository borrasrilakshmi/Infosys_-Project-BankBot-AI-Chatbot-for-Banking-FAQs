import json, os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_FILE = os.path.join(BASE_DIR, "data", "knowledge_base.json")

def load_kb():
    if not os.path.exists(KB_FILE):
        return []
    with open(KB_FILE, "r") as f:
        return json.load(f)

def save_kb(kb):
    with open(KB_FILE, "w") as f:
        json.dump(kb, f, indent=4)
