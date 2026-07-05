import streamlit as st
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# CSS to FORCE 3-wide uniformity and prevent layout shifting
st.markdown("""
    <style>
    /* Force 3 columns, ignore screen size */
    .category-grid {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 10px !important;
        width: 100% !important;
    }
    /* Force buttons to fill their cell and keep uniform height */
    div[data-testid="stButton"] {
        width: 100% !important;
    }
    div[data-testid="stButton"] button {
        width: 100% !important;
        height: 50px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def connect_to_google_sheets():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # Ensure your google_creds.json is in the same folder as the script
        creds = ServiceAccountCredentials.from_json_keyfile_name("google_creds.json", scope)
        client = gspread.authorize(creds)
        return client.open("3D Printing Market Sales")
    except Exception as e:
        return None

wb = connect_to_google_sheets()

@st.cache_data(ttl=60)
def load_inventory():
    if not wb: return {}
    try:
        sheet = wb.worksheet("Inventory")
        data = sheet.get_all_records()
        return {item["Product"]: {
            "category": item.get("Category", "General"),
            "weight": float(item.get("Weight", 0) or 0),
            "target": float(item.get("Target Price", 0) or 0)
        } for item in data}
    except Exception as e:
        return {}

products = load_inventory()

# Initialize State
if 'cart' not in st.session_state: st.session_state['cart'] = []
if 'selected_cat' not in st.session_state: st.session_state['selected_cat'] = None

st.title("🖨️ Spazz Shack")

# --- UI LAYOUT ---
main_col1, main_col2 = st.columns([0.6, 0.4])

with main_col1:
    st.markdown("### 🛍️ Quick-Add Inventory")
    
    categories = sorted(list(set(p["category"] for p in products.values())))
    
    if not categories:
        st.error("No data found in 'Inventory' sheet. Check your tab name and headers.")
    else:
        if not st.session_state['selected_cat']: 
            st.session_state['selected_cat'] = categories[0]
            
        # CSS Grid Wrapper
        st.markdown('<div class="category-grid">', unsafe_allow_html=True)
        for cat in categories:
            btn_type = "primary" if st.session_state['selected_cat'] == cat else "secondary"
            if st.button(cat, key=f"btn_{cat}", type=btn_type):
                st.session_state['selected_cat'] = cat
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with main_col2:
    st.markdown("### 🛒 Checkout")
    st.write("Cart is empty.")
