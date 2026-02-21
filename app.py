import streamlit as st
from openai import OpenAI
from gtts import gTTS
import requests
import os

st.set_page_config(page_title="KisanVaani+", page_icon="🌾")

st.title("🌾 KisanVaani+ Smart Farmer Assistant")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
WEATHER_KEY = st.secrets["WEATHER_API_KEY"]

# ---------------- WEATHER FUNCTION ----------------
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != 200:
        return None

    weather_data = {
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "description": data["weather"][0]["description"]
    }

    return weather_data

# ---------------- TELUGU WEATHER RESPONSE ----------------
def generate_telugu_weather(city):
    weather = get_weather(city)

    if not weather:
        return "క్షమించండి, వాతావరణ సమాచారం పొందలేకపోయాము."

    prompt = f"""
    నగరం: {city}
    ఉష్ణోగ్రత: {weather['temp']}°C
    తేమ: {weather['humidity']}%
    గాలి వేగం: {weather['wind']} m/s
    పరిస్థితి: {weather['description']}

    పై సమాచారం ఆధారంగా రైతులకు సరళమైన తెలుగు వాతావరణ నివేదిక ఇవ్వండి.
    స్ప్రేయింగ్ లేదా వ్యవసాయ పనులకు అనుకూలమా కాదా చెప్పండి.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

# ---------------- VOICE FUNCTION ----------------
def speak(text):
    tts = gTTS(text=text, lang="te")
    filename = "weather.mp3"
    tts.save(filename)
    st.audio(filename)

# ---------------- UI ----------------
st.markdown("### 🌦 వాతావరణ సమాచారం పొందండి")

city = st.text_input("మీ జిల్లా లేదా నగరం పేరు ఇవ్వండి:")

if st.button("వాతావరణం చూపించు"):
    if city:
        report = generate_telugu_weather(city)
        st.success(report)
        speak(report)
    else:
        st.warning("దయచేసి నగరం పేరు ఇవ్వండి.")
