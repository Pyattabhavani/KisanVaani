import streamlit as st
from gtts import gTTS
import requests
import tempfile

st.set_page_config(
    page_title="KisanVaani+",
    page_icon="🌾",
    layout="wide"
)

# ---------- CUSTOM UI ----------
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #d4fc79, #96e6a1);
}
.big-title {
    font-size:38px;
    font-weight:bold;
    color:#1b5e20;
    text-align:center;
}
.card {
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.2);
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-title'>🌾 KisanVaani+ Smart Farmer Assistant</div>", unsafe_allow_html=True)
st.markdown("### 🌦 వాతావరణం + పంటల సలహా వ్యవస్థ")

WEATHER_KEY = st.secrets["WEATHER_API_KEY"]

# ---------- WEATHER FUNCTION ----------
def get_weather(city):
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

# ---------- CROP ADVISORY ----------
def crop_advisory(crop, weather):
    temp = weather["temp"]
    humidity = weather["humidity"]
    wind = weather["wind"]
    desc = weather["description"]

    advice = f"ఈ రోజు ఉష్ణోగ్రత {temp}°C, తేమ {humidity}%, గాలి వేగం {wind} మీ/సెక. "

    if "rain" in desc:
        advice += "వర్షం అవకాశం ఉంది. "
    else:
        advice += "వర్షం అవకాశం తక్కువ. "

    # Paddy Advice
    if crop == "Paddy (ధాన్యం)":
        if temp > 35:
            advice += "ధాన్యానికి ఎక్కువ వేడి ఉంది. నీటిని నిల్వ చేయండి. "
        if humidity > 80:
            advice += "ఫంగస్ వచ్చే అవకాశం ఉంది. కీటకనాశిని జాగ్రత్తగా వాడండి. "
        advice += "నీటి మట్టం నిల్వ ఉంచండి."

    # Cotton Advice
    elif crop == "Cotton (పత్తి)":
        if wind > 8:
            advice += "గాలి ఎక్కువగా ఉంది. స్ప్రేయింగ్ చేయవద్దు. "
        else:
            advice += "స్ప్రేయింగ్ చేయడానికి అనుకూలం. "
        advice += "పత్తిలో తెల్లదోమలు పరిశీలించండి."

    # Maize Advice
    elif crop == "Maize (మొక్కజొన్న)":
        if temp < 20:
            advice += "చలిగా ఉంది. వృద్ధి మందగించవచ్చు. "
        advice += "ఎరువులు సరైన మోతాదులో ఇవ్వండి."

    return advice

# ---------- VOICE ----------
def speak(text):
    tts = gTTS(text=text, lang="te")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        st.audio(tmp.name)

# ---------- UI ----------
col1, col2 = st.columns(2)

with col1:
    city = st.text_input("📍 మీ నగరం (English లో):")

with col2:
    crop = st.selectbox(
        "🌾 పంట ఎంపిక చేయండి:",
        ["Paddy (ధాన్యం)", "Cotton (పత్తి)", "Maize (మొక్కజొన్న)"]
    )

if st.button("📊 సమాచారం పొందండి"):
    weather = get_weather(city)

    if not weather:
        st.error("❌ నగరం పేరు తప్పుగా ఉంది.")
    else:
        st.markdown(f"""
        <div class='card'>
        🌡 ఉష్ణోగ్రత: {weather['temp']}°C<br>
        💧 తేమ: {weather['humidity']}%<br>
        🌬 గాలి వేగం: {weather['wind']} m/s<br>
        ☁ పరిస్థితి: {weather['description']}
        </div>
        """, unsafe_allow_html=True)

        advice = crop_advisory(crop, weather)

        st.success("🌾 పంట సలహా:")
        st.write(advice)

        speak(advice)
