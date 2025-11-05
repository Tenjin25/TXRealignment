import json

# Load the JSON file
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("Years in results_by_year:")
for year in sorted(data['results_by_year'].keys()):
    print(f"\n{year}:")
    for category in data['results_by_year'][year].keys():
        print(f"  {category}:")
        for contest in data['results_by_year'][year][category].keys():
            print(f"    - {contest}")
