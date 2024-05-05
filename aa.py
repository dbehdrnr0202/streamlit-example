import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from  PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px
import io
import geopandas as gpd
import plotly.express as px

with st.sidebar:
    choose = option_menu("제주 여행", ["성별", "연령대", "여행동기_1", ],
                         icons=['house', 'bar-chart', 'kanban'],
                         menu_icon="bi bi-folder2", default_index=0,
                         styles={
                         # default_index = 처음에 보여줄 페이지 인덱스 번호
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "pink", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#baf7de"},
    } # css 설정
    )

# Title of the Streamlit app
st.title('제주도 추천 여행코스 얍 !')

# Path to the audio file
audio_file = '태연_제주도의푸른밤.mp3'

# Adding an audio player to play the MP3 file
st.audio(audio_file, format='audio/mp3', start_time=0)

st.write("🤍수료식하고 놀러가자🤍")


# Load the CSV data
data_path = 'final_df_0425.csv'
data = pd.read_csv(data_path)

# Load GeoJSON data
geo_data = "jeju.geojson"
try:
    jeju_map = gpd.read_file(geo_data)
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

if jeju_map.empty:
    st.error("No data loaded into GeoDataFrame.")
    st.stop()

# Ensure the coordinate reference system is set to latitude and longitude
jeju_map = jeju_map.to_crs(epsg=4326)

# Plotting with Plotly
fig = px.choropleth(jeju_map,
                    geojson=jeju_map.geometry,
                    locations=jeju_map.index,
                    color="adm_nm",  # Assuming 'adm_nm' is the field for administrative names
                    projection="mercator",
                    title="Jeju Island Administrative Divisions")
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Display the Plotly figure in Streamlit
st.plotly_chart(fig)


# Load your dataset
df = pd.read_csv('final_df_0425.csv')


# Streamlit sidebar for selection
st.sidebar.title('선택해봐욤')
selected_travel_type = st.sidebar.selectbox(
    "성별:",
    options=df['성별'].unique()
)
selected_travel_type = st.sidebar.selectbox(
    "동반 여행 종류:",
    options=df['동반 여행 종류'].unique()
)
selected_travel_type = st.sidebar.selectbox(
    "사진촬영 중요하지 않음 vs 사진촬영 중요함:",
    options=df['사진촬영 중요하지 않음 vs 사진촬영 중요함'].unique()
)

# Filter the data based on the selections
filtered_data = df[
    (df['성별'] == '성별') &
    (df['동반 여행 종류'] == '동반 여행 종류') &
    (df['사진촬영 중요하지 않음 vs 사진촬영 중요함'] == '사진촬영 중요하지 않음 vs 사진촬영 중요함')
]


# Additional info
st.write("서울대학교 빅데이터 핀테크 마스터 3조 김지선 나승찬 박연아 양혜민 오도은 유동국")

# Sidebar for user input
st.sidebar.header("Filter options")
age_group = st.sidebar.multiselect("Select Age Group:", options=data['연령대'].unique(), default=data['연령대'].unique())
travel_purpose_1 = st.sidebar.multiselect("Select 1st Travel Purpose:", options=data['1순위 여행목적'].unique(), default=data['1순위 여행목적'].unique())

# Filtering data based on selection
filtered_data = data[(data['연령대'].isin(age_group)) & (data['1순위 여행목적'].isin(travel_purpose_1))]

# Display filtered data
st.write("Filtered Data", filtered_data[['연령대', '1순위 여행목적']])

# Custom CSS to change font color
st.markdown("""
<style>
body {
    color: #000000;  # Black color
}
</style>
""", unsafe_allow_html=True)

