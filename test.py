import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Path to your GeoJSON file
geo_data = "jeju.geojson"

# Title of the Streamlit app
st.title('Jeju Island Administrative Map')

# Load GeoJSON file using GeoPandas
try:
    jeju_map = gpd.read_file(geo_data)
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

if jeju_map.empty:
    st.error("No data loaded into GeoDataFrame.")
    st.stop()

# Initialize the map at a central point on Jeju Island
m = folium.Map(location=[33.3617, 126.5292], zoom_start=10)

# Function to determine style (optional customization)
def style_function(feature):
    return {
        'fillColor': 'green',
        'color': 'black',
        'weight': 2,
        'dashArray': '5, 5'
    }

# Add the GeoJSON overlay to the map
folium.GeoJson(
    jeju_map,
    name='Jeju Administrative Areas',
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=['adm_nm'], labels=True)  # Using 'adm_nm' as the field name
).add_to(m)

# Display the map in Streamlit
st_data = st_folium(m, width=725, height=500)

# Add some textual information or additional controls if needed
st.write("Interactive map of Jeju Island showing different administrative regions.")
