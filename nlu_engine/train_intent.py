import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

INTENTS_PATH = "nlu_engine/intents.json"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "intent_model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")

# Load intents
with open(INTENTS_PATH) as f:
    intents = json.load(f)

# Prepare training data
X = []
y = []

for intent, examples in intents.items():
    for ex in examples:
        X.append(ex)
        y.append(intent)

# Vectorize
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_vec, y)

# Save model
os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)

print("Model trained successfully!")
