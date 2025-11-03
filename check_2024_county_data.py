import json

# Load the data
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

# Check 2024 county data
pres_2024 = data['results_by_year']['2024']['presidential']['president']

print("2024 Presidential County-Level Analysis:")
print("=" * 80)
print(f"Number of counties: {len(pres_2024['results'])}")

# Check a few counties for sanity
counties_to_check = ['ANDERSON', 'TRAVIS', 'HARRIS']
for county in counties_to_check:
    if county in pres_2024['results']:
        county_data = pres_2024['results'][county]
        print(f"\n{county}:")
        print(f"  Total votes: {county_data['total_votes']:,}")
        print(f"  Dem votes: {county_data['dem_votes']:,}")
        print(f"  Rep votes: {county_data['rep_votes']:,}")
        print(f"  Other votes: {county_data['other_votes']:,}")
        print(f"  Sum: {county_data['dem_votes'] + county_data['rep_votes'] + county_data['other_votes']:,}")

# Find counties with astronomically high totals
print("\n" + "=" * 80)
print("\nCounties with suspiciously high totals:")
for county, county_data in pres_2024['results'].items():
    if county_data['total_votes'] > 10_000_000:  # More than 10M votes in a single county is impossible
        print(f"  {county}: {county_data['total_votes']:,}")
