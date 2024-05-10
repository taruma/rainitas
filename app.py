"""Streamlit app"""

import os

import streamlit as st
from dotenv import load_dotenv
from st_pages import Page, show_pages

from src import mainfunc

# Load environment variables
load_dotenv()

# --- SETUP PAGE

st.set_page_config(
    page_title="Rainitas by Taruma",
    page_icon=":material/rainy:",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "Report a bug": "https://github.com/taruma/rainitas/issues/new",
        "About": "Simple app to process rainfall data with AI.",
    },
)

show_pages(
    [
        Page("app.py", "Rainitas", "🌧️"),
        Page("pages/stations.py", "Stations", "📍"),
        Page("pages/rainfall.py", "Rainfall", "📈"),
        Page("pages/anfrek.py", "Analysis", "🔮"),
        Page("pages/summary.py", "Summary", "📊"),
    ]
)

mainfunc.load_css("assets/mainstyles.css")

# SIDEBAR

# LOADING MARKDOWN FILES
data_md = mainfunc.load_markdown("docs/rainitas.md")

# ----------- START OF PAGE

st.title("🌧️ RAINITAS")
st.markdown(data_md)
st.divider()

# ----------- SETUP PAGE

if "OPENAI_API_KEY" not in st.session_state:
    st.session_state.OPENAI_API_KEY = None

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
st.session_state["OPENAI_API_KEY"] = OPENAI_API_KEY
