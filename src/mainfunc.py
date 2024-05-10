"""Collection of functions for doing my project."""

import streamlit as st


@st.cache_data
def load_markdown(filename: str) -> str:
    """Load markdown file from the given filename."""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

@st.cache_data
def load_css(filename: str) -> None:
    """Load CSS file from the given filename."""
    with open(filename, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
