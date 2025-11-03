import json

with open('data/texas_election_results.json') as f:
    data = json.load(f)

print("2020 Categories and Contests:")
for cat, contests in data['results_by_year']['2020'].items():
    print(f"  {cat}:")
    for contest_key, contest_data in contests.items():
        print(f"    - {contest_data.get('contest_name', contest_key)}")

print("\n2022 Categories and Contests:")
for cat, contests in data['results_by_year']['2022'].items():
    print(f"  {cat}:")
    for contest_key, contest_data in contests.items():
        print(f"    - {contest_data.get('contest_name', contest_key)}")

# Sample county data for 2020 President
print("\n2020 President:")
counties_2020 = list(data['results_by_year']['2020']['presidential']['president']['results'].keys())
print(f"  Total counties: {len(counties_2020)}")
print(f"  First 5 counties: {counties_2020[:5]}")

# Check a specific county
if counties_2020:
    sample_county = counties_2020[0]
    sample_data = data['results_by_year']['2020']['presidential']['president']['results'][sample_county]
    print(f"\n  Sample: {sample_county}")
    print(f"    Total votes: {sample_data['total_votes']}")
    print(f"    DEM: {sample_data['dem_votes']}")
    print(f"    REP: {sample_data['rep_votes']}")
    print(f"    Other: {sample_data['other_votes']}")
    print(f"    Competitiveness: {sample_data['competitiveness']['description']}")
    print(f"    Margin: {sample_data['margin_pct']}% {sample_data['winner']}")

# Sample county data for 2022 Governor
print("\n2022 Governor:")
counties_2022 = list(data['results_by_year']['2022']['statewide']['governor']['results'].keys())
print(f"  Total counties: {len(counties_2022)}")
print(f"  First 5 counties: {counties_2022[:5]}")
