import json
from pathlib import Path
p = Path(__file__).resolve().parents[1] / 'data' / 'texas_election_results.json'
j = json.loads(p.read_text(encoding='utf-8'))
ry = j.get('results_by_year', {})
for key, contests in ry.get('2018', {}).items():
    for k,c in contests.items():
        name = c.get('contest_name') or c.get('contest') or ''
        ln = name.lower()
        if 'sup' in k or 'sup' in ln or 'cca' in k or 'cca' in ln or 'rail' in k or 'rail' in ln or 'represent' in ln:
            print(k, '->', name)
