import json

# Read the main JSON file
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

# Find Lampasas County
lampasas = None
for county in data['counties']:
    if county['name'] == 'Lampasas':
        lampasas = county
        break

if lampasas:
    print("✅ Lampasas County found in JSON!")
    print("="*70)
    
    # Check 2020 Senate race
    if '2020' in lampasas['results']:
        results_2020 = lampasas['results']['2020']
        if 'US Senate' in results_2020:
            senate = results_2020['US Senate']
            print("\n2020 US Senate Results:")
            print(f"  Democrat: {senate.get('DEM', 0):,}")
            print(f"  Republican: {senate.get('REP', 0):,}")
            print(f"  Other parties: {senate.get('LIB', 0) + senate.get('GRN', 0):,}")
            total = sum(senate.values())
            print(f"  TOTAL: {total:,}")
            
            if total == 10330:
                print("\n  ✅ Vote total is CORRECT! (10,330)")
            else:
                print(f"\n  ⚠️ Vote total mismatch. Expected 10,330, got {total:,}")
        else:
            print("\n⚠️ US Senate race not found in 2020 results")
    else:
        print("\n⚠️ 2020 results not found for Lampasas")
    
    print("\n" + "="*70)
    
    # Show all available years
    print(f"\nAvailable years for Lampasas: {sorted(lampasas['results'].keys())}")
else:
    print("❌ Lampasas County NOT found in JSON")
    print("\nSearching for similar names...")
    for county in data['counties']:
        if 'lamp' in county['name'].lower():
            print(f"  Found: {county['name']}")
