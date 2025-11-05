import json

# Load the JSON file
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("2018 Judicial Contests:")
print("=" * 60)
if '2018' in data['results_by_year']:
    if 'judicial' in data['results_by_year']['2018']:
        for contest_key, contest_data in data['results_by_year']['2018']['judicial'].items():
            contest_name = contest_data.get('contest_name', contest_key)
            print(f"\nKey: {contest_key}")
            print(f"Name: {contest_name}")
            if 'ELLIS' in contest_data.get('results', {}):
                ellis = contest_data['results']['ELLIS']
                print(f"  Ellis: DEM {ellis.get('dem_votes'):,}, REP {ellis.get('rep_votes'):,}")
