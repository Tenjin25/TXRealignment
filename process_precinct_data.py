"""
Process precinct-level election data and aggregate to county level
for 2020 and 2022 Texas elections.
"""
import pandas as pd
import json

# Read the precinct data
print("Reading precinct data...")
df = pd.read_csv('Election_Data/election_data_TX.v06-aligned.csv')

# Clean column names (remove leading/trailing spaces)
df.columns = df.columns.str.strip()

# Extract county FIPS from GEOID20 (first 5 characters)
df['county_fips'] = df['GEOID20'].astype(str).str[:5]

# Load FIPS to county name mapping
print("Loading FIPS to county name mapping...")
fips_df = pd.read_csv('TX_Data/texas_county_fips.csv')
fips_df['fips'] = fips_df['fips'].astype(str)
fips_df['county'] = fips_df['county'].str.strip()
fips_to_name = dict(zip(fips_df['fips'], fips_df['county']))

# Map FIPS to county names
df['county_name'] = df['county_fips'].map(fips_to_name)

# Define contests to process
contests_2020 = {
    'President': ('E_20_PRES_Total', 'E_20_PRES_Dem', 'E_20_PRES_Rep'),
    'U.S. Senate': ('E_20_SEN_Total', 'E_20_SEN_Dem', 'E_20_SEN_Rep')
}

contests_2022 = {
    'Governor': ('E_22_GOV_Total', 'E_22_GOV_Dem', 'E_22_GOV_Rep'),
    'Attorney General': ('E_22_AG_Total', 'E_22_AG_Dem', 'E_22_AG_Rep'),
    'Lieutenant Governor': ('E_22_LTG_Total', 'E_22_LTG_Dem', 'E_22_LTG_Rep'),
    'Comptroller': ('E_22_TREAS_Total', 'E_22_TREAS_Dem', 'E_22_TREAS_Rep')
}

# Aggregate to county level
print("Aggregating to county level...")

results = {}

def process_year(year, contests):
    year_results = []
    
    for contest_name, (total_col, dem_col, rep_col) in contests.items():
        # Group by county and sum
        county_data = df.groupby('county_name').agg({
            total_col: 'sum',
            dem_col: 'sum',
            rep_col: 'sum'
        }).reset_index()
        
        # Rename columns for clarity
        county_data.columns = ['county_name', 'total_votes', 'dem_votes', 'rep_votes']
        
        # Calculate third-party votes
        county_data['other_votes'] = county_data['total_votes'] - county_data['dem_votes'] - county_data['rep_votes']
        
        # Add year and contest info
        county_data['year'] = year
        county_data['office'] = contest_name
        county_data['party_dem'] = 'DEM'
        county_data['party_rep'] = 'REP'
        
        year_results.append(county_data)
    
    return pd.concat(year_results, ignore_index=True)

# Process both years
print("Processing 2020...")
results_2020 = process_year(2020, contests_2020)
print(f"  Found {len(results_2020)} county-contest combinations for 2020")

print("Processing 2022...")
results_2022 = process_year(2022, contests_2022)
print(f"  Found {len(results_2022)} county-contest combinations for 2022")

# Combine results
all_results = pd.concat([results_2020, results_2022], ignore_index=True)

# Create output in OpenElections CSV format
output_rows = []

for _, row in all_results.iterrows():
    county_name = row['county_name']
    
    # DEM candidate
    output_rows.append({
        'county': county_name,
        'office': row['office'],
        'party': 'DEM',
        'candidate': '',
        'votes': int(row['dem_votes'])
    })
    
    # REP candidate
    output_rows.append({
        'county': county_name,
        'office': row['office'],
        'party': 'REP',
        'candidate': '',
        'votes': int(row['rep_votes'])
    })
    
    # Other parties (if any votes)
    if row['other_votes'] > 0:
        output_rows.append({
            'county': county_name,
            'office': row['office'],
            'party': 'LIB',  # Assuming Libertarian for third-party
            'candidate': '',
            'votes': int(row['other_votes'])
        })

# Create DataFrames for each year
df_2020 = pd.DataFrame([r for r in output_rows if r['office'] in contests_2020.keys()])
df_2022 = pd.DataFrame([r for r in output_rows if r['office'] in contests_2022.keys()])

# Save to CSV files
print("\nSaving CSV files...")
df_2020.to_csv('Election_Data/20201103__tx__general__county_from_precinct.csv', index=False)
print(f"  Saved 20201103__tx__general__county_from_precinct.csv ({len(df_2020)} rows)")

df_2022.to_csv('Election_Data/20221108__tx__general__county_from_precinct.csv', index=False)
print(f"  Saved 20221108__tx__general__county_from_precinct.csv ({len(df_2022)} rows)")

# Show sample output
print("\n2020 Sample:")
print(df_2020.head(10))

print("\n2022 Sample:")
print(df_2022.head(10))

# County count check
print(f"\nUnique counties in 2020: {df_2020['county'].nunique()}")
print(f"Unique counties in 2022: {df_2022['county'].nunique()}")

print("\n✅ Processing complete!")
