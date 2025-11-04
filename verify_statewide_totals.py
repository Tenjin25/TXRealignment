import json

# Load the JSON file
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("2018 STATEWIDE TOTALS VERIFICATION")
print("=" * 80)

# 2018 U.S. Senate - Beto vs Cruz (famous race)
print("\n2018 U.S. Senate (Beto O'Rourke vs Ted Cruz):")
print("-" * 80)
if '2018' in data['results_by_year'] and 'us_senate' in data['results_by_year']['2018']:
    senate_2018 = data['results_by_year']['2018']['us_senate']['us_senate']
    st = senate_2018.get('statewide_totals', {})
    dem_votes = st.get('dem_votes', 0)
    rep_votes = st.get('rep_votes', 0)
    total = st.get('total_votes', 0)
    
    print(f"Our Data:")
    print(f"  DEM (Beto): {dem_votes:,}")
    print(f"  REP (Cruz):  {rep_votes:,}")
    print(f"  Total:       {total:,}")
    
    print(f"\nOfficial Texas SOS Results:")
    print(f"  DEM (Beto): 4,045,632")
    print(f"  REP (Cruz):  4,260,553")
    print(f"  Total:       8,371,655 (includes other candidates)")
    
    print(f"\nComparison:")
    official_dem = 4045632
    official_rep = 4260553
    diff_dem = dem_votes - official_dem
    diff_rep = rep_votes - official_rep
    
    print(f"  DEM difference: {diff_dem:+,} ({(diff_dem/official_dem*100):+.2f}%)")
    print(f"  REP difference: {diff_rep:+,} ({(diff_rep/official_rep*100):+.2f}%)")
    
    if abs(diff_dem) > 1000 or abs(diff_rep) > 1000:
        print(f"  ⚠️  WARNING: Significant discrepancy detected!")
    else:
        print(f"  ✅ Values match official results")

print("\n" + "=" * 80)
print("2014 STATEWIDE TOTALS VERIFICATION")
print("=" * 80)

# 2014 U.S. Senate - Cornyn
print("\n2014 U.S. Senate (David Alameel vs John Cornyn):")
print("-" * 80)
if '2014' in data['results_by_year'] and 'us_senate' in data['results_by_year']['2014']:
    senate_2014 = data['results_by_year']['2014']['us_senate']['us_senate']
    st = senate_2014.get('statewide_totals', {})
    dem_votes = st.get('dem_votes', 0)
    rep_votes = st.get('rep_votes', 0)
    total = st.get('total_votes', 0)
    
    print(f"Our Data:")
    print(f"  DEM (Alameel): {dem_votes:,}")
    print(f"  REP (Cornyn):  {rep_votes:,}")
    print(f"  Total:         {total:,}")
    
    print(f"\nOfficial Texas SOS Results:")
    print(f"  DEM (Alameel): 1,597,387")
    print(f"  REP (Cornyn):  2,861,531")
    print(f"  Total:         4,747,442 (includes other candidates)")
    
    print(f"\nComparison:")
    official_dem = 1597387
    official_rep = 2861531
    diff_dem = dem_votes - official_dem
    diff_rep = rep_votes - official_rep
    
    print(f"  DEM difference: {diff_dem:+,} ({(diff_dem/official_dem*100):+.2f}%)")
    print(f"  REP difference: {diff_rep:+,} ({(diff_rep/official_rep*100):+.2f}%)")
    
    if abs(diff_dem) > 1000 or abs(diff_rep) > 1000:
        print(f"  ⚠️  WARNING: Significant discrepancy detected!")
    else:
        print(f"  ✅ Values match official results")

# Also check 2018 Governor
print("\n" + "=" * 80)
print("2018 Governor (Lupe Valdez vs Greg Abbott):")
print("-" * 80)
if '2018' in data['results_by_year'] and 'statewide' in data['results_by_year']['2018']:
    for key, contest in data['results_by_year']['2018']['statewide'].items():
        if contest.get('contest_name') == 'Governor':
            st = contest.get('statewide_totals', {})
            dem_votes = st.get('dem_votes', 0)
            rep_votes = st.get('rep_votes', 0)
            
            print(f"Our Data:")
            print(f"  DEM (Valdez): {dem_votes:,}")
            print(f"  REP (Abbott): {rep_votes:,}")
            
            print(f"\nOfficial Texas SOS Results:")
            print(f"  DEM (Valdez): 3,546,615")
            print(f"  REP (Abbott): 4,656,196")
            
            print(f"\nComparison:")
            official_dem = 3546615
            official_rep = 4656196
            diff_dem = dem_votes - official_dem
            diff_rep = rep_votes - official_rep
            
            print(f"  DEM difference: {diff_dem:+,} ({(diff_dem/official_dem*100):+.2f}%)")
            print(f"  REP difference: {diff_rep:+,} ({(diff_rep/official_rep*100):+.2f}%)")
            
            if abs(diff_dem) > 1000 or abs(diff_rep) > 1000:
                print(f"  ⚠️  WARNING: Significant discrepancy detected!")
            else:
                print(f"  ✅ Values match official results")

print("\n" + "=" * 80)
print("Sources:")
print("-" * 80)
print("2018: https://results.texas-election.com/races")
print("2014: https://www.sos.texas.gov/elections/historical/70-95.shtml")
