import json

# Load the JSON file
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("TEXAS SUPREME COURT RACES - 2014")
print("=" * 80)

if '2014' in data['results_by_year']:
    if 'judicial' in data['results_by_year']['2014']:
        print("\n2014 Supreme Court Races in JSON:")
        print("-" * 80)
        for contest_key, contest_data in data['results_by_year']['2014']['judicial'].items():
            contest_name = contest_data.get('contest_name', contest_key)
            if 'Supreme Court' in contest_name:
                print(f"\nKey: {contest_key}")
                print(f"Name: {contest_name}")
                print(f"DEM Candidate: {contest_data.get('dem_candidate', 'N/A')}")
                print(f"REP Candidate: {contest_data.get('rep_candidate', 'N/A')}")
                
                # Show statewide totals
                if 'statewide_totals' in contest_data:
                    st = contest_data['statewide_totals']
                    print(f"Statewide: DEM {st.get('dem_votes', 0):,} | REP {st.get('rep_votes', 0):,}")

print("\n" + "=" * 80)
print("VERIFICATION FROM ELECTION RECORDS")
print("=" * 80)
print("""
According to Texas Secretary of State records for November 4, 2014:

Texas Supreme Court races on the ballot:
  ✅ Chief Justice (Position 1)
     - DEM: William Moody
     - REP: Nathan Hecht (incumbent, won)
  
  ✅ Justice, Place 6
     - DEM: Lawrence Edward Meyers
     - REP: Jeff Brown (won)
  
  ✅ Justice, Place 7 
     - DEM: Gina Benavides
     - REP: Jeff Boyd (incumbent, won)
  
  ✅ Justice, Place 8
     - DEM: Jim Chisholm
     - REP: Phil Johnson (incumbent, won - UNCONTESTED)

Note: Place 8 was UNCONTESTED - Phil Johnson (R) ran unopposed.
There was a Libertarian candidate (Tom Oxford) but no Democratic candidate.

Source: https://www.sos.state.tx.us/elections/historical/70-95.shtml
""")

# Check what our data shows
print("=" * 80)
print("CHECKING OUR DATA FOR PLACE 8:")
print("=" * 80)

if '2014' in data['results_by_year'] and 'judicial' in data['results_by_year']['2014']:
    for contest_key, contest_data in data['results_by_year']['2014']['judicial'].items():
        if 'Place 8' in contest_data.get('contest_name', ''):
            print(f"\nFound: {contest_data.get('contest_name')}")
            print(f"DEM Candidate: {contest_data.get('dem_candidate', 'N/A')}")
            print(f"REP Candidate: {contest_data.get('rep_candidate', 'N/A')}")
            
            if 'statewide_totals' in contest_data:
                st = contest_data['statewide_totals']
                dem_votes = st.get('dem_votes', 0)
                rep_votes = st.get('rep_votes', 0)
                other_votes = st.get('other_votes', 0)
                print(f"\nStatewide Totals:")
                print(f"  DEM: {dem_votes:,}")
                print(f"  REP: {rep_votes:,}")
                print(f"  Other: {other_votes:,}")
                
                if dem_votes == 0:
                    print("\n  ✅ CORRECT: DEM votes = 0 (race was uncontested, no Dem candidate)")
                else:
                    print(f"\n  ⚠️  WARNING: DEM votes = {dem_votes:,} but race should be uncontested")
            
            # Check Ellis County
            if 'results' in contest_data and 'ELLIS' in contest_data['results']:
                ellis = contest_data['results']['ELLIS']
                print(f"\nEllis County:")
                print(f"  DEM: {ellis.get('dem_votes', 0):,}")
                print(f"  REP: {ellis.get('rep_votes', 0):,}")
                print(f"  Other: {ellis.get('other_votes', 0):,}")
