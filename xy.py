import pandas as pd

# Sample DataFrame
data = {
    'Column1': ['ABC', 'XYZ', 'TDNLBY'],
    'Column2': ['123', 'jj', '456'],
    'Column3': ['789', 'DEF', 'GHI']
}
df = pd.DataFrame(data)

# Check if "TDNL" is present in any of the columns
if df.apply(lambda x: x.str.contains('TDNL', na=False)).any().any():
    print("TDNL is present in at least one column.")
else:
    print("TDNL is not present in any column.")
