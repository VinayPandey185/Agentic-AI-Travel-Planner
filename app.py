import streamlit as st
from agent.langchain_agent import ask_travel_agent
from datetime import (
    datetime,
    time,
    timedelta,
)
import time
from utils.pdf_generator import generate_travel_pdf

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")


# -------------------------
# Premium CSS
# -------------------------
st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #0F172A,
        #111827,
        #1E293B
    );
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0B1120;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Hero */
.hero {
    background: linear-gradient(
        135deg,
        rgba(255,215,0,0.2),
        rgba(255,255,255,0.05)
    );

    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 30px;
    padding: 35px;
    margin-bottom: 30px;
}

/* Glass cards */
.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    border-radius: 25px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

/* KPI cards */
.metric-card {
    background: linear-gradient(
        135deg,
        #111827,
        #1F2937
    );

    border-radius: 25px;
    padding: 25px;
    text-align: center;
    border: 1px solid rgba(255,215,0,0.2);
}

.metric-number {
    font-size: 32px;
    font-weight: 700;
    color: gold;
}

.metric-text {
    color: #CBD5E1;
    font-size: 15px;
}

/* Section title */
.section-title {
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 20px;
    color: gold;
}

/* Generate Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(
        90deg,
        #FFD700,
        #F59E0B
    );

    color: black;
    border-radius: 18px;
    height: 60px;
    font-size: 20px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    transform: scale(1.02);
    transition: 0.3s;
}

</style>
""",
    unsafe_allow_html=True,
)


# -------------------------
# HERO
# -------------------------
st.markdown(
    """
<div class="hero">
<h1>✈️ AI Travel<span style="color:#FFD700;"> Planner</span></h1>
<p>
Plan luxurious trips using Agentic AI,
weather intelligence, itinerary planning,
budget optimization and premium experiences.
</p>
</div>
""",
    unsafe_allow_html=True,
)


# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.image(
    "assets/ai-trip-planner.png",
    width=220,
)

st.sidebar.markdown(
    """
    <h3 style="
    text-align:left;
    color:#E5E7EB;
    margin-top:8px;
    margin-bottom:15px;
    font-weight:600;
    padding-left:5px;
    ">
    ✨ Plan with AI
    </h3>
    """,
    unsafe_allow_html=True,
)

source_city = st.sidebar.text_input("Source Location", placeholder="Enter source city")

destination_city = st.sidebar.text_input(
    "Destination", placeholder="Enter destination city"
)

total_days = st.sidebar.slider("Trip Duration", 1, 10, 5)

budget = st.sidebar.number_input(
    "Budget ₹", min_value=5000, max_value=100000, value=25000, step=1000
)

preferences = st.sidebar.text_area(
    "Travel Preferences", placeholder="Nightlife, luxury, beaches..."
)

generate = st.sidebar.button("✨ Generate Premium Plan")


# -------------------------
# GENERATE
# -------------------------
if generate:

    if not source_city or not destination_city:

        st.warning("Please enter both cities.")

    else:

        # Premium Loading Box
        loading_box = st.empty()

        loading_messages = [
            "✈️ Finding best flights...",
            "🏨 Searching premium hotels...",
            "🌤 Checking weather forecast...",
            "📍 Planning itinerary...",
            "💰 Optimizing budget...",
            "🧠 AI generating insights...",
        ]

        # Show loading steps
        for msg in loading_messages:

            loading_box.info(msg)

            time.sleep(0.7)

        # Final spinner
        with st.spinner("Creating luxury itinerary..."):

            result = ask_travel_agent(
                source_city=source_city,
                destination_city=destination_city,
                total_days=total_days,
                budget=budget,
                preferences=preferences,
            )

        # Remove loading box
        loading_box.empty()

        # -------------------------
        # Error Handling
        # -------------------------
        if "error" in result:
            st.error(result["error"])
            st.stop()

        # -------------------------
        # Success Message
        # -------------------------
        st.success("✨ Premium travel plan generated!")

        # -------------------------
        # KPI Cards
        # -------------------------
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-number">
                ₹{budget:,}
                </div>
                <div class="metric-text">
                Total Budget
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-number">
                {total_days}
                </div>
                <div class="metric-text">
                Days
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                f"""
            <div class="metric-card">
                <div class="metric-number">
                📍
                </div>
                <div class="metric-text">
                {destination_city}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # -------------------------
        # Flight + Hotel
        # -------------------------
        left, right = st.columns(2)

        departure_date = datetime.now().strftime("%Y-%m-%d")

        return_date = (datetime.now() + timedelta(days=total_days)).strftime("%Y-%m-%d")

        # -------------------------
        # Flight Details
        # -------------------------
        with left:
            st.markdown(
                f"""
                <div class="card"
                style="
                min-height:320px;
                display:flex;
                flex-direction:column;
                justify-content:space-between;
                ">

                <div>

                <div class="section-title">
                ✈️ Flight Details
                </div>

                <b>Airline:</b>
                {result['departure_flight']['airline']}<br>

                <b>Departure:</b>
                {result['departure_flight']['departure']}<br>

                <b>Arrival:</b>
                {result['departure_flight']['arrival']}<br>

                <b>Price:</b>
                ₹{result['departure_flight']['price']}

                </div>

                <div style="margin-top:20px;">

                <a href="https://www.google.com/travel/flights?q=flights+from+{source_city.replace(' ', '+')}+to+{destination_city.replace(' ', '+')}+on+{departure_date}+return+{return_date}"
                target="_blank"
                style="
                display:inline-block;
                padding:12px 18px;
                background:#FFD700;
                color:black;
                text-decoration:none;
                border-radius:12px;
                font-weight:bold;
                box-shadow:
                0px 4px 12px
                rgba(255,215,0,0.25);
                ">
                ✈️ Book Flight
                </a>

                </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        # -------------------------
        # Hotel Details
        # -------------------------
        with right:
            st.markdown(
                f"""
                <div class="card"
                style="
                min-height:320px;
                display:flex;
                flex-direction:column;
                justify-content:space-between;
                ">

                <div>

                <div class="section-title">
                🏨 Hotel Details
                </div>

                <b>Hotel:</b>
                {result['hotel']['name']}<br>

                <b>Stars:</b>
                ⭐ {result['hotel']['stars']}<br>

                <b>Price/Night:</b>
                ₹{result['hotel']['price_per_night']}<br>

                <b>Amenities:</b>
                {", ".join(result['hotel'] ['amenities'])}

                </div>

                <div style="margin-top:20px;">

                <a href="https://www.google.com/travel/hotels?q=hotels+in+{destination_city.replace(' ', '+')}+on+{departure_date}+return+{return_date}"
                target="_blank"
                style="
                display:inline-block;
                padding:12px 18px;
                background:#FFD700;
                color:black;
                text-decoration:none;
                border-radius:12px;
                font-weight:bold;
                box-shadow:
                0px 4px 12px
                rgba(255,215,0,0.25);
                ">
                🏨 Book Hotel
                </a>

                </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        # -------------------------
        # Weather
        # -------------------------
        st.markdown(
            """
            <div class="section-title">
            🌤 Weather Forecast
            </div>
            """,
            unsafe_allow_html=True,
        )

        cols = st.columns(len(result["weather"]))

        for i, weather in enumerate(result["weather"]):

            with cols[i]:
                st.markdown(
                    f"""
                    <div class="card">

                    <b>
                    📅
                    {weather['date']}
                    </b>
                    <br><br>
                    🌡 <b>Max:</b>
                    {weather['max_temp']}°C
                    <br>
                    ❄ <b>Min:</b>
                    {weather['min_temp']}°C

                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        # -------------------------
        # Itinerary
        # -------------------------
        st.markdown(
            """
            <div class="section-title">
            📅 Travel Itinerary
            </div>
            """,
            unsafe_allow_html=True,
        )

        for item in result["itinerary"]:

            st.markdown(
                f"""
                <div class="card"
                style="
                margin-bottom:20px;
                border-left:5px solid #FFD700;
                padding:22px;
                transition:0.3s ease;
                ">

                <h4 style="
                margin-bottom:10px;
                color:#FFD700;
                font-weight:700;
                ">
                ✨ Day {item['day']} Experience
                </h4>

                <h3 style="
                margin-bottom:10px;
                font-size:22px;
                ">
                📍 {item['activity']}
                </h3>

                <p style="
                font-size:18px;
                font-weight:bold;
                color:#FFD700;
                margin-top:10px;
                margin-bottom:15px;
                ">
                {item.get('place_name', '')}
                </p>

                <p>
                📌 <b>Location:</b>
                {item.get('location', 'N/A')}
                </p>

                <p>
                🏛 <b>Category:</b>
                {item.get('type', 'Tourist Place')}
                </p>

                <p>
                ⭐ <b>Rating:</b>
                {item.get('rating', '4.5')}
                </p>

                <a href="{item.get('maps_link', '#')}"
                target="_blank"
                style="
                display:inline-block;
                margin-top:15px;
                padding:12px 18px;
                background:#FFD700;
                color:black;
                text-decoration:none;
                border-radius:12px;
                font-weight:bold;
                font-size:15px;
                box-shadow:
                0px 4px 12px
                rgba(255,215,0,0.25);
                ">
                🗺 Open in Maps
                </a>

                </div>
                """,
                unsafe_allow_html=True,
            )

        # -------------------------
        # Budget
        # -------------------------
        st.markdown(
            """
            <div class="section-title">
            💰 Budget Breakdown
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Budget Columns
        cols = st.columns(6)

        budget_data = result["budget"]

        data = [
            ("✈ Flight", budget_data["flight_cost"]),
            ("🏨 Hotel", budget_data["hotel_cost"]),
            ("🍽 Food", budget_data["food_cost"]),
            ("🚕 Transport", budget_data["local_transport"]),
            ("🎡 Activities", budget_data["activities_cost"]),
            ("💰 Total", budget_data["total_cost"]),
        ]

        # -------------------------
        # Budget Cards
        # -------------------------
        for col, item in zip(cols, data):

            with col:

                st.markdown(
                    f"""
                    <div style="
                    background:linear-gradient(
                        135deg,
                        #111827,
                        #1F2937
                    );
                    border-radius:25px;
                    padding:25px 15px;
                    text-align:center;
                    border:1px solid
                    rgba(255,215,0,0.2);
                    min-height:140px;
                    display:flex;
                    flex-direction:column;
                    justify-content:center;
                    ">

                    <div style="
                    font-size:30px;
                    font-weight:700;
                    color:gold;
                    margin-bottom:12px;
                    ">
                    ₹{item[1]:,}
                    </div>

                    <div style="
                    color:#CBD5E1;
                    font-size:15px;
                    font-weight:500;
                    ">
                    {item[0]}
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # -------------------------
        # Smart Budget Status
        # -------------------------
        remaining_budget = budget - budget_data["total_cost"]

        st.markdown(
            "<br>",
            unsafe_allow_html=True,
        )

        if remaining_budget >= 0:

            budget_status_html = f"""
            <div style="background:linear-gradient(
                135deg,
                #0f9d58,
                #34a853
            );
            padding:20px;
            border-radius:20px;
            color:white;
            text-align:center;
            font-size:24px;
            font-weight:bold;
            margin-top:10px;
            box-shadow:
            0px 8px 20px
            rgba(0,0,0,0.2);
            ">
            💰 Smart Budget Plan
            <br>
            Saved ₹{remaining_budget:,}
            </div>
            """

        else:

            budget_status_html = f"""
            <div style="
            background:
            linear-gradient(
                135deg,
                #d93025,
                #ea4335
            );
            padding:20px;
            border-radius:20px;
            color:white;
            text-align:center;
            font-size:24px;
            font-weight:bold;
            margin-top:10px;
            box-shadow:
            0px 8px 20px
            rgba(0,0,0,0.2);
            ">
            ⚠ Budget Exceeded
            <br>
            Extra ₹{abs(remaining_budget):,}
            Needed
            </div>
            """

        st.markdown(
            budget_status_html,
            unsafe_allow_html=True,
        )
        # -------------------------
        # AI Insights
        # -------------------------
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="section-title">
            💡 AI Insights
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="card">
            {result['reasoning']}
            </div>
            """,
            unsafe_allow_html=True,
        )
        # -------------------------
        # Download PDF
        # -------------------------
        st.markdown(
            "<br>",
            unsafe_allow_html=True,
        )

        pdf_file = generate_travel_pdf(
            result,
            source_city,
            destination_city,
        )

        with open(
            pdf_file,
            "rb",
        ) as pdf:

            st.download_button(
                label="📄 Download Travel Plan PDF",
                data=pdf,
                file_name="travel_plan.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
