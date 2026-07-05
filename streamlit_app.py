import streamlit as st
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# --- DUMMY DATA FOR LAYOUT TESTING ---
# This allows the app to run immediately. Replace this with your 
# Google Sheets logic once the sheet is ready.
def load_inventory():
    return {
        "Toy Car": {"category": "Toys", "weight": 10, "target": 5},
        "Keychain": {"category": "Accessories", "weight": 2, "target": 2},
        "Vase": {"category": "Decor", "weight": 50, "target": 15},
        "Action Figure": {"category": "Toys", "weight": 20, "target": 10},
        "Earrings": {"category": "Accessories", "weight": 1, "target": 8},
        "Planter": {"category": "Decor", "weight": 100, "target": 20},
        "Dinosaur": {"category": "Toys", "weight": 30, "target": 12}
    }

products = load_inventory()
# Extract unique categories
categories = sorted(list(set(p["category"] for p in products.values())))

# Initialize State
if 'selected_cat' not in st.session_state:
    st.session_state['selected_cat'] = categories[0]
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

st.title("🖨️ Spazz Shack")

# --- UI LAYOUT ---
main_col1, main_col2 = st.columns([0.6, 0.4])

with main_col1:
    st.markdown("### 🛍️ Quick-Add Inventory")
    
    # MANUAL 3-COLUMN LOOP
    # This divides categories into rows of 3 to force uniform alignment
    for i in range(0, len(categories), 3):
        row_categories = categories[i:i+3]
        cols = st.columns(3)
        for idx, cat in enumerate(row_categories):
            with cols[idx]:
                btn_type = "primary" if st.session_state['selected_cat'] == cat else "secondary"
                if st.button(cat, key=f"btn_{cat}", use_container_width=True, type=btn_type):
                    st.session_state['selected_cat'] = cat
                    st.rerun()

    st.markdown("---")
    
    # Display Products for the selected category
    sel_cat = st.session_state['selected_cat']
    filtered_prods = [name for name, info in products.items() if info["category"] == sel_cat]
    
    for prod_name in filtered_prods:
        if st.button(prod_name, key=f"prod_{prod_name}", use_container_width=True):
            st.session_state['selected_product'] = prod_name

with main_col2:
    st.markdown("### 🛒 Checkout")
    st.write("Cart is empty.")
