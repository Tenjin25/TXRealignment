import os
import requests
from bs4 import BeautifulSoup

GITHUB_URL = "https://github.com/openelections/openelections-data-tx/tree/master/2016/counties"
RAW_BASE = "https://raw.githubusercontent.com/openelections/openelections-data-tx/master/2016/counties/"
DOWNLOAD_DIR = "openelections_tx_2016"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Scrape the GitHub page for CSV file names
response = requests.get(GITHUB_URL)
soup = BeautifulSoup(response.text, "html.parser")

csv_files = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if href.endswith('.csv') and '/blob/' in href:
        filename = href.split('/')[-1]
        csv_files.append(filename)

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
