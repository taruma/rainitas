"""Collection of functions for doing my project."""

import streamlit as st
from st_pages import Page, show_pages, Section

@st.cache_data
def load_markdown(filename: str) -> str:
    """Load markdown file from the given filename."""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

@st.cache_data
def load_css(filename: str) -> None:
    """Load CSS file from the given filename."""
    with open(filename, "r", encoding="utf-8") as f:
        st.html(f"<style>{f.read()}</style>")

def main_sidebar():
    
    with st.sidebar:
        st.page_link("app.py", label="Rainitas", icon="🌧️")
        st.write("**Aplikasi**")
        st.page_link("pages/stations.py", label="Stations", icon="📍")
        st.page_link("pages/rainfall.py", label="Rainfall", icon="📈")
        st.page_link("pages/anfrek.py", label="Analysis", icon="🔮")
        st.write("_Generated_")
        st.page_link("pages/summary.py", label="Summary", icon="📊")
