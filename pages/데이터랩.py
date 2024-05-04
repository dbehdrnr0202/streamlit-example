import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from clustering import clustering

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

data = load_data("data/data_file.csv")
columns = ['성별', '연령대', '소득수준', '만족도', '추천 의향 점수']
multi_selected = st.sidebar.multiselect('구분자 선택', columns)
start_button = st.sidebar.button(
    "filter apply 📊 "#"버튼에 표시될 내용"
)
if start_button:
    filtered_data = data.copy(deep=True)
    for selected in multi_selected:
        if selected=='소득수준':
            print(selected)
            selected_dict = {
                '월평균 100만원 미만':50, 
                '월평균 100만원 ~ 200만원 미만':150, 
                '소득없음':0,
                '월평균 600만원 ~ 700만원 미만':650,
                '월평균 200만원 ~ 300만원 미만':250,
                '월평균 300만원 ~ 400만원 미만':350, 
                '월평균 500만원 ~ 600만원 미만':550,
                '월평균 400만원 ~ 500만원 미만':450, 
                '월평균 700만원 ~ 800만원 미만':750, 
                '월평균 1,000만원 이상':1000,
                '월평균 900만원 ~ 1,000만원 미만':950, 
                '월평균 800만원 ~ 900만원 미만':850}
            filtered_data[selected] = filtered_data[selected].map(selected_dict)
        elif selected=='성별':
            selected_dict  = {'남':0, '여':1}
            filtered_data[selected] = filtered_data[selected].map(selected_dict)
    st.plotly_chart(clustering(filtered_data[multi_selected], do_pca=False))
else:
    st.text("좌측 사이드바를 사용해주세요~")