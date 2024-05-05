# file_name : map_de.py
# last modified : 24/05/04
# purpose : use streamlit, folium to filter by gender & ages


import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# 여행지 방문 데이터 불러오기
# @st.cache
url = 'https://raw.githubusercontent.com/JSK961/streamlit-example/master/final_df_0425.csv'
data = pd.read_csv(url)
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


private_child = data[(data['이동수단 방법'] == '대중교통 등') & data['동반 여행 종류'] == '자녀 동반 여행']
for index, row in private_child.iterrows():
    folium.CircleMarker(location=(row['GPS Y좌표'], row['GPS X좌표']), radius=5, color='red', fill=True).add_to(map)
    # Folium 지도를 스트림릿에 추가
folium_static(map)



import seaborn as sns
# import matplotlib
import matplotlib.pyplot as plt
lst = ['동반 인원수', '동반 여행 종류', '연령대', '여행지 유형', '활동 유형', '여행동기_1']

# Streamlit 앱 시작
st.title('이동수단 방법 비교')


for col in lst:
    fig, ax = plt.subplots(figsize=(12, 8))  # 별도의 피겨 객체 생성
    sns.countplot(data=data, x=col, hue='이동수단 방법', dodge=True, palette='pastel', ax=ax)
    ax.set_title(f'{col}에 따른 이동수단 방법 비교')
    ax.set_xlabel(col)
    ax.set_ylabel('빈도수')
    ax.legend(title='이동수단 방법')

    if (col == '여행지 유형') or (col == '여행동기_1'):
        ax.tick_params(axis='x', rotation=90)

    # 플롯을 Streamlit에 전달
    st.pyplot(fig)