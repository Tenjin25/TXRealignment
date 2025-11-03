import pandas as pd

# Read the aligned CSV
df = pd.read_csv('Election_Data/election_data_TX.v06-aligned.csv')
df.columns = df.columns.str.strip()

# Extract county FIPS
df['county_fips'] = df['GEOID20'].astype(str).str[:5]

# Filter for Lampasas County (FIPS 48281)
lampasas = df[df['county_fips'] == '48281']

print(f"Lampasas County Analysis:")
print(f"  Number of precincts: {len(lampasas)}")
print(f"  2020 President Total: {lampasas['E_20_PRES_Total'].sum()}")
print(f"  2020 President Dem: {lampasas['E_20_PRES_Dem'].sum()}")
print(f"  2020 President Rep: {lampasas['E_20_PRES_Rep'].sum()}")
print(f"  2020 Senate Total: {lampasas['E_20_SEN_Total'].sum()}")
print(f"  2020 Senate Dem: {lampasas['E_20_SEN_Dem'].sum()}")
print(f"  2020 Senate Rep: {lampasas['E_20_SEN_Rep'].sum()}")

print(f"\nSample precincts:")
print(lampasas[['GEOID20', 'Name', 'E_20_PRES_Total', 'E_20_SEN_Total']].head(10))

# Compare to expected county total (from official sources)
print(f"\n⚠️ If these totals are significantly lower than expected,")
print(f"   the aligned CSV may be missing Lampasas precincts.")
