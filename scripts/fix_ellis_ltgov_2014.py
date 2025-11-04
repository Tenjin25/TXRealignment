import json
from pathlib import Path
import pandas as pd
import re

BASE = Path(__file__).resolve().parents[1]
JSON_FILE = BASE / 'data' / 'texas_election_results.json'
CSV_2014 = BASE / 'Election_Data' / '2014_General_Election_Returns.csv'

# Competitiveness scale copied from project metadata if present, else fallback
def load_competitive_scale(j):
    return j.get('metadata', {}).get('categorization_system', {}).get('competitiveness_scale', {})

# parse CSV and aggregate Ellis lieutenant-related rows

def aggregate_ltgov(csv_path):
    df = pd.read_csv(csv_path, on_bad_lines='skip')
    df.columns = [c.strip() for c in df.columns]
    # find columns
    col_map = {c.lower(): c for c in df.columns}
    county_col = office_col = party_col = votes_col = None
    for k, orig in col_map.items():
        if 'county' in k:
            county_col = orig
        if 'office' in k:
            office_col = orig
        if 'party' in k:
            party_col = orig
        if 'vote' in k:
            votes_col = orig
    if not (county_col and office_col and party_col and votes_col):
        raise RuntimeError('required columns not found')
    df[county_col] = df[county_col].astype(str)
    ellis = df[df[county_col].str.strip().str.upper() == 'ELLIS'].copy()
    # normalize office text and detect lieutenant governor rows robustly
    ellis['office_norm'] = ellis[office_col].astype(str).str.lower()
    # match 'lieutenant', 'lt', 'lt.' and cases like 'lt governor' or 'lt. governor'
    mask = (
        ellis['office_norm'].str.contains('lieutenant', na=False)
        | ellis['office_norm'].str.contains(r"\blt\.?\b", na=False)
        | (ellis['office_norm'].str.contains('lt', na=False) & ellis['office_norm'].str.contains('governor', na=False))
    )
    sub = ellis[mask].copy()
    if sub.empty:
        print('No lieutenant rows found in CSV for ELLIS')
        return None
    # normalize party and votes safely using .loc to avoid SettingWithCopyWarning
    sub.loc[:, party_col] = sub[party_col].astype(str).str.upper().str.strip()
    sub.loc[:, votes_col] = pd.to_numeric(sub[votes_col], errors='coerce').fillna(0).astype(int)
    pcol = sub[party_col]
    # consider parties that start with D or R as Democratic/Republican respectively
    dem = int(sub[pcol.str.startswith('D', na=False)][votes_col].sum())
    rep = int(sub[pcol.str.startswith('R', na=False)][votes_col].sum())
    other = int(sub[~(pcol.str.startswith('D', na=False) | pcol.str.startswith('R', na=False))][votes_col].sum())
    total = dem + rep + other
    return {'dem': dem, 'rep': rep, 'other': other, 'total': total}


def pick_category_from_scale(scale_dict, margin_pct):
    # scale_dict as in metadata: keys 'Republican','Tossup','Democratic' -> lists
    if margin_pct is None:
        return None
    if abs(margin_pct) <= 0.5 and 'Tossup' in scale_dict:
        ent = scale_dict['Tossup'][0]
        return {'category': ent['category'], 'party': 'Tossup', 'code': 'TOSSUP', 'color': ent.get('color'), 'description': ent.get('category')}
    party = 'Democratic' if margin_pct > 0 else 'Republican'
    abs_pct = abs(margin_pct)
    buckets = scale_dict.get(party, [])
    # parse ranges like 'D+1-5.5%'
    def parse(r):
        r = r.replace('%','').strip()
        if r.startswith('±'):
            v = float(r[1:])
            return -v, v
        m = re.match(r'[RD]\+([0-9\.]+)(?:-([0-9\.]+))?\+?', r)
        if not m:
            return None
        low = float(m.group(1))
        high = float(m.group(2)) if m.group(2) else float('inf')
        return low, high
    for b in buckets:
        rng = parse(b['range'])
        if not rng:
            continue
        low, high = rng
        if low <= abs_pct <= high:
            code = ('D_' if party=='Democratic' else 'R_') + b['category'].upper()
            return {'category': b['category'], 'party': party, 'code': code, 'color': b.get('color'), 'description': b.get('category')}
    # fallback last
    if buckets:
        b = buckets[-1]
        code = ('D_' if party=='Democratic' else 'R_') + b['category'].upper()
        return {'category': b['category'], 'party': party, 'code': code, 'color': b.get('color'), 'description': b.get('category')}
    return None


def main():
    agg = aggregate_ltgov(CSV_2014)
    if not agg:
        return
    print('Aggregated CSV for Lt Governor (ELLIS):', agg)
    j = json.loads(JSON_FILE.read_text(encoding='utf-8'))
    # locate lt_governor entry
    try:
        contest = j['results_by_year']['2014']['statewide']['lt_governor']
    except Exception as e:
        print('Could not find lt_governor contest in JSON for 2014:', e)
        return
    results = contest.setdefault('results', {})
    before = results.get('ELLIS')
    print('\nBefore JSON entry for ELLIS lt_governor 2014:')
    print(before)
    # build new entry
    new = {
        'county': 'ELLIS',
        'contest': contest.get('contest_name','Lieutenant Governor'),
        'year': '2014',
        'dem_votes': agg['dem'],
        'rep_votes': agg['rep'],
        'other_votes': agg['other'],
        'total_votes': agg['total'],
        'two_party_total': agg['dem'] + agg['rep'],
        'dem_candidate': None,
        'rep_candidate': None,
        'party_breakdown': {},
        'all_parties': {'DEM': agg['dem'], 'REP': agg['rep']}
    }
    # calc margin
    new['margin'] = agg['dem'] - agg['rep']
    new['margin_pct'] = round((new['margin']) / agg['total'] * 100, 2) if agg['total']>0 else None
    new['winner'] = 'DEM' if agg['dem']>agg['rep'] else ('REP' if agg['rep']>agg['dem'] else 'TIE')
    # competitiveness
    scale = load_competitive_scale(j)
    comp = pick_category_from_scale(scale, new['margin_pct'])
    if comp:
        new['competitiveness'] = comp
    # write new entry
    results['ELLIS'] = new
    # backup and write
    bak = JSON_FILE.with_suffix('.json.bak')
    bak.write_text(JSON_FILE.read_text(encoding='utf-8'), encoding='utf-8')
    JSON_FILE.write_text(json.dumps(j, indent=2, ensure_ascii=False), encoding='utf-8')
    print('\nAfter updated JSON entry for ELLIS lt_governor 2014:')
    print(results.get('ELLIS'))

if __name__ == '__main__':
    main()
