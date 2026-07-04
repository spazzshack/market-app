import streamlit as st
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# Pathing setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(SCRIPT_DIR, "static", "logo.png")

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

image_code = get_base64_image(IMAGE_PATH)

# CSS for styling
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(15, 23, 42, 0.90), rgba(15, 23, 42, 0.90)), 
                    url("data:image/png;base64,{image_code}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    h1, h2, h3, p, div {{ color: white !important; }}
    </style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def connect_to_google_sheets():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        # Look for secret or local file
        if "gcp_service_account" in st.secrets:
            import json
            creds_dict = dict(st.secrets["gcp_service_account"])
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        else:
            # Fallback path - verify this path on your machine
            creds = ServiceAccountCredentials.from_json_keyfile_name("google_creds.json", scope)
        client = gspread.authorize(creds)
        return client.open("3D Printing Market Sales")
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

wb = connect_to_google_sheets()

# --- LOAD INVENTORY ---
@st.cache_data(ttl=60)
def load_inventory():
    if not wb: return {}
    try:
        data = wb.worksheet("Inventory").get_all_records()
        return {item["Product"]: {
            "weight": float(item.get("Weight", 0) or 0), 
            "time": float(item.get("Time", 0) or 0), 
            "labor": float(item.get("Labor", 0) or 0),
            "comp": float(item.get("Component Cost", 0) or 0),
            "target": float(item.get("Target Price", 0) or 0),
            "category": item.get("Category", "General")
        } for item in data}
    except Exception as e:
        return {}

if 'cart' not in st.session_state: st.session_state['cart'] = []
if 'selected_cat' not in st.session_state: st.session_state['selected_cat'] = None

# --- UI LAYOUT ---
st.title("🖨️ Spazz Shack")
products = load_inventory()

if not products:
    st.warning("No inventory loaded. Please check your Google Sheet connection.")
    st.stop()

main_col1, main_col2 = st.columns([0.6, 0.4])

with main_col1:
    st.markdown("### 🛍️ Quick-Add Inventory")
    
    # Extract categories safely
    categories = sorted(list(set(p["category"] for p in products.values())))
    
    # Manual 3-column grid for buttons
    if not st.session_state['selected_cat']:
        st.session_state['selected_cat'] = categories[0]
        
    for i in range(0, len(categories), 3):
        row = st.columns(3)
        for j in range(3):
            if i + j < len(categories):
                cat = categories[i+j]
                # Highlight active button
                btn_type = "primary" if st.session_state['selected_cat'] == cat else "secondary"
                if row[j].button(cat, use_container_width=True, type=btn_type):
                    st.session_state['selected_cat'] = cat
                    st.rerun()
    
    # Filter and display products
    sel_cat = st.session_state['selected_cat']
    filtered_prods = {k: v for k, v in products.items() if v["category"] == sel_cat}
    
    cols = st.columns(3)
    for i, prod_name in enumerate(filtered_prods.keys()):
        if cols[i % 3].button(prod_name, use_container_width=True):
            st.session_state['selected_product'] = prod_name

    # Product details
    current_product = st.session_state.get('selected_product', None)
    if current_product and current_product in products:
        data = products[current_product]
        # Calculations...
        printing_cost = (data["weight"] * 0.02) + (data["time"] * 0.02)
        total_make_cost = printing_cost + data["comp"]
        suggested_price = (printing_cost / 0.20) + data["comp"] + data["labor"]
        
        st.markdown(f"**Active:** {current_product}")
        c1, c2 = st.columns(2)
        c1.metric("Cost to Make", f"${total_make_cost:.2f}")
        c2.metric("Suggested Price", f"${suggested_price:.2f}")
        
        price = st.number_input("Sale Price ($)", value=data["target"] if data["target"] > 0 else int(suggested_price))
        qty = st.number_input("Quantity", min_value=1, value=1)
        
        if st.button("🛒 Add to Cart", type="primary"):
            st.session_state['cart'].append({"Product": current_product, "Qty": qty, "Sale Price": price, "Total": qty * price})
            st.rerun()

with main_col2:
    st.markdown("### 🛒 Checkout")
    if st.session_state['cart']:
        df = pd.DataFrame(st.session_state['cart'])
        st.table(df)
        running_total = df["Total"].sum()
        pay_type = st.selectbox("Payment", ["Cash", "Venmo", "Square", "PayPal"])
        fee = (running_total * 0.03) if pay_type != "Cash" and st.checkbox("Add 3% Fee?") else 0.0
        st.metric("Total Due", f"${(running_total + fee):.2f}")
        if st.button("💾 Checkout"):
            sales_sheet = wb.worksheet("Sales")
            for item in st.session_state['cart']:
                sales_sheet.append_row([str(datetime.date.today()), item["Product"], item["Qty"], pay_type, 0, item["Total"], 0, 0])
            st.session_state['cart'] = []
            st.rerun()
