"""Collection of functions for doing my project."""

import streamlit as st


@st.cache_data
def load_markdown(filename: str) -> str:
    """Load markdown file from the given filename."""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


