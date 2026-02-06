import streamlit as st
from gtts import gTTS
import uuid
import os

st.set_page_config(page_title="KisanVaani", page_icon="🌾")
st.title("🌾 KisanVaani – Telugu Voice Assistant")

if "spoken_text" not in st.session_state:
    st.session_state.spoken_text = ""

st.markdown("### 🎤 మాట్లాడండి")

# JavaScript – Speech to Text
st.components.v1.html(
    """
    <script>
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'te-IN';

    function startRec() {
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

    <button onclick="startRec()" style="font-size:22px;">
        🎤 మాట్లాడండి
    </button>
    """,
    height=100,
)

# Receive spoken text safely
spoken_text = st.session_state.get("spoken_text", "")

def respond(text: str):
    if "వాతావరణం" in text:
        return "ఈరోజు వాతావరణం వ్యవసాయానికి అనుకూలంగా ఉంది"
    elif "వరి" in text:
        return "వరి పంటకు నైట్రోజన్ ఎరువు ఉపయోగించండి"
    elif "ఎరువు" in text:
        return "పంట రకాన్ని బట్టి సరైన ఎరువు ఉపయోగించాలి"
    else:
        return "దయచేసి పంట లేదా వాతావరణం గురించి అడగండి"

# Process only if text is valid
if isinstance(spoken_text, str) and spoken_text.strip():
    st.success(f"మీ ప్రశ్న: {spoken_text}")

    answer = respond(spoken_text)
    st.info(f"సమాధానం: {answer}")

    # Text to Speech
    audio_file = f"reply_{uuid.uuid4()}.mp3"
    tts = gTTS(answer, lang="te")
    tts.save(audio_file)

    st.audio(audio_file, format="audio/mp3")
    os.remove(audio_file)
