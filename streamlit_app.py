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
        return client.open("3D Printing
