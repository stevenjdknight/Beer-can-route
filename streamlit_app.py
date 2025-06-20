import streamlit as st
import json
from PIL import Image
import os

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

island_names = list(island_data.keys())

# --- SESSION STATE ---
if "selected" not in st.session_state:
    st.session_state.selected = []

# --- DISPLAY IMAGE ---
st.image(img, use_column_width=True)

# --- ISLAND SELECTION ---
st.subheader("🏝️ Island Options (up to 3 roundings each)")

cols = st.columns(4)
for i, name in enumerate(island_names):
    for j in range(1, 4):  # Allow 3 rounds per island
        label = f"{name} ({j})"
        with cols[i % 4]:
            if st.button(f"{'✅ ' if label in st.session_state.selected else ''}{label}", key=label):
                if label in st.session_state.selected:
                    st.session_state.selected.remove(label)
                else:
                    st.session_state.selected.append(label)

# --- DISPLAY ROUTE ---
if st.session_state.selected:
    st.markdown("### 📍 Selected Route")
    st.markdown(" → ".join(st.session_state.selected))
else:
    st.info("Click islands above to build your route.")

# --- RESET ---
if st.button("🔄 Clear Route"):
    st.session_state.selected = []
