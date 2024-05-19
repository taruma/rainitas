"""Function for stations page."""

import streamlit as st
from src.stations import pyfunc
from src import mainfunc

# pylint: disable=too-many-arguments


@st.cache_data
def get_nearest_stations(
    coordinate_location, metadata_df, radius_km, num_nearest, round_decimal=3
):
    """Get nearest stations from the given coordinate location."""
    stations_with_distance = pyfunc.dataframe_calc_distance(
        coordinate_location, metadata_df
    )

    nearest_stations_df = (
        stations_with_distance.sort_values("distance")
        .round(round_decimal)
        .loc[stations_with_distance.distance < radius_km]
        .iloc[:num_nearest]
    )

    return nearest_stations_df


@st.cache_data
def rename_table_nearest(nearest_df):
    """Rename columns of nearest stations table."""
    old_columns_name = "title distance station_name".split()
    new_columns_name = "ID,DATASET,DISTANCE,STATION NAME".split(",")

    renamed_nearest_df = (
        nearest_df[old_columns_name]
        .rename_axis("ID")
        .rename(columns=dict(zip(old_columns_name, new_columns_name[1:])))
    )
    return renamed_nearest_df


@st.cache_data
def load_metadata():
    """Load metadata from CSV files."""

    rainfall = pyfunc.read_metadata_csv("data/rainfall")
    completeness = pyfunc.read_metadata_csv("data/completeness")

    return rainfall, completeness


@st.cache_data
def load_templates():
    """Load markdown files."""

    markdown_file_path = {
        "abstract": "docs/stations/abstract.md",
        "map_intro": "docs/stations/map_intro_template.md",
        "map_info": "docs/stations/map_info.md",
        "map_coordinate": "docs/stations/map_coordinate.md",
        "nearest_intro": "docs/stations/nearest_intro_template.md",
        "nearest_summary": "docs/stations/nearest_summary_template.md",
        "completeness_intro": "docs/stations/completeness_intro.md",
        "heatmap_intro": "docs/stations/heatmap_intro_template.md",
        "heatmap_summary": "docs/stations/heatmap_summary_placeholder.md",
        "rainfall_intro": "docs/stations/rainfall_intro_template.md",
        "rainfall_summary": "docs/stations/rainfall_summary_placeholder.md",
        "closing": "docs/stations/closing_placeholder.md",
    }

    loaded_markdown_files = {
        key: mainfunc.load_markdown(value) for key, value in markdown_file_path.items()
    }

    loaded_prompt_files = {
        "completeness": mainfunc.load_markdown(
            "prompt/stations/prompt_completeness.md"
        ),
        "rainfall": mainfunc.load_markdown("prompt/stations/prompt_rainfall_data.md"),
    }

    return loaded_markdown_files, loaded_prompt_files



def validate_input(coordinate_name, latitude, longitude, layout):
    """Validate input from user."""
    validation_name = (coordinate_name is not None) and (coordinate_name != "")
    validation_latitude = pyfunc.validate_single_coordinate(latitude, "lat")
    validation_longitude = pyfunc.validate_single_coordinate(longitude, "lon")

    all_valid = validation_name and validation_latitude and validation_longitude
    if not all_valid:
        emoji_check = [":x:", ":heavy_check_mark:"]

        # error message
        layout.error(
            f"""
            Please input the coordinate information correctly.\n
            - Coordinate Name: {emoji_check[validation_name]} \n
            - Latitude: {emoji_check[validation_latitude]} \n
            - Longitude: {emoji_check[validation_longitude]} \n
            """
        )

        # reset state
        st.session_state.fig_nearest_stations = None
        st.session_state.IS_NEAREST_SECTION_DONE = False

        return False

    return True


def render_gpt_result(
    btn_generate,
    layout_summary,
    prompt,
    gpt_model,
    openai_api_key,
    response_key,
    prompt_key,
    placeholder,
):
    """Render GPT result."""

    if btn_generate:
        with layout_summary.container():
            response = mainfunc.generate_gpt(
                prompt=prompt, model=gpt_model, openai_api_key=openai_api_key
            )

            mainfunc.session_state_update({response_key: response, prompt_key: prompt})

    if st.session_state.get(response_key) is not None:
        with layout_summary.container():
            with st.expander("View Prompt"):
                st.code(st.session_state.get(prompt_key))
            st.markdown(st.session_state.get(response_key))
    else:
        with layout_summary.container(border=True):
            st.markdown(placeholder, unsafe_allow_html=True)
