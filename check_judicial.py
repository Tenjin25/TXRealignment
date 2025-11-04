import json

with open('data/texas_election_results.json') as f:
    data = json.load(f)
    
print("Checking for judicial contests...\n")
has_judicial = False

for year in sorted(data['results_by_year'].keys()):
    categories = list(data['results_by_year'][year].keys())
    if 'judicial' in categories:
        has_judicial = True
        judicial_contests = data['results_by_year'][year]['judicial']
        print(f'{year} judicial ({len(judicial_contests)} contests):')
        for key, val in judicial_contests.items():
            contest_name = val.get('contest_name', key)
            county_count = len(val.get('results', {}))
            print(f'  {key}: {contest_name} ({county_count} counties)')

if not has_judicial:
    print('No judicial category found in any year')
