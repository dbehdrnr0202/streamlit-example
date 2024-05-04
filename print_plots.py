import pandas as pd
import plotly.express as px
import os

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

## 도은추가
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.rcParams['font.family'] = 'AppleGothic'

def print_twoway_heatmap(df:pd.DataFrame, columns:list[str]):
    # columns의 빈도 계산
    column1, column2 = columns[0], columns[1]
    freq_df = df.groupby([column1,column2]).size().unstack(fill_value=0)

    # 그래프 생성
    plt.figure(figsize=(10, 6))
    sns.heatmap(freq_df, annot=True, cmap='Blues', fmt='.2f')
    plt.title(f"Frequency by {column1} and {column2}")
    plt.xlabel(f"{column1}")
    plt.ylabel(f"{column2}")

    return plt.gcf()