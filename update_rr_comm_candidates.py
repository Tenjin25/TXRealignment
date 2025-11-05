import json
import os

# Path to the main JSON file
json_path = "texas_election_results.json"

# Load the JSON data
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

updated = False

# Update 2020 Railroad Commissioner candidate names
try:
    rr_comm = data["results_by_year"]["2020"]["statewide"]["railroad_commissioner"]
    # Update dem_candidate
    if rr_comm.get("dem_candidate") == "Castaneda":
        rr_comm["dem_candidate"] = "Chrysta Castaneda"
        updated = True
    # Update rep_candidate
    if rr_comm.get("rep_candidate") == "Wright":
        rr_comm["rep_candidate"] = "Jim Wright"
        updated = True
except Exception as e:
    print(f"Error updating candidate names: {e}")

if updated:
    # Write the updated JSON back to file
    backup_path = json_path + ".bak"
    os.rename(json_path, backup_path)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Candidate names updated. Backup created as", backup_path)
else:
    print("No candidate names updated. Check if values already correct.")
