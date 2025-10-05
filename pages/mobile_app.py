import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.grid import grid
from datetime import datetime
from api import get_lat_lon, get_current_weather, get_daily_forecast, get_hourly_forecast
import base64


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
    56: images_path + "icon-drizzle.webp",
    57: images_path + "icon-drizzle.webp",
    61: images_path + "icon-rain.webp",         
    63: images_path + "icon-rain.webp", 
    65: images_path + "icon-rain.webp", 
    66: images_path + "icon-rain.webp", 
    67: images_path + "icon-rain.webp", 
    71: images_path + "icon-snow.webp",         
    73: images_path + "icon-snow.webp",
    75: images_path + "icon-snow.webp",
    77: images_path + "icon-snow.webp",
    80: images_path + "icon-rain.webp",  
    81: images_path + "icon-rain.webp",
    82: images_path + "icon-rain.webp",
    85: images_path + "icon-rain.webp",
    86: images_path + "icon-rain.webp",
    95: images_path + "icon-storm.webp",
    96: images_path + "icon-storm.webp",
    99: images_path + "icon-storm.webp"
}

st.set_page_config(page_title="Weather Now | Frontend Mentor",page_icon="☀️",layout="wide")

col1, col2 = st.columns(2)

with col1:
    st.write("")
    st.image(images_path + "logo.svg")
    
    
with col2:
    unit_options = st.selectbox("Units",("⚙️ Switch to Metrics","⚙️ Switch to Imperial",),label_visibility="hidden",placeholder="⚙️ Units",index=None)


st.markdown("<h1 style='text-align: center;'>How's the sky looking today?</h1>", unsafe_allow_html=True)

search_grid = grid([0.8,0.2], vertical_align="bottom")

city_name = search_grid.text_input(label="",placeholder="  Search for a place...",value="Chennai",label_visibility="hidden", icon=':material/search:')
search_button = search_grid.button("Search", type="primary",use_container_width=True)

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
# UNIT SWITCH
# ---------------------------


if unit_options is None:
    unit_options = "Switch to Metrics"
    
def convert_temperature(temp_c):
    if unit_options.startswith("Switch to Imperial"):
        return round(temp_c * 9 / 5 + 32)  # Celsius to Fahrenheit
    return round(temp_c)  # Metric

def convert_wind_speed(speed_kmh):
    if unit_options.startswith("Switch to Imperial"):
        return round(speed_kmh / 1.609, 1)  # km/h to mph
    return round(speed_kmh)

def convert_precipitation(mm):
    if unit_options.startswith("Switch to Imperial"):
        return round(mm / 25.4, 2)  # mm to inches
    return round(mm, 1)

# ---------------------------
# CURRENT WEATHER SECTION
# ---------------------------

location = name + ", " + country
date = datetime.fromisoformat(time)
date = date.strftime("%A, %b %d, %Y")
#temperature = str(temperature) + "°"
weather_code =weather_code

temperature = f"{convert_temperature(temperature)}°"
feels_like = f"{convert_temperature(feels_like)}°"
wind_speed = f"{convert_wind_speed(wind_speed)} {'km/h' if unit_options.startswith('Switch to Metrics') else 'mph'}"
precipitation = f"{convert_precipitation(precipitation)} {'mm' if unit_options.startswith('Switch to Metrics') else 'in'}"

with open(images_path + "bg-today-small.svg", "r", encoding="utf-8") as f:
    svg_content = f.read()

icon_path = weather_icons.get(weather_code, images_path + "icon-sunny.webp")
with open(icon_path, "rb") as image_file:
    encoded_icon = base64.b64encode(image_file.read()).decode()

st.markdown(
    f"""<div style="position: relative; text-align: center; color: white";>
        {svg_content}
        <div style="position: absolute; top: 10%; left: 40%;"><h2>{location}</h2></div>
        <div style="position: absolute; top: 40%; left: 44%;"><p>{date}</p></div>
        <div style="position: absolute; top: 50%; left: 45%;display: flex; align-items: center;"">
        <img src="data:image/webp;base64,{encoded_icon}" style="width:48px; height:48px; margin-right: 10px;">
        <h1 style="font-size: 48px;">{temperature}</h1></div>
    </div>""",unsafe_allow_html=True)

add_vertical_space(2)
row1 = st.columns([1, 1])
row2 = st.columns([1, 1])
with row1[0]: 
    st.markdown(f"""<div style="background-color: #262540; color: white; padding: 20px; border-radius: 12px; text-align: left; min-height: 118px;width: 165px;margin-bottom: 5px;margin-left: 450px;"> 
                <div style="font-weight: 600;">Feels Like</div> <div style="font-size: 24px;margin-top: 20px">{feels_like}</div> </div>""",unsafe_allow_html=True) 
with row1[1]: 
    st.markdown(f"""<div style="background-color: #262540; color: white; padding: 20px; border-radius: 12px; text-align: left; min-height: 118px;width: 165px;margin-left: 0.1px; margin-bottom: 5px;"> 
                <div style="font-weight: 600;">Humidity</div> <div style="font-size: 24px;margin-top: 20px">{humidity}%</div> </div>""",unsafe_allow_html=True) 
with row2[0]: 
    st.markdown(f"""<div style="background-color: #262540; color: white; padding: 20px; border-radius: 12px; text-align: left; min-height: 118px;width: 165px;margin-left: 0.1px;margin-bottom: 5px;margin-left: 450px;"> 
                <div style="font-weight: 600;">Wind</div> <div style="font-size: 24px;margin-top: 20px">{wind_speed}</div> </div>""",unsafe_allow_html=True) 
with row2[1]: 
    st.markdown(f"""<div style="background-color: #262540; color: white; padding: 20px; border-radius: 12px; text-align: left; min-height: 118px;width: 165px;margin-left: 0.1px;margin-bottom: 5px;"> 
                <div style="font-weight: 600;">Precipitation</div> <div style="font-size: 24px;margin-top: 20px">{precipitation}</div> </div>""",unsafe_allow_html=True)

# ---------------------------
# DAILY WEATHER SECTION
# ---------------------------

add_vertical_space(1)
st.markdown(f"""<div style="margin-left: 450px;"><h4>Daily forecast</h4></div>""", unsafe_allow_html=True)
d_forecast = get_daily_forecast(lat, lon)

if d_forecast:
    rows = [range(0, 3), range(3, 6), range(6, 7)]

    for row_indices in rows:
        cards_html = ""
        for i in row_indices:
            day = datetime.fromisoformat(d_forecast["dates"][i]).strftime("%a")

            if unit_options and unit_options.startswith("Switch to Imperial"):
                temp_max = convert_temperature(d_forecast["temp_max"][i])
                temp_min = convert_temperature(d_forecast["temp_min"][i])
            else:
                temp_max = round(d_forecast["temp_max"][i])
                temp_min = round(d_forecast["temp_min"][i])

            code = d_forecast["weather_code"][i]
            icon_path = weather_icons.get(code, images_path + "icon-sunny.webp")
            with open(icon_path, "rb") as image_file:
                encoded_icon = base64.b64encode(image_file.read()).decode()

            cards_html += f"""
            <div style="background-color: #262540; padding: 20px; min-height: 200px; width: 110px;
                        border-radius: 12px; text-align: center; color: white;margin-left: 450px">
                <div style="font-weight: 600; font-size: 18px; margin-bottom: 20px;">{day}</div>
                <div>
                    <img src="data:image/webp;base64,{encoded_icon}" style="width:40px; height:40px;">
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 16px; margin-top: 45px;">
                    <span style="color: white;text-align:left;">{temp_max}°</span>
                    <span style="color: white;text-align:right;">{temp_min}°</span>
                </div>
            </div>
            """

        # Wrap the row in a grid
        st.markdown(
            f"""
            <div style="
                display: grid;
                grid-template-columns: repeat({len(row_indices)}, 110px);
                gap: 10px;
                justify-content: flex-start;
                margin-bottom: 15px;
            ">
                {cards_html}
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------------------
# HOURLY FORECAST SECTION
# ---------------------------


h_forecast = get_hourly_forecast(lat, lon)
hourly_by_day = {}

if h_forecast:
    now = datetime.now()
    for t, temp, code in zip(h_forecast["dates"], h_forecast["temp_max"], h_forecast["weather_code"]):
        dt = datetime.fromisoformat(t)
        day_str = dt.strftime("%A")
        if day_str not in hourly_by_day:
            hourly_by_day[day_str] = []
        if unit_options and unit_options.startswith("Switch to Imperial"):
            temp = convert_temperature(temp)
        else:
            temp = temp
        if dt.date() == now.date() and dt < now:
            continue
        hourly_by_day[day_str].append({
            "hour": dt.strftime("%I %p"),
            "temp": int(round(temp)),
            "code": code
        })
        
        

days = list(hourly_by_day.keys())

with st.container(border=True, height=770):
    col1, col2 = st.columns([3, 1])
    with col1:
        add_vertical_space(1)
        st.markdown("<h4>Hourly Forecast</h4>", unsafe_allow_html=True)
    with col2:
        selected_day = st.selectbox("Select Day", days, index=0, label_visibility="hidden")

    hours = hourly_by_day[selected_day]

    for h in hours:
        icon_path = weather_icons.get(h["code"], images_path + "icon-sunny.webp")
        with open(icon_path, "rb") as image_file:
            encoded_icon = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <div style="background-color: #302F4A; padding: 12px; border-radius: 12px;
                        text-align: center; color: white; width: 100%; height: 70px; 
                        margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center;
                            font-size: 14px; font-weight: 600; padding: 8px;">
                    <span style="display:flex; align-items:center;">
                        <img src="data:image/webp;base64,{encoded_icon}"  width='24' height='24' style='margin-right:8px;'/>
                        {h["hour"]}
                    </span>
                    <span style="font-size: 16px;">{h["temp"]}°</span>
                </div>
            </div>""",unsafe_allow_html=True)





