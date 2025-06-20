import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import math
import json

st.set_page_config(page_title="Lake Ramsey Route Selector", layout="wide")
st.title("🗺️ Lake Ramsey Sailing Route Builder")

# --- LOAD MAP IMAGE ---
map_img = Image.open("lake_ramsey_map.png")
canvas_width, canvas_height = map_img.size

# --- ISLAND LOCATIONS (pixel coordinates on the image) ---
with open("islands.json") as f:
    islands = json.load(f)  # Format: {"Island Name": [x_percent, y_percent]}

island_coords = {
    name: (int(p[0] * canvas_width), int(p[1] * canvas_height))
    for name, p in islands.items()
}

# --- SESSION STATE ---
if "route" not in st.session_state:
    st.session_state.route = []

# --- DRAWING ---
st.markdown("Click islands on the map to build your route. Use the reset button to clear.")
import numpy as np

canvas_result = st_canvas(
    fill_color="#eee",
    stroke_width=0,
    background_image=np.array(map_img),
    update_streamlit=True,
    height=canvas_height,
    width=canvas_width,
    drawing_mode="transform",
    key="lake-canvas"
)

# --- CLICK HANDLING ---
if canvas_result.json_data and "objects" in canvas_result.json_data:
    if len(canvas_result.json_data["objects"]) > 0:
        last = canvas_result.json_data["objects"][-1]
        x_click = last.get("left", 0)
        y_click = last.get("top", 0)

        for name, (x, y) in island_coords.items():
            if math.hypot(x - x_click, y - y_click) < 30 and name not in st.session_state.route:
                st.session_state.route.append(name)
                st.experimental_rerun()

# --- SHOW ROUTE ---
if st.session_state.route:
    st.subheader("📍 Selected Route")
    st.markdown(" → ".join(st.session_state.route))
    if st.button("Clear Route"):
        st.session_state.route = []
        st.experimental_rerun()
else:
    st.info("Click islands on the map to start building your route.")
