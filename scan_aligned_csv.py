import pandas as pd

# Read the aligned CSV
print("Reading aligned CSV...")
df = pd.read_csv('Election_Data/election_data_TX.v06-aligned.csv')
df.columns = df.columns.str.strip()

# Extract county FIPS
df['county_fips'] = df['GEOID20'].astype(str).str[:5]

# Overall stats
print(f"\n=== OVERALL STATISTICS ===")
print(f"Total rows (precincts): {len(df):,}")
print(f"Unique counties: {df['county_fips'].nunique()}")

# Lampasas County analysis
print(f"\n=== LAMPASAS COUNTY (FIPS 48281) ===")
lampasas = df[df['county_fips'] == '48281']
print(f"Precincts: {len(lampasas)}")
print(f"2020 President Total: {int(lampasas['E_20_PRES_Total'].sum()):,}")
print(f"2020 President Dem: {int(lampasas['E_20_PRES_Dem'].sum()):,}")
print(f"2020 President Rep: {int(lampasas['E_20_PRES_Rep'].sum()):,}")
print(f"2020 Senate Total: {int(lampasas['E_20_SEN_Total'].sum()):,}")
print(f"2020 Senate Dem: {int(lampasas['E_20_SEN_Dem'].sum()):,}")
print(f"2020 Senate Rep: {int(lampasas['E_20_SEN_Rep'].sum()):,}")

# Show precinct details
print(f"\nLampasas Precincts:")
print(lampasas[['GEOID20', 'Name', 'E_20_PRES_Total', 'E_20_SEN_Total']].to_string())

# Check a few other counties for comparison
print(f"\n=== COMPARISON WITH OTHER COUNTIES ===")
sample_counties = ['48015', '48027', '48061']  # Austin, Bell, Cameron
for fips in sample_counties:
    county_df = df[df['county_fips'] == fips]
    print(f"FIPS {fips}: {len(county_df)} precincts, 2020 Pres: {int(county_df['E_20_PRES_Total'].sum()):,}")

# Check for missing data
print(f"\n=== DATA QUALITY CHECK ===")
print(f"Rows with null GEOID20: {df['GEOID20'].isna().sum()}")
print(f"Rows with zero 2020 Pres votes: {(df['E_20_PRES_Total'] == 0).sum()}")
print(f"Rows with zero 2020 Senate votes: {(df['E_20_SEN_Total'] == 0).sum()}")
