import json

with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

fb = data['results_by_year']['2024']['presidential']['president']['results']['FORT BEND']
dem = fb['dem_votes']
rep = fb['rep_votes']
total = dem + rep
margin = ((dem - rep) / total) * 100

print(f"Fort Bend County 2024 Presidential:")
print(f"  Democratic votes: {dem:,}")
print(f"  Republican votes: {rep:,}")
print(f"  Total: {total:,}")
print(f"  Dem %: {(dem/total)*100:.4f}%")
print(f"  Rep %: {(rep/total)*100:.4f}%")
print(f"  Margin: D+{margin:.10f}%")
print(f"  Rounded to 2 decimals: D+{margin:.2f}%")
