import json

with open('data/texas_election_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

contested = 0
total = 0

for year, year_data in data['results_by_year'].items():
    for category, contests in year_data.items():
        for contest_key, contest in contests.items():
            total += 1
            dem = contest.get('dem_candidate')
            rep = contest.get('rep_candidate')
            if dem and rep and dem.strip() and rep.strip():
                contested += 1

print(f'Total contests: {total}')
print(f'Contested (both DEM and REP candidates): {contested}')
print(f'Uncontested: {total - contested}')
print(f'Percentage contested: {contested/total*100:.1f}%')
