import json

# Load the data
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

# Check 2024 to see how the total is calculated
year = '2024'
pres = data['results_by_year'][year]['presidential']['president']

print("2024 Presidential Data:")
print(f"Stored total_votes: {pres['total_votes']:,}")
print(f"Number of counties in results: {len(pres.get('results', {}))}")

# Calculate actual total from county data
if 'results' in pres and pres['results']:
    county_total = sum(county_data['total_votes'] for county_data in pres['results'].values())
    print(f"Sum from county data: {county_total:,}")
    
    # Check candidate totals
    if 'dem_candidate' in pres and isinstance(pres['dem_candidate'], dict):
        print(f"Dem candidate votes: {pres['dem_candidate'].get('votes', 'N/A')}")
    if 'rep_candidate' in pres and isinstance(pres['rep_candidate'], dict):
        print(f"Rep candidate votes: {pres['rep_candidate'].get('votes', 'N/A')}")
    if 'other_votes' in pres:
        print(f"Other votes: {pres['other_votes']:,}")
    
    # Try calculating from dem + rep + other
    dem_votes = pres.get('dem_candidate', {}).get('votes', 0) if isinstance(pres.get('dem_candidate'), dict) else 0
    rep_votes = pres.get('rep_candidate', {}).get('votes', 0) if isinstance(pres.get('rep_candidate'), dict) else 0
    other_votes = pres.get('other_votes', 0)
    calculated_total = dem_votes + rep_votes + other_votes
    print(f"Calculated from candidates: {calculated_total:,}")

print("\n" + "="*80)
print("\n2000 Senate (known to be overcounted by 2.39x):")
senate_2000 = data['results_by_year']['2000']['us_senate']['us_senate']
print(f"Stored total_votes: {senate_2000['total_votes']:,}")
if 'results' in senate_2000 and senate_2000['results']:
    county_total = sum(county_data['total_votes'] for county_data in senate_2000['results'].values())
    print(f"Sum from county data: {county_total:,}")
