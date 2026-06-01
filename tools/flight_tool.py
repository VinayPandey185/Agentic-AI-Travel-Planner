from langchain.tools import tool
from utils.helper import load_json
from datetime import datetime


# -------------------------
# Calculate Flight Duration
# -------------------------
def calculate_duration(departure_time, arrival_time):
    """
    Calculate flight duration
    """

    departure = datetime.fromisoformat(departure_time)

    arrival = datetime.fromisoformat(arrival_time)

    duration = arrival - departure

    return duration.total_seconds() / 3600


# -------------------------
# NORMAL FUNCTION
# -------------------------
def search_flights(from_city, to_city, preference="cheapest"):
    """
    Search flights
    """

    flights = load_json("data/flights.json")

    matching_flights = []

    # -------------------------
    # Clean user input
    # -------------------------
    from_city = from_city.strip().lower().split(",")[0]

    to_city = to_city.strip().lower().split(",")[0]

    for flight in flights:

        flight_from = flight.get("from", "").strip().lower()

        flight_to = flight.get("to", "").strip().lower()

        # -------------------------
        # Flexible Matching
        # -------------------------
        if (
            from_city in flight_from
            or flight_from in from_city
            or from_city == flight_from
        ) and (to_city in flight_to or flight_to in to_city or to_city == flight_to):

            flight["duration"] = calculate_duration(
                flight["departure_time"], flight["arrival_time"]
            )

            matching_flights.append(flight)

    # -------------------------
    # No Flights Found
    # -------------------------
    if not matching_flights:

        return {
            "flight_id": "DEFAULT001",
            "airline": "IndiGo",
            "from": from_city.title(),
            "to": to_city.title(),
            "departure_time": "2025-08-01T09:00:00",
            "arrival_time": "2025-08-01T11:00:00",
            "price": 4500,
            "duration": 2.0,
            "is_fallback": True,
        }

    # -------------------------
    # Cheapest Flight
    # -------------------------
    if preference == "cheapest":

        best_flight = min(matching_flights, key=lambda x: x["price"])

    # -------------------------
    # Fastest Flight
    # -------------------------
    else:

        best_flight = min(matching_flights, key=lambda x: x["duration"])

    return best_flight


# -------------------------
# LANGCHAIN TOOL
# -------------------------
@tool
def flight_search_tool(from_city: str, to_city: str):
    """
    Search cheapest flight
    between source and
    destination
    """

    result = search_flights(from_city, to_city)

    return str(result)
