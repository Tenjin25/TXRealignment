import json

# Read the main JSON file
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("Checking Lampasas County in the final JSON output...")
print("="*70)

# Navigate to 2020 US Senate results
if '2020' in data['results_by_year']:
    if 'us_senate' in data['results_by_year']['2020']:
        senate_2020 = data['results_by_year']['2020']['us_senate']
        
        # Check if Lampasas exists
        if 'Lampasas' in senate_2020:
            lamp = senate_2020['Lampasas']
            print("\n✅ Lampasas County found in 2020 US Senate results!")
            print("\nVote breakdown:")
            print(f"  Democrat:   {lamp.get('DEM', 0):>6,}")
            print(f"  Republican: {lamp.get('REP', 0):>6,}")
            print(f"  Libertarian: {lamp.get('LIB', 0):>5,}")
            print(f"  Other:      {lamp.get('OTH', 0):>6,}")
            
            total = sum(lamp.values())
            print(f"\n  TOTAL:      {total:>6,}")
            
            if total == 10330:
                print("\n  ✅ CORRECT! Vote total matches expected 10,330 votes")
            else:
                print(f"\n  ⚠️ Mismatch: Expected 10,330, got {total:,}")
                
            print("\n" + "="*70)
        else:
            print("\n❌ Lampasas County NOT found in 2020 US Senate results")
            print("\nCounties starting with 'L':")
            for county in sorted(senate_2020.keys()):
                if county.startswith('L'):
                    print(f"  - {county}")
    else:
        print("\n❌ No us_senate data for 2020")
else:
    print("\n❌ No 2020 data in results")
