import json

with open('data/texas_election_results.json') as f:
    data = json.load(f)

# Check 2020 President
pres_2020 = data['results_by_year']['2020']['presidential']['president']
sample = list(pres_2020['results'].values())[0]

print('2020 President sample county:')
print(f'  DEM candidate: {sample.get("dem_candidate")}')
print(f'  REP candidate: {sample.get("rep_candidate")}')

print('\n2020 Contest level:')
print(f'  DEM candidate: {pres_2020.get("dem_candidate")}')
print(f'  REP candidate: {pres_2020.get("rep_candidate")}')

# Check 2022 Governor
gov_2022 = data['results_by_year']['2022']['statewide']['governor']
sample2 = list(gov_2022['results'].values())[0]

print('\n2022 Governor sample county:')
print(f'  DEM candidate: {sample2.get("dem_candidate")}')
print(f'  REP candidate: {sample2.get("rep_candidate")}')

print('\n2022 Contest level:')
print(f'  DEM candidate: {gov_2022.get("dem_candidate")}')
print(f'  REP candidate: {gov_2022.get("rep_candidate")}')
