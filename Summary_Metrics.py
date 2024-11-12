import streamlit as st
import pandas as pd
import altair as alt
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
dpv_data = pd.read_csv('Datapoints/DPV_Model.csv')
dpv_df = dpv_data.copy()



#######################
# Load data
dpv_data_gen_count = pd.read_csv('Datapoints/DPV_Model_gen_count.csv')
dpv_df_gen_count = dpv_data_gen_count.copy()



# Merging on a similar column, e.g., 'id'
dpv_df = pd.merge(dpv_df, dpv_df_gen_count, on='Local Government Area', how='inner')  # 'how' can be 'inner', 'outer', 'left', or 'right'



wb_data = pd.read_csv('Datapoints/floating_solar_model.csv')
wb_df = wb_data.copy()



st.sidebar.header('Filters')

LGA = st.sidebar.multiselect(
    "Select the LGA:",
    options=dpv_df['Local Government Area'].unique(),
    #default='Select LGA'
)


dpv_selection = dpv_df.query(
    "`Local Government Area` == @LGA"
) if LGA else dpv_df


##############
local_government_count = dpv_selection.shape[0] if LGA else dpv_df.shape[0]
avg_household_income = dpv_selection['Median_household_income'].mean() if LGA else dpv_df['Median_household_income'].mean()
avg_Industrial_activity = dpv_selection['Industrial_activity'].mean() if LGA else dpv_df['Industrial_activity'].mean()
avg_Gen_expenditure = dpv_selection['Gen_expenditure'].mean() if LGA else dpv_df['Gen_expenditure'].mean()
avg_Energy_spend_ratio = dpv_selection['Energy_spend_ratio'].mean() if LGA else dpv_df['Energy_spend_ratio'].mean()
avg_Population_density = dpv_selection['Population_density'].mean() if LGA else dpv_df['Population_density'].mean()
Total_Household_count = dpv_selection['Household_count'].sum() if LGA else dpv_df['Household_count'].sum()
avg_Grid_supply_reliability = (dpv_selection['Grid_supply_reliability'].mean()/5 * 100) if LGA else (dpv_df['Grid_supply_reliability'].mean()/5 * 100)
avg_Road_accessibility = (dpv_selection['Road_accessibility'].mean()/5 *100) if LGA else (dpv_df['Road_accessibility'].mean()/5 * 100)
avg_Safety = (dpv_selection['Safety'].mean()/5 *100)  if LGA else (dpv_df['Safety'].mean()/5 *100) 
avg_Solar_panel_usage = dpv_selection['Solar_panel_usage'].mean() if LGA else dpv_df['Solar_panel_usage'].mean()
avg_Solar_panel_adoption = dpv_selection['Solar_panel_adoption'].mean() if LGA else dpv_df['Solar_panel_adoption'].mean()
total_Emmission_Reduction = dpv_selection['Emmission_Reduction'].sum() if LGA else dpv_df['Emmission_Reduction'].sum()
total_gen_count = dpv_df_gen_count['Generator Count'].sum() if LGA else dpv_df['Generator Count'].sum()
Employment_rate = dpv_selection['Employment_rate'].mean() if LGA else dpv_df['Employment_rate'].mean()

	


import streamlit as st

# CSS for styling the metric containers
st.markdown("""
    <style>
    .metric-container {
        width: 200px,
        display: inline-block;
        padding: 20px;
        margin: 5px;
        background-color: #f0f2f6; /* Light background color */
        border-radius: 10px; /* Rounded corners */
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1); /* Light shadow */
        text-align: center;
        width: 200px; /* Fixed width for consistency */
    }
    .metric-container h3 {
        font-size: 1.5rem;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Creating a function to wrap the st.metric in a styled container
def display_styled_metric(label, value, delta, icon):
    st.markdown(f"""
    <div class="metric-container">
        <h5>{icon} {label}</h5>
        <h6><strong>{value}</strong></h6>
    </div>
    """, unsafe_allow_html=True)

# Display metrics in columns
col1, col2, col3 = st.columns(3)


# Creating two columns inside col[1]
with col1:
    inner_col1, inner_col2 = st.columns(2)

    # Add content to inner_col1
    with inner_col1:
        st.markdown('#### General')
        display_styled_metric("Local Government Count", f"{local_government_count:,.0f}", "", "📍")
        st.markdown('#### ')
        st.markdown('#### Social')
        display_styled_metric("Avg Population Density",  f"{avg_Population_density:,.0f}", "", "🌐")
        display_styled_metric("Household Count", f"{Total_Household_count:,.0f}", "", "👨‍👨‍👦‍👦")
    
    # Add content to inner_col1
    with inner_col2:
        st.markdown('#### ')
        display_styled_metric("Estimated Generator Count", f"{total_gen_count:,.0f}", "", "🔌")
        st.markdown('#### ')
        st.markdown('#### ')
        display_styled_metric("Safety Rating",  f"{avg_Safety:,.2f}%", "", "⚠️")




with col2:
    inner_col2A, inner_col2B = st.columns(2)

    # Add content to inner_col1
    with inner_col2A:
        st.markdown('#### Financial')
        display_styled_metric("Avg Monthly Generator Expenditure", f"₦{avg_Gen_expenditure:,.0f}", "", "💳")
 
        st.markdown('#### ')

        st.markdown('#### Economic')
        display_styled_metric("Household Income",  f"₦{avg_household_income:,.0f}", "", "💰")
        display_styled_metric("Commercial Activities (Residential)",  f"{avg_Industrial_activity:,.2f}%", "", "🏭")
        

   
    
    # Add content to inner_col1
    with inner_col2B:
        st.markdown('#### ')
        display_styled_metric("Energy Spend  to Income Ratio",  f"{avg_Energy_spend_ratio:,.2f}%", "", "💲")
    
        st.markdown('#### ')
        st.markdown('#### ')
        display_styled_metric("Employement Rate",  f"{Employment_rate:,.2f}%", "", "👨‍💼")












with col3:
    inner_col3A, inner_col3B = st.columns(2)
    
    # Add content to inner_col1
    with inner_col3A:
        st.markdown('#### Infrastructure')
        display_styled_metric("Grid Availability",  f"{avg_Grid_supply_reliability:,.2f}%", "", "⚡")
    
        st.markdown('#### ')
        st.markdown('#### Environmental')
        display_styled_metric("Solar Panel Usage (%)", f"{avg_Solar_panel_usage:,.2f}%", "", "🔆")
        display_styled_metric("Solar Interest (%)",  f"{avg_Solar_panel_adoption:,.2f}%", "", "🔆")
    

   
    
    # Add content to inner_col1
    with inner_col3B:
        st.markdown('#### ')
        display_styled_metric("Road Accessibility",  f"{avg_Road_accessibility:,.2f}%", "", "🚗")
 
        st.markdown('#### ')

        st.markdown('#### ')
        display_styled_metric("Yearly Fuel Consumption (L)",  f"{total_Emmission_Reduction:,.2f}", "", "⛽")
