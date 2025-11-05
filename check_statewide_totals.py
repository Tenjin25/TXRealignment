import json

# Load the JSON file
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("=" * 70)
print("STATEWIDE TOTALS VERIFICATION")
print("=" * 70)

# Check 2018 U.S. Senate statewide totals
us_senate_2018 = data['results_by_year']['2018']['us_senate']['us_senate']
statewide_2018 = us_senate_2018.get('statewide_totals', {})

print("\n2018 U.S. Senate - Statewide Totals:")
dem_votes = statewide_2018.get('dem_votes', 'N/A')
rep_votes = statewide_2018.get('rep_votes', 'N/A')
other_votes = statewide_2018.get('other_votes', 'N/A')
total_votes_sw = statewide_2018.get('total_votes', 'N/A')

print(f"  DEM votes: {dem_votes if dem_votes == 'N/A' else f'{dem_votes:,}'}")
print(f"  REP votes: {rep_votes if rep_votes == 'N/A' else f'{rep_votes:,}'}")
print(f"  Other votes: {other_votes if other_votes == 'N/A' else f'{other_votes:,}'}")
print(f"  Total votes: {total_votes_sw if total_votes_sw == 'N/A' else f'{total_votes_sw:,}'}")
print(f"  DEM candidate: {us_senate_2018.get('dem_candidate', 'N/A')}")
print(f"  REP candidate: {us_senate_2018.get('rep_candidate', 'N/A')}")

# Calculate sum from all counties
print("\n2018 U.S. Senate - Sum of All County Results:")
results = us_senate_2018.get('results', {})
total_dem = 0
total_rep = 0
total_other = 0
total_votes = 0
county_count = 0

for county, county_data in results.items():
    if county != 'statewide':  # Skip if there's a statewide entry in results
        total_dem += county_data.get('dem_votes', 0)
        total_rep += county_data.get('rep_votes', 0)
        total_other += county_data.get('other_votes', 0)
        total_votes += county_data.get('total_votes', 0)
        county_count += 1

print(f"  DEM votes (sum): {total_dem:,}")
print(f"  REP votes (sum): {total_rep:,}")
print(f"  Other votes (sum): {total_other:,}")
print(f"  Total votes (sum): {total_votes:,}")
print(f"  Counties counted: {county_count}")

# Check if they match
print("\n" + "=" * 70)
if statewide_2018.get('dem_votes') == total_dem:
    print("✅ DEM votes match!")
else:
    print(f"❌ DEM votes DON'T match! Difference: {statewide_2018.get('dem_votes', 0) - total_dem:,}")

if statewide_2018.get('rep_votes') == total_rep:
    print("✅ REP votes match!")
else:
    print(f"❌ REP votes DON'T match! Difference: {statewide_2018.get('rep_votes', 0) - total_rep:,}")

if statewide_2018.get('total_votes') == total_votes:
    print("✅ Total votes match!")
else:
    print(f"❌ Total votes DON'T match! Difference: {statewide_2018.get('total_votes', 0) - total_votes:,}")

# Also check 2014
print("\n" + "=" * 70)
print("2014 U.S. Senate - Statewide Totals:")
print("=" * 70)

us_senate_2014 = data['results_by_year']['2014']['us_senate']['us_senate']
statewide_2014 = us_senate_2014.get('statewide_totals', {})

dem_votes_2014 = statewide_2014.get('dem_votes', 'N/A')
rep_votes_2014 = statewide_2014.get('rep_votes', 'N/A')
other_votes_2014 = statewide_2014.get('other_votes', 'N/A')
total_votes_sw_2014 = statewide_2014.get('total_votes', 'N/A')

print(f"  DEM votes: {dem_votes_2014 if dem_votes_2014 == 'N/A' else f'{dem_votes_2014:,}'}")
print(f"  REP votes: {rep_votes_2014 if rep_votes_2014 == 'N/A' else f'{rep_votes_2014:,}'}")
print(f"  Other votes: {other_votes_2014 if other_votes_2014 == 'N/A' else f'{other_votes_2014:,}'}")
print(f"  Total votes: {total_votes_sw_2014 if total_votes_sw_2014 == 'N/A' else f'{total_votes_sw_2014:,}'}")

# Calculate sum from all counties for 2014
print("\n2014 U.S. Senate - Sum of All County Results:")
results_2014 = us_senate_2014.get('results', {})
total_dem_2014 = 0
total_rep_2014 = 0
total_other_2014 = 0
total_votes_2014 = 0
county_count_2014 = 0

for county, county_data in results_2014.items():
    if county != 'statewide':
        total_dem_2014 += county_data.get('dem_votes', 0)
        total_rep_2014 += county_data.get('rep_votes', 0)
        total_other_2014 += county_data.get('other_votes', 0)
        total_votes_2014 += county_data.get('total_votes', 0)
        county_count_2014 += 1

print(f"  DEM votes (sum): {total_dem_2014:,}")
print(f"  REP votes (sum): {total_rep_2014:,}")
print(f"  Other votes (sum): {total_other_2014:,}")
print(f"  Total votes (sum): {total_votes_2014:,}")
print(f"  Counties counted: {county_count_2014}")

print("\n" + "=" * 70)
if statewide_2014.get('dem_votes') == total_dem_2014:
    print("✅ DEM votes match!")
else:
    print(f"❌ DEM votes DON'T match! Difference: {statewide_2014.get('dem_votes', 0) - total_dem_2014:,}")

if statewide_2014.get('rep_votes') == total_rep_2014:
    print("✅ REP votes match!")
else:
    print(f"❌ REP votes DON'T match! Difference: {statewide_2014.get('rep_votes', 0) - total_rep_2014:,}")
