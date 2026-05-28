from langchain.tools import tool
import requests


CITY_COORDINATES = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Goa": (15.2993, 74.1240),
    "Hyderabad": (17.3850, 78.4867),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Pune": (18.5204, 73.8567),
    "Jaipur": (26.9124, 75.7873)
}


# NORMAL FUNCTION
def get_weather(city):

    if city not in CITY_COORDINATES:
        return {"message": "City not found"}

    latitude, longitude = CITY_COORDINATES[city]

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&forecast_days=5"
        f"&timezone=auto"
    )

    response = requests.get(url)

    data = response.json()

    weather_report = []

    dates = data["daily"]["time"]
    max_temp = data["daily"]["temperature_2m_max"]
    min_temp = data["daily"]["temperature_2m_min"]

    for i in range(len(dates)):

        weather_report.append({
            "date": dates[i],
            "max_temp": max_temp[i],
            "min_temp": min_temp[i]
        })

    return weather_report


# LANGCHAIN TOOL
@tool
def weather_lookup_tool(city: str):
    """
    Get weather forecast
    for a city
    """

    result = get_weather(city)

    return str(result)