import streamlit as st
import pandas as pd
import altair as alt
import folium
from folium import Choropleth, GeoJson
from folium import DivIcon
from folium.features import DivIcon
from streamlit_folium import folium_static
import geopandas as gpd
import pandas as pd

#######################
# Page configuration
st.set_page_config(
    page_title="Indicator Weights",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")

#######################
# Load data
raw_df = pd.read_csv('Datapoints/DPV_Model.csv')
data = raw_df.copy()

# Load the GeoJSON file for Lagos LGAs
geojson_path = "Datapoints/nigeria_lga.json"


# Normalize specific columns
def normalize(column):
    min_val = column.min()
    max_val = column.max()
    if min_val == max_val:
        norm_dig = 100
    else:
        norm_dig = (column - min_val) / (max_val - min_val) * 100  # Multiply by 100 to keep consistency
    return norm_dig

data['Median_household_income'] = normalize(data['Median_household_income'])
data['Employment_rate'] = normalize(data['Employment_rate'])
data['Industrial_activity'] = normalize(data['Industrial_activity'])
data['Gen_expenditure'] = normalize(data['Gen_expenditure'])
data['Energy_spend_ratio'] = normalize(data['Energy_spend_ratio'])
data['Population_density'] = normalize(data['Population_density'])
data['Household_count'] = normalize(data['Household_count'])
data['Safety'] = normalize(data['Safety'])
data['Grid_supply_reliability'] = normalize(data['Grid_supply_reliability'])
data['Road_accessibility'] = normalize(data['Road_accessibility'])
data['Building_type_ID'] = normalize(data['Building_type_ID'])
data['Building_type_GD'] = normalize(data['Building_type_GD'])
data['Solar_panel_usage'] = normalize(data['Solar_panel_usage'])
data['Solar_panel_adoption'] = normalize(data['Solar_panel_adoption'])
data['Emmission_Reduction'] = normalize(data['Emmission_Reduction'])


#######################
# Sidebar
with st.sidebar:
    st.title('Indicator Weights and Subweights')
		

    # Define indicators
    economic_indicators = ['Median_household_income', 'Employment_rate', 'Industrial_activity']
    financial_indicators = ['Gen_expenditure', 'Energy_spend_ratio']
    social_indicators = ['Population_density', 'Household_count', 'Safety']
    infrastructure_indicators = ['Grid_supply_reliability', 'Road_accessibility', 'Building_type_ID', 'Building_type_GD']
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
        'Economic Indicators': economic_indicators,
        'Financial Indicators': financial_indicators,
        'Social Indicators': social_indicators,
        'Infrastructure Indicators': infrastructure_indicators,
        'Environmental Indicators': environmental_indicators
    }

    # Define descriptions for each classification
    descriptions = {
        'Economic Indicators': "Economic indicators measure the financial health and economic activity within a local government area.",
        'Financial Indicators': "Financial indicators assess the spending patterns and financial resilience of a region.",
        'Social Indicators': "Social indicators reflect the demographic and social structure of a community.",
        'Infrastructure Indicators': "Infrastructure indicators evaluate the quality and availability of essential services and facilities.",
        'Environmental Indicators': "Environmental indicators focus on the region's adoption of sustainable practices and the impact on the environment."
    }

    # Predefined slider values for each group
    weight_structures = {
        "Developer": {
            'Economic Indicators': 20,
            'Financial Indicators': 20,
            'Social Indicators': 15,
            'Infrastructure Indicators': 30,
            'Environmental Indicators': 15
        },
        "Investor": {
            'Economic Indicators': 30,
            'Financial Indicators': 30,
            'Social Indicators': 10,
            'Infrastructure Indicators': 20,
            'Environmental Indicators': 10
        },
        "Government Official": {
            'Economic Indicators': 15,
            'Financial Indicators': 15,
            'Social Indicators': 20,
            'Infrastructure Indicators': 20,
            'Environmental Indicators': 30
        },
        "Custom": {
            'Economic Indicators': 20,
            'Financial Indicators': 20,
            'Social Indicators': 20,
            'Infrastructure Indicators': 20,
            'Environmental Indicators': 20
        }
    }

    # Sub-weight structures for each group
    sub_weight_structures = { 
        "Developer": {
            'Median_household_income': 8, 'Employment_rate': 6, 'Industrial_activity': 6,
            'Gen_expenditure': 8, 'Energy_spend_ratio': 12,
            'Population_density': 6, 'Household_count': 6, 'Safety': 3,
            'Building_type_ID': 4.5, 'Building_type_GD': 4.5, 'Grid_supply_reliability': 15, 'Road_accessibility': 6,
            'Solar_panel_usage': 3, 'Solar_panel_adoption': 6, 'Emmission_Reduction': 6
        },
        "Investor": {
            'Median_household_income': 8, 'Employment_rate': 6, 'Industrial_activity': 6,
            'Gen_expenditure': 8, 'Energy_spend_ratio': 12,
            'Population_density': 6, 'Household_count': 6, 'Safety': 3,
            'Building_type_ID': 4.5, 'Building_type_GD': 4.5, 'Grid_supply_reliability': 15, 'Road_accessibility': 6,
            'Solar_panel_usage': 3, 'Solar_panel_adoption': 6, 'Emmission_Reduction': 6
        },
        "Government Official": {
            'Median_household_income': 8, 'Employment_rate': 6, 'Industrial_activity': 6,
            'Gen_expenditure': 8, 'Energy_spend_ratio': 12,
            'Population_density': 6, 'Household_count': 6, 'Safety': 3,
            'Building_type_ID': 4.5, 'Building_type_GD': 4.5, 'Grid_supply_reliability': 15, 'Road_accessibility': 6,
            'Solar_panel_usage': 3, 'Solar_panel_adoption': 6, 'Emmission_Reduction': 6
        },
        "Custom": {
            # For Custom, initial sub-weights can be equally distributed or copied from one of the predefined structures
            # ...
        }
    }

    # Dropdown to select weight structure
    selected_structure = st.selectbox(
        "Select Template",
        options=list(weight_structures.keys())
    )


    # Define sliders and sub-sliders for "Custom" structure
    group_sliders = {}
    sub_sliders = {}

    if selected_structure == "Custom":
        st.subheader("Adjust Custom Weights")

        # Main weight sliders for each indicator group
        total_group_weight = 0
        for group_name, indicators in indicator_groups.items():
            slider_value = st.slider(f"{group_name}", min_value=0.0, max_value=100.0, value=11.11, step=0.01)
            group_sliders[group_name] = slider_value
            total_group_weight += slider_value

####
            with st.expander(f"Adjust {group_name} Subweights"):
                sub_sliders[group_name] = {}
                total_sub_weight = 0
                for indicator in indicators:
                    sub_slider_value = st.slider(
                        f"{indicator}",
                        min_value=0.0,
                        max_value=100.0,
                        value=100 / len(indicators),
                        step=0.1
                    )
                    sub_sliders[group_name][indicator] = sub_slider_value
                    total_sub_weight += sub_slider_value

                # Normalize sub-weights to sum to 100
                if total_sub_weight != 0:
                    for indicator in indicators:
                        sub_sliders[group_name][indicator] = (sub_sliders[group_name][indicator] / total_sub_weight) * 100
####

        # Normalize group weights to sum to 100
        if total_group_weight != 0:
            for group_name in group_sliders:
                group_sliders[group_name] = (group_sliders[group_name] / total_group_weight) * 100

#####
        selected_weights = group_sliders

        # Calculate individual indicator weights based on sliders
        indicator_weights = {}
        for group_name, indicators in indicator_groups.items():
            group_weight = group_sliders[group_name]

            for indicator in indicators:
                sub_weight = sub_sliders[group_name][indicator] / 100  # Normalize to fraction
                indicator_weight = (group_weight) * sub_weight  # Calculate final indicator weight
                indicator_weights[indicator] = indicator_weight
        
        # Use the group slider values directly
        sum_economic = group_sliders['Economic Indicators']
        sum_financial = group_sliders['Financial Indicators']
        sum_social = group_sliders['Social Indicators']
        sum_infrastructure = group_sliders['Infrastructure Indicators']
        sum_environmental = group_sliders['Environmental Indicators']

    else:
        # Retrieve the weights based on the selected structure
        selected_weights = weight_structures[selected_structure]

        # Display the main group weights as text
        st.subheader(f"{selected_structure} Weights")
        for group_name, weight in selected_weights.items():
            st.write(f"**{group_name}:** {weight}%")

            # Expander to show subweights as text
            with st.expander(f"View {group_name} Subweights"):
                group_sub_weights = {}
                total_sub_weight = 0
                for indicator in indicator_groups[group_name]:
                    sub_weight = sub_weight_structures[selected_structure][indicator]
                    group_sub_weights[indicator] = sub_weight
                    total_sub_weight += sub_weight

                # Normalize sub-weights to sum to 100
                for indicator in indicator_groups[group_name]:
                    group_sub_weights[indicator] = (group_sub_weights[indicator] / total_sub_weight) * 100

                # Display subweights as text
                for indicator, sub_weight in group_sub_weights.items():
                    st.write(f"- **{indicator}:** {sub_weight:.2f}%")

        # Calculate individual indicator weights for predefined structures
        indicator_weights = {}
        for group_name, indicators in indicator_groups.items():
            group_weight = selected_weights[group_name]

            # Get sub-weights for this group and normalize
            group_sub_weights = {}
            total_sub_weight = 0
            for indicator in indicators:
                sub_weight = sub_weight_structures[selected_structure][indicator]
                group_sub_weights[indicator] = sub_weight
                total_sub_weight += sub_weight

            # Normalize sub-weights to sum to 100
            for indicator in indicators:
                group_sub_weights[indicator] = (group_sub_weights[indicator] / total_sub_weight) * 100

            # Calculate final indicator weights
            for indicator in indicators:
                sub_weight = group_sub_weights[indicator] / 100  # Normalize to fraction
                indicator_weight = group_weight * sub_weight  # Calculate final indicator weight
                indicator_weights[indicator] = indicator_weight       


        # Use the group slider values directly
        sum_economic = selected_weights['Economic Indicators']
        sum_financial = selected_weights['Financial Indicators']
        sum_social = selected_weights['Social Indicators']
        sum_infrastructure = selected_weights['Infrastructure Indicators']
        sum_environmental = selected_weights['Environmental Indicators']
 

    # Calculate the 'Rating' for each location
    data['Rating'] = 0

    # Calculate the rating as the sum of each indicator's value multiplied by its weight
    for indicator, weight in indicator_weights.items():
        data['Rating'] += data[indicator] * weight / 100  # Divide by 100 to adjust weight percentage

    # Ensure that scores for each indicator group are calculated and reflected properly
    for group_name, indicators in indicator_groups.items():
        # Initialize the score column for the group
        score_column = f"{group_name}_score"
        data[score_column] = 0  # Initialize the score column to 0

        # Sum up the scores for each indicator in the group
        for indicator in indicators:
            data[score_column] += data[indicator] * indicator_weights[indicator] / 100




    #########################################################################
    # Function to format values with colored percentages based on score and weight
    def format_category(score, percentage, threshold):
        # Safeguard against division by zero
        if threshold == 0:
            return "Threshold is zero"
        
        if score == 0:
            return "0"
        
        if percentage == 0:
            return "0%"

        # This ensures that we don't divide by zero
        percentage = (score / (max(threshold, 1)*2)) * 100  # Ensures threshold is at least 1
        
    # Format the result with color based on the percentage, and score to 2 decimal places
        if percentage >= 50:
            return f'{score:.2f} (<span style="color:green;">{percentage:.2f}%</span>)'  # Green for 50% and above
        else:
            return f'{score:.2f} (<span style="color:red;">{percentage:.2f}%</span>)'   # Red for below 50%
  
    # Ensure sum_economic and others are not zero
    sum_economic = max(sum_economic,1)
    sum_financial = max(sum_financial,1)
    sum_social = max(sum_social,1)
    sum_infrastructure = max(sum_infrastructure,1)
    sum_environmental = max(sum_environmental,1)
    

    # Format the results
    formatted_data = {
        'LGA': data['Local Government Area'],
        'Economic': data['Economic Indicators_score'].apply(
            lambda x: format_category(x, (x / sum_economic) * 100, sum_economic / 2)
        ),
        'Financial': data['Financial Indicators_score'].apply(
            lambda x: format_category(x, (x / sum_financial) * 100, sum_financial / 2)
        ),
        'Social': data['Social Indicators_score'].apply(
            lambda x: format_category(x, (x / sum_social) * 100, sum_social / 2)
        ),
        'Infrastructure': data['Infrastructure Indicators_score'].apply(
            lambda x: format_category(x, (x / sum_infrastructure) * 100, sum_infrastructure / 2)
        ),
        'Environmental': data['Environmental Indicators_score'].apply(
            lambda x: format_category(x, (x / sum_environmental) * 100, sum_environmental / 2)
        ),
        'Rated_value': (
            data['Rating']
        ),
        'Rating': (
            data['Economic Indicators_score'] +
            data['Financial Indicators_score'] +
            data['Social Indicators_score'] +
            data['Infrastructure Indicators_score'] +
            data['Environmental Indicators_score']
        ).apply(
            lambda x: format_category(x, (x / (sum_economic + sum_financial + sum_social + sum_infrastructure + sum_environmental)) * 100, 50)
        ),
        'Ratings': (
            data['Economic Indicators_score'] +
            data['Financial Indicators_score'] +
            data['Social Indicators_score'] +
            data['Infrastructure Indicators_score'] +
            data['Environmental Indicators_score']
        )  # Summing and rounding the total score to 2 decimal places
    }

    # Convert formatted data to DataFrame
    aggr_df = pd.DataFrame(formatted_data)

    summary_1_df = aggr_df[['LGA', 'Economic', 'Financial', 'Social', 'Infrastructure', 'Environmental', 'Rating', 'Rated_value']]

    summary_2_df = aggr_df[['LGA', 'Economic', 'Financial', 'Social', 'Infrastructure', 'Environmental', 'Ratings', 'Rated_value']]

     # Sort data by the aggregate score
    summary_1_df = summary_1_df.sort_values(by='Rating', ascending=False)
    summary_2_df= summary_2_df.sort_values(by='Ratings', ascending=False)
    summary_2_df['Ratings'] = summary_2_df['Ratings'].round(1)




    # Display total sum of all slider values
    total_sum = sum_economic + sum_financial + sum_social + sum_infrastructure + sum_environmental
    st.write("SUM OF RATINGS: ", total_sum)

    # Calculate the percentage of each category relative to the total sum
    percentage_economic = round((sum_economic / total_sum) * 100, 0) if total_sum else 0
    percentage_financial = round((sum_financial / total_sum) * 100, 0) if total_sum else 0
    percentage_social = round((sum_social / total_sum) * 100, 0) if total_sum else 0
    percentage_infrastructure = round((sum_infrastructure / total_sum) * 100, 0) if total_sum else 0
    percentage_environmental = round((sum_environmental / total_sum) * 100, 0) if total_sum else 0


# Optionally plot maps or charts here


# Sort data by the aggregate score
data____ = data[['Local Government Area','Rating']]
data____ = data____.reset_index(drop=True)
data____.Rating = data____.Rating.round(2)



# merge with raw data to get rating in a new column with actual values in other columns
# Merge dataframes on the 'key' column
raw_df_with_rating = pd.merge(raw_df, data____, on='Local Government Area')


#######################
# Dashboard Main Panel
col = st.columns((1.5,6.5), gap='medium')

st.markdown("""
    <style>
    /* Style for the metric containers */
    .metric-container {
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        text-align: center;
        justify-content: space-between;
        align-items: center;
    }

    /* Style for the labels */
    .metric-label {
        font-size: 0.9rem;
        font-weight: bold;
        color: #333;
        align-items: center;
    }

    /* Style for the values */
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #ff4b4b;
    }

    /* Tooltip icon and styling */
    .tooltip-icon {
        display: inline-block;
        position: relative;
        cursor: pointer;
        margin-left: 5px;
        color: #17a2b8;
        font-size: 1rem;
    }

    .tooltip-text {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%; /* Position above the icon */
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }

    .tooltip-icon:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    </style>
""", unsafe_allow_html=True)


with col[0]:
    st.markdown('#### Weights (%)')

    # Metric with background and hover description icon
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">
                Economic Indicators 
                <span class="tooltip-icon">ℹ️
                    <span class="tooltip-text">Economic indicators measure the financial health and economic activity within a local government area.</span>
                </span>
            </div>
            <div class="metric-value">{percentage_economic}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">
                Financial Indicators 
                <span class="tooltip-icon">ℹ️
                    <span class="tooltip-text">Financial indicators assess the spending patterns and financial resilience of a region.</span>
                </span>
            </div>
            <div class="metric-value">{percentage_financial}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">
                Social Indicators 
                <span class="tooltip-icon">ℹ️
                    <span class="tooltip-text">Social indicators reflect the demographic and social structure of a community.</span>
                </span>
            </div>
            <div class="metric-value">{percentage_social}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">
                Infrastructure Indicators 
                <span class="tooltip-icon">ℹ️
                    <span class="tooltip-text">Infrastructure indicators evaluate the quality and availability of essential services and facilities.</span>
                </span>
            </div>
            <div class="metric-value">{percentage_infrastructure}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">
                Environmental Indicators 
                <span class="tooltip-icon">ℹ️
                    <span class="tooltip-text">Environmental indicators focus on the region's adoption of sustainable practices and the impact on the environment.</span>
                </span>
            </div>
            <div class="metric-value">{percentage_environmental}</div>
        </div>
    """, unsafe_allow_html=True)




# Creating two columns inside col[1]
with col[1]:
    inner_col1, inner_col2 = st.columns(2)

    # Add content to inner_col1
    with inner_col1:
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
                icon=folium.DivIcon(  # type: ignore
                    icon_size=(150, 36),
                    icon_anchor=(0, 0),
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

        # Render the map in the Streamlit app
        folium_static(m, width= 350, height=400)


    # Add content to inner_col2
    with inner_col2:
        st.markdown('#### Local Government Ranking')

        st.dataframe(summary_2_df,
                    column_order=("LGA", 
                                    "Ratings"),
                    hide_index=True,
                    width=None,
                    column_config={
                        "LGA": st.column_config.TextColumn(
                            "LGA",
                        ),
                        "Ratings": st.column_config.ProgressColumn(
                            "Ratings",
                            format="%f",
                            min_value=0,
                            max_value=100,
                        )}
                    )


    # Alternatively, you can use st.container() if you need more complex layout or control
    with st.container():
        with st.expander('Summary', expanded=True):
            st.markdown(summary_1_df.to_html(escape=False, index=False), unsafe_allow_html=True)

