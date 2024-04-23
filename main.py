import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import layout

# 기본 형식
def main():
    # 화면에 관해 처리를 하고 싶다면 st를 사용해야한다.
    st.title('시각화 팀 프로젝트')
    # 대부분 main에서 작업을 한다.
    st.subheader('제주도 여행지 시각화')
    st.text('3조')
    st.markdown('**아름다운 섬 제주**, 어디로 놀러가면 좋을까?')
    layout.create_layout()
    layout.create_sidebar([], ['a', 'b'])
    layout.create_tab()
    
if __name__ == '__main__':
    main()

# number1

st.text('첫번째 지도')
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [33.4, 126.8],
    columns=['lat', 'lon'])

st.map(df)

st.text('두번째 지도')
# 점의 크기와 색상을 지정
st.map(df, size=20, color='#0044ff')

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