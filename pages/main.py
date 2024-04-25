# -*- coding:utf-8 -*-
import pandas as pd
import streamlit as st
from millify import prettify

def run_main():
    total_df = pd.read_csv('data/data_file.csv')
    st.title("시각화 팀 프로젝트")
    # 대부분 main에서 작업을 한다.
    st.subheader("제주도 여행지 시각화")
    st.image("img/main.gif", caption="부릉부릉")
    st.text("3조")
    st.markdown("**아름다운 섬 제주**, 어디로 놀러가면 좋을까?")

    
    st.markdown("## 대시보드 개요 \n"
    "본 프로젝트는 서울시 부동산 실거래가를 알려주는 대시보드입니다. "
    "여기에 독자가 넣고 싶은 추가 내용을 더 넣을 수 있습니다.")

    total_df['DEAL_YMD'] = pd.to_datetime(total_df['DEAL_YMD'], format="%Y-%m-%d")
    total_df['month'] = total_df['DEAL_YMD'].dt.month
    total_df = total_df.loc[total_df['HOUSE_TYPE'] == '아파트', :]

    sgg_nm = st.sidebar.selectbox("자치구", sorted(total_df['SGG_NM'].unique()))
    selected_month = st.sidebar.radio("확인하고 싶은 월을 선택하세요 ", ['3월', '4월'])
    month_dict = {'3월' : 3, '4월' : 4}
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(f'{sgg_nm} {selected_month} 아파트 가격 개요')
    st.markdown("자치구와 월을 클릭하면 자동으로 각 지역구의 거래된 **최소가격**, **최대가격**을 확인할 수 있습니다.")
    col1, col2 = st.columns(2)
    filtered_month = total_df[total_df['month'] == month_dict[selected_month]]
    filtered_month = filtered_month[filtered_month['SGG_NM'] == sgg_nm]
    march_min_price = filtered_month['OBJ_AMT'].min()
    march_max_price = filtered_month['OBJ_AMT'].max()

    with col1:
        st.metric(label = f"{sgg_nm} 최소가격(만원)", value = prettify(march_min_price))
    
    with col2:
        st.metric(label=f"{sgg_nm} 최대가격(만원)", value = prettify(march_max_price))
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 아파트 가격 상위 3")
    sorted_df = filtered_month[["SGG_NM", "BJDONG_NM", "BLDG_NM", "BLDG_AREA", "OBJ_AMT"]]
    st.dataframe(sorted_df.sort_values(by='OBJ_AMT', ascending=False).head(3).reset_index(drop=True))
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 아파트 가격 하위 3")
    sorted_df = filtered_month[["SGG_NM", "BJDONG_NM", "BLDG_NM", "BLDG_AREA", "OBJ_AMT"]]
    st.dataframe(sorted_df.sort_values(by='OBJ_AMT', ascending=True).head(3).reset_index(drop=True))
    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("출처 : [서울시 부동산 실거래가 정보](https://data.seoul.go.kr/dataList/OA-21275/S/1/datasetView.do)")