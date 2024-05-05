import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import print_plots
import os
import geopandas as gpd
from ipywidgets import interact, Dropdown
from dotenv import load_dotenv
load_dotenv()
# 여행지 방문 데이터 불러오기
# @st.cache 
data = pd.read_csv("data/data_file.csv")
data.dropna(inplace=True)

# 지도 초기 위치 설정
map_center = [data['GPS Y좌표'].mean(),data['GPS X좌표'].mean()]
multi_select_columns = ['성별', '연령대', '소득수준', '동반 여행 종류', '동반 인원수', '동반자 관계', '동반자 연령대', '방문지명', 
       '여행지 유형', '만족도', '추천 의향 점수', '활동 유형', '소비인원', '결제금액',
       '여행동기_1', '여행동기_2', '여행동기_3', '동반자 성별',
       '1순위 여행목적', '2순위 여행목적', '3순위 여행목적', '여행 시작 월', '여행 시작 연도',
       '여행자 유형']


print(multi_select_columns)

# 연아
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['GPS X좌표'], data['GPS Y좌표']))
gdf.crs = "EPSG:4326"  # 원본 데이터의 좌표계 설정
gdf = gdf.to_crs(epsg=3857)  # Web Mercator 좌표계로 변환


# 스트림릿 앱 제목 설정
st.title('여행지 방문 데이터 시각화 - 도은 수정중~~~')
st.sidebar.title('this is sidebar')
# 성별 및 연령대 필터링 옵션 추가
multi_selected = st.sidebar.multiselect('구분자 선택', multi_select_columns)
if multi_selected=='여행자 유형':
    여행자_유형 = ['자연 vs 도시', '숙박 vs 당일', '새로운 지역 vs 익숙한 지역','편하지만 비싼 숙소 vs 불편하지만 저렴한 숙소', '휴양/휴식 vs 체험활동',
       '잘 알려지지 않은 방문지 vs 알려진 방문지', '계획에 따른 여행 vs 상황에 따른 여행','사진촬영 중요하지 않음 vs 사진촬영 중요함']
    radio = st.sidebar.radio("여행자 유형을 선택하세욤",여행자_유형)

print(multi_selected)

start_button = st.sidebar.button(
    "filter apply 📊 "#"버튼에 표시될 내용"
)

st.set_option('deprecation.showPyplotGlobalUse', False)
if start_button:    
    # 필터링된 데이터셋 만들기
    filtered_data = data
    for selected_구분자 in multi_selected:
        st.plotly_chart(print_plots.print_map_column(filtered_data, selected_구분자))
        st.plotly_chart(print_plots.print_pie_chart(filtered_data, selected_구분자))

    if len(multi_selected) == 2:
        print_plots.print_twoway_heatmap(filtered_data, multi_selected)
        st.pyplot()
    
    
trip_types = gdf['동반 여행 종류'].unique()
dropdown = Dropdown(options=trip_types)
interact(print_plots.plot_data, gdf=gdf, trip_type=dropdown)