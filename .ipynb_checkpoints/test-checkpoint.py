import pandas as pd

residential_df = pd.read_excel("residential_dashboard_data.xlsx")


#print(residential_df.head())

print(residential_df[["Primary source of income of the household?"]].head())

