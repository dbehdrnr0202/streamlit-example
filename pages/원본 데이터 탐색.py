import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import print_plots
import numpy as np

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")


st.title("데이터 쿼리")
df = load_data("data/data_file.csv")
df = df.drop(columns=["Unnamed: 0", "여행ID"]).dropna()
st.dataframe(df)
st.button("Rerun")
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
filtered_df = df.copy(deep=True)
for multi_select in multi_selected:
        if df[multi_select].dtype==np.int64:
            min_value = min(df[multi_select].unique())
            max_value = max(df[multi_select].unique())
            value_range = st.sidebar.slider(f"{multi_select} 범위를 선택해주세요.", min_value, max_value, (min_value, max_value), step=10)
            filtered_df = filtered_df[filtered_df[multi_select].between(value_range[0], value_range[1])]
        else:
            value = st.sidebar.multiselect(f"{multi_select} 를 지정해주세요", options=df[multi_select].unique())
            print(value)
            if value==[]:
                 value = df[multi_select].unique()
            filtered_df = filtered_df[filtered_df[multi_select].isin(value)]
start_button = st.sidebar.button(
    "filter apply 📊 "#"버튼에 표시될 내용"
)

if start_button:
    csv = convert_df(filtered_df) 
    st.dataframe(filtered_df)
    st.download_button(label='필터링된 그래프 이미지 다운받기',
                       data=csv,
                       file_name='filtered_dataframe.png',
                       mime="text/csv",)

