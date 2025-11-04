import json
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
JSON_FILE = BASE / 'data' / 'texas_election_results.json'
CSV_2014 = BASE / 'Election_Data' / '2014_General_Election_Returns.csv'

j = json.loads(JSON_FILE.read_text(encoding='utf-8'))
ry = j.get('results_by_year', {})

# locate lt_governor entry
lt_entry = None
for cat, contests in ry.get('2014', {}).items():
    if 'lt_governor' in contests:
        lt_entry = contests['lt_governor'].get('results', {}).get('ELLIS')
        break

print('JSON ELLIS lt_governor 2014 entry:')
print(lt_entry)

# aggregate CSV
print('\nAggregating CSV for ELLIS Lt Governor rows...')
df = pd.read_csv(CSV_2014, on_bad_lines='skip')
df.columns = [c.strip() for c in df.columns]
# find county/office/party/votes columns
col_map = {c.lower(): c for c in df.columns}
county_col = office_col = party_col = votes_col = None
for k, orig in col_map.items():
    if 'county' == k:
        county_col = orig
    if 'office' in k:
        office_col = orig
    if 'party' in k:
        party_col = orig
    if 'vote' in k:
        votes_col = orig

if not (county_col and office_col and party_col and votes_col):
    print('Could not find required columns in CSV')
    raise SystemExit(1)

ellis = df[df[county_col].astype(str).str.upper().str.strip() == 'ELLIS']
# show unique office names that mention lieutenant or lt
candidates = [o for o in ellis[office_col].unique() if 'lieut' in str(o).lower() or 'lt' in str(o).lower()]
print('Candidate office names matching lieutenant/lt:')
for o in candidates:
    print('-', o)

# aggregate votes for those office strings
agg = {}
for o in candidates:
    sub = ellis[ellis[office_col] == o]
    dem = int(sub[sub[party_col].str.upper() == 'D'][votes_col].sum())
    rep = int(sub[sub[party_col].str.upper() == 'R'][votes_col].sum())
    other = int(sub[~sub[party_col].str.upper().isin(['D','R'])][votes_col].sum())
    total = dem + rep + other
    agg[o] = {'dem': dem, 'rep': rep, 'other': other, 'total': total}

print('\nAggregated totals from CSV for lieutenant-related office names:')
print(json.dumps(agg, indent=2))
