"""Streamlit app"""

import streamlit as st
from st_pages import Page, show_pages
from src.myfunc import load_markdown

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
        Page("pages/01_stations.py", "Stations", "📍"),
        Page("pages/02_rainfall.py", "Rainfall", "📈"),
        Page("pages/03_anfrek.py", "Analysis", "🔮"),
        Page("pages/04_summary.py", "Summary", "📊"),
    ]
)

# LOADING MARKDOWN FILES
data_md = load_markdown("docs/rainitas.md")
info_md = load_markdown("docs/info.md")

INFO_DICT = {
    "author": "Taruma",
    "version": "v0.1.0",
}

# ----------- START OF PAGE

st.title("🌧️ RAINITAS")
st.markdown(data_md)
st.divider()
st.markdown(info_md.format(**INFO_DICT))
