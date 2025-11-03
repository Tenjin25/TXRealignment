import json

# Load the election data
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

# Get presidential results
pres2020 = data['results_by_year']['2020']['presidential']['president']
pres2024 = data['results_by_year']['2024']['presidential']['president']

counties = ['HARRIS', 'MONTGOMERY']

print("=== Harris & Montgomery Counties: 2020 vs 2024 ===\n")

for county in counties:
    if county in pres2020['results'] and county in pres2024['results']:
        # 2020 data
        results_2020 = pres2020['results'][county]
        margin_2020 = results_2020['margin_pct']
        winner_2020 = results_2020['winner']
        dem_pct_2020 = (results_2020['dem_votes'] / results_2020['total_votes']) * 100
        rep_pct_2020 = (results_2020['rep_votes'] / results_2020['total_votes']) * 100
        
        # 2024 data
        results_2024 = pres2024['results'][county]
        margin_2024 = results_2024['margin_pct']
        winner_2024 = results_2024['winner']
        dem_pct_2024 = (results_2024['dem_votes'] / results_2024['total_votes']) * 100
        rep_pct_2024 = (results_2024['rep_votes'] / results_2024['total_votes']) * 100
        
        # Calculate swing
        signed_margin_2020 = margin_2020 if winner_2020 == 'DEM' else -margin_2020
        signed_margin_2024 = margin_2024 if winner_2024 == 'DEM' else -margin_2024
        swing = signed_margin_2020 - signed_margin_2024  # Positive = rightward
        
        print(f"**{county} COUNTY**")
        print(f"2020: {'D+' if winner_2020 == 'DEM' else 'R+'}{margin_2020:.2f}% (Biden {dem_pct_2020:.2f}% vs Trump {rep_pct_2020:.2f}%)")
        print(f"2024: {'D+' if winner_2024 == 'DEM' else 'R+'}{margin_2024:.2f}% (Harris {dem_pct_2024:.2f}% vs Trump {rep_pct_2024:.2f}%)")
        print(f"Swing: {swing:.2f}-point rightward shift")
        print()
