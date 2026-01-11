import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="BankBot Assistant", layout="wide")

# ---------------- ENHANCED CSS ----------------
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
h1, h2, h3 {
    text-align: center;
}

/* Sidebar buttons */
.stButton > button {
    background-color: #fdb813;
    color: black;
    font-weight: 600;
    width: 100%;
    margin-bottom: 10px;
    border-radius: 10px;
    padding: 8px;
}
.stButton > button:hover {
    background-color: #e6a100;
    color: white;
}

/* Card style */
.card {
    background-color: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    max-width: 500px;
    margin: auto;
}

/* Inputs */
.stTextInput input, .stNumberInput input {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Create Account"

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🏦 BankBot")

    if st.button("📝 Create Account"):
        st.session_state.page = "Create Account"

    if st.button("🔐 Login"):
        st.session_state.page = "Login"

    if st.button("💰 Check Balance"):
        if st.session_state.logged_in:
            st.session_state.page = "Check Balance"
        else:
            st.warning("Please login first")

    if st.button("💸 Transfer Money"):
        if st.session_state.logged_in:
            st.session_state.page = "Transfer Money"
        else:
            st.warning("Please login first")

    st.divider()

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "Login"
        st.success("Logged out successfully")

# ---------------- HEADER ----------------
st.markdown("<h1>🏦 BankBot Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h3>Milestone 2 – Dialogue Manager</h3>", unsafe_allow_html=True)
st.divider()

# ---------------- CREATE ACCOUNT ----------------
if st.session_state.page == "Create Account":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 Create Account")

    name = st.text_input("Name")
    acc_no = st.text_input("Account Number")

    acc_type = st.selectbox(
        "Account Type",
        ["Savings", "Current"]
    )

    init_balance = st.number_input(
        "Initial Balance",
        min_value=0,
        step=500
    )

    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        if name and acc_no and password:
            st.success("Account created successfully!")
            st.info(
                f"""
                **Account Details**
                - Account Type: {acc_type}
                - Initial Balance: ₹{init_balance}
                """
            )
        else:
            st.error("Please fill all fields")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- LOGIN ----------------
elif st.session_state.page == "Login":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🔐 Login")

    acc_no = st.text_input("Account Number")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if acc_no and password:
            st.session_state.logged_in = True
            st.session_state.page = "Check Balance"
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CHECK BALANCE ----------------
elif st.session_state.page == "Check Balance":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💰 Account Balance")
    st.success("Your current balance is")
    st.markdown("### ₹10,000")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- TRANSFER MONEY ----------------
elif st.session_state.page == "Transfer Money":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💸 Transfer Money")

    to_acc = st.text_input("To Account Number")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Transfer"):
        if to_acc and amount:
            st.success(f"₹{amount} transferred successfully!")
        else:
            st.error("Please fill all fields")

    st.markdown('</div>', unsafe_allow_html=True)
