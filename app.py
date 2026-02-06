import streamlit as st
from gtts import gTTS
from PIL import Image
import uuid
import os
from openai import OpenAI

# ---------------- CONFIG ----------------
st.set_page_config(page_title="KisanVaani", page_icon="🌾")
st.title("🌾 KisanVaani – AI Farmer Assistant")

st.markdown(
    """
    ✅ ఏ ప్రశ్నైనా అడగండి  
    ✅ పంట, పురుగు, ఎరువు, ప్రభుత్వం, లోన్, మార్కెట్  
    ✅ సమాధానం తెలుగులో వాయిస్‌గా  
    """
)

# 🔐 OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- AI RESPONSE ----------------
def ai_respond(question):
    prompt = f"""
    You are an agricultural assistant for Indian farmers.
    Answer clearly in Telugu.
    Do NOT give exact pesticide or chemical dosages.
    Give safe, advisory-style answers.

    Question: {question}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content.strip()

def speak(text):
    file = f"reply_{uuid.uuid4()}.mp3"
    gTTS(text, lang="te").save(file)
    st.audio(file)
    os.remove(file)

# ---------------- TEXT QUESTION ----------------
st.markdown("## ✍️ మీ ప్రశ్న అడగండి")
query = st.text_input("ఉదా: పత్తి పంటలో పురుగులు ఎలా నివారించాలి?")

if query:
    with st.spinner("సమాధానం సిద్ధం అవుతోంది..."):
        answer = ai_respond(query)

    st.success(answer)
    speak(answer)

# ---------------- CAMERA INPUT ----------------
st.markdown("## 📸 పంట లేదా ఆకుల ఫోటో తీయండి")

img = st.camera_input("కెమెరా ఓపెన్ చేయండి")

if img:
    image = Image.open(img)
    st.image(image, caption="మీరు తీసిన చిత్రం")

    cam_answer = (
        "ఈ చిత్రంలో పంటకు సంబంధించిన సమస్య ఉండే అవకాశం ఉంది. "
        "దయచేసి సమీప వ్యవసాయ అధికారిని సంప్రదించండి."
    )

    st.info(cam_answer)
    speak(cam_answer)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "⚠️ ఈ యాప్ సలహా మాత్రమే ఇస్తుంది. "
    "రసాయనాల వినియోగానికి ముందు నిపుణుల సలహా తప్పనిసరి."
)
