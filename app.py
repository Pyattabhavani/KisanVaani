import streamlit as st
from openai import OpenAI
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
# API Keys
# ----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
WEATHER_KEY = st.secrets["WEATHER_API_KEY"]

# ----------------------------
# Weather Fetch Function
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
# Telugu Weather Report Generator
# ----------------------------
def generate_telugu_weather(city):
    weather = get_weather(city)

    if not weather:
        return "క్షమించండి, వాతావరణ సమాచారం పొందలేకపోయాము. నగరం పేరు సరైనదిగా ఇవ్వండి."

    prompt = f"""
    నగరం: {city}
    ఉష్ణోగ్రత: {weather['temp']}°C
    తేమ: {weather['humidity']}%
    గాలి వేగం: {weather['wind']} m/s
    పరిస్థితి: {weather['description']}

    పై సమాచారం ఆధారంగా రైతులకు సరళమైన తెలుగు వాతావరణ నివేదిక ఇవ్వండి.
    స్ప్రేయింగ్ లేదా వ్యవసాయ పనులకు అనుకూలమా కాదా కూడా చెప్పండి.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300
    )

    return response.choices[0].message.content


# ----------------------------
# Voice Output Function
# ----------------------------
def speak(text):
    tts = gTTS(text=text, lang="te")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        st.audio(tmp.name)


# ----------------------------
# UI Section
# ----------------------------
city = st.text_input("మీ జిల్లా లేదా నగరం పేరు (English లో) ఇవ్వండి:")

if st.button("వాతావరణం చూపించు"):
    if city:
        report = generate_telugu_weather(city)
        st.success(report)
        speak(report)
    else:
        st.warning("దయచేసి నగరం పేరు ఇవ్వండి.")
