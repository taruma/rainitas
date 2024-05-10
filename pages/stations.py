"""Station page"""

import streamlit as st
import plotly.io as pio

# from openai import OpenAI
from src.stations import pyfunc, pyfigure
from src.stations import pytemplate
from src import mainfunc


pio.templates.default = pytemplate.mytemplate

st.set_page_config(
    page_title="Rainitas | Stations",
    page_icon=":material/pin_drop:",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "Report a bug": "https://github.com/taruma/rainitas/issues/new",
        "About": "Simple app to process rainfall data with AI.",
    },
)

mainfunc.load_css("assets/stations.css")

# INITIALIZE

combined_metadata_rr = pyfunc.read_metadata_csv("data/rainfall")
combined_metadata_comp = pyfunc.read_metadata_csv("data/completeness")

# ----------- START OF PAGE

st.title(":round_pushpin: Eksplorasi Data Hujan :round_pushpin:")

with st.expander("Pendahuluan"):
    md_introduction = mainfunc.load_markdown("docs/stations/01_intro.md")
    st.markdown(md_introduction, unsafe_allow_html=True)

st.markdown("## 🗺️ Peta Stasiun Pengamatan Hujan")

fig_map = pyfigure.generate_station_map_figure(combined_metadata_rr)

tab1, tab2, tab3 = st.tabs(["Peta Stasiun", "Metadata", "Informasi Metadata"])


with tab1:
    st.plotly_chart(fig_map, use_container_width=True)

with tab2:
    st.dataframe(combined_metadata_rr)

with tab3:
    md_metadata_info = mainfunc.load_markdown("docs/stations/02_metadata_info.md")
    with st.container(border=True):
        st.markdown(md_metadata_info, unsafe_allow_html=True)


st.markdown("#### 📌 Titik Koordinat Tinjauan")

tab1, tab2, col3 = st.columns(3)

with tab1:
    coordinate_name = st.text_input(
        "Coordinate Name / Nama Koordinat", "Koordinat Saya", key="sta_coordinate_name"
    )
    is_name_valid = (coordinate_name is not None) and (coordinate_name != "")

with tab2:
    latitude = st.text_input(
        "Latitude / Lintang Derajat", "-6.2631", key="sta_latitude"
    )
    longitude = st.text_input(
        "Longitude / Bujur Derajat", "106.8095", key="sta_longitude"
    )

    IS_LAT_VALID = pyfunc.validate_single_coordinate(latitude, "lat")
    # st.checkbox("Latitude / Lintang Derajat", value=IS_LAT_VALID, disabled=True)
    IS_LON_VALID = pyfunc.validate_single_coordinate(longitude, "lon")
    # st.checkbox("Bujur", value=IS_LON_VALID, disabled=True)

with col3:
    radius_km = st.number_input("Radius (km)", 1, step=1, value=25, key="sta_radius_km")
    n_nearest = st.number_input(
        "Total Stations", 1, step=1, value=10, key="sta_n_nearest"
    )
    btn_coordinate = st.button(
        ":round_pushpin: Find Nearest Stations",
        use_container_width=True,
    )

is_all_valid = IS_LAT_VALID and IS_LON_VALID and is_name_valid
if not is_all_valid:
    EMOJI_CHECK = [":x:", ":heavy_check_mark:"]
    st.error(
        f"""
        Please input the coordinate information correctly.\n
        - Coordinate Name: {EMOJI_CHECK[is_name_valid]} \n
        - Latitude: {EMOJI_CHECK[IS_LAT_VALID]} \n
        - Longitude: {EMOJI_CHECK[IS_LON_VALID]} \n
        """
    )

if btn_coordinate and is_all_valid:

    point_coordinate = f"{latitude},{longitude}"

    data_with_distance = pyfunc.dataframe_calc_distance(
        point_coordinate, combined_metadata_rr
    )

    @st.cache_data
    def find_nearest_stations(data, radius, n_stations):
        """Find nearest stations based on distance and radius."""

        df_nearest_stations = (
            data.sort_values("distance")
            .round(3)
            .loc[data.distance < radius]
            .iloc[:n_stations]
        )
        return df_nearest_stations

    table_nearest_stations = find_nearest_stations(
        data_with_distance, radius_km, n_nearest
    )

    fig_nearest_stations = pyfigure.generate_nearest_stations_map(
        point_coordinate, coordinate_name, table_nearest_stations
    )

    st.session_state["table_nearest_stations"] = table_nearest_stations
    st.session_state["fig_nearest_stations"] = fig_nearest_stations

    st.session_state.prev_coordinate_name = coordinate_name
    st.session_state.prev_latitude = latitude
    st.session_state.prev_longitude = longitude

else:
    st.info("Click the button to find/update nearest stations.")



placeholder = st.empty()

if st.session_state.get("fig_nearest_stations") is not None and is_all_valid:
    with placeholder.container():
        st.divider()
        st.markdown("#### 🔍 Peta Stasiun Terdekat")
        st.markdown(
            f"###### {st.session_state.prev_coordinate_name} ({st.session_state.prev_latitude}, {st.session_state.prev_longitude})"
        )
        st.plotly_chart(st.session_state.fig_nearest_stations, use_container_width=True)
        COLS_TABLE = "title distance station_name".split()
        COLS_NAME = "ID,DATASET,DISTANCE,STATION NAME".split(",")
        with st.expander("Table Nearest Stations"):
            st.dataframe(
                st.session_state.table_nearest_stations[COLS_TABLE]
                .rename_axis("ID")
                .rename(columns=dict(zip(COLS_TABLE, COLS_NAME[1:])))
            )
        st.divider()



st.button("Refresh", key="sta_refresh")
