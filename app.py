import streamlit as st
from gtts import gTTS
import requests
import tempfile
from datetime import datetime

st.set_page_config(page_title="KisanVaani+ Smart Farmer", page_icon="🌾")

st.title("🌾 KisanVaani+ Smart Farmer Assistant")
st.markdown("### 🌦 5 రోజుల వాతావరణ సమాచారం")

WEATHER_KEY = st.secrets["WEATHER_API_KEY"]

# -----------------------------
# Get 5-Day Forecast
# -----------------------------
def get_forecast(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != "200":
            return None

        forecast_list = data["list"]
        daily_data = {}

        for item in forecast_list:
            date = item["dt_txt"].split(" ")[0]

            if date not in daily_data:
                daily_data[date] = {
                    "temp": item["main"]["temp"],
                    "humidity": item["main"]["humidity"],
                    "wind": item["wind"]["speed"],
                    "description": item["weather"][0]["description"],
                    "rain": item.get("rain", {}).get("3h", 0)
                }

        return daily_data

    except:
        return None


# -----------------------------
# Telugu Forecast Generator
# -----------------------------
def generate_telugu_forecast(city):
    forecast = get_forecast(city)

    if not forecast:
        return "క్షమించండి, వాతావరణ సమాచారం పొందలేకపోయాము."

    report = ""
    today = datetime.now().date()

    for i, (date, data) in enumerate(forecast.items()):
        if i >= 5:
            break

        temp = data["temp"]
        humidity = data["humidity"]
        wind = data["wind"]
        desc = data["description"]
        rain = data["rain"]

        report += f"\n📅 తేదీ: {date}\n"
        report += f"🌡 ఉష్ణోగ్రత: {temp}°C\n"
        report += f"💧 తేమ: {humidity}%\n"
        report += f"🌬 గాలి వేగం: {wind} మీ/సెక\n"
        report += f"☁ పరిస్థితి: {desc}\n"

        if rain > 0:
            report += "🌧 వర్షం వచ్చే అవకాశం ఉంది.\n"
        else:
            report += "☀ వర్షం అవకాశం తక్కువ.\n"

        if wind < 8:
            report += "👉 స్ప్రేయింగ్ చేయడానికి అనుకూలం.\n"
        else:
            report += "👉 గాలి ఎక్కువగా ఉంది. స్ప్రేయింగ్ చేయవద్దు.\n"

        report += "\n--------------------------\n"

    return report


# -----------------------------
# Voice Output
# -----------------------------
def speak(text):
    tts = gTTS(text=text, lang="te")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        st.audio(tmp.name)


# -----------------------------
# UI
# -----------------------------
city = st.text_input("మీ జిల్లా లేదా నగరం పేరు (English లో) ఇవ్వండి:")

if st.button("5 రోజుల వాతావరణం చూపించు"):
    if city:
        report = generate_telugu_forecast(city)
        st.success(report)
        speak(report)
    else:
        st.warning("దయచేసి నగరం పేరు ఇవ్వండి.")
