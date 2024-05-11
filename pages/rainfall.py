"""Rainfall page"""

import streamlit as st
from src import mainfunc

st.set_page_config(
    page_title="Rainitas | Rainfall",
    page_icon=":material/query_stats:",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "Report a bug": "https://github.com/taruma/rainitas/issues/new",
        "About": "Simple app to process rainfall data with AI.",
    },
)

mainfunc.main_sidebar()

# ----------- START OF PAGE

st.write("Hello World from Second Page")
