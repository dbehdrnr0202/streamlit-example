import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import streamlit as st
# import geopandas as gpd
# import matplotlib.pyplot as plt
# import contextily as ctx
# from ipywidgets import interact, Dropdown
import json

def print_map_column(df:pd.DataFrame, column, differ_size:bool=False, radius:float=0.5, size_max:int=3):
    activity_dict = dict(df[column].value_counts())
    activities = [[v, k] for k, v in activity_dict.items()]
    if differ_size:
        activities.sort()
        activities = [[(index+1)*radius, v[1]] for index, v in enumerate(activities)]
    else:
        activities = [[1*radius, v[1]] for index, v in enumerate(activities)]
    for activity_item in activities:
        activity_dict[activity_item[1]] = activity_item[0]
    df[column+'_rank'] = df[column].map(activity_dict)
    px.set_mapbox_access_token(os.environ.get('MAPBOX_API_TOKEN'))
    fig = px.scatter_mapbox(df, 
                        lat="GPS Y좌표", 
                        lon="GPS X좌표",     
                        color=column, 
                        size=column+"_rank",
                        text='방문지명',
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=size_max, zoom=10)
    # fig.show()
    return fig
    
def print_pie_chart(df:pd.DataFrame, column:str, hole_size:float=0):
    fig = px.pie(df, 
                names=column, 
                title=f'Percentage of {column}')
    fig.update_traces(hoverinfo='label', textinfo='value+percent', textfont_size=20,
                  marker=dict(line=dict(color='#000000', width=2)), hole=hole_size)
    # fig.show()
    return fig

@st.cache_data
def print_nested_pie_chart(df:pd.DataFrame, columns:list):
    grouped_data = df.groupby(columns).size().reset_index(name='count')
    fig = px.sunburst(grouped_data, path=columns, values='count')
    total_count = grouped_data['count'].sum()
    grouped_data['percentage'] = grouped_data['count'] / total_count * 100
    percentage_labels = grouped_data['percentage'].apply(lambda x: f'{x:.2f}%')
    fig.update_traces(text=percentage_labels, textinfo='label+percent entry')
    return fig

# def plot_data(df, trip_type):
#     gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['GPS X좌표'], df['GPS Y좌표']))
#     gdf.crs = "EPSG:4326"  # 원본 데이터의 좌표계 설정
#     gdf = gdf.to_crs(epsg=3857)
#     filtered_data = gdf[gdf['동반 여행 종류'] == trip_type]
#     fig, ax = plt.subplots(figsize=(10, 6))
#     filtered_data.plot(ax=ax, color='blue', markersize=100, alpha=0.6)
#     ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
#     ax.set_axis_off()
#     plt.show()
#     return fig

# def plot_data(df, trip_type):
#     filtered_df = df[df['동반 여행 종류']==trip_type]
#     with open('data/jeju.geojson', 'r') as f:
#         jeju_geo = json.load(f)
#     fig = px.choropleth_mapbox(filtered_df,
#                            geojson=jeju_geo,
#                            locations='지번주소',
#                            color='동반 여행 종류',
#                            color_continuous_scale='viridis', featureidkey = 'properties.adm_nm',
#                            mapbox_style='carto-positron',
#                            zoom=9.5,
#                            center = {"lat": df['GPS Y좌표'].mean(), "lon": df['GPS X좌표'].mean()},
#                            opacity=0.5,
#                           )
#     return fig

def print_corr_plot(df : pd.DataFrame, column1:str, column2 : str) :
    ord_dict = {'소득수준' : ['소득없음', '월평균 100만원 미만', '월평균 100만원 ~ 200만원 미만', '월평균 200만원 ~ 300만원 미만', '월평균 300만원 ~ 400만원 미만', '월평균 400만원 ~ 500만원 미만', '월평균 500만원 ~ 600만원 미만', '월평균 600만원 ~ 700만원 미만', '월평균 700만원 ~ 800만원 미만', '월평균 800만원 ~ 900만원 미만', '월평균 900만원 ~ 1,000만원 미만', '월평균 1,000만원 이상'],
                '계획에 따른 여행 vs 상황에 따른 여행' : ['상황에 따른 여행 매우선호', '상황에 따른 여행 중간선호', '상황에 따른 여행 약간선호', '중립', '계획에 따른 여행 약간선호', '계획에 따른 여행 중간선호', '계획에 따른 여행 매우선호'],
                '여행 시작 월' : ['8월', '9월', '10월', '11월'],
                '자연 vs 도시' : ['자연 매우선호', '자연 중간선호', '자연 약간선호', '중립', '도시 약간선호', '도시 중간선호', '도시 매우선호'],
                '숙박 vs 당일' : ['숙박 매우선호', '숙박 중간선호', '숙박 약간선호', '중립', '당일 약간선호' , '당일 중간선호', '당일 매우선호'],
                '새로운 지역 vs 익숙한 지역' : ['새로운 지역 매우선호', '새로운 지역 중간선호', '새로운 지역 약간선호', '중립', '익숙한 지역 약간선호' , '익숙한 지역 중간선호', '익숙한 지역 매우선호'],
                '편하지만 비싼 숙소 vs 불편하지만 저렴한 숙소' : ['편하지만 비싼 숙소 매우선호', '편하지만 비싼 숙소 중간선호', '편하지만 비싼 숙소 약간선호', '중립', '불편하지만 저렴한 숙소 약간선호' , '불편하지만 저렴한 숙소 중간선호', '불편하지만 저렴한 숙소 매우선호'],
                '휴양/휴식 vs 체험활동' : ['휴양/휴식 매우선호', '휴양/휴식 중간선호', '휴양/휴식 약간선호', '중립', '체험활동 약간선호', '체험활동 중간선호', '체험활동 매우선호'],
                '잘 알려지지 않은 방문지 vs 잘 알려진 방문지' : ['잘 알려지지 않은 방문지 매우선호', '잘 알려지지 않은 방문지 중간선호', '잘 알려지지 않은 방문지 약간선호', '중립', '알려진 방문지 약간선호', '알려진 방문지 중간선호', '알려진 방문지 매우선호'],
                '사진촬영 중요하지 않음 vs 사진촬영 중요함' : ['사진촬영 중요하지 않음 매우선호', '사진촬영 중요하지 않음 중간선호', '사진촬영 중요하지 않음 약간선호', '중립', '사진촬영 중요함 약간선호', '사진촬영 중요함 중간선호', '사진촬영 중요함 매우선호'],
}
    #if column2 in ord_dict.keys() :
    #    ord2 = pd.api.types.CategoricalDtype(categories=ord_dict[column2], ordered = True)
    #    df[column2] = df[column2].astype(ord2)
    if column1 in ord_dict.keys() and column2 in ord_dict.keys() :
        fig = px.density_heatmap(df, x = column1, y = column2, marginal_x = 'histogram', marginal_y = 'histogram', text_auto = True, category_orders={column1: ord_dict[column1], column2: ord_dict[column2]})
    elif column1 in ord_dict.keys() :
        fig = px.density_heatmap(df, x = column1, y = column2, marginal_x = 'histogram', marginal_y = 'histogram', text_auto = True, category_orders={column1: ord_dict[column1]},title=f'Density Heatmap of {column1} and {column2}')
    elif column2 in ord_dict.keys() :
        fig = px.density_heatmap(df, x = column1, y = column2, marginal_x = 'histogram', marginal_y = 'histogram', text_auto = True, category_orders={column2: ord_dict[column2]},title=f'Density Heatmap of {column1} and {column2}')
    else :
        fig = px.density_heatmap(df, x = column1, y = column2, marginal_x = 'histogram', marginal_y = 'histogram', text_auto = True,title=f'Density Heatmap of {column1} and {column2}')
    #fig.show()
    return fig