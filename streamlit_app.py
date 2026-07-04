import streamlit as st
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import os

# --- PAGE SETUP & ABSOLUTE PATH FIX ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(SCRIPT_DIR, "static", "logo.png")

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

image_code = get_base64_image(IMAGE_PATH)

# Refined CSS
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

# --- LOAD INVENTORY ---
@st.cache_data(ttl=60)
def load_inventory():
    if not wb: return {}
    data = wb.worksheet("Inventory").get_all_records()
    def safe_float(val):
        try: return float(val) if str(val).strip() != "" else 0.0
        except: return 0.0
    return {item["Product"]: {
        "weight": safe_float(item["Weight"]), 
        "time": safe_float(item["Time"]), 
        "labor": safe_float(item["Labor"]),
        "comp": safe_float(item.get("Component Cost", 0)),
        "target": safe_float(item.get("Target Price", 0)),
        "category": item.get("Category", "General")
    } for item in data}

products = load_inventory()
if 'cart' not in st.session_state: st.session_state['cart'] = []

# --- UI LAYOUT ---
st.title("🖨️ Spazz Shack")

main_col1, main_col2 = st.columns([4, 3], gap="large")

with main_col1:
    st.markdown("### 🛍️ Quick-Add Inventory")
    all_prods = load_inventory()
    categories = sorted(list(set(p["category"] for p in all_prods.values())))
    
    # Keyboard-friendly selection
    selected_cat = st.radio(
        "Filter by Category", 
        categories, 
        horizontal=True
    )
    
    filtered_prods = {k: v for k, v in all_prods.items() if v["category"] == selected_cat}
    
    cols = st.columns(3)
    for i, prod_name in enumerate(filtered_prods.keys()):
        if cols[i % 3].button(prod_name, use_container_width=True):
            st.session_state['selected_product'] = prod_name

    current_product = st.session_state.get('selected_product', None)
    if current_product:
        data = products[current_product]
        printing_cost = (data["weight"] * 0.02) + (data["time"] * 0.02)
        total_make_cost = printing_cost + data["comp"]
        suggested_price = (printing_cost / 0.20) + data["comp"] + data["labor"]
        
        st.markdown(f"**Active:** {current_product}")
        c1, c2 = st.columns(2)
        c1.metric("Cost to Make", f"${total_make_cost:.2f}")
        c2.metric("Suggested Price", f"${suggested_price:.2f}")
        
        default_price = data["target"] if data["target"] > 0 else int(suggested_price)
        price = st.number_input("Final Sale Price ($)", value=default_price)
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
        
        fee = 0.0
        if pay_type != "Cash":
            add_fee = st.checkbox(f"Add 3% Processing Fee?", value=False)
            if add_fee: fee = running_total * 0.03
        
        st.metric("Total Due", f"${(running_total + fee):.2f}")
        
        if st.button("💾 Checkout"):
            js_code = "<script>var audio = new Audio('https://actions.google.com/sounds/v1/ui/gameshow_correct_answer.ogg'); audio.play();</script>"
            st.components.v1.html(js_code, height=0)
            
            sales_sheet = wb.worksheet("Sales")
            for item in st.session_state['cart']:
                data = products[item["Product"]]
                cost_per_item = ((data["weight"] * 0.02) + (data["time"] * 0.02) + data["comp"])
                total_row_cost = round(item["Qty"] * cost_per_item, 2)
                item_fee = (fee / len(st.session_state['cart'])) if fee > 0 else 0
                total_rev = item["Qty"] * item["Sale Price"]
                profit = total_rev - total_row_cost - item_fee
                sales_sheet.append_row([str(datetime.date.today()), item["Product"], item["Qty"], pay_type, total_row_cost, total_rev, round(profit, 2), round(item_fee, 2)])
            
            st.session_state['cart'] = []
            st.balloons()
            st.rerun()
