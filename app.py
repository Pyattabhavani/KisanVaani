import streamlit as st
from openai import OpenAI
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
import tempfile

st.set_page_config(page_title="KisanVaani Voice AI", page_icon="🌾")

st.title("🌾 KisanVaani – Voice to Voice Assistant")

# OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# Speech to Text
# -----------------------------
def speech_to_text(audio_bytes):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file
            )

        return transcript.text

    except Exception as e:
        st.error(f"Transcription Error: {e}")
        return None


# -----------------------------
# AI Response
# -----------------------------
def ai_response(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Telugu AI assistant for farmers. Reply only in Telugu."
                },
                {"role": "user", "content": question}
            ],
            temperature=0.4,
            max_tokens=300
        )
        return response.choices[0].message.content

    except Exception as e:
        st.error(f"AI Error: {e}")
        return None


# -----------------------------
# Text to Speech
# -----------------------------
def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang="te")
        filename = "response.mp3"
        tts.save(filename)
        return filename
    except Exception as e:
        st.error(f"TTS Error: {e}")
        return None


# -----------------------------
# Mic Recorder
# -----------------------------
audio = mic_recorder(
    start_prompt="🎤 మాట్లాడండి",
    stop_prompt="⏹️ ఆపు",
    key="recorder"
)

if audio:
    st.audio(audio["bytes"])

    st.info("🔄 Converting speech to text...")
    spoken_text = speech_to_text(audio["bytes"])

    if spoken_text:
        st.success(f"మీ ప్రశ్న: {spoken_text}")

        st.info("🤖 Getting AI answer...")
        answer = ai_response(spoken_text)

        if answer:
            st.success(f"సమాధానం: {answer}")

            st.info("🔊 Generating voice...")
            audio_file = text_to_speech(answer)

            if audio_file:
                st.audio(audio_file)
