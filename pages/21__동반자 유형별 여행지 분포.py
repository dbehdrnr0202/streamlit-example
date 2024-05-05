import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import contextily as ctx

# 데이터 로드 함수
@st.cache_data  # 데이터 캐싱
def load_data():
    data = pd.read_csv("data/data_file.csv")  # 파일 경로 주의
    return gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['GPS X좌표'], data['GPS Y좌표']))

gdf = load_data()
gdf.crs = "EPSG:4326"  # 원본 데이터의 좌표계 설정
gdf = gdf.to_crs(epsg=3857)  # Web Mercator 좌표계로 변환

# Streamlit 인터페이스
trip_type = st.selectbox('동반 여행 종류 선택', gdf['동반 여행 종류'].unique())

# 컬러맵과 노멀라이저 설정
unique_trip_types = gdf['동반 여행 종류'].unique()
trip_type_colors, _ = pd.factorize(unique_trip_types)
cmap = plt.get_cmap('tab20')  # 적절한 컬러맵 선택
norm = Normalize(vmin=trip_type_colors.min(), vmax=trip_type_colors.max())

def plot_data(trip_type):
    filtered_data = gdf[gdf['동반 여행 종류'] == trip_type]
    fig, ax = plt.subplots(figsize=(10, 6))
    color = cmap(norm(trip_type_colors[unique_trip_types.tolist().index(trip_type)]))
    filtered_data.plot(ax=ax, color=color, markersize=100, alpha=0.6)
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    ax.set_axis_off()
    return fig

fig = plot_data(trip_type)
st.pyplot(fig)