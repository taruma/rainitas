"""Collection of functions for doing my project."""

# from datetime import datetime
import streamlit as st
from openai import OpenAI

from src.version import APP_AUTHOR, APP_AUTHOR_URL, APP_NAME, APP_VERSION, APP_URL


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
        st.header("🌧️ Rainitas", anchor=False, divider="blue")
        st.page_link("app.py", label="Rainitas", icon="🌧️")
        st.header("**Aplikasi**", anchor=False, divider="green")
        st.page_link("pages/stations.py", label="Stations", icon="📍")
        # st.page_link("pages/rainfall.py", label="Rainfall", icon="📈")
        # st.page_link("pages/anfrek.py", label="Analysis", icon="🔮")
        # st.page_link("pages/summary.py", label="Summary", icon="📊")

        st.markdown(
            f"#### [{APP_NAME}]({APP_URL}) {APP_VERSION} by [{APP_AUTHOR}]({APP_AUTHOR_URL})"
        )


def load_state():
    """Load the state of the app."""

    # if "openai_api_key" not in st.session_state:
    #     st.session_state.openai_api_key = st.secrets["OPENAI_API_KEY"]

    print("//// Loading state...")
    for key, value in st.session_state.items():
        print(f"{key}: {type(value)}")
        st.session_state[key] = value
    print("//// Loading state... done")


@st.cache_data
def generate_gpt(
    prompt="hello!",
    model="gpt-3.5-turbo",
    role_system="Kamu adalah ahli hidrologi yang akan membantu pengguna.",
    openai_api_key=None,
):
    """Generate text from the given prompt."""
    try:
        # now = datetime.now()
        # print(f"RUNNING GPT {now.strftime('%Y%m%d_%H%M%S')}")

        client = OpenAI(api_key=openai_api_key)

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": role_system},
                {"role": "user", "content": prompt},
            ],
        )

        message = completion.choices[0].message.content

        # REMOVE THIS PART WHEN LIVE
        # filename = f"output_prompt/prompt_{now.strftime('%Y%m%d_%H%M%S')}.txt"
        # with open(filename, "w", encoding="utf-8") as f:
        #     f.write("MODEL: " + model + "\n")
        #     f.write("\n[SYSTEM]\n" + role_system + "\n")
        #     f.write("\n\n[USER]\n" + prompt + "\n")
        #     f.write("\n\n[RESPONSE]\n" + message + "\n")

        return message

    except Exception as e:  # pylint: disable=broad-except
        print(f"Error: {e}")
        return f"Error: {e}"


def session_state_create(kwargs):
    """Create the given kwargs to the session state if not exist."""

    for key, value in kwargs.items():
        if key not in st.session_state:
            # print(f"{key} created")
            st.session_state[key] = value


def session_state_update(kwargs):
    """Update the given kwargs to the session state and create if not exist."""

    for key, value in kwargs.items():
        if key in st.session_state:
            # print(f"{key} updated")
            st.session_state[key] = value
        else:
            # print(f"{key} created via update")
            st.session_state[key] = value
