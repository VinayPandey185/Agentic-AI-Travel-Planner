from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import create_agent
from datetime import datetime

from tools.flight_tool import flight_search_tool, search_flights

from tools.hotel_tool import hotel_recommendation_tool, recommend_hotel

from tools.places_tool import places_discovery_tool, recommend_places

from tools.weather_tool import weather_lookup_tool, get_weather

from tools.budget_tool import estimate_budget

load_dotenv()


# -------------------------
# LLM
# -------------------------
llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)


# -------------------------
# LangChain Tools
# -------------------------
tools = [
    flight_search_tool,
    hotel_recommendation_tool,
    places_discovery_tool,
    weather_lookup_tool,
]


# -------------------------
# Agent
# -------------------------
travel_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
    You are an intelligent
    AI Travel Planner.
    Generate clean,
    professional and
    structured travel
    itineraries.
    """,
)


def ask_travel_agent(source_city, destination_city, total_days, budget, preferences=""):
    """
    Agentic AI Travel Planner
    """

    # -------------------------
    # Departure Flight
    # -------------------------
    flight = search_flights(source_city, destination_city)

    # -------------------------
    # Safety Check
    # -------------------------
    if "price" not in flight:
        return {
            "error": f"❌ No flight found "
            f"from {source_city} "
            f"to {destination_city}."
        }

    # -------------------------
    # Budget-aware Hotel Logic
    # -------------------------
    remaining_budget = (
        budget
        - flight["price"]
        - (total_days * 500)  # food
        - (total_days * 300)  # transport
        - (total_days * 700)  # activities
    )
    hotel_budget = remaining_budget // total_days

    hotel = recommend_hotel(destination_city, max_price=hotel_budget)

    # -------------------------
    # Places
    # -------------------------
    places = recommend_places(destination_city, preferences)

    # -------------------------
    # Places Safety Check
    # -------------------------
    if not isinstance(places, list) or len(places) == 0:

        places = [{"name": "City Tour", "type": "Tourist Place", "rating": 4.5}]
    # -------------------------
    # Weather
    # -------------------------
    weather = get_weather(destination_city)

    # Safety check
    if not isinstance(weather, list):
        weather = []
    # -------------------------
    # Budget Calculation
    # -------------------------
    budget_data = estimate_budget(
        flight_price=flight["price"],
        hotel_price_per_night=hotel["price_per_night"],
        total_days=total_days,
        food_expense_per_day=500,
        transport_expense_per_day=300,
        activities_expense_per_day=700,
    )

    # -------------------------
    # Flight Time Formatting
    # -------------------------
    departure_time = datetime.fromisoformat(flight["departure_time"]).strftime(
        "%I:%M %p"
    )

    arrival_time = datetime.fromisoformat(flight["arrival_time"]).strftime("%I:%M %p")

    # -------------------------
    # Itinerary Generation
    # -------------------------
    itinerary = []

    for day in range(total_days):

        # -------------------------
        # Day 1 Arrival
        # -------------------------
        if day == 0:

            itinerary.append(
                {
                    "day": day + 1,
                    "activity": f"Arrival in "
                    f"{destination_city} "
                    f"+ Visit "
                    f"{places[0]['name']}",
                    "place_name": places[0]["name"],
                    "location": destination_city,
                    "type": (
                        "Fort"
                        if "fort" in places[0]["name"].lower()
                        else (
                            "Museum"
                            if "museum" in places[0]["name"].lower()
                            else (
                                "Temple"
                                if "temple" in places[0]["name"].lower()
                                else places[0].get("type", "Tourist Place").title()
                            )
                        )
                    ),
                    "rating": places[0].get("rating", 4.5),
                    "maps_link": f"https://www.google.com/maps/search/"
                    f"{places[0]['name']}+"
                    f"{destination_city}",
                }
            )

        # -------------------------
        # Tourist Places
        # -------------------------
        elif day < len(places):

            itinerary.append(
                {
                    "day": day + 1,
                    "activity": f"Visit " f"{places[day]['name']}",
                    "place_name": places[day]["name"],
                    "location": destination_city,
                    "type": (
                        "Fort"
                        if "fort" in places[day]["name"].lower()
                        else (
                            "Museum"
                            if "museum" in places[day]["name"].lower()
                            else (
                                "Temple"
                                if "temple" in places[day]["name"].lower()
                                else (
                                    "Lake"
                                    if "lake" in places[day]["name"].lower()
                                    else places[day]
                                    .get("type", "Tourist Place")
                                    .title()
                                )
                            )
                        )
                    ),
                    "rating": places[day].get("rating", 4.5),
                    "maps_link": f"https://www.google.com/maps/search/"
                    f"{places[day]['name']}+"
                    f"{destination_city}",
                }
            )
        # -------------------------
        # Relax Day
        # -------------------------
        else:

            itinerary.append(
                {
                    "day": day + 1,
                    "activity": "Explore local market "
                    "and prepare for return journey",
                    "place_name": "Local Market",
                    "location": destination_city,
                    "type": "Shopping",
                    "rating": 4.5,
                    "maps_link": f"https://www.google.com/maps/search/"
                    f"local+market+"
                    f"{destination_city}",
                }
            )

    # -------------------------
    # AI Reasoning
    # -------------------------
    reasoning_prompt = f"""
    Explain briefly why these
    travel recommendations
    were selected.

    Departure Flight:
    {flight}

    Hotel:
    {hotel}

    Places:
    {places}

    Preferences:
    {preferences}

    Budget:
    ₹{budget}
    """

    response = travel_agent.invoke(
        {"messages": [{"role": "user", "content": reasoning_prompt}]}
    )

    reasoning = response["messages"][-1].content

    # -------------------------
    # Return Structured Data
    # -------------------------
    return {
        "trip_summary": f"{total_days}-Day "
        f"Trip from "
        f"{source_city} "
        f"to "
        f"{destination_city}",
        "departure_flight": {
            "airline": flight["airline"],
            "price": flight["price"],
            "departure": departure_time,
            "arrival": arrival_time,
        },
        "hotel": {
            "name": hotel["name"],
            "stars": hotel["stars"],
            "price_per_night": hotel["price_per_night"],
            "amenities": hotel["amenities"],
        },
        "weather": weather[:total_days] if weather else [],
        "itinerary": itinerary,
        "budget": budget_data,
        "reasoning": reasoning,
    }
