
import streamlit as st
import pandas as pd
from datetime import date, timedelta

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="TravelPilot AI ✈️",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ TravelPilot AI")
st.subheader("Intelligent Trip Planning & Disruption Management Agent")

st.markdown(
    "Plan, optimize and automatically rebuild your travel itinerary using AI."
)

# ----------------------------
# SIDEBAR INPUT
# ----------------------------
st.sidebar.header("🧳 Trip Details")

destination = st.sidebar.selectbox(
    "Destination",
    ["Ooty", "Goa", "Chennai", "Bangalore", "Munnar", "Coimbatore"]
)

start_date = st.sidebar.date_input("Start Date", date.today())
end_date = st.sidebar.date_input(
    "End Date", date.today() + timedelta(days=3)
)

budget = st.sidebar.slider("Budget (₹)", 5000, 50000, 15000, step=1000)

travelers = st.sidebar.number_input(
    "Number of Travellers", 1, 10, 2
)

interests = st.sidebar.multiselect(
    "Interests",
    ["Nature", "Adventure", "Food", "Shopping", "Photography", "Culture"],
    default=["Nature", "Photography"]
)

hotel_type = st.sidebar.radio(
    "Hotel Preference",
    ["Budget", "Standard", "Luxury"]
)

generate = st.sidebar.button("🚀 Generate My Trip")

# ----------------------------
# SAMPLE ITINERARY
# ----------------------------
sample_places = {
    "Ooty": [
        ("Botanical Garden", "9:00 AM", 200),
        ("Doddabetta Peak", "11:30 AM", 100),
        ("Tea Museum", "2:30 PM", 150),
        ("Ooty Lake", "5:30 PM", 250),
    ],
    "Goa": [
        ("Calangute Beach", "9:00 AM", 0),
        ("Fort Aguada", "11:30 AM", 50),
        ("Basilica of Bom Jesus", "2:00 PM", 0),
        ("Cruise Ride", "6:00 PM", 600),
    ],
    "Chennai": [
        ("Marina Beach", "7:30 AM", 0),
        ("Government Museum", "11:00 AM", 100),
        ("Kapaleeshwarar Temple", "3:00 PM", 0),
        ("Elliot Beach", "6:30 PM", 0),
    ],
    "Bangalore": [
        ("Lalbagh", "8:30 AM", 50),
        ("Cubbon Park", "11:00 AM", 0),
        ("Vidhana Soudha", "2:00 PM", 0),
        ("MG Road", "6:00 PM", 500),
    ],
    "Munnar": [
        ("Tea Garden", "9:00 AM", 100),
        ("Echo Point", "11:30 AM", 100),
        ("Mattupetty Dam", "3:00 PM", 150),
        ("Top Station", "5:30 PM", 150),
    ],
    "Coimbatore": [
        ("Marudamalai Temple", "8:00 AM", 0),
        ("VOC Park", "11:00 AM", 30),
        ("Gass Forest Museum", "2:00 PM", 50),
        ("Brookefields Mall", "6:00 PM", 500),
    ],
}

# ----------------------------
# GENERATE ITINERARY
# ----------------------------
if generate:

    days = (end_date - start_date).days + 1

    if days <= 0:
        st.error("End date should be after start date.")
        st.stop()

    st.success("✅ Personalized itinerary generated!")

    hotel_cost = {"Budget": 1200, "Standard": 2200, "Luxury": 4200}[hotel_type]
    food_cost = 600 * travelers
    transport_cost = 500 * travelers

    total_activity_cost = 0

    st.header("📅 Day-wise Itinerary")

    for i in range(days):

        trip_day = start_date + timedelta(days=i)

        st.subheader(f"Day {i+1} — {trip_day}")

        places = sample_places[destination]

        table = []

        for place, time, cost in places:
            table.append(
                {
                    "Time": time,
                    "Activity": place,
                    "Estimated Cost (₹)": cost,
                }
            )
            total_activity_cost += cost

        df = pd.DataFrame(table)
        st.dataframe(df, use_container_width=True)

    # ----------------------------
    # BUDGET
    # ----------------------------
    st.header("💰 Budget Dashboard")

    stay = hotel_cost * days
    food = food_cost * days
    transport = transport_cost * days

    total = stay + food + transport + total_activity_cost

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Hotel", f"₹{stay}")
    c2.metric("Food", f"₹{food}")
    c3.metric("Transport", f"₹{transport}")
    c4.metric("Activities", f"₹{total_activity_cost}")

    st.metric("Estimated Total Trip Cost", f"₹{total}")

    if total > budget:
        st.error(
            f"Budget exceeded by ₹{total-budget}"
        )
    else:
        st.success(
            f"Remaining Budget: ₹{budget-total}"
        )

    # ----------------------------
    # MAP SECTION
    # ----------------------------
    st.header("🗺️ Nearby Attractions")

    st.info(
        f"All selected attractions are optimized around **{destination}** to reduce travel time."
    )

    # ----------------------------
    # DISRUPTION AGENT
    # ----------------------------
    st.header("⚠️ Disruption Management Agent")

    disruption = st.selectbox(
        "Simulate a Travel Disruption",
        [
            "No Disruption",
            "🌧 Heavy Rain",
            "✈ Flight Delay",
            "🚫 Attraction Closed",
        ],
    )

    if disruption == "🌧 Heavy Rain":
        st.warning("Heavy rain detected tomorrow.")
        st.write("### AI Rebuilt Your Schedule")
        st.write("- Botanical Garden moved to Day 2 Morning.")
        st.write("- Tea Museum shifted to Morning.")
        st.write("- Chocolate Museum added as indoor activity.")

    elif disruption == "✈ Flight Delay":
        st.warning("Flight delayed by 2 hours.")
        st.write("### Updated Itinerary")
        st.write("- Hotel Check-in postponed.")
        st.write("- Evening sightseeing shifted to next morning.")

    elif disruption == "🚫 Attraction Closed":
        st.warning("Tea Museum is closed today.")
        st.write("### Nearby Alternatives")
        st.write("- Chocolate Factory")
        st.write("- Thread Garden")
        st.write("- Shopping Street")

    else:
        st.success("No disruptions detected.")

    # ----------------------------
    # AI CHATBOT
    # ----------------------------
    st.header("🤖 TravelPilot AI Assistant")

    question = st.text_input(
        "Ask your itinerary assistant",
        placeholder="Example: What should I do tomorrow morning?",
    )

    if question:

        q = question.lower()

        if "morning" in q:
            st.success(
                f"Tomorrow morning you should visit **{sample_places[destination][0][0]}** at **{sample_places[destination][0][1]}**."
            )

        elif "hotel" in q:
            st.success(
                f"Nearby hotel recommendations in {destination}: Green Valley Stay, Hill View Residency, Pine Woods Hotel."
            )

        elif "budget" in q:
            st.success(
                f"Estimated total spending is **₹{total}**."
            )

        elif "cancel" in q:
            st.success(
                "If a booking is cancelled, TravelPilot AI automatically rebuilds the day's itinerary and recommends nearby alternatives."
            )

        elif "close" in q:
            st.success(
                "Nearby attractions within 5 km: Rose Garden, Tea Factory, Local Market."
            )

        else:
            st.info(
                "TravelPilot AI suggests optimizing your schedule to reduce travel time and keep activities within budget."
            )

    # ----------------------------
    # BACKUP PLAN
    # ----------------------------
    st.header("🛡️ Backup Travel Options")

    st.write(
        """
- Indoor Attractions
- Local Cafés
- Shopping Streets
- Museums
- Weather-safe Activities
"""
    )

    # ----------------------------
    # CHECKLIST
    # ----------------------------
    st.header("🎒 Packing Checklist")

    checklist = [
        "Identity Card",
        "Power Bank",
        "Phone Charger",
        "Medicines",
        "Water Bottle",
        "Umbrella",
        "Camera",
    ]

    for item in checklist:
        st.checkbox(item)

    # ----------------------------
    # IMPORTANT TIMINGS
    # ----------------------------
    st.header("⏰ Important Timings")

    st.table(
        pd.DataFrame(
            {
                "Event": [
                    "Hotel Check-in",
                    "Breakfast",
                    "Lunch",
                    "Dinner",
                    "Hotel Check-out",
                ],
                "Time": [
                    "2:00 PM",
                    "8:00 AM",
                    "1:00 PM",
                    "8:00 PM",
                    "11:00 AM",
                ],
            }
        )
    )

    st.success("🎉 Your intelligent travel dashboard is ready!")

else:
    st.info("Enter trip details from the sidebar and click **Generate My Trip**.")