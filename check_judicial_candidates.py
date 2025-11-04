import json

with open('data/texas_election_results.json') as f:
    data = json.load(f)

print("Checking judicial candidate names...\n")

for year in sorted(data['results_by_year'].keys()):
    if 'judicial' in data['results_by_year'][year]:
        print(f"\n{year}:")
        judicial_contests = data['results_by_year'][year]['judicial']
        
        for contest_key, contest in judicial_contests.items():
            contest_name = contest.get('contest_name', contest_key)
            dem_cand = contest.get('dem_candidate')
            rep_cand = contest.get('rep_candidate')
            
            print(f"  {contest_name}")
            print(f"    DEM: {dem_cand}")
            print(f"    REP: {rep_cand}")
