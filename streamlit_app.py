import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# --- CSS FOR EDGE-TO-EDGE BUTTONS ---
st.markdown("""
    <style>
    /* Force every button to be full width */
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

# --- DATA LOADING ---
def load_inventory():
    # Replace the dict below with your actual Google Sheets connection code
    # This ensures your categories are pulled dynamically
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

# Extract unique categories from the product data
# This ensures that if you add a new category to your sheet, it shows up automatically
categories = sorted(list(set(p["category"] for p in products.values())))

# --- SESSION STATE ---
if 'selected_cat' not in st.session_state and categories:
    st.session_state['selected_cat'] = categories[0]

# --- APP UI ---
st.title("🖨️ Spazz Shack")

main_col1, main_col2 = st.columns([0.6, 0.4])

with main_col1:
    st.subheader("🛍️ Categories")
    
    # RENDER ALL CATEGORIES
    # This loop reads the 'categories' list created from your data
    for cat in categories:
        btn_type = "primary" if st.session_state.get('selected_cat') == cat else "secondary"
        if st.button(cat, key=f"btn_{cat}", type=btn_type):
            st.session_state['selected_cat'] = cat
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📦 Products")
    
    # RENDER FILTERED PRODUCTS
    sel_cat = st.session_state.get('selected_cat')
    if sel_cat:
        filtered_prods = [name for name, info in products.items() if info["category"] == sel_cat]
        for prod_name in filtered_prods:
            st.button(prod_name, key=f"prod_{prod_name}", use_container_width=True)

with main_col2:
    st.subheader("🛒 Checkout")
    st.write("Cart is empty.")
