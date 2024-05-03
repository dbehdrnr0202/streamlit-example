import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# 여행지 방문 데이터 불러오기
# @st.cache 
data = pd.read_csv("data/data_file.csv")
data.dropna(inplace=True)

# 지도 초기 위치 설정
map_center = [data['GPS Y좌표'].mean(),data['GPS X좌표'].mean()]

# 스트림릿 앱 제목 설정
st.title('여행지 방문 데이터 시각화')
st.sidebar.title('this is sidebar')
# 성별 및 연령대 필터링 옵션 추가
multi_selected = st.sidebar.multiselect('구분자 선택', data.columns)

selected_radio =  {}
for selected_구분자 in multi_selected:
    selected_radio[selected_구분자] = st.sidebar.radio(selected_구분자, data[selected_구분자].unique())
    
start_button = st.sidebar.button(
    "filter apply 📊 "#"버튼에 표시될 내용"
)
if start_button:    
    # 필터링된 데이터셋 만들기
    filtered_data = data
    print("멀티 셀렉티드",multi_selected)
    print("라디오", selected_radio)
    for selected_구분자 in multi_selected:
        filtered_data = filtered_data[filtered_data[selected_구분자].isin(list(selected_radio[selected_구분자]))]
        # print(filtered_data)
    # Folium을 사용하여 지도에 점 표시하기
    map = folium.Map(location=map_center, zoom_start=11)
    # folium.CircleMarker(location=(map_center[0],map_center[1]), radius=5, color='blue', fill=True).add_to(map)

    for index, row in filtered_data.iterrows():
        folium.CircleMarker(location=(row['GPS Y좌표'], row['GPS X좌표']), radius=5, color='blue', fill=True).add_to(map)

    # Folium 지도를 스트림릿에 추가
    folium_static(map)
