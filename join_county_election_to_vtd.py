import pandas as pd
import geopandas as gpd
import os

# --- CONFIG ---
# Set these paths as needed
VTD_GEOJSON = r'./TX_Data/tl_2012_48_vtd10.geojson'  # Change to your target year
COUNTY_FIPS_CSV = r'./TX_Data/texas_county_fips.csv'
ELECTION_CSV = r'./Election_Data/20121106__tx__general__county.csv'  # Change to your target year
OUTPUT_GEOJSON = r'./TX_Data/tl_2012_48_vtd10_with_election.geojson'

# --- LOAD DATA ---
print('Loading VTD GeoJSON...')
vtd_gdf = gpd.read_file(VTD_GEOJSON)
print('Loading county FIPS...')
fips_df = pd.read_csv(COUNTY_FIPS_CSV, dtype={'fips': str})
print('Loading election results...')
election_df = pd.read_csv(ELECTION_CSV, dtype={'county_fips': str, 'fips': str})

# --- PREPARE FIPS ---
# Try to find the county FIPS column in election data
election_fips_col = None
for col in ['fips', 'county_fips', 'county_fips_code', 'county_fips_number']:
    if col in election_df.columns:
        election_fips_col = col
        break
if not election_fips_col:
    raise Exception('No county FIPS column found in election CSV!')

# --- JOIN FIPS TO VTDs ---
# Most Texas VTDs have a county FIPS property like COUNTYFP10 or COUNTYFP20
county_fips_col = None
for col in vtd_gdf.columns:
    if col.lower().startswith('countyfp'):
        county_fips_col = col
        break
if not county_fips_col:
    raise Exception('No county FIPS property found in VTD GeoJSON!')

# Pad county FIPS to 5 digits (state+county)
vtd_gdf['fips'] = vtd_gdf[county_fips_col].astype(str).str.zfill(5)

# Merge election results onto VTDs (all VTDs in a county get the county's results)
print('Merging election results onto VTDs...')
vtd_gdf = vtd_gdf.merge(election_df, left_on='fips', right_on=election_fips_col, how='left', suffixes=('', '_election'))

# --- SAVE ---
print(f'Saving output to {OUTPUT_GEOJSON}...')
vtd_gdf.to_file(OUTPUT_GEOJSON, driver='GeoJSON')
print('Done!')
