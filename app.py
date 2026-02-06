import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import uuid

st.set_page_config(page_title="KisanVaani", page_icon="🌾")
st.title("🌾 KisanVaani – Telugu Voice Assistant")

def respond(text):
    if "వాతావరణం" in text:
        return "ఈరోజు వాతావరణం వ్యవసాయానికి అనుకూలంగా ఉంది"
    elif "వరి" in text:
        return "వరి పంటకు నైట్రోజన్ ఎరువు ఉపయోగించండి"
    elif "ఎరువు" in text:
        return "పంట రకాన్ని బట్టి సరైన ఎరువు ఉపయోగించాలి"
    else:
        return "దయచేసి పంట లేదా వాతావరణం గురించి అడగండి"

st.info("🎤 Speak & then press the button")

if st.button("🎤 మాట్లాడండి"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("వినుతున్నాను...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="te-IN")
        st.success(f"మీ ప్రశ్న: {text}")

        answer = respond(text)
        st.info(f"సమాధానం: {answer}")

        file = f"reply_{uuid.uuid4()}.mp3"
        gTTS(answer, lang="te").save(file)
        st.audio(file)
        os.remove(file)

    except:
        st.error("మళ్లీ ప్రయత్నించండి")
