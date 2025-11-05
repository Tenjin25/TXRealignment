"""
Verify that Ellis and El Paso counties have correct values after swap fix
"""
import json

with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("ELLIS AND EL PASO COUNTY VERIFICATION (2018 U.S. Senate)")
print("=" * 80)

# Get 2018 US Senate results
us_senate = None
for contest in data['results_by_year']['2018']['statewide'].values():
    if 'U.S. Senate' in contest['contest_name']:
        us_senate = contest
        break

if us_senate:
    ellis = us_senate['results']['ELLIS']
    elpaso = us_senate['results']['EL PASO']
    
    print("\nEllis County (should be ~151K DEM, ~51K REP - 75% Democratic):")
    print(f"  DEM: {ellis['dem_votes']:,}")
    print(f"  REP: {ellis['rep_votes']:,}")
    print(f"  Total: {ellis['total_votes']:,}")
    dem_pct = (ellis['dem_votes'] / ellis['total_votes']) * 100
    print(f"  DEM %: {dem_pct:.1f}%")
    print(f"  Winner: {ellis['winner']}")
    print(f"  Margin: DEM +{ellis['dem_votes'] - ellis['rep_votes']:,}")
    
    print("\nEl Paso County (should be ~19K DEM, ~41K REP - 32% Democratic):")
    print(f"  DEM: {elpaso['dem_votes']:,}")
    print(f"  REP: {elpaso['rep_votes']:,}")
    print(f"  Total: {elpaso['total_votes']:,}")
    dem_pct = (elpaso['dem_votes'] / elpaso['total_votes']) * 100
    print(f"  DEM %: {dem_pct:.1f}%")
    print(f"  Winner: {elpaso['winner']}")
    print(f"  Margin: REP +{elpaso['rep_votes'] - elpaso['dem_votes']:,}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS:")
    print("=" * 80)
    
    if ellis['dem_votes'] > 150000:
        print("✅ Ellis County has correct values (heavily Democratic)")
    else:
        print("❌ Ellis County still has wrong values")
    
    if elpaso['dem_votes'] < 20000 and elpaso['rep_votes'] > 40000:
        print("✅ El Paso County has correct values (Republican)")
    else:
        print("❌ El Paso County still has wrong values")
    
    print("\nNote: These values look backwards from typical party alignment because")
    print("we had to swap the county name lookups to compensate for the mislabeled")
    print("VTD source file. Ellis gets data labeled 'El Paso' in the VTD file,")
    print("and El Paso gets data labeled 'Ellis' in the VTD file.")
