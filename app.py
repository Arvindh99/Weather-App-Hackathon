import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
from api import get_lat_lon, get_current_weather, get_daily_forecast, get_hourly_forecast

images_path = "C:/Users/LENOVO PC/Desktop/Arvindh/Weather App/assets/images/"

st.set_page_config(
    page_title="Weather Now | Frontend Mentor",
    page_icon="☀️",
    layout="wide"
)

col1, col2, col3 = st.columns([0.5, 2, 0.5])

with col1:
    st.write("")
    st.image(images_path + "logo.svg")

with col2:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("<h1 style='text-align: center;'>How's the sky looking today?</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        # Default value: Chennai
        city_name = st.text_input(
            "City Name:",
            label_visibility="hidden",
            placeholder="Search for a place...",
            value="Chennai"
        )
    with col2:
        st.write("")
        search_button = st.button("Search", type="primary")

# ---------------------------
# DEFAULT / SEARCH HANDLING
# ---------------------------
if search_button and city_name.strip() != "":
    selected_city = city_name
else:
    selected_city = "Chennai"  # Default city

# ---------------------------
# FETCH WEATHER DATA
# ---------------------------
name, country = "", ""
temperature = feels_like = humidity = precipitation = wind_speed = 0
time = datetime.now().isoformat()

lat, lon, name, country = get_lat_lon(selected_city)
lat = round(lat, 2)
lon = round(lon, 2)

weather = get_current_weather(lat, lon)
if weather:
    temperature = weather["temperature"]
    feels_like = weather["feels_like"]
    humidity = weather["humidity"]
    precipitation = weather["precipitation"]
    wind_speed = weather["wind_speed"]
    weather_code = weather["weather_code"]
    time = weather["time"]
else:
    st.warning("Could not fetch weather data.")

# ---------------------------
# CURRENT WEATHER SECTION
# ---------------------------
col1, col2 = st.columns(2)
with col1:
    location = name + ", " + country
    date = datetime.fromisoformat(time)
    date = date.strftime("%A, %b %d, %Y")
    temperature = str(temperature) + "°"

    with open(images_path + "bg-today-large.svg", "r", encoding="utf-8") as f:
        svg_content = f.read()

    st.write("")
    st.markdown(
        f"""
        <div style="position: relative; color: white">
            {svg_content}
            <div style="position: absolute; top: 30%; left: 5%"><h2>{location}</h2></div>
            <div style="position: absolute; top: 60%; left: 5%"><p>{date}</p></div>
            <div style="position: absolute; top: 35%; left: 70%"><h1 style="font-size: 48px;">{temperature}</h1></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    row1 = st.columns(4)
    with row1[0]:
        st.metric(label="Feels Like", value=f"{feels_like}°")
    with row1[1]:
        st.metric(label="Humidity", value=f"{humidity}%")
    with row1[2]:
        st.metric(label="Wind", value=f"{wind_speed} km/h")
    with row1[3]:
        st.metric(label="Precipitation", value=f"{precipitation} mm")

    st.write("")
    st.markdown("<h4>Daily forecast</h4>", unsafe_allow_html=True)
    d_forecast = get_daily_forecast(lat, lon)

    if d_forecast:
        row2 = st.columns(7)
        for i in range(7):
            with row2[i]:
                day = datetime.fromisoformat(d_forecast["dates"][i]).strftime("%a")
                temp_max = d_forecast["temp_max"][i]
                temp_min = d_forecast["temp_min"][i]
                code = d_forecast["weather_code"][i]

                st.markdown(
                    f"""
                    <div style="background-color: #1e1e1e; padding: 15px; border-radius: 12px; text-align: center; color: white;">
                        <div style="font-weight: 600; font-size: 16px; margin-bottom: 20px;">{day}</div>
                        <div style="display: flex; justify-content: space-between; font-size: 14px; margin-top: 20px;">
                            <span style="color: #FF4B4B;">{temp_max}°</span>
                            <span style="color: #4BA3FF;">{temp_min}°</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ---------------------------
# HOURLY FORECAST SECTION
# ---------------------------
with col2:
    h_forecast = get_hourly_forecast(lat, lon)
    hourly_by_day = {}

    if h_forecast:
        for t, temp, code in zip(h_forecast["dates"], h_forecast["temp_max"], h_forecast["weather_code"]):
            dt = datetime.fromisoformat(t)
            day_str = dt.strftime("%A")
            if day_str not in hourly_by_day:
                hourly_by_day[day_str] = []
            hourly_by_day[day_str].append({"hour": dt.strftime("%H:%M"), "temp": temp, "code": code})

    days = list(hourly_by_day.keys())

    st.write("")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h4>Hourly Forecast</h4>", unsafe_allow_html=True)

        with col2:
            selected_day = st.selectbox("Select Day", days, index=0, label_visibility="hidden")

        hours = hourly_by_day[selected_day]
        row = st.columns(len(hours))

        for i, h in enumerate(hours):
            with st.container():
                st.markdown(
                    f"""
                    <div style="background-color: #1e1e1e; 
                                padding: 12px; 
                                border-radius: 12px; 
                                text-align: center; 
                                color: white; 
                                width: 900px;
                                height: 40px;
                                margin: auto;">
                        <!-- Time -->
                        <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px;">
                            {h["hour"]}
                        </div>
                        <!-- Temperature -->
                        <div style="font-size: 16px; color: #FFDD57;">
                            {h["temp"]}°
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ---------------------------
# UNIT SWITCH
# ---------------------------
with col3:
    unit_options = st.selectbox(
        "Units",
        ("Switch to Imperial",),
        label_visibility="hidden",
        placeholder="Units",
        index=None
    )
