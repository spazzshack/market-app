import streamlit as st
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# --- CSS FOR PERFECT 3-WIDE GRID ---
st.markdown("""
    <style>
    /* This container forces 3 equal columns regardless of screen size */
    .category-grid {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 10px !important;
        width: 100% !important;
        margin-bottom: 20px;
    }
    /* Force buttons to fill their grid cells */
    div[data-testid="stButton"] {
        width: 100% !important;
    }
    div[data-testid="stButton"] button {
        width: 100% !important;
        height: 50px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DUMMY DATA FOR LAYOUT TESTING ---
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

# --- STATE ---
if 'selected_cat' not in st.session_state: 
    categories = sorted(list(set(p["category"] for p in products.values())))
    st.session_state['selected_cat'] = categories[0]

st.title("🖨️ Spazz Shack")

# --- UI LAYOUT ---
# We keep the main columns here, but we put the grid directly inside main_col1
main_col1, main_col2 = st.columns([0.6, 0.4])

with main_col1:
    st.markdown("### 🛍️ Quick-Add Inventory")
    
    # Render the 3-wide Grid
    categories = sorted(list(set(p["category"] for p in products.values())))
    st.markdown('<div class="category-grid">', unsafe_allow_html=True)
    for cat in categories:
        btn_type = "primary" if st.session_state['selected_cat'] == cat else "secondary"
        if st.button(cat, key=f"btn_{cat}", type=btn_type):
            st.session_state['selected_cat'] = cat
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Products
    st.markdown("---")
    sel_cat = st.session_state['selected_cat']
    filtered_prods = {k: v for k, v in products.items() if v["category"] == sel_cat}
    
    # Just list the products for the category
    for prod_name in filtered_prods.keys():
        st.button(prod_name, key=f"prod_{prod_name}", use_container_width=True)

with main_col2:
    st.markdown("### 🛒 Checkout")
    st.write("Cart is ready for items.")
