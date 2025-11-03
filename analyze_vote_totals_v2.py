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
        
        # Check if we have the simplified structure or detailed results
        if 'total_votes' in pres_contest:
            print(f"\n{year} Presidential: {pres_contest['total_votes']:,} votes")
            if 'dem_candidate' in pres_contest and isinstance(pres_contest['dem_candidate'], dict):
                print(f"  {pres_contest['dem_candidate']['name']} (D): {pres_contest['dem_candidate']['votes']:,}")
            elif 'dem_candidate' in pres_contest:
                print(f"  Dem candidate: {pres_contest['dem_candidate']}")
            if 'rep_candidate' in pres_contest and isinstance(pres_contest['rep_candidate'], dict):
                print(f"  {pres_contest['rep_candidate']['name']} (R): {pres_contest['rep_candidate']['votes']:,}")
            elif 'rep_candidate' in pres_contest:
                print(f"  Rep candidate: {pres_contest['rep_candidate']}")
            if 'other_votes' in pres_contest:
                print(f"  Others: {pres_contest['other_votes']:,}")
        
        # Check for detailed results by county
        if 'results' in pres_contest and pres_contest['results']:
            county_count = len(pres_contest['results'])
            sample_county = list(pres_contest['results'].keys())[0]
            print(f"  Has county-level data for {county_count} counties")
            print(f"  Sample (county {sample_county}):", pres_contest['results'][sample_county])
    
    # US Senate
    if 'us_senate' in year_data and 'us_senate' in year_data['us_senate']:
        senate_contest = year_data['us_senate']['us_senate']
        if 'total_votes' in senate_contest:
            print(f"\n{year} US Senate: {senate_contest['total_votes']:,} votes")
            if 'dem_candidate' in senate_contest and isinstance(senate_contest['dem_candidate'], dict):
                print(f"  {senate_contest['dem_candidate']['name']} (D): {senate_contest['dem_candidate']['votes']:,}")
            elif 'dem_candidate' in senate_contest:
                print(f"  Dem candidate: {senate_contest['dem_candidate']}")
            if 'rep_candidate' in senate_contest and isinstance(senate_contest['rep_candidate'], dict):
                print(f"  {senate_contest['rep_candidate']['name']} (R): {senate_contest['rep_candidate']['votes']:,}")
            elif 'rep_candidate' in senate_contest:
                print(f"  Rep candidate: {senate_contest['rep_candidate']}")
            if 'other_votes' in senate_contest:
                print(f"  Others: {senate_contest['other_votes']:,}")

print("\n" + "=" * 80)
print("\nExpected totals (approximate, based on Texas historical data):")
print("2000: ~6.4M, 2004: ~7.4M, 2008: ~8.1M, 2012: ~7.9M, 2016: ~8.9M, 2020: ~11.3M, 2024: ~11.2M")
