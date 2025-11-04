"""
Comprehensive verification of anchor counties across 2014 and 2018 contests
to ensure no county swaps or data issues remain.

Checks major Texas counties with known political leanings:
- Ellis: Republican (Dallas exurb)
- El Paso: Democratic (border county)
- Harris: Democratic (Houston)
- Dallas: Democratic (Dallas)
- Tarrant: Republican (Fort Worth)
- Travis: Democratic (Austin)
- Bexar: Democratic (San Antonio)
"""
import json
import sys

# Load the JSON data
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

# Expected political leanings (True = should be Democratic, False = should be Republican)
EXPECTED_LEANINGS = {
    'ELLIS': False,      # Republican Dallas exurb
    'EL PASO': True,     # Democratic border county
    'HARRIS': True,      # Democratic (Houston)
    'DALLAS': True,      # Democratic
    'TARRANT': False,    # Republican (Fort Worth) - though competitive
    'TRAVIS': True,      # Democratic (Austin)
    'BEXAR': True,       # Democratic (San Antonio) - though competitive
}

# Contests to check (category_key, contest_key, display_name)
CONTESTS_TO_CHECK = {
    2018: [
        ('us_senate', 'us_senate', 'U.S. Senate'),
        ('statewide', 'governor', 'Governor'),
        ('statewide', 'lt_governor', 'Lieutenant Governor'),
        ('statewide', 'attorney_general', 'Attorney General'),
        ('statewide', 'comptroller', 'Comptroller'),
        ('statewide', 'land_commissioner', 'Land Commissioner'),
        ('statewide', 'agriculture_commissioner', 'Agriculture Commissioner'),
        ('statewide', 'railroad_commissioner', 'Railroad Commissioner'),
    ],
    2014: [
        ('us_senate', 'us_senate', 'U.S. Senate'),
        ('statewide', 'governor', 'Governor'),
        ('statewide', 'lt_governor', 'Lieutenant Governor'),
        ('statewide', 'attorney_general', 'Attorney General'),
        ('statewide', 'comptroller', 'Comptroller'),
        ('statewide', 'land_commissioner', 'Land Commissioner'),
        ('statewide', 'agriculture_commissioner', 'Agriculture Commissioner'),
        ('statewide', 'railroad_commissioner', 'Railroad Commissioner'),
    ]
}

def check_county_alignment(county, dem_votes, rep_votes, expected_dem):
    """Check if county results match expected political leaning"""
    is_dem = dem_votes > rep_votes
    matches = is_dem == expected_dem
    return matches, is_dem

print("=" * 80)
print("COMPREHENSIVE ANCHOR COUNTY VERIFICATION")
print("=" * 80)

all_passed = True
total_checks = 0
failed_checks = []

for year in ['2014', '2018']:
    print(f"\n{'=' * 80}")
    print(f"{year} CONTESTS")
    print("=" * 80)
    
    for category_key, contest_key, contest_name in CONTESTS_TO_CHECK[int(year)]:
        print(f"\n{contest_name}:")
        print("-" * 80)
        
        # Navigate to the contest
        try:
            contest = data['results_by_year'][year][category_key][contest_key]
        except KeyError:
            print(f"  ⚠️  Contest not found in JSON structure")
            continue
        
        results = contest.get('results', {})
        
        for county_name, expected_dem in EXPECTED_LEANINGS.items():
            if county_name not in results:
                print(f"  ⚠️  {county_name}: Not found in results")
                continue
            
            county_data = results[county_name]
            dem = county_data.get('dem_votes', 0)
            rep = county_data.get('rep_votes', 0)
            total = county_data.get('total_votes', 0)
            
            if total == 0:
                print(f"  ⚠️  {county_name}: No votes recorded")
                continue
            
            matches, is_dem = check_county_alignment(county_name, dem, rep, expected_dem)
            total_checks += 1
            
            status = "✅" if matches else "❌"
            party = "DEM" if is_dem else "REP"
            expected_party = "DEM" if expected_dem else "REP"
            
            dem_pct = (dem / total) * 100
            
            print(f"  {status} {county_name:12} → {party} wins ({dem:>7,} DEM / {rep:>7,} REP = {dem_pct:5.1f}% DEM) | Expected: {expected_party}")
            
            if not matches:
                all_passed = False
                failed_checks.append({
                    'year': year,
                    'contest': contest_name,
                    'county': county_name,
                    'expected': expected_party,
                    'actual': party,
                    'dem': dem,
                    'rep': rep
                })

print("\n" + "=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)
print(f"Total checks: {total_checks}")
print(f"Passed: {total_checks - len(failed_checks)}")
print(f"Failed: {len(failed_checks)}")

if failed_checks:
    print("\n❌ FAILED CHECKS:")
    for check in failed_checks:
        print(f"  {check['year']} {check['contest']} - {check['county']}: "
              f"Expected {check['expected']}, got {check['actual']} "
              f"({check['dem']:,} DEM / {check['rep']:,} REP)")
    sys.exit(1)
else:
    print("\n✅ ALL CHECKS PASSED - County alignments are correct!")
    sys.exit(0)
