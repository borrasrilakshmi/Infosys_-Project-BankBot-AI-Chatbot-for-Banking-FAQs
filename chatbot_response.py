import pickle
import random

# ---------- LOAD MODEL ----------
with open("model/chatbot_model.pkl", "rb") as f:
    model, vectorizer = pickle.load(f)

# ---------- LOAD INTENTS ----------
import json
with open("ADMIN/DATA/intents.json", "r", encoding="utf-8") as f:
    intents_data = json.load(f).get("intents", [])

def get_response(user_input):
    X = vectorizer.transform([user_input])
    probabilities = model.predict_proba(X)[0]
    predicted_index = probabilities.argmax()

    predicted_intent = model.classes_[predicted_index]
    confidence = probabilities[predicted_index] * 100

    # Choose response
    for intent in intents_data:
        if intent["tag"] == predicted_intent:
            response = random.choice(intent["responses"])
            return predicted_intent, round(confidence, 2), response

    return "unknown", 0.0, "Sorry, I didn't understand that."
