import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from ipywidgets import interact, Dropdown

def print_map_column(df:pd.DataFrame, column, differ_size:bool=False, radius:float=0.5):
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
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=3, zoom=10)
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

def print_nested_pie_chart(df:pd.DataFrame, columns:list):
    grouped_data = df.groupby(columns).size().reset_index(name='count')
    fig = px.sunburst(grouped_data, path=columns, values='count')
    total_count = grouped_data['count'].sum()
    grouped_data['percentage'] = grouped_data['count'] / total_count * 100
    percentage_labels = grouped_data['percentage'].apply(lambda x: f'{x:.2f}%')
    fig.update_traces(text=percentage_labels, textinfo='label+percent entry')
    return fig

def plot_data(df, trip_type):
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['GPS X좌표'], df['GPS Y좌표']))
    gdf.crs = "EPSG:4326"  # 원본 데이터의 좌표계 설정
    gdf = gdf.to_crs(epsg=3857)
    filtered_data = gdf[gdf['동반 여행 종류'] == trip_type]
    fig, ax = plt.subplots(figsize=(10, 6))
    filtered_data.plot(ax=ax, color='blue', markersize=100, alpha=0.6)
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
    ax.set_axis_off()
    plt.show()
    return fig