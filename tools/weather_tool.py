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
    "Jaipur": (26.9124, 75.7873),
    "Patna": (25.5941, 85.1376),
    "Lucknow": (26.8467, 80.9462),
    "Ahmedabad": (23.0225, 72.5714),
    "Surat": (21.1702, 72.8311),
    "Chandigarh": (30.7333, 76.7794),
    "Amritsar": (31.6340, 74.8723),
    "Varanasi": (25.3176, 82.9739),
    "Haridwar": (29.9457, 78.1642),
    "Rishikesh": (30.0869, 78.2676),
    "Kochi": (9.9312, 76.2673),
    "Mysore": (12.2958, 76.6394),
    "Shimla": (31.1048, 77.1734),
    "Manali": (32.2432, 77.1892),
    "Udaipur": (24.5854, 73.7125),
    "Jodhpur": (26.2389, 73.0243),
    "Nagpur": (21.1458, 79.0882),
    "Indore": (22.7196, 75.8577),
    "Bhopal": (23.2599, 77.4126),
}


# NORMAL FUNCTION
def get_weather(city):

    city = city.strip().title()
    if city not in CITY_COORDINATES:
        city = "Delhi"

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

        weather_report.append(
            {"date": dates[i], "max_temp": max_temp[i], "min_temp": min_temp[i]}
        )

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
