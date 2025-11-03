import pandas as pd
import json
from datetime import date

# --- CONFIG ---
ELECTION_CSV = r'./Election_Data/20121106__tx__general__county.csv'  # Change as needed
OUTPUT_JSON = r'./TX_Data/tx_election_2012_county.json'
TARGET_OFFICES = [
    'President/VicePresident',
    'U.S. Senate',
    'US Senate',
    'United States Senate',
    'President and Vice President',
]

# --- COMPETITIVENESS SCALE ---
COMPETITIVENESS_SCALE = [
    (40, 'Annihilation', 'Republican', '#67000d'),
    (30, 'Dominant', 'Republican', '#a50f15'),
    (20, 'Stronghold', 'Republican', '#cb181d'),
    (10, 'Safe', 'Republican', '#ef3b2c'),
    (5.5, 'Likely', 'Republican', '#fb6a4a'),
    (1, 'Lean', 'Republican', '#fcae91'),
    (0.5, 'Tilt', 'Republican', '#fee8c8'),
    (0.5, 'Tossup', 'Tossup', '#f7f7f7'),
    (1, 'Tilt', 'Democratic', '#e1f5fe'),
    (5.5, 'Lean', 'Democratic', '#c6dbef'),
    (10, 'Likely', 'Democratic', '#9ecae1'),
    (20, 'Safe', 'Democratic', '#6baed6'),
    (30, 'Stronghold', 'Democratic', '#3182bd'),
    (40, 'Dominant', 'Democratic', '#08519c'),
    (100, 'Annihilation', 'Democratic', '#08306b'),
]

def categorize_competitiveness(margin_pct):
    # margin_pct: positive = Republican, negative = Democratic
    abs_margin = abs(margin_pct)
    if margin_pct > 0:
        # Republican
        for threshold, cat, party, color in COMPETITIVENESS_SCALE:
            if abs_margin >= threshold and party == 'Republican':
                return {'category': cat, 'party': party, 'color': color}
        if abs_margin < 0.5:
            return {'category': 'Tossup', 'party': 'Tossup', 'color': '#f7f7f7'}
    elif margin_pct < 0:
        # Democratic
        for threshold, cat, party, color in COMPETITIVENESS_SCALE:
            if abs_margin >= threshold and party == 'Democratic':
                return {'category': cat, 'party': party, 'color': color}
        if abs_margin < 0.5:
            return {'category': 'Tossup', 'party': 'Tossup', 'color': '#f7f7f7'}
    else:
        return {'category': 'Tossup', 'party': 'Tossup', 'color': '#f7f7f7'}

# --- LOAD DATA ---
df = pd.read_csv(ELECTION_CSV, dtype=str)

# Normalize office column
if 'office' in df.columns:
    df['office_norm'] = df['office'].str.strip().str.lower()
else:
    raise Exception('No office column found!')

# Filter for target offices
office_map = {
    'president/vicepresident': 'presidential',
    'president and vice president': 'presidential',
    'u.s. senate': 'us_senate',
    'us senate': 'us_senate',
    'united states senate': 'us_senate',
}

def get_office_key(office):
    office = office.strip().lower()
    return office_map.get(office, office.replace(' ', '_'))

results_by_year = {}
year = '2012'
contests = {}

# --- REGION MAPPING ---
# Example: Southeast Texas counties from Wikipedia
COUNTY_REGION_MAP = {
    # Southeast Texas
    'JEFFERSON': 'Southeast Texas',
    'ORANGE': 'Southeast Texas',
    'HARDIN': 'Southeast Texas',
    'CHAMBERS': 'Southeast Texas',
    'LIBERTY': 'Southeast Texas',
    'NEWTON': 'Southeast Texas',
    'TYLER': 'Southeast Texas',
    'JASPER': 'Southeast Texas',
    'POLK': 'Southeast Texas',
    'SAN JACINTO': 'Southeast Texas',
    'WALKER': 'Southeast Texas',
    'TRINITY': 'Southeast Texas',
    'MONTGOMERY': 'Southeast Texas',
    'HOUSTON': 'Southeast Texas',
    'SABINE': 'Southeast Texas',
    'ANGELINA': 'Southeast Texas',
    'NACOGDOCHES': 'Southeast Texas',
    'SHELBY': 'Southeast Texas',
    'SAN AUGUSTINE': 'Southeast Texas',
    'HARRIS': 'Southeast Texas',
    # Add more as needed, e.g. 'HOOD': 'DFW Metroplex',
}

for office in TARGET_OFFICES:
    office_norm = office.strip().lower()
    office_key = get_office_key(office)
    office_df = df[df['office_norm'] == office_norm]
    if office_df.empty:
        continue
    # Aggregate by county and party, and collect candidate names
    county_party = office_df.groupby(['county', 'party'])['votes'].apply(lambda x: x.astype(float).sum()).unstack(fill_value=0)
    # Get candidate names for DEM and REP
    candidate_map = {}
    for county, group in office_df.groupby('county'):
        dem_cand = group[(group['party'] == 'DEM') & (group['votes'].astype(float) > 0)]['candidate'].unique()
        rep_cand = group[(group['party'] == 'REP') & (group['votes'].astype(float) > 0)]['candidate'].unique()
        candidate_map[county.upper()] = {
            'dem_candidate': dem_cand[0] if len(dem_cand) > 0 else '',
            'rep_candidate': rep_cand[0] if len(rep_cand) > 0 else ''
        }
    contest_results = {}
    for county, row in county_party.iterrows():
        dem_votes = int(row.get('DEM', 0))
        rep_votes = int(row.get('REP', 0))
        # Calculate margin and margin_pct
        if dem_votes + rep_votes == 0:
            margin = 0
            margin_pct = 0
        else:
            margin = abs(rep_votes - dem_votes)
            margin_pct = 100 * margin / (dem_votes + rep_votes)
            # Make margin_pct positive for winner, negative for loser
            if rep_votes > dem_votes:
                margin_pct = margin_pct
            elif dem_votes > rep_votes:
                margin_pct = -margin_pct
            else:
                margin_pct = 0
        winner = 'REP' if rep_votes > dem_votes else ('DEM' if dem_votes > rep_votes else 'TIE')
        competitiveness = categorize_competitiveness(margin_pct)
        cands = candidate_map.get(county.upper(), {'dem_candidate': '', 'rep_candidate': ''})
        # Add margin_label (D+ or R+)
        if winner == 'REP':
            margin_label = f'R+{round(margin_pct, 2)}%'
        elif winner == 'DEM':
            margin_label = f'D+{abs(round(margin_pct, 2))}%'
        else:
            margin_label = 'Tied'
        region = COUNTY_REGION_MAP.get(county.upper(), '')
        contest_results[county.upper()] = {
            'county': county.upper(),
            'region': region,
            'contest': office_key,
            'year': year,
            'dem_candidate': cands['dem_candidate'],
            'rep_candidate': cands['rep_candidate'],
            'dem_votes': dem_votes,
            'rep_votes': rep_votes,
            'total_votes': dem_votes + rep_votes,
            'margin': margin,
            'margin_pct': round(margin_pct, 2),
            'margin_label': margin_label,
            'winner': winner,
            'competitiveness': competitiveness
        }
    contests[office_key] = {
        f'{office_key}_{year}_1': {
            'contest_name': office,
            'results': contest_results
        }
    }

results_by_year[year] = contests

output = {
    'focus': 'Clean geographic political patterns',
    'processed_date': str(date.today()),
    'categorization_system': {
        'competitiveness_scale': COMPETITIVENESS_SCALE,
        'office_types': ['Federal', 'State', 'Judicial', 'Other'],
        'enhanced_features': [
            'Competitiveness categorization for each county',
            'Contest type classification (Federal/State/Judicial)',
            'Office ranking system for analysis prioritization',
            'Color coding compatible with political geography visualization'
        ]
    },
    'summary': {
        'total_years': 1,
        'total_contests': len(contests),
        'total_county_results': sum(len(c[list(c.keys())[0]]['results']) for c in contests.values()),
        'years_covered': [year]
    },
    'results_by_year': results_by_year
}

with open(OUTPUT_JSON, 'w') as f:
    json.dump(output, f, indent=2)

print(f'Wrote {OUTPUT_JSON}')
