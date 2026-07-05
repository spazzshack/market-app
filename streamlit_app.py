import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# --- CSS GRID: FORCES EVERYTHING TO BE CENTERED AND 3-WIDE ---
st.markdown("""
    <style>
    .main-grid {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 10px !important;
        width: 100% !important;
        margin: 0 auto !important;
    }
    div[data-testid="stButton"] {
        width: 100% !important;
    }
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

if 'selected_cat' not in st.session_state:
    st.session_state['selected_cat'] = categories[0]

st.title("🖨️ Spazz Shack")

# --- UI LAYOUT ---
main_col1, main_col2 = st.columns([0.6, 0.4])

with main_col1:
    st.subheader("🛍️ Categories")
    # Use the CSS grid for categories
    st.markdown('<div class="main-grid">', unsafe_allow_html=True)
    for cat in categories:
        btn_type = "primary" if st.session_state['selected_cat'] == cat else "secondary"
        if st.button(cat, key=f"btn_{cat}", type=btn_type):
            st.session_state['selected_cat'] = cat
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("📦 Products")
    # Use the same CSS grid for products to ensure alignment
    st.markdown('<div class="main-grid">', unsafe_allow_html=True)
    sel_cat = st.session_state['selected_cat']
    filtered_prods = [name for name, info in products.items() if info["category"] == sel_cat]
    for prod_name in filtered_prods:
        st.button(prod_name, key=f"prod_{prod_name}")
    st.markdown('</div>', unsafe_allow_html=True)

with main_col2:
    st.subheader("🛒 Checkout")
    st.write("Cart is empty.")
