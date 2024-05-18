"""Station page"""

import plotly.io as pio
import streamlit as st
from streamlit import session_state as state

from src import mainfunc, stationsfunc
from src.stations import pyfigure, pyfunc, pytemplate

# SETUP PAGE

pio.templates.default = pytemplate.mytemplate

st.set_page_config(
    page_title="Rainitas | Stations",
    page_icon=":material/pin_drop:",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "Report a bug": "https://github.com/taruma/rainitas/issues/new",
        "About": "Simple app to process rainfall data",
    },
)

# SESSION STATE INITIALIZATION

mainfunc.session_state_create(
    {
        "IS_INPUT_VALID": False,
        "IS_NEAREST_SECTION_DONE": False,
        "GPT_RESPONSE_COMPLETENESS": None,
        "GPT_RESPONSE_RAINFALL": None,
        "coordinate_name": "Queensdale",
        "latitude": "-6.2631",
        "longitude": "106.8095",
        "radius_km": 25,
        "nearest_station_limit": 10,
    }
)

# LOAD CSS & SIDEBAR
mainfunc.load_css("assets/stations.css")
mainfunc.main_sidebar()


# INITIALIZE / LOAD DATA
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


metadata_rainfall, metadata_completeness = load_metadata()
markdown_templates, prompt_templates = load_templates()

# LOAD MARKDOWN TEMPLATES
template_map_intro = markdown_templates["map_intro"]
text_map_info = markdown_templates["map_info"]
template_map_coordinate = markdown_templates["map_coordinate"]

template_nearest_intro = markdown_templates["nearest_intro"]
template_nearest_summary = markdown_templates["nearest_summary"]

text_completeness_intro = markdown_templates["completeness_intro"]

template_heatmap_intro = markdown_templates["heatmap_intro"]
placeholder_heatmap_summary = markdown_templates["heatmap_summary"]

template_rainfall_intro = markdown_templates["rainfall_intro"]
placeholder_rainfall_summary = markdown_templates["rainfall_summary"]

placeholder_closing = markdown_templates["closing"]

# LOAD PROMPT TEMPLATES
prompt_template_completeness = prompt_templates["completeness"]
prompt_template_rainfall = prompt_templates["rainfall"]


# MAIN LAYOUT:

PAGE_TITLES = {
    "title": ":round_pushpin: Eksplorasi Data Hujan :round_pushpin:",
    "subtitle": "Mengakses dan Mengakuisisi Data Hujan",
    "title_map": "🗺️ Peta Stasiun Pengamatan Hujan",
    "title_map_coordinate": "📌 Titik Koordinat Tinjauan",
    "title_nearest": "🔍 Peta Stasiun Terdekat",
    "title_completeness": "📊 Data Kelengkapan Pengamatan",
    "title_heatmap": "🎲 Grafik Kelengkapan Data",
    "title_rainfall": "👓 Grafik Hujan Harian",
    "title_closing": "🚪 Penutup",
}

# SIDEBAR SECTION ------------------------------------------
with st.sidebar:
    st.text_input("OpenAI API Key", type="password", key="openai_api_key")
    st.selectbox(
        "Select Model", ["gpt-4o", "gpt-3.5-turbo", "gpt-4-turbo"], key="gpt_model"
    )

# HEADER SECTION -------------------------------------------
# HEADER - TITLE SECTION -----------------------------------
st.title(PAGE_TITLES["title"], anchor="rainitas-stations")
st.subheader(PAGE_TITLES["subtitle"], anchor=False)

# HEADER - ABSTRACT SECTION --------------------------------
text_abstract = markdown_templates["abstract"]
st.markdown(text_abstract, unsafe_allow_html=True)

# MAIN SECTION ---------------------------------------------
# MAIN - MAP SECTION ---------------------------------------
st.header(PAGE_TITLES["title_map"], anchor="map", divider="blue")
layout_map_intro = st.empty()
layout_map_figure = st.empty()

# MAIN - MAP COORDINATE SECTION ----------------------------
st.header(PAGE_TITLES["title_map_coordinate"], anchor="map-coordinate", divider="red")
st.markdown(markdown_templates["map_coordinate"])
layout_map_input = st.empty()
layout_map_validate = st.empty()

# MAIN - NEAREST SECTION -----------------------------------
st.header(PAGE_TITLES["title_nearest"], anchor="nearest", divider="blue")
layout_nearest_intro = st.empty()
layout_nearest_map = st.empty()
layout_nearest_map.warning("Click 'Find Nearest Stations' to see the result.")
layout_nearest_summary = st.empty()

# MAIN - COMPLETENESS SECTION ------------------------------
st.header(PAGE_TITLES["title_completeness"], anchor="completeness", divider="blue")
layout_completeness_intro = st.empty()
layout_completeness_intro.warning("Complete Nearest Stations to continue.")

# MAIN - HEATMAP SECTION -----------------------------------
st.header(PAGE_TITLES["title_heatmap"], anchor="heatmap", divider="blue")
layout_heatmap_intro = st.empty()
layout_heatmap_figure = st.empty()
layout_heatmap_figure.warning("Complete Nearest Stations to continue.")
with st.expander("Generate Analysis Using 🤖 GPT"):
    btn_generate_completeness = st.button(
        "Generate analysis of completeness",
        use_container_width=True,
        disabled=False,
    )
layout_heatmap_summary = st.empty()

# MAIN - RAINFALL SECTION ----------------------------------
st.header(PAGE_TITLES["title_rainfall"], anchor="rainfall", divider="blue")
layout_rainfall_intro = st.empty()
layout_rainfall_figure = st.empty()
layout_rainfall_figure.warning("Complete Nearest Stations to continue.")
with st.expander("Generate Analysis Using 🤖 GPT"):
    btn_generate_rainfall = st.button(
        "Generate analysis of rainfall", use_container_width=True, disabled=False
    )
layout_rainfall_summary = st.empty()

# MAIN - CLOSING SECTION -----------------------------------
st.header(PAGE_TITLES["title_closing"], anchor="closing", divider="blue")
layout_closing = st.empty()
layout_closing.warning("Complete all sections to finish.")


# ----------- START OF PAGE


# MAP 1 (INTRO)
with layout_map_intro.container():
    ## data
    DATA_MAPS_INTRO = {
        "dataset_name": "Kaggle - greegtitan/indonesia-climate",
        "dataset_link": "https://www.kaggle.com/datasets/greegtitan/indonesia-climate",
        "total_stations": len(metadata_rainfall),
    }

    pg_map_intro = template_map_intro.format(**DATA_MAPS_INTRO)

    ## layout
    st.markdown(pg_map_intro)

    ## save
    mainfunc.session_state_update({"pg_map_intro": pg_map_intro})

# MAP 2 (FIGURE)
with layout_map_figure.container():
    ## data
    TABTITLE_MAP = ["Peta Stasiun", "Tabel Metadata Stasiun", "Informasi Dataset"]

    fig_map = pyfigure.generate_station_map_figure(metadata_rainfall)

    ## layout
    tabs_map = st.tabs(TABTITLE_MAP)
    with tabs_map[0]:
        st.plotly_chart(fig_map, use_container_width=True)
    with tabs_map[1]:
        st.dataframe(metadata_rainfall, use_container_width=True)
    with tabs_map[2]:
        with st.container(border=True):
            st.markdown(text_map_info, unsafe_allow_html=True)

    ## save
    mainfunc.session_state_update({"pg_map_info": text_map_info})


# INPUT COORDINATE
with layout_map_input.container():
    ## data

    ## layout
    cols_map = st.columns(3)

    with cols_map[0]:
        coordinate_name = st.text_input(
            "Coordinate Name",
            st.session_state.coordinate_name,
            key="coordinate_name",
        )

    with cols_map[1]:
        latitude = st.text_input(
            "Latitude / Lintang Derajat", state.latitude, key="latitude"
        )
        longitude = st.text_input(
            "Longitude / Bujur Derajat", state.longitude, key="longitude"
        )

    with cols_map[2]:
        radius_km = st.number_input(
            "Radius (km)", min_value=1, step=1, value=state.radius_km, key="radius_km"
        )
        nearest_stations_limit = st.number_input(
            "Maximum Number of Nearest Stations",
            min_value=1,
            step=1,
            value=state.nearest_station_limit,
            key="nearest_station_limit",
        )
        btn_coordinate = st.button(
            ":round_pushpin: Find Nearest Stations",
            use_container_width=True,
            type="primary",
        )

# INPUT VALIDATION

IS_NAME_VALID = (coordinate_name is not None) and (coordinate_name != "")
IS_LAT_VALID = pyfunc.validate_single_coordinate(latitude, "lat")
IS_LON_VALID = pyfunc.validate_single_coordinate(longitude, "lon")

is_all_valid = IS_LAT_VALID and IS_LON_VALID and IS_NAME_VALID

## reset status if not valid
if not is_all_valid:
    EMOJI_CHECK = [":x:", ":heavy_check_mark:"]

    # error message
    layout_map_validate.error(
        f"""
        Please input the coordinate information correctly.\n
        - Coordinate Name: {EMOJI_CHECK[IS_NAME_VALID]} \n
        - Latitude: {EMOJI_CHECK[IS_LAT_VALID]} \n
        - Longitude: {EMOJI_CHECK[IS_LON_VALID]} \n
        """
    )

    # reset state
    st.session_state.fig_nearest_stations = None
    st.session_state.IS_NEAREST_SECTION_DONE = False

# FIND NEAREST STATIONS - DATA / ACTION
# GET TABLE AND FIGURE IF BUTTON IS CLICKED AND ALL VALID

if btn_coordinate and is_all_valid:
    coordinate_point = f"{latitude},{longitude}"

    table_nearest_stations = stationsfunc.get_nearest_stations(
        coordinate_point, metadata_rainfall, radius_km, nearest_stations_limit
    )

    fig_nearest_stations = pyfigure.generate_nearest_stations_map(
        coordinate_point, coordinate_name, table_nearest_stations
    )

    mainfunc.session_state_update(
        {
            "table_nearest_stations": table_nearest_stations,
            "fig_nearest_stations": fig_nearest_stations,
            "prev_coordinate_name": coordinate_name,
            "prev_latitude": latitude,
            "prev_longitude": longitude,
            "prev_radius_km": radius_km,
            "prev_nearest_stations_limit": nearest_stations_limit,
        }
    )

# FIND NEAREST STATIONS - DISPLAY
# DISPLAY ONLY FIGURE IS SAVED IN SESSION STATE AND ALL VALID

if st.session_state.get("fig_nearest_stations") is not None and is_all_valid:
    ## data
    table_nearest_updated = stationsfunc.rename_table_nearest(
        st.session_state.table_nearest_stations
    )

    data_nearest = {
        "coordinate_name": st.session_state.prev_coordinate_name,
        "latitude": st.session_state.prev_latitude,
        "longitude": st.session_state.prev_longitude,
        "radius_km": st.session_state.prev_radius_km,
        "nearest_stations_limit": st.session_state.prev_nearest_stations_limit,
        "total_nearest_stations": len(table_nearest_updated),
        "nearest_stations_name": ", ".join(
            table_nearest_updated["STATION NAME"].tolist()
        ),
        "closest_station_name": table_nearest_updated.iloc[0]["STATION NAME"],
        "closest_station_distance": table_nearest_updated.iloc[0]["DISTANCE"],
        "farthest_station_name": table_nearest_updated.iloc[-1]["STATION NAME"],
        "farthest_station_distance": table_nearest_updated.iloc[-1]["DISTANCE"],
    }

    pg_nearest_intro = template_nearest_intro.format(**data_nearest)
    pg_nearest_sum = template_nearest_summary.format(**data_nearest)

    ## layout
    with layout_nearest_intro.container():
        st.markdown(pg_nearest_intro)

    with layout_nearest_map.container():
        TABTITLE_NEAREST = ["Peta Stasiun Terdekat", "Tabel Stasiun Terdekat"]
        tabs_nearest_map = st.tabs(TABTITLE_NEAREST)

        with tabs_nearest_map[0]:
            st.plotly_chart(
                st.session_state.fig_nearest_stations, use_container_width=True
            )
        with tabs_nearest_map[1]:
            st.dataframe(table_nearest_updated, use_container_width=True)

    with layout_nearest_summary.container():
        st.markdown(pg_nearest_sum)

    ## session
    st.session_state.IS_NEAREST_SECTION_DONE = True

    mainfunc.session_state_update(
        {
            "pg_nearest_intro": pg_nearest_intro,
            "pg_nearest_sum": pg_nearest_sum,
        }
    )


# Completeness Data

if st.session_state.IS_NEAREST_SECTION_DONE:
    ## data
    nearest_station_ids = table_nearest_updated.index.tolist()

    completeness_df = pyfunc.get_dataframe_from_folder(
        nearest_station_ids, metadata_completeness, "data/completeness"
    )

    fig_completeness = pyfigure.generate_completeness_heatmap(
        completeness_df, metadata_completeness
    )

    figs_bar_completeness = []
    names_bar_completeness = []

    for station_id in nearest_station_ids:
        _series = completeness_df[station_id].dropna()
        _bar = pyfigure.generate_completeness_bar(_series, metadata_completeness)
        _name = metadata_completeness.loc[station_id, "station_name"]
        figs_bar_completeness.append(_bar)
        names_bar_completeness.append(_name)

    data_completeness = {
        "table_nearest_stations_csv": table_nearest_updated.to_markdown(),
        "table_completeness_data_csv": completeness_df.to_markdown(),
    }

    prompt_completeness = prompt_template_completeness.format(**data_completeness)
    pg_heatmap_intro = template_heatmap_intro.format(**data_nearest)

    # DISPLAY
    with layout_completeness_intro.container():
        st.markdown(text_completeness_intro)

    with layout_heatmap_intro.container():
        st.markdown(pg_heatmap_intro)

    with layout_heatmap_figure.container():
        TABTITLE_COMPLETENESS = [
            "Heatmap Kelengkapan",
            "Tabel Kelengkapan Data",
            "Grafik Bar Kelengkapan Data",
        ]

        tabs_completeness = st.tabs(TABTITLE_COMPLETENESS)

        with tabs_completeness[0]:
            st.plotly_chart(
                fig_completeness,
                use_container_width=True,
                config={"displayModeBar": False},
            )
        with tabs_completeness[1]:
            st.dataframe(completeness_df, use_container_width=True)
        with tabs_completeness[2]:
            for station_id, station_name, fig_bar in zip(
                nearest_station_ids, names_bar_completeness, figs_bar_completeness
            ):
                st.markdown(f"###### 🌧️ {station_id} - {station_name} 🌧️")
                st.plotly_chart(
                    fig_bar,
                    use_container_width=True,
                    config={"displayModeBar": False},
                )

    ## save
    mainfunc.session_state_update(
        {
            "pg_completeness_intro": text_completeness_intro,
            "pg_heatmap_intro": pg_heatmap_intro,
        }
    )

    if btn_generate_completeness:
        with layout_heatmap_summary.container():
            with st.spinner("Generating Analysis..."):
                response_completeness = mainfunc.generate_gpt(
                    prompt=prompt_completeness,
                    model=st.session_state.gpt_model,
                    openai_api_key=st.session_state.openai_api_key,
                )

                mainfunc.session_state_update(
                    {
                        "GPT_RESPONSE_COMPLETENESS": response_completeness,
                        "GPT_PROMPT_COMPLETENESS": prompt_completeness,
                    }
                )

    if st.session_state.get("GPT_RESPONSE_COMPLETENESS") is not None:
        with layout_heatmap_summary.container():
            with st.expander("View Prompt"):
                st.code(st.session_state.GPT_PROMPT_COMPLETENESS)
            st.markdown(st.session_state.GPT_RESPONSE_COMPLETENESS)
    else:
        with layout_heatmap_summary.container(border=True):
            st.markdown(placeholder_heatmap_summary, unsafe_allow_html=True)

    # RAINFALL GRAPH

    nearest_ids_names = []
    for station_id, station_name in zip(
        nearest_station_ids, table_nearest_updated["STATION NAME"]
    ):
        nearest_ids_names.append(
            f"1. `{station_id}` - :green-background[**{station_name}**]"
        )

    rainfall_df = pyfunc.get_dataframe_from_folder(
        nearest_station_ids, metadata_rainfall, "data/rainfall"
    )

    pyfunc.replace_unmeasured_data(rainfall_df)

    fig_rainfall = pyfigure.generated_rainfall_figure(rainfall_df, metadata_rainfall)

    data_rainfall = {
        "table_nearest_stations_csv": table_nearest_updated.to_markdown(),
        "table_describe_rainfall_csv": rainfall_df.describe().to_markdown(),
    }

    prompt_rainfall = prompt_template_rainfall.format(**data_rainfall)
    pg_rainfall_intro = template_rainfall_intro.format(
        **{"list_of_nearest_stations": "\n".join(nearest_ids_names)}
    )

    with layout_rainfall_intro.container():
        st.markdown(pg_rainfall_intro)

    with layout_rainfall_figure.container():
        TABTITLE_RAINFALL = [
            "Grafik Hujan Harian",
            "Tabel Hujan Harian",
            "Statistik Hujan Harian",
        ]

        tabs_rainfall = st.tabs(TABTITLE_RAINFALL)

        with tabs_rainfall[0]:
            st.plotly_chart(
                fig_rainfall, use_container_width=True, config={"displayModeBar": False}
            )
        with tabs_rainfall[1]:
            st.dataframe(rainfall_df, use_container_width=True)
        with tabs_rainfall[2]:
            st.dataframe(rainfall_df.describe(), use_container_width=True)

    ## save
    mainfunc.session_state_update({"pg_rainfall_intro": pg_rainfall_intro})

    if btn_generate_rainfall:
        with layout_rainfall_summary.container():
            with st.spinner("Generating Analysis..."):
                response_rainfall = mainfunc.generate_gpt(
                    prompt=prompt_rainfall,
                    model=st.session_state.gpt_model,
                    openai_api_key=st.session_state.openai_api_key,
                )

                mainfunc.session_state_update(
                    {
                        "GPT_RESPONSE_RAINFALL": response_rainfall,
                        "GPT_PROMPT_RAINFALL": prompt_rainfall,
                    }
                )

    if st.session_state.get("GPT_RESPONSE_RAINFALL") is not None:
        with layout_rainfall_summary.container():
            with st.expander("View Prompt"):
                st.code(st.session_state.GPT_PROMPT_RAINFALL)
            st.markdown(st.session_state.GPT_RESPONSE_RAINFALL)
    else:
        with layout_rainfall_summary.container(border=True):
            st.markdown(placeholder_rainfall_summary, unsafe_allow_html=True)

    layout_closing.markdown(placeholder_closing)


# REFRESH BUTTON
st.divider()
st.button("Refresh")
