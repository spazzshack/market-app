import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import base64
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# --- CSS FOR EDGE-TO-EDGE BUTTONS ---
st.markdown("""
    <style>
    /* Force every button to be full width and height consistent */
    div[data-testid="stButton"] {
        width: 100% !important;
        margin-bottom: 5px !important;
    }
    div[data-testid="stButton"] button {
        width: 100% !important;
        height: 50px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
# Ensure your google_creds.json is in your project folder
def load_inventory():
    try:
        # Example: Replace with your actual sheet logic
        # scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # creds = ServiceAccountCredentials.from_json_keyfile_name("google_creds.json", scope)
        # sheet = gspread.authorize(creds).open("3D Printing Market Sales").sheet1
        # data = sheet.get_all_records()
        # return {row['Product']: {'category': row['Category']} for row in data}
        
        # Fallback dummy data if sheet connection isn't active
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
    except:
        return {}

# Load data and get unique categories
products = load_inventory()
categories = sorted(list(set(p["category"] for p in products.values())))

# --- SESSION STATE ---
if 'selected_cat' not in st.session_state and categories:
    st.session_state['selected_cat'] = categories[0]

# --- APP UI ---
st.title("🖨️ Spazz Shack")

main_col1, main_col2 = st.columns([0.6, 0.4])

with main_col1:
    st.subheader("🛍️ Categories")
    
    # EDGE-TO-EDGE CATEGORY BUTTONS
    # No columns, just a direct loop. Every button will be 100% width.
    for cat in categories:
        btn_type = "primary" if st.session_state.get('selected_cat') == cat else "secondary"
        if st.button(cat, key=f"btn_{cat}", type=btn_type):
            st.session_state['selected_cat'] = cat
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📦 Products")
    
    # WIDE BUTTONS FOR PRODUCTS (Edge-to-edge)
    sel_cat = st.session_state.get('selected_cat')
    if sel_cat:
        filtered_prods = [name for name, info in products.items() if info["category"] == sel_cat]
        for prod_name in filtered_prods:
            st.button(prod_name, key=f"prod_{prod_name}", use_container_width=True)

with main_col2:
    st.subheader("🛒 Checkout")
    st.write("Cart is empty.")
