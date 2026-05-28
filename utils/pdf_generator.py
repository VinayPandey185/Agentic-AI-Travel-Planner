from reportlab.platypus import (
    SimpleDocTemplate,
    Spacer,
    Paragraph,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generate_travel_pdf(
    result,
    source_city,
    destination_city,
):
    """
    Generate Travel Plan PDF
    """

    file_name = "travel_plan.pdf"

    pdf = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    content = []

    # -------------------------
    # Title
    # -------------------------
    title = Paragraph(
        f"""
        <font size=20 color='gold'>
        AI Travel Plan
        </font>
        """,
        styles["Title"],
    )

    content.append(title)

    content.append(Spacer(1, 12))

    # -------------------------
    # Trip Summary
    # -------------------------
    content.append(
        Paragraph(
            "<b>Trip Summary</b>",
            styles["Heading2"],
        )
    )

    content.append(
        Paragraph(
            f"""
            {source_city}
            →
            {destination_city}
            <br/>
            {result['trip_summary']}
            """,
            styles["BodyText"],
        )
    )

    content.append(Spacer(1, 10))

    # -------------------------
    # Flight Details
    # -------------------------
    content.append(
        Paragraph(
            "<b>Flight Details</b>",
            styles["Heading2"],
        )
    )

    content.append(
        Paragraph(
            f"""
            Airline:
            {result['departure_flight']['airline']}
            <br/>
            Departure:
            {result['departure_flight']['departure']}
            <br/>
            Arrival:
            {result['departure_flight']['arrival']}
            <br/>
            Price:
            ₹{result['departure_flight']['price']}
            """,
            styles["BodyText"],
        )
    )

    # -------------------------
    # Hotel
    # -------------------------
    content.append(
        Paragraph(
            "<b>Hotel Details</b>",
            styles["Heading2"],
        )
    )

    content.append(
        Paragraph(
            f"""
            Hotel:
            {result['hotel']['name']}
            <br/>
            Stars:
            {result['hotel']['stars']}
            <br/>
            Price/Night:
            ₹{result['hotel']['price_per_night']}
            """,
            styles["BodyText"],
        )
    )

    # -------------------------
    # Itinerary
    # -------------------------
    content.append(
        Paragraph(
            "<b>Travel Itinerary</b>",
            styles["Heading2"],
        )
    )

    for item in result["itinerary"]:

        content.append(
            Paragraph(
                f"""
                Day
                {item['day']}:
                {item['activity']}
                """,
                styles["BodyText"],
            )
        )

    # -------------------------
    # Budget
    # -------------------------
    content.append(
        Paragraph(
            "<b>Budget Breakdown</b>",
            styles["Heading2"],
        )
    )

    budget = result["budget"]

    content.append(
        Paragraph(
            f"""
            Flight:
            ₹{budget['flight_cost']}
            <br/>
            Hotel:
            ₹{budget['hotel_cost']}
            <br/>
            Food:
            ₹{budget['food_cost']}
            <br/>
            Transport:
            ₹{budget['local_transport']}
            <br/>
            Activities:
            ₹{budget['activities_cost']}
            <br/>
            Total:
            ₹{budget['total_cost']}
            """,
            styles["BodyText"],
        )
    )

    # -------------------------
    # AI Insights
    # -------------------------
    content.append(
        Paragraph(
            "<b>AI Insights</b>",
            styles["Heading2"],
        )
    )

    content.append(
        Paragraph(
            result["reasoning"],
            styles["BodyText"],
        )
    )

    pdf.build(content)

    return file_name
