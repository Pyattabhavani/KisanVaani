import streamlit as st
from gtts import gTTS
import requests
import tempfile

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="KisanVaani+ Smart Farmer", page_icon="🌾")

st.title("🌾 KisanVaani+ Smart Farmer Assistant")
st.markdown("### 🌦 వాతావరణ సమాచారం పొందండి")

# ----------------------------
# Weather API Key
# ----------------------------
WEATHER_KEY = st.secrets["WEATHER_API_KEY"]

# ----------------------------
# Get Weather Data
# ----------------------------
def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return None

        return {
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"],
            "description": data["weather"][0]["description"]
        }

    except:
        return None


# ----------------------------
# Telugu Weather Report (Manual Logic)
# ----------------------------
def generate_telugu_weather(city):
    weather = get_weather(city)

    if not weather:
        return "క్షమించండి, వాతావరణ సమాచారం పొందలేకపోయాము. నగరం పేరు సరైనదిగా ఇవ్వండి."

    temp = weather["temp"]
    humidity = weather["humidity"]
    wind = weather["wind"]
    desc = weather["description"]

    report = f"""
🌡 ఉష్ణోగ్రత: {temp}°C  
💧 తేమ: {humidity}%  
🌬 గాలి వేగం: {wind} మీ/సెకన్డు  
☁ పరిస్థితి: {desc}
"""

    # Farming Advice Logic
    if wind < 8:
        report += "\n👉 స్ప్రేయింగ్ చేయడానికి అనుకూలమైన రోజు."
    else:
        report += "\n👉 గాలి ఎక్కువగా ఉంది. స్ప్రేయింగ్ చేయడం మంచిది కాదు."

    if humidity > 80:
        report += "\n👉 తేమ ఎక్కువగా ఉంది. ఫంగస్ వచ్చే అవకాశం ఉంది."

    if temp > 35:
        report += "\n👉 ఉష్ణోగ్రత ఎక్కువగా ఉంది. పంటలకు నీరు అవసరం."

    return report


# ----------------------------
# Voice Output
# ----------------------------
def speak(text):
    tts = gTTS(text=text, lang="te")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        st.audio(tmp.name)


# ----------------------------
# UI
# ----------------------------
city = st.text_input("మీ జిల్లా లేదా నగరం పేరు (English లో) ఇవ్వండి:")

if st.button("వాతావరణం చూపించు"):
    if city:
        report = generate_telugu_weather(city)
        st.success(report)
        speak(report)
    else:
        st.warning("దయచేసి నగరం పేరు ఇవ్వండి.")
