import pandas as pd

# Load county-level aggregation
county_df = pd.read_csv('Election_Data/20201103__tx__general__county_from_precinct.csv')
lampasas_county = county_df[(county_df['county'].str.upper() == 'LAMPASAS') & (county_df['office'] == 'U.S. Senate')]
print('County-level aggregation for Lampasas, U.S. Senate:')
print(lampasas_county)

# Load precinct-level data
precinct_df = pd.read_csv('Election_Data/20201103__tx__general__precinct.csv')
lampasas_precincts = precinct_df[(precinct_df['county'].str.upper() == 'LAMPASAS') & (precinct_df['office'] == 'U.S. Senate')]
print('\nPrecinct-level totals for Lampasas, U.S. Senate:')
print(lampasas_precincts.groupby(['party', 'candidate'])['votes'].sum())

print('\nTotal votes by party:')
print(lampasas_precincts.groupby('party')['votes'].sum())