import streamlit as st
import pandas as pd

# Load the data
data = pd.read_csv("C:/Users/Vista/Documents/Projects/DPV-Model/DPV_Model.csv")

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

# Normalize the data using min-max normalization
def normalize(column):
    return (column - column.min()) / (column.max() - column.min())

for indicator in all_indicators:
    data[indicator] = normalize(data[indicator])

# Streamlit app
st.title("DPV Model Scoring App")

st.sidebar.header("Adjust Weights")

def weight_slider(category):
    weights = {}
    for indicator in category:
        weights[indicator] = st.sidebar.slider(f"{indicator}", 0, 100, 50, step=10)
    return weights

st.sidebar.subheader("Economic Indicators")
economic_weights = weight_slider(economic_indicators)

st.sidebar.subheader("Financial Indicators")
financial_weights = weight_slider(financial_indicators)

st.sidebar.subheader("Social Indicators")
social_weights = weight_slider(social_indicators)

st.sidebar.subheader("Infrastructure Indicators")
infrastructure_weights = weight_slider(infrastructure_indicators)

st.sidebar.subheader("Environmental Indicators")
environmental_weights = weight_slider(environmental_indicators)

# Combine all weights into one dictionary and normalize them
user_weights = {**economic_weights, **financial_weights, **social_weights, **infrastructure_weights, **environmental_weights}

total_weight = sum(user_weights.values())
normalized_weights = {key: value / total_weight for key, value in user_weights.items()}

# Calculate the new aggregate score
data['Aggregate_score'] = 0
for indicator, weight in normalized_weights.items():
    data['Aggregate_score'] += data[indicator] * weight

# Sort data by the aggregate score
data = data.sort_values(by='Aggregate_score', ascending=False)

# Display the data
st.header("Rescored Data")
st.write(data)
