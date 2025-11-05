import json

# Load the JSON file
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

# Expected statewide races for Texas
expected_races = {
    'presidential': ['President'],
    'us_senate': ['U.S. Senate'],
    'statewide': [
        'Governor',
        'Lieutenant Governor', 
        'Attorney General',
        'Comptroller',
        'Land Commissioner',
        'Agriculture Commissioner',
        'Railroad Commissioner'
    ]
}

print("=" * 80)
print("TEXAS STATEWIDE RACES COVERAGE CHECK")
print("=" * 80)

# Check each year
for year in sorted(data['results_by_year'].keys()):
    print(f"\n{year}:")
    print("-" * 80)
    
    year_data = data['results_by_year'][year]
    
    # Check Presidential (every 4 years)
    if int(year) % 4 == 0:
        if 'presidential' in year_data:
            print("  ✅ Presidential: President")
        else:
            print("  ❌ MISSING: Presidential")
    
    # Check U.S. Senate (2000, 2002, 2006, 2008, 2012, 2014, 2018, 2020, 2024)
    senate_years = [2000, 2002, 2006, 2008, 2012, 2014, 2018, 2020, 2024]
    if int(year) in senate_years:
        if 'us_senate' in year_data:
            print("  ✅ U.S. Senate")
        else:
            print("  ❌ MISSING: U.S. Senate")
    
    # Check Statewide (Gubernatorial years: 2002, 2006, 2010, 2014, 2018, 2022)
    gubernatorial_years = [2002, 2006, 2010, 2014, 2018, 2022]
    if int(year) in gubernatorial_years:
        if 'statewide' in year_data:
            print("  ✅ Statewide Offices:")
            for contest_key, contest_data in year_data['statewide'].items():
                contest_name = contest_data.get('contest_name', contest_key)
                print(f"      - {contest_name}")
            
            # Check for missing statewide offices
            found_races = [contest_data.get('contest_name', '') for contest_data in year_data['statewide'].values()]
            missing = []
            for expected in expected_races['statewide']:
                if expected not in found_races:
                    # Handle variations
                    variations = {
                        'Comptroller': ['Comptroller of Public Accounts', 'Comptroller'],
                        'Land Commissioner': ['Commissioner of the General Land Office', 'Land Commissioner'],
                        'Agriculture Commissioner': ['Commissioner of Agriculture', 'Agriculture Commissioner']
                    }
                    found = False
                    for var in variations.get(expected, [expected]):
                        if var in found_races:
                            found = True
                            break
                    if not found:
                        missing.append(expected)
            
            if missing:
                print(f"      ❌ MISSING: {', '.join(missing)}")
        else:
            print("  ❌ MISSING: All Statewide Offices")
    
    # Check off-year Railroad Commissioner races
    # RR Comm runs every 2 years, so should appear in all even years
    if int(year) % 2 == 0:
        has_rr = False
        if 'statewide' in year_data:
            for contest_data in year_data['statewide'].values():
                if 'Railroad' in contest_data.get('contest_name', ''):
                    has_rr = True
                    break
        if not has_rr:
            print("  ⚠️  NOTE: No Railroad Commissioner race found (check if one occurred)")
    
    # Show judicial races count
    if 'judicial' in year_data:
        judicial_count = len(year_data['judicial'])
        print(f"  📊 Judicial: {judicial_count} races")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("\nTexas Statewide Elections Schedule:")
print("  • Presidential: Every 4 years (2000, 2004, 2008, 2012, 2016, 2020, 2024)")
print("  • U.S. Senate: Class I (2000, 2006, 2012, 2018, 2024)")
print("  • U.S. Senate: Class II (2002, 2008, 2014, 2020)")
print("  • Governor + 6 other statewide: Every 4 years (2002, 2006, 2010, 2014, 2018, 2022)")
print("  • Railroad Commissioner: Every 6 years (staggered - 3 seats)")
print("  • Supreme Court & CCA: Various elections each cycle")
