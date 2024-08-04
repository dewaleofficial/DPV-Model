import pandas as pd

residential_df = pd.read_csv("residential_data.csv")
residential_df.head()

data = pd.DataFrame({
    # Example structure of your data
    'GDP_per_capita': [10000, 20000, 30000],
    'Employment_rate': [95, 90, 85],
    'Industrial_activity': [70, 80, 90],
    'Household_income': [50000, 60000, 70000],
    'Fuel_expenditure': [5000, 6000, 7000],
    'Energy_spend_ratio': [0.1, 0.15, 0.2],
    'Population_density': [100, 200, 300],
    'Household_count': [1000, 1500, 2000],
    'Building_type': [0.3, 0.4, 0.5],  # Assuming a numerical representation
    'Grid_supply_reliability': [99, 95, 90],
    'Road_accessibility': [80, 85, 90],
    'Safety': [80, 85, 90],
    'Solar_panel_usage': [0.05, 0.1, 0.15],
    'Environmental_impact': [0.1, 0.2, 0.3]
})





economic_indicators = ['GDP_per_capita', 'Employment_rate', 'Industrial_activity']
financial_indicators = ['Household_income', 'Fuel_expenditure', 'Energy_spend_ratio']
social_indicators = ['Population_density', 'Household_count', 'Building_type']
infrastructure_indicators = ['Grid_supply_reliability', 'Road_accessibility', 'Safety']
environmental_indicators = ['Solar_panel_usage', 'Environmental_impact']


# Assign weights and calculate the aggregate score
weights = {
    'GDP_per_capita': 0.2,
    'Employment_rate': 0.15,
    'Industrial_activity': 0.15,
    'Household_income': 0.2,
    'Fuel_expenditure': 0.1,
    'Energy_spend_ratio': 0.1,
    'Population_density': 0.05,
    'Household_count': 0.05,
    'Building_type': 0.05,
    'Grid_supply_reliability': 0.1,
    'Road_accessibility': 0.1,
    'Safety': 0.1,
    'Solar_panel_usage': 0.15,
    'Environmental_impact': 0.1
}

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



data['Aggregate_score'] = 0
for indicator, weight in weights.items():
    data['Aggregate_score'] += data[indicator] * weight

# Sort data by the aggregate score
data = data.sort_values(by='Aggregate_score', ascending=False)

print(data)

