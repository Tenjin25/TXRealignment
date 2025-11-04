import json
from pathlib import Path
import pandas as pd
import re

BASE = Path(__file__).resolve().parents[1]
JSON_FILE = BASE / 'data' / 'texas_election_results.json'
CSV_2018 = BASE / 'Election_Data' / '2018_General_Election_Returns-aligned.csv'
CSV_2014 = BASE / 'Election_Data' / '2014_General_Election_Returns.csv'

# Competitiveness scale provided by user (copied into Python dict)
COMPETITIVENESS_SCALE = {
    'Republican': [
        {'category': 'Annihilation', 'range': 'R+40%+', 'color': '#67000d'},
        {'category': 'Dominant', 'range': 'R+30-40%', 'color': '#a50f15'},
        {'category': 'Stronghold', 'range': 'R+20-30%', 'color': '#cb181d'},
        {'category': 'Safe', 'range': 'R+10-20%', 'color': '#ef3b2c'},
        {'category': 'Likely', 'range': 'R+5.5-10%', 'color': '#fb6a4a'},
        {'category': 'Lean', 'range': 'R+1-5.5%', 'color': '#fcae91'},
        {'category': 'Tilt', 'range': 'R+0.5-1%', 'color': '#fee8c8'},
    ],
    'Tossup': [
        {'category': 'Tossup', 'range': '±0.5%', 'color': '#f7f7f7'}
    ],
    'Democratic': [
        {'category': 'Tilt', 'range': 'D+0.5-1%', 'color': '#e1f5fe'},
        {'category': 'Lean', 'range': 'D+1-5.5%', 'color': '#c6dbef'},
        {'category': 'Likely', 'range': 'D+5.5-10%', 'color': '#9ecae1'},
        {'category': 'Safe', 'range': 'D+10-20%', 'color': '#6baed6'},
        {'category': 'Stronghold', 'range': 'D+20-30%', 'color': '#3182bd'},
        {'category': 'Dominant', 'range': 'D+30-40%', 'color': '#08519c'},
        {'category': 'Annihilation', 'range': 'D+40%+', 'color': '#08306b'},
    ]
}

# helpers to parse range strings like 'R+30-40%' or 'D+40%+' or '±0.5%'
range_re = re.compile(r'([RD])\+([0-9\.]+)(?:-([0-9\.]+))?%?\+?')
plus_inf_re = re.compile(r'([RD])\+([0-9\.]+)%\+')
plus_minus_re = re.compile(r'±([0-9\.]+)%')


def parse_range(rstr):
    rstr = rstr.strip()
    if rstr.startswith('±'):
        m = plus_minus_re.match(rstr)
        if m:
            val = float(m.group(1))
            return {'low': -val, 'high': val}
    m = range_re.match(rstr)
    if not m:
        return None
    side = m.group(1)
    low = float(m.group(2))
    high = float(m.group(3)) if m.group(3) else None
    if high is None:
        return {'low': low, 'high': float('inf')}
    return {'low': low, 'high': high}


def pick_category(margin_pct):
    # margin_pct: signed percent (dem - rep)/total*100
    if margin_pct is None:
        return None
    if abs(margin_pct) <= 0.5:
        entry = COMPETITIVENESS_SCALE['Tossup'][0]
        return {
            'category': entry['category'],
            'party': 'Tossup',
            'code': 'TOSSUP',
            'color': entry.get('color'),
            'description': 'Tossup'
        }
    if margin_pct > 0:
        party = 'Democratic'
        abs_pct = margin_pct
    else:
        party = 'Republican'
        abs_pct = abs(margin_pct)
    # iterate party buckets and find matching range
    buckets = COMPETITIVENESS_SCALE[party]
    for b in buckets:
        parsed = parse_range(b['range'])
        if not parsed:
            continue
        low = parsed['low']
        high = parsed['high']
        # For Democratic ranges parsed low/high are positive numbers; compare abs_pct
        if low <= abs_pct <= high:
            code = ('D_' if party == 'Democratic' else 'R_') + b['category'].upper()
            return {
                'category': b['category'],
                'party': party if party in ('Democratic','Republican') else party,
                'code': code,
                'color': b.get('color'),
                'description': f"{b['category']} {party if party in ('Democratic','Republican') else ''}".strip()
            }
    # fallback: largest bucket
    last = buckets[-1]
    code = ('D_' if party == 'Democratic' else 'R_') + last['category'].upper()
    return {
        'category': last['category'],
        'party': party,
        'code': code,
        'color': last.get('color'),
        'description': f"{last['category']} {party}"
    }


def office_to_key(office):
    s = office.lower()
    # quick heuristics - keep and expand previous mapping
    if 'u.s.' in s or 'us' in s and 'sen' in s:
        return 'us_senate'
    if 'governor' in s and 'lieutenant' not in s:
        return 'governor'
    if 'lieutenant governor' in s or 'lt.' in s or 'lt ' in s:
        return 'lt_governor'
    if 'attorney general' in s or 'att gen' in s or 'att gen.' in s:
        return 'attorney_general'
    if 'comptroller' in s:
        return 'comptroller'
    if 'railroad' in s:
        return 'railroad_commissioner'
    if 'land' in s and 'commission' in s:
        return 'land_commissioner'
    if 'agriculture' in s or 'ag comm' in s:
        return 'agriculture_commissioner'
    if 'president' in s:
        return 'president'
    if 'representative' in s or 'congress' in s or 'house' in s:
        return 'us_house'
    # otherwise None
    return None


def token_overlap_score(a, b):
    a_tokens = set(re.findall(r"[a-z0-9]+", a.lower()))
    b_tokens = set(re.findall(r"[a-z0-9]+", b.lower()))
    if not a_tokens or not b_tokens:
        return 0.0
    inter = a_tokens & b_tokens
    score = len(inter) / max(1, len(a_tokens | b_tokens))
    return score


def aggregate_csv_all(csv_path):
    print(f"Reading {csv_path}...")
    df = pd.read_csv(csv_path, on_bad_lines='skip')
    df.columns = [c.strip() for c in df.columns]
    col_map = {c.lower(): c for c in df.columns}
    county_col = office_col = party_col = votes_col = None
    for k, orig in col_map.items():
        if k == 'county':
            county_col = orig
        if 'office' in k:
            office_col = orig
        if 'party' in k:
            party_col = orig
        if 'vote' in k:
            votes_col = orig
    if not (county_col and office_col and party_col and votes_col):
        raise RuntimeError('Could not find required CSV columns')
    df[county_col] = df[county_col].astype(str)
    ellis_df = df[df[county_col].str.strip().str.upper() == 'ELLIS'].copy()
    ellis_df[party_col] = ellis_df[party_col].astype(str).str.strip()
    ellis_df[votes_col] = pd.to_numeric(ellis_df[votes_col], errors='coerce').fillna(0).astype(int)
    # group by office and party
    grouped = ellis_df.groupby([office_col, party_col])[votes_col].sum().reset_index()
    # build dict office -> {DEM:, REP:, OTHER:}
    offices = {}
    for _, row in grouped.iterrows():
        office = str(row[office_col]).strip()
        party = row[party_col].upper()
        votes = int(row[votes_col])
        offices.setdefault(office, {'DEM': 0, 'REP': 0, 'OTHER': 0})
        if party == 'D':
            offices[office]['DEM'] += votes
        elif party == 'R':
            offices[office]['REP'] += votes
        else:
            offices[office]['OTHER'] += votes
    # also compute total
    for k, v in offices.items():
        v['TOTAL'] = v['DEM'] + v['REP'] + v['OTHER']
        v['TWO'] = v['DEM'] + v['REP']
    return offices


def map_offices_to_contests(j, year, office_names):
    # j is JSON dict
    year_str = str(year)
    matches = {}
    rby = j.get('results_by_year', {})
    if year_str not in rby:
        return matches, []
    contest_map = {}
    # flatten contest keys to contest_name strings
    for cat, contests in rby[year_str].items():
        for key, c in contests.items():
            # try contest_name or contest
            name = c.get('contest_name') or c.get('contest') or key
            contest_map[key] = name
    unmatched = []
    for office in office_names:
        of_low = office.lower()
        # RR: Railroad Commissioner variants
        if re.search(r"\brr\b|\brr\.?\s*comm\b|railroad|rr\s*comm", of_low):
            for k, name in contest_map.items():
                if 'railroad' in k or 'railroad' in name.lower():
                    matches[office] = k
                    break
            if office in matches:
                continue

        # Supreme Court with explicit place number -> create place-specific key
        m_sup = re.search(r"sup(reme)?\s*ct\b(?:\s*(?:place)?\s*(\d+))?", of_low)
        if m_sup:
            place = m_sup.group(2)
            if place:
                target = f"supreme_court_place_{place}"
                matches[office] = target
                continue
            # fallback to best matching supreme court contest
            best_k = None
            best_s = 0.0
            for k, name in contest_map.items():
                if k.startswith('supreme_court_place_') or 'supreme' in name.lower():
                    s = token_overlap_score(office, name)
                    if s > best_s:
                        best_s = s
                        best_k = k
            if best_k and best_s >= 0.08:
                matches[office] = best_k
                continue

        # CCA with place number -> create place-specific key
        if re.search(r"\bcca\b", of_low):
            mcca = re.search(r"cca\s*(?:pres|presiding)?\s*(\d{1,2})?", of_low)
            if mcca and mcca.group(1):
                place = mcca.group(1)
                target = f"cca_judge_place_{place}"
                matches[office] = target
                continue
            # presiding judge vs judge
            if re.search(r"pres|presiding", of_low):
                for k, name in contest_map.items():
                    if 'presiding' in name.lower() or 'presiding' in k:
                        matches[office] = k
                        break
            if office in matches:
                continue
            # default to cca_judge-like keys
            for k, name in contest_map.items():
                if 'criminal appeals' in name.lower() or 'court of criminal appeals' in name.lower() or k.startswith('cca_'):
                    matches[office] = k
                    break
            if office in matches:
                continue

        # state rep -> try to find state representative/house contests (match district number if present)
        if re.search(r"state rep|state representative|state house|house district|state house", of_low):
            # extract number if present
            mnum = re.search(r"(\d{1,3})", of_low)
            candidate_keys = []
            for k, name in contest_map.items():
                ln = name.lower()
                if 'representative' in ln or 'house' in ln or 'state representative' in ln:
                    candidate_keys.append((k, name))
            if mnum and candidate_keys:
                num = mnum.group(1)
                # try to match the number in the contest name
                for k, name in candidate_keys:
                    if num in name:
                        matches[office] = k
                        break
                if office in matches:
                    continue
            # fallback: pick best overlap among candidate_keys
            best_k = None
            best_s = 0.0
            for k, name in candidate_keys:
                s = token_overlap_score(office, name)
                if s > best_s:
                    best_s = s
                    best_k = k
            if best_k and best_s >= 0.2:
                matches[office] = best_k
                continue

        # generic key mapping
        key = office_to_key(office)
        if key and key in contest_map:
            matches[office] = key
            continue

        # fuzzy token overlap to pick best matching contest
        best = None
        best_score = 0.0
        for k, name in contest_map.items():
            s = token_overlap_score(office, name)
            if s > best_score:
                best_score = s
                best = k
        # threshold
        if best_score >= 0.25:
            matches[office] = best
        else:
            unmatched.append((office, best_score))
    return matches, unmatched


def update_json_with_office_aggregates(json_path, year, office_aggs):
    print(f"Applying {len(office_aggs)} office aggregates into JSON for {year}...")
    j = json.loads(json_path.read_text(encoding='utf-8'))
    year_str = str(year)
    rby = j.setdefault('results_by_year', {})
    if year_str not in rby:
        print(f"Year {year_str} not in JSON; skipping")
        return j, []
    # map offices
    matches, unmatched = map_offices_to_contests(j, year, list(office_aggs.keys()))
    applied = []
    for office, key in matches.items():
        a = office_aggs[office]
        # find contest dict; if missing, create place-specific contest entries under an appropriate category
        contest = None
        found_cat = None
        for cat, contests in rby[year_str].items():
            if key in contests:
                contest = contests[key]
                found_cat = cat
                break
        if contest is None:
            # determine where to put new contest: prefer category that already contains similar contests
            preferred_cat = None
            # look for categories that contain supreme court or cca related contests
            for cat, contests in rby[year_str].items():
                for k in contests.keys():
                    if key.startswith('supreme_court') and ('supreme_court' in k or 'supreme' in str(contests[k].get('contest_name','')).lower()):
                        preferred_cat = cat
                        break
                    if key.startswith('cca') and ('criminal appeals' in str(contests[k].get('contest_name','')).lower() or k.startswith('cca_')):
                        preferred_cat = cat
                        break
                if preferred_cat:
                    break
            if not preferred_cat:
                preferred_cat = 'statewide' if 'statewide' in rby[year_str] else list(rby[year_str].keys())[0]
            # create a minimal contest entry
            contests = rby[year_str].setdefault(preferred_cat, {})
            # craft a contest_name if possible
            if key.startswith('supreme_court_place_'):
                pn = key.split('_')[-1]
                contest_name = f"Justice, Supreme Court, Place {pn}"
            elif key.startswith('cca_judge_place_'):
                pn = key.split('_')[-1]
                contest_name = f"Judge, Court of Criminal Appeals, Place {pn}"
            else:
                contest_name = key
            contests[key] = {'contest_name': contest_name, 'results': {}}
            contest = contests[key]
            found_cat = preferred_cat
        if 'results' not in contest:
            contest['results'] = {}
        ent = contest['results'].setdefault('ELLIS', {
            'county': 'ELLIS', 'contest': contest.get('contest_name', key), 'year': year_str
        })
        ent['dem_votes'] = a['DEM']
        ent['rep_votes'] = a['REP']
        ent['other_votes'] = a['OTHER']
        ent['total_votes'] = a['TOTAL']
        ent['two_party_total'] = a['TWO']
        ent['margin'] = a['DEM'] - a['REP']
        ent['margin_pct'] = round((a['DEM'] - a['REP']) / a['TOTAL'] * 100, 2) if a['TOTAL'] > 0 else None
        ent['winner'] = 'DEM' if a['DEM'] > a['REP'] else ('REP' if a['REP'] > a['DEM'] else 'TIE')
        ent['all_parties'] = {'DEM': a['DEM'], 'REP': a['REP']}
        if 'party_breakdown' not in ent:
            ent['party_breakdown'] = {}
        applied.append((office, key))
    # write back
    json_path.write_text(json.dumps(j, indent=2, ensure_ascii=False), encoding='utf-8')
    return j, (matches, unmatched, applied)


def recompute_competitiveness(j, years):
    # replace competitiveness_scale in metadata
    md = j.setdefault('metadata', {})
    cat = md.setdefault('categorization_system', {})
    cat['competitiveness_scale'] = COMPETITIVENESS_SCALE
    changed = []
    for year in years:
        ys = str(year)
        rby = j.get('results_by_year', {})
        if ys not in rby:
            continue
        for cat_name, contests in rby[ys].items():
            for key, contest in contests.items():
                results = contest.get('results', {})
                for county, ent in results.items():
                    dem = int(ent.get('dem_votes', 0) or 0)
                    rep = int(ent.get('rep_votes', 0) or 0)
                    total = int(ent.get('total_votes', 0) or 0)
                    if total <= 0:
                        margin_pct = None
                    else:
                        margin_pct = round((dem - rep) / total * 100, 2)
                    ent['margin'] = dem - rep
                    ent['margin_pct'] = margin_pct
                    if dem > rep:
                        ent['winner'] = 'DEM'
                    elif rep > dem:
                        ent['winner'] = 'REP'
                    else:
                        ent['winner'] = 'TIE'
                    comp = pick_category(margin_pct)
                    if comp:
                        ent['competitiveness'] = comp
                        changed.append((year, key, county, comp['category'], comp['party']))
    return j, changed


def main():
    # aggregate all offices from both CSVs
    office18 = aggregate_csv_all(CSV_2018)
    office14 = aggregate_csv_all(CSV_2014)
    # backup JSON
    bak = JSON_FILE.with_suffix('.json.bak')
    bak.write_text(JSON_FILE.read_text(encoding='utf-8'), encoding='utf-8')
    print(f"Backed up JSON to {bak}")
    # apply aggregates
    j, info18 = update_json_with_office_aggregates(JSON_FILE, 2018, office18)
    j, info14 = update_json_with_office_aggregates(JSON_FILE, 2014, office14)
    matches18, unmatched18, applied18 = info18
    matches14, unmatched14, applied14 = info14
    print('\nMapping summary:')
    print(f' 2018 matched {len(matches18)} offices, unmatched {len(unmatched18)}')
    print(f' 2014 matched {len(matches14)} offices, unmatched {len(unmatched14)}')
    if unmatched18:
        print('\n Unmatched 2018 offices (office,score):')
        for o,s in unmatched18[:40]:
            print('  -', o, round(s,3))
    if unmatched14:
        print('\n Unmatched 2014 offices (office,score):')
        for o,s in unmatched14[:40]:
            print('  -', o, round(s,3))
    # recompute competitiveness using the supplied scale for both years
    j = json.loads(JSON_FILE.read_text(encoding='utf-8'))
    j, changed = recompute_competitiveness(j, [2014, 2018])
    JSON_FILE.write_text(json.dumps(j, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\nRecomputed competitiveness for {len(changed)} county-contest entries across 2014 and 2018")
    # show some samples
    for c in changed[:10]:
        print(' -', c)
    print('\nDone. JSON updated.')

if __name__ == '__main__':
    main()
