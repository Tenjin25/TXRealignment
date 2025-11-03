import json

# Load the JSON
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

# Get 2020 U.S. Senate results for Lampasas
senate_2020 = data['results_by_year']['2020']['us_senate']['us_senate']
lampasas = senate_2020['results'].get('LAMPASAS')

if lampasas:
    print("Lampasas County 2020 U.S. Senate Results:")
    print(f"  Dem: {lampasas['dem_votes']} ({lampasas['dem_candidate']})")
    print(f"  Rep: {lampasas['rep_votes']} ({lampasas['rep_candidate']})")
    print(f"  Other: {lampasas['other_votes']}")
    print(f"  Total: {lampasas['total_votes']}")
else:
    print("⚠️ Lampasas County not found in 2020 U.S. Senate results")
