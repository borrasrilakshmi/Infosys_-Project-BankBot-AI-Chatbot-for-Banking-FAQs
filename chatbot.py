import json
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ADMIN import confidence_logs

with open("intents.json") as f:
    intents = json.load(f)

patterns = []
tags = []

for i in intents:
    for p in i["patterns"]:
        patterns.append(p)
        tags.append(i["tag"])

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)

st.title("🤖 BankBot Chatbot")

user_input = st.text_input("Ask something")

if user_input:
    user_vec = vectorizer.transform([user_input])
    sims = cosine_similarity(user_vec, X)[0]

    best_index = sims.argmax()
    confidence = sims[best_index]
    intent = tags[best_index]

    confidence_logs.log_confidence(user_input, intent, confidence)

    st.success(f"Intent: {intent}")
    st.progress(min(confidence, 1.0))
    st.write(f"Confidence: {confidence*100:.2f}%")
