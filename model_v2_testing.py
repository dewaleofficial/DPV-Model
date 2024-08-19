#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from streamlit_folium import st_folium, folium_static
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium import Choropleth, GeoJson
from folium.plugins import HeatMap
from folium import DivIcon
import geopandas as gpd
from shapely.geometry import shape
#######################
# Page configuration
st.set_page_config(
    page_title="DPV Prioritization Model",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#######################
# Load data
raw_df = pd.read_csv('datasets/DPV_Model.csv')
data = raw_df.copy()

# Load the GeoJSON file for Lagos LGAs
geojson_path = "nigeria_lga.json"

#######################
# Sidebar
with st.sidebar:
    st.title('DPV Prioritization Model')
    
    # Define indicators
    economic_indicators = ['Median_household_income', 'Employment_rate', 'Industrial_activity']
    financial_indicators = ['Gen_expenditure', 'Energy_spend_ratio']
    social_indicators = ['Population_density', 'Household_count', 'Building_type_ID', 'Building_type_GD']
    infrastructure_indicators = ['Grid_supply_reliability', 'Road_accessibility', 'Safety']
    environmental_indicators = ['Solar_panel_usage', 'Solar_panel_adoption', 'Emmission_Reduction']

    # Combine all indicators into one list
    all_indicators = (
        economic_indicators +
        financial_indicators +
        social_indicators +
        infrastructure_indicators +
        environmental_indicators
    )

    # Define the indicator groups
    indicator_groups = {
    'Economic Indicators': ['Median_household_income', 'Employment_rate', 'Industrial_activity'],
    'Financial Indicators': ['Gen_expenditure', 'Energy_spend_ratio'],
    'Social Indicators': ['Population_density', 'Household_count', 'Building_type_ID', 'Building_type_GD'],
    'Infrastructure Indicators': ['Grid_supply_reliability', 'Road_accessibility', 'Safety'],
    'Environmental Indicators': ['Solar_panel_usage', 'Solar_panel_adoption', 'Emmission_Reduction']
    }

    # Sliders for each indicator group
    group_sliders = {}
    for group_name, indicators in indicator_groups.items():
        slider_value = st.sidebar.slider(f"{group_name}", min_value=0, max_value=100, value=20, step=10)
        group_sliders[group_name] = slider_value

    # Use the group slider values directly
    sum_economic = group_sliders['Economic Indicators']
    sum_financial = group_sliders['Financial Indicators']
    sum_social = group_sliders['Social Indicators']
    sum_infrastructure = group_sliders['Infrastructure Indicators']
    sum_environmental = group_sliders['Environmental Indicators']


    # Calculate individual indicator weights
    indicator_weights = {}
    for group_name, indicators in indicator_groups.items():
        weight_per_indicator = group_sliders[group_name] / len(indicators)
        for indicator in indicators:
            indicator_weights[indicator] = weight_per_indicator

    # Normalize the data using min-max normalization
    def normalize(column):
        return (column - column.min()) / (column.max() - column.min())

    for indicator in all_indicators:
        data[indicator] = normalize(data[indicator])


    data['Rating'] = 0
    for indicator, weight in indicator_weights.items():
        data['Rating'] += data[indicator] * weight

    # Sort data by the aggregate score
    data = data.sort_values(by='Rating', ascending=False)

    # Total sum of all slider values
    __total_sum = sum_economic + sum_financial + sum_social + sum_infrastructure + sum_environmental

    st.write("SUM OF RATINGS: ", __total_sum)

# Total sum of all slider values
total_sum = sum_economic + sum_financial + sum_social + sum_infrastructure + sum_environmental

# Calculate the percentage of each category relative to the total sum
percentage_economic = round((sum_economic / total_sum) * 100, 0) if total_sum else 0
percentage_financial = round((sum_financial / total_sum) * 100, 0) if total_sum else 0
percentage_social = round((sum_social / total_sum) * 100, 0) if total_sum else 0
percentage_infrastructure = round((sum_infrastructure / total_sum) * 100, 0) if total_sum else 0
percentage_environmental = round((sum_environmental / total_sum) * 100, 0) if total_sum else 0

# Calculate the new aggregate score
data['Rating'] = 0
for indicator, weight in indicator_weights.items():
    data['Rating'] += data[indicator] * weight

# Sort data by the aggregate score
data = data.sort_values(by='Rating', ascending=False)


# Sort data by the aggregate score
data____ = data[['Local Government Area','Rating']]
data____ = data____.reset_index(drop=True)
data____.Rating = data____.Rating.round(2)



# merge with raw data to get rating in a new column with actual values in other columns
# Merge dataframes on the 'key' column
raw_df_with_rating = pd.merge(raw_df, data____, on='Local Government Area')


#######################
# Dashboard Main Panel
col = st.columns((1.5, 3.5, 3), gap='medium')

# CSS to style the metrics
st.markdown("""
    <style>
    .metric-container {
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        text-align: center;
    }
    .metric-label {
        font-size: 0.9rem;
        font-weight: bold;
        color: #333;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

with col[0]:
    st.markdown('#### Weights (%)')

    # Metric with background
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Economic Indicators</div>
            <div class="metric-value">{percentage_economic}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Financial Indicators</div>
            <div class="metric-value">{percentage_financial}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Social Indicators</div>
            <div class="metric-value">{percentage_social}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Infrastructure Indicators</div>
            <div class="metric-value">{percentage_infrastructure}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Environmental Indicators</div>
            <div class="metric-value">{percentage_environmental}</div>
        </div>
    """, unsafe_allow_html=True)







with col[2]:
    st.markdown('#### LGA Ranking')

    st.dataframe(data____,
                 column_order=("Local Government Area", "Rating"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Local Government Area": st.column_config.TextColumn(
                        "Local Government Area",
                    ),
                    "Rating": st.column_config.ProgressColumn(
                        "Rating",
                        format="%f",
                        min_value=0,
                        max_value=max(data____.Rating),
                     )}
                 )
    with st.expander('Summary', expanded=True):
        
        st.write(data____.Rating[0],  " jakhfalhf")








# Select the relevant columns for the heatmap
# Assuming the dataset has these indicators
heatmap_data = data[['Local Government Area', 'Median_household_income', 'Employment_rate',
                     'Industrial_activity', 'Gen_expenditure', 'Energy_spend_ratio',
                     'Population_density', 'Household_count', 'Building_type_ID', 
                     'Building_type_GD', 'Grid_supply_reliability', 'Road_accessibility', 
                     'Safety', 'Solar_panel_usage', 'Solar_panel_adoption', 
                     'Emmission_Reduction']]

# Prepare data for heatmap
heatmap_data = heatmap_data.set_index('Local Government Area').T




with col[1]:
    st.markdown('#### Geospatial Heatmap')

    # Create a Folium map centered around Lagos with a fixed size
    m = folium.Map(location=[6.5244, 3.3792], zoom_start=10, width='100%', height='100%')

    # Load GeoJSON and data files
    geojson = gpd.read_file(geojson_path)  # GeoJSON as GeoDataFrame
    data_df = pd.DataFrame(raw_df_with_rating)  # Assuming `data` is a dict-like structure, convert to DataFrame

     # Merge GeoJSON data with the data DataFrame
    geojson = geojson.merge(data_df, left_on='NAME_2', right_on='Local Government Area')

    # Add the choropleth (heatmap)
    Choropleth(
        geo_data=geojson.__geo_interface__,  # Use the GeoJSON interface of the GeoDataFrame
        name='choropleth',
        data=geojson,
        columns=['Local Government Area', 'Rating'],
        key_on='feature.properties.NAME_2',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Rating'
    ).add_to(m)


    # Add LGA names as labels on the map using folium.Marker with DivIcon
    for _, row in geojson.iterrows():
        folium.Marker(
            location=[row['geometry'].centroid.y, row['geometry'].centroid.x],
            icon=folium.DivIcon(
                icon_size=(150,36),
                icon_anchor=(0,0),
                html=f'<div style="font-size: 6pt; font-weight: light;">{row["Local Government Area"]}</div>'
            )
        ).add_to(m)

        
    # Add info boxes with the LGA names and ratings
    folium.GeoJson(
        data=geojson,
        name="LGA Info",
        tooltip=folium.GeoJsonTooltip(
            fields=[
                'Local Government Area', 
                'Rating',
                'Median_household_income',
                'Energy_spend_ratio',
                'Household_count',
                'Grid_supply_reliability',
                'Solar_panel_usage',
                'Solar_panel_adoption',
                'Emmission_Reduction'
            ],
            aliases=[
                'LGA:', 
                'Overall Rating:',
                'Median Household Income (₦):',
                'Energy Spend to Income Ratio (%):',
                'Household Population:',
                'Grid Supply Reliability (/5):',
                '% of Solar Panel Usage:',
                '% Wiling to adopt solar:',
                'Yearly fuel consumption (Litres):'
                ],
            localize=True,
            sticky=False,
            labels=True,
            style="font-weight: bold;",
            max_width=800
        )
    ).add_to(m)

 #Move the legend using custom CSS
    st.markdown(
        """
        <style>
        .leaflet-control-color-scale {
            transform: translate(-20px, 20px); /* Adjust the position (x, y) */
            right: auto !important;
            left: 20px !important; /* Move to the left side */
            bottom: 10px !important; /* Position above the bottom */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Render the map in the Streamlit app
    folium_static(m, width=420, height=250)

# Create the heatmap using seaborn
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, cmap='YlOrRd', linewidths=.5)
    st.pyplot(plt)
