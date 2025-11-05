import json

with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

judicial = data['results_by_year']['2022']['judicial']

for contest_name, contest_data in judicial.items():
    print(f"\n{contest_name}:")
    print(f"  Contest Name: {contest_data.get('contest_name', 'N/A')}")
    print(f"  DEM: {contest_data.get('dem_candidate', 'N/A')}")
    print(f"  REP: {contest_data.get('rep_candidate', 'N/A')}")
