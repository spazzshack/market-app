import streamlit as st
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# CSS to FORCE 3-wide uniformity and prevent layout shifting on any device
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
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DUMMY DATA FOR LAYOUT TESTING ---
# Once you add your 'Inventory' sheet, replace this with your actual connection logic
def load_inventory():
    return {
        "Toy Car": {"category": "Toys", "weight": 10, "target": 5},
        "Keychain": {"category": "Accessories", "weight": 2, "target": 2},
        "Vase": {"category": "Decor", "weight": 50, "target": 15},
        "Action Figure": {"category": "Toys", "weight": 20, "target": 10},
        "Earrings": {"category": "Accessories", "weight": 1, "target": 8},
        "Planter": {"category": "Decor", "weight": 100, "target": 20}
    }

products = load_inventory()

# Initialize State
if 'cart' not in st.session_state: st.session_state['cart'] = []
if 'selected_cat' not in st.session_state: st.session_state['selected_cat'] = None

st.title("🖨️ Spazz Shack")

# --- UI LAYOUT ---
main_col1, main_col2 = st.columns([0.6, 0.4])

with main_col1:
    st.markdown("### 🛍️ Quick-Add Inventory")
    
    # Get categories from our data
    categories = sorted(list(set(p["category"] for p in products.values())))
    
    if not st.session_state['selected_cat']: 
        st.session_state['selected_cat'] = categories[0]
        
    # CSS Grid Wrapper to force 3-wide layout
    st.markdown('<div class="category-grid">', unsafe_allow_html=True)
    for cat in categories:
        btn_type = "primary" if st.session_state['selected_cat'] == cat else "secondary"
        if st.button(cat, key=f"btn_{cat}", type=btn_type):
            st.session_state['selected_cat'] = cat
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display Products for the category
    sel_cat = st.session_state['selected_cat']
    filtered_prods = {k: v for k, v in products.items() if v["category"] == sel_cat}
    
    st.markdown("---")
    for prod_name in filtered_prods.keys():
        if st.button(prod_name, key=f"prod_{prod_name}", use_container_width=True):
            st.session_state['selected_product'] = prod_name

with main_col2:
    st.markdown("### 🛒 Checkout")
    st.write("Current Cart: Empty")
