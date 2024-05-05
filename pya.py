#위 코드에 지도합침
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from ipywidgets import interact, Dropdown

# import streamlit as st

def load_data():
    data = pd.read_csv("data/final_df_0425.csv")
    return gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['GPS X좌표'], data['GPS Y좌표']))

gdf = load_data()
gdf.crs = "EPSG:4326"  # 원본 데이터의 좌표계 설정
gdf = gdf.to_crs(epsg=3857)  # Web Mercator 좌표계로 변환

def plot_data(trip_type):
    filtered_data = gdf[gdf['동반 여행 종류'] == trip_type]
    fig, ax = plt.subplots(figsize=(10, 6))
    filtered_data.plot(ax=ax, color='blue', markersize=100, alpha=0.6)
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    ax.set_axis_off()
    # plt.show()

# st.title('여행지 방문 데이터 시각화 - 도은 수정중~~~')

trip_types = gdf['동반 여행 종류'].unique()
dropdown = Dropdown(options=trip_types)
interact(plot_data, trip_type=dropdown)
