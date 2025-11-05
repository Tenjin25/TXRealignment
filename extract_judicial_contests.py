import json

# Path to the backup file
backup_path = "BackupData/texas_election_results_last.json"

with open(backup_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for year, year_data in data.get("results_by_year", {}).items():
    judicial = year_data.get("judicial", {})
    for contest_key, contest in judicial.items():
        print(f"Year: {year}")
        print(f"Contest Key: {contest_key}")
        print(f"Contest Name: {contest.get('contest_name')}")
        print(f"Dem Candidate: {contest.get('dem_candidate')}")
        print(f"Rep Candidate: {contest.get('rep_candidate')}")
        print(f"Other Votes: {contest.get('other_votes')}")
        print(f"Total Votes: {contest.get('total_votes')}")
        print("-" * 40)
