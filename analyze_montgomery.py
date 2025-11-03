import json

# Load the data
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

def calculate_margin(dem_votes, rep_votes):
    """Calculate margin percentage (positive = Dem, negative = Rep)"""
    total = dem_votes + rep_votes
    if total == 0:
        return 0
    return ((dem_votes - rep_votes) / total) * 100

print("=" * 80)
print("MONTGOMERY COUNTY ANALYSIS - Presidential Elections")
print("=" * 80)

years = [2000, 2004, 2008, 2012, 2016, 2020, 2024]

for year in years:
    if str(year) in data['results_by_year']:
        year_data = data['results_by_year'][str(year)]
        if 'presidential' in year_data and 'president' in year_data['presidential']:
            pres = year_data['presidential']['president']
            
            if 'MONTGOMERY' in pres['results']:
                county_data = pres['results']['MONTGOMERY']
                dem = county_data.get('dem_votes', 0)
                rep = county_data.get('rep_votes', 0)
                margin = calculate_margin(dem, rep)
                total = dem + rep
                
                print(f"\n{year}: {pres.get('dem_candidate', 'Unknown')} vs {pres.get('rep_candidate', 'Unknown')}")
                print(f"  Margin: R+{abs(margin):.2f}%")
                print(f"  Total votes: {total:,}")
                print(f"  Dem: {dem:,} ({(dem/total)*100:.1f}%) | Rep: {rep:,} ({(rep/total)*100:.1f}%)")

# Compare with similar growth counties
print("\n" + "=" * 80)
print("COMPARISON: Fast-Growing Suburban Counties (2024)")
print("=" * 80)

growth_counties = ['MONTGOMERY', 'COLLIN', 'DENTON', 'WILLIAMSON', 'FORT BEND', 'HAYS']

y2024 = data['results_by_year']['2024']['presidential']['president']
y2000 = data['results_by_year']['2000']['presidential']['president']

results = []
for county in growth_counties:
    if county in y2024['results'] and county in y2000['results']:
        # 2024
        dem_24 = y2024['results'][county].get('dem_votes', 0)
        rep_24 = y2024['results'][county].get('rep_votes', 0)
        margin_24 = calculate_margin(dem_24, rep_24)
        total_24 = dem_24 + rep_24
        
        # 2000
        dem_00 = y2000['results'][county].get('dem_votes', 0)
        rep_00 = y2000['results'][county].get('rep_votes', 0)
        margin_00 = calculate_margin(dem_00, rep_00)
        total_00 = dem_00 + rep_00
        
        growth = ((total_24 - total_00) / total_00) * 100
        swing = margin_24 - margin_00
        
        results.append({
            'county': county,
            'margin_2000': margin_00,
            'margin_2024': margin_24,
            'swing': swing,
            'growth': growth,
            'total_2024': total_24
        })

results.sort(key=lambda x: x['growth'], reverse=True)

for r in results:
    party_00 = 'D' if r['margin_2000'] > 0 else 'R'
    party_24 = 'D' if r['margin_2024'] > 0 else 'R'
    swing_direction = 'more Democratic' if r['swing'] > 0 else 'more Republican'
    
    print(f"\n{r['county']} County:")
    print(f"  2000: {party_00}+{abs(r['margin_2000']):.1f}% → 2024: {party_24}+{abs(r['margin_2024']):.1f}%")
    print(f"  Swing: {abs(r['swing']):.1f} points {swing_direction}")
    print(f"  Growth: {r['growth']:.0f}% increase in turnout")
    print(f"  2024 Total: {r['total_2024']:,} votes")
