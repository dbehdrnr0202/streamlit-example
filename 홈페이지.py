import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import pydeck as pdk  # type: ignore
import map
from dotenv import load_dotenv
from streamlit_option_menu import option_menu


def main():
    # Title of the Streamlit app
    st.title('제주도 추천 여행코스 얍 !')

    # Path to the audio file
    audio_file = 'data/태연_제주도의푸른밤.mp3'

    # Adding an audio player to play the MP3 file
    st.audio(audio_file, format='audio/mp3', start_time=0)

    st.write("🤍수료식하고 놀러가자🤍")
    st.write("서울대학교 빅데이터 핀테크 마스터 3조 김지선 나승찬 박연아 양혜민 오도은 유동국")

    st.page_link("홈페이지.py", label="Home", icon="🏠")
    st.page_link("pages/1_원본 데이터 탐색.py", label="Page 1: 원본 데이터 프레임 확인하기", icon="1️⃣")
    st.page_link("pages/2_데이터 시각화.py", label="Page 2: 데이터 차트로 시각화하기", icon="2️⃣")
    st.page_link("pages/3_Top10 랭킹.py", label="Page 3: 랭킹 데이터 확인하기", icon="3️⃣")
    st.page_link("pages/4_데이터랩.py", label="Page 4: 비슷한 여행지 확인하기", icon="4️⃣")
    st.page_link("pages/5_챗봇.py", label="Page 5: 챗봇 대화하기", icon="5️⃣")

    st.page_link("https://www.jeju.go.kr/index.htm", label="제주도~", icon="🏝️")
    


if __name__ == "__main__":
    load_dotenv()
    main()
