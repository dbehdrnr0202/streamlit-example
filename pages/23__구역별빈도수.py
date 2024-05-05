import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import print_plots
import numpy as np
import os
import io
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from branca.colormap import linear

load_dotenv()

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Load GeoJSON file using GeoPandas
jeju_map = gpd.read_file("data/jeju.geojson")
if jeju_map.empty:
    st.stop()
jeju_map = jeju_map[jeju_map.adm_nm != '제주특별자치도 제주시 추자면']


# Load 여행 데이터 
import pandas as pd
data = pd.read_csv('data/data_file.csv')
data.dropna(inplace=True)

data['adm_nm'] = data.지번주소.apply(lambda x: ' '.join(x.split()[:3]))
dic_addr = {'화북일동':'화북동', '화북이동':'화북동',
            '삼양일동':'삼양동', '삼양이동':'삼양동',
            '아라일동':'아라동', '아라이동':'아라동',
            '오라일동':'오라동', '오라이동':'오라동', '오라삼동':'오라동',
            '외도일동':'외도동', '외도이동':'외도동',
            '이호일동':'이호동', '이호이동':'이호동', 
            '도두일동':'도두동', '도두이동':'도두동',
            '법환동':'대륜동','서호동':'대륜동','호근동':'대륜동',
            '강정동':'대천동','영남동':'대천동','월평동':'대천동','하원동':'대천동',
            '서귀동':'송산동','보목동':'송산동',
            '상효동':'영천동','토평동':'영천동',
            '색달동':'예래동','하예동':'예래동',
            '신효동':'효돈동','하효동':'효돈동',
            '대포동':'중문동','도순동':'중문동','상예동':'중문동','회수동':'중문동'
            }
data['adm_nm'] = data['adm_nm'].replace(dic_addr, regex=True)

map_center = [data['GPS Y좌표'].mean(), data['GPS X좌표'].mean()]
multi_select_columns = ['성별', '연령대', '소득수준', '동반 여행 종류', '동반 인원수', '동반자 관계', '동반자 연령대', '방문지명', 
       '여행지 유형', '만족도', '추천 의향 점수', '활동 유형', '소비인원', '결제금액',
       '여행동기_1', '여행동기_2', '여행동기_3', '동반자 성별',
       '1순위 여행목적', '2순위 여행목적', '3순위 여행목적', '여행 시작 월', '여행 시작 연도',
       '여행자 유형']
st.title('여행지 방문 데이터 시각화')
st.sidebar.title('데이터 차트 시각화')
multi_selected = st.sidebar.multiselect("구분자 선택", multi_select_columns)
if multi_selected=='여행자 유형':
    여행자_유형 = ['자연 vs 도시', '숙박 vs 당일', '새로운 지역 vs 익숙한 지역','편하지만 비싼 숙소 vs 불편하지만 저렴한 숙소', '휴양/휴식 vs 체험활동',
       '잘 알려지지 않은 방문지 vs 알려진 방문지', '계획에 따른 여행 vs 상황에 따른 여행','사진촬영 중요하지 않음 vs 사진촬영 중요함']
    radio = st.sidebar.radio("여행자 유형을 선택하세욤",여행자_유형)
filtered_df = data.copy(deep=True)
for multi_select in multi_selected:
        if filtered_df[multi_select].dtype==np.int64:
            min_value = min(filtered_df[multi_select].unique())
            max_value = max(filtered_df[multi_select].unique())
            value_range = st.sidebar.slider(f"{multi_select} 범위를 선택해주세요.", min_value, max_value, (min_value, max_value), step=10)
            filtered_df = filtered_df[filtered_df[multi_select].between(value_range[0], value_range[1])]
        else:
            value = st.sidebar.multiselect(f"{multi_select} 를 지정해주세요", options=filtered_df[multi_select].unique())
            if value==[]:
                 value = filtered_df[multi_select].unique()
            filtered_df = filtered_df[filtered_df[multi_select].isin(value)]

if multi_selected==[]:
    multi_selected = ['성별']


tabs = st.tabs(multi_selected)
for tab_index, selected_구분자 in enumerate(multi_selected):
    with tabs[tab_index]:
        df_count = filtered_df['adm_nm'].value_counts().reset_index()
        print(df_count.head())
        jeju_map = jeju_map.merge(df_count, on='adm_nm', how='left')
        print("컬럼들", jeju_map.columns)
        m = folium.Map(location=[33.3617, 126.5292], zoom_start=10)
        colormap = linear.YlGn_09.scale(
            df_count['count'].min()/len(df_count), df_count['count'].max()/len(df_count)
        )
        df_dict = jeju_map.set_index("adm_nm").reset_index()
        print("제주", jeju_map.columns)
        print("딕셔너리")
        jeju_map.drop(columns=['adm_cd'])
        folium.GeoJson(
            jeju_map,
            name='Jeju Administrative Areas',
            style_function= lambda feature:{
                'fillColor': colormap(df_dict.index[int(feature['id'])]),
                'color': 'black',
                'weight': 2,
                'dashArray': '5, 5',
                'fillOpacity': 0.6
            },
            tooltip=folium.GeoJsonTooltip(fields=['adm_nm'], labels=True)
        ).add_to(m)
        st_data = st_folium(m, width=725, height=500)