import json
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
JSON_FILE = BASE / 'data' / 'texas_election_results.json'
CSV_2018 = BASE / 'Election_Data' / '2018_General_Election_Returns-aligned.csv'
CSV_2014 = BASE / 'Election_Data' / '2014_General_Election_Returns.csv'


def office_to_key(office):
    s = office.lower()
    if 'sen' in s and 'u.s.' in s:
        return 'us_senate'
    if 'governor' in s and 'lieutenant' not in s:
        return 'governor'
    if 'lieutenant governor' in s or 'lt.' in s:
        return 'lt_governor'
    if 'attorney general' in s or 'att gen' in s:
        return 'attorney_general'
    if 'comptroller' in s:
        return 'comptroller'
    if 'railroad' in s:
        return 'railroad_commissioner'
    if 'land' in s and 'commission' in s:
        return 'land_commissioner'
    if 'agriculture' in s or 'ag comm' in s:
        return 'agriculture_commissioner'
    return None


def aggregate_csv_for_ellis(csv_path):
    df = pd.read_csv(csv_path, on_bad_lines='skip')
    df.columns = [c.strip() for c in df.columns]
    col_map = {c.lower(): c for c in df.columns}
    county_col = office_col = party_col = votes_col = None
    for k, orig in col_map.items():
        if k == 'county':
            county_col = orig
        if k in ('office', 'office '):
            office_col = orig
        if k in ('party', 'party '):
            party_col = orig
        if k in ('votes', 'votes '):
            votes_col = orig
    if county_col is None:
        for c in df.columns:
            if 'county' in c.lower():
                county_col = c
                break
    if office_col is None:
        for c in df.columns:
            if 'office' in c.lower():
                office_col = c
                break
    if party_col is None:
        for c in df.columns:
            if 'party' in c.lower():
                party_col = c
                break
    if votes_col is None:
        for c in df.columns:
            if 'vote' in c.lower():
                votes_col = c
                break
    if not (county_col and office_col and party_col and votes_col):
        raise RuntimeError('Could not find required CSV columns')

    df[county_col] = df[county_col].astype(str)
    ellis_df = df[df[county_col].str.strip().str.upper() == 'ELLIS']
    ellis_df[party_col] = ellis_df[party_col].astype(str).str.strip()
    ellis_df[votes_col] = pd.to_numeric(ellis_df[votes_col], errors='coerce').fillna(0).astype(int)

    agg = {}
    for office in ellis_df[office_col].unique():
        key = office_to_key(str(office))
        if not key:
            continue
        sub = ellis_df[ellis_df[office_col] == office]
        dem = int(sub[sub[party_col].str.upper() == 'D'][votes_col].sum())
        rep = int(sub[sub[party_col].str.upper() == 'R'][votes_col].sum())
        other = int(sub[~sub[party_col].str.upper().isin(['D','R'])][votes_col].sum())
        total = dem + rep + other
        agg[key] = {'dem_votes': dem, 'rep_votes': rep, 'other_votes': other, 'total_votes': total, 'two_party_total': dem+rep}
    return agg


def find_json_entry(j, year, key):
    rby = j.get('results_by_year', {})
    ys = str(year)
    if ys not in rby:
        return None, None, None
    for cat, contests in rby[ys].items():
        if key in contests:
            contest = contests[key]
            results = contest.get('results', {})
            if 'ELLIS' in results:
                return results['ELLIS'], cat, contest
    return None, None, None


def compare_and_report(year, agg, j):
    mismatches = []
    print(f"\nComparing year {year}: {len(agg)} aggregated contests")
    keys = sorted(agg.keys())
    for key in keys:
        a = agg[key]
        entry, cat, contest = find_json_entry(j, year, key)
        if entry is None:
            print(f" - {key}: NOT FOUND in JSON")
            mismatches.append((year,key,'missing'))
            continue
        j_dem = int(entry.get('dem_votes', 0) or 0)
        j_rep = int(entry.get('rep_votes', 0) or 0)
        j_other = int(entry.get('other_votes', 0) or 0)
        j_total = int(entry.get('total_votes', 0) or 0)
        print(f" - {key} (category: {cat}):")
        print(f"    agg -> DEM: {a['dem_votes']}  REP: {a['rep_votes']}  OTHER: {a['other_votes']}  TOTAL: {a['total_votes']}")
        print(f"    json-> DEM: {j_dem}  REP: {j_rep}  OTHER: {j_other}  TOTAL: {j_total}")
        if (a['dem_votes'], a['rep_votes'], a['other_votes'], a['total_votes']) != (j_dem, j_rep, j_other, j_total):
            print("    => MISMATCH")
            mismatches.append((year,key,'mismatch'))
        else:
            print("    => OK")
    return mismatches


def main():
    print('Aggregating CSVs...')
    agg18 = aggregate_csv_for_ellis(CSV_2018)
    agg14 = aggregate_csv_for_ellis(CSV_2014)
    print('Loading JSON...')
    j = json.loads(JSON_FILE.read_text(encoding='utf-8'))

    mismatches = []
    mismatches += compare_and_report(2018, agg18, j)
    mismatches += compare_and_report(2014, agg14, j)

    print('\nSummary:')
    if not mismatches:
        print(' All aggregated entries match the JSON ELLIS entries.')
    else:
        print(f" Found {len(mismatches)} issues:")
        for m in mismatches:
            print(' -', m)

if __name__ == '__main__':
    main()
