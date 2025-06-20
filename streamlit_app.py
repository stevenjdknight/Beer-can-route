import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

st.set_page_config(page_title="Lake Route Selector", layout="wide")
st.title("📍 BCS Route Builder - Lake Ramsey")

# Island coordinates: (lat, lon)
islands = {
    "Potter Island": (46.4564, -80.9457),
    "Swiss Island": (46.4582, -80.9495),
    "McCrea Island": (46.4601, -80.9520),
    "Norway Island": (46.4642, -80.9531),
    "Berry Island": (46.4674, -80.9488),
    "Swansea Island": (46.4665, -80.9405),
    "Galliard, Bass & Pike Island": (46.4708, -80.9369),
    "Gull Rock": (46.4682, -80.9302),
    "Snug": (46.4656, -80.9265),
    "Spooky": (46.4632, -80.9241),
    "Ida Island": (46.4591, -80.9282),
}

# Persistent session state
if "route" not in st.session_state:
    st.session_state.route = []

# Build map
lake_center = (46.463, -80.940)
m = folium.Map(location=lake_center, zoom_start=14, tiles="CartoDB positron")

# Draw markers and route
for name, coord in islands.items():
    folium.Marker(coord, tooltip=name, popup=name).add_to(m)

# Draw polyline for route
if len(st.session_state.route) > 1:
    folium.PolyLine([islands[pt] for pt in st.session_state.route], color="blue", weight=3).add_to(m)

# Calculate total distance
if len(st.session_state.route) > 1:
    distance_km = 0.0
    for i in range(len(st.session_state.route) - 1):
        p1 = islands[st.session_state.route[i]]
        p2 = islands[st.session_state.route[i+1]]
        distance_km += geodesic(p1, p2).km
    st.markdown(f"### 🧭 Estimated Distance: `{distance_km:.2f} km`")

# Click-based interaction
st.markdown("#### 🏝️ Select Islands (Click to Add to Route)")
clicked = st_folium(m, width=900, height=600)

if clicked and clicked.get("last_object_clicked_tooltip"):
    name = clicked["last_object_clicked_tooltip"]
    if name not in st.session_state.route:
        st.session_state.route.append(name)
        st.rerun()

# Show current route
if st.session_state.route:
    st.success(f"Route: {' → '.join(st.session_state.route)}")
    if st.button("Reset Route"):
        st.session_state.route = []
        st.rerun()
else:
    st.info("Click an island to begin plotting your route.")
