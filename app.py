import streamlit as st  # type: ignore
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import pydeck as pdk  # type: ignore
import layout
import map
from pages.chatbot import run_chat_bot
from pages.main import run_main
from pages.eda import run_eda
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

def main():
    page_names_to_funcs = {
        "메인 메뉴": run_main,
        "데이터 시각화 페이지": run_eda,
        "챗봇페이지": run_chat_bot,
    }
    st.markdown(
        """
        <style>
            [data-testid=stSidebar] {
                background-color: #E9EDC9;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )
    with st.sidebar:
        page_name = option_menu(
            "Menu",
            ["메인 메뉴", "데이터 시각화 페이지", "챗봇페이지"],
            icons=["house", "kanban", "bi bi-robot"],
            menu_icon="app-indicator",
            default_index=0,
            styles={
                "container": {"padding": "4!important", "background-color": "#FEFAE0"},
                "icon": {"color": "#D4A373", "font-size": "25px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "black",
                },
                "nav-link-selected": {"background-color": "#CCD5AE"},
            },
        )
    page_names_to_funcs[page_name]()


if __name__ == "__main__":
    load_dotenv()
    main()
