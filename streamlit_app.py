import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import base64
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# --- CSS FOR CENTERED GRID ---
st.markdown("""
    <style>
    /* This container forces 2 items per row and centers the whole block */
    .centered-grid {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 10px !important;
        width: 100% !important;
        margin-bottom: 20px !important;
    }
    /* Each item takes ~50% width (minus gap) to make it 2-wide */
    .centered-grid > div {
        flex: 0 0 calc(50% - 10px) !important;
    }
    /* Buttons forced to fill their space */
    div[data-testid="stButton"] button {
        width: 100% !important;
        height: 50px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DUMMY DATA ---
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
categories = sorted(list(set(p["category"] for p in products.values())))

# --- SESSION STATE ---
if 'selected_cat' not in st.session_state:
    st.session_state['selected_cat'] = categories[0]

# --- APP UI ---
st.title("🖨️ Spazz Shack")

main_col1, main_col2 = st.columns([0.6, 0.4])

with main_col1:
    st.subheader("🛍️ Categories")
    
    # WRAPPER FOR CENTERED GRID
    st.markdown('<div class="centered-grid">', unsafe_allow_html=True)
    for cat in categories:
        # We need a small container per button so the flex-grid can handle it
        st.markdown('<div>', unsafe_allow_html=True)
        btn_type = "primary" if st.session_state['selected_cat'] == cat else "secondary"
        if st.button(cat, key=f"btn_{cat}", type=btn_type):
            st.session_state['selected_cat'] = cat
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("📦 Products")
    sel_cat = st.session_state['selected_cat']
    filtered_prods = [name for name, info in products.items() if info["category"] == sel_cat]
    
    for prod_name in filtered_prods:
        st.button(prod_name, key=f"prod_{prod_name}", use_container_width=True)

with main_col2:
    st.subheader("🛒 Checkout")
    st.write("Cart is empty.")
    
