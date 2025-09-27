

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
from api import get_lat_lon, get_current_weather

images_path = "C:/Users/LENOVO PC/Desktop/Arvindh/Weather App/assets/images/"

st.set_page_config(page_title="Weather Now | Frontend Mentor",page_icon="☀️" ,layout="wide")

col1, col2, col3 = st.columns([0.5,2,0.5])
    
with col1:
    st.write("")
    st.image(images_path + "logo.svg")
    
with col2:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.markdown("<h1 style='text-align: center;'>How's the sky looking today?</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns([4,1])
    with col1:   
        city_name = st.text_input("City Name:",label_visibility="hidden", placeholder= "Search for a place...", icon = ":material/search:")
    with col2:
        st.write("")
        search_button = st.button("Search", type="primary")
    name, country = "", ""
    time = datetime.now().isoformat()
    temperature = feels_like = humidity = precipitation = wind_speed = 0
    if search_button:
        lat, lon, name, country = get_lat_lon(city_name)
        # st.write(lat, lon)
        lat = round(lat,2)
        lon = round(lon,2)
        weather = get_current_weather(lat, lon)
        if weather:
            temperature = weather["temperature"]
            feels_like = weather["feels_like"]
            humidity = weather["humidity"]
            precipitation = weather["precipitation"]
            wind_speed = weather["wind_speed"]
            weather_code = weather["weather_code"]
            time = weather["time"]
        
            #st.write(weather["temperature"], weather["feels_like"], weather["humidity"], weather["precipitation"], weather["wind_speed"], weather["weather_code"])
        else:
            st.warning("Could not fetch weather data.")


        
        

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
        st.metric(label="Feels Like", value=f"{feels_like}°", border=True)
    with row1[1]:
        st.metric(label="Humidity", value=f"{humidity}%", border=True)
    with row1[2]:
        st.metric(label="Wind", value=f"{wind_speed} km/h", border=True)
    with row1[3]:
        st.metric(label="Precipitation", value=f"{precipitation} mm", border=True)





    
with col3:
    unit_options = st.selectbox("Units" , ("Switch to Imperial"), label_visibility="hidden", placeholder="Units",index=None)