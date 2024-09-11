import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium import Choropleth, GeoJson
from folium.plugins import HeatMap
from folium import DivIcon
from folium.features import DivIcon
import geopandas as gpd
from shapely.geometry import shape
from shapely.geometry import Point

#######################
# Page configuration
st.set_page_config(
    page_title="",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# Load the Excel data
raw_df = pd.read_csv('Datapoints/floating_solar_model.csv')

data = raw_df.copy()

columns_to_exclude = ['Location']

# Functions to calculate scores based on ideal ranges
def range_based_score(value, min_value=6.5, max_value=8.5):
    if min_value <= value <= max_value:
        return 100
    elif value < min_value:
        return (value / min_value) * 100
    else:  # value > max_value
        return (max_value / value) * 100

def range_based_score_2(value, min_value=15, max_value=35):
    if min_value <= value <= max_value:
        return 100
    elif value < min_value:
        return (value / min_value) * 100
    else:  # value > max_value
        return (max_value / value) * 100

def range_based_score_3(value, max_value=1000):
    if value <= max_value:
        return 100
    else:  # value > max_value
        return (max_value / value) * 100

def range_based_score_4(value, min_value=0, max_value=500, next_mil=2000):
    if min_value <= value <= max_value:
        return 100
    elif max_value < value <= next_mil:
        return 75
    else:  # value > next_mil
        return (max_value / value) * 50

def range_based_score_5(value, min_value=0, max_value=0.5, next_mil=30):
    if min_value <= value <= max_value:
        return 100
    elif max_value <= value <= next_mil:
        return 75
    elif value > next_mil:
        return 50
    else:  # value < min_value
        return 0

def range_based_score_6(value, max_value=10):
    if value <= max_value:
        return 100
    else:  # value > max_value
        return (max_value / value) * 100

def range_based_score_7(value, min_value=2, max_value=6):
    if min_value <= value <= max_value:
        return 100
    elif value < min_value:
        return (value / min_value) * 100
    else:  # value > max_value
        return (max_value / value) * 100

def range_based_score_8(value, max_value = 1.0):
    if value <= max_value:
        return 100
    else:  # value > max_value
        return (max_value / value) * 100

def range_based_score_9(value, min_value=4, max_value=6):
    if min_value <= value <= max_value:
        return 100
    elif value < min_value:
        return (value / min_value) * 100
    else:  # value > max_value
        return (max_value / value) * 100

def range_based_score_10(value, min_value=15, max_value=35):
    if min_value <= value <= max_value:
        return 100
    elif value < min_value:
        return (value / min_value) * 100
    else:  # value > max_value
        return (max_value / value) * 100

def range_based_score_11(value, min_value=10000):
    if value >= min_value:
        return 100
    else:  # value > max_value
        return (value / min_value) * 100


# Apply range-based scoring functions to relevant columns
data['pH Value'] = data['pH Value'].apply(range_based_score)
data['Water Temp'] = data['Water Temp'].apply(range_based_score_2)
data['Electrical Conductivity'] = data['Electrical Conductivity'].apply(range_based_score_3)
data['Total Dissolve Solids'] = data['Total Dissolve Solids'].apply(range_based_score_4)
data['Salinity'] = data['Salinity'].apply(range_based_score_5)
data['Turbidity'] = data['Turbidity'].apply(range_based_score_6)
data['Wind Speed'] = data['Wind Speed'].apply(range_based_score_7)
data['Water Current'] = data['Water Current'].apply(range_based_score_8)
data['Max Solar Value'] = data['Max Solar Value'].apply(range_based_score_9)
data['Atmospheric Temperature'] = data['Atmospheric Temperature'].apply(range_based_score_10)
data['Water Size'] = data['Water Size'].apply(range_based_score_11)

def normalize(column):
    min_val = column.min()
    max_val = column.max()
    return (column - min_val) / (max_val - min_val)


data['Land Availability Near Water Body for Supporting Infrastructure'] = normalize(data['Land Availability Near Water Body for Supporting Infrastructure'])
data['Proximity of Land Availability to Water'] = normalize(data['Proximity of Land Availability to Water'])
data['Proximity to nearest substation'] = normalize(data['Proximity to nearest substation'])





#######################
# Sidebar
with st.sidebar:
    st.title('')
 
    Water_Quality_indicator = ['pH Value', 'Water Temp', 'Electrical Conductivity', 'Total Dissolve Solids', 'Salinity', 'Turbidity']
    Resource_Assessment_indicator =  ['Water Size', 'Water Current', 'Land Availability Near Water Body for Supporting Infrastructure', 'Proximity of Land Availability to Water', 'Wind Speed']
    Solar_Irradiation_indicator = ['Max Solar Value', 'Atmospheric Temperature']
    Anchor_Points_indicator = ['Anchor Point availability', 'Distance of anchor point to Water']
    Site_Accessibility_indicator = ['Access road availability', 'Distance to access road', 'Type of access road', 'Accessible for heavy equipment']
    Proximity_to_Consumption_Centers_indicator = ['Available Grid Capacity (MVA)', 'Energy Demand (MW)', 'Predominant Consumption Type (R,C,I) or Mixed']
    Proximity_to_Grid_indicator =  ['Proximity to nearest substation', 'Availability of Grid Connection']
    Safety_and_Security_indicator = ['How safe is the environment', 'Incidence of Vandalism/Theft']
    Strategic_Positioning_indicator = ['Is water body close to Schools? Healtcare Centers? Other strategic locations that increase viability, attract fi0ncing and promote renewable deployments']

    # Combine all indicators into one list
    all_indicators = (
        Water_Quality_indicator +
        Resource_Assessment_indicator +
        Solar_Irradiation_indicator +
        Anchor_Points_indicator +
        Site_Accessibility_indicator +
        Proximity_to_Consumption_Centers_indicator +
        Proximity_to_Grid_indicator +
        Safety_and_Security_indicator +
        Strategic_Positioning_indicator 
    )

    # Define the indicator groups
    indicator_groups = {
        'Water Quality Indicators': Water_Quality_indicator,
        'Resource Assessment Indicators': Resource_Assessment_indicator,
        'Solar Irradiation Indicators': Solar_Irradiation_indicator,
        'Anchor Points Indicators': Anchor_Points_indicator,
        'Site Accessibility Indicators': Site_Accessibility_indicator,
        'Proximity to Consumption Centers Indicators': Proximity_to_Consumption_Centers_indicator,
        'Proximity to Grid Indicators': Proximity_to_Grid_indicator,
        'Safety and Security Indicators': Safety_and_Security_indicator,
        'Strategic Positioning Indicators': Strategic_Positioning_indicator
    }



    # Predefined slider values for each group
    weight_structures = {
        "Vista (Recommendation": {
            'Water Quality Indicators': 10.00,
            'Resource Assessment Indicators': 15.00,
            'Solar Irradiation Indicators': 10.00,
            'Anchor Points Indicators': 5.00,
            'Site Accessibility Indicators': 10.00,
            'Proximity to Consumption Centers Indicators': 15.00,
            'Proximity to Grid Indicators': 25,
            'Safety and Security Indicators': 5.00,
            'Strategic Positioning Indicators': 5.00
        },
        "Investor": {
            'Water Quality Indicators': 10.00,
            'Resource Assessment Indicators': 15.00,
            'Solar Irradiation Indicators': 10.00,
            'Anchor Points Indicators': 5.00,
            'Site Accessibility Indicators': 10.00,
            'Proximity to Consumption Centers Indicators': 15.00,
            'Proximity to Grid Indicators': 25,
            'Safety and Security Indicators': 5.00,
            'Strategic Positioning Indicators': 5.00
        },
        "Custom": {
            'Water Quality Indicators': 10.00,
            'Resource Assessment Indicators': 15.00,
            'Solar Irradiation Indicators': 10.00,
            'Anchor Points Indicators': 5.00,
            'Site Accessibility Indicators': 10.00,
            'Proximity to Consumption Centers Indicators': 15.00,
            'Proximity to Grid Indicators': 25,
            'Safety and Security Indicators': 5.00,
            'Strategic Positioning Indicators': 5.00
        }
    }

    # Dropdown to select weight structure
    selected_structure = st.selectbox(
        "Select Template",
        options=list(weight_structures.keys())
    )

    # If the user selects "Custom", show sliders for manual input
    if selected_structure == "Custom":
        st.subheader("Adjust Custom Weights")
        
        # Sliders for each indicator group
        group_sliders = {}
        for group_name, indicators in indicator_groups.items():
            slider_value = st.sidebar.slider(f"{group_name}", min_value=0, max_value=100, value=20, step=2)
            group_sliders[group_name] = slider_value

        # Use the group slider values directly
        sum_Water_Quality = group_sliders['Water Quality Indicators']
        sum_Resource_Assessment = group_sliders['Resource Assessment Indicators']
        sum_Solar_Irradiation = group_sliders['Solar Irradiation Indicators']
        sum_Anchor_Points = group_sliders['Anchor Points Indicators']
        sum_Site_Accessibility = group_sliders['Site Accessibility Indicators']
        sum_Proximity_to_Consumption_Centers = group_sliders['Proximity to Consumption Centers Indicators']
        sum_Proximity_to_Grid = group_sliders['Proximity to Grid Indicators']
        sum_Safety_and_Security = group_sliders['Safety and Security Indicators']
        sum_Strategic_Positioning = group_sliders['Strategic Positioning Indicators']

    else:
        
        # Retrieve the weights based on the selected structure
        selected_weights = weight_structures[selected_structure]

        # Use the group slider values directly
        sum_Water_Quality = selected_weights['Water Quality Indicators']
        sum_Resource_Assessment = selected_weights['Resource Assessment Indicators']
        sum_Solar_Irradiation = selected_weights['Solar Irradiation Indicators']
        sum_Anchor_Points = selected_weights['Anchor Points Indicators']
        sum_Site_Accessibility = selected_weights['Site Accessibility Indicators']
        sum_Proximity_to_Consumption_Centers = selected_weights['Proximity to Consumption Centers Indicators']
        sum_Proximity_to_Grid = selected_weights['Proximity to Grid Indicators']
        sum_Safety_and_Security = selected_weights['Safety and Security Indicators']
        sum_Strategic_Positioning = selected_weights['Strategic Positioning Indicators']
    
    # Calculate individual indicator weights
    indicator_weights = {}
    for group_name, indicators in indicator_groups.items():
        if selected_structure == "Custom":
            weight_per_indicator = group_sliders[group_name] / len(indicators)
            for indicator in indicators:
                indicator_weights[indicator] = weight_per_indicator
        else:            
            weight_per_indicator = selected_weights[group_name] / len(indicators)
            for indicator in indicators:
                indicator_weights[indicator] = weight_per_indicator

    # Normalize the data using min-max normalization
    def normalize(column):
        min_val = column.min()
        max_val = column.max()
        if min_val == max_val:
            return column  # No normalization if min == max
        return (column - min_val) / (max_val - min_val)


    for indicator in all_indicators:
        data[indicator] = normalize(data[indicator])

    
    # Calculate overall rating
    data['Rating'] = 0


    for indicator, weight in indicator_weights.items():
    # Loop through all indicators, apply weights, and compute the aggregate score
        max_value = data[indicator].max()
        data['Rating'] += data[indicator] * weight



    #########################################################################
    #def to return percentage
    def percentage_re(score, max_indicator_score):
        return (score/max_indicator_score) * 100

    # Function to format values with colored percentages based on score and weight
    def format_category(score, percentage, threshold):
        # Safeguard against division by zero
        if threshold == 0:
            return "Threshold is zero"
        
        if score == 0:
            return "No score"
        
        if percentage == 0:
            return "No percentage"

        # This ensures that we don't divide by zero
        threshold = max(threshold, 1)
        
    # Format the result with color based on the percentage, and score to 2 decimal places
        if percentage >= 50:
            return f'{score:.2f} (<span style="color:green;">{percentage:.2f}%</span>)'  # Green for 50% and above
        else:
            return f'{score:.2f} (<span style="color:red;">{percentage:.2f}%</span>)'   # Red for below 50%
   
# Function to format values with colored percentages based on score and weight
    def format_category_1(score, percentage):
        if score == 0:
            return "No score"
        
        if percentage == 0:
            return "No percentage"
    # Format the result with color based on the percentage, and score to 2 decimal places
        if percentage >= 50:
            return percentage
        else:
            return percentage
      
   
   
    # Calculate and store scores for each indicator group
    for group_name, indicators in indicator_groups.items():
        group_weight = selected_weights[group_name] if selected_structure != "Custom" else group_sliders[group_name]
        
        for indicator in indicators:
            # Create score column for each indicator
            max_value = data[indicator].max()
            score_column = f"{group_name}_score"  # Change the naming convention for clarity
            
            if indicator in data.columns and indicator not in columns_to_exclude:
                data[indicator + '_score'] = data[indicator] * group_weight  # Calculate score for each indicator
                data[score_column] = data[indicator + '_score']  # Assign score to new column
            else:
                data[indicator + '_score'] = 0  # Default value for excluded columns           
                data[score_column] = data[indicator + '_score']
            
            


# Ensure sum_economic and others are not zero
    sum_Water_Quality = max(sum_Water_Quality, 1)
    sum_Resource_Assessment = max(sum_Resource_Assessment, 1)
    sum_Solar_Irradiation = max(sum_Solar_Irradiation, 1)
    sum_Anchor_Points = max(sum_Anchor_Points, 1)
    sum_Site_Accessibility = max(sum_Site_Accessibility, 1)
    sum_Proximity_to_Consumption_Centers = max(sum_Proximity_to_Consumption_Centers, 1)
    sum_Proximity_to_Grid = max(sum_Proximity_to_Grid, 1)
    sum_Safety_and_Security = max(sum_Safety_and_Security, 1)
    sum_Strategic_Positioning = max(sum_Strategic_Positioning, 1)
       
    # Now, apply the lambda function safely
    formatted_data = {
        'Water Body': data['Location'],
        'Water Quality': data['Water Quality Indicators_score'].apply(
            lambda x: format_category(x, (x / sum_Water_Quality) * 100, sum_Water_Quality/2)
        ),
        'Resource Assessment': data['Resource Assessment Indicators_score'].apply(
            lambda x: format_category(x, (x / sum_Resource_Assessment) * 100, sum_Resource_Assessment/2)
        ),
        'Solar Irradiation': data['Solar Irradiation Indicators_score'].apply(
            lambda x: format_category(x, (x / sum_Solar_Irradiation) * 100, sum_Solar_Irradiation/2)
        ),
        'Anchor Points': data['Anchor Points Indicators_score'].apply(
            lambda x: format_category(x, (x / sum_Anchor_Points) * 100, sum_Anchor_Points/2)
        ),
        'Site Accessibility': data['Site Accessibility Indicators_score'].apply(
            lambda x: format_category(x, (x / sum_Site_Accessibility) * 100, sum_Site_Accessibility/2)
        ),
        'Proximity to Consumption Centers': data['Proximity to Consumption Centers Indicators_score'].apply(
            lambda x: format_category(x, (x / sum_Proximity_to_Consumption_Centers) * 100, sum_Proximity_to_Consumption_Centers/2)
        ),
        'Proximity to Grid': data['Proximity to Grid Indicators_score'].apply(
            lambda x: format_category(x, (x / sum_Proximity_to_Grid) * 100, sum_Proximity_to_Grid/2)
        ),
        'Safety and Security': data['Safety and Security Indicators_score'].apply(
            lambda x: format_category(x, (x / sum_Safety_and_Security) * 100, sum_Safety_and_Security/2)
        ),
        'Strategic Positioning': data['Strategic Positioning Indicators_score'].apply(
            lambda x: format_category(x, (x / sum_Strategic_Positioning) * 100, sum_Strategic_Positioning/2)
        ),
        
        'Rating': (
        data['Water Quality Indicators_score'] + 
        data['Resource Assessment Indicators_score'] + 
        data['Solar Irradiation Indicators_score'] + 
        data['Anchor Points Indicators_score'] + 
        data['Site Accessibility Indicators_score'] + 
        data['Proximity to Consumption Centers Indicators_score'] +
        data['Proximity to Grid Indicators_score']+
        data['Safety and Security Indicators_score']+
        data['Strategic Positioning Indicators_score']
    ).apply(
        lambda x: format_category(x, (x / (sum_Water_Quality + sum_Resource_Assessment + sum_Solar_Irradiation + sum_Anchor_Points + sum_Site_Accessibility + sum_Proximity_to_Consumption_Centers + sum_Proximity_to_Grid + sum_Safety_and_Security + sum_Strategic_Positioning)) * 100, 50)
    )  ,
        'Ratings': (
        data['Water Quality Indicators_score'] + 
        data['Resource Assessment Indicators_score'] + 
        data['Solar Irradiation Indicators_score'] + 
        data['Anchor Points Indicators_score'] + 
        data['Site Accessibility Indicators_score'] + 
        data['Proximity to Consumption Centers Indicators_score'] +
        data['Proximity to Grid Indicators_score']+
        data['Safety and Security Indicators_score']+
        data['Strategic Positioning Indicators_score']
    ) ,
        'Rating(100%)':(
        data['Water Quality Indicators_score'] + 
        data['Resource Assessment Indicators_score'] + 
        data['Solar Irradiation Indicators_score'] + 
        data['Anchor Points Indicators_score'] + 
        data['Site Accessibility Indicators_score'] + 
        data['Proximity to Consumption Centers Indicators_score'] +
        data['Proximity to Grid Indicators_score']+
        data['Safety and Security Indicators_score']+
        data['Strategic Positioning Indicators_score']
    ).apply(
        lambda x: format_category_1(x, (x / (sum_Water_Quality + sum_Resource_Assessment + sum_Solar_Irradiation + sum_Anchor_Points + sum_Site_Accessibility + sum_Proximity_to_Consumption_Centers + sum_Proximity_to_Grid + sum_Safety_and_Security + sum_Strategic_Positioning)) * 100)
    )  
    }

    # Convert formatted data to DataFrame
    
    aggr_df = pd.DataFrame(formatted_data)
    aggr_df = aggr_df.sort_values(by = 'Ratings', ascending=False)
    summary_1_df = aggr_df[['Water Body', 'Water Quality', 'Resource Assessment', 'Solar Irradiation', 'Anchor Points', 'Site Accessibility', 'Proximity to Consumption Centers', 'Proximity to Grid', 'Safety and Security', 'Strategic Positioning', 'Rating']]

    summary_2_df = aggr_df[['Water Body', 'Water Quality', 'Resource Assessment', 'Solar Irradiation', 'Anchor Points', 'Site Accessibility', 'Proximity to Consumption Centers', 'Proximity to Grid', 'Safety and Security', 'Strategic Positioning', 'Ratings', 'Rating(100%)']]
  #  summary_2_df = summary_2_df.fillna(0)
    
     # Sort data by the aggregate score
    summary_2_df['Ratings'] = summary_2_df['Ratings'].round(2)
    summary_2_df['Rating(100%)'] = summary_2_df['Rating(100%)'].round(2)




    # Display total sum of all slider values
    total_sum = sum_Water_Quality + sum_Resource_Assessment + sum_Solar_Irradiation + sum_Anchor_Points + sum_Site_Accessibility + sum_Proximity_to_Consumption_Centers + sum_Proximity_to_Grid + sum_Safety_and_Security + sum_Strategic_Positioning
    st.write("SUM OF RATINGS: ", total_sum)

    # Calculate the percentage of each category relative to the total sum
    percentage_Water_Quality = round((sum_Water_Quality / total_sum) * 100, 0) if total_sum else 0
    percentage_Resource_Assessment = round((sum_Resource_Assessment / total_sum) * 100, 0) if total_sum else 0
    percentage_Solar_Irradiation = round((sum_Solar_Irradiation / total_sum) * 100, 0) if total_sum else 0
    percentage_Anchor_Points = round((sum_Anchor_Points / total_sum) * 100, 0) if total_sum else 0
    percentage_Site_Accessibility = round((sum_Site_Accessibility / total_sum) * 100, 0) if total_sum else 0
    percentage_Proximity_to_Consumption_Centers = round((sum_Proximity_to_Consumption_Centers / total_sum) * 100, 0) if total_sum else 0
    percentage_Proximity_to_Grid = round((sum_Proximity_to_Grid / total_sum) * 100, 0) if total_sum else 0
    percentage_Safety_and_Security = round((sum_Safety_and_Security / total_sum) * 100, 0) if total_sum else 0
    percentage_Strategic_Positioning = round((sum_Strategic_Positioning / total_sum) * 100, 0) if total_sum else 0




# Optionally plot maps or charts here


#######################
# Dashboard Main Panel
col = st.columns((2.5,2.5,3.0), gap='medium')

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
            <div class="metric-label">Water Quality</div>
            <div class="metric-value">{percentage_Water_Quality}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Resource Assessment</div>
            <div class="metric-value">{percentage_Resource_Assessment}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Solar Irradiation</div>
            <div class="metric-value">{percentage_Solar_Irradiation}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Anchor Points</div>
            <div class="metric-value">{percentage_Anchor_Points}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Site Accessibility</div>
            <div class="metric-value">{percentage_Site_Accessibility}</div>
        </div>
    """, unsafe_allow_html=True)




# Creating two columns inside col[1]
with col[1]:
    st.markdown('#### Weights (%)')
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Proximity to Consumption</div>
            <div class="metric-value">{percentage_Proximity_to_Consumption_Centers}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Proximity to Grid</div>
            <div class="metric-value">{percentage_Proximity_to_Grid}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Safety & Security</div>
            <div class="metric-value">{percentage_Safety_and_Security}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Strategic Positioning</div>
            <div class="metric-value">{percentage_Strategic_Positioning}</div>
        </div>
    """, unsafe_allow_html=True)


with col[2]:
    st.markdown('#### Water Body Ranking')

    st.dataframe(summary_2_df,
                column_order=("Water Body", 
                                "Rating(100%)",
                                "Ratings"),
                hide_index=True,
                width=None,
                column_config={
                    "Water Body": st.column_config.TextColumn(
                        "Water Body",
                    ),
                    "Rating(100%)":st.column_config.TextColumn(
                        "Rating(100%)"
                    ),
                    "Ratings": st.column_config.ProgressColumn(
                        "Ratings",
                        format="%f",
                        min_value=0,
                        max_value=max(summary_2_df.Ratings),
                    )}
                )
    # Alternatively, you can use st.container() if you need more complex layout or control
with st.container():
    with st.expander('Summary', expanded=True):
        st.markdown(summary_1_df.to_html(escape=False, index=False), unsafe_allow_html=True)

