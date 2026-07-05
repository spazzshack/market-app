import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# --- CSS FOR CENTERED GRID ---
st.markdown("""
    <style>
    .centered-grid {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 15px !important;
        width: 100% !important;
    }
    .grid-item {
        flex: 0 0 calc(45%) !important; /* 2-wide layout */
    }
    /* Style our custom buttons to look like Streamlit buttons */
    .custom-btn {
        display: block;
        width: 100%;
        padding: 10px;
        text-align: center;
        border: 1px solid #ccc;
        border-radius: 5px;
        text-decoration: none;
        color: black;
        background-color: #f0f2f6;
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

main_col1, main_col2 = st.columns([0.6, 0.4])

with main_col1:
    st.subheader("🛍️ Categories")
    
    # RENDER CENTERED CATEGORY BUTTONS
    st.markdown('<div class="centered-grid">', unsafe_allow_html=True)
    for cat in categories:
        # We use a query parameter hack to detect button clicks on HTML elements
        btn_class = "custom-btn"
        if st.session_state['selected_cat'] == cat:
            btn_class += " primary-style"
        
        # Link button to trigger a rerun with the selection
        if st.button(cat, key=f"cat_{cat}", use_container_width=True):
            st.session_state['selected_cat'] = cat
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.subheader("📦 Products")
    sel_cat = st.session_state['selected_cat']
    filtered_prods = [name for name, info in products.items() if info["category"] == sel_cat]
    for prod_name in filtered_prods:
        st.button(prod_name, key=f"prod_{prod_name}", use_container_width=True)

with main_col2:
    st.subheader("🛒 Checkout")
    st.write("Cart is empty.")
