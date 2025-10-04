import requests

def get_lat_lon(city_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            loc = data["results"][0]
            return loc["latitude"], loc["longitude"], loc["name"], loc["country"]
    return None, None, None, None

    
def get_current_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        current = data.get("current", {})  # <-- correct key
        if current:
            return {
                "temperature": current.get("temperature_2m"),
                "feels_like": current.get("apparent_temperature"),
                "humidity": current.get("relative_humidity_2m"),
                "precipitation": current.get("precipitation"),
                "wind_speed": current.get("wind_speed_10m"),
                "weather_code": current.get("weather_code"),
                "time": current.get("time")
            }
    return None

def get_daily_forecast(lat,lon):
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_max,temperature_2m_min")
    response = requests.get(url)
    if response.status_code == 200:
        data=response.json()
        daily = data.get("daily", {})
        return {
            "dates": daily.get("time", []),
            "weather_code": daily.get("weather_code", []),
            "temp_max": daily.get("temperature_2m_max", []),
            "temp_min": daily.get("temperature_2m_min", []),
        }
    else:
        return None
        
def get_hourly_forecast(lat,lon):
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=,temperature_2m,weather_code")
    response = requests.get(url)
    if response.status_code == 200:
        data=response.json()
        daily = data.get("hourly", {})
        return {
            "dates": daily.get("time", []),
            "weather_code": daily.get("weather_code", []),
            "temp_max": daily.get("temperature_2m", [])
        }
    else:
        return None
    
    

