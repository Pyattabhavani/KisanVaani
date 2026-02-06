import streamlit as st
from gtts import gTTS
import base64
import uuid
import os

st.set_page_config(page_title="KisanVaani", page_icon="🌾")
st.title("🌾 KisanVaani – Telugu Voice Assistant")

st.markdown("### 🎤 మాట్లాడండి (Chrome browser లో మాత్రమే పని చేస్తుంది)")

# JavaScript component: voice → auto-send to Streamlit
spoken_text = st.components.v1.html(
    """
    <script>
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'te-IN';
    recognition.continuous = false;

    function startRecognition() {
        recognition.start();
    }

    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;
        window.parent.postMessage(
            { type: "streamlit:setComponentValue", value: text },
            "*"
        );
    };
    </script>

    <button onclick="startRecognition()" style="font-size:20px;">
        🎤 మాట్లాడండి
    </button>
    """,
    height=100,
)

def respond(text):
    if "వాతావరణం" in text:
        return "ఈరోజు వాతావరణం వ్యవసాయానికి అనుకూలంగా ఉంది"
    elif "వరి" in text:
        return "వరి పంటకు నైట్రోజన్ ఎరువు ఉపయోగించండి"
    elif "ఎరువు" in text:
        return "పంట రకాన్ని బట్టి సరైన ఎరువు ఉపయోగించాలి"
    else:
        return "పంట లేదా వాతావరణం గురించి అడగండి"

if spoken_text:
    st.success(f"మీ ప్రశ్న: {spoken_text}")

    answer = respond(spoken_text)
    st.info(f"సమాధానం: {answer}")

    # Generate Telugu voice
    filename = f"reply_{uuid.uuid4()}.mp3"
    tts = gTTS(answer, lang="te")
    tts.save(filename)

    st.audio(filename, format="audio/mp3")

    os.remove(filename)
