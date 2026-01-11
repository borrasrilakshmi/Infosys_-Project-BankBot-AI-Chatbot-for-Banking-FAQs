import os
import sqlite3
import streamlit as st
from groq import Groq

# ================= RESET DATABASE =================
DB_FILE = "bankbot.db"

# Close any active connection (if exists)
try:
    conn.close()
except:
    pass

# Delete old database file
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("✅ Old database deleted")

# ================= CONFIG =================
GROQ_API_KEY = "gsk_DtkOsb1pS050riGtLOU2WGdyb3FYDrWwuJdYGJzu4fnGA2F1u"
client = Groq(api_key=GROQ_API_KEY)

# ================= DATABASE =================
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

# Initialize fresh DB
init_db()
