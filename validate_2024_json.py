import json
from pathlib import Path

# Load the generated JSON
json_path = Path("data/texas_election_results.json")
with open(json_path, 'r') as f:
    data = json.load(f)

print("2024 Results Validation")
print("="*70)

year_2024 = data['results_by_year']['2024']

# Presidential
if 'presidential' in year_2024 and 'president' in year_2024['presidential']:
    pres = year_2024['presidential']['president']
    print(f"\nPresidential:")
    print(f"  Total votes: {pres['total_votes']:,}")
    print(f"  Dem candidate: {pres['dem_candidate']}")
    print(f"  Rep candidate: {pres['rep_candidate']}")
    print(f"  Other votes: {pres['other_votes']:,}")
    print(f"  Counties: {len(pres['results'])}")
    
    # Sample county
    if 'ANDERSON' in pres['results']:
        anderson = pres['results']['ANDERSON']
        print(f"\n  Sample - Anderson County:")
        print(f"    Dem: {anderson['dem_votes']:,}, Rep: {anderson['rep_votes']:,}, Other: {anderson['other_votes']:,}")
        print(f"    Total: {anderson['total_votes']:,}")

# U.S. Senate
if 'us_senate' in year_2024 and 'us_senate' in year_2024['us_senate']:
    senate = year_2024['us_senate']['us_senate']
    print(f"\nU.S. Senate:")
    print(f"  Total votes: {senate['total_votes']:,}")
    print(f"  Dem candidate: {senate['dem_candidate']}")
    print(f"  Rep candidate: {senate['rep_candidate']}")
    print(f"  Other votes: {senate['other_votes']:,}")
    print(f"  Counties: {len(senate['results'])}")
    
    # Sample county
    if 'ANDERSON' in senate['results']:
        anderson = senate['results']['ANDERSON']
        print(f"\n  Sample - Anderson County:")
        print(f"    Dem: {anderson['dem_votes']:,}, Rep: {anderson['rep_votes']:,}, Other: {anderson['other_votes']:,}")
        print(f"    Total: {anderson['total_votes']:,}")

print("\n" + "="*70)
print("Comparison with quick test:")
print("  Quick test Presidential total: 11,404,528")
print("  Quick test U.S. Senate total:  11,290,233")
print("\nNote: The JSON aggregation excludes some offices/counties, so totals may differ")
print("from the raw CSV sum. The important thing is internal consistency.")
