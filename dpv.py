import streamlit as st
import pandas as pd

st.title("DPV Prioritization model")
st.markdown("_Prototype v0.4.1_")

@st.cache_data
def load_data(file):
    data = pd.read_excel(file)
    return data

df = load_data("residential_dashboard_data.xlsx")

with st.expander("Data Preview"):
    st.dataframe(df)