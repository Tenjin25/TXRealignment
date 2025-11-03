import json

# Load the data
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

# Check structure
print("Top-level keys:", list(data.keys()))
print("\nresults_by_year keys:", list(data['results_by_year'].keys()))

# Examine one year in detail
year = '2008'
print(f"\n{year} structure:")
year_data = data['results_by_year'][year]
print(f"Categories in {year}:", list(year_data.keys()))

if 'presidential' in year_data:
    print(f"\nPresidential keys:", list(year_data['presidential'].keys()))
    pres = year_data['presidential']['president']
    print(f"President contest keys:", list(pres.keys()))
    print(f"Number of candidates:", len(pres.get('candidates', [])))
    if pres.get('candidates'):
        print(f"First candidate structure:", pres['candidates'][0])

# Check if votes are stored elsewhere
print("\n\nLet's check the actual data structure more carefully:")
if 'presidential' in year_data:
    pres = year_data['presidential']['president']
    if 'candidates' in pres and len(pres['candidates']) > 0:
        first_cand = pres['candidates'][0]
        print("First candidate full data:")
        print(json.dumps(first_cand, indent=2))
