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
        "IS_NEAREST_SECTION_DONE": False,
        "GPT_RESPONSE_COMPLETENESS": None,
        "GPT_RESPONSE_RAINFALL": None,
        "coordinate_name": "Queensdale",
        "latitude": "-6.2631",
        "longitude": "106.8095",
        "radius_km": 25,
        "nearest_stations_limit": 10,
        "gpt_model": "gpt-4o",
    }
)

# LOAD CSS & SIDEBAR
mainfunc.load_css("assets/stations.css")
mainfunc.main_sidebar()


# START OF LAYOUT SECTION #################################
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
    st.header("Station Configuration", anchor=False, divider="grey")
    st.text_input("OpenAI API Key", type="password", key="openai_api_key")
    st.selectbox(
        "Select Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], key="gpt_model"
    )

# HEADER SECTION -------------------------------------------
# HEADER - TITLE SECTION -----------------------------------
st.title(PAGE_TITLES["title"], anchor="rainitas-stations")
st.subheader(PAGE_TITLES["subtitle"], anchor=False)

# HEADER - ABSTRACT SECTION --------------------------------
layout_abstract = st.empty()

# MAIN SECTION ---------------------------------------------
# MAIN - MAP SECTION ---------------------------------------
st.header(PAGE_TITLES["title_map"], anchor="map", divider="blue")
layout_map_intro = st.empty()
layout_map_figure = st.empty()

# MAIN - MAP COORDINATE SECTION ----------------------------
st.header(PAGE_TITLES["title_map_coordinate"], anchor="map-coordinate", divider="red")
layout_map_coordinate_intro = st.empty()
layout_map_input = st.empty()
layout_map_update = st.empty()
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
layout_heatmap_gpt = st.empty()
layout_heatmap_summary = st.empty()

# MAIN - RAINFALL SECTION ----------------------------------
st.header(PAGE_TITLES["title_rainfall"], anchor="rainfall", divider="blue")
layout_rainfall_intro = st.empty()
layout_rainfall_figure = st.empty()
layout_rainfall_figure.warning("Complete Nearest Stations to continue.")
layout_rainfall_gpt = st.empty()
layout_rainfall_summary = st.empty()

# MAIN - CLOSING SECTION -----------------------------------
st.header(PAGE_TITLES["title_closing"], anchor="closing", divider="blue")
layout_closing = st.empty()
layout_closing.warning("Complete all sections to finish.")

# FOOTER SECTION -------------------------------------------
layout_footer = st.empty()

# END OF LAYOUT SECTION ------------------------------------


# LOAD DATA & TEXT
metadata_rainfall, metadata_completeness = stationsfunc.load_metadata()
markdown_templates, prompt_templates = stationsfunc.load_templates()

# LAYOUT DETAILS
# DETAIL - HEADER SECTION -----------------------------------
# DETAIL - HEADER - ABSTRACT
text_abstract = markdown_templates["abstract"]
with layout_abstract.container():
    st.markdown(text_abstract, unsafe_allow_html=True)

# DETAIL - MAIN SECTION -------------------------------------
# DETAIL - MAIN - MAP
DATASET_INFO = {
    "dataset_name": "Kaggle - greegtitan/indonesia-climate",
    "dataset_link": "https://www.kaggle.com/datasets/greegtitan/indonesia-climate",
}
DATASET_STATS = {
    "total_stations": len(metadata_rainfall),
}
TABTITLE_MAP = ["Peta Stasiun", "Tabel Metadata Stasiun", "Informasi Dataset"]

text_map_intro = markdown_templates["map_intro"].format(**DATASET_INFO, **DATASET_STATS)
text_map_info = markdown_templates["map_info"]
fig_map = pyfigure.generate_station_map_figure(metadata_rainfall)

with layout_map_intro.container():
    st.markdown(text_map_intro)
with layout_map_figure.container():
    tabs_map = st.tabs(TABTITLE_MAP)
    with tabs_map[0]:
        st.plotly_chart(fig_map, use_container_width=True)
    with tabs_map[1]:
        st.dataframe(metadata_rainfall, use_container_width=True)
    with tabs_map[2]:
        st.markdown(text_map_info, unsafe_allow_html=True)

# DETAIL - MAIN - MAP COORDINATE // INPUT
with layout_map_coordinate_intro:
    st.markdown(markdown_templates["map_coordinate"])

LABELS_COORDINATE = {
    "coordinate_name": "Coordinate Name",
    "latitude": "Latitude / Lintang Derajat",
    "longitude": "Longitude / Bujur Derajat",
    "radius_km": "Radius (km)",
    "nearest_stations_limit": "Maximum Number of Nearest Stations",
    "btn_find_nearest": ":round_pushpin: Find Nearest Stations",
}

with layout_map_input.container():
    cols_map = st.columns(3)
    with cols_map[0]:
        st.text_input(
            LABELS_COORDINATE["coordinate_name"],
            state.coordinate_name,
            key="coordinate_name",
        )
    with cols_map[1]:
        st.text_input(LABELS_COORDINATE["latitude"], state.latitude, key="latitude")
        st.text_input(LABELS_COORDINATE["longitude"], state.longitude, key="longitude")
    with cols_map[2]:
        st.number_input(
            LABELS_COORDINATE["radius_km"],
            min_value=1,
            step=1,
            value=state.radius_km,
            key="radius_km",
        )
        st.number_input(
            LABELS_COORDINATE["nearest_stations_limit"],
            min_value=1,
            value=state.nearest_stations_limit,
            key="nearest_stations_limit",
        )
        btn_find_nearest = st.button(
            LABELS_COORDINATE["btn_find_nearest"],
            use_container_width=True,
            type="primary",
        )

# BUTTONS SECTION ------------------------------------------
with layout_heatmap_gpt.expander("Generate Analysis Using 🤖 GPT"):
    btn_generate_completeness = st.button(
        "Generate analysis of completeness", use_container_width=True
    )
with layout_rainfall_gpt.expander("Generate Analysis Using 🤖 GPT"):
    btn_generate_rainfall = st.button(
        "Generate analysis of rainfall", use_container_width=True
    )

with layout_footer:
    st.divider()
    btn_refresh = st.button("Refresh", use_container_width=True)


IS_COORDINATE_VALID = stationsfunc.validate_input(
    state.coordinate_name, state.latitude, state.longitude, layout_map_validate
)

if btn_find_nearest and IS_COORDINATE_VALID:
    # SAVE VALID COORDINATE INFO
    mainfunc.session_state_update(
        {
            "valid_coordinate_name": state.coordinate_name,
            "valid_latitude": state.latitude,
            "valid_longitude": state.longitude,
            "valid_radius_km": state.radius_km,
            "valid_nearest_stations_limit": state.nearest_stations_limit,
        }
    )

    valid_coordinate_info = {
        "coordinate_name": state.valid_coordinate_name,
        "latitude": state.valid_latitude,
        "longitude": state.valid_longitude,
        "radius_km": state.valid_radius_km,
        "nearest_stations_limit": state.valid_nearest_stations_limit,
    }

    # CALCULATE NEAREST STATIONS
    coordinate_point = f"{state.latitude},{state.longitude}"
    table_nearest_stations = stationsfunc.get_nearest_stations(
        coordinate_point,
        metadata_rainfall,
        state.radius_km,
        state.nearest_stations_limit,
    )
    fig_nearest_stations = pyfigure.generate_nearest_stations_map(
        coordinate_point, state.coordinate_name, table_nearest_stations
    )

    mainfunc.session_state_update(
        {
            "table_nearest_stations": table_nearest_stations,
            "fig_nearest_stations": fig_nearest_stations,
        }
    )

    table_nearest_updated = stationsfunc.rename_table_nearest(
        state.table_nearest_stations
    )

    nearest_stats = {
        "total_nearest_stations": len(table_nearest_updated),
        "nearest_stations_name": ", ".join(
            table_nearest_updated["STATION NAME"].tolist()
        ),
        "closest_station_name": table_nearest_updated.iloc[0]["STATION NAME"],
        "closest_station_distance": table_nearest_updated.iloc[0]["DISTANCE"],
        "farthest_station_name": table_nearest_updated.iloc[-1]["STATION NAME"],
        "farthest_station_distance": table_nearest_updated.iloc[-1]["DISTANCE"],
    }

    text_nearest_intro = markdown_templates["nearest_intro"].format(
        **valid_coordinate_info, **nearest_stats
    )
    text_nearest_summary = markdown_templates["nearest_summary"].format(
        **valid_coordinate_info, **nearest_stats
    )

    mainfunc.session_state_update(
        {
            "table_nearest_updated": table_nearest_updated,
            "valid_coordinate_info": valid_coordinate_info,
            "nearest_stats": nearest_stats,
            "text_nearest_intro": text_nearest_intro,
            "text_nearest_summary": text_nearest_summary,
        }
    )

    # COMPLETENESS HEATMAP/BAR

    nearest_station_ids = table_nearest_updated.index.tolist()

    completeness_df = pyfunc.get_dataframe_from_folder(
        nearest_station_ids, metadata_completeness, "data/completeness"
    )

    fig_heatmap = pyfigure.generate_completeness_heatmap(
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
        "table_nearest_stations": table_nearest_updated.to_markdown(),
        "table_completeness_data": completeness_df.to_markdown(),
    }

    prompt_completeness = prompt_templates["completeness"].format(**data_completeness)
    text_heatmap_intro = markdown_templates["heatmap_intro"].format(
        **valid_coordinate_info, **nearest_stats
    )

    mainfunc.session_state_update(
        {
            "completeness_df": completeness_df,
            "fig_heatmap": fig_heatmap,
            "figs_bar_completeness": figs_bar_completeness,
            "names_bar_completeness": names_bar_completeness,
            "nearest_station_ids": nearest_station_ids,
            "prompt_completeness": prompt_completeness,
            "text_heatmap_intro": text_heatmap_intro,
        }
    )

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
        "table_nearest_stations": table_nearest_updated.to_markdown(),
        "table_describe_rainfall": rainfall_df.describe().to_markdown(),
    }

    prompt_rainfall = prompt_templates["rainfall"].format(**data_rainfall)
    text_rainfall_intro = markdown_templates["rainfall_intro"].format(
        **{"list_of_nearest_stations": "\n".join(nearest_ids_names)}
    )

    mainfunc.session_state_update(
        {
            "fig_rainfall": fig_rainfall,
            "rainfall_df": rainfall_df,
            "prompt_rainfall": prompt_rainfall,
            "text_rainfall_intro": text_rainfall_intro,
        }
    )

    state.IS_NEAREST_SECTION_DONE = True

# DISPLAY RESULT (LAYOUT) ###################################

if state.IS_NEAREST_SECTION_DONE:
    with layout_nearest_intro.container():
        st.markdown(state.text_nearest_intro)

    TABTITLE_NEAREST = ["Peta Stasiun Terdekat", "Tabel Stasiun Terdekat"]
    with layout_nearest_map.container():
        tabs_nearest_map = st.tabs(TABTITLE_NEAREST)
        with tabs_nearest_map[0]:
            st.plotly_chart(state.fig_nearest_stations, use_container_width=True)
        with tabs_nearest_map[1]:
            st.dataframe(state.table_nearest_updated, use_container_width=True)

    with layout_nearest_summary.container():
        st.markdown(state.text_nearest_summary)

    with layout_completeness_intro.container():
        st.markdown(markdown_templates["completeness_intro"])

    with layout_heatmap_intro.container():
        st.markdown(state.text_heatmap_intro)

    with layout_heatmap_figure.container():
        TABTITLE_COMPLETENESS = [
            "Heatmap Kelengkapan",
            "Tabel Kelengkapan Data",
            "Grafik Bar Kelengkapan Data",
        ]

        tabs_completeness = st.tabs(TABTITLE_COMPLETENESS)

        with tabs_completeness[0]:
            st.plotly_chart(
                state.fig_heatmap,
                use_container_width=True,
                config={"displayModeBar": False},
            )
        with tabs_completeness[1]:
            st.dataframe(state.completeness_df, use_container_width=True)
        with tabs_completeness[2]:
            for station_id, station_name, fig_bar in zip(
                state.nearest_station_ids,
                state.names_bar_completeness,
                state.figs_bar_completeness,
            ):
                st.markdown(f"###### 🌧️ {station_id} - {station_name} 🌧️")
                st.plotly_chart(
                    fig_bar,
                    use_container_width=True,
                    config={"displayModeBar": False},
                )

    with layout_rainfall_intro.container():
        st.markdown(state.text_rainfall_intro)

    with layout_rainfall_figure.container():
        TABTITLE_RAINFALL = [
            "Grafik Hujan Harian",
            "Tabel Hujan Harian",
            "Statistik Hujan Harian",
        ]

        tabs_rainfall = st.tabs(TABTITLE_RAINFALL)

        with tabs_rainfall[0]:
            st.plotly_chart(
                state.fig_rainfall,
                use_container_width=True,
                config={"displayModeBar": False},
            )
        with tabs_rainfall[1]:
            st.dataframe(state.rainfall_df, use_container_width=True)
        with tabs_rainfall[2]:
            st.dataframe(state.rainfall_df.describe(), use_container_width=True)

    layout_closing.markdown(markdown_templates["closing"])

# GPT SECTION ################################################

if state.IS_NEAREST_SECTION_DONE:
    stationsfunc.render_gpt_result(
        btn_generate_completeness,
        layout_heatmap_summary,
        state.prompt_completeness,
        state.gpt_model,
        state.openai_api_key,
        "GPT_RESPONSE_COMPLETENESS",
        "GPT_PROMPT_COMPLETENESS",
        markdown_templates["heatmap_summary"],
    )

    stationsfunc.render_gpt_result(
        btn_generate_rainfall,
        layout_rainfall_summary,
        state.prompt_rainfall,
        state.gpt_model,
        state.openai_api_key,
        "GPT_RESPONSE_RAINFALL",
        "GPT_PROMPT_RAINFALL",
        markdown_templates["rainfall_summary"],
    )

# REFRESH BUTTON
if btn_refresh:
    layout_heatmap_gpt.empty()
    layout_rainfall_gpt.empty()
