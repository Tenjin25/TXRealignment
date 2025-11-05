import json

backup_path = "BackupData/texas_election_results_last.json"
output = {}

with open(backup_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for year in ["2014", "2018"]:
    year_data = data.get("results_by_year", {}).get(year, {})
    judicial = year_data.get("judicial", {})
    for contest_key in ["cca_judge", "cca_presiding_judge"]:
        contest = judicial.get(contest_key)
        if contest:
            # Exclude Ellis County from results if present
            results = contest.get("results", {})
            filtered_results = {k: v for k, v in results.items() if k.upper() != "ELLIS"}
            # Prepare output structure
            if year not in output:
                output[year] = {}
            if "judicial" not in output[year]:
                output[year]["judicial"] = {}
            output[year]["judicial"][contest_key] = dict(contest)
            output[year]["judicial"][contest_key]["results"] = filtered_results

# Print the output JSON structure for review or insertion
print(json.dumps(output, indent=2))
