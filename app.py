"""Streamlit app"""

import streamlit as st
from src import mainfunc

# SETUP PAGE CONFIG
st.set_page_config(
    page_title="Rainitas by Taruma",
    page_icon=":material/rainy:",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "Report a bug": "https://github.com/taruma/rainitas/issues/new",
        "About": "Simple app to process rainfall data.",
    },
)

# SETUP PAGES
mainfunc.load_css("assets/mainstyles.css")
mainfunc.main_sidebar()

# LOADING MARKDOWN FILES
text_rainitas = mainfunc.load_markdown("docs/rainitas.md")

# ----------- START OF PAGE

st.title("🌧️ RAINITAS")
st.markdown(text_rainitas, unsafe_allow_html=True)
st.divider()

# ----------- SETUP PAGE
