import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.grid import grid
from datetime import datetime
from api import get_lat_lon, get_current_weather, get_daily_forecast, get_hourly_forecast
import base64

# ---------------------------
# PAGE SETUP
# ---------------------------
st.set_page_config(page_title="Weather Now", page_icon="☀️", layout="wide")

# JavaScript to detect screen width
screen_width = st.session_state.get("screen_width", None)
width_script = """
<script>
const width = window.innerWidth;
const streamlitDoc = window.parent.document;
const input = streamlitDoc.querySelector('input[data-testid="stSessionState-screen_width"]');
if (input) {
    const lastValue = input.value;
    if (lastValue !== width.toString()) {
        const event = new Event('input', { bubbles: true });
        input.value = width;
        input.dispatchEvent(event);
    }
}
</script>
"""

# Inject JS into Streamlit
st.components.v1.html(width_script, height=0)

# Hidden input for width value
screen_width = st.text_input("screen_width", value=str(screen_width or ""), label_visibility="collapsed")
if screen_width:
    screen_width = int(screen_width)
    st.session_state["screen_width"] = screen_width
else:
    st.session_state["screen_width"] = 1200  # fallback default

# Determine view type
is_mobile = st.session_state["screen_width"] < 768
is_tablet = 768 <= st.session_state["screen_width"] < 1024

# ---------------------------
# WEATHER ICONS + PATHS
# ---------------------------
images_path = "assets/images/"

weather_icons = {
    0: images_path + "icon-sunny.webp",
    1: images_path + "icon-partly-cloudy.webp",
    2: images_path + "icon-partly-cloudy.webp",
    3: images_path + "icon-overcast.webp",
    45: images_path + "icon-fog.webp",
    48: images_path + "icon-fog.webp",
    51: images_path + "icon-drizzle.webp",
    53: images_path + "icon-drizzle.webp",
    55: images_path + "icon-drizzle.webp",
    61: images_path + "icon-rain.webp",
    63: images_path + "icon-rain.webp",
    65: images_path + "icon-rain.webp",
    71: images_path + "icon-snow.webp",
    73: images_path + "icon-snow.webp",
    75: images_path + "icon-snow.webp",
    95: images_path + "icon-storm.webp"
}

# ---------------------------
# HEADER
# ---------------------------
st.image(images_path + "logo.svg", width=120)
add_vertical_space(2)
st.markdown("<h1 style='text-align:center;'>How's the sky looking today?</h1>", unsafe_allow_html=True)

# ---------------------------
# SEARCH + SETTINGS
# ---------------------------
if is_mobile:
    city_name = st.text_input("Search for a place", "Chennai")
    unit_options = st.selectbox("Units", ("Metric", "Imperial"), index=0)
else:
    col1, col2 = st.columns([3, 1])
    with col1:
        city_name = st.text_input("Search for a place", "Chennai")
    with col2:
        unit_options = st.selectbox("Units", ("Metric", "Imperial"), index=0)

# ---------------------------
# FETCH WEATHER
# ---------------------------
lat, lon, name, country = get_lat_lon(city_name)
weather = get_current_weather(lat, lon)

temperature = weather["temperature"]
feels_like = weather["feels_like"]
humidity = weather["humidity"]
precipitation = weather["precipitation"]
wind_speed = weather["wind_speed"]
weather_code = weather["weather_code"]
time = weather["time"]

# Unit conversion
def convert_temperature(temp_c): return round(temp_c * 1.8 + 32)
def convert_wind_speed(speed_kmh): return round(speed_kmh * 0.621371)
def convert_precipitation(mm): return round(mm * 0.03937)

if unit_options == "Imperial":
    temperature = f"{convert_temperature(temperature)}°F"
    feels_like = f"{convert_temperature(feels_like)}°F"
    wind_speed = f"{convert_wind_speed(wind_speed)} mph"
    precipitation = f"{convert_precipitation(precipitation)} in"
else:
    temperature = f"{round(temperature)}°C"
    feels_like = f"{round(feels_like)}°C"
    wind_speed = f"{round(wind_speed)} km/h"
    precipitation = f"{round(precipitation)} mm"

# ---------------------------
# RESPONSIVE LAYOUT
# ---------------------------
if is_mobile:
    st.markdown(f"<h2 style='text-align:center'>{name}, {country}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;font-size:18px;'>{datetime.fromisoformat(time).strftime('%A, %b %d, %Y')}</p>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center;font-size:64px;'>{temperature}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>Feels like {feels_like}, Wind {wind_speed}, Humidity {humidity}%, Precipitation {precipitation}</p>", unsafe_allow_html=True)
else:
    col1, col2 = st.columns([1.5, 2])
    with col1:
        st.markdown(f"### {name}, {country}")
        st.markdown(f"**{datetime.fromisoformat(time).strftime('%A, %b %d, %Y')}**")
        st.markdown(f"#### {temperature}")
        st.markdown(f"Feels like: {feels_like}")
    with col2:
        st.markdown(f"**Humidity:** {humidity}%")
        st.markdown(f"**Wind:** {wind_speed}")
        st.markdown(f"**Precipitation:** {precipitation}")

# ---------------------------
# FORECAST SECTIONS (reused)
# ---------------------------
st.divider()
st.markdown("### Daily Forecast")
d_forecast = get_daily_forecast(lat, lon)
if d_forecast:
    cols = st.columns(3 if is_mobile else 7)
    for i, col in enumerate(cols[:7]):
        day = datetime.fromisoformat(d_forecast["dates"][i]).strftime("%a")
        temp_max = round(d_forecast["temp_max"][i])
        temp_min = round(d_forecast["temp_min"][i])
        if unit_options == "Imperial":
            temp_max = convert_temperature(temp_max)
            temp_min = convert_temperature(temp_min)
        icon_path = weather_icons.get(d_forecast["weather_code"][i], images_path + "icon-sunny.webp")
        with open(icon_path, "rb") as img:
            encoded_icon = base64.b64encode(img.read()).decode()
        with col:
            st.markdown(
                f"""
                <div style="background-color:#262540;border-radius:12px;padding:12px;color:white;text-align:center;">
                    <div>{day}</div>
                    <img src="data:image/webp;base64,{encoded_icon}" width="40">
                    <div>{temp_max}° / {temp_min}°</div>
                </div>""", unsafe_allow_html=True)

st.divider()
st.markdown("### Hourly Forecast")
h_forecast = get_hourly_forecast(lat, lon)
if h_forecast:
    for t, temp, code in zip(h_forecast["dates"], h_forecast["temp_max"], h_forecast["weather_code"]):
        dt = datetime.fromisoformat(t)
        if unit_options == "Imperial":
            temp = convert_temperature(temp)
        icon_path = weather_icons.get(code, images_path + "icon-sunny.webp")
        with open(icon_path, "rb") as img:
            encoded_icon = base64.b64encode(img.read()).decode()
        st.markdown(
            f"""
            <div style="background-color:#302F4A;border-radius:8px;padding:10px;margin-bottom:5px;color:white;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span><img src="data:image/webp;base64,{encoded_icon}" width="20" style="margin-right:8px;"> {dt.strftime("%I %p")}</span>
                    <span>{int(round(temp))}°</span>
                </div>
            </div>""", unsafe_allow_html=True)
