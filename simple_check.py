"""
Simple check of Ellis and El Paso counties in JSON
"""
import json

with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

# Get 2018 US Senate
senate_2018 = data['results_by_year']['2018']['statewide']
us_senate = None
for key, contest in senate_2018.items():
    if 'Senate' in contest.get('contest_name', ''):
        us_senate = contest
        break

if us_senate:
    print("2018 U.S. Senate Results:")
    print("-" * 60)
    
    ellis = us_senate['results']['ELLIS']
    print(f"ELLIS: DEM {ellis['dem_votes']:>7,} | REP {ellis['rep_votes']:>7,} | Total {ellis['total_votes']:>7,}")
    
    elpaso = us_senate['results']['EL PASO']
    print(f"EL PASO: DEM {elpaso['dem_votes']:>7,} | REP {elpaso['rep_votes']:>7,} | Total {elpaso['total_votes']:>7,}")
    
    print("\nExpected (post-swap):")
    print("ELLIS: ~151K DEM, ~51K REP (Democratic)")
    print("EL PASO: ~19K DEM, ~41K REP (Republican)")
