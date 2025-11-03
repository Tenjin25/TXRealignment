import json

# Load the data
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("=" * 60)
print("FINAL VERIFICATION")
print("=" * 60)

# Check 2024 contests and candidates
print("\n=== 2024 CONTESTS & CANDIDATES ===")
y2024 = data['results_by_year']['2024']

print("\nPresidential:")
pres = y2024['presidential']['president']
print(f"  Contest Name: {pres['contest_name']}")
print(f"  Dem: {pres.get('dem_candidate', 'N/A')}")
print(f"  Rep: {pres.get('rep_candidate', 'N/A')}")

print("\nU.S. Senate:")
sen = y2024['us_senate']['us_senate']
print(f"  Contest Name: {sen['contest_name']}")
print(f"  Dem: {sen.get('dem_candidate', 'N/A')}")
print(f"  Rep: {sen.get('rep_candidate', 'N/A')}")

print("\nRailroad Commissioner:")
rr = y2024['statewide']['railroad_commissioner']
print(f"  Contest Name: {rr['contest_name']}")
print(f"  Dem: {rr.get('dem_candidate', 'N/A')}")
print(f"  Rep: {rr.get('rep_candidate', 'N/A')}")

# Check 2022 contests
print("\n=== 2022 CONTESTS ===")
y2022 = data['results_by_year']['2022']
print("\nStatewide contests:")
for key, contest in y2022['statewide'].items():
    print(f"  {key}: {contest['contest_name']}")

# Check county count for 2024
print("\n=== 2024 COUNTY COUNT ===")
county_count = len(pres['results'])
print(f"Total counties: {county_count} (should be 254)")

# Check multi-word counties
print("\n=== MULTI-WORD COUNTIES ===")
counties = list(pres['results'].keys())
multi_word = [c for c in counties if ' ' in c]
print(f"Found {len(multi_word)} multi-word counties:")
for c in sorted(multi_word):
    print(f"  {c}")

# Verify La Salle specifically
if 'LA SALLE' in counties:
    print("\n✅ LA SALLE county found (correctly formatted with space)")
else:
    print("\n❌ LA SALLE county NOT found")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
