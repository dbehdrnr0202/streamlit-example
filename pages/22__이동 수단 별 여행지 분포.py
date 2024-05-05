# file_name : map_de.py
# last modified : 24/05/04
# purpose : use streamlit, folium to filter by gender & ages
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# 여행지 방문 데이터 불러오기
# @st.cache
# url = 'https://raw.githubusercontent.com/JSK961/streamlit-example/master/final_df_0425.csv'
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df
data = load_data("data/data_file.csv")
data.dropna(inplace=True)
print(data.shape)

# 지도 초기 위치 설정
map_center = [data['GPS Y좌표'].mean(),data['GPS X좌표'].mean()]
map = folium.Map(location=map_center, zoom_start=11)

# 스트림릿 앱 제목 설정
st.title('여행지 방문 데이터 시각화_by folium')

# 이동수단 옵션 설정
transportation = st.selectbox('이동수단 방법', ['대중교통 등', '자가용'], index=None, placeholder='이동수단을 선택하세요.')

# 선택이 이루어지지 않았을 때의 기본 지도 표시 코드
if not transportation:
    map = folium.Map(location=map_center, zoom_start=11)
    folium_static(map)

elif transportation == '대중교통 등':
# Folium을 사용하여 지도에 점 표시하기
    public = data[data['이동수단 방법'] == '대중교통 등']
    for index, row in public.iterrows():
        folium.CircleMarker(location=(row['GPS Y좌표'], row['GPS X좌표']), radius=5, color='red', fill=True).add_to(map)
        # Folium 지도를 스트림릿에 추가
    folium_static(map)

else:
    private = data[data['이동수단 방법'] == '자가용']
    for index, row in private.iterrows():
        folium.CircleMarker(location=(row['GPS Y좌표'], row['GPS X좌표']), radius=5, color='blue', fill=True).add_to(map)
    # Folium 지도를 스트림릿에 추가
    folium_static(map)