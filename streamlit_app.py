import streamlit as st
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import os

# Page configuration
st.set_page_config(page_title="3D Printing Market Hub", page_icon="🖨️", layout="wide")

# Helper for images
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

image_code = get_base64_image("logo.png") or get_base64_image("static/logo.png")
bg_style = f'background-image: linear-gradient(rgba(15, 23, 42, 0.90), rgba(15, 23, 42, 0.90)), url("data:image/png;base64,{image_code}");' if image_code else "background-color: #0f172a;"

st.markdown(f"""
    <style>
    .stApp {{ {bg_style} background-size: cover; background-position: center; background-attachment: fixed; }}
    div.stButton > button:first-child {{ border-radius: 12px; font-weight: 700; background-color: #1e293b; border: 2px solid #334155; color: #f8fafc; transition: 0.2s; }}
    div.stButton > button:first-child:hover {{ border-color: #10b981; color: #10b981; }}
    .metric-box {{ background-color: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; }}
    </style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def connect_to_google_sheets():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        if "gcp_service_account" in st.secrets:
            import json
            creds_dict = dict(st.secrets["gcp_service_account"])
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        else:
            creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/adamq/desktop/market-app/google_creds.json", scope)
        client = gspread.authorize(creds)
        return client.open("3D Printing Market Sales")
    except Exception as e:
        st.error(f"Could not connect to Google Sheet: {e}")
        return None

wb = connect_to_google_sheets()

# --- LOAD INVENTORY FROM SHEET ---
@st.cache_data(ttl=60)
def load_inventory():
    if not wb: return {}
    data = wb.worksheet("Inventory").get_all_records()
    return {item["Product"]: {"weight": float(item["Weight"]), "time": float(item["Time"]), "labor": float(item["Labor"])} for item in data}

products = load_inventory()

if 'cart' not in st.session_state: st.session_state['cart'] = []

# --- UI LAYOUT ---
st.title("🖨️ 3D Printing Market Hub")
if wb: st.success("🟢 Connected to Live Sheet")
else: st.error("🔴 Cloud Sync Offline")

main_col1, main_col2 = st.columns([4, 3], gap="large")

with main_col1:
    st.markdown("### 🛍️ Quick-Add Inventory")
    cols = st.columns(3)
    for i, prod_name in enumerate(products.keys()):
        if cols[i % 3].button(prod_name, use_container_width=True):
            st.session_state['selected_product'] = prod_name

    current_product = st.session_state.get('selected_product', None)
    if current_product:
        st.markdown(f"<div class='metric-box'><strong>Active:</strong> {current_product}</div>", unsafe_allow_html=True)
        w = products[current_product]["weight"]
        t = products[current_product]["time"]
        l = products[current_product]["labor"]
        
        cost = (w * 0.10) + (t * 0.105 * 0.17)
        suggested = round((cost / 0.20) + l)
        
        st.metric("Suggested Price", f"${suggested}")
        price = st.number_input("Sale Price ($)", value=int(suggested))
        qty = st.number_input("Quantity", min_value=1, value=1)
        
        if st.button("🛒 Add to Cart", type="primary"):
            st.session_state['cart'].append({"Product": current_product, "Qty": qty, "Price": price, "Cost": cost})
            st.rerun()

with main_col2:
    st.markdown("### 🛒 Checkout")
    if st.session_state['cart']:
        df = pd.DataFrame(st.session_state['cart'])
        st.table(df)
        pay_type = st.selectbox("Payment", ["Cash", "Venmo", "Square"])
        if st.button("💾 Checkout"):
            sales_sheet = wb.worksheet("Sales")
            for item in st.session_state['cart']:
                total_cost = round(item["Qty"] * item["Cost"], 2)
                total_rev = item["Qty"] * item["Price"]
                sales_sheet.append_row([str(datetime.date.today()), item["Product"], item["Qty"], pay_type, total_cost, total_rev, total_rev - total_cost])
            st.session_state['cart'] = []
            st.balloons()
            st.rerun()
