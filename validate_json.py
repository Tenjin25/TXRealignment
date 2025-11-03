import json

# Validate JSON
with open('data/texas_election_results.json') as f:
    data = json.load(f)

print('✅ JSON is valid!')
print(f'Years: {len(data["results_by_year"])}')
print(f'Total contests: {sum(len(y) for y in data["results_by_year"].values())}')

# Check for NaN values
print('\nChecking for NaN values...')
json_str = json.dumps(data)
if 'NaN' in json_str:
    print('❌ Found NaN in JSON!')
else:
    print('✅ No NaN values found!')
