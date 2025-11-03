import pandas as pd

df = pd.read_csv('Election_Data/election_data_TX.v06-aligned.csv')
# Use correct column name for county
lampasas = df[df[' Name  '].str.upper().str.strip() == 'LAMPASAS']

print('Lampasas County - 2020 U.S. Senate Aggregation:')
print('Total:', lampasas[' E_20_SEN_Total'].sum())
print('Dem:', lampasas[' E_20_SEN_Dem'].sum())
print('Rep:', lampasas[' E_20_SEN_Rep'].sum())
print('Other:', lampasas[' E_20_SEN_Total'].sum() - lampasas[' E_20_SEN_Dem'].sum() - lampasas[' E_20_SEN_Rep'].sum())