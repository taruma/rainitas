"""Station page"""

import streamlit as st
import plotly.io as pio

from src.stations import pyfunc, pyfigure
from src.stations import pytemplate
from src import mainfunc, stationsfunc

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
mainfunc.load_state()
mainfunc.main_sidebar()

# INITIALIZE / LOAD DATA

metadata_rainfall = pyfunc.read_metadata_csv("data/rainfall")
metadata_completeness = pyfunc.read_metadata_csv("data/completeness")

# SESSION STATE INITIALIZATION
mainfunc.create_to_session(
    {
        "IS_INPUT_VALID": False,
        "IS_NEAREST_SECTION_DONE": False,
        "GPT_RESPONSE_COMPLETENESS": None,
        "GPT_RESPONSE_RAINFALL": None,
    }
)

# LAYOUT

layout_title = st.empty()
layout_intro = st.empty()

st.markdown("## 🗺️ Peta Stasiun Pengamatan Hujan")
layout_map_intro = st.empty()
layout_map_figure = st.empty()

st.markdown("#### 📌 Titik Koordinat Tinjauan")
layout_map_input = st.empty()
layout_map_validate = st.empty()

st.markdown("#### 🔍 Peta Stasiun Terdekat")
layout_nearest_intro = st.empty()
layout_nearest_map = st.empty()
layout_nearest_map.warning("Click 'Find Nearest Stations' to see the result.")
layout_nearest_summary = st.empty()

st.markdown("### 📊 Data Kelengkapan Pengamatan")
layout_completeness_intro = st.empty()
layout_completeness_intro.warning("Complete Nearest Stations to continue.")

st.markdown("##### 🎲 Heatmap & Grafik Bar Kelengkapan Data")
layout_completeness_heatmap_intro = st.empty()
layout_completeness_heatmap_figure = st.empty()
layout_completeness_heatmap_figure.warning("Complete Nearest Stations to continue.")
layout_completeness_button = st.empty()

with layout_completeness_button.expander("Generate Analysis Using 🤖 GPT"):
    st.text_input("OpenAI API Key", type="password", key="openai_api_key")
    st.selectbox("Select Model", ["gpt-3.5-turbo", "gpt-4-turbo"], key="gpt_model")
    btn_generate_completeness = st.button(
        "Generate analysis of completeness",
        use_container_width=True,
        disabled=False,
    )

layout_completeness_heatmap_summary = st.empty()

st.markdown("##### 👓 Grafik Hujan Harian")
layout_rainfall_intro = st.empty()
layout_rainfall_figure = st.empty()
layout_rainfall_figure.warning("Complete Nearest Stations to continue.")
layout_rainfall_button = st.empty()

with layout_rainfall_button.expander("Generate Analysis Using 🤖 GPT"):
    btn_generate_rainfall = st.button(
        "Generate analysis of rainfall", use_container_width=True, disabled=False
    )

layout_rainfall_summary = st.empty()

st.markdown("## 🚪 Penutup")
layout_closing = st.empty()
layout_closing.warning("Complete all sections to finish.")

# LOAD MD
md_introduction = mainfunc.load_markdown("docs/stations/01_intro.md")
md_map_intro = mainfunc.load_markdown("docs/stations/02a_maps_intro.md")
md_map_info = mainfunc.load_markdown("docs/stations/02b_maps_info.md")
md_map_input_coordinate = mainfunc.load_markdown(
    "docs/stations/02c_map_input_coordinate.md"
)
md_nearest_intro = mainfunc.load_markdown("docs/stations/03a_nearest_intro.md")
md_nearest_sum = mainfunc.load_markdown("docs/stations/03b_nearest_sum.md")
md_completeness_intro = mainfunc.load_markdown("docs/stations/04_complete_intro.md")
md_heatmap_intro = mainfunc.load_markdown("docs/stations/05a_heatmap_intro.md")
md_heatmap_sum = mainfunc.load_markdown("docs/stations/05b_heatmap_sum.md")
md_rainfall_intro = mainfunc.load_markdown("docs/stations/06a_rainfall_intro.md")
md_rainfall_sum = mainfunc.load_markdown("docs/stations/06b_rainfall_sum.md")
md_closing = mainfunc.load_markdown("docs/stations/07_closing.md")

# MAIN APPS

data_intro_maps = {
    "dataset_name": "Kaggle - greegtitan/indonesia-climate",
    "dataset_link": "https://www.kaggle.com/datasets/greegtitan/indonesia-climate",
    "total_stations": len(metadata_rainfall),
}

fig_map = pyfigure.generate_station_map_figure(metadata_rainfall)

# ----------- START OF PAGE

with layout_title.container():
    st.title(":round_pushpin: Eksplorasi Data Hujan :round_pushpin:")
    st.subheader("Mengakses dan Mengakuisisi Data Hujan")

## Introduction

with layout_intro.container():
    st.markdown(md_introduction, unsafe_allow_html=True)

## Map of Stations

with layout_map_intro.container():
    st.markdown(md_map_intro.format(**data_intro_maps))

with layout_map_figure.container():
    tab1, tab2, tab3 = st.tabs(["Peta Stasiun", "Tabel Metadata Stasiun", "Informasi Dataset"])

    with tab1:
        st.plotly_chart(fig_map, use_container_width=True)
    with tab2:
        st.dataframe(metadata_rainfall)
    with tab3:
        with st.container(border=True):
            st.markdown(md_map_info, unsafe_allow_html=True)


## Input Coordinate

with layout_map_input.container():
    st.markdown(md_map_input_coordinate, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        coordinate_name = st.text_input(
            "Coordinate Name / Nama Koordinat", "TinjauanKu", key="coordinate_name"
        )

    with col2:
        latitude = st.text_input(
            "Latitude / Lintang Derajat", "-6.2631", key="latitude"
        )
        longitude = st.text_input(
            "Longitude / Bujur Derajat", "106.8095", key="longitude"
        )

    with col3:
        radius_km = st.number_input("Radius (km)", 1, step=1, value=25, key="radius_km")
        num_nearest = st.number_input(
            "Total Stations", 1, step=1, value=10, key="num_nearest"
        )
        btn_coordinate = st.button(
            ":round_pushpin: Find Nearest Stations",
            use_container_width=True,
            type="primary"
        )

### Validate Input

IS_NAME_VALID = (coordinate_name is not None) and (coordinate_name != "")
IS_LAT_VALID = pyfunc.validate_single_coordinate(latitude, "lat")
IS_LON_VALID = pyfunc.validate_single_coordinate(longitude, "lon")

is_all_valid = IS_LAT_VALID and IS_LON_VALID and IS_NAME_VALID

if not is_all_valid:
    EMOJI_CHECK = [":x:", ":heavy_check_mark:"]
    layout_map_validate.error(
        f"""
        Please input the coordinate information correctly.\n
        - Coordinate Name: {EMOJI_CHECK[IS_NAME_VALID]} \n
        - Latitude: {EMOJI_CHECK[IS_LAT_VALID]} \n
        - Longitude: {EMOJI_CHECK[IS_LON_VALID]} \n
        """
    )
    st.session_state.table_nearest_stations = None
    st.session_state.fig_nearest_stations = None
    st.session_state.IS_NEAREST_SECTION_DONE = False

### Find Nearest Stations (table and map)

if btn_coordinate and is_all_valid:
    coordinate_point = f"{latitude},{longitude}"

    table_nearest_stations = stationsfunc.get_nearest_stations(
        coordinate_point, metadata_rainfall, radius_km, num_nearest
    )

    fig_nearest_stations = pyfigure.generate_nearest_stations_map(
        coordinate_point, coordinate_name, table_nearest_stations
    )

    mainfunc.update_to_session(
        {
            "table_nearest_stations": table_nearest_stations,
            "fig_nearest_stations": fig_nearest_stations,
            "prev_coordinate_name": coordinate_name,
            "prev_latitude": latitude,
            "prev_longitude": longitude,
            "prev_radius_km": radius_km,
            "prev_num_nearest": num_nearest,
        }
    )

### Display Nearest Stations

if st.session_state.get("fig_nearest_stations") is not None and is_all_valid:

    table_nearest_updated = stationsfunc.rename_table_nearest(
        st.session_state.table_nearest_stations
    )

    dict_nearest = {
        "coordinate_name": st.session_state.prev_coordinate_name,
        "latitude": st.session_state.prev_latitude,
        "longitude": st.session_state.prev_longitude,
        "radius_km": st.session_state.prev_radius_km,
        "n_nearest": st.session_state.prev_num_nearest,
        "total_nearest_stations": len(table_nearest_updated),
        "nearest_stations_name": ", ".join(
            table_nearest_updated["STATION NAME"].tolist()
        ),
        "closest_station_name": table_nearest_updated.iloc[0]["STATION NAME"],
        "closest_station_distance": table_nearest_updated.iloc[0]["DISTANCE"],
        "farthest_station_name": table_nearest_updated.iloc[-1]["STATION NAME"],
        "farthest_station_distance": table_nearest_updated.iloc[-1]["DISTANCE"],
    }

    with layout_nearest_intro.container():
        st.markdown(md_nearest_intro.format(**dict_nearest))

    with layout_nearest_map.container():
        tab1, tab2 = st.tabs(["Peta Stasiun Terdekat", "Tabel Stasiun Terdekat"])

        with tab1:
            st.plotly_chart(
                st.session_state.fig_nearest_stations, use_container_width=True
            )
        with tab2:
            st.dataframe(table_nearest_updated)

    with layout_nearest_summary.container():
        st.markdown(md_nearest_sum.format(**dict_nearest))

    st.session_state.IS_NEAREST_SECTION_DONE = True


## Completeness Data

if st.session_state.IS_NEAREST_SECTION_DONE:

    ids_nearest_stations = table_nearest_updated.index.tolist()

    completeness_df = pyfunc.get_dataframe_from_folder(
        ids_nearest_stations, metadata_completeness, "data/completeness"
    )

    fig_completeness = pyfigure.generate_completeness_heatmap(
        completeness_df, metadata_completeness
    )

    graph_bars = []
    bar_names = []

    for stat_id in ids_nearest_stations:
        _series = completeness_df[stat_id].dropna()
        _bar = pyfigure.generate_completeness_bar(_series, metadata_completeness)
        _name = metadata_completeness.loc[stat_id, "station_name"]
        graph_bars.append(_bar)
        bar_names.append(_name)

    mainfunc.update_to_session(
        {
            "nearest_stations_list": ids_nearest_stations,
            "completeness_df": completeness_df,
            "fig_completeness": fig_completeness,
            "graph_bars": graph_bars,
            "bar_names": bar_names,
        }
    )

    # DISPLAY
    with layout_completeness_intro.container():
        st.markdown(md_completeness_intro)

    with layout_completeness_heatmap_intro.container():
        st.markdown(md_heatmap_intro.format(**dict_nearest))

    with layout_completeness_heatmap_figure.container():
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
            st.dataframe(completeness_df)
        with tab3:
            for (i, tab), station_id in zip(enumerate(bar_names), ids_nearest_stations):
                st.markdown(f"###### 🌧️ {station_id} - {tab} 🌧️")
                st.plotly_chart(
                    graph_bars[i],
                    use_container_width=True,
                    config={"displayModeBar": False},
                )

    if btn_generate_completeness:
        with layout_completeness_heatmap_summary.container():
            with st.spinner("Generating Analysis..."):
                dict_comp_analysis = {
                    "table_nearest_stations_csv": st.session_state.table_nearest_stations.to_csv(),
                    "table_completeness_data_csv": completeness_df.to_csv(),
                }

                md_prompt_generate_analysis = mainfunc.load_markdown(
                    "prompt/stations/prompt_completeness.md"
                )

                generated_analysis = mainfunc.generate_gpt(
                    prompt=md_prompt_generate_analysis.format(**dict_comp_analysis),
                    model=st.session_state.gpt_model,
                    openai_api_key=st.session_state.openai_api_key,
                )

                mainfunc.update_to_session(
                    {
                        "GPT_RESPONSE_COMPLETENESS": generated_analysis,
                        "GPT_PROMPT_COMPLETENESS": md_prompt_generate_analysis.format(
                            **dict_comp_analysis
                        ),
                    }
                )

    if st.session_state.GPT_RESPONSE_COMPLETENESS is not None:
        with layout_completeness_heatmap_summary.container():
            with st.expander("View Prompt"):
                st.code(st.session_state.GPT_PROMPT_COMPLETENESS)
            st.markdown(st.session_state.GPT_RESPONSE_COMPLETENESS)
    else:
        with layout_completeness_heatmap_summary.container(border=True):
            st.markdown(md_heatmap_sum, unsafe_allow_html=True)

    ### GRAFIK HUJAN HARIAN

    id_name_nearest_stations = []
    for ids, station_name in zip(
        ids_nearest_stations, table_nearest_updated["STATION NAME"]
    ):
        id_name_nearest_stations.append(
            f"1. `{ids}` - :green-background[**{station_name}**]"
        )

    rainfall_df = pyfunc.get_dataframe_from_folder(
        ids_nearest_stations, metadata_rainfall, "data/rainfall"
    )

    pyfunc.replace_unmeasured_data(rainfall_df)

    fig_rainfall = pyfigure.generate_rainfall_scatter(rainfall_df, metadata_rainfall)

    with layout_rainfall_intro.container():
        st.markdown(
            md_rainfall_intro.format(
                **{"list_of_nearest_stations": "\n".join(id_name_nearest_stations)}
            )
        )

    with layout_rainfall_figure.container():

        lrtab1, lrtab2, lrtab3 = st.tabs(
            ["Grafik Hujan Harian", "Tabel Hujan Harian", "Statistik Hujan Harian"]
        )

        with lrtab1:
            st.plotly_chart(
                fig_rainfall, use_container_width=True, config={"displayModeBar": False}
            )
        with lrtab2:
            st.dataframe(rainfall_df)
        with lrtab3:
            st.dataframe(rainfall_df.describe())

    if btn_generate_rainfall:
        with layout_rainfall_summary.container():
            with st.spinner("Generating Analysis..."):
                data_md_rainfall = {
                    "table_nearest_stations_csv": st.session_state.table_nearest_stations.to_csv(),
                    "table_describe_rainfall_csv": rainfall_df.describe().to_csv(),
                }

                md_prompt_rainfall_data = mainfunc.load_markdown(
                    "prompt/stations/prompt_rainfall_data.md"
                )

                generated_rainfall_analysis = mainfunc.generate_gpt(
                    prompt=md_prompt_rainfall_data.format(**data_md_rainfall),
                    model=st.session_state.gpt_model,
                    openai_api_key=st.session_state.openai_api_key,
                )

                mainfunc.update_to_session(
                    {
                        "GPT_RESPONSE_RAINFALL": generated_rainfall_analysis,
                        "GPT_PROMPT_RAINFALL": md_prompt_rainfall_data.format(
                            **data_md_rainfall
                        ),
                    }
                )

    if st.session_state.get("GPT_RESPONSE_RAINFALL") is not None:
        with layout_rainfall_summary.container():
            with st.expander("View Prompt"):
                st.code(st.session_state.GPT_PROMPT_RAINFALL)
            st.markdown(st.session_state.GPT_RESPONSE_RAINFALL)
    else:
        with layout_rainfall_summary.container(border=True):
            st.markdown(md_rainfall_sum, unsafe_allow_html=True)

    layout_closing.markdown(md_closing)


# REFRESH BUTTON
st.divider()
st.button("Refresh")
