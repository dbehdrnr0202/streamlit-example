import streamlit as st # type: ignore
from PIL import Image # type: ignore
import pandas as pd # type: ignore

def create_layout():
    col1,col2 = st.columns([2,3])
    # 공간을 2:3 으로 분할하여 col1과 col2라는 이름을 가진 컬럼을 생성합니다.  

    with col1 :
    # column 1 에 담을 내용
        st.title('here is column1')
    with col2 :
    # column 2 에 담을 내용
        st.title('here is column2')
        st.checkbox('this is checkbox1 in col2 ')
    # with 구문 말고 다르게 사용 가능 
    col1.subheader(' i am column1  subheader !! ')
    col2.checkbox('this is checkbox2 in col2 ') 

def create_tab():
    # 탭 생성 : 첫번째 탭의 이름은 Tab A 로, Tab B로 표시합니다. 
    tab1, tab2= st.tabs(['Tab A' , 'Tab B'])
    with tab1:
    #tab A 를 누르면 표시될 내용
        st.write('hello')
    with tab2:
    #tab B를 누르면 표시될 내용 
        st.write('hi')
        
def create_sidebar(origin_df:pd.DataFrame, columns:list[str]):
    st.sidebar.title('sidebar')
    st.sidebar.checkbox('pi chart')
    st.sidebar.checkbox('heatmap')
    
    # 사이드바에 체크박스, 버튼등 추가할 수 있습니다! 
    # 사이드바에 select box를 활용하여 종을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
    st.sidebar.title('제주도 여행~')

    # select_species 변수에 사용자가 선택한 값이 지정됩니다
    selected_column = st.sidebar.selectbox(
        '관련 컬럼을 확인하세요',
        columns
    )
    # 원래 dataframe으로 부터 꽃의 종류가 선택한 종류들만 필터링 되어서 나오게 일시적인 dataframe을 생성합니다
    tmp_df = origin_df[selected_column]
    # df[df['species']== select_species]
    # 선택한 종의 맨 처음 5행을 보여줍니다 
    st.table(tmp_df.head())
    
    
    select_multi_species = st.sidebar.multiselect(
    '확인하고자 하는 종을 선택해 주세요. 복수선택가능',
    ['setosa','versicolor','virginica']

    )

    # 원래 dataframe으로 부터 꽃의 종류가 선택한 종류들만 필터링 되어서 나오게 일시적인 dataframe을 생성합니다
    tmp_df = []
    # df[df['species'].isin(select_multi_species)]
    # 선택한 종들의 결과표를 나타냅니다.  
    st.table(tmp_df)
    
def load_img():
    #PIL 패키지에 이미지 모듈을 통해 이미지 열기 
    # Image.open('이미지 경로')
    zarathu_img = Image.open('zarathu.png')
    col1,col2 = st.columns([2,3])
    with col1 :
    # column 1 에 담을 내용
        st.title('here is column1')
    with col2 :
    # column 2 에 담을 내용
        st.title('here is column2')
        st.checkbox('this is checkbox1 in col2 ')
    # 컬럼2에 불러온 사진 표시하기
    col2.image(zarathu_img)