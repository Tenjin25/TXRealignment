import pandas as pd
import json

# Load the JSON to see how it's stored
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("CHECKING COUNTY NAMES IN JSON")
print("=" * 80)

# Get 2018 US Senate county names
if '2018' in data['results_by_year'] and 'us_senate' in data['results_by_year']['2018']:
    senate_2018 = data['results_by_year']['2018']['us_senate']['us_senate']
    results = senate_2018.get('results', {})
    
    # Look for El Paso variations
    el_paso_variants = [name for name in results.keys() if 'PASO' in name or 'EL' in name[:5]]
    
    print(f"\nCounties containing 'PASO' or starting with 'EL':")
    for county in sorted(el_paso_variants):
        county_data = results[county]
        dem = county_data.get('dem_votes', 0)
        rep = county_data.get('rep_votes', 0)
        print(f"  '{county}': DEM {dem:,}, REP {rep:,}")

print("\n" + "=" * 80)
print("CHECKING VTD FILE FOR EL PASO")
print("=" * 80)

# Check the VTD CSV
try:
    df = pd.read_csv('Election_Data/2018_General_Election_Returns-aligned.csv', on_bad_lines='skip')
    df.columns = df.columns.str.strip()
    
    # Check unique county names that contain "paso" or "el"
    counties = df['County'].dropna().unique()
    el_paso_like = [c for c in counties if 'paso' in str(c).lower() or str(c).lower().startswith('el')]
    
    print(f"\nCounties in VTD file containing 'paso' or starting with 'el':")
    for county in sorted(el_paso_like):
        count = len(df[df['County'] == county])
        print(f"  '{county}': {count} rows")
    
    # Check for El Paso specifically with different formats
    for test_name in ['El Paso', 'EL PASO', 'ElPaso', 'el paso']:
        match = df[df['County'].str.strip().str.upper() == test_name.upper()]
        if len(match) > 0:
            print(f"\n✅ Found using '{test_name}': {len(match)} rows")
            # Get US Senate data
            us_sen = match[match['Office'].str.contains('Sen', case=False, na=False)]
            if len(us_sen) > 0:
                print(f"   US Senate rows: {len(us_sen)}")
                for party in ['D', 'R']:
                    party_votes = us_sen[us_sen['Party'].str.upper() == party]['Votes'].sum()
                    print(f"   {party}: {party_votes:,}")
            break
    
except FileNotFoundError:
    print("VTD file not found")
except Exception as e:
    print(f"Error reading VTD file: {e}")

print("\n" + "=" * 80)
print("CHECKING HOW COUNTIES ARE NORMALIZED")
print("=" * 80)
print("\nThe issue: County names might have:")
print("  - Multiple words: 'El Paso' vs 'EL PASO' vs 'ELPASO'")
print("  - The processing script likely converts to uppercase: 'EL PASO'")
print("  - But it might also be stripping/merging words")
