# =========================================================
# BANKBOT AI – FINAL UNIFIED PROJECT (ALL 4 MILESTONES)
# Author: BORRA SRI LAKSHMI
# =========================================================

import streamlit as st
import os, json, sqlite3
from datetime import datetime
from collections import defaultdict

# ML
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

# Analytics
import pandas as pd
import altair as alt

# LLM
from groq import Groq

# =========================================================
# PAGE CONFIG (ONLY ONCE)
# =========================================================
st.set_page_config("🏦 BankBot AI", layout="wide")

# =========================================================
# PATHS & FILES
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_FILE = os.path.join(BASE_DIR, "bankbot.db")

os.makedirs(DATA_DIR, exist_ok=True)

INTENTS_FILE = os.path.join(DATA_DIR, "intents.json")
ANALYTICS_FILE = os.path.join(DATA_DIR, "analytics.json")
KB_FILE = os.path.join(DATA_DIR, "knowledge_base.json")

# =========================================================
# DEFAULT DATA
# =========================================================
DEFAULT_INTENTS = [
    {"tag":"check_balance","patterns":["check balance","my balance"],"responses":["Your balance is displayed securely."]},
    {"tag":"transfer_money","patterns":["transfer money","send money"],"responses":["Money transfer option is available."]},
    {"tag":"card_block","patterns":["block card","lost card"],"responses":["Your card can be blocked instantly."]},
    {"tag":"find_atm","patterns":["nearest atm","find atm"],"responses":["Here are nearby ATM locations."]}
]

# =========================================================
# JSON HELPERS
# =========================================================
def load_json(path, default):
    if not os.path.exists(path):
        save_json(path, default)
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

load_json(INTENTS_FILE, DEFAULT_INTENTS)
load_json(ANALYTICS_FILE, [])
load_json(KB_FILE, [])

# =========================================================
# DATABASE (MILESTONE 3)
# =========================================================
def get_db():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            account_type TEXT,
            balance INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

def create_account(acc, user, pwd, acc_type, bal):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts WHERE account_number=? OR username=?", (acc, user))
    if cur.fetchone():
        conn.close()
        return False
    cur.execute("INSERT INTO accounts VALUES (?,?,?,?,?)",(acc,user,pwd,acc_type,bal))
    conn.commit()
    conn.close()
    return True

def login_user(user, pwd):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts WHERE username=? AND password=?", (user,pwd))
    row = cur.fetchone()
    conn.close()
    return row

def get_balance(acc):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE account_number=?", (acc,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def transfer_money(sender, receiver, amt):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE account_number=?", (sender,))
    s = cur.fetchone()
    cur.execute("SELECT balance FROM accounts WHERE account_number=?", (receiver,))
    r = cur.fetchone()
    if not s or not r:
        conn.close()
        return "❌ Invalid account"
    if s[0] < amt:
        conn.close()
        return "❌ Insufficient balance"
    cur.execute("UPDATE accounts SET balance=balance-? WHERE account_number=?", (amt,sender))
    cur.execute("UPDATE accounts SET balance=balance+? WHERE account_number=?", (amt,receiver))
    conn.commit()
    conn.close()
    return "✅ Transfer successful"

# =========================================================
# MILESTONE 1 & 2 – NLU + ML
# =========================================================
def train_model(intents):
    corpus, labels = [], []
    for i in intents:
        for p in i["patterns"]:
            corpus.append(p.lower())
            labels.append(i["tag"])
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    model = LogisticRegression()
    model.fit(X, labels)
    return model, vectorizer, corpus, labels

def predict_intent(query, model, vectorizer, corpus, labels):
    X = vectorizer.transform(corpus + [query.lower()])
    scores = cosine_similarity(X[-1], X[:-1])[0]
    intent_scores = {}
    for s,l in zip(scores, labels):
        intent_scores[l] = max(intent_scores.get(l,0), s)
    intent = max(intent_scores, key=intent_scores.get)
    return intent, round(intent_scores[intent],3)

# =========================================================
# GROQ AI (MILESTONE 3)
# =========================================================
client = Groq(api_key="YOUR_GROQ_API_KEY")

def groq_answer(q):
    try:
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"user","content":q}]
        )
        return r.choices[0].message.content
    except Exception as e:
        return str(e)

# =========================================================
# ANALYTICS (MILESTONE 4)
# =========================================================
def log_analytics(query, intent, confidence):
    data = load_json(ANALYTICS_FILE, [])
    data.append({
        "query":query,
        "intent":intent,
        "confidence":confidence,
        "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_json(ANALYTICS_FILE, data)

# =========================================================
# SESSION
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in=False
    st.session_state.user=None
    st.session_state.acc=None

# =========================================================
# TRAIN MODEL
# =========================================================
INTENTS = load_json(INTENTS_FILE, DEFAULT_INTENTS)
model, vectorizer, corpus, labels = train_model(INTENTS)

# =========================================================
# UI
# =========================================================
st.sidebar.title("🏦 BankBot AI")
page = st.sidebar.radio("Navigate",[
    "Chatbot","Create Account","Login",
    "Check Balance","Transfer Money",
    "Admin Panel","Analytics","Logout"
])

# ================= CHATBOT =================
if page=="Chatbot":
    st.header("💬 BankBot Chatbot")
    q = st.text_input("Ask something")
    if st.button("Send"):
        intent, conf = predict_intent(q, model, vectorizer, corpus, labels)
        log_analytics(q,intent,conf)
        st.success(groq_answer(q))
        st.caption(f"Intent: {intent} | Confidence: {conf}")

# ================= CREATE ACCOUNT =================
elif page=="Create Account":
    st.header("🆕 Create Account")
    acc = st.text_input("Account Number")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    acc_type = st.selectbox("Account Type",["Savings","Current"])
    bal = st.number_input("Initial Balance",min_value=0)
    if st.button("Create"):
        st.success("Account created") if create_account(acc,user,pwd,acc_type,bal) else st.error("Already exists")

# ================= LOGIN =================
elif page=="Login":
    st.header("🔑 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        d = login_user(u,p)
        if d:
            st.session_state.logged_in=True
            st.session_state.user=d[1]
            st.session_state.acc=d[0]
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

# ================= CHECK BALANCE =================
elif page=="Check Balance":
    if not st.session_state.logged_in:
        st.warning("Login required")
    else:
        st.success(f"Balance: ₹{get_balance(st.session_state.acc)}")

# ================= TRANSFER =================
elif page=="Transfer Money":
    if not st.session_state.logged_in:
        st.warning("Login required")
    else:
        to = st.text_input("Receiver Account")
        amt = st.number_input("Amount",min_value=1)
        if st.button("Transfer"):
            st.info(transfer_money(st.session_state.acc,to,amt))

# ================= ADMIN =================
elif page=="Admin Panel":
    st.header("🛠 Admin Panel")
    st.json(INTENTS)

# ================= ANALYTICS =================
elif page=="Analytics":
    st.header("📊 Analytics")
    df = pd.DataFrame(load_json(ANALYTICS_FILE, []))
    if not df.empty:
        st.dataframe(df)
        st.altair_chart(
            alt.Chart(df).mark_bar().encode(x="intent",y="count()"),
            use_container_width=True
        )

# ================= LOGOUT =================
elif page=="Logout":
    st.session_state.logged_in=False
    st.session_state.user=None
    st.session_state.acc=None
    st.success("Logged out")
