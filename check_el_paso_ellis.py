import json

# Load the JSON file
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("CHECKING EL PASO AND ELLIS COUNTY DATA")
print("=" * 80)

# 2018 U.S. Senate
if '2018' in data['results_by_year'] and 'us_senate' in data['results_by_year']['2018']:
    senate_2018 = data['results_by_year']['2018']['us_senate']['us_senate']
    results = senate_2018.get('results', {})
    
    print("\n2018 U.S. Senate:")
    print("-" * 80)
    
    for county_name in ['EL PASO', 'ELLIS']:
        if county_name in results:
            county_data = results[county_name]
            dem = county_data.get('dem_votes', 0)
            rep = county_data.get('rep_votes', 0)
            total = county_data.get('total_votes', 0)
            print(f"\n{county_name}:")
            print(f"  DEM: {dem:,}")
            print(f"  REP: {rep:,}")
            print(f"  Total: {total:,}")
            print(f"  Winner: {county_data.get('winner', 'N/A')}")
    
    print("\n" + "=" * 80)
    print("Expected values (from official sources):")
    print("-" * 80)
    print("\nEL PASO County (heavily Democratic, border county):")
    print("  Expected ~134,000 DEM, ~46,000 REP")
    print("  (About 74% DEM / 26% REP)")
    
    print("\nELLIS County (Republican, south of Dallas):")
    print("  Expected ~19,106 DEM, ~41,022 REP (from VTD data)")
    print("  (About 32% DEM / 68% REP)")
    
    # Check if values match
    if 'EL PASO' in results:
        ep_dem = results['EL PASO'].get('dem_votes', 0)
        ep_rep = results['EL PASO'].get('rep_votes', 0)
        
        if ep_dem == 19106 and ep_rep == 41022:
            print("\n⚠️  ERROR FOUND!")
            print("   EL PASO has ELLIS County's values!")
            print("   This explains the missing ~115,000 Democratic votes!")

# Also check all counties to find any others that might have Ellis values
print("\n" + "=" * 80)
print("Searching for duplicate Ellis County values:")
print("-" * 80)
if '2018' in data['results_by_year'] and 'us_senate' in data['results_by_year']['2018']:
    senate_2018 = data['results_by_year']['2018']['us_senate']['us_senate']
    results = senate_2018.get('results', {})
    
    ellis_signature = (19106, 41022)
    duplicates = []
    
    for county, county_data in results.items():
        dem = county_data.get('dem_votes', 0)
        rep = county_data.get('rep_votes', 0)
        if (dem, rep) == ellis_signature:
            duplicates.append(county)
    
    if len(duplicates) > 1:
        print(f"⚠️  Found {len(duplicates)} counties with Ellis County values:")
        for county in sorted(duplicates):
            print(f"    - {county}")
    elif duplicates:
        print(f"✅ Only ELLIS has these values (correct)")
