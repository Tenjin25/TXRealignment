"""
Check 2024 election data for potential undercounts by comparing against 
official results and checking for missing county data.
"""
import json

# Load the JSON data
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("2024 ELECTION UNDERCOUNT CHECK")
print("=" * 80)

# Check if 2024 exists
if '2024' not in data['results_by_year']:
    print("\n❌ 2024 data not found in JSON")
    exit(1)

year_2024 = data['results_by_year']['2024']

# Find US Senate race (Cruz vs Allred)
us_senate = None
if 'us_senate' in year_2024 and 'us_senate' in year_2024['us_senate']:
    us_senate = year_2024['us_senate']['us_senate']

if not us_senate:
    print("\n❌ 2024 U.S. Senate race not found")
else:
    print("\n2024 U.S. Senate (Ted Cruz vs Colin Allred):")
    print("-" * 80)
    
    statewide = us_senate.get('statewide_totals', {})
    results = us_senate.get('results', {})
    
    # Count counties
    counties_with_data = [c for c in results.keys() if c != 'statewide']
    print(f"Counties with data: {len(counties_with_data)}/254")
    
    if statewide:
        dem = statewide.get('dem_votes', 0)
        rep = statewide.get('rep_votes', 0)
        total = statewide.get('total_votes', 0)
        
        print(f"\nOur statewide totals:")
        print(f"  DEM (Allred): {dem:>10,}")
        print(f"  REP (Cruz):   {rep:>10,}")
        print(f"  Total votes:  {total:>10,}")
        
        # Official 2024 results (from Texas SOS - preliminary/unofficial as of Nov 2024)
        # These are estimates based on reporting - update with official certified results
        official_dem = 4_481_000  # Allred (estimated)
        official_rep = 5_298_000  # Cruz (estimated)
        official_total = 9_867_000  # Total (estimated)
        
        print(f"\nEstimated official results (preliminary):")
        print(f"  DEM (Allred): {official_dem:>10,}")
        print(f"  REP (Cruz):   {official_rep:>10,}")
        print(f"  Total votes:  {official_total:>10,}")
        
        dem_diff = dem - official_dem
        rep_diff = rep - official_rep
        total_diff = total - official_total
        
        dem_pct = (dem_diff / official_dem * 100) if official_dem else 0
        rep_pct = (rep_diff / official_rep * 100) if official_rep else 0
        total_pct = (total_diff / official_total * 100) if official_total else 0
        
        print(f"\nDifference from estimated official:")
        print(f"  DEM: {dem_diff:>+10,} ({dem_pct:>+6.2f}%)")
        print(f"  REP: {rep_diff:>+10,} ({rep_pct:>+6.2f}%)")
        print(f"  Total: {total_diff:>+10,} ({total_pct:>+6.2f}%)")
        
        if abs(dem_pct) > 2 or abs(rep_pct) > 2:
            print("\n⚠️  WARNING: Significant discrepancy detected (>2%)")
            print("    Check for missing counties or data issues")
        else:
            print("\n✅ Totals within acceptable range (<2% difference)")
    
    # Check for Ellis and El Paso specifically in 2024
    print("\n" + "=" * 80)
    print("Ellis and El Paso County Check (2024):")
    print("-" * 80)
    
    if 'ELLIS' in results:
        ellis = results['ELLIS']
        print(f"ELLIS:   DEM {ellis['dem_votes']:>7,} | REP {ellis['rep_votes']:>7,} | Winner: {ellis.get('winner', 'N/A')}")
    else:
        print("⚠️  ELLIS county not found in 2024 data")
    
    if 'EL PASO' in results:
        elpaso = results['EL PASO']
        print(f"EL PASO: DEM {elpaso['dem_votes']:>7,} | REP {elpaso['rep_votes']:>7,} | Winner: {elpaso.get('winner', 'N/A')}")
    else:
        print("⚠️  EL PASO county not found in 2024 data")

# Check other major 2024 races
print("\n" + "=" * 80)
print("Other 2024 Statewide Races:")
print("-" * 80)

if 'statewide' in year_2024:
    for key, contest in year_2024['statewide'].items():
        name = contest.get('contest_name', key)
        statewide = contest.get('statewide_totals', {})
        
        if statewide:
            dem = statewide.get('dem_votes', 0)
            rep = statewide.get('rep_votes', 0)
            total = statewide.get('total_votes', 0)
            
            if total > 0:
                dem_pct = (dem / total * 100)
                print(f"{name:40} | DEM {dem:>10,} ({dem_pct:>5.1f}%) | REP {rep:>10,}")

print("\n" + "=" * 80)
print("NOTE: 2024 official results may not be certified yet.")
print("Comparison uses preliminary/estimated totals.")
print("Update with certified results when available.")
print("=" * 80)
