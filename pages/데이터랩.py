import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from clustering import clustering
import numpy as np

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

data = load_data("data/data_file.csv")
data = data.drop(columns=["Unnamed: 0", "여행ID"]).dropna()
st.title("여행지 별 군집 보기")
k_number = st.sidebar.number_input("군집 갯수를 입력하세요", value=3, placeholder="입력란")

columns = ['성별', '연령대', '소득수준', '만족도', '추천 의향 점수']
multi_select_columns = ['성별', '연령대', '소득수준', '동반 여행 종류', '동반 인원수', '동반자 관계', '동반자 연령대', '방문지명', 
       '여행지 유형', '만족도', '추천 의향 점수', '활동 유형', '소비인원', '결제금액',
       '여행동기_1', '여행동기_2', '여행동기_3', '동반자 성별',
       '1순위 여행목적', '2순위 여행목적', '3순위 여행목적', '여행 시작 월', '여행 시작 연도',
       '여행자 유형']
multi_selected = st.sidebar.multiselect("구분자 선택", multi_select_columns)
if multi_selected=='여행자 유형':
    여행자_유형 = ['자연 vs 도시', '숙박 vs 당일', '새로운 지역 vs 익숙한 지역','편하지만 비싼 숙소 vs 불편하지만 저렴한 숙소', '휴양/휴식 vs 체험활동',
       '잘 알려지지 않은 방문지 vs 알려진 방문지', '계획에 따른 여행 vs 상황에 따른 여행','사진촬영 중요하지 않음 vs 사진촬영 중요함']
    radio = st.sidebar.radio("여행자 유형을 선택하세욤",여행자_유형)
for multi_select in multi_selected:
        if data[multi_select].dtype==np.int64:
            min_value = min(data[multi_select].unique())
            max_value = max(data[multi_select].unique())
            value_range = st.sidebar.slider(f"{multi_select} 범위를 선택해주세요.", min_value, max_value, (min_value, max_value), step=10)
            filtered_df = data[data[multi_select].between(value_range[0], value_range[1])]
        else:
            value = st.sidebar.multiselect(f"{multi_select} 를 지정해주세요", options=data[multi_select].unique())
            if value==[]:
                 value = data[multi_select].unique()
            filtered_df = data[data[multi_select].isin(value)]
start_button = st.sidebar.button(
    "filter apply 📊 "
)

if start_button:
    filtered_data = filtered_df[columns+['방문지명']].copy(deep=True)
    for selected in columns:
        if selected=='소득수준':
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
    grouped_df = filtered_data.groupby("방문지명").mean()
    grouped_df.reset_index(inplace=True)
    st.plotly_chart(clustering(grouped_df, do_pca=True, n_clusters=k_number))
else:
    st.text("좌측 사이드바를 사용해주세요~")