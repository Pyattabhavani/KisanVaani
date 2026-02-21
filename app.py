import streamlit as st
from gtts import gTTS
import base64
import os

st.set_page_config(page_title="KisanVaani", page_icon="🌾")
st.title("🌾 KisanVaani – Telugu Voice Assistant (Web)")

st.markdown("### 🎤 మాట్లాడండి (Chrome Browser లో మాత్రమే పని చేస్తుంది)")

# JavaScript for speech recognition
st.components.v1.html("""
<script>
var recognition = new webkitSpeechRecognition();
recognition.lang = 'te-IN';
recognition.continuous = false;

function startDictation() {
    recognition.start();
}

recognition.onresult = function(event) {
    var text = event.results[0][0].transcript;
    document.getElementById("spoken").value = text;
};
</script>

<button onclick="startDictation()">🎤 మాట్లాడండి</button>
<br><br>
<textarea id="spoken" rows="3" cols="40" placeholder="మీ మాట ఇక్కడ కనిపిస్తుంది"></textarea>
""", height=200)

query = st.text_input("🔁 మాటలను ఇక్కడ paste చేయండి:")

def respond(text):
    if "వాతావరణం" in text:
        return "ఈరోజు వాతావరణం వ్యవసాయానికి అనుకూలంగా ఉంది"
    elif "వరి" in text:
        return "వరి పంటకు నైట్రోజన్ ఎరువు ఉపయోగించండి"
    else:
        return "పంట లేదా వాతావరణం గురించి అడగండి"

if st.button("సమాధానం పొందండి"):
    if query:
        answer = respond(query)
        st.success(answer)

        tts = gTTS(answer, lang="te")
        tts.save("reply.mp3")

        audio_file = open("reply.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")
