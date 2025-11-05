"""
Update 2020 Railroad Commissioner candidate names to include first names
"""
import json

# Load the JSON
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

# Update 2020 Railroad Commissioner
if '2020' in data['results_by_year']:
    if 'statewide' in data['results_by_year']['2020']:
        if 'railroad_commissioner' in data['results_by_year']['2020']['statewide']:
            rr = data['results_by_year']['2020']['statewide']['railroad_commissioner']
            
            print("Current candidate names:")
            print(f"  DEM: {rr.get('dem_candidate', 'NOT FOUND')}")
            print(f"  REP: {rr.get('rep_candidate', 'NOT FOUND')}")
            
            # Update with full names
            rr['dem_candidate'] = 'Chrysta Castañeda'
            rr['rep_candidate'] = 'Jim Wright'
            
            print("\nUpdated candidate names:")
            print(f"  DEM: {rr['dem_candidate']}")
            print(f"  REP: {rr['rep_candidate']}")
            
            # Also update in county-level results
            if 'results' in rr:
                for county, county_data in rr['results'].items():
                    county_data['dem_candidate'] = 'Chrysta Castañeda'
                    county_data['rep_candidate'] = 'Jim Wright'
                
                print(f"\nUpdated {len(rr['results'])} county-level entries")

# Save back to JSON
with open('data/texas_election_results.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✅ Successfully updated 2020 Railroad Commissioner candidate names")
