import pandas as pd

df = pd.read_csv('Election_Data/20201103__tx__general__county_from_precinct.csv')

print('First 20 unique counties:')
print(sorted(df['county'].unique())[:20])
print(f'\nTotal unique counties: {df["county"].nunique()}')

# Check if Lampasas appears anywhere
lampasas_rows = df[df['county'].str.contains('Lamp', case=False, na=False)]
print(f'\nRows containing "Lamp": {len(lampasas_rows)}')
if len(lampasas_rows) > 0:
    print(lampasas_rows[['county', 'office', 'votes']].head(10))
