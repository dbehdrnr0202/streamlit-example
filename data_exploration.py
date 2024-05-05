import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 데이터 불러오기
url = 'https://raw.githubusercontent.com/JSK961/streamlit-example/master/final_df_0425.csv'
data = pd.read_csv(url)
data.dropna(inplace=True)

# 여행일수 그래프
plt.figure(figsize=(10,6))
st.subheader('여행일수')
days = data['여행일수'].value_counts().sort_index()
sns.barplot(x=days.index, y=days.values, palette='pastel')
plt.title('여행일수')
plt.xlabel('days')
st.pyplot(plt.gcf())

# 동반 인원수 그래프
plt.figure(figsize=(10,6))
st.subheader('동반 인원수')
n_companion = data['동반 인원수'].value_counts().sort_index()
sns.barplot(x=n_companion.index, y=n_companion.values, palette='pastel')
plt.xlabel('n_companion')
st.pyplot(plt.gcf())

# 동반 여행 종류 그래프
plt.figure(figsize=(10,6))
st.subheader('동반 여행 종류')
companion_type = data['동반 여행 종류'].value_counts().sort_index()
sns.barplot(x=companion_type.index, y=companion_type.values, palette='pastel')
plt.xlabel('companion_type')
plt.xticks(rotation=90)
st.pyplot(plt.gcf())

# 월별 여행 횟수 그래프
plt.figure(figsize=(10,6))
st.subheader('월별 여행 횟수')
month = data['여행 시작 월'].value_counts().sort_index()
sns.barplot(x=month.index, y=month.values, palette='pastel')
plt.title('월별 여행 횟수')
plt.xlabel('month')
st.pyplot(plt.gcf())

# 소득수준 그래프
plt.figure(figsize=(10,6))
st.subheader('소득수준')
income = data['소득수준'].value_counts().sort_index()
sns.barplot(x=income.index, y=income.values, palette='pastel')
plt.xlabel('income')
plt.xticks(rotation=90)
st.pyplot(plt.gcf())

# 여행지 유형 그래프
plt.figure(figsize=(10,6))
st.subheader('여행지 유형')
types = data['여행지 유형'].value_counts()
sns.barplot(x=types.index, y=types.values, palette='pastel')
plt.xlabel('types')
plt.xticks(rotation=90)
st.pyplot(plt.gcf())

# 성별 나이별 빈도 계산 및 히트맵
plt.figure(figsize=(10,6))
st.subheader('성별 나이별 빈도')
freq_df = data.groupby(['연령대','성별']).size().unstack(fill_value=0)
plt.figure(figsize=(10, 6))
sns.heatmap(freq_df, annot=True, cmap='Blues', fmt='.2f')
plt.title("Frequency by Gender and Ages")
plt.xlabel("Gender")
plt.ylabel("Ages")
st.pyplot(plt.gcf())
