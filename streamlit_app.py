import streamlit as st
import json
from PIL import Image, ImageDraw
import os

# --- CONFIG ---
st.set_page_config(page_title="Lake Ramsey Route Selector", layout="wide")
st.title("🗺️ Lake Ramsey Course Selector")

# --- LOAD MAP IMAGE ---
MAP_IMAGE_PATH = "lake_ramsey_map.png"  # Use the full lake map with contours and island positions
ISLANDS_JSON_PATH = "islands.json"

# Load and resize image
if not os.path.exists(MAP_IMAGE_PATH):
    st.error("Map image file not found. Please upload 'lake_ramsey_map.png' to the app directory.")
    st.stop()

image = Image.open(MAP_IMAGE_PATH)
image_width, image_height = image.size

# Load island data
if not os.path.exists(ISLANDS_JSON_PATH):
    st.error("Island data file not found. Please upload 'islands.json' to the app directory.")
    st.stop()

with open(ISLANDS_JSON_PATH, 'r') as f:
    islands = json.load(f)

# Convert island coords from percentages to pixels
island_coords = {
    name: (int(x * image_width), int(y * image_height))
    for name, (x, y) in islands.items()
}

# Session state to hold route
if "route" not in st.session_state:
    st.session_state.route = []

# --- SHOW MAP AND HANDLE CLICKS ---
st.subheader("Click on islands to build your race route")
clicked = st.image(image, use_column_width=True)

# Display legend and instructions
st.markdown("""
- Each click should match an island on the map.
- Route is built in the order of clicks.
- Galliard, Bass & Pike are treated as one point due to shallow water.
- Route will auto-snap to island centers (safe navigation).
""")

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🔁 Reset Route"):
        st.session_state.route = []

with col2:
    if st.button("✅ Finalize Route") and st.session_state.route:
        st.success("Route submitted!")
        st.json(st.session_state.route)

# --- DRAW ROUTE ON IMAGE ---
overlay = image.copy()
draw = ImageDraw.Draw(overlay)

# Draw island points and names
for name, (x, y) in island_coords.items():
    draw.ellipse((x-6, y-6, x+6, y+6), fill="red")
    draw.text((x+8, y-8), name, fill="white")

# Draw route
for i in range(1, len(st.session_state.route)):
    p1 = island_coords[st.session_state.route[i-1]]
    p2 = island_coords[st.session_state.route[i]]
    draw.line([p1, p2], fill="yellow", width=3)

# Display updated image
st.image(overlay, use_column_width=True)

# --- CLICK SIMULATION (DEV ONLY) ---
# Ideally, we'd use a click detector. For now, dropdown selection mimics user action.
selected = st.selectbox("Select island to add to route", [""] + list(island_coords.keys()))
if selected and selected not in st.session_state.route:
    st.session_state.route.append(selected)
    st.rerun()
