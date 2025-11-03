import json

with open('data/texas_election_results.json') as f:
    data = json.load(f)

y2024 = data['results_by_year'].get('2024', {})

print("2024 Categories and Contests:")
for cat, contests in y2024.items():
    print(f"  {cat}:")
    for contest_key, contest_data in contests.items():
        print(f"    - {contest_data.get('contest_name', contest_key)}")
        print(f"      Counties: {len(contest_data.get('results', {}))}")

# Check sample data
if y2024:
    first_cat = list(y2024.keys())[0]
    first_contest = list(y2024[first_cat].keys())[0]
    first_county = list(y2024[first_cat][first_contest]['results'].values())[0]
    
    print(f"\nSample 2024 data ({first_cat} - {first_contest}):")
    print(f"  County: {first_county.get('county')}")
    print(f"  Total votes: {first_county.get('total_votes')}")
    print(f"  DEM votes: {first_county.get('dem_votes')}")
    print(f"  REP votes: {first_county.get('rep_votes')}")
    print(f"  DEM candidate: {first_county.get('dem_candidate')}")
    print(f"  REP candidate: {first_county.get('rep_candidate')}")
