import numpy as np # type: ignore
import pandas as pd # type: ignore
import streamlit as st # type: ignore
import altair as alt # type: ignore
import pydeck as pdk # type: ignore

def print_map():
    st.text('첫번째 지도')
    df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [33.4, 126.8],
    columns=['lat', 'lon'])
    st.map(df)

    st.text('두번째 지도')
    # 점의 크기와 색상을 지정
    st.map(df, size=10, color='#0044ff')

    st.text('세번째 지도')
    df = pd.DataFrame({
        "col1": np.random.randn(1000) / 50 + 37.76,
        "col2": np.random.randn(1000) / 50 + -122.4,
        "col3": np.random.randn(1000) * 100,
        "col4": np.random.rand(1000, 4).tolist(),
    })

    st.map(df,
        latitude='col1',
        longitude='col2',
        size='col3',
        color='col4')

    chart_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
            'hexagonLayer',
            data=chart_data,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=chart_data,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))