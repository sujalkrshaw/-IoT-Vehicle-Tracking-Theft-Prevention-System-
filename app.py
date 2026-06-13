import streamlit as st
import pandas as pd
import time
import os
import folium
from streamlit_folium import st_folium
from datetime import datetime
from alerts.telegram_alert import send_alert
from firebase.firebase_handler import upload_vehicle_data


from vehicle_simulator import VehicleSimulator
from geofence import is_outside_geofence
from report_generator import create_pdf
os.makedirs("reports", exist_ok=True)
import os


# ------------------------
# Setup
# ------------------------

st.set_page_config(
    page_title="Vehicle Tracking System",
    layout="wide"
)

st.markdown("""
# 🚗 IoT Vehicle Tracking & Theft Prevention System
### Real-Time GPS Tracking | Geofencing | Theft Detection
""")

simulator = VehicleSimulator()

LOG_FILE = "data/vehicle_logs.csv"

os.makedirs("data", exist_ok=True)

if not os.path.exists(LOG_FILE):

    df = pd.DataFrame(
        columns=[
            "Timestamp",
            "Latitude",
            "Longitude",
            "Status",
            "Google Maps"
        ]
    )

    df.to_csv(LOG_FILE, index=False)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Vehicle", "ACTIVE")
col2.metric("Status", "SAFE")
col3.metric("Alerts", "0")
col4.metric("Mode", "TRACKING")

# ------------------------
# Buttons
# ------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Vehicle Status", "SAFE")
logs = pd.read_csv(LOG_FILE)

total_logs = len(logs)

total_alerts = len(
    logs[logs["Status"] == "THEFT ALERT"]
)

col2.metric("Total Logs", total_logs)
col3.metric("Alerts", total_alerts)
col4.metric("Tracking Mode", "ACTIVE")

col1, col2 = st.columns(2)

col1, col2, col3 = st.columns(3)

start = col1.button("▶ Start Tracking")
simulate_theft = col2.button("🚨 Simulate Theft")
generate_report = col3.button("📄 Generate PDF")

if start or simulate_theft:

    st.write("Tracking Started")

    status_placeholder = st.empty()

    map_placeholder = st.empty()

    table_placeholder = st.empty()

    for _ in range(50):

        gps = simulator.move()

        lat = gps["latitude"]
        lon = gps["longitude"]

        if simulate_theft:
            lat += 0.01
            lon += 0.01

        alert = is_outside_geofence(
            lat,
            lon
        )

        st.write("Alert Status:", alert)

        status = "SAFE"

        alert_sent = False

        if alert:

             status = "THEFT ALERT"

             st.error("🚨 THEFT DETECTED!")

             message = f"""
                 🚨 VEHICLE THEFT ALERT

                  Latitude: {lat}
                  Longitude: {lon}

            Google Maps:
                 https://www.google.com/maps?q={lat},{lon}
            """

        

        maps_url = (
            f"https://www.google.com/maps?q={lat},{lon}"
        )

        row = {
            "Timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            "Latitude": lat,
            "Longitude": lon,
            "Status": status,
            "Google Maps": maps_url
        }

         

        upload_vehicle_data(
          {
            "timestamp": row["Timestamp"],
            "latitude": lat,
            "longitude": lon,
            "status": status,
            "google_maps": maps_url
          }
        )

        pd.DataFrame([row]).to_csv(
            LOG_FILE,
            mode="a",
            header=False,
            index=False
        )

        status_placeholder.metric(
            "Vehicle Status",
            status
        )

        st.markdown(
             f"[📍 Open in Google Maps]({maps_url})"
        )

        st.info(
            f"Latitude: {lat} | Longitude: {lon}"
        )

        if status == "THEFT ALERT":
            st.error(
                 "🚨 THEFT DETECTED: Vehicle Left Safe Zone!"
            )

            


        map_df = pd.DataFrame(
            {
                "lat": [lat],
                "lon": [lon]
            }
        )

        map_placeholder.map(map_df)

        logs = pd.read_csv(LOG_FILE)

        total_logs = len(logs)

        total_alerts = len(
            logs[logs["Status"] == "THEFT ALERT"]
        )

        st.sidebar.metric(
              "Total Logs",
               total_logs
        )

        st.sidebar.metric(
             "Total Alerts",
             total_alerts
        )

        table_placeholder.dataframe(
            logs.tail(10)
        )

        time.sleep(1)

st.subheader("Location History")

if os.path.exists(LOG_FILE):
    history = pd.read_csv(LOG_FILE)

    st.subheader("🗺 Vehicle Route History")

if len(history) > 1:

    center_lat = history["Latitude"].iloc[-1]
    center_lon = history["Longitude"].iloc[-1]

    route_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=15
    )

    route_points = []

    for _, row in history.iterrows():

        route_points.append(
            [row["Latitude"], row["Longitude"]]
        )

    folium.PolyLine(
        route_points,
        weight=5,
        color="blue"
    ).add_to(route_map)

    folium.Marker(
        route_points[0],
        tooltip="Start"
    ).add_to(route_map)

    folium.Marker(
        route_points[-1],
        tooltip="Current Location"
    ).add_to(route_map)

    st_folium(
        route_map,
        width=1200,
        height=500
    )

    chart_data = pd.DataFrame({
          "Tracking Records": range(
           1,
           len(history) + 1
          )
    })

    st.subheader("📈 Tracking Activity")

    st.line_chart(chart_data)

    st.dataframe(history.tail(20))

chart_df = pd.DataFrame({
    "Logs": range(1, len(logs) + 1)
})

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Records",
    len(history)
)

col2.metric(
    "Safe Events",
    len(
        history[
            history["Status"] == "SAFE"
        ]
    )
)

col3.metric(
    "Theft Events",
    len(
        history[
            history["Status"] == "THEFT ALERT"
        ]
    )
)

st.line_chart(chart_df)    

if generate_report:

    create_pdf(
        LOG_FILE,
        "reports/Vehicle_Report.pdf"
    )

    st.success(
        "PDF Report Generated!"
    )

if os.path.exists(
    "reports/Vehicle_Report.pdf"
):

    with open(
        "reports/Vehicle_Report.pdf",
        "rb"
    ) as pdf:

        st.download_button(
            "📄 Download PDF Report",
            pdf,
            file_name="Vehicle_Report.pdf",
            mime="application/pdf"
        )    
with open(LOG_FILE, "rb") as file:

    st.download_button(
        label="⬇ Download CSV Report",
        data=file,
        file_name="vehicle_logs.csv",
        mime="text/csv"
    )    

