import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import base64
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# --- CSS FOR GRID ALIGNMENT ---
st.markdown("""
    <style>
    /* Force consistent button sizing */
    div[data-testid="stButton"] {
        width: 100% !important;
    }
    div[data-testid="stButton"] button {
        width: 100% !important;
        height: 50px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DUMMY DATA FOR LAYOUT TESTING ---
# Replace this with your Google Sheets connection once ready
def load_inventory():
    return {
        "Toy Car": {"category": "Toys"},
        "Keychain": {"category": "Accessories"},
        "Vase": {"category": "Decor"},
        "Action Figure": {"category": "Toys"},
        "Earrings": {"category": "Accessories"},
        "Planter": {"category": "Decor"},
        "Dinosaur": {"category": "Toys"},
        "Ring": {"category": "Accessories"},
        "Bowl": {"category": "Decor"}
    }

products = load_inventory()
# Get all categories
categories = sorted(list(set(p["category"] for p in products.values())))

# Initialize State
if 'selected_cat' not in st.session_state:
    st.session_state['selected_cat'] = categories[0]

st.title("🖨️ Spazz Shack")

# --- UI LAYOUT ---
main_col1, main_col2 = st.columns([0.6, 0.4])

with main_col1:
    st.markdown("### 🛍️ Quick-Add Inventory")
    
    # MANUAL 3-COLUMN LAYOUT
    # We break the categories into chunks of 3 to force a perfect 3-wide grid
    for i in range(0, len(categories), 3):
        row = categories[i:i+3]
        cols = st.columns(3)
        for idx, cat in enumerate(row):
            with cols[idx]:
                btn_type = "primary" if st.session_state['selected_cat'] == cat else "secondary"
                if st.button(cat, key=f"btn_{cat}", type=btn_type):
                    st.session_state['selected_cat'] = cat
                    st.rerun()
    
    # Products list
    st.subheader("Products")
    sel_cat = st.session_state['selected_cat']
    filtered_prods = [name for name, info in products.items() if info["category"] == sel_cat]
    
    for prod_name in filtered_prods:
        st.button(prod_name, key=f"prod_{prod_name}", use_container_width=True)

with main_col2:
    st.markdown("### 🛒 Checkout")
    st.write("Cart is empty.")
