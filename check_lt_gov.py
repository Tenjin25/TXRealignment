import json

with open('data/texas_election_results.json') as f:
    data = json.load(f)

print("2006 statewide contests:")
y2006 = data['results_by_year']['2006']['statewide']
for key in y2006.keys():
    contest = y2006[key]
    print(f"  {key}: {contest.get('contest_name')}")

print("\n2010 statewide contests:")
y2010 = data['results_by_year']['2010']['statewide']
for key in y2010.keys():
    contest = y2010[key]
    print(f"  {key}: {contest.get('contest_name')}")
