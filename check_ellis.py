import json

# Load the JSON data
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("=" * 60)
print("ELLIS COUNTY VERIFICATION")
print("=" * 60)

# Check 2018 U.S. Senate
print("\n2018 U.S. Senate - Ellis County:")
try:
    ellis_2018_senate = data['results_by_year']['2018']['us_senate']['us_senate']['results']['ELLIS']
    print(f"  DEM votes: {ellis_2018_senate['dem_votes']}")
    print(f"  REP votes: {ellis_2018_senate['rep_votes']}")
    print(f"  Other votes: {ellis_2018_senate['other_votes']}")
    print(f"  Total votes: {ellis_2018_senate['total_votes']}")
    print(f"  Two-party total: {ellis_2018_senate['two_party_total']}")
    print(f"  Margin: {ellis_2018_senate['margin']}")
    print(f"  Margin %: {ellis_2018_senate['margin_pct']}")
    print(f"  Winner: {ellis_2018_senate['winner']}")
    print(f"  Competitiveness: {ellis_2018_senate['competitiveness']['description']}")
except Exception as e:
    print(f"  Error: {e}")

# Check 2018 Governor
print("\n2018 Governor - Ellis County:")
try:
    ellis_2018_gov = data['results_by_year']['2018']['statewide']['governor']['results']['ELLIS']
    print(f"  DEM votes: {ellis_2018_gov['dem_votes']}")
    print(f"  REP votes: {ellis_2018_gov['rep_votes']}")
    print(f"  Other votes: {ellis_2018_gov['other_votes']}")
    print(f"  Total votes: {ellis_2018_gov['total_votes']}")
    print(f"  Margin: {ellis_2018_gov['margin']}")
    print(f"  Winner: {ellis_2018_gov['winner']}")
except Exception as e:
    print(f"  Error: {e}")

# Check 2014 U.S. Senate
print("\n2014 U.S. Senate - Ellis County:")
try:
    ellis_2014_senate = data['results_by_year']['2014']['us_senate']['us_senate']['results']['ELLIS']
    print(f"  DEM votes: {ellis_2014_senate['dem_votes']}")
    print(f"  REP votes: {ellis_2014_senate['rep_votes']}")
    print(f"  Other votes: {ellis_2014_senate['other_votes']}")
    print(f"  Total votes: {ellis_2014_senate['total_votes']}")
    print(f"  Margin: {ellis_2014_senate['margin']}")
    print(f"  Winner: {ellis_2014_senate['winner']}")
except Exception as e:
    print(f"  Error: {e}")

# Check 2014 Governor
print("\n2014 Governor - Ellis County:")
try:
    ellis_2014_gov = data['results_by_year']['2014']['statewide']['governor']['results']['ELLIS']
    print(f"  DEM votes: {ellis_2014_gov['dem_votes']}")
    print(f"  REP votes: {ellis_2014_gov['rep_votes']}")
    print(f"  Other votes: {ellis_2014_gov['other_votes']}")
    print(f"  Total votes: {ellis_2014_gov['total_votes']}")
    print(f"  Margin: {ellis_2014_gov['margin']}")
    print(f"  Winner: {ellis_2014_gov['winner']}")
except Exception as e:
    print(f"  Error: {e}")

# Compare with expected 2018 values from VTD CSV
print("\n" + "=" * 60)
print("EXPECTED VALUES FROM VTD CSV (2018):")
print("=" * 60)
print("U.S. Senate: DEM 19106, REP 41022, Other 461")
print("Governor: Expected values TBD")

print("\nChecking if values match VTD aggregation...")
