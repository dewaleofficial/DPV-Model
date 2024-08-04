import pandas as pd


## Use the absolute path to the file
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

# Assign weights and calculate the aggregate score
weights = {
    'Median_household_income': 0.2,
    'Employment_rate': 0.15,
    'Industrial_activity': 0.15,
    'Gen_expenditure': 0.1,
    'Energy_spend_ratio': 0.1,
    'Population_density': 0.05,
    'Household_count': 0.05,
    'Building_type_ID': 0.05,
    'Building_type_GD': 0.05,
    'Grid_supply_reliability': 0.1,
    'Road_accessibility': 0.1,
    'Safety': 0.1,
    'Solar_panel_usage': 0.15,
    'Solar_panel_adoption':0.15,
    'Emmission_Reduction': 0.1
}


data['Aggregate_score'] = 0
for indicator, weight in weights.items():
    data['Aggregate_score'] += data[indicator] * weight

# Sort data by the aggregate score
data = data.sort_values(by='Aggregate_score', ascending=False)

print(data)
