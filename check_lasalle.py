import json

data = json.load(open('data/texas_election_results.json'))['results_by_year']
years = [2000, 2004, 2008, 2012, 2016, 2020, 2024]

print('La Salle County Presidential Data:\n')
for year in years:
    pres = data[str(year)]['presidential']['president']['results']
    lasalle = pres.get('LA SALLE')
    if lasalle:
        print(f'{year}: DEM={lasalle["dem_votes"]}, REP={lasalle["rep_votes"]}, Total={lasalle["total_votes"]}')
    else:
        # Check if it exists under LASALLE (without space)
        lasalle_no_space = pres.get('LASALLE')
        if lasalle_no_space:
            print(f'{year}: FOUND AS "LASALLE" (NO SPACE) - DEM={lasalle_no_space["dem_votes"]}, REP={lasalle_no_space["rep_votes"]}')
        else:
            print(f'{year}: NOT FOUND')

print('\nChecking all multi-word counties for 2024:')
multi_word = ['LA SALLE', 'DE WITT', 'DEAF SMITH', 'EL PASO', 'FORT BEND', 'JEFF DAVIS', 
              'JIM HOGG', 'JIM WELLS', 'LIVE OAK', 'PALO PINTO', 'RED RIVER', 
              'SAN AUGUSTINE', 'SAN JACINTO', 'SAN PATRICIO', 'SAN SABA', 
              'TOM GREEN', 'VAL VERDE', 'VAN ZANDT']

pres_2024 = data['2024']['presidential']['president']['results']
missing = []
for county in multi_word:
    if county not in pres_2024:
        missing.append(county)

if missing:
    print(f'Missing counties: {missing}')
else:
    print('✅ All multi-word counties found!')
