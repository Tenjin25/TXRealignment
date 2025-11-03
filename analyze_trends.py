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

def analyze_presidential_trends():
    """Analyze presidential race trends from 2000-2024"""
    print("=" * 80)
    print("PRESIDENTIAL RACE ANALYSIS (2000-2024)")
    print("=" * 80)
    
    years = [2000, 2004, 2008, 2012, 2016, 2020, 2024]
    statewide_margins = {}
    
    for year in years:
        if str(year) in data['results_by_year']:
            year_data = data['results_by_year'][str(year)]
            if 'presidential' in year_data and 'president' in year_data['presidential']:
                pres = year_data['presidential']['president']
                
                total_dem = 0
                total_rep = 0
                
                for county, results in pres['results'].items():
                    total_dem += results.get('dem_votes', 0)
                    total_rep += results.get('rep_votes', 0)
                
                margin = calculate_margin(total_dem, total_rep)
                statewide_margins[year] = margin
                
                print(f"\n{year}: {pres.get('dem_candidate', 'Unknown')} vs {pres.get('rep_candidate', 'Unknown')}")
                print(f"  Democratic votes: {total_dem:,}")
                print(f"  Republican votes: {total_rep:,}")
                print(f"  Margin: R+{abs(margin):.2f}%")
    
    # Calculate shift
    if 2000 in statewide_margins and 2024 in statewide_margins:
        shift = statewide_margins[2024] - statewide_margins[2000]
        print(f"\n24-Year Shift (2000-2024): {abs(shift):.2f} points more Republican")

def find_swing_counties():
    """Find counties with biggest swings between 2000 and 2024"""
    print("\n" + "=" * 80)
    print("TOP 10 COUNTIES BY SWING (2000 → 2024 Presidential)")
    print("=" * 80)
    
    y2000 = data['results_by_year']['2000']['presidential']['president']
    y2024 = data['results_by_year']['2024']['presidential']['president']
    
    swings = []
    
    for county in y2000['results'].keys():
        if county in y2024['results']:
            # 2000 margin
            dem_2000 = y2000['results'][county].get('dem_votes', 0)
            rep_2000 = y2000['results'][county].get('rep_votes', 0)
            margin_2000 = calculate_margin(dem_2000, rep_2000)
            
            # 2024 margin
            dem_2024 = y2024['results'][county].get('dem_votes', 0)
            rep_2024 = y2024['results'][county].get('rep_votes', 0)
            margin_2024 = calculate_margin(dem_2024, rep_2024)
            
            swing = margin_2024 - margin_2000
            
            swings.append({
                'county': county,
                'margin_2000': margin_2000,
                'margin_2024': margin_2024,
                'swing': swing
            })
    
    # Sort by absolute swing
    swings.sort(key=lambda x: abs(x['swing']), reverse=True)
    
    print("\nMost Republican Shift:")
    for i, county_data in enumerate(swings[:10]):
        if county_data['swing'] < 0:  # More Republican
            print(f"{i+1}. {county_data['county']}")
            print(f"   2000: {'D' if county_data['margin_2000'] > 0 else 'R'}+{abs(county_data['margin_2000']):.1f}% → "
                  f"2024: {'D' if county_data['margin_2024'] > 0 else 'R'}+{abs(county_data['margin_2024']):.1f}%")
            print(f"   Shift: {abs(county_data['swing']):.1f} points more Republican")
    
    print("\nMost Democratic Shift:")
    dem_shifts = [c for c in swings if c['swing'] > 0]
    dem_shifts.sort(key=lambda x: x['swing'], reverse=True)
    for i, county_data in enumerate(dem_shifts[:10]):
        print(f"{i+1}. {county_data['county']}")
        print(f"   2000: {'D' if county_data['margin_2000'] > 0 else 'R'}+{abs(county_data['margin_2000']):.1f}% → "
              f"2024: {'D' if county_data['margin_2024'] > 0 else 'R'}+{abs(county_data['margin_2024']):.1f}%")
        print(f"   Shift: {abs(county_data['swing']):.1f} points more Democratic")

def analyze_major_metros():
    """Analyze major metropolitan counties"""
    print("\n" + "=" * 80)
    print("MAJOR METRO COUNTIES - 2024 PRESIDENTIAL")
    print("=" * 80)
    
    metros = {
        'HARRIS': 'Houston',
        'DALLAS': 'Dallas',
        'TARRANT': 'Fort Worth',
        'BEXAR': 'San Antonio',
        'TRAVIS': 'Austin',
        'COLLIN': 'Plano/Frisco',
        'DENTON': 'Denton',
        'EL PASO': 'El Paso',
        'HIDALGO': 'McAllen',
        'FORT BEND': 'Sugar Land'
    }
    
    y2024 = data['results_by_year']['2024']['presidential']['president']
    
    results = []
    for county, city in metros.items():
        if county in y2024['results']:
            dem = y2024['results'][county].get('dem_votes', 0)
            rep = y2024['results'][county].get('rep_votes', 0)
            margin = calculate_margin(dem, rep)
            total = dem + rep
            results.append({
                'county': county,
                'city': city,
                'margin': margin,
                'total': total,
                'dem': dem,
                'rep': rep
            })
    
    results.sort(key=lambda x: x['margin'], reverse=True)
    
    for r in results:
        party = 'D' if r['margin'] > 0 else 'R'
        print(f"\n{r['county']} County ({r['city']})")
        print(f"  {party}+{abs(r['margin']):.2f}%")
        print(f"  Total votes: {r['total']:,}")
        print(f"  Harris: {r['dem']:,} | Trump: {r['rep']:,}")

def analyze_border_counties():
    """Analyze South Texas border counties"""
    print("\n" + "=" * 80)
    print("SOUTH TEXAS BORDER COUNTIES - PRESIDENTIAL MARGINS")
    print("=" * 80)
    
    border = ['CAMERON', 'HIDALGO', 'STARR', 'WEBB', 'ZAPATA', 'MAVERICK', 'VAL VERDE']
    
    years = [2000, 2012, 2016, 2020, 2024]
    
    for county in border:
        print(f"\n{county} County:")
        for year in years:
            if str(year) in data['results_by_year']:
                year_data = data['results_by_year'][str(year)]
                if 'presidential' in year_data and 'president' in year_data['presidential']:
                    pres = year_data['presidential']['president']
                    if county in pres['results']:
                        dem = pres['results'][county].get('dem_votes', 0)
                        rep = pres['results'][county].get('rep_votes', 0)
                        margin = calculate_margin(dem, rep)
                        party = 'D' if margin > 0 else 'R'
                        print(f"  {year}: {party}+{abs(margin):.1f}%")

def analyze_competitive_counties():
    """Find most competitive counties in 2024"""
    print("\n" + "=" * 80)
    print("MOST COMPETITIVE COUNTIES - 2024 PRESIDENTIAL")
    print("=" * 80)
    
    y2024 = data['results_by_year']['2024']['presidential']['president']
    
    competitive = []
    for county, results in y2024['results'].items():
        dem = results.get('dem_votes', 0)
        rep = results.get('rep_votes', 0)
        margin = calculate_margin(dem, rep)
        total = dem + rep
        
        if total > 1000:  # Filter out very small counties
            competitive.append({
                'county': county,
                'margin': abs(margin),
                'actual_margin': margin,
                'total': total
            })
    
    competitive.sort(key=lambda x: x['margin'])
    
    print("\nClosest 15 Counties:")
    for i, c in enumerate(competitive[:15]):
        party = 'D' if c['actual_margin'] > 0 else 'R'
        print(f"{i+1}. {c['county']}: {party}+{c['margin']:.2f}% ({c['total']:,} votes)")

if __name__ == '__main__':
    analyze_presidential_trends()
    find_swing_counties()
    analyze_major_metros()
    analyze_border_counties()
    analyze_competitive_counties()
