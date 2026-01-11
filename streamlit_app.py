import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="BankBot NLU Engine", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp { background-color: #F5F7FB; }

.main-title {
    text-align: center;
    color: #1E3A8A;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 25px;
}

.section-title {
    color: #111827;
    font-size: 26px;
    font-weight: 600;
    margin-top: 30px;
}

.stButton > button {
    background-color: #1E40AF;
    color: white;
    border-radius: 8px;
    padding: 10px 22px;
    font-size: 16px;
    font-weight: 600;
    border: none;
}
.stButton > button:hover { background-color: #1D4ED8; }

/* ---- Intent Recognition Styling ---- */
.intent-card {
    background-color: white;
    padding: 14px 18px;
    margin: 10px 0;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    font-size: 16px;
    font-weight: 500;
}

.intent-top {
    border-left: 6px solid #22C55E;
    background-color: #ECFDF5;
    font-weight: 700;
}

.intent-score {
    float: right;
    color: #1E40AF;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown(
    "<div class='main-title'>BORRA SRI LAKSHMI’s BankBot NLU Engine</div>",
    unsafe_allow_html=True
)

# ---------------- INTENT DATA ----------------
data = {
"check_balance": [
"What is my account balance?","How can I check my account balance?",
"Where can I view my account balance?","Which account shows my balance?",
"What is my current balance?","How do I see my savings balance?",
"Where is my balance displayed?","Which account has more balance?",
"What is the available balance?","How can I know my bank balance?",
"Where can I check my savings balance?","Which account has less balance?",
"What is my balance today?","How do I view balance online?",
"Where is my checking balance shown?","Which account has the highest balance?",
"What is my remaining balance?","How can I find my balance details?",
"Where do I see my account amount?","Which account balance is updated?",
"What is my total balance?","How can I view my balance in the app?",
"Where can I find balance information?","Which account has recent balance updates?",
"What is my last known balance?","How do I check my balance quickly?",
"Where is my bank balance shown?","Which account balance is active?",
"What is my balance after last transaction?","How can I know available funds?",
"Where can I check my account funds?","Which account contains my money?",
"What is my savings account balance?","How do I access my balance?",
"Where can I view balance summary?","Which account balance should I check?",
"What is my updated balance?","How can I confirm my balance?",
"Where is balance information available?","Which account shows balance details?"
],

"transfer_money": [
"What is the process to transfer money?","How can I transfer money?",
"Where can I initiate a money transfer?","Which account should I transfer from?",
"What steps are required to transfer money?","How do I send money to another account?",
"Where is the transfer option available?","Which account can receive transferred money?",
"What is the safest way to transfer money?","How can I move money between accounts?",
"Where can I check transfer options?","Which account is used for transfers?",
"What details are required for transfer?","How do I make a fund transfer?",
"Where can I send money online?","Which bank supports money transfer?",
"What is the fastest way to transfer funds?","How can I send money securely?",
"Where can I track my transfer status?","Which account gets credited first?",
"What is the transfer procedure?","How do I initiate a transfer?",
"Where can I view transfer history?","Which transfer method is best?",
"What amount can I transfer?","How do I transfer money using the app?",
"Where do I enter transfer details?","Which account can I send money to?",
"What is the limit for money transfer?","How long does a transfer take?",
"Where can I make instant transfers?","Which option transfers money quickly?",
"What are the steps for online transfer?","How do I send funds to savings?",
"Where is fund transfer located?","Which mode is used for transfer?",
"What information is needed to transfer?","How can I complete a money transfer?",
"Where can I initiate fund transfer?","Which account supports transfer service?"
],

"card_block": [
"What is the process to block my card?","How can I block my debit card?",
"Where can I block my credit card?","Which number should I call to block card?",
"What should I do if my card is lost?","How do I freeze my card?",
"Where is the card blocking option?","Which helpline blocks bank cards?",
"What steps are required to block a card?","How can I stop card transactions?",
"Where can I report a stolen card?","Which bank service blocks cards?",
"What is the emergency card block process?","How do I secure my card immediately?",
"Where can I request card blocking?","Which card can be blocked online?",
"What happens after blocking my card?","How do I deactivate my card?",
"Where can I report card loss?","Which documents are needed to block card?",
"What is the fastest way to block card?","How can I block my card using app?",
"Where can I find block card option?","Which card types can be blocked?",
"What should I do for stolen card?","How do I protect my card from misuse?",
"Where can I call to block card?","Which support blocks lost cards?",
"What actions are needed to block card?","How do I stop unauthorized card usage?",
"Where is card security option?","Which card should I block?",
"What is the card blocking procedure?","How can I temporarily block card?",
"Where do I report card theft?","Which service helps block cards?",
"What is the online process to block card?","How can I secure a lost card?",
"Where can I get help to block card?","Which step blocks card immediately?"
],

"find_atm": [
"Where is the nearest ATM?","How can I find an ATM nearby?",
"Which ATM is closest to me?","Where can I withdraw cash?",
"How do I locate an ATM?","Which ATM is open now?",
"Where can I find a bank ATM?","How can I search for ATM?",
"Which ATM is available near me?","Where is the closest cash machine?",
"How do I find ATM location?","Which bank ATM can I use?",
"Where can I get cash nearby?","How can I locate a 24 hour ATM?",
"Which ATM is operational now?","Where is the ATM located?",
"How do I find ATM in my area?","Which ATM is nearest to my location?",
"Where can I withdraw money now?","How can I get ATM directions?",
"Which ATM has no charges?","Where is the nearest cash point?",
"How do I locate bank ATM?","Which ATM supports my card?",
"Where can I check ATM availability?","How can I find ATM on map?",
"Which ATM is nearby?","Where is the closest ATM center?",
"How do I search ATM quickly?","Which ATM is accessible now?",
"Where can I withdraw money safely?","How do I identify nearest ATM?",
"Which ATM location is best?","Where can I find ATM services?",
"How do I find cash withdrawal point?","Which ATM is closest today?",
"Where can I locate emergency ATM?","How can I know ATM location?",
"Which ATM is available in my area?","Where is ATM service provided?"
]
}

# ---------------- TRAIN MODEL ----------------
texts, labels = [], []
for intent, examples in data.items():
    for q in examples:
        texts.append(q)
        labels.append(intent)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

# ---------------- INTENTS UI ----------------
st.markdown("<div class='section-title'>Intents (edit & add)</div>", unsafe_allow_html=True)
for intent, examples in data.items():
    with st.expander(f"{intent} ({len(examples)} examples)", expanded=True):
        for i, q in enumerate(examples, 1):
            st.text_input(f"{i}.", q, key=f"{intent}_{i}")

# ---------------- NLU VISUALIZER ----------------
st.markdown("<div class='section-title'>NLU Visualizer</div>", unsafe_allow_html=True)
query = st.text_area("User Query", height=80)

if st.button("Analyze"):
    q_vec = vectorizer.transform([query])
    probs = model.predict_proba(q_vec)[0]
    intents = model.classes_
    max_prob = max(probs)

    st.subheader("Intent Recognition")
    for intent, p in sorted(zip(intents, probs), key=lambda x: x[1], reverse=True):
        card_class = "intent-card intent-top" if p == max_prob else "intent-card"
        st.markdown(
            f"<div class='{card_class}'>{intent}<span class='intent-score'>{p*100:.1f}%</span></div>",
            unsafe_allow_html=True
        )

    st.subheader("Entity Extraction")
    st.info("No entities found")

# ---------------- TRAIN MODEL ----------------
st.markdown("<div class='section-title'>Train Model</div>", unsafe_allow_html=True)
if st.button("Train Model"):
    model.fit(X, labels)
    st.success("Model trained successfully")

# ---------------- CREATE NEW CONTENT ----------------
st.markdown("<div class='section-title'>Create New Content</div>", unsafe_allow_html=True)

if "new_intents" not in st.session_state:
    st.session_state.new_intents = {}

new_intent = st.text_input("New Intent Name")
new_example = st.text_input("Example Sentence")

if st.button("Add Example"):
    if new_intent and new_example:
        st.session_state.new_intents.setdefault(new_intent, []).append(new_example)
        st.success("New content added successfully")
    else:
        st.warning("Please enter both intent name and example")

if st.session_state.new_intents:
    st.subheader("Newly Added Intents")
    for intent, examples in st.session_state.new_intents.items():
        with st.expander(f"{intent} ({len(examples)} examples)"):
            for ex in examples:
                st.write("•", ex)
