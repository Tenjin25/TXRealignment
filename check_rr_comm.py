import json

# Load the JSON file
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("RAILROAD COMMISSIONER RACES BY YEAR")
print("=" * 80)
print("\nTexas Railroad Commission has 3 members with 6-year staggered terms")
print("This means elections occur every 2 years for different seats\n")

for year in sorted(data['results_by_year'].keys()):
    year_data = data['results_by_year'][year]
    
    if 'statewide' in year_data:
        rr_races = []
        for contest_key, contest_data in year_data['statewide'].items():
            contest_name = contest_data.get('contest_name', '')
            if 'Railroad' in contest_name or 'RR Comm' in contest_name:
                rr_races.append(contest_name)
        
        if rr_races:
            print(f"{year}: {', '.join(rr_races)}")
    
    # Check presidential/off-years without RR races
    if int(year) in [2004, 2008, 2016, 2020, 2024]:
        if 'statewide' not in year_data or not any('Railroad' in c.get('contest_name', '') for c in year_data.get('statewide', {}).values()):
            # These years SHOULD have RR Commissioner
            expected_rr = {
                2004: "Likely missing - should have RR Comm election",
                2008: "Likely missing - should have RR Comm election", 
                2016: "Likely missing - should have RR Comm election",
                2020: "Has RR Comm in judicial? Check...",
                2024: "Has RR Comm in judicial? Check..."
            }
            if int(year) in expected_rr:
                # Check if it's in judicial by mistake
                has_in_judicial = False
                if 'judicial' in year_data:
                    for contest_data in year_data['judicial'].values():
                        if 'Railroad' in contest_data.get('contest_name', ''):
                            has_in_judicial = True
                            break
                
                if not has_in_judicial:
                    print(f"{year}: ⚠️  {expected_rr[int(year)]}")

print("\n" + "=" * 80)
print("Expected Railroad Commissioner Election Years:")
print("=" * 80)
print("Seat 1: 2000, 2006, 2012, 2018, 2024")
print("Seat 2: 2002, 2008, 2014, 2020")  
print("Seat 3: 2004, 2010, 2016, 2022")
print("\n(Note: Some years may have special/unexpired term elections)")
