import streamlit as st
from openai import OpenAI
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
import os
import time

st.set_page_config(page_title="KisanVaani Voice Assistant", page_icon="🌾")

st.title("🌾 KisanVaani – Voice to Voice AI")
st.write("🎤 మాట్లాడండి → 🤖 AI సమాధానం → 🔊 వాయిస్ లో వినండి")

# -----------------------
# OpenAI Client
# -----------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------
# Speech to Text (Whisper)
# -----------------------
def speech_to_text(audio_bytes):
    try:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_bytes
        )
        return transcript.text
    except:
        return None

# -----------------------
# AI Telugu Response
# -----------------------
def ai_response(question):
    try:
        SYSTEM_PROMPT = """
        మీరు రైతుల కోసం రూపొందించిన AI సహాయకుడు.
        పంటలు, పురుగులు, మందుల మోతాదు, పశుపోషణ,
        రుణాలు, మార్కెట్ ధరలు, ప్రభుత్వ పథకాలు —
        అన్నిటికీ సరళమైన తెలుగు భాషలో సమాధానం ఇవ్వండి.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            temperature=0.4,
            max_tokens=400
        )

        return response.choices[0].message.content

    except:
        return "⚠️ ప్రస్తుతం సర్వర్ బిజీగా ఉంది."

# -----------------------
# Text to Telugu Voice
# -----------------------
def text_to_speech(text):
    tts = gTTS(text=text, lang="te")
    filename = "response.mp3"
    tts.save(filename)
    return filename

# -----------------------
# Voice Recorder Button
# -----------------------
audio = mic_recorder(
    start_prompt="🎤 మాట్లాడండి",
    stop_prompt="⏹️ ఆపు",
    key="recorder"
)

if audio:
    st.audio(audio["bytes"])

    # Convert speech to text
    spoken_text = speech_to_text(audio["bytes"])

    if spoken_text:
        st.success(f"మీ ప్రశ్న: {spoken_text}")

        # AI answer
        answer = ai_response(spoken_text)
        st.info(f"సమాధానం: {answer}")

        # Convert to voice
        audio_file = text_to_speech(answer)
        st.audio(audio_file)
