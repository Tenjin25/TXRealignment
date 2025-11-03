import json

# Load the data
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

y2018 = data['results_by_year']['2018']

print('2018 Data:')
print('Categories:', list(y2018.keys()))

senate = y2018.get('us_senate', {}).get('us_senate', {})
print('\n2018 US Senate (Beto O\'Rourke vs Ted Cruz):')
print(f"Total votes: {senate.get('total_votes', 0):,}")
print(f"Expected: ~8.4M (this was a very high turnout race)")
print(f"Ratio: {senate.get('total_votes', 0) / 8_400_000:.2f}x")

if 'results' in senate:
    county_total = sum(county_data['total_votes'] for county_data in senate['results'].values())
    print(f"\nSum from county data: {county_total:,}")
    print(f"Number of counties: {len(senate['results'])}")
    
    # Check if there's a mismatch
    if senate.get('total_votes') != county_total:
        print(f"⚠️ MISMATCH: Stored total ({senate.get('total_votes'):,}) != County sum ({county_total:,})")

# Check if there's a presidential race in 2018 (there shouldn't be)
if 'presidential' in y2018:
    print('\n⚠️ WARNING: 2018 has presidential data (midterm year - should not have this)')
