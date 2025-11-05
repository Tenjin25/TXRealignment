import json

# Load the JSON file
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("COMPREHENSIVE STATEWIDE RACE AUDIT")
print("=" * 80)

# Track all unique statewide office types we have
all_statewide = set()
all_judicial = set()

for year in sorted(data['results_by_year'].keys()):
    year_data = data['results_by_year'][year]
    
    if 'presidential' in year_data:
        all_statewide.add('President')
    
    if 'us_senate' in year_data:
        all_statewide.add('U.S. Senate')
    
    if 'statewide' in year_data:
        for contest_data in year_data['statewide'].values():
            all_statewide.add(contest_data.get('contest_name', 'Unknown'))
    
    if 'judicial' in year_data:
        for contest_data in year_data['judicial'].values():
            contest_name = contest_data.get('contest_name', 'Unknown')
            # Normalize judicial names to see patterns
            if 'Supreme Court' in contest_name:
                if 'Chief' in contest_name:
                    all_judicial.add('Chief Justice, Supreme Court')
                else:
                    all_judicial.add('Justice, Supreme Court (various places)')
            elif 'Criminal Appeals' in contest_name or 'CCA' in contest_name:
                if 'Presiding' in contest_name:
                    all_judicial.add('Presiding Judge, CCA')
                else:
                    all_judicial.add('Judge, CCA (various places)')

print("\nSTATEWIDE ELECTED OFFICES FOUND:")
print("-" * 80)
for office in sorted(all_statewide):
    print(f"  ✅ {office}")

print("\nJUDICIAL OFFICES FOUND:")
print("-" * 80)
for office in sorted(all_judicial):
    print(f"  ⚖️  {office}")

print("\n" + "=" * 80)
print("KNOWN STATEWIDE ELECTED OFFICES IN TEXAS:")
print("=" * 80)
print("""
Executive Branch (elected):
  ✅ Governor
  ✅ Lieutenant Governor
  ✅ Attorney General
  ✅ Comptroller of Public Accounts
  ✅ Commissioner of the General Land Office
  ✅ Commissioner of Agriculture
  ✅ Railroad Commissioner (3 seats, staggered)

Federal:
  ✅ President
  ✅ U.S. Senate (2 seats, Class I and Class II)

Judicial (statewide elected):
  ⚖️  Texas Supreme Court (9 justices, staggered terms)
     - 1 Chief Justice
     - 8 Associate Justices (Places 2-9)
  ⚖️  Texas Court of Criminal Appeals (9 judges, staggered terms)
     - 1 Presiding Judge
     - 8 Judges (Places 2-9)

NOT statewide elected (so we should NOT have them):
  ❌ Secretary of State (appointed by Governor)
  ❌ State Board of Education (15 districts, not statewide)
  ❌ State House Representatives (150 districts)
  ❌ State Senate (31 districts)
""")

# Check for any unexpected categories
print("=" * 80)
print("CHECKING FOR UNEXPECTED DATA:")
print("=" * 80)
for year in sorted(data['results_by_year'].keys()):
    year_data = data['results_by_year'][year]
    expected_cats = {'presidential', 'us_senate', 'statewide', 'judicial'}
    actual_cats = set(year_data.keys())
    unexpected = actual_cats - expected_cats
    if unexpected:
        print(f"\n{year}: Unexpected categories: {unexpected}")
        for cat in unexpected:
            print(f"  Contents of '{cat}':")
            for key in year_data[cat].keys():
                print(f"    - {key}")
