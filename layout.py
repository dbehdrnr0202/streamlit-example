import streamlit as st  # type: ignore
from streamlit_option_menu import option_menu  # type: ignore
from PIL import Image  # type: ignore
import pandas as pd  # type: ignore
import map
import chatbot
import time


def create_layout():
    # 공간을 2:3 으로 분할 후, col1과 col2라는 이름을 가진 컬럼을 생성합니다.
    col1, col2 = st.columns([2, 3])
    with col1:
        st.title("here is column1")
    with col2:
        st.title("here is column2")
        st.checkbox("this is checkbox1 in col2 ")
    col1.subheader(" i am column1  subheader !! ")
    col2.checkbox("this is checkbox2 in col2 ")
    create_sidebar()


def create_tab():
    tab1, tab2 = st.tabs(["Tab1", "Tab2"])
    with tab1:
        st.write("msg_tab_1")
    with tab2:
        st.write("msg_tab_2")


def create_sidebar():
    with st.sidebar:
        choice = option_menu(
            "Menu",
            ["page1", "page2", "page3"],
            icons=["house", "kanban", "bi bi-robot"],
            menu_icon="app-indicator",
            default_index=0,
            styles={
                "container": {"padding": "4!important", "background-color": "#fafafa"},
                "icon": {"color": "black", "font-size": "25px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#fafafa",
                },
                "nav-link-selected": {"background-color": "#08c7b4"},
            },
        )
        if choice == "page1":
            clear_screen()
            show_main_page()
        elif choice == "page2":
            show_plot_page()
        elif choice == "page3":
            chatbot.create_chat_gpt()
        print(choice)


def show_plot_page():
    st.title("데이터 시각화 페이지")


def show_main_page():
    st.title("시각화 팀 프로젝트")
    # 대부분 main에서 작업을 한다.
    st.subheader("제주도 여행지 시각화")
    st.image("img/main.gif", caption="부릉부릉")
    st.text("3조")
    st.markdown("**아름다운 섬 제주**, 어디로 놀러가면 좋을까?")


def print_slider(df, select_multi_species, columns):
    radio_select = st.sidebar.radio("what is key column?", columns, horizontal=True)
    # 선택한 컬럼의 값의 범위를 지정할 수 있는 slider를 만듭니다.
    slider_range = st.sidebar.slider(
        "choose range of key column",
        0.0,  # 시작 값
        10.0,  # 끝 값
        (2.5, 7.5),  # 기본값, 앞 뒤로 2개 설정 /  하나만 하는 경우 value=2.5 이런 식으로 설정가능
    )

    # 필터 적용버튼 생성
    start_button = st.sidebar.button("apply filter")
    # button이 눌리는 경우 start_button의 값이 true로 바뀌게 된다.
    # 이를 이용해서 if문으로 버튼이 눌렸을 때를 구현
    if start_button:
        tmp_df = df[df["species"].isin(select_multi_species)]
        # slider input으로 받은 값에 해당하는 값을 기준으로 데이터를 필터링합니다.
        tmp_df = tmp_df[
            (tmp_df[radio_select] >= slider_range[0])
            & (tmp_df[radio_select] <= slider_range[1])
        ]
        st.table(tmp_df)
        # 성공문구 + 풍선이 날리는 특수효과
        st.sidebar.success("Filter Applied!")
        st.balloons()


def clear_screen():
    # 빈 공간 생성
    placeholder = st.empty()

    # 잠시 후에 빈 공간을 지우기
    placeholder.text("화면을 지우려면 잠시 기다려주세요...")
    time.sleep(1)
    placeholder.empty()
