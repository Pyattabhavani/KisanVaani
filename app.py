import streamlit as st
from gtts import gTTS
import requests
import tempfile

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="KisanVaani+",
    page_icon="🌾",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #d4fc79, #96e6a1);
}
.big-title {
    font-size:40px;
    font-weight:bold;
    color:#1b5e20;
}
.card {
    background-color:white;
    padding:20px;
    border-radius:15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    margin-bottom:15px;
}
.center {
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='center big-title'>🌾 KisanVaani+ Smart Farmer Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='center'>🌦 5 రోజుల వాతావరణ నివేదిక</div>", unsafe_allow_html=True)
st.markdown("---")

WEATHER_KEY = st.secrets["WEATHER_API_KEY"]

# ---------------- GET FORECAST ----------------
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


# ---------------- VOICE ----------------
def speak(text):
    tts = gTTS(text=text, lang="te")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        st.audio(tmp.name)

# ---------------- UI INPUT ----------------
city = st.text_input("📍 మీ జిల్లా లేదా నగరం పేరు (English లో) ఇవ్వండి:")

if st.button("🌤 వాతావరణ నివేదిక పొందండి"):
    forecast = get_forecast(city)

    if not forecast:
        st.error("❌ నగరం పేరు తప్పుగా ఉండవచ్చు.")
    else:
        report_text = ""
        col1, col2, col3 = st.columns(3)

        cols = [col1, col2, col3]

        for i, (date, data) in enumerate(list(forecast.items())[:5]):
            col = cols[i % 3]
            with col:
                st.markdown(f"""
                <div class='card'>
                <h4>📅 {date}</h4>
                🌡 <b>{data['temp']}°C</b><br>
                💧 {data['humidity']}%<br>
                🌬 {data['wind']} m/s<br>
                ☁ {data['description']}<br>
                </div>
                """, unsafe_allow_html=True)

            report_text += f"{date} రోజున ఉష్ణోగ్రత {data['temp']} డిగ్రీలు, తేమ {data['humidity']} శాతం, గాలి వేగం {data['wind']} మీటర్లు ప్రతిసెకను. "

            if data['rain'] > 0:
                report_text += "వర్షం వచ్చే అవకాశం ఉంది. "
            else:
                report_text += "వర్షం అవకాశం తక్కువ. "

        st.markdown("### 🔊 వాయిస్ నివేదిక")
        speak(report_text)
