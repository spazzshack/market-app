import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# --- CSS FOR EDGE-TO-EDGE BUTTONS ---
st.markdown("""
    <style>
    div[data-testid="stButton"] { width: 100% !important; margin-bottom: 5px !important; }
    div[data-testid="stButton"] button { width: 100% !important; height: 50px !important; }
    </style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
def get_inventory():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("google_creds.json", scope)
        client = gspread.authorize(creds)
        # Change "3D Printing Market Sales" if your sheet name is different
        sheet = client.open("3D Printing Market Sales").sheet1 
        data = sheet.get_all_records()
        # This maps the Sheet data. Ensure your headers are 'Product' and 'Category'
        return {row['Product']: {'category': row['Category']} for row in data}
    except Exception as e:
        # If this runs, check your terminal for the exact error (e.g., file not found)
        st.error(f"Could not load data from Google Sheets: {e}")
        return {}

# Load live data
products = get_inventory()
# This creates the category list directly from your live sheet data
categories = sorted(list(set(p["category"] for p in products.values())))

# --- SESSION STATE ---
if 'selected_cat' not in st.session_state and categories:
    st.session_state['selected_cat'] = categories[0]

# --- APP UI ---
st.title("🖨️ Spazz Shack")

col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.subheader("🛍️ Categories")
    
    if not categories:
        st.info("Waiting for data from Google Sheets...")
    
    # RENDER CATEGORIES EDGE-TO-EDGE
    for cat in categories:
        btn_type = "primary" if st.session_state.get('selected_cat') == cat else "secondary"
        if st.button(cat, key=f"btn_{cat}", type=btn_type):
            st.session_state['selected_cat'] = cat
            st.rerun()
            
    st.markdown("---")
    st.subheader("📦 Products")
    
    # RENDER PRODUCTS
    sel_cat = st.session_state.get('selected_cat')
    if sel_cat:
        filtered_prods = [name for name, info in products.items() if info["category"] == sel_cat]
        for prod_name in filtered_prods:
            st.button(prod_name, key=f"prod_{prod_name}", use_container_width=True)

with col2:
    st.subheader("🛒 Checkout")
    st.write("Cart is empty.")
