import json

# Load the JSON file
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("CHECKING FOR MISSING OR INCOMPLETE COUNTY DATA")
print("=" * 80)

# 2018 U.S. Senate
print("\n2018 U.S. Senate - County Coverage:")
print("-" * 80)
if '2018' in data['results_by_year'] and 'us_senate' in data['results_by_year']['2018']:
    senate_2018 = data['results_by_year']['2018']['us_senate']['us_senate']
    results = senate_2018.get('results', {})
    
    total_counties = len(results)
    print(f"Total counties in data: {total_counties}")
    print(f"Expected: 254 counties")
    
    if total_counties < 254:
        print(f"⚠️  MISSING {254 - total_counties} counties!")
    
    # Check for counties with zero votes
    zero_vote_counties = []
    low_vote_counties = []
    
    for county, county_data in results.items():
        total_votes = county_data.get('total_votes', 0)
        dem_votes = county_data.get('dem_votes', 0)
        rep_votes = county_data.get('rep_votes', 0)
        
        if total_votes == 0:
            zero_vote_counties.append(county)
        elif total_votes < 100:  # Suspiciously low
            low_vote_counties.append((county, total_votes))
    
    if zero_vote_counties:
        print(f"\n⚠️  Counties with ZERO votes ({len(zero_vote_counties)}):")
        for county in sorted(zero_vote_counties):
            print(f"    - {county}")
    
    if low_vote_counties:
        print(f"\n⚠️  Counties with suspiciously low votes:")
        for county, votes in sorted(low_vote_counties, key=lambda x: x[1]):
            print(f"    - {county}: {votes} votes")
    
    # Check for major counties
    major_counties = ['HARRIS', 'DALLAS', 'TARRANT', 'BEXAR', 'TRAVIS', 'COLLIN', 'DENTON', 'EL PASO']
    print(f"\nChecking major counties:")
    for county in major_counties:
        if county in results:
            county_data = results[county]
            dem = county_data.get('dem_votes', 0)
            rep = county_data.get('rep_votes', 0)
            total = county_data.get('total_votes', 0)
            print(f"  ✅ {county}: {total:,} total votes (DEM: {dem:,}, REP: {rep:,})")
        else:
            print(f"  ❌ {county}: MISSING!")

# Also check 2014
print("\n" + "=" * 80)
print("2014 U.S. Senate - County Coverage:")
print("-" * 80)
if '2014' in data['results_by_year'] and 'us_senate' in data['results_by_year']['2014']:
    senate_2014 = data['results_by_year']['2014']['us_senate']['us_senate']
    results = senate_2014.get('results', {})
    
    total_counties = len(results)
    print(f"Total counties in data: {total_counties}")
    print(f"Expected: 254 counties")
    
    if total_counties < 254:
        print(f"⚠️  MISSING {254 - total_counties} counties!")
    
    # Check for counties with zero votes
    zero_vote_counties = []
    
    for county, county_data in results.items():
        total_votes = county_data.get('total_votes', 0)
        if total_votes == 0:
            zero_vote_counties.append(county)
    
    if zero_vote_counties:
        print(f"\n⚠️  Counties with ZERO votes ({len(zero_vote_counties)}):")
        for county in sorted(zero_vote_counties):
            print(f"    - {county}")
