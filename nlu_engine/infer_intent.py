import joblib
import numpy as np

class IntentClassifier:
    def __init__(self, intents_path):
        self.model = joblib.load("models/intent_model.pkl")
        self.vectorizer = joblib.load("models/vectorizer.pkl")

        import json
        with open(intents_path) as f:
            self.intent_labels = list(json.load(f).keys())

    def predict(self, text, top_n=4):
        X = self.vectorizer.transform([text])
        probs = self.model.predict_proba(X)[0]

        results = list(zip(self.model.classes_, probs))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_n]
