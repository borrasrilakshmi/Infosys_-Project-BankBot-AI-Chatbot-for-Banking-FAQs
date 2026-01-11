import streamlit as st
import sqlite3
from groq import Groq

# ================= CONFIG =================
GROQ_API_KEY = "gsk_DtkOsb1pS050riGtLOU2WGdyb3FYDrWwuJdYGJzu4fnGA2F1u"
DB_FILE = "bankbot.db"

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

init_db()

# ================= BANK FUNCTIONS =================
def create_account(acc_no, user, pwd, acc_type, bal):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts WHERE account_number=? OR username=?", (acc_no, user))
    if cur.fetchone():
        conn.close()
        return False
    cur.execute(
        "INSERT INTO accounts VALUES (?, ?, ?, ?, ?)",
        (acc_no, user, pwd, acc_type, bal)
    )
    conn.commit()
    conn.close()
    return True

def login_user(user, pwd):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts WHERE username=? AND password=?", (user, pwd))
    data = cur.fetchone()
    conn.close()
    return data

def get_balance(acc_no):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE account_number=?", (acc_no,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def transfer_money(sender_acc, receiver_acc, amount):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE account_number=?", (sender_acc,))
    sender = cur.fetchone()
    cur.execute("SELECT balance FROM accounts WHERE account_number=?", (receiver_acc,))
    receiver = cur.fetchone()
    if not sender or not receiver:
        conn.close()
        return "❌ Invalid account number"
    if sender[0] < amount:
        conn.close()
        return "❌ Insufficient balance"
    cur.execute("UPDATE accounts SET balance=balance-? WHERE account_number=?", (amount, sender_acc))
    cur.execute("UPDATE accounts SET balance=balance+? WHERE account_number=?", (amount, receiver_acc))
    conn.commit()
    conn.close()
    return "✅ Transfer successful"

# ================= AI CHAT =================
def groq_answer(question):
    try:
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        return res.choices[0].message.content
    except:
        return "❌ Groq AI error occurred. Please try again later."

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.acc_no = None

# ================= UI =================
st.set_page_config("🏦 BankBot", layout="centered")
st.sidebar.title("🏦 BankBot Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Chatbot",
        "Create Account",
        "Login",
        "Check Balance",
        "Transfer Money",
        "Database",
        "User Query",
        "Logout"
    ]
)

# ================= CREATE ACCOUNT =================
if page == "Create Account":
    st.header("🆕 Create Account")
    acc = st.text_input("Account Number")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    acc_type = st.selectbox("Account Type", ["Savings", "Current"])
    bal = st.number_input("Initial Balance", min_value=0)

    if st.button("Create Account"):
        if create_account(acc, user, pwd, acc_type, bal):
            st.success("✅ Account created successfully")
        else:
            st.error("❌ Account number or username already exists")

# ================= LOGIN =================
elif page == "Login":
    st.header("🔑 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        data = login_user(user, pwd)
        if data:
            st.session_state.logged_in = True
            st.session_state.user = data[1]
            st.session_state.acc_no = data[0]
            st.success(f"✅ Welcome {data[1]}")
        else:
            st.error("❌ Login failed")

# ================= CHECK BALANCE =================
elif page == "Check Balance":
    st.header("💰 Check Balance")
    if not st.session_state.logged_in:
        st.warning("Please login first")
    else:
        bal = get_balance(st.session_state.acc_no)
        st.success(f"💰 Your balance is ₹{bal}")

# ================= TRANSFER MONEY =================
elif page == "Transfer Money":
    st.header("💸 Transfer Money")
    if not st.session_state.logged_in:
        st.warning("Please login first")
    else:
        to_acc = st.text_input("Receiver Account Number")
        amount = st.number_input("Amount", min_value=1)
        if st.button("Transfer"):
            msg = transfer_money(st.session_state.acc_no, to_acc, amount)
            st.info(msg)

# ================= DATABASE =================
elif page == "Database":
    st.header("🗄 Database – All Accounts")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT account_number, username, account_type, balance FROM accounts")
    rows = cur.fetchall()
    conn.close()
    if rows:
        st.table([{"Account Number": r[0], "Username": r[1], "Account Type": r[2], "Balance": r[3]} for r in rows])
    else:
        st.info("No accounts found")

# ================= CHATBOT =================
elif page == "Chatbot":
    st.header("💬 Bank Chatbot")
    q = st.text_input("Ask anything (banking or general question)")
    if st.button("Send"):
        st.write("🤖", groq_answer(q))

# ================= USER QUERY =================
elif page == "User Query":
    st.header("📌 User Query")
    q = st.text_input("Ask any question")
    if st.button("Submit"):
        st.write("🤖", groq_answer(q))

# ================= LOGOUT =================
elif page == "Logout":
    if st.session_state.logged_in:
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.acc_no = None
        st.success("✅ Logged out successfully")
    else:
        st.info("You are not logged in")
