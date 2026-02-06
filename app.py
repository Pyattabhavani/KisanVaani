import streamlit as st
from gtts import gTTS
import uuid
import os

st.set_page_config(page_title="KisanVaani", page_icon="🌾")
st.title("🌾 KisanVaani – Smart Farming Assistant")

def respond(text):
    if "వాతావరణం" in text:
        return "ఈరోజు వాతావరణం వ్యవసాయానికి అనుకూలంగా ఉంది"
    elif "వరి" in text:
        return "వరి పంటకు నైట్రోజన్ ఎరువు ఉపయోగించండి"
    elif "ఎరువు" in text:
        return "పంట రకాన్ని బట్టి సరైన ఎరువు వాడాలి"
    else:
        return "దయచేసి పంట లేదా వాతావరణం గురించి అడగండి"

query = st.text_input("✍️ మీ ప్రశ్న టైప్ చేయండి (Telugu)")

if query:
    answer = respond(query)
    st.success(answer)

    file = f"reply_{uuid.uuid4()}.mp3"
    gTTS(answ
