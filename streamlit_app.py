import streamlit as st
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# CSS to FORCE 3-wide uniformity
st.markdown("""
    <style>
    /* Force 3 columns, ignore screen size */
    .category-container {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 10px !important;
        width: 100% !important;
    }
    /* Force buttons to fill their cell and keep uniform height */
    .category-container button {
        width: 100% !important;
        height: 50px !important;
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def connect_to_google_sheets():
    try:
        # Use your existing logic
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("google_creds.json", scope)
        return gspread.authorize(creds).open("3D Printing Market Sales")
    except: return None

wb = connect_to_google_sheets()

@st.cache_data(ttl=60)
def load_inventory():
    if not wb: return {}
    data = wb.worksheet("Inventory").get_all_records()
    return {item["Product"]: {
        "category": item.get("Category", "General"),
        "weight": float(item.get("Weight", 0) or 0),
        "target": float(item.get("Target Price", 0) or 0)
    } for item in data}

products = load_inventory()

if 'cart' not in st.session_state: st.session_state['cart'] = []
if 'selected_cat' not in st.session_state: st.session_state['selected_cat'] = None

st.title("🖨️ Spazz Shack")

# --- UI LAYOUT ---
main_col1, main_col2 = st.columns([0.6, 0.4])

with main_col1:
    st.markdown("### 🛍️ Quick-Add Inventory")
    
    categories = sorted(list(set(p["category"] for p in products.values())))
    
    # SAFETY CHECK: Prevent IndexError
    if not categories:
        st.warning("No categories found. Check your Google Sheet data.")
    else:
        if not st.session_state['selected_cat']: 
            st.session_state['selected_cat'] = categories[0]
            
        # Manually create the CSS container
        st.markdown('<div class="category-container">', unsafe_allow_html=True)
        for cat in categories:
            # Buttons are now inside the CSS grid
            if st.button(cat, key=f"btn_{cat}", type="primary" if st.session_state['selected_cat'] == cat else "secondary"):
                st.session_state['selected_cat'] = cat
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
