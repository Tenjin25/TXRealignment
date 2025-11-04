import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'data' / 'texas_election_results.json'
if not path.exists():
    print(f"File not found: {path}")
    raise SystemExit(1)

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
year = '2018'
found_all = []
for contest in data.get('results', []):
    if contest.get('year') == year:
        contest_name = contest.get('contest')
        counties = contest.get('counties', {})
        has_ellis = 'ELLIS' in counties
        sample = None
        if has_ellis:
            sample = counties.get('ELLIS')
        found_all.append({
            'contest': contest_name,
            'has_ellis': has_ellis,
            'ellis_sample': sample
        })

print(json.dumps(found_all, indent=2))
