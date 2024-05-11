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
        "About": "Simple app to process rainfall data",
    },
)

mainfunc.load_css("assets/stations.css")
mainfunc.main_sidebar()

# INITIALIZE

combined_metadata_rr = pyfunc.read_metadata_csv("data/rainfall")
combined_metadata_comp = pyfunc.read_metadata_csv("data/completeness")
IS_SECTION_NEAREST_DONE = False

# ----------- START OF PAGE

st.title(":round_pushpin: Eksplorasi Data Hujan :round_pushpin:")
st.subheader("Mengakses dan Mengakuisisi Data Hujan")

## Introduction

# with st.expander("Pendahuluan"):
md_introduction = mainfunc.load_markdown("docs/stations/01_intro.md")
st.markdown(md_introduction, unsafe_allow_html=True)

## Map of Stations

st.markdown("## 🗺️ Peta Stasiun Pengamatan Hujan")
md_intro_maps = mainfunc.load_markdown("docs/stations/02a_intro_maps.md")
data_intro_maps = {
    "dataset_name": "Kaggle - greegtitan/indonesia-climate",
    "dataset_link": "https://www.kaggle.com/datasets/greegtitan/indonesia-climate",
    "total_stations": len(combined_metadata_rr),
}
st.markdown(md_intro_maps.format(**data_intro_maps))

fig_map = pyfigure.generate_station_map_figure(combined_metadata_rr)

tab1, tab2, tab3 = st.tabs(["Peta Stasiun", "Metadata", "Informasi Metadata"])

with tab1:
    st.plotly_chart(fig_map, use_container_width=True)

with tab2:
    st.dataframe(combined_metadata_rr)

with tab3:
    md_metadata_info = mainfunc.load_markdown("docs/stations/02b_metadata_info.md")
    with st.container(border=True):
        st.markdown(md_metadata_info, unsafe_allow_html=True)


## Input Coordinate

st.markdown("#### 📌 Titik Koordinat Tinjauan")
md_my_coordinate = mainfunc.load_markdown("docs/stations/03_my_coordinate.md")
st.markdown(md_my_coordinate, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    coordinate_name = st.text_input(
        "Coordinate Name / Nama Koordinat", "TinjauanKu", key="coordinate_name"
    )
    IS_NAME_VALID = (coordinate_name is not None) and (coordinate_name != "")

with col2:
    latitude = st.text_input("Latitude / Lintang Derajat", "-6.2631", key="latitude")
    longitude = st.text_input("Longitude / Bujur Derajat", "106.8095", key="longitude")

    IS_LAT_VALID = pyfunc.validate_single_coordinate(latitude, "lat")
    IS_LON_VALID = pyfunc.validate_single_coordinate(longitude, "lon")

with col3:
    radius_km = st.number_input("Radius (km)", 1, step=1, value=25, key="radius_km")
    n_nearest = st.number_input("Total Stations", 1, step=1, value=10, key="n_nearest")
    btn_coordinate = st.button(
        ":round_pushpin: Find Nearest Stations",
        use_container_width=True,
    )

### Validate Input

is_all_valid = IS_LAT_VALID and IS_LON_VALID and IS_NAME_VALID
if not is_all_valid:
    EMOJI_CHECK = [":x:", ":heavy_check_mark:"]
    st.error(
        f"""
        Please input the coordinate information correctly.\n
        - Coordinate Name: {EMOJI_CHECK[IS_NAME_VALID]} \n
        - Latitude: {EMOJI_CHECK[IS_LAT_VALID]} \n
        - Longitude: {EMOJI_CHECK[IS_LON_VALID]} \n
        """
    )
    st.session_state.table_nearest_stations = None
    st.session_state.fig_nearest_stations = None
    IS_SECTION_NEAREST_DONE = False

### Find Nearest Stations (table and map)

if btn_coordinate and is_all_valid:

    point_coordinate = f"{latitude},{longitude}"

    data_with_distance = pyfunc.dataframe_calc_distance(
        point_coordinate, combined_metadata_rr
    )

    @st.cache_data
    def find_nearest_stations(data, radius, n_stations, round_decimal=3):
        """Find nearest stations based on distance and radius."""

        df_nearest_stations = (
            data.sort_values("distance")
            .round(round_decimal)
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
    st.session_state.prev_radius_km = radius_km
    st.session_state.prev_n_nearest = n_nearest

### Display Nearest Stations

ph_nearest_stations = st.empty()
ph_nearest_stations.info("Click 'Find Nearest Stations' to see the result.")

if st.session_state.get("fig_nearest_stations") is not None and is_all_valid:
    with ph_nearest_stations.container():

        # Load Data
        @st.cache_data
        def table_nearest_rename_columns(df_nearest):
            """Rename columns of nearest stations table."""
            selected_columns = "title distance station_name".split()
            new_columns_name = "ID,DATASET,DISTANCE,STATION NAME".split(",")

            df_updated = (
                df_nearest[selected_columns]
                .rename_axis("ID")
                .rename(columns=dict(zip(selected_columns, new_columns_name[1:])))
            )
            return df_updated

        table_nearest_updated = table_nearest_rename_columns(
            st.session_state.table_nearest_stations
        )

        dict_nearest = {
            "coordinate_name": st.session_state.prev_coordinate_name,
            "latitude": st.session_state.prev_latitude,
            "longitude": st.session_state.prev_longitude,
            "radius_km": st.session_state.prev_radius_km,
            "n_nearest": st.session_state.prev_n_nearest,
            "total_nearest_stations": len(table_nearest_updated),
            "nearest_stations_name": ", ".join(
                table_nearest_updated["STATION NAME"].tolist()
            ),
            "closest_station_name": table_nearest_updated.iloc[0]["STATION NAME"],
            "closest_station_distance": table_nearest_updated.iloc[0]["DISTANCE"],
            "farthest_station_name": table_nearest_updated.iloc[-1]["STATION NAME"],
            "farthest_station_distance": table_nearest_updated.iloc[-1]["DISTANCE"],
        }

        # Intro Nearest Stations
        st.markdown("#### 🔍 Peta Stasiun Terdekat")
        md_intro_nearest = mainfunc.load_markdown("docs/stations/04_intro_nearest.md")
        st.markdown(md_intro_nearest.format(**dict_nearest))

        # Map Nearest Stations

        tab1, tab2 = st.tabs(["Peta Stasiun Terdekat", "Tabel Stasiun Terdekat"])

        with tab1:
            st.plotly_chart(
                st.session_state.fig_nearest_stations, use_container_width=True
            )

        with tab2:
            # Table Nearest Stations
            # with st.expander("Table Nearest Stations"):
            st.dataframe(table_nearest_updated)

        # Summary Nearest Stataions
        md_sum_nearest = mainfunc.load_markdown("docs/stations/05_sum_nearest.md")
        st.markdown(md_sum_nearest.format(**dict_nearest))

        IS_SECTION_NEAREST_DONE = True


## Completeness Data

st.markdown("### 📊 Data Kelengkapan Pengamatan")

placeholder_completeness = st.empty()
placeholder_completeness.info("Complete Nearest Stations to continue.")

if IS_SECTION_NEAREST_DONE:

    # LOAD DATA
    md_intro_complete = mainfunc.load_markdown("docs/stations/06_intro_complete.md")
    md_intro_heatmap = mainfunc.load_markdown("docs/stations/07_intro_heatmap.md")
    md_sum_heatmap = mainfunc.load_markdown("docs/stations/08_sum_heatmap.md")
    nearest_stations_list = table_nearest_updated.index.tolist()

    dataframe_comp = pyfunc.get_dataframe_from_folder(
        nearest_stations_list, combined_metadata_comp, "data/completeness"
    )

    fig_completeness = pyfigure.generate_completeness_heatmap(
        dataframe_comp, combined_metadata_comp
    )

    graph_bars = []
    bar_names = []

    for stat_id in nearest_stations_list:
        _series = dataframe_comp[stat_id].dropna()
        _bar = pyfigure.generate_completeness_bar(_series, combined_metadata_comp)
        _name = combined_metadata_comp.loc[stat_id, "station_name"]
        graph_bars.append(_bar)
        bar_names.append(_name)

    # DISPLAY
    with placeholder_completeness.container():

        # Intro Completeness
        st.markdown(md_intro_complete)

        # Completeness Heatmap
        st.markdown("###### 🎲 Heatmap Kelengkapan Data")
        st.markdown(md_intro_heatmap.format(**dict_nearest))

        tab1, tab2, tab3 = st.tabs(
            [
                "Heatmap Kelengkapan",
                "Tabel Kelengkapan Data",
                "Grafik Bar Kelengkapan Data",
            ]
        )

        with tab1:
            st.plotly_chart(
                fig_completeness,
                use_container_width=True,
                config={"displayModeBar": False},
            )
        with tab2:
            st.dataframe(dataframe_comp)
        with tab3:
            for i, tab in enumerate(bar_names):
                st.markdown(f"###### 🌧️ {tab}")
                st.plotly_chart(
                    graph_bars[i],
                    use_container_width=True,
                    config={"displayModeBar": False},
                )

        # st.markdown(md_sum_heatmap)
        with st.expander("Analisis Data Kelengkapan"):
            text_analysis_complete = st.text_area(
                "Masukan analisis kamu",
                value=md_sum_heatmap,
                height=200,
                key="text_analysis_complete",
            )

        if st.session_state.text_analysis_complete:
            st.markdown(st.session_state.text_analysis_complete)


st.button("Refresh", key="sta_refresh")
