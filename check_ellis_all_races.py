import json

# Load the JSON file
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("ELLIS COUNTY - ALL RACES (2014 & 2018)")
print("=" * 80)

# Check all 2018 races
print("\n2018 RACES:")
print("-" * 80)
if '2018' in data['results_by_year']:
    for category, contests in data['results_by_year']['2018'].items():
        for contest_key, contest_data in contests.items():
            contest_name = contest_data.get('contest_name', contest_key)
            if 'results' in contest_data and 'ELLIS' in contest_data['results']:
                ellis = contest_data['results']['ELLIS']
                dem = ellis.get('dem_votes', 0)
                rep = ellis.get('rep_votes', 0)
                other = ellis.get('other_votes', 0)
                winner = ellis.get('winner', 'N/A')
                
                # Highlight if DEM won
                marker = " ⚠️ DEM WIN" if winner == 'DEM' else ""
                
                print(f"\n{contest_name}:{marker}")
                print(f"  DEM: {dem:>6,} | REP: {rep:>6,} | Other: {other:>6,}")
                print(f"  Winner: {winner} | Margin: {dem - rep:>+7,}")

# Check all 2014 races
print("\n" + "=" * 80)
print("2014 RACES:")
print("-" * 80)
if '2014' in data['results_by_year']:
    for category, contests in data['results_by_year']['2014'].items():
        for contest_key, contest_data in contests.items():
            contest_name = contest_data.get('contest_name', contest_key)
            if 'results' in contest_data and 'ELLIS' in contest_data['results']:
                ellis = contest_data['results']['ELLIS']
                dem = ellis.get('dem_votes', 0)
                rep = ellis.get('rep_votes', 0)
                other = ellis.get('other_votes', 0)
                winner = ellis.get('winner', 'N/A')
                
                # Highlight if DEM won
                marker = " ⚠️ DEM WIN" if winner == 'DEM' else ""
                
                print(f"\n{contest_name}:{marker}")
                print(f"  DEM: {dem:>6,} | REP: {rep:>6,} | Other: {other:>6,}")
                print(f"  Winner: {winner} | Margin: {dem - rep:>+7,}")

print("\n" + "=" * 80)
