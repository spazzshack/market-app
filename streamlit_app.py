import streamlit as st
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# CSS to force the grid and button uniformity
st.markdown("""
    <style>
    /* 1. Define the grid container */
    .category-grid {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 10px !important;
        width: 100% !important;
    }
    
    /* 2. Force buttons inside the grid to match cell size */
    .category-grid div[data-testid="stButton"] {
        width: 100% !important;
    }
    
    .category-grid div[data-testid="stButton"] button {
        width: 100% !important;
        height: 50px !important;
        font-size: 14px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def connect_to_google_sheets():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("google_creds.json", scope)
        return gspread.authorize(creds).open("3D Printing Market Sales")
    except: return None

wb = connect_to_google_sheets()

# --- LOAD INVENTORY ---
@st.cache_data(ttl=60)
def load_inventory():
    if not wb: return {}
    data = wb.worksheet("Inventory").get_all_records()
    return {item["Product"]: {
        "category": item.get("Category", "General"),
        "weight": float(item.get("Weight", 0) or 0),
        "time": float(item.get("Time", 0) or 0),
        "labor": float(item.get("Labor", 0) or 0),
        "comp": float(item.get("Component Cost", 0) or 0),
        "target": float(item.get("Target Price", 0) or 0)
    } for item in data}

products = load_inventory()
if 'cart' not in st.session_state: st.session_state['cart'] = []
if 'selected_cat' not in st.session_state: st.session_state['selected_cat'] = None

# --- UI LAYOUT ---
st.title("🖨️ Spazz Shack")
main_col1, main_col2 = st.columns([0.6, 0.4])

with main_col1:
    st.markdown("### 🛍️ Quick-Add Inventory")
    
    categories = sorted(list(set(p["category"] for p in products.values())))
    if not st.session_state['selected_cat']: st.session_state['selected_cat'] = categories[0]
        
    # Inject the grid container
    st.markdown('<div class="category-grid">', unsafe_allow_html=True)
    for cat in categories:
        if st.button(cat, key=f"btn_{cat}", type="primary" if st.session_state['selected_cat'] == cat else "secondary"):
            st.session_state['selected_cat'] = cat
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Products
    sel_cat = st.session_state['selected_cat']
    filtered_prods = {k: v for k, v in products.items() if v["category"] == sel_cat}
    
    # Product display list
    for prod in filtered_prods.keys():
        if st.button(prod, key=f"prod_{prod}"):
            st.session_state['selected_product'] = prod
            
    # ... (Keep existing product details logic below here)
