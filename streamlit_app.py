import streamlit as st
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# ... (Keep your existing path and background logic here) ...
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(SCRIPT_DIR, "static", "logo.png")

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

image_code = get_base64_image(IMAGE_PATH)

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(15, 23, 42, 0.90), rgba(15, 23, 42, 0.90)), 
                    url("data:image/png;base64,{image_code}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    h1, h2, h3, p, div {{ color: white !important; }}
    
    /* --- CUSTOM BUTTON STYLING FOR RADIO --- */
    div[role="radiogroup"] > label {{
        background-color: rgba(255, 255, 255, 0.1);
        padding: 10px 20px;
        border-radius: 20px;
        margin-right: 10px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        cursor: pointer;
    }}
    div[role="radiogroup"] > label:hover {{
        background-color: rgba(255, 255, 255, 0.2);
    }}
    /* Hide the little radio dots */
    div[role="radiogroup"] input[type="radio"] {{
        display: none;
    }}
    </style>
""", unsafe_allow_html=True)

# ... (Keep your connection and load_inventory functions here) ...

# --- UI LAYOUT ---
st.title("🖨️ Spazz Shack")

main_col1, main_col2 = st.columns([4, 3], gap="large")

with main_col1:
    st.markdown("### 🛍️ Quick-Add Inventory")
    all_prods = load_inventory()
    categories = sorted(list(set(p["category"] for p in all_prods.values())))
    
    # This radio group now uses our custom CSS styling
    selected_cat = st.radio(
        "Filter by Category", 
        categories, 
        horizontal=True,
        label_visibility="collapsed"
    )
    
    filtered_prods = {k: v for k, v in all_prods.items() if v["category"] == selected_cat}
    
    cols = st.columns(3)
    for i, prod_name in enumerate(filtered_prods.keys()):
        if cols[i % 3].button(prod_name, use_container_width=True):
            st.session_state['selected_product'] = prod_name
# ... (Rest of your existing checkout/add-to-cart logic) ...
