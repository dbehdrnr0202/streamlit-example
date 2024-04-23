import streamlit as st # type: ignore
from PIL import Image # type: ignore
import pandas as pd # type: ignore
import map
def create_layout():
    # 공간을 2:3 으로 분할 후, col1과 col2라는 이름을 가진 컬럼을 생성합니다.  
    col1,col2 = st.columns([2,3])

    with col1 :
        st.title('here is column1')
    with col2 :
        st.title('here is column2')
        st.checkbox('this is checkbox1 in col2 ')
    col1.subheader(' i am column1  subheader !! ')
    col2.checkbox('this is checkbox2 in col2 ') 
    map.print_map()
def create_tab():
    tab1, tab2= st.tabs(['Tab1' , 'Tab2'])
    with tab1:
        st.write('msg_tab_1')
    with tab2:
        st.write('msg_tab_2')
        
def create_sidebar(origin_df:pd.DataFrame, columns:list[str]):
    st.sidebar.title('sidebar')
    st.sidebar.checkbox('pi chart')
    st.sidebar.checkbox('heatmap')
    # 사이드바에 체크박스, 버튼등 추가할 수 있습니다! 
    # 사이드바에 select box를 활용하여 차트 출력하기
    st.sidebar.title('제주도 여행~')

    # selected_column 변수에 사용자가 선택한 값이 지정됩니다
    selected_column = st.sidebar.selectbox('관련 컬럼을 확인하세요',columns)
    
    tmp_df = origin_df[selected_column]
    st.table(tmp_df.head())
    
    selected_multi_columns = st.sidebar.multiselect('확인하고자 하는 컬럼들을 선택해 주세요. 복수선택가능',columns)

    tmp_df = []
    st.table(tmp_df)

def load_img(file_name:str):
    #PIL 패키지에 이미지 모듈을 통해 이미지 열기 
    # Image.open('이미지 경로')
    try:
        opened_img = Image.open(file_name)
    except FileNotFoundError as e:
        print(e)
    col1,col2 = st.columns([2,3])
    with col1 :
    # column 1 에 담을 내용
        st.title('here is column1')
    with col2 :
    # column 2 에 담을 내용
        st.title('here is column2')
        st.checkbox('this is checkbox1 in col2 ')
    # 컬럼2에 불러온 사진 표시하기
    col2.image(opened_img)
    
def print_slider(df, select_multi_species, columns):
    # 라디오에 선택한 내용을 radio select변수에 담습니다
    radio_select =st.sidebar.radio(
        "what is key column?",
        columns,
        horizontal=True
        )
    # 선택한 컬럼의 값의 범위를 지정할 수 있는 slider를 만듭니다. 
    slider_range = st.sidebar.slider(
        "choose range of key column",
        0.0, #시작 값 
        10.0, #끝 값  
        (2.5, 7.5) # 기본값, 앞 뒤로 2개 설정 /  하나만 하는 경우 value=2.5 이런 식으로 설정가능
    )

    # 필터 적용버튼 생성 
    start_button = st.sidebar.button(
        "apply filter"
    )

    # button이 눌리는 경우 start_button의 값이 true로 바뀌게 된다.
    # 이를 이용해서 if문으로 버튼이 눌렸을 때를 구현 
    if start_button:
        tmp_df = df[df['species'].isin(select_multi_species)]
        #slider input으로 받은 값에 해당하는 값을 기준으로 데이터를 필터링합니다.
        tmp_df= tmp_df[ (tmp_df[radio_select] >= slider_range[0]) & (tmp_df[radio_select] <= slider_range[1])]
        st.table(tmp_df)
        # 성공문구 + 풍선이 날리는 특수효과 
        st.sidebar.success("Filter Applied!")
        st.balloons()