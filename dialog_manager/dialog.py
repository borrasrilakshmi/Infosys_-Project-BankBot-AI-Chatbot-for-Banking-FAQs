from groq import Groq
from database.db import create_account, get_balance

# 🔑 Put your Groq API key here
client = Groq(api_key="YOUR_GROQ_API_KEY")

def llm_reply(prompt):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def get_response(user_input, session):
    text = user_input.lower()

    # -------- ACCOUNT CREATION FLOW --------
    if "create account" in text:
        session.step = "name"
        return "👤 Please enter your name"

    if session.step == "name":
        session.name = user_input
        session.step = "deposit"
        return "💰 Enter initial deposit amount"

    if session.step == "deposit":
        create_account(session.name, int(user_input))
        session.step = None
        return "✅ Account created successfully!"

    # -------- MONEY TRANSFER FLOW --------
    if "transfer" in text:
        session.step = "amount"
        return "💸 How much amount do you want to transfer?"

    if session.step == "amount":
        session.amount = user_input
        session.step = "password"
        return "🔐 Please enter your password"

    if session.step == "password":
        session.step = "receiver"
        return "🏦 Enter receiver account number"

    if session.step == "receiver":
        session.step = None
        return "✅ Transfer Successful"

    # -------- BALANCE --------
    if "balance" in text:
        return f"💳 Your balance is ₹{get_balance()}"

    # -------- LLM FALLBACK --------
    return llm_reply(user_input)
