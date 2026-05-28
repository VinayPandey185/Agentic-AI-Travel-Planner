from reportlab.platypus import (
    SimpleDocTemplate,
    Spacer,
    Paragraph,
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_travel_pdf(
    result,
    source_city,
    destination_city,
):
    """
    Generate Travel Plan PDF
    """

    from reportlab.platypus import (
        SimpleDocTemplate,
        Spacer,
        Paragraph,
    )


from reportlab.lib.styles import (
    getSampleStyleSheet,
)
from datetime import datetime
import os


def generate_travel_pdf(
    result,
    source_city,
    destination_city,
):
    """
    Generate Travel Plan PDF
    """

    # -------------------------
    # Create folder automatically
    # -------------------------
    os.makedirs(
        "generated_trips",
        exist_ok=True,
    )

    # -------------------------
    # Dynamic File Name
    # -------------------------
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = (
        f"generated_trips/"
        f"trip_"
        f"{source_city}_"
        f"{destination_city}_"
        f"{timestamp}.pdf"
    )

    pdf = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    content = []

    pdf = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    content = []

    # -------------------------
    # Title
    # -------------------------
    title = Paragraph(
        """
        <font size="22" color="darkblue">
        <b>✈ AI Travel Plan</b>
        </font>
        """,
        styles["Title"],
    )

    content.append(title)

    content.append(Spacer(1, 15))

    # -------------------------
    # Trip Summary
    # -------------------------
    content.append(
        Paragraph(
            "Trip Summary",
            styles["Heading2"],
        )
    )

    trip_summary = (
        f"<b>Route:</b> "
        f"{source_city} → {destination_city}"
        f"<br/>"
        f"<b>Duration:</b> "
        f"{result['trip_summary']}"
    )

    content.append(
        Paragraph(
            trip_summary,
            styles["BodyText"],
        )
    )

    content.append(Spacer(1, 10))

    # -------------------------
    # Flight Details
    # -------------------------
    content.append(
        Paragraph(
            "Flight Details",
            styles["Heading2"],
        )
    )

    flight_details = (
        f"<b>Airline:</b> "
        f"{result['departure_flight']['airline']}"
        f"<br/>"
        f"<b>Departure:</b> "
        f"{result['departure_flight']['departure']}"
        f"<br/>"
        f"<b>Arrival:</b> "
        f"{result['departure_flight']['arrival']}"
        f"<br/>"
        f"<b>Price:</b> "
        f"Rs. {result['departure_flight']['price']:,}"
    )

    content.append(
        Paragraph(
            flight_details,
            styles["BodyText"],
        )
    )

    content.append(Spacer(1, 10))

    # -------------------------
    # Hotel Details
    # -------------------------
    content.append(
        Paragraph(
            "Hotel Details",
            styles["Heading2"],
        )
    )

    hotel_details = (
        f"<b>Hotel:</b> "
        f"{result['hotel']['name']}"
        f"<br/>"
        f"<b>Stars:</b> "
        f"{result['hotel']['stars']} Star"
        f"<br/>"
        f"<b>Price/Night:</b> "
        f"Rs. {result['hotel']['price_per_night']:,}"
    )

    content.append(
        Paragraph(
            hotel_details,
            styles["BodyText"],
        )
    )

    content.append(Spacer(1, 10))

    # -------------------------
    # Travel Itinerary
    # -------------------------
    content.append(
        Paragraph(
            "Travel Itinerary",
            styles["Heading2"],
        )
    )

    for item in result["itinerary"]:

        content.append(
            Paragraph(
                f"<b>Day {item['day']}:</b> " f"{item['activity']}",
                styles["BodyText"],
            )
        )

    content.append(Spacer(1, 10))

    # -------------------------
    # Budget Breakdown
    # -------------------------
    content.append(
        Paragraph(
            "Budget Breakdown",
            styles["Heading2"],
        )
    )

    budget = result["budget"]

    budget_text = (
        f"<b>Flight:</b> "
        f"Rs. {budget['flight_cost']:,}"
        f"<br/>"
        f"<b>Hotel:</b> "
        f"Rs. {budget['hotel_cost']:,}"
        f"<br/>"
        f"<b>Food:</b> "
        f"Rs. {budget['food_cost']:,}"
        f"<br/>"
        f"<b>Transport:</b> "
        f"Rs. {budget['local_transport']:,}"
        f"<br/>"
        f"<b>Activities:</b> "
        f"Rs. {budget['activities_cost']:,}"
        f"<br/><br/>"
        f"<font color='green'>"
        f"<b>Total Cost:</b> "
        f"Rs. {budget['total_cost']:,}"
        f"</font>"
    )

    content.append(
        Paragraph(
            budget_text,
            styles["BodyText"],
        )
    )

    content.append(Spacer(1, 10))

    # -------------------------
    # AI Insights
    # -------------------------
    content.append(
        Paragraph(
            "AI Insights",
            styles["Heading2"],
        )
    )

    ai_reasoning = result["reasoning"].replace("₹", "Rs. ")

    content.append(
        Paragraph(
            ai_reasoning,
            styles["BodyText"],
        )
    )

    pdf.build(content)

    return file_name
