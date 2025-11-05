import json

main_path = "data/texas_election_results.json"
cca_path = "cca_2014_2018.json"
out_path = "data/texas_election_results_merged.json"

with open(main_path, "r", encoding="utf-8") as f:
    main_data = json.load(f)
with open(cca_path, "r", encoding="utf-8") as f:
    cca_data = json.load(f)

for year in cca_data:
    if year in main_data.get("results_by_year", {}):
        judicial = main_data["results_by_year"][year].setdefault("judicial", {})
        for contest_key, contest_val in cca_data[year]["judicial"].items():
            judicial[contest_key] = contest_val

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(main_data, f, indent=2)

print(f"Merged CCA results for 2014 and 2018 into {out_path}")
