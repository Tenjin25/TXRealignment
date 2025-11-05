import json

with open('data/texas_election_results.json','r') as f:
    d=json.load(f)

s = d['results_by_year']['2018']['us_senate']['us_senate']
print('2018 U.S. Senate county checks:')
print('ELLIS: DEM', s['results']['ELLIS']['dem_votes'], 'REP', s['results']['ELLIS']['rep_votes'])
print('EL PASO: DEM', s['results']['EL PASO']['dem_votes'], 'REP', s['results']['EL PASO']['rep_votes'])
