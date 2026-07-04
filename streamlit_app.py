import streamlit as st
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import os

# Page configuration for a professional wide layout
st.set_page_config(page_title="3D Printing Market Hub", page_icon="🖨️", layout="wide")

# Convert the image file directly into web-safe code text
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Try finding logo.png in the main folder or inside the static folder
image_code = get_base64_image("logo.png") or get_base64_image("static/logo.png")

# Inject your custom dark mode CSS and background image code
if image_code:
    bg_style = f'background-image: linear-gradient(rgba(15, 23, 42, 0.90), rgba(15, 23, 42, 0.90)), url("data:image/png;base64,{image_code}");'
else:
    bg_style = "background-color: #0f172a;"

st.markdown(f"""
    <style>
    /* Injects a dark charcoal/blue overlay over your converted logo image */
    .stApp {{
        {bg_style}
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Styles the big product buttons to stand out in the dark */
    div.stButton > button:first-child {{
        border-radius: 12px;
        font-weight: 700;
        background-color: #1e293b;   /* Dark slate background for buttons */
        border: 2px solid #334155;   /* Crisp border */
        color: #f8fafc;              /* White text */
        transition: 0.2s;
    }}
    
    /* Button hover pop effect */
    div.stButton > button:first-child:hover {{
        border-color: #10b981;       /* Turns green on hover to match dark mode accents */
        color: #10b981;
    }}

    /* Styles the information cards to stay dark slate grey and readable */
    .metric-box {{
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);
        border: 1px solid #334155;
    }}
    </style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS LIVE SETUP ---
@st.cache_resource
def connect_to_google_sheets():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/adamq/desktop/market-app/google_creds.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("3D Printing Market Sales").sheet1
        return sheet
    except Exception as e:
        st.error(f"Could not connect to Google Sheet: {e}")
        return None

sheet_connection = connect_to_google_sheets()

# Product catalog configuration
products = {
    "Dummy 13 Kit": {"weight": 75, "time": 2.0, "labor": 0},
    "Dummy 13 Assembled": {"weight": 75, "time": 2.0, "labor": 10},
    "Post-it Stencil Station": {"weight": 100, "time": 3.5, "labor": 0},
    "Goofy Axolotl": {"weight": 35, "time": 1.5, "labor": 0},
    "Custom Request": {"weight": 0, "time": 0.0, "labor": 0},
    "4th tick tack toe": {"weight": 100, "time": 5, "labor": 0}
}

if 'cart' not in st.session_state:
    st.session_state['cart'] = []

# Header UI layout split into columns
header_left, header_right = st.columns([2, 1])
with header_left:
    st.title("🖨️ 3D Printing Market Hub")
    st.caption("Cloud Connected Terminal • Real-Time Inventory Calculations")
with header_right:
    if sheet_connection:
        st.success("🟢 Connected to Live Sheet")
    else:
        st.error("🔴 Cloud Sync Offline")

st.divider()

# Split the screen horizontally into two major sections: Left for actions, Right for active Cart
main_col1, main_col2 = st.columns([4, 3], gap="large")

with main_col1:
    st.markdown("### 🛍️ Quick-Add Inventory")
    
    # Grid arrangement for crisp, modern buttons
    cols = st.columns(3)
    for i, prod_name in enumerate(products.keys()):
        col_idx = i % 3
        if cols[col_idx].button(prod_name, use_container_width=True, key=f"btn_{prod_name}", type="secondary"):
            st.session_state['selected_product'] = prod_name

    current_product = st.session_state.get('selected_product', None)

    if current_product:
        st.write("")
        st.markdown(f"<div class='metric-box'><strong>Active Configurator:</strong> {current_product}</div>", unsafe_allow_html=True)
        st.write("")
        
        if current_product == "Custom Request":
            c_w, c_t = st.columns(2)
            weight = c_w.number_input("Custom Weight (g)", min_value=1, value=50)
            print_time = c_t.number_input("Custom Print Time (hrs)", min_value=0.1, value=2.0)
            labor = 0
        else:
            weight = products[current_product]["weight"]
            print_time = products[current_product]["time"]
            labor = products[current_product]["labor"]
            
        material_cost_per_g = 0.10
        elec_cost_per_kwh = 0.17
        printer_kw = 0.105 
        
        total_item_cost = (weight * material_cost_per_g) + (print_time * printer_kw * elec_cost_per_kwh)
        target_price = round((total_item_cost / 0.20) + labor)
        
        # Use clean metric column displays for a polished dashboard feel
        m1, m2 = st.columns(2)
        with m1:
            st.metric(label="Target Suggested Price", value=f"${target_price}", delta="80% Profit Margin")
        with m2:
            st.metric(label="Raw Material/Power Cost", value=f"${total_item_cost:.2f}")
            
        st.markdown("---")
        st.write("**Adjust Final Quantity & Pricing:**")
        input_col1, input_col2 = st.columns(2)
        actual_price = input_col1.number_input("Actual Sale Price ($)", min_value=1, value=int(target_price), key="actual_price_input")
        quantity = input_col2.number_input("Quantity", min_value=1, value=1, key="quantity_input")
        
        if st.button("🛒 Confirm & Add to Cart", type="primary", use_container_width=True):
            st.session_state['cart'].append({
                "Product": current_product,
                "Quantity": quantity,
                "Price per Unit": actual_price,
                "Unit Cost": total_item_cost
            })
            st.toast(f"Added {quantity}x {current_product}!", icon="🛒")
            st.session_state['selected_product'] = None
            st.rerun()

with main_col2:
    st.markdown("### 🛒 Active Checkout Desk")
    
    if st.session_state['cart']:
        cart_df = pd.DataFrame(st.session_state['cart'])
        # Dynamic calculation summaries for display
        cart_df["Total"] = cart_df["Quantity"] * cart_df["Price per Unit"]
        
        st.dataframe(cart_df[["Product", "Quantity", "Price per Unit", "Total"]], use_container_width=True, hide_index=True)
        
        grand_total = cart_df["Total"].sum()
        st.markdown(f"#### **Total Due: ${grand_total:.2f}**")
        
        payment_type = st.selectbox("Payment Gateway Type", ["Cash", "Venmo", "Square"])
        
        st.write("")
        col_check, col_clear = st.columns(2)
        
        if col_check.button("💾 Secure Cloud Checkout", type="primary", use_container_width=True):
            today_str = datetime.date.today().strftime("%Y-%m-%d")
            
            if sheet_connection is not None:
                with st.spinner("Syncing encrypted records to cloud ledger..."):
                    for item in st.session_state['cart']:
                        total_unit_cost = round(item["Quantity"] * item["Unit Cost"], 2)
                        total_revenue = round(item["Quantity"] * item["Price per Unit"], 2)
                        total_net_profit = round(total_revenue - total_unit_cost, 2)
                        
                        row_to_append = [
                            today_str,
                            item["Product"],
                            item["Quantity"],
                            payment_type,
                            total_unit_cost,
                            total_revenue,
                            total_net_profit
                        ]
                        sheet_connection.append_row(row_to_append)
                        
                st.balloons() # Fun reward effect on a successful save
                st.success("Transaction pushed successfully!")
                st.session_state['cart'] = [] 
                st.rerun()
            else:
                st.error("Sheet Connection Refused. Please refresh.")
            
        if col_clear.button("🗑️ Void Entire Cart", use_container_width=True, type="secondary"):
            st.session_state['cart'] = []
            st.rerun()
    else:
        st.info("The checkout desk is currently empty. Click a product on the left to begin compiling a transaction.")
