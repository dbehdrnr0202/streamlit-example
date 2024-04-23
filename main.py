import streamlit as st # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore
import pydeck as pdk # type: ignore
import layout
import map
# 기본 형식
def main():
    # 화면에 관해 처리를 하고 싶다면 st를 사용해야한다.
    st.title('시각화 팀 프로젝트')
    # 대부분 main에서 작업을 한다.
    st.subheader('제주도 여행지 시각화')
    st.text('3조')
    st.markdown('**아름다운 섬 제주**, 어디로 놀러가면 좋을까?')
    layout.create_layout()
    layout.create_sidebar(pd.DataFrame({'a':[],'b':[]}), ['a', 'b'])
    layout.create_tab()    
    
if __name__ == '__main__':
    main()