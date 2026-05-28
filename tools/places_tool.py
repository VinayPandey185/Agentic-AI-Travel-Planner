from langchain.tools import tool
from utils.helper import load_json


# -------------------------
# NORMAL FUNCTION
# -------------------------
def recommend_places(
    city,
    preferences="",
    min_rating=4.0,
):
    """
    Recommend tourist places
    based on city +
    travel preference
    """

    places = load_json("data/places.json")

    matching_places = []

    # Clean preference
    preferences = preferences.strip().lower()

    for place in places:

        city_match = place["city"].lower() == city.lower()

        rating_match = place["rating"] >= min_rating

        place_type = place.get("type", "").lower()

        # Preference Match
        preference_match = not preferences or preferences in place_type

        if city_match and rating_match and preference_match:

            matching_places.append(place)

    # -------------------------
    # Fallback
    # -------------------------
    if not matching_places:

        for place in places:

            if place["city"].lower() == city.lower() and place["rating"] >= min_rating:

                matching_places.append(place)

    # No places found
    if not matching_places:

        return {"message": "No places found"}

    # Sort by rating
    recommended_places = sorted(
        matching_places,
        key=lambda x: x["rating"],
        reverse=True,
    )

    return recommended_places[:5]


# -------------------------
# LANGCHAIN TOOL
# -------------------------
@tool
def places_discovery_tool(
    city: str,
    preferences: str = "",
):
    """
    Recommend tourist places
    in a city based on
    user preference
    """

    result = recommend_places(
        city,
        preferences,
    )

    return str(result)
