from langchain.tools import tool


# -------------------------
# NORMAL FUNCTION
# -------------------------
def estimate_budget(
    flight_price,
    hotel_price_per_night,
    total_days,
    food_expense_per_day=500,
    transport_expense_per_day=300,
    activities_expense_per_day=700,
):
    """
    Estimate realistic travel budget
    """

    # -------------------------
    # Cost Calculation
    # -------------------------
    hotel_cost = hotel_price_per_night * total_days

    food_cost = food_expense_per_day * total_days

    transport_cost = transport_expense_per_day * total_days

    activities_cost = activities_expense_per_day * total_days

    total_budget = (
        flight_price + hotel_cost + food_cost + transport_cost + activities_cost
    )

    # -------------------------
    # Return Budget Data
    # -------------------------
    return {
        "flight_cost": flight_price,
        "hotel_cost": hotel_cost,
        "food_cost": food_cost,
        "local_transport": transport_cost,
        "activities_cost": activities_cost,
        "total_cost": total_budget,
    }


# -------------------------
# LANGCHAIN TOOL
# -------------------------
@tool
def budget_estimation_tool(
    flight_price: float,
    hotel_price_per_night: float,
    total_days: int,
):
    """
    Estimate total travel budget
    """

    result = estimate_budget(
        flight_price,
        hotel_price_per_night,
        total_days,
    )

    return str(result)
