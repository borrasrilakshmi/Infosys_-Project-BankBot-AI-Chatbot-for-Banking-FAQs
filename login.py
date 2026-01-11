import streamlit as st
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "data", "users.json")

def login():
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if not os.path.exists(USERS_FILE):
            st.error(f"Users file not found! Path checked: {USERS_FILE}")
            return

        with open(USERS_FILE, "r") as f:
            users = json.load(f)

        username = username.strip()
        password = password.strip()

        user_found = any(u['username'] == username and u['password'] == password for u in users)
        if user_found:
            st.session_state['logged_in'] = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials!")
