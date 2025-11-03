import json

data = json.load(open('data/texas_election_results.json'))

# Presidential
pres = data['results_by_year']['2024']['presidential']['president']
pres_total = 0
harris_total = 0
trump_total = 0

for county, results in pres['results'].items():
    pres_total += results['total_votes']
    harris_total += results['dem_votes']
    trump_total += results['rep_votes']

print('2024 PRESIDENTIAL:')
print(f'  Total votes: {pres_total:,}')
print(f'  Harris (D): {harris_total:,} ({harris_total/pres_total*100:.2f}%)')
print(f'  Trump (R): {trump_total:,} ({trump_total/pres_total*100:.2f}%)')
print(f'  Other: {pres_total - harris_total - trump_total:,}')
print(f'  Margin: Trump +{trump_total - harris_total:,} ({(trump_total - harris_total)/pres_total*100:.2f}%)')

# Senate
senate = data['results_by_year']['2024']['us_senate']['us_senate']
senate_total = 0
allred_total = 0
cruz_total = 0

for county, results in senate['results'].items():
    senate_total += results['total_votes']
    allred_total += results['dem_votes']
    cruz_total += results['rep_votes']

print('\n2024 U.S. SENATE:')
print(f'  Total votes: {senate_total:,}')
print(f'  Allred (D): {allred_total:,} ({allred_total/senate_total*100:.2f}%)')
print(f'  Cruz (R): {cruz_total:,} ({cruz_total/senate_total*100:.2f}%)')
print(f'  Other: {senate_total - allred_total - cruz_total:,}')
print(f'  Margin: Cruz +{cruz_total - allred_total:,} ({(cruz_total - allred_total)/senate_total*100:.2f}%)')

print('\n' + '='*60)
print('OFFICIAL RESULTS (from Texas SOS):')
print('Presidential: ~11.4M votes, Trump 56.3%, Harris 42.4%')
print('Senate: ~11.3M votes, Cruz 53.1%, Allred 44.5%')
