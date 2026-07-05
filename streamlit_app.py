import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import base64
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# --- CSS FOR UNIFORM BUTTONS ---
st.markdown("""
    <style>
    /* Force all buttons to be the same height for consistency */
    div[data-testid="stButton"] button {
        height: 50px !important;
        width: 100% !important;
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
    
    # 3-WIDE GRID FOR CATEGORIES
    # This loop forces 3 buttons per row, perfectly centered.
    for i in range(0, len(categories), 3):
        row = categories[i:i+3]
        # Create columns based on how many items are in the row
        cols = st.columns(3)
        for idx, cat in enumerate(row):
            with cols[idx]:
                btn_type = "primary" if st.session_state['selected_cat'] == cat else "secondary"
                if st.button(cat, key=f"btn_{cat}", type=btn_type):
                    st.session_state['selected_cat'] = cat
                    st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True) # Small gap
    st.subheader("📦 Products")
    
    # WIDE BUTTONS FOR PRODUCTS (One per line)
    sel_cat = st.session_state['selected_cat']
    filtered_prods = [name for name, info in products.items() if info["category"] == sel_cat]
    
    for prod_name in filtered_prods:
        st.button(prod_name, key=f"prod_{prod_name}", use_container_width=True)

with main_col2:
    st.subheader("🛒 Checkout")
    st.write("Cart is empty.")
