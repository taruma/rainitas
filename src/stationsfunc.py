"""Function for stations page."""

import streamlit as st
from src.stations import pyfunc


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
