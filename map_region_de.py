import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Load GeoJSON file using GeoPandas
jeju_map = gpd.read_file("data/jeju.geojson")
if jeju_map.empty:
    st.stop()
jeju_map = jeju_map[jeju_map.adm_nm != '제주특별자치도 제주시 추자면']


# Load 여행 데이터 
import pandas as pd
df = pd.read_csv('data/final_df_0425.csv')
print('df shape : ',df.shape)

df['adm_nm'] = df.지번주소.apply(lambda x: ' '.join(x.split()[:3]))
dic_addr = {'화북일동':'화북동', '화북이동':'화북동',
            '삼양일동':'삼양동', '삼양이동':'삼양동',
            '아라일동':'아라동', '아라이동':'아라동',
            '오라일동':'오라동', '오라이동':'오라동', '오라삼동':'오라동',
            '외도일동':'외도동', '외도이동':'외도동',
            '이호일동':'이호동', '이호이동':'이호동', 
            '도두일동':'도두동', '도두이동':'도두동',
            '법환동':'대륜동','서호동':'대륜동','호근동':'대륜동',
            '강정동':'대천동','영남동':'대천동','월평동':'대천동','하원동':'대천동',
            '서귀동':'송산동','보목동':'송산동',
            '상효동':'영천동','토평동':'영천동',
            '색달동':'예래동','하예동':'예래동',
            '신효동':'효돈동','하효동':'효돈동',
            '대포동':'중문동','도순동':'중문동','상예동':'중문동','회수동':'중문동'
            }
df['adm_nm'] = df['adm_nm'].replace(dic_addr, regex=True)

# '지번주소'를 기반으로 방문 횟수 집계
df_count = df['adm_nm'].value_counts().reset_index()
df_count.columns = ['adm_nm', 'visit_counts']

# jeju_map에 병합
jeju_map = jeju_map.merge(df_count, on='adm_nm', how='left')
print('jeju_map shape :', jeju_map.shape)

# Title of the Streamlit app
st.title('Jeju Island Administrative Map - ehdms')

# Initialize the map at a central point on Jeju Island
m = folium.Map(location=[33.3617, 126.5292], zoom_start=10)

# 색상을 동적으로 조정하는 함수
def style_function(feature):
    count = feature['properties']['visit_counts']
    if count is None:
        fillColor = 'black'
    else:
        intensity = max(0, 255 - int(min(count, 100) * 2.55))
        fillColor = f'#00{intensity:02x}00'
    
    return {
        'fillColor': fillColor,
        'color': 'black',
        'weight': 2,
        'dashArray': '5, 5',
        'fillOpacity': 0.6
    }

# Add the GeoJSON overlay to the map
folium.GeoJson(
    jeju_map,
    name='Jeju Administrative Areas',
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['adm_nm'], labels=True)  # Using 'adm_nm' as the field name
).add_to(m)

# print(jeju_map[['adm_nm','visit_counts']])

# Display the map in Streamlit
st_data = st_folium(m, width=725, height=500)

# Add some textual information or additional controls if needed
st.write("Interactive map of Jeju Island showing different administrative regions.")
