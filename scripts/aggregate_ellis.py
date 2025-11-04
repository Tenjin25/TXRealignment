import json
from pathlib import Path
import pandas as pd

# Paths
BASE = Path(__file__).resolve().parents[1]
DATA_DIR = BASE / 'data'
JSON_FILE = DATA_DIR / 'texas_election_results.json'
CSV_2018 = BASE / 'Election_Data' / '2018_General_Election_Returns-aligned.csv'
CSV_2014 = BASE / 'Election_Data' / '2014_General_Election_Returns.csv'

# Map office text in VTD CSV to contest key used in JSON
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
    print(f"Reading {csv_path} ...")
    df = pd.read_csv(csv_path, on_bad_lines='skip')
    # normalize columns
    df.columns = [c.strip() for c in df.columns]
    # Accept various column name cases
    col_map = {c.lower(): c for c in df.columns}
    # Resolve required columns
    county_col = None
    office_col = None
    party_col = None
    votes_col = None
    for k, orig in col_map.items():
        if k == 'county':
            county_col = orig
        if k in ('office', 'office '):
            office_col = orig
        if k in ('party', 'party '):
            party_col = orig
        if k in ('votes', 'votes '):
            votes_col = orig
    # Fallbacks
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
        raise RuntimeError('Could not find required CSV columns (County, Office, Party, Votes)')

    # Filter Ellis rows
    df[county_col] = df[county_col].astype(str)
    ellis_df = df[df[county_col].str.strip().str.upper() == 'ELLIS']

    # Clean party and votes
    ellis_df[party_col] = ellis_df[party_col].astype(str).str.strip()
    ellis_df[votes_col] = pd.to_numeric(ellis_df[votes_col], errors='coerce').fillna(0).astype(int)
    agg = {}
    for office in ellis_df[office_col].unique():
        sub = ellis_df[ellis_df[office_col] == office]
        dem = int(sub[sub[party_col].str.upper() == 'D'][votes_col].sum())
        rep = int(sub[sub[party_col].str.upper() == 'R'][votes_col].sum())
        other = int(sub[~sub[party_col].str.upper().isin(['D','R'])][votes_col].sum())
        total = dem + rep + other
        # store under the raw office text; caller will attempt to map to contest keys
        agg[str(office).strip()] = {
            'dem_votes': dem,
            'rep_votes': rep,
            'other_votes': other,
            'total_votes': total,
            'two_party_total': dem + rep
        }
    return agg


def update_json_with_agg(json_path, year, agg):
    print(f"Updating JSON for {year} with {len(agg)} contests...")
    j = json.loads(json_path.read_text(encoding='utf-8'))
    year_str = str(year)
    rby = j.get('results_by_year', {})
    if year_str not in rby:
        print(f"Year {year_str} not present in JSON. Skipping.")
        return j, []
    updated = []
    for cat, contests in rby[year_str].items():
        for key, contest in contests.items():
            if key in agg:
                if 'results' not in contest:
                    contest['results'] = {}
                if 'ELLIS' not in contest['results']:
                    # create a minimal entry
                    contest['results']['ELLIS'] = {
                        'county': 'ELLIS',
                        'contest': contest.get('contest_name', key),
                        'year': year_str,
                    }
                ent = contest['results']['ELLIS']
                a = agg[key]
                ent['dem_votes'] = a['dem_votes']
                ent['rep_votes'] = a['rep_votes']
                ent['other_votes'] = a['other_votes']
                ent['total_votes'] = a['total_votes']
                ent['two_party_total'] = a['two_party_total']
                # recalc margin and winner
                dem = a['dem_votes']
                rep = a['rep_votes']
                total = a['total_votes']
                ent['margin'] = dem - rep
                ent['margin_pct'] = round((dem - rep) / total * 100, 2) if total > 0 else None
                if dem > rep:
                    ent['winner'] = 'DEM'
                elif rep > dem:
                    ent['winner'] = 'REP'
                else:
                    ent['winner'] = 'TIE'
                # update all_parties breakdown
                ent['all_parties'] = { 'DEM': dem, 'REP': rep }
                # leave party_breakdown as-is if present; else create minimal
                if 'party_breakdown' not in ent:
                    ent['party_breakdown'] = {}
                updated.append((int(year_str), key))
    # write back
    json_path.write_text(json.dumps(j, indent=2, ensure_ascii=False), encoding='utf-8')
    return j, updated


def map_offices_to_contest_keys(j, year, office_aggs):
    """Attempt to map raw office text (from CSV) to contest keys present in JSON for the given year.
    Returns a tuple (agg_by_key, unmatched_offices)
    """
    year_str = str(year)
    rby = j.get('results_by_year', {})
    if year_str not in rby:
        return {}, list(office_aggs.keys())

    # build a list of (key, contest_name, category)
    candidates = []
    for cat, contests in rby[year_str].items():
        for key, contest in contests.items():
            cname = contest.get('contest_name') or contest.get('contest') or key
            candidates.append((key, str(cname).lower(), cat))

    def norm(s):
        import re
        s2 = s.lower()
        # expand common abbreviations to improve matching
        repl = {
            'sup ct': 'supreme court',
            'supct': 'supreme court',
            'sup. ct': 'supreme court',
            'sup court': 'supreme court',
            'cca': 'court of criminal appeals',
            'cca.': 'court of criminal appeals',
            'pres judge': 'presiding judge',
            'presiding jdg': 'presiding judge',
            'rr comm': 'railroad commissioner',
            'rrcomm': 'railroad commissioner',
            'ag comm': 'agriculture commissioner',
            'att gen': 'attorney general',
            'lt.': 'lieutenant',
            'lt': 'lieutenant',
            'state rep': 'state representative',
        }
        for a, b in repl.items():
            s2 = s2.replace(a, b)
        return re.sub(r"[^a-z0-9]+", ' ', s2).strip()

    agg_by_key = {}
    unmatched = []
    for office_text, a in office_aggs.items():
        office_norm = norm(office_text)
        # first try hard-coded mapping
        k = office_to_key(office_text)
        if k and any(k == c[0] for c in candidates):
            agg_by_key[k] = a
            continue

        # token overlap matching
        best = None
        best_score = 0
        office_tokens = set(office_norm.split())
        for key, cname, cat in candidates:
            cname_tokens = set(norm(cname).split())
            if not cname_tokens:
                continue
            inter = office_tokens & cname_tokens
            score = len(inter) / max(1, min(len(office_tokens), len(cname_tokens)))
            if score > best_score:
                best_score = score
                best = key

        # accept match if score >= 0.5 or office substring in contest name
        mapped = None
        if best and best_score >= 0.5:
            mapped = best
        else:
            # fallback: substring
            for key, cname, cat in candidates:
                if office_norm in cname or cname in office_norm:
                    mapped = key
                    break

        # final fallback: difflib close match on the normalized strings
        if not mapped:
            try:
                from difflib import get_close_matches
                office_name = office_norm
                choices = [c[1] for c in candidates]
                close = get_close_matches(office_name, choices, n=1, cutoff=0.7)
                if close:
                    # find corresponding key
                    for key, cname, cat in candidates:
                        if cname == close[0]:
                            mapped = key
                            break
            except Exception:
                pass

        if mapped:
            agg_by_key[mapped] = a
        else:
            unmatched.append(office_text)

    return agg_by_key, unmatched


def main():
    # aggregate both CSVs
    agg_2018 = aggregate_csv_for_ellis(CSV_2018)
    agg_2014 = aggregate_csv_for_ellis(CSV_2014)

    # backup JSON
    bak = JSON_FILE.with_suffix('.json.bak')
    bak.write_text(JSON_FILE.read_text(encoding='utf-8'), encoding='utf-8')
    print(f"Backed up JSON to {bak}")

    # load JSON into memory for mapping
    j = json.loads(JSON_FILE.read_text(encoding='utf-8'))

    # map office texts from CSV to contest keys present in JSON for each year
    agg18_by_key, unmatched18 = map_offices_to_contest_keys(j, 2018, agg_2018)
    agg14_by_key, unmatched14 = map_offices_to_contest_keys(j, 2014, agg_2014)

    if unmatched18:
        print(f"Unmatched 2018 offices (will be skipped): {len(unmatched18)}")
        for o in unmatched18:
            print(' -', o)
    if unmatched14:
        print(f"Unmatched 2014 offices (will be skipped): {len(unmatched14)}")
        for o in unmatched14:
            print(' -', o)

    j, upd18 = update_json_with_agg(JSON_FILE, 2018, agg18_by_key)
    j, upd14 = update_json_with_agg(JSON_FILE, 2014, agg14_by_key)

    print('\nUpdated contests:')
    for y,k in sorted(set(upd18+upd14)):
        print(f" - Year {y}: {k}")

    print('\nDone. Open data/texas_election_results.json to review the updated ELLIS entries.')

if __name__ == '__main__':
    main()
