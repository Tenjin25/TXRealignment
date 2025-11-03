import pandas as pd

# Read the aligned CSV
print("Testing aggregation for Lampasas County...")
df = pd.read_csv('Election_Data/election_data_TX.v06-aligned.csv')
df.columns = df.columns.str.strip()

# Extract county FIPS
df['county_fips'] = df['GEOID20'].astype(str).str[:5]

# Load FIPS to county name mapping
fips_df = pd.read_csv('TX_Data/texas_county_fips.csv')
fips_df['fips'] = fips_df['fips'].astype(str)
fips_df['county'] = fips_df['county'].str.strip()
fips_to_name = dict(zip(fips_df['fips'], fips_df['county']))

# Map FIPS to county names
df['county_name'] = df['county_fips'].map(fips_to_name)

print(f"\nTotal precincts in CSV: {len(df)}")
print(f"Precincts with mapped county names: {df['county_name'].notna().sum()}")
print(f"Precincts without mapped county names: {df['county_name'].isna().sum()}")

# Check Lampasas specifically
lampasas = df[df['county_fips'] == '48281']
print(f"\nLampasas precincts: {len(lampasas)}")
print(f"Lampasas county_name values: {lampasas['county_name'].unique()}")

# Try manual aggregation for Lampasas Senate
lampasas_agg = lampasas.groupby('county_name').agg({
    'E_20_SEN_Total': 'sum',
    'E_20_SEN_Dem': 'sum',
    'E_20_SEN_Rep': 'sum'
}).reset_index()

print(f"\nManual aggregation for Lampasas 2020 Senate:")
print(lampasas_agg)

# Check if there's a FIPS mapping issue
print(f"\nFIPS 48281 maps to: {fips_to_name.get('48281', 'NOT FOUND')}")
