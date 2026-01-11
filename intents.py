import json, os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_FILE = os.path.join(BASE_DIR, "data", "intents.json")

def load_intents():
    if not os.path.exists(INTENTS_FILE):
        return []
    with open(INTENTS_FILE, "r") as f:
        return json.load(f)

def save_intents(intents):
    with open(INTENTS_FILE, "w") as f:
        json.dump(intents, f, indent=4)
