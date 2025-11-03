import json

rr = json.load(open('data/texas_election_results.json'))['results_by_year']['2024']['statewide']['railroad_commissioner']

print('2024 Railroad Commissioner:')
print(f'  Contest: {rr["contest_name"]}')
print(f'  Dem: {rr["dem_candidate"]}')
print(f'  Rep: {rr["rep_candidate"]}')

county = list(rr['results'].values())[0]
print(f'\nSample county data:')
print(f'  Dem: {county["dem_candidate"]}')
print(f'  Rep: {county["rep_candidate"]}')
