import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'data' / 'texas_election_results.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

year = '2018'
ry = data.get('results_by_year', {})
if year not in ry:
    print(f"Year {year} not found in results_by_year")
    raise SystemExit(1)

y = ry[year]
print('Top-level keys under results_by_year["2018"]:')
for k in y.keys():
    print('-', k)

print('\nDrilling into each category and contest:')
for category, contests in y.items():
    print('\nCategory:', category)
    for contest_key, contest_val in contests.items():
        print('  Contest key:', contest_key)
        # contest_val should be a dict containing 'results' mapping counties
        if isinstance(contest_val, dict) and 'results' in contest_val:
            results = contest_val['results']
            has_ellis = 'ELLIS' in results
            print('    has_results:', True, 'ELLIS present:', has_ellis)
            if has_ellis:
                print('    ELLIS sample:', results['ELLIS'])
        else:
            print('    (no results field)')

print('\nDone')
