import json

with open('data/texas_election_results.json') as f:
    data = json.load(f)

# Extract 2020 and 2024 presidential margins for key counties
print('=== 2020 Presidential Margins ===')
pres2020 = data['results_by_year']['2020']['presidential']['president']
counties = ['STARR', 'HIDALGO', 'CAMERON', 'COLLIN', 'DENTON', 'TARRANT', 'TRAVIS', 'WILLIAMSON', 'FORT BEND', 'MIDLAND', 'BEXAR', 'HARRIS']

for county in counties:
    if county in pres2020['results']:
        result = pres2020['results'][county]
        dem_votes = result['dem_votes']
        rep_votes = result['rep_votes']
        total_votes = result['total_votes']
        margin_pct = result['margin_pct']
        winner = result['winner']
        
        dem_pct = (dem_votes / total_votes * 100) if total_votes > 0 else 0
        rep_pct = (rep_votes / total_votes * 100) if total_votes > 0 else 0
        
        margin_str = f"D+{margin_pct:.2f}%" if winner == 'DEM' else f"R+{margin_pct:.2f}%"
        print(f"{county}: {margin_str} (Trump {rep_pct:.2f}% vs Biden {dem_pct:.2f}%)")

print('\n=== 2024 Presidential Margins ===')
pres2024 = data['results_by_year']['2024']['presidential']['president']

for county in counties:
    if county in pres2024['results']:
        result = pres2024['results'][county]
        dem_votes = result['dem_votes']
        rep_votes = result['rep_votes']
        total_votes = result['total_votes']
        margin_pct = result['margin_pct']
        winner = result['winner']
        
        dem_pct = (dem_votes / total_votes * 100) if total_votes > 0 else 0
        rep_pct = (rep_votes / total_votes * 100) if total_votes > 0 else 0
        
        margin_str = f"D+{margin_pct:.2f}%" if winner == 'DEM' else f"R+{margin_pct:.2f}%"
        print(f"{county}: {margin_str} (Trump {rep_pct:.2f}% vs Harris {dem_pct:.2f}%)")

print('\n=== Swing Analysis (2020 → 2024) ===')
for county in counties:
    if county in pres2020['results'] and county in pres2024['results']:
        result2020 = pres2020['results'][county]
        result2024 = pres2024['results'][county]
        
        # Calculate swing
        margin2020 = result2020['margin_pct'] if result2020['winner'] == 'DEM' else -result2020['margin_pct']
        margin2024 = result2024['margin_pct'] if result2024['winner'] == 'DEM' else -result2024['margin_pct']
        swing = margin2024 - margin2020
        
        swing_str = f"{abs(swing):.2f}% {'leftward' if swing > 0 else 'rightward'}" if swing != 0 else "no change"
        
        margin2020_str = f"D+{result2020['margin_pct']:.2f}%" if result2020['winner'] == 'DEM' else f"R+{result2020['margin_pct']:.2f}%"
        margin2024_str = f"D+{result2024['margin_pct']:.2f}%" if result2024['winner'] == 'DEM' else f"R+{result2024['margin_pct']:.2f}%"
        
        print(f"{county}: {margin2020_str} → {margin2024_str} ({swing_str})")
