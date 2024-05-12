"""Collection of functions for doing my project."""

from datetime import datetime
from openai import OpenAI
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
        st.html(f"<style>{f.read()}</style>")


def main_sidebar():
    """Create the main sidebar for the app."""
    with st.sidebar:
        st.page_link("app.py", label="Rainitas", icon="🌧️")
        st.write("**Aplikasi**")
        st.page_link("pages/stations.py", label="Stations", icon="📍")
        # st.page_link("pages/rainfall.py", label="Rainfall", icon="📈")
        # st.page_link("pages/anfrek.py", label="Analysis", icon="🔮")
        # st.write("_Generated_")
        # st.page_link("pages/summary.py", label="Summary", icon="📊")

        st.divider()
        st.write("created by [taruma](https://github.com/taruma)")


def load_state():
    """Load the state of the app."""

    # if "openai_api_key" not in st.session_state:
    #     st.session_state.openai_api_key = st.secrets["OPENAI_API_KEY"]

    # print("//// Loading state...")
    for key, value in st.session_state.items():
        # print(f"{key}: {type(value)}")
        st.session_state[key] = value
    # print("//// Loading state... done")


@st.cache_data
def generate_gpt(
    prompt="hello!",
    model="gpt-3.5-turbo",
    role_system="Kamu adalah ahli hidrologi yang akan membantu pengguna.",
):
    """Generate text from the given prompt."""

    now = datetime.now()
    print(f"RUNNING GPT {now.strftime('%Y%m%d_%H%M%S')}")

    client = OpenAI(api_key=st.session_state.openai_api_key)

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": role_system},
            {"role": "user", "content": prompt},
        ],
    )

    message = completion.choices[0].message.content

    # REMOVE THIS PART WHEN LIVE
    # filename = f"prompt_{now.strftime('%Y%m%d_%H%M%S')}.txt"
    # with open(filename, "w", encoding="utf-8") as f:
    #     f.write("MODEL: " + model + "\n")
    #     f.write("\n[SYSTEM]\n" + role_system + "\n")
    #     f.write("\n\n[USER]\n" + prompt + "\n")
    #     f.write("\n\n[RESPONSE]\n" + message + "\n")

    return message


def create_to_session(kwargs):
    """Create the given kwargs to the session state."""

    for key, value in kwargs.items():
        if key not in st.session_state:
            print(f"{key} created")
            st.session_state[key] = value


def update_to_session(kwargs):
    """Update the given kwargs to the session state."""

    for key, value in kwargs.items():
        if key in st.session_state:
            print(f"{key} updated")
            st.session_state[key] = value
        else:
            print(f"{key} created via update")
            st.session_state[key] = value
