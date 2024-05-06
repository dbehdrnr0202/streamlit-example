import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path, index_col=False)
    return df

# TODO
# 우선순위10개의 방문지들을 빈도수, 평점, 추천의향에 따라서 랭킹 매기기
# 그 새로운 식에 의해서 랭킹 매기기(평점*추천의향/빈도수)

st.title("랭킹 10")
df = load_data("data/data_file.csv")
df = df.drop(columns=["Unnamed: 0", "여행ID"]).dropna()
# st.dataframe(df)
sorted_radio = st.sidebar.radio("정렬 기준을 선택하세욤", ["만족도", "추천 의향 점수", "방문횟수", "Unique"])
sort_reverse = st.sidebar.toggle("역순 정렬")
bottom_value = st.sidebar.slider("최소 방문횟수 범위를 선택해주세요.", 0, 50, step=10)

multi_select_columns = ['성별', '연령대', '소득수준', '동반 여행 종류', '동반 인원수', '동반자 관계', '동반자 연령대', 
       '여행지 유형', '만족도', '추천 의향 점수', '활동 유형', '소비인원', '결제금액',
       '여행동기_1', '여행동기_2', '여행동기_3', '동반자 성별',
       '1순위 여행목적', '2순위 여행목적', '3순위 여행목적', '여행 시작 월', '여행 시작 연도']

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
        if value==[]:
                value = df[multi_select].unique()
        filtered_df = filtered_df[filtered_df[multi_select].isin(value)]
    
start_button = st.sidebar.button(
    "filter apply 📊 "#"버튼에 표시될 내용"
)

if start_button:
    filtered_data = filtered_df[['방문지명', '만족도', '추천 의향 점수', 'GPS X좌표', 'GPS Y좌표']].copy(deep=True)
    grouped_df = filtered_data.groupby('방문지명').mean()
    grouped_df.reset_index(inplace=True)
    방문횟수_dict = dict(filtered_df['방문지명'].value_counts())
    grouped_df['방문횟수'] = grouped_df['방문지명'].map(방문횟수_dict)
    grouped_df['Unique'] = grouped_df['만족도']*grouped_df['추천 의향 점수'] / grouped_df['방문횟수']
    if sort_reverse:
        sorted_df = grouped_df.sort_values(by=[sorted_radio, '방문횟수'], ascending=[True, False])
    else:
        sorted_df = grouped_df.sort_values(by=[sorted_radio, '방문횟수'], axis=0, ascending=False)
    if bottom_value:
        sorted_df = sorted_df[sorted_df['방문횟수']>=bottom_value]
    top_10_df = sorted_df[:10]
    sorted_df.index = np.arange(1, len(sorted_df)+1)
    top_10_df.index = np.arange(1, len(top_10_df)+1)
    st.dataframe(top_10_df.drop(columns=['GPS X좌표', 'GPS Y좌표']))
    px.set_mapbox_access_token(os.environ.get('MAPBOX_API_TOKEN'))
    st.plotly_chart(px.scatter_mapbox(top_10_df, 
                        lat="GPS Y좌표", 
                        lon="GPS X좌표",     
                        text='방문지명',
                        size=10-top_10_df.index,
                  color_continuous_scale=px.colors.cyclical.Edge, size_max=10, zoom=10))