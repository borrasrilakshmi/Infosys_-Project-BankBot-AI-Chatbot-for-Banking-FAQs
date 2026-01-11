import streamlit as st
import json, os
import pandas as pd
import altair as alt
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🏦 BankBot Admin",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DARK THEME & ENHANCED UI ----------------
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#020617 0%,#020617 100%);}
section[data-testid="stSidebar"] {background: linear-gradient(180deg, #020617, #020617);}
h1,h2,h3,h4 {color:#7dd3fc !important; font-weight:700;}
div.stButton>button {
    background: linear-gradient(135deg,#2563eb,#38bdf8); color:#020617; border-radius:12px; height:46px; font-weight:700; border:none; transition:all 0.3s ease-in-out;
}
div.stButton>button:hover {
    background: linear-gradient(135deg,#38bdf8,#22d3ee); transform:translateY(-2px) scale(1.03); box-shadow:0 8px 20px rgba(56,189,248,0.45);
}
.metric {background: linear-gradient(135deg,#020617,#020617); border:1px solid #1e293b; padding:22px; border-radius:18px; color:#e5e7eb; text-align:center; font-weight:700; box-shadow:0 10px 30px rgba(0,0,0,0.6);}
.card {background: linear-gradient(135deg,#020617,#020617); border:1px solid #38bdf8; padding:20px; border-radius:18px; text-align:center; color:#e5e7eb; font-weight:700; box-shadow:0 15px 40px rgba(0,0,0,0.6); transition: all 0.3s ease; cursor:pointer;}
.card:hover {transform: translateY(-6px) scale(1.06); box-shadow:0 0 30px rgba(56,189,248,0.6);}
div[data-testid="stDataFrame"] {background:#020617; border-radius:14px; border:1px solid #1e293b;}
div[data-baseweb="select"]>div, input, textarea {background-color:#020617 !important; color:#e5e7eb !important; border-radius:10px !important; border:1px solid #1e293b !important;}
div.stAlert {border-radius:12px;}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
DATA = "data"
os.makedirs(DATA, exist_ok=True)
INTENTS_FILE = f"{DATA}/intents.json"
KB_FILE = f"{DATA}/knowledge_base.json"
ANALYTICS_FILE = f"{DATA}/analytics.json"

# ---------------- JSON HELPERS ----------------
def load_json(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ---------------- LOGIN ----------------
def login():
    if "login" not in st.session_state:
        st.session_state.login = False
    if not st.session_state.login:
        st.title("🔐 Admin Login")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            if u == "admin" and p == "admin":
                st.session_state.login = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        st.stop()

login()

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio("Navigation", ["Dashboard","Intent Manager","Knowledge Base","Chatbot Test","Analytics","Export PDF"])

# ---------------- DASHBOARD ----------------
if page=="Dashboard":
    st.markdown("## 📊 Dashboard Overview")
    intents = load_json(INTENTS_FILE)
    analytics = load_json(ANALYTICS_FILE)
    df = pd.DataFrame(analytics) if analytics else pd.DataFrame()
    
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='metric' style='background:#1e40af'>Total Intents<br>{len(intents)}</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric' style='background:#16a34a'>Total Queries<br>{len(analytics)}</div>", unsafe_allow_html=True)
    if not df.empty:
        top = df['intent'].value_counts().idxmax()
        count = df['intent'].value_counts().max()
        c3.markdown(f"<div class='metric' style='background:#dc2626'>Top Intent<br>{top} ({count})</div>", unsafe_allow_html=True)
    
    st.markdown("### 🎯 All Intents (Click to Open Analytics)")
    icons = ["💳","👋","💸","🏦","📍","🔑","📈","💼","📄","📞"]
    cols_per_row = 4
    for i in range(0,len(intents),cols_per_row):
        cols = st.columns(cols_per_row)
        for j,intent in enumerate(intents[i:i+cols_per_row]):
            icon = icons[(i+j)%len(icons)]
            if cols[j].button(f"{icon} {intent['tag']}"):
                st.session_state.selected_intent=intent["tag"]
                st.session_state.page_jump="Analytics"
                st.rerun()

# ---------------- INTENT MANAGER ----------------
elif page=="Intent Manager":
    st.markdown("## 🧠 Intent Manager")
    intents = load_json(INTENTS_FILE)
    tag = st.text_input("Intent Tag")
    patterns = st.text_area("Patterns (one per line)")
    responses = st.text_area("Responses (one per line)")
    if st.button("Add Intent"):
        intents.append({"tag":tag,"patterns":patterns.lower().splitlines(),"responses":responses.splitlines()})
        save_json(INTENTS_FILE,intents)
        st.success("Intent added")
    if intents:
        st.markdown("### Existing Intents")
        sel = st.selectbox("Select Intent",[i["tag"] for i in intents])
        st.json(next(i for i in intents if i["tag"]==sel))

# ---------------- KNOWLEDGE BASE ----------------
elif page=="Knowledge Base":
    st.markdown("## 📚 Knowledge Base")
    kb = load_json(KB_FILE)
    q = st.text_input("Question")
    a = st.text_area("Answer")
    if st.button("Add Knowledge"):
        kb.append({"question":q,"answer":a})
        save_json(KB_FILE,kb)
        st.success("Added")
    if kb:
        sel = st.selectbox("Select Question",[k["question"] for k in kb])
        st.info(next(k for k in kb if k["question"]==sel)["answer"])

# ---------------- CHATBOT TEST ----------------
elif page=="Chatbot Test":
    st.markdown("<h2 style='color:#1e88e5;'>🤖 Chatbot Test</h2>",unsafe_allow_html=True)
    intents = load_json(INTENTS_FILE)
    if not intents:
        st.warning("Please add intents first")
        st.stop()
    query = st.text_input("Enter your query")
    if query.strip():
        corpus=[]
        labels=[]
        for intent in intents:
            for pattern in intent["patterns"]:
                corpus.append(pattern.lower())
                labels.append(intent["tag"])
        if not corpus:
            st.error("No intent patterns found")
            st.stop()
        vectorizer=TfidfVectorizer()
        X=vectorizer.fit_transform(corpus+[query.lower()])
        similarity_scores=cosine_similarity(X[-1],X[:-1])[0]
        scores={}
        for score,label in zip(similarity_scores,labels):
            scores[label]=max(scores.get(label,0),score)
        df_scores=pd.DataFrame(scores.items(),columns=["Intent","Confidence"]).sort_values("Confidence",ascending=False)
        df_scores["Confidence"]=df_scores["Confidence"].round(4)
        st.success(f"Detected Intent: {df_scores.iloc[0]['Intent']}")
        st.subheader("📊 NLU Confidence Scores")
        st.dataframe(df_scores,use_container_width=True)
        analytics = load_json(ANALYTICS_FILE)
        analytics.append({"intent":df_scores.iloc[0]["Intent"],"confidence":float(df_scores.iloc[0]["Confidence"]),"query":query,"time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        save_json(ANALYTICS_FILE,analytics)

# ---------------- ANALYTICS ----------------
elif page=="Analytics":
    st.markdown("## 📈 Analytics Dashboard")
    analytics = load_json(ANALYTICS_FILE)
    if not analytics:
        st.info("No queries yet.")
        st.stop()
    df = pd.DataFrame(analytics)
    df["time"] = pd.to_datetime(df["time"])
    unique_intents = df["intent"].unique().tolist()
    default_intent = st.session_state.get("selected_intent", unique_intents[0])
    if default_intent not in unique_intents:
        default_intent = unique_intents[0]
    intent_selected = st.selectbox("Select Intent", unique_intents, index=unique_intents.index(default_intent))
    d = df[df.intent==intent_selected]
    c1, c2 = st.columns(2)
    c1.altair_chart(alt.Chart(d).mark_line(point=True).encode(x="time:T",y="confidence:Q").interactive(), use_container_width=True)
    donut = pd.DataFrame({"Category":["High ≥75%","Low <75%"],"Count":[len(d[d.confidence>=0.75]),len(d[d.confidence<0.75])]})
    c2.altair_chart(alt.Chart(donut).mark_arc(innerRadius=60).encode(theta="Count",color="Category:N").interactive(), use_container_width=True)
    overview=[]
    for intent in unique_intents:
        d_int=df[df.intent==intent]
        overview.append({"Intent":intent,"High ≥75%":len(d_int[d_int.confidence>=0.75]),"Low <75%":len(d_int[d_int.confidence<0.75])})
    stacked_df=pd.melt(pd.DataFrame(overview),id_vars=["Intent"],value_vars=["High ≥75%","Low <75%"],var_name="Category",value_name="Count")
    st.markdown("### 🏷 All Intents Overview")
    st.altair_chart(alt.Chart(stacked_df).mark_bar().encode(x="Intent:N",y="Count:Q",color="Category:N",tooltip=["Intent","Category","Count"]),use_container_width=True)
    st.markdown("### 🧾 Latest Queries")
    st.dataframe(d.sort_values("time",ascending=False),use_container_width=True)

# ---------------- EXPORT PDF ----------------
elif page=="Export PDF":
    st.markdown("## 📄 Export Analytics PDF")
    analytics = load_json(ANALYTICS_FILE)
    if not analytics:
        st.warning("No analytics data available")
        st.stop()
    if st.button("Generate PDF"):
        df = pd.DataFrame(analytics)
        df["time"] = pd.to_datetime(df["time"])
        pdf_file = "analytics_report.pdf"
        pdf = SimpleDocTemplate(pdf_file)
        styles = getSampleStyleSheet()
        content=[]
        content.append(Paragraph("BankBot Analytics Report",styles["Title"]))
        content.append(Spacer(1,14))
        for intent in df["intent"].unique():
            intent_df=df[df["intent"]==intent]
            content.append(Paragraph(f"Intent: <b>{intent}</b>",styles["Heading2"]))
            content.append(Spacer(1,8))
            table_data=[["Time","Query","Confidence"]]
            for _,row in intent_df.sort_values("time",ascending=False).iterrows():
                table_data.append([row["time"].strftime("%Y-%m-%d %H:%M:%S"),row["query"],f"{row['confidence']:.3f}"])
            table=Table(table_data,colWidths=[140,260,80],repeatRows=1)
            table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.darkblue),
                                       ("TEXTCOLOR",(0,0),(-1,0),colors.whitesmoke),
                                       ("GRID",(0,0),(-1,-1),0.5,colors.grey),
                                       ("FONT",(0,0),(-1,0),"Helvetica-Bold"),
                                       ("ALIGN",(2,1),(-1,-1),"CENTER"),
                                       ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                                       ("BACKGROUND",(0,1),(-1,-1),colors.beige)]))
            content.append(table)
            content.append(Spacer(1,20))
        pdf.build(content)
        st.success("PDF generated successfully!")
        with open(pdf_file,"rb") as f:
            st.download_button("⬇ Download Analytics PDF",data=f.read(),file_name="analytics_report.pdf",mime="application/pdf")
