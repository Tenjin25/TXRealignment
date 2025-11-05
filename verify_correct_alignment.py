"""
Check Ellis County and El Paso County voting patterns to verify correct political alignment
"""
import json

with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("ELLIS COUNTY - Historical Voting Patterns")
print("(Should be REPUBLICAN - Dallas exurb)")
print("=" * 80)

# Check multiple years to see pattern
test_years = {
    '2016': 'governor',
    '2018': 'us_senate', 
    '2020': 'governor',
    '2022': 'governor',
    '2024': 'us_senate'
}

for year, category in test_years.items():
    if year in data['results_by_year']:
        if category in data['results_by_year'][year]:
            contests = data['results_by_year'][year][category]
            first_contest = list(contests.values())[0]
            if 'ELLIS' in first_contest['results']:
                ellis = first_contest['results']['ELLIS']
                total = ellis['dem_votes'] + ellis['rep_votes']
                rep_pct = (ellis['rep_votes'] / total * 100) if total > 0 else 0
                print(f"{year}: DEM {ellis['dem_votes']:>6,} | REP {ellis['rep_votes']:>6,} | REP {rep_pct:>5.1f}% | Winner: {ellis['winner']}")

print("\n" + "=" * 80)
print("EL PASO COUNTY - Historical Voting Patterns")
print("(Should be DEMOCRATIC - Border county)")
print("=" * 80)

for year, category in test_years.items():
    if year in data['results_by_year']:
        if category in data['results_by_year'][year]:
            contests = data['results_by_year'][year][category]
            first_contest = list(contests.values())[0]
            if 'EL PASO' in first_contest['results']:
                elpaso = first_contest['results']['EL PASO']
                total = elpaso['dem_votes'] + elpaso['rep_votes']
                dem_pct = (elpaso['dem_votes'] / total * 100) if total > 0 else 0
                print(f"{year}: DEM {elpaso['dem_votes']:>6,} | REP {elpaso['rep_votes']:>6,} | DEM {dem_pct:>5.1f}% | Winner: {elpaso['winner']}")

print("\n" + "=" * 80)
print("2018 US SENATE COMPARISON (Current Values)")
print("=" * 80)
us_senate_2018 = data['results_by_year']['2018']['us_senate']['us_senate']
ellis = us_senate_2018['results']['ELLIS']
elpaso = us_senate_2018['results']['EL PASO']

print(f"ELLIS:   DEM {ellis['dem_votes']:>7,} | REP {ellis['rep_votes']:>7,}")
print(f"EL PASO: DEM {elpaso['dem_votes']:>7,} | REP {elpaso['rep_votes']:>7,}")

print("\n⚠️  CURRENT STATUS:")
if ellis['rep_votes'] > ellis['dem_votes']:
    print("✅ Ellis shows REPUBLICAN (correct)")
else:
    print("❌ Ellis shows DEMOCRATIC (WRONG - should be Republican exurb!)")

if elpaso['dem_votes'] > elpaso['rep_votes']:
    print("✅ El Paso shows DEMOCRATIC (correct)")
else:
    print("❌ El Paso shows REPUBLICAN (WRONG - should be Democratic border county!)")
