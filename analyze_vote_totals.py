import json

# Load the data
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

years = sorted(data['results_by_year'].keys())

print("Year-by-year vote totals:")
print("=" * 80)

for year in years:
    year_data = data['results_by_year'][year]
    
    # Presidential
    if 'presidential' in year_data and 'president' in year_data['presidential']:
        pres_contest = year_data['presidential']['president']
        pres_total = sum(cand['votes'] for cand in pres_contest.get('candidates', []))
        print(f"\n{year} Presidential: {pres_total:,} votes")
        
        # Show top candidates
        candidates = sorted(pres_contest.get('candidates', []), key=lambda x: x['votes'], reverse=True)[:3]
        for cand in candidates:
            print(f"  {cand['name']}: {cand['votes']:,}")
    
    # US Senate
    if 'us_senate' in year_data and 'us_senate' in year_data['us_senate']:
        senate_contest = year_data['us_senate']['us_senate']
        senate_total = sum(cand['votes'] for cand in senate_contest.get('candidates', []))
        print(f"\n{year} US Senate: {senate_total:,} votes")
        
        # Show top candidates
        candidates = sorted(senate_contest.get('candidates', []), key=lambda x: x['votes'], reverse=True)[:3]
        for cand in candidates:
            print(f"  {cand['name']}: {cand['votes']:,}")

print("\n" + "=" * 80)
print("\nExpected totals (approximate, based on Texas historical data):")
print("2000: ~6.4M, 2004: ~7.4M, 2008: ~8.1M, 2012: ~7.9M, 2016: ~8.9M, 2020: ~11.3M, 2024: ~11.2M")
