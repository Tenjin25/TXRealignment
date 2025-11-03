import json

data = json.load(open('data/texas_election_results.json'))['results_by_year']['2024']

print('2024 categories and contests:')
for cat in data.keys():
    print(f'\n{cat.upper()}:')
    for contest in data[cat].keys():
        contest_name = data[cat][contest].get('contest_name', contest)
        print(f'  - {contest}: {contest_name}')
