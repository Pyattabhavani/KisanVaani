import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os

st.set_page_config(page_title="KisanVaani", page_icon="🌾")
st.title("🌾 KisanVaani – రైతుల వాయిస్ సహాయకుడు")

def listen_telugu():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 మాట్లాడండి...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio, language="te-IN")
    except:
        return None

def respond(text):
    if "వాతావరణం" in text:
        return "ఈరోజు వాతావరణం వ్యవసాయానికి అనుకూలంగా ఉంది"
    elif "వరి" in text:
        return "వరి పంటకు నైట్రోజన్ ఎరువు ఉపయోగించండి"
    elif "ఎరువు" in text:
        return "పంట రకాన్ని బట్టి సరైన ఎరువు ఉపయోగించాలి"
    else:
        return "పంట లేదా వాతావరణం గురించి అడగండి"

if st.button("🎤 మాట్లాడండి"):
    query = listen_telugu()
    if query:
        st.success(f"మీ ప్రశ్న: {query}")
        answer = respond(query)
        st.info(f"సమాధానం: {answer}")

        tts = gTTS(answer, lang='te')
        tts.save("reply.mp3")
        st.audio("reply.mp3")
    else:
        st.error("స్పష్టంగా వినిపించలేదు")
