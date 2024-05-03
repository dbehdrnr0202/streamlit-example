import streamlit as st
import geopandas as gpd
import plotly.express as px

# Title of the Streamlit app
st.title('Jeju Island Administrative Map with Plotly')

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

# Additional info
st.write("Interactive map of Jeju Island showing different administrative regions using Plotly.")
