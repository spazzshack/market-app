import streamlit as st
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64
import os

# --- PAGE SETUP & ABSOLUTE PATH FIX ---
st.set_page_config(page_title="Spazz Shack", page_icon="🖨️", layout="wide")

# Get the directory where THIS script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(SCRIPT_DIR, "static", "logo.png")

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

image_code = get_base64_image(IMAGE_PATH)
bg_style = f'background-image: linear-gradient(rgba(15, 23, 42, 0.90), rgba(15, 23, 42, 0.90)), url("data:image/png;base64,{image_code}");' if image_code else "background-color: #0f172a;"

st.markdown(f"""
    <style>
    .stApp {{ {bg_style} background-size: cover; background-position: center; background-attachment: fixed; }}
    </style>
""", unsafe_allow_html=True)
