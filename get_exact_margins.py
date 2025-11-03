import json

# Load the data
with open('data/texas_election_results.json', 'r') as f:
    data = json.load(f)

def get_margin(county, year):
    """Get exact margin for a county in a specific year"""
    try:
        pres = data['results_by_year'][str(year)]['presidential']['president']
        if county in pres['results']:
            dem = pres['results'][county].get('dem_votes', 0)
            rep = pres['results'][county].get('rep_votes', 0)
            total = dem + rep
            if total == 0:
                return 0
            margin = ((dem - rep) / total) * 100
            return margin
    except:
        return None

# Counties to check with their years
counties_to_check = {
    'MONTGOMERY': [2000, 2024],
    'WILLIAMSON': [2000, 2024],
    'COLLIN': [2000, 2024],
    'FORT BEND': [2000, 2024],
    'TARRANT': [2000, 2024],
    'DENTON': [2024],
    'STARR': [2000, 2012, 2020, 2024],
    'TRAVIS': [2000, 2008, 2024],
    'DALLAS': [2024],
    'HARRIS': [2024],
    'BEXAR': [2024],
    'EL PASO': [2024],
    'HAYS': [2024],
    'WEBB': [2024],
    'HIDALGO': [2024],
    'CAMERON': [2024]
}

print("EXACT COUNTY MARGINS")
print("=" * 60)

for county, years in sorted(counties_to_check.items()):
    print(f"\n{county} County:")
    for year in years:
        margin = get_margin(county, year)
        if margin is not None:
            party = 'D' if margin > 0 else 'R'
            print(f"  {year}: {party}+{abs(margin):.2f}%")
