import streamlit as st
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# --- CSS for 3-Wide Grid ---
st.markdown("""
    <style>
    /* Styling for our manual category buttons */
    .cat-btn {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 10px;
        width: 100%;
        text-align: center;
        color: white;
        margin-bottom: 10px;
    }
    .cat-btn:hover { background-color: rgba(255, 255, 255, 0.2); }
    </style>
""", unsafe_allow_html=True)

# --- LOAD INVENTORY ---
@st.cache_data(ttl=60)
def load_inventory():
    # ... (Keep your existing connection logic here) ...
    pass

products = load_inventory()
all_prods = products

# --- UI LAYOUT ---
st.title("🖨️ Spazz Shack")

# Lock the columns to prevent jumping
main_col1, main_col2 = st.columns([0.6, 0.4])

with main_col1:
    st.markdown("### 🛍️ Quick-Add Inventory")
    
    # --- MANUAL 3-WIDE CATEGORY GRID ---
    categories = sorted(list(set(p["category"] for p in all_prods.values())))
    
    # Create the grid rows
    for i in range(0, len(categories), 3):
        row = st.columns(3)
        for j in range(3):
            if i + j < len(categories):
                cat = categories[i+j]
                if row[j].button(cat, use_container_width=True):
                    st.session_state['selected_cat'] = cat
    
    selected_cat = st.session_state.get('selected_cat', categories[0] if categories else None)
    
    # Now show products for the selected category
    if selected_cat:
        filtered_prods = {k: v for k, v in all_prods.items() if v["category"] == selected_cat}
        # ... (Rest of your product selection logic) ...

with main_col2:
    # --- CHECKOUT ---
    st.markdown("### 🛒 Checkout")
    # ... (Keep your existing checkout logic) ...
