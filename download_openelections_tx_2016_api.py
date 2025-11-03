import os
import requests

API_URL = "https://api.github.com/repos/openelections/openelections-data-tx/contents/2016/counties"
RAW_BASE = "https://raw.githubusercontent.com/openelections/openelections-data-tx/master/2016/counties/"
DOWNLOAD_DIR = "openelections_tx_2016"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

response = requests.get(API_URL)
if response.status_code != 200:
    print(f"GitHub API error: {response.status_code}")
    exit(1)

files = response.json()
csv_files = [f['name'] for f in files if f['name'].endswith('.csv')]
print(f"Found {len(csv_files)} CSV files.")

for filename in csv_files:
    raw_url = RAW_BASE + filename
    print(f"Downloading {raw_url} ...")
    r = requests.get(raw_url)
    local_path = os.path.join(DOWNLOAD_DIR, filename)
    with open(local_path, 'wb') as f:
        f.write(r.content)
    print(f"Saved to {local_path}")

print("All county CSVs downloaded.")
