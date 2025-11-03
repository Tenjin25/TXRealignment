import json

data = json.load(open('data/texas_election_results.json'))['results_by_year']['2022']['statewide']

print('2022 Statewide contests:')
for key in data.keys():
    contest_name = data[key].get('contest_name', key)
    print(f'  - {key}: {contest_name}')
