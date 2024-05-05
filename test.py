import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# 여행지 방문 데이터 불러오기
# @st.cache 
data = pd.read_csv("final_df_0425.csv")
data.dropna(inplace=True)

# 지도 초기 위치 설정
map_center = [data['GPS Y좌표'].mean(),data['GPS X좌표'].mean()]

# 스트림릿 앱 제목 설정
st.title('여행지 방문 데이터 시각화')

# 성별 및 연령대 필터링 옵션 추가
gender = st.selectbox('성별 선택', ['남성', '여성'])
age_range = st.slider('연령대 선택', min_value=0, max_value=100, value=(0, 100))
gender_dict = {"남성":"남", "여성":'여'}

# 필터링된 데이터셋 만들기
filtered_data = data
if gender != '전체':
    filtered_data = filtered_data[filtered_data['성별'] == gender_dict[gender]]
filtered_data = filtered_data[(filtered_data['연령대'] >= age_range[0]) & (filtered_data['연령대'] <= age_range[1])]
print(filtered_data)
# Folium을 사용하여 지도에 점 표시하기
map = folium.Map(location=map_center, zoom_start=11)
# folium.CircleMarker(location=(map_center[0],map_center[1]), radius=5, color='blue', fill=True).add_to(map)

for index, row in filtered_data.iterrows():
    folium.CircleMarker(location=(row['GPS Y좌표'], row['GPS X좌표']), radius=5, color='blue', fill=True).add_to(map)

# Folium 지도를 스트림릿에 추가
folium_static(map)