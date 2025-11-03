import json

# Load the data
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

print("Comparing actual vs expected vote totals:")
print("=" * 100)

expected = {
    '2000': 6_400_000,
    '2004': 7_400_000,
    '2008': 8_100_000,
    '2012': 7_900_000,
    '2016': 8_900_000,
    '2020': 11_300_000,
    '2024': 11_200_000
}

issues = []

for year in sorted(data['results_by_year'].keys()):
    year_data = data['results_by_year'][year]
    
    # Check Presidential
    if 'presidential' in year_data and 'president' in year_data['presidential']:
        pres = year_data['presidential']['president']
        if 'total_votes' in pres:
            actual = pres['total_votes']
            exp = expected.get(year, None)
            
            if exp:
                ratio = actual / exp
                status = "✓ OK" if 0.9 <= ratio <= 1.1 else "✗ ISSUE"
                
                print(f"\n{year} Presidential:")
                print(f"  Actual:   {actual:,}")
                print(f"  Expected: ~{exp:,}")
                print(f"  Ratio:    {ratio:.2f}x  {status}")
                
                if ratio > 1.5 or ratio < 0.5:
                    issues.append({
                        'year': year,
                        'contest': 'Presidential',
                        'actual': actual,
                        'expected': exp,
                        'ratio': ratio
                    })
    
    # Check US Senate
    if 'us_senate' in year_data and 'us_senate' in year_data['us_senate']:
        senate = year_data['us_senate']['us_senate']
        if 'total_votes' in senate:
            actual = senate['total_votes']
            exp = expected.get(year, None)
            
            if exp:
                # Senate typically gets similar turnout to presidential
                ratio = actual / exp
                
                # But not all years have Senate races that draw same turnout
                if year in ['2000', '2012', '2018']:  # High profile Senate races
                    status = "✓ OK" if 0.8 <= ratio <= 1.5 else "? CHECK"
                else:
                    status = "? (Special election or low turnout expected)"
                
                print(f"{year} US Senate:")
                print(f"  Actual:   {actual:,}")
                print(f"  Expected: ~{exp:,} (if similar turnout)")
                print(f"  Ratio:    {ratio:.2f}x  {status}")
                
                if ratio > 3.0:  # Clear overcounting
                    issues.append({
                        'year': year,
                        'contest': 'US Senate',
                        'actual': actual,
                        'expected': exp,
                        'ratio': ratio
                    })

print("\n" + "=" * 100)
print("\nSUMMARY OF ISSUES:")
for issue in issues:
    print(f"  {issue['year']} {issue['contest']}: {issue['ratio']:.2f}x overcounted ({issue['actual']:,} vs ~{issue['expected']:,})")
