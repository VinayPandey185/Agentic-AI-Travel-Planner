from langchain.tools import tool
from utils.helper import load_json


# NORMAL FUNCTION
def recommend_hotel(
    city,
    min_stars=3,
    max_price=5000
):
    """
    Recommend hotel based on city,
    stars and budget
    """

    hotels = load_json("data/hotels.json")

    matching_hotels = []

    for hotel in hotels:

        if (
            hotel["city"].lower() == city.lower()
            and hotel["stars"] >= min_stars
            and hotel["price_per_night"] <= max_price
        ):

            matching_hotels.append(hotel)

    # fallback if no hotel found
    if not matching_hotels:

        fallback_hotels = [
            hotel for hotel in hotels
            if hotel["city"].lower() == city.lower()
        ]

        if fallback_hotels:

            return min(
                fallback_hotels,
                key=lambda x: x["price_per_night"]
            )

        return {"message": "No hotels found"}

    best_hotel = sorted(
        matching_hotels,
        key=lambda x: (
            -x["stars"],
            x["price_per_night"]
        )
    )[0]

    return best_hotel


# LANGCHAIN TOOL
@tool
def hotel_recommendation_tool(city: str):
    """
    Recommend best affordable hotel
    in a city
    """

    result = recommend_hotel(city)

    return str(result)