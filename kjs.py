import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

import matplotlib
matplotlib.rcParams['font.family'] = 'AppleGothic'

data = pd.read_csv('data/data_file.csv')
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