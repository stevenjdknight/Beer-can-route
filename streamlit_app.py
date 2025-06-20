import streamlit as st
import json
from PIL import Image, ImageDraw

# --- CONFIG ---
st.set_page_config(page_title="🏝️ Lake Ramsey Route Selector", layout="wide")
st.title("🧭 Lake Ramsey Sailing Route Planner")

st.markdown("""
Select a sequence of islands by clicking on them in the image below. Your selections will be highlighted and logged in order.

We'll use this to:
- Estimate total course distance
- Automatically route around islands/land
- Log safe water tracks based on known contours
""")

# --- LOAD IMAGE & ISLAND DATA ---
img = Image.open("lake_ramsey_map.png")

with open("islands.json", "r") as f:
    island_data = json.load(f)

# --- CONFIGURATION ---
single_round_only = {"Norway Island", "Berry Island", "Galliard, Bass & Pike Island", "Swansea Island", "Ida Island"}
max_roundings = 3

# --- SESSION STATE ---
if "selected" not in st.session_state:
    st.session_state.selected = []

# --- FUNCTION: Get pixel coordinates ---
def get_xy(island_key):
    base_name = island_key.split(" (")[0]
    if base_name not in island_data:
        return None
    x_pct, y_pct = island_data[base_name]
    width, height = img.size
    return int(x_pct * width), int(y_pct * height)

# --- DRAWING MAP WITH ROUTE ---
img_drawn = img.copy()
draw = ImageDraw.Draw(img_drawn)

route_points = []
for island in st.session_state.selected:
    xy = get_xy(island)
    if xy:
        route_points.append(xy)
        draw.ellipse((xy[0] - 6, xy[1] - 6, xy[0] + 6, xy[1] + 6), fill="red")

if len(route_points) >= 2:
    draw.line(route_points, fill="red", width=3)

st.image(img_drawn, use_container_width=True)

# --- ISLAND OPTIONS UI ---
st.markdown("### 🏝️ Island Options – click on the islands in the order of rounding (up to 3 roundings each)")
cols = st.columns(4)

for i, name in enumerate(island_data.keys()):
    count = sum(1 for s in st.session_state.selected if s.startswith(name))
    max_count = 1 if name in single_round_only else max_roundings
    for j in range(max_count):
        label = f"{name}" if max_count == 1 else f"{name} ({j+1})"
        selected_label = f"✅ {label}" if label in st.session_state.selected else label
        with cols[i % 4]:
            if st.button(selected_label, key=f"{label}"):
                if label in st.session_state.selected:
                    st.session_state.selected.remove(label)
                else:
                    st.session_state.selected.append(label)

# --- DISPLAY ROUTE ---
if st.session_state.selected:
    st.markdown("### 📍 Selected Route")
    st.markdown(" → ".join(st.session_state.selected))

# --- RESET BUTTON ---
if st.button("🔄 Clear Route"):
    st.session_state.selected = []
    st.experimental_rerun()
